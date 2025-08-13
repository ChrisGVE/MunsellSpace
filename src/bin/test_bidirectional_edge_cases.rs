/// Edge case and stress test for bidirectional consistency
/// Focuses on problematic colors, boundary conditions, and error cases

use munsellspace::{MunsellConverter, ReverseConverter};
use munsellspace::python_converter::PythonMunsellConverter;
use munsellspace::reverse_conversion::parse_munsell_notation;
use std::env;

/// Test result for detailed analysis
#[derive(Debug)]
struct DetailedResult {
    original_rgb: [u8; 3],
    munsell_notation: String,
    converted_rgb: [u8; 3],
    rgb_delta: f64,
    success: bool,
    error_message: Option<String>,
}

fn calculate_rgb_delta(rgb1: [u8; 3], rgb2: [u8; 3]) -> f64 {
    let dr = (rgb1[0] as i16 - rgb2[0] as i16).abs() as f64;
    let dg = (rgb1[1] as i16 - rgb2[1] as i16).abs() as f64;
    let db = (rgb1[2] as i16 - rgb2[2] as i16).abs() as f64;
    (dr * dr + dg * dg + db * db).sqrt()
}

fn test_round_trip_detailed(
    forward_converter: &MunsellConverter,
    reverse_converter: &PythonMunsellConverter,
    rgb: [u8; 3],
    test_name: &str,
) -> DetailedResult {
    // Forward: RGB → Munsell
    let munsell = match forward_converter.srgb_to_munsell(rgb) {
        Ok(color) => color,
        Err(e) => return DetailedResult {
            original_rgb: rgb,
            munsell_notation: "FORWARD_FAILED".to_string(),
            converted_rgb: [0, 0, 0],
            rgb_delta: 999.0,
            success: false,
            error_message: Some(format!("Forward conversion failed: {}", e)),
        },
    };
    
    // Reverse: Munsell → RGB
    let rgb_back = match reverse_converter.munsell_to_srgb(&munsell.notation) {
        Ok(color) => [color.r, color.g, color.b],
        Err(e) => return DetailedResult {
            original_rgb: rgb,
            munsell_notation: munsell.notation,
            converted_rgb: [0, 0, 0],
            rgb_delta: 999.0,
            success: false,
            error_message: Some(format!("Reverse conversion failed: {}", e)),
        },
    };
    
    let delta = calculate_rgb_delta(rgb, rgb_back);
    
    DetailedResult {
        original_rgb: rgb,
        munsell_notation: munsell.notation,
        converted_rgb: rgb_back,
        rgb_delta: delta,
        success: true,
        error_message: None,
    }
}

fn test_munsell_notation_edge_cases() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔍 Testing Munsell Notation Edge Cases");
    println!("=====================================");
    
    let reverse_converter = PythonMunsellConverter::new();
    
    let edge_notations = vec![
        // Boundary hues
        ("10R 5/10", "Boundary hue 10R"),
        ("1R 5/10", "Boundary hue 1R"),
        ("10RP 5/10", "Cross-family boundary 10RP"),
        ("1YR 5/10", "Cross-family boundary 1YR"),
        
        // Extreme values
        ("5R 1/2", "Very dark color"),
        ("5R 9/2", "Very light color"),
        ("5R 5/1", "Very low chroma"),
        ("5R 5/20", "Very high chroma (may be out-of-gamut)"),
        
        // Neutral variations
        ("N 1", "Pure black neutral"),
        ("N 9", "Near-white neutral"),
        ("N5", "Compact neutral notation"),
        ("N5/0", "Explicit zero chroma neutral"),
        ("N 5/", "Trailing slash neutral"),
        ("N 5/0.0", "Decimal zero chroma"),
        
        // Decimal precision
        ("2.5YR 6.5/12.5", "High decimal precision"),
        ("7.5B 3.7/8.3", "Mixed decimal values"),
        ("0.5R 4/6", "Sub-1 hue number"),
        ("9.9GY 8.1/15.7", "Near-boundary decimal"),
    ];
    
    let mut successes = 0;
    let mut failures = 0;
    
    for (notation, description) in &edge_notations {
        print!("{:25} ({:30}) → ", notation, description);
        
        match parse_munsell_notation(notation) {
            Ok(_) => {
                match reverse_converter.munsell_to_srgb(notation) {
                    Ok(rgb) => {
                        println!("✅ RGB [{:3}, {:3}, {:3}]", rgb.r, rgb.g, rgb.b);
                        successes += 1;
                    }
                    Err(e) => {
                        println!("❌ Conversion failed: {}", e);
                        failures += 1;
                    }
                }
            }
            Err(e) => {
                println!("❌ Parse failed: {}", e);
                failures += 1;
            }
        }
    }
    
    println!("\nNotation Edge Cases Summary:");
    println!("  ✅ Successful: {}/{} ({:.1}%)", successes, successes + failures, 
             (successes as f64 / (successes + failures) as f64) * 100.0);
    println!("  ❌ Failed: {}", failures);
    
    Ok(())
}

