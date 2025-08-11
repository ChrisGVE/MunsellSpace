//! Comprehensive Conversion Dataset - Mismatches Analysis V3b
//! 
//! FIXED VERSION addressing bugs found in v3:
//! - Properly count Python errors as failures
//! - Correctly parse expected names from W3 dataset
//! - Add detailed mismatch format from v2
//! - Fix statistics to count per-color not per-test
//! - Investigate "Unknown" classifications

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
    python_iscc: String,
    rust_iscc: String,
    rust_match: bool,
    python_match: bool,
    python_error: bool,
}

#[derive(Debug, Default)]
struct Statistics {
    total_unique_colors: usize,
    
    // Per-illuminant accuracy tracking
    rust_matches: HashMap<String, usize>,
    python_matches: HashMap<String, usize>,
    python_errors: HashMap<String, usize>,
    
    // Track "Unknown" classifications
    rust_unknowns: HashMap<String, usize>,
    python_unknowns: HashMap<String, usize>,
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

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 Generating Comprehensive Conversion Dataset - Mismatches Analysis V3b");
    println!("======================================================================");
    println!("FIXED VERSION: Properly counting errors, parsing names, detailed format");
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
    
    // Prepare batch Python conversion request
    let mut python_requests = Vec::new();
    let mut all_test_data = Vec::new();
    
    // Collect all test combinations
    for (_illuminant, illum_name) in &configurations {
        // W3 dataset
        for color in &w3_colors {
            let rgb = parse_rgb(&color.srgb)?;
            let id = format!("W3_{}_{}", illum_name, color.srgb.trim());
            python_requests.push(PythonConversion {
                id: id.clone(),
                rgb,
                illuminant: illum_name.to_string(),
                adaptation: "XYZScaling".to_string(),
            });
            
            // Parse expected name correctly - remove extra spaces and combine
            let modifier = color.modifier.trim();
            let color_name = color.color.trim();
            let expected_name = if modifier.is_empty() || modifier == "-" {
                color_name.to_string()
            } else if modifier.ends_with("-ish") {
                format!("{} {}", modifier, color_name)
            } else {
                format!("{} {}", modifier, color_name)
            };
            
            all_test_data.push((id, rgb, illum_name.to_string(), expected_name, "W3"));
        }
        
        // Centore dataset
        for color in &centore_colors {
            let rgb = [color.r, color.g, color.b];
            let id = format!("Centore_{}_{}", illum_name, color.number);
            python_requests.push(PythonConversion {
                id: id.clone(),
                rgb,
                illuminant: illum_name.to_string(),
                adaptation: "XYZScaling".to_string(),
            });
            all_test_data.push((id, rgb, illum_name.to_string(), color.name.clone(), "Centore"));
        }
    }
    
    println!("🐍 Getting Python Munsell values for {} color/illuminant combinations...", python_requests.len());
    let python_results = get_python_munsell_batch(&python_requests)?;
    println!("✅ Received {} Python results", python_results.len());
    
    // Analyze results
    let mut w3_stats = Statistics::default();
    let mut centore_stats = Statistics::default();
    let mut w3_results: HashMap<String, Vec<TestResult>> = HashMap::new();
    let mut centore_results: HashMap<String, Vec<TestResult>> = HashMap::new();
    
    w3_stats.total_unique_colors = w3_colors.len();
    centore_stats.total_unique_colors = centore_colors.len();
    
    println!("\n🔍 Analyzing conversions with breakthrough mathematical converter...");
    
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
        
        // Classify with Rust
        let rust_iscc = match classifier.classify_munsell(&format!("{:.1}{}", rust_spec.hue, rust_spec.family), 
                                                          rust_spec.value, rust_spec.chroma) {
            Ok(Some(result)) => result.iscc_nbs_descriptor.clone(),
            _ => "Unknown".to_string(),
        };
        
        // Get Python result
        let python_munsell = python_results.get(&id).cloned().unwrap_or_default();
        let python_error = python_munsell.is_empty() || python_munsell.starts_with("ERROR:");
        
        // Parse Python ISCC-NBS classification
        let python_iscc = if !python_error {
            if let Some((hue_part, value_chroma)) = python_munsell.split_once(' ') {
                if let Some((value_str, chroma_str)) = value_chroma.split_once('/') {
                    let value = value_str.parse::<f64>().unwrap_or(0.0);
                    let chroma = chroma_str.parse::<f64>().unwrap_or(0.0);
                    match classifier.classify_munsell(hue_part, value, chroma) {
                        Ok(Some(result)) => result.iscc_nbs_descriptor.clone(),
                        _ => "Unknown".to_string(),
                    }
                } else {
                    "Unknown".to_string()
                }
            } else {
                "Unknown".to_string()
            }
        } else {
            "Error".to_string()
        };
        
