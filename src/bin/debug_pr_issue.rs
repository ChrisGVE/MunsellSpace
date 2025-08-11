use munsellspace::mathematical::MathematicalMunsellConverter;
use munsellspace::illuminants::{Illuminant, ChromaticAdaptationMethod};

fn main() {
    // Test the first few colors to find which one causes "PR"
    let test_colors = vec![
        ([255, 255, 255], "white"),
        ([0, 0, 0], "black"),
        ([255, 0, 0], "red"),
        ([0, 255, 0], "green"),
        ([0, 0, 255], "blue"),
        // Add more if needed
    ];
    
    for (rgb, name) in test_colors {
        println!("Testing {}: RGB {:?}", name, rgb);
        
        match MathematicalMunsellConverter::with_illuminants(
            Illuminant::D65,
            Illuminant::A,
            ChromaticAdaptationMethod::Bradford,
        ) {
            Ok(converter) => {
                match converter.srgb_to_munsell(rgb) {
                    Ok(munsell) => {
                        println!("  Result: {:.1}{} {:.1}/{:.1}", 
                            munsell.hue, munsell.family, munsell.value, munsell.chroma);
                    },
                    Err(e) => {
                        println!("  Error: {}", e);
                    }
                }
            },
            Err(e) => {
                println!("  Converter error: {}", e);
            }
        }
    }
}