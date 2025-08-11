//! Comprehensive Conversion Dataset Analysis Tool
//! 
//! Generates a SINGLE comprehensive report file with:
//! - Both mathematical converters (v1 and v2)
//! - All 10 illuminants
//! - Both ISCC-NBS hue range methods
//! - Special chromatic adaptation analysis for first 10 colors

use munsellspace::iscc::{IsccNbsClassifier, HueRangeMethod};
use munsellspace::mathematical::{MathematicalMunsellConverter};
use munsellspace::mathematical_v2::{MathematicalMunsellConverter as MathematicalMunsellConverterV2, MunsellConfig};
use munsellspace::illuminants::{Illuminant, ChromaticAdaptationMethod};
use std::collections::HashMap;
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

/// Result for a single color test
#[derive(Debug, Clone)]
struct ColorTestResult {
    munsell_notation: String,
    method1_result: String,
    method1_match: bool,
    method2_result: String,
    method2_match: bool,
    conversion_success: bool,
}

/// Statistics for an illuminant configuration
#[derive(Debug, Clone)]
struct IlluminantStats {
    method1_correct: usize,
    method2_correct: usize,
    total_tested: usize,
    method1_accuracy: f64,
    method2_accuracy: f64,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 Generating Comprehensive Conversion Dataset Analysis");
    println!("======================================================");
    
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
    
    // Process both datasets
    println!("\n🧪 Processing W3 ISCC-NBS dataset...");
    let w3_results = process_dataset_w3(
        &w3_colors,
        &illuminants,
        &adaptation_methods,
        &method1_classifier,
        &method2_classifier,
    )?;
    
    println!("\n🧪 Processing Paul Centore dataset...");
    let centore_results = process_dataset_centore(
        &centore_colors,
        &illuminants,
        &adaptation_methods,
        &method1_classifier,
        &method2_classifier,
    )?;
    
