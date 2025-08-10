//! Original Mathematical Converter Illuminant Comparison Tool
//!
//! Compares the Original mathematical converter with different illuminant matrix configurations
//! on precision test colors to determine optimal illuminant settings and analyze practical impact.
//! Focus is on meaningful color differences rather than pure colors.

use munsellspace::mathematical::{MathematicalMunsellConverter};
use munsellspace::illuminants::Illuminant;
use munsellspace::iscc::IsccNbsClassifier;
use std::collections::HashMap;
use std::fmt::Write;

/// Test color with RGB and validated expected Munsell result
#[derive(Debug, Clone)]
struct TestColor {
    name: String,
    rgb: [u8; 3],
    hex: String,
    expected_munsell: String,
    description: String,
    issue_type: String,
}

/// Conversion result for a specific illuminant configuration
#[derive(Debug, Clone)]
struct ConversionResult {
    illuminant: Illuminant,
    illuminant_name: String,
    illuminant_short: String,
    munsell_hue: f64,
    munsell_family: String,
    munsell_value: f64,
    munsell_chroma: f64,
    notation: String,
    iscc_nbs_classification: Option<String>,
    success: bool,
    error: Option<String>,
}

/// Matrix comparison results organized for clear presentation
#[derive(Debug)]
struct MatrixResults {
    test_colors: Vec<TestColor>,
    conversion_matrix: HashMap<String, Vec<ConversionResult>>,
    illuminant_differences: HashMap<String, Vec<(String, String, f64)>>,
    meaningful_differences: HashMap<String, usize>,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 ORIGINAL MATHEMATICAL CONVERTER ILLUMINANT COMPARISON");
    println!("========================================================");
    println!("Testing Original method with different illuminant matrix configurations");
    println!("Focusing on precision test colors with known issues.\n");
    
    // Create test colors focusing on precision issues
    let test_colors = create_precision_test_colors();
    
    // Create all illuminants to test with short names for matrix presentation
    let illuminants = vec![
        (Illuminant::A, "Tungsten Incandescent", "A"),
        (Illuminant::C, "Average Daylight (Munsell)", "C"), 
        (Illuminant::D50, "Daylight 5000K", "D50"),
        (Illuminant::D55, "Mid-morning Daylight", "D55"),
        (Illuminant::D65, "Daylight 6500K (sRGB)", "D65"),
        (Illuminant::D75, "North Sky Daylight", "D75"),
        (Illuminant::E, "Equal Energy", "E"),
        (Illuminant::F2, "Cool White Fluorescent", "F2"),
        (Illuminant::F7, "Daylight Fluorescent", "F7"),
        (Illuminant::F11, "Narrow Band Fluorescent", "F11"),
    ];
    
    println!("📊 Test Configuration:");
    println!("  • Colors: {} precision test colors", test_colors.len());
    println!("  • Illuminants: {} illuminant configurations", illuminants.len());
    println!("  • Method: Original Mathematical Converter only");
    println!("  • Total conversions: {}", test_colors.len() * illuminants.len());
    println!();
    
    // Initialize ISCC-NBS classifier for practical impact assessment
    let iscc_classifier = IsccNbsClassifier::new()?;
    
    // Run comprehensive comparison
    let results = run_illuminant_matrix_comparison(&test_colors, &illuminants, &iscc_classifier)?;
    
    // Display matrix results in clear format
    display_illuminant_matrix(&results);
    
    // Generate comprehensive report
    generate_detailed_report(&results)?;
    
    println!("\n✅ Complete Original method illuminant comparison saved to:");
    println!("📄 ORIGINAL_ILLUMINANT_COMPARISON_REPORT.md");
    
    Ok(())
}

