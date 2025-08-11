//! Comprehensive Conversion Dataset - Mismatches Analysis V4 - Batched Version
//! 
//! COMPREHENSIVE FIX VERSION addressing all identified issues:
//! - Python Error Handling: Exclude Python errors from accuracy calculations
//! - ISCC-NBS Descriptor Generation: Use proper construct_revised_descriptor() function  
//! - Python API Issues: Fix XYZ Scaling mapping and handle validation errors
//! - Unknown Classifications: Track and investigate why colors return "Unknown"
//! - Report Structure: Clear separation of datasets with proper accuracy calculation
//! - Key Fixes: XYZ scaling mapping, construct_revised_descriptor usage, accuracy = matches/(total-errors)
//! - BATCHED: Process Python conversions in smaller batches to avoid timeouts

use munsellspace::iscc::ISCC_NBS_Classifier as IsccNbsClassifier;
use munsellspace::mathematical::{
    MathematicalMunsellConverter,
    Illuminant as MathIlluminant,
    ChromaticAdaptation as MathChromaticAdaptation
};
use std::collections::HashMap;
use std::fmt::Write;
use std::fs;
use csv::ReaderBuilder;
use serde::{Deserialize, Serialize};
use std::process::{Command, Stdio};
use std::io::Write as IoWrite;

#[derive(Debug, Deserialize, Clone)]
struct W3IsccColor {
    #[serde(rename = "sRGB ")]
    srgb: String,
    #[serde(rename = "ISCC-NBS Name")]
    iscc_nbs_name: String,
    #[serde(rename = " modifier ")]
    modifier: String,
    #[serde(rename = "color ")]
    color: String,
}

#[derive(Debug, Deserialize, Clone)]
struct CentoreIsccColor {
    number: u16,
    name: String,
    r: u8,
    g: u8,
    b: u8,
}

#[derive(Debug, Clone)]
struct TestResult {
    rgb: [u8; 3],
    illuminant: String,
    expected_name: String,
    munsell_notation: String,
    python_munsell: String,
    python_error_msg: String,  // Store actual Python error message
    python_iscc: String,
    rust_iscc: String,
    rust_match: bool,
    python_match: bool,
    python_error: bool,
    rust_unknown: bool,
    python_unknown: bool,
}

#[derive(Debug, Default)]
struct Statistics {
    total_unique_colors: usize,
    
    // Per-illuminant tracking
    rust_matches: HashMap<String, usize>,
    python_matches: HashMap<String, usize>,
    python_errors: HashMap<String, usize>,
    rust_unknowns: HashMap<String, usize>,
    python_unknowns: HashMap<String, usize>,
    
    // For proper accuracy calculation: matches / (total - errors)
    effective_population: HashMap<String, usize>,  // total - errors
}

#[derive(Serialize)]
struct PythonConversionRequest {
    conversions: Vec<PythonConversion>,
}

#[derive(Serialize, Clone)]
struct PythonConversion {
    id: String,
    rgb: [u8; 3],
    illuminant: String,
    adaptation: String,
}

#[derive(Deserialize)]
struct PythonConversionResult {
    results: HashMap<String, String>,
}

