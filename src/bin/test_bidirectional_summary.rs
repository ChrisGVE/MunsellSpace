/// Bidirectional consistency test with clean summary output
/// Provides executive summary without debug output for production use

use munsellspace::{MunsellConverter, ReverseConverter};
use munsellspace::python_converter::PythonMunsellConverter;
use munsellspace::reverse_conversion::{parse_munsell_notation, ColorFormats};
use std::collections::HashMap;
use std::time::Instant;
use std::env;

/// Test result for a single round-trip conversion
#[derive(Debug, Clone)]
struct RoundTripResult {
    original_rgb: [u8; 3],
    munsell_notation: String,
    converted_rgb: [u8; 3],
    rgb_delta: f64,
    max_component_diff: u8,
}

/// Summary statistics for test results
#[derive(Debug, Default)]
struct TestSummary {
    total_tests: usize,
    successful_conversions: usize,
    excellent_roundtrips: usize,  // RGB delta < 10
    good_roundtrips: usize,       // RGB delta < 30
    poor_roundtrips: usize,       // RGB delta >= 30
    failed_conversions: usize,
    total_rgb_delta: f64,
    max_rgb_delta: f64,
    max_component_delta: u8,
    category_results: HashMap<String, CategoryResult>,
}

#[derive(Debug, Default)]
struct CategoryResult {
    count: usize,
    successful: usize,
    avg_delta: f64,
    max_delta: f64,
    excellent: usize,
    good: usize,
    poor: usize,
}

impl TestSummary {
    fn add_result(&mut self, result: &RoundTripResult, category: &str, success: bool) {
        self.total_tests += 1;
        
        if success {
            self.successful_conversions += 1;
            self.total_rgb_delta += result.rgb_delta;
            
            if result.rgb_delta < 10.0 {
                self.excellent_roundtrips += 1;
            } else if result.rgb_delta < 30.0 {
                self.good_roundtrips += 1;
            } else {
                self.poor_roundtrips += 1;
            }
            
            if result.rgb_delta > self.max_rgb_delta {
                self.max_rgb_delta = result.rgb_delta;
            }
            
            if result.max_component_diff > self.max_component_delta {
                self.max_component_delta = result.max_component_diff;
            }
        } else {
            self.failed_conversions += 1;
        }
        
        // Update category statistics
        let cat_result = self.category_results.entry(category.to_string()).or_default();
        cat_result.count += 1;
        if success {
            cat_result.successful += 1;
            cat_result.avg_delta += result.rgb_delta;
            if result.rgb_delta > cat_result.max_delta {
                cat_result.max_delta = result.rgb_delta;
            }
            
            if result.rgb_delta < 10.0 {
                cat_result.excellent += 1;
            } else if result.rgb_delta < 30.0 {
                cat_result.good += 1;
            } else {
                cat_result.poor += 1;
            }
        }
    }
    
    fn finalize(&mut self) {
        // Calculate category averages
        for result in self.category_results.values_mut() {
            if result.successful > 0 {
                result.avg_delta /= result.successful as f64;
            }
        }
    }
    
    fn print_executive_summary(&self) {
        let success_rate = if self.total_tests > 0 {
            (self.successful_conversions as f64 / self.total_tests as f64) * 100.0
        } else { 0.0 };
        
        let avg_delta = if self.successful_conversions > 0 {
            self.total_rgb_delta / self.successful_conversions as f64
        } else { 0.0 };
        
        let excellent_rate = (self.excellent_roundtrips as f64 / self.successful_conversions as f64) * 100.0;
        let good_rate = (self.good_roundtrips as f64 / self.successful_conversions as f64) * 100.0;
        let poor_rate = (self.poor_roundtrips as f64 / self.successful_conversions as f64) * 100.0;
        
        println!("🎯 BIDIRECTIONAL CONSISTENCY EXECUTIVE SUMMARY");
        println!("=============================================");
        println!("Success Rate:     {:.1}% ({}/{})", success_rate, self.successful_conversions, self.total_tests);
        println!("Average RGB Δ:    {:.2}", avg_delta);
        println!("Max RGB Δ:        {:.2}", self.max_rgb_delta);
        println!("Max Component Δ:  {}", self.max_component_delta);
        println!();
        println!("Quality Distribution:");
        println!("  🟢 Excellent (Δ<10): {:.1}% ({} colors)", excellent_rate, self.excellent_roundtrips);
        println!("  🟡 Good (10≤Δ<30):   {:.1}% ({} colors)", good_rate, self.good_roundtrips);
        println!("  🔴 Poor (Δ≥30):      {:.1}% ({} colors)", poor_rate, self.poor_roundtrips);
        println!();
        
        // Category breakdown
        println!("📂 Performance by Category:");
        let mut categories: Vec<_> = self.category_results.iter().collect();
        categories.sort_by_key(|(name, _)| *name);
        
        for (name, result) in categories {
            let cat_success_rate = (result.successful as f64 / result.count as f64) * 100.0;
            let cat_excellent_rate = if result.successful > 0 {
                (result.excellent as f64 / result.successful as f64) * 100.0
            } else { 0.0 };
            
            println!("  {:15} {:3}/{:2} ({:4.1}%) excellent:{:4.1}% avg_Δ:{:5.2}", 
                     name, result.successful, result.count, cat_success_rate, 
                     cat_excellent_rate, result.avg_delta);
        }
    }
}

