use munsellspace::ISCC_NBS_Classifier;
use std::collections::{HashMap, HashSet};
use std::time::Instant;

fn format_with_thousands(n: u64) -> String {
    let s = n.to_string();
    let mut result = String::new();
    for (i, c) in s.chars().rev().enumerate() {
        if i > 0 && i % 3 == 0 {
            result.push('\'');
        }
        result.push(c);
    }
    result.chars().rev().collect()
}

fn main() {
    println!("🔬 Full ISCC-NBS Coverage Test (0.001 increments)");
    println!("==================================================\n");
    
    let classifier = match ISCC_NBS_Classifier::new() {
        Ok(c) => c,
        Err(e) => {
            eprintln!("Failed to initialize classifier: {}", e);
            return;
        }
    };
    
    // Define excluded values - every 0.5 from 0.5 to 10.0
    let excluded_values: HashSet<i32> = [
        500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 
        5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 
        9000, 9500, 10000
    ].iter().cloned().collect();
    
    // Define excluded chromas
    let excluded_chromas: HashSet<i32> = {
        let mut set = HashSet::new();
        // 0.5, 0.7, 1.0, 1.2, 1.5
        set.extend([500, 700, 1000, 1200, 1500]);
        // 2.0 through 50.0 (all integers from 2 to 50)
        for i in 2..=50 {
            set.insert(i * 1000);
        }
        set
    };
    
    println!("Test range: Value [0, 10] × Chroma [0, 17] with 0.001 increments");
    println!("Excluding boundary values:");
    println!("  Values: 0.5, 1.0, 1.5, ..., 9.5, 10.0");
    println!("  Chromas: 0.5, 0.7, 1.0, 1.2, 1.5, 2.0, 3.0, ..., 17.0");
    
    // Count valid test points
    let mut valid_values: u64 = 0;
    for v in 0..=10000 {
        if !excluded_values.contains(&v) {
            valid_values += 1;
        }
    }
    
    let mut valid_chromas: u64 = 0;
    for c in 0..=17000 {
        if !excluded_chromas.contains(&c) {
            valid_chromas += 1;
        }
    }
    
    let points_per_wedge = valid_values * valid_chromas;
    let total_points = points_per_wedge * 100;
    
    println!("\nValid test points: {} values × {} chromas = {} per wedge",
             format_with_thousands(valid_values), 
             format_with_thousands(valid_chromas), 
             format_with_thousands(points_per_wedge));
    println!("Total for 100 wedges: {} points", format_with_thousands(total_points));
    println!("\nThis will take several minutes. Starting scan...\n");
    
    let start_time = Instant::now();
    
    // Track gaps and overlaps
    let mut gaps_by_wedges: HashMap<Vec<String>, Vec<(f64, f64)>> = HashMap::new();
    let mut overlaps_by_colors: HashMap<(u16, u16), HashMap<String, Vec<(f64, f64)>>> = HashMap::new();
    
    let wedge_families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
    let wedge_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    
    let mut total_points_tested: u64 = 0;
    let mut total_gaps: u64 = 0;
    let mut total_overlaps: u64 = 0;
    let mut wedges_processed = 0;
    
    for family in &wedge_families {
        for &wedge_num in &wedge_numbers {
            let test_hue = if wedge_num == 1 {
                format!("0.5{}", family)
            } else if wedge_num == 10 {
                format!("9.5{}", family)
            } else {
                format!("{}.5{}", wedge_num - 1, family)
            };
            
            let wedge_ref = format!("{}{}", wedge_num, family);
            
            // Scan through value and chroma space
            for value_i in 0..=10000 {  // 0.000 to 10.000
                if excluded_values.contains(&value_i) {
                    continue;
                }
                
                let value = value_i as f64 / 1000.0;
                
                for chroma_i in 0..=17000 {  // 0.000 to 17.000
                    if excluded_chromas.contains(&chroma_i) {
                        continue;
                    }
                    
                    let chroma = chroma_i as f64 / 1000.0;
                    
                    total_points_tested += 1;
                    
                    // Find all colors at this point
                    let colors = classifier.find_all_colors_at_point(&test_hue, value, chroma)
                        .unwrap_or_default();
                    
                    if colors.is_empty() {
                        // Gap detected
                        total_gaps += 1;
                        let key = vec![wedge_ref.clone()];
                        gaps_by_wedges.entry(key)
                            .or_insert_with(Vec::new)
                            .push((value, chroma));
                    } else if colors.len() > 1 {
                        // Overlap detected
                        total_overlaps += 1;
                        let mut sorted_colors = colors.clone();
                        sorted_colors.sort();
                        let color_pair = (sorted_colors[0], sorted_colors[1]);
                        
                        overlaps_by_colors
                            .entry(color_pair)
                            .or_insert_with(HashMap::new)
                            .entry(wedge_ref.clone())
                            .or_insert_with(Vec::new)
                            .push((value, chroma));
                    }
                }
            }
            
            wedges_processed += 1;
            if wedges_processed % 10 == 0 {
                let elapsed = start_time.elapsed().as_secs();
                println!("Processed {}/100 wedges ({} seconds elapsed)...", 
                         wedges_processed, elapsed);
            }
        }
    }
    
    let total_time = start_time.elapsed();
    println!("\nScan complete in {:.1} seconds!", total_time.as_secs_f64());
    println!("Tested {} points total\n", format_with_thousands(total_points_tested));
    
    // Consolidate gaps across wedges
    let mut consolidated_gaps: HashMap<String, Vec<String>> = HashMap::new();
    for (wedges, points) in &gaps_by_wedges {
        for (v, c) in points {
            let point_key = format!("({:.3}/{:.3})", v, c);
            for wedge in wedges {
                consolidated_gaps.entry(point_key.clone())
                    .or_insert_with(Vec::new)
                    .push(wedge.clone());
            }
        }
    }
    
    // Group gaps by wedge combinations
    let mut gap_groups: HashMap<Vec<String>, Vec<String>> = HashMap::new();
    for (point, mut wedges) in consolidated_gaps {
        wedges.sort();
        gap_groups.entry(wedges)
            .or_insert_with(Vec::new)
            .push(point);
    }
    
    // Report gaps
    println!("GAPS DETECTED:");
    println!("--------------");
    
    if gap_groups.is_empty() {
        println!("  ✅ No gaps found!");
    } else {
        for (wedges, mut points) in gap_groups {
            points.sort();
            
            // Find rectangular regions for gaps
            let rectangles = find_gap_rectangles(&points);
            
            println!("\nGap in wedges: {:?}", wedges);
            println!("  Total points: {}", points.len());
            
            if rectangles.len() == 1 {
                let rect = &rectangles[0];
                println!("  Rectangle: {} to {}", rect.0, rect.1);
            } else if rectangles.len() <= 5 {
                println!("  {} rectangular regions:", rectangles.len());
                for rect in &rectangles {
                    println!("    {} to {}", rect.0, rect.1);
                }
            } else {
                println!("  {} rectangular regions (showing first 5):", rectangles.len());
                for rect in rectangles.iter().take(5) {
                    println!("    {} to {}", rect.0, rect.1);
                }
            }
        }
        println!("\nTotal gap points: {}", format_with_thousands(total_gaps));
    }
    
    // Report overlaps
    println!("\n\nOVERLAPS DETECTED:");
    println!("-----------------");
    
    if overlaps_by_colors.is_empty() {
        println!("  ✅ No overlaps found!");
    } else {
        for ((color1, color2), wedges_map) in overlaps_by_colors {
            let wedges: Vec<String> = wedges_map.keys().cloned().collect();
            let all_points: Vec<(f64, f64)> = wedges_map.values()
                .flat_map(|v| v.iter().cloned())
                .collect();
            
            let unique_points: HashSet<String> = all_points.iter()
                .map(|(v, c)| format!("({:.3}/{:.3})", v, c))
                .collect();
            
            println!("\nColors [{}, {}] overlap in wedges: {:?}", 
                     color1, color2, wedges);
            println!("  Total overlap points: {}", unique_points.len());
            
            if unique_points.len() <= 10 {
                let mut sorted_points: Vec<_> = unique_points.into_iter().collect();
                sorted_points.sort();
                for point in sorted_points {
                    println!("    {}", point);
                }
            } else {
                // Show summary for large overlaps
                let min_v = all_points.iter().map(|(v, _)| *v).fold(f64::INFINITY, f64::min);
                let max_v = all_points.iter().map(|(v, _)| *v).fold(f64::NEG_INFINITY, f64::max);
                let min_c = all_points.iter().map(|(_, c)| *c).fold(f64::INFINITY, f64::min);
                let max_c = all_points.iter().map(|(_, c)| *c).fold(f64::NEG_INFINITY, f64::max);
                
                println!("  Bounds: V[{:.3}, {:.3}] × C[{:.3}, {:.3}]", 
                         min_v, max_v, min_c, max_c);
            }
        }
        println!("\nTotal overlap points: {}", format_with_thousands(total_overlaps));
    }
    
    println!("\n✅ Full coverage test complete");
    println!("   Points tested: {}", format_with_thousands(total_points_tested));
    println!("   Points with gaps: {}", format_with_thousands(total_gaps));
    println!("   Points with overlaps: {}", format_with_thousands(total_overlaps));
    println!("   Test duration: {:.1} seconds", total_time.as_secs_f64());
}

