use munsellspace::python_converter::PythonMunsellConverter;

fn main() {
    let converter = PythonMunsellConverter::new();
    
    // Test a simple color that should work
    println!("Testing RGB(128, 128, 128) - should be grey");
    let rgb = [128u8, 128u8, 128u8];
    match converter.srgb_to_munsell(rgb) {
        Ok(munsell) => println!("Result: {}", munsell),
        Err(e) => println!("Error: {}", e),
    }
    
    // Test a primary color
    println!("\nTesting RGB(255, 0, 0) - should be red");
    let rgb = [255u8, 0u8, 0u8];
    match converter.srgb_to_munsell(rgb) {
        Ok(munsell) => println!("Result: {}", munsell),
        Err(e) => println!("Error: {}", e),
    }
    
    // Test the problematic color
    println!("\nTesting RGB(221, 238, 238) - should be 7.5BG 9.277/2.085");
    let rgb = [221u8, 238u8, 238u8];
    match converter.srgb_to_munsell(rgb) {
        Ok(munsell) => println!("Result: {}", munsell),
        Err(e) => println!("Error: {}", e),
    }
}