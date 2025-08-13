/// Test reverse conversion from Munsell to RGB and other color systems

use munsellspace::python_converter::PythonMunsellConverter;
use munsellspace::reverse_conversion::{parse_munsell_notation, munsell_to_hex_string};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Testing Reverse Conversion: Munsell → RGB/Hex/Lab/HSL/HSV");
    println!("=========================================================\n");
    
    // Create converter
    let converter = PythonMunsellConverter::new();
    
    // Test colors with known conversions
    let test_cases = vec![
        ("5R 4/14", "vivid red"),
        ("2.5YR 6/12", "orange"),
        ("5Y 8/10", "yellow"),
        ("7.5GY 5/8", "yellow-green"),
        ("5G 4/6", "green"),
        ("7.5BG 5/4", "blue-green"),
        ("5B 5/8", "blue"),
        ("7.5PB 3/10", "purple-blue"),
        ("5P 4/8", "purple"),
        ("7.5RP 5/10", "red-purple"),
        ("N 5", "medium gray"),
        ("N 9", "light gray"),
        ("N 2", "dark gray"),
    ];
    
    println!("Test 1: Munsell → sRGB Conversion");
    println!("----------------------------------");
    
    for (munsell_str, description) in &test_cases {
        match converter.munsell_to_srgb(munsell_str) {
            Ok(rgb) => {
                println!("{:15} ({:15}) → RGB [{:3}, {:3}, {:3}]", 
                    munsell_str, description, rgb.r, rgb.g, rgb.b);
            }
            Err(e) => {
                println!("{:15} ({:15}) → ERROR: {}", munsell_str, description, e);
            }
        }
    }
    
    println!("\n\nTest 2: Munsell → Hex Conversion (via convenience function)");
    println!("------------------------------------------------------------");
    
    for (munsell_str, description) in &test_cases {
        match munsell_to_hex_string(munsell_str) {
            Ok(hex) => {
                println!("{:15} ({:15}) → {}", munsell_str, description, hex);
            }
            Err(e) => {
                println!("{:15} ({:15}) → ERROR: {}", munsell_str, description, e);
            }
        }
    }
    
    println!("\n\nTest 3: Round-trip Test (RGB → Munsell → RGB)");
    println!("----------------------------------------------");
    
    // Test some RGB values
    let rgb_tests = vec![
        ([255, 0, 0], "pure red"),
        ([0, 255, 0], "pure green"),
        ([0, 0, 255], "pure blue"),
        ([255, 255, 0], "yellow"),
        ([255, 0, 255], "magenta"),
        ([0, 255, 255], "cyan"),
        ([128, 128, 128], "medium gray"),
        ([255, 165, 0], "orange"),
    ];
    
    // We need the forward converter too
    let forward_converter = munsellspace::MunsellConverter::new()?;
    
    for (rgb, description) in &rgb_tests {
        // Forward: RGB → Munsell
        let munsell = forward_converter.srgb_to_munsell(*rgb)?;
        println!("\nRGB {:?} ({}):", rgb, description);
        println!("  → Munsell: {}", munsell.notation);
        
        // Reverse: Munsell → RGB
        match converter.munsell_to_srgb(&munsell.notation) {
            Ok(rgb_back) => {
                println!("  ← RGB: [{}, {}, {}]", rgb_back.r, rgb_back.g, rgb_back.b);
                
                // Calculate difference
                let dr = (rgb[0] as i16 - rgb_back.r as i16).abs();
                let dg = (rgb[1] as i16 - rgb_back.g as i16).abs();
                let db = (rgb[2] as i16 - rgb_back.b as i16).abs();
                let total_diff = dr + dg + db;
                
                if total_diff <= 10 {
                    println!("  ✅ Excellent round-trip (diff: {})", total_diff);
                } else if total_diff <= 30 {
                    println!("  ⚠️  Good round-trip (diff: {})", total_diff);
                } else {
                    println!("  ❌ Poor round-trip (diff: {})", total_diff);
                }
            }
            Err(e) => {
                println!("  ← ERROR: {}", e);
            }
        }
    }
    
    println!("\n\nTest 4: Edge Cases");
    println!("------------------");
    
    let edge_cases = vec![
        "N 0",      // Pure black
        "N 10",     // Pure white (theoretical)
        "N 9.5",    // Near white
        "5R 9/2",   // Very light, low chroma
        "5R 2/20",  // Very dark, high chroma (may be out of gamut)
    ];
    
    for munsell_str in &edge_cases {
        print!("{:12} → ", munsell_str);
        match converter.munsell_to_srgb(munsell_str) {
            Ok(rgb) => {
                println!("RGB [{:3}, {:3}, {:3}]", rgb.r, rgb.g, rgb.b);
            }
            Err(e) => {
                println!("ERROR: {}", e);
            }
        }
    }
    
    println!("\n\nTest 5: Parse Munsell Notation Formats");
    println!("---------------------------------------");
    
    let notation_tests = vec![
        "5R 4/14",        // Standard format
        "2.5YR 6/12",     // Decimal hue
        "N 5",            // Neutral short
        "N5",             // Neutral compact
        "N 5/",           // Neutral with slash
        "N5/0",           // Neutral with explicit zero chroma
        "N 5/0.0",        // Neutral with decimal zero chroma
        "10RP 3/4",       // 10 hue (boundary)
    ];
    
    for notation in &notation_tests {
        print!("{:15} → ", notation);
        match parse_munsell_notation(notation) {
            Ok(spec) => {
                println!("Parsed: hue={:.1} family={} value={:.1} chroma={:.1}", 
                    spec.hue, spec.family, spec.value, spec.chroma);
            }
            Err(e) => {
                println!("Parse ERROR: {}", e);
            }
        }
    }
    
    println!("\n✅ Reverse conversion testing complete!");
    
    Ok(())
}