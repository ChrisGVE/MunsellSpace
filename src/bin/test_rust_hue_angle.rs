use munsellspace::python_port::{hue_to_hue_angle, hue_angle_to_hue};

fn main() {
    // Test the exact case that's failing
    let hue1 = 9.8947;
    let code1 = 4; // GY
    
    println!("Starting: hue={:.4}, code={} (GY)", hue1, code1);
    
    let angle1 = hue_to_hue_angle(hue1, code1);
    println!("Hue angle: {:.4}°", angle1);
    
    // Test small adjustments
    let adjustments = [-5.0, -2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 5.0];
    
    println!("\nTesting small angle adjustments:");
    println!("{}", "=".repeat(60));
    
    for adj in &adjustments {
        let mut new_angle = angle1 + adj;
        
        // Normalize to 0-360
        if new_angle < 0.0 {
            new_angle += 360.0;
        } else if new_angle >= 360.0 {
            new_angle -= 360.0;
        }
        
        let (hue_new, code_new) = hue_angle_to_hue(new_angle);
        
        let families = ["", "B", "BG", "G", "GY", "Y", "YR", "R", "RP", "P", "PB"];
        let family = if code_new <= 10 { families[code_new as usize] } else { "?" };
        
        println!("Angle {:.2}° + {:+.1}° = {:.2}° → hue={:.4}, code={} ({})",
                 angle1, adj, new_angle, hue_new, code_new, family);
    }
    
    println!("\n{}", "=".repeat(60));
    println!("Compare with Python:");
    println!("Angle 102.32° → Python: hue=9.9716, code=4 (GY)");
    println!("Angle 102.82° → Python: hue=0.0485, code=3 (G)");
}