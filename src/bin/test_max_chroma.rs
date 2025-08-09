use munsellspace::python_port::maximum_chroma_from_renotation;

fn main() {
    let test_cases = vec![
        (5.242, 9.277, 3, "Initial spec from Rust"),
        (7.181, 9.277, 3, "Converged spec from Rust"),
        (7.105611, 9.277364, 3, "Python's final spec"),
        (5.0, 9.0, 3, "Standard 5G at value 9"),
        (7.5, 9.0, 3, "Standard 7.5G at value 9"),
    ];
    
    println!("Testing maximum chroma lookups:");
    for (hue, value, code, desc) in test_cases {
        let max_chroma = maximum_chroma_from_renotation(hue, value, code);
        println!("{}: hue={:.3}, value={:.3}, code={}", desc, hue, value, code);
        println!("  Maximum chroma: {:?}", max_chroma);
        println!();
    }
}