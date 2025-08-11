use munsellspace::mathematical::{
    MathematicalMunsellConverter, 
    Illuminant, 
    ChromaticAdaptation
};
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Testing illuminant accuracy with reference dataset\n");
    
    // Load reference dataset
    let file = File::open("tests/data/srgb-to-munsell.csv")?;
    let reader = BufReader::new(file);
    
    let mut reference_data = Vec::new();
    for line in reader.lines().skip(1) {
        let line = line?;
        let parts: Vec<&str> = line.split(',').collect();
        if parts.len() >= 4 {
            let r = parts[0].trim().parse::<u8>().unwrap_or(0);
            let g = parts[1].trim().parse::<u8>().unwrap_or(0);
            let b = parts[2].trim().parse::<u8>().unwrap_or(0);
            let munsell = parts[3].trim().to_string();
            reference_data.push(([r, g, b], munsell));
        }
    }
    
    println!("Loaded {} reference colors", reference_data.len());
    
    // Test configurations
    let configs = [
        (Illuminant::D65, ChromaticAdaptation::Bradford, "D65/Bradford"),
        (Illuminant::D65, ChromaticAdaptation::XYZScaling, "D65/XYZScaling"),
        (Illuminant::C, ChromaticAdaptation::XYZScaling, "C/XYZScaling"),
        (Illuminant::F7, ChromaticAdaptation::XYZScaling, "F7/XYZScaling"),
    ];
    
    for (illuminant, adaptation, name) in configs {
        println!("\nTesting {}", name);
        
        let converter = if illuminant == Illuminant::D65 && adaptation == ChromaticAdaptation::Bradford {
            // Use default for D65/Bradford
            MathematicalMunsellConverter::new()?
        } else {
            MathematicalMunsellConverter::with_illuminants(
                Illuminant::D65,
                illuminant,
                adaptation
            )?
        };
        
        let mut exact_matches = 0;
        let mut family_matches = 0;
        let mut within_0_1_value = 0;
        let mut within_0_1_chroma = 0;
        let mut within_0_5_hue = 0;
        
        // Test first 100 colors for quick check
        for (rgb, expected) in reference_data.iter().take(100) {
            let result = converter.srgb_to_munsell(*rgb)?;
            let notation = format!("{:.1}{} {:.1}/{:.1}", 
                result.hue, result.family, result.value, result.chroma);
            
            // Check exact match
            if notation == *expected {
                exact_matches += 1;
            }
            
            // Parse expected for component comparison
            if let Some(space_pos) = expected.find(' ') {
                let hue_part = &expected[..space_pos];
                let value_chroma = &expected[space_pos+1..];
                
                // Extract family from expected
                let expected_family = hue_part.chars()
                    .skip_while(|c| c.is_numeric() || *c == '.')
                    .collect::<String>();
                
                if result.family == expected_family {
                    family_matches += 1;
                }
                
                // Parse value/chroma
                if let Some(slash_pos) = value_chroma.find('/') {
                    if let Ok(expected_value) = value_chroma[..slash_pos].parse::<f64>() {
                        if (result.value - expected_value).abs() <= 0.1 {
                            within_0_1_value += 1;
                        }
                    }
                    if let Ok(expected_chroma) = value_chroma[slash_pos+1..].parse::<f64>() {
                        if (result.chroma - expected_chroma).abs() <= 0.1 {
                            within_0_1_chroma += 1;
                        }
                    }
                }
                
                // Parse hue
                let expected_hue_str = hue_part.chars()
                    .take_while(|c| c.is_numeric() || *c == '.')
                    .collect::<String>();
                if let Ok(expected_hue) = expected_hue_str.parse::<f64>() {
                    if (result.hue - expected_hue).abs() <= 0.5 {
                        within_0_5_hue += 1;
                    }
                }
            }
        }
        
        println!("  Exact matches: {}/100 ({}%)", exact_matches, exact_matches);
        println!("  Family matches: {}/100 ({}%)", family_matches, family_matches);
        println!("  Value within 0.1: {}/100 ({}%)", within_0_1_value, within_0_1_value);
        println!("  Chroma within 0.1: {}/100 ({}%)", within_0_1_chroma, within_0_1_chroma);
        println!("  Hue within 0.5: {}/100 ({}%)", within_0_5_hue, within_0_5_hue);
    }
    
    // Now test the full dataset with default configuration to verify 60.4% accuracy
    println!("\n=== Full dataset test with default configuration (D65/Bradford) ===");
    let converter = MathematicalMunsellConverter::new()?;
    
    let mut exact_matches = 0;
    let mut family_matches = 0;
    
    for (rgb, expected) in &reference_data {
        let result = converter.srgb_to_munsell(*rgb)?;
        let notation = format!("{:.1}{} {:.1}/{:.1}", 
            result.hue, result.family, result.value, result.chroma);
        
        if notation == *expected {
            exact_matches += 1;
        }
        
        // Extract family from expected
        if let Some(space_pos) = expected.find(' ') {
            let hue_part = &expected[..space_pos];
            let expected_family = hue_part.chars()
                .skip_while(|c| c.is_numeric() || *c == '.')
                .collect::<String>();
            
            if result.family == expected_family {
                family_matches += 1;
            }
        }
    }
    
    let total = reference_data.len();
    let exact_pct = (exact_matches as f64 / total as f64) * 100.0;
    let family_pct = (family_matches as f64 / total as f64) * 100.0;
    
    println!("Total colors tested: {}", total);
    println!("Exact matches: {}/{} ({:.1}%)", exact_matches, total, exact_pct);
    println!("Family matches: {}/{} ({:.1}%)", family_matches, total, family_pct);
    
    if exact_pct >= 60.0 && exact_pct <= 61.0 {
        println!("\n✅ SUCCESS: Maintained ~60.4% accuracy from breakthrough version!");
    } else if exact_pct < 60.0 {
        println!("\n⚠️ WARNING: Accuracy dropped below 60.4% - illuminant changes may have affected the formula");
    } else {
        println!("\n🎉 IMPROVED: Accuracy increased above expected 60.4%!");
    }
    
    Ok(())
}