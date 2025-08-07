use munsellspace::python_port::{xyy_to_munsell_specification};

fn main() {
    // Test RGB(221, 238, 238)
    let xyy = [0.3016555411, 0.3289901051, 0.8269331673];
    
    println!("Testing convergence for RGB(221, 238, 238)");
    println!("xyY: [{:.10}, {:.10}, {:.10}]", xyy[0], xyy[1], xyy[2]);
    println!("Python gets: 7.1G 9.3/2.1 (chroma=2.084644)");
    println!("We currently get: chroma ~1.556");
    println!();
    
    // Set environment variable to get debug output
    std::env::set_var("MUNSELL_DEBUG", "1");
    
    match xyy_to_munsell_specification(xyy) {
        Ok(spec) => {
            println!("\n=== FINAL RESULT ===");
            println!("Specification: [{:.6}, {:.6}, {:.6}, {}]", 
                spec[0], spec[1], spec[2], spec[3] as i32);
            println!("Munsell notation: {:.1}G {:.1}/{:.1}", spec[0], spec[1], spec[2]);
            println!("Chroma difference from Python: {:.6}", spec[2] - 2.084644);
        }
        Err(e) => {
            println!("Error: {}", e);
        }
    }
}