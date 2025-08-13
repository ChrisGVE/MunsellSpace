/// Comprehensive bidirectional consistency tests for MunsellSpace library
/// Tests RGB ↔ Munsell round-trip conversions for accuracy and reliability

use munsellspace::{MunsellConverter, ReverseConverter};
use munsellspace::python_converter::PythonMunsellConverter;
use munsellspace::reverse_conversion::{parse_munsell_notation, ColorFormats};
use munsellspace::mathematical::MunsellSpecification;
use std::collections::HashMap;
use std::time::Instant;

/// Test result for a single round-trip conversion
#[derive(Debug, Clone)]
struct RoundTripResult {
    original_rgb: [u8; 3],
    munsell_notation: String,
    converted_rgb: [u8; 3],
    rgb_delta: f64,
    max_component_diff: u8,
    description: String,
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
    
    fn print_summary(&self) {
        println!("\n🎯 BIDIRECTIONAL CONSISTENCY TEST SUMMARY");
        println!("========================================");
        
        let success_rate = if self.total_tests > 0 {
            (self.successful_conversions as f64 / self.total_tests as f64) * 100.0
        } else { 0.0 };
        
        let avg_delta = if self.successful_conversions > 0 {
            self.total_rgb_delta / self.successful_conversions as f64
        } else { 0.0 };
        
        println!("📊 Overall Statistics:");
        println!("  Total tests:           {}", self.total_tests);
        println!("  Successful conversions: {} ({:.1}%)", self.successful_conversions, success_rate);
        println!("  Failed conversions:     {}", self.failed_conversions);
        println!();
        
        println!("🔄 Round-trip Quality:");
        println!("  Excellent (Δ < 10):     {} ({:.1}%)", 
                 self.excellent_roundtrips, 
                 (self.excellent_roundtrips as f64 / self.successful_conversions as f64) * 100.0);
        println!("  Good (10 ≤ Δ < 30):     {} ({:.1}%)", 
                 self.good_roundtrips,
                 (self.good_roundtrips as f64 / self.successful_conversions as f64) * 100.0);
        println!("  Poor (Δ ≥ 30):          {} ({:.1}%)", 
                 self.poor_roundtrips,
                 (self.poor_roundtrips as f64 / self.successful_conversions as f64) * 100.0);
        println!();
        
        println!("📏 RGB Delta Statistics:");
        println!("  Average RGB delta:      {:.2}", avg_delta);
        println!("  Maximum RGB delta:      {:.2}", self.max_rgb_delta);
        println!("  Max component delta:    {}", self.max_component_delta);
        println!();
        
        println!("📂 Category Breakdown:");
        let mut categories: Vec<_> = self.category_results.iter().collect();
        categories.sort_by_key(|(name, _)| *name);
        
        for (name, result) in categories {
            let success_rate = (result.successful as f64 / result.count as f64) * 100.0;
            println!("  {:15} {:3}/{} ({:5.1}%) avg_Δ={:5.2} max_Δ={:5.2}", 
                     name, result.successful, result.count, success_rate,
                     result.avg_delta, result.max_delta);
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
    description: &str,
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
        description: description.to_string(),
    })
}