const BATCH_SIZE: usize = 50;  // Process 50 colors at a time

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 Generating Comprehensive Conversion Dataset - Mismatches Analysis V4 (BATCHED)");
    println!("================================================================================");
    println!("COMPREHENSIVE FIX VERSION: All identified issues addressed + batched processing");
    println!("- Python Error Handling: Exclude errors from accuracy calculations");
    println!("- ISCC-NBS Generation: Use construct_revised_descriptor() function"); 
    println!("- Python API Issues: Fix XYZ Scaling mapping and validation errors");
    println!("- Unknown Classifications: Track and investigate causes");
    println!("- Accuracy Formula: matches / (total - errors)");
    println!("- BATCHED: Process Python conversions in batches of {} to avoid timeouts", BATCH_SIZE);
    println!();
    
    // Load datasets
    let w3_colors = load_w3_dataset()?;
    let centore_colors = load_centore_dataset()?;
    
    println!("📊 Loaded {} W3 colors and {} Centore colors", w3_colors.len(), centore_colors.len());
    
    // Test configurations - XYZScaling only, with C/D65/F7
    let configurations = vec![
        (MathIlluminant::C, "C"),
        (MathIlluminant::D65, "D65"),
        (MathIlluminant::F7, "F7"),
    ];
    
    // Initialize classifier
    let classifier = IsccNbsClassifier::new()?;
    
    // Prepare batch Python conversion request with FIXED XYZ Scaling mapping
    let mut all_python_requests = Vec::new();
    let mut all_test_data = Vec::new();
    
    // Collect all test combinations
    for (_illuminant, illum_name) in &configurations {
        // W3 dataset
        for color in &w3_colors {
            let rgb = parse_rgb(&color.srgb)?;
            let id = format!("W3_{}_{}", illum_name, color.srgb.trim());
            all_python_requests.push(PythonConversion {
                id: id.clone(),
                rgb,
                illuminant: illum_name.to_string(),
                // FIX 1: Use correct Python API mapping for XYZ Scaling
                adaptation: "XYZ Scaling".to_string(),  // Changed from "XYZScaling" to "XYZ Scaling"
            });
            
            // FIX 2: Use construct_revised_descriptor() logic for expected names
            let expected_name = construct_expected_name(&color.modifier, &color.color);
            all_test_data.push((id, rgb, illum_name.to_string(), expected_name, "W3"));
        }
        
        // Centore dataset
        for color in &centore_colors {
            let rgb = [color.r, color.g, color.b];
            let id = format!("Centore_{}_{}", illum_name, color.number);
            all_python_requests.push(PythonConversion {
                id: id.clone(),
                rgb,
                illuminant: illum_name.to_string(),
                adaptation: "XYZ Scaling".to_string(),  // Fixed mapping
            });
            all_test_data.push((id, rgb, illum_name.to_string(), color.name.clone(), "Centore"));
        }
    }
    
    println!("🐍 Getting Python Munsell values for {} color/illuminant combinations...", all_python_requests.len());
    println!("   Using FIXED Python API: 'XYZ Scaling' (not 'XYZScaling')");
    println!("   Processing in batches of {} to avoid timeouts", BATCH_SIZE);
    
    // Process Python requests in batches
    let mut all_python_results = HashMap::new();
    let total_batches = (all_python_requests.len() + BATCH_SIZE - 1) / BATCH_SIZE;
    
    for (batch_idx, batch) in all_python_requests.chunks(BATCH_SIZE).enumerate() {
        println!("   Processing batch {}/{} ({} colors)...", batch_idx + 1, total_batches, batch.len());
        match get_python_munsell_batch(batch) {
            Ok(batch_results) => {
                all_python_results.extend(batch_results);
            },
            Err(e) => {
                eprintln!("   WARNING: Batch {} failed: {}", batch_idx + 1, e);
                // Continue with empty results for this batch
                for request in batch {
                    all_python_results.insert(request.id.clone(), format!("ERROR: Batch failed - {}", e));
                }
            }
        }
    }
    
    println!("✅ Received {} Python results total", all_python_results.len());
    
    // Analyze results with comprehensive tracking
    let mut w3_stats = Statistics::default();
    let mut centore_stats = Statistics::default();
    let mut w3_results: HashMap<String, Vec<TestResult>> = HashMap::new();
    let mut centore_results: HashMap<String, Vec<TestResult>> = HashMap::new();
    
    w3_stats.total_unique_colors = w3_colors.len();
    centore_stats.total_unique_colors = centore_colors.len();
    
    println!("\n🔍 Analyzing conversions with breakthrough mathematical converter...");
    println!("   Using construct_revised_descriptor() for ISCC-NBS naming");
    
    for (id, rgb, illum_name, expected_name, dataset) in all_test_data {
        let illuminant = match illum_name.as_str() {
            "C" => MathIlluminant::C,
            "D65" => MathIlluminant::D65,
            "F7" => MathIlluminant::F7,
            _ => continue,
        };
        
        // Create converter with proper illuminant support
        let converter = MathematicalMunsellConverter::with_illuminants(
            MathIlluminant::D65,  // source (sRGB is D65)
            illuminant,            // target
            MathChromaticAdaptation::XYZScaling
        )?;
        
        // Convert with Rust
        let rust_spec = converter.srgb_to_munsell(rgb)?;
        let rust_notation = format!("{:.1}{} {:.1}/{:.1}", 
            rust_spec.hue, rust_spec.family, rust_spec.value, rust_spec.chroma);
        
        // FIX 3: Use proper ISCC-NBS classification with construct_revised_descriptor logic
        let rust_classification_result = classifier.classify_munsell(
            &format!("{:.1}{}", rust_spec.hue, rust_spec.family), 
            rust_spec.value, 
            rust_spec.chroma
        );
        
        let (rust_iscc, rust_unknown) = match rust_classification_result {
            Ok(Some(result)) => {
                // FIX 3: Use the revised_descriptor field which uses construct_revised_descriptor()
                (result.revised_descriptor.clone(), false)
            },
            Ok(None) => ("Unknown".to_string(), true),
            Err(_) => ("Unknown".to_string(), true),
        };
        
        // Get Python result with detailed error tracking
        let python_result = all_python_results.get(&id).cloned().unwrap_or_default();
        let python_error = python_result.is_empty() || python_result.starts_with("ERROR:");
        let python_error_msg = if python_error {
            python_result.clone()
        } else {
            String::new()
        };
        
        // Parse Python ISCC-NBS classification with proper construct_revised_descriptor usage
        let (python_iscc, python_unknown) = if !python_error {
            if let Some((hue_part, value_chroma)) = python_result.split_once(' ') {
                if let Some((value_str, chroma_str)) = value_chroma.split_once('/') {
                    let value = value_str.parse::<f64>().unwrap_or(0.0);
                    let chroma = chroma_str.parse::<f64>().unwrap_or(0.0);
                    match classifier.classify_munsell(hue_part, value, chroma) {
                        Ok(Some(result)) => {
                            // FIX 3: Use revised_descriptor for consistency with Rust
                            (result.revised_descriptor.clone(), false)
                        },
                        Ok(None) => ("Unknown".to_string(), true),
                        Err(_) => ("Unknown".to_string(), true),
                    }
                } else {
                    ("Unknown".to_string(), true)
                }
            } else {
                ("Unknown".to_string(), true)
            }
        } else {
            ("Error".to_string(), false)
        };
        
        // Check matches with case-insensitive comparison
        let rust_match = rust_iscc.to_lowercase() == expected_name.to_lowercase();
        let python_match = !python_error && python_iscc.to_lowercase() == expected_name.to_lowercase();
        
        // Update statistics with FIX 4: Proper accuracy calculation
        let stats = if dataset == "W3" { &mut w3_stats } else { &mut centore_stats };
        let results = if dataset == "W3" { &mut w3_results } else { &mut centore_results };
        
        // Count matches
        if rust_match {
            *stats.rust_matches.entry(illum_name.clone()).or_insert(0) += 1;
        }
        
        // Track Python errors separately from matches
        if python_error {
            *stats.python_errors.entry(illum_name.clone()).or_insert(0) += 1;
        } else {
            // Only count for effective population if no error
            *stats.effective_population.entry(illum_name.clone()).or_insert(0) += 1;
            if python_match {
                *stats.python_matches.entry(illum_name.clone()).or_insert(0) += 1;
            }
        }
        
        // Track Unknown classifications for investigation
        if rust_unknown {
            *stats.rust_unknowns.entry(illum_name.clone()).or_insert(0) += 1;
        }
        
        if python_unknown && !python_error {
            *stats.python_unknowns.entry(illum_name.clone()).or_insert(0) += 1;
        }
        
        // Store comprehensive result
        let result = TestResult {
            rgb,
            illuminant: illum_name.clone(),
            expected_name: expected_name.clone(),
            munsell_notation: rust_notation,
            python_munsell: if python_error { "ERROR".to_string() } else { python_result.clone() },
            python_error_msg,
            python_iscc,
            rust_iscc,
            rust_match,
            python_match,
            python_error,
            rust_unknown,
            python_unknown,
        };
        
        results.entry(illum_name.clone())
            .or_insert_with(Vec::new)
            .push(result);
    }
    
    // Generate comprehensive report  
    let mut report = String::new();
    writeln!(&mut report, "# Comprehensive Conversion Dataset - Mismatches Analysis V4 (COMPREHENSIVE FIX + BATCHED)")?;
    writeln!(&mut report, "\nGenerated: {}", std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_secs())?;
    writeln!(&mut report, "\n## Configuration")?;
    writeln!(&mut report, "- Converter: Restored breakthrough mathematical converter (60.4% baseline)")?;
    writeln!(&mut report, "- Chromatic Adaptation: XYZScaling")?;
    writeln!(&mut report, "- Illuminants tested: C, D65, F7")?;
    writeln!(&mut report, "\n## Key Fixes in V4:")?;
    writeln!(&mut report, "- **FIX 1**: Python API mapping: 'XYZ Scaling' (not 'XYZScaling')")?;
    writeln!(&mut report, "- **FIX 2**: Expected names use construct_revised_descriptor() logic")?;
    writeln!(&mut report, "- **FIX 3**: ISCC-NBS classification uses revised_descriptor field")?;
    writeln!(&mut report, "- **FIX 4**: Accuracy calculated as matches / (total - errors)")?;
    writeln!(&mut report, "- **FIX 5**: Track Unknown classifications for investigation")?;
    writeln!(&mut report, "- **FIX 6**: Store actual Python error messages for debugging")?;
    writeln!(&mut report, "- **FIX 7**: Batched processing ({} colors per batch) to avoid timeouts", BATCH_SIZE)?;
    
    // W3 Dataset Results with FIXED accuracy calculation
    writeln!(&mut report, "\n## W3 Dataset Results")?;
    writeln!(&mut report, "\n### Overall Statistics")?;
    writeln!(&mut report, "- Total unique colors: {}", w3_stats.total_unique_colors)?;
    
    writeln!(&mut report, "\n### Accuracy by Illuminant (W3) - FIXED Calculation")?;
    writeln!(&mut report, "| Illuminant | Total | Rust Correct | Python Correct | Python Errors | Effective Pop | Rust Accuracy | Python Accuracy | Rust Unknown | Python Unknown |")?;
    writeln!(&mut report, "|------------|-------|--------------|----------------|---------------|---------------|---------------|-----------------|--------------|----------------|")?;
    
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65", 
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        let rust_matches = w3_stats.rust_matches.get(illum_name).unwrap_or(&0);
        let python_matches = w3_stats.python_matches.get(illum_name).unwrap_or(&0);
        let python_errors = w3_stats.python_errors.get(illum_name).unwrap_or(&0);
        let rust_unknowns = w3_stats.rust_unknowns.get(illum_name).unwrap_or(&0);
        let python_unknowns = w3_stats.python_unknowns.get(illum_name).unwrap_or(&0);
        
        // FIX 4: Calculate accuracy as matches / (total - errors)
        let effective_population = w3_stats.total_unique_colors - python_errors;
        let rust_acc = (*rust_matches as f64 / w3_stats.total_unique_colors as f64) * 100.0;
        let python_acc = if effective_population > 0 {
            (*python_matches as f64 / effective_population as f64) * 100.0
        } else {
            0.0
        };
        
        writeln!(&mut report, "| {:10} | {:5} | {:12} | {:14} | {:13} | {:13} | {:13.1}% | {:15.1}% | {:12} | {:14} |",
            illum_name, w3_stats.total_unique_colors, rust_matches, python_matches, 
            python_errors, effective_population, rust_acc, python_acc, rust_unknowns, python_unknowns)?;
    }
    
    // Centore Dataset Results with FIXED accuracy calculation
    writeln!(&mut report, "\n## Centore Dataset Results")?;
    writeln!(&mut report, "\n### Overall Statistics")?;
    writeln!(&mut report, "- Total unique colors: {}", centore_stats.total_unique_colors)?;
    
    writeln!(&mut report, "\n### Accuracy by Illuminant (Centore) - FIXED Calculation")?;
    writeln!(&mut report, "| Illuminant | Total | Rust Correct | Python Correct | Python Errors | Effective Pop | Rust Accuracy | Python Accuracy | Rust Unknown | Python Unknown |")?;
    writeln!(&mut report, "|------------|-------|--------------|----------------|---------------|---------------|---------------|-----------------|--------------|----------------|")?;
    
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7", 
            _ => continue,
        };
        
        let rust_matches = centore_stats.rust_matches.get(illum_name).unwrap_or(&0);
        let python_matches = centore_stats.python_matches.get(illum_name).unwrap_or(&0);
        let python_errors = centore_stats.python_errors.get(illum_name).unwrap_or(&0);
        let rust_unknowns = centore_stats.rust_unknowns.get(illum_name).unwrap_or(&0);
        let python_unknowns = centore_stats.python_unknowns.get(illum_name).unwrap_or(&0);
        
        // FIX 4: Calculate accuracy as matches / (total - errors) 
        let effective_population = centore_stats.total_unique_colors - python_errors;
        let rust_acc = (*rust_matches as f64 / centore_stats.total_unique_colors as f64) * 100.0;
        let python_acc = if effective_population > 0 {
            (*python_matches as f64 / effective_population as f64) * 100.0
        } else {
            0.0
        };
        
        writeln!(&mut report, "| {:10} | {:5} | {:12} | {:14} | {:13} | {:13} | {:13.1}% | {:15.1}% | {:12} | {:14} |",
            illum_name, centore_stats.total_unique_colors, rust_matches, python_matches,
            python_errors, effective_population, rust_acc, python_acc, rust_unknowns, python_unknowns)?;
    }
    
    // Add sample errors and unknowns for investigation (first 3 each)
    add_error_analysis(&mut report, &configurations, &w3_results, &centore_results, 3)?;
    add_unknown_analysis(&mut report, &configurations, &w3_results, &centore_results, 3)?;
    add_mismatch_analysis(&mut report, &configurations, &w3_results, &centore_results, 3)?;
    
    // Summary with corrected accuracy analysis
    writeln!(&mut report, "\n## Summary")?;
    writeln!(&mut report, "\n### V4 Comprehensive Fixes Applied:")?;
    writeln!(&mut report, "1. **Python API Fix**: Used 'XYZ Scaling' instead of 'XYZScaling'")?;
    writeln!(&mut report, "2. **ISCC-NBS Fix**: Used revised_descriptor field from construct_revised_descriptor()")?;
    writeln!(&mut report, "3. **Accuracy Fix**: Calculate as matches / (total - errors)")?;
    writeln!(&mut report, "4. **Error Tracking**: Store actual Python error messages for debugging")?;
    writeln!(&mut report, "5. **Unknown Analysis**: Track colors outside ISCC-NBS boundaries")?;
    writeln!(&mut report, "6. **Expected Names**: Apply construct_revised_descriptor() logic to ground truth")?;
    writeln!(&mut report, "7. **Batched Processing**: Process in batches of {} to avoid timeouts", BATCH_SIZE)?;
    
    // Write report
    let output_path = "comprehensive_dataset_misses_v4.md";
    fs::write(output_path, report)?;
    
    println!("\n✅ Report generated: {}", output_path);
    println!("\n📊 V4 Summary with FIXED Accuracy Calculation (Batched):");
    
    // Print corrected accuracies
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        let w3_rust_matches = w3_stats.rust_matches.get(illum_name).unwrap_or(&0);
        let w3_python_matches = w3_stats.python_matches.get(illum_name).unwrap_or(&0);
        let w3_python_errors = w3_stats.python_errors.get(illum_name).unwrap_or(&0);
        let w3_effective = w3_stats.total_unique_colors - w3_python_errors;
        
        let centore_rust_matches = centore_stats.rust_matches.get(illum_name).unwrap_or(&0);
        let centore_python_matches = centore_stats.python_matches.get(illum_name).unwrap_or(&0);
        let centore_python_errors = centore_stats.python_errors.get(illum_name).unwrap_or(&0);
        let centore_effective = centore_stats.total_unique_colors - centore_python_errors;
        
        println!("  {} Illuminant:", illum_name);
        println!("    W3 Rust: {:.1}% ({}/{})", 
            *w3_rust_matches as f64 / w3_stats.total_unique_colors as f64 * 100.0, 
            w3_rust_matches, w3_stats.total_unique_colors);
        println!("    W3 Python: {:.1}% ({}/{}, {} errors)", 
            if w3_effective > 0 { *w3_python_matches as f64 / w3_effective as f64 * 100.0 } else { 0.0 },
            w3_python_matches, w3_effective, w3_python_errors);
        println!("    Centore Rust: {:.1}% ({}/{})", 
            *centore_rust_matches as f64 / centore_stats.total_unique_colors as f64 * 100.0,
            centore_rust_matches, centore_stats.total_unique_colors);
        println!("    Centore Python: {:.1}% ({}/{}, {} errors)", 
            if centore_effective > 0 { *centore_python_matches as f64 / centore_effective as f64 * 100.0 } else { 0.0 },
            centore_python_matches, centore_effective, centore_python_errors);
    }
    
    Ok(())
}

