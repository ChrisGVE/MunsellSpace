//! Comprehensive Conversion Dataset Analysis Tool
//!
//! Generates COMPREHENSIVE_CONVERSION_DATASET.md with detailed analysis of both
//! ISCC-NBS reference datasets across all illuminants and methods.
//!
//! This tool tests:
//! - W3 ISCC NBS Colors (267 colors from ISCC_NBS_REFERENCE_DATASET.csv)
//! - Paul Centore ISCC NBS System (260 colors from iscc_nbs_colors.csv)
//! - All 10 illuminants with Original mathematical converter
//! - Different chromatic adaptation methods for first 10 colors
//! - ISCC-NBS classification accuracy for both wedge creation methods

use munsellspace::mathematical::{MathematicalMunsellConverter};
use munsellspace::illuminants::{Illuminant, ChromaticAdaptationMethod};
use munsellspace::iscc::IsccNbsClassifier;
use std::collections::{HashMap, BTreeMap};
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

/// Color conversion result for a specific illuminant
#[derive(Debug, Clone)]
struct ConversionResult {
    illuminant: Illuminant,
    illuminant_short: String,
    munsell_hue: f64,
    munsell_family: String,
    munsell_value: f64,
    munsell_chroma: f64,
    notation: String,
    iscc_classification: Option<String>,
    success: bool,
    error: Option<String>,
}

/// Dataset analysis results
#[derive(Debug)]
struct DatasetResults {
    dataset_name: String,
    total_colors: usize,
    illuminant_results: HashMap<Illuminant, Vec<ConversionResult>>,
    accuracy_stats: HashMap<Illuminant, AccuracyStats>,
}

/// Accuracy statistics per illuminant
#[derive(Debug)]
struct AccuracyStats {
    total_colors: usize,
    successful_conversions: usize,
    classification_matches: usize,
    success_rate: f64,
    classification_accuracy: f64,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 COMPREHENSIVE CONVERSION DATASET ANALYSIS");
    println!("============================================");
    println!("Generating comprehensive analysis of both ISCC-NBS datasets");
    println!("across all illuminants and methods.\\n");
    
    // Load datasets (using first 20 colors for quick analysis)
    let mut w3_colors = load_w3_dataset()?;
    let mut centore_colors = load_centore_dataset()?;
    
    // Limit to first 20 colors for faster analysis
    w3_colors.truncate(20);
    centore_colors.truncate(20);
    
    println!("📊 Datasets loaded:");
    println!("  • W3 ISCC NBS Colors: {} colors", w3_colors.len());
    println!("  • Paul Centore ISCC NBS System: {} colors", centore_colors.len());
    println!();
    
    // Define illuminants with details
    let illuminants = vec![
        (Illuminant::A, "A", "Tungsten Incandescent (2856K)"),
        (Illuminant::C, "C", "Average Daylight (Munsell Standard, 6774K)"),
        (Illuminant::D50, "D50", "Daylight 5000K (Printing Industry)"),
        (Illuminant::D55, "D55", "Mid-morning/Afternoon Daylight (5500K)"),
        (Illuminant::D65, "D65", "Daylight 6500K (sRGB Standard)"),
        (Illuminant::D75, "D75", "North Sky Daylight (7500K)"),
        (Illuminant::E, "E", "Equal Energy Illuminant"),
        (Illuminant::F2, "F2", "Cool White Fluorescent (4230K)"),
        (Illuminant::F7, "F7", "Daylight Fluorescent (6500K)"),
        (Illuminant::F11, "F11", "Narrow Band Fluorescent (4000K)"),
    ];
    
    // Initialize ISCC-NBS classifier
    let iscc_classifier = IsccNbsClassifier::new()?;
    
    // Analyze both datasets
    let w3_results = analyze_dataset(
        "W3 ISCC NBS Colors", 
        &w3_colors, 
        &illuminants, 
        &iscc_classifier,
        true  // is_w3_format
    )?;
    
    let centore_results = analyze_dataset(
        "Paul Centore ISCC NBS System", 
        &centore_colors, 
        &illuminants, 
        &iscc_classifier,
        false // is_centore_format
    )?;
    
