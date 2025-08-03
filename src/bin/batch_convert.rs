use munsellspace::mathematical::MathematicalMunsellConverter;
use std::io::{self, BufRead};

fn main() {
    // Disable debug output
    std::env::set_var("RUST_LOG", "error");
    
    let converter = match MathematicalMunsellConverter::new() {
        Ok(c) => c,
        Err(e) => {
            eprintln!("Failed to create converter: {}", e);
            return;
        }
    };
    
    let stdin = io::stdin();
    
    for line in stdin.lock().lines() {
        let line = line.unwrap();
        let parts: Vec<&str> = line.trim().split(',').collect();
        
        if parts.len() != 3 {
            println!("ERROR: Invalid input");
            continue;
        }
        
        let r: u8 = parts[0].parse().unwrap_or(0);
        let g: u8 = parts[1].parse().unwrap_or(0);
        let b: u8 = parts[2].parse().unwrap_or(0);
        
        match converter.srgb_to_munsell([r, g, b]) {
            Ok(spec) => {
                // Format the Munsell notation
                if spec.chroma == 0.0 {
                    println!("N {:.1}", spec.value);
                } else {
                    println!("{:.1}{} {:.1}/{:.1}", spec.hue, spec.family, spec.value, spec.chroma);
                }
            },
            Err(_) => println!("ERROR"),
        }
    }
}