        // Check matches
        let rust_match = rust_iscc.to_lowercase() == expected_name.to_lowercase();
        let python_match = !python_error && python_iscc.to_lowercase() == expected_name.to_lowercase();
        
        // Update statistics
        let stats = if dataset == "W3" { &mut w3_stats } else { &mut centore_stats };
        let results = if dataset == "W3" { &mut w3_results } else { &mut centore_results };
        
        if rust_match {
            *stats.rust_matches.entry(illum_name.clone()).or_insert(0) += 1;
        }
        
        if python_error {
            *stats.python_errors.entry(illum_name.clone()).or_insert(0) += 1;
        } else if python_match {
            *stats.python_matches.entry(illum_name.clone()).or_insert(0) += 1;
        }
        
        if rust_iscc == "Unknown" {
            *stats.rust_unknowns.entry(illum_name.clone()).or_insert(0) += 1;
        }
        
        if python_iscc == "Unknown" && !python_error {
            *stats.python_unknowns.entry(illum_name.clone()).or_insert(0) += 1;
        }
        
        // Store all results for detailed analysis
        let result = TestResult {
            rgb,
            illuminant: illum_name.clone(),
            expected_name: expected_name.clone(),
            munsell_notation: rust_notation,
            python_munsell: if python_error { "ERROR".to_string() } else { python_munsell.clone() },
            python_iscc,
            rust_iscc,
            rust_match,
            python_match,
            python_error,
        };
        
