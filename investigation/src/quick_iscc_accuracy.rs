//! Quick ISCC-NBS Accuracy Test
//! 
//! Tests only the most promising combinations to quickly identify the best configuration:
//! - Mathematical v1 (Original) only - the more accurate converter
//! - Illuminant C only - Munsell standard
//! - Bradford adaptation only - most common method
//! - Both hue range methods

use munsellspace::iscc::ISCC_NBS_Classifier as IsccNbsClassifier;
use munsellspace::HueRangeMethod;
use munsellspace::mathematical::MathematicalMunsellConverter;
use munsellspace::illuminants::{Illuminant, ChromaticAdaptationMethod};
use csv::ReaderBuilder;
use serde::Deserialize;

#[derive(Debug, Deserialize, Clone)]
struct W3IsccColor {
    #[serde(rename = "sRGB ")]
    srgb: String,
    #[serde(rename = "ISCC-NBS Name")]
    iscc_nbs_name: String,
}

#[derive(Debug, Deserialize, Clone)]
struct CentoreIsccColor {
    number: u16,
    name: String,
    r: u8,
    g: u8,
    b: u8,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 Quick ISCC-NBS Accuracy Test");
    println!("================================");
    
    // Load datasets
    let w3_colors = load_w3_dataset()?;
    let centore_colors = load_centore_dataset()?;
    
    println!("📊 Loaded {} W3 colors and {} Centore colors", w3_colors.len(), centore_colors.len());
    
    // Test with Illuminant C (Munsell standard) and Bradford adaptation
    let converter = MathematicalMunsellConverter::with_illuminants(
        Illuminant::D65,
        Illuminant::C,
        ChromaticAdaptationMethod::Bradford,
    )?;
    
    // Initialize classifiers
    let method1_classifier = IsccNbsClassifier::new_with_hue_range_method(
        HueRangeMethod::IncludeStartExcludeEnd
    )?;
    let method2_classifier = IsccNbsClassifier::new_with_hue_range_method(
        HueRangeMethod::ExcludeStartIncludeEnd
    )?;
    
    // Test W3 Dataset
    println!("\n🧪 Testing W3 ISCC-NBS dataset...");
    let (w3_m1_correct, w3_m2_correct, w3_total) = test_dataset_w3(
        &w3_colors,
        &converter,
        &method1_classifier,
        &method2_classifier,
    )?;
    
    println!("  Method 1 (Include Start): {}/{} = {:.1}% accuracy", 
        w3_m1_correct, w3_total, (w3_m1_correct as f64 / w3_total as f64) * 100.0);
    println!("  Method 2 (Exclude Start): {}/{} = {:.1}% accuracy", 
        w3_m2_correct, w3_total, (w3_m2_correct as f64 / w3_total as f64) * 100.0);
    
    // Test Centore Dataset
    println!("\n🧪 Testing Paul Centore dataset...");
    let (centore_m1_correct, centore_m2_correct, centore_total) = test_dataset_centore(
        &centore_colors,
        &converter,
        &method1_classifier,
        &method2_classifier,
    )?;
    
    println!("  Method 1 (Include Start): {}/{} = {:.1}% accuracy", 
        centore_m1_correct, centore_total, (centore_m1_correct as f64 / centore_total as f64) * 100.0);
    println!("  Method 2 (Exclude Start): {}/{} = {:.1}% accuracy", 
        centore_m2_correct, centore_total, (centore_m2_correct as f64 / centore_total as f64) * 100.0);
    
    // Summary
    println!("\n📈 Summary (Illuminant C, Bradford Adaptation):");
    println!("==================================================");
    println!("W3 Dataset (267 colors):");
    println!("  Best Method: {}", if w3_m1_correct >= w3_m2_correct { "Method 1" } else { "Method 2" });
    println!("  Best Accuracy: {:.1}%", 
        ((w3_m1_correct.max(w3_m2_correct) as f64 / w3_total as f64) * 100.0));
    
