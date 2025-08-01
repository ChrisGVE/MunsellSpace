use munsellspace::{IsccNbsClassifier, MunsellConverter};

#[test]
fn analyze_no_classification_cases() {
    println!("=== NO-CLASSIFICATION ANALYSIS ===");
    println!("Investigating the remaining 13 no-classification cases to understand why they fail");
    
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Load the reference dataset to find no-classification cases
    let csv_content = include_str!("../ISCC_NBS_REFERENCE_DATASET.csv");
    let mut reader = csv::Reader::from_reader(csv_content.as_bytes());
    
    println!("\nProcessing reference dataset to find no-classification cases...\n");
    
    let mut no_classification_cases = Vec::new();
    let mut total_processed = 0;
    
    for (i, result) in reader.records().enumerate() {
        let record = result.expect("Failed to read CSV record");
        
        let hex = record.get(0).expect("Missing hex").trim();
        let expected_descriptor = record.get(1).expect("Missing descriptor").trim();
        
        // Parse hex to RGB
        let rgb = match hex_to_rgb(hex) {
            Ok(rgb) => rgb,
            Err(e) => {
                println!("❌ Failed to parse hex {}: {}", hex, e);
                continue;
            }
        };
        
        // Convert to Munsell
        let munsell = match converter.srgb_to_munsell(rgb) {
            Ok(munsell) => munsell,
            Err(e) => {
                println!("❌ Munsell conversion failed for {}: {}", hex, e);
                continue;
            }
        };
        
        // Try ISCC classification
        match classifier.classify_munsell_color(&munsell) {
            Ok(Some(_result)) => {
                // Has classification - skip
            }
            Ok(None) => {
                // No classification found!
                no_classification_cases.push((hex.to_string(), expected_descriptor.to_string(), munsell.to_string(), rgb));
                println!("🔍 NO CLASSIFICATION #{}: {} → Expected: \"{}\" (Munsell: {}, RGB: {:?})", 
                    no_classification_cases.len(), hex, expected_descriptor, munsell, rgb);
            }
            Err(e) => {
                println!("❌ Classification error for {}: {}", hex, e);
            }
        }
        
        total_processed += 1;
        if total_processed % 50 == 0 {
            println!("  Processed {}/267 colors...", total_processed);
        }
    }
    
    println!("\n=== NO-CLASSIFICATION ANALYSIS RESULTS ===");
    println!("Total no-classification cases found: {}", no_classification_cases.len());
    
    if no_classification_cases.is_empty() {
        println!("✅ All colors now have classifications! This suggests the issue may be in test counting.");
        return;
    }
    
    println!("\n=== DETAILED ANALYSIS OF NO-CLASSIFICATION CASES ===");
    
    for (i, (hex, expected, munsell_str, rgb)) in no_classification_cases.iter().enumerate() {
        println!("\n--- CASE {} ---", i + 1);
        println!("Hex: {}", hex);
        println!("Expected: \"{}\"", expected);
        println!("Munsell: {}", munsell_str);
        println!("RGB: {:?}", rgb);
        
        // Re-convert to get the MunsellColor object for analysis
        let munsell = match converter.srgb_to_munsell(*rgb) {
            Ok(m) => m,
            Err(_) => continue,
        };
        
        if let (Some(hue), Some(chroma)) = (&munsell.hue, munsell.chroma) {
            println!("  Parsed components: Hue: {}, Value: {}, Chroma: {}", hue, munsell.value, chroma);
            
            // Try direct classification with components
            match classifier.classify_munsell(hue, munsell.value, chroma) {
                Ok(Some(result)) => {
                    println!("  ✅ DIRECT CLASSIFICATION WORKS: \"{}\"", result.revised_descriptor());
                    println!("     This suggests a parsing issue in classify_munsell_color()!");
                }
                Ok(None) => {
                    println!("  ❌ DIRECT CLASSIFICATION ALSO FAILS");
                    
                    // Analyze why this specific point fails
                    analyze_classification_failure(hue, munsell.value, chroma, expected);
                }
                Err(e) => {
                    println!("  ❌ DIRECT CLASSIFICATION ERROR: {}", e);
                }
            }
        } else {
            println!("  ⚠️  NEUTRAL COLOR (no hue/chroma) - expected for grays/blacks/whites");
            analyze_neutral_color_handling(expected);
        }
    }
    
    println!("\n=== RECOMMENDATIONS ===");
    if no_classification_cases.len() > 0 {
        println!("1. Check if neutral colors (grays, blacks, whites) need special handling");
        println!("2. Verify that all polygon boundaries include expected points");
        println!("3. Check for edge cases in value/chroma ranges");
        println!("4. Investigate potential gaps in polygon coverage");
    }
}

fn analyze_classification_failure(hue: &str, value: f64, chroma: f64, expected: &str) {
    println!("    Analyzing why {}/{:.1}/{:.1} fails to classify...", hue, value, chroma);
    
    // Check if this is an extreme value/chroma case
    if value < 1.0 || value > 9.0 {
        println!("    🎯 EXTREME VALUE: {:.1} (outside typical 1-9 range)", value);
    }
    
    if chroma > 15.0 {
        println!("    🎯 EXTREME CHROMA: {:.1} (outside typical 0-15 range)", chroma);
    }
    
    if chroma < 0.5 {
        println!("    🎯 VERY LOW CHROMA: {:.1} (near-neutral)", chroma);
    }
    
    // Check expected descriptor patterns
    if expected.contains("black") || expected.contains("white") {
        println!("    🎯 ACHROMATIC COLOR: Expected \"{}\" suggests neutral handling needed", expected);
    }
    
    if expected.contains("deep") && value < 3.0 {
        println!("    🎯 VERY DARK COLOR: Deep colors with low value may be edge cases");
    }
}

fn analyze_neutral_color_handling(expected: &str) {
    println!("    Analyzing neutral color handling for expected: \"{}\"", expected);
    
    if expected.contains("black") {
        println!("    🎯 BLACK HANDLING: System may need special logic for blacks");
    } else if expected.contains("white") {
        println!("    🎯 WHITE HANDLING: System may need special logic for whites");
    } else if expected.contains("gray") {
        println!("    🎯 GRAY HANDLING: System may need special logic for grays");
    } else {
        println!("    ⚠️  UNEXPECTED NEUTRAL: Expected descriptor doesn't match typical neutral patterns");
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