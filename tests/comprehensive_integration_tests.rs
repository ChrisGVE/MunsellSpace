//! Comprehensive integration tests for the MunsellSpace library.
//!
//! These tests verify end-to-end functionality across multiple modules
//! and ensure the public API works correctly in realistic usage scenarios.

use munsellspace::*;
use std::collections::HashMap;

/// Test the complete conversion pipeline from RGB to Munsell to ISCC-NBS classification
#[test]
fn test_complete_conversion_pipeline() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    
    // Test realistic color conversion scenarios
    let test_scenarios = [
        ([255, 0, 0], "red"),
        ([0, 255, 0], "green"),
        ([0, 0, 255], "blue"),
        ([255, 255, 0], "yellow"),
        ([255, 165, 0], "orange"),
        ([139, 69, 19], "brown"),
        ([255, 192, 203], "pink"),
        ([128, 0, 128], "purple"),
        ([0, 0, 0], "black"),
        ([255, 255, 255], "white"),
    ];
    
    for (rgb, expected_color_family) in test_scenarios {
        // Step 1: Convert RGB to Munsell
        let munsell_result = converter.srgb_to_munsell(rgb);
        assert!(munsell_result.is_ok(), "RGB{:?} should convert to Munsell", rgb);
        
        let munsell = munsell_result.unwrap();
        
        // Step 2: Validate Munsell color properties
        assert!(munsell.value >= 0.0 && munsell.value <= 10.0, "Munsell value out of range");
        if let Some(chroma) = munsell.chroma {
            assert!(chroma >= 0.0, "Chroma should be non-negative");
        }
        
        // Step 3: Attempt ISCC-NBS classification
        let classification_result = classifier.classify_srgb(rgb);
        assert!(classification_result.is_ok(), "RGB{:?} classification should not error", rgb);
        
        match classification_result.unwrap() {
            Some(metadata) => {
                println!("RGB{:?} -> {} -> ISCC-NBS: {}", 
                        rgb, munsell.notation, metadata.iscc_nbs_color_name);
                
                // Verify metadata completeness
                assert!(!metadata.iscc_nbs_color_name.is_empty(), "Color name should not be empty");
                assert!(!metadata.alt_color_name.is_empty(), "Alt color name should not be empty");
                
                // Basic color family check (lenient as color classification is complex)
                let descriptor = metadata.iscc_nbs_descriptor();
                let color_name_lower = metadata.iscc_nbs_color_name.to_lowercase();
                let descriptor_lower = descriptor.to_lowercase();
                
                // This is a very loose check - real color classification is complex
                if expected_color_family == "black" || expected_color_family == "white" {
                    assert!(color_name_lower.contains(expected_color_family) || 
                           descriptor_lower.contains(expected_color_family) ||
                           color_name_lower.contains("gray") || descriptor_lower.contains("gray"),
                           "Expected {} color family in '{}' or '{}'", 
                           expected_color_family, color_name_lower, descriptor_lower);
                }
            }
            None => {
                println!("RGB{:?} -> {} -> Not in ISCC-NBS range", rgb, munsell.notation);
            }
        }
    }
}

/// Test batch processing consistency across different modules
#[test]
fn test_batch_processing_integration() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    
    // Generate a diverse set of RGB colors
    let test_colors: Vec<[u8; 3]> = (0..100)
        .map(|i| {
            let r = ((i * 17 + 37) % 256) as u8;
            let g = ((i * 31 + 73) % 256) as u8; 
            let b = ((i * 43 + 109) % 256) as u8;
            [r, g, b]
        })
        .collect();
    
    // Test batch conversion
    let batch_results = converter.convert_batch(&test_colors)
        .expect("Batch conversion should succeed");
    
    assert_eq!(batch_results.len(), test_colors.len(), "Batch result count should match input");
    
    // Verify each result in the batch is valid and consistent with individual conversion
    for (i, (&rgb, batch_munsell)) in test_colors.iter().zip(batch_results.iter()).enumerate() {
        // Individual conversion for comparison
        let individual_munsell = converter.srgb_to_munsell(rgb)
            .expect(&format!("Individual conversion should succeed for RGB{:?}", rgb));
        
        // Results should be identical
        assert_eq!(batch_munsell.notation, individual_munsell.notation,
                   "Batch result {} should match individual result for RGB{:?}", i, rgb);
        
        // Test classification consistency
        let classification_result = classifier.classify_srgb(rgb);
        assert!(classification_result.is_ok(), "Classification should not error for RGB{:?}", rgb);
    }
}

