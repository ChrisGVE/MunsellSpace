use munsellspace::python_port::{maximum_chroma_from_renotation, xy_from_renotation_ovoid};

fn main() {
    // The problematic initial spec
    let spec = [5.242, 9.277, 2.178, 3.0];
    
    println!("Testing problematic spec: {:?}", spec);
    println!();
    
    // Test maximum chroma
    let max_chroma = maximum_chroma_from_renotation(spec[0], spec[1], spec[3] as u8);
    println!("Maximum chroma for hue={:.3}, value={:.3}, code={}: {:?}", 
             spec[0], spec[1], spec[3] as u8, max_chroma);
    
    // Try with integer value
    let max_chroma_9 = maximum_chroma_from_renotation(spec[0], 9.0, spec[3] as u8);
    println!("Maximum chroma for hue={:.3}, value=9.0, code={}: {:?}", 
             spec[0], spec[3] as u8, max_chroma_9);
    
    // Try with standard hue
    let max_chroma_std = maximum_chroma_from_renotation(5.0, 9.0, spec[3] as u8);
    println!("Maximum chroma for hue=5.0, value=9.0, code={}: {:?}", 
             spec[3] as u8, max_chroma_std);
    
    println!();
    println!("Testing xy_from_renotation_ovoid with spec:");
    match xy_from_renotation_ovoid(&spec) {
        Ok(xy) => println!("Success: xy = ({:.6}, {:.6})", xy[0], xy[1]),
        Err(e) => println!("Error: {}", e),
    }
}