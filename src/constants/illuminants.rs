//! Standard illuminant white points and chromaticity coordinates
//! 
//! This module provides CIE standard illuminant data for color space conversion.
//! All values are for CIE 1931 2° Standard Observer.

/// CIE Standard Illuminant A (Incandescent/Tungsten)
pub const ILLUMINANT_A_XYZ: [f64; 3] = [1.09850, 1.00000, 0.35585];
pub const ILLUMINANT_A_CHROMATICITY: [f64; 2] = [0.44757, 0.40745];

/// CIE Standard Illuminant B (Obsolete, noon sunlight)
pub const ILLUMINANT_B_XYZ: [f64; 3] = [0.99072, 1.00000, 0.85223];
pub const ILLUMINANT_B_CHROMATICITY: [f64; 2] = [0.34842, 0.35161];

/// CIE Standard Illuminant C (Average daylight)
pub const ILLUMINANT_C_XYZ: [f64; 3] = [0.98074, 1.00000, 1.18232];
pub const ILLUMINANT_C_CHROMATICITY: [f64; 2] = [0.31006, 0.31616];

/// CIE Standard Illuminant D50 (Horizon light)
pub const ILLUMINANT_D50_XYZ: [f64; 3] = [0.96422, 1.00000, 0.82521];
pub const ILLUMINANT_D50_CHROMATICITY: [f64; 2] = [0.34567, 0.35850];

/// CIE Standard Illuminant D55 (Mid-morning/afternoon)
pub const ILLUMINANT_D55_XYZ: [f64; 3] = [0.95682, 1.00000, 0.92149];
pub const ILLUMINANT_D55_CHROMATICITY: [f64; 2] = [0.33242, 0.34743];

/// CIE Standard Illuminant D65 (Noon daylight)
pub const ILLUMINANT_D65_XYZ: [f64; 3] = [0.95047, 1.00000, 1.08883];
pub const ILLUMINANT_D65_CHROMATICITY: [f64; 2] = [0.31271, 0.32902];

/// CIE Standard Illuminant D75 (North sky daylight)
pub const ILLUMINANT_D75_XYZ: [f64; 3] = [0.94972, 1.00000, 1.22638];
pub const ILLUMINANT_D75_CHROMATICITY: [f64; 2] = [0.29902, 0.31485];

/// CIE Standard Illuminant E (Equal energy)
pub const ILLUMINANT_E_XYZ: [f64; 3] = [1.00000, 1.00000, 1.00000];
pub const ILLUMINANT_E_CHROMATICITY: [f64; 2] = [1.0/3.0, 1.0/3.0];

/// CIE Standard Illuminant F2 (Cool white fluorescent)
pub const ILLUMINANT_F2_XYZ: [f64; 3] = [0.99186, 1.00000, 0.67393];
pub const ILLUMINANT_F2_CHROMATICITY: [f64; 2] = [0.37208, 0.37529];

/// CIE Standard Illuminant F7 (Broadband daylight fluorescent)
pub const ILLUMINANT_F7_XYZ: [f64; 3] = [0.95041, 1.00000, 1.08747];
pub const ILLUMINANT_F7_CHROMATICITY: [f64; 2] = [0.31292, 0.32933];

/// CIE Standard Illuminant F11 (Narrow band white fluorescent)
pub const ILLUMINANT_F11_XYZ: [f64; 3] = [1.00962, 1.00000, 0.64350];
pub const ILLUMINANT_F11_CHROMATICITY: [f64; 2] = [0.38052, 0.37713];

/// Legacy constant for backward compatibility - use ILLUMINANT_C_CHROMATICITY instead
pub const ILLUMINANT_C: [f64; 2] = ILLUMINANT_C_CHROMATICITY;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_illuminant_c_consistency() {
        // Verify backward compatibility
        assert_eq!(ILLUMINANT_C, ILLUMINANT_C_CHROMATICITY);
    }

    #[test]
    fn test_chromaticity_validity() {
        // Test that all chromaticity coordinates are valid (sum <= 1.0)
        let illuminants = [
            ILLUMINANT_A_CHROMATICITY,
            ILLUMINANT_B_CHROMATICITY,
            ILLUMINANT_C_CHROMATICITY,
            ILLUMINANT_D50_CHROMATICITY,
            ILLUMINANT_D55_CHROMATICITY,
            ILLUMINANT_D65_CHROMATICITY,
            ILLUMINANT_D75_CHROMATICITY,
            ILLUMINANT_E_CHROMATICITY,
            ILLUMINANT_F2_CHROMATICITY,
            ILLUMINANT_F7_CHROMATICITY,
            ILLUMINANT_F11_CHROMATICITY,
        ];

        for (i, chromaticity) in illuminants.iter().enumerate() {
            assert!(chromaticity[0] >= 0.0 && chromaticity[0] <= 1.0, 
                "Invalid x coordinate for illuminant {}: {}", i, chromaticity[0]);
            assert!(chromaticity[1] >= 0.0 && chromaticity[1] <= 1.0, 
                "Invalid y coordinate for illuminant {}: {}", i, chromaticity[1]);
            assert!(chromaticity[0] + chromaticity[1] <= 1.0, 
                "Invalid chromaticity sum for illuminant {}: {}", i, chromaticity[0] + chromaticity[1]);
        }
    }

    #[test]
    fn test_xyz_validity() {
        // Test that all XYZ coordinates are positive and Y=1.0
        let illuminants = [
            ILLUMINANT_A_XYZ,
            ILLUMINANT_B_XYZ,
            ILLUMINANT_C_XYZ,
            ILLUMINANT_D50_XYZ,
            ILLUMINANT_D55_XYZ,
            ILLUMINANT_D65_XYZ,
            ILLUMINANT_D75_XYZ,
            ILLUMINANT_E_XYZ,
            ILLUMINANT_F2_XYZ,
            ILLUMINANT_F7_XYZ,
            ILLUMINANT_F11_XYZ,
        ];

        for (i, xyz) in illuminants.iter().enumerate() {
            assert!(xyz[0] > 0.0, "Invalid X coordinate for illuminant {}: {}", i, xyz[0]);
            assert!((xyz[1] - 1.0).abs() < 1e-10, "Y coordinate should be 1.0 for illuminant {}: {}", i, xyz[1]);
            assert!(xyz[2] > 0.0, "Invalid Z coordinate for illuminant {}: {}", i, xyz[2]);
        }
    }
}