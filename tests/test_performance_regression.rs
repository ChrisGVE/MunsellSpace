//! Performance and regression tests for MunsellSpace converter.
//! 
//! These tests ensure that the converter maintains performance characteristics
//! and doesn't regress in accuracy over time.

use munsellspace::MunsellConverter;
use std::time::{Duration, Instant};

/// Test single color conversion performance
#[test]
fn test_single_conversion_performance() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Test colors covering different performance characteristics
    let test_colors = vec![
        [255, 0, 0],    // Pure red (likely in reference data)
        [128, 64, 192], // Random color (likely requires computation)
        [238, 0, 85],   // Known convergence case
        [0, 0, 0],      // Pure black (edge case)
        [255, 255, 255], // Pure white (edge case)
    ];
    
    let mut total_duration = Duration::new(0, 0);
    let iterations = 1000;
    
    for &rgb in &test_colors {
        let start = Instant::now();
        
        for _ in 0..iterations {
            let _result = converter.srgb_to_munsell(rgb)
                .expect(&format!("Conversion failed for RGB{:?}", rgb));
        }
        
        let duration = start.elapsed();
        total_duration += duration;
        
        let avg_duration = duration / iterations;
        println!("RGB{:?}: {:.2}μs per conversion ({}x)", rgb, 
            avg_duration.as_micros(), iterations);
        
        // Assert single conversion takes less than 1ms
        assert!(avg_duration < Duration::from_millis(1), 
            "Single conversion too slow: {:.2}ms for RGB{:?}", 
            avg_duration.as_secs_f64() * 1000.0, rgb);
    }
    
    let avg_overall = total_duration / (iterations * test_colors.len() as u32);
    println!("Overall average: {:.2}μs per conversion", avg_overall.as_micros());
    
    // Assert overall average is under 500μs
    assert!(avg_overall < Duration::from_micros(500), 
        "Overall average too slow: {:.2}μs", avg_overall.as_micros());
}

/// Test batch processing performance - should achieve 4,000+ colors/second
#[test]
fn test_batch_processing_performance() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Generate test batch of 1000 diverse colors
    let mut test_batch = Vec::new();
    for r in (0..=255).step_by(32) {
        for g in (0..=255).step_by(32) {
            for b in (0..=255).step_by(32) {
                test_batch.push([r as u8, g as u8, b as u8]);
                if test_batch.len() >= 1000 {
                    break;
                }
            }
            if test_batch.len() >= 1000 {
                break;
            }
        }
        if test_batch.len() >= 1000 {
            break;
        }
    }
    
    // Time batch conversion
    let start = Instant::now();
    let results = converter.convert_batch(&test_batch)
        .expect("Batch conversion failed");
    let duration = start.elapsed();
    
    // Verify all conversions succeeded
    assert_eq!(results.len(), test_batch.len());
    
    // Calculate throughput
    let colors_per_second = test_batch.len() as f64 / duration.as_secs_f64();
    println!("Batch processing: {:.0} colors/second ({} colors in {:.2}ms)", 
        colors_per_second, test_batch.len(), duration.as_secs_f64() * 1000.0);
    
    // Assert minimum 4000 colors/second throughput
    assert!(colors_per_second >= 4000.0, 
        "Batch processing too slow: {:.0} colors/second (expected >= 4000)", 
        colors_per_second);
}

/// Test memory usage with large batches
#[test]
fn test_memory_usage_large_batch() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Generate 10,000 color test batch
    let mut large_batch = Vec::new();
    for i in 0..10000 {
        let r = (i % 256) as u8;
        let g = ((i / 256) % 256) as u8;
        let b = ((i / 65536) % 256) as u8;
        large_batch.push([r, g, b]);
    }
    
    // This test mainly ensures we don't crash with large batches
    // and that memory usage stays reasonable
    let start = Instant::now();
    let results = converter.convert_batch(&large_batch)
        .expect("Large batch conversion failed");
    let duration = start.elapsed();
    
    assert_eq!(results.len(), large_batch.len());
    
    let colors_per_second = large_batch.len() as f64 / duration.as_secs_f64();
    println!("Large batch ({}): {:.0} colors/second in {:.2}s", 
        large_batch.len(), colors_per_second, duration.as_secs_f64());
    
    // Should still maintain reasonable throughput even with large batches
    assert!(colors_per_second >= 3000.0, 
        "Large batch processing too slow: {:.0} colors/second", colors_per_second);
}

/// Test converter instance creation performance 
#[test]
fn test_converter_initialization_performance() {
    let iterations = 10;
    let start = Instant::now();
    
    for _ in 0..iterations {
        let _converter = MunsellConverter::new()
            .expect("Failed to create converter");
    }
    
    let duration = start.elapsed();
    let avg_init_time = duration / iterations;
    
    println!("Converter initialization: {:.2}ms average", 
        avg_init_time.as_secs_f64() * 1000.0);
    
    // Initialization should take less than 100ms on average
    assert!(avg_init_time < Duration::from_millis(100), 
        "Converter initialization too slow: {:.2}ms", 
        avg_init_time.as_secs_f64() * 1000.0);
}

