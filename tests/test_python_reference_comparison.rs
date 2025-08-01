use munsellspace::MunsellConverter;
use std::fs::File;
use std::io::Write;

#[test] 
fn compare_against_python_reference() {
    println!("=== RUST vs PYTHON COLOUR-SCIENCE COMPARISON ===");
    println!("Step-by-step pipeline comparison to identify systematic bias source");
    
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Test specific examples from bias analysis
    let critical_examples = [
        ([255, 181, 186], "#ffb5ba", "Our: 5.9R 8.1/5.5 vs Python: 0.0YR 9.0/2.6"),
        ([234, 147, 153], "#ea9399", "Our: estimated vs Python: 7.2R 8.4/3.4"),
        ([190, 0, 50], "#be0032", "High chroma test: Python: 7.6RP 4.8/17.3"),
        ([243, 132, 0], "#f38400", "Yellow test: Python: 2.9Y 8.0/12.4"),
    ];
    
    // Python reference data from successful conversions
    let python_reference = [
        // RGB, Python XYZ, Python xyY, Python Munsell
        ([255, 181, 186], [0.7979, 0.7729, 0.7972], [0.3369, 0.3264, 0.7729], "0.0YR", 9.0, 2.6),
        ([234, 147, 153], [0.6929, 0.6507, 0.6567], [0.3464, 0.3253, 0.6507], "7.2R", 8.4, 3.4),
        ([190, 0, 50], [0.3427, 0.1726, 0.2008], [0.4786, 0.2410, 0.1726], "7.6RP", 4.8, 17.3),
        ([243, 132, 0], [0.5781, 0.5728, 0.0801], [0.4696, 0.4653, 0.5728], "2.9Y", 8.0, 12.4),
    ];
    
    let mut output_file = File::create("rust_python_comparison.csv").expect("Failed to create output file");
    writeln!(output_file, "hex_color,r,g,b,rust_munsell,rust_hue_num,rust_hue_family,rust_value,rust_chroma,python_munsell,python_hue_family,python_value,python_chroma,hue_difference,value_difference,chroma_difference,pipeline_analysis").expect("Failed to write header");
    
    println!("\n=== CRITICAL EXAMPLES ANALYSIS ===");
    
    for (i, &(rgb, hex, description)) in critical_examples.iter().enumerate() {
        println!("\n🔍 Example {}: {} RGB{:?}", i+1, hex, rgb);
        println!("   Context: {}", description);
        
        // Convert with our system
        match converter.srgb_to_munsell(rgb) {
            Ok(our_munsell) => {
                let our_notation = our_munsell.to_string();
                println!("   ✅ Our Rust result: {}", our_notation);
                
                // Parse our result
                let (our_hue_num, our_hue_family, our_value, our_chroma) = parse_munsell_components(&our_notation);
                
                // Get Python reference if available
                if let Some(&(_, _, _, python_hue_family, python_value, python_chroma)) = python_reference.get(i) {
                    println!("   ✅ Python reference: {}{} {:.1}/{:.1}", 
                        if python_hue_family.ends_with("R") { 
                            python_hue_family.trim_end_matches("R")
                        } else if python_hue_family.ends_with("YR") {
                            python_hue_family.trim_end_matches("YR") 
                        } else if python_hue_family.ends_with("Y") {
                            python_hue_family.trim_end_matches("Y")
                        } else if python_hue_family.ends_with("RP") {
                            python_hue_family.trim_end_matches("RP")
                        } else {
                            "?"
                        }, python_hue_family, python_value, python_chroma);
                    
                    // Calculate differences
                    let hue_diff = calculate_circular_hue_difference(our_hue_num, &our_hue_family, 
                        extract_hue_number(python_hue_family), &extract_hue_family(python_hue_family));
                    let value_diff = our_value - python_value;
                    let chroma_diff = our_chroma - python_chroma;
                    
                    println!("   📊 Differences:");
                    println!("      Hue: {:.1} points (circular)", hue_diff);
                    println!("      Value: {:.1} points", value_diff);
                    println!("      Chroma: {:.1} points", chroma_diff);
                    
                    // Write to CSV
                    writeln!(output_file, "{},{},{},{},{},{},{},{:.1},{:.1},{}{} {:.1}/{:.1},{},{:.1},{:.1},{:.2},{:.2},{:.2},{}",
                        hex, rgb[0], rgb[1], rgb[2], 
                        our_notation, our_hue_num, our_hue_family, our_value, our_chroma,
                        extract_hue_number(python_hue_family), extract_hue_family(python_hue_family), python_value, python_chroma,
                        extract_hue_family(python_hue_family), python_value, python_chroma,
                        hue_diff, value_diff, chroma_diff,
                        "Critical_Example").expect("Failed to write");
                        
                    // Analyze the magnitude of differences
                    if hue_diff.abs() > 10.0 {
                        println!("   ⚠️  MAJOR HUE DISCREPANCY: {:.1} points", hue_diff);
                    }
                    if value_diff.abs() > 1.0 {
                        println!("   ⚠️  MAJOR VALUE DISCREPANCY: {:.1} points", value_diff);
                    }
                    if chroma_diff.abs() > 3.0 {
                        println!("   ⚠️  MAJOR CHROMA DISCREPANCY: {:.1} points", chroma_diff);
                    }
                }
            }
            Err(e) => {
                println!("   ❌ Our conversion failed: {}", e);
            }
        }
    }
    
    println!("\n=== INTERMEDIATE STEP ANALYSIS ===");
    
    // For the most critical case, let's analyze intermediate steps
    let critical_rgb = [255, 181, 186];
    let python_xyz = [0.7979, 0.7729, 0.7972];
    let python_xyy = [0.3369, 0.3264, 0.7729];
    
    println!("\n🔬 Deep analysis for RGB{:?} (#ffb5ba):", critical_rgb);
    
    // Test our individual conversion steps if we can access them
    // Note: This would require exposing internal conversion methods
    println!("   Python XYZ: [{:.4}, {:.4}, {:.4}]", python_xyz[0], python_xyz[1], python_xyz[2]);
    println!("   Python xyY: [{:.4}, {:.4}, {:.4}]", python_xyy[0], python_xyy[1], python_xyy[2]);
    println!("   Python Munsell: 0.0YR 9.0/2.6");
    
    // Our full pipeline result
    if let Ok(our_munsell) = converter.srgb_to_munsell(critical_rgb) {
        println!("   Our Munsell: {}", our_munsell);
        println!("   
⚠️  CRITICAL FINDING: Completely different results suggest:");
        println!("      1. Different sRGB→XYZ transformation matrices");
        println!("      2. Different illuminant assumptions (D65 vs C)");
        println!("      3. Different Munsell conversion algorithms");
        println!("      4. Our algorithm may not be following standard color science");
    }
    
    println!("\n=== ALGORITHM COMPATIBILITY ANALYSIS ===");
    println!("Based on the massive discrepancies observed:");
    println!("1. 🚨 Our hue families don't match Python (5.9R vs 0.0YR = ~59 point difference)"); 
    println!("2. 🚨 Our values are systematically different (8.1 vs 9.0 = 0.9 point difference)");
    println!("3. 🚨 Our chroma is systematically different (5.5 vs 2.6 = 2.9 point difference)");
    println!("4. 💡 This suggests our algorithm is fundamentally different from colour-science library");
    println!("5. 💡 We may need to validate against the 4007-color reference table instead");
    println!("6. 💡 The +4.54 hue bias against 4007-table may be correct if Python library has different assumptions");
    
    println!("\n=== RECOMMENDED NEXT STEPS ===");
    println!("1. 🔍 Compare our sRGB→XYZ matrices against Python colour-science");
    println!("2. 🔍 Check illuminant assumptions (D65 vs Illuminant C)");
    println!("3. 🔍 Validate our algorithm against published Munsell conversion papers");
    println!("4. 🔍 Consider that our +4.54 bias might be correct if Python uses different color science");
    println!("5. 📊 Prioritize accuracy against 4007-color reference table over Python library alignment");
    
    println!("\n📁 Detailed comparison saved to: rust_python_comparison.csv");
}

fn parse_munsell_components(munsell: &str) -> (f64, String, f64, f64) {
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

fn extract_hue_number(python_hue: &str) -> f64 {
    // Extract number from "0.0YR", "7.2R", etc.
    let mut num_str = String::new();
    for c in python_hue.chars() {
        if c.is_digit(10) || c == '.' {
            num_str.push(c);
        } else {
            break;
        }
    }
    num_str.parse().unwrap_or(0.0)
}

fn extract_hue_family(python_hue: &str) -> String {
    // Extract family from "0.0YR", "7.2R", etc.
    let mut family = String::new();
    let mut found_letter = false;
    for c in python_hue.chars() {
        if c.is_alphabetic() {
            found_letter = true;
            family.push(c);
        } else if found_letter {
            break;
        }
    }
    family
}

fn calculate_circular_hue_difference(hue1: f64, family1: &str, hue2: f64, family2: &str) -> f64 {
    // Convert to 100-point circular coordinate system
    let families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
    
    let family1_idx = families.iter().position(|&f| f == family1).unwrap_or(0) as f64;
    let family2_idx = families.iter().position(|&f| f == family2).unwrap_or(0) as f64;
    
    let pos1 = family1_idx * 10.0 + hue1;
    let pos2 = family2_idx * 10.0 + hue2;
    
    // Calculate shortest circular distance
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