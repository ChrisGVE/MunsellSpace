// Test to compare the two hue_to_astm_hue formulas

// BREAKTHROUGH VERSION (60.4% accuracy)
fn hue_to_astm_hue_breakthrough(hue: f64, code: u8) -> f64 {
    // Calculate single_hue following exact Python formula
    // CRITICAL: Use 17.0 as in Python, and handle modulo correctly!
    let raw = ((17.0 - code as f64) % 10.0 + (hue / 10.0) - 0.5);
    // Python-style modulo: always returns positive result
    let single_hue = if raw < 0.0 {
        (raw % 10.0 + 10.0) % 10.0
    } else {
        raw % 10.0
    };
    
    // Linear interpolation with exact breakpoints from Python
    linear_interpolate_hue_angle(single_hue)
}

// Linear interpolation function needed by breakthrough version
fn linear_interpolate_hue_angle(single_hue: f64) -> f64 {
    // Exact breakpoints from Python colour-science
    // Maps single_hue to hue_angle
    let x = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0];
    let y = [0.0, 10.83, 20.37, 28.30, 37.20, 44.98, 54.55, 64.35, 74.20, 83.75, 100.0];
    
    // Find interpolation points
    for i in 0..10 {
        if single_hue >= x[i] && single_hue <= x[i+1] {
            let t = (single_hue - x[i]) / (x[i+1] - x[i]);
            return y[i] + t * (y[i+1] - y[i]);
        }
    }
    
    // Handle boundary cases
    if single_hue < 0.0 { y[0] } else { y[10] }
}

// CURRENT VERSION (regressed accuracy)
fn hue_to_astm_hue_current(hue: f64, code: u8) -> f64 {
    let astm_hue = 10.0 * (((7 - code as i32) % 10) as f64) + hue;
    
    // Return 100 if ASTM_hue == 0, else ASTM_hue
    if astm_hue == 0.0 {
        100.0
    } else {
        astm_hue
    }
}

fn main() {
    println!("Testing hue_to_astm_hue formula differences\n");
    println!("BREAKTHROUGH (60.4%) vs CURRENT (regressed)\n");
    
    // Test cases with different hue/code combinations
    let test_cases = [
        (5.0, 6),  // 5R
        (2.5, 6),  // 2.5R
        (7.5, 5),  // 7.5YR
        (10.0, 1), // 10B
        (5.0, 3),  // 5G
        (0.0, 7),  // 10RP (boundary case)
        (1.0, 6),  // 1R (very red)
        (9.0, 6),  // 9R (almost RP)
    ];
    
    for (hue, code) in test_cases {
        let breakthrough = hue_to_astm_hue_breakthrough(hue, code);
        let current = hue_to_astm_hue_current(hue, code);
        let diff = (breakthrough - current).abs();
        
        println!("hue={:.1}, code={} : breakthrough={:.2}, current={:.2}, diff={:.2}",
                 hue, code, breakthrough, current, diff);
    }
}