//! Standard illuminants and chromatic adaptation
//!
//! This module provides support for various CIE standard illuminants and
//! chromatic adaptation transforms for accurate color space conversion.

use crate::error::{MunsellError, Result};

/// CIE Standard Illuminant
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Illuminant {
    /// CIE Standard Illuminant A (Incandescent/Tungsten)
    A,
    /// CIE Standard Illuminant B (Obsolete, noon sunlight)
    B,
    /// CIE Standard Illuminant C (Average daylight)
    C,
    /// CIE Standard Illuminant D50 (Horizon light)
    D50,
    /// CIE Standard Illuminant D55 (Mid-morning/afternoon)
    D55,
    /// CIE Standard Illuminant D65 (Noon daylight)
    D65,
    /// CIE Standard Illuminant D75 (North sky daylight)
    D75,
    /// CIE Standard Illuminant E (Equal energy)
    E,
    /// CIE Standard Illuminant F2 (Cool white fluorescent)
    F2,
    /// CIE Standard Illuminant F7 (Broadband daylight fluorescent)
    F7,
    /// CIE Standard Illuminant F11 (Narrow band white fluorescent)
    F11,
}

impl Illuminant {
    /// Get the CIE 1931 2° chromaticity coordinates (x, y) for this illuminant
    pub fn chromaticity(&self) -> (f64, f64) {
        match self {
            Illuminant::A => (0.44757, 0.40745),
            Illuminant::B => (0.34842, 0.35161),
            Illuminant::C => (0.31006, 0.31616),
            Illuminant::D50 => (0.34567, 0.35850),
            Illuminant::D55 => (0.33242, 0.34743),
            Illuminant::D65 => (0.31271, 0.32902),
            Illuminant::D75 => (0.29902, 0.31485),
            Illuminant::E => (1.0/3.0, 1.0/3.0),
            Illuminant::F2 => (0.37208, 0.37529),
            Illuminant::F7 => (0.31292, 0.32933),
            Illuminant::F11 => (0.38052, 0.37713),
        }
    }
    
    /// Get the XYZ tristimulus values for this illuminant (normalized Y=1)
    pub fn xyz(&self) -> [f64; 3] {
        let (x, y) = self.chromaticity();
        // Convert xy to XYZ with Y=1
        [
            x / y,           // X
            1.0,             // Y (normalized)
            (1.0 - x - y) / y  // Z
        ]
    }
    
    /// Get the name of this illuminant as a string
    pub fn name(&self) -> &'static str {
        match self {
            Illuminant::A => "A",
            Illuminant::B => "B",
            Illuminant::C => "C",
            Illuminant::D50 => "D50",
            Illuminant::D55 => "D55",
            Illuminant::D65 => "D65",
            Illuminant::D75 => "D75",
            Illuminant::E => "E",
            Illuminant::F2 => "F2",
            Illuminant::F7 => "F7",
            Illuminant::F11 => "F11",
        }
    }
}

impl Default for Illuminant {
    /// Default to D65 (standard for sRGB)
    fn default() -> Self {
        Illuminant::D65
    }
}

/// Chromatic Adaptation Method
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ChromaticAdaptationMethod {
    /// Von Kries transform (simple diagonal scaling)
    VonKries,
    /// Bradford transform (most common, used in ICC profiles)
    Bradford,
    /// CAT02 transform (used in CIECAM02)
    CAT02,
    /// XYZ scaling (simplest method, often inaccurate)
    XYZScaling,
}

impl Default for ChromaticAdaptationMethod {
    /// Default to Bradford (most widely used)
    fn default() -> Self {
        ChromaticAdaptationMethod::Bradford
    }
}

/// Chromatic adaptation transformer
pub struct ChromaticAdaptation;

impl ChromaticAdaptation {
    /// Bradford transformation matrix (RGB primaries to cone response)
    const BRADFORD_MA: [[f64; 3]; 3] = [
        [ 0.8951000,  0.2664000, -0.1614000],
        [-0.7502000,  1.7135000,  0.0367000],
        [ 0.0389000, -0.0685000,  1.0296000],
    ];
    
    /// Bradford inverse transformation matrix
    const BRADFORD_MA_INV: [[f64; 3]; 3] = [
        [ 0.9869929, -0.1470543,  0.1599627],
        [ 0.4323053,  0.5183603,  0.0492912],
        [-0.0085287,  0.0400428,  0.9684867],
    ];
    
    /// Von Kries transformation matrix (Hunt-Pointer-Estevez)
    const VON_KRIES_MA: [[f64; 3]; 3] = [
        [ 0.38971, 0.68898, -0.07868],
        [-0.22981, 1.18340,  0.04641],
        [ 0.00000, 0.00000,  1.00000],
    ];
    
    /// Von Kries inverse transformation matrix
    const VON_KRIES_MA_INV: [[f64; 3]; 3] = [
        [ 1.91019, -1.11214,  0.20195],
        [ 0.37095,  0.62905,  0.00000],
        [ 0.00000,  0.00000,  1.00000],
    ];
    
    /// CAT02 transformation matrix
    const CAT02_MA: [[f64; 3]; 3] = [
        [ 0.7328,  0.4296, -0.1624],
        [-0.7036,  1.6975,  0.0061],
        [ 0.0030,  0.0136,  0.9834],
    ];
    
    /// CAT02 inverse transformation matrix
    const CAT02_MA_INV: [[f64; 3]; 3] = [
        [ 1.0961, -0.2789,  0.1827],
        [ 0.4544,  0.4735,  0.0721],
        [-0.0096, -0.0057,  1.0153],
    ];
    