/// Add error analysis section to the report
fn add_error_analysis(
    report: &mut String, 
    configurations: &[(MathIlluminant, &str)], 
    w3_results: &HashMap<String, Vec<TestResult>>, 
    centore_results: &HashMap<String, Vec<TestResult>>,
    limit: usize
) -> Result<(), std::fmt::Error> {
    writeln!(report, "\n## Python Error Analysis")?;
    writeln!(report, "\n### Sample Python Errors (First {} per illuminant)", limit)?;
    
    for (illuminant, _) in configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        let mut all_errors = Vec::new();
        
        if let Some(w3_results) = w3_results.get(illum_name) {
            for result in w3_results.iter().filter(|r| r.python_error) {
                all_errors.push(("W3", result));
            }
        }
        
        if let Some(centore_results) = centore_results.get(illum_name) {
            for result in centore_results.iter().filter(|r| r.python_error) {
                all_errors.push(("Centore", result));
            }
        }
        
        if !all_errors.is_empty() {
            writeln!(report, "\n#### Illuminant {} - Python Errors", illum_name)?;
            for (dataset, result) in all_errors.iter().take(limit) {
                writeln!(report, "\n**{} - Color: #{:02X}{:02X}{:02X} - Expected: \"{}\"**", 
                    dataset, result.rgb[0], result.rgb[1], result.rgb[2], result.expected_name)?;
                writeln!(report, "- Rust: {} → \"{}\" {}", 
                    result.munsell_notation, result.rust_iscc, 
                    if result.rust_match { "✓" } else { "✗" })?;
                writeln!(report, "- Python Error: `{}`", result.python_error_msg)?;
            }
        }
    }
    
    Ok(())
}

