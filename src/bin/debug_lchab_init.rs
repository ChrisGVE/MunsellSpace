use munsellspace::python_port_lab::{xyz_to_lab, lab_to_lchab, lchab_to_munsell_specification, xyy_to_xyz, xyz_to_xy};

fn main() {
    let xyy = [0.3016555411, 0.3289901051, 0.8269331673];
    println!("Testing RGB(221, 238, 238) LCHab initialization");
    println!("xyY: {:?}", xyy);
    
    // Convert to XYZ
    let xyz = xyy_to_xyz(xyy);
    println!("\nXYZ: [{:.6}, {:.6}, {:.6}]", xyz[0], xyz[1], xyz[2]);
    
    // Get reference white at same Y
    let (x_i, y_i) = (0.31006, 0.31616); // Illuminant C
    let xyz_r = xyy_to_xyz([x_i, y_i, xyy[2]]);
    println!("XYZ_r: [{:.6}, {:.6}, {:.6}]", xyz_r[0], xyz_r[1], xyz_r[2]);
    
    // Normalize reference white
    let xyz_r_norm = [xyz_r[0] / xyz_r[1], 1.0, xyz_r[2] / xyz_r[1]];
    println!("XYZ_r_norm: [{:.6}, {:.6}, {:.6}]", xyz_r_norm[0], xyz_r_norm[1], xyz_r_norm[2]);
    
    // Convert to xy for Lab
    let xy_r = xyz_to_xy(xyz_r_norm);
    println!("xy_r: [{:.6}, {:.6}]", xy_r[0], xy_r[1]);
    
    // Convert to Lab (using Illuminant C)
    let lab = xyz_to_lab(xyz, "C");
    println!("\nLab: [{:.6}, {:.6}, {:.6}]", lab[0], lab[1], lab[2]);
    
    // Convert to LCHab
    let lchab = lab_to_lchab(lab);
    println!("LCHab: [{:.6}, {:.6}, {:.6}]", lchab[0], lchab[1], lchab[2]);
    
    // Convert to Munsell specification
    let spec = lchab_to_munsell_specification(lchab);
    println!("\nInitial Munsell spec from LCHab:");
    println!("  Hue:    {:.6}", spec[0]);
    println!("  Value:  {:.6}", spec[1]);
    println!("  Chroma: {:.6}", spec[2]);
    println!("  Code:   {}", spec[3]);
    
    // Check what the hue angle mapping gives
    let h = lchab[2];
    println!("\nDebug hue angle mapping:");
    println!("  LCHab hue angle: {:.2}°", h);
    
    if h >= 140.0 && h < 180.0 {
        let mapped_hue = (h - 140.0) / 4.0;
        println!("  Falls in G family range (140-180°)");
        println!("  Formula: ({:.2} - 140) / 4.0 = {:.3}", h, mapped_hue);
        println!("  Should give hue={:.3}, code=3", mapped_hue);
    }
}