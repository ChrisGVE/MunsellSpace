//! Test BG colors that are failing to converge

use munsellspace::python_port::xyy_to_munsell_specification;

fn main() {
    // Test BG colors that are failing
    let test_cases = vec![
        ([0.216740, 0.300235, 0.323373], "9.6BG 6.3/7.9"),
        ([0.218390, 0.306176, 0.578859], "9.6BG 8.0/9.4"),
        ([0.217379, 0.302534, 0.399003], "9.5BG 6.8/8.5"),
        ([0.218798, 0.307643, 0.683691], "9.7BG 8.6/9.5"),
        ([0.215979, 0.297495, 0.256847], "9.6BG 5.7/7.2"),
    ];
    
    for (xyy, expected) in test_cases {
        println!("\nTesting xyY [{:.6}, {:.6}, {:.6}] (expected {})", 
                 xyy[0], xyy[1], xyy[2], expected);
        
        match xyy_to_munsell_specification(xyy) {
            Ok(spec) => {
                let hue_codes = ["", "R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
                let code = spec[3] as usize;
                let family = if code > 0 && code <= 10 { hue_codes[code] } else { "?" };
                
                if spec[2] < 0.05 {
                    println!("  Result: N{:.1}", spec[1]);
                } else {
                    println!("  Result: {:.1}{} {:.1}/{:.1}", spec[0], family, spec[1], spec[2]);
                }
                
                // Check if it matches expected
                let formatted = if spec[2] < 0.05 {
                    format!("N{:.1}", spec[1])
                } else {
                    format!("{:.1}{} {:.1}/{:.1}", spec[0], family, spec[1], spec[2])
                };
                
                if formatted == expected {
                    println!("  ✓ Match!");
                } else {
                    println!("  ✗ Mismatch");
                }
            }
            Err(e) => {
                println!("  Error: {:?}", e);
            }
        }
    }
}