    // Generate comprehensive report
    println!("\n📝 Generating comprehensive report...");
    generate_comprehensive_report(
        &w3_results,
        &centore_results,
        &illuminants,
        &adaptation_methods,
    )?;
    
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

fn process_dataset_w3(
    colors: &[W3IsccColor],
    illuminants: &[(Illuminant, &str, &str)],
    adaptation_methods: &[(ChromaticAdaptationMethod, &str)],
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> Result<HashMap<String, HashMap<String, ColorTestResult>>, Box<dyn std::error::Error>> {
    
    let mut all_results = HashMap::new();
    
    for (idx, color) in colors.iter().enumerate() {
        // Parse hex color
        let hex = color.srgb.trim_start_matches('#');
        if hex.len() != 6 { continue; }
        
        let r = u8::from_str_radix(&hex[0..2], 16)?;
        let g = u8::from_str_radix(&hex[2..4], 16)?;
        let b = u8::from_str_radix(&hex[4..6], 16)?;
        let rgb = [r, g, b];
        
        let hex_code = format!("#{:02X}{:02X}{:02X}", r, g, b);
        let expected_name = format!("{} {}", color.modifier.trim(), color.color.trim());
        
        let mut color_results = HashMap::new();
        
        // Test all illuminant configurations
        for (illuminant, illum_code, _) in illuminants {
            // Test v1 (mathematical.rs)
            let v1_key = format!("{}_v1", illum_code);
            color_results.insert(v1_key.clone(), test_color_v1(
                rgb, 
                &expected_name,
                *illuminant, 
                ChromaticAdaptationMethod::Bradford,
                method1_classifier,
                method2_classifier,
            ));
            
            // Test v2 (mathematical_v2.rs)
            let v2_key = format!("{}_v2", illum_code);
            color_results.insert(v2_key.clone(), test_color_v2(
                rgb,
                &expected_name,
                *illuminant,
                ChromaticAdaptationMethod::Bradford,
                method1_classifier,
                method2_classifier,
            ));
            
            // For first 10 colors, test all adaptation methods
            if idx < 10 {
                for (adapt_method, adapt_name) in adaptation_methods {
                    if *adapt_name != "Bradford" {  // Bradford already tested above
                        let v1_adapt_key = format!("{}_v1_{}", illum_code, adapt_name);
                        color_results.insert(v1_adapt_key, test_color_v1(
                            rgb,
                            &expected_name,
                            *illuminant,
                            *adapt_method,
                            method1_classifier,
                            method2_classifier,
                        ));
                        
                        let v2_adapt_key = format!("{}_v2_{}", illum_code, adapt_name);
                        color_results.insert(v2_adapt_key, test_color_v2(
                            rgb,
                            &expected_name,
                            *illuminant,
                            *adapt_method,
                            method1_classifier,
                            method2_classifier,
                        ));
                    }
                }
            }
        }
        
        all_results.insert(hex_code, color_results);
        
        if (idx + 1) % 50 == 0 {
            println!("  Processed {} colors...", idx + 1);
        }
    }
    
    Ok(all_results)
}

fn process_dataset_centore(
    colors: &[CentoreIsccColor],
    illuminants: &[(Illuminant, &str, &str)],
    adaptation_methods: &[(ChromaticAdaptationMethod, &str)],
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> Result<HashMap<String, HashMap<String, ColorTestResult>>, Box<dyn std::error::Error>> {
    
    let mut all_results = HashMap::new();
    
    for (idx, color) in colors.iter().enumerate() {
        let rgb = [color.r, color.g, color.b];
        let hex_code = format!("#{:02X}{:02X}{:02X}", color.r, color.g, color.b);
        let expected_name = color.name.clone();
        
        let mut color_results = HashMap::new();
        
        // Test all illuminant configurations
        for (illuminant, illum_code, _) in illuminants {
            // Test v1 (mathematical.rs)
            let v1_key = format!("{}_v1", illum_code);
            color_results.insert(v1_key.clone(), test_color_v1(
                rgb,
                &expected_name,
                *illuminant,
                ChromaticAdaptationMethod::Bradford,
                method1_classifier,
                method2_classifier,
            ));
            
            // Test v2 (mathematical_v2.rs)
            let v2_key = format!("{}_v2", illum_code);
            color_results.insert(v2_key.clone(), test_color_v2(
                rgb,
                &expected_name,
                *illuminant,
                ChromaticAdaptationMethod::Bradford,
                method1_classifier,
                method2_classifier,
            ));
            
            // For first 10 colors, test all adaptation methods
            if idx < 10 {
                for (adapt_method, adapt_name) in adaptation_methods {
                    if *adapt_name != "Bradford" {
                        let v1_adapt_key = format!("{}_v1_{}", illum_code, adapt_name);
                        color_results.insert(v1_adapt_key, test_color_v1(
                            rgb,
                            &expected_name,
                            *illuminant,
                            *adapt_method,
                            method1_classifier,
                            method2_classifier,
                        ));
                        
                        let v2_adapt_key = format!("{}_v2_{}", illum_code, adapt_name);
                        color_results.insert(v2_adapt_key, test_color_v2(
                            rgb,
                            &expected_name,
                            *illuminant,
                            *adapt_method,
                            method1_classifier,
                            method2_classifier,
                        ));
                    }
                }
            }
        }
        
        all_results.insert(hex_code, color_results);
        
        if (idx + 1) % 50 == 0 {
            println!("  Processed {} colors...", idx + 1);
        }
    }
    
    Ok(all_results)
}

fn test_color_v1(
    rgb: [u8; 3],
    expected_name: &str,
    illuminant: Illuminant,
    adaptation: ChromaticAdaptationMethod,
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> ColorTestResult {
    // Use v1 converter (mathematical.rs)
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
                            // Use modifier and color (not descriptor)
                            let modifier = result.iscc_nbs_modifier().unwrap_or("");
                            let color = result.iscc_nbs_color();
                            if modifier.is_empty() {
                                color.to_string()
                            } else {
                                format!("{} {}", modifier, color)
                            }
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
                            // Use modifier and color (not descriptor)
                            let modifier = result.iscc_nbs_modifier().unwrap_or("");
                            let color = result.iscc_nbs_color();
                            if modifier.is_empty() {
                                color.to_string()
                            } else {
                                format!("{} {}", modifier, color)
                            }
                        },
                        _ => "N/A".to_string(),
                    };
                    
                    ColorTestResult {
                        munsell_notation: notation,
                        method1_result: method1_result.clone(),
                        method1_match: method1_result.to_lowercase() == expected_name.to_lowercase(),
                        method2_result: method2_result.clone(),
                        method2_match: method2_result.to_lowercase() == expected_name.to_lowercase(),
                        conversion_success: true,
                    }
                },
                Err(_) => ColorTestResult {
                    munsell_notation: "ERROR".to_string(),
                    method1_result: "N/A".to_string(),
                    method1_match: false,
                    method2_result: "N/A".to_string(),
                    method2_match: false,
                    conversion_success: false,
                }
            }
        },
        Err(_) => ColorTestResult {
            munsell_notation: "ERROR".to_string(),
            method1_result: "N/A".to_string(),
            method1_match: false,
            method2_result: "N/A".to_string(),
            method2_match: false,
            conversion_success: false,
        }
    }
}

