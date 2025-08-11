use munsellspace::mathematical::MathematicalMunsellConverter;

fn main() {
    println!("Testing fully restored breakthrough mathematical.rs (commit cec13b2)\n");
    
    // The breakthrough version used D65 only (no illuminant configuration)
    let converter = MathematicalMunsellConverter::new().unwrap();
    
    // Test colors from the report
    let test_colors = [
        ([255, 181, 186], "vivid pink", "1.0R 8.0/6.6"),     // Python C result
        ([234, 147, 153], "strong pink", "1.6R 6.9/8.0"),    // Python C result
        ([228, 113, 122], "deep pink", "2.5R 6.0/10.7"),     // Python C result
    ];
    
    println!("Color             | Expected (Python) | Rust (restored)");
    println!("------------------|-------------------|------------------");
    
    for (rgb, name, python_result) in test_colors {
        let result = converter.srgb_to_munsell(rgb).unwrap();
        let rust_notation = format!("{:.1}{} {:.1}/{:.1}", 
            result.hue, result.family, result.value, result.chroma);
        
        println!("{:16} | {:17} | {}", name, python_result, rust_notation);
    }
    
    println!("\nNote: These should now be much closer to Python results with the restored formula");
}