/// Test performance regression with reference colors
#[test] 
fn test_reference_colors_performance() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Load first 100 colors from reference dataset for performance testing
    let reference_colors = vec![
        [68, 68, 68],     // N 2.7
        [119, 119, 119],  // N 4.7 
        [170, 170, 170],  // N 6.7
        [255, 0, 0],      // Red
        [0, 255, 0],      // Green
        [0, 0, 255],      // Blue
        [255, 255, 0],    // Yellow
        [255, 0, 255],    // Magenta
        [0, 255, 255],    // Cyan
        [128, 64, 192],   // Purple
        [192, 64, 128],   // Pink
        [64, 192, 128],   // Teal
        [255, 128, 0],    // Orange
        [128, 255, 0],    // Lime
        [0, 128, 255],    // Sky blue
        [255, 0, 128],    // Rose
        [128, 0, 255],    // Violet
        [0, 255, 128],    // Spring green
        [238, 0, 85],     // Convergence test case
        [150, 100, 50],   // Brown
    ];
    
    let iterations = 100;
    let start = Instant::now();
    
    for _ in 0..iterations {
        for &rgb in &reference_colors {
            let _result = converter.srgb_to_munsell(rgb)
                .expect(&format!("Reference color conversion failed for RGB{:?}", rgb));
        }
    }
    
    let duration = start.elapsed();
    let total_conversions = iterations * reference_colors.len();
    let avg_per_conversion = duration / total_conversions as u32;
    let colors_per_second = total_conversions as f64 / duration.as_secs_f64();
    
    println!("Reference colors performance: {:.0} colors/second ({:.2}μs each)", 
        colors_per_second, avg_per_conversion.as_micros());
    
    // Reference colors should be fast (many are direct lookup)
    assert!(colors_per_second >= 5000.0, 
        "Reference color processing too slow: {:.0} colors/second", colors_per_second);
}

/// Test that performance is consistent across multiple runs
#[test]
fn test_performance_stability() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    let test_rgb = [128, 64, 192]; // Standard test color
    let iterations_per_run = 1000;
    let num_runs = 5;
    
    let mut run_times = Vec::new();
    
    for run in 0..num_runs {
        let start = Instant::now();
        
        for _ in 0..iterations_per_run {
            let _result = converter.srgb_to_munsell(test_rgb)
                .expect("Stability test conversion failed");
        }
        
        let duration = start.elapsed();
        let avg_duration = duration / iterations_per_run;
        run_times.push(avg_duration.as_micros());
        
        println!("Run {}: {:.2}μs per conversion", run + 1, avg_duration.as_micros());
    }
    
    // Calculate coefficient of variation to measure stability
    let mean: f64 = run_times.iter().map(|&x| x as f64).sum::<f64>() / num_runs as f64;
    let variance: f64 = run_times.iter()
        .map(|&x| (x as f64 - mean).powi(2))
        .sum::<f64>() / num_runs as f64;
    let std_dev = variance.sqrt();
    let cv = std_dev / mean;
    
    println!("Performance stability: mean={:.2}μs, std={:.2}μs, CV={:.3}", 
        mean, std_dev, cv);
    
    // Coefficient of variation should be less than 20% for stable performance
    assert!(cv < 0.2, "Performance too unstable: CV={:.3} (expected < 0.2)", cv);
}

