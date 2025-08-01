use munsellspace::MunsellConverter;
use std::fs::File;
use std::io::Write;

#[test]
fn validate_against_4007_reference_table() {
    println!("=== 4007-COLOR REFERENCE TABLE VALIDATION ===");
    println!("Direct validation against scientific ground truth");
    
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Load the 4007-color reference table
    let csv_content = include_str!("../tests/data/srgb-to-munsell.csv");
    let mut reader = csv::Reader::from_reader(csv_content.as_bytes());
    
    let mut output_file = File::create("4007_validation_results.csv").expect("Failed to create output file");
    writeln!(output_file, "r,g,b,reference_munsell,our_munsell,hue_diff,value_diff,chroma_diff,match_type,analysis").expect("Failed to write header");
    
    let mut total_colors = 0;
    let mut exact_matches = 0;
    let mut close_matches = 0; // Within reasonable tolerance
    let mut conversion_failures = 0;
    let mut processed = 0;
    
    let mut hue_differences = Vec::new();
    let mut value_differences = Vec::new();
    let mut chroma_differences = Vec::new();
    
    println!("Processing 4007-color reference table...");
    
    for result in reader.records() {
        let record = result.expect("Failed to read CSV record");
        
        // Parse: R, G, B, Munsell Colour
        let r: u8 = record.get(0).expect("Missing R").trim().parse().expect("Invalid R");
        let g: u8 = record.get(1).expect("Missing G").trim().parse().expect("Invalid G");
        let b: u8 = record.get(2).expect("Missing B").trim().parse().expect("Invalid B");
        let reference_munsell = record.get(3).expect("Missing Munsell").trim();
        
        total_colors += 1;
        
        // Convert with our system
        match converter.srgb_to_munsell([r, g, b]) {
            Ok(our_munsell) => {
                let our_notation = our_munsell.to_string();
                
                // Parse both Munsell notations
                let (ref_hue_num, ref_hue_family, ref_value, ref_chroma) = parse_munsell_components(reference_munsell);
                let (our_hue_num, our_hue_family, our_value, our_chroma) = parse_munsell_components(&our_notation);
                
                // Calculate differences
                let hue_diff = calculate_circular_hue_difference(our_hue_num, &our_hue_family, ref_hue_num, &ref_hue_family);
                let value_diff = our_value - ref_value;
                let chroma_diff = our_chroma - ref_chroma;
                
                // Store for statistics
                hue_differences.push(hue_diff);
                value_differences.push(value_diff);
                chroma_differences.push(chroma_diff);
                
                // Determine match type
                let (match_type, analysis) = if reference_munsell == &our_notation {
                    exact_matches += 1;
                    ("EXACT", "Perfect match".to_string())
                } else if hue_diff.abs() <= 2.0 && value_diff.abs() <= 0.5 && chroma_diff.abs() <= 1.0 {
                    close_matches += 1;
                    ("CLOSE", "Within reasonable tolerance".to_string())
                } else if hue_diff.abs() > 10.0 {
                    ("HUE_MAJOR", format!("Major hue difference: {:.1} points", hue_diff))
                } else if value_diff.abs() > 2.0 {
                    ("VALUE_MAJOR", format!("Major value difference: {:.1} points", value_diff))
                } else if chroma_diff.abs() > 5.0 {
                    ("CHROMA_MAJOR", format!("Major chroma difference: {:.1} points", chroma_diff))
                } else {
                    ("MINOR", "Minor differences within acceptable range".to_string())
                };
                
                // Write to CSV
                writeln!(output_file, "{},{},{},{},{},{:.2},{:.2},{:.2},{},{}",
                    r, g, b, reference_munsell, our_notation, hue_diff, value_diff, chroma_diff, match_type, analysis).expect("Failed to write");
                
                processed += 1;
            }
            Err(e) => {
                conversion_failures += 1;
                writeln!(output_file, "{},{},{},{},CONVERSION_FAILED,,,,,Conversion error: {}",
                    r, g, b, reference_munsell, e).expect("Failed to write");
            }
        }
        
        // Progress indicator
        if total_colors % 500 == 0 {
            println!("  Processed {}/4007 colors...", total_colors);
        }
    }
    
    println!("\n=== 4007-COLOR VALIDATION RESULTS ===");
    println!("Total colors in reference table: {}", total_colors);
    println!("Successfully converted: {} ({:.1}%)", processed, (processed as f64 / total_colors as f64) * 100.0);
    println!("Conversion failures: {} ({:.1}%)", conversion_failures, (conversion_failures as f64 / total_colors as f64) * 100.0);
    println!("Exact matches: {} ({:.2}%)", exact_matches, (exact_matches as f64 / processed as f64) * 100.0);
    println!("Close matches: {} ({:.2}%)", close_matches, (close_matches as f64 / processed as f64) * 100.0);
    println!("Combined accuracy: {} ({:.2}%)", exact_matches + close_matches, ((exact_matches + close_matches) as f64 / processed as f64) * 100.0);
    
    // Statistical analysis
    if !hue_differences.is_empty() {
        let hue_mean = hue_differences.iter().sum::<f64>() / hue_differences.len() as f64;
        let hue_std = calculate_std_dev(&hue_differences, hue_mean);
        println!("\n=== SYSTEMATIC BIAS ANALYSIS ===");
        println!("HUE ANALYSIS (4007-color reference):");
        println!("  Mean difference: {:.3} hue points", hue_mean);
        println!("  Std deviation: {:.3} hue points", hue_std);
        println!("  Range: {:.2} to {:.2}", 
            hue_differences.iter().fold(f64::INFINITY, |a, &b| a.min(b)),
            hue_differences.iter().fold(f64::NEG_INFINITY, |a, &b| a.max(b)));
        
        if hue_mean.abs() > 2.0 {
            println!("  ⚠️  SYSTEMATIC HUE BIAS: {:.3} points", hue_mean);
            if hue_mean > 0.0 {
                println!("     Our system calculates hues {:.3} points HIGHER than reference", hue_mean);
            } else {
                println!("     Our system calculates hues {:.3} points LOWER than reference", hue_mean.abs());
            }
        } else {
            println!("  ✅ No significant hue bias detected");
        }
        
        // Value analysis  
        let value_mean = value_differences.iter().sum::<f64>() / value_differences.len() as f64;
        let value_std = calculate_std_dev(&value_differences, value_mean);
        println!("\nVALUE ANALYSIS:");
        println!("  Mean difference: {:.3} value points", value_mean);
        println!("  Std deviation: {:.3} value points", value_std);
        
        if value_mean.abs() > 0.3 {
            println!("  ⚠️  SYSTEMATIC VALUE BIAS: {:.3} points", value_mean);
        } else {
            println!("  ✅ No significant value bias detected");
        }
        
        // Chroma analysis
        let chroma_mean = chroma_differences.iter().sum::<f64>() / chroma_differences.len() as f64;
        let chroma_std = calculate_std_dev(&chroma_differences, chroma_mean);
        println!("\nCHROMA ANALYSIS:");
        println!("  Mean difference: {:.3} chroma points", chroma_mean);
        println!("  Std deviation: {:.3} chroma points", chroma_std);
        
        if chroma_mean.abs() > 0.5 {
            println!("  ⚠️  SYSTEMATIC CHROMA BIAS: {:.3} points", chroma_mean);
        } else {
            println!("  ✅ No significant chroma bias detected");
        }
    }
    
    println!("\n=== COMPARISON WITH PREVIOUS FINDINGS ===");
    println!("Previous ISCC-NBS analysis against 4007-table found: +4.54 hue point bias");
    println!("This direct validation should confirm if that bias is real or artifact");
    
    println!("\n=== ACCURACY ASSESSMENT ===");
    let total_acceptable = exact_matches + close_matches;
    let accuracy_rate = (total_acceptable as f64 / processed as f64) * 100.0;
    
    if accuracy_rate >= 99.0 {
        println!("✅ EXCELLENT: {:.2}% accuracy - Ready for publication", accuracy_rate);
    } else if accuracy_rate >= 95.0 {
        println!("✅ GOOD: {:.2}% accuracy - Production ready with minor calibration needed", accuracy_rate);
    } else if accuracy_rate >= 90.0 {
        println!("⚠️  ACCEPTABLE: {:.2}% accuracy - Needs calibration improvement", accuracy_rate);
    } else {
        println!("❌ NEEDS WORK: {:.2}% accuracy - Significant algorithm issues", accuracy_rate);
    }
    
    println!("\n=== CONCLUSIONS ===");
    println!("1. Our algorithm's true accuracy against scientific reference: {:.2}% combined", accuracy_rate);
    println!("2. This is the authoritative measure - not Python library comparison");
    println!("3. Python colour-science differences are algorithm variations, not errors");
    println!("4. Focus should be on improving accuracy against 4007-color reference");
    
    println!("\n📁 Detailed validation saved to: 4007_validation_results.csv");
}

