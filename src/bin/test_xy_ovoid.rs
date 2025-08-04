use munsellspace::mathematical::MathematicalMunsellConverter;

fn main() {
    let converter = MathematicalMunsellConverter::new().unwrap();
    
    // Test cases
    let test_cases = vec![
        (5.296, 5.0, 0.0, 4, "chroma=0"),
        (5.296, 5.0, 2.0, 4, "chroma=2"),
    ];
    
    for (hue, value, chroma, code, label) in test_cases {
        // Access the private method through a workaround
        // Actually, we can't access private methods. Let's test through the public API
        
        // We need to test through munsell_specification_to_xy which is also private
        // Let's create a full spec and convert
        let spec = munsellspace::MunsellSpecification {
            hue,
            family: "GY".to_string(),
            value,
            chroma,
        };
        
        let xyy = converter.munsell_specification_to_xyy(&spec).unwrap();
        println!("{}: hue={}, value={}, chroma={}, code={}", label, hue, value, chroma, code);
        println!("  xy: ({:.6}, {:.6})", xyy.x, xyy.y);
    }
    
    println!("\nExpected from Python:");
    println!("chroma=0: xy=(0.310060, 0.316160)");
    println!("chroma=2: xy=(0.327586, 0.360707)");
}