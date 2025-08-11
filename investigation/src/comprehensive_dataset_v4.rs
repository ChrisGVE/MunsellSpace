//! Comprehensive Conversion Dataset Analysis Tool V4
//! 
//! Tests ALL combinations and outputs only matches
//! - Both mathematical converters (v1 and v2)
//! - All 10 illuminants
//! - All 4 chromatic adaptation methods
//! - Both ISCC-NBS hue range methods
//! - Shows only rows where classification matches

use munsellspace::iscc::ISCC_NBS_Classifier as IsccNbsClassifier;
use munsellspace::HueRangeMethod;
use munsellspace::mathematical::MathematicalMunsellConverter;
use munsellspace::mathematical_v2::{MathematicalMunsellConverter as MathematicalMunsellConverterV2, MunsellConfig};
use munsellspace::illuminants::{Illuminant, ChromaticAdaptationMethod};
use std::fmt::Write;
use std::fs;
use csv::ReaderBuilder;
use serde::Deserialize;

/// W3 ISCC-NBS reference color entry
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

/// Paul Centore ISCC-NBS color entry
#[derive(Debug, Deserialize, Clone)]
struct CentoreIsccColor {
    number: u16,
    name: String,
    r: u8,
    g: u8,
    b: u8,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 Generating Comprehensive Conversion Dataset Analysis V4");
    println!("==========================================================");
    
    // Load datasets
    let w3_colors = load_w3_dataset()?;
    let centore_colors = load_centore_dataset()?;
    
    println!("📊 Loaded {} W3 colors and {} Centore colors", w3_colors.len(), centore_colors.len());
    
    // Define illuminants
    let illuminants = vec![
        (Illuminant::A, "A", "Incandescent/Tungsten (2856K)"),
        (Illuminant::C, "C", "Average Daylight (6774K)"),
        (Illuminant::D50, "D50", "Horizon Light (5003K)"),
        (Illuminant::D55, "D55", "Mid-morning Daylight (5503K)"),
        (Illuminant::D65, "D65", "Noon Daylight (6504K)"),
        (Illuminant::D75, "D75", "North Sky Daylight (7504K)"),
        (Illuminant::E, "E", "Equal Energy"),
        (Illuminant::F2, "F2", "Cool White Fluorescent"),
        (Illuminant::F7, "F7", "D65 Simulator Fluorescent"),
        (Illuminant::F11, "F11", "Narrow Band Fluorescent"),
    ];
    
    // Define chromatic adaptation methods
    let adaptation_methods = vec![
        (ChromaticAdaptationMethod::Bradford, "Bradford"),
        (ChromaticAdaptationMethod::VonKries, "VonKries"),
        (ChromaticAdaptationMethod::CAT02, "CAT02"),
        (ChromaticAdaptationMethod::XYZScaling, "XYZScaling"),
    ];
    
    // Initialize classifiers
    let method1_classifier = IsccNbsClassifier::new_with_hue_range_method(
        HueRangeMethod::IncludeStartExcludeEnd
    )?;
    let method2_classifier = IsccNbsClassifier::new_with_hue_range_method(
        HueRangeMethod::ExcludeStartIncludeEnd
    )?;
    
    // Create comprehensive report
    let mut report = String::new();
    