fn test_rgb_boundary_cases() -> Result<(), Box<dyn std::error::Error>> {
    println!("\n🎯 Testing RGB Boundary Cases");
    println!("=============================");
    
    // Disable debug output
    env::set_var("DEBUG_MUNSELL", "0");
    
    let forward_converter = MunsellConverter::new()?;
    let reverse_converter = PythonMunsellConverter::new();
    
    let boundary_colors = vec![
        // Pure component boundaries
        ([0, 0, 0], "Pure black"),
        ([1, 0, 0], "Minimal red"),
        ([0, 1, 0], "Minimal green"),
        ([0, 0, 1], "Minimal blue"),
        ([255, 255, 255], "Pure white"),
        ([254, 255, 255], "Near-white"),
        
        // Single-component colors
        ([128, 0, 0], "Pure red tone"),
        ([0, 128, 0], "Pure green tone"),
        ([0, 0, 128], "Pure blue tone"),
        
        // Adjacent values (test quantization)
        ([127, 127, 127], "Medium gray -1"),
        ([128, 128, 128], "Medium gray exact"),
        ([129, 129, 129], "Medium gray +1"),
        
        // High contrast pairs
        ([255, 0, 0], "Pure red"),
        ([0, 255, 255], "Red complement"),
        ([255, 255, 0], "Yellow"),
        ([128, 0, 128], "Yellow complement"),
        
        // Problematic colors identified from previous tests
        ([255, 255, 0], "Yellow (problematic)"),
        ([0, 0, 255], "Blue (high delta)"),
        ([75, 0, 130], "Indigo (high delta)"),
    ];
    
    let mut excellent_count = 0;
    let mut good_count = 0;
    let mut poor_count = 0;
    let mut failed_count = 0;
    let mut max_delta = 0.0;
    let mut worst_color = [0u8; 3];
    
    for (rgb, description) in &boundary_colors {
        let result = test_round_trip_detailed(&forward_converter, &reverse_converter, *rgb, description);
        
        print!("{:20} RGB{:?} → ", description, rgb);
        
        if result.success {
            println!("{} → RGB{:?} (Δ={:.2})", 
                     result.munsell_notation, result.converted_rgb, result.rgb_delta);
            
            if result.rgb_delta > max_delta {
                max_delta = result.rgb_delta;
                worst_color = *rgb;
            }
            
            if result.rgb_delta < 10.0 {
                excellent_count += 1;
            } else if result.rgb_delta < 30.0 {
                good_count += 1;
            } else {
                poor_count += 1;
            }
        } else {
            println!("FAILED: {}", result.error_message.unwrap_or("Unknown error".to_string()));
            failed_count += 1;
        }
    }
    
    let total_successful = excellent_count + good_count + poor_count;
    let total_tests = total_successful + failed_count;
    
    println!("\nRGB Boundary Cases Summary:");
    println!("  Total tests: {}", total_tests);
    println!("  ✅ Excellent (Δ<10): {} ({:.1}%)", excellent_count, 
             (excellent_count as f64 / total_successful as f64) * 100.0);
    println!("  🟡 Good (10≤Δ<30):   {} ({:.1}%)", good_count,
             (good_count as f64 / total_successful as f64) * 100.0);
    println!("  🔴 Poor (Δ≥30):      {} ({:.1}%)", poor_count,
             (poor_count as f64 / total_successful as f64) * 100.0);
    println!("  ❌ Failed:           {}", failed_count);
    println!("  📊 Max delta: {:.2} (RGB{:?})", max_delta, worst_color);
    
    Ok(())
}

fn test_systematic_gray_scale() -> Result<(), Box<dyn std::error::Error>> {
    println!("\n🔘 Testing Systematic Gray Scale");
    println!("===============================");
    
    env::set_var("DEBUG_MUNSELL", "0");
    
    let forward_converter = MunsellConverter::new()?;
    let reverse_converter = PythonMunsellConverter::new();
    
    // Test systematic grayscale values
    let gray_levels = vec![0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 255];
    
    let mut successful_grays = 0;
    let mut failed_grays = 0;
    let mut total_delta = 0.0;
    let mut max_gray_delta = 0.0;
    
    for level in &gray_levels {
        let rgb = [*level, *level, *level];
        let result = test_round_trip_detailed(&forward_converter, &reverse_converter, rgb, "Gray level");
        
        print!("Gray {:3} → ", level);
        
        if result.success {
            println!("{} → Gray {:3} (Δ={:.2})", 
                     result.munsell_notation, 
                     (result.converted_rgb[0] + result.converted_rgb[1] + result.converted_rgb[2]) / 3,
                     result.rgb_delta);
            
            successful_grays += 1;
            total_delta += result.rgb_delta;
            
            if result.rgb_delta > max_gray_delta {
                max_gray_delta = result.rgb_delta;
            }
        } else {
            println!("FAILED: {}", result.error_message.unwrap_or("Unknown error".to_string()));
            failed_grays += 1;
        }
    }
    
    if successful_grays > 0 {
        let avg_delta = total_delta / successful_grays as f64;
        println!("\nGrayscale Summary:");
        println!("  Successful: {}/{} ({:.1}%)", successful_grays, gray_levels.len(),
                 (successful_grays as f64 / gray_levels.len() as f64) * 100.0);
        println!("  Average delta: {:.2}", avg_delta);
        println!("  Max delta: {:.2}", max_gray_delta);
        
        if successful_grays == 0 || avg_delta > 20.0 {
            println!("  ⚠️  WARNING: Gray scale conversion has significant issues");
        } else if avg_delta < 5.0 {
            println!("  ✅ Gray scale conversion is excellent");
        } else {
            println!("  🟡 Gray scale conversion is acceptable");
        }
    }
    
    Ok(())
}

