use munsellspace::python_port_lab::*;

fn main() {
    println!("=== DEBUGGING LAB INITIALIZATION FOR GREY ===");
    
    // Test RGB(221, 238, 238) - near grey
    let xyy = [0.3016456112, 0.3289687108, 0.8269427000];
    println!("Testing xyY: ({:.6}, {:.6}, {:.6})", xyy[0], xyy[1], xyy[2]);
    
    // Convert to XYZ
    let xyz = xyy_to_xyz(xyy);
    println!("XYZ: ({:.6}, {:.6}, {:.6})", xyz[0], xyz[1], xyz[2]);
    
    // Reference white (Illuminant C)
    let xyz_r = xyy_to_xyz([0.31006, 0.31616, xyy[2]]);
    println!("XYZ_r: ({:.6}, {:.6}, {:.6})", xyz_r[0], xyz_r[1], xyz_r[2]);
    
    // Convert to Lab
    let lab = xyz_to_lab(xyz, "C");
    println!("Lab: L={:.3}, a={:.3}, b={:.3}", lab[0], lab[1], lab[2]);
    
    // Convert to LCHab
    let lchab = lab_to_lchab(lab);
    println!("LCHab: L={:.3}, C={:.3}, H={:.3}", lchab[0], lchab[1], lchab[2]);
    
    // Get initial Munsell specification
    let initial_spec = lchab_to_munsell_specification(lchab);
    println!("Initial spec from LCHab: [{:.3}, {:.3}, {:.3}, {}]", 
             initial_spec[0], initial_spec[1], initial_spec[2], initial_spec[3] as i32);
    
    // Apply the scaling
    let initial_chroma = (5.0 / 5.5) * initial_spec[2];
    println!("After scaling (5.0/5.5): {:.3}", initial_chroma);
    
    // Check clamping
    let final_chroma = if initial_chroma.is_nan() || initial_chroma < 0.1 {
        1.0
    } else {
        initial_chroma
    };
    println!("After clamping: {:.3}", final_chroma);
    
    println!("\nDebug output shows initial chroma = 1.978");
    println!("Difference: {:.3}", 1.978 - final_chroma);
    
    // Also check the polar coordinates
    let x_center = 0.31006;
    let y_center = 0.31616;
    let rho = ((xyy[0] - x_center).powi(2) + (xyy[1] - y_center).powi(2)).sqrt();
    println!("\nPolar rho from center: {:.6}", rho);
    println!("This is close to grey threshold (0.001)");
}