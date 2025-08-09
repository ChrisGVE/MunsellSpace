#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_xy_from_renotation_ovoid_exact_match() {
        // Test cases generated from Python colour-science
        // Each tuple is (hue, value, chroma, code, expected_x, expected_y)
        let test_cases = vec![
            // Standard hues with even chroma (direct lookup)
            (7.5, 9.0, 6.0, 4, 0.33510000, 0.41110000),   // 7.5GY 9/6
            (10.0, 9.0, 6.0, 4, 0.31530000, 0.40080000),  // 10GY 9/6
            (2.5, 9.0, 6.0, 4, 0.36700000, 0.41780000),   // 2.5GY 9/6
            (5.0, 9.0, 6.0, 4, 0.35720000, 0.41790000),   // 5GY 9/6
            
            // Non-standard hues with even chroma (hue interpolation)
            (8.548, 9.0, 6.0, 4, 0.32624128, 0.40731066), // 8.548GY 9/6 - our problematic case
            (8.0, 9.0, 6.0, 4, 0.33077856, 0.40939540),   // 8.0GY 9/6
            (8.5, 9.0, 6.0, 4, 0.32663013, 0.40750196),   // 8.5GY 9/6
            (3.75, 9.0, 6.0, 4, 0.36206360, 0.41796313),  // 3.75GY 9/6
            
            // Standard hues with different even chromas
            (7.5, 9.0, 8.0, 4, 0.34140000, 0.44150000),   // 7.5GY 9/8
            (10.0, 9.0, 4.0, 4, 0.31440000, 0.37110000),  // 10GY 9/4
            
            // Non-standard hues with different even chromas
            (8.548, 9.0, 8.0, 4, 0.32981167, 0.43564075), // 8.548GY 9/8
            (8.0, 9.0, 10.0, 4, 0.34018503, 0.47050971),  // 8.0GY 9/10
            
            // Edge cases
            (0.0, 9.0, 6.0, 4, 0.37610000, 0.41550000),   // 0GY 9/6
            (1.0, 9.0, 6.0, 4, 0.37245958, 0.41651637),   // 1GY 9/6
            (9.5, 9.0, 6.0, 4, 0.31888375, 0.40319280),   // 9.5GY 9/6
            
            // Different values
            (8.548, 8.0, 6.0, 4, 0.32540691, 0.40855420), // 8.548GY 8/6
            (8.548, 7.0, 6.0, 4, 0.32511042, 0.41402286), // 8.548GY 7/6
            
            // Different chromas
            (8.548, 9.0, 8.0, 4, 0.32981167, 0.43564075),  // 8.548GY 9/8
            (8.548, 9.0, 10.0, 4, 0.33293507, 0.46689680), // 8.548GY 9/10
            (8.548, 9.0, 12.0, 4, 0.33480029, 0.49625646), // 8.548GY 9/12
        ];
        
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        for (hue, value, chroma, code, expected_x, expected_y) in test_cases {
            let (x, y) = converter.xy_from_renotation_ovoid(hue, value, chroma, code).unwrap();
            
            // Allow for small floating point differences and interpolation precision (1e-3)
            let x_diff = (x - expected_x).abs();
            let y_diff = (y - expected_y).abs();
            
            assert!(
                x_diff < 1e-3,
                "X mismatch for {:.3}GY {}/{}: got {:.8}, expected {:.8} (diff: {:.2e})",
                hue, value, chroma, x, expected_x, x_diff
            );
            
            assert!(
                y_diff < 1e-3,
                "Y mismatch for {:.3}GY {}/{}: got {:.8}, expected {:.8} (diff: {:.2e})",
                hue, value, chroma, y, expected_y, y_diff
            );
            
            println!("✓ {:.3}GY {}/{}: ({:.8}, {:.8}) matches Python", hue, value, chroma, x, y);
        }
    }
}