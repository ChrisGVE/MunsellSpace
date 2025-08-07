use munsellspace::python_port::xyy_to_munsell_specification;

fn main() {
    println!("=== DEBUGGING GREY CONVERGENCE ===");
    println!("Testing RGB (221, 238, 238) = #ddeeee");
    println!();
    
    // Hardcoded xyY values for RGB (221, 238, 238)
    let xyy = [0.3016456112, 0.3289687108, 0.8269427000];
    
    println!("xyY: ({:.10}, {:.10}, {:.10})", xyy[0], xyy[1], xyy[2]);
    
    // Call the function
    match xyy_to_munsell_specification(xyy) {
        Ok(spec) => {
            println!("Final specification: [{:.10}, {:.10}, {:.10}, {}]", 
                     spec[0], spec[1], spec[2], spec[3] as u8);
            println!("Final chroma: {:.10}", spec[2]);
            println!();
            println!("Python gets: [7.1207827853, 9.2774063954, 2.0837109549, 3.0]");
            println!("Chroma difference: {:.10}", spec[2] - 2.0837109549);
        },
        Err(e) => println!("Error: {:?}", e),
    }
}