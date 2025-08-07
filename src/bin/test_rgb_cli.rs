//! Simple command-line test for RGB to Munsell conversion

use munsellspace::python_port::*;
use munsellspace::python_port_strings::*;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() != 4 {
        eprintln!("Usage: {} R G B", args[0]);
        std::process::exit(1);
    }
    
    let r: u8 = args[1].parse().expect("Invalid R value");
    let g: u8 = args[2].parse().expect("Invalid G value");
    let b: u8 = args[3].parse().expect("Invalid B value");
    
    // Convert to sRGB (0-1 range)
    let srgb = [r as f64 / 255.0, g as f64 / 255.0, b as f64 / 255.0];
    
    // sRGB to XYZ using D65 illuminant
    let xyz = srgb_to_xyz_d65(srgb);
    
    // XYZ to xyY
    let xyy = xyz_to_xyy(xyz);
    
    // xyY to Munsell specification
    match xyy_to_munsell_specification(xyy) {
        Ok(spec) => {
            // Convert specification to Munsell notation string
            // Use default decimals: 1 for hue, 1 for value, 1 for chroma
            match munsell_specification_to_munsell_colour(&spec, 1, 1, 1) {
                Ok(notation) => println!("Munsell: {}", notation),
                Err(_) => {
                    // Fallback formatting if the string function fails
                    if spec[0].is_nan() {
                        println!("Munsell: N{:.1}", spec[1]);
                    } else {
                        let code = spec[3] as u8;
                        let family = match code {
                            1 => "B", 2 => "BG", 3 => "G", 4 => "GY", 5 => "Y",
                            6 => "YR", 7 => "R", 8 => "RP", 9 => "P", 10 => "PB",
                            _ => "?"
                        };
                        println!("Munsell: {:.1}{} {:.1}/{:.1}", spec[0], family, spec[1], spec[2]);
                    }
                }
            }
        }
        Err(e) => {
            eprintln!("Error: {:?}", e);
            std::process::exit(1);
        }
    }
}

// Helper functions
fn srgb_to_xyz_d65(srgb: [f64; 3]) -> [f64; 3] {
    // Gamma correction
    let linear: Vec<f64> = srgb.iter().map(|&c| {
        if c <= 0.04045 {
            c / 12.92
        } else {
            ((c + 0.055) / 1.055).powf(2.4)
        }
    }).collect();
    
    // sRGB to XYZ matrix (D65)
    [
        0.4124564 * linear[0] + 0.3575761 * linear[1] + 0.1804375 * linear[2],
        0.2126729 * linear[0] + 0.7151522 * linear[1] + 0.0721750 * linear[2],
        0.0193339 * linear[0] + 0.1191920 * linear[1] + 0.9503041 * linear[2],
    ]
}

fn xyz_to_xyy(xyz: [f64; 3]) -> [f64; 3] {
    let sum = xyz[0] + xyz[1] + xyz[2];
    if sum < 1e-10 {
        [0.3127, 0.3290, 0.0]  // D65 white point for black
    } else {
        [xyz[0] / sum, xyz[1] / sum, xyz[1]]
    }
}