fn main() {
    let converter = munsellspace::mathematical::MathematicalMunsellConverter::new().unwrap();
    
    // Test spec: hue=5.296, value=5.255, chroma=0.248, code=4
    let spec = munsellspace::MunsellSpecification {
        hue: 5.296,
        family: "GY".to_string(),
        value: 5.255,
        chroma: 0.248,
    };
    
    println!("Testing spec: hue={}, family={}, value={}, chroma={}", 
             spec.hue, spec.family, spec.value, spec.chroma);
    
    // Convert to xyY
    let xyy = converter.munsell_specification_to_xyy(&spec).unwrap();
    println!("Result: x={:.6}, y={:.6}, Y={:.6}", xyy.x, xyy.y, xyy.Y);
    
    // Calculate rho
    let x_c = 0.31006;
    let y_c = 0.31616;
    let rho = ((xyy.x - x_c).powi(2) + (xyy.y - y_c).powi(2)).sqrt();
    println!("Rho relative to Illuminant C: {:.6}", rho);
    
    println!("\nExpected from Python: x=0.312233, y=0.321630, rho=0.005885");
}