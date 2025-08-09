use munsellspace::{IsccNbsClassifier, MunsellConverter};
use std::fs::File;
use std::io::Write;

#[test]
fn generate_mismatch_csv() {
    println!("=== GENERATING COMPREHENSIVE MISMATCH CSV ===");
    
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Load the reference dataset
    let csv_content = include_str!("data/ISCC_NBS_REFERENCE_DATASET.csv");
    let mut reader = csv::Reader::from_reader(csv_content.as_bytes());
    
    // Create output CSV file
    let mut output_file = File::create("mismatch_analysis.csv").expect("Failed to create output file");
    
    // Write CSV header
    writeln!(output_file, "hex_color,r_component,g_component,b_component,munsell_notation,expected_iscc_nbs_name,actual_iscc_nbs_descriptor,match_status,notes").expect("Failed to write header");
    
    let mut total_processed = 0;
    let mut exact_matches = 0;
    let mut mismatches = 0;
    let mut no_classifications = 0;
    let mut conversion_failures = 0;
    
    println!("Processing all {} colors from reference dataset...", 267);
    
    for result in reader.records() {
        let record = result.expect("Failed to read CSV record");
        
        // Extract data with proper trimming
        let hex = record.get(0).expect("Missing hex").trim();
        let expected_iscc_nbs_name = record.get(1).expect("Missing ISCC-NBS Name").trim();
        
        // Parse hex to RGB components
        let (r, g, b) = match hex_to_rgb_components(hex) {
            Ok((r, g, b)) => (r, g, b),
            Err(e) => {
                // Write parsing failure row
                writeln!(output_file, "{},{},{},{},PARSE_ERROR,{},PARSE_ERROR,PARSE_FAILURE,Failed to parse hex: {}", 
                    hex, "ERROR", "ERROR", "ERROR", expected_iscc_nbs_name, e).expect("Failed to write");
                continue;
            }
        };
        
        let rgb = [r, g, b];
        
        // Convert to Munsell
        let munsell = match converter.srgb_to_munsell(rgb) {
            Ok(munsell) => munsell,
            Err(e) => {
                // Write conversion failure row
                writeln!(output_file, "{},{},{},{},CONVERSION_ERROR,{},CONVERSION_ERROR,CONVERSION_FAILURE,Munsell conversion failed: {}", 
                    hex, r, g, b, expected_iscc_nbs_name, e).expect("Failed to write");
                conversion_failures += 1;
                total_processed += 1;
                continue;
            }
        };
        
        let munsell_notation = munsell.to_string();
        
        // Try ISCC-NBS classification
        match classifier.classify_munsell_color(&munsell) {
            Ok(Some(result)) => {
                let actual_iscc_nbs_descriptor = result.iscc_nbs_descriptor().trim();
                
                if expected_iscc_nbs_name == actual_iscc_nbs_descriptor {
                    // Exact match
                    writeln!(output_file, "{},{},{},{},{},{},{},EXACT_MATCH,Perfect classification match", 
                        hex, r, g, b, munsell_notation, expected_iscc_nbs_name, actual_iscc_nbs_descriptor).expect("Failed to write");
                    exact_matches += 1;
                } else {
                    // Mismatch - analyze the type
                    let mismatch_note = analyze_mismatch_pattern(expected_iscc_nbs_name, actual_iscc_nbs_descriptor);
                    writeln!(output_file, "{},{},{},{},{},{},{},MISMATCH,{}", 
                        hex, r, g, b, munsell_notation, expected_iscc_nbs_name, actual_iscc_nbs_descriptor, mismatch_note).expect("Failed to write");
                    mismatches += 1;
                }
                total_processed += 1;
            }
            Ok(None) => {
                // No classification found
                writeln!(output_file, "{},{},{},{},{},{},NO_CLASSIFICATION,NO_CLASSIFICATION,Point not found in any ISCC-NBS polygon", 
                    hex, r, g, b, munsell_notation, expected_iscc_nbs_name).expect("Failed to write");
                no_classifications += 1;
                total_processed += 1;
            }
            Err(e) => {
                // Classification error
                writeln!(output_file, "{},{},{},{},{},{},CLASSIFICATION_ERROR,CLASSIFICATION_ERROR,Classification error: {}", 
                    hex, r, g, b, munsell_notation, expected_iscc_nbs_name, e).expect("Failed to write");
                total_processed += 1;
            }
        }
        
        // Progress indicator
        if total_processed % 50 == 0 {
            println!("  Processed {}/267 colors...", total_processed);
        }
    }
    
    println!("\n=== CSV GENERATION COMPLETE ===");
    println!("Output file: mismatch_analysis.csv");
    println!("Total processed: {}", total_processed);
    println!("Exact matches: {} ({:.1}%)", exact_matches, (exact_matches as f64 / total_processed as f64) * 100.0);
    println!("Mismatches: {} ({:.1}%)", mismatches, (mismatches as f64 / total_processed as f64) * 100.0);
    println!("No classifications: {} ({:.1}%)", no_classifications, (no_classifications as f64 / total_processed as f64) * 100.0);
    println!("Conversion failures: {} ({:.1}%)", conversion_failures, (conversion_failures as f64 / total_processed as f64) * 100.0);
    
    println!("\n=== CSV COLUMN EXPLANATION ===");
    println!("hex_color: Original hex color from reference dataset");
    println!("r_component, g_component, b_component: Base 10 RGB values (0-255)");
    println!("munsell_notation: Our Munsell conversion result (e.g., '5R 4.0/10.0')");
    println!("expected_iscc_nbs_name: Expected classification from reference dataset");
    println!("actual_iscc_nbs_descriptor: Our system's classification result");
    println!("match_status: EXACT_MATCH, MISMATCH, NO_CLASSIFICATION, CONVERSION_FAILURE, etc.");
    println!("notes: Analysis of mismatch pattern or error details");
}

