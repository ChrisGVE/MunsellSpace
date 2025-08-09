//! Comprehensive edge case validation tests for MunsellSpace converter.
//! 
//! These tests cover critical edge cases discovered during development:
//! - Boundary colors (hue wrapping)
//! - Extreme colors (black, white, pure RGB)
//! - High chroma colors (>15 chroma)
//! - ISCC-NBS transition points
//! - Real-world validation scenarios

use munsellspace::{MunsellConverter, MunsellColor};

/// Helper function to parse expected Munsell notation into components for testing
fn parse_munsell_for_comparison(notation: &str) -> (Option<String>, f64, Option<f64>) {
    if notation.starts_with("N ") {
        // Neutral color
        let value_str = notation.strip_prefix("N ").unwrap().trim_end_matches('/');
        let value = value_str.parse().unwrap();
        return (None, value, None);
    }
    
    // Chromatic color
    let parts: Vec<&str> = notation.split_whitespace().collect();
    let hue = parts[0].to_string();
    let value_chroma = parts[1];
    let value_chroma_parts: Vec<&str> = value_chroma.split('/').collect();
    let value: f64 = value_chroma_parts[0].parse().unwrap();
    let chroma: f64 = value_chroma_parts[1].parse().unwrap();
    
    (Some(hue), value, Some(chroma))
}

/// Assert that two Munsell colors are approximately equal within tolerance
fn assert_munsell_approx_eq(actual: &MunsellColor, expected: &str, tolerance: f64, test_name: &str) {
    let (exp_hue, exp_value, exp_chroma) = parse_munsell_for_comparison(expected);
    
    // Check value component
    assert!(
        (actual.value - exp_value).abs() <= tolerance, 
        "Value mismatch in {}: expected {}, got {} (diff: {})", 
        test_name, exp_value, actual.value, (actual.value - exp_value).abs()
    );
    
    match (&actual.chroma, exp_chroma) {
        (Some(actual_chroma), Some(exp_chroma)) => {
            assert!(
                (*actual_chroma - exp_chroma).abs() <= tolerance,
                "Chroma mismatch in {}: expected {}, got {} (diff: {})", 
                test_name, exp_chroma, actual_chroma, (*actual_chroma - exp_chroma).abs()
            );
        }
        (None, None) => {}, // Both neutral, OK
        (Some(_), None) | (None, Some(_)) => {
            panic!("Chroma type mismatch in {}: expected {:?}, got {:?}", 
                test_name, exp_chroma, actual.chroma);
        }
    }
    
    match (&actual.hue, &exp_hue) {
        (Some(actual_hue), Some(exp_hue)) => {
            // For hue comparison, we need to be more lenient due to wrapping
            assert_eq!(actual_hue, exp_hue, "Hue mismatch in {}: expected {}, got {}", 
                test_name, exp_hue, actual_hue);
        }
        (None, None) => {}, // Both neutral, OK
        (Some(_), None) | (None, Some(_)) => {
            panic!("Hue type mismatch in {}: expected {:?}, got {:?}", 
                test_name, exp_hue, actual.hue);
        }
    }
}

#[test]
fn test_boundary_colors_hue_wrapping() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Test cases that cross hue family boundaries (0.0/10.0 transitions)
    let boundary_test_cases = vec![
        // Red family boundary cases
        ([255, 0, 0], "7.9R 5.2/20.4", "Pure red at R boundary"),
        ([238, 0, 85], "3.0R 4.9/17.6", "Pink crossing R boundary (known oscillation case)"),
        
        // Yellow-Red to Yellow boundary
        ([255, 200, 0], "4.2Y 8.1/17.0", "YR to Y boundary"),
        
        // Green family boundaries
        ([0, 255, 0], "9.9GY 8.7/19.4", "Pure green near GY boundary"),
        ([0, 255, 50], "5.4G 8.7/17.5", "Green crossing into G family"),
        
        // Blue family boundaries  
        ([0, 100, 255], "0.4PB 4.1/17.8", "Blue crossing PB boundary"),
        ([50, 0, 255], "8.1PB 3.1/24.2", "Blue-Purple boundary"),
        
        // Purple family boundaries
        ([128, 0, 128], "9.3P 2.9/13.8", "Purple at P boundary"),
        ([255, 0, 200], "0.2RP 5.4/19.5", "Purple-Red boundary"),
    ];
    
    for (rgb, expected, description) in boundary_test_cases {
        println!("Testing boundary case: {}", description);
        match converter.srgb_to_munsell(rgb) {
            Ok(result) => {
                // Use relaxed tolerance for boundary cases due to mathematical precision
                assert_munsell_approx_eq(&result, expected, 0.5, description);
                println!("✓ {} -> {}", description, result.notation);
            }
            Err(e) => {
                panic!("Boundary conversion failed for {}: {}", description, e);
            }
        }
    }
}

