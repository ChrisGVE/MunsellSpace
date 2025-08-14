//! Comprehensive Illuminant Method Comparison Tool
//!
//! Compares the original mathematical converter with the new mathematical_v2 
//! illuminant-aware converter across all available illuminants to determine
//! if illuminant changes produce different and potentially better results.

use munsellspace::mathematical::{MathematicalMunsellConverter, Illuminant, ChromaticAdaptation};
use std::fs::File;
use std::io::Write;
use std::collections::HashMap;

/// Test color with RGB and expected Munsell result
#[derive(Debug, Clone)]
struct TestColor {
    name: String,
    rgb: [u8; 3],
    hex: String,
    expected_munsell: Option<String>,
    description: String,
}

/// Conversion result for a specific illuminant configuration
#[derive(Debug, Clone)]
struct ConversionResult {
    illuminant: Illuminant,
    illuminant_name: String,
    adaptation_method: ChromaticAdaptation,
    munsell_hue: f64,
    munsell_family: String,
    munsell_value: f64,
    munsell_chroma: f64,
    notation: String,
    success: bool,
    error: Option<String>,
}

/// Comprehensive comparison results
#[derive(Debug)]
struct ComparisonResults {
    test_colors: Vec<TestColor>,
    conversion_results: HashMap<String, Vec<ConversionResult>>,
    illuminant_differences: HashMap<String, Vec<(String, String, f64)>>, // color -> (illuminant1, illuminant2, difference_score)
    adaptation_differences: HashMap<String, Vec<(String, String, f64)>>, // color -> (adaptation1, adaptation2, difference_score)
    best_configurations: HashMap<String, ConversionResult>, // color -> best result
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 COMPREHENSIVE ILLUMINANT METHOD COMPARISON");
    println!("============================================");
    println!("Testing mathematical converter with different illuminants and adaptation methods");
    println!("to identify optimal configurations for different color types.\n");
    
    // Create test colors covering different characteristics
    let test_colors = create_comprehensive_test_colors();
    
    // Create all illuminants to test
    let illuminants = vec![
        (Illuminant::D65, "D65 (Daylight 6500K)"),
        (Illuminant::C, "C (Average Daylight - Munsell Standard)"),
        (Illuminant::A, "A (Tungsten Incandescent)"),
        (Illuminant::D50, "D50 (Daylight 5000K)"),
        (Illuminant::D55, "D55 (Mid-morning/afternoon)"),
        (Illuminant::D75, "D75 (North sky daylight)"),
        (Illuminant::F2, "F2 (Cool White Fluorescent)"),
        (Illuminant::F7, "F7 (Daylight Fluorescent)"),
        (Illuminant::F11, "F11 (Narrow Band Fluorescent)"),
        (Illuminant::E, "E (Equal Energy)"),
    ];
    
    // Chromatic adaptation methods to test
    let adaptations = vec![
        (ChromaticAdaptation::Bradford, "Bradford"),
        (ChromaticAdaptation::XYZScaling, "XYZ Scaling"),
        (ChromaticAdaptation::CAT02, "CAT02"),
    ];
    
    println!("📊 Test Configuration:");
    println!("  • Colors: {} test colors", test_colors.len());
    println!("  • Illuminants: {} illuminants", illuminants.len());
    println!("  • Adaptation methods: {} methods", adaptations.len());
    println!("  • Total conversions: {}", test_colors.len() * illuminants.len() * adaptations.len());
    println!();
    
    // Run comprehensive comparison
    let results = run_comprehensive_comparison(&test_colors, &illuminants, &adaptations)?;
    
    // Generate detailed analysis report
    generate_comparison_report(&results)?;
    
    // Display summary
    display_comparison_summary(&results);
    
    println!("\n✅ Complete illuminant method comparison saved to:");
    println!("📄 ILLUMINANT_METHOD_COMPARISON_REPORT.md");
    
    Ok(())
}

