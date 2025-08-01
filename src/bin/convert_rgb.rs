use munsellspace::MunsellConverter;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() != 4 {
        eprintln!("Usage: convert_rgb <r> <g> <b>");
        eprintln!("Example: convert_rgb 255 128 64");
        std::process::exit(1);
    }
    
    let r: u8 = match args[1].parse() {
        Ok(val) => val,
        Err(_) => {
            eprintln!("ERROR: Invalid R value: {}", args[1]);
            std::process::exit(1);
        }
    };
    
    let g: u8 = match args[2].parse() {
        Ok(val) => val,
        Err(_) => {
            eprintln!("ERROR: Invalid G value: {}", args[2]);
            std::process::exit(1);
        }
    };
    
    let b: u8 = match args[3].parse() {
        Ok(val) => val,
        Err(_) => {
            eprintln!("ERROR: Invalid B value: {}", args[3]);
            std::process::exit(1);
        }
    };
    
    let converter = match MunsellConverter::new() {
        Ok(converter) => converter,
        Err(e) => {
            eprintln!("ERROR: Failed to create converter: {}", e);
            std::process::exit(1);
        }
    };
    
    match converter.srgb_to_munsell([r, g, b]) {
        Ok(munsell) => {
            println!("{}", munsell.to_string());
        }
        Err(e) => {
            eprintln!("ERROR: Conversion failed: {}", e);
            std::process::exit(1);
        }
    }
}