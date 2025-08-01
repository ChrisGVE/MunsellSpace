use munsellspace::{IsccNbsClassifier, MunsellConverter};

#[test]
fn analyze_exact_match_issues() {
    println!("=== EXACT MATCH ANALYSIS ===");
    println!("Investigating why we only have 103/267 (38.58%) exact matches");
    println!("Both datasets should contain lowercase names, so case shouldn't be the issue");
    
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Load the reference dataset
    let csv_content = include_str!("../ISCC_NBS_REFERENCE_DATASET.csv");
    let mut reader = csv::Reader::from_reader(csv_content.as_bytes());
    
    println!("\nSampling first 20 cases to understand exact match vs mismatch patterns...\n");
    
    let mut exact_matches = 0;
    let mut case_issues = 0;
    let mut whitespace_issues = 0;
    let mut word_order_issues = 0;
    let mut descriptor_differences = 0;
    let mut other_issues = 0;
    let mut total_processed = 0;
    
    for (i, result) in reader.records().enumerate() {
        if i >= 20 { break; } // Sample first 20 cases
        
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
            Ok(Some(result)) => {
                let actual_descriptor = result.revised_descriptor();
                
                println!("=== CASE {} ===", i + 1);
                println!("Hex: {}", hex);
                println!("Expected: \"{}\"", expected_descriptor);
                println!("Actual:   \"{}\"", actual_descriptor);
                
                // Check for exact match
                if expected_descriptor == actual_descriptor {
                    println!("✅ EXACT MATCH");
                    exact_matches += 1;
                } else {
                    println!("❌ MISMATCH - Analyzing...");
                    
                    // Analyze the type of mismatch
                    let mismatch_type = analyze_mismatch_type(expected_descriptor, actual_descriptor);
                    println!("   Type: {}", mismatch_type);
                    
                    match mismatch_type.as_str() {
                        "case_difference" => case_issues += 1,
                        "whitespace_difference" => whitespace_issues += 1,
                        "word_order_difference" => word_order_issues += 1,
                        "descriptor_difference" => descriptor_differences += 1,
                        _ => other_issues += 1,
                    }
                }
                
                total_processed += 1;
            }
            Ok(None) => {
                println!("=== CASE {} ===", i + 1);
                println!("Hex: {}", hex);
                println!("Expected: \"{}\"", expected_descriptor);
                println!("❌ NO CLASSIFICATION");
                total_processed += 1;
            }
            Err(e) => {
                println!("❌ Classification error for {}: {}", hex, e);
            }
        }
        
        println!();
    }
    
    println!("=== SAMPLE ANALYSIS RESULTS (First 20 cases) ===");
    println!("Total processed: {}", total_processed);
    println!("Exact matches: {} ({:.1}%)", exact_matches, (exact_matches as f64 / total_processed as f64) * 100.0);
    println!("Case issues: {}", case_issues);
    println!("Whitespace issues: {}", whitespace_issues);
    println!("Word order issues: {}", word_order_issues);
    println!("Descriptor differences: {}", descriptor_differences);
    println!("Other issues: {}", other_issues);
    
    // Now let's do a broader statistical analysis
    println!("\n=== FULL DATASET STATISTICAL ANALYSIS ===");
    analyze_full_dataset_statistics(&classifier, &converter);
}

fn analyze_mismatch_type(expected: &str, actual: &str) -> String {
    // Check for case differences
    if expected.to_lowercase() == actual.to_lowercase() {
        return "case_difference".to_string();
    }
    
    // Check for whitespace differences
    let expected_normalized = expected.split_whitespace().collect::<Vec<_>>().join(" ");
    let actual_normalized = actual.split_whitespace().collect::<Vec<_>>().join(" ");
    if expected_normalized == actual_normalized {
        return "whitespace_difference".to_string();
    }
    
    // Check for word order differences
    let mut expected_words: Vec<&str> = expected.split_whitespace().collect();
    let mut actual_words: Vec<&str> = actual.split_whitespace().collect();
    expected_words.sort();
    actual_words.sort();
    if expected_words == actual_words {
        return "word_order_difference".to_string();
    }
    
    // Check if it's a descriptor vs modifier issue
    if expected.len() != actual.len() || expected.split_whitespace().count() != actual.split_whitespace().count() {
        return "descriptor_difference".to_string();
    }
    
    "other_difference".to_string()
}

fn analyze_full_dataset_statistics(classifier: &IsccNbsClassifier, converter: &MunsellConverter) {
    let csv_content = include_str!("../ISCC_NBS_REFERENCE_DATASET.csv");
    let mut reader = csv::Reader::from_reader(csv_content.as_bytes());
    
    let mut exact_matches = 0;
    let mut case_mismatches = 0;
    let mut whitespace_mismatches = 0;
    let mut word_count_differences = 0;
    let mut no_classifications = 0;
    let mut total_processed = 0;
    
    for result in reader.records() {
        let record = result.expect("Failed to read CSV record");
        
        let hex = record.get(0).expect("Missing hex").trim();
        let expected_descriptor = record.get(1).expect("Missing descriptor").trim();
        
        let rgb = match hex_to_rgb(hex) {
            Ok(rgb) => rgb,
            Err(_) => continue,
        };
        
        let munsell = match converter.srgb_to_munsell(rgb) {
            Ok(munsell) => munsell,
            Err(_) => continue,
        };
        
        match classifier.classify_munsell_color(&munsell) {
            Ok(Some(result)) => {
                let actual_descriptor = result.revised_descriptor();
                
                if expected_descriptor == actual_descriptor {
                    exact_matches += 1;
                } else if expected_descriptor.to_lowercase() == actual_descriptor.to_lowercase() {
                    case_mismatches += 1;
                } else if expected_descriptor.split_whitespace().collect::<Vec<_>>().join(" ") == 
                         actual_descriptor.split_whitespace().collect::<Vec<_>>().join(" ") {
                    whitespace_mismatches += 1;
                } else if expected_descriptor.split_whitespace().count() != actual_descriptor.split_whitespace().count() {
                    word_count_differences += 1;
                }
                
                total_processed += 1;
            }
            Ok(None) => {
                no_classifications += 1;
                total_processed += 1;
            }
            Err(_) => {}
        }
    }
    
    println!("Total colors: {}", total_processed);
    println!("Exact matches: {} ({:.1}%)", exact_matches, (exact_matches as f64 / total_processed as f64) * 100.0);
    println!("Case-only differences: {} ({:.1}%)", case_mismatches, (case_mismatches as f64 / total_processed as f64) * 100.0);
    println!("Whitespace-only differences: {} ({:.1}%)", whitespace_mismatches, (whitespace_mismatches as f64 / total_processed as f64) * 100.0);
    println!("Word count differences: {} ({:.1}%)", word_count_differences, (word_count_differences as f64 / total_processed as f64) * 100.0);
    println!("No classifications: {} ({:.1}%)", no_classifications, (no_classifications as f64 / total_processed as f64) * 100.0);
    
    let potential_easy_fixes = case_mismatches + whitespace_mismatches;
    let theoretical_max_matches = exact_matches + potential_easy_fixes;
    
    println!("\n=== IMPROVEMENT POTENTIAL ===");
    println!("Current exact matches: {:.1}%", (exact_matches as f64 / total_processed as f64) * 100.0);
    println!("Potential with case/whitespace fixes: {:.1}%", (theoretical_max_matches as f64 / total_processed as f64) * 100.0);
    println!("Main remaining issue: Word count/descriptor differences ({:.1}%)", (word_count_differences as f64 / total_processed as f64) * 100.0);
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