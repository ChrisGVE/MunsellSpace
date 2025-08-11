//! Comprehensive Conversion Dataset - Mismatches Analysis V2
//! 
//! Based on findings:
//! - Method 2 (ExcludeStartIncludeEnd) is systematically better - ONLY METHOD USED
//! - XYZScaling is the best adaptation method
//! - Illuminants: C (best for W3), D65/F7 (best for Centore)
//! - Adds Python ISCC-NBS classification comparison

use munsellspace::iscc::ISCC_NBS_Classifier as IsccNbsClassifier;
use munsellspace::HueRangeMethod;
use munsellspace::mathematical::MathematicalMunsellConverter;
use munsellspace::illuminants::{Illuminant, ChromaticAdaptationMethod};
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
    println!("🔬 Generating Comprehensive Conversion Dataset - Mismatches Analysis V2");
    println!("=====================================================================");
    println!("Using Method 2 (ExcludeStartIncludeEnd) exclusively based on findings");
    println!();
    
    // Load datasets
    let w3_colors = load_w3_dataset()?;
    let centore_colors = load_centore_dataset()?;
    
    println!("📊 Loaded {} W3 colors and {} Centore colors", w3_colors.len(), centore_colors.len());
    
    // Define test configurations - XYZScaling only, with C/D65/F7
    let configurations = vec![
        (Illuminant::C, "C"),
        (Illuminant::D65, "D65"),
        (Illuminant::F7, "F7"),
    ];
    
    println!("📋 Testing {} illuminants with XYZScaling adaptation and Method 2 only", configurations.len());
    
    // Initialize classifier - Method 2 only
    let classifier = IsccNbsClassifier::new_with_hue_range_method(
        HueRangeMethod::ExcludeStartIncludeEnd
    )?;
    
    // Create report
    let mut report = String::new();
    
    // Header
    writeln!(&mut report, "# Comprehensive Conversion Dataset - Mismatches Analysis V2")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "## Configuration")?;
    writeln!(&mut report, "- **Illuminants**: C, D65, F7")?;
    writeln!(&mut report, "- **Adaptation**: XYZScaling (winner across datasets)")?;
    writeln!(&mut report, "- **Hue Method**: Method 2 (ExcludeStartIncludeEnd) - systematically better")?;
    writeln!(&mut report, "- **Python Reference**: colour-science library with ISCC-NBS classification")?;
    writeln!(&mut report)?;
    
    // Process W3 Dataset
    println!("\n🧪 Processing W3 ISCC-NBS dataset...");
    writeln!(&mut report, "## W3 ISCC-NBS Dataset ({} colors)", w3_colors.len())?;
    writeln!(&mut report)?;
    
    let mut w3_stats = Statistics::default();
    w3_stats.total_colors = w3_colors.len();
    
    // Prepare Python requests for ALL colors
    let mut python_requests = Vec::new();
    for (idx, color) in w3_colors.iter().enumerate() {
        let hex = color.srgb.trim_start_matches('#');
        if hex.len() != 6 { continue; }
        
        let r = u8::from_str_radix(&hex[0..2], 16)?;
        let g = u8::from_str_radix(&hex[2..4], 16)?;
        let b = u8::from_str_radix(&hex[4..6], 16)?;
        let rgb = [r, g, b];
        
        for (illuminant, illum_code) in &configurations {
            python_requests.push(PythonConversion {
                id: format!("w3_{}_{}", idx, illum_code),
                rgb,
                illuminant: illum_code.to_string(),
                adaptation: "XYZScaling".to_string(),
            });
        }
    }
    
    // Get Python results for ALL colors
    println!("🐍 Getting Python reference values for {} color/illuminant combinations...", python_requests.len());
    let python_results = if !python_requests.is_empty() {
        get_python_munsell_batch(&python_requests)?
    } else {
        HashMap::new()
    };
    
    // Summary statistics table
    writeln!(&mut report, "### Summary Statistics")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Illuminant | Rust Accuracy | Python Accuracy | Python Errors |")?;
    writeln!(&mut report, "|------------|---------------|-----------------|---------------|")?;
    
    // Calculate accuracies for each illuminant
    for (illuminant, illum_code) in &configurations {
        let (rust_acc, python_acc, python_err) = calculate_accuracy_for_dataset(
            &w3_colors,
            *illuminant,
            illum_code,
            &classifier,
            &python_results,
            &mut w3_stats,
            true, // is_w3
        )?;
        
        writeln!(&mut report, "| {} | {:.1}% | {:.1}% | {} |", 
            illum_code, rust_acc, python_acc, python_err)?;
    }
    writeln!(&mut report)?;
    
    // Collect mismatches for detailed reporting (limited to 5)
    let mut mismatch_indices = Vec::new();
    for (idx, color) in w3_colors.iter().enumerate() {
        let hex = color.srgb.trim_start_matches('#');
        if hex.len() != 6 { continue; }
        
        let r = u8::from_str_radix(&hex[0..2], 16)?;
        let g = u8::from_str_radix(&hex[2..4], 16)?;
        let b = u8::from_str_radix(&hex[4..6], 16)?;
        let rgb = [r, g, b];
        let expected_name = color.iscc_nbs_name.trim().to_lowercase();
        
        let mut has_mismatch = false;
        
        for (illuminant, illum_code) in &configurations {
            let converter = MathematicalMunsellConverter::with_illuminants(
                Illuminant::D65,
                *illuminant,
                ChromaticAdaptationMethod::XYZScaling,
            )?;
            
            if let Ok(munsell) = converter.srgb_to_munsell(rgb) {
                let hue_str = format!("{:.1}{}", munsell.hue, munsell.family);
                
                let rust_match = if let Ok(Some(result)) = classifier.classify_munsell(
                    &hue_str, munsell.value, munsell.chroma
                ) {
                    result.iscc_nbs_descriptor.to_lowercase() == expected_name
                } else { false };
                
                if !rust_match {
                    has_mismatch = true;
                    break;
                }
            }
        }
        
        if has_mismatch {
            mismatch_indices.push(idx);
            if mismatch_indices.len() >= 5 { break; } // Limit to 5 for detail
        }
    }
    
    // Detailed mismatches
    writeln!(&mut report, "### Detailed Mismatches (First 5)")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "Total colors with mismatches: {} ({:.1}%)", 
        w3_stats.colors_with_mismatch,
        (w3_stats.colors_with_mismatch as f64 / w3_stats.total_colors as f64) * 100.0)?;
    writeln!(&mut report)?;
    
    for idx in mismatch_indices {
        let color = &w3_colors[idx];
        let hex = color.srgb.trim_start_matches('#');
        if hex.len() != 6 { continue; }
        
        let r = u8::from_str_radix(&hex[0..2], 16)?;
        let g = u8::from_str_radix(&hex[2..4], 16)?;
        let b = u8::from_str_radix(&hex[4..6], 16)?;
        let rgb = [r, g, b];
        let hex_code = format!("#{:02X}{:02X}{:02X}", r, g, b);
        let expected_name = color.iscc_nbs_name.trim().to_lowercase();
        
        writeln!(&mut report, "#### {}. Expected: {}", idx + 1, expected_name)?;
        writeln!(&mut report, "Hex: {}", hex_code)?;
        writeln!(&mut report)?;
        writeln!(&mut report, "| Illuminant | Rust Munsell | Rust ISCC | R✓ | Python Munsell | Python ISCC | P✓ |")?;
        writeln!(&mut report, "|------------|--------------|-----------|----|--------------|-----------|----|")?;
        
        for (illuminant, illum_code) in &configurations {
            let result = test_color_with_python(
                rgb,
                &expected_name,
                *illuminant,
                illum_code,
                &classifier,
                &python_results,
                idx,
            )?;
            
            writeln!(&mut report, "| {} | {} | {} | {} | {} | {} | {} |",
                result.illuminant,
                result.munsell_notation,
                result.rust_iscc,
                if result.match_status { "✅" } else { "❌" },
                result.python_munsell,
                result.python_iscc,
                if result.python_match { "✅" } else { "❌" },
            )?;
        }
        writeln!(&mut report)?;
    }
    
    // Process Centore Dataset
    println!("\n🧪 Processing Paul Centore dataset...");
    writeln!(&mut report, "## Paul Centore Dataset ({} colors)", centore_colors.len())?;
    writeln!(&mut report)?;
    
    let mut centore_stats = Statistics::default();
    centore_stats.total_colors = centore_colors.len();
    
    // Prepare Python requests for ALL Centore colors
    let mut centore_python_requests = Vec::new();
    for (idx, color) in centore_colors.iter().enumerate() {
        let rgb = [color.r, color.g, color.b];
        
        for (illuminant, illum_code) in &configurations {
            centore_python_requests.push(PythonConversion {
                id: format!("centore_{}_{}", idx, illum_code),
                rgb,
                illuminant: illum_code.to_string(),
                adaptation: "XYZScaling".to_string(),
            });
        }
    }
    
    // Get Python results for ALL Centore colors
    println!("🐍 Getting Python reference values for {} Centore combinations...", centore_python_requests.len());
    let centore_python_results = if !centore_python_requests.is_empty() {
        get_python_munsell_batch(&centore_python_requests)?
    } else {
        HashMap::new()
    };
    
    // Summary statistics table
    writeln!(&mut report, "### Summary Statistics")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Illuminant | Rust Accuracy | Python Accuracy | Python Errors |")?;
    writeln!(&mut report, "|------------|---------------|-----------------|---------------|")?;
    
    // Calculate accuracies for each illuminant
    for (illuminant, illum_code) in &configurations {
        let (rust_acc, python_acc, python_err) = calculate_accuracy_for_centore(
            &centore_colors,
            *illuminant,
            illum_code,
            &classifier,
            &centore_python_results,
            &mut centore_stats,
        )?;
        
        writeln!(&mut report, "| {} | {:.1}% | {:.1}% | {} |", 
            illum_code, rust_acc, python_acc, python_err)?;
    }
    writeln!(&mut report)?;
    
    // Collect Centore mismatches (limited to 5)
    let mut centore_mismatch_indices = Vec::new();
    for (idx, color) in centore_colors.iter().enumerate() {
        let rgb = [color.r, color.g, color.b];
        let expected_name = color.name.trim().to_lowercase();
        
        let mut has_mismatch = false;
        
        for (illuminant, illum_code) in &configurations {
            let converter = MathematicalMunsellConverter::with_illuminants(
                Illuminant::D65,
                *illuminant,
                ChromaticAdaptationMethod::XYZScaling,
            )?;
            
            if let Ok(munsell) = converter.srgb_to_munsell(rgb) {
                let hue_str = format!("{:.1}{}", munsell.hue, munsell.family);
                
                let rust_match = if let Ok(Some(result)) = classifier.classify_munsell(
                    &hue_str, munsell.value, munsell.chroma
                ) {
                    result.iscc_nbs_descriptor.to_lowercase() == expected_name
                } else { false };
                
                if !rust_match {
                    has_mismatch = true;
                    break;
                }
            }
        }
        
        if has_mismatch {
            centore_mismatch_indices.push(idx);
            if centore_mismatch_indices.len() >= 5 { break; } // Limit to 5
        }
    }
    
    // Detailed Centore mismatches
    writeln!(&mut report, "### Detailed Mismatches (First 5)")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "Total colors with mismatches: {} ({:.1}%)", 
        centore_stats.colors_with_mismatch,
        (centore_stats.colors_with_mismatch as f64 / centore_stats.total_colors as f64) * 100.0)?;
    writeln!(&mut report)?;
    
    for idx in centore_mismatch_indices {
        let color = &centore_colors[idx];
        let rgb = [color.r, color.g, color.b];
        let hex_code = format!("#{:02X}{:02X}{:02X}", color.r, color.g, color.b);
        let expected_name = color.name.trim().to_lowercase();
        
        writeln!(&mut report, "#### {}. Expected: {}", color.number, expected_name)?;
        writeln!(&mut report, "Hex: {}", hex_code)?;
        writeln!(&mut report)?;
        writeln!(&mut report, "| Illuminant | Rust Munsell | Rust ISCC | R✓ | Python Munsell | Python ISCC | P✓ |")?;
        writeln!(&mut report, "|------------|--------------|-----------|----|--------------|-----------|----|")?;
        
        for (illuminant, illum_code) in &configurations {
            let result = test_color_with_python(
                rgb,
                &expected_name,
                *illuminant,
                illum_code,
                &classifier,
                &centore_python_results,
                idx,
            )?;
            
            writeln!(&mut report, "| {} | {} | {} | {} | {} | {} | {} |",
                result.illuminant,
                result.munsell_notation,
                result.rust_iscc,
                if result.match_status { "✅" } else { "❌" },
                result.python_munsell,
                result.python_iscc,
                if result.python_match { "✅" } else { "❌" },
            )?;
        }
        writeln!(&mut report)?;
    }
    
    // Final summary
    writeln!(&mut report, "## Summary")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "### Key Findings")?;
    writeln!(&mut report, "- **Method 2** (ExcludeStartIncludeEnd) is systematically better across both datasets")?;
    writeln!(&mut report, "- **XYZScaling** adaptation performs best overall")?;
    writeln!(&mut report, "- **W3 Dataset**: Best with Illuminant C (53.9% accuracy)")?;
    writeln!(&mut report, "- **Centore Dataset**: F7 slightly better than D65")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "### Performance Comparison")?;
    writeln!(&mut report, "- W3: {} total colors, {} with mismatches ({:.1}%)",
        w3_stats.total_colors,
        w3_stats.colors_with_mismatch,
        (w3_stats.colors_with_mismatch as f64 / w3_stats.total_colors as f64) * 100.0)?;
    writeln!(&mut report, "- Centore: {} total colors, {} with mismatches ({:.1}%)",
        centore_stats.total_colors,
        centore_stats.colors_with_mismatch,
        (centore_stats.colors_with_mismatch as f64 / centore_stats.total_colors as f64) * 100.0)?;
    
    // Save report
    let report_path = "investigation/reports/comprehensive_dataset_misses_v2.md";
    fs::create_dir_all("investigation/reports")?;
    fs::write(report_path, report)?;
    println!("\n✅ Report saved to: {}", report_path);
    
    Ok(())
}