fn test_color_space_corners() -> Result<(), Box<dyn std::error::Error>> {
    println!("\n🔺 Testing Color Space Corner Cases");
    println!("==================================");
    
    env::set_var("DEBUG_MUNSELL", "0");
    
    let forward_converter = MunsellConverter::new()?;
    let reverse_converter = PythonMunsellConverter::new();
    
    // RGB color space corners and near-corners
    let corner_colors = vec![
        // RGB cube corners
        ([0, 0, 0], "Black corner"),
        ([255, 0, 0], "Red corner"),
        ([0, 255, 0], "Green corner"),
        ([0, 0, 255], "Blue corner"),
        ([255, 255, 0], "Yellow corner"),
        ([255, 0, 255], "Magenta corner"),
        ([0, 255, 255], "Cyan corner"),
        ([255, 255, 255], "White corner"),
        
        // Near-corners (avoiding exact boundaries)
        ([250, 5, 5], "Near-red corner"),
        ([5, 250, 5], "Near-green corner"),
        ([5, 5, 250], "Near-blue corner"),
        ([250, 250, 5], "Near-yellow corner"),
        ([250, 5, 250], "Near-magenta corner"),
        ([5, 250, 250], "Near-cyan corner"),
    ];
    
    let mut corner_results = Vec::new();
    
    for (rgb, description) in &corner_colors {
        let result = test_round_trip_detailed(&forward_converter, &reverse_converter, *rgb, description);
        corner_results.push((description, result));
    }
    
    // Sort by delta (worst first)
    corner_results.sort_by(|a, b| b.1.rgb_delta.partial_cmp(&a.1.rgb_delta).unwrap());
    
    println!("Corner cases ranked by round-trip accuracy (worst first):");
    for (description, result) in &corner_results {
        if result.success {
            let quality = if result.rgb_delta < 10.0 { "✅" } else if result.rgb_delta < 30.0 { "🟡" } else { "🔴" };
            println!("  {} {:20} Δ={:6.2} {:12} → RGB{:?}", 
                     quality, description, result.rgb_delta, 
                     result.munsell_notation, result.converted_rgb);
        } else {
            println!("  ❌ {:20} FAILED: {}", description, 
                     result.error_message.as_ref().unwrap_or(&"Unknown".to_string()));
        }
    }
    
    // Summary statistics
    let successful: Vec<_> = corner_results.iter().filter(|(_, r)| r.success).collect();
    let failed_count = corner_results.len() - successful.len();
    
    if !successful.is_empty() {
        let avg_delta: f64 = successful.iter().map(|(_, r)| r.rgb_delta).sum::<f64>() / successful.len() as f64;
        let max_delta = successful.iter().map(|(_, r)| r.rgb_delta).fold(0.0, f64::max);
        
        println!("\nCorner Cases Summary:");
        println!("  Successful: {}/{} ({:.1}%)", successful.len(), corner_colors.len(),
                 (successful.len() as f64 / corner_colors.len() as f64) * 100.0);
        println!("  Failed: {}", failed_count);
        println!("  Average delta: {:.2}", avg_delta);
        println!("  Worst delta: {:.2}", max_delta);
    }
    
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🧪 MUNSELL SPACE BIDIRECTIONAL EDGE CASE TESTING");
    println!("================================================");
    println!("Comprehensive testing of boundary conditions and problematic scenarios\n");
    
    // Run all edge case test suites
    test_munsell_notation_edge_cases()?;
    test_rgb_boundary_cases()?;
    test_systematic_gray_scale()?;
    test_color_space_corners()?;
    
    println!("\n🏁 FINAL ASSESSMENT");
    println!("==================");
    println!("Edge case testing complete. Key findings:");
    println!("• Neutral color parsing needs attention (multiple format failures)");
    println!("• Some RGB boundaries show high conversion deltas");
    println!("• Color space corners reveal systematic accuracy issues");
    println!("• Grayscale conversion likely problematic based on previous tests");
    println!("\nRecommended next steps:");
    println!("1. Fix neutral Munsell notation parsing (especially 'N 5' format)");
    println!("2. Investigate mathematical conversion calibration for high-delta colors");
    println!("3. Review color space transformation matrices and constants");
    println!("4. Validate against reference implementation for boundary cases");
    
    Ok(())
}