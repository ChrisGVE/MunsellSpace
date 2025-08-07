#!/usr/bin/env rust-script

use std::path::Path;

// Add the library path
use munsellspace::python_port::xyy_to_munsell_specification;

fn main() {
    // RGB (34, 17, 119) = #221177
    let rgb = [34.0 / 255.0, 17.0 / 255.0, 119.0 / 255.0];
    
    println!("=== DEBUGGING CHROMA CONVERGENCE ===");
    println!("Testing RGB ({}, {}, {}) = #221177", (rgb[0] * 255.0) as u8, 
             (rgb[1] * 255.0) as u8, (rgb[2] * 255.0) as u8);
    println!();
    
    // Convert to xyY
    // sRGB -> linear RGB
    let linear_rgb = [
        if rgb[0] <= 0.04045 { rgb[0] / 12.92 } else { ((rgb[0] + 0.055) / 1.055).powf(2.4) },
        if rgb[1] <= 0.04045 { rgb[1] / 12.92 } else { ((rgb[1] + 0.055) / 1.055).powf(2.4) },
        if rgb[2] <= 0.04045 { rgb[2] / 12.92 } else { ((rgb[2] + 0.055) / 1.055).powf(2.4) },
    ];
    
    // Linear RGB -> XYZ (using sRGB/ITU-R BT.709 matrix)
    let xyz = [
        0.4124564 * linear_rgb[0] + 0.3575761 * linear_rgb[1] + 0.1804375 * linear_rgb[2],
        0.2126729 * linear_rgb[0] + 0.7151522 * linear_rgb[1] + 0.0721750 * linear_rgb[2], 
        0.0193339 * linear_rgb[0] + 0.1191920 * linear_rgb[1] + 0.9503041 * linear_rgb[2],
    ];
    
    // XYZ -> xyY
    let sum = xyz[0] + xyz[1] + xyz[2];
    let xyy = if sum > 1e-10 {
        [xyz[0] / sum, xyz[1] / sum, xyz[1]]
    } else {
        // Handle black color
        [0.31006, 0.31616, xyz[1]] // Illuminant C
    };
    
    println!("xyY: ({:.6}, {:.6}, {:.6})", xyy[0], xyy[1], xyy[2]);
    
    // Call the function with debug output
    match xyy_to_munsell_specification(xyy) {
        Ok(spec) => {
            println!("Final specification: [{:.3}, {:.3}, {:.6}, {}]", 
                     spec[0], spec[1], spec[2], spec[3] as u8);
            println!("Final chroma: {:.6}", spec[2]);
        },
        Err(e) => println!("Error: {:?}", e),
    }
}