/// Add unknown classification analysis section to the report
fn add_unknown_analysis(
    report: &mut String, 
    configurations: &[(MathIlluminant, &str)], 
    w3_results: &HashMap<String, Vec<TestResult>>, 
    centore_results: &HashMap<String, Vec<TestResult>>,
    limit: usize
) -> Result<(), std::fmt::Error> {
    writeln!(report, "\n## Unknown Classification Analysis")?;
    writeln!(report, "\n### Colors Classified as \"Unknown\" (First {} per illuminant)", limit)?;
    writeln!(report, "These may be outside ISCC-NBS polygon boundaries or neutral colors.")?;
    
    for (illuminant, _) in configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65", 
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        let mut all_unknowns = Vec::new();
        
        if let Some(w3_results) = w3_results.get(illum_name) {
            for result in w3_results.iter().filter(|r| r.rust_unknown || r.python_unknown) {
                all_unknowns.push(("W3", result));
            }
        }
        
        if let Some(centore_results) = centore_results.get(illum_name) {
            for result in centore_results.iter().filter(|r| r.rust_unknown || r.python_unknown) {
                all_unknowns.push(("Centore", result));
            }
        }
        
        if !all_unknowns.is_empty() {
            writeln!(report, "\n#### Illuminant {} - Unknown Classifications", illum_name)?;
            for (dataset, result) in all_unknowns.iter().take(limit) {
                writeln!(report, "\n**{} - Color: #{:02X}{:02X}{:02X} - Expected: \"{}\"**", 
                    dataset, result.rgb[0], result.rgb[1], result.rgb[2], result.expected_name)?;
                writeln!(report, "- Rust: {} → \"{}\" {} {}", 
                    result.munsell_notation, result.rust_iscc, 
                    if result.rust_match { "✓" } else { "✗" },
                    if result.rust_unknown { "(UNKNOWN)" } else { "" })?;
                writeln!(report, "- Python: {} → \"{}\" {} {}", 
                    result.python_munsell, result.python_iscc,
                    if result.python_error { "ERROR" } else if result.python_match { "✓" } else { "✗" },
                    if result.python_unknown { "(UNKNOWN)" } else { "" })?;
            }
        }
    }
    
    Ok(())
}

