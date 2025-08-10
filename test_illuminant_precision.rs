//! Comprehensive illuminant testing for precision issue colors
//! 
//! Tests all available illuminants on the 4 colors with ISCC-NBS classification issues
//! to determine if illuminant changes can resolve red/purple confusion and chroma precision errors.

use munsellspace::{Illuminant, ChromaticAdaptationMethod, HueFamily};
use munsellspace::mathematical_v2::{MathematicalMunsellConverter, MunsellConfig};
use std::fmt::Write;

#[derive(Debug, Clone)]
struct TestColor {
    rgb: [u8; 3],
    hex: &'static str,
    description: &'static str,
    expected_hue_family: HueFamily,
    expected_chroma: Option<f64>,
    issue_type: &'static str,
}

#[derive(Debug, Clone)]
struct TestResult {
    illuminant: Illuminant,
    config_type: &'static str,
    hue: f64,
    family: HueFamily,
    value: f64,
    chroma: f64,
    hue_family_correct: bool,
    chroma_error: Option<f64>,
    distance_from_expected: f64,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Define the 4 problem colors with their expected characteristics
    let test_colors = vec![
        TestColor {
            rgb: [239, 221, 229], // #EFDDE5
            hex: "#EFDDE5",
            description: "Pinkish white with chroma precision issue",
            expected_hue_family: HueFamily::R, // Assuming R family based on context
            expected_chroma: Some(1.5),
            issue_type: "Chroma precision (expected 1.5, got 1.6)",
        },
        TestColor {
            rgb: [92, 6, 37],     // #5C0625
            hex: "#5C0625",
            description: "Dark red with hue family misclassification",
            expected_hue_family: HueFamily::R,
            expected_chroma: None,
            issue_type: "Hue family (expected R, got 6.6RP)",
        },
        TestColor {
            rgb: [199, 182, 189], // #C7B6BD
            hex: "#C7B6BD",
            description: "Light grayish red with chroma precision issue",
            expected_hue_family: HueFamily::YR, // Based on 3YR mentioned
            expected_chroma: Some(1.5),
            issue_type: "Chroma precision (expected 1.5, got 1.6)",
        },
        TestColor {
            rgb: [72, 17, 39],    // #481127
            hex: "#481127",
            description: "Very dark red with hue family misclassification", 
            expected_hue_family: HueFamily::R,
            expected_chroma: None,
            issue_type: "Hue family (expected R, got 3.7RP)",
        },
    ];

    // All available illuminants to test
    let illuminants = vec![
        Illuminant::A,   // Tungsten
        Illuminant::B,   // Obsolete noon sunlight
        Illuminant::C,   // Average daylight (Munsell standard)
        Illuminant::D50, // Horizon light
        Illuminant::D55, // Mid-morning/afternoon
        Illuminant::D65, // Noon daylight (sRGB standard)
        Illuminant::D75, // North sky daylight
        Illuminant::E,   // Equal energy
        Illuminant::F2,  // Cool white fluorescent
        Illuminant::F7,  // Broadband daylight fluorescent
        Illuminant::F11, // Narrow band white fluorescent
    ];

    println!("COMPREHENSIVE ILLUMINANT PRECISION TEST");
    println!("=====================================\n");
    
    println!("Testing {} colors under {} illuminants with 2 configuration types each.", 
        test_colors.len(), illuminants.len());
    println!("Total tests: {}\n", test_colors.len() * illuminants.len() * 2);

    let mut all_results = Vec::new();

