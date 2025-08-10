//! Comprehensive Illuminant Precision Testing Tool
//!
//! Tests different illuminants on precision issue colors to determine if illuminant
//! changes can resolve red/purple confusion and chroma precision errors affecting
//! ISCC-NBS classification accuracy.

use munsellspace::mathematical_v2::{MathematicalMunsellConverter, MunsellConfig, MunsellSpecification};
use munsellspace::illuminants::{Illuminant, ChromaticAdaptationMethod};
use std::fs::File;
use std::io::Write;
use std::collections::HashMap;

/// Color with precision issue details
#[derive(Debug, Clone)]
struct PrecisionTestColor {
    rgb: [u8; 3],
    hex: String,
    name: String,
    expected_munsell: String,
    current_result: String,
    issue_type: String,
    expected_chroma: Option<f64>,
    expected_family: Option<String>,
}

/// Test result for a specific color/illuminant combination
#[derive(Debug, Clone)]
struct IlluminantTestResult {
    illuminant: Illuminant,
    illuminant_name: String,
    munsell_hue: f64,
    munsell_family: String,
    munsell_value: f64,
    munsell_chroma: f64,
    notation: String,
    improvement_score: f64,
}

/// Comprehensive test results for all colors and illuminants
#[derive(Debug)]
struct ComprehensiveResults {
    color_results: HashMap<String, Vec<IlluminantTestResult>>,
    best_illuminant_per_color: HashMap<String, IlluminantTestResult>,
    overall_best_illuminant: Option<Illuminant>,
    summary_statistics: SummaryStatistics,
}

#[derive(Debug)]
struct SummaryStatistics {
    total_tests: usize,
    colors_improved: usize,
    average_improvement: f64,
    best_illuminant_frequency: HashMap<Illuminant, usize>,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 COMPREHENSIVE ILLUMINANT PRECISION TESTING");
    println!("==============================================");
    println!("Testing different illuminants on precision issue colors");
    println!("to determine optimal configuration for ISCC-NBS classification.\n");
    
    // Define precision issue colors with detailed analysis
    let test_colors = create_precision_test_colors();
    
    // Define all illuminants to test
    let illuminants = vec![
        (Illuminant::D65, "D65 (Daylight 6500K)"),
        (Illuminant::C, "C (Average Daylight - Munsell Standard)"),
        (Illuminant::A, "A (Tungsten Incandescent)"),
        (Illuminant::D50, "D50 (Daylight 5000K)"),
        (Illuminant::F2, "F2 (Cool White Fluorescent)"),
        (Illuminant::F7, "F7 (Daylight Fluorescent)"),
        (Illuminant::F11, "F11 (Narrow Band Fluorescent)"),
        (Illuminant::E, "E (Equal Energy)"),
    ];
    
    // Run comprehensive testing
    let results = run_comprehensive_illuminant_test(&test_colors, &illuminants)?;
    
    // Generate detailed report
    generate_illuminant_precision_report(&test_colors, &results)?;
    
    // Display summary
    display_summary(&results);
    
    println!("\n✅ Complete illuminant precision analysis saved to:");
    println!("📄 ILLUMINANT_PRECISION_ANALYSIS_REPORT.md");
    
    Ok(())
}