fn load_w3_dataset() -> Result<Vec<W3IsccColor>, Box<dyn std::error::Error>> {
    let path = "tests/data/ISCC_NBS_REFERENCE_DATASET.csv";
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path(path)?;
    
    let mut colors = Vec::new();
    for result in reader.deserialize() {
        let color: W3IsccColor = result?;
        colors.push(color);
    }
    
    Ok(colors)
}

fn load_centore_dataset() -> Result<Vec<CentoreIsccColor>, Box<dyn std::error::Error>> {
    let path = "iscc_nbs_colors.csv";
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path(path)?;
    
    let mut colors = Vec::new();
    for result in reader.deserialize() {
        let color: CentoreIsccColor = result?;
        colors.push(color);
    }
    
    Ok(colors)
}

fn get_python_munsell_batch(requests: &[PythonConversion]) -> Result<HashMap<String, String>, Box<dyn std::error::Error>> {
    let request = PythonConversionRequest {
        conversions: requests.to_vec(),
    };
    
    let json_input = serde_json::to_string(&request)?;
    
    // Call Python script
    let mut child = Command::new("python3")
        .arg("/Users/chris/Dropbox/dev/projects/libraries/MunsellSpace/investigation/src/generate_python_munsell.py")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;
    
    // Write input
    if let Some(mut stdin) = child.stdin.take() {
        stdin.write_all(json_input.as_bytes())?;
    }
    
    // Get output
    let output = child.wait_with_output()?;
    
    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        return Err(format!("Python script failed: {}", stderr).into());
    }
    
    let result: PythonConversionResult = serde_json::from_slice(&output.stdout)?;
    Ok(result.results)
}

