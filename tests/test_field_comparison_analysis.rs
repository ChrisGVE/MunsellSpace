use munsellspace::{IsccNbsClassifier, MunsellConverter};

#[test]
fn analyze_field_comparison_details() {
    println!("=== FIELD COMPARISON ANALYSIS ===");
    println!("Examining exactly what fields we're comparing and what's available");
    
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // First, let's examine the CSV structure
    println!("\n=== CSV STRUCTURE ANALYSIS ===");
    let csv_content = include_str!("../ISCC_NBS_REFERENCE_DATASET.csv");
    let mut reader = csv::Reader::from_reader(csv_content.as_bytes());
    
    // Read the header
    let headers = reader.headers().expect("Failed to read headers");
    println!("CSV Headers:");
    for (i, header) in headers.iter().enumerate() {
        println!("  Column {}: \"{}\"", i, header);
    }
    
    println!("\n=== COMPARISON FIELD ANALYSIS ===");
    println!("Currently comparing:");
    println!("  CSV Column 1 (expected_descriptor) vs result.revised_descriptor()");
    
    // Let's examine the first few records in detail
    println!("\n=== DETAILED FIELD EXAMINATION (First 5 cases) ===");
    
    let mut reader = csv::Reader::from_reader(csv_content.as_bytes());
    
    for (i, result) in reader.records().enumerate() {
        if i >= 5 { break; }
        
        let record = result.expect("Failed to read CSV record");
        
        println!("\n--- RECORD {} ---", i + 1);
        
        // Show all CSV fields
        println!("CSV Fields:");
        for (j, field) in record.iter().enumerate() {
            println!("  [{}]: \"{}\"", j, field);
        }
        
        let hex = record.get(0).expect("Missing hex").trim();
        let expected_descriptor = record.get(1).expect("Missing descriptor").trim();
        
        // Convert and classify
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
        
        match classifier.classify_munsell_color(&munsell) {
            Ok(Some(result)) => {
                println!("ISCC-NBS Result Fields:");
                println!("  iscc_nbs_descriptor(): \"{}\"", result.iscc_nbs_descriptor());
                println!("  iscc_nbs_color(): \"{}\"", result.iscc_nbs_color());
                println!("  iscc_nbs_modifier(): {:?}", result.iscc_nbs_modifier());
                println!("  revised_color(): \"{}\"", result.revised_color());
                println!("  revised_descriptor(): \"{}\"", result.revised_descriptor());
                println!("  shade(): \"{}\"", result.shade());
                println!("  iscc_nbs_color_id(): {}", result.iscc_nbs_color_id());
                
                println!("\nCOMPARISON ANALYSIS:");
                println!("  CSV expected: \"{}\"", expected_descriptor);
                println!("  Using revised_descriptor(): \"{}\"", result.revised_descriptor());
                println!("  Match: {}", expected_descriptor == result.revised_descriptor());
                
                // Let's check other potential matches
                println!("\nALTERNATIVE FIELD MATCHES:");
                println!("  vs iscc_nbs_descriptor(): {} (\"{}\")", 
                    expected_descriptor == result.iscc_nbs_descriptor(), result.iscc_nbs_descriptor());
                println!("  vs revised_color(): {} (\"{}\")", 
                    expected_descriptor == result.revised_color(), result.revised_color());
                    
                // Construct other possible combinations
                let simple_combination = format!("{} {}", result.iscc_nbs_descriptor(), result.revised_color());
                println!("  vs simple combination (descriptor + color): {} (\"{}\")", 
                    expected_descriptor == simple_combination, simple_combination);
                    
                if let Some(modifier) = result.iscc_nbs_modifier() {
                    let with_modifier = format!("{} {}", modifier, result.revised_color());
                    println!("  vs modifier + color: {} (\"{}\")", 
                        expected_descriptor == with_modifier, with_modifier);
                }
            }
            Ok(None) => {
                println!("❌ NO CLASSIFICATION");
            }
            Err(e) => {
                println!("❌ Classification error: {}", e);
            }
        }
    }
    
    println!("\n=== RECOMMENDATION ===");
    println!("Check if we should be comparing against a different field combination");
    println!("or if the CSV reference uses a different descriptor construction method.");
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