    println!("\nCentore Dataset (260 colors):");
    println!("  Best Method: {}", if centore_m1_correct >= centore_m2_correct { "Method 1" } else { "Method 2" });
    println!("  Best Accuracy: {:.1}%", 
        ((centore_m1_correct.max(centore_m2_correct) as f64 / centore_total as f64) * 100.0));
    
    let combined_m1 = w3_m1_correct + centore_m1_correct;
    let combined_m2 = w3_m2_correct + centore_m2_correct;
    let combined_total = w3_total + centore_total;
    
    println!("\nCombined (527 colors):");
    println!("  Method 1: {}/{} = {:.1}% accuracy", 
        combined_m1, combined_total, (combined_m1 as f64 / combined_total as f64) * 100.0);
    println!("  Method 2: {}/{} = {:.1}% accuracy", 
        combined_m2, combined_total, (combined_m2 as f64 / combined_total as f64) * 100.0);
    println!("  Best Overall: {}", if combined_m1 >= combined_m2 { "Method 1" } else { "Method 2" });
    
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

fn test_dataset_w3(
    colors: &[W3IsccColor],
    converter: &MathematicalMunsellConverter,
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> Result<(usize, usize, usize), Box<dyn std::error::Error>> {
    let mut m1_correct = 0;
    let mut m2_correct = 0;
    let mut total = 0;
    
    for color in colors {
        let hex = color.srgb.trim_start_matches('#');
        if hex.len() != 6 { continue; }
        
        let r = u8::from_str_radix(&hex[0..2], 16)?;
        let g = u8::from_str_radix(&hex[2..4], 16)?;
        let b = u8::from_str_radix(&hex[4..6], 16)?;
        let rgb = [r, g, b];
        let expected_name = color.iscc_nbs_name.trim().to_lowercase();
        
        match converter.srgb_to_munsell(rgb) {
            Ok(munsell) => {
                let hue_str = format!("{:.1}{}", munsell.hue, munsell.family);
                
                // Test Method 1
                if let Ok(Some(result)) = method1_classifier.classify_munsell(
                    &hue_str,
                    munsell.value,
                    munsell.chroma
                ) {
                    if result.iscc_nbs_descriptor.to_lowercase() == expected_name {
                        m1_correct += 1;
                    }
                }
                
                // Test Method 2
                if let Ok(Some(result)) = method2_classifier.classify_munsell(
                    &hue_str,
                    munsell.value,
                    munsell.chroma
                ) {
                    if result.iscc_nbs_descriptor.to_lowercase() == expected_name {
                        m2_correct += 1;
                    }
                }
                
                total += 1;
            },
            Err(_) => {}
        }
    }
    
    Ok((m1_correct, m2_correct, total))
}

fn test_dataset_centore(
    colors: &[CentoreIsccColor],
    converter: &MathematicalMunsellConverter,
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> Result<(usize, usize, usize), Box<dyn std::error::Error>> {
    let mut m1_correct = 0;
    let mut m2_correct = 0;
    let mut total = 0;
    
    for color in colors {
        let rgb = [color.r, color.g, color.b];
        let expected_name = color.name.trim().to_lowercase();
        
        match converter.srgb_to_munsell(rgb) {
            Ok(munsell) => {
                let hue_str = format!("{:.1}{}", munsell.hue, munsell.family);
                
                // Test Method 1
                if let Ok(Some(result)) = method1_classifier.classify_munsell(
                    &hue_str,
                    munsell.value,
                    munsell.chroma
                ) {
                    if result.iscc_nbs_descriptor.to_lowercase() == expected_name {
                        m1_correct += 1;
                    }
                }
                
                // Test Method 2
                if let Ok(Some(result)) = method2_classifier.classify_munsell(
                    &hue_str,
                    munsell.value,
                    munsell.chroma
                ) {
                    if result.iscc_nbs_descriptor.to_lowercase() == expected_name {
                        m2_correct += 1;
                    }
                }
                
                total += 1;
            },
            Err(_) => {}
        }
    }
    
    Ok((m1_correct, m2_correct, total))
}