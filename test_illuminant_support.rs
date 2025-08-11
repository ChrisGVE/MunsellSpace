use munsellspace::mathematical::{
    MathematicalMunsellConverter, 
    Illuminant, 
    ChromaticAdaptation
};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Testing illuminant support in restored breakthrough mathematical.rs\n");
    
    // Test colors from previous testing
    let test_colors = [
        ([255, 181, 186], "vivid pink"),
        ([234, 147, 153], "strong pink"),
        ([228, 113, 122], "deep pink"),
        ([255, 0, 0], "pure red"),
        ([0, 255, 0], "pure green"),
        ([0, 0, 255], "pure blue"),
    ];
    
    // Test with different illuminants
    let illuminants = [
        (Illuminant::D65, "D65"),
        (Illuminant::C, "C"),
        (Illuminant::F7, "F7"),
    ];
    
    // Test with XYZScaling adaptation (winner from investigation)
    let adaptation = ChromaticAdaptation::XYZScaling;
    
    println!("Testing with XYZScaling chromatic adaptation:");
    println!("Color            | Illuminant | Munsell Result");
    println!("-----------------|------------|------------------");
    
    for (rgb, name) in test_colors {
        for (illuminant, illum_name) in &illuminants {
            // Create converter with D65 -> target illuminant
            let converter = MathematicalMunsellConverter::with_illuminants(
                Illuminant::D65,
                *illuminant,
                adaptation
            )?;
            
            let result = converter.srgb_to_munsell(rgb)?;
            let notation = format!("{:.1}{} {:.1}/{:.1}", 
                result.hue, result.family, result.value, result.chroma);
            
            println!("{:16} | {:10} | {}", name, illum_name, notation);
        }
        println!("-----------------|------------|------------------");
    }
    
    println!("\nTesting that D65->D65 produces same results as default:");
    let default_converter = MathematicalMunsellConverter::new()?;
    let d65_converter = MathematicalMunsellConverter::with_illuminants(
        Illuminant::D65,
        Illuminant::D65,
        ChromaticAdaptation::Bradford
    )?;
    
    for (rgb, name) in test_colors {
        let default_result = default_converter.srgb_to_munsell(rgb)?;
        let d65_result = d65_converter.srgb_to_munsell(rgb)?;
        
        let default_notation = format!("{:.1}{} {:.1}/{:.1}", 
            default_result.hue, default_result.family, default_result.value, default_result.chroma);
        let d65_notation = format!("{:.1}{} {:.1}/{:.1}", 
            d65_result.hue, d65_result.family, d65_result.value, d65_result.chroma);
        
        if default_notation == d65_notation {
            println!("{:16}: ✅ Same ({}))", name, default_notation);
        } else {
            println!("{:16}: ❌ Different - Default: {} vs D65->D65: {}", 
                name, default_notation, d65_notation);
        }
    }
    
    Ok(())
}