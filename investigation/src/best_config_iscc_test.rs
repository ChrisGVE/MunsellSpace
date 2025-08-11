//! Best Configuration ISCC-NBS Test
//! 
//! Tests only the best configuration identified from previous testing:
//! - Mathematical v1 (Original) converter
//! - Illuminant C (Munsell standard)
//! - Bradford adaptation
//! - Method 2 (ExcludeStartIncludeEnd) hue range

use munsellspace::iscc::ISCC_NBS_Classifier as IsccNbsClassifier;
use munsellspace::HueRangeMethod;
use munsellspace::mathematical::MathematicalMunsellConverter;
use munsellspace::illuminants::{Illuminant, ChromaticAdaptationMethod};
use csv::ReaderBuilder;
use serde::Deserialize;
use std::fs;
use std::fmt::Write;

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

#[derive(Debug)]
struct ColorMatch {
    hex: String,
    expected_name: String,
    munsell: String,
    predicted_name: String,
    is_match: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 Best Configuration ISCC-NBS Test");
    println!("===================================");
    println!("Configuration: Mathematical v1, Illuminant C, Bradford, Method 2");
    println!();
    
    // Load datasets
    let w3_colors = load_w3_dataset()?;
    let centore_colors = load_centore_dataset()?;
    
    println!("📊 Loaded {} W3 colors and {} Centore colors", w3_colors.len(), centore_colors.len());
    
    // Create converter and classifier
    let converter = MathematicalMunsellConverter::with_illuminants(
        Illuminant::D65,
        Illuminant::C,
        ChromaticAdaptationMethod::Bradford,
    )?;
    
    let classifier = IsccNbsClassifier::new_with_hue_range_method(
        HueRangeMethod::ExcludeStartIncludeEnd
    )?;
    
    // Test W3 Dataset
    println!("\n🧪 Testing W3 ISCC-NBS dataset...");
    let mut w3_matches = Vec::new();
    let mut w3_mismatches = Vec::new();
    let mut w3_total = 0;
    
    for color in &w3_colors {
        let hex = color.srgb.trim_start_matches('#');
        if hex.len() != 6 { continue; }
        
        let r = u8::from_str_radix(&hex[0..2], 16)?;
        let g = u8::from_str_radix(&hex[2..4], 16)?;
        let b = u8::from_str_radix(&hex[4..6], 16)?;
        let rgb = [r, g, b];
        let hex_code = format!("#{:02X}{:02X}{:02X}", r, g, b);
        let expected_name = color.iscc_nbs_name.trim().to_lowercase();
        
        match converter.srgb_to_munsell(rgb) {
            Ok(munsell) => {
                let hue_str = format!("{:.1}{}", munsell.hue, munsell.family);
                let munsell_notation = format!("{} {:.1}/{:.1}", hue_str, munsell.value, munsell.chroma);
                
                if let Ok(Some(result)) = classifier.classify_munsell(
                    &hue_str,
                    munsell.value,
                    munsell.chroma
                ) {
                    let predicted_name = result.iscc_nbs_descriptor.to_lowercase();
                    let is_match = predicted_name == expected_name;
                    
                    let color_match = ColorMatch {
                        hex: hex_code,
                        expected_name: expected_name.clone(),
                        munsell: munsell_notation,
                        predicted_name: predicted_name.clone(),
                        is_match,
                    };
                    
                    if is_match {
                        w3_matches.push(color_match);
                    } else {
                        w3_mismatches.push(color_match);
                    }
                    
                    w3_total += 1;
                }
            },
            Err(_) => {}
        }
    }
    
    let w3_accuracy = (w3_matches.len() as f64 / w3_total as f64) * 100.0;
    println!("  ✅ Matches: {}/{} ({:.1}%)", w3_matches.len(), w3_total, w3_accuracy);
    
    // Test Centore Dataset
    println!("\n🧪 Testing Paul Centore dataset...");
    let mut centore_matches = Vec::new();
    let mut centore_mismatches = Vec::new();
    let mut centore_total = 0;
    
    for color in &centore_colors {
        let rgb = [color.r, color.g, color.b];
        let hex_code = format!("#{:02X}{:02X}{:02X}", color.r, color.g, color.b);
        let expected_name = color.name.trim().to_lowercase();
        
        match converter.srgb_to_munsell(rgb) {
            Ok(munsell) => {
                let hue_str = format!("{:.1}{}", munsell.hue, munsell.family);
                let munsell_notation = format!("{} {:.1}/{:.1}", hue_str, munsell.value, munsell.chroma);
                
                if let Ok(Some(result)) = classifier.classify_munsell(
                    &hue_str,
                    munsell.value,
                    munsell.chroma
                ) {
                    let predicted_name = result.iscc_nbs_descriptor.to_lowercase();
                    let is_match = predicted_name == expected_name;
                    
                    let color_match = ColorMatch {
                        hex: hex_code,
                        expected_name: expected_name.clone(),
                        munsell: munsell_notation,
                        predicted_name: predicted_name.clone(),
                        is_match,
                    };
                    
                    if is_match {
                        centore_matches.push(color_match);
                    } else {
                        centore_mismatches.push(color_match);
                    }
                    
                    centore_total += 1;
                }
            },
            Err(_) => {}
        }
    }
    