fn test_munsell_notation_formats() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔤 Testing Munsell Notation Format Support");
    println!("==========================================");
    
    let reverse_converter = PythonMunsellConverter::new();
    let forward_converter = MunsellConverter::new()?;
    
    let notation_tests = vec![
        ("5R 4/14", "Standard format"),
        ("2.5YR 6/12", "Decimal hue"),
        ("N 5", "Neutral short"),
        ("N5", "Neutral compact"),
        ("N 5/", "Neutral with slash"),
        ("N5/0", "Neutral with explicit zero chroma"),
        ("N 5/0.0", "Neutral with decimal zero chroma"),
        ("10RP 3/4", "10 hue (boundary case)"),
        ("7.5B 5/8", "Decimal mid-hue"),
        ("1R 2/6", "Low hue number"),
        ("5R 9/2", "High value, low chroma"),
        ("5R 1/2", "Low value, low chroma"),
    ];
    
    let mut format_summary = TestSummary::default();
    
    for (notation, description) in &notation_tests {
        print!("{:15} ({:20}) → ", notation, description);
        
        match reverse_converter.munsell_to_srgb(notation) {
            Ok(rgb) => {
                println!("RGB [{:3}, {:3}, {:3}]", rgb.r, rgb.g, rgb.b);
                
                // Test reverse conversion
                let test_rgb = [rgb.r, rgb.g, rgb.b];
                if let Some(result) = test_round_trip_conversion(
                    &forward_converter, 
                    &reverse_converter, 
                    test_rgb, 
                    description
                ) {
                    format_summary.add_result(&result, "Notation Format", true);
                    
                    if result.rgb_delta < 10.0 {
                        println!("    ✅ Excellent round-trip (Δ={:.2})", result.rgb_delta);
                    } else if result.rgb_delta < 30.0 {
                        println!("    ⚠️  Good round-trip (Δ={:.2})", result.rgb_delta);
                    } else {
                        println!("    ❌ Poor round-trip (Δ={:.2})", result.rgb_delta);
                    }
                } else {
                    format_summary.add_result(&RoundTripResult {
                        original_rgb: test_rgb,
                        munsell_notation: notation.to_string(),
                        converted_rgb: [0, 0, 0],
                        rgb_delta: 999.0,
                        max_component_diff: 255,
                        description: description.to_string(),
                    }, "Notation Format", false);
                    println!("    ❌ Round-trip failed");
                }
            }
            Err(e) => {
                println!("PARSE ERROR: {}", e);
                format_summary.add_result(&RoundTripResult {
                    original_rgb: [0, 0, 0],
                    munsell_notation: notation.to_string(),
                    converted_rgb: [0, 0, 0],
                    rgb_delta: 999.0,
                    max_component_diff: 255,
                    description: description.to_string(),
                }, "Notation Format", false);
            }
        }
    }
    
    format_summary.finalize();
    format_summary.print_summary();
    
    Ok(())
}

fn test_color_categories() -> Result<(), Box<dyn std::error::Error>> {
    println!("\n🎨 Testing Color Category Consistency");
    println!("=====================================");
    
    let forward_converter = MunsellConverter::new()?;
    let reverse_converter = PythonMunsellConverter::new();
    let mut summary = TestSummary::default();
    
    // Primary colors
    let primary_colors = vec![
        ([255, 0, 0], "Pure red"),
        ([0, 255, 0], "Pure green"),
        ([0, 0, 255], "Pure blue"),
    ];
    
    println!("\n🔴 Primary Colors:");
    for (rgb, desc) in &primary_colors {
        if let Some(result) = test_round_trip_conversion(&forward_converter, &reverse_converter, *rgb, desc) {
            println!("  {:12} RGB{:?} ↔ {} → RGB{:?} (Δ={:.2})", 
                desc, result.original_rgb, result.munsell_notation, result.converted_rgb, result.rgb_delta);
            summary.add_result(&result, "Primary", true);
        } else {
            println!("  {:12} RGB{:?} → FAILED", desc, rgb);
            summary.add_result(&RoundTripResult {
                original_rgb: *rgb,
                munsell_notation: "FAILED".to_string(),
                converted_rgb: [0, 0, 0],
                rgb_delta: 999.0,
                max_component_diff: 255,
                description: desc.to_string(),
            }, "Primary", false);
        }
    }
    
    // Secondary colors
    let secondary_colors = vec![
        ([255, 255, 0], "Yellow"),
        ([255, 0, 255], "Magenta"),
        ([0, 255, 255], "Cyan"),
    ];
    
    println!("\n🟡 Secondary Colors:");
    for (rgb, desc) in &secondary_colors {
        if let Some(result) = test_round_trip_conversion(&forward_converter, &reverse_converter, *rgb, desc) {
            println!("  {:12} RGB{:?} ↔ {} → RGB{:?} (Δ={:.2})", 
                desc, result.original_rgb, result.munsell_notation, result.converted_rgb, result.rgb_delta);
            summary.add_result(&result, "Secondary", true);
        } else {
            println!("  {:12} RGB{:?} → FAILED", desc, rgb);
            summary.add_result(&RoundTripResult {
                original_rgb: *rgb,
                munsell_notation: "FAILED".to_string(),
                converted_rgb: [0, 0, 0],
                rgb_delta: 999.0,
                max_component_diff: 255,
                description: desc.to_string(),
            }, "Secondary", false);
        }
    }
    
    // Neutral colors (grays)
    let neutral_colors = vec![
        ([0, 0, 0], "Pure black"),
        ([32, 32, 32], "Very dark gray"),
        ([64, 64, 64], "Dark gray"),
        ([128, 128, 128], "Medium gray"),
        ([192, 192, 192], "Light gray"),
        ([224, 224, 224], "Very light gray"),
        ([248, 248, 248], "Near white"),
    ];
    
    println!("\n⚫ Neutral Colors (Grays):");
    for (rgb, desc) in &neutral_colors {
        if let Some(result) = test_round_trip_conversion(&forward_converter, &reverse_converter, *rgb, desc) {
            println!("  {:16} RGB{:?} ↔ {} → RGB{:?} (Δ={:.2})", 
                desc, result.original_rgb, result.munsell_notation, result.converted_rgb, result.rgb_delta);
            summary.add_result(&result, "Neutral", true);
        } else {
            println!("  {:16} RGB{:?} → FAILED", desc, rgb);
            summary.add_result(&RoundTripResult {
                original_rgb: *rgb,
                munsell_notation: "FAILED".to_string(),
                converted_rgb: [0, 0, 0],
                rgb_delta: 999.0,
                max_component_diff: 255,
                description: desc.to_string(),
            }, "Neutral", false);
        }
    }
    
    // Edge cases
    let edge_cases = vec![
        ([255, 255, 255], "Pure white"),
        ([1, 0, 0], "Very dark red"),
        ([254, 254, 254], "Almost white"),
        ([127, 64, 32], "Brown-ish"),
        ([255, 165, 0], "Orange"),
        ([75, 0, 130], "Indigo"),
        ([238, 130, 238], "Violet"),
        ([255, 20, 147], "Deep pink"),
    ];
    
    println!("\n⚡ Edge Cases:");
    for (rgb, desc) in &edge_cases {
        if let Some(result) = test_round_trip_conversion(&forward_converter, &reverse_converter, *rgb, desc) {
            println!("  {:16} RGB{:?} ↔ {} → RGB{:?} (Δ={:.2})", 
                desc, result.original_rgb, result.munsell_notation, result.converted_rgb, result.rgb_delta);
            summary.add_result(&result, "Edge Case", true);
        } else {
            println!("  {:16} RGB{:?} → FAILED", desc, rgb);
            summary.add_result(&RoundTripResult {
                original_rgb: *rgb,
                munsell_notation: "FAILED".to_string(),
                converted_rgb: [0, 0, 0],
                rgb_delta: 999.0,
                max_component_diff: 255,
                description: desc.to_string(),
            }, "Edge Case", false);
        }
    }
    
    summary.finalize();
    summary.print_summary();
    
    Ok(())
}

