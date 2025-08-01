use munsellspace::{IsccNbsClassifier, MunsellConverter};

#[test]
fn analyze_descriptor_mismatch_patterns() {
    println!("=== DESCRIPTOR MISMATCH PATTERN ANALYSIS ===");
    
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Focus on specific mismatch patterns identified in the reference test
    let test_cases = vec![
        // Word count differences (2 vs 3 words)
        ("#f9ccca", "light pink", "light yellowish pink"),
        ("#dea5a4", "moderate pink", "moderate yellowish pink"), 
        ("#c08081", "dark pink", "dark yellowish pink"),
        ("#722f37", "dark red", "dark purplish red"),
        
        // Family assignment differences  
        ("#eae3e1", "pinkish white", "yellowish white"),
        ("#c1b6b3", "pinkish gray", "yellowish gray"),
        
        // Descriptor construction differences
        ("#ffb5ba", "vivid pink", "light pink"),
        ("#c4aead", "grayish pink", "brownish pink"),
        
        // Very vs dark differences
        ("#5c0923", "very deep red", "very dark purplish red"),
        ("#3f1728", "very dark red", "very dark reddish purple"),
    ];
    
    println!("\nAnalyzing {} mismatch patterns...\n", test_cases.len());
    
    for (i, (hex, expected, actual_prev)) in test_cases.iter().enumerate() {
        println!("=== CASE {} ===", i + 1);
        println!("Hex: {}", hex);
        println!("Expected: \"{}\"", expected);
        println!("Previous:  \"{}\"", actual_prev);
        
        // Parse hex to RGB
        let rgb = hex_to_rgb(hex).expect("Failed to parse hex");
        println!("RGB: {:?}", rgb);
        
        // Convert to Munsell
        match converter.srgb_to_munsell(rgb) {
            Ok(munsell) => {
                println!("Munsell: {}", munsell);
                
                // Get current classification
                match classifier.classify_munsell_color(&munsell) {
                    Ok(Some(result)) => {
                        println!("Current:   \"{}\"", result.revised_descriptor());
                        
                        // Analyze the difference pattern
                        analyze_difference_pattern(expected, &result.revised_descriptor());
                        
                        // Show detailed components
                        println!("  Components:");
                        println!("    ISCC-NBS Descriptor: \"{}\"", result.iscc_nbs_descriptor());
                        println!("    ISCC-NBS Color: \"{}\"", result.iscc_nbs_color()); 
                        println!("    ISCC-NBS Modifier: {:?}", result.iscc_nbs_modifier());
                        println!("    Revised Color: \"{}\"", result.revised_color());
                        println!("    Shade: \"{}\"", result.shade());
                        println!("    Color ID: {}", result.iscc_nbs_color_id());
                    }
                    Ok(None) => println!("Current:   NO CLASSIFICATION"),
                    Err(e) => println!("Current:   ERROR: {}", e),
                }
            }
            Err(e) => println!("Munsell conversion error: {}", e),
        }
        
        println!();
    }
    
    println!("=== SUMMARY ===");
    println!("Analysis complete. Look for patterns in:");
    println!("1. Word count differences (modifier inclusion)");
    println!("2. Family assignment logic (hue boundaries)");
    println!("3. Descriptor vs modifier construction");
    println!("4. Very vs dark descriptor selection");
}

fn analyze_difference_pattern(expected: &str, actual: &str) {
    let expected_words: Vec<&str> = expected.split_whitespace().collect();
    let actual_words: Vec<&str> = actual.split_whitespace().collect();
    
    println!("  Pattern Analysis:");
    println!("    Expected words: {} {:?}", expected_words.len(), expected_words);
    println!("    Actual words:   {} {:?}", actual_words.len(), actual_words);
    
    if expected_words.len() != actual_words.len() {
        println!("    ⚠️  WORD COUNT DIFFERENCE: {} vs {}", expected_words.len(), actual_words.len());
    }
    
    // Find word differences
    let mut different_positions = Vec::new();
    let max_len = expected_words.len().max(actual_words.len());
    
    for i in 0..max_len {
        let exp_word = expected_words.get(i).unwrap_or(&"<missing>");
        let act_word = actual_words.get(i).unwrap_or(&"<missing>");
        
        if exp_word != act_word {
            different_positions.push((i, exp_word, act_word));
        }
    }
    
    if !different_positions.is_empty() {
        println!("    🔍 WORD DIFFERENCES:");
        for (pos, exp, act) in different_positions {
            println!("      Position {}: \"{}\" vs \"{}\"", pos, exp, act);
        }
    }
    
    // Check for specific patterns
    if expected.contains("pink") && actual.contains("yellowish") {
        println!("    🎯 PINK vs YELLOWISH pattern detected");
    }
    
    if expected.contains("very") && actual.contains("dark") {
        println!("    🎯 VERY vs DARK pattern detected"); 
    }
    
    if expected_words.len() < actual_words.len() && actual.contains("ish") {
        println!("    🎯 MODIFIER OVER-INCLUSION pattern detected");
    }
}

fn hex_to_rgb(hex: &str) -> Result<[u8; 3], Box<dyn std::error::Error>> {
    let hex = hex.trim_start_matches('#');
    if hex.len() != 6 {
        return Err("Invalid hex length".into());
    }
    
    let r = u8::from_str_radix(&hex[0..2], 16)?;
    let g = u8::from_str_radix(&hex[2..4], 16)?;
    let b = u8::from_str_radix(&hex[4..6], 16)?;
    
    Ok([r, g, b])
}