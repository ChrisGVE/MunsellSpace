//! Detailed trace of convergence algorithm

use munsellspace::python_port::*;
use munsellspace::python_port_helpers;

fn main() {
    let rgb = [221u8, 238u8, 238u8];
    println!("Testing RGB({}, {}, {})", rgb[0], rgb[1], rgb[2]);
    
    // Convert to xyY
    let rgb_norm = [rgb[0] as f64 / 255.0, rgb[1] as f64 / 255.0, rgb[2] as f64 / 255.0];
    
    // Linearize
    let mut rgb_linear = [0.0; 3];
    for i in 0..3 {
        let c = rgb_norm[i];
        rgb_linear[i] = if c <= 0.04045 {
            c / 12.92
        } else {
            ((c + 0.055) / 1.055).powf(2.4)
        };
    }
    
    // Convert to XYZ (unscaled)
    let matrix = [
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ];
    
    let xyz = [
        matrix[0][0] * rgb_linear[0] + matrix[0][1] * rgb_linear[1] + matrix[0][2] * rgb_linear[2],
        matrix[1][0] * rgb_linear[0] + matrix[1][1] * rgb_linear[1] + matrix[1][2] * rgb_linear[2],
        matrix[2][0] * rgb_linear[0] + matrix[2][1] * rgb_linear[1] + matrix[2][2] * rgb_linear[2],
    ];
    
    // Convert to xyY
    let sum = xyz[0] + xyz[1] + xyz[2];
    let xyy = [xyz[0] / sum, xyz[1] / sum, xyz[1]];
    
    println!("Input xyY: [{:.10}, {:.10}, {:.10}]", xyy[0], xyy[1], xyy[2]);
    
    // Get Lab for initial guess
    let xyz_to_convert = python_port_helpers::xyy_to_xyz(xyy);
    let lab = python_port_helpers::xyz_to_lab(xyz_to_convert, [0.31006, 0.31616]);
    println!("Lab: [{:.6}, {:.6}, {:.6}]", lab[0], lab[1], lab[2]);
    
    // Convert to LCHab
    let lchab = python_port_helpers::lab_to_lchab(lab);
    println!("LCHab: L={:.6}, C={:.6}, H={:.6}", lchab[0], lchab[1], lchab[2]);
    
    // Get initial hue
    let (hue_initial, code_initial) = hue_angle_to_hue(lchab[2]);
    println!("Initial hue from angle {:.3}: {:.3}, code={}", lchab[2], hue_initial, code_initial);
    
    // Get value
    let value = munsell_value_astmd1535(xyy[2] * 100.0);
    println!("Value from Y={:.6}: {:.6}", xyy[2], value);
    
    // Scale chroma
    let chroma_initial = lchab[1] * 0.2;
    println!("Initial chroma estimate: {:.3}", chroma_initial);
    
    // Now run the actual convergence
    println!("\n--- Starting Convergence ---");
    match xyy_to_munsell_specification(xyy) {
        Ok(spec) => {
            println!("Final specification: [{:.6}, {:.6}, {:.6}, {}]", 
                     spec[0], spec[1], spec[2], spec[3] as u8);
            
            // Format as notation
            let hue = spec[0];
            let value = spec[1];
            let chroma = spec[2];
            let code = spec[3] as u8;
            
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
            
            println!("\nFinal notation: {:.1}{} {:.1}/{:.1}", hue, family, value, chroma);
            println!("Reference:      7.1G 9.3/2.1");
            
            // Test reverse conversion
            println!("\n--- Reverse Check ---");
            let ref_spec = [7.1, 9.3, 2.1, 3.0];
            match munsell_specification_to_xyy(&ref_spec) {
                Ok(ref_xyy) => {
                    println!("Reference xyY: [{:.10}, {:.10}, {:.10}]", 
                             ref_xyy[0], ref_xyy[1], ref_xyy[2]);
                    
                    println!("\nInput xy:     [{:.10}, {:.10}]", xyy[0], xyy[1]);
                    println!("Reference xy: [{:.10}, {:.10}]", ref_xyy[0], ref_xyy[1]);
                    println!("Difference:   [{:.10}, {:.10}]", 
                             xyy[0] - ref_xyy[0], xyy[1] - ref_xyy[1]);
                    
                    let dx = xyy[0] - ref_xyy[0];
                    let dy = xyy[1] - ref_xyy[1];
                    let distance = (dx * dx + dy * dy).sqrt();
                    println!("Euclidean distance: {:.10}", distance);
                }
                Err(e) => {
                    println!("Error in reverse conversion: {:?}", e);
                }
            }
        }
        Err(e) => {
            println!("Error: {:?}", e);
        }
    }
}