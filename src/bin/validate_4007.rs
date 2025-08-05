use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;
use munsellspace::MathematicalMunsellConverter;

fn parse_munsell(notation: &str) -> Option<(f64, String, f64, f64)> {
    if notation.starts_with("N ") {
        let parts: Vec<&str> = notation.split_whitespace().collect();
        if parts.len() >= 2 {
            let value: f64 = parts[1].parse().ok()?;
            return Some((0.0, "N".to_string(), value, 0.0));
        }
    }
    
    // Parse chromatic notation like "5.0R 4.0/12.0"
    let parts: Vec<&str> = notation.split_whitespace().collect();
    if parts.len() == 2 {
        // Parse hue and family
        let hue_part = parts[0];
        let mut hue = 10.0;
        let mut family = String::new();
        
        // Extract numeric part and letter part
        let mut numeric_end = 0;
        for (i, c) in hue_part.chars().enumerate() {
            if c.is_alphabetic() {
                numeric_end = i;
                family = hue_part[i..].to_string();
                break;
            }
        }
        
        if numeric_end > 0 {
            hue = hue_part[..numeric_end].parse().unwrap_or(10.0);
        }
        
        // Parse value/chroma
        let value_chroma = parts[1];
        if let Some(slash_pos) = value_chroma.find('/') {
            let value: f64 = value_chroma[..slash_pos].parse().ok()?;
            let chroma: f64 = value_chroma[slash_pos+1..].parse().ok()?;
            return Some((hue, family, value, chroma));
        } else {
            // No chroma (neutral-like)
            let value: f64 = value_chroma.parse().ok()?;
            return Some((hue, family, value, 0.0));
        }
    }
    
    None
}

