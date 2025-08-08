use munsellspace::python_converter::PythonMunsellConverter;

fn main() {
    // Redirect stderr to null to suppress trace output
    std::env::set_var("RUST_LOG", "");
    
    // Test a few colors
    let test_colors = vec![
        (221, 238, 238),  // 7.2G vs 7.1G issue
        (34, 17, 119),    // #221177 - PB color  
        (255, 0, 0),      // Pure red
        (0, 255, 0),      // Pure green
        (0, 0, 255),      // Pure blue
        (128, 128, 128),  // Gray
    ];
    
    let converter = PythonMunsellConverter::new();
    
    for (r, g, b) in test_colors {
        match converter.srgb_to_munsell([r, g, b]) {
            Ok(munsell) => {
                println!("RGB({},{},{}): {}", r, g, b, munsell);
            }
            Err(e) => {
                println!("RGB({},{},{}): Error: {}", r, g, b, e);
            }
        }
    }
}