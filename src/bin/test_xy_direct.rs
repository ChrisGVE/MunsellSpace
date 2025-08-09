//! Direct test of xy_from_renotation functions

use munsellspace::python_port::*;

fn main() {
    // Test the problematic specification from iteration 1
    let spec = [8.6058, 9.3528, 12.6521, 4.0];
    
    println!("Testing specification: {:?}", spec);
    println!("  Hue: {:.4}", spec[0]);
    println!("  Value: {:.4}", spec[1]);
    println!("  Chroma: {:.4}", spec[2]);
    println!("  Code: {} (GY)", spec[3] as u8);
    
    // Test xy_from_renotation_ovoid_interpolated
    match xy_from_renotation_ovoid_interpolated(&spec) {
        Ok(xy) => {
            println!("\nRust xy_from_renotation_ovoid_interpolated result:");
            println!("  x: {:.6}", xy[0]);
            println!("  y: {:.6}", xy[1]);
            
            // Calculate rho
            let x_center = 0.31006;
            let y_center = 0.31616;
            let x_diff = xy[0] - x_center;
            let y_diff = xy[1] - y_center;
            let rho = (x_diff * x_diff + y_diff * y_diff).sqrt();
            
            println!("\nCalculated rho from neutral:");
            println!("  x_diff: {:.6}", x_diff);
            println!("  y_diff: {:.6}", y_diff);
            println!("  rho: {:.6}", rho);
            
            println!("\nPython's _munsell_specification_to_xyY gives:");
            println!("  x: 0.326212, y: 0.443071, rho: 0.127935");
            println!("\nDifference in rho: {:.6}", (rho - 0.127935).abs());
        }
        Err(e) => {
            println!("Error: {}", e);
        }
    }
    
    // Also test munsell_specification_to_xy which should be the main entry point
    println!("\n{}", "=".repeat(50));
    match munsell_specification_to_xy(&spec) {
        Ok(xy) => {
            println!("Rust munsell_specification_to_xy result:");
            println!("  x: {:.6}", xy[0]);
            println!("  y: {:.6}", xy[1]);
            
            let x_diff = xy[0] - 0.31006;
            let y_diff = xy[1] - 0.31616;
            let rho = (x_diff * x_diff + y_diff * y_diff).sqrt();
            println!("  rho: {:.6}", rho);
        }
        Err(e) => {
            println!("Error: {}", e);
        }
    }
}