    /// Perform chromatic adaptation from source to destination illuminant
    pub fn adapt(
        xyz: [f64; 3],
        source: Illuminant,
        destination: Illuminant,
        method: ChromaticAdaptationMethod,
    ) -> Result<[f64; 3]> {
        // If source and destination are the same, no adaptation needed
        if source == destination {
            return Ok(xyz);
        }
        
        // Get the white points
        let source_white = source.xyz();
        let destination_white = destination.xyz();
        
        match method {
            ChromaticAdaptationMethod::XYZScaling => {
                // Simple XYZ scaling
                Ok([
                    xyz[0] * destination_white[0] / source_white[0],
                    xyz[1] * destination_white[1] / source_white[1],
                    xyz[2] * destination_white[2] / source_white[2],
                ])
            }
            ChromaticAdaptationMethod::VonKries => {
                Self::matrix_adaptation(
                    xyz,
                    source_white,
                    destination_white,
                    &Self::VON_KRIES_MA,
                    &Self::VON_KRIES_MA_INV,
                )
            }
            ChromaticAdaptationMethod::Bradford => {
                Self::matrix_adaptation(
                    xyz,
                    source_white,
                    destination_white,
                    &Self::BRADFORD_MA,
                    &Self::BRADFORD_MA_INV,
                )
            }
            ChromaticAdaptationMethod::CAT02 => {
                Self::matrix_adaptation(
                    xyz,
                    source_white,
                    destination_white,
                    &Self::CAT02_MA,
                    &Self::CAT02_MA_INV,
                )
            }
        }
    }
    
    /// Perform matrix-based chromatic adaptation
    fn matrix_adaptation(
        xyz: [f64; 3],
        source_white: [f64; 3],
        destination_white: [f64; 3],
        ma: &[[f64; 3]; 3],
        ma_inv: &[[f64; 3]; 3],
    ) -> Result<[f64; 3]> {
        // Step 1: Transform to cone response domain
        let cone = Self::matrix_multiply(ma, &xyz);
        let cone_source = Self::matrix_multiply(ma, &source_white);
        let cone_dest = Self::matrix_multiply(ma, &destination_white);
        
        // Step 2: Apply scaling in cone response domain
        // Check for zero values to avoid division by zero
        if cone_source[0].abs() < 1e-15 || 
           cone_source[1].abs() < 1e-15 || 
           cone_source[2].abs() < 1e-15 {
            return Err(MunsellError::ConversionError {
                message: "Source white point has zero cone response".to_string(),
            });
        }
        
        let cone_adapted = [
            cone[0] * cone_dest[0] / cone_source[0],
            cone[1] * cone_dest[1] / cone_source[1],
            cone[2] * cone_dest[2] / cone_source[2],
        ];
        
        // Step 3: Transform back to XYZ
        Ok(Self::matrix_multiply(ma_inv, &cone_adapted))
    }
    
    /// Multiply 3x3 matrix with 3D vector
    fn matrix_multiply(matrix: &[[f64; 3]; 3], vector: &[f64; 3]) -> [f64; 3] {
        [
            matrix[0][0] * vector[0] + matrix[0][1] * vector[1] + matrix[0][2] * vector[2],
            matrix[1][0] * vector[0] + matrix[1][1] * vector[1] + matrix[1][2] * vector[2],
            matrix[2][0] * vector[0] + matrix[2][1] * vector[1] + matrix[2][2] * vector[2],
        ]
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_illuminant_chromaticity() {
        // Test known illuminant values
        let d65 = Illuminant::D65.chromaticity();
        assert!((d65.0 - 0.31271).abs() < 1e-5);
        assert!((d65.1 - 0.32902).abs() < 1e-5);
        
        let c = Illuminant::C.chromaticity();
        assert!((c.0 - 0.31006).abs() < 1e-5);
        assert!((c.1 - 0.31616).abs() < 1e-5);
    }
    
    #[test]
    fn test_illuminant_xyz() {
        // Test XYZ calculation
        let xyz = Illuminant::D65.xyz();
        assert!((xyz[1] - 1.0).abs() < 1e-10); // Y should be 1.0
        
        // Check that x/y ratio is preserved
        let (x, y) = Illuminant::D65.chromaticity();
        assert!((xyz[0] - x/y).abs() < 1e-10);
    }
    
    #[test]
    fn test_chromatic_adaptation_identity() {
        // Adapting from an illuminant to itself should return the same values
        let xyz = [0.5, 0.5, 0.5];
        let result = ChromaticAdaptation::adapt(
            xyz,
            Illuminant::D65,
            Illuminant::D65,
            ChromaticAdaptationMethod::Bradford,
        ).unwrap();
        
        assert!((result[0] - xyz[0]).abs() < 1e-10);
        assert!((result[1] - xyz[1]).abs() < 1e-10);
        assert!((result[2] - xyz[2]).abs() < 1e-10);
    }
    
    #[test]
    fn test_chromatic_adaptation_d65_to_c() {
        // Test adaptation from D65 to C
        let xyz = [0.5, 0.5, 0.5];
        let result = ChromaticAdaptation::adapt(
            xyz,
            Illuminant::D65,
            Illuminant::C,
            ChromaticAdaptationMethod::Bradford,
        ).unwrap();
        
        // Result should be different from input
        assert!((result[0] - xyz[0]).abs() > 1e-3);
        assert!((result[2] - xyz[2]).abs() > 1e-3);
    }
}