fn analyze_mismatch_pattern(expected: &str, actual: &str) -> String {
    let expected_words: Vec<&str> = expected.split_whitespace().collect();
    let actual_words: Vec<&str> = actual.split_whitespace().collect();
    
    if expected_words.len() != actual_words.len() {
        return format!("Word count difference: {} vs {} words", expected_words.len(), actual_words.len());
    }
    
    // Check for specific patterns
    if expected.contains("pink") && actual.contains("yellowish") {
        return "Pink vs Yellowish family boundary issue".to_string();
    }
    
    if expected.contains("vivid") && actual.contains("light") {
        return "Intensity difference: vivid vs light".to_string();
    }
    
    if expected.contains("grayish") && actual.contains("brownish") {
        return "Modifier type difference: grayish vs brownish".to_string();
    }
    
    if expected.contains("pinkish") && actual.contains("yellowish") {
        return "Hue family assignment: pinkish vs yellowish".to_string();
    }
    
    // Generic difference description
    let mut differences = Vec::new();
    for (i, (exp_word, act_word)) in expected_words.iter().zip(actual_words.iter()).enumerate() {
        if exp_word != act_word {
            differences.push(format!("pos{}: {} vs {}", i, exp_word, act_word));
        }
    }
    
    if differences.is_empty() {
        "Unknown difference pattern".to_string()
    } else {
        format!("Word differences: {}", differences.join(", "))
    }
}

fn hex_to_rgb_components(hex: &str) -> Result<(u8, u8, u8), Box<dyn std::error::Error>> {
    let hex = hex.trim_start_matches('#');
    if hex.len() != 6 {
        return Err("Invalid hex length".into());
    }
    
    let r = u8::from_str_radix(&hex[0..2], 16)?;
    let g = u8::from_str_radix(&hex[2..4], 16)?;
    let b = u8::from_str_radix(&hex[4..6], 16)?;
    
    Ok((r, g, b))
}