//! Comprehensive Conversion Dataset - Mismatches Analysis V3
//! 
//! Uses the restored breakthrough mathematical converter with illuminant support
//! Based on findings from V2:
//! - Method 2 (ExcludeStartIncludeEnd) is systematically better - ONLY METHOD USED
//! - XYZScaling is the best adaptation method
//! - Illuminants: C (best for W3), D65/F7 (best for Centore)
//! - Adds Python ISCC-NBS classification comparison

use munsellspace::iscc::ISCC_NBS_Classifier as IsccNbsClassifier;
use munsellspace::mechanical_wedges::{MechanicalWedgeSystem, HueRangeMethod};
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
    illuminant: String,
    munsell_notation: String,
    python_munsell: String,  // Clean Python reference (empty if error)
    python_iscc: String,      // Python's ISCC-NBS classification
    rust_iscc: String,        // Rust's ISCC-NBS classification
    match_status: bool,       // Does Rust match expected?
    python_match: bool,       // Does Python match expected?
}

#[derive(Debug, Default)]
struct Statistics {
    total_colors: usize,
    colors_with_mismatch: usize,
    
    // Accuracy by illuminant
    rust_matches: HashMap<String, usize>,
    python_matches: HashMap<String, usize>,
    python_errors: HashMap<String, usize>,
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
    println!("🔬 Generating Comprehensive Conversion Dataset - Mismatches Analysis V3");
    println!("=====================================================================");
    println!("Using restored breakthrough mathematical converter with illuminant support");
    println!("Method 2 (ExcludeStartIncludeEnd) exclusively based on V2 findings");
    println!();
    
    // Load datasets
    let w3_colors = load_w3_dataset()?;
    let centore_colors = load_centore_dataset()?;
    
    println!("📊 Loaded {} W3 colors and {} Centore colors", w3_colors.len(), centore_colors.len());
    
    // Define test configurations - XYZScaling only, with C/D65/F7
    let configurations = vec![
        (MathIlluminant::C, "C"),
        (MathIlluminant::D65, "D65"),
        (MathIlluminant::F7, "F7"),
    ];
    