fn test_color_v2(
    rgb: [u8; 3],
    expected_name: &str,
    illuminant: Illuminant,
    adaptation: ChromaticAdaptationMethod,
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> ColorTestResult {
    // Use v2 converter (mathematical_v2.rs)
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
                            // Use modifier and color (not descriptor)
                            let modifier = result.iscc_nbs_modifier().unwrap_or("");
                            let color = result.iscc_nbs_color();
                            if modifier.is_empty() {
                                color.to_string()
                            } else {
                                format!("{} {}", modifier, color)
                            }
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
                            // Use modifier and color (not descriptor)
                            let modifier = result.iscc_nbs_modifier().unwrap_or("");
                            let color = result.iscc_nbs_color();
                            if modifier.is_empty() {
                                color.to_string()
                            } else {
                                format!("{} {}", modifier, color)
                            }
                        },
                        _ => "N/A".to_string(),
                    };
                    
                    ColorTestResult {
                        munsell_notation: notation,
                        method1_result: method1_result.clone(),
                        method1_match: method1_result.to_lowercase() == expected_name.to_lowercase(),
                        method2_result: method2_result.clone(),
                        method2_match: method2_result.to_lowercase() == expected_name.to_lowercase(),
                        conversion_success: true,
                    }
                },
                Err(_) => ColorTestResult {
                    munsell_notation: "ERROR".to_string(),
                    method1_result: "N/A".to_string(),
                    method1_match: false,
                    method2_result: "N/A".to_string(),
                    method2_match: false,
                    conversion_success: false,
                }
            }
        },
        Err(_) => ColorTestResult {
            munsell_notation: "ERROR".to_string(),
            method1_result: "N/A".to_string(),
            method1_match: false,
            method2_result: "N/A".to_string(),
            method2_match: false,
            conversion_success: false,
        }
    }
}

