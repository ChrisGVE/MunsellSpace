use munsellspace::iscc::ISCC_NBS_Classifier;
use std::collections::HashMap;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔍 ISCC-NBS Wedge Coverage Test");
    println!("================================");
    println!("Testing for gaps and overlaps in the ISCC-NBS color space\n");
    
    // Initialize classifier
    let classifier = ISCC_NBS_Classifier::new()?;
    
    // Define test grid
    let values: Vec<f64> = (0..=20)
        .map(|i| i as f64 * 0.5)
        .collect();
    
    let chromas = vec![
        0.0, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0,
        5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0,
        16.0, 17.0, 18.0, 19.0, 20.0
    ];
    
    // Create the 100 wedge references
    let families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
    let mut wedge_refs = Vec::new();
    
    for family in &families {
        for hue_num in 1..=10 {
            wedge_refs.push(format!("{}{}", hue_num, family));
        }
    }
    
    // Track issues by grid point
    let mut gaps_by_point: HashMap<(String, String), Vec<String>> = HashMap::new();
    let mut overlaps_by_point: HashMap<(String, String), Vec<String>> = HashMap::new();
    
    // Test each wedge
    for wedge_ref in &wedge_refs {
        // Extract the hue number and family
        let (hue_num_str, family) = if let Some(pos) = wedge_ref.find(|c: char| c.is_alphabetic()) {
            wedge_ref.split_at(pos)
        } else {
            continue; // Skip if we can't parse
        };
        
        let hue_num: f64 = hue_num_str.parse().unwrap_or(1.0);
        
        // For wedge N, use a hue clearly inside that wedge's range
        // Wedge 1R: use 0.5R (in [0,1])
        // Wedge 2R: use 1.5R (in (1,2])
        // Wedge 3R: use 2.5R (in (2,3])
        // Wedge 10R: use 9.5R (in (9,10])
        // etc.
        let test_hue_num = if hue_num == 1.0 {
            0.5  // For wedge 1, use 0.5 which is in [0,1]
        } else if hue_num == 10.0 {
            9.5  // For wedge 10, use 9.5 which is in (9,10]
        } else {
            hue_num - 0.5  // For wedges 2-9, use N-0.5 which is in (N-1,N]
        };
        
        let test_hue = format!("{}{}", test_hue_num, family);
        
        for &value in &values {
            for &chroma in &chromas {
                // Get all colors that match this point
                let colors = classifier.find_all_colors_at_point(&test_hue, value, chroma)?;
                
                let point_key = (format!("{:.1}", value), format!("{:.1}", chroma));
                
                if colors.is_empty() {
                    // Track gap
                    gaps_by_point.entry(point_key)
                        .or_insert_with(Vec::new)
                        .push(wedge_ref.clone());
                } else if colors.len() > 1 {
                    // Track overlap
                    let overlap_info = format!("{} [{}]", wedge_ref, colors.iter().map(|c| c.to_string()).collect::<Vec<_>>().join(", "));
                    overlaps_by_point.entry(point_key)
                        .or_insert_with(Vec::new)
                        .push(overlap_info);
                }
                // If exactly one color found, no output (as requested)
            }
        }
    }
    
    // Output results grouped by issue type
    
    // Report gaps
    if !gaps_by_point.is_empty() {
        println!("GAPS DETECTED:");
        println!("--------------");
        for ((value, chroma), wedges) in &gaps_by_point {
            if wedges.len() == 1 {
                println!("({}/{}) - Gap in wedge: {}", value, chroma, wedges[0]);
            } else {
                println!("({}/{}) - Gap in wedges: [{}]", value, chroma, wedges.join(", "));
            }
        }
        println!();
    }
    
    // Report overlaps - group by unique color combinations
    if !overlaps_by_point.is_empty() {
        println!("OVERLAPS DETECTED:");
        println!("-----------------");
        
        // Group overlaps by the actual color numbers involved
        let mut overlap_groups: HashMap<String, Vec<(String, String, Vec<String>)>> = HashMap::new();
        
        for ((value, chroma), overlap_infos) in &overlaps_by_point {
            // Extract the color numbers from the first overlap info (they should all be the same for this point)
            if let Some(first_info) = overlap_infos.first() {
                if let Some(bracket_start) = first_info.find('[') {
                    let color_part = &first_info[bracket_start..];
                    
                    // Extract just the wedge names
                    let wedges: Vec<String> = overlap_infos.iter()
                        .map(|info| {
                            if let Some(space_pos) = info.find(' ') {
                                info[..space_pos].to_string()
                            } else {
                                info.clone()
                            }
                        })
                        .collect();
                    
                    overlap_groups.entry(color_part.to_string())
                        .or_insert_with(Vec::new)
                        .push((value.clone(), chroma.clone(), wedges));
                }
            }
        }
        
        // Output grouped overlaps
        for (colors, points) in &overlap_groups {
            println!("Colors {}", colors);
            for (value, chroma, wedges) in points {
                if wedges.len() == 1 {
                    println!("  ({}/{}) in wedge: {}", value, chroma, wedges[0]);
                } else {
                    println!("  ({}/{}) in wedges: [{}]", value, chroma, wedges.join(", "));
                }
            }
        }
        println!();
    }
    
    // Test neutral colors separately
    println!("NEUTRAL (N) COLORS:");
    println!("------------------");
    let mut neutral_gaps = Vec::new();
    let mut neutral_overlaps = Vec::new();
    
    for &value in &values {
        // For neutral colors, chroma should be 0, but let's test with the first few chromas
        for &chroma in &[0.0, 0.4, 0.5] {
            // Test neutral classification
            let colors = classifier.find_all_colors_at_point("N", value, chroma)?;
            
            if colors.is_empty() {
                neutral_gaps.push(format!("({:.1}/{:.1}) - Gap", value, chroma));
            } else if colors.len() > 1 {
                let color_nums: Vec<String> = colors.iter().map(|c| c.to_string()).collect();
                neutral_overlaps.push(format!("({:.1}/{:.1}) - [{}]", value, chroma, color_nums.join(", ")));
            }
        }
    }
    
    if !neutral_gaps.is_empty() {
        println!("Gaps:");
        for gap in &neutral_gaps {
            println!("  {}", gap);
        }
    }
    
    if !neutral_overlaps.is_empty() {
        println!("Overlaps:");
        for overlap in &neutral_overlaps {
            println!("  {}", overlap);
        }
    }
    
    if neutral_gaps.is_empty() && neutral_overlaps.is_empty() {
        println!("  No issues detected");
    }
    
    println!("\n✅ Coverage test complete");
    
    Ok(())
}