    // Initialize classifier (Method 2 will be used internally)
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
            all_test_data.push((id, rgb, illum_name.to_string(), format!("{} {}", color.modifier.trim(), color.color.trim())));
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
            all_test_data.push((id, rgb, illum_name.to_string(), color.name.clone()));
        }
    }
    
    println!("🐍 Getting Python Munsell values for {} color/illuminant combinations...", python_requests.len());
    let python_results = get_python_munsell_batch(&python_requests)?;
    println!("✅ Received {} Python results", python_results.len());
    
    // Analyze mismatches
    let mut w3_stats = Statistics::default();
    let mut centore_stats = Statistics::default();
    let mut w3_mismatches: HashMap<String, Vec<(String, String, TestResult)>> = HashMap::new();
    let mut centore_mismatches: HashMap<String, Vec<(String, String, TestResult)>> = HashMap::new();
    
    println!("\n🔍 Analyzing conversions with breakthrough mathematical converter...");
    
    for (id, rgb, illum_name, expected_name) in all_test_data {
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
        let python_iscc = if !python_munsell.is_empty() {
            // Parse Python Munsell notation (e.g., "7.8R 5.2/20.5")
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
        let python_match = python_iscc.to_lowercase() == expected_name.to_lowercase();
        
        // Update statistics
        let stats = if id.starts_with("W3") { &mut w3_stats } else { &mut centore_stats };
        let mismatches = if id.starts_with("W3") { &mut w3_mismatches } else { &mut centore_mismatches };
        
        stats.total_colors += 1;
        
        if rust_match {
            *stats.rust_matches.entry(illum_name.clone()).or_insert(0) += 1;
        }
        
        if python_munsell.is_empty() {
            *stats.python_errors.entry(illum_name.clone()).or_insert(0) += 1;
        } else if python_match {
            *stats.python_matches.entry(illum_name.clone()).or_insert(0) += 1;
        }
        
        if !rust_match {
            stats.colors_with_mismatch += 1;
            let result = TestResult {
                illuminant: illum_name.clone(),
                munsell_notation: rust_notation,
                python_munsell: python_munsell.clone(),
                python_iscc,
                rust_iscc,
                match_status: rust_match,
                python_match,
            };
            
            let rgb_str = format!("#{:02X}{:02X}{:02X}", rgb[0], rgb[1], rgb[2]);
            mismatches.entry(illum_name.clone())
                .or_insert_with(Vec::new)
                .push((rgb_str, expected_name.clone(), result));
        }
    }
    
    // Generate report
    let mut report = String::new();
    writeln!(&mut report, "# Comprehensive Conversion Dataset - Mismatches Analysis V3")?;
    writeln!(&mut report, "\nGenerated: {}", std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_secs())?;
    writeln!(&mut report, "\n## Configuration")?;
    writeln!(&mut report, "- Converter: Restored breakthrough mathematical converter (60.4% baseline)")?;
    writeln!(&mut report, "- Hue Range Method: ExcludeStartIncludeEnd (Method 2)")?;
    writeln!(&mut report, "- Chromatic Adaptation: XYZScaling")?;
    writeln!(&mut report, "- Illuminants tested: C, D65, F7")?;
    
    // W3 Dataset Results
    writeln!(&mut report, "\n## W3 Dataset Results")?;
    writeln!(&mut report, "\n### Overall Statistics")?;
    let w3_unique = w3_colors.len();
    writeln!(&mut report, "- Unique colors: {}", w3_unique)?;
    writeln!(&mut report, "- Total tests: {} (3 illuminants × {} colors)", w3_stats.total_colors, w3_unique)?;
    writeln!(&mut report, "- Colors with at least one mismatch: {}/{} ({:.1}%)", 
        w3_stats.colors_with_mismatch, w3_stats.total_colors,
        (w3_stats.colors_with_mismatch as f64 / w3_stats.total_colors as f64) * 100.0)?;
    
    writeln!(&mut report, "\n### Accuracy by Illuminant (W3)")?;
    writeln!(&mut report, "| Illuminant | Rust Matches | Python Matches | Python Errors | Rust Accuracy | Python Accuracy |")?;
    writeln!(&mut report, "|------------|-------------|----------------|---------------|---------------|-----------------|")?;
    
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
        let rust_acc = (*rust_matches as f64 / w3_unique as f64) * 100.0;
        let python_acc = (*python_matches as f64 / w3_unique as f64) * 100.0;
        
        writeln!(&mut report, "| {:10} | {:11} | {:14} | {:13} | {:13.1}% | {:15.1}% |",
            illum_name, rust_matches, python_matches, python_errors, rust_acc, python_acc)?;
    }
    
    // Centore Dataset Results
    writeln!(&mut report, "\n## Centore Dataset Results")?;
    writeln!(&mut report, "\n### Overall Statistics")?;
    let centore_unique = centore_colors.len();
    writeln!(&mut report, "- Unique colors: {}", centore_unique)?;
    writeln!(&mut report, "- Total tests: {} (3 illuminants × {} colors)", centore_stats.total_colors, centore_unique)?;
    writeln!(&mut report, "- Colors with at least one mismatch: {}/{} ({:.1}%)", 
        centore_stats.colors_with_mismatch, centore_stats.total_colors,
        (centore_stats.colors_with_mismatch as f64 / centore_stats.total_colors as f64) * 100.0)?;
    
    writeln!(&mut report, "\n### Accuracy by Illuminant (Centore)")?;
    writeln!(&mut report, "| Illuminant | Rust Matches | Python Matches | Python Errors | Rust Accuracy | Python Accuracy |")?;
    writeln!(&mut report, "|------------|-------------|----------------|---------------|---------------|-----------------|")?;
    
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
        let rust_acc = (*rust_matches as f64 / centore_unique as f64) * 100.0;
        let python_acc = (*python_matches as f64 / centore_unique as f64) * 100.0;
        
        writeln!(&mut report, "| {:10} | {:11} | {:14} | {:13} | {:13.1}% | {:15.1}% |",
            illum_name, rust_matches, python_matches, python_errors, rust_acc, python_acc)?;
    }
    
    // Sample mismatches for analysis
    writeln!(&mut report, "\n## Sample Mismatches (First 5 per illuminant)")?;
    
    writeln!(&mut report, "\n### W3 Dataset Mismatches")?;
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        if let Some(mismatches) = w3_mismatches.get(illum_name) {
            writeln!(&mut report, "\n#### Illuminant {}", illum_name)?;
            writeln!(&mut report, "| RGB | Expected | Rust Result | Rust ISCC | Python Result | Python ISCC |")?;
            writeln!(&mut report, "|-----|----------|-------------|-----------|---------------|-------------|")?;
            
            for (rgb, expected, result) in mismatches.iter().take(5) {
                writeln!(&mut report, "| {} | {} | {} | {} | {} | {} |",
                    rgb, expected, result.munsell_notation, result.rust_iscc,
                    if result.python_munsell.is_empty() { "ERROR" } else { &result.python_munsell },
                    &result.python_iscc)?;
            }
        }
    }
    
    writeln!(&mut report, "\n### Centore Dataset Mismatches")?;
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        if let Some(mismatches) = centore_mismatches.get(illum_name) {
            writeln!(&mut report, "\n#### Illuminant {}", illum_name)?;
            writeln!(&mut report, "| RGB | Expected | Rust Result | Rust ISCC | Python Result | Python ISCC |")?;
            writeln!(&mut report, "|-----|----------|-------------|-----------|---------------|-------------|")?;
            
            for (rgb, expected, result) in mismatches.iter().take(5) {
                writeln!(&mut report, "| {} | {} | {} | {} | {} | {} |",
                    rgb, expected, result.munsell_notation, result.rust_iscc,
                    if result.python_munsell.is_empty() { "ERROR" } else { &result.python_munsell },
                    &result.python_iscc)?;
            }
        }
    }
    
    // Comparison with V2
    writeln!(&mut report, "\n## Comparison with V2 Results")?;
    writeln!(&mut report, "\n### V2 Results (mathematical_v2 converter):")?;
    writeln!(&mut report, "- W3 Dataset: Best 53.9% with Illuminant C")?;
    writeln!(&mut report, "- Centore Dataset: Best 63.8% with F7")?;
    writeln!(&mut report, "- Python accuracy: 82.3% on Centore with F7")?;
    
    writeln!(&mut report, "\n### V3 Results (breakthrough mathematical converter):")?;
    writeln!(&mut report, "- Using restored 60.4% accuracy baseline version")?;
    writeln!(&mut report, "- Added illuminant configurability with chromatic adaptation")?;
    writeln!(&mut report, "- See accuracy tables above for detailed comparison")?;
    
    // Write report
    let output_path = "comprehensive_dataset_misses_v3.md";
    fs::write(output_path, report)?;
    
    println!("\n✅ Report generated: {}", output_path);
    println!("\n📊 Summary:");
    println!("  W3 Dataset best: {:.1}% accuracy", 
        w3_stats.rust_matches.values().max().unwrap_or(&0).clone() as f64 / w3_unique as f64 * 100.0);
    println!("  Centore Dataset best: {:.1}% accuracy",
        centore_stats.rust_matches.values().max().unwrap_or(&0).clone() as f64 / centore_unique as f64 * 100.0);
    
    Ok(())
}

fn load_w3_dataset() -> Result<Vec<W3IsccColor>, Box<dyn std::error::Error>> {
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path("ISCC_NBS_REFERENCE_DATASET.csv")?;
    
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