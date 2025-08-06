//! Debug BG color convergence issue

use munsellspace::python_port::*;
use munsellspace::python_port_helpers::*;

fn main() {
    // Test one problematic BG color
    let xyy = [0.216740, 0.300235, 0.323373];  // Should be 9.6BG 6.3/7.9
    println!("Testing xyY: {:?}", xyy);
    
    // Manual convergence debugging
    let (x, y, big_y) = (xyy[0], xyy[1], xyy[2]);
    
    // Convert Y to Munsell value
    let value = munsell_value_astmd1535(big_y * 100.0);
    println!("Value: {:.2}", value);
    
    // Get initial spec from LCHab
    let xyz = xyy_to_xyz(xyy);
    let xyz_r = xyy_to_xyz([0.31006, 0.31616, big_y]); // Illuminant C
    let xyz_r_norm = [xyz_r[0] / xyz_r[1], 1.0, xyz_r[2] / xyz_r[1]];
    let lab = xyz_to_lab(xyz, xyz_to_xy(xyz_r_norm));
    let lchab = lab_to_lchab(lab);
    let initial_spec = lchab_to_munsell_specification(lchab);
    
    println!("Initial spec from LCHab: [{:.2}, {:.2}, {:.2}, {}]", 
             initial_spec[0], initial_spec[1], initial_spec[2], initial_spec[3] as u8);
    
    // Check what happens in first iteration
    let hue_current = initial_spec[0];
    let chroma_current = (5.0 / 5.5) * initial_spec[2];
    let code_current = initial_spec[3] as u8;
    
    println!("\nFirst iteration:");
    println!("  Hue: {:.2}, Value: {:.2}, Chroma: {:.2}, Code: {}", 
             hue_current, value, chroma_current, code_current);
    
    // Try to get xy from this specification
    let spec = [hue_current, value, chroma_current, code_current as f64];
    match xy_from_renotation_ovoid_interpolated(&spec) {
        Ok(xy) => {
            let (x_current, y_current) = (xy[0], xy[1]);
            println!("  xy from spec: ({:.6}, {:.6})", x_current, y_current);
            
            // Calculate error
            let error_x = x - x_current;
            let error_y = y - y_current;
            println!("  Error: ({:.6}, {:.6})", error_x, error_y);
            
            // Check convergence
            let distance = (error_x.powi(2) + error_y.powi(2)).sqrt();
            println!("  Distance: {:.9}", distance);
        }
        Err(e) => {
            println!("  Error getting xy: {:?}", e);
        }
    }
}