//! Comprehensive Conversion Dataset Analysis Tool V5 - Parallel Processing Version
//! 
//! Tests ALL combinations with parallel processing for speed
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
use std::sync::{Arc, Mutex};
use rayon::prelude::*;
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

/// Test configuration for parallel processing
#[derive(Clone)]
struct TestConfig {
    illuminant: Illuminant,
    illum_code: &'static str,
    adapt_method: ChromaticAdaptationMethod,
    adapt_name: &'static str,
    converter_version: u8, // 1 or 2
}

/// Test result for a single color
#[derive(Clone)]
struct TestResult {
    config: TestConfig,
    munsell_notation: String,
    method1_result: String,
    method1_match: bool,
    method2_result: String,
    method2_match: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 Generating Comprehensive Conversion Dataset Analysis V5 (Parallel)");
    println!("=====================================================================");
    
    // Load datasets
    let w3_colors = load_w3_dataset()?;
    let centore_colors = load_centore_dataset()?;
    
    println!("📊 Loaded {} W3 colors and {} Centore colors", w3_colors.len(), centore_colors.len());
    
    // Define test configurations
    let illuminants = vec![
        (Illuminant::A, "A"),
        (Illuminant::C, "C"),
        (Illuminant::D50, "D50"),
        (Illuminant::D55, "D55"),
        (Illuminant::D65, "D65"),
        (Illuminant::D75, "D75"),
        (Illuminant::E, "E"),
        (Illuminant::F2, "F2"),
        (Illuminant::F7, "F7"),
        (Illuminant::F11, "F11"),
    ];
    
    let adaptation_methods = vec![
        (ChromaticAdaptationMethod::Bradford, "Bradford"),
        (ChromaticAdaptationMethod::VonKries, "VonKries"),
        (ChromaticAdaptationMethod::CAT02, "CAT02"),
        (ChromaticAdaptationMethod::XYZScaling, "XYZScaling"),
    ];
    
    // Generate all test configurations
    let mut test_configs = Vec::new();
    for (illuminant, illum_code) in &illuminants {
        for (adapt_method, adapt_name) in &adaptation_methods {
            // v1 converter
            test_configs.push(TestConfig {
                illuminant: *illuminant,
                illum_code,
                adapt_method: *adapt_method,
                adapt_name,
                converter_version: 1,
            });
            // v2 converter
            test_configs.push(TestConfig {
                illuminant: *illuminant,
                illum_code,
                adapt_method: *adapt_method,
                adapt_name,
                converter_version: 2,
            });
        }
    }
    
    println!("📋 Testing {} configurations...", test_configs.len());
    
    // Process W3 Dataset in parallel
    println!("\n🧪 Processing W3 ISCC-NBS dataset (parallel)...");
    let w3_results = Arc::new(Mutex::new(Vec::new()));
    
    w3_colors.par_iter().enumerate().for_each(|(idx, color)| {
        let hex = color.srgb.trim_start_matches('#');
        if hex.len() != 6 { return; }
        
        let r = u8::from_str_radix(&hex[0..2], 16).unwrap_or(0);
        let g = u8::from_str_radix(&hex[2..4], 16).unwrap_or(0);
        let b = u8::from_str_radix(&hex[4..6], 16).unwrap_or(0);
        let rgb = [r, g, b];
        let expected_name = color.iscc_nbs_name.trim().to_lowercase();
        
        // Create thread-local classifiers
        let method1_classifier = IsccNbsClassifier::new_with_hue_range_method(
            HueRangeMethod::IncludeStartExcludeEnd
        ).unwrap();
        let method2_classifier = IsccNbsClassifier::new_with_hue_range_method(
            HueRangeMethod::ExcludeStartIncludeEnd
        ).unwrap();
        
        // Test all configurations for this color (sequential since we're already parallel at color level)
        let color_results: Vec<TestResult> = test_configs.iter()
            .filter_map(|config| {
                test_single_color(
                    rgb,
                    &expected_name,
                    config,
                    &method1_classifier,
                    &method2_classifier,
                )
            })
            .collect();
        
        if !color_results.is_empty() {
            let mut results = w3_results.lock().unwrap();
            results.push((idx, rgb, expected_name.clone(), color_results));
        }
        
        if (idx + 1) % 50 == 0 {
            println!("  Processed {} colors...", idx + 1);
        }
    });
    
    // Process Centore Dataset in parallel
    println!("\n🧪 Processing Paul Centore dataset (parallel)...");
    let centore_results = Arc::new(Mutex::new(Vec::new()));
    
