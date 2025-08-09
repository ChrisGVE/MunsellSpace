use munsellspace::python_port::maximum_chroma_from_renotation;

fn main() {
    // Test max chroma for G family at various values
    let hue = 7.1;
    let code = 3; // G family
    
    let values = vec![8.0, 8.5, 9.0, 9.2, 9.277, 9.5, 9.8, 9.9, 9.95, 9.99, 10.0];
    
    println!("Testing maximum chroma for G family (hue={}, code={}):", hue, code);
    println!();
    
    for value in values {
        let max_chroma = maximum_chroma_from_renotation(hue, value, code);
        println!("  Value {:.3}: max_chroma = {:?}", value, max_chroma);
    }
}