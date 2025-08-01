use munsellspace::MunsellConverter;
use std::fs::File;
use std::io::Write;

#[test]
fn analyze_munsell_conversion_bias() {
    println!("=== MUNSELL CONVERSION BIAS ANALYSIS ===");
    println!("Comparing our conversions against 4007-color reference table to detect systematic shifts");
    
    let converter = MunsellConverter::new().expect("Failed to create converter");
    
    // Load our reference dataset
    let csv_content = include_str!("../ISCC_NBS_REFERENCE_DATASET.csv");
    let mut reader = csv::Reader::from_reader(csv_content.as_bytes());
    
    // Load the 4007-color reference table
    println!("Loading 4007-color reference table...");
    let reference_colors = load_4007_reference_table(&converter);
    println!("Loaded {} reference colors", reference_colors.len());
    
    // Create output CSV for detailed analysis
    let mut output_file = File::create("munsell_bias_analysis.csv").expect("Failed to create output file");
    writeln!(output_file, "hex_color,r,g,b,our_munsell,our_hue_num,our_hue_family,our_value,our_chroma,closest_rgb_r,closest_rgb_g,closest_rgb_b,closest_munsell,closest_hue_num,closest_hue_family,closest_value,closest_chroma,hue_diff_circular,value_diff,chroma_diff,rgb_distance").expect("Failed to write header");
    
    let mut hue_differences = Vec::new();
    let mut value_differences = Vec::new();
    let mut chroma_differences = Vec::new();
    let mut rgb_distances = Vec::new();
    
    let mut processed = 0;
    
    for result in reader.records() {
        let record = result.expect("Failed to read CSV record");
        
        let hex = record.get(0).expect("Missing hex").trim();
        let (r, g, b) = match hex_to_rgb_components(hex) {
            Ok(components) => components,
            Err(_) => continue,
        };
        
        // Convert with our system
        let our_munsell = match converter.srgb_to_munsell([r, g, b]) {
            Ok(munsell) => munsell,
            Err(_) => continue,
        };
        
        // Find closest color in 4007-color table
        let closest = find_closest_reference_color([r, g, b], &reference_colors);
        
        // Parse our Munsell notation
        let (our_hue_num, our_hue_family, our_value, our_chroma) = parse_munsell_components(&our_munsell.to_string());
        let (ref_hue_num, ref_hue_family, ref_value, ref_chroma) = parse_munsell_components(&closest.munsell);
        
        // Calculate differences
        let hue_diff = calculate_circular_hue_difference(our_hue_num, &our_hue_family, ref_hue_num, &ref_hue_family);
        let value_diff = our_value - ref_value;
        let chroma_diff = our_chroma - ref_chroma;
        let rgb_distance = calculate_rgb_distance([r, g, b], closest.rgb);
        
        // Store for statistics
        hue_differences.push(hue_diff);
        value_differences.push(value_diff);
        chroma_differences.push(chroma_diff);
        rgb_distances.push(rgb_distance);
        
        // Write to CSV
        writeln!(output_file, "{},{},{},{},{},{},{},{:.1},{:.1},{},{},{},{},{},{},{:.1},{:.1},{:.2},{:.2},{:.2},{:.1}",
            hex, r, g, b, our_munsell, our_hue_num, our_hue_family, our_value, our_chroma,
            closest.rgb[0], closest.rgb[1], closest.rgb[2], closest.munsell,
            ref_hue_num, ref_hue_family, ref_value, ref_chroma,
            hue_diff, value_diff, chroma_diff, rgb_distance
        ).expect("Failed to write");
        
        processed += 1;
        if processed % 50 == 0 {
            println!("  Processed {}/267 colors...", processed);
        }
    }
    
    println!("\n=== STATISTICAL ANALYSIS RESULTS ===");
    
    // Hue analysis
    let hue_mean = hue_differences.iter().sum::<f64>() / hue_differences.len() as f64;
    let hue_std = calculate_std_dev(&hue_differences, hue_mean);
    println!("HUE ANALYSIS (circular coordinate system):");
    println!("  Mean difference: {:.2} hue points", hue_mean);
    println!("  Std deviation: {:.2} hue points", hue_std);
    println!("  Range: {:.2} to {:.2}", 
        hue_differences.iter().fold(f64::INFINITY, |a, &b| a.min(b)),
        hue_differences.iter().fold(f64::NEG_INFINITY, |a, &b| a.max(b)));
    
    if hue_mean.abs() > 2.0 {
        println!("  ⚠️  SYSTEMATIC HUE BIAS DETECTED: {:.2} points", hue_mean);
        if hue_mean > 0.0 {
            println!("     Our system calculates hues {} points higher than reference", hue_mean);
        } else {
            println!("     Our system calculates hues {} points lower than reference", hue_mean.abs());
        }
    } else {
        println!("  ✅ No significant hue bias detected");
    }
    
    // Value analysis
    let value_mean = value_differences.iter().sum::<f64>() / value_differences.len() as f64;
    let value_std = calculate_std_dev(&value_differences, value_mean);
    println!("\nVALUE ANALYSIS:");
    println!("  Mean difference: {:.2} value points", value_mean);
    println!("  Std deviation: {:.2} value points", value_std);
    println!("  Range: {:.2} to {:.2}", 
        value_differences.iter().fold(f64::INFINITY, |a, &b| a.min(b)),
        value_differences.iter().fold(f64::NEG_INFINITY, |a, &b| a.max(b)));
    
    if value_mean.abs() > 0.3 {
        println!("  ⚠️  SYSTEMATIC VALUE BIAS DETECTED: {:.2} points", value_mean);
        if value_mean > 0.0 {
            println!("     Our system calculates values {} points higher than reference", value_mean);
        } else {
            println!("     Our system calculates values {} points lower than reference", value_mean.abs());
        }
    } else {
        println!("  ✅ No significant value bias detected");
    }
    
    // Chroma analysis
    let chroma_mean = chroma_differences.iter().sum::<f64>() / chroma_differences.len() as f64;
    let chroma_std = calculate_std_dev(&chroma_differences, chroma_mean);
    println!("\nCHROMA ANALYSIS:");
    println!("  Mean difference: {:.2} chroma points", chroma_mean);
    println!("  Std deviation: {:.2} chroma points", chroma_std);
    println!("  Range: {:.2} to {:.2}", 
        chroma_differences.iter().fold(f64::INFINITY, |a, &b| a.min(b)),
        chroma_differences.iter().fold(f64::NEG_INFINITY, |a, &b| a.max(b)));
    
    if chroma_mean.abs() > 0.5 {
        println!("  ⚠️  SYSTEMATIC CHROMA BIAS DETECTED: {:.2} points", chroma_mean);
        if chroma_mean > 0.0 {
            println!("     Our system calculates chroma {} points higher than reference", chroma_mean);
        } else {
            println!("     Our system calculates chroma {} points lower than reference", chroma_mean.abs());
        }
    } else {
        println!("  ✅ No significant chroma bias detected");
    }
    
    // RGB distance analysis
    let rgb_mean = rgb_distances.iter().sum::<f64>() / rgb_distances.len() as f64;
    let rgb_std = calculate_std_dev(&rgb_distances, rgb_mean);
    println!("\nRGB DISTANCE ANALYSIS:");
    println!("  Mean RGB distance to closest reference: {:.1}", rgb_mean);
    println!("  Std deviation: {:.1}", rgb_std);
    println!("  This indicates how close our test colors are to reference table entries");
    
    println!("\n=== SPECIFIC EXAMPLES FROM YOUR ANALYSIS ===");
    analyze_specific_examples(&converter, &reference_colors);
    
    println!("\n=== RECOMMENDATIONS ===");
    if hue_mean.abs() > 2.0 || value_mean.abs() > 0.3 || chroma_mean.abs() > 0.5 {
        println!("SYSTEMATIC BIASES DETECTED - Consider calibration adjustment:");
        if hue_mean.abs() > 2.0 {
            println!("  - Hue bias: {} points", hue_mean);
        }
        if value_mean.abs() > 0.3 {
            println!("  - Value bias: {} points", value_mean);
        }
        if chroma_mean.abs() > 0.5 {
            println!("  - Chroma bias: {} points", chroma_mean);
        }
    } else {
        println!("✅ No significant systematic biases detected");
        println!("The conversion differences may be due to:");
        println!("  - Individual color variations within tolerance");
        println!("  - Different measurement conditions");
        println!("  - Rounding differences in the datasets");
    }
    
    println!("\nDetailed analysis saved to: munsell_bias_analysis.csv");
}

