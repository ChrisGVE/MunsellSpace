//! Test simple colors to debug the Python port

use munsellspace::python_port::*;

fn main() {
    println!("Testing simple colors with Python port...\n");
    
    // Test exact xyY values from Python
    let test_xyy = [
        ([0.640000, 0.330000, 0.212673], "red"),
        ([0.185539, 0.187939, 0.054654], "2.9PB reference"),
        ([0.312727, 0.329023, 0.215861], "grey 128"),
        ([0.300000, 0.600000, 0.715152], "green"),
        ([0.150000, 0.060000, 0.072175], "blue"),
    ];
    
    println!("Testing exact xyY values from Python:\n");
    
    for (xyy, name) in test_xyy.iter() {
        println!("Testing {} xyY {:?}:", name, xyy);
        
        match xyy_to_munsell_specification(*xyy) {
            Ok(spec) => {
                println!("  Raw spec: hue={:.3}, value={:.3}, chroma={:.3}, code={}", 
                         spec[0], spec[1], spec[2], spec[3] as u8);
                
                // Compare with Python output
                match name {
                    &"red" => println!("  Python: hue=7.939, value=5.221, chroma=20.443, code=7"),
                    &"2.9PB reference" => println!("  Python: hue=2.899, value=2.771, chroma=7.032, code=10"),
                    &"grey 128" => println!("  Python: hue=7.737, value=5.255, chroma=0.658, code=4"),
                    &"green" => println!("  Python: hue=9.919, value=8.747, chroma=19.382, code=4"),
                    _ => {}
                }
                
                let notation = format_munsell_notation(spec);
                println!("  Our notation: {}", notation);
            }
            Err(e) => {
                println!("  Error: {:?}", e);
            }
        }
        println!();
    }
    
    println!("\nOriginal RGB color tests:\n");
    
    // Test colors
    let test_colors = [
        ([0, 0, 0], "black"),
        ([255, 255, 255], "white"), 
        ([128, 128, 128], "grey"),
        ([255, 0, 0], "red"),
        ([0, 255, 0], "green"),
        ([0, 0, 255], "blue"),
        ([0, 68, 119], "reference 2.9PB 2.8/7.0"),
    ];
    
    for (rgb, name) in test_colors.iter() {
        println!("Testing {} {:?}:", name, rgb);
        
        // Convert to xyY
        let rgb_f = [rgb[0] as f64 / 255.0, rgb[1] as f64 / 255.0, rgb[2] as f64 / 255.0];
        let xyz = srgb_to_xyz_d65(rgb_f);
        let xyy = xyz_to_xyy(xyz);
        
        println!("  xyY: [{:.6}, {:.6}, {:.6}]", xyy[0], xyy[1], xyy[2]);
        
        // Try to convert to Munsell
        match xyy_to_munsell_specification(xyy) {
            Ok(spec) => {
                println!("  Raw spec: hue={:.2}, value={:.2}, chroma={:.2}, code={}", 
                         spec[0], spec[1], spec[2], spec[3] as u8);
                
                // Try to format it
                let notation = format_munsell_notation(spec);
                println!("  Notation: {}", notation);
            }
            Err(e) => {
                println!("  Error: {:?}", e);
            }
        }
        println!();
    }
}

// Helper functions
fn srgb_to_xyz_d65(rgb: [f64; 3]) -> [f64; 3] {
    // Apply gamma correction
    let linear: Vec<f64> = rgb.iter().map(|&c| {
        if c <= 0.04045 {
            c / 12.92
        } else {
            ((c + 0.055) / 1.055).powf(2.4)
        }
    }).collect();
    
    // sRGB to XYZ matrix (D65 illuminant)
    let matrix = [
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ];
    
    [
        matrix[0][0] * linear[0] + matrix[0][1] * linear[1] + matrix[0][2] * linear[2],
        matrix[1][0] * linear[0] + matrix[1][1] * linear[1] + matrix[1][2] * linear[2],
        matrix[2][0] * linear[0] + matrix[2][1] * linear[1] + matrix[2][2] * linear[2],
    ]
}

fn xyz_to_xyy(xyz: [f64; 3]) -> [f64; 3] {
    let sum = xyz[0] + xyz[1] + xyz[2];
    if sum.abs() < 1e-10 {
        // Return D65 white point for black
        [0.31271, 0.32902, 0.0]
    } else {
        [xyz[0] / sum, xyz[1] / sum, xyz[1]]
    }
}

fn format_munsell_notation(spec: [f64; 4]) -> String {
    let hue = spec[0];
    let value = spec[1];
    let chroma = spec[2];
    let code = spec[3] as u8;
    
    // Handle neutral
    if hue.is_nan() || chroma < 0.01 {
        if value == 0.0 {
            return "N 0.0".to_string();
        } else {
            return format!("N {:.1}/", value);
        }
    }
    
    // Convert code to family using Python's mapping
    let family = match code {
        1 => "B",
        2 => "BG",
        3 => "G",
        4 => "GY",
        5 => "Y",
        6 => "YR",
        7 => "R",
        8 => "RP",
        9 => "P",
        10 => "PB",
        _ => "?",
    };
    
    format!("{:.1}{} {:.1}/{:.1}", hue, family, value, chroma)
}