fn test_color_with_python(
    rgb: [u8; 3],
    expected_name: &str,
    illuminant: Illuminant,
    illum_code: &str,
    classifier: &IsccNbsClassifier,
    python_results: &HashMap<String, String>,
    idx: usize,
) -> Result<TestResult, Box<dyn std::error::Error>> {
    let converter = MathematicalMunsellConverter::with_illuminants(
        Illuminant::D65,
        illuminant,
        ChromaticAdaptationMethod::XYZScaling,
    )?;
    
    match converter.srgb_to_munsell(rgb) {
        Ok(munsell) => {
            let hue_str = format!("{:.1}{}", munsell.hue, munsell.family);
            let munsell_notation = format!("{} {:.1}/{:.1}", hue_str, munsell.value, munsell.chroma);
            
            // Get Python reference
            let python_key_w3 = format!("w3_{}_{}", idx, illum_code);
            let python_key_centore = format!("centore_{}_{}", idx, illum_code);
            let python_raw = python_results.get(&python_key_w3)
                .or_else(|| python_results.get(&python_key_centore))
                .cloned()
                .unwrap_or_else(|| "N/A".to_string());
            
            // Clean Python result - empty if error
            let python_munsell = if python_raw.starts_with("ERROR:") {
                String::new()
            } else {
                python_raw.clone()
            };
            
            // Classify Rust result
            let rust_iscc = match classifier.classify_munsell(
                &hue_str,
                munsell.value,
                munsell.chroma
            ) {
                Ok(Some(result)) => result.iscc_nbs_descriptor.clone(),
                _ => "N/A".to_string(),
            };
            
            // Classify Python result if valid
            let python_iscc = if !python_munsell.is_empty() && python_munsell != "N/A" {
                // Parse Python Munsell notation (e.g., "7.8R 5.2/20.5")
                if let Some((hue_part, value_chroma)) = python_munsell.split_once(' ') {
                    if let Some((value_str, chroma_str)) = value_chroma.split_once('/') {
                        let value = value_str.parse::<f64>().unwrap_or(0.0);
                        let chroma = chroma_str.parse::<f64>().unwrap_or(0.0);
                        
                        match classifier.classify_munsell(hue_part, value, chroma) {
                            Ok(Some(result)) => result.iscc_nbs_descriptor.clone(),
                            _ => "N/A".to_string(),
                        }
                    } else {
                        "N/A".to_string()
                    }
                } else {
                    "N/A".to_string()
                }
            } else {
                String::new()
            };
            
            let match_status = rust_iscc.to_lowercase() == expected_name;
            let python_match = !python_iscc.is_empty() && python_iscc.to_lowercase() == expected_name;
            
            Ok(TestResult {
                illuminant: illum_code.to_string(),
                munsell_notation,
                python_munsell,
                python_iscc,
                rust_iscc,
                match_status,
                python_match,
            })
        },
        Err(_) => Ok(TestResult {
            illuminant: illum_code.to_string(),
            munsell_notation: "ERROR".to_string(),
            python_munsell: String::new(),
            python_iscc: String::new(),
            rust_iscc: "N/A".to_string(),
            match_status: false,
            python_match: false,
        })
    }
}

