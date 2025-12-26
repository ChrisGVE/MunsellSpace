use munsellspace::mathematical::MathematicalMunsellConverter;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 4 {
        eprintln!("Usage: {} <r> <g> <b>", args[0]);
        std::process::exit(1);
    }

    let r: u8 = args[1].parse().expect("Invalid R value");
    let g: u8 = args[2].parse().expect("Invalid G value");
    let b: u8 = args[3].parse().expect("Invalid B value");

    let converter = MathematicalMunsellConverter::new().expect("Failed to create converter");

    println!("🔬 MATHEMATICAL DEBUG for RGB [{}, {}, {}]", r, g, b);
    println!();

    // Step 1: sRGB to xyY conversion
    match converter.srgb_to_xyy([r, g, b]) {
        Ok(xyy) => {
            println!("Step 1 - sRGB to xyY (with chromatic adaptation):");
            println!("  x: {:.6}", xyy.x);
            println!("  y: {:.6}", xyy.y);
            println!("  Y: {:.6}", xyy.y_luminance);
            println!();

            // Step 2: xyY to Munsell conversion
            match converter.xyy_to_munsell_specification(xyy) {
                Ok(munsell) => {
                    println!("Step 2 - xyY to Munsell:");
                    println!("  Hue: {:.1}", munsell.hue);
                    println!("  Family: {}", munsell.family);
                    println!("  Value: {:.1}", munsell.value);
                    println!("  Chroma: {:.1}", munsell.chroma);
                    println!();
                    
                    let notation = converter.format_munsell_notation(&munsell);
                    println!("Final Result: {}", notation);
                }
                Err(e) => {
                    eprintln!("Error in xyY to Munsell conversion: {:?}", e);
                }
            }
        }
        Err(e) => {
            eprintln!("Error in sRGB to xyY conversion: {:?}", e);
        }
    }
}