use munsellspace::mathematical::MathematicalMunsellConverter;
use std::fs::File;
use std::io::{BufReader, BufRead};

fn main() {
    println!("Testing mathematical accuracy on 4007 reference colors...\n");
    
    let converter = MathematicalMunsellConverter::new().unwrap();
    
    // Load reference data
    let file = File::open("tests/data/srgb-to-munsell.csv").expect("Failed to open reference file");
    let reader = BufReader::new(file);
    let mut lines = reader.lines();
    
    // Skip header
    lines.next();
    
    let mut total = 0;
    let mut exact_matches = 0;
    let mut close_matches = 0;  // Within 0.1 difference
    let mut family_mismatches = 0;
    let mut max_hue_diff = 0.0;
    let mut max_value_diff = 0.0;
    let mut max_chroma_diff = 0.0;
    let mut sum_hue_diff = 0.0;
    let mut sum_value_diff = 0.0;
    let mut sum_chroma_diff = 0.0;
    
    for line in lines {
        let line = line.unwrap();
        let parts: Vec<&str> = line.split(',').collect();
        
        if parts.len() < 4 {
            continue;
        }
        
        let r = parts[0].trim().parse::<u8>().unwrap();
        let g = parts[1].trim().parse::<u8>().unwrap();
        let b = parts[2].trim().parse::<u8>().unwrap();
        let reference = parts[3].trim();
        
        total += 1;
        
        match converter.srgb_to_munsell([r, g, b]) {
            Ok(spec) => {
                let computed = format!("{:.1}{} {:.1}/{:.1}", 
                                     spec.hue, spec.family, spec.value, spec.chroma);
                
                // Parse reference for comparison
                if let Some((ref_hue_str, ref_rest)) = reference.split_once(|c: char| c.is_alphabetic()) {
                    if let Some((ref_family, ref_rest)) = ref_rest.split_once(' ') {
                        if let Some((ref_value_str, ref_chroma_str)) = ref_rest.split_once('/') {
                            let ref_hue: f64 = ref_hue_str.parse().unwrap_or(0.0);
                            let ref_value: f64 = ref_value_str.parse().unwrap_or(0.0);
                            let ref_chroma: f64 = ref_chroma_str.parse().unwrap_or(0.0);
                            
                            let hue_diff = (spec.hue - ref_hue).abs();
                            let value_diff = (spec.value - ref_value).abs();
                            let chroma_diff = (spec.chroma - ref_chroma).abs();
                            
                            sum_hue_diff += hue_diff;
                            sum_value_diff += value_diff;
                            sum_chroma_diff += chroma_diff;
                            
                            if hue_diff > max_hue_diff {
                                max_hue_diff = hue_diff;
                            }
                            if value_diff > max_value_diff {
                                max_value_diff = value_diff;
                            }
                            if chroma_diff > max_chroma_diff {
                                max_chroma_diff = chroma_diff;
                            }
                            
                            if spec.family != ref_family {
                                family_mismatches += 1;
                            }
                            
                            if computed == reference {
                                exact_matches += 1;
                            } else if hue_diff <= 0.1 && value_diff <= 0.1 && chroma_diff <= 0.1 {
                                close_matches += 1;
                            }
                            
                            // Show first few differences for debugging
                            if total <= 10 && computed != reference {
                                println!("RGB [{:3},{:3},{:3}]: {} vs {} (Δh={:.2}, Δv={:.2}, Δc={:.2})",
                                       r, g, b, computed, reference, hue_diff, value_diff, chroma_diff);
                            }
                        }
                    }
                } else if reference == "N 0.0" && spec.family == "N" && spec.value.abs() < 0.1 {
                    exact_matches += 1;
                }
            }
            Err(e) => {
                println!("ERROR converting RGB [{},{},{}]: {:?}", r, g, b, e);
            }
        }
    }
    
    println!("\n=== ACCURACY RESULTS ===");
    println!("Total colors: {}", total);
    println!("Exact matches: {} ({:.2}%)", exact_matches, exact_matches as f64 / total as f64 * 100.0);
    println!("Close matches (≤0.1): {} ({:.2}%)", close_matches, close_matches as f64 / total as f64 * 100.0);
    println!("Family mismatches: {} ({:.2}%)", family_mismatches, family_mismatches as f64 / total as f64 * 100.0);
    
    println!("\n=== DIFFERENCE STATISTICS ===");
    println!("Maximum differences:");
    println!("  Hue: {:.3}", max_hue_diff);
    println!("  Value: {:.3}", max_value_diff);
    println!("  Chroma: {:.3}", max_chroma_diff);
    
    println!("\nAverage differences:");
    println!("  Hue: {:.3}", sum_hue_diff / total as f64);
    println!("  Value: {:.3}", sum_value_diff / total as f64);
    println!("  Chroma: {:.3}", sum_chroma_diff / total as f64);
    
    let target_accuracy = close_matches + exact_matches;
    println!("\n=== TARGET ACHIEVEMENT ===");
    println!("Target: ≤0.1 difference in all dimensions");
    println!("Achievement: {} / {} ({:.2}%)", 
             target_accuracy, total, target_accuracy as f64 / total as f64 * 100.0);
    
    if target_accuracy as f64 / total as f64 >= 0.999 {
        println!("✅ TARGET ACHIEVED!");
    } else {
        println!("❌ Target not yet achieved");
    }
}