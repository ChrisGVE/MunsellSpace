use munsellspace::python_port::{xyy_to_munsell_specification};

fn main() {
    // Test the problematic grey color RGB(221, 238, 238)
    let xyy = [0.3016555411, 0.3289901051, 0.8269331673];
    
    println!("Testing convergence for xyY: [{:.10}, {:.10}, {:.10}]", xyy[0], xyy[1], xyy[2]);
    println!("Expected Python result: 7.1G 9.3/2.1");
    println!("Current Rust result: 7.2G 9.3/1.6");
    println!();
    
    match xyy_to_munsell_specification(xyy) {
        Ok(spec) => {
            println!("Final specification: [{:.10}, {:.10}, {:.10}, {}]", 
                spec[0], spec[1], spec[2], spec[3] as i32);
            println!("Munsell notation: {:.1}G {:.1}/{:.1}", spec[0], spec[1], spec[2]);
            
            println!("\nChroma difference from Python: {:.3}", spec[2] - 2.084);
            println!("This suggests our convergence is stopping when phi_difference < threshold");
            println!("But Python continues iterating to get closer to the target.");
        }
        Err(e) => {
            println!("Error: {}", e);
        }
    }
}