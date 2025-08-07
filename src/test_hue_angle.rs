#[cfg(test)]
mod tests {
    use crate::python_port::hue_angle_to_hue;

    #[test]
    fn test_hue_angle_to_hue_alignment() {
        // Test angles and expected results from Python
        let test_cases = vec![
            (0.0, 5.0, 7),    // R
            (30.0, 8.3, 6),   // YR
            (45.0, 5.0, 5),   // Y
            (60.0, 1.0, 4),   // GY
            (70.0, 5.0, 4),   // GY
            (90.0, 8.1, 4),   // GY
            (120.0, 2.7, 3),  // G
            (135.0, 5.0, 3),  // G
            (150.0, 1.0, 2),  // BG
            (160.0, 5.0, 2),  // BG
            (180.0, 8.1, 2),  // BG
            (210.0, 2.7, 1),  // B
            (225.0, 5.0, 1),  // B
            (240.0, 5.0, 10), // PB
            (255.0, 5.0, 9),  // P
            (270.0, 7.5, 9),  // P
            (300.0, 2.5, 8),  // RP
            (315.0, 5.0, 8),  // RP
            (330.0, 8.3, 8),  // RP
            (360.0, 5.0, 7),  // R
        ];
        
        let hue_codes = vec!["", "B", "BG", "G", "GY", "Y", "YR", "R", "RP", "P", "PB"];
        
        for (angle, expected_hue, expected_code) in test_cases {
            let (hue, code) = hue_angle_to_hue(angle);
            println!("Angle {:3.0}° -> Rust: {:.1} {} ({}), Expected: {:.1} {} ({})",
                     angle, hue, code, hue_codes[code as usize],
                     expected_hue, expected_code, hue_codes[expected_code as usize]);
            
            assert!((hue - expected_hue).abs() < 0.1, 
                    "Angle {}: hue mismatch: {} vs {}", angle, hue, expected_hue);
            assert_eq!(code, expected_code, 
                       "Angle {}: code mismatch: {} vs {}", angle, code, expected_code);
        }
    }
}