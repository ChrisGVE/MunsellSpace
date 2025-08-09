//! Debug convergence issues

use munsellspace::python_port::xyy_to_munsell_specification;

fn main() {
    // Test using the direct Python port function
    
    // Test cases that are failing
    let test_cases = vec![
        ("green", [0.3, 0.6, 0.715152]),
        // ("red", [0.64, 0.33, 0.212673]),
        // ("grey", [0.312727, 0.329023, 0.215861]),
    ];
    
    for (name, xyy) in test_cases {
        println!("\n=== Testing {} xyY {:?} ===", name, xyy);
        
        match xyy_to_munsell_specification(xyy) {
            Ok(spec) => {
                println!("Success: spec [{:.3}, {:.3}, {:.3}, {}]", 
                         spec[0], spec[1], spec[2], spec[3] as u8);
            }
            Err(e) => {
                println!("Error: {:?}", e);
            }
        }
    }
}