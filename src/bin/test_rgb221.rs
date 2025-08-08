use munsellspace::python_port::xyy_to_munsell_specification;

fn main() {
    let xyy = [0.3016555411, 0.3289901051, 0.8269331673];
    
    println!("Testing RGB(221, 238, 238)");
    println!("xyY: {:?}", xyy);
    
    match xyy_to_munsell_specification(xyy) {
        Ok(spec) => {
            println!("\nFinal Munsell spec:");
            println!("  Hue:    {:.6}", spec[0]);
            println!("  Value:  {:.6}", spec[1]);
            println!("  Chroma: {:.6}", spec[2]);
            println!("  Code:   {}", spec[3]);
            
            println!("\nCompare with Python:");
            println!("  Python hue:    7.105611");
            println!("  Python value:  9.277364");
            println!("  Python chroma: 2.084644");
            println!("  Python code:   3");
            
            println!("\nDifferences:");
            println!("  Hue diff:    {:.6}", (spec[0] - 7.105611).abs());
            println!("  Value diff:  {:.6}", (spec[1] - 9.277364).abs());
            println!("  Chroma diff: {:.6}", (spec[2] - 2.084644).abs());
        }
        Err(e) => println!("Error: {}", e)
    }
}