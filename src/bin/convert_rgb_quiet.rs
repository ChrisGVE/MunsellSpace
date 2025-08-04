//! Binary for testing mathematical Munsell conversion (quiet mode)
//! 
//! This binary uses the new mathematical implementation without debug output

use munsellspace::mathematical::MathematicalMunsellConverter;
use std::env;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    
    if args.len() != 4 {
        eprintln!("Usage: {} <R> <G> <B>", args[0]);
        eprintln!("  R, G, B: RGB values (0-255)");
        std::process::exit(1);
    }

    let r: u8 = args[1].parse()?;
    let g: u8 = args[2].parse()?;
    let b: u8 = args[3].parse()?;

    // Disable all debug output
    std::env::set_var("MUNSELL_NO_DEBUG", "1");
    
    let converter = MathematicalMunsellConverter::new()?;
    let munsell_spec = converter.srgb_to_munsell([r, g, b])?;
    let notation = converter.format_munsell_notation(&munsell_spec);
    
    println!("{}", notation);
    
    Ok(())
}