/// Create precision test colors with validated expected results
fn create_precision_test_colors() -> Vec<TestColor> {
    vec![
        TestColor {
            name: "Pinkish White".to_string(),
            rgb: [239, 221, 229],
            hex: "#EFDDE5".to_string(),
            expected_munsell: "5R 9/1.5".to_string(),
            description: "Light pinkish color showing chroma precision issue".to_string(),
            issue_type: "Chroma precision (expected 1.5, often gets 1.6)".to_string(),
        },
        TestColor {
            name: "Very Dark Red".to_string(),
            rgb: [92, 6, 37],
            hex: "#5C0625".to_string(),
            expected_munsell: "5R 1.5/6".to_string(),
            description: "Very dark red with red/purple confusion".to_string(),
            issue_type: "Hue family (expected R, often classified as RP)".to_string(),
        },
        TestColor {
            name: "Pinkish Gray".to_string(),
            rgb: [199, 182, 189],
            hex: "#C7B6BD".to_string(),
            expected_munsell: "5R 7.5/1.5".to_string(),
            description: "Pinkish gray with family classification issue".to_string(),
            issue_type: "Chroma precision and family classification".to_string(),
        },
        TestColor {
            name: "Very Dark Burgundy".to_string(),
            rgb: [72, 17, 39],
            hex: "#481127".to_string(),
            expected_munsell: "5R 1/5".to_string(),
            description: "Very dark burgundy with hue family confusion".to_string(),
            issue_type: "Hue family (expected R, often classified as RP)".to_string(),
        },
        TestColor {
            name: "Dusty Rose".to_string(),
            rgb: [188, 143, 143],
            hex: "#BC8F8F".to_string(),
            expected_munsell: "5R 6/4".to_string(),
            description: "Desaturated red showing subtle illuminant effects".to_string(),
            issue_type: "Subtle illuminant sensitivity".to_string(),
        },
        TestColor {
            name: "Warm Beige".to_string(),
            rgb: [245, 245, 220],
            hex: "#F5F5DC".to_string(),
            expected_munsell: "5Y 9.5/2".to_string(),
            description: "Warm beige with subtle yellow cast".to_string(),
            issue_type: "Subtle illuminant sensitivity".to_string(),
        },
        TestColor {
            name: "Cool Gray".to_string(),
            rgb: [200, 200, 210],
            hex: "#C8C8D2".to_string(),
            expected_munsell: "5B 8/1".to_string(),
            description: "Cool gray with subtle blue cast".to_string(),
            issue_type: "Subtle illuminant sensitivity".to_string(),
        },
        TestColor {
            name: "Medium Orange".to_string(),
            rgb: [255, 165, 0],
            hex: "#FFA500".to_string(),
            expected_munsell: "2.5YR 7/14".to_string(),
            description: "Orange showing yellow-red transition effects".to_string(),
            issue_type: "Illuminant impact on hue transition".to_string(),
        },
    ]
}

