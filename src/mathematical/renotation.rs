//! Munsell Renotation dataset lookup and interpolation methods.

use crate::constants::*;
use crate::error::{MunsellError, Result};

use super::coordinate_transforms;
use super::hue_conversions;
use super::MathematicalMunsellConverter;

impl MathematicalMunsellConverter {
    /// Linear interpolation helper function.
    pub(super) fn linear_interpolate(
        &self, x_values: &[f64], y_values: &[f64], x_target: f64,
    ) -> Result<f64> {
        if x_values.len() != y_values.len() || x_values.len() < 2 {
            return Err(MunsellError::InterpolationError {
                message: "Invalid data for interpolation".to_string()
            });
        }

        // Find the two closest x values that bracket x_target
        let mut best_result = y_values[0];
        let mut best_distance = (x_values[0] - x_target).abs();

        for i in 0..x_values.len()-1 {
            let x1 = x_values[i];
            let x2 = x_values[i+1];
            let y1 = y_values[i];
            let y2 = y_values[i+1];

            if (x1 <= x_target && x_target <= x2) || (x2 <= x_target && x_target <= x1) {
                if (x2 - x1).abs() < 1e-10 {
                    return Ok(y1);
                }
                let t = (x_target - x1) / (x2 - x1);
                return Ok(y1 + t * (y2 - y1));
            }

            let distance = (x1 - x_target).abs();
            if distance < best_distance {
                best_distance = distance;
                best_result = y1;
            }
        }

        // Check last point
        let last_idx = x_values.len() - 1;
        let distance = (x_values[last_idx] - x_target).abs();
        if distance < best_distance {
            best_result = y_values[last_idx];
        }

        // Match np.interp behavior - CLAMP to boundaries
        if x_values.len() >= 2 {
            let mut indices: Vec<usize> = (0..x_values.len()).collect();
            indices.sort_by(|&i, &j| x_values[i].partial_cmp(&x_values[j]).unwrap());

            let sorted_x: Vec<f64> = indices.iter().map(|&i| x_values[i]).collect();
            let sorted_y: Vec<f64> = indices.iter().map(|&i| y_values[i]).collect();

            let first_x = sorted_x[0];
            let last_x = sorted_x[sorted_x.len() - 1];

            if x_target <= first_x {
                return Ok(sorted_y[0]);
            } else if x_target >= last_x {
                return Ok(sorted_y[sorted_y.len() - 1]);
            }
        }

        Ok(best_result)
    }

    /// Calculate maximum chroma from renotation data.
    pub(super) fn maximum_chroma_from_renotation(
        &self, _hue: f64, value: f64, code: u8,
    ) -> Result<f64> {
        let family = hue_conversions::code_to_family(code);
        let value_rounded = (value * 2.0).round() / 2.0;
        let mut max_chroma = 0.0;

        for entry in self.renotation_data.iter() {
            let ((hue_str, entry_value, entry_chroma), _) = entry;

            let entry_family = hue_str.chars()
                .skip_while(|c| c.is_numeric() || *c == '.')
                .collect::<String>();

            if entry_family != family { continue; }
            if (entry_value - value_rounded).abs() > 0.25 { continue; }

            if *entry_chroma > max_chroma {
                max_chroma = *entry_chroma;
            }
        }

        if max_chroma < 0.1 {
            max_chroma = match value as i32 {
                0..=2 => 10.0,
                3..=5 => 15.0,
                6..=8 => 20.0,
                9..=10 => 10.0,
                _ => 8.0,
            };
        }

        Ok(max_chroma)
    }

    /// Convert Munsell specification to xy coordinates using interpolation.
    /// Implements Python's _munsell_specification_to_xyY logic for value interpolation.
    pub(super) fn munsell_specification_to_xy(
        &self, hue: f64, value: f64, chroma: f64, code: u8,
    ) -> Result<(f64, f64)> {
        let is_integer = (value - value.round()).abs() < 1e-10;

        if is_integer {
            self.xy_from_renotation_ovoid(hue, value.round(), chroma, code)
        } else {
            let value_minus = value.floor();
            let value_plus = value_minus + 1.0;

            let (x_minus, y_minus) = self.xy_from_renotation_ovoid(hue, value_minus, chroma, code)?;

            let (x_plus, y_plus) = if value_plus >= 10.0 {
                (x_minus, y_minus)
            } else {
                self.xy_from_renotation_ovoid(hue, value_plus, chroma, code)?
            };

            if value_minus == value_plus || (x_minus == x_plus && y_minus == y_plus) {
                Ok((x_minus, y_minus))
            } else {
                let y_minus_lum = self.munsell_value_to_luminance(value_minus)?;
                let y_plus_lum = self.munsell_value_to_luminance(value_plus)?;
                let y_actual = self.munsell_value_to_luminance(value)?;

                let t = (y_actual - y_minus_lum) / (y_plus_lum - y_minus_lum);
                let x = x_minus + t * (x_plus - x_minus);
                let y = y_minus + t * (y_plus - y_minus);

                Ok((x, y))
            }
        }
    }