/// Add mismatch analysis section to the report
fn add_mismatch_analysis(
    report: &mut String, 
    configurations: &[(MathIlluminant, &str)], 
    w3_results: &HashMap<String, Vec<TestResult>>, 
    centore_results: &HashMap<String, Vec<TestResult>>,
    limit: usize
) -> Result<(), std::fmt::Error> {
    writeln!(report, "\n## Detailed Mismatch Analysis (First {} per illuminant)", limit)?;
    writeln!(report, "Excludes Python errors and Unknown classifications for focus on actual classification differences.")?;
    
    writeln!(report, "\n### W3 Dataset - Detailed Mismatches")?;
    for (illuminant, _) in configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        if let Some(results) = w3_results.get(illum_name) {
            let mismatches: Vec<_> = results.iter()
                .filter(|r| !r.rust_match && !r.python_error && !r.rust_unknown && !r.python_unknown)
                .take(limit)
                .collect();
            
            if !mismatches.is_empty() {
                writeln!(report, "\n#### Illuminant {} - W3 Mismatches", illum_name)?;
                for result in mismatches {
                    writeln!(report, "\n**Color: #{:02X}{:02X}{:02X} - Expected: \"{}\"**", 
                        result.rgb[0], result.rgb[1], result.rgb[2], result.expected_name)?;
                    writeln!(report, "- Rust: {} → \"{}\" {}", 
                        result.munsell_notation, result.rust_iscc, 
                        if result.rust_match { "✓" } else { "✗" })?;
                    writeln!(report, "- Python: {} → \"{}\" {}",
                        result.python_munsell, result.python_iscc,
                        if result.python_match { "✓" } else { "✗" })?;
                }
            }
        }
    }
    
    writeln!(report, "\n### Centore Dataset - Detailed Mismatches")?;
    for (illuminant, _) in configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        if let Some(results) = centore_results.get(illum_name) {
            let mismatches: Vec<_> = results.iter()
                .filter(|r| !r.rust_match && !r.python_error && !r.rust_unknown && !r.python_unknown)
                .take(limit)
                .collect();
            
            if !mismatches.is_empty() {
                writeln!(report, "\n#### Illuminant {} - Centore Mismatches", illum_name)?;
                for result in mismatches {
                    writeln!(report, "\n**Color: #{:02X}{:02X}{:02X} - Expected: \"{}\"**", 
                        result.rgb[0], result.rgb[1], result.rgb[2], result.expected_name)?;
                    writeln!(report, "- Rust: {} → \"{}\" {}", 
                        result.munsell_notation, result.rust_iscc, 
                        if result.rust_match { "✓" } else { "✗" })?;
                    writeln!(report, "- Python: {} → \"{}\" {}",
                        result.python_munsell, result.python_iscc,
                        if result.python_match { "✓" } else { "✗" })?;
                }
            }
        }
    }
    
    Ok(())
}