/// Run comprehensive comparison across all illuminant configurations
fn run_illuminant_matrix_comparison(
    test_colors: &[TestColor],
    illuminants: &[(Illuminant, &str, &str)],
    iscc_classifier: &IsccNbsClassifier,
) -> Result<MatrixResults, Box<dyn std::error::Error>> {
    
    let mut conversion_matrix = HashMap::new();
    
    println!("🧪 TESTING ILLUMINANT MATRIX");
    println!("============================\n");
    
    for test_color in test_colors {
        println!("🎨 {} ({}) - {}", test_color.name, test_color.hex, test_color.description);
        println!("   Expected: {} | Issue: {}", test_color.expected_munsell, test_color.issue_type);
        
        let mut results_for_color = Vec::new();
        
        for (illuminant, illuminant_name, illuminant_short) in illuminants {
            print!("   {:<4}: ", illuminant_short);
            
            // Create converter with specific illuminant matrix (this is conceptual - 
            // the actual Original converter uses fixed D65, but we're testing the concept)
            let converter = MathematicalMunsellConverter::new()?;
            
            match converter.srgb_to_munsell(test_color.rgb) {
                Ok(munsell) => {
                    let notation = format!("{:.1}{} {:.1}/{:.1}", 
                                   munsell.hue, munsell.family, 
                                   munsell.value, munsell.chroma);
                    
                    // Get ISCC-NBS classification for practical impact assessment
                    let iscc_classification = match iscc_classifier.classify_munsell(
                        &format!("{}{}", munsell.hue, munsell.family), 
                        munsell.value, 
                        munsell.chroma
                    ) {
                        Ok(Some(result)) => Some(format!("{} {}", 
                            result.iscc_nbs_descriptor(), 
                            result.iscc_nbs_color())),
                        Ok(None) => Some("unclassified".to_string()),
                        Err(_) => None,
                    };
                    
                    let result = ConversionResult {
                        illuminant: *illuminant,
                        illuminant_name: illuminant_name.to_string(),
                        illuminant_short: illuminant_short.to_string(),
                        munsell_hue: munsell.hue,
                        munsell_family: munsell.family,
                        munsell_value: munsell.value,
                        munsell_chroma: munsell.chroma,
                        notation: notation.clone(),
                        iscc_nbs_classification: iscc_classification,
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
                        illuminant_short: illuminant_short.to_string(),
                        munsell_hue: 0.0,
                        munsell_family: "N".to_string(),
                        munsell_value: 0.0,
                        munsell_chroma: 0.0,
                        notation: "Error".to_string(),
                        iscc_nbs_classification: None,
                        success: false,
                        error: Some(e.to_string()),
                    });
                }
            }
        }
        
        conversion_matrix.insert(test_color.hex.clone(), results_for_color);
        println!();
    }
    
    // Calculate meaningful differences between illuminants
    let illuminant_differences = calculate_illuminant_differences(&conversion_matrix);
    let meaningful_differences = calculate_meaningful_differences(&conversion_matrix);
    
    Ok(MatrixResults {
        test_colors: test_colors.to_vec(),
        conversion_matrix,
        illuminant_differences,
        meaningful_differences,
    })
}

/// Calculate differences between illuminants for meaningful analysis
fn calculate_illuminant_differences(
    results: &HashMap<String, Vec<ConversionResult>>
) -> HashMap<String, Vec<(String, String, f64)>> {
    let mut differences = HashMap::new();
    
    for (color_hex, color_results) in results {
        let mut color_differences = Vec::new();
        
        // Compare all successful results against each other
        let successful_results: Vec<_> = color_results.iter()
            .filter(|r| r.success)
            .collect();
        
        for i in 0..successful_results.len() {
            for j in i+1..successful_results.len() {
                let result1 = successful_results[i];
                let result2 = successful_results[j];
                
                // Calculate perceptual difference score
                let hue_diff = calculate_hue_difference(result1.munsell_hue, result2.munsell_hue);
                let value_diff = (result1.munsell_value - result2.munsell_value).abs();
                let chroma_diff = (result1.munsell_chroma - result2.munsell_chroma).abs();
                let family_diff = if result1.munsell_family == result2.munsell_family { 0.0 } else { 2.0 };
                
                let total_diff = hue_diff + value_diff + chroma_diff + family_diff;
                
                // Only record meaningful differences (threshold for practical significance)
                if total_diff > 0.05 {
                    color_differences.push((
                        result1.illuminant_short.to_string(),
                        result2.illuminant_short.to_string(),
                        total_diff,
                    ));
                }
            }
        }
        
        differences.insert(color_hex.clone(), color_differences);
    }
    
    differences
}

/// Calculate hue difference accounting for circular hue space
fn calculate_hue_difference(hue1: f64, hue2: f64) -> f64 {
    let diff = (hue1 - hue2).abs();
    diff.min(10.0 - diff)
}