    /// Direct lookup from renotation data.
    fn lookup_xy_from_renotation(
        &self, hue: f64, value: f64, chroma: f64, code: u8,
    ) -> Result<(f64, f64)> {
        if chroma.abs() < 1e-10 {
            return Ok((ILLUMINANT_C[0], ILLUMINANT_C[1]));
        }

        let family = hue_conversions::code_to_family(code);
        let hue_str = format!("{}{}", hue, family);

        for entry in self.renotation_data {
            let ((entry_hue, entry_value, entry_chroma), (x, y, _)) = entry;
            if *entry_hue == hue_str &&
               (entry_value - value).abs() < 0.01 &&
               (entry_chroma - chroma).abs() < 0.01 {
                return Ok((*x, *y));
            }
        }

        Err(MunsellError::InterpolationError {
            message: format!("No renotation data for {}{} {:.1}/{:.1}",
                hue, family, value, chroma),
        })
    }

    /// Interpolate from renotation data for non-standard chroma values.
    fn interpolate_from_renotation_data(
        &self, hue: f64, value: f64, chroma: f64, code: u8,
    ) -> Result<(f64, f64)> {
        let chroma_low = 2.0 * (chroma / 2.0).floor();
        let chroma_high = chroma_low + 2.0;

        let max_chroma = self.maximum_chroma_from_renotation(hue, value, code)?;

        if chroma_high > max_chroma {
            if chroma_low <= max_chroma {
                return self.lookup_xy_from_renotation(hue, value, chroma_low, code);
            }
            return self.lookup_xy_from_renotation(hue, value, max_chroma, code);
        }

        let (x_low, y_low) = self.lookup_xy_from_renotation(hue, value, chroma_low, code)?;
        let (x_high, y_high) = self.lookup_xy_from_renotation(hue, value, chroma_high, code)?;

        let t = (chroma - chroma_low) / 2.0;
        Ok((
            x_low + t * (x_high - x_low),
            y_low + t * (y_high - y_low),
        ))
    }

    /// Get xy coordinates from renotation ovoid for standard hues.
    pub(super) fn xy_from_renotation_ovoid(
        &self, hue: f64, value: f64, chroma: f64, code: u8,
    ) -> Result<(f64, f64)> {
        if chroma.abs() < 1e-10 {
            return Ok((ILLUMINANT_C[0], ILLUMINANT_C[1]));
        }

        let is_standard_chroma = (chroma % 2.0).abs() < 1e-10;
        let is_standard_hue = (hue % 2.5).abs() < 1e-10;

        if is_standard_hue && is_standard_chroma {
            return self.lookup_xy_from_renotation(hue, value, chroma, code);
        }

        if is_standard_hue && !is_standard_chroma {
            return self.interpolate_from_renotation_data(hue, value, chroma, code);
        }

        // Non-standard hue — interpolate between bounding hues
        self.xy_from_renotation_ovoid_for_even_chroma(hue, value, chroma, code)
    }