    // Header
    writeln!(&mut report, "# Comprehensive Conversion Dataset Analysis")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "## Illuminant Descriptions")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Code | Illuminant | Description | Mathematical Method |")?;
    writeln!(&mut report, "|------|------------|-------------|---------------------|")?;
    
    for (_, code, desc) in &illuminants {
        writeln!(&mut report, "| {}_v1 | {} | {} | mathematical.rs (Original) |", code, code, desc)?;
        writeln!(&mut report, "| {}_v2 | {} | {} | mathematical_v2.rs (V2) |", code, code, desc)?;
    }
    writeln!(&mut report)?;
    
    // Process W3 Dataset
    println!("\n🧪 Processing W3 ISCC-NBS dataset...");
    writeln!(&mut report, "## W3 ISCC-NBS Dataset ({} colors)", w3_colors.len())?;
    writeln!(&mut report)?;
    
    // Calculate and display statistics for W3
    let w3_stats = calculate_w3_statistics(
        &w3_colors,
        &illuminants,
        &adaptation_methods,
        &method1_classifier,
        &method2_classifier,
    )?;
    
    writeln!(&mut report, "### Summary Statistics")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Illuminant | Adaptation | Method 1 Accuracy | Method 2 Accuracy | Total Tested |")?;
    writeln!(&mut report, "|------------|------------|-------------------|-------------------|--------------|")?;
    
    for ((illum_code, adapt_name), stats) in &w3_stats {
        writeln!(&mut report, "| {} | {} | {:.1}% ({}/{}) | {:.1}% ({}/{}) | {} |",
            illum_code, adapt_name,
            stats.0, stats.1, stats.4,  // Method 1 accuracy
            stats.2, stats.3, stats.4,  // Method 2 accuracy
            stats.4,  // Total tested
        )?;
    }
    writeln!(&mut report)?;
    
    // Detailed results for W3 colors (only showing matches)
    writeln!(&mut report, "### Detailed Results (Showing Matches Only)")?;
    writeln!(&mut report)?;
    
    for (idx, color) in w3_colors.iter().enumerate() {
        let hex = color.srgb.trim_start_matches('#');
        if hex.len() != 6 { continue; }
        
        let r = u8::from_str_radix(&hex[0..2], 16)?;
        let g = u8::from_str_radix(&hex[2..4], 16)?;
        let b = u8::from_str_radix(&hex[4..6], 16)?;
        let rgb = [r, g, b];
        let hex_code = format!("#{:02X}{:02X}{:02X}", r, g, b);
        let expected_name = color.iscc_nbs_name.trim().to_lowercase();
        
        writeln!(&mut report, "#### {}. {} - Expected: {}", idx + 1, hex_code, expected_name)?;
        writeln!(&mut report)?;
        
        let mut has_matches = false;
        let mut match_table = String::new();
        
        writeln!(&mut match_table, "| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |")?;
        writeln!(&mut match_table, "|------------|------------|---------|----------|-----|----------|-----|")?;
        
        // Test all combinations
        for (illuminant, illum_code, _) in &illuminants {
            for (adapt_method, adapt_name) in &adaptation_methods {
                // Test v1
                let v1_result = test_color_v1(
                    rgb,
                    &expected_name,
                    *illuminant,
                    *adapt_method,
                    &method1_classifier,
                    &method2_classifier,
                );
                
                if v1_result.2 || v1_result.4 {  // If either method matches
                    has_matches = true;
                    writeln!(&mut match_table, "| {}_v1 | {} | {} | {} | {} | {} | {} |",
                        illum_code,
                        adapt_name,
                        v1_result.0,
                        v1_result.1,
                        if v1_result.2 { "✅" } else { "❌" },
                        v1_result.3,
                        if v1_result.4 { "✅" } else { "❌" },
                    )?;
                }
                
                // Test v2
                let v2_result = test_color_v2(
                    rgb,
                    &expected_name,
                    *illuminant,
                    *adapt_method,
                    &method1_classifier,
                    &method2_classifier,
                );
                
                if v2_result.2 || v2_result.4 {  // If either method matches
                    has_matches = true;
                    writeln!(&mut match_table, "| {}_v2 | {} | {} | {} | {} | {} | {} |",
                        illum_code,
                        adapt_name,
                        v2_result.0,
                        v2_result.1,
                        if v2_result.2 { "✅" } else { "❌" },
                        v2_result.3,
                        if v2_result.4 { "✅" } else { "❌" },
                    )?;
                }
            }
        }
        
        if has_matches {
            report.push_str(&match_table);
        } else {
            writeln!(&mut report, "No matches")?;
        }
        writeln!(&mut report)?;
        
        if (idx + 1) % 10 == 0 {
            println!("  Processed {} colors...", idx + 1);
        }
    }
    
    // Process Centore Dataset
    println!("\n🧪 Processing Paul Centore dataset...");
    writeln!(&mut report, "## Paul Centore ISCC-NBS Dataset ({} colors)", centore_colors.len())?;
    writeln!(&mut report)?;
    
    // Calculate and display statistics for Centore
    let centore_stats = calculate_centore_statistics(
        &centore_colors,
        &illuminants,
        &adaptation_methods,
        &method1_classifier,
        &method2_classifier,
    )?;
    
    writeln!(&mut report, "### Summary Statistics")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Illuminant | Adaptation | Method 1 Accuracy | Method 2 Accuracy | Total Tested |")?;
    writeln!(&mut report, "|------------|------------|-------------------|-------------------|--------------|")?;
    
    for ((illum_code, adapt_name), stats) in &centore_stats {
        writeln!(&mut report, "| {} | {} | {:.1}% ({}/{}) | {:.1}% ({}/{}) | {} |",
            illum_code, adapt_name,
            stats.0, stats.1, stats.4,  // Method 1 accuracy
            stats.2, stats.3, stats.4,  // Method 2 accuracy
            stats.4,  // Total tested
        )?;
    }
    writeln!(&mut report)?;
    
    // Detailed results for Centore colors (only showing matches)
    writeln!(&mut report, "### Detailed Results (Showing Matches Only)")?;
    writeln!(&mut report)?;
    
    for (idx, color) in centore_colors.iter().enumerate() {
        let rgb = [color.r, color.g, color.b];
        let hex_code = format!("#{:02X}{:02X}{:02X}", color.r, color.g, color.b);
        let expected_name = color.name.trim().to_lowercase();
        
        writeln!(&mut report, "#### {}. {} - Expected: {}", idx + 1, hex_code, expected_name)?;
        writeln!(&mut report)?;
        
        let mut has_matches = false;
        let mut match_table = String::new();
        
        writeln!(&mut match_table, "| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |")?;
        writeln!(&mut match_table, "|------------|------------|---------|----------|-----|----------|-----|")?;
        
        // Test all combinations
        for (illuminant, illum_code, _) in &illuminants {
            for (adapt_method, adapt_name) in &adaptation_methods {
                // Test v1
                let v1_result = test_color_v1(
                    rgb,
                    &expected_name,
                    *illuminant,
                    *adapt_method,
                    &method1_classifier,
                    &method2_classifier,
                );
                
                if v1_result.2 || v1_result.4 {  // If either method matches
                    has_matches = true;
                    writeln!(&mut match_table, "| {}_v1 | {} | {} | {} | {} | {} | {} |",
                        illum_code,
                        adapt_name,
                        v1_result.0,
                        v1_result.1,
                        if v1_result.2 { "✅" } else { "❌" },
                        v1_result.3,
                        if v1_result.4 { "✅" } else { "❌" },
                    )?;
                }
                
                // Test v2
                let v2_result = test_color_v2(
                    rgb,
                    &expected_name,
                    *illuminant,
                    *adapt_method,
                    &method1_classifier,
                    &method2_classifier,
                );
                
                if v2_result.2 || v2_result.4 {  // If either method matches
                    has_matches = true;
                    writeln!(&mut match_table, "| {}_v2 | {} | {} | {} | {} | {} | {} |",
                        illum_code,
                        adapt_name,
                        v2_result.0,
                        v2_result.1,
                        if v2_result.2 { "✅" } else { "❌" },
                        v2_result.3,
                        if v2_result.4 { "✅" } else { "❌" },
                    )?;
                }
            }
        }
        
        if has_matches {
            report.push_str(&match_table);
        } else {
            writeln!(&mut report, "No matches")?;
        }
        writeln!(&mut report)?;
        
        if (idx + 1) % 10 == 0 {
            println!("  Processed {} colors...", idx + 1);
        }
    }
    
    // Write report to file
    fs::write("COMPREHENSIVE_CONVERSION_DATASET.md", report)?;
    
    println!("\n✅ Report generated: COMPREHENSIVE_CONVERSION_DATASET.md");
    
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
        .from_path("tests/data/MUNSELL_COLOR_SCIENCE_COMPLETE.csv")?;
    
    let mut colors = Vec::new();
    for result in reader.deserialize() {
        let color: CentoreIsccColor = result?;
        colors.push(color);
    }
    
    Ok(colors)
}