fn generate_comprehensive_report(
    w3_results: &HashMap<String, HashMap<String, ColorTestResult>>,
    centore_results: &HashMap<String, HashMap<String, ColorTestResult>>,
    illuminants: &[(Illuminant, &str, &str)],
    adaptation_methods: &[(ChromaticAdaptationMethod, &str)],
) -> Result<(), Box<dyn std::error::Error>> {
    
    let mut report = String::new();
    
    // Header
    writeln!(&mut report, "# Comprehensive Conversion Dataset Analysis")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "## Illuminant Descriptions")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Code | Illuminant | Description | Mathematical Method |")?;
    writeln!(&mut report, "|------|------------|-------------|---------------------|")?;
    
    for (illuminant, code, desc) in illuminants {
        writeln!(&mut report, "| {}_v1 | {} | {} | mathematical.rs (Original) |", code, code, desc)?;
        writeln!(&mut report, "| {}_v2 | {} | {} | mathematical_v2.rs (V2) |", code, code, desc)?;
    }
    writeln!(&mut report)?;
    
    // Calculate statistics for summary tables
    let w3_stats = calculate_dataset_statistics(w3_results, illuminants);
    let centore_stats = calculate_dataset_statistics(centore_results, illuminants);
    
    // Summary table for W3 dataset
    writeln!(&mut report, "## Summary: W3 ISCC-NBS Dataset ({} colors)", w3_results.len())?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Illuminant | Method 1 Accuracy | Method 2 Accuracy |")?;
    writeln!(&mut report, "|------------|-------------------|-------------------|")?;
    
    for (illuminant, code, _) in illuminants {
        let v1_key = format!("{}_v1", code);
        let v2_key = format!("{}_v2", code);
        
        if let Some(stats) = w3_stats.get(&v1_key) {
            writeln!(&mut report, "| {} | {:.1}% | {:.1}% |", 
                v1_key, stats.method1_accuracy, stats.method2_accuracy)?;
        }
        if let Some(stats) = w3_stats.get(&v2_key) {
            writeln!(&mut report, "| {} | {:.1}% | {:.1}% |",
                v2_key, stats.method1_accuracy, stats.method2_accuracy)?;
        }
    }
    writeln!(&mut report)?;
    
    // Summary table for Centore dataset
    writeln!(&mut report, "## Summary: Paul Centore ISCC-NBS Dataset ({} colors)", centore_results.len())?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Illuminant | Method 1 Accuracy | Method 2 Accuracy |")?;
    writeln!(&mut report, "|------------|-------------------|-------------------|")?;
    
    for (illuminant, code, _) in illuminants {
        let v1_key = format!("{}_v1", code);
        let v2_key = format!("{}_v2", code);
        
        if let Some(stats) = centore_stats.get(&v1_key) {
            writeln!(&mut report, "| {} | {:.1}% | {:.1}% |",
                v1_key, stats.method1_accuracy, stats.method2_accuracy)?;
        }
        if let Some(stats) = centore_stats.get(&v2_key) {
            writeln!(&mut report, "| {} | {:.1}% | {:.1}% |",
                v2_key, stats.method1_accuracy, stats.method2_accuracy)?;
        }
    }
    writeln!(&mut report)?;
    
    // W3 Dataset Details
    writeln!(&mut report, "## W3 ISCC-NBS Dataset - Detailed Results")?;
    writeln!(&mut report)?;
    
    // Sort colors by hex code for consistent ordering
    let mut w3_colors: Vec<_> = w3_results.iter().collect();
    w3_colors.sort_by_key(|(hex, _)| hex.as_str());
    
    for (idx, (hex_code, color_results)) in w3_colors.iter().enumerate() {
        if idx < 10 {
            // First 10 colors with adaptation methods
            write_color_detail_with_adaptation(
                &mut report,
                idx + 1,
                hex_code,
                color_results,
                illuminants,
                adaptation_methods,
            )?;
        } else {
            // Regular colors
            write_color_detail(
                &mut report,
                idx + 1,
                hex_code,
                color_results,
                illuminants,
            )?;
        }
    }
    
    // Centore Dataset Details
    writeln!(&mut report, "## Paul Centore ISCC-NBS Dataset - Detailed Results")?;
    writeln!(&mut report)?;
    
    let mut centore_colors: Vec<_> = centore_results.iter().collect();
    centore_colors.sort_by_key(|(hex, _)| hex.as_str());
    
    for (idx, (hex_code, color_results)) in centore_colors.iter().enumerate() {
        if idx < 10 {
            // First 10 colors with adaptation methods
            write_color_detail_with_adaptation(
                &mut report,
                idx + 1,
                hex_code,
                color_results,
                illuminants,
                adaptation_methods,
            )?;
        } else {
            // Regular colors
            write_color_detail(
                &mut report,
                idx + 1,
                hex_code,
                color_results,
                illuminants,
            )?;
        }
    }
    
    // Write report to file
    fs::write("COMPREHENSIVE_CONVERSION_DATASET.md", report)?;
    
    Ok(())
}

fn calculate_dataset_statistics(
    results: &HashMap<String, HashMap<String, ColorTestResult>>,
    illuminants: &[(Illuminant, &str, &str)],
) -> HashMap<String, IlluminantStats> {
    
    let mut stats = HashMap::new();
    
    for (illuminant, code, _) in illuminants {
        let v1_key = format!("{}_v1", code);
        let v2_key = format!("{}_v2", code);
        
        // Calculate v1 stats
        let mut v1_m1_correct = 0;
        let mut v1_m2_correct = 0;
        let mut v1_total = 0;
        
        for (_, color_results) in results {
            if let Some(result) = color_results.get(&v1_key) {
                if result.conversion_success {
                    v1_total += 1;
                    if result.method1_match { v1_m1_correct += 1; }
                    if result.method2_match { v1_m2_correct += 1; }
                }
            }
        }
        
        stats.insert(v1_key, IlluminantStats {
            method1_correct: v1_m1_correct,
            method2_correct: v1_m2_correct,
            total_tested: v1_total,
            method1_accuracy: if v1_total > 0 { (v1_m1_correct as f64 / v1_total as f64) * 100.0 } else { 0.0 },
            method2_accuracy: if v1_total > 0 { (v1_m2_correct as f64 / v1_total as f64) * 100.0 } else { 0.0 },
        });
        
        // Calculate v2 stats
        let mut v2_m1_correct = 0;
        let mut v2_m2_correct = 0;
        let mut v2_total = 0;
        
        for (_, color_results) in results {
            if let Some(result) = color_results.get(&v2_key) {
                if result.conversion_success {
                    v2_total += 1;
                    if result.method1_match { v2_m1_correct += 1; }
                    if result.method2_match { v2_m2_correct += 1; }
                }
            }
        }
        
        stats.insert(v2_key, IlluminantStats {
            method1_correct: v2_m1_correct,
            method2_correct: v2_m2_correct,
            total_tested: v2_total,
            method1_accuracy: if v2_total > 0 { (v2_m1_correct as f64 / v2_total as f64) * 100.0 } else { 0.0 },
            method2_accuracy: if v2_total > 0 { (v2_m2_correct as f64 / v2_total as f64) * 100.0 } else { 0.0 },
        });
    }
    
    stats
}