        results.entry(illum_name.clone())
            .or_insert_with(Vec::new)
            .push(result);
    }
    
    // Generate report
    let mut report = String::new();
    writeln!(&mut report, "# Comprehensive Conversion Dataset - Mismatches Analysis V3b (FIXED)")?;
    writeln!(&mut report, "\nGenerated: {}", std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_secs())?;
    writeln!(&mut report, "\n## Configuration")?;
    writeln!(&mut report, "- Converter: Restored breakthrough mathematical converter (60.4% baseline)")?;
    writeln!(&mut report, "- Chromatic Adaptation: XYZScaling")?;
    writeln!(&mut report, "- Illuminants tested: C, D65, F7")?;
    writeln!(&mut report, "- **FIX**: Python errors now counted as failures")?;
    writeln!(&mut report, "- **FIX**: Expected names properly parsed")?;
    writeln!(&mut report, "- **FIX**: Statistics based on unique colors, not total tests")?;
    
    // W3 Dataset Results
    writeln!(&mut report, "\n## W3 Dataset Results")?;
    writeln!(&mut report, "\n### Overall Statistics")?;
    writeln!(&mut report, "- Unique colors in dataset: {}", w3_stats.total_unique_colors)?;
    
    writeln!(&mut report, "\n### Accuracy by Illuminant (W3)")?;
    writeln!(&mut report, "| Illuminant | Rust Correct | Python Correct | Python Errors | Rust Unknown | Python Unknown | Rust Accuracy | Python Accuracy |")?;
    writeln!(&mut report, "|------------|--------------|----------------|---------------|--------------|----------------|---------------|-----------------|")?;
    
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
        let rust_acc = (*rust_matches as f64 / w3_stats.total_unique_colors as f64) * 100.0;
        let python_acc = (*python_matches as f64 / w3_stats.total_unique_colors as f64) * 100.0;
        
        writeln!(&mut report, "| {:10} | {:12} | {:14} | {:13} | {:12} | {:14} | {:13.1}% | {:15.1}% |",
            illum_name, rust_matches, python_matches, python_errors, rust_unknowns, python_unknowns, rust_acc, python_acc)?;
    }
    
    // Centore Dataset Results
    writeln!(&mut report, "\n## Centore Dataset Results")?;
    writeln!(&mut report, "\n### Overall Statistics")?;
    writeln!(&mut report, "- Unique colors in dataset: {}", centore_stats.total_unique_colors)?;
    
    writeln!(&mut report, "\n### Accuracy by Illuminant (Centore)")?;
    writeln!(&mut report, "| Illuminant | Rust Correct | Python Correct | Python Errors | Rust Unknown | Python Unknown | Rust Accuracy | Python Accuracy |")?;
    writeln!(&mut report, "|------------|--------------|----------------|---------------|--------------|----------------|---------------|-----------------|")?;
    
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
        let rust_acc = (*rust_matches as f64 / centore_stats.total_unique_colors as f64) * 100.0;
        let python_acc = (*python_matches as f64 / centore_stats.total_unique_colors as f64) * 100.0;
        
        writeln!(&mut report, "| {:10} | {:12} | {:14} | {:13} | {:12} | {:14} | {:13.1}% | {:15.1}% |",
            illum_name, rust_matches, python_matches, python_errors, rust_unknowns, python_unknowns, rust_acc, python_acc)?;
    }
    
    // Detailed Mismatches (like v2 format)
    writeln!(&mut report, "\n## Detailed Mismatch Analysis (First 5 per illuminant)")?;
    
    writeln!(&mut report, "\n### W3 Dataset - Detailed Mismatches")?;
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        if let Some(results) = w3_results.get(illum_name) {
            let mismatches: Vec<_> = results.iter()
                .filter(|r| !r.rust_match)
                .take(5)
                .collect();
            
            if !mismatches.is_empty() {
                writeln!(&mut report, "\n#### Illuminant {} - W3 Mismatches", illum_name)?;
                for result in mismatches {
                    writeln!(&mut report, "\n**Color: #{:02X}{:02X}{:02X} - Expected: \"{}\"**", 
                        result.rgb[0], result.rgb[1], result.rgb[2], result.expected_name)?;
                    writeln!(&mut report, "- Rust: {} → \"{}\" {}", 
                        result.munsell_notation, result.rust_iscc, 
                        if result.rust_match { "✓" } else { "✗" })?;
                    writeln!(&mut report, "- Python: {} → \"{}\" {}",
                        result.python_munsell, result.python_iscc,
                        if result.python_error { "ERROR" } else if result.python_match { "✓" } else { "✗" })?;
                }
            }
        }
    }
    
    writeln!(&mut report, "\n### Centore Dataset - Detailed Mismatches")?;
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        if let Some(results) = centore_results.get(illum_name) {
            let mismatches: Vec<_> = results.iter()
                .filter(|r| !r.rust_match)
                .take(5)
                .collect();
            
            if !mismatches.is_empty() {
                writeln!(&mut report, "\n#### Illuminant {} - Centore Mismatches", illum_name)?;
                for result in mismatches {
                    writeln!(&mut report, "\n**Color: #{:02X}{:02X}{:02X} - Expected: \"{}\"**", 
                        result.rgb[0], result.rgb[1], result.rgb[2], result.expected_name)?;
                    writeln!(&mut report, "- Rust: {} → \"{}\" {}", 
                        result.munsell_notation, result.rust_iscc, 
                        if result.rust_match { "✓" } else { "✗" })?;
                    writeln!(&mut report, "- Python: {} → \"{}\" {}",
                        result.python_munsell, result.python_iscc,
                        if result.python_error { "ERROR" } else if result.python_match { "✓" } else { "✗" })?;
                }
            }
        }
    }
    
    // Summary comparison
    writeln!(&mut report, "\n## Summary")?;
    writeln!(&mut report, "\n### Key Findings:")?;
    writeln!(&mut report, "1. Python errors are now properly counted as failures")?;
    writeln!(&mut report, "2. \"Unknown\" classifications may indicate colors outside ISCC-NBS boundaries")?;
    writeln!(&mut report, "3. Expected names now correctly parsed from W3 dataset")?;
    writeln!(&mut report, "4. Statistics based on unique colors, not total tests")?;
    
    // Write report
    let output_path = "comprehensive_dataset_misses_v3b.md";
    fs::write(output_path, report)?;
    
    println!("\n✅ Report generated: {}", output_path);
    println!("\n📊 Summary:");
    
    // Print best accuracies
    let w3_best_rust = w3_stats.rust_matches.values().max().unwrap_or(&0);
    let w3_best_python = w3_stats.python_matches.values().max().unwrap_or(&0);
    let centore_best_rust = centore_stats.rust_matches.values().max().unwrap_or(&0);
    let centore_best_python = centore_stats.python_matches.values().max().unwrap_or(&0);
    
    println!("  W3 Dataset:");
    println!("    Best Rust: {:.1}%", *w3_best_rust as f64 / w3_stats.total_unique_colors as f64 * 100.0);
    println!("    Best Python: {:.1}%", *w3_best_python as f64 / w3_stats.total_unique_colors as f64 * 100.0);
    println!("  Centore Dataset:");
    println!("    Best Rust: {:.1}%", *centore_best_rust as f64 / centore_stats.total_unique_colors as f64 * 100.0);
    println!("    Best Python: {:.1}%", *centore_best_python as f64 / centore_stats.total_unique_colors as f64 * 100.0);
    
    Ok(())
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
        return Err("Python script failed".into());
    }
    
    let response: PythonConversionResult = serde_json::from_slice(&output.stdout)?;
    Ok(response.results)
}