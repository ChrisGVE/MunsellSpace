//! Test to trace XYZ scaling flow

use munsellspace::python_converter::PythonMunsellConverter;

fn main() {
    let rgb = [221u8, 238u8, 238u8];
    println!("Testing RGB({}, {}, {})", rgb[0], rgb[1], rgb[2]);
    
    // Manual conversion to see each step
    let converter = PythonMunsellConverter::new();
    
    // Step 1: sRGB to linear
    let rgb_norm = [rgb[0] as f64 / 255.0, rgb[1] as f64 / 255.0, rgb[2] as f64 / 255.0];
    println!("Normalized RGB: [{:.6}, {:.6}, {:.6}]", rgb_norm[0], rgb_norm[1], rgb_norm[2]);
    
    let mut rgb_linear = [0.0; 3];
    for i in 0..3 {
        let c = rgb_norm[i];
        rgb_linear[i] = if c <= 0.04045 {
            c / 12.92
        } else {
            ((c + 0.055) / 1.055).powf(2.4)
        };
    }
    println!("Linear RGB: [{:.6}, {:.6}, {:.6}]", rgb_linear[0], rgb_linear[1], rgb_linear[2]);
    
    // Step 2: Linear RGB to XYZ (unscaled)
    let matrix = [
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ];
    
    let xyz_unscaled = [
        matrix[0][0] * rgb_linear[0] + matrix[0][1] * rgb_linear[1] + matrix[0][2] * rgb_linear[2],
        matrix[1][0] * rgb_linear[0] + matrix[1][1] * rgb_linear[1] + matrix[1][2] * rgb_linear[2],
        matrix[2][0] * rgb_linear[0] + matrix[2][1] * rgb_linear[1] + matrix[2][2] * rgb_linear[2],
    ];
    println!("XYZ (unscaled): [{:.6}, {:.6}, {:.6}]", xyz_unscaled[0], xyz_unscaled[1], xyz_unscaled[2]);
    
    // Step 3: Apply scaling
    const XYZ_SCALING: f64 = 1.111528762434975;
    let xyz_scaled = [
        xyz_unscaled[0] * XYZ_SCALING,
        xyz_unscaled[1] * XYZ_SCALING,
        xyz_unscaled[2] * XYZ_SCALING,
    ];
    println!("XYZ (scaled):   [{:.6}, {:.6}, {:.6}]", xyz_scaled[0], xyz_scaled[1], xyz_scaled[2]);
    
    // Step 4: XYZ to xyY (unscaled)
    let sum_unscaled = xyz_unscaled[0] + xyz_unscaled[1] + xyz_unscaled[2];
    let xyy_unscaled = [
        xyz_unscaled[0] / sum_unscaled,
        xyz_unscaled[1] / sum_unscaled,
        xyz_unscaled[1],
    ];
    println!("xyY (unscaled): [{:.6}, {:.6}, {:.6}]", xyy_unscaled[0], xyy_unscaled[1], xyy_unscaled[2]);
    
    // Step 5: XYZ to xyY (scaled)
    let sum_scaled = xyz_scaled[0] + xyz_scaled[1] + xyz_scaled[2];
    let xyy_scaled = [
        xyz_scaled[0] / sum_scaled,
        xyz_scaled[1] / sum_scaled,
        xyz_scaled[1],
    ];
    println!("xyY (scaled):   [{:.6}, {:.6}, {:.6}]", xyy_scaled[0], xyy_scaled[1], xyy_scaled[2]);
    
    println!("\nComparison:");
    println!("  Python gets xyY: [0.307683, 0.328987, 0.919160]");
    println!("  We should get:   [{:.6}, {:.6}, {:.6}]", xyy_scaled[0], xyy_scaled[1], xyy_scaled[2]);
    
    // Now test with the converter
    println!("\nUsing PythonMunsellConverter:");
    match converter.srgb_to_munsell(rgb) {
        Ok(munsell) => {
            println!("Result: {}", munsell.notation);
        }
        Err(e) => {
            println!("Error: {:?}", e);
        }
    }
}