fn write_color_detail(
    report: &mut String,
    number: usize,
    hex_code: &str,
    color_results: &HashMap<String, ColorTestResult>,
    illuminants: &[(Illuminant, &str, &str)],
) -> Result<(), Box<dyn std::error::Error>> {
    
    writeln!(report, "### {}. {}", number, hex_code)?;
    writeln!(report)?;
    writeln!(report, "| Illuminant | Munsell Result | Method 1 Result | M1✓ | Method 2 Result | M2✓ |")?;
    writeln!(report, "|------------|----------------|-----------------|-----|-----------------|-----|")?;
    
    for (_, code, _) in illuminants {
        // v1 results
        let v1_key = format!("{}_v1", code);
        if let Some(result) = color_results.get(&v1_key) {
            writeln!(report, "| {} | {} | {} | {} | {} | {} |",
                v1_key,
                result.munsell_notation,
                result.method1_result,
                if result.method1_match { "✅" } else { "❌" },
                result.method2_result,
                if result.method2_match { "✅" } else { "❌" }
            )?;
        }
        
        // v2 results
        let v2_key = format!("{}_v2", code);
        if let Some(result) = color_results.get(&v2_key) {
            writeln!(report, "| {} | {} | {} | {} | {} | {} |",
                v2_key,
                result.munsell_notation,
                result.method1_result,
                if result.method1_match { "✅" } else { "❌" },
                result.method2_result,
                if result.method2_match { "✅" } else { "❌" }
            )?;
        }
    }
    writeln!(report)?;
    
    Ok(())
}

fn write_color_detail_with_adaptation(
    report: &mut String,
    number: usize,
    hex_code: &str,
    color_results: &HashMap<String, ColorTestResult>,
    illuminants: &[(Illuminant, &str, &str)],
    adaptation_methods: &[(ChromaticAdaptationMethod, &str)],
) -> Result<(), Box<dyn std::error::Error>> {
    
    writeln!(report, "### {}. {} (with chromatic adaptation methods)", number, hex_code)?;
    writeln!(report)?;
    writeln!(report, "| Illuminant | Adaptation | Munsell Result | Method 1 Result | M1✓ | Method 2 Result | M2✓ |")?;
    writeln!(report, "|------------|------------|----------------|-----------------|-----|-----------------|-----|")?;
    
    for (_, code, _) in illuminants {
        // Show all adaptation methods
        for (_, adapt_name) in adaptation_methods {
            // v1 results
            let v1_key = if *adapt_name == "Bradford" {
                format!("{}_v1", code)
            } else {
                format!("{}_v1_{}", code, adapt_name)
            };
            
            if let Some(result) = color_results.get(&v1_key) {
                writeln!(report, "| {} | {} | {} | {} | {} | {} | {} |",
                    format!("{}_v1", code),
                    adapt_name,
                    result.munsell_notation,
                    result.method1_result,
                    if result.method1_match { "✅" } else { "❌" },
                    result.method2_result,
                    if result.method2_match { "✅" } else { "❌" }
                )?;
            }
            
            // v2 results
            let v2_key = if *adapt_name == "Bradford" {
                format!("{}_v2", code)
            } else {
                format!("{}_v2_{}", code, adapt_name)
            };
            
            if let Some(result) = color_results.get(&v2_key) {
                writeln!(report, "| {} | {} | {} | {} | {} | {} | {} |",
                    format!("{}_v2", code),
                    adapt_name,
                    result.munsell_notation,
                    result.method1_result,
                    if result.method1_match { "✅" } else { "❌" },
                    result.method2_result,
                    if result.method2_match { "✅" } else { "❌" }
                )?;
            }
        }
    }
    writeln!(report)?;
    
    Ok(())
}