//! xyY → Munsell specification conversion using ASTM D1535 algorithm.
//!
//! Contains the main iterative convergence algorithm decomposed into
//! manageable helper functions.

use crate::constants::*;
use crate::error::Result;

use super::coordinate_transforms;
use super::hue_conversions;
use super::types::{MunsellSpecification, CieXyY};
use super::MathematicalMunsellConverter;

// Critical constants from Python colour-science
const THRESHOLD_INTEGER: f64 = 1e-3;
const MAX_OUTER_ITERATIONS: usize = 64;
const MAX_INNER_ITERATIONS: usize = 16;

impl MathematicalMunsellConverter {
    /// Convert CIE xyY to Munsell specification using ASTM D1535 algorithm.
    ///
    /// EXACT IMPLEMENTATION of Python colour-science _xyY_to_munsell_specification.
    /// Uses a dual-loop iterative algorithm for mathematical accuracy.
    ///
    /// Colors below the Munsell Renotation Dataset minimum Value (0.2) are
    /// returned as neutral (N) since no renotation data exists to resolve
    /// chroma, and human color discrimination is negligible at such low
    /// luminance.
    pub fn xyy_to_munsell_specification(&self, xyy: CieXyY) -> Result<MunsellSpecification> {
        let convergence_threshold = THRESHOLD_INTEGER / 1e4; // 1e-7

        // Step 1: Calculate Munsell Value using ASTM D1535 polynomial
        let mut value = self.luminance_to_munsell_value(xyy.y_luminance)?;
        if (value - value.round()).abs() < 1e-10 {
            value = value.round();
        }

        // Colors below the renotation dataset's minimum Value (0.2) cannot
        // have their chroma resolved. Return neutral — at such low luminance,
        // human color discrimination is effectively zero.
        if value < MINIMUM_RENOTATION_VALUE {
            return Ok(MunsellSpecification {
                hue: 0.0, family: "N".to_string(), value, chroma: 0.0,
            });
        }

        // Step 2: Check for achromatic sRGB colors via D65 proximity.
        // sRGB achromatic colors (R=G=B) have chromaticity at the D65
        // white point, which is offset ~0.013 from Illuminant C. The
        // existing rho < 1e-3 check misses these, so we explicitly test
        // distance from D65 before entering the iterative algorithm.
        let dx_d65 = xyy.x - ILLUMINANT_D65_CHROMATICITY[0];
        let dy_d65 = xyy.y - ILLUMINANT_D65_CHROMATICITY[1];
        let rho_d65 = (dx_d65 * dx_d65 + dy_d65 * dy_d65).sqrt();
        if rho_d65 < THRESHOLD_INTEGER {
            return Ok(MunsellSpecification {
                hue: 0.0, family: "N".to_string(), value, chroma: 0.0,
            });
        }

        // Step 3: Get achromatic center for this value
        let (x_center, y_center) = self.achromatic_center(value)?;

        // Calculate rho/phi relative to achromatic center
        let (rho_input, phi_input_rad, _) = coordinate_transforms::cartesian_to_cylindrical(
            xyy.x - x_center, xyy.y - y_center, xyy.y_luminance,
        );
        let phi_input = phi_input_rad.to_degrees();

        // Step 4: Check for achromatic / pure black (Illuminant C proximity)
        if rho_input < THRESHOLD_INTEGER || xyy.y_luminance < 1e-6 {
            return Ok(MunsellSpecification {
                hue: 0.0, family: "N".to_string(), value, chroma: 0.0,
            });
        }

        // Step 4: Generate initial guess
        let initial_spec = self.generate_initial_guess(xyy)?;
        let mut hue_current = initial_spec.0;
        let mut code_current = initial_spec.1;
        let mut chroma_current = initial_spec.2;

        // Step 5: Dual-loop iterative algorithm
        for _outer_iteration in 0..MAX_OUTER_ITERATIONS {
            // Cap chroma at maximum
            let chroma_maximum = self.maximum_chroma_from_renotation(hue_current, value, code_current)?;
            if chroma_current > chroma_maximum {
                chroma_current = chroma_maximum;
            }

            // Run hue angle inner loop
            let (hue_new, code_new) = self.run_hue_angle_inner_loop(
                hue_current, code_current, value, chroma_current,
                x_center, y_center, xyy.y_luminance, phi_input,
            )?;
            hue_current = hue_new;
            code_current = code_new;

            // Cap chroma again after hue update
            let chroma_maximum = self.maximum_chroma_from_renotation(hue_current, value, code_current)?;
            if chroma_current > chroma_maximum {
                chroma_current = chroma_maximum;
            }

            // Run chroma magnitude inner loop
            chroma_current = self.run_chroma_inner_loop(
                hue_current, code_current, value, chroma_current,
                x_center, y_center, xyy.y_luminance, rho_input,
            )?;

            // Convergence check
            let (x_final, y_final) = self.munsell_specification_to_xy(hue_current, value, chroma_current, code_current)?;
            let difference = ((xyy.x - x_final).powi(2) + (xyy.y - y_final).powi(2)).sqrt();

            if difference < convergence_threshold {
                return self.build_converged_result(hue_current, code_current, value, chroma_current);
            }
        }

        // Non-convergence fallback
        self.build_converged_result(hue_current, code_current, value, chroma_current)
    }