/// Regression test to ensure accuracy doesn't degrade
#[test]
fn test_accuracy_regression() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Known good results from our reference test set (from TEST_COLORS_REFERENCE.md)
    let regression_test_cases = vec![
        ([255, 0, 0], "7.9R 5.2/20.4", "Pure red"),
        ([255, 128, 0], "3.7YR 6.6/14.7", "Orange"),
        ([0, 255, 0], "9.9GY 8.7/19.4", "Pure green"),
        ([128, 0, 128], "9.3P 2.9/13.8", "Purple (allow 0.1 tolerance)"),
        ([150, 100, 100], "7.4R 4.7/4.0", "Medium red"),
        ([100, 150, 100], "0.3G 5.6/6.2", "Medium green (allow 0.1 chroma)"),
        ([160, 120, 120], "8.4R 5.3/3.1", "Low chroma red"),
        ([120, 140, 160], "8.0B 5.6/2.7", "Low chroma blue"),
        ([100, 50, 50], "8.3R 2.7/4.4", "Dark red (allow 0.1 hue)"),
        ([200, 160, 160], "9.2R 6.9/3.0", "Light red (allow 0.1 diff)"),
    ];
    
    let mut exact_matches = 0;
    let mut close_matches = 0;
    
    for (rgb, expected, description) in &regression_test_cases {
        match converter.srgb_to_munsell(*rgb) {
            Ok(result) => {
                if result.notation == *expected {
                    exact_matches += 1;
                    println!("✓ Exact: {} -> {}", description, result.notation);
                } else if is_close_munsell_match(&result.notation, *expected) {
                    close_matches += 1;
                    println!("≈ Close: {} -> {} (expected {})", 
                        description, result.notation, *expected);
                } else {
                    panic!("Accuracy regression detected for {}: got '{}', expected '{}'", 
                        description, result.notation, *expected);
                }
            }
            Err(e) => {
                panic!("Conversion failed in regression test for {}: {}", description, e);
            }
        }
    }
    
    println!("Regression test results: {} exact, {} close matches", 
        exact_matches, close_matches);
    
    // Should maintain at least 70% exact matches and 90% close matches
    let total = regression_test_cases.len();
    let exact_rate = exact_matches as f64 / total as f64;
    let close_rate = (exact_matches + close_matches) as f64 / total as f64;
    
    assert!(exact_rate >= 0.7, 
        "Exact match regression: {:.1}% (expected >= 70%)", exact_rate * 100.0);
    assert!(close_rate >= 0.9, 
        "Close match regression: {:.1}% (expected >= 90%)", close_rate * 100.0);
}

/// Helper function to determine if two Munsell notations are "close enough"
fn is_close_munsell_match(actual: &str, expected: &str) -> bool {
    // Parse components and check if differences are within acceptable tolerance
    if let (Ok(actual_color), Ok(expected_color)) = (
        parse_munsell_components(actual),
        parse_munsell_components(expected)
    ) {
        match (actual_color, expected_color) {
            ((Some(a_hue), a_val, Some(a_chr)), (Some(e_hue), e_val, Some(e_chr))) => {
                // Chromatic colors: check hue family, value, and chroma differences
                let hue_close = hue_families_match(&a_hue, &e_hue);
                let value_close = (a_val - e_val).abs() <= 0.2;
                let chroma_close = (a_chr - e_chr).abs() <= 0.3;
                
                hue_close && value_close && chroma_close
            }
            ((None, a_val, None), (None, e_val, None)) => {
                // Neutral colors: check value only
                (a_val - e_val).abs() <= 0.2
            }
            _ => false, // Type mismatch (chromatic vs neutral)
        }
    } else {
        false
    }
}

/// Parse Munsell notation into components
fn parse_munsell_components(notation: &str) -> Result<(Option<String>, f64, Option<f64>), ()> {
    if notation.starts_with("N ") {
        // Neutral color
        let value_str = notation.strip_prefix("N ").unwrap().trim_end_matches('/');
        let value = value_str.parse().map_err(|_| ())?;
        Ok((None, value, None))
    } else {
        // Chromatic color
        let parts: Vec<&str> = notation.split_whitespace().collect();
        if parts.len() != 2 {
            return Err(());
        }
        
        let hue = parts[0].to_string();
        let value_chroma = parts[1];
        let value_chroma_parts: Vec<&str> = value_chroma.split('/').collect();
        if value_chroma_parts.len() != 2 {
            return Err(());
        }
        
        let value: f64 = value_chroma_parts[0].parse().map_err(|_| ())?;
        let chroma: f64 = value_chroma_parts[1].parse().map_err(|_| ())?;
        
        Ok((Some(hue), value, Some(chroma)))
    }
}

/// Check if two hue strings represent the same or adjacent hue families
fn hue_families_match(hue1: &str, hue2: &str) -> bool {
    // Extract hue family (R, YR, Y, GY, G, BG, B, PB, P, RP)
    let get_family = |hue: &str| -> String {
        hue.chars().filter(|c| c.is_alphabetic()).collect()
    };
    
    let family1 = get_family(hue1);
    let family2 = get_family(hue2);
    
    family1 == family2
}

/// Test that the converter doesn't leak memory over extended use
#[test]
fn test_memory_stability() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Run many conversions to detect potential memory leaks
    let test_colors = vec![
        [255, 0, 0], [0, 255, 0], [0, 0, 255],
        [128, 128, 128], [64, 64, 64], [192, 192, 192],
    ];
    
    // This is more of a smoke test - we can't easily measure memory in unit tests
    // but we can ensure the converter doesn't crash over extended use
    for iteration in 0..1000 {
        for &rgb in &test_colors {
            let _result = converter.srgb_to_munsell(rgb)
                .expect(&format!("Memory stability test failed at iteration {} for RGB{:?}", 
                    iteration, rgb));
        }
        
        if iteration % 200 == 0 {
            println!("Memory stability: {} iterations completed", iteration + 1);
        }
    }
    
    println!("✓ Memory stability test completed: 6,000 conversions without issues");
}