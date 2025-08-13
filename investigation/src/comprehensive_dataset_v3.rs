//! Comprehensive Conversion Dataset Analysis Tool V3
//! 
//! Optimized version that generates a SINGLE comprehensive report file with:
//! - Both mathematical converters (v1 and v2)
//! - All 10 illuminants
//! - Both ISCC-NBS hue range methods
//! - Special chromatic adaptation analysis for first 10 colors

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
    println!("🔬 Generating Comprehensive Conversion Dataset Analysis V3");
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
    
    // Define chromatic adaptation methods for first 10 colors
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
    
    // Test sample colors from each dataset with all illuminants
    println!("\n🧪 Testing sample colors with all illuminants...");
    
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
    
    // Test a sample of colors to generate statistics
    println!("📈 Generating accuracy statistics...");
    
    // W3 Dataset Section
    writeln!(&mut report, "## W3 ISCC-NBS Dataset ({} colors)", w3_colors.len())?;
    writeln!(&mut report)?;
    
    // Summary statistics for W3
    writeln!(&mut report, "### Summary Statistics")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Illuminant | Method 1 Accuracy | Method 2 Accuracy |")?;
    writeln!(&mut report, "|------------|-------------------|-------------------|")?;
    
    // Test sample colors for statistics (test 20 colors evenly distributed)
    let w3_sample_indices: Vec<usize> = (0..w3_colors.len()).step_by(w3_colors.len() / 20).collect();
    
    for (illuminant, code, _) in &illuminants {
        // Test v1
        let (v1_m1_acc, v1_m2_acc) = test_sample_accuracy_v1(
            &w3_colors, 
            &w3_sample_indices,
            *illuminant,
            &method1_classifier,
            &method2_classifier,
        );
        writeln!(&mut report, "| {}_v1 | {:.1}% | {:.1}% |", code, v1_m1_acc, v1_m2_acc)?;
        
        // Test v2
        let (v2_m1_acc, v2_m2_acc) = test_sample_accuracy_v2(
            &w3_colors,
            &w3_sample_indices,
            *illuminant,
            &method1_classifier,
            &method2_classifier,
        );
        writeln!(&mut report, "| {}_v2 | {:.1}% | {:.1}% |", code, v2_m1_acc, v2_m2_acc)?;
    }
    writeln!(&mut report)?;
    
    // First 10 colors with chromatic adaptation
    writeln!(&mut report, "### First 10 Colors - Detailed Analysis with Chromatic Adaptation")?;
    writeln!(&mut report)?;
    
    for (idx, color) in w3_colors.iter().take(10).enumerate() {
        let hex = color.srgb.trim_start_matches('#');
        if hex.len() != 6 { continue; }
        
        let r = u8::from_str_radix(&hex[0..2], 16)?;
        let g = u8::from_str_radix(&hex[2..4], 16)?;
        let b = u8::from_str_radix(&hex[4..6], 16)?;
        let rgb = [r, g, b];
        let hex_code = format!("#{:02X}{:02X}{:02X}", r, g, b);
        // Use the ISCC-NBS name directly from the dataset
        let expected_name = color.iscc_nbs_name.trim().to_lowercase();
        
        writeln!(&mut report, "#### {}. {} - Expected: {}", idx + 1, hex_code, expected_name)?;
        writeln!(&mut report)?;
        writeln!(&mut report, "| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |")?;
        writeln!(&mut report, "|------------|------------|---------|----------|-----|----------|-----|")?;
        
        for (illuminant, illum_code, _) in &illuminants {
            for (adapt_method, adapt_name) in &adaptation_methods {
                // Test v1
                let v1_result = test_color_simple_v1(
                    rgb,
                    &expected_name,
                    *illuminant,
                    *adapt_method,
                    &method1_classifier,
                    &method2_classifier,
                );
                writeln!(&mut report, "| {}_v1 | {} | {} | {} | {} | {} | {} |",
                    illum_code,
                    adapt_name,
                    v1_result.0,  // Munsell notation
                    v1_result.1,  // Method 1 result
                    if v1_result.2 { "✅" } else { "❌" },  // Method 1 match
                    v1_result.3,  // Method 2 result
                    if v1_result.4 { "✅" } else { "❌" },  // Method 2 match
                )?;
                
                // Only test first adaptation method for brevity after the first
                if *adapt_name != "Bradford" { continue; }
                
                // Test v2
                let v2_result = test_color_simple_v2(
                    rgb,
                    &expected_name,
                    *illuminant,
                    *adapt_method,
                    &method1_classifier,
                    &method2_classifier,
                );
                writeln!(&mut report, "| {}_v2 | {} | {} | {} | {} | {} | {} |",
                    illum_code,
                    adapt_name,
                    v2_result.0,  // Munsell notation
                    v2_result.1,  // Method 1 result
                    if v2_result.2 { "✅" } else { "❌" },  // Method 1 match
                    v2_result.3,  // Method 2 result
                    if v2_result.4 { "✅" } else { "❌" },  // Method 2 match
                )?;
            }
        }
        writeln!(&mut report)?;
    }
    
    // Paul Centore Dataset Section
    writeln!(&mut report, "## Paul Centore ISCC-NBS Dataset ({} colors)", centore_colors.len())?;
    writeln!(&mut report)?;
    
    // Summary statistics for Centore
    writeln!(&mut report, "### Summary Statistics")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Illuminant | Method 1 Accuracy | Method 2 Accuracy |")?;
    writeln!(&mut report, "|------------|-------------------|-------------------|")?;
    
    // Test sample colors for statistics
    let centore_sample_indices: Vec<usize> = (0..centore_colors.len()).step_by(centore_colors.len() / 20).collect();
    
    for (illuminant, code, _) in &illuminants {
        // Test v1
        let (v1_m1_acc, v1_m2_acc) = test_centore_sample_accuracy_v1(
            &centore_colors,
            &centore_sample_indices,
            *illuminant,
            &method1_classifier,
            &method2_classifier,
        );
        writeln!(&mut report, "| {}_v1 | {:.1}% | {:.1}% |", code, v1_m1_acc, v1_m2_acc)?;
        
        // Test v2
        let (v2_m1_acc, v2_m2_acc) = test_centore_sample_accuracy_v2(
            &centore_colors,
            &centore_sample_indices,
            *illuminant,
            &method1_classifier,
            &method2_classifier,
        );
        writeln!(&mut report, "| {}_v2 | {:.1}% | {:.1}% |", code, v2_m1_acc, v2_m2_acc)?;
    }
    writeln!(&mut report)?;
    
    // First 10 colors with chromatic adaptation
    writeln!(&mut report, "### First 10 Colors - Detailed Analysis with Chromatic Adaptation")?;
    writeln!(&mut report)?;
    
    for (idx, color) in centore_colors.iter().take(10).enumerate() {
        let rgb = [color.r, color.g, color.b];
        let hex_code = format!("#{:02X}{:02X}{:02X}", color.r, color.g, color.b);
        let expected_name = color.name.clone();
        
        writeln!(&mut report, "#### {}. {} - Expected: {}", idx + 1, hex_code, expected_name)?;
        writeln!(&mut report)?;
        writeln!(&mut report, "| Illuminant | Adaptation | Munsell | Method 1 | M1✓ | Method 2 | M2✓ |")?;
        writeln!(&mut report, "|------------|------------|---------|----------|-----|----------|-----|")?;
        
        for (illuminant, illum_code, _) in &illuminants {
            for (adapt_method, adapt_name) in &adaptation_methods {
                // Test v1
                let v1_result = test_color_simple_v1(
                    rgb,
                    &expected_name,
                    *illuminant,
                    *adapt_method,
                    &method1_classifier,
                    &method2_classifier,
                );
                writeln!(&mut report, "| {}_v1 | {} | {} | {} | {} | {} | {} |",
                    illum_code,
                    adapt_name,
                    v1_result.0,  // Munsell notation
                    v1_result.1,  // Method 1 result
                    if v1_result.2 { "✅" } else { "❌" },  // Method 1 match
                    v1_result.3,  // Method 2 result
                    if v1_result.4 { "✅" } else { "❌" },  // Method 2 match
                )?;
                
                // Only test first adaptation method for brevity after the first
                if *adapt_name != "Bradford" { continue; }
                
                // Test v2
                let v2_result = test_color_simple_v2(
                    rgb,
                    &expected_name,
                    *illuminant,
                    *adapt_method,
                    &method1_classifier,
                    &method2_classifier,
                );
                writeln!(&mut report, "| {}_v2 | {} | {} | {} | {} | {} | {} |",
                    illum_code,
                    adapt_name,
                    v2_result.0,  // Munsell notation
                    v2_result.1,  // Method 1 result
                    if v2_result.2 { "✅" } else { "❌" },  // Method 1 match
                    v2_result.3,  // Method 2 result
                    if v2_result.4 { "✅" } else { "❌" },  // Method 2 match
                )?;
            }
        }
        writeln!(&mut report)?;
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

// Test sample accuracy for W3 colors using v1 converter
fn test_sample_accuracy_v1(
    colors: &[W3IsccColor],
    indices: &[usize],
    illuminant: Illuminant,
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> (f64, f64) {
    let mut method1_correct = 0;
    let mut method2_correct = 0;
    let mut total = 0;
    
    for &idx in indices {
        if idx >= colors.len() { continue; }
        let color = &colors[idx];
        
        let hex = color.srgb.trim_start_matches('#');
        if hex.len() != 6 { continue; }
        
        let r = u8::from_str_radix(&hex[0..2], 16).unwrap_or(0);
        let g = u8::from_str_radix(&hex[2..4], 16).unwrap_or(0);
        let b = u8::from_str_radix(&hex[4..6], 16).unwrap_or(0);
        let rgb = [r, g, b];
        // Use the ISCC-NBS name directly from the dataset
        let expected_name = color.iscc_nbs_name.trim().to_lowercase();
        
        let result = test_color_simple_v1(
            rgb,
            &expected_name,
            illuminant,
            ChromaticAdaptationMethod::Bradford,
            method1_classifier,
            method2_classifier,
        );
        
        total += 1;
        if result.2 { method1_correct += 1; }
        if result.4 { method2_correct += 1; }
    }
    
    let m1_acc = if total > 0 { (method1_correct as f64 / total as f64) * 100.0 } else { 0.0 };
    let m2_acc = if total > 0 { (method2_correct as f64 / total as f64) * 100.0 } else { 0.0 };
    
    (m1_acc, m2_acc)
}

// Test sample accuracy for W3 colors using v2 converter
fn test_sample_accuracy_v2(
    colors: &[W3IsccColor],
    indices: &[usize],
    illuminant: Illuminant,
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> (f64, f64) {
    let mut method1_correct = 0;
    let mut method2_correct = 0;
    let mut total = 0;
    
    for &idx in indices {
        if idx >= colors.len() { continue; }
        let color = &colors[idx];
        
        let hex = color.srgb.trim_start_matches('#');
        if hex.len() != 6 { continue; }
        
        let r = u8::from_str_radix(&hex[0..2], 16).unwrap_or(0);
        let g = u8::from_str_radix(&hex[2..4], 16).unwrap_or(0);
        let b = u8::from_str_radix(&hex[4..6], 16).unwrap_or(0);
        let rgb = [r, g, b];
        // Use the ISCC-NBS name directly from the dataset
        let expected_name = color.iscc_nbs_name.trim().to_lowercase();
        
        let result = test_color_simple_v2(
            rgb,
            &expected_name,
            illuminant,
            ChromaticAdaptationMethod::Bradford,
            method1_classifier,
            method2_classifier,
        );
        
        total += 1;
        if result.2 { method1_correct += 1; }
        if result.4 { method2_correct += 1; }
    }
    
    let m1_acc = if total > 0 { (method1_correct as f64 / total as f64) * 100.0 } else { 0.0 };
    let m2_acc = if total > 0 { (method2_correct as f64 / total as f64) * 100.0 } else { 0.0 };
    
    (m1_acc, m2_acc)
}

// Test sample accuracy for Centore colors using v1 converter
fn test_centore_sample_accuracy_v1(
    colors: &[CentoreIsccColor],
    indices: &[usize],
    illuminant: Illuminant,
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> (f64, f64) {
    let mut method1_correct = 0;
    let mut method2_correct = 0;
    let mut total = 0;
    
    for &idx in indices {
        if idx >= colors.len() { continue; }
        let color = &colors[idx];
        
        let rgb = [color.r, color.g, color.b];
        let expected_name = color.name.clone();
        
        let result = test_color_simple_v1(
            rgb,
            &expected_name,
            illuminant,
            ChromaticAdaptationMethod::Bradford,
            method1_classifier,
            method2_classifier,
        );
        
        total += 1;
        if result.2 { method1_correct += 1; }
        if result.4 { method2_correct += 1; }
    }
    
    let m1_acc = if total > 0 { (method1_correct as f64 / total as f64) * 100.0 } else { 0.0 };
    let m2_acc = if total > 0 { (method2_correct as f64 / total as f64) * 100.0 } else { 0.0 };
    
    (m1_acc, m2_acc)
}

// Test sample accuracy for Centore colors using v2 converter
fn test_centore_sample_accuracy_v2(
    colors: &[CentoreIsccColor],
    indices: &[usize],
    illuminant: Illuminant,
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> (f64, f64) {
    let mut method1_correct = 0;
    let mut method2_correct = 0;
    let mut total = 0;
    
    for &idx in indices {
        if idx >= colors.len() { continue; }
        let color = &colors[idx];
        
        let rgb = [color.r, color.g, color.b];
        let expected_name = color.name.clone();
        
        let result = test_color_simple_v2(
            rgb,
            &expected_name,
            illuminant,
            ChromaticAdaptationMethod::Bradford,
            method1_classifier,
            method2_classifier,
        );
        
        total += 1;
        if result.2 { method1_correct += 1; }
        if result.4 { method2_correct += 1; }
    }
    
    let m1_acc = if total > 0 { (method1_correct as f64 / total as f64) * 100.0 } else { 0.0 };
    let m2_acc = if total > 0 { (method2_correct as f64 / total as f64) * 100.0 } else { 0.0 };
    
    (m1_acc, m2_acc)
}

// Simple test for a single color using v1 converter
// Returns: (munsell_notation, method1_result, method1_match, method2_result, method2_match)
fn test_color_simple_v1(
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
                    
                    // Test Method 1
                    let method1_result = match method1_classifier.classify_munsell(
                        &format!("{}{}", munsell.hue, munsell.family),
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
                        &format!("{}{}", munsell.hue, munsell.family),
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

// Simple test for a single color using v2 converter
fn test_color_simple_v2(
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
                    
                    // Test Method 1
                    let method1_result = match method1_classifier.classify_munsell(
                        &format!("{}{}", munsell.hue, munsell.family),
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
                        &format!("{}{}", munsell.hue, munsell.family),
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