fn test_reference_dataset_samples() -> Result<(), Box<dyn std::error::Error>> {
    println!("\n📚 Testing Reference Dataset Samples");
    println!("====================================");
    
    // Load a few samples from the reference dataset
    let reference_samples = vec![
        // These are known good conversions from the dataset
        ([255, 0, 0], "7.9R 5.2/20.5"),      // Pure red
        ([0, 255, 0], "1.8G 8.7/20.4"),      // Pure green  
        ([0, 0, 255], "6.8PB 2.7/18.6"),     // Pure blue
        ([255, 255, 0], "2.7Y 9.7/18.4"),    // Yellow
        ([128, 128, 128], "N 5.4"),          // Medium gray
        ([64, 64, 64], "N 2.7"),             // Dark gray
        ([192, 192, 192], "N 7.6"),          // Light gray
    ];
    
    let forward_converter = MunsellConverter::new()?;
    let reverse_converter = PythonMunsellConverter::new();
    let mut summary = TestSummary::default();
    
    for (rgb, expected_munsell) in &reference_samples {
        print!("RGB{:?} → ", rgb);
        
        // Forward conversion
        match forward_converter.srgb_to_munsell(*rgb) {
            Ok(munsell_result) => {
                println!("{} (expected: {})", munsell_result.notation, expected_munsell);
                
                // Test round-trip
                if let Some(result) = test_round_trip_conversion(
                    &forward_converter, 
                    &reverse_converter, 
                    *rgb, 
                    "Reference sample"
                ) {
                    println!("    Round-trip: RGB{:?} (Δ={:.2})", result.converted_rgb, result.rgb_delta);
                    summary.add_result(&result, "Reference", true);
                } else {
                    println!("    Round-trip: FAILED");
                    summary.add_result(&RoundTripResult {
                        original_rgb: *rgb,
                        munsell_notation: expected_munsell.to_string(),
                        converted_rgb: [0, 0, 0],
                        rgb_delta: 999.0,
                        max_component_diff: 255,
                        description: "Reference sample".to_string(),
                    }, "Reference", false);
                }
            }
            Err(e) => {
                println!("CONVERSION ERROR: {}", e);
                summary.add_result(&RoundTripResult {
                    original_rgb: *rgb,
                    munsell_notation: "FAILED".to_string(),
                    converted_rgb: [0, 0, 0],
                    rgb_delta: 999.0,
                    max_component_diff: 255,
                    description: "Reference sample".to_string(),
                }, "Reference", false);
            }
        }
    }
    
    summary.finalize();
    summary.print_summary();
    
    Ok(())
}

