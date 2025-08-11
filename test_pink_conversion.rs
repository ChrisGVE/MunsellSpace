use munsellspace::mathematical::MathematicalMunsellConverter;
use munsellspace::illuminants::{Illuminant, ChromaticAdaptationMethod};

fn main() {
    // Test with D65 (default)
    let converter_d65 = MathematicalMunsellConverter::new().unwrap();
    
    // Test with Illuminant C
    let converter_c = MathematicalMunsellConverter::with_illuminants(
        Illuminant::D65,
        Illuminant::C,
        ChromaticAdaptationMethod::XYZScaling,
    ).unwrap();
    
    // Test vivid pink #FFB5BA - should be around 1.0R per Python
    let rgb = [255, 181, 186];
    
    println!("Vivid pink #FFB5BA:");
    let result_d65 = converter_d65.srgb_to_munsell(rgb).unwrap();
    println!("  Rust D65: {:.1}{} {:.1}/{:.1}", result_d65.hue, result_d65.family, result_d65.value, result_d65.chroma);
    
    let result_c = converter_c.srgb_to_munsell(rgb).unwrap();
    println!("  Rust C:   {:.1}{} {:.1}/{:.1}", result_c.hue, result_c.family, result_c.value, result_c.chroma);
    println!("  Python C: 1.0R 8.0/6.6");
    println!();
    
    // Test strong pink #EA9399 - should be around 1.6R per Python
    let rgb2 = [234, 147, 153];
    println!("Strong pink #EA9399:");
    let result2_d65 = converter_d65.srgb_to_munsell(rgb2).unwrap();
    println!("  Rust D65: {:.1}{} {:.1}/{:.1}", result2_d65.hue, result2_d65.family, result2_d65.value, result2_d65.chroma);
    
    let result2_c = converter_c.srgb_to_munsell(rgb2).unwrap();
    println!("  Rust C:   {:.1}{} {:.1}/{:.1}", result2_c.hue, result2_c.family, result2_c.value, result2_c.chroma);
    println!("  Python C: 1.6R 6.9/8.0");
}