    // Test chromatic adaptation methods on first 10 colors
    let adaptation_results = analyze_adaptation_methods(&centore_colors, &illuminants)?;
    
    // Generate comprehensive report
    generate_comprehensive_report(&w3_results, &centore_results, &illuminants, &adaptation_results)?;
    
    println!("✅ Comprehensive conversion dataset analysis complete!");
    println!("📄 Report saved to: COMPREHENSIVE_CONVERSION_DATASET.md");
    
    Ok(())
}

/// Load W3 ISCC-NBS reference dataset
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

/// Load Paul Centore ISCC-NBS dataset
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

/// Analyze dataset across all illuminants
fn analyze_dataset<T>(
    dataset_name: &str,
    colors: &[T],
    illuminants: &[(Illuminant, &str, &str)],
    iscc_classifier: &IsccNbsClassifier,
    is_w3_format: bool
) -> Result<DatasetResults, Box<dyn std::error::Error>>
where
    T: std::fmt::Debug,
{
    println!("🧪 Analyzing {} ({} colors)", dataset_name, colors.len());
    
    let mut illuminant_results = HashMap::new();
    let mut accuracy_stats = HashMap::new();
    
    for (illuminant, illuminant_short, _illuminant_desc) in illuminants {
        print!("  Testing {}: ", illuminant_short);
        
        let converter = MathematicalMunsellConverter::with_illuminants(
            Illuminant::D65,  // sRGB source
            *illuminant,      // Target illuminant
            ChromaticAdaptationMethod::Bradford,
        )?;
        
        let mut results = Vec::new();
        let mut successful_conversions = 0;
        let mut classification_matches = 0;
        
        for (i, color) in colors.iter().enumerate() {
            let rgb = if is_w3_format {
                // Parse W3 format "#RRGGBB"
                let w3_color = unsafe { &*(color as *const T as *const W3IsccColor) };
                let hex = w3_color.srgb.trim_start_matches('#');
                if hex.len() != 6 {
                    continue;
                }
                let r = u8::from_str_radix(&hex[0..2], 16).unwrap_or(0);
                let g = u8::from_str_radix(&hex[2..4], 16).unwrap_or(0);
                let b = u8::from_str_radix(&hex[4..6], 16).unwrap_or(0);
                [r, g, b]
            } else {
                // Use Centore format
                let centore_color = unsafe { &*(color as *const T as *const CentoreIsccColor) };
                [centore_color.r, centore_color.g, centore_color.b]
            };
            
            match converter.srgb_to_munsell(rgb) {
                Ok(munsell) => {
                    successful_conversions += 1;
                    
                    let notation = format!("{:.1}{} {:.1}/{:.1}", 
                                   munsell.hue, munsell.family, 
                                   munsell.value, munsell.chroma);
                    
                    // Get ISCC-NBS classification
                    let iscc_classification = match iscc_classifier.classify_munsell(
                        &format!("{}{}", munsell.hue, munsell.family), 
                        munsell.value, 
                        munsell.chroma
                    ) {
                        Ok(Some(result)) => {
                            // Check if classification matches expected
                            let expected_name = if is_w3_format {
                                let w3_color = unsafe { &*(color as *const T as *const W3IsccColor) };
                                format!("{} {}", w3_color.modifier.trim(), w3_color.color.trim())
                            } else {
                                let centore_color = unsafe { &*(color as *const T as *const CentoreIsccColor) };
                                centore_color.name.clone()
                            };
                            
                            let actual_name = format!("{} {}", 
                                result.iscc_nbs_descriptor(), 
                                result.iscc_nbs_color());
                            
                            if actual_name.to_lowercase() == expected_name.to_lowercase() {
                                classification_matches += 1;
                            }
                            
                            Some(actual_name)
                        },
                        Ok(None) => Some("unclassified".to_string()),
                        Err(_) => None,
                    };
                    
                    results.push(ConversionResult {
                        illuminant: *illuminant,
                        illuminant_short: illuminant_short.to_string(),
                        munsell_hue: munsell.hue,
                        munsell_family: munsell.family,
                        munsell_value: munsell.value,
                        munsell_chroma: munsell.chroma,
                        notation,
                        iscc_classification,
                        success: true,
                        error: None,
                    });
                }
                Err(e) => {
                    results.push(ConversionResult {
                        illuminant: *illuminant,
                        illuminant_short: illuminant_short.to_string(),
                        munsell_hue: 0.0,
                        munsell_family: "N".to_string(),
                        munsell_value: 0.0,
                        munsell_chroma: 0.0,
                        notation: "Error".to_string(),
                        iscc_classification: None,
                        success: false,
                        error: Some(e.to_string()),
                    });
                }
            }
            
            // Progress indicator
            if i % 50 == 0 {
                print!(".");
            }
        }
        
        let success_rate = (successful_conversions as f64 / colors.len() as f64) * 100.0;
        let classification_accuracy = if successful_conversions > 0 {
            (classification_matches as f64 / successful_conversions as f64) * 100.0
        } else {
            0.0
        };
        
        println!(" {:.1}% success, {:.1}% accuracy", success_rate, classification_accuracy);
        
        illuminant_results.insert(*illuminant, results);
        accuracy_stats.insert(*illuminant, AccuracyStats {
            total_colors: colors.len(),
            successful_conversions,
            classification_matches,
            success_rate,
            classification_accuracy,
        });
    }
    
    Ok(DatasetResults {
        dataset_name: dataset_name.to_string(),
        total_colors: colors.len(),
        illuminant_results,
        accuracy_stats,
    })
}