fn test_colorformats_pipeline() -> Result<(), Box<dyn std::error::Error>> {
    println!("\n🌈 Testing ColorFormats Pipeline");
    println!("================================");
    
    let reverse_converter = ReverseConverter::new()?;
    let forward_converter = MunsellConverter::new()?;
    let python_converter = PythonMunsellConverter::new();
    
    let munsell_tests = vec![
        "5R 4/14",
        "2.5YR 6/12", 
        "5Y 8/10",
        "7.5GY 5/8",
        "5G 4/6",
        "5B 5/8",
        "5P 4/8",
        "N 5",
        "N 2",
        "N 8",
    ];
    
    let mut pipeline_summary = TestSummary::default();
    
    for munsell_str in &munsell_tests {
        println!("\nTesting: {}", munsell_str);
        
        // Parse Munsell to specification
        let spec = match parse_munsell_notation(munsell_str) {
            Ok(s) => s,
            Err(_) => {
                println!("  ❌ Failed to parse Munsell specification");
                continue;
            }
        };
        
        // Convert through ColorFormats pipeline
        match reverse_converter.munsell_to_all_formats(&spec) {
            Ok(formats) => {
                println!("  ✅ Munsell → ColorFormats conversion successful");
                println!("    sRGB: [{}, {}, {}]", formats.srgb[0], formats.srgb[1], formats.srgb[2]);
                println!("    Hex:  {}", formats.hex);
                println!("    Lab:  L={:.2} a={:.2} b={:.2}", formats.lab.l, formats.lab.a, formats.lab.b);
                println!("    HSL:  H={:.1}° S={:.1}% L={:.1}%", formats.hsl.h, formats.hsl.s, formats.hsl.l);
                println!("    HSV:  H={:.1}° S={:.1}% V={:.1}%", formats.hsv.h, formats.hsv.s, formats.hsv.v);
                
                // Test round-trip through RGB
                if let Some(result) = test_round_trip_conversion(
                    &forward_converter,
                    &python_converter,
                    formats.srgb,
                    "ColorFormats pipeline"
                ) {
                    println!("    Round-trip RGB delta: {:.2}", result.rgb_delta);
                    pipeline_summary.add_result(&result, "ColorFormats", true);
                } else {
                    println!("    ❌ Round-trip failed");
                    pipeline_summary.add_result(&RoundTripResult {
                        original_rgb: formats.srgb,
                        munsell_notation: munsell_str.to_string(),
                        converted_rgb: [0, 0, 0],
                        rgb_delta: 999.0,
                        max_component_diff: 255,
                        description: "ColorFormats pipeline".to_string(),
                    }, "ColorFormats", false);
                }
            }
            Err(e) => {
                println!("  ❌ ColorFormats conversion failed: {}", e);
                pipeline_summary.add_result(&RoundTripResult {
                    original_rgb: [0, 0, 0],
                    munsell_notation: munsell_str.to_string(),
                    converted_rgb: [0, 0, 0],
                    rgb_delta: 999.0,
                    max_component_diff: 255,
                    description: "ColorFormats pipeline".to_string(),
                }, "ColorFormats", false);
            }
        }
    }
    
    pipeline_summary.finalize();
    pipeline_summary.print_summary();
    
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔄 MUNSELL SPACE BIDIRECTIONAL CONSISTENCY TESTS");
    println!("================================================");
    println!("Testing round-trip conversion accuracy: RGB ↔ Munsell");
    println!("Target: RGB delta < 10 for excellent, < 30 for good conversion\n");
    
    let start_time = Instant::now();
    
    // Run all test categories
    test_color_categories()?;
    test_munsell_notation_formats()?;
    test_reference_dataset_samples()?;
    test_colorformats_pipeline()?;
    
    let elapsed = start_time.elapsed();
    
    println!("\n⏱️  Total test time: {:.2}s", elapsed.as_secs_f64());
    println!("\n✅ Bidirectional consistency testing complete!");
    println!("Review the results above to assess conversion quality and identify any issues.");
    
    Ok(())
}