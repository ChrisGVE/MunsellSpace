use munsellspace::{IsccNbsClassifier, MunsellConverter};

#[test]
fn test_correct_field_comparison() {
    println!("=== CORRECT FIELD COMPARISON ANALYSIS ===");
    println!("Comparing 'ISCC-NBS Name' from REFERENCE_DATASET vs 'iscc-nbs-descriptor' from ISCC-NBS-Definitions");
    println!("With proper string trimming from CSV");
    
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Load the reference dataset
    let csv_content = include_str!("../ISCC_NBS_REFERENCE_DATASET.csv");
    let mut reader = csv::Reader::from_reader(csv_content.as_bytes());
    
    println!("\n=== CORRECTED ANALYSIS (First 10 cases) ===");
    
    let mut exact_matches = 0;
    let mut total_processed = 0;
    let mut mismatches = Vec::new();
    
    for (i, result) in reader.records().enumerate() {
        if i >= 10 { break; } // First 10 cases for detailed analysis
        
        let record = result.expect("Failed to read CSV record");
        
        // PROPER CSV STRING TRIMMING
        let hex = record.get(0).expect("Missing hex").trim();
        let reference_iscc_nbs_name = record.get(1).expect("Missing ISCC-NBS Name").trim();
        let reference_modifier = record.get(2).map(|s| s.trim()).unwrap_or("");
        let reference_color = record.get(3).map(|s| s.trim()).unwrap_or("");
        
        println!("\n--- CASE {} ---", i + 1);
        println!("Hex: {}", hex);
        println!("Reference ISCC-NBS Name: \"{}\"", reference_iscc_nbs_name);
        println!("Reference modifier: \"{}\"", reference_modifier);
        println!("Reference color: \"{}\"", reference_color);
        
        // Convert to RGB and then Munsell
        let rgb = match hex_to_rgb(hex) {
            Ok(rgb) => rgb,
            Err(e) => {
                println!("❌ Failed to parse hex: {}", e);
                continue;
            }
        };
        
        let munsell = match converter.srgb_to_munsell(rgb) {
            Ok(munsell) => munsell,
            Err(e) => {
                println!("❌ Munsell conversion failed: {}", e);
                continue;
            }
        };
        
        // Classify with ISCC-NBS system
        match classifier.classify_munsell_color(&munsell) {
            Ok(Some(result)) => {
                // CORRECT COMPARISON: ISCC-NBS Name vs iscc-nbs-descriptor
                let system_iscc_nbs_descriptor = result.iscc_nbs_descriptor().trim();
                
                println!("System iscc-nbs-descriptor: \"{}\"", system_iscc_nbs_descriptor);
                
                // The CORRECT comparison
                if reference_iscc_nbs_name == system_iscc_nbs_descriptor {
                    println!("✅ EXACT MATCH!");
                    exact_matches += 1;
                } else {
                    println!("❌ MISMATCH");
                    mismatches.push((hex.to_string(), reference_iscc_nbs_name.to_string(), system_iscc_nbs_descriptor.to_string()));
                    
                    // Additional debug info
                    println!("   All system fields for comparison:");
                    println!("     iscc_nbs_descriptor: \"{}\"", result.iscc_nbs_descriptor());
                    println!("     iscc_nbs_color: \"{}\"", result.iscc_nbs_color());
                    println!("     iscc_nbs_modifier: {:?}", result.iscc_nbs_modifier());
                    println!("     revised_color: \"{}\"", result.revised_color());
                    println!("     revised_descriptor: \"{}\"", result.revised_descriptor());
                }
                
                total_processed += 1;
            }
            Ok(None) => {
                println!("❌ NO CLASSIFICATION");
                total_processed += 1;
            }
            Err(e) => {
                println!("❌ Classification error: {}", e);
            }
        }
    }
    
    println!("\n=== CORRECTED SAMPLE RESULTS (First 10 cases) ===");
    println!("Total processed: {}", total_processed);
    println!("Exact matches: {} ({:.1}%)", exact_matches, (exact_matches as f64 / total_processed as f64) * 100.0);
    println!("Mismatches: {}", mismatches.len());
    
    if !mismatches.is_empty() {
        println!("\nMismatch details:");
        for (hex, expected, actual) in &mismatches {
            println!("  {} → Expected: \"{}\", Got: \"{}\"", hex, expected, actual);
        }
    }
    
    // Now do full dataset analysis with corrected comparison
    println!("\n=== FULL DATASET CORRECTED ANALYSIS ===");
    analyze_full_dataset_corrected(&classifier, &converter);
}

fn analyze_full_dataset_corrected(classifier: &IsccNbsClassifier, converter: &MunsellConverter) {
    let csv_content = include_str!("../ISCC_NBS_REFERENCE_DATASET.csv");
    let mut reader = csv::Reader::from_reader(csv_content.as_bytes());
    
    let mut exact_matches = 0;
    let mut no_classifications = 0;
    let mut mismatches = 0;
    let mut total_processed = 0;
    
    for result in reader.records() {
        let record = result.expect("Failed to read CSV record");
        
        // PROPER CSV STRING TRIMMING
        let hex = record.get(0).expect("Missing hex").trim();
        let reference_iscc_nbs_name = record.get(1).expect("Missing ISCC-NBS Name").trim();
        
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
                // CORRECT COMPARISON: Reference ISCC-NBS Name vs System iscc-nbs-descriptor  
                let system_iscc_nbs_descriptor = result.iscc_nbs_descriptor().trim();
                
                if reference_iscc_nbs_name == system_iscc_nbs_descriptor {
                    exact_matches += 1;
                } else {
                    mismatches += 1;
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
    
    println!("=== CORRECTED FULL DATASET RESULTS ===");
    println!("Total colors: {}", total_processed);
    println!("Exact matches: {} ({:.1}%)", exact_matches, (exact_matches as f64 / total_processed as f64) * 100.0);
    println!("Mismatches: {} ({:.1}%)", mismatches, (mismatches as f64 / total_processed as f64) * 100.0);
    println!("No classifications: {} ({:.1}%)", no_classifications, (no_classifications as f64 / total_processed as f64) * 100.0);
    
    println!("\n=== IMPROVEMENT FROM CORRECT COMPARISON ===");
    println!("This should show significantly better results than the previous 38% if the issue was field mismatch!");
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