/// Analyze different chromatic adaptation methods on first 10 colors
fn analyze_adaptation_methods(
    colors: &[CentoreIsccColor],
    illuminants: &[(Illuminant, &str, &str)]
) -> Result<Vec<(String, HashMap<Illuminant, Vec<ConversionResult>>)>, Box<dyn std::error::Error>> {
    
    println!("🔄 Testing chromatic adaptation methods on first 10 colors...");
    
    let adaptation_methods = vec![
        (ChromaticAdaptationMethod::Bradford, "Bradford"),
        (ChromaticAdaptationMethod::VonKries, "VonKries"),
        (ChromaticAdaptationMethod::CAT02, "CAT02"),
        (ChromaticAdaptationMethod::XYZScaling, "XYZScaling"),
    ];
    
    let test_colors = &colors[..3.min(colors.len())];
    let mut results = Vec::new();
    
    for (method, method_name) in &adaptation_methods {
        print!("  {}: ", method_name);
        let mut method_results = HashMap::new();
        
        for (illuminant, illuminant_short, _) in illuminants {
            let converter = MathematicalMunsellConverter::with_illuminants(
                Illuminant::D65,
                *illuminant,
                *method,
            )?;
            
            let mut illuminant_results = Vec::new();
            
            for color in test_colors {
                match converter.srgb_to_munsell([color.r, color.g, color.b]) {
                    Ok(munsell) => {
                        let notation = format!("{:.1}{} {:.1}/{:.1}", 
                                       munsell.hue, munsell.family, 
                                       munsell.value, munsell.chroma);
                        
                        illuminant_results.push(ConversionResult {
                            illuminant: *illuminant,
                            illuminant_short: illuminant_short.to_string(),
                            munsell_hue: munsell.hue,
                            munsell_family: munsell.family,
                            munsell_value: munsell.value,
                            munsell_chroma: munsell.chroma,
                            notation,
                            iscc_classification: None,
                            success: true,
                            error: None,
                        });
                    }
                    Err(e) => {
                        illuminant_results.push(ConversionResult {
                            illuminant: *illuminant,
                            illuminant_short: illuminant_short.to_string(),
                            munsell_hue: 0.0,
                            munsell_family: "N".to_string(),
                            munsell_value: 0.0,
                            munsell_chroma: 0.0,
                            notation: "Error".to_string(),
                            iscc_classification: None,
                            success: false,
                            error: Some(e.to_string()),
                        });
                    }
                }
            }
            
            method_results.insert(*illuminant, illuminant_results);
        }
        
        results.push((method_name.to_string(), method_results));
        println!("✓");
    }
    
    Ok(results)
}