// Calculate statistics for W3 dataset
fn calculate_w3_statistics(
    colors: &[W3IsccColor],
    illuminants: &[(Illuminant, &str, &str)],
    adaptation_methods: &[(ChromaticAdaptationMethod, &str)],
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> Result<std::collections::HashMap<(String, String), (f64, usize, f64, usize, usize)>, Box<dyn std::error::Error>> {
    use std::collections::HashMap;
    let mut stats = HashMap::new();
    
    for (illuminant, illum_code, _) in illuminants {
        for (adapt_method, adapt_name) in adaptation_methods {
            let mut v1_m1_correct = 0;
            let mut v1_m2_correct = 0;
            let mut v2_m1_correct = 0;
            let mut v2_m2_correct = 0;
            let mut total = 0;
            
            for color in colors {
                let hex = color.srgb.trim_start_matches('#');
                if hex.len() != 6 { continue; }
                
                let r = u8::from_str_radix(&hex[0..2], 16).unwrap_or(0);
                let g = u8::from_str_radix(&hex[2..4], 16).unwrap_or(0);
                let b = u8::from_str_radix(&hex[4..6], 16).unwrap_or(0);
                let rgb = [r, g, b];
                let expected_name = color.iscc_nbs_name.trim().to_lowercase();
                
                // Test v1
                let v1_result = test_color_v1(
                    rgb,
                    &expected_name,
                    *illuminant,
                    *adapt_method,
                    method1_classifier,
                    method2_classifier,
                );
                if v1_result.2 { v1_m1_correct += 1; }
                if v1_result.4 { v1_m2_correct += 1; }
                
                // Test v2
                let v2_result = test_color_v2(
                    rgb,
                    &expected_name,
                    *illuminant,
                    *adapt_method,
                    method1_classifier,
                    method2_classifier,
                );
                if v2_result.2 { v2_m1_correct += 1; }
                if v2_result.4 { v2_m2_correct += 1; }
                
                total += 1;
            }
            
            // Store stats for v1
            let v1_key = (format!("{}_v1", illum_code), adapt_name.to_string());
            let v1_m1_acc = if total > 0 { (v1_m1_correct as f64 / total as f64) * 100.0 } else { 0.0 };
            let v1_m2_acc = if total > 0 { (v1_m2_correct as f64 / total as f64) * 100.0 } else { 0.0 };
            stats.insert(v1_key, (v1_m1_acc, v1_m1_correct, v1_m2_acc, v1_m2_correct, total));
            
            // Store stats for v2
            let v2_key = (format!("{}_v2", illum_code), adapt_name.to_string());
            let v2_m1_acc = if total > 0 { (v2_m1_correct as f64 / total as f64) * 100.0 } else { 0.0 };
            let v2_m2_acc = if total > 0 { (v2_m2_correct as f64 / total as f64) * 100.0 } else { 0.0 };
            stats.insert(v2_key, (v2_m1_acc, v2_m1_correct, v2_m2_acc, v2_m2_correct, total));
        }
    }
    
    Ok(stats)
}

// Calculate statistics for Centore dataset
fn calculate_centore_statistics(
    colors: &[CentoreIsccColor],
    illuminants: &[(Illuminant, &str, &str)],
    adaptation_methods: &[(ChromaticAdaptationMethod, &str)],
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> Result<std::collections::HashMap<(String, String), (f64, usize, f64, usize, usize)>, Box<dyn std::error::Error>> {
    use std::collections::HashMap;
    let mut stats = HashMap::new();
    
    for (illuminant, illum_code, _) in illuminants {
        for (adapt_method, adapt_name) in adaptation_methods {
            let mut v1_m1_correct = 0;
            let mut v1_m2_correct = 0;
            let mut v2_m1_correct = 0;
            let mut v2_m2_correct = 0;
            let mut total = 0;
            
            for color in colors {
                let rgb = [color.r, color.g, color.b];
                let expected_name = color.name.trim().to_lowercase();
                
                // Test v1
                let v1_result = test_color_v1(
                    rgb,
                    &expected_name,
                    *illuminant,
                    *adapt_method,
                    method1_classifier,
                    method2_classifier,
                );
                if v1_result.2 { v1_m1_correct += 1; }
                if v1_result.4 { v1_m2_correct += 1; }
                
                // Test v2
                let v2_result = test_color_v2(
                    rgb,
                    &expected_name,
                    *illuminant,
                    *adapt_method,
                    method1_classifier,
                    method2_classifier,
                );
                if v2_result.2 { v2_m1_correct += 1; }
                if v2_result.4 { v2_m2_correct += 1; }
                
                total += 1;
            }
            
            // Store stats for v1
            let v1_key = (format!("{}_v1", illum_code), adapt_name.to_string());
            let v1_m1_acc = if total > 0 { (v1_m1_correct as f64 / total as f64) * 100.0 } else { 0.0 };
            let v1_m2_acc = if total > 0 { (v1_m2_correct as f64 / total as f64) * 100.0 } else { 0.0 };
            stats.insert(v1_key, (v1_m1_acc, v1_m1_correct, v1_m2_acc, v1_m2_correct, total));
            
            // Store stats for v2
            let v2_key = (format!("{}_v2", illum_code), adapt_name.to_string());
            let v2_m1_acc = if total > 0 { (v2_m1_correct as f64 / total as f64) * 100.0 } else { 0.0 };
            let v2_m2_acc = if total > 0 { (v2_m2_correct as f64 / total as f64) * 100.0 } else { 0.0 };
            stats.insert(v2_key, (v2_m1_acc, v2_m1_correct, v2_m2_acc, v2_m2_correct, total));
        }
    }
    
    Ok(stats)
}

// Test a single color using v1 converter
// Returns: (munsell_notation, method1_result, method1_match, method2_result, method2_match)
fn test_color_v1(
    rgb: [u8; 3],
    expected_name: &str,
    illuminant: Illuminant,
    adaptation: ChromaticAdaptationMethod,
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> (String, String, bool, String, bool) {
    match MathematicalMunsellConverter::with_illuminants(
        Illuminant::D65,
        illuminant,
        adaptation,
    ) {
        Ok(converter) => {
            match converter.srgb_to_munsell(rgb) {
                Ok(munsell) => {
                    let notation = format!("{:.1}{} {:.1}/{:.1}",
                        munsell.hue, munsell.family,
                        munsell.value, munsell.chroma);
                    
                    // Debug invalid families
                    let hue_str = format!("{}{}", munsell.hue, munsell.family);
                    if munsell.family == "PR" || munsell.family.len() > 2 || 
                       !["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP", "N"].contains(&munsell.family.as_str()) {
                        eprintln!("ERROR: Invalid family '{}' for RGB {:?}, hue_str: '{}'", 
                            munsell.family, rgb, hue_str);
                    }
                    
                    // Test Method 1
                    let method1_result = match method1_classifier.classify_munsell(
                        &hue_str,
                        munsell.value,
                        munsell.chroma
                    ) {
                        Ok(Some(result)) => {
                            // Use the iscc_nbs_descriptor directly - it handles -ish compounds correctly
                            result.iscc_nbs_descriptor.clone()
                        },
                        _ => "N/A".to_string(),
                    };
                    
                    // Test Method 2
                    let method2_result = match method2_classifier.classify_munsell(
                        &hue_str,
                        munsell.value,
                        munsell.chroma
                    ) {
                        Ok(Some(result)) => {
                            // Use the iscc_nbs_descriptor directly - it handles -ish compounds correctly
                            result.iscc_nbs_descriptor.clone()
                        },
                        _ => "N/A".to_string(),
                    };
                    
                    let clean_expected = expected_name.trim().to_lowercase();
                    (
                        notation,
                        method1_result.clone(),
                        method1_result.to_lowercase() == clean_expected,
                        method2_result.clone(),
                        method2_result.to_lowercase() == clean_expected,
                    )
                },
                Err(_) => ("ERROR".to_string(), "N/A".to_string(), false, "N/A".to_string(), false)
            }
        },
        Err(_) => ("ERROR".to_string(), "N/A".to_string(), false, "N/A".to_string(), false)
    }
}

// Test a single color using v2 converter
fn test_color_v2(
    rgb: [u8; 3],
    expected_name: &str,
    illuminant: Illuminant,
    adaptation: ChromaticAdaptationMethod,
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> (String, String, bool, String, bool) {
    let config = MunsellConfig {
        source_illuminant: Illuminant::D65,
        target_illuminant: illuminant,
        adaptation_method: adaptation,
    };
    
    match MathematicalMunsellConverterV2::with_config(config) {
        Ok(converter) => {
            match converter.srgb_to_munsell(rgb) {
                Ok(munsell) => {
                    let notation = format!("{:.1}{} {:.1}/{:.1}",
                        munsell.hue, munsell.family,
                        munsell.value, munsell.chroma);
                    
                    // Debug invalid families
                    let hue_str = format!("{}{}", munsell.hue, munsell.family);
                    if munsell.family == "PR" || munsell.family.len() > 2 || 
                       !["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP", "N"].contains(&munsell.family.as_str()) {
                        eprintln!("ERROR: Invalid family '{}' for RGB {:?}, hue_str: '{}'", 
                            munsell.family, rgb, hue_str);
                    }
                    
                    // Test Method 1
                    let method1_result = match method1_classifier.classify_munsell(
                        &hue_str,
                        munsell.value,
                        munsell.chroma
                    ) {
                        Ok(Some(result)) => {
                            // Use the iscc_nbs_descriptor directly - it handles -ish compounds correctly
                            result.iscc_nbs_descriptor.clone()
                        },
                        _ => "N/A".to_string(),
                    };
                    
                    // Test Method 2
                    let method2_result = match method2_classifier.classify_munsell(
                        &hue_str,
                        munsell.value,
                        munsell.chroma
                    ) {
                        Ok(Some(result)) => {
                            // Use the iscc_nbs_descriptor directly - it handles -ish compounds correctly
                            result.iscc_nbs_descriptor.clone()
                        },
                        _ => "N/A".to_string(),
                    };
                    
                    let clean_expected = expected_name.trim().to_lowercase();
                    (
                        notation,
                        method1_result.clone(),
                        method1_result.to_lowercase() == clean_expected,
                        method2_result.clone(),
                        method2_result.to_lowercase() == clean_expected,
                    )
                },
                Err(_) => ("ERROR".to_string(), "N/A".to_string(), false, "N/A".to_string(), false)
            }
        },
        Err(_) => ("ERROR".to_string(), "N/A".to_string(), false, "N/A".to_string(), false)
    }
}