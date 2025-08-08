fn main() {
    eprintln!("Test starting");
    
    // Just try to create a converter
    use munsellspace::python_converter::PythonMunsellConverter;
    let converter = PythonMunsellConverter::new();
    eprintln!("Converter created");
    
    // Try to call the method
    eprintln!("Calling srgb_to_munsell...");
    let result = converter.srgb_to_munsell([221, 238, 238]);
    eprintln!("Conversion returned");
    
    match result {
        Ok(munsell) => println!("Success: {}", munsell),
        Err(e) => println!("Error: {}", e),
    }
}