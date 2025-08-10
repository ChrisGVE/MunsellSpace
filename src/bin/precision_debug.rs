
use munsellspace::python_converter::PythonMunsellConverter;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 4 {
        eprintln!("Usage: {} R G B", args[0]);
        std::process::exit(1);
    }
    
    let r: u8 = args[1].parse().unwrap();
    let g: u8 = args[2].parse().unwrap();
    let b: u8 = args[3].parse().unwrap();
    
    let converter = PythonMunsellConverter::new();
    
    // Get detailed conversion info
    let rgb_array = [r, g, b];
    println!("RGB input: [{}, {}, {}]", r, g, b);
    
    match converter.srgb_to_munsell(rgb_array) {
        Ok(munsell_str) => {
            println!("Munsell result: {}", munsell_str);
            
            // Try to get the specification
            match converter.srgb_to_specification(rgb_array) {
                Ok(spec) => {
                    println!("Specification: hue={:.6}, value={:.6}, chroma={:.6}, code={}", 
                             spec[0], spec[1], spec[2], spec[3] as u8);
                }
                Err(e) => {
                    println!("Could not get specification: {}", e);
                }
            }
        }
        Err(e) => {
            println!("Rust conversion failed: {}", e);
        }
    }
}