    for color in &test_colors {
        println!("COLOR: {} {} - {}", color.hex, format!("RGB{:?}", color.rgb), color.description);
        println!("ISSUE: {}", color.issue_type);
        println!("{}", "=".repeat(80));

        let mut color_results = Vec::new();

        for illuminant in &illuminants {
            // Test 1: sRGB (D65) → target illuminant 
            let config1 = MunsellConfig {
                source_illuminant: Illuminant::D65,
                target_illuminant: *illuminant,
                adaptation_method: ChromaticAdaptationMethod::Bradford,
            };
            
            // Test 2: source = target = illuminant
            let config2 = MunsellConfig {
                source_illuminant: *illuminant,
                target_illuminant: *illuminant, 
                adaptation_method: ChromaticAdaptationMethod::Bradford,
            };

            for (config, config_name) in [(&config1, "sRGB→Illuminant"), (&config2, "Illuminant→Illuminant")] {
                match MathematicalMunsellConverter::with_config(*config) {
                    Ok(converter) => {
                        match converter.srgb_to_munsell(color.rgb) {
                            Ok(munsell) => {
                                let hue_family_correct = munsell.family == color.expected_hue_family;
                                
                                let chroma_error = color.expected_chroma.map(|expected| {
                                    (munsell.chroma - expected).abs()
                                });

                                // Calculate overall distance from expected (focusing on the specific issues)
                                let distance = match color.issue_type {
                                    s if s.contains("Chroma precision") => {
                                        chroma_error.unwrap_or(0.0)
                                    },
                                    s if s.contains("Hue family") => {
                                        if hue_family_correct { 0.0 } else { 1.0 } // Binary: correct family or not
                                    },
                                    _ => 0.0,
                                };

                                let result = TestResult {
                                    illuminant: *illuminant,
                                    config_type: config_name,
                                    hue: munsell.hue,
                                    family: munsell.family,
                                    value: munsell.value,
                                    chroma: munsell.chroma,
                                    hue_family_correct,
                                    chroma_error,
                                    distance_from_expected: distance,
                                };

                                println!("{:>4} {:>18} → {:.1}{} {:.1}/{:.1} | Family: {} | Chroma Err: {:.3} | Distance: {:.3}",
                                    format!("{:?}", illuminant),
                                    config_name,
                                    result.hue,
                                    result.family,
                                    result.value,
                                    result.chroma,
                                    if result.hue_family_correct { "✓" } else { "✗" },
                                    result.chroma_error.unwrap_or(0.0),
                                    result.distance_from_expected
                                );

                                color_results.push(result.clone());
                                all_results.push((color.clone(), result));
                            }
                            Err(e) => {
                                println!("{:>4} {:>18} → Error: {}", 
                                    format!("{:?}", illuminant), config_name, e);
                            }
                        }
                    }
                    Err(e) => {
                        println!("{:>4} {:>18} → Config Error: {}", 
                            format!("{:?}", illuminant), config_name, e);
                    }
                }
            }
        }

        // Find best results for this color
        color_results.sort_by(|a, b| a.distance_from_expected.partial_cmp(&b.distance_from_expected).unwrap());
        
        println!("\nBEST RESULTS FOR {}:", color.hex);
        println!("{}", "-".repeat(50));
        for (i, result) in color_results.iter().take(5).enumerate() {
            println!("{}. {:?} ({}) → Distance: {:.3} | {:.1}{} {:.1}/{:.1}", 
                i + 1,
                result.illuminant,
                result.config_type,
                result.distance_from_expected,
                result.hue,
                result.family,
                result.value,
                result.chroma
            );
        }
        println!();
    }

    // Generate comprehensive analysis
    generate_analysis(&all_results)?;

    Ok(())
}

