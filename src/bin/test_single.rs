use munsellspace::python_converter::PythonMunsellConverter;
use std::env;

fn main() {
    // Get RGB from environment variable or use default
    let rgb_str = env::var("TEST_RGB").unwrap_or_else(|_| "221,238,238".to_string());
    let rgb_parts: Vec<u8> = rgb_str.split(',')
        .map(|s| s.trim().parse().unwrap_or(0))
        .collect();
    
    if rgb_parts.len() != 3 {
        println!("Error: Invalid RGB format");
        std::process::exit(1);
    }
    
    let rgb = [rgb_parts[0], rgb_parts[1], rgb_parts[2]];
    
    // Test the color
    let converter = PythonMunsellConverter::new();
    
    // Try to convert
    match converter.srgb_to_munsell(rgb) {
        Ok(munsell) => {
            println!("Success: {}", munsell);
            std::process::exit(0);
        }
        Err(e) => {
            println!("Error: {}", e);
            std::process::exit(1);
        }
    }
}