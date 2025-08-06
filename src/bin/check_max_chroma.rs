//! Check maximum chroma for debugging

use munsellspace::python_port::maximum_chroma_from_renotation;

fn main() {
    // Check maximum chroma for the green spec
    // The spec is [7.877, 8.0, 22.595, 4]
    let hue = 7.877;
    let value = 8.0;
    let code = 4; // GY
    
    let max_chroma = maximum_chroma_from_renotation(hue, value, code);
    println!("Maximum chroma for hue={:.3} value={} code={}: {:.1}", 
             hue, value, code, max_chroma);
    
    // Try 7.5GY instead
    let hue = 7.5;
    let max_chroma = maximum_chroma_from_renotation(hue, value, code);
    println!("Maximum chroma for hue={:.3} value={} code={}: {:.1}", 
             hue, value, code, max_chroma);
    
    // Try value 9
    let value = 9.0;
    let hue = 7.877;
    let max_chroma = maximum_chroma_from_renotation(hue, value, code);
    println!("Maximum chroma for hue={:.3} value={} code={}: {:.1}", 
             hue, value, code, max_chroma);
             
    // Try 7.5GY value 9
    let hue = 7.5;
    let max_chroma = maximum_chroma_from_renotation(hue, value, code);
    println!("Maximum chroma for hue={:.3} value={} code={}: {:.1}", 
             hue, value, code, max_chroma);
}