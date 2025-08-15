//! Integration test for embedded ISCC-NBS constants

use munsellspace::ISCC_NBS_Classifier;

#[test]
fn test_embedded_iscc_constants_integration() {
    // Create classifier using embedded data (no file I/O)
    let classifier = ISCC_NBS_Classifier::new()
        .expect("Should be able to create ISCC-NBS classifier with embedded data");
    
    // Test Munsell color classification
    let result = classifier.classify_munsell("5R", 4.0, 14.0)
        .expect("Should be able to classify Munsell color");
    
    assert!(result.is_some(), "Should find a classification for vivid red");
    
    let metadata = result.unwrap();
    let descriptor = metadata.iscc_nbs_descriptor();
    
    // Should get some kind of red descriptor
    assert!(descriptor.to_lowercase().contains("red"), 
        "Expected red color, got: {}", descriptor);
    
    // Test neutral color
    let neutral_result = classifier.classify_munsell("N", 5.0, 0.0)
        .expect("Should be able to classify neutral color");
    
    // Neutral colors may or may not have matches depending on the system
    if let Some(neutral_metadata) = neutral_result {
        let neutral_descriptor = neutral_metadata.iscc_nbs_descriptor();
        assert!(neutral_descriptor.to_lowercase().contains("gray") || 
                neutral_descriptor.to_lowercase().contains("grey"),
            "Expected gray color, got: {}", neutral_descriptor);
    }
}

#[test] 
fn test_embedded_rgb_classification() {
    let classifier = ISCC_NBS_Classifier::new()
        .expect("Should be able to create ISCC-NBS classifier with embedded data");
    
    // Test RGB red
    let rgb_result = classifier.classify_srgb([255, 0, 0])
        .expect("Should be able to classify sRGB color");
    
    if let Some(metadata) = rgb_result {
        let descriptor = metadata.iscc_nbs_descriptor();
        // Should get some kind of red
        println!("RGB red classified as: {}", descriptor);
        // We don't assert specific descriptor since RGB->Munsell->ISCC-NBS is complex
    }
}

#[test]
fn test_embedded_hex_classification() {
    let classifier = ISCC_NBS_Classifier::new()
        .expect("Should be able to create ISCC-NBS classifier with embedded data");
    
    // Test hex colors
    let test_cases = ["#FF0000", "#00FF00", "#0000FF", "#808080"];
    
    for hex in &test_cases {
        let hex_result = classifier.classify_hex(hex);
        assert!(hex_result.is_ok(), "Should be able to parse hex color: {}", hex);
        
        if let Ok(Some(metadata)) = hex_result {
            let descriptor = metadata.iscc_nbs_descriptor();
            println!("Hex {} classified as: {}", hex, descriptor);
            // Descriptor should be non-empty
            assert!(!descriptor.trim().is_empty(), "Descriptor should not be empty");
        }
    }
}

#[test]
fn test_embedded_constants_have_all_colors() {
    use munsellspace::constants::get_all_color_numbers;
    
    let color_numbers = get_all_color_numbers();
    
    // Should have all 267 ISCC-NBS colors
    assert_eq!(color_numbers.len(), 267, "Should have all 267 ISCC-NBS colors embedded");
    
    // Should include colors 1 through 267
    for i in 1..=267u16 {
        assert!(color_numbers.contains(&i), "Missing color number: {}", i);
    }
}

#[test]
fn test_embedded_constants_lookup() {
    use munsellspace::constants::get_color_by_number;
    
    // Test specific known colors
    let pink = get_color_by_number(1).expect("Should find color 1 (vivid pink)");
    assert_eq!(pink.iscc_nbs_color_name, "pink");
    assert_eq!(pink.iscc_nbs_formatter, Some("vivid {0}"));
    
    let white = get_color_by_number(263).expect("Should find color 263 (white)");
    assert_eq!(white.iscc_nbs_color_name, "white");
    assert_eq!(white.iscc_nbs_formatter, Some("{0}"));
    
    let black = get_color_by_number(267).expect("Should find color 267 (black)");
    assert_eq!(black.iscc_nbs_color_name, "black");
    assert_eq!(black.iscc_nbs_formatter, Some("{0}"));
    
    // Test non-existent color
    assert!(get_color_by_number(999).is_none(), "Should not find non-existent color");
}