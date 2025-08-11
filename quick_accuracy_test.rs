use munsellspace::mathematical::{
    MathematicalMunsellConverter, 
    Illuminant, 
    ChromaticAdaptation
};
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Quick accuracy test with restored breakthrough version\n");
    
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
    
    // Test default configuration (should maintain 60.4% accuracy)
    let converter = MathematicalMunsellConverter::new()?;
    
    // Sample every 10th color for speed
    let sample_size = 400;
    let step = reference_data.len() / sample_size;
    
    let mut exact_matches = 0;
    let mut family_matches = 0;
    let mut colors_tested = 0;
    
    for i in (0..reference_data.len()).step_by(step) {
        let (rgb, expected) = &reference_data[i];
        
        // Set a timeout environment variable for convergence
        std::env::set_var("MUNSELL_MAX_ITERATIONS", "10");
        
        let result = converter.srgb_to_munsell(*rgb)?;
        let notation = format!("{:.1}{} {:.1}/{:.1}", 
            result.hue, result.family, result.value, result.chroma);
        
        colors_tested += 1;
        
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
        
        // Print progress every 50 colors
        if colors_tested % 50 == 0 {
            print!(".");
            use std::io::{self, Write};
            io::stdout().flush().unwrap();
        }
    }
    println!();
    
    let exact_pct = (exact_matches as f64 / colors_tested as f64) * 100.0;
    let family_pct = (family_matches as f64 / colors_tested as f64) * 100.0;
    
    println!("\nColors tested: {} (sampled from {})", colors_tested, reference_data.len());
    println!("Exact matches: {}/{} ({:.1}%)", exact_matches, colors_tested, exact_pct);
    println!("Family matches: {}/{} ({:.1}%)", family_matches, colors_tested, family_pct);
    
    println!("\n=== Testing with different illuminants ===");
    
    // Test a few colors with different illuminants
    let test_colors = [
        ([255, 0, 0], "pure red"),
        ([0, 255, 0], "pure green"),
        ([0, 0, 255], "pure blue"),
        ([255, 255, 0], "yellow"),
        ([128, 128, 128], "gray"),
    ];
    
    for (rgb, name) in test_colors {
        println!("\n{} RGB{:?}:", name, rgb);
        
        // D65 (default)
        let d65_converter = MathematicalMunsellConverter::new()?;
        let d65_result = d65_converter.srgb_to_munsell(rgb)?;
        println!("  D65: {:.1}{} {:.1}/{:.1}", 
            d65_result.hue, d65_result.family, d65_result.value, d65_result.chroma);
        
        // Illuminant C with XYZScaling
        let c_converter = MathematicalMunsellConverter::with_illuminants(
            Illuminant::D65,
            Illuminant::C,
            ChromaticAdaptation::XYZScaling
        )?;
        let c_result = c_converter.srgb_to_munsell(rgb)?;
        println!("  C:   {:.1}{} {:.1}/{:.1}", 
            c_result.hue, c_result.family, c_result.value, c_result.chroma);
        
        // Check if they differ
        let hue_diff = (d65_result.hue - c_result.hue).abs();
        let value_diff = (d65_result.value - c_result.value).abs();
        let chroma_diff = (d65_result.chroma - c_result.chroma).abs();
        
        if hue_diff > 0.1 || value_diff > 0.1 || chroma_diff > 0.1 {
            println!("  ✅ Illuminant adaptation is working (differences detected)");
        } else {
            println!("  ⚠️ No significant difference between illuminants");
        }
    }
    
    if exact_pct >= 55.0 && exact_pct <= 65.0 {
        println!("\n✅ SUCCESS: Accuracy is in expected range (~60.4%) for breakthrough version!");
    } else {
        println!("\n⚠️ WARNING: Accuracy {:.1}% is outside expected range (55-65%)", exact_pct);
    }
    
    Ok(())
}