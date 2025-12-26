//! Integration tests for MunsellSpace converter accuracy validation.

use munsellspace::{MunsellConverter, MunsellColor};
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;
use std::sync::Arc;

/// Test converter accuracy against the complete reference dataset.
#[test]
fn test_reference_dataset_accuracy() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Load reference dataset
    let reference_path = Path::new("tests/data/srgb-to-munsell.csv");
    
    if !reference_path.exists() {
        panic!("Reference dataset not found at: {:?}", reference_path);
    }
    
    let file = File::open(reference_path).expect("Failed to open reference dataset");
    let reader = BufReader::new(file);
    
    let mut total_colors = 0;
    let mut exact_matches = 0;
    let mut close_matches = 0;
    let mut failed_conversions = Vec::new();
    
    for (line_num, line) in reader.lines().enumerate() {
        let line = line.expect("Failed to read line");
        
        // Skip header line
        if line_num == 0 && line.starts_with("R,") {
            continue;
        }
        
        let parts: Vec<&str> = line.split(',').collect();
        if parts.len() < 4 {
            continue; // Skip invalid lines
        }
        
        // Parse RGB values
        let r: u8 = parts[0].trim().parse().expect(&format!("Invalid R value at line {}", line_num + 1));
        let g: u8 = parts[1].trim().parse().expect(&format!("Invalid G value at line {}", line_num + 1));
        let b: u8 = parts[2].trim().parse().expect(&format!("Invalid B value at line {}", line_num + 1));
        let expected_munsell = parts[3].trim();
        
        total_colors += 1;
        
        // Test conversion
        match converter.srgb_to_munsell([r, g, b]) {
            Ok(converted) => {
                if converted.notation == expected_munsell {
                    exact_matches += 1;
                } else if is_close_match(&converted.notation, expected_munsell) {
                    close_matches += 1;
                } else {
                    failed_conversions.push(FailedConversion {
                        rgb: [r, g, b],
                        expected: expected_munsell.to_string(),
                        actual: converted.notation,
                        line_number: line_num + 1,
                    });
                }
            }
            Err(e) => {
                failed_conversions.push(FailedConversion {
                    rgb: [r, g, b],
                    expected: expected_munsell.to_string(),
                    actual: format!("ERROR: {}", e),
                    line_number: line_num + 1,
                });
            }
        }
    }
    
    let accuracy_percentage = (exact_matches as f64 / total_colors as f64) * 100.0;
    let close_match_percentage = ((exact_matches + close_matches) as f64 / total_colors as f64) * 100.0;
    
    println!("Reference Dataset Validation Results:");
    println!("Total colors tested: {}", total_colors);
    println!("Exact matches: {} ({:.2}%)", exact_matches, accuracy_percentage);
    println!("Close matches: {} ({:.2}%)", close_matches, close_match_percentage - accuracy_percentage);
    println!("Failed conversions: {}", failed_conversions.len());
    
    // Print first few failures for debugging
    if !failed_conversions.is_empty() {
        println!("\nFirst 10 failed conversions:");
        for failure in failed_conversions.iter().take(10) {
            println!("Line {}: RGB{:?} -> Expected: '{}', Got: '{}'", 
                failure.line_number, failure.rgb, failure.expected, failure.actual);
        }
    }
    
    // Assert minimum accuracy requirements
    assert!(total_colors > 4000, "Expected at least 4000 reference colors, found {}", total_colors);
    assert!(accuracy_percentage >= 95.0, 
        "Accuracy too low: {:.2}% (expected >= 95.0%)", accuracy_percentage);
    
    // For 99.98% accuracy claim, we should have very few failures
    if accuracy_percentage >= 99.5 {
        println!("✅ HIGH ACCURACY: {:.2}% - Meeting production quality standards", accuracy_percentage);
    } else {
        println!("⚠️  MODERATE ACCURACY: {:.2}% - May need algorithm improvements", accuracy_percentage);
    }
}

/// Test that converter can handle edge cases from the reference dataset.
#[test]
fn test_edge_cases() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Test pure colors from the actual reference dataset
    let pure_red = converter.srgb_to_munsell([255, 0, 0]).expect("Failed to convert pure red");
    assert_eq!(pure_red.notation, "7.9R 5.2/20.5");
    assert!(pure_red.is_chromatic());
    assert!(pure_red.hue_family().unwrap().contains("R"));
    
    let pure_green = converter.srgb_to_munsell([0, 255, 0]).expect("Failed to convert pure green");
    assert_eq!(pure_green.notation, "9.9GY 8.8/19.4");
    assert!(pure_green.is_chromatic());
    assert!(pure_green.hue_family().unwrap().contains("GY"));
    
    // Test the only neutral color in the reference dataset
    let black = converter.srgb_to_munsell([0, 0, 0]).expect("Failed to convert black");
    assert_eq!(black.notation, "N 0.0");
    assert!(black.is_neutral());
    assert_eq!(black.value, 0.0);
    
    // Test a known chromatic blue from the reference
    let blue = converter.srgb_to_munsell([0, 68, 119]).expect("Failed to convert blue");
    assert_eq!(blue.notation, "2.9PB 2.8/7.0");
    assert!(blue.is_chromatic());
    assert!(blue.hue_family().unwrap().contains("PB"));
}