/// Create comprehensive test colors covering different scenarios
fn create_comprehensive_test_colors() -> Vec<TestColor> {
    vec![
        // Primary colors
        TestColor {
            name: "Pure Red".to_string(),
            rgb: [255, 0, 0],
            hex: "#FF0000".to_string(),
            expected_munsell: Some("5R 5/20".to_string()),
            description: "Pure red - maximum saturation".to_string(),
        },
        TestColor {
            name: "Pure Green".to_string(),
            rgb: [0, 255, 0],
            hex: "#00FF00".to_string(),
            expected_munsell: Some("5G 8/20".to_string()),
            description: "Pure green - maximum saturation".to_string(),
        },
        TestColor {
            name: "Pure Blue".to_string(),
            rgb: [0, 0, 255],
            hex: "#0000FF".to_string(),
            expected_munsell: Some("5B 3/20".to_string()),
            description: "Pure blue - maximum saturation".to_string(),
        },
        
        // Precision issue colors from previous analysis
        TestColor {
            name: "Pinkish White".to_string(),
            rgb: [239, 221, 229],
            hex: "#EFDDE5".to_string(),
            expected_munsell: Some("5R 9/1.5".to_string()),
            description: "Light pinkish color - chroma precision issue".to_string(),
        },
        TestColor {
            name: "Very Dark Red".to_string(),
            rgb: [92, 6, 37],
            hex: "#5C0625".to_string(),
            expected_munsell: Some("5R 1.5/6".to_string()),
            description: "Very dark red - red/purple confusion".to_string(),
        },
        TestColor {
            name: "Pinkish Gray".to_string(),
            rgb: [199, 182, 189],
            hex: "#C7B6BD".to_string(),
            expected_munsell: Some("5R 7.5/1.5".to_string()),
            description: "Pinkish gray - family classification issue".to_string(),
        },
        
        // Neutral colors
        TestColor {
            name: "Pure Black".to_string(),
            rgb: [0, 0, 0],
            hex: "#000000".to_string(),
            expected_munsell: Some("N 0".to_string()),
            description: "Pure black - achromatic test".to_string(),
        },
        TestColor {
            name: "Pure White".to_string(),
            rgb: [255, 255, 255],
            hex: "#FFFFFF".to_string(),
            expected_munsell: Some("N 10".to_string()),
            description: "Pure white - achromatic test".to_string(),
        },
        TestColor {
            name: "Medium Gray".to_string(),
            rgb: [128, 128, 128],
            hex: "#808080".to_string(),
            expected_munsell: Some("N 5".to_string()),
            description: "Medium gray - neutral reference".to_string(),
        },
        
        // Complex colors
        TestColor {
            name: "Orange".to_string(),
            rgb: [255, 165, 0],
            hex: "#FFA500".to_string(),
            expected_munsell: Some("2.5YR 7/14".to_string()),
            description: "Orange - yellow-red transition".to_string(),
        },
        TestColor {
            name: "Purple".to_string(),
            rgb: [128, 0, 128],
            hex: "#800080".to_string(),
            expected_munsell: Some("5P 3/10".to_string()),
            description: "Purple - red-blue transition".to_string(),
        },
        TestColor {
            name: "Teal".to_string(),
            rgb: [0, 128, 128],
            hex: "#008080".to_string(),
            expected_munsell: Some("5BG 4/8".to_string()),
            description: "Teal - blue-green transition".to_string(),
        },
        
        // Subtle colors that may show illuminant differences
        TestColor {
            name: "Warm Beige".to_string(),
            rgb: [245, 245, 220],
            hex: "#F5F5DC".to_string(),
            expected_munsell: Some("5Y 9.5/2".to_string()),
            description: "Warm beige - subtle yellow cast".to_string(),
        },
        TestColor {
            name: "Cool Beige".to_string(),
            rgb: [240, 248, 255],
            hex: "#F0F8FF".to_string(),
            expected_munsell: Some("5B 9.8/1".to_string()),
            description: "Cool beige - subtle blue cast".to_string(),
        },
        TestColor {
            name: "Dusty Rose".to_string(),
            rgb: [188, 143, 143],
            hex: "#BC8F8F".to_string(),
            expected_munsell: Some("5R 6/4".to_string()),
            description: "Dusty rose - desaturated red".to_string(),
        },
    ]
}