fn calculate_rgb_delta(rgb1: [u8; 3], rgb2: [u8; 3]) -> (f64, u8) {
    let dr = (rgb1[0] as i16 - rgb2[0] as i16).abs() as f64;
    let dg = (rgb1[1] as i16 - rgb2[1] as i16).abs() as f64;
    let db = (rgb1[2] as i16 - rgb2[2] as i16).abs() as f64;
    
    let euclidean_delta = (dr * dr + dg * dg + db * db).sqrt();
    let max_component = [dr as u8, dg as u8, db as u8].iter().max().cloned().unwrap_or(0);
    
    (euclidean_delta, max_component)
}

fn test_round_trip_conversion(
    forward_converter: &MunsellConverter,
    reverse_converter: &PythonMunsellConverter,
    rgb: [u8; 3],
) -> Option<RoundTripResult> {
    // Forward: RGB → Munsell
    let munsell = match forward_converter.srgb_to_munsell(rgb) {
        Ok(color) => color,
        Err(_) => return None,
    };
    
    // Reverse: Munsell → RGB
    let rgb_back = match reverse_converter.munsell_to_srgb(&munsell.notation) {
        Ok(color) => [color.r, color.g, color.b],
        Err(_) => return None,
    };
    
    let (rgb_delta, max_component_diff) = calculate_rgb_delta(rgb, rgb_back);
    
    Some(RoundTripResult {
        original_rgb: rgb,
        munsell_notation: munsell.notation,
        converted_rgb: rgb_back,
        rgb_delta,
        max_component_diff,
    })
}