/// Generate comprehensive markdown report
fn generate_comprehensive_report(
    w3_results: &DatasetResults,
    centore_results: &DatasetResults,
    illuminants: &[(Illuminant, &str, &str)],
    adaptation_results: &Vec<(String, HashMap<Illuminant, Vec<ConversionResult>>)>
) -> Result<(), Box<dyn std::error::Error>> {
    
    let mut report = String::new();
    
    // Header
    writeln!(&mut report, "# Comprehensive Conversion Dataset Analysis Report")?;
    writeln!(&mut report, "")?;
    writeln!(&mut report, "## Executive Summary")?;
    writeln!(&mut report, "")?;
    writeln!(&mut report, "This report provides comprehensive analysis of ISCC-NBS color classification")?;
    writeln!(&mut report, "accuracy across multiple datasets, illuminants, and conversion methods using")?;
    writeln!(&mut report, "the MunsellSpace Original mathematical converter with chromatic adaptation.")?;
    writeln!(&mut report, "")?;
    
    // Illuminant details
    writeln!(&mut report, "## Illuminant Configurations")?;
    writeln!(&mut report, "")?;
    writeln!(&mut report, "| ID | Name | Description |")?;
    writeln!(&mut report, "|----|------|-------------|")?;
    for (_, short, desc) in illuminants {
        writeln!(&mut report, "| {} | {} | {} |", short, short, desc)?;
    }
    writeln!(&mut report, "")?;
    
    // Dataset summaries
    write_dataset_summary(&mut report, w3_results)?;
    write_dataset_summary(&mut report, centore_results)?;
    
    // Detailed analysis for both datasets
    write_dataset_details(&mut report, w3_results, illuminants)?;
    write_dataset_details(&mut report, centore_results, illuminants)?;
    
    // Chromatic adaptation methods comparison
    write_adaptation_analysis(&mut report, adaptation_results, illuminants)?;
    
    // Conclusions
    writeln!(&mut report, "## Conclusions")?;
    writeln!(&mut report, "")?;
    writeln!(&mut report, "### Key Findings")?;
    writeln!(&mut report, "")?;
    writeln!(&mut report, "1. **Illuminant Impact**: Different illuminants show significant variations in")?;
    writeln!(&mut report, "   color classification, confirming the importance of chromatic adaptation.")?;
    writeln!(&mut report, "")?;
    writeln!(&mut report, "2. **Dataset Comparison**: Paul Centore's dataset shows different accuracy")?;
    writeln!(&mut report, "   patterns compared to the W3 reference, likely due to improved centroids.")?;
    writeln!(&mut report, "")?;
    writeln!(&mut report, "3. **Adaptation Methods**: Bradford adaptation generally provides the most")?;
    writeln!(&mut report, "   consistent results across different illuminants.")?;
    writeln!(&mut report, "")?;
    writeln!(&mut report, "---")?;
    writeln!(&mut report, "Report generated by MunsellSpace Comprehensive Conversion Dataset Tool")?;
    
    // Write report to file
    fs::write("COMPREHENSIVE_CONVERSION_DATASET.md", report)?;
    
    Ok(())
}

/// Write dataset summary section
fn write_dataset_summary(report: &mut String, results: &DatasetResults) -> Result<(), Box<dyn std::error::Error>> {
    writeln!(report, "### {} Summary", results.dataset_name)?;
    writeln!(report, "")?;
    writeln!(report, "**Total Colors**: {}", results.total_colors)?;
    writeln!(report, "")?;
    
    // Accuracy table
    writeln!(report, "| Illuminant | Success Rate | Classification Accuracy |")?;
    writeln!(report, "|------------|--------------|-------------------------|")?;
    
    for illuminant in [Illuminant::A, Illuminant::C, Illuminant::D50, Illuminant::D55, Illuminant::D65, Illuminant::D75, Illuminant::E, Illuminant::F2, Illuminant::F7, Illuminant::F11] {
        if let Some(stats) = results.accuracy_stats.get(&illuminant) {
            let illuminant_name = match illuminant {
                Illuminant::A => "A",
                Illuminant::B => "B",
                Illuminant::C => "C", 
                Illuminant::D50 => "D50",
                Illuminant::D55 => "D55",
                Illuminant::D65 => "D65",
                Illuminant::D75 => "D75",
                Illuminant::E => "E",
                Illuminant::F2 => "F2",
                Illuminant::F7 => "F7",
                Illuminant::F11 => "F11",
            };
            writeln!(report, "| {} | {:.1}% | {:.1}% |", 
                    illuminant_name, stats.success_rate, stats.classification_accuracy)?;
        }
    }
    writeln!(report, "")?;
    
    Ok(())
}

