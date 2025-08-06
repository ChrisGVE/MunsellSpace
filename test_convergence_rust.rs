use munsellspace::python_port::xyy_to_munsell_specification;

fn main() {
    // Test colors that were causing convergence issues
    let test_colors = [
        // Green (was causing family jump)
        ([0.3, 0.6, 0.715152], "9.9GY 8.7/19.4"),
        // Red (was causing oscillation)
        ([0.64007712, 0.3298325, 0.2126], "7.5R 5.2/18.5"),
        // Grey (should be achromatic)
        ([0.31006, 0.31616, 0.5], "N6.9"),
    ];
    
    println!("Rust convergence test:");
    println!("{}", "=".repeat(60));
    
    for (xyy, expected) in test_colors {
        match xyy_to_munsell_specification(xyy) {
            Ok(spec) => {
                if spec[0].is_nan() {
                    // Achromatic
                    println!("xyY {:?} -> N{:.1} (expected: {})", xyy, spec[1], expected);
                } else {
                    let hue_family = match spec[3] as u8 {
                        1 => "B", 2 => "BG", 3 => "G", 4 => "GY", 5 => "Y",
                        6 => "YR", 7 => "R", 8 => "RP", 9 => "P", 10 => "PB",
                        _ => "?"
                    };
                    println!("xyY {:?} -> {:.1}{} {:.1}/{:.1} (expected: {})", 
                             xyy, spec[0], hue_family, spec[1], spec[2], expected);
                }
            }
            Err(e) => {
                println!("xyY {:?} -> ERROR: {} (expected: {})", xyy, e, expected);
            }
        }
    }
}