use munsellspace::python_port::*;

fn main() {
    // Test RGB [0, 64, 64]
    let rgb = [0u8, 64, 64];
    
    // Convert to xyY
    let srgb = [rgb[0] as f64 / 255.0, rgb[1] as f64 / 255.0, rgb[2] as f64 / 255.0];
    
    // sRGB to XYZ
    let xyz = {
        let r = if srgb[0] <= 0.04045 {
            srgb[0] / 12.92
        } else {
            ((srgb[0] + 0.055) / 1.055).powf(2.4)
        };
        let g = if srgb[1] <= 0.04045 {
            srgb[1] / 12.92
        } else {
            ((srgb[1] + 0.055) / 1.055).powf(2.4)
        };
        let b = if srgb[2] <= 0.04045 {
            srgb[2] / 12.92
        } else {
            ((srgb[2] + 0.055) / 1.055).powf(2.4)
        };
        
        let x = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b;
        let y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b;
        let z = 0.0193339 * r + 0.1191920 * g + 0.9503041 * b;
        
        [x, y, z]
    };
    
    // XYZ to xyY
    let xyy = {
        let sum = xyz[0] + xyz[1] + xyz[2];
        if sum < 1e-10 {
            [0.31006, 0.31616, 0.0]
        } else {
            [xyz[0] / sum, xyz[1] / sum, xyz[1]]
        }
    };
    
    println!("RGB {:?}", rgb);
    println!("xyY: [{:.6}, {:.6}, {:.6}]", xyy[0], xyy[1], xyy[2]);
    
    // Calculate angle
    let x_c = 0.31006;
    let y_c = 0.31616;
    
    let dx = xyy[0] - x_c;
    let dy = xyy[1] - y_c;
    
    println!("\nCoordinates relative to Illuminant C:");
    println!("  dx = {:.6}", dx);
    println!("  dy = {:.6}", dy);
    
    let angle_rad = dy.atan2(dx);
    let mut angle = angle_rad * 180.0 / std::f64::consts::PI;
    if angle < 0.0 {
        angle += 360.0;
    }
    
    println!("\nHue angle (Rust): {:.1}°", angle);
    
    // Test hue_angle_to_hue
    let (hue, code) = hue_angle_to_hue(angle);
    println!("hue_angle_to_hue({:.1}°) -> {:.1}, code {}", angle, hue, code);
    
    let hue_codes = ["", "B", "BG", "G", "GY", "Y", "YR", "R", "RP", "P", "PB"];
    println!("Family: {}", hue_codes[code as usize]);
}