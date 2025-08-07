
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
    match converter.srgb_to_munsell([r, g, b]) {
        Ok(munsell) => {
            println!("{}", munsell);
        }
        Err(e) => {
            println!("Error: {}", e);
        }
    }
}
