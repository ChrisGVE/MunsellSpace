use munsellspace::{IsccNbsClassifier, MunsellConverter};

#[test]
fn debug_classification_failures() {
    println!("=== DEBUGGING CLASSIFICATION FAILURES ===");
    
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Test some of the failing colors from the reference dataset
    let failing_colors = vec![
        ("#ea9399", "strong pink"),
        ("#f9ccca", "light pink"),
        ("#dea5a4", "moderate pink"),
        ("#eae3e1", "pinkish white"),
        ("#c1b6b3", "pinkish gray"),
    ];
    
    for (hex, expected) in failing_colors {
        println!("\nDebugging: {} (expected: {})", hex, expected);
        
        // Convert hex to RGB
        let rgb = hex_to_rgb(hex).expect("Invalid hex");
        println!("  RGB: {:?}", rgb);
        
        // Convert to Munsell
        match converter.srgb_to_munsell(rgb) {
            Ok(munsell) => {
                println!("  Munsell: {}", munsell);
                println!("  Hue: {:?}, Value: {:.1}, Chroma: {:?}", munsell.hue, munsell.value, munsell.chroma);
                
                // Try to classify
                if let (Some(hue), Some(chroma)) = (&munsell.hue, munsell.chroma) {
                    match classifier.classify_munsell(hue, munsell.value, chroma) {
                        Ok(Some(result)) => {
                            println!("  ✅ FOUND: {}", result.revised_descriptor());
                        }
                        Ok(None) => {
                            println!("  ❌ NO CLASSIFICATION: Failed to find color in any adjacent plane");
                            // Let's debug the hue plane lookup
                            debug_hue_lookup(&classifier, hue, munsell.value, chroma);
                        }
                        Err(e) => {
                            println!("  ❌ ERROR: {}", e);
                        }
                    }
                } else {
                    println!("  ⚠️  NEUTRAL: No hue/chroma");
                }
            }
            Err(e) => {
                println!("  ❌ MUNSELL CONVERSION FAILED: {}", e);
            }
        }
    }
}

fn debug_hue_lookup(classifier: &IsccNbsClassifier, hue: &str, value: f64, chroma: f64) {
    println!("    Debug: Looking up hue {} {:.1}/{:.1}", hue, value, chroma);
    
    // We can't access private fields directly, so let's try some common plane keys
    let test_planes = vec![
        hue.to_string(),
        format!("{}R", hue.chars().filter(|c| c.is_numeric() || *c == '.').collect::<String>()),
        format!("5R"),
        format!("10R"),
        format!("1YR"),
        format!("5YR"),
        format!("10YR"),
    ];
    
    println!("    Attempting common plane patterns...");
    for plane in &test_planes {
        println!("      Trying plane key: '{}'", plane);
    }
}

fn hex_to_rgb(hex: &str) -> Result<[u8; 3], Box<dyn std::error::Error>> {
    let hex = hex.trim_start_matches('#');
    if hex.len() != 6 {
        return Err("Invalid hex color format".into());
    }
    
    let r = u8::from_str_radix(&hex[0..2], 16)?;
    let g = u8::from_str_radix(&hex[2..4], 16)?;
    let b = u8::from_str_radix(&hex[4..6], 16)?;
    
    Ok([r, g, b])
}

#[test]
fn debug_specific_hue_families() {
    println!("=== DEBUGGING SPECIFIC HUE FAMILIES ===");
    
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    
    // Test some Y and PB family hues that should work
    let test_cases = vec![
        ("7Y", 8.0, 8.0, "Should find Y family"),
        ("2GY", 8.0, 8.0, "Should find GY family"), 
        ("9B", 5.0, 8.0, "Should find B family"),
        ("7PB", 5.0, 8.0, "Should find PB family"),
        ("1Y", 5.0, 6.0, "Y family test"),
        ("1PB", 3.0, 6.0, "PB family test"),
    ];
    
    for (hue, value, chroma, description) in test_cases {
        println!("\nTesting: {} {:.1}/{:.1} ({})", hue, value, chroma, description);
        
        match classifier.classify_munsell(hue, value, chroma) {
            Ok(Some(result)) => {
                println!("  ✅ FOUND: {}", result.revised_descriptor());
            }
            Ok(None) => {
                println!("  ❌ NO CLASSIFICATION found");
            }
            Err(e) => {
                println!("  ❌ ERROR: {}", e);
            }
        }
    }
}