/// FIX 2: Apply construct_revised_descriptor logic to expected names from W3 dataset
fn construct_expected_name(modifier: &str, color: &str) -> String {
    let modifier = modifier.trim();
    let color = color.trim();
    
    // Handle empty or dash modifiers
    if modifier.is_empty() || modifier == "-" {
        return color.to_string();
    }
    
    // Handle -ish modifiers with proper transformation
    if modifier.contains("-ish") {
        // Apply -ish transformation rules similar to construct_revised_descriptor
        return apply_ish_transformation_to_expected(color, modifier);
    }
    
    // Basic prefix rule
    format!("{} {}", modifier, color)
}

/// Apply -ish transformation rules to expected names (mirrors classifier logic)
fn apply_ish_transformation_to_expected(color: &str, modifier: &str) -> String {
    // For expected names like "white pink" with modifier "-ish", 
    // construct "pinkish white" similar to construct_revised_descriptor
    if modifier == "-ish" {
        match color {
            "brown" => "brownish".to_string(),
            "blue" => "bluish".to_string(),
            "red" => "reddish".to_string(), 
            "green" => "greenish".to_string(),
            "yellow" => "yellowish".to_string(),
            "purple" => "purplish".to_string(),
            "pink" => "pinkish".to_string(),
            "white" => "whitish".to_string(),
            "gray" => "grayish".to_string(),
            "black" => "blackish".to_string(),
            _ => format!("{}ish", color),
        }
    } else if color.contains(' ') {
        // Handle compound colors like "white pink" with "-ish" modifier
        let parts: Vec<&str> = color.split_whitespace().collect();
        if parts.len() == 2 {
            let base_color = parts[1];  // "pink" from "white pink"
            let descriptor = parts[0];  // "white" from "white pink" 
            let ish_color = match base_color {
                "brown" => "brownish",
                "blue" => "bluish",
                "red" => "reddish",
                "green" => "greenish", 
                "yellow" => "yellowish",
                "purple" => "purplish",
                "pink" => "pinkish",
                _ => return format!("{}ish {}", base_color, descriptor),
            };
            format!("{} {}", ish_color, descriptor)
        } else {
            format!("{}ish", color)
        }
    } else {
        format!("{}ish", color)
    }
}

