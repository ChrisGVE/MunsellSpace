use munsellspace::python_port::hue_to_hue_angle;

fn main() {
    // Test the exact values from the trace
    let hue = 5.2417998371; // Slightly different from Python due to float precision
    let code = 3;
    
    let result = hue_to_hue_angle(hue, code);
    println!("Rust hue_to_hue_angle({}, {}) = {}", hue, code, result);
    
    // Manual calculation
    let raw = (17.0 - code as f64) % 10.0 + (hue / 10.0) - 0.5;
    println!("raw = (17 - {}) % 10 + ({} / 10) - 0.5 = {}", code, hue, raw);
    
    let single_hue = if raw < 0.0 {
        (raw % 10.0) + 10.0
    } else {
        raw % 10.0
    };
    println!("single_hue = {}", single_hue);
    
    // Find interpolation segment
    let breakpoints = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0];
    let angles = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0];
    
    for i in 0..breakpoints.len()-1 {
        if single_hue >= breakpoints[i] && single_hue <= breakpoints[i+1] {
            let t = (single_hue - breakpoints[i]) / (breakpoints[i+1] - breakpoints[i]);
            let angle = angles[i] + t * (angles[i+1] - angles[i]);
            println!("Interpolation: segment [{}, {}], t={:.6}", breakpoints[i], breakpoints[i+1], t);
            println!("angle = {} + {:.6} * ({} - {}) = {}", angles[i], t, angles[i+1], angles[i], angle);
            break;
        }
    }
    
    // Test with Python's exact value
    let hue_exact = 5.2417998370553125;
    let result_exact = hue_to_hue_angle(hue_exact, code);
    println!("\nWith Python's exact value:");
    println!("Rust hue_to_hue_angle({}, {}) = {}", hue_exact, code, result_exact);
    
    // Also test the cases that appear in the trace where Python returns 135.0
    println!("\n=== Testing values that should return exactly 135.0 ===");
    // If single_hue = 4.0 exactly, it should return 135.0
    // Working backwards: single_hue = 4.0
    // 4.0 = (17 - code) % 10 + (hue / 10) - 0.5
    // For code = 3: 4.0 = 4 + (hue/10) - 0.5
    // hue/10 = 0.5, so hue = 5.0
    
    let test_hue = 5.0;
    let test_code = 3;
    let test_result = hue_to_hue_angle(test_hue, test_code);
    println!("hue_to_hue_angle({}, {}) = {}", test_hue, test_code, test_result);
}