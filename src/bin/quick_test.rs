use munsellspace::mathematical::MathematicalMunsellConverter;
use std::fs::File;
use std::io::{BufReader, BufRead};

fn main() {
    println!("Quick test of 100 colors...\n");
    
    let converter = MathematicalMunsellConverter::new().unwrap();
    
    // Load reference data
    let file = File::open("tests/data/srgb-to-munsell.csv").expect("Failed to open reference file");
    let reader = BufReader::new(file);
    let mut lines = reader.lines();
    
    // Skip header
    lines.next();
    
    let mut total = 0;
    let mut exact_matches = 0;
    let mut family_matches = 0;
    let mut max_hue_diff = 0.0f64;
    let mut max_value_diff = 0.0f64;
    let mut max_chroma_diff = 0.0f64;
    
    for line in lines.take(100) {  // Only test first 100 colors
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
                            
                            max_hue_diff = max_hue_diff.max(hue_diff);
                            max_value_diff = max_value_diff.max(value_diff);
                            max_chroma_diff = max_chroma_diff.max(chroma_diff);
                            
                            if spec.family == ref_family {
                                family_matches += 1;
                            }
                            
                            if computed == reference {
                                exact_matches += 1;
                            }
                            
                            // Show first few for debugging
                            if total <= 5 {
                                println!("RGB [{:3},{:3},{:3}]: {} vs {} (Δh={:.2}, Δv={:.2}, Δc={:.2})",
                                       r, g, b, computed, reference, hue_diff, value_diff, chroma_diff);
                            }
                        }
                    }
                } else if reference == "N 0.0" && spec.family == "N" && spec.value.abs() < 0.1 {
                    exact_matches += 1;
                    family_matches += 1;
                    if total <= 5 {
                        println!("RGB [{:3},{:3},{:3}]: {} vs {} (achromatic)",
                               r, g, b, spec.family, reference);
                    }
                }
            }
            Err(e) => {
                println!("ERROR converting RGB [{},{},{}]: {:?}", r, g, b, e);
            }
        }
    }
    
    println!("\n=== QUICK RESULTS (100 colors) ===");
    println!("Exact matches: {}/{} ({:.1}%)", exact_matches, total, exact_matches as f64 / total as f64 * 100.0);
    println!("Family matches: {}/{} ({:.1}%)", family_matches, total, family_matches as f64 / total as f64 * 100.0);
    println!("Max differences: Δh={:.2}, Δv={:.2}, Δc={:.2}", max_hue_diff, max_value_diff, max_chroma_diff);
}