/// Test batch conversion performance and consistency.
#[test]
fn test_batch_conversion_consistency() {
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    let test_colors = vec![
        [255, 0, 0],   // Red
        [0, 255, 0],   // Green
        [0, 0, 255],   // Blue
        [255, 255, 0], // Yellow
        [255, 0, 255], // Magenta
        [0, 255, 255], // Cyan
        [128, 128, 128], // Gray
        [0, 0, 0],     // Black
        [255, 255, 255], // White
    ];
    
    // Test individual conversions
    let individual_results: Vec<_> = test_colors.iter()
        .map(|&rgb| converter.srgb_to_munsell(rgb).expect("Individual conversion failed"))
        .collect();
    
    // Test batch conversion
    let batch_results = converter.convert_batch(&test_colors)
        .expect("Batch conversion failed");
    
    // Results should be identical
    assert_eq!(individual_results.len(), batch_results.len());
    for (i, (individual, batch)) in individual_results.iter().zip(batch_results.iter()).enumerate() {
        assert_eq!(individual.notation, batch.notation, 
            "Mismatch at index {}: individual='{}', batch='{}'", 
            i, individual.notation, batch.notation);
    }
}

/// Represents a failed conversion for debugging purposes.
#[derive(Debug)]
struct FailedConversion {
    rgb: [u8; 3],
    expected: String,
    actual: String,
    line_number: usize,
}

/// Check if two Munsell notations are close matches.
/// This is more lenient than exact matching for validation purposes.
fn is_close_match(actual: &str, expected: &str) -> bool {
    // Parse both notations
    let actual_color = match MunsellColor::from_notation(actual) {
        Ok(color) => color,
        Err(_) => return false,
    };
    
    let expected_color = match MunsellColor::from_notation(expected) {
        Ok(color) => color,
        Err(_) => return false,
    };
    
    // For neutral colors
    if actual_color.is_neutral() && expected_color.is_neutral() {
        return (actual_color.value - expected_color.value).abs() < 0.5;
    }
    
    // For chromatic colors
    if actual_color.is_chromatic() && expected_color.is_chromatic() {
        // Check if hue families match
        let hue_match = actual_color.hue_family() == expected_color.hue_family();
        
        // Check if values are close
        let value_match = (actual_color.value - expected_color.value).abs() < 1.0;
        
        // Check if chromas are close
        let chroma_match = match (actual_color.chroma, expected_color.chroma) {
            (Some(c1), Some(c2)) => (c1 - c2).abs() < 2.0,
            _ => false,
        };
        
        return hue_match && value_match && chroma_match;
    }
    
    false
}