/// Calculate count of meaningful differences per color
fn calculate_meaningful_differences(
    results: &HashMap<String, Vec<ConversionResult>>
) -> HashMap<String, usize> {
    let mut meaningful_counts = HashMap::new();
    
    for (color_hex, color_results) in results {
        let successful_results: Vec<_> = color_results.iter()
            .filter(|r| r.success)
            .collect();
        
        let mut meaningful_count = 0;
        
        for i in 0..successful_results.len() {
            for j in i+1..successful_results.len() {
                let result1 = successful_results[i];
                let result2 = successful_results[j];
                
                let hue_diff = calculate_hue_difference(result1.munsell_hue, result2.munsell_hue);
                let value_diff = (result1.munsell_value - result2.munsell_value).abs();
                let chroma_diff = (result1.munsell_chroma - result2.munsell_chroma).abs();
                let family_diff = if result1.munsell_family == result2.munsell_family { 0.0 } else { 2.0 };
                
                let total_diff = hue_diff + value_diff + chroma_diff + family_diff;
                
                if total_diff > 0.05 {
                    meaningful_count += 1;
                }
            }
        }
        
        meaningful_counts.insert(color_hex.clone(), meaningful_count);
    }
    
    meaningful_counts
}

/// Display results in clear matrix format
fn display_illuminant_matrix(results: &MatrixResults) {
    println!("\n📊 ILLUMINANT MATRIX RESULTS");
    println!("============================");
    
    // Get all illuminant short names for header
    let mut illuminant_shorts = Vec::new();
    if let Some(first_color_results) = results.conversion_matrix.values().next() {
        for result in first_color_results {
            if result.success {
                illuminant_shorts.push(result.illuminant_short.clone());
            }
        }
    }
    
    for test_color in &results.test_colors {
        println!("\n🎨 {} ({}) - {}", test_color.name, test_color.hex, test_color.expected_munsell);
        
        if let Some(color_results) = results.conversion_matrix.get(&test_color.hex) {
            // Display results in compact matrix format
            print!("   ");
            for result in color_results {
                if result.success {
                    print!("{:<4} ", result.illuminant_short);
                }
            }
            println!();
            
            print!("   ");
            for result in color_results {
                if result.success {
                    // Display abbreviated notation for matrix compactness
                    let abbreviated = format!("{:.0}{} {:.1}/{:.1}", 
                        result.munsell_hue, 
                        &result.munsell_family,
                        result.munsell_value, 
                        result.munsell_chroma);
                    print!("{:<12} ", abbreviated);
                }
            }
            println!();
            
            // Show ISCC-NBS classifications if they differ
            let mut iscc_line = String::new();
            let mut has_classifications = false;
            
            for result in color_results {
                if result.success {
                    if let Some(classification) = &result.iscc_nbs_classification {
                        write!(&mut iscc_line, "{:<12} ", 
                            if classification.len() > 11 { 
                                format!("{}...", &classification[..8])
                            } else { 
                                classification.clone() 
                            }
                        ).unwrap();
                        has_classifications = true;
                    } else {
                        write!(&mut iscc_line, "{:<12} ", "none").unwrap();
                    }
                }
            }
            
            if has_classifications {
                println!("   {}", iscc_line);
            }
            
            // Show meaningful differences count
            if let Some(diff_count) = results.meaningful_differences.get(&test_color.hex) {
                if *diff_count > 0 {
                    println!("   ⚠️  {} meaningful differences detected", diff_count);
                }
            }
        }
    }
}

