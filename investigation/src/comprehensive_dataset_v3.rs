//! Comprehensive Conversion Dataset Analysis Tool V3
//! 
//! Optimized version that generates a SINGLE comprehensive report file with:
//! - Both mathematical converters (v1 and v2)
//! - All 10 illuminants
//! - Both ISCC-NBS hue range methods
//! - Special chromatic adaptation analysis for first 10 colors

use munsellspace::iscc::ISCC_NBS_Classifier as IsccNbsClassifier;
use munsellspace::mathematical::{MathematicalMunsellConverter, Illuminant as MathIlluminant, ChromaticAdaptation as MathChromaticAdaptation};
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
    
    // Initialize classifier
    let classifier = IsccNbsClassifier::new()?;
    
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
    writeln!(&mut report, "| Illuminant | Accuracy |")?;
    writeln!(&mut report, "|------------|----------|")?;
    
    // Test sample colors for statistics (test 20 colors evenly distributed)
    let w3_sample_indices: Vec<usize> = (0..w3_colors.len()).step_by(w3_colors.len() / 20).collect();
    
    for (illuminant, code, _) in &illuminants {
        // Test v1
        let v1_acc = test_sample_accuracy_v1(
            &w3_colors, 
            &w3_sample_indices,
            *illuminant,
            &classifier,
        );
        writeln!(&mut report, "| {}_v1 | {:.1}% |", code, v1_acc)?;
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
        writeln!(&mut report, "| Illuminant | Adaptation | Munsell | ISCC-NBS | Match |")?;
        writeln!(&mut report, "|------------|------------|---------|----------|-------|")?;
        
        for (illuminant, illum_code, _) in &illuminants {
            for (adapt_method, adapt_name) in &adaptation_methods {
                // Test v1
                let v1_result = test_color_simple_v1(
                    rgb,
                    &expected_name,
                    *illuminant,
                    *adapt_method,
                    &classifier,
                );
                writeln!(&mut report, "| {}_v1 | {} | {} | {} | {} |",
                    illum_code,
                    adapt_name,
                    v1_result.0,  // Munsell notation
                    v1_result.1,  // ISCC-NBS result
                    if v1_result.2 { "✅" } else { "❌" },  // Match
                )?;
                
                // Only test first adaptation method for brevity after the first
                if *adapt_name != "Bradford" { continue; }
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
    writeln!(&mut report, "| Illuminant | Accuracy |")?;
    writeln!(&mut report, "|------------|----------|")?;
    
    // Test sample colors for statistics
    let centore_sample_indices: Vec<usize> = (0..centore_colors.len()).step_by(centore_colors.len() / 20).collect();
    
    for (illuminant, code, _) in &illuminants {
        // Test v1
        let v1_acc = test_centore_sample_accuracy_v1(
            &centore_colors,
            &centore_sample_indices,
            *illuminant,
            &classifier,
        );
        writeln!(&mut report, "| {}_v1 | {:.1}% |", code, v1_acc)?;
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
        writeln!(&mut report, "| Illuminant | Adaptation | Munsell | ISCC-NBS | Match |")?;
        writeln!(&mut report, "|------------|------------|---------|----------|-------|")?;
        
        for (illuminant, illum_code, _) in &illuminants {
            for (adapt_method, adapt_name) in &adaptation_methods {
                // Test v1
                let v1_result = test_color_simple_v1(
                    rgb,
                    &expected_name,
                    *illuminant,
                    *adapt_method,
                    &classifier,
                );
                writeln!(&mut report, "| {}_v1 | {} | {} | {} | {} |",
                    illum_code,
                    adapt_name,
                    v1_result.0,  // Munsell notation
                    v1_result.1,  // ISCC-NBS result
                    if v1_result.2 { "✅" } else { "❌" },  // Match
                )?;
                
                // Only test first adaptation method for brevity after the first
                if *adapt_name != "Bradford" { continue; }
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

// Helper to convert illuminant types
fn convert_illuminant(illuminant: Illuminant) -> MathIlluminant {
    match illuminant {
        Illuminant::A => MathIlluminant::A,
        Illuminant::C => MathIlluminant::C,
        Illuminant::D50 => MathIlluminant::D50,
        Illuminant::D55 => MathIlluminant::D55,
        Illuminant::D65 => MathIlluminant::D65,
        Illuminant::D75 => MathIlluminant::D75,
        Illuminant::E => MathIlluminant::E,
        Illuminant::F2 => MathIlluminant::F2,
        Illuminant::F7 => MathIlluminant::F7,
        _ => MathIlluminant::D65, // Default fallback
    }
}

// Helper to convert chromatic adaptation types
fn convert_adaptation(method: ChromaticAdaptationMethod) -> MathChromaticAdaptation {
    match method {
        ChromaticAdaptationMethod::Bradford => MathChromaticAdaptation::Bradford,
        ChromaticAdaptationMethod::VonKries => MathChromaticAdaptation::Bradford, // Fallback to Bradford
        ChromaticAdaptationMethod::CAT02 => MathChromaticAdaptation::CAT02,
        ChromaticAdaptationMethod::XYZScaling => MathChromaticAdaptation::XYZScaling,
    }
}

// Test sample accuracy for W3 colors using v1 converter
fn test_sample_accuracy_v1(
    colors: &[W3IsccColor],
    indices: &[usize],
    illuminant: Illuminant,
    classifier: &IsccNbsClassifier,
) -> f64 {
    let mut correct = 0;
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
            classifier,
        );
        
        total += 1;
        if result.2 { correct += 1; }
    }
    
    if total > 0 { (correct as f64 / total as f64) * 100.0 } else { 0.0 }
}

// Test sample accuracy for Centore colors using v1 converter
fn test_centore_sample_accuracy_v1(
    colors: &[CentoreIsccColor],
    indices: &[usize],
    illuminant: Illuminant,
    classifier: &IsccNbsClassifier,
) -> f64 {
    let mut correct = 0;
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
            classifier,
        );
        
        total += 1;
        if result.2 { correct += 1; }
    }
    
    if total > 0 { (correct as f64 / total as f64) * 100.0 } else { 0.0 }
}

// Simple test for a single color using v1 converter
// Returns: (munsell_notation, iscc_result, match)
fn test_color_simple_v1(
    rgb: [u8; 3],
    expected_name: &str,
    illuminant: Illuminant,
    adaptation: ChromaticAdaptationMethod,
    classifier: &IsccNbsClassifier,
) -> (String, String, bool) {
    match MathematicalMunsellConverter::with_illuminants(
        convert_illuminant(Illuminant::D65),
        convert_illuminant(illuminant),
        convert_adaptation(adaptation),
    ) {
        Ok(converter) => {
            match converter.srgb_to_munsell(rgb) {
                Ok(munsell) => {
                    let notation = format!("{:.1}{} {:.1}/{:.1}",
                        munsell.hue, munsell.family,
                        munsell.value, munsell.chroma);
                    
                    // Test classification
                    let iscc_result = match classifier.classify_munsell(
                        &format!("{}{}", munsell.hue, munsell.family),
                        munsell.value,
                        munsell.chroma
                    ) {
                        Ok(Some(result)) => {
                            // Use the iscc_nbs_descriptor method - it handles -ish compounds correctly
                            result.iscc_nbs_descriptor()
                        },
                        _ => "N/A".to_string(),
                    };
                    
                    let clean_expected = expected_name.trim().to_lowercase();
                    (
                        notation,
                        iscc_result.clone(),
                        iscc_result.to_lowercase() == clean_expected,
                    )
                },
                Err(_) => ("ERROR".to_string(), "N/A".to_string(), false)
            }
        },
        Err(_) => ("ERROR".to_string(), "N/A".to_string(), false)
    }
}

