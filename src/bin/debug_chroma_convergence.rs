use munsellspace::python_port::xyy_to_munsell_specification;

fn main() {
    println!("=== DEBUGGING CHROMA CONVERGENCE ===");
    println!("Testing RGB (34, 17, 119) = #221177");
    println!();
    
    // Hardcoded xyY values for RGB (34, 17, 119) based on manual calculation matching Python
    let xyy = [0.175340, 0.086753, 0.020725];
    
    println!("xyY: ({:.6}, {:.6}, {:.6})", xyy[0], xyy[1], xyy[2]);
    
    // Call the function with debug output
    match xyy_to_munsell_specification(xyy) {
        Ok(spec) => {
            println!("Final specification: [{:.3}, {:.3}, {:.6}, {}]", 
                     spec[0], spec[1], spec[2], spec[3] as u8);
            println!("Final chroma: {:.6}", spec[2]);
        },
        Err(e) => println!("Error: {:?}", e),
    }
}