// Test hue_angle_to_hue function
use munsellspace::python_port::hue_angle_to_hue;

fn main() {
    let angles = vec![85.0, 90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 116.9, 120.0, 125.0];
    
    for angle in angles {
        let (hue, code) = hue_angle_to_hue(angle);
        let families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
        let family = if code >= 1 && code <= 10 { families[(code - 1) as usize] } else { "??" };
        println!("Angle {:5.1}° => hue={:5.2} code={} ({})", angle, hue, code, family);
    }
}