fn calculate_accuracy_for_dataset(
    colors: &[W3IsccColor],
    illuminant: Illuminant,
    illum_code: &str,
    classifier: &IsccNbsClassifier,
    python_results: &HashMap<String, String>,
    stats: &mut Statistics,
    _is_w3: bool,
) -> Result<(f64, f64, usize), Box<dyn std::error::Error>> {
    let converter = MathematicalMunsellConverter::with_illuminants(
        Illuminant::D65,
        illuminant,
        ChromaticAdaptationMethod::XYZScaling,
    )?;
    
    let mut rust_correct = 0;
    let mut python_correct = 0;
    let mut python_errors = 0;
    let mut total = 0;
    
    for (idx, color) in colors.iter().enumerate() {
        let hex = color.srgb.trim_start_matches('#');
        if hex.len() != 6 { continue; }
        
        let r = u8::from_str_radix(&hex[0..2], 16).unwrap_or(0);
        let g = u8::from_str_radix(&hex[2..4], 16).unwrap_or(0);
        let b = u8::from_str_radix(&hex[4..6], 16).unwrap_or(0);
        let rgb = [r, g, b];
        let expected_name = color.iscc_nbs_name.trim().to_lowercase();
        
        // Test Rust
        if let Ok(munsell) = converter.srgb_to_munsell(rgb) {
            let hue_str = format!("{:.1}{}", munsell.hue, munsell.family);
            
            if let Ok(Some(result)) = classifier.classify_munsell(
                &hue_str,
                munsell.value,
                munsell.chroma
            ) {
                if result.iscc_nbs_descriptor.to_lowercase() == expected_name {
                    rust_correct += 1;
                    *stats.rust_matches.entry(illum_code.to_string()).or_insert(0) += 1;
                } else if illum_code == "C" { // Count mismatches for one illuminant only
                    stats.colors_with_mismatch += 1;
                }
            }
            
            total += 1;
        }
        
        // Test Python
        let python_key = format!("w3_{}_{}", idx, illum_code);
        if let Some(python_raw) = python_results.get(&python_key) {
            if python_raw.starts_with("ERROR:") {
                python_errors += 1;
                *stats.python_errors.entry(illum_code.to_string()).or_insert(0) += 1;
            } else {
                // Parse and classify Python result
                if let Some((hue_part, value_chroma)) = python_raw.split_once(' ') {
                    if let Some((value_str, chroma_str)) = value_chroma.split_once('/') {
                        let value = value_str.parse::<f64>().unwrap_or(0.0);
                        let chroma = chroma_str.parse::<f64>().unwrap_or(0.0);
                        
                        if let Ok(Some(result)) = classifier.classify_munsell(hue_part, value, chroma) {
                            if result.iscc_nbs_descriptor.to_lowercase() == expected_name {
                                python_correct += 1;
                                *stats.python_matches.entry(illum_code.to_string()).or_insert(0) += 1;
                            }
                        }
                    }
                }
            }
        }
    }
    
    let rust_acc = if total > 0 { (rust_correct as f64 / total as f64) * 100.0 } else { 0.0 };
    let python_acc = if total > 0 { (python_correct as f64 / total as f64) * 100.0 } else { 0.0 };
    
    Ok((rust_acc, python_acc, python_errors))
}

