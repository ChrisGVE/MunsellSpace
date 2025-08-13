/// Test and demonstrate all available color conversion utilities

use munsellspace::*;

fn main() {
    println!("MunsellSpace Color Conversion Utilities");
    println!("=======================================\n");
    
    // Start with a red color
    let rgb = [255, 64, 128];
    println!("Starting RGB: {:?}\n", rgb);
    
    println!("Direct RGB Conversions:");
    println!("-----------------------");
    
    // RGB to other formats
    let hex = rgb_to_hex(rgb);
    println!("RGB → Hex: {}", hex);
    
    let lab = rgb_to_lab(rgb).unwrap();
    println!("RGB → Lab: L={:.2}, a={:.2}, b={:.2}", lab[0], lab[1], lab[2]);
    
    let hsl = rgb_to_hsl(rgb).unwrap();
    println!("RGB → HSL: H={:.1}°, S={:.1}%, L={:.1}%", hsl[0], hsl[1], hsl[2]);
    
    let hsv = rgb_to_hsv(rgb).unwrap();
    println!("RGB → HSV: H={:.1}°, S={:.1}%, V={:.1}%", hsv[0], hsv[1], hsv[2]);
    
    println!("\nHex Conversions:");
    println!("----------------");
    
    let rgb_from_hex = hex_to_rgb(&hex).unwrap();
    println!("Hex → RGB: {:?}", rgb_from_hex);
    
    let lab_from_hex = hex_to_lab(&hex).unwrap();
    println!("Hex → Lab: L={:.2}, a={:.2}, b={:.2}", lab_from_hex[0], lab_from_hex[1], lab_from_hex[2]);
    
    let hsl_from_hex = hex_to_hsl(&hex).unwrap();
    println!("Hex → HSL: H={:.1}°, S={:.1}%, L={:.1}%", hsl_from_hex[0], hsl_from_hex[1], hsl_from_hex[2]);
    
    let hsv_from_hex = hex_to_hsv(&hex).unwrap();
    println!("Hex → HSV: H={:.1}°, S={:.1}%, V={:.1}%", hsv_from_hex[0], hsv_from_hex[1], hsv_from_hex[2]);
    
    println!("\nLab Conversions:");
    println!("----------------");
    
    let rgb_from_lab = lab_to_rgb(lab).unwrap();
    println!("Lab → RGB: {:?}", rgb_from_lab);
    
    let hex_from_lab = lab_to_hex(lab).unwrap();
    println!("Lab → Hex: {}", hex_from_lab);
    
    let hsl_from_lab = lab_to_hsl(lab).unwrap();
    println!("Lab → HSL: H={:.1}°, S={:.1}%, L={:.1}%", hsl_from_lab[0], hsl_from_lab[1], hsl_from_lab[2]);
    
    let hsv_from_lab = lab_to_hsv(lab).unwrap();
    println!("Lab → HSV: H={:.1}°, S={:.1}%, V={:.1}%", hsv_from_lab[0], hsv_from_lab[1], hsv_from_lab[2]);
    
    println!("\nHSL Conversions:");
    println!("----------------");
    
    let rgb_from_hsl = hsl_to_rgb(hsl).unwrap();
    println!("HSL → RGB: {:?}", rgb_from_hsl);
    
    let hex_from_hsl = hsl_to_hex(hsl).unwrap();
    println!("HSL → Hex: {}", hex_from_hsl);
    
    let lab_from_hsl = hsl_to_lab(hsl).unwrap();
    println!("HSL → Lab: L={:.2}, a={:.2}, b={:.2}", lab_from_hsl[0], lab_from_hsl[1], lab_from_hsl[2]);
    
    println!("\nHSV Conversions:");
    println!("----------------");
    
    let rgb_from_hsv = hsv_to_rgb(hsv).unwrap();
    println!("HSV → RGB: {:?}", rgb_from_hsv);
    
    let hex_from_hsv = hsv_to_hex(hsv).unwrap();
    println!("HSV → Hex: {}", hex_from_hsv);
    
    let lab_from_hsv = hsv_to_lab(hsv).unwrap();
    println!("HSV → Lab: L={:.2}, a={:.2}, b={:.2}", lab_from_hsv[0], lab_from_hsv[1], lab_from_hsv[2]);
    
    println!("\nRound-trip Consistency Tests:");
    println!("-----------------------------");
    
    // Test round-trips
    let rgb2 = hex_to_rgb(&rgb_to_hex(rgb)).unwrap();
    println!("RGB → Hex → RGB: {:?} (diff: {:?})", 
        rgb2, 
        [rgb[0] as i32 - rgb2[0] as i32, rgb[1] as i32 - rgb2[1] as i32, rgb[2] as i32 - rgb2[2] as i32]);
    
    let rgb3 = lab_to_rgb(rgb_to_lab(rgb).unwrap()).unwrap();
    println!("RGB → Lab → RGB: {:?} (diff: {:?})", 
        rgb3,
        [rgb[0] as i32 - rgb3[0] as i32, rgb[1] as i32 - rgb3[1] as i32, rgb[2] as i32 - rgb3[2] as i32]);
    
    let rgb4 = hsl_to_rgb(rgb_to_hsl(rgb).unwrap()).unwrap();
    println!("RGB → HSL → RGB: {:?} (diff: {:?})", 
        rgb4,
        [rgb[0] as i32 - rgb4[0] as i32, rgb[1] as i32 - rgb4[1] as i32, rgb[2] as i32 - rgb4[2] as i32]);
    
    let rgb5 = hsv_to_rgb(rgb_to_hsv(rgb).unwrap()).unwrap();
    println!("RGB → HSV → RGB: {:?} (diff: {:?})", 
        rgb5,
        [rgb[0] as i32 - rgb5[0] as i32, rgb[1] as i32 - rgb5[1] as i32, rgb[2] as i32 - rgb5[2] as i32]);
    
    println!("\n✅ All color conversion utilities are working!");
    println!("\n📊 Available Conversions Matrix:");
    println!("┌─────┬─────┬─────┬─────┬─────┬─────┐");
    println!("│From↓│ RGB │ Hex │ Lab │ HSL │ HSV │");
    println!("├─────┼─────┼─────┼─────┼─────┼─────┤");
    println!("│ RGB │  -  │  ✓  │  ✓  │  ✓  │  ✓  │");
    println!("│ Hex │  ✓  │  -  │  ✓  │  ✓  │  ✓  │");
    println!("│ Lab │  ✓  │  ✓  │  -  │  ✓  │  ✓  │");
    println!("│ HSL │  ✓  │  ✓  │  ✓  │  -  │  *  │");
    println!("│ HSV │  ✓  │  ✓  │  ✓  │  *  │  -  │");
    println!("└─────┴─────┴─────┴─────┴─────┴─────┘");
    println!("* HSL↔HSV conversion goes through RGB");
}