/// Create the 4 precision issue colors with detailed analysis
fn create_precision_test_colors() -> Vec<PrecisionTestColor> {
    vec![
        PrecisionTestColor {
            rgb: [239, 221, 229],
            hex: "#EFDDE5".to_string(),
            name: "Precision Case 1".to_string(),
            expected_munsell: "pinkish white".to_string(),
            current_result: "pale yellowish pink (9.8R 9.1/1.6)".to_string(),
            issue_type: "Chroma precision - needs 1.5 instead of 1.6".to_string(),
            expected_chroma: Some(1.5),
            expected_family: Some("R".to_string()),
        },
        PrecisionTestColor {
            rgb: [92, 6, 37],
            hex: "#5C0625".to_string(), 
            name: "Precision Case 2".to_string(),
            expected_munsell: "very deep red".to_string(),
            current_result: "very dark purplish red (6.6RP 1.6/6.3)".to_string(),
            issue_type: "Family confusion - RP instead of R family".to_string(),
            expected_chroma: None,
            expected_family: Some("R".to_string()),
        },
        PrecisionTestColor {
            rgb: [199, 182, 189],
            hex: "#C7B6BD".to_string(),
            name: "Precision Case 3".to_string(), 
            expected_munsell: "pinkish gray".to_string(),
            current_result: "grayish yellowish pink (3YR 7.5/1.6)".to_string(),
            issue_type: "Chroma precision - needs 1.5 instead of 1.6".to_string(),
            expected_chroma: Some(1.5),
            expected_family: Some("R".to_string()),
        },
        PrecisionTestColor {
            rgb: [72, 17, 39],
            hex: "#481127".to_string(),
            name: "Precision Case 4".to_string(),
            expected_munsell: "very dark red".to_string(), 
            current_result: "very dark purplish red (3.7RP 1.3/4.0)".to_string(),
            issue_type: "Family confusion - RP instead of R family".to_string(),
            expected_chroma: None,
            expected_family: Some("R".to_string()),
        },
    ]
}

/// Run comprehensive testing across all color/illuminant combinations
fn run_comprehensive_illuminant_test(
    test_colors: &[PrecisionTestColor],
    illuminants: &[(Illuminant, &str)],
) -> Result<ComprehensiveResults, Box<dyn std::error::Error>> {
    
    let mut color_results = HashMap::new();
    let mut best_illuminant_per_color = HashMap::new();
    
    println!("Running {} × {} = {} total tests...", 
             test_colors.len(), illuminants.len(), 
             test_colors.len() * illuminants.len());
    
    for test_color in test_colors {
        println!("\n🎨 Testing {} ({})", test_color.name, test_color.hex);
        
        let mut results_for_color = Vec::new();
        let mut best_result: Option<IlluminantTestResult> = None;
        
        for (illuminant, illuminant_name) in illuminants {
            // Test with source=D65, target=illuminant (standard approach)
            let config = MunsellConfig {
                source_illuminant: Illuminant::D65,  // sRGB standard
                target_illuminant: *illuminant,
                adaptation_method: ChromaticAdaptationMethod::Bradford,
            };
            
            let converter = MathematicalMunsellConverter::with_config(config)?;
            
            match converter.srgb_to_munsell(test_color.rgb) {
                Ok(munsell) => {
                    let notation = format!("{:.1}{} {:.1}/{:.1}", 
                                         munsell.hue, munsell.family, 
                                         munsell.value, munsell.chroma);
                    
                    // Calculate improvement score based on issue type
                    let improvement_score = calculate_improvement_score(&test_color, &munsell);
                    
                    let result = IlluminantTestResult {
                        illuminant: *illuminant,
                        illuminant_name: illuminant_name.to_string(),
                        munsell_hue: munsell.hue,
                        munsell_family: munsell.family,
                        munsell_value: munsell.value,
                        munsell_chroma: munsell.chroma,
                        notation: notation.clone(),
                        improvement_score,
                    };
                    
                    println!("  {} → {} (score: {:.3})", 
                             illuminant_name, notation, improvement_score);
                    
                    // Track best result for this color
                    if best_result.is_none() || improvement_score > best_result.as_ref().unwrap().improvement_score {
                        best_result = Some(result.clone());
                    }
                    
                    results_for_color.push(result);
                }
                Err(e) => {
                    println!("  {} → Error: {}", illuminant_name, e);
                }
            }
        }
        
        color_results.insert(test_color.hex.clone(), results_for_color);
        if let Some(best) = best_result {
            best_illuminant_per_color.insert(test_color.hex.clone(), best);
        }
    }
    
    // Calculate overall statistics
    let summary_statistics = calculate_summary_statistics(&color_results, &best_illuminant_per_color);
    let overall_best_illuminant = determine_overall_best_illuminant(&summary_statistics);
    
    Ok(ComprehensiveResults {
        color_results,
        best_illuminant_per_color,
        overall_best_illuminant,
        summary_statistics,
    })
}

