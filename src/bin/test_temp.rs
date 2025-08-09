
use munsellspace::python_converter::PythonMunsellConverter;

fn main() {
    let converter = PythonMunsellConverter::new();
    let rgb = [0u8, 68u8, 170u8];
    match converter.srgb_to_munsell(rgb) {
        Ok(munsell) => println!("{}", munsell),
        Err(e) => eprintln!("ERROR: {}", e),
    }
}