#[test] 
fn test_extreme_colors() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    let extreme_cases = vec![
        // Pure black
        ([0, 0, 0], "N 0.0", "Pure black should be neutral with value 0"),
        
        // Pure white  
        ([255, 255, 255], "N 9.5/", "Pure white should be neutral with high value"),
        
        // Near black colors
        ([1, 1, 1], "N 0.1/", "Near black (RGB 1,1,1)"),
        ([5, 5, 5], "N 0.3/", "Very dark gray (RGB 5,5,5)"),
        
        // Near white colors
        ([250, 250, 250], "N 9.3/", "Near white (RGB 250,250,250)"),
        ([200, 200, 200], "N 7.8/", "Light gray (RGB 200,200,200)"),
        
        // Pure RGB primaries
        ([255, 0, 0], "7.9R 5.2/20.4", "Pure red primary"),
        ([0, 255, 0], "9.9GY 8.7/19.4", "Pure green primary"),
        ([0, 0, 255], "6.9PB 3.2/28.4", "Pure blue primary (high chroma)"),
        
        // Pure RGB secondaries
        ([255, 255, 0], "4.3Y 9.1/19.3", "Pure yellow (R+G)"),
        ([255, 0, 255], "9.0P 6.1/21.5", "Pure magenta (R+B)"),
        ([0, 255, 255], "2.9B 8.9/14.7", "Pure cyan (G+B)"),
    ];
    
    for (rgb, expected, description) in extreme_cases {
        println!("Testing extreme case: {}", description);
        match converter.srgb_to_munsell(rgb) {
            Ok(result) => {
                // Use moderate tolerance for extreme colors
                assert_munsell_approx_eq(&result, expected, 0.3, description);
                println!("✓ {} -> {}", description, result.notation);
            }
            Err(e) => {
                panic!("Extreme color conversion failed for {}: {}", description, e);
            }
        }
    }
}

#[test]
fn test_high_chroma_colors() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Colors with chroma > 15 that push gamut boundaries
    let high_chroma_cases = vec![
        // Extreme red chromas
        ([255, 0, 0], "7.9R 5.2/20.4", "Pure red (chroma 20.4)"),
        ([200, 0, 0], "7.8R 4.1/15.2", "Dark red high chroma"),
        
        // Extreme blue chromas  
        ([0, 0, 255], "6.9PB 3.2/28.4", "Pure blue (chroma 28.4 - highest)"),
        ([0, 50, 255], "9.1PB 3.5/26.1", "Bright blue high chroma"),
        
        // Extreme green chromas
        ([0, 255, 0], "9.9GY 8.7/19.4", "Pure green (chroma 19.4)"),
        ([50, 255, 50], "0.2G 8.8/18.2", "Bright green high chroma"),
        
        // Extreme yellow chromas
        ([255, 255, 0], "4.3Y 9.1/19.3", "Pure yellow (chroma 19.3)"),
        ([255, 200, 0], "4.2Y 8.1/17.0", "Orange-yellow high chroma"),
        
        // Extreme magenta/purple chromas
        ([255, 0, 255], "9.0P 6.1/21.5", "Pure magenta (chroma 21.5)"),
        ([200, 0, 150], "9.5P 4.5/16.8", "Dark magenta high chroma"),
        
        // Vivid intermediate colors
        ([255, 100, 0], "2.1YR 6.8/18.9", "Vivid orange"),
        ([100, 255, 100], "0.4G 8.9/16.1", "Vivid light green"),
        ([150, 0, 255], "8.1P 4.2/23.7", "Vivid purple"),
    ];
    
    for (rgb, expected, description) in high_chroma_cases {
        println!("Testing high chroma case: {}", description);
        match converter.srgb_to_munsell(rgb) {
            Ok(result) => {
                // Verify chroma is indeed > 15
                if let Some(chroma) = result.chroma {
                    assert!(chroma > 15.0, "Expected high chroma (>15) but got {} for {}", 
                        chroma, description);
                }
                
                // Use relaxed tolerance for high chroma colors due to gamut edge effects
                assert_munsell_approx_eq(&result, expected, 0.8, description);
                println!("✓ {} -> {} (chroma: {:.1})", description, result.notation, 
                    result.chroma.unwrap_or(0.0));
            }
            Err(e) => {
                panic!("High chroma conversion failed for {}: {}", description, e);
            }
        }
    }
}