    centore_colors.par_iter().enumerate().for_each(|(idx, color)| {
        let rgb = [color.r, color.g, color.b];
        let expected_name = color.name.trim().to_lowercase();
        
        // Create thread-local classifiers
        let method1_classifier = IsccNbsClassifier::new_with_hue_range_method(
            HueRangeMethod::IncludeStartExcludeEnd
        ).unwrap();
        let method2_classifier = IsccNbsClassifier::new_with_hue_range_method(
            HueRangeMethod::ExcludeStartIncludeEnd
        ).unwrap();
        
        // Test all configurations for this color (sequential since we're already parallel at color level)
        let color_results: Vec<TestResult> = test_configs.iter()
            .filter_map(|config| {
                test_single_color(
                    rgb,
                    &expected_name,
                    config,
                    &method1_classifier,
                    &method2_classifier,
                )
            })
            .collect();
        
        if !color_results.is_empty() {
            let mut results = centore_results.lock().unwrap();
            results.push((idx, rgb, expected_name.clone(), color_results));
        }
        
        if (idx + 1) % 50 == 0 {
            println!("  Processed {} colors...", idx + 1);
        }
    });
    
    // Generate report
    println!("\n📝 Generating report...");
    let mut report = String::new();
    
    // Header
    writeln!(&mut report, "# Comprehensive Conversion Dataset Analysis V5")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "## Summary Statistics")?;
    writeln!(&mut report)?;
    
    // Calculate statistics
    let w3_stats = calculate_statistics(&w3_results.lock().unwrap());
    let centore_stats = calculate_statistics(&centore_results.lock().unwrap());
    
    writeln!(&mut report, "### W3 Dataset ({} colors with matches)", w3_stats.total_colors)?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Illuminant | Adaptation | Converter | Method 1 | Method 2 |")?;
    writeln!(&mut report, "|------------|------------|-----------|----------|----------|")?;
    
    for ((illum_code, adapt_name, version), (m1_acc, m2_acc)) in &w3_stats.accuracies {
        writeln!(&mut report, "| {} | {} | v{} | {:.1}% | {:.1}% |",
            illum_code, adapt_name, version, m1_acc, m2_acc)?;
    }
    
    writeln!(&mut report)?;
    writeln!(&mut report, "### Centore Dataset ({} colors with matches)", centore_stats.total_colors)?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Illuminant | Adaptation | Converter | Method 1 | Method 2 |")?;
    writeln!(&mut report, "|------------|------------|-----------|----------|----------|")?;
    
    for ((illum_code, adapt_name, version), (m1_acc, m2_acc)) in &centore_stats.accuracies {
        writeln!(&mut report, "| {} | {} | v{} | {:.1}% | {:.1}% |",
            illum_code, adapt_name, version, m1_acc, m2_acc)?;
    }
    
    writeln!(&mut report)?;
    writeln!(&mut report, "## Best Configurations")?;
    writeln!(&mut report)?;
    
    // Find best configurations
    let best_w3 = find_best_config(&w3_stats.accuracies);
    let best_centore = find_best_config(&centore_stats.accuracies);
    
    writeln!(&mut report, "- **W3 Dataset Best**: {} {} v{} Method {} ({:.1}% accuracy)",
        best_w3.0, best_w3.1, best_w3.2, best_w3.3, best_w3.4)?;
    writeln!(&mut report, "- **Centore Dataset Best**: {} {} v{} Method {} ({:.1}% accuracy)",
        best_centore.0, best_centore.1, best_centore.2, best_centore.3, best_centore.4)?;
    
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