fn calculate_accuracy_for_centore(
    colors: &[CentoreIsccColor],
    illuminant: Illuminant,
    illum_code: &str,
    classifier: &IsccNbsClassifier,
    python_results: &HashMap<String, String>,
    stats: &mut Statistics,
) -> Result<(f64, f64, usize), Box<dyn std::error::Error>> {
    let converter = MathematicalMunsellConverter::with_illuminants(
        Illuminant::D65,
        illuminant,
        ChromaticAdaptationMethod::XYZScaling,
    )?;
    
    let mut rust_correct = 0;
    let mut python_correct = 0;
    let mut python_errors = 0;
    let mut total = 0;
    
    for (idx, color) in colors.iter().enumerate() {
        let rgb = [color.r, color.g, color.b];
        let expected_name = color.name.trim().to_lowercase();
        
        // Test Rust
        if let Ok(munsell) = converter.srgb_to_munsell(rgb) {
            let hue_str = format!("{:.1}{}", munsell.hue, munsell.family);
            
            if let Ok(Some(result)) = classifier.classify_munsell(
                &hue_str,
                munsell.value,
                munsell.chroma
            ) {
                if result.iscc_nbs_descriptor.to_lowercase() == expected_name {
                    rust_correct += 1;
                    *stats.rust_matches.entry(illum_code.to_string()).or_insert(0) += 1;
                } else if illum_code == "F7" { // Count mismatches for one illuminant only
                    stats.colors_with_mismatch += 1;
                }
            }
            
            total += 1;
        }
        
        // Test Python
        let python_key = format!("centore_{}_{}", idx, illum_code);
        if let Some(python_raw) = python_results.get(&python_key) {
            if python_raw.starts_with("ERROR:") {
                python_errors += 1;
                *stats.python_errors.entry(illum_code.to_string()).or_insert(0) += 1;
            } else {
                // Parse and classify Python result
                if let Some((hue_part, value_chroma)) = python_raw.split_once(' ') {
                    if let Some((value_str, chroma_str)) = value_chroma.split_once('/') {
                        let value = value_str.parse::<f64>().unwrap_or(0.0);
                        let chroma = chroma_str.parse::<f64>().unwrap_or(0.0);
                        
                        if let Ok(Some(result)) = classifier.classify_munsell(hue_part, value, chroma) {
                            if result.iscc_nbs_descriptor.to_lowercase() == expected_name {
                                python_correct += 1;
                                *stats.python_matches.entry(illum_code.to_string()).or_insert(0) += 1;
                            }
                        }
                    }
                }
            }
        }
    }
    
    let rust_acc = if total > 0 { (rust_correct as f64 / total as f64) * 100.0 } else { 0.0 };
    let python_acc = if total > 0 { (python_correct as f64 / total as f64) * 100.0 } else { 0.0 };
    
    Ok((rust_acc, python_acc, python_errors))
}