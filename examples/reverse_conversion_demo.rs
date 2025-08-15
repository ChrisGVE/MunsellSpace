//! Reverse Conversion Demo
//! 
//! Demonstrates the complete reverse conversion pipeline:
//! Munsell → Lab → sRGB/hex/HSL/HSV

use munsellspace::{ReverseConverter, Result};
use munsellspace::mathematical::MunsellSpecification;

fn main() -> Result<()> {
    println!("🎨 MunsellSpace Reverse Conversion Demo");
    println!("=====================================");
    println!();
    
    // Create reverse converter
    let converter = ReverseConverter::new()?;
    
    // Demo colors with different characteristics
    let demo_colors = vec![
        // Classic red
        MunsellSpecification {
            hue: 5.0,
            family: "R".to_string(),
            value: 4.0,
            chroma: 14.0,
        },
        // Neutral gray
        MunsellSpecification {
            hue: 0.0,
            family: "N".to_string(),
            value: 5.0,
            chroma: 0.0,
        },
        // Blue-green
        MunsellSpecification {
            hue: 7.5,
            family: "BG".to_string(),
            value: 6.0,
            chroma: 8.0,
        },
        // Yellow
        MunsellSpecification {
            hue: 2.5,
            family: "Y".to_string(),
            value: 8.0,
            chroma: 12.0,
        },
    ];
    
    for (i, munsell) in demo_colors.iter().enumerate() {
        println!("Demo Color #{}", i + 1);
        println!("━━━━━━━━━━━━━━");
        
        // Convert to all formats
        let colors = converter.munsell_to_all_formats(munsell)?;
        
        // Display results
        println!("📋 Munsell:   {:.1}{} {:.1}/{:.1}", 
                colors.munsell.hue, colors.munsell.family, 
                colors.munsell.value, colors.munsell.chroma);
        
        println!("🔬 Lab:       L*{:.1} a*{:.1} b*{:.1}", 
                colors.lab.l, colors.lab.a, colors.lab.b);
        
        println!("🖥️  sRGB:      [{}, {}, {}]", 
                colors.srgb[0], colors.srgb[1], colors.srgb[2]);
        
        println!("🎯 Hex:       {}", colors.hex);
        
        println!("🌈 HSL:       H{:.1}° S{:.1}% L{:.1}%", 
                colors.hsl.h, colors.hsl.s, colors.hsl.l);
        
        println!("✨ HSV:       H{:.1}° S{:.1}% V{:.1}%", 
                colors.hsv.h, colors.hsv.s, colors.hsv.v);
        
        println!();
    }
    
    // Demonstrate individual conversion methods
    println!("🔧 Individual Conversion Methods");
    println!("================================");
    
    let red = &demo_colors[0];
    
    // Individual conversions
    let lab = converter.munsell_to_lab(red)?;
    let srgb = converter.munsell_to_srgb(red)?;
    let hex = converter.munsell_to_hex(red)?;
    let hsl = converter.munsell_to_hsl(red)?;
    let hsv = converter.munsell_to_hsv(red)?;
    
    println!("Individual conversions for 5R 4/14:");
    println!("  Lab:  L*{:.1} a*{:.1} b*{:.1}", lab.l, lab.a, lab.b);
    println!("  sRGB: [{}, {}, {}]", srgb[0], srgb[1], srgb[2]);
    println!("  Hex:  {}", hex);
    println!("  HSL:  H{:.1}° S{:.1}% L{:.1}%", hsl.h, hsl.s, hsl.l);
    println!("  HSV:  H{:.1}° S{:.1}% V{:.1}%", hsv.h, hsv.s, hsv.v);
    
    println!();
    
    // Demonstrate parsing convenience function
    println!("📝 Munsell Notation Parsing");
    println!("===========================");
    
    let notation_examples = vec![
        "5R 4/14",      // Standard red
        "N 5",          // Neutral gray
        "2.5YR 6/8",    // Decimal hue
        "10PB 3/6",     // Purple-blue
    ];
    
    for notation in notation_examples {
        match munsellspace::munsell_to_hex_string(notation) {
            Ok(hex) => println!("  {} → {}", notation, hex),
            Err(e) => println!("  {} → Error: {}", notation, e),
        }
    }
    
    println!();
    println!("✅ Reverse conversion demo completed!");
    println!();
    println!("🔬 Scientific Pipeline Used:");
    println!("   Munsell → xyY → XYZ → Lab → sRGB/HSL/HSV");
    println!("   ├── CIE Lab provides perceptually uniform intermediate space");
    println!("   ├── Chromatic adaptation handles illuminant differences");  
    println!("   └── Palette crate ensures accurate color space conversions");
    
    Ok(())
}