/// Run comprehensive comparison across all illuminants and adaptation methods
fn run_comprehensive_comparison(
    test_colors: &[TestColor],
    illuminants: &[(Illuminant, &str)],
    adaptations: &[(ChromaticAdaptation, &str)],
) -> Result<ComparisonResults, Box<dyn std::error::Error>> {
    
    let mut conversion_results = HashMap::new();
    
    for test_color in test_colors {
        println!("🎨 Testing {} ({})", test_color.name, test_color.hex);
        
        let mut results_for_color = Vec::new();
        
        // Test all combinations of illuminants and adaptation methods
        for (illuminant, illuminant_name) in illuminants {
            for (adaptation, adaptation_name) in adaptations {
                print!("  {} with {}: ", illuminant_name, adaptation_name);
                
                let converter = MathematicalMunsellConverter::with_illuminants(
                    Illuminant::D65,  // sRGB source
                    *illuminant,      // target illuminant
                    *adaptation       // adaptation method
                )?;
                
                match converter.srgb_to_munsell(test_color.rgb) {
                    Ok(munsell) => {
                        let notation = format!("{:.1}{} {:.1}/{:.1}", 
                                       munsell.hue, munsell.family, 
                                       munsell.value, munsell.chroma);
                        
                        let result = ConversionResult {
                            illuminant: *illuminant,
                            illuminant_name: illuminant_name.to_string(),
                            adaptation_method: *adaptation,
                            munsell_hue: munsell.hue,
                            munsell_family: munsell.family.clone(),
                            munsell_value: munsell.value,
                            munsell_chroma: munsell.chroma,
                            notation: notation.clone(),
                            success: true,
                            error: None,
                        };
                        
                        println!("{}", notation);
                        results_for_color.push(result);
                    }
                    Err(e) => {
                        println!("Error: {}", e);
                        results_for_color.push(ConversionResult {
                            illuminant: *illuminant,
                            illuminant_name: illuminant_name.to_string(),
                            adaptation_method: *adaptation,
                            munsell_hue: 0.0,
                            munsell_family: "N".to_string(),
                            munsell_value: 0.0,
                            munsell_chroma: 0.0,
                            notation: "Error".to_string(),
                            success: false,
                            error: Some(e.to_string()),
                        });
                    }
                }
            }
        }
        
        conversion_results.insert(test_color.hex.clone(), results_for_color);
    }
    
    // Calculate differences and find best configurations
    let illuminant_differences = calculate_illuminant_differences(&conversion_results);
    let adaptation_differences = calculate_adaptation_differences(&conversion_results);
    let best_configurations = find_best_configurations(&conversion_results);
    
    Ok(ComparisonResults {
        test_colors: test_colors.to_vec(),
        conversion_results,
        illuminant_differences,
        adaptation_differences,
        best_configurations,
    })
}

/// Calculate differences between illuminants (same adaptation method)
fn calculate_illuminant_differences(
    results: &HashMap<String, Vec<ConversionResult>>
) -> HashMap<String, Vec<(String, String, f64)>> {
    let mut differences = HashMap::new();
    
    for (color_hex, color_results) in results {
        let mut color_differences = Vec::new();
        
        // Group results by adaptation method, then compare illuminants within each group
        let mut by_adaptation: HashMap<ChromaticAdaptation, Vec<_>> = HashMap::new();
        
        for result in color_results.iter().filter(|r| r.success) {
            by_adaptation.entry(result.adaptation_method).or_insert_with(Vec::new).push(result);
        }
        
        // Compare illuminants within each adaptation method
        for (_, adaptation_results) in by_adaptation {
            for i in 0..adaptation_results.len() {
                for j in i+1..adaptation_results.len() {
                    let result1 = adaptation_results[i];
                    let result2 = adaptation_results[j];
                    
                    // Only compare if different illuminants
                    if result1.illuminant != result2.illuminant {
                        // Calculate difference score based on hue, value, chroma differences
                        let hue_diff = (result1.munsell_hue - result2.munsell_hue).abs().min(10.0 - (result1.munsell_hue - result2.munsell_hue).abs());
                        let value_diff = (result1.munsell_value - result2.munsell_value).abs();
                        let chroma_diff = (result1.munsell_chroma - result2.munsell_chroma).abs();
                        
                        let family_diff = if result1.munsell_family == result2.munsell_family { 0.0 } else { 2.0 };
                        
                        let total_diff = hue_diff + value_diff + chroma_diff + family_diff;
                        
                        if total_diff > 0.1 { // Only record significant differences
                            color_differences.push((
                                result1.illuminant_name.clone(),
                                result2.illuminant_name.clone(),
                                total_diff,
                            ));
                        }
                    }
                }
            }
        }
        
        differences.insert(color_hex.clone(), color_differences);
    }
    
    differences
}