#[derive(Debug, Clone)]
struct ReferenceColor {
    rgb: [u8; 3],
    munsell: String,
}

fn load_4007_reference_table(_converter: &MunsellConverter) -> Vec<ReferenceColor> {
    // Load the actual 4007-color reference table
    let csv_content = include_str!("../tests/data/srgb-to-munsell.csv");
    let mut reader = csv::Reader::from_reader(csv_content.as_bytes());
    
    let mut reference_colors = Vec::new();
    
    for result in reader.records() {
        let record = result.expect("Failed to read reference CSV record");
        
        // Parse: R, G, B, Munsell Colour
        let r: u8 = record.get(0).expect("Missing R").trim().parse().expect("Invalid R");
        let g: u8 = record.get(1).expect("Missing G").trim().parse().expect("Invalid G");
        let b: u8 = record.get(2).expect("Missing B").trim().parse().expect("Invalid B");
        let munsell = record.get(3).expect("Missing Munsell").trim().to_string();
        
        reference_colors.push(ReferenceColor {
            rgb: [r, g, b],
            munsell,
        });
    }
    
    reference_colors
}

fn find_closest_reference_color(target_rgb: [u8; 3], reference_colors: &[ReferenceColor]) -> ReferenceColor {
    reference_colors.iter()
        .min_by_key(|color| calculate_rgb_distance(target_rgb, color.rgb) as i32)
        .unwrap()
        .clone()
}