    let centore_accuracy = (centore_matches.len() as f64 / centore_total as f64) * 100.0;
    println!("  ✅ Matches: {}/{} ({:.1}%)", centore_matches.len(), centore_total, centore_accuracy);
    
    // Generate report
    let mut report = String::new();
    
    writeln!(&mut report, "# Best Configuration ISCC-NBS Test Results")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "## Configuration")?;
    writeln!(&mut report, "- **Converter**: Mathematical v1 (Original)")?;
    writeln!(&mut report, "- **Illuminant**: C (Munsell standard, 6774K)")?;
    writeln!(&mut report, "- **Adaptation**: Bradford")?;
    writeln!(&mut report, "- **Hue Range Method**: Method 2 (ExcludeStartIncludeEnd)")?;
    writeln!(&mut report)?;
    
    writeln!(&mut report, "## Summary")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Dataset | Matches | Total | Accuracy |")?;
    writeln!(&mut report, "|---------|---------|-------|----------|")?;
    writeln!(&mut report, "| W3 ISCC-NBS | {} | {} | {:.1}% |", 
        w3_matches.len(), w3_total, w3_accuracy)?;
    writeln!(&mut report, "| Paul Centore | {} | {} | {:.1}% |", 
        centore_matches.len(), centore_total, centore_accuracy)?;
    writeln!(&mut report, "| **Combined** | {} | {} | **{:.1}%** |", 
        w3_matches.len() + centore_matches.len(),
        w3_total + centore_total,
        ((w3_matches.len() + centore_matches.len()) as f64 / (w3_total + centore_total) as f64) * 100.0)?;
    writeln!(&mut report)?;
    
    // Add sample matches and mismatches
    writeln!(&mut report, "## Sample Matches (W3 Dataset)")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Hex | Expected | Munsell | Predicted |")?;
    writeln!(&mut report, "|-----|----------|---------|-----------|")?;
    for (i, m) in w3_matches.iter().take(10).enumerate() {
        writeln!(&mut report, "| {} | {} | {} | {} |", 
            m.hex, m.expected_name, m.munsell, m.predicted_name)?;
    }
    writeln!(&mut report)?;
    
    writeln!(&mut report, "## Sample Mismatches (W3 Dataset)")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Hex | Expected | Munsell | Predicted |")?;
    writeln!(&mut report, "|-----|----------|---------|-----------|")?;
    for (i, m) in w3_mismatches.iter().take(10).enumerate() {
        writeln!(&mut report, "| {} | {} | {} | {} |", 
            m.hex, m.expected_name, m.munsell, m.predicted_name)?;
    }
    writeln!(&mut report)?;
    
    writeln!(&mut report, "## Sample Matches (Centore Dataset)")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Hex | Expected | Munsell | Predicted |")?;
    writeln!(&mut report, "|-----|----------|---------|-----------|")?;
    for (i, m) in centore_matches.iter().take(10).enumerate() {
        writeln!(&mut report, "| {} | {} | {} | {} |", 
            m.hex, m.expected_name, m.munsell, m.predicted_name)?;
    }
    writeln!(&mut report)?;
    
    writeln!(&mut report, "## Sample Mismatches (Centore Dataset)")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Hex | Expected | Munsell | Predicted |")?;
    writeln!(&mut report, "|-----|----------|---------|-----------|")?;
    for (i, m) in centore_mismatches.iter().take(10).enumerate() {
        writeln!(&mut report, "| {} | {} | {} | {} |", 
            m.hex, m.expected_name, m.munsell, m.predicted_name)?;
    }
    
    // Write report
    fs::write("BEST_CONFIG_ISCC_RESULTS.md", report)?;
    
    println!("\n📈 Overall Results:");
    println!("==================");
    println!("W3 Dataset: {:.1}% accuracy", w3_accuracy);
    println!("Centore Dataset: {:.1}% accuracy", centore_accuracy);
    println!("Combined: {:.1}% accuracy", 
        ((w3_matches.len() + centore_matches.len()) as f64 / (w3_total + centore_total) as f64) * 100.0);
    
    println!("\n✅ Report generated: BEST_CONFIG_ISCC_RESULTS.md");
    
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