fn generate_analysis(results: &[(TestColor, TestResult)]) -> Result<(), Box<dyn std::error::Error>> {
    println!("\n{}", "=".repeat(100));
    println!("COMPREHENSIVE ILLUMINANT ANALYSIS REPORT");
    println!("{}", "=".repeat(100));

    // Group results by color for analysis
    let mut color_groups: std::collections::HashMap<String, Vec<&TestResult>> = std::collections::HashMap::new();
    for (color, result) in results {
        color_groups.entry(color.hex.to_string()).or_insert_with(Vec::new).push(result);
    }

    for (hex, color_results) in &color_groups {
        // Find the color info
        let color_info = results.iter()
            .find(|(c, _)| c.hex == hex)
            .map(|(c, _)| c)
            .unwrap();

        println!("\n{} - {} ANALYSIS:", hex, color_info.description.to_uppercase());
        println!("{}", "-".repeat(80));
        
        // Sort by distance from expected
        let mut sorted_results = color_results.clone();
        sorted_results.sort_by(|a, b| a.distance_from_expected.partial_cmp(&b.distance_from_expected).unwrap());
        
        println!("Issue: {}", color_info.issue_type);
        println!("Expected hue family: {:?}", color_info.expected_hue_family);
        if let Some(expected_chroma) = color_info.expected_chroma {
            println!("Expected chroma: {:.1}", expected_chroma);
        }
        
        println!("\nBest 3 illuminant configurations:");
        for (i, result) in sorted_results.iter().take(3).enumerate() {
            let improvement = if color_info.issue_type.contains("Chroma precision") {
                format!("Chroma error: {:.3}", result.chroma_error.unwrap_or(0.0))
            } else {
                format!("Family correct: {}", result.hue_family_correct)
            };
            
            println!("  {}. {:?} ({}) → {:.1}{} {:.1}/{:.1} | {} | Distance: {:.3}",
                i + 1,
                result.illuminant,
                result.config_type,
                result.hue,
                result.family,
                result.value,
                result.chroma,
                improvement,
                result.distance_from_expected
            );
        }
        
        // Check if any illuminant solves the issue
        let best_result = sorted_results.first().unwrap();
        let issue_resolved = if color_info.issue_type.contains("Chroma precision") {
            best_result.chroma_error.map(|e| e < 0.05).unwrap_or(false) // Within 0.05 tolerance
        } else {
            best_result.hue_family_correct
        };
        
        if issue_resolved {
            println!("\n✓ ISSUE RESOLVED with {:?} ({})", 
                best_result.illuminant, best_result.config_type);
        } else {
            println!("\n✗ Issue NOT resolved by any illuminant tested");
        }

        // Analyze family distribution for hue family issues
        if color_info.issue_type.contains("Hue family") {
            let mut family_counts: std::collections::HashMap<HueFamily, usize> = std::collections::HashMap::new();
            for result in color_results {
                *family_counts.entry(result.family).or_insert(0) += 1;
            }
            
            println!("\nHue family distribution across all illuminants:");
            for (family, count) in &family_counts {
                let percentage = (*count as f64 / color_results.len() as f64) * 100.0;
                let marker = if *family == color_info.expected_hue_family { "✓" } else { " " };
                println!("  {}{:?}: {} occurrences ({:.1}%)", marker, family, count, percentage);
            }
        }
    }

    println!("\n{}", "=".repeat(100));
    println!("OVERALL ILLUMINANT EFFECTIVENESS SUMMARY");
    println!("{}", "=".repeat(100));

    // Calculate average performance per illuminant
    let mut illuminant_scores: std::collections::HashMap<(Illuminant, &str), Vec<f64>> = std::collections::HashMap::new();
    
    for (_, result) in results {
        let key = (result.illuminant, result.config_type);
        illuminant_scores.entry(key).or_insert_with(Vec::new).push(result.distance_from_expected);
    }
    
    let mut avg_scores: Vec<((Illuminant, &str), f64)> = illuminant_scores
        .iter()
        .map(|(key, scores)| {
            let avg = scores.iter().sum::<f64>() / scores.len() as f64;
            (*key, avg)
        })
        .collect();
    
    avg_scores.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap());
    
    println!("\nBest illuminant configurations (lower distance = better):");
    for (i, ((illuminant, config_type), avg_distance)) in avg_scores.iter().take(10).enumerate() {
        println!("{}. {:?} ({:18}) → Avg distance: {:.4}", 
            i + 1, illuminant, config_type, avg_distance);
    }

    // Special analysis for red/purple confusion
    let rp_confusion_colors: Vec<_> = results.iter()
        .filter(|(color, _)| color.issue_type.contains("Hue family"))
        .collect();
    
    if !rp_confusion_colors.is_empty() {
        println!("\nRED/PURPLE CONFUSION ANALYSIS:");
        println!("{}", "-".repeat(50));
        
        let mut correct_family_count = 0;
        let total_rp_tests = rp_confusion_colors.len();
        
        for (color, result) in &rp_confusion_colors {
            if result.hue_family_correct {
                correct_family_count += 1;
                println!("✓ {} resolved with {:?} ({}): {:.1}{} instead of RP family",
                    color.hex, result.illuminant, result.config_type, 
                    result.hue, result.family);
            }
        }
        
        let success_rate = (correct_family_count as f64 / total_rp_tests as f64) * 100.0;
        println!("\nRed/Purple classification success rate: {:.1}% ({}/{} tests)", 
            success_rate, correct_family_count, total_rp_tests);
    }

    Ok(())
}