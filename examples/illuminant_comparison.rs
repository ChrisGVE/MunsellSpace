//! Compare Munsell conversion results under different viewing conditions
//! 
//! This example demonstrates how colors appear differently under various
//! lighting conditions, which is critical for color matching in different
//! environments (e.g., daylight vs. tungsten lighting).

use munsellspace::{Illuminant, ChromaticAdaptationMethod};
use munsellspace::mathematical_v2::{MathematicalMunsellConverter, MunsellConfig};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Test colors representing different scenarios
    let test_colors = vec![
        ([255, 0, 0], "Pure Red"),
        ([0, 255, 0], "Pure Green"),
        ([0, 0, 255], "Pure Blue"),
        ([255, 255, 0], "Yellow"),
        ([128, 128, 128], "Gray 50%"),
        ([255, 128, 0], "Orange"),
        ([128, 0, 128], "Purple"),
        ([255, 192, 203], "Pink"),
    ];
    
    // Common viewing conditions
    let viewing_conditions = vec![
        (Illuminant::D65, "Daylight (noon)"),
        (Illuminant::D50, "Daylight (horizon)"),
        (Illuminant::A, "Tungsten bulb"),
        (Illuminant::F2, "Cool white fluorescent"),
        (Illuminant::C, "Average daylight (Munsell standard)"),
    ];
    
    println!("MUNSELL COLOR APPEARANCE UNDER DIFFERENT ILLUMINANTS");
    println!("====================================================\n");
    
    for (rgb, name) in &test_colors {
        println!("{} RGB{:?}", name, rgb);
        println!("{:-<60}", "");
        
        for (illuminant, condition) in &viewing_conditions {
            let config = MunsellConfig {
                source_illuminant: Illuminant::D65,  // sRGB is defined in D65
                target_illuminant: *illuminant,
                adaptation_method: ChromaticAdaptationMethod::Bradford,
            };
            
            let converter = MathematicalMunsellConverter::with_config(config)?;
            
            match converter.srgb_to_munsell(*rgb) {
                Ok(munsell) => {
                    println!("{:25} → {:.1}{} {:.1}/{:.1}", 
                        condition,
                        munsell.hue, 
                        munsell.family, 
                        munsell.value, 
                        munsell.chroma
                    );
                }
                Err(e) => {
                    println!("{:25} → Error: {}", condition, e);
                }
            }
        }
        
        println!();
    }
    
    // Demonstrate the importance of illuminant specification
    println!("\nWHY ILLUMINANT MATTERS:");
    println!("========================\n");
    
    let rgb = [200, 150, 100]; // Beige/tan color
    println!("Testing a beige color RGB{:?} that shifts significantly:\n", rgb);
    
    // Configure for tungsten lighting
    let tungsten_config = MunsellConfig {
        source_illuminant: Illuminant::D65,
        target_illuminant: Illuminant::A,
        adaptation_method: ChromaticAdaptationMethod::Bradford,
    };
    
    let tungsten_converter = MathematicalMunsellConverter::with_config(tungsten_config)?;
    let tungsten_munsell = tungsten_converter.srgb_to_munsell(rgb)?;
    
    // Configure for daylight
    let daylight_config = MunsellConfig {
        source_illuminant: Illuminant::D65,
        target_illuminant: Illuminant::D65,
        adaptation_method: ChromaticAdaptationMethod::Bradford,
    };
    
    let daylight_converter = MathematicalMunsellConverter::with_config(daylight_config)?;
    let daylight_munsell = daylight_converter.srgb_to_munsell(rgb)?;
    
    println!("Under tungsten light (A):  {:.1}{} {:.1}/{:.1}", 
        tungsten_munsell.hue, tungsten_munsell.family, 
        tungsten_munsell.value, tungsten_munsell.chroma);
    
    println!("Under daylight (D65):      {:.1}{} {:.1}/{:.1}", 
        daylight_munsell.hue, daylight_munsell.family, 
        daylight_munsell.value, daylight_munsell.chroma);
    
    println!("\nNote how the same RGB color appears as different Munsell colors");
    println!("under different lighting conditions. This is why specifying the");
    println!("illuminant is crucial for accurate color communication!");
    
    Ok(())
}