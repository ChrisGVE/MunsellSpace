use munsellspace::python_converter::PythonMunsellConverter;

fn main() {
    // Test RGB(221, 238, 238) which should give chroma 2.084
    let converter = PythonMunsellConverter::new();
    let rgb = [221u8, 238u8, 238u8];
    
    println!("Testing RGB(221, 238, 238)");
    println!("Expected: 7.5BG 9.277364/2.084771");
    
    match converter.srgb_to_munsell(rgb) {
        Ok(munsell) => {
            println!("Actual:   {}", munsell);
            
            // Extract values for comparison
            let notation = munsell.to_string();
            if let Some(slash_pos) = notation.find('/') {
                if let Some(space_pos) = notation.rfind(' ') {
                    let value_str = &notation[space_pos+1..slash_pos];
                    let chroma_str = &notation[slash_pos+1..];
                    
                    if let Ok(value) = value_str.parse::<f64>() {
                        if let Ok(chroma) = chroma_str.parse::<f64>() {
                            println!("\nValue:  {:.6} (expected: 9.277364)", value);
                            println!("Chroma: {:.6} (expected: 2.084771)", chroma);
                            
                            let value_diff = (value - 9.277364).abs();
                            let chroma_diff = (chroma - 2.084771).abs();
                            
                            println!("\nValue difference:  {:.6}", value_diff);
                            println!("Chroma difference: {:.6}", chroma_diff);
                            
                            if value_diff <= 0.1 && chroma_diff <= 0.1 {
                                println!("✓ Within tolerance!");
                            } else {
                                println!("✗ Outside tolerance");
                            }
                        }
                    }
                }
            }
        }
        Err(e) => {
            println!("Error: {}", e);
        }
    }
}