fn parse_munsell_components(munsell: &str) -> (f64, String, f64, f64) {
    // Handle special cases
    if munsell.starts_with("N ") {
        // Neutral: "N 5.0" -> (0.0, "N", 5.0, 0.0)
        let value_str = munsell.trim_start_matches("N ").trim();
        let value: f64 = value_str.parse().unwrap_or(0.0);
        return (0.0, "N".to_string(), value, 0.0);
    }
    
    // Parse "5.9R 8.1/5.5" into components
    let parts: Vec<&str> = munsell.split_whitespace().collect();
    if parts.len() != 2 {
        return (0.0, "N".to_string(), 0.0, 0.0);
    }
    
    // Parse hue (e.g., "5.9R")
    let hue_part = parts[0];
    let mut split_pos = 0;
    for (i, c) in hue_part.char_indices() {
        if c.is_alphabetic() {
            split_pos = i;
            break;
        }
    }
    
    let hue_num: f64 = hue_part[..split_pos].parse().unwrap_or(0.0);
    let hue_family = hue_part[split_pos..].to_string();
    
    // Parse value/chroma (e.g., "8.1/5.5")
    let value_chroma: Vec<&str> = parts[1].split('/').collect();
    let value: f64 = value_chroma[0].parse().unwrap_or(0.0);
    let chroma: f64 = value_chroma.get(1).unwrap_or(&"0").parse().unwrap_or(0.0);
    
    (hue_num, hue_family, value, chroma)
}

fn calculate_circular_hue_difference(hue1: f64, family1: &str, hue2: f64, family2: &str) -> f64 {
    // Handle neutral colors
    if family1 == "N" || family2 == "N" {
        return 0.0; // Neutral colors have no hue difference
    }
    
    // Convert to 100-point circular coordinate system
    let families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
    
    let family1_idx = families.iter().position(|&f| f == family1).unwrap_or(0) as f64;
    let family2_idx = families.iter().position(|&f| f == family2).unwrap_or(0) as f64;
    
    let pos1 = family1_idx * 10.0 + hue1;
    let pos2 = family2_idx * 10.0 + hue2;
    
    // Calculate signed circular distance (pos1 - pos2)
    let diff = pos1 - pos2;
    if diff.abs() > 50.0 {
        if diff > 0.0 {
            diff - 100.0
        } else {
            diff + 100.0
        }
    } else {
        diff
    }
}

fn calculate_std_dev(values: &[f64], mean: f64) -> f64 {
    if values.is_empty() {
        return 0.0;
    }
    
    let variance = values.iter()
        .map(|&x| (x - mean).powi(2))
        .sum::<f64>() / values.len() as f64;
    
    variance.sqrt()
}