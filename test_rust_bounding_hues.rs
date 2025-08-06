// Test to compare Rust and Python bounding hues

pub fn bounding_hues_from_renotation_python_exact(hue: f64, code: u8) -> ((f64, u8), (f64, u8)) {
    // Exact 1:1 port from Python colour-science
    let mut hue_cw: f64;
    let mut code_cw: u8;
    let hue_ccw: f64;
    let code_ccw: u8;
    
    // Check if hue is multiple of 2.5
    if (hue % 2.5).abs() < 1e-10 {
        if hue.abs() < 1e-10 {
            // hue == 0
            hue_cw = 10.0;
            // Python: code_cw = (code + 1) % 10
            let mut temp_code = ((code as i32 + 1) % 10) as u8;
            // Python: if code_cw == 0: code_cw = 10
            if temp_code == 0 {
                temp_code = 10;
            }
            code_cw = temp_code;
        } else {
            hue_cw = hue;
            code_cw = code;
        }
        hue_ccw = hue_cw;
        code_ccw = code_cw;
    } else {
        // Non-standard hue
        hue_cw = 2.5 * (hue / 2.5).floor();
        let mut temp_hue_ccw = (hue_cw + 2.5) % 10.0;
        if temp_hue_ccw.abs() < 1e-10 {
            temp_hue_ccw = 10.0;
        }
        hue_ccw = temp_hue_ccw;
        
        if hue_cw.abs() < 1e-10 {
            hue_cw = 10.0;
            // Python: code_cw = (code + 1) % 10
            let mut temp_code = ((code as i32 + 1) % 10) as u8;
            // Python: if code_cw == 0: code_cw = 10
            if temp_code == 0 {
                temp_code = 10;
            }
            code_cw = temp_code;
        } else {
            code_cw = code;
        }
        code_ccw = code;
    }
    
    ((hue_cw, code_cw), (hue_ccw, code_ccw))
}

fn main() {
    let test_cases = [
        (0.0, 1),   // B family, hue=0
        (0.0, 2),   // BG family, hue=0
        (0.0, 3),   // G family, hue=0
        (0.0, 4),   // GY family, hue=0
        (0.0, 5),   // Y family, hue=0
        (0.0, 6),   // YR family, hue=0
        (0.0, 7),   // R family, hue=0
        (0.0, 8),   // RP family, hue=0
        (0.0, 9),   // P family, hue=0
        (0.0, 10),  // PB family, hue=0
        (1.3, 5),   // Y family, non-standard hue
    ];
    
    println!("Rust bounding_hues_from_renotation results:");
    println!("=" .repeat(60));
    
    for (hue, code) in test_cases {
        let ((hue_cw, code_cw), (hue_ccw, code_ccw)) = 
            bounding_hues_from_renotation_python_exact(hue, code);
        
        println!("Input: hue={:.1}, code={}", hue, code);
        println!("  CW:  hue={:.1}, code={}", hue_cw, code_cw);
        println!("  CCW: hue={:.1}, code={}", hue_ccw, code_ccw);
        
        if hue == 0.0 {
            let next = ((code as i32 + 1) % 10) as u8;
            let adjusted = if next == 0 { 10 } else { next };
            println!("  -> Rust: (code + 1) % 10 = {}, adjusted to {}", next, adjusted);
        }
        println!();
    }
}