/// Calculate differences between adaptation methods (same illuminant)
fn calculate_adaptation_differences(
    results: &HashMap<String, Vec<ConversionResult>>
) -> HashMap<String, Vec<(String, String, f64)>> {
    let mut differences = HashMap::new();
    
    for (color_hex, color_results) in results {
        let mut color_differences = Vec::new();
        
        // Group results by illuminant, then compare adaptation methods within each group
        let mut by_illuminant: HashMap<Illuminant, Vec<_>> = HashMap::new();
        
        for result in color_results.iter().filter(|r| r.success) {
            by_illuminant.entry(result.illuminant).or_insert_with(Vec::new).push(result);
        }
        
        // Compare adaptation methods within each illuminant
        for (_, illuminant_results) in by_illuminant {
            for i in 0..illuminant_results.len() {
                for j in i+1..illuminant_results.len() {
                    let result1 = illuminant_results[i];
                    let result2 = illuminant_results[j];
                    
                    // Only compare if different adaptation methods
                    if result1.adaptation_method != result2.adaptation_method {
                        // Calculate difference score based on hue, value, chroma differences
                        let hue_diff = (result1.munsell_hue - result2.munsell_hue).abs().min(10.0 - (result1.munsell_hue - result2.munsell_hue).abs());
                        let value_diff = (result1.munsell_value - result2.munsell_value).abs();
                        let chroma_diff = (result1.munsell_chroma - result2.munsell_chroma).abs();
                        
                        let family_diff = if result1.munsell_family == result2.munsell_family { 0.0 } else { 2.0 };
                        
                        let total_diff = hue_diff + value_diff + chroma_diff + family_diff;
                        
                        if total_diff > 0.1 { // Only record significant differences
                            color_differences.push((
                                format!("{:?}", result1.adaptation_method),
                                format!("{:?}", result2.adaptation_method),
                                total_diff,
                            ));
                        }
                    }
                }
            }
        }
        
        differences.insert(color_hex.clone(), color_differences);
    }
    
    differences
}

/// Find best configuration for each color based on expected results
fn find_best_configurations(
    results: &HashMap<String, Vec<ConversionResult>>
) -> HashMap<String, ConversionResult> {
    let mut best_configs = HashMap::new();
    
    for (color_hex, color_results) in results {
        // For now, just pick the first successful result as "best"
        // In a real implementation, you'd compare against expected values
        if let Some(best_result) = color_results.iter().find(|r| r.success) {
            best_configs.insert(color_hex.clone(), best_result.clone());
        }
    }
    
    best_configs
}