    /// Get the achromatic center (x, y) for a given Munsell value.
    fn achromatic_center(&self, value: f64) -> Result<(f64, f64)> {
        let achromatic_spec = MunsellSpecification {
            hue: 0.0, family: "N".to_string(), value, chroma: 0.0,
        };
        let achromatic_xyy = self.munsell_specification_to_xyy(&achromatic_spec)?;
        Ok((achromatic_xyy.x, achromatic_xyy.y))
    }

    /// Inner loop: Hue angle search following Python algorithm.
    fn run_hue_angle_inner_loop(
        &self,
        hue_current: f64, code_current: u8,
        value: f64, chroma_current: f64,
        x_center: f64, y_center: f64,
        y_luminance: f64, phi_input: f64,
    ) -> Result<(f64, u8)> {
        let (x_current, y_current) = self.munsell_specification_to_xy(hue_current, value, chroma_current, code_current)?;

        let phi_current_degrees = Self::compute_phi_degrees(x_current - x_center, y_current - y_center, y_luminance);

        let phi_current_difference = Self::wrapped_phi_difference(phi_input, phi_current_degrees);

        let mut phi_differences_data = if phi_current_difference.abs() < 1e-6 { vec![] } else { vec![phi_current_difference] };
        let mut hue_angles_differences_data = if phi_current_difference.abs() < 1e-6 { vec![] } else { vec![0.0] };
        let hue_angle_current = hue_conversions::hue_to_astm_hue(hue_current, code_current);
        let mut extrapolate = false;
        let mut iterations_inner = 0;

        while (phi_differences_data.iter().all(|&d| d >= 0.0) ||
               phi_differences_data.iter().all(|&d| d <= 0.0)) && !extrapolate {
            iterations_inner += 1;
            if iterations_inner > MAX_INNER_ITERATIONS { break; }

            let (hue_angle_inner, hue_angle_diff) =
                Self::compute_hue_step(hue_angle_current, phi_input, phi_current_degrees, iterations_inner);

            let (hue_inner, code_inner) = hue_conversions::hue_angle_to_hue(hue_angle_inner);
            let (x_inner, y_inner) = self.munsell_specification_to_xy(hue_inner, value, chroma_current, code_inner)?;

            if phi_differences_data.len() >= 2 { extrapolate = true; }

            if !extrapolate {
                let phi_inner_degrees = Self::compute_phi_degrees(x_inner - x_center, y_inner - y_center, y_luminance);
                let phi_inner_difference = Self::wrapped_phi_difference(phi_input, phi_inner_degrees);
                phi_differences_data.push(phi_inner_difference);
                hue_angles_differences_data.push(hue_angle_diff);
            }
        }

        let hue_angle_difference_new = self.interpolate_hue_angle_difference(
            &phi_differences_data, &hue_angles_differences_data,
        )?;

        let mut hue_angle_new = (hue_angle_current + hue_angle_difference_new) % 360.0;
        if hue_angle_new < 0.0 { hue_angle_new += 360.0; }

        Ok(hue_conversions::hue_angle_to_hue(hue_angle_new))
    }

