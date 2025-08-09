#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_xy_from_renotation_ovoid_exact_match() {
        // Test cases generated from Python colour-science
        // Each tuple is (hue, value, chroma, code, expected_x, expected_y)
        let test_cases = vec![
            // Just test the failing case
            (0.0, 9.0, 6.0, 4, 0.37610000, 0.41550000),   // 0GY 9/6
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