fn test_single_color(
    rgb: [u8; 3],
    expected_name: &str,
    config: &TestConfig,
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> Option<TestResult> {
    let result = if config.converter_version == 1 {
        test_color_v1(rgb, expected_name, config, method1_classifier, method2_classifier)
    } else {
        test_color_v2(rgb, expected_name, config, method1_classifier, method2_classifier)
    };
    
    // Only return if at least one method matches
    if result.method1_match || result.method2_match {
        Some(result)
    } else {
        None
    }
}

fn test_color_v1(
    rgb: [u8; 3],
    expected_name: &str,
    config: &TestConfig,
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> TestResult {
    match MathematicalMunsellConverter::with_illuminants(
        Illuminant::D65,
        config.illuminant,
        config.adapt_method,
    ) {
        Ok(converter) => {
            match converter.srgb_to_munsell(rgb) {
                Ok(munsell) => {
                    let notation = format!("{:.1}{} {:.1}/{:.1}",
                        munsell.hue, munsell.family,
                        munsell.value, munsell.chroma);
                    let hue_str = format!("{:.1}{}", munsell.hue, munsell.family);
                    
                    // Test Method 1
                    let method1_result = match method1_classifier.classify_munsell(
                        &hue_str,
                        munsell.value,
                        munsell.chroma
                    ) {
                        Ok(Some(result)) => result.iscc_nbs_descriptor.clone(),
                        _ => "N/A".to_string(),
                    };
                    
                    // Test Method 2
                    let method2_result = match method2_classifier.classify_munsell(
                        &hue_str,
                        munsell.value,
                        munsell.chroma
                    ) {
                        Ok(Some(result)) => result.iscc_nbs_descriptor.clone(),
                        _ => "N/A".to_string(),
                    };
                    
                    TestResult {
                        config: config.clone(),
                        munsell_notation: notation,
                        method1_result: method1_result.clone(),
                        method1_match: method1_result.to_lowercase() == expected_name,
                        method2_result: method2_result.clone(),
                        method2_match: method2_result.to_lowercase() == expected_name,
                    }
                },
                Err(_) => TestResult {
                    config: config.clone(),
                    munsell_notation: "ERROR".to_string(),
                    method1_result: "N/A".to_string(),
                    method1_match: false,
                    method2_result: "N/A".to_string(),
                    method2_match: false,
                }
            }
        },
        Err(_) => TestResult {
            config: config.clone(),
            munsell_notation: "ERROR".to_string(),
            method1_result: "N/A".to_string(),
            method1_match: false,
            method2_result: "N/A".to_string(),
            method2_match: false,
        }
    }
}

fn test_color_v2(
    rgb: [u8; 3],
    expected_name: &str,
    config: &TestConfig,
    method1_classifier: &IsccNbsClassifier,
    method2_classifier: &IsccNbsClassifier,
) -> TestResult {
    let munsell_config = MunsellConfig {
        source_illuminant: Illuminant::D65,
        target_illuminant: config.illuminant,
        adaptation_method: config.adapt_method,
    };
    
    match MathematicalMunsellConverterV2::with_config(munsell_config) {
        Ok(converter) => {
            match converter.srgb_to_munsell(rgb) {
                Ok(munsell) => {
                    let notation = format!("{:.1}{} {:.1}/{:.1}",
                        munsell.hue, munsell.family,
                        munsell.value, munsell.chroma);
                    let hue_str = format!("{:.1}{}", munsell.hue, munsell.family);
                    
                    // Test Method 1
                    let method1_result = match method1_classifier.classify_munsell(
                        &hue_str,
                        munsell.value,
                        munsell.chroma
                    ) {
                        Ok(Some(result)) => result.iscc_nbs_descriptor.clone(),
                        _ => "N/A".to_string(),
                    };
                    
                    // Test Method 2
                    let method2_result = match method2_classifier.classify_munsell(
                        &hue_str,
                        munsell.value,
                        munsell.chroma
                    ) {
                        Ok(Some(result)) => result.iscc_nbs_descriptor.clone(),
                        _ => "N/A".to_string(),
                    };
                    
                    TestResult {
                        config: config.clone(),
                        munsell_notation: notation,
                        method1_result: method1_result.clone(),
                        method1_match: method1_result.to_lowercase() == expected_name,
                        method2_result: method2_result.clone(),
                        method2_match: method2_result.to_lowercase() == expected_name,
                    }
                },
                Err(_) => TestResult {
                    config: config.clone(),
                    munsell_notation: "ERROR".to_string(),
                    method1_result: "N/A".to_string(),
                    method1_match: false,
                    method2_result: "N/A".to_string(),
                    method2_match: false,
                }
            }
        },
        Err(_) => TestResult {
            config: config.clone(),
            munsell_notation: "ERROR".to_string(),
            method1_result: "N/A".to_string(),
            method1_match: false,
            method2_result: "N/A".to_string(),
            method2_match: false,
        }
    }
}

struct DatasetStats {
    total_colors: usize,
    accuracies: std::collections::HashMap<(String, String, u8), (f64, f64)>,
}

fn calculate_statistics(results: &[(usize, [u8; 3], String, Vec<TestResult>)]) -> DatasetStats {
    use std::collections::HashMap;
    
    let mut stats: HashMap<(String, String, u8), (usize, usize, usize)> = HashMap::new();
    
    for (_, _, _, color_results) in results {
        for result in color_results {
            let key = (
                result.config.illum_code.to_string(),
                result.config.adapt_name.to_string(),
                result.config.converter_version,
            );
            
            let entry = stats.entry(key).or_insert((0, 0, 0));
            if result.method1_match { entry.0 += 1; }
            if result.method2_match { entry.1 += 1; }
            entry.2 += 1; // total
        }
    }
    
    let mut accuracies = HashMap::new();
    for (key, (m1_correct, m2_correct, total)) in stats {
        if total > 0 {
            let m1_acc = (m1_correct as f64 / total as f64) * 100.0;
            let m2_acc = (m2_correct as f64 / total as f64) * 100.0;
            accuracies.insert(key, (m1_acc, m2_acc));
        }
    }
    
    DatasetStats {
        total_colors: results.len(),
        accuracies,
    }
}

fn find_best_config(accuracies: &std::collections::HashMap<(String, String, u8), (f64, f64)>) 
    -> (String, String, u8, u8, f64) {
    let mut best = ("".to_string(), "".to_string(), 0u8, 0u8, 0.0f64);
    
    for ((illum, adapt, version), (m1_acc, m2_acc)) in accuracies {
        if *m1_acc > best.4 {
            best = (illum.clone(), adapt.clone(), *version, 1, *m1_acc);
        }
        if *m2_acc > best.4 {
            best = (illum.clone(), adapt.clone(), *version, 2, *m2_acc);
        }
    }
    
    best
}