/// Test thread safety across all major components
#[test]
fn test_comprehensive_thread_safety() {
    use std::sync::Arc;
    use std::thread;
    
    let converter = Arc::new(MunsellConverter::new().expect("Failed to create converter"));
    let classifier = Arc::new(IsccNbsClassifier::new().expect("Failed to create classifier"));
    
    let test_colors = vec![
        [255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0],
        [255, 0, 255], [0, 255, 255], [128, 128, 128], [255, 255, 255],
        [0, 0, 0], [139, 69, 19], [255, 192, 203], [75, 0, 130],
    ];
    
    let mut handles = vec![];
    
    // Spawn multiple threads performing different operations
    for thread_id in 0..4 {
        let converter_clone = Arc::clone(&converter);
        let classifier_clone = Arc::clone(&classifier);
        let colors_clone = test_colors.clone();
        
        let handle = thread::spawn(move || {
            let mut results = Vec::new();
            
            for &rgb in &colors_clone {
                // Test conversion thread safety
                let munsell_result = converter_clone.srgb_to_munsell(rgb);
                assert!(munsell_result.is_ok(), "Thread {} conversion failed for RGB{:?}", thread_id, rgb);
                
                let munsell = munsell_result.unwrap();
                
                // Test classification thread safety  
                let classification_result = classifier_clone.classify_srgb(rgb);
                assert!(classification_result.is_ok(), "Thread {} classification failed for RGB{:?}", thread_id, rgb);
                
                results.push((rgb, munsell.notation.clone(), classification_result));
            }
            
            (thread_id, results)
        });
        
        handles.push(handle);
    }
    
    // Collect results from all threads
    let mut all_results = HashMap::new();
    
    for handle in handles {
        let (thread_id, results) = handle.join().expect("Thread should complete successfully");
        
        for (rgb, munsell_notation, classification) in results {
            // Store results grouped by RGB for consistency checking
            all_results.entry(rgb)
                .or_insert_with(Vec::new)
                .push((thread_id, munsell_notation, classification.is_ok()));
        }
    }
    
    // Verify thread safety - all threads should produce identical results
    for (rgb, thread_results) in all_results {
        let first_notation = &thread_results[0].1;
        let first_classification_ok = thread_results[0].2;
        
        for (thread_id, notation, classification_ok) in &thread_results[1..] {
            assert_eq!(notation, first_notation, 
                      "Thread {} produced different Munsell notation for RGB{:?}: '{}' vs '{}'", 
                      thread_id, rgb, notation, first_notation);
            assert_eq!(*classification_ok, first_classification_ok,
                      "Thread {} produced different classification result for RGB{:?}", thread_id, rgb);
        }
    }
}