fn run_comprehensive_test_suite() -> Result<TestSummary, Box<dyn std::error::Error>> {
    // Disable debug output for clean testing
    env::set_var("DEBUG_MUNSELL", "0");
    
    let forward_converter = MunsellConverter::new()?;
    let reverse_converter = PythonMunsellConverter::new();
    let mut summary = TestSummary::default();
    
    // Primary colors
    let primary_colors = vec![
        ([255, 0, 0], "Pure red"),
        ([0, 255, 0], "Pure green"), 
        ([0, 0, 255], "Pure blue"),
    ];
    
    for (rgb, desc) in &primary_colors {
        if let Some(result) = test_round_trip_conversion(&forward_converter, &reverse_converter, *rgb) {
            summary.add_result(&result, "Primary", true);
        } else {
            summary.add_result(&RoundTripResult {
                original_rgb: *rgb,
                munsell_notation: "FAILED".to_string(),
                converted_rgb: [0, 0, 0],
                rgb_delta: 999.0,
                max_component_diff: 255,
            }, "Primary", false);
        }
    }
    
    // Secondary colors
    let secondary_colors = vec![
        ([255, 255, 0], "Yellow"),
        ([255, 0, 255], "Magenta"),
        ([0, 255, 255], "Cyan"),
    ];
    
    for (rgb, desc) in &secondary_colors {
        if let Some(result) = test_round_trip_conversion(&forward_converter, &reverse_converter, *rgb) {
            summary.add_result(&result, "Secondary", true);
        } else {
            summary.add_result(&RoundTripResult {
                original_rgb: *rgb,
                munsell_notation: "FAILED".to_string(),
                converted_rgb: [0, 0, 0],
                rgb_delta: 999.0,
                max_component_diff: 255,
            }, "Secondary", false);
        }
    }
    
    // Neutral colors - test a subset for clean results
    let neutral_colors = vec![
        ([64, 64, 64], "Dark gray"),
        ([128, 128, 128], "Medium gray"),
        ([192, 192, 192], "Light gray"),
    ];
    
    for (rgb, desc) in &neutral_colors {
        if let Some(result) = test_round_trip_conversion(&forward_converter, &reverse_converter, *rgb) {
            summary.add_result(&result, "Neutral", true);
        } else {
            summary.add_result(&RoundTripResult {
                original_rgb: *rgb,
                munsell_notation: "FAILED".to_string(),
                converted_rgb: [0, 0, 0],
                rgb_delta: 999.0,
                max_component_diff: 255,
            }, "Neutral", false);
        }
    }
    
    // Common web colors
    let web_colors = vec![
        ([255, 165, 0], "Orange"),
        ([255, 192, 203], "Pink"),
        ([128, 0, 128], "Purple"),
        ([165, 42, 42], "Brown"),
        ([255, 20, 147], "Deep pink"),
        ([75, 0, 130], "Indigo"),
        ([238, 130, 238], "Violet"),
        ([240, 230, 140], "Khaki"),
    ];
    
    for (rgb, desc) in &web_colors {
        if let Some(result) = test_round_trip_conversion(&forward_converter, &reverse_converter, *rgb) {
            summary.add_result(&result, "Web Colors", true);
        } else {
            summary.add_result(&RoundTripResult {
                original_rgb: *rgb,
                munsell_notation: "FAILED".to_string(),
                converted_rgb: [0, 0, 0],
                rgb_delta: 999.0,
                max_component_diff: 255,
            }, "Web Colors", false);
        }
    }
    
    // Test some Munsell notation formats through reverse conversion
    let munsell_tests = vec![
        "5R 4/14",
        "2.5YR 6/12",
        "N5/0", 
        "10RP 3/4",
        "7.5B 5/8",
    ];
    
    for munsell_str in &munsell_tests {
        if let Ok(spec) = parse_munsell_notation(munsell_str) {
            let reverse_conv = ReverseConverter::new()?;
            if let Ok(formats) = reverse_conv.munsell_to_all_formats(&spec) {
                if let Some(result) = test_round_trip_conversion(
                    &forward_converter,
                    &reverse_converter,
                    formats.srgb
                ) {
                    summary.add_result(&result, "Munsell Format", true);
                } else {
                    summary.add_result(&RoundTripResult {
                        original_rgb: formats.srgb,
                        munsell_notation: munsell_str.to_string(),
                        converted_rgb: [0, 0, 0],
                        rgb_delta: 999.0,
                        max_component_diff: 255,
                    }, "Munsell Format", false);
                }
            }
        }
    }
    
    summary.finalize();
    Ok(summary)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔄 MUNSELL SPACE BIDIRECTIONAL CONSISTENCY TEST");
    println!("===============================================");
    println!("Running comprehensive round-trip accuracy analysis...\n");
    
    let start_time = Instant::now();
    let summary = run_comprehensive_test_suite()?;
    let elapsed = start_time.elapsed();
    
    summary.print_executive_summary();
    
    println!();
    println!("⏱️  Test completed in {:.2}s", elapsed.as_secs_f64());
    
    // Provide interpretation
    println!("\n📝 INTERPRETATION:");
    let success_rate = (summary.successful_conversions as f64 / summary.total_tests as f64) * 100.0;
    let excellent_rate = (summary.excellent_roundtrips as f64 / summary.successful_conversions as f64) * 100.0;
    
    if success_rate >= 90.0 && excellent_rate >= 70.0 {
        println!("✅ EXCELLENT: High conversion success and accuracy");
    } else if success_rate >= 75.0 && excellent_rate >= 50.0 {
        println!("⚠️  GOOD: Reasonable conversion quality with room for improvement");
    } else {
        println!("❌ POOR: Significant conversion accuracy issues need attention");
    }
    
    if summary.max_rgb_delta > 50.0 {
        println!("⚠️  WARNING: Some colors have very large round-trip errors (Δ > 50)");
    }
    
    println!("\nRecommendations:");
    if summary.failed_conversions > 0 {
        println!("• Fix neutral color conversion issues (likely parsing problems)");
    }
    if summary.poor_roundtrips > summary.excellent_roundtrips {
        println!("• Investigate mathematical conversion calibration");
    }
    if summary.max_component_delta > 30 {
        println!("• Review color space transformation accuracy");
    }
    
    Ok(())
}