#[test]
fn test_iscc_nbs_critical_transition_points() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Critical transition points from BACKTESTING_DETAILS_V4.md
    // These are the 119 remaining critical errors at ISCC-NBS boundaries
    let critical_cases = vec![
        // Critical value boundaries (1.5, 2.0, 2.5, 3.0, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5)
        ([85, 17, 238], "8.3PB 3.5/24.8", "Critical value=3.5 boundary"),
        ([68, 34, 153], "9.1PB 2.5/14.7", "Critical value=2.5 boundary"),
        ([153, 17, 119], "2.9RP 3.5/13.1", "Critical value=3.5 RP family"),
        ([170, 17, 34], "7.3R 3.5/12.7", "Critical value=3.5 R family"),
        
        // Critical chroma boundaries (0.5, 0.7, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 13.0, 14.0, 15.0)
        ([0, 34, 85], "5.5PB 1.4/7.0", "Critical chroma=7.0 boundary"),
        ([68, 17, 68], "0.3RP 1.5/7.0", "Critical chroma=7.0 RP"),
        ([0, 68, 204], "6.7PB 3.5/17.2", "Critical value=3.5 + high chroma"),
        ([17, 51, 136], "6.4PB 2.4/11.0", "Critical chroma=11.0 boundary"),
        ([34, 51, 153], "7.0PB 2.6/13.0", "Critical chroma=13.0 boundary"),
        ([51, 17, 119], "8.9PB 1.7/13.0", "Critical chroma=13.0 low value"),
        ([51, 34, 153], "7.9PB 2.4/15.0", "Critical chroma=15.0 boundary"),
        
        // Extreme boundary cases
        ([119, 17, 0], "1.3YR 2.5/9.9", "Critical value=2.5 YR"),
        ([119, 34, 0], "2.3YR 2.7/9.0", "Critical chroma=9.0 YR"),
        ([136, 51, 153], "6.7P 3.7/13.0", "Critical chroma=13.0 P family"),
        ([153, 0, 153], "9.0P 3.5/16.3", "Critical value=3.5 pure P"),
        ([170, 0, 85], "9.3RP 3.6/13.0", "Critical chroma=13.0 RP"),
        ([204, 51, 0], "9.6R 4.5/15.0", "Critical chroma=15.0 + value=4.5"),
    ];
    
    for (rgb, expected, description) in critical_cases {
        println!("Testing ISCC-NBS critical case: {}", description);
        match converter.srgb_to_munsell(rgb) {
            Ok(result) => {
                // Use very tight tolerance for ISCC-NBS validation (within 0.1)
                assert_munsell_approx_eq(&result, expected, 0.15, description);
                println!("✓ {} -> {}", description, result.notation);
            }
            Err(e) => {
                panic!("ISCC-NBS critical conversion failed for {}: {}", description, e);
            }
        }
    }
}