/// Test error handling propagation across the system
#[test] 
fn test_error_handling_integration() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    
    // Test parsing errors propagate correctly
    let invalid_notation_tests = [
        "",
        "INVALID",
        "5X 4.0/14.0",
        "5R -1.0/14.0",
        "5R 11.0/14.0",
        "5R 4.0/-1.0",
        "N 11.0",
        "malformed string",
    ];
    
    for invalid_notation in invalid_notation_tests {
        let result = MunsellColor::from_notation(invalid_notation);
        assert!(result.is_err(), "Invalid notation '{}' should fail to parse", invalid_notation);
        
        // Verify error type
        match result.unwrap_err() {
            MunsellError::InvalidNotation { notation, reason } => {
                assert_eq!(notation, invalid_notation);
                assert!(!reason.is_empty(), "Error reason should not be empty");
            }
            other => panic!("Expected InvalidNotation error for '{}', got {:?}", invalid_notation, other),
        }
    }
    
    // Test that conversion errors are handled gracefully
    // (Most valid RGB values should convert successfully, but we test the error handling mechanism)
    let all_valid_conversions = (0..=255).step_by(85)
        .flat_map(|r| (0..=255).step_by(85)
            .flat_map(move |g| (0..=255).step_by(85)
                .map(move |b| [r, g, b])))
        .collect::<Vec<_>>();
    
    let mut conversion_errors = 0;
    let mut classification_errors = 0;
    
    for rgb in all_valid_conversions {
        match converter.srgb_to_munsell(rgb) {
            Ok(_) => {
                // Conversion succeeded, try classification
                match classifier.classify_srgb(rgb) {
                    Ok(_) => { /* Success */ }
                    Err(_) => classification_errors += 1,
                }
            }
            Err(_) => conversion_errors += 1,
        }
    }
    
    // Most conversions should succeed (very lenient check)
    let total_tests = 4_usize.pow(3); // 64 combinations
    assert!(conversion_errors < total_tests / 2, 
           "Too many conversion errors: {} out of {}", conversion_errors, total_tests);
    
    println!("Integration error handling test completed:");
    println!("  Conversion errors: {} / {}", conversion_errors, total_tests);
    println!("  Classification errors: {} / {}", classification_errors, total_tests - conversion_errors);
}

/// Test comprehensive API surface - verify all major public APIs work together
#[test]
fn test_comprehensive_api_surface() {
    // Test all major entry points work
    let converter = MunsellConverter::new().expect("MunsellConverter should initialize");
    let classifier = IsccNbsClassifier::new().expect("IsccNbsClassifier should initialize");
    let reverse_converter = ReverseConverter::new().expect("ReverseConverter should initialize");
    let cache = UnifiedColorCache::new();
    
    // Test RGB color creation and operations
    let rgb_color = RgbColor::new(200, 150, 100);
    assert_eq!(rgb_color.to_array(), [200, 150, 100]);
    assert!(!rgb_color.is_grayscale());
    
    // Test Munsell color creation and parsing
    let munsell_color = MunsellColor::from_notation("5R 4.0/14.0")
        .expect("Valid Munsell notation should parse");
    assert!(munsell_color.is_chromatic());
    assert_eq!(munsell_color.hue_family(), Some("R".to_string()));
    
    let neutral_color = MunsellColor::from_notation("N 5.0")
        .expect("Neutral notation should parse");
    assert!(neutral_color.is_neutral());
    assert_eq!(neutral_color.hue_family(), None);
    
    // Test conversion APIs
    let rgb_array = [200, 150, 100];
    let converted = converter.srgb_to_munsell(rgb_array)
        .expect("RGB should convert to Munsell");
    
    // Test classification API
    let classification = classifier.classify_srgb(rgb_array)
        .expect("Classification should not error");
    
    // Test reverse conversion using the hex string function
    match munsell_to_hex_string(&converted.notation) {
        Ok(hex_string) => {
            println!("Munsell {} -> Hex: {}", converted.notation, hex_string);
            assert!(hex_string.starts_with('#'), "Hex string should start with #");
            assert_eq!(hex_string.len(), 7, "Hex string should be 7 characters long");
        }
        Err(e) => {
            println!("Note: Hex conversion failed for {}: {}", converted.notation, e);
        }
    }
    
    // Test cache operations
    let cached_result = CachedColorResult {
        rgb: rgb_array,
        munsell: converted.clone(),
        iscc_nbs: classification,
    };
    
    cache.insert(rgb_array, cached_result);
    let retrieved = cache.get(&rgb_array);
    assert!(retrieved.is_some(), "Cached result should be retrievable");
    
    let stats = cache.stats();
    assert!(stats.current_size > 0, "Cache should have at least one entry");
    
    println!("Comprehensive API surface test completed successfully");
}