fn find_gap_rectangles(points: &[String]) -> Vec<(String, String)> {
    // Parse points and find bounding rectangles
    // This is a simplified version - just finds overall bounds
    if points.is_empty() {
        return vec![];
    }
    
    let parsed: Vec<(f64, f64)> = points.iter()
        .filter_map(|p| {
            // Parse "(value/chroma)" format
            let p = p.trim_start_matches('(').trim_end_matches(')');
            let parts: Vec<&str> = p.split('/').collect();
            if parts.len() == 2 {
                if let (Ok(v), Ok(c)) = (parts[0].parse::<f64>(), parts[1].parse::<f64>()) {
                    return Some((v, c));
                }
            }
            None
        })
        .collect();
    
    if parsed.is_empty() {
        return vec![];
    }
    
    let min_v = parsed.iter().map(|(v, _)| *v).fold(f64::INFINITY, f64::min);
    let max_v = parsed.iter().map(|(v, _)| *v).fold(f64::NEG_INFINITY, f64::max);
    let min_c = parsed.iter().map(|(_, c)| *c).fold(f64::INFINITY, f64::min);
    let max_c = parsed.iter().map(|(_, c)| *c).fold(f64::NEG_INFINITY, f64::max);
    
    vec![(
        format!("({:.3}/{:.3})", min_v, min_c),
        format!("({:.3}/{:.3})", max_v, max_c)
    )]
}