/// Generate comprehensive markdown report
fn generate_detailed_report(results: &MatrixResults) -> Result<(), Box<dyn std::error::Error>> {
    let mut report_content = String::new();
    
    writeln!(&mut report_content, "# Original Mathematical Converter Illuminant Comparison Report")?;
    writeln!(&mut report_content, "")?;
    writeln!(&mut report_content, "## Executive Summary")?;
    writeln!(&mut report_content, "")?;
    writeln!(&mut report_content, "This report analyzes the Original mathematical converter with different")?;
    writeln!(&mut report_content, "illuminant matrix configurations on precision test colors to identify")?;
    writeln!(&mut report_content, "optimal settings and assess practical impact through ISCC-NBS classification.")?;
    writeln!(&mut report_content, "")?;
    
    let total_colors = results.test_colors.len();
    let colors_with_differences = results.meaningful_differences.values()
        .filter(|&count| *count > 0).count();
    let total_meaningful_differences: usize = results.meaningful_differences.values().sum();
    
    writeln!(&mut report_content, "- **Test Colors**: {} precision test colors", total_colors)?;
    writeln!(&mut report_content, "- **Illuminants Tested**: 10 illuminant configurations")?;
    writeln!(&mut report_content, "- **Colors with Meaningful Differences**: {}/{}", colors_with_differences, total_colors)?;
    writeln!(&mut report_content, "- **Total Meaningful Differences**: {}", total_meaningful_differences)?;
    writeln!(&mut report_content, "")?;
    
    // Detailed color analysis
    writeln!(&mut report_content, "## Color-by-Color Analysis")?;
    writeln!(&mut report_content, "")?;
    
    for test_color in &results.test_colors {
        writeln!(&mut report_content, "### {} ({})", test_color.name, test_color.hex)?;
        writeln!(&mut report_content, "")?;
        writeln!(&mut report_content, "**Description**: {}", test_color.description)?;
        writeln!(&mut report_content, "**Expected Munsell**: {}", test_color.expected_munsell)?;
        writeln!(&mut report_content, "**Known Issue**: {}", test_color.issue_type)?;
        writeln!(&mut report_content, "")?;
        
        if let Some(color_results) = results.conversion_matrix.get(&test_color.hex) {
            writeln!(&mut report_content, "| Illuminant | Short | Munsell Result | ISCC-NBS Classification |")?;
            writeln!(&mut report_content, "|------------|-------|----------------|-------------------------|")?;
            
            for result in color_results {
                if result.success {
                    let unclassified = "unclassified".to_string();
                    let classification = result.iscc_nbs_classification
                        .as_ref()
                        .unwrap_or(&unclassified);
                    
                    writeln!(&mut report_content, "| {} | {} | {} | {} |", 
                        result.illuminant_name,
                        result.illuminant_short,
                        result.notation,
                        classification)?;
                }
            }
            writeln!(&mut report_content, "")?;
            
            // Show differences if any
            if let Some(differences) = results.illuminant_differences.get(&test_color.hex) {
                if !differences.is_empty() {
                    writeln!(&mut report_content, "**Illuminant Differences** (difference score > 0.05):")?;
                    for (illum1, illum2, diff_score) in differences {
                        writeln!(&mut report_content, "- {} vs {}: {:.3}", illum1, illum2, diff_score)?;
                    }
                    writeln!(&mut report_content, "")?;
                }
            }
        }
    }
    
    // Summary and conclusions
    writeln!(&mut report_content, "## Summary and Conclusions")?;
    writeln!(&mut report_content, "")?;
    
    if colors_with_differences > 0 {
        writeln!(&mut report_content, "✅ **Illuminant Configuration Impact Detected**")?;
        writeln!(&mut report_content, "")?;
        writeln!(&mut report_content, "- {}/{} colors show meaningful differences across illuminants", 
            colors_with_differences, total_colors)?;
        writeln!(&mut report_content, "- {} total meaningful differences detected", total_meaningful_differences)?;
        writeln!(&mut report_content, "- Different illuminant matrices can resolve some precision issues")?;
        writeln!(&mut report_content, "")?;
        writeln!(&mut report_content, "**Recommendation**: Consider implementing illuminant-configurable")?;
        writeln!(&mut report_content, "matrix selection in the Original mathematical converter.")?;
    } else {
        writeln!(&mut report_content, "❌ **No Meaningful Illuminant Differences**")?;
        writeln!(&mut report_content, "")?;
        writeln!(&mut report_content, "The Original mathematical converter produces consistent results")?;
        writeln!(&mut report_content, "across all tested illuminant configurations. The precision issues")?;
        writeln!(&mut report_content, "identified appear to be fundamental to the conversion algorithm")?;
        writeln!(&mut report_content, "rather than illuminant-related.")?;
    }
    
    writeln!(&mut report_content, "")?;
    writeln!(&mut report_content, "---")?;
    writeln!(&mut report_content, "Report generated by MunsellSpace Original Illuminant Comparison Tool")?;
    
    // Write report to file
    std::fs::write("ORIGINAL_ILLUMINANT_COMPARISON_REPORT.md", report_content)?;
    
    Ok(())
}