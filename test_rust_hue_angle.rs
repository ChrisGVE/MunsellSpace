use munsellspace::python_port::hue_angle_to_hue;

fn main() {
    let test_angles = vec![
        0.0, 30.0, 45.0, 60.0, 70.0, 90.0, 120.0, 135.0, 150.0,
        160.0, 180.0, 210.0, 225.0, 240.0, 255.0, 270.0, 300.0, 315.0, 330.0, 360.0
    ];
    
    println!("Rust's hue_angle_to_hue results:");
    println!("{}", "=".repeat(60));
    
    let hue_codes = vec!["", "B", "BG", "G", "GY", "Y", "YR", "R", "RP", "P", "PB"];
    
    for angle in test_angles {
        let (hue, code) = hue_angle_to_hue(angle);
        println!("Angle {:3.0}° -> Hue {:.1}, Code {} ({})", 
                 angle, hue, code, hue_codes[code as usize]);
    }
}