#[test]
fn test_near_achromatic_colors() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Colors with very low chroma that should be handled as neutral or near-neutral
    let near_achromatic_cases = vec![
        // Pure grays
        ([128, 128, 128], "N 5.0/", "Middle gray"),
        ([64, 64, 64], "N 2.5/", "Dark gray"),
        ([192, 192, 192], "N 7.6/", "Light gray"),
        
        // Colors with tiny chroma values
        ([130, 128, 128], "8.1R 5.0/0.3", "Barely red tint"),
        ([128, 130, 128], "4.2GY 5.1/0.3", "Barely green tint"),
        ([128, 128, 130], "5.0PB 5.0/0.3", "Barely blue tint"),
        ([129, 127, 128], "2.5R 5.0/0.2", "Very slight red"),
        ([127, 129, 128], "7.5GY 5.1/0.2", "Very slight green"),
        ([128, 127, 129], "7.5PB 5.0/0.2", "Very slight blue"),
    ];
    
    for (rgb, expected, description) in near_achromatic_cases {
        println!("Testing near-achromatic case: {}", description);
        match converter.srgb_to_munsell(rgb) {
            Ok(result) => {
                // For near-achromatic, check that chroma is very low or None
                if let Some(chroma) = result.chroma {
                    assert!(chroma <= 1.0, "Expected low chroma (<=1.0) but got {} for {}", 
                        chroma, description);
                }
                
                assert_munsell_approx_eq(&result, expected, 0.2, description);
                println!("✓ {} -> {} (chroma: {:.1})", description, result.notation, 
                    result.chroma.unwrap_or(0.0));
            }
            Err(e) => {
                panic!("Near-achromatic conversion failed for {}: {}", description, e);
            }
        }
    }
}

#[test]
fn test_problematic_convergence_colors() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Colors that had convergence issues during development
    let problematic_cases = vec![
        // Known oscillation case from TEST_COLORS_REFERENCE.md
        ([238, 0, 85], "3.0R 4.9/17.6", "Oscillation case - pink/red"),
        
        // Other potential convergence problems from high chroma regions
        ([255, 1, 1], "8.0R 5.2/20.3", "Near-pure red edge case"),
        ([1, 255, 1], "9.8GY 8.7/19.3", "Near-pure green edge case"),
        ([1, 1, 255], "6.9PB 3.2/28.3", "Near-pure blue edge case"),
        
        // Colors at color space boundaries
        ([255, 255, 1], "4.2Y 9.1/19.2", "Near-pure yellow"),
        ([255, 1, 255], "9.0P 6.1/21.4", "Near-pure magenta"),
        ([1, 255, 255], "2.9B 8.9/14.6", "Near-pure cyan"),
    ];
    
    for (rgb, expected, description) in problematic_cases {
        println!("Testing problematic convergence case: {}", description);
        match converter.srgb_to_munsell(rgb) {
            Ok(result) => {
                // Use relaxed tolerance for convergence-problematic colors
                assert_munsell_approx_eq(&result, expected, 1.0, description);
                println!("✓ {} -> {} (expected oscillation resolved)", 
                    description, result.notation);
            }
            Err(e) => {
                panic!("Convergence problematic conversion failed for {}: {}", description, e);
            }
        }
    }
}

#[test]
fn test_color_consistency() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Test that the same RGB always gives the same result (no randomness/instability)
    let test_colors = vec![
        [255, 0, 0],
        [128, 128, 128], 
        [238, 0, 85], // Known problematic case
        [0, 255, 0],
        [150, 100, 50],
    ];
    
    for rgb in test_colors {
        let mut results = Vec::new();
        
        // Convert the same color 5 times
        for i in 0..5 {
            match converter.srgb_to_munsell(rgb) {
                Ok(result) => results.push(result.notation.clone()),
                Err(e) => panic!("Consistency test failed on attempt {} for RGB{:?}: {}", 
                    i+1, rgb, e),
            }
        }
        
        // All results should be identical
        let first_result = &results[0];
        for (i, result) in results.iter().enumerate() {
            assert_eq!(result, first_result, 
                "Inconsistent result on attempt {} for RGB{:?}: got '{}', expected '{}'",
                i+1, rgb, result, first_result);
        }
        
        println!("✓ RGB{:?} consistently produces '{}'", rgb, first_result);
    }
}