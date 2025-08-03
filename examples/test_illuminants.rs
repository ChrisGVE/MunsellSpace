//! Test the mathematical Munsell converter with different illuminants

use munsellspace::{Illuminant, ChromaticAdaptationMethod};
use munsellspace::mathematical_v2::{MathematicalMunsellConverter, MunsellConfig};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Test RGB color
    let rgb = [128, 64, 192]; // Purple color
    
    println!("Testing RGB {:?} with different illuminants\n", rgb);
    println!("{:-<80}", "");
    
    // Test with default configuration (D65 → C, Bradford)
    let converter_default = MathematicalMunsellConverter::new()?;
    let munsell_default = converter_default.srgb_to_munsell(rgb)?;
    println!("Default (D65 → C, Bradford):");
    println!("  Munsell: {:.1}{} {:.1}/{:.1}", 
        munsell_default.hue, munsell_default.family, 
        munsell_default.value, munsell_default.chroma);
    
    println!("\n{:-<80}", "");
    
    // Test with different target illuminants
    let illuminants = [
        Illuminant::A,
        Illuminant::C,
        Illuminant::D50,
        Illuminant::D65,
        Illuminant::E,
        Illuminant::F2,
    ];
    
    println!("Different target illuminants (source: D65, method: Bradford):\n");
    
    for target in &illuminants {
        let config = MunsellConfig {
            source_illuminant: Illuminant::D65,
            target_illuminant: *target,
            adaptation_method: ChromaticAdaptationMethod::Bradford,
        };
        
        let converter = MathematicalMunsellConverter::with_config(config)?;
        let munsell = converter.srgb_to_munsell(rgb)?;
        
        println!("{:6} → {:3}: {:.1}{} {:.1}/{:.1}", 
            "D65", target.name(),
            munsell.hue, munsell.family, 
            munsell.value, munsell.chroma);
    }
    
    println!("\n{:-<80}", "");
    
    // Test with different adaptation methods
    let methods = [
        ChromaticAdaptationMethod::XYZScaling,
        ChromaticAdaptationMethod::VonKries,
        ChromaticAdaptationMethod::Bradford,
        ChromaticAdaptationMethod::CAT02,
    ];
    
    println!("Different adaptation methods (D65 → C):\n");
    
    for method in &methods {
        let config = MunsellConfig {
            source_illuminant: Illuminant::D65,
            target_illuminant: Illuminant::C,
            adaptation_method: *method,
        };
        
        let converter = MathematicalMunsellConverter::with_config(config)?;
        let munsell = converter.srgb_to_munsell(rgb)?;
        
        println!("{:12}: {:.1}{} {:.1}/{:.1}", 
            format!("{:?}", method),
            munsell.hue, munsell.family, 
            munsell.value, munsell.chroma);
    }
    
    println!("\n{:-<80}", "");
    
    // Test round-trip conversion
    println!("Round-trip test (Munsell → RGB → Munsell):\n");
    
    let converter = MathematicalMunsellConverter::new()?;
    let munsell1 = converter.srgb_to_munsell(rgb)?;
    println!("Original RGB: {:?}", rgb);
    println!("→ Munsell: {:.1}{} {:.1}/{:.1}", 
        munsell1.hue, munsell1.family, munsell1.value, munsell1.chroma);
    
    let rgb2 = converter.munsell_to_srgb(&munsell1)?;
    println!("→ RGB: {:?}", rgb2);
    
    let munsell2 = converter.srgb_to_munsell(rgb2)?;
    println!("→ Munsell: {:.1}{} {:.1}/{:.1}", 
        munsell2.hue, munsell2.family, munsell2.value, munsell2.chroma);
    
    let diff = [
        (rgb[0] as i32 - rgb2[0] as i32).abs(),
        (rgb[1] as i32 - rgb2[1] as i32).abs(),
        (rgb[2] as i32 - rgb2[2] as i32).abs(),
    ];
    println!("\nRGB difference: {:?}", diff);
    
    Ok(())
}