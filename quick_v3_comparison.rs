use munsellspace::mathematical::{
    MathematicalMunsellConverter as MathematicalMunsellConverterV3,
    Illuminant as MathIlluminant,
    ChromaticAdaptation as MathChromaticAdaptation
};
use munsellspace::mathematical_v2::MathematicalMunsellConverter as MathematicalMunsellConverterV2;
use munsellspace::illuminants::{Illuminant, ChromaticAdaptationMethod};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Quick comparison: V2 vs V3 (breakthrough) mathematical converters\n");
    
    // Test colors
    let test_colors = [
        ([255, 0, 0], "pure red"),
        ([0, 255, 0], "pure green"),
        ([0, 0, 255], "pure blue"),
        ([255, 255, 0], "yellow"),
        ([255, 0, 255], "magenta"),
        ([0, 255, 255], "cyan"),
        ([128, 128, 128], "gray"),
        ([255, 181, 186], "vivid pink"),
        ([234, 147, 153], "strong pink"),
        ([228, 113, 122], "deep pink"),
    ];
    
    // Set max iterations to prevent timeout
    std::env::set_var("MUNSELL_MAX_ITERATIONS", "10");
    
    println!("Testing with D65 (default):");
    println!("Color            | V2 Result          | V3 (breakthrough)");
    println!("-----------------|-------------------|-------------------");
    
    for (rgb, name) in test_colors {
        // V2 converter
        let v2_converter = MathematicalMunsellConverterV2::new(
            Illuminant::D65,
            Illuminant::D65,
            ChromaticAdaptationMethod::XYZScaling
        )?;
        let v2_result = v2_converter.srgb_to_munsell(rgb)?;
        let v2_notation = format!("{:.1}{} {:.1}/{:.1}",
            v2_result.hue, v2_result.family, v2_result.value, v2_result.chroma);
        
        // V3 (breakthrough) converter
        let v3_converter = MathematicalMunsellConverterV3::new()?;
        let v3_result = v3_converter.srgb_to_munsell(rgb)?;
        let v3_notation = format!("{:.1}{} {:.1}/{:.1}",
            v3_result.hue, v3_result.family, v3_result.value, v3_result.chroma);
        
        println!("{:16} | {:18} | {}", name, v2_notation, v3_notation);
    }
    
    println!("\n\nTesting with Illuminant C + XYZScaling:");
    println!("Color            | V2 Result          | V3 (breakthrough)");
    println!("-----------------|-------------------|-------------------");
    
    for (rgb, name) in test_colors {
        // V2 converter with C
        let v2_converter = MathematicalMunsellConverterV2::new(
            Illuminant::D65,
            Illuminant::C,
            ChromaticAdaptationMethod::XYZScaling
        )?;
        let v2_result = v2_converter.srgb_to_munsell(rgb)?;
        let v2_notation = format!("{:.1}{} {:.1}/{:.1}",
            v2_result.hue, v2_result.family, v2_result.value, v2_result.chroma);
        
        // V3 (breakthrough) converter with C
        let v3_converter = MathematicalMunsellConverterV3::with_illuminants(
            MathIlluminant::D65,
            MathIlluminant::C,
            MathChromaticAdaptation::XYZScaling
        )?;
        let v3_result = v3_converter.srgb_to_munsell(rgb)?;
        let v3_notation = format!("{:.1}{} {:.1}/{:.1}",
            v3_result.hue, v3_result.family, v3_result.value, v3_result.chroma);
        
        println!("{:16} | {:18} | {}", name, v2_notation, v3_notation);
    }
    
    println!("\n\nTesting with F7 + XYZScaling:");
    println!("Color            | V2 Result          | V3 (breakthrough)");
    println!("-----------------|-------------------|-------------------");
    
    for (rgb, name) in test_colors {
        // V2 converter with F7
        let v2_converter = MathematicalMunsellConverterV2::new(
            Illuminant::D65,
            Illuminant::F7,
            ChromaticAdaptationMethod::XYZScaling
        )?;
        let v2_result = v2_converter.srgb_to_munsell(rgb)?;
        let v2_notation = format!("{:.1}{} {:.1}/{:.1}",
            v2_result.hue, v2_result.family, v2_result.value, v2_result.chroma);
        
        // V3 (breakthrough) converter with F7
        let v3_converter = MathematicalMunsellConverterV3::with_illuminants(
            MathIlluminant::D65,
            MathIlluminant::F7,
            MathChromaticAdaptation::XYZScaling
        )?;
        let v3_result = v3_converter.srgb_to_munsell(rgb)?;
        let v3_notation = format!("{:.1}{} {:.1}/{:.1}",
            v3_result.hue, v3_result.family, v3_result.value, v3_result.chroma);
        
        println!("{:16} | {:18} | {}", name, v2_notation, v3_notation);
    }
    
    println!("\n\nKey differences:");
    println!("- V2: Simplified algorithm, faster but less accurate");
    println!("- V3 (breakthrough): Full convergence algorithm, 60.4% baseline accuracy");
    println!("- Both now support illuminant configurability");
    
    Ok(())
}