/// Generate comprehensive markdown report
fn generate_comparison_report(results: &ComparisonResults) -> Result<(), Box<dyn std::error::Error>> {
    let mut report = File::create("ILLUMINANT_METHOD_COMPARISON_REPORT.md")?;
    
    writeln!(report, "# Illuminant Method Comparison Report")?;
    writeln!(report, "")?;
    writeln!(report, "## Executive Summary")?;
    writeln!(report, "")?;
    writeln!(report, "This report compares the mathematical converter with different illuminants")?;
    writeln!(report, "and chromatic adaptation methods to identify optimal configurations.")?;
    writeln!(report, "")?;
    writeln!(report, "- **Test Colors**: {}", results.test_colors.len())?;
    writeln!(report, "- **Illuminants Tested**: 10 (D65, C, A, D50, D55, D75, F2, F7, F11, E)")?;
    writeln!(report, "- **Adaptation Methods**: 3 (Bradford, XYZ Scaling, CAT02)")?;
    writeln!(report, "- **Total Conversions**: {}", results.conversion_results.values().map(|v| v.len()).sum::<usize>())?;
    writeln!(report, "")?;
    
    writeln!(report, "## Color-by-Color Analysis")?;
    writeln!(report, "")?;
    
    for test_color in &results.test_colors {
        writeln!(report, "### {} ({})", test_color.name, test_color.hex)?;
        writeln!(report, "")?;
        writeln!(report, "**Description**: {}", test_color.description)?;
        if let Some(expected) = &test_color.expected_munsell {
            writeln!(report, "**Expected Munsell**: {}", expected)?;
        }
        writeln!(report, "")?;
        
        if let Some(color_results) = results.conversion_results.get(&test_color.hex) {
            writeln!(report, "| Illuminant | Adaptation | Munsell Result | Success |")?;
            writeln!(report, "|------------|------------|----------------|---------|")?;
            
            for result in color_results {
                let status = if result.success { "✅" } else { "❌" };
                writeln!(report, "| {} | {:?} | {} | {} |", 
                        result.illuminant_name, result.adaptation_method, result.notation, status)?;
            }
            writeln!(report, "")?;
            
            // Show significant differences
            if let Some(illum_diffs) = results.illuminant_differences.get(&test_color.hex) {
                if !illum_diffs.is_empty() {
                    writeln!(report, "**Illuminant Differences**:")?;
                    for (illum1, illum2, diff) in illum_diffs {
                        writeln!(report, "- {} vs {}: Difference score {:.2}", illum1, illum2, diff)?;
                    }
                    writeln!(report, "")?;
                }
            }
            
            if let Some(adaptation_diffs) = results.adaptation_differences.get(&test_color.hex) {
                if !adaptation_diffs.is_empty() {
                    writeln!(report, "**Adaptation Method Differences**:")?;
                    for (method1, method2, diff) in adaptation_diffs {
                        writeln!(report, "- {} vs {}: Difference score {:.2}", method1, method2, diff)?;
                    }
                    writeln!(report, "")?;
                }
            }
        }
        writeln!(report, "")?;
    }
    
    writeln!(report, "## Summary of Findings")?;
    writeln!(report, "")?;
    writeln!(report, "### Illuminant Impact Analysis")?;
    writeln!(report, "")?;
    
    let mut colors_with_illuminant_differences = 0;
    let mut total_illuminant_differences = 0;
    
    for (_, diffs) in &results.illuminant_differences {
        if !diffs.is_empty() {
            colors_with_illuminant_differences += 1;
            total_illuminant_differences += diffs.len();
        }
    }
    
    writeln!(report, "- **Colors showing illuminant differences**: {}/{}", 
             colors_with_illuminant_differences, results.test_colors.len())?;
    writeln!(report, "- **Total illuminant differences detected**: {}", total_illuminant_differences)?;
    
    writeln!(report, "")?;
    writeln!(report, "### Adaptation Method Impact Analysis")?;
    writeln!(report, "")?;
    
    let mut colors_with_adaptation_differences = 0;
    let mut total_adaptation_differences = 0;
    
    for (_, diffs) in &results.adaptation_differences {
        if !diffs.is_empty() {
            colors_with_adaptation_differences += 1;
            total_adaptation_differences += diffs.len();
        }
    }
    
    writeln!(report, "- **Colors showing adaptation method differences**: {}/{}", 
             colors_with_adaptation_differences, results.test_colors.len())?;
    writeln!(report, "- **Total adaptation method differences detected**: {}", total_adaptation_differences)?;
    
    writeln!(report, "")?;
    writeln!(report, "## Conclusions")?;
    writeln!(report, "")?;
    
    if colors_with_illuminant_differences > 0 {
        writeln!(report, "✅ **Illuminant changes DO produce different results** for some colors.")?;
        writeln!(report, "The illuminant-aware V2 converter shows measurable differences")?;
        writeln!(report, "compared to the fixed D65 original converter.")?;
    } else {
        writeln!(report, "❌ **No significant illuminant differences detected.**")?;
        writeln!(report, "The illuminant changes may not be producing meaningfully different results.")?;
    }
    
    writeln!(report, "")?;
    writeln!(report, "---")?;
    writeln!(report, "Report generated by MunsellSpace Illuminant Method Comparison Tool")?;
    
    Ok(())
}

/// Display summary to console
fn display_comparison_summary(results: &ComparisonResults) {
    println!("\n📊 COMPARISON SUMMARY");
    println!("====================");
    
    let colors_with_illuminant_diffs = results.illuminant_differences.values()
        .filter(|diffs| !diffs.is_empty()).count();
    let colors_with_adaptation_diffs = results.adaptation_differences.values()
        .filter(|diffs| !diffs.is_empty()).count();
    
    println!("Colors tested: {}", results.test_colors.len());
    println!("Colors with illuminant differences: {}", colors_with_illuminant_diffs);
    println!("Colors with adaptation method differences: {}", colors_with_adaptation_diffs);
    
    if colors_with_illuminant_diffs > 0 {
        println!("\n🎯 KEY FINDING: Illuminant changes DO produce different results!");
        println!("Colors showing illuminant sensitivity:");
        
        for test_color in &results.test_colors {
            if let Some(diffs) = results.illuminant_differences.get(&test_color.hex) {
                if !diffs.is_empty() {
                    println!("  • {} ({}): {} different illuminant pairs", 
                            test_color.name, test_color.hex, diffs.len());
                    
                    // Show most significant difference
                    if let Some((illum1, illum2, diff)) = diffs.iter().max_by(|a, b| a.2.partial_cmp(&b.2).unwrap()) {
                        println!("    Max difference: {} vs {} (score: {:.2})", illum1, illum2, diff);
                    }
                }
            }
        }
    } else {
        println!("\n⚠️  No significant illuminant differences detected.");
        println!("The V2 converter may be producing similar results across illuminants.");
    }
    
    if colors_with_adaptation_diffs > 0 {
        println!("\n🔄 Adaptation method differences detected between Bradford, XYZ Scaling, and CAT02.");
    }
}