/// Calculate improvement score based on the specific issue type
fn calculate_improvement_score(test_color: &PrecisionTestColor, munsell: &MunsellSpecification) -> f64 {
    let mut score = 0.0;
    
    // Score based on expected chroma (higher score for closer to expected)
    if let Some(expected_chroma) = test_color.expected_chroma {
        let chroma_diff = (munsell.chroma - expected_chroma).abs();
        score += (2.0 - chroma_diff).max(0.0); // Higher score for smaller difference
    }
    
    // Score based on expected family (bonus for correct family)
    if let Some(expected_family) = &test_color.expected_family {
        if munsell.family.contains(expected_family) {
            score += 3.0; // Significant bonus for correct family
        }
    }
    
    // Base score for reasonable values
    if munsell.value > 0.0 && munsell.chroma >= 0.0 {
        score += 1.0;
    }
    
    score
}

/// Calculate summary statistics across all tests
fn calculate_summary_statistics(
    color_results: &HashMap<String, Vec<IlluminantTestResult>>,
    best_per_color: &HashMap<String, IlluminantTestResult>,
) -> SummaryStatistics {
    let total_tests = color_results.values().map(|v| v.len()).sum();
    let colors_improved = best_per_color.len();
    
    let average_improvement = if colors_improved > 0 {
        best_per_color.values().map(|r| r.improvement_score).sum::<f64>() / colors_improved as f64
    } else {
        0.0
    };
    
    let mut best_illuminant_frequency = HashMap::new();
    for result in best_per_color.values() {
        *best_illuminant_frequency.entry(result.illuminant).or_insert(0) += 1;
    }
    
    SummaryStatistics {
        total_tests,
        colors_improved,
        average_improvement,
        best_illuminant_frequency,
    }
}

/// Determine overall best illuminant based on frequency and performance
fn determine_overall_best_illuminant(stats: &SummaryStatistics) -> Option<Illuminant> {
    stats.best_illuminant_frequency
        .iter()
        .max_by_key(|(_, &count)| count)
        .map(|(&illuminant, _)| illuminant)
}

