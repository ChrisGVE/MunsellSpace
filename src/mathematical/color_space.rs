//! Color space transformations: sRGB → XYZ → xyY, chromatic adaptation.

use palette::{Srgb, Xyz, convert::IntoColor, white_point::D65};

use crate::constants::*;
use crate::error::{MunsellError, Result};

use super::types::{Illuminant, CieXyY, MunsellSpecification};
use super::MathematicalMunsellConverter;

impl MathematicalMunsellConverter {
    /// Convert sRGB color to Munsell specification using mathematical algorithms.
    ///
    /// # Arguments
    /// * `rgb` - sRGB color as [R, G, B] with values 0-255
    ///
    /// # Returns
    /// * `MunsellSpecification` with hue, value, chroma, and family
    ///
    /// # Example
    /// ```rust
    /// use munsellspace::MathematicalMunsellConverter;
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let converter = MathematicalMunsellConverter::new()?;
    /// let munsell = converter.srgb_to_munsell([255, 0, 0])?;
    /// println!("Red: {}.{} {:.1}/{:.1}", munsell.hue, munsell.family, munsell.value, munsell.chroma);
    /// # Ok(())
    /// # }
    /// ```
    pub fn srgb_to_munsell(&self, rgb: [u8; 3]) -> Result<MunsellSpecification> {
        // Step 1: Convert sRGB to xyY using palette crate
        let xyy = self.srgb_to_xyy(rgb)?;

        // Step 2: Convert xyY to Munsell specification using mathematical algorithm
        self.xyy_to_munsell_specification(xyy)
    }

    /// Convert sRGB to CIE xyY color space with optional chromatic adaptation.
    pub fn srgb_to_xyy(&self, rgb: [u8; 3]) -> Result<CieXyY> {
        // Create sRGB color with normalized values [0.0, 1.0]
        let rgb_norm = [
            rgb[0] as f64 / 255.0,
            rgb[1] as f64 / 255.0,
            rgb[2] as f64 / 255.0,
        ];

        let srgb = Srgb::new(rgb_norm[0], rgb_norm[1], rgb_norm[2]);

        // Convert sRGB → Linear RGB
        let linear_rgb = srgb.into_linear();

        // Convert Linear RGB → XYZ (source illuminant)
        let xyz_source: Xyz<D65, f64> = linear_rgb.into_color();
        let (x_src, y_src, z_src) = xyz_source.into_components();
        let xyz_src = [x_src, y_src, z_src];

        // Apply chromatic adaptation if needed
        let xyz_adapted = if self.source_illuminant == self.target_illuminant {
            xyz_src
        } else {
            self.chromatic_adaptation(xyz_src, self.source_illuminant, self.target_illuminant)?
        };

        // Convert XYZ to xyY
        let xyy = self.xyz_to_xyy(xyz_adapted);

        Ok(xyy)
    }

    /// Perform chromatic adaptation between illuminants.
    pub(super) fn chromatic_adaptation(
        &self, xyz: [f64; 3], source: Illuminant, target: Illuminant,
    ) -> Result<[f64; 3]> {
        match self.adaptation_method {
            super::types::ChromaticAdaptation::XYZScaling => {
                let source_wp = source.white_point();
                let target_wp = target.white_point();

                if source_wp[0].abs() < 1e-15 || source_wp[1].abs() < 1e-15 || source_wp[2].abs() < 1e-15 {
                    return Err(MunsellError::ConvergenceFailed);
                }

                Ok([
                    xyz[0] * target_wp[0] / source_wp[0],
                    xyz[1] * target_wp[1] / source_wp[1],
                    xyz[2] * target_wp[2] / source_wp[2],
                ])
            }
            super::types::ChromaticAdaptation::Bradford => {
                self.bradford_adaptation(xyz, source, target)
            }
            super::types::ChromaticAdaptation::CAT02 => {
                self.cat02_adaptation(xyz, source, target)
            }
        }
    }

    /// Bradford chromatic adaptation transform.
    fn bradford_adaptation(
        &self, xyz: [f64; 3], source: Illuminant, target: Illuminant,
    ) -> Result<[f64; 3]> {
        let source_wp = source.white_point();
        let target_wp = target.white_point();

        let cone_src = self.matrix_multiply_3x3(&BRADFORD_MATRIX, &xyz);
        let cone_src_wp = self.matrix_multiply_3x3(&BRADFORD_MATRIX, &source_wp);
        let cone_tgt_wp = self.matrix_multiply_3x3(&BRADFORD_MATRIX, &target_wp);

        if cone_src_wp[0].abs() < 1e-15 || cone_src_wp[1].abs() < 1e-15 || cone_src_wp[2].abs() < 1e-15 {
            return Err(MunsellError::ConvergenceFailed);
        }

        let cone_adapted = [
            cone_src[0] * cone_tgt_wp[0] / cone_src_wp[0],
            cone_src[1] * cone_tgt_wp[1] / cone_src_wp[1],
            cone_src[2] * cone_tgt_wp[2] / cone_src_wp[2],
        ];

        Ok(self.matrix_multiply_3x3(&BRADFORD_MATRIX_INV, &cone_adapted))
    }

    /// CAT02 chromatic adaptation transform.
    fn cat02_adaptation(
        &self, xyz: [f64; 3], source: Illuminant, target: Illuminant,
    ) -> Result<[f64; 3]> {
        let source_wp = source.white_point();
        let target_wp = target.white_point();

        let cat_src = self.matrix_multiply_3x3(&CAT02_MATRIX, &xyz);
        let cat_src_wp = self.matrix_multiply_3x3(&CAT02_MATRIX, &source_wp);
        let cat_tgt_wp = self.matrix_multiply_3x3(&CAT02_MATRIX, &target_wp);

        if cat_src_wp[0].abs() < 1e-15 || cat_src_wp[1].abs() < 1e-15 || cat_src_wp[2].abs() < 1e-15 {
            return Err(MunsellError::ConvergenceFailed);
        }

        let cat_adapted = [
            cat_src[0] * cat_tgt_wp[0] / cat_src_wp[0],
            cat_src[1] * cat_tgt_wp[1] / cat_src_wp[1],
            cat_src[2] * cat_tgt_wp[2] / cat_src_wp[2],
        ];

        Ok(self.matrix_multiply_3x3(&CAT02_MATRIX_INV, &cat_adapted))
    }

    /// Convert XYZ to xyY coordinates.
    pub(super) fn xyz_to_xyy(&self, xyz: [f64; 3]) -> CieXyY {
        let sum = xyz[0] + xyz[1] + xyz[2];

        if sum < 1e-15 {
            CieXyY { x: 0.0, y: 0.0, y_luminance: xyz[1] }
        } else {
            CieXyY {
                x: xyz[0] / sum,
                y: xyz[1] / sum,
                y_luminance: xyz[1],
            }
        }
    }

    /// Multiply 3x3 matrix with 3D vector.
    pub(super) fn matrix_multiply_3x3(&self, matrix: &[[f64; 3]; 3], vector: &[f64; 3]) -> [f64; 3] {
        [
            matrix[0][0] * vector[0] + matrix[0][1] * vector[1] + matrix[0][2] * vector[2],
            matrix[1][0] * vector[0] + matrix[1][1] * vector[1] + matrix[1][2] * vector[2],
            matrix[2][0] * vector[0] + matrix[2][1] * vector[1] + matrix[2][2] * vector[2],
        ]
    }
}
