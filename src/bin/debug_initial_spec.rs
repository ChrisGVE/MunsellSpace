use munsellspace::python_port::xyy_to_munsell_specification;
use munsellspace::python_port_lab::{xyz_to_lab, lab_to_lchab};

fn main() {
    let xyy = [0.3016555411, 0.3289901051, 0.8269331673];
    
    println!("Testing initial specification for RGB(221, 238, 238)");
    println!("xyY: {:?}", xyy);
    println!();
    
    // Manually calculate the initial spec like Python does
    let (x, y, big_y) = (xyy[0], xyy[1], xyy[2]);
    
    // Convert to XYZ
    let x_capital = x * big_y / y;
    let z = (1.0 - x - y) * big_y / y;
    let xyz = [x_capital, big_y, z];
    println!("XYZ: {:?}", xyz);
    
    // Convert to Lab using Illuminant C
    let lab = xyz_to_lab(xyz, "C");
    println!("Lab: {:?}", lab);
    
    // Convert to LCHab
    let lchab = lab_to_lchab(lab);
    println!("LCHab: {:?}", lchab);
    println!();
    
    println!("Initial specification components:");
    println!("  L* (lightness): {:.6}", lchab[0]);
    println!("  C* (chroma):    {:.6}", lchab[1]);
    println!("  H (hue angle):  {:.6}", lchab[2]);
    println!();
    
    // Now call the actual conversion function
    match xyy_to_munsell_specification(xyy) {
        Ok(spec) => {
            println!("Rust's final Munsell specification:");
            println!("  Hue:    {:.6}", spec[0]);
            println!("  Value:  {:.6}", spec[1]);
            println!("  Chroma: {:.6}", spec[2]);
            println!("  Code:   {}", spec[3]);
            println!();
            
            println!("Key insight:");
            println!("  LCHab chroma is {:.6}", lchab[1]);
            println!("  Final chroma is {:.6}", spec[2]);
            println!("  Ratio: {:.6}", spec[2] / lchab[1]);
        }
        Err(e) => println!("Error: {}", e)
    }
}