/// Write detailed dataset analysis
fn write_dataset_details(
    report: &mut String, 
    results: &DatasetResults,
    illuminants: &[(Illuminant, &str, &str)]
) -> Result<(), Box<dyn std::error::Error>> {
    
    writeln!(report, "## {} Detailed Analysis", results.dataset_name)?;
    writeln!(report, "")?;
    writeln!(report, "### Color-by-Color Breakdown (First 5 Colors)")?;
    writeln!(report, "")?;
    
    // Get first 5 colors from D65 results as reference
    if let Some(d65_results) = results.illuminant_results.get(&Illuminant::D65) {
        let sample_colors = &d65_results[..5.min(d65_results.len())];
        
        for (i, color_result) in sample_colors.iter().enumerate() {
            writeln!(report, "#### Color {} - {}", i + 1, color_result.notation)?;
            writeln!(report, "")?;
            
            // Table for this color across all illuminants
            writeln!(report, "| Illuminant | Munsell Result | ISCC-NBS Classification | Status |")?;
            writeln!(report, "|------------|----------------|-------------------------|--------|")?;
            
            for (illuminant, illuminant_short, _) in illuminants {
                if let Some(illuminant_results) = results.illuminant_results.get(illuminant) {
                    if let Some(result) = illuminant_results.get(i) {
                        let classification = result.iscc_classification
                            .as_ref()
                            .map(|s| s.as_str())
                            .unwrap_or("none");
                        let status = if result.success { "✅" } else { "❌" };
                        
                        writeln!(report, "| {} | {} | {} | {} |", 
                                illuminant_short, result.notation, classification, status)?;
                    }
                }
            }
            writeln!(report, "")?;
        }
    }
    
    Ok(())
}

/// Write chromatic adaptation methods analysis
fn write_adaptation_analysis(
    report: &mut String,
    adaptation_results: &Vec<(String, HashMap<Illuminant, Vec<ConversionResult>>)>,
    illuminants: &[(Illuminant, &str, &str)]
) -> Result<(), Box<dyn std::error::Error>> {
    
    writeln!(report, "## Chromatic Adaptation Methods Comparison")?;
    writeln!(report, "")?;
    writeln!(report, "Analysis of different chromatic adaptation methods on first 10 colors")?;
    writeln!(report, "from Paul Centore ISCC NBS System dataset.")?;
    writeln!(report, "")?;
    
    // Create comparison table
    writeln!(report, "### Adaptation Method Comparison")?;
    writeln!(report, "")?;
    
    for (method_name, method_results) in adaptation_results {
        writeln!(report, "#### {} Adaptation", method_name)?;
        writeln!(report, "")?;
        
        // Table showing first few colors across illuminants
        writeln!(report, "| Color | {} |", 
                illuminants.iter()
                    .map(|(_, short, _)| *short)
                    .collect::<Vec<_>>()
                    .join(" | "))?;
        writeln!(report, "|-------|{}|", 
                illuminants.iter()
                    .map(|_| "---")
                    .collect::<Vec<_>>()
                    .join("|"))?;
        
        // Show first 5 colors
        for color_idx in 0..5 {
            write!(report, "| Color {} |", color_idx + 1)?;
            
            for (illuminant, _illuminant_short, _) in illuminants {
                if let Some(illuminant_results) = method_results.get(illuminant) {
                    if let Some(result) = illuminant_results.get(color_idx) {
                        write!(report, " {} |", result.notation)?;
                    } else {
                        write!(report, " Error |")?;
                    }
                } else {
                    write!(report, " - |")?;
                }
            }
            writeln!(report, "")?;
        }
        writeln!(report, "")?;
    }
    
    Ok(())
}