/// Generate comprehensive markdown report
fn generate_illuminant_precision_report(
    test_colors: &[PrecisionTestColor],
    results: &ComprehensiveResults,
) -> Result<(), Box<dyn std::error::Error>> {
    
    let mut report = File::create("ILLUMINANT_PRECISION_ANALYSIS_REPORT.md")?;
    
    writeln!(report, "# Illuminant Precision Analysis Report")?;
    writeln!(report, "")?;
    writeln!(report, "## Executive Summary")?;
    writeln!(report, "")?;
    writeln!(report, "- **Total Tests**: {}", results.summary_statistics.total_tests)?;
    writeln!(report, "- **Colors Analyzed**: {}", test_colors.len())?;
    writeln!(report, "- **Average Improvement Score**: {:.3}", results.summary_statistics.average_improvement)?;
    
    if let Some(best_illuminant) = results.overall_best_illuminant {
        writeln!(report, "- **Recommended Illuminant**: {:?}", best_illuminant)?;
    }
    
    writeln!(report, "")?;
    writeln!(report, "## Test Colors Analysis")?;
    writeln!(report, "")?;
    
    for test_color in test_colors {
        writeln!(report, "### {} ({})", test_color.name, test_color.hex)?;
        writeln!(report, "")?;
        writeln!(report, "- **RGB**: {:?}", test_color.rgb)?;
        writeln!(report, "- **Expected**: {}", test_color.expected_munsell)?;
        writeln!(report, "- **Current Result**: {}", test_color.current_result)?;
        writeln!(report, "- **Issue Type**: {}", test_color.issue_type)?;
        writeln!(report, "")?;
        
        if let Some(results_for_color) = results.color_results.get(&test_color.hex) {
            writeln!(report, "| Illuminant | Munsell Result | Improvement Score |")?;
            writeln!(report, "|------------|----------------|-------------------|")?;
            
            for result in results_for_color {
                writeln!(report, "| {} | {} | {:.3} |", 
                        result.illuminant_name, result.notation, result.improvement_score)?;
            }
        }
        
        if let Some(best_result) = results.best_illuminant_per_color.get(&test_color.hex) {
            writeln!(report, "")?;
            writeln!(report, "**Best Result**: {} with {} (score: {:.3})", 
                    best_result.illuminant_name, best_result.notation, best_result.improvement_score)?;
        }
        
        writeln!(report, "")?;
    }
    
    writeln!(report, "## Illuminant Performance Summary")?;
    writeln!(report, "")?;
    writeln!(report, "| Illuminant | Times Best | Description |")?;
    writeln!(report, "|------------|------------|-------------|")?;
    
    for (&illuminant, &count) in &results.summary_statistics.best_illuminant_frequency {
        let description = match illuminant {
            Illuminant::D65 => "Standard sRGB illuminant (daylight 6500K)",
            Illuminant::C => "Munsell standard (average daylight)",
            Illuminant::A => "Tungsten incandescent lighting",
            Illuminant::D50 => "Daylight 5000K (graphic arts standard)",
            Illuminant::F2 => "Cool white fluorescent",
            _ => "Alternative illuminant",
        };
        writeln!(report, "| {:?} | {} | {} |", illuminant, count, description)?;
    }
    
    writeln!(report, "")?;
    writeln!(report, "## Conclusions and Recommendations")?;
    writeln!(report, "")?;
    
    if let Some(best_illuminant) = results.overall_best_illuminant {
        writeln!(report, "### Recommended Configuration")?;
        writeln!(report, "")?;
        writeln!(report, "Based on the analysis, **{:?}** provides the best overall performance", best_illuminant)?;
        writeln!(report, "for resolving precision issues in ISCC-NBS color classification.")?;
        writeln!(report, "")?;
        writeln!(report, "**Optimal Settings:**")?;
        writeln!(report, "- Source Illuminant: D65 (sRGB standard)")?;
        writeln!(report, "- Target Illuminant: {:?}", best_illuminant)?;
        writeln!(report, "- Chromatic Adaptation: Bradford method")?;
        writeln!(report, "")?;
    }
    
    writeln!(report, "### Implementation")?;
    writeln!(report, "")?;
    writeln!(report, "```rust")?;
    writeln!(report, "use munsellspace::mathematical_v2::{{MathematicalMunsellConverter, MunsellConfig}};")?;
    writeln!(report, "use munsellspace::illuminants::{{Illuminant, ChromaticAdaptationMethod}};")?;
    writeln!(report, "")?;
    writeln!(report, "let config = MunsellConfig {{")?;
    writeln!(report, "    source_illuminant: Illuminant::D65,")?;
    if let Some(best_illuminant) = results.overall_best_illuminant {
        writeln!(report, "    target_illuminant: Illuminant::{:?},", best_illuminant)?;
    }
    writeln!(report, "    adaptation_method: ChromaticAdaptationMethod::Bradford,")?;
    writeln!(report, "}};")?;
    writeln!(report, "")?;
    writeln!(report, "let converter = MathematicalMunsellConverter::with_config(config)?;")?;
    writeln!(report, "```")?;
    
    writeln!(report, "")?;
    writeln!(report, "---")?;
    writeln!(report, "Report generated by MunsellSpace Illuminant Precision Testing Tool")?;
    
    Ok(())
}

/// Display summary to console
fn display_summary(results: &ComprehensiveResults) {
    println!("\n📊 ANALYSIS SUMMARY");
    println!("===================");
    println!("Total tests conducted: {}", results.summary_statistics.total_tests);
    println!("Average improvement score: {:.3}", results.summary_statistics.average_improvement);
    
    if let Some(best_illuminant) = results.overall_best_illuminant {
        let best_count = results.summary_statistics.best_illuminant_frequency
            .get(&best_illuminant).unwrap_or(&0);
        println!("Best performing illuminant: {:?} (best for {}/{} colors)", 
                best_illuminant, best_count, results.best_illuminant_per_color.len());
    }
    
    println!("\n🏆 BEST RESULTS PER COLOR:");
    for (hex, result) in &results.best_illuminant_per_color {
        println!("  {} → {} with {} (score: {:.3})", 
                hex, result.illuminant_name, result.notation, result.improvement_score);
    }
}