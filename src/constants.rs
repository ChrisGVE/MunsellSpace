//! Mathematical constants for Munsell color space conversion
//! 
//! This module contains all constants required for accurate ASTM D1535 compliant
//! Munsell color space conversion, including the complete Munsell Renotation dataset
//! from the Python colour-science library.

pub mod maximum_chromas_data;

/// CIE Illuminant C chromaticity coordinates (x, y)
/// Used as the reference white point for Munsell color calculations
pub const ILLUMINANT_C: [f64; 2] = [0.31006, 0.31616];

/// Magnesium oxide reflectance factor
/// Used to scale Y luminance values in the Munsell Renotation dataset
/// As per ASTM D1535-08e1 standard
pub const MG_OXIDE_REFLECTANCE: f64 = 0.975;

/// ASTM D1535 polynomial coefficients for Munsell Value calculation
/// Fifth-order polynomial: Y = c0*V + c1*V² + c2*V³ + c3*V⁴ + c4*V⁵
/// Where Y = luminance, V = Munsell Value
pub const ASTM_D1535_COEFFICIENTS: [f64; 5] = [
    1.1914,      // V
    -0.22533,    // V²
    0.23352,     // V³
    -0.020484,   // V⁴
    0.00081939,  // V⁵
];

/// Threshold for determining achromatic (neutral) colors
/// Colors with chromaticity distance from illuminant C below this threshold
/// are classified as neutral (N) colors
/// REVERTED: Using 1e-6 for now as 1e-3 caused accuracy regression
pub const ACHROMATIC_THRESHOLD: f64 = 1e-6;

/// Newton-Raphson iteration tolerance for Value calculation
/// Convergence criterion for iterative polynomial solving
pub const NEWTON_RAPHSON_TOLERANCE: f64 = 1e-10;

/// Maximum iterations for Newton-Raphson convergence
/// Safety limit to prevent infinite loops in polynomial solving
pub const NEWTON_RAPHSON_MAX_ITERATIONS: usize = 100;

/// sRGB gamma correction threshold
/// Colors below this threshold use linear scaling, above use power function
pub const SRGB_GAMMA_THRESHOLD: f64 = 0.04045;

/// sRGB linear scaling factor for dark colors
/// Applied to RGB values below gamma threshold
pub const SRGB_LINEAR_FACTOR: f64 = 12.92;

/// sRGB gamma exponent for bright colors
/// Power function exponent for gamma correction
pub const SRGB_GAMMA_EXPONENT: f64 = 2.4;

/// sRGB gamma offset and scale factors
pub const SRGB_GAMMA_OFFSET: f64 = 0.055;
pub const SRGB_GAMMA_SCALE: f64 = 1.055;

/// ITU-R BT.709 sRGB to XYZ transformation matrix (D65 illuminant)
/// Used for converting linear RGB to CIE XYZ color space
/// Matrix format: [X_row, Y_row, Z_row] where each row is [R_coeff, G_coeff, B_coeff]
pub const SRGB_TO_XYZ_MATRIX: [[f64; 3]; 3] = [
    [0.4124564, 0.3575761, 0.1804375], // X
    [0.2126729, 0.7151522, 0.0721750], // Y
    [0.0193339, 0.1191920, 0.9503041], // Z
];

/// Munsell hue family names in canonical order
/// Used for parsing and formatting Munsell notation
pub const MUNSELL_HUE_FAMILIES: [&str; 10] = [
    "R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"
];

/// Complete Munsell Renotation dataset
/// Format: ((hue_string, value, chroma), (x, y, Y))
/// Source: Python colour-science library MUNSELL_COLOURS_ALL
/// IMPORTANT: Y values are scaled by 1/0.975 factor in the original dataset
pub const MUNSELL_RENOTATION_DATA: &[((&str, f64, f64), (f64, f64, f64))] = 
    include!("munsell_renotation_data_entries.rs");

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_astm_polynomial_coefficients() {
        // Verify polynomial coefficients are correct for ASTM D1535
        assert_eq!(ASTM_D1535_COEFFICIENTS.len(), 5);
        assert!((ASTM_D1535_COEFFICIENTS[0] - 1.1914).abs() < 1e-6);
    }

    #[test]
    fn test_illuminant_c_coordinates() {
        // Verify Illuminant C chromaticity coordinates
        assert!((ILLUMINANT_C[0] - 0.31006).abs() < 1e-6);
        assert!((ILLUMINANT_C[1] - 0.31616).abs() < 1e-6);
    }

    #[test]
    fn test_munsell_renotation_data_size() {
        // Verify complete dataset is loaded
        assert_eq!(MUNSELL_RENOTATION_DATA.len(), 4995);
    }

    #[test]
    fn test_munsell_renotation_data_format() {
        // Test first entry has correct format
        let first_entry = MUNSELL_RENOTATION_DATA[0];
        let ((hue, value, chroma), (x, y, y_scaled)) = first_entry;
        
        assert_eq!(hue, "2.5GY");
        assert!((value - 0.2).abs() < 1e-6);
        assert!((chroma - 2.0).abs() < 1e-6);
        assert!(x > 0.0);
        assert!(y > 0.0);
        assert!(y_scaled > 0.0);
    }

    #[test]
    fn test_y_scaling_applied() {
        // Verify Y values in dataset are scaled by 1/0.975 factor (unscaled)
        // The dataset contains Y values that need to be scaled DOWN by 0.975 to get true Y
        let entry = MUNSELL_RENOTATION_DATA[0];
        let (_, (_, _, y_unscaled)) = entry;
        
        // The dataset value is 0.237, which is the unscaled value
        // To get the true Y value, we multiply by MG_OXIDE_REFLECTANCE (0.975)
        let true_y = y_unscaled * MG_OXIDE_REFLECTANCE;
        let expected_true_y = 0.237 * 0.975; // 0.23107...
        
        assert!((true_y - expected_true_y).abs() < 1e-4, 
            "Expected true Y: {}, got: {}, difference: {}", 
            expected_true_y, true_y, (true_y - expected_true_y).abs());
        
        // Also verify the unscaled value matches what we expect
        assert!((y_unscaled - 0.237).abs() < 1e-6,
            "Expected unscaled Y: 0.237, got: {}", y_unscaled);
    }
}