fn calculate_rgb_distance(rgb1: [u8; 3], rgb2: [u8; 3]) -> f64 {
    let dr = rgb1[0] as f64 - rgb2[0] as f64;
    let dg = rgb1[1] as f64 - rgb2[1] as f64;
    let db = rgb1[2] as f64 - rgb2[2] as f64;
    (dr * dr + dg * dg + db * db).sqrt()
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

fn calculate_circular_hue_difference(hue1: f64, family1: &str, hue2: f64, family2: &str) -> f64 {
    // Convert to 100-point circular coordinate system
    let families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
    
    let family1_idx = families.iter().position(|&f| f == family1).unwrap_or(0) as f64;
    let family2_idx = families.iter().position(|&f| f == family2).unwrap_or(0) as f64;
    
    let pos1 = family1_idx * 10.0 + hue1;
    let pos2 = family2_idx * 10.0 + hue2;
    
    // Calculate shortest circular distance
    let diff = (pos1 - pos2).abs();
    if diff > 50.0 {
        100.0 - diff
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

fn analyze_specific_examples(converter: &MunsellConverter, reference_colors: &[ReferenceColor]) {
    let examples = [
        ("#ffb5ba", [255, 181, 186], "Your analysis: closest should be (255, 187, 187) -> 6.8R 8.2/5.2"),
        ("#ea9399", [234, 147, 153], "Your analysis: closest should be (238, 153, 153) -> 6.0R 7.1/7.1"),
        ("#ead8d7", [234, 216, 215], "Your analysis: closest should be (221, 221, 221) -> 8.4GY 8.8/0.8"),
    ];
    
    for (hex, rgb, note) in &examples {
        println!("\nExample: {} {:?}", hex, rgb);
        println!("  {}", note);
        
        if let Ok(our_munsell) = converter.srgb_to_munsell(*rgb) {
            println!("  Our conversion: {}", our_munsell);
            let closest = find_closest_reference_color(*rgb, reference_colors);
            println!("  Closest reference: {:?} -> {}", closest.rgb, closest.munsell);
            println!("  RGB distance: {:.1}", calculate_rgb_distance(*rgb, closest.rgb));
        }
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