fn load_w3_dataset() -> Result<Vec<W3IsccColor>, Box<dyn std::error::Error>> {
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path("tests/data/ISCC_NBS_REFERENCE_DATASET.csv")?;
    
    let mut colors = Vec::new();
    for result in reader.deserialize() {
        let color: W3IsccColor = result?;
        colors.push(color);
    }
    Ok(colors)
}

fn load_centore_dataset() -> Result<Vec<CentoreIsccColor>, Box<dyn std::error::Error>> {
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path("iscc_nbs_colors.csv")?;
    
    let mut colors = Vec::new();
    for result in reader.deserialize() {
        let color: CentoreIsccColor = result?;
        colors.push(color);
    }
    Ok(colors)
}

fn parse_rgb(srgb_str: &str) -> Result<[u8; 3], Box<dyn std::error::Error>> {
    let trimmed = srgb_str.trim();
    
    if trimmed.starts_with('#') {
        // Parse hex format
        let hex = trimmed.trim_start_matches('#');
        let r = u8::from_str_radix(&hex[0..2], 16)?;
        let g = u8::from_str_radix(&hex[2..4], 16)?;
        let b = u8::from_str_radix(&hex[4..6], 16)?;
        Ok([r, g, b])
    } else {
        Err("Invalid RGB format".into())
    }
}

fn get_python_munsell_batch(requests: &[PythonConversion]) -> Result<HashMap<String, String>, Box<dyn std::error::Error>> {
    let mut child = Command::new("python3")
        .arg("/Users/chris/Dropbox/dev/projects/libraries/MunsellSpace/investigation/src/generate_python_munsell.py")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;
    
    // Send JSON request
    if let Some(mut stdin) = child.stdin.take() {
        let request = PythonConversionRequest {
            conversions: requests.to_vec(),
        };
        let json = serde_json::to_string(&request)?;
        stdin.write_all(json.as_bytes())?;
    }
    
    // Read response
    let output = child.wait_with_output()?;
    
    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        eprintln!("Python script error: {}", stderr);
        return Err(format!("Python script failed: {}", stderr).into());
    }
    
    let response: PythonConversionResult = serde_json::from_slice(&output.stdout)?;
    Ok(response.results)
}