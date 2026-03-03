//! ASTM D1535 polynomial value computation and Munsell notation formatting.

use crate::constants::*;
use crate::error::{MunsellError, Result};

use super::types::{MunsellSpecification, CieXyY};
use super::MathematicalMunsellConverter;

impl MathematicalMunsellConverter {
    /// Calculate Munsell Value from CIE Y luminance using ASTM D1535 polynomial.
    ///
    /// Uses Newton-Raphson iteration to solve the fifth-order polynomial:
    /// Y = 1.1914*V - 0.22533*V² + 0.23352*V³ - 0.020484*V⁴ + 0.00081939*V⁵
    pub(super) fn luminance_to_munsell_value(&self, y: f64) -> Result<f64> {
        if y <= 0.0 {
            return Ok(0.0);
        }

        // Convert Y from [0,1] scale to [0,100] scale for ASTM polynomial
        let y_scaled = y * 100.0;

        if y_scaled >= 100.0 {
            return Ok(10.0);
        }

        // Newton-Raphson iteration to solve for V given Y
        let mut v = 10.0 * y.sqrt(); // Initial guess

        for _ in 0..NEWTON_RAPHSON_MAX_ITERATIONS {
            let f = self.astm_polynomial(v) - y_scaled;
            let df = self.astm_polynomial_derivative(v);

            if df.abs() < 1e-15 {
                return Err(MunsellError::ConvergenceFailed);
            }

            let delta = f / df;
            v -= delta;

            if delta.abs() < NEWTON_RAPHSON_TOLERANCE {
                return Ok(v.max(0.0).min(10.0));
            }
        }

        Err(MunsellError::ConvergenceFailed)
    }

    /// ASTM D1535 fifth-order polynomial for Munsell Value.
    pub(super) fn astm_polynomial(&self, v: f64) -> f64 {
        let coeffs = &ASTM_D1535_COEFFICIENTS;
        coeffs[0] * v +
        coeffs[1] * v * v +
        coeffs[2] * v * v * v +
        coeffs[3] * v * v * v * v +
        coeffs[4] * v * v * v * v * v
    }

    /// Derivative of ASTM D1535 polynomial for Newton-Raphson iteration.
    pub(super) fn astm_polynomial_derivative(&self, v: f64) -> f64 {
        let coeffs = &ASTM_D1535_COEFFICIENTS;
        coeffs[0] +
        2.0 * coeffs[1] * v +
        3.0 * coeffs[2] * v * v +
        4.0 * coeffs[3] * v * v * v +
        5.0 * coeffs[4] * v * v * v * v
    }

    /// Convert Munsell Value to CIE Y luminance using ASTM polynomial directly.
    pub(super) fn munsell_value_to_luminance(&self, value: f64) -> Result<f64> {
        if value < 0.0 || value > 10.0 {
            return Err(MunsellError::InvalidNotation {
                notation: value.to_string(),
                reason: "Munsell Value must be between 0.0 and 10.0".to_string(),
            });
        }

        // ASTM polynomial gives Y on [0,100] scale, convert to [0,1] scale
        Ok(self.astm_polynomial(value) / 100.0)
    }

    /// Convert Munsell specification back to xyY coordinates.
    ///
    /// This implements the reverse conversion for bidirectional capability.
    pub fn munsell_specification_to_xyy(&self, spec: &MunsellSpecification) -> Result<CieXyY> {
        // Handle neutral colors
        if spec.family == "N" {
            let y = self.munsell_value_to_luminance(spec.value)?;
            return Ok(CieXyY {
                x: ILLUMINANT_C[0],
                y: ILLUMINANT_C[1],
                y_luminance: y,
            });
        }

        // For chromatic colors, find matching entry in renotation data
        let hue_str = format!("{}{}", spec.hue, spec.family);

        for entry in self.renotation_data {
            let ((entry_hue, entry_value, entry_chroma), (x, y, luma)) = entry;

            if entry_hue == &hue_str &&
               (entry_value - spec.value).abs() < 0.1 &&
               (entry_chroma - spec.chroma).abs() < 0.1 {
                return Ok(CieXyY { x: *x, y: *y, y_luminance: *luma });
            }
        }

        Err(MunsellError::InterpolationError {
            message: format!("No matching renotation data for {}{} {:.1}/{:.1}",
                spec.hue, spec.family, spec.value, spec.chroma),
        })
    }

    /// Convert Munsell specification to formatted notation string.
    pub fn format_munsell_notation(&self, spec: &MunsellSpecification) -> String {
        if spec.family == "N" {
            format!("N {:.1}", spec.value)
        } else {
            format!("{:.1}{} {:.1}/{:.1}", spec.hue, spec.family, spec.value, spec.chroma)
        }
    }
}