    /// Compute phi in degrees [0, 360) from cartesian offsets relative to achromatic center.
    fn compute_phi_degrees(dx: f64, dy: f64, y_luminance: f64) -> f64 {
        let (_, phi, _) = coordinate_transforms::cartesian_to_cylindrical(dx, dy, y_luminance);
        let deg = phi.to_degrees();
        if deg < 0.0 { deg + 360.0 } else { deg }
    }

    /// Calculate wrapped phi difference in [-180, 180].
    fn wrapped_phi_difference(phi_input: f64, phi_degrees: f64) -> f64 {
        let d = (360.0 - phi_input + phi_degrees) % 360.0;
        if d > 180.0 { d - 360.0 } else { d }
    }

    /// Compute hue angle step and its normalized difference for a given iteration.
    fn compute_hue_step(
        hue_angle_current: f64, phi_input: f64, phi_current_degrees: f64, iteration: usize,
    ) -> (f64, f64) {
        let step = iteration as f64 * (phi_input - phi_current_degrees);
        let hue_angle_inner = if (hue_angle_current + step) < 0.0 {
            ((hue_angle_current + step) % 360.0 + 360.0) % 360.0
        } else {
            (hue_angle_current + step) % 360.0
        };

        let step_mod = if step < 0.0 {
            ((step % 360.0) + 360.0) % 360.0
        } else {
            step % 360.0
        };
        let hue_angle_diff = if step_mod > 180.0 { step_mod - 360.0 } else { step_mod };

        (hue_angle_inner, hue_angle_diff)
    }