    /// Interpolate xy from bounding hues for non-standard hue values.
    fn xy_from_renotation_ovoid_for_even_chroma(
        &self, hue: f64, value: f64, chroma: f64, code: u8,
    ) -> Result<(f64, f64)> {
        let ((hue_cw, code_cw), (hue_ccw, code_ccw)) =
            hue_conversions::bounding_hues_from_renotation(hue, code);

        let is_standard_chroma = (chroma % 2.0).abs() < 1e-10;

        let (x_minus, y_minus) = if is_standard_chroma {
            self.lookup_xy_from_renotation(hue_cw, value, chroma, code_cw)?
        } else {
            self.interpolate_from_renotation_data(hue_cw, value, chroma, code_cw)?
        };
        let (x_plus, y_plus) = if is_standard_chroma {
            self.lookup_xy_from_renotation(hue_ccw, value, chroma, code_ccw)?
        } else {
            self.interpolate_from_renotation_data(hue_ccw, value, chroma, code_ccw)?
        };

        let x_grey = ILLUMINANT_C[0];
        let y_grey = ILLUMINANT_C[1];
        let y_luminance_minus = self.munsell_value_to_luminance(value).unwrap_or(0.0);
        let y_luminance_plus = y_luminance_minus;

        // Convert to cylindrical coordinates relative to grey point
        let (rho_minus, phi_minus, _) = coordinate_transforms::cartesian_to_cylindrical(
            x_minus - x_grey, y_minus - y_grey, y_luminance_minus,
        );
        let phi_minus_deg = phi_minus.to_degrees();

        let (rho_plus, phi_plus, _) = coordinate_transforms::cartesian_to_cylindrical(
            x_plus - x_grey, y_plus - y_grey, y_luminance_plus,
        );
        let mut phi_plus_deg = phi_plus.to_degrees();

        // Get hue angles
        let hue_angle_lower = hue_conversions::hue_to_hue_angle(hue_cw, code_cw);
        let hue_angle = hue_conversions::hue_to_hue_angle(hue, code);
        let hue_angle_upper = hue_conversions::hue_to_hue_angle(hue_ccw, code_ccw);

        // Handle phi angle wrapping
        if phi_minus_deg - phi_plus_deg > 180.0 {
            phi_plus_deg += 360.0;
        }

        // Handle hue angle wrapping and corrections
        let mut hue_angle_lower_corrected = hue_angle_lower;
        let mut hue_angle_corrected = hue_angle;

        if hue_angle_lower == 0.0 {
            hue_angle_lower_corrected = 360.0;
        }

        if hue_angle_lower_corrected > hue_angle_upper {
            if hue_angle_lower_corrected > hue_angle {
                hue_angle_lower_corrected -= 360.0;
            } else {
                hue_angle_lower_corrected -= 360.0;
                hue_angle_corrected -= 360.0;
            }
        }

        // Get interpolation method
        let interpolation_method = self.get_interpolation_method(hue, value, chroma, code)?;

        if interpolation_method == "Linear" {
            let x = self.linear_interpolate_2d(
                hue_angle_lower_corrected, hue_angle_upper, x_minus, x_plus, hue_angle_corrected,
            );
            let y = self.linear_interpolate_2d(
                hue_angle_lower_corrected, hue_angle_upper, y_minus, y_plus, hue_angle_corrected,
            );
            Ok((x, y))
        } else if interpolation_method == "Radial" {
            let rho = self.linear_interpolate_2d(
                hue_angle_lower_corrected, hue_angle_upper, rho_minus, rho_plus, hue_angle_corrected,
            );
            let phi_deg = self.linear_interpolate_2d(
                hue_angle_lower_corrected, hue_angle_upper, phi_minus_deg, phi_plus_deg, hue_angle_corrected,
            );

            let phi_rad = phi_deg.to_radians();
            let (x_offset, y_offset) = coordinate_transforms::polar_to_cartesian(rho, phi_rad);
            let x = x_offset + x_grey;
            let y = y_offset + y_grey;
            Ok((x, y))
        } else {
            Err(MunsellError::InterpolationError {
                message: format!("Invalid interpolation method: {}", interpolation_method),
            })
        }
    }

    /// Get Y luminance value from renotation data.
    #[allow(dead_code)]
    fn get_y_luminance_from_renotation(
        &self, _hue: f64, value: f64, chroma: f64, code: u8,
    ) -> Result<f64> {
        let family = hue_conversions::code_to_family(code);

        for &((ref entry_family, entry_value, entry_chroma), (_, _, y_luminance)) in self.renotation_data {
            if (*entry_family == family ||
               (entry_family.len() > family.len() &&
                entry_family.ends_with(family) &&
                entry_family.chars().nth(entry_family.len() - family.len() - 1).unwrap_or(' ').is_numeric())) &&
               (entry_value - value).abs() < 0.01 &&
               (entry_chroma - chroma).abs() < 0.01 {
                return Ok(y_luminance);
            }
        }

        // Fallback: approximate relationship
        Ok(0.1 * value)
    }

    /// Get interpolation method using simplified lookup.
    fn get_interpolation_method(
        &self, _hue: f64, value: f64, chroma: f64, _code: u8,
    ) -> Result<&'static str> {
        if value <= 1.0 || chroma <= 2.0 {
            return Ok("Linear");
        }
        if chroma >= 20.0 {
            return Ok("Radial");
        }
        if chroma <= 10.0 {
            return Ok("Linear");
        }
        Ok("Radial")
    }

    /// Simple linear interpolation between two points.
    fn linear_interpolate_2d(&self, x1: f64, x2: f64, y1: f64, y2: f64, x: f64) -> f64 {
        if (x2 - x1).abs() < 1e-10 {
            return y1;
        }
        y1 + (x - x1) * (y2 - y1) / (x2 - x1)
    }
}