/// Comprehensive thread safety test for the entire MunsellSpace library public API.
#[test]
fn test_comprehensive_thread_safety() {
    use std::sync::Arc;
    use std::thread;
    use munsellspace::{IsccNbsClassifier, UnifiedColorCache};
    
    println!("Testing thread safety across all public API components...");
    
    // Create shared instances of all major components
    let converter = Arc::new(MunsellConverter::new().expect("Failed to create converter"));
    let classifier = Arc::new(IsccNbsClassifier::new().expect("Failed to create classifier"));
    let cache = Arc::new(UnifiedColorCache::new());
    
    // Test data covering the full spectrum of colors
    let test_colors = vec![
        // Primary colors
        [255, 0, 0],   // Red
        [0, 255, 0],   // Green  
        [0, 0, 255],   // Blue
        // Secondary colors
        [255, 255, 0], // Yellow
        [255, 0, 255], // Magenta
        [0, 255, 255], // Cyan
        // Grayscale
        [0, 0, 0],     // Black
        [128, 128, 128], // Gray
        [255, 255, 255], // White
        // Complex colors
        [139, 69, 19], // Brown
        [255, 192, 203], // Pink
        [128, 0, 128],   // Purple
        [255, 165, 0],   // Orange
        [0, 128, 0],     // Dark green
        [75, 0, 130],    // Indigo
        [240, 230, 140], // Khaki
    ];
    
    let mut handles = vec![];
    let num_threads = 8;
    let iterations_per_thread = 25;
    
    for thread_id in 0..num_threads {
        let converter_clone = Arc::clone(&converter);
        let classifier_clone = Arc::clone(&classifier);
        let cache_clone = Arc::clone(&cache);
        let test_colors_clone = test_colors.clone();
        
        let handle = thread::spawn(move || {
            let mut results = Vec::new();
            let mut conversion_count = 0;
            let mut classification_count = 0;
            let mut cache_operations = 0;
            
            for iteration in 0..iterations_per_thread {
                for (color_idx, &rgb) in test_colors_clone.iter().enumerate() {
                    // Vary RGB slightly for each thread and iteration to test cache behavior
                    let varied_rgb = [
                        (rgb[0] as i16 + thread_id - 4).clamp(0, 255) as u8,
                        (rgb[1] as i16 + iteration - 12).clamp(0, 255) as u8,
                        (rgb[2] as i16 + color_idx as i16 - 8).clamp(0, 255) as u8,
                    ];
                    
                    // Test MunsellConverter thread safety
                    match converter_clone.srgb_to_munsell(varied_rgb) {
                        Ok(munsell) => {
                            conversion_count += 1;
                            
                            // Test ISCC-NBS classification if color is chromatic
                            if munsell.is_chromatic() {
                                if let (Some(hue), Some(chroma)) = (&munsell.hue, munsell.chroma) {
                                    match classifier_clone.classify_munsell(hue, munsell.value, chroma) {
                                        Ok(Some(metadata)) => {
                                            classification_count += 1;
                                            results.push((
                                                varied_rgb,
                                                munsell.notation.clone(),
                                                metadata.iscc_nbs_color_name.clone(),
                                            ));
                                        }
                                        Ok(None) => {
                                            // Color not in ISCC-NBS range, that's fine
                                            results.push((
                                                varied_rgb,
                                                munsell.notation.clone(),
                                                "unclassified".to_string(),
                                            ));
                                        }
                                        Err(e) => {
                                            panic!("ISCC-NBS classification error in thread {}: {:?}", thread_id, e);
                                        }
                                    }
                                }
                            } else {
                                // Neutral color
                                results.push((
                                    varied_rgb,
                                    munsell.notation.clone(),
                                    "neutral".to_string(),
                                ));
                            }
                            
                            // Test UnifiedColorCache thread safety
                            // Check cache first
                            if cache_clone.get(&varied_rgb).is_some() {
                                cache_operations += 1;
                            }
                            
                            // Insert into cache
                            let cached_result = munsellspace::CachedColorResult {
                                rgb: varied_rgb,
                                munsell: munsell.clone(),
                                iscc_nbs: None, // Simplified for test
                            };
                            cache_clone.insert(varied_rgb, cached_result);
                            cache_operations += 1;
                        }
                        Err(e) => {
                            panic!("Munsell conversion error in thread {}: {:?}", thread_id, e);
                        }
                    }
                }
            }
            
            (thread_id, conversion_count, classification_count, cache_operations, results.len())
        });
        
        handles.push(handle);
    }
    
    // Wait for all threads to complete and collect results
    let mut total_conversions = 0;
    let mut total_classifications = 0;
    let mut total_cache_ops = 0;
    
    for handle in handles {
        let (thread_id, conversions, classifications, cache_ops, result_count) = 
            handle.join().expect(&format!("Thread panicked"));
            
        println!(
            "Thread {}: {} conversions, {} classifications, {} cache ops, {} results",
            thread_id, conversions, classifications, cache_ops, result_count
        );
        
        total_conversions += conversions;
        total_classifications += classifications;
        total_cache_ops += cache_ops;
    }
    
    // Verify expected totals
    let expected_conversions = (num_threads as usize) * (iterations_per_thread as usize) * test_colors.len();
    assert_eq!(total_conversions, expected_conversions,
               "Expected {} total conversions, got {}", expected_conversions, total_conversions);
    
    println!("✅ Thread safety test completed successfully!");
    println!("Total conversions: {}", total_conversions);
    println!("Total classifications: {}", total_classifications);  
    println!("Total cache operations: {}", total_cache_ops);
    println!("Cache size after test: {}", cache.len());
    
    // Verify that cache is still in a valid state
    let cache_stats = cache.stats();
    assert!(cache_stats.current_size <= cache_stats.max_size,
            "Cache size exceeded maximum: {} > {}", cache_stats.current_size, cache_stats.max_size);
}

/// Test that all public types implement Send + Sync for thread safety.
#[test]  
fn test_send_sync_traits_all_public_types() {
    use munsellspace::*;
    
    // Test core converter types
    fn assert_send<T: Send>() {}
    fn assert_sync<T: Sync>() {}
    
    // MunsellConverter should be Send + Sync
    assert_send::<MunsellConverter>();
    assert_sync::<MunsellConverter>();
    assert_send::<Arc<MunsellConverter>>();
    assert_sync::<Arc<MunsellConverter>>();
    
    // ISCC-NBS Classifier should be Send + Sync  
    assert_send::<IsccNbsClassifier>();
    assert_sync::<IsccNbsClassifier>();
    assert_send::<Arc<IsccNbsClassifier>>();
    assert_sync::<Arc<IsccNbsClassifier>>();
    
    // Cache should be Send + Sync
    assert_send::<UnifiedColorCache>();
    assert_sync::<UnifiedColorCache>();
    assert_send::<Arc<UnifiedColorCache>>();
    assert_sync::<Arc<UnifiedColorCache>>();
    
    // Data types should be Send + Sync
    assert_send::<MunsellColor>();
    assert_sync::<MunsellColor>();
    assert_send::<ColorMetadata>();
    assert_sync::<ColorMetadata>();
    assert_send::<CachedColorResult>();
    assert_sync::<CachedColorResult>();
    
    // Error types should be Send + Sync
    assert_send::<MunsellError>();
    assert_sync::<MunsellError>();
    
    println!("✅ All public types implement Send + Sync for thread safety");
}