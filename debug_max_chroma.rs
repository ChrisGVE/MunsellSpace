// Debug maximum chroma calculation
fn main() {
    // Test for value 9.35
    let value = 9.35;
    
    // Current formula
    let reduction_factor: f64 = 2.0 - (value / 10.0); // At 9.35: 2.0 - 0.935 = 1.065
    let reduction_factor = reduction_factor.min(1.0); // Cap at 1.0
    
    println!("Value: {}", value);
    println!("Reduction factor: {}", reduction_factor);
    
    // If base chroma is say 20
    let base_chroma = 20.0;
    println!("Base chroma: {}", base_chroma);
    println!("Reduced chroma: {}", base_chroma * reduction_factor);
    
    // But we need chroma 12.8 for RGB(187,255,153)
    // If base is 20, we need factor 0.64
    // If base is 15, we need factor 0.85
    println!("\nFor chroma 12.8:");
    println!("  If base=20, need factor={}", 12.8 / 20.0);
    println!("  If base=15, need factor={}", 12.8 / 15.0);
}