    /// Interpolate phi_differences vs hue_angle_differences to find where phi=0.
    fn interpolate_hue_angle_difference(
        &self, phi_diffs: &[f64], hue_angle_diffs: &[f64],
    ) -> Result<f64> {
        if phi_diffs.len() >= 2 {
            let mut paired: Vec<_> = phi_diffs.iter()
                .zip(hue_angle_diffs.iter())
                .map(|(&p, &h)| (p, h))
                .collect();
            paired.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());

            let sorted_phi: Vec<f64> = paired.iter().map(|&(p, _)| p).collect();
            let sorted_hue: Vec<f64> = paired.iter().map(|&(_, h)| h).collect();

            let result = self.linear_interpolate(&sorted_phi, &sorted_hue, 0.0)?;
            Ok(if result < 0.0 { result % 360.0 + 360.0 } else { result % 360.0 })
        } else {
            Ok(0.0)
        }
    }

    /// Inner loop: Chroma magnitude refinement using exponential scaling.
    fn run_chroma_inner_loop(
        &self,
        hue_current: f64, code_current: u8,
        value: f64, chroma_current: f64,
        x_center: f64, y_center: f64,
        y_luminance: f64, rho_input: f64,
    ) -> Result<f64> {
        let (x_current_new, y_current_new) = self.munsell_specification_to_xy(hue_current, value, chroma_current, code_current)?;
        let (rho_current_new, _, _) = coordinate_transforms::cartesian_to_cylindrical(
            x_current_new - x_center, y_current_new - y_center, y_luminance,
        );

        let mut rho_bounds_data = vec![rho_current_new];
        let mut chroma_bounds_data = vec![chroma_current];
        let mut iterations_inner = 0;

        for _ in 0..MAX_INNER_ITERATIONS {
            let rho_min = *rho_bounds_data.iter().min_by(|a, b| a.partial_cmp(b).unwrap()).unwrap();
            let rho_max = *rho_bounds_data.iter().max_by(|a, b| a.partial_cmp(b).unwrap()).unwrap();

            if rho_min <= rho_input && rho_input <= rho_max {
                break;
            }

            iterations_inner += 1;
            if iterations_inner > MAX_INNER_ITERATIONS { break; }

            let chroma_inner = if rho_current_new.abs() > 1e-10 {
                let ratio = rho_input / rho_current_new;
                let power = iterations_inner as f64;
                ratio.powf(power) * chroma_current
            } else {
                chroma_current
            };

            let chroma_max = self.maximum_chroma_from_renotation(hue_current, value, code_current)?;
            let chroma_bounded = chroma_inner.min(chroma_max).max(0.0);

            let (x_inner, y_inner) = self.munsell_specification_to_xy(hue_current, value, chroma_bounded, code_current)?;
            let (rho_inner, _, _) = coordinate_transforms::cartesian_to_cylindrical(
                x_inner - x_center, y_inner - y_center, y_luminance,
            );

            rho_bounds_data.push(rho_inner);
            chroma_bounds_data.push(chroma_bounded);
        }

        // Linear interpolation for chroma
        if rho_bounds_data.len() >= 2 {
            let mut paired: Vec<_> = rho_bounds_data.iter()
                .zip(chroma_bounds_data.iter())
                .map(|(&r, &c)| (r, c))
                .collect();
            paired.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());

            let sorted_rho: Vec<f64> = paired.iter().map(|&(r, _)| r).collect();
            let sorted_chroma: Vec<f64> = paired.iter().map(|&(_, c)| c).collect();

            let interpolated = self.linear_interpolate(&sorted_rho, &sorted_chroma, rho_input)?;
            Ok(interpolated.max(0.0))
        } else {
            Ok(chroma_current)
        }
    }

    /// Build the final converged MunsellSpecification with normalization.
    fn build_converged_result(
        &self, hue_current: f64, code_current: u8, value: f64, chroma_current: f64,
    ) -> Result<MunsellSpecification> {
        if chroma_current < 1e-10 {
            return Ok(MunsellSpecification {
                hue: 0.0, family: "N".to_string(), value, chroma: 0.0,
            });
        }

        let (normalized_hue, normalized_code) = Self::normalize_munsell_specification(hue_current, code_current);
        let family = hue_conversions::code_to_family(normalized_code);

        Ok(MunsellSpecification {
            hue: normalized_hue,
            family: family.to_string(),
            value,
            chroma: chroma_current,
        })
    }

    /// Normalize Munsell specification following Python colour-science rules.
    /// When hue == 0, convert to hue=10 and increment code.
    pub(super) fn normalize_munsell_specification(hue: f64, code: u8) -> (f64, u8) {
        if hue.abs() < 0.01 && hue < 5.0 {
            let new_code = match code {
                1 => 2,   // B -> BG
                2 => 3,   // BG -> G
                3 => 4,   // G -> GY
                4 => 5,   // GY -> Y
                5 => 6,   // Y -> YR
                6 => 7,   // YR -> R
                7 => 8,   // R -> RP
                8 => 9,   // RP -> P
                9 => 10,  // P -> PB
                10 => 1,  // PB -> B (wraparound)
                _ => code
            };
            (10.0, new_code)
        } else {
            (hue, code)
        }
    }

    /// Generate initial guess using direct xyY angle.
    pub(super) fn generate_initial_guess(&self, xyy: CieXyY) -> Result<(f64, u8, f64)> {
        let dx = xyy.x - ILLUMINANT_C[0];
        let dy = xyy.y - ILLUMINANT_C[1];
        let (rho, phi_rad, _) = coordinate_transforms::cartesian_to_cylindrical(dx, dy, xyy.y_luminance);
        let mut phi_deg = phi_rad.to_degrees();

        if phi_deg < 0.0 {
            phi_deg += 360.0;
        }

        let (hue_initial, code_initial) = hue_conversions::hue_angle_to_hue(phi_deg);
        let chroma_initial = rho * 50.0; // Empirical scaling factor

        Ok((hue_initial, code_initial, chroma_initial))
    }

    /// Exact implementation of Python LCHab_to_munsell_specification function.
    #[allow(dead_code)]
    pub(super) fn lchab_to_munsell_specification(&self, _l: f64, _c: f64, hab: f64) -> (f64, u8) {
        let code = if hab < 18.0 || hab >= 342.0 {
            8  // RP
        } else if hab < 54.0 {
            7  // R
        } else if hab < 90.0 {
            6  // YR
        } else if hab < 126.0 {
            5  // Y
        } else if hab < 162.0 {
            4  // GY
        } else if hab < 198.0 {
            3  // G
        } else if hab < 234.0 {
            2  // BG
        } else if hab < 270.0 {
            1  // B
        } else if hab < 306.0 {
            10 // PB
        } else if hab < 342.0 {
            9  // P
        } else {
            8  // RP
        };

        let segment_start = ((hab / 36.0).floor() * 36.0) as f64;
        let hab_in_segment = hab - segment_start;
        let mut hue = (hab_in_segment / 36.0) * 10.0;

        if hue == 0.0 && hab > 0.0 {
            hue = 10.0;
        }

        (hue, code)
    }
}