fn main() {
    println!("Validating all 4007 reference colors...");
    println!("{}", "=".repeat(70));
    
    let converter = MathematicalMunsellConverter::new().expect("Failed to create converter");
    
    // Read CSV file
    let file = File::open("tests/data/srgb-to-munsell.csv").expect("Failed to open CSV");
    let reader = BufReader::new(file);
    let mut lines = reader.lines();
    
    // Skip header
    lines.next();
    
    let mut total = 0;
    let mut exact_matches = 0;
    let mut family_matches = 0;
    let mut value_within_01 = 0;
    let mut chroma_within_01 = 0;
    let mut hue_within_01 = 0;
    let mut chromatic_count = 0;
    
    let mut value_diffs = Vec::new();
    let mut chroma_diffs = Vec::new();
    let mut hue_diffs = Vec::new();
    
    let start = Instant::now();
    
    for line in lines {
        if let Ok(line) = line {
            let parts: Vec<&str> = line.split(',').collect();
            if parts.len() >= 4 {
                let r: u8 = parts[0].trim().parse().unwrap_or(0);
                let g: u8 = parts[1].trim().parse().unwrap_or(0);
                let b: u8 = parts[2].trim().parse().unwrap_or(0);
                let expected = parts[3].trim();
                
                // Convert RGB to Munsell
                match converter.srgb_to_munsell([r, g, b]) {
                    Ok(munsell) => {
                        let rust_output = converter.format_munsell_notation(&munsell);
                        
                        // Check exact match
                        if rust_output == expected {
                            exact_matches += 1;
                        }
                        
                        // Parse and compare components
                        if let (Some(expected_parsed), Some(rust_parsed)) = 
                            (parse_munsell(expected), parse_munsell(&rust_output)) {
                            
                            // Family match
                            if expected_parsed.1 == rust_parsed.1 {
                                family_matches += 1;
                                
                                // Value difference
                                let v_diff = (expected_parsed.2 - rust_parsed.2).abs();
                                value_diffs.push(v_diff);
                                if v_diff <= 0.1 {
                                    value_within_01 += 1;
                                }
                                
                                // Chroma difference
                                let c_diff = (expected_parsed.3 - rust_parsed.3).abs();
                                chroma_diffs.push(c_diff);
                                if c_diff <= 0.1 {
                                    chroma_within_01 += 1;
                                }
                                
                                // Hue difference (only for chromatic)
                                if expected_parsed.1 != "N" {
                                    chromatic_count += 1;
                                    let mut h_diff = (expected_parsed.0 - rust_parsed.0).abs();
                                    // Handle wraparound
                                    if h_diff > 5.0 {
                                        h_diff = 10.0 - h_diff;
                                    }
                                    hue_diffs.push(h_diff);
                                    if h_diff <= 0.1 {
                                        hue_within_01 += 1;
                                    }
                                }
                            }
                        }
                    }
                    Err(_) => {}
                }
                
                total += 1;
                
                // Progress indicator
                if total % 100 == 0 {
                    let elapsed = start.elapsed().as_secs_f64();
                    let rate = total as f64 / elapsed;
                    let remaining = (4007 - total) as f64 / rate;
                    print!("\rProcessed {}/4007 colors... ({:.1}%, ~{:.0}s remaining)    ", 
                           total, 100.0 * total as f64 / 4007.0, remaining);
                    use std::io::Write;
                    std::io::stdout().flush().unwrap();
                }
            }
        }
    }
    
    let elapsed = start.elapsed().as_secs_f64();
    
    // Clear progress line
    println!("\r{}", " ".repeat(80));
    
    // Calculate statistics
    let mean = |v: &[f64]| -> f64 {
        if v.is_empty() { 0.0 } else { v.iter().sum::<f64>() / v.len() as f64 }
    };
    
    let median = |v: &mut [f64]| -> f64 {
        if v.is_empty() { 
            0.0 
        } else {
            v.sort_by(|a, b| a.partial_cmp(b).unwrap());
            if v.len() % 2 == 0 {
                (v[v.len()/2 - 1] + v[v.len()/2]) / 2.0
            } else {
                v[v.len()/2]
            }
        }
    };
    
    let std_dev = |v: &[f64], mean: f64| -> f64 {
        if v.len() <= 1 { 
            0.0 
        } else {
            let variance = v.iter().map(|x| (x - mean).powi(2)).sum::<f64>() / (v.len() - 1) as f64;
            variance.sqrt()
        }
    };
    
    let max = |v: &[f64]| -> f64 {
        v.iter().fold(0.0, |acc, &x| if x > acc { x } else { acc })
    };
    
    println!("\n{}", "=".repeat(70));
    println!("FINAL RESULTS FOR ALL 4007 REFERENCE COLORS");
    println!("{}", "=".repeat(70));
    
    println!("\nExact Matches: {}/{} ({:.2}%)", 
             exact_matches, total, 100.0 * exact_matches as f64 / total as f64);
    println!("Family Matches: {}/{} ({:.2}%)", 
             family_matches, total, 100.0 * family_matches as f64 / total as f64);
    
    if family_matches > 0 {
        println!("\nComponent Accuracy (for {} family matches):", family_matches);
        println!("  Values within 0.1: {}/{} ({:.1}%)", 
                 value_within_01, family_matches, 100.0 * value_within_01 as f64 / family_matches as f64);
        println!("  Chromas within 0.1: {}/{} ({:.1}%)", 
                 chroma_within_01, family_matches, 100.0 * chroma_within_01 as f64 / family_matches as f64);
        
        if chromatic_count > 0 {
            println!("  Hues within 0.1: {}/{} ({:.1}%)", 
                     hue_within_01, chromatic_count, 100.0 * hue_within_01 as f64 / chromatic_count as f64);
        }
        
        let v_mean = mean(&value_diffs);
        let c_mean = mean(&chroma_diffs);
        
        println!("\nDifference Statistics (for {} family matches):", family_matches);
        println!("  Value differences:");
        println!("    Mean: {:.4}", v_mean);
        println!("    Median: {:.4}", median(&mut value_diffs.clone()));
        println!("    Std Dev: {:.4}", std_dev(&value_diffs, v_mean));
        println!("    Max: {:.4}", max(&value_diffs));
        
        println!("  Chroma differences:");
        println!("    Mean: {:.4}", c_mean);
        println!("    Median: {:.4}", median(&mut chroma_diffs.clone()));
        println!("    Std Dev: {:.4}", std_dev(&chroma_diffs, c_mean));
        println!("    Max: {:.4}", max(&chroma_diffs));
        
        if !hue_diffs.is_empty() {
            let h_mean = mean(&hue_diffs);
            println!("  Hue differences (chromatic only):");
            println!("    Mean: {:.4}", h_mean);
            println!("    Median: {:.4}", median(&mut hue_diffs.clone()));
            println!("    Std Dev: {:.4}", std_dev(&hue_diffs, h_mean));
            println!("    Max: {:.4}", max(&hue_diffs));
        }
    }
    
    println!("\nProcessing time: {:.2} seconds ({:.1} colors/sec)", 
             elapsed, total as f64 / elapsed);
    
    // Success criteria
    println!("\n{}", "=".repeat(70));
    println!("SUCCESS CRITERIA ASSESSMENT:");
    println!("{}", "=".repeat(70));
    
    if family_matches >= (0.99 * total as f64) as usize {
        println!("✅ Family accuracy ≥ 99%: PASSED ({:.2}%)", 
                 100.0 * family_matches as f64 / total as f64);
    } else {
        println!("❌ Family accuracy ≥ 99%: FAILED ({:.2}%)", 
                 100.0 * family_matches as f64 / total as f64);
    }
    
    if family_matches > 0 {
        if value_within_01 >= (0.9 * family_matches as f64) as usize {
            println!("✅ Values within 0.1 ≥ 90%: PASSED ({:.1}%)", 
                     100.0 * value_within_01 as f64 / family_matches as f64);
        } else {
            println!("❌ Values within 0.1 ≥ 90%: FAILED ({:.1}%)", 
                     100.0 * value_within_01 as f64 / family_matches as f64);
        }
        
        if chroma_within_01 >= (0.85 * family_matches as f64) as usize {
            println!("✅ Chromas within 0.1 ≥ 85%: PASSED ({:.1}%)", 
                     100.0 * chroma_within_01 as f64 / family_matches as f64);
        } else {
            println!("❌ Chromas within 0.1 ≥ 85%: FAILED ({:.1}%)", 
                     100.0 * chroma_within_01 as f64 / family_matches as f64);
        }
    }
    
    if chromatic_count > 0 {
        if hue_within_01 >= (0.85 * chromatic_count as f64) as usize {
            println!("✅ Hues within 0.1 ≥ 85%: PASSED ({:.1}%)", 
                     100.0 * hue_within_01 as f64 / chromatic_count as f64);
        } else {
            println!("❌ Hues within 0.1 ≥ 85%: FAILED ({:.1}%)", 
                     100.0 * hue_within_01 as f64 / chromatic_count as f64);
        }
    }
    
    println!("\n{}", "=".repeat(70));
}