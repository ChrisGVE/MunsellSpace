// Debug RGB(187,255,153) chroma issue
use munsellspace::python_converter::PythonMunsellConverter;

fn main() {
    let converter = PythonMunsellConverter::new();
    
    println!("Testing RGB(187,255,153)");
    println!("Expected: 8.5GY 9.3/12.8");
    
    match converter.srgb_to_munsell([187, 255, 153]) {
        Ok(result) => {
            println!("Got:      {}", result);
            
            // Parse the result to get chroma
            let parts: Vec<&str> = result.split_whitespace().collect();
            if parts.len() == 2 {
                let value_chroma = parts[1];
                if let Some(chroma_str) = value_chroma.split('/').nth(1) {
                    if let Ok(chroma) = chroma_str.parse::<f64>() {
                        println!("Chroma difference: {:.2}", chroma - 12.8);
                    }
                }
            }
        }
        Err(e) => println!("Error: {}", e),
    }
}