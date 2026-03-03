//! Legacy and unused methods on MathematicalMunsellConverter.
//!
//! These are kept for potential future use but are not part of the active
//! conversion pipeline. All methods are marked `#[allow(dead_code)]`.

use crate::constants::*;
use crate::error::{MunsellError, Result};

use super::types::{MunsellSpecification, CieXyY};
use super::MathematicalMunsellConverter;

impl MathematicalMunsellConverter {
    /// Check if color is achromatic based on chromaticity distance from Illuminant D65.
    #[allow(dead_code)]
    fn is_achromatic_d65(&self, x: f64, y: f64) -> bool {
        if x == 0.0 && y == 0.0 {
            return true;
        }
        const ILLUMINANT_D65: [f64; 2] = [0.31270, 0.32900];
        let dx = x - ILLUMINANT_D65[0];
        let dy = y - ILLUMINANT_D65[1];
        let distance = (dx * dx + dy * dy).sqrt();
        distance < ACHROMATIC_THRESHOLD
    }

    /// Check if color is achromatic based on chromaticity distance from Illuminant C.
    #[allow(dead_code)]
    pub(super) fn is_achromatic(&self, x: f64, y: f64) -> bool {
        if x == 0.0 && y == 0.0 {
            return true;
        }
        let dx = x - ILLUMINANT_C[0];
        let dy = y - ILLUMINANT_C[1];
        let distance = (dx * dx + dy * dy).sqrt();
        distance < ACHROMATIC_THRESHOLD
    }

    /// Interpolate hue and chroma from Munsell Renotation dataset using advanced algorithm.
    #[allow(dead_code)]
    fn interpolate_hue_chroma(&self, x: f64, y: f64, luma: f64) -> Result<(f64, String, f64)> {
        let (initial_hue, initial_family, initial_chroma) = self.find_nearest_neighbor(x, y, luma)?;

        let mut current_spec = MunsellSpecification {
            hue: initial_hue,
            family: initial_family.clone(),
            value: self.luminance_to_munsell_value(luma)?,
            chroma: initial_chroma,
        };

        for _outer_iteration in 0..super::MAX_OUTER_ITERATIONS {
            let target_xyy = self.munsell_specification_to_xyy_interpolated(&current_spec)?;

            let error_x = x - target_xyy.x;
            let error_y = y - target_xyy.y;
            let error_magnitude = (error_x * error_x + error_y * error_y).sqrt();

            if error_magnitude < super::TOLERANCE_ABSOLUTE_DEFAULT {
                return Ok((current_spec.hue, current_spec.family, current_spec.chroma));
            }

            current_spec = self.refine_munsell_specification(&current_spec, x, y, error_x, error_y)?;
        }

        Ok((initial_hue, initial_family, initial_chroma))
    }

    /// Find nearest neighbor in renotation data as initial guess.
    #[allow(dead_code)]
    fn find_nearest_neighbor(&self, x: f64, y: f64, luma: f64) -> Result<(f64, String, f64)> {
        let mut best_distance = f64::INFINITY;
        let mut best_match: Option<&'static ((&'static str, f64, f64), (f64, f64, f64))> = None;

        for entry in self.renotation_data {
            let ((_, _, _), (entry_x, entry_y, entry_luma)) = entry;

            let dx = x - entry_x;
            let dy = y - entry_y;
            let dluma = luma - entry_luma;
            let distance = (dx * dx + dy * dy + dluma * dluma * 0.1).sqrt();

            if distance < best_distance {
                best_distance = distance;
                best_match = Some(entry);
            }
        }

        match best_match {
            Some(((hue_str, _value, chroma), _)) => {
                let (hue, family) = self.parse_hue_string(hue_str)?;
                Ok((hue, family, *chroma))
            }
            None => Err(MunsellError::InterpolationError {
                message: "No matching color found in renotation data".to_string(),
            })
        }
    }

    /// Advanced interpolation from Munsell specification to xyY using radial basis functions.
    #[allow(dead_code)]
    fn munsell_specification_to_xyy_interpolated(&self, spec: &MunsellSpecification) -> Result<CieXyY> {
        if spec.family == "N" {
            let y = self.munsell_value_to_luminance(spec.value)?;
            return Ok(CieXyY {
                x: ILLUMINANT_C[0],
                y: ILLUMINANT_C[1],
                y_luminance: y,
            });
        }

        let hue_str = format!("{}{}", spec.hue, spec.family);
        let neighbors = self.find_interpolation_neighbors(&hue_str, spec.value, spec.chroma);

        if neighbors.is_empty() {
            return Err(MunsellError::InterpolationError {
                message: format!("No neighbors found for interpolation: {}", hue_str),
            });
        }

        self.radial_basis_interpolation(&neighbors, spec.value, spec.chroma)
    }

    /// Find neighboring points for advanced interpolation.
    #[allow(dead_code)]
    fn find_interpolation_neighbors(
        &self, target_hue: &str, target_value: f64, target_chroma: f64,
    ) -> Vec<&'static ((&'static str, f64, f64), (f64, f64, f64))> {
        let mut neighbors = Vec::new();

        for entry in self.renotation_data {
            let ((entry_hue, entry_value, entry_chroma), _) = entry;

            if self.hue_families_match(target_hue, entry_hue) {
                let value_diff = (target_value - entry_value).abs();
                let chroma_diff = (target_chroma - entry_chroma).abs();

                if value_diff <= 2.0 && chroma_diff <= 4.0 {
                    neighbors.push(entry);
                }
            }
        }

        if neighbors.len() < 4 {
            for entry in self.renotation_data {
                let ((entry_hue, entry_value, entry_chroma), _) = entry;

                let hue_distance = self.calculate_hue_distance(target_hue, entry_hue);

                if hue_distance <= 2.5 {
                    let value_diff = (target_value - entry_value).abs();
                    let chroma_diff = (target_chroma - entry_chroma).abs();

                    if value_diff <= 3.0 && chroma_diff <= 6.0 {
                        neighbors.push(entry);
                    }
                }
            }
        }

        neighbors
    }

    /// Check if two hue families match (same letters).
    #[allow(dead_code)]
    fn hue_families_match(&self, hue1: &str, hue2: &str) -> bool {
        let family1 = hue1.chars().filter(|c| c.is_alphabetic()).collect::<String>();
        let family2 = hue2.chars().filter(|c| c.is_alphabetic()).collect::<String>();
        family1 == family2
    }

    /// Calculate angular distance between two hue strings.
    #[allow(dead_code)]
    fn calculate_hue_distance(&self, hue1: &str, hue2: &str) -> f64 {
        let (num1, family1) = self.parse_hue_string(hue1).unwrap_or((0.0, "".to_string()));
        let (num2, family2) = self.parse_hue_string(hue2).unwrap_or((0.0, "".to_string()));

        if family1 == family2 {
            (num1 - num2).abs()
        } else {
            let angle1 = self.hue_to_angle(num1, &family1);
            let angle2 = self.hue_to_angle(num2, &family2);
            let diff = (angle1 - angle2).abs();
            diff.min(360.0 - diff) / 36.0
        }
    }

    /// Convert hue notation to angle (simplified).
    #[allow(dead_code)]
    fn hue_to_angle(&self, hue: f64, family: &str) -> f64 {
        let base_angle = match family {
            "R" => 0.0, "YR" => 36.0, "Y" => 72.0, "GY" => 108.0, "G" => 144.0,
            "BG" => 180.0, "B" => 216.0, "PB" => 252.0, "P" => 288.0, "RP" => 324.0,
            _ => 0.0,
        };
        base_angle + (hue - 5.0) * 3.6
    }

    /// Radial basis function interpolation.
    #[allow(dead_code)]
    fn radial_basis_interpolation(
        &self,
        neighbors: &[&'static ((&'static str, f64, f64), (f64, f64, f64))],
        target_value: f64,
        target_chroma: f64,
    ) -> Result<CieXyY> {
        if neighbors.is_empty() {
            return Err(MunsellError::InterpolationError {
                message: "No neighbors for radial basis interpolation".to_string(),
            });
        }

        let mut weighted_x = 0.0;
        let mut weighted_y = 0.0;
        let mut total_weight = 0.0;

        for neighbor in neighbors {
            let ((_, neighbor_value, neighbor_chroma), (x, y, luma)) = neighbor;

            let value_dist = target_value - neighbor_value;
            let chroma_dist = target_chroma - neighbor_chroma;
            let distance = (value_dist * value_dist + chroma_dist * chroma_dist).sqrt();

            let weight = if distance < 0.001 {
                1000.0
            } else {
                1.0 / (distance + 0.1)
            };

            weighted_x += x * weight;
            weighted_y += y * weight;
            weighted_y += luma * weight;
            total_weight += weight;
        }

        if total_weight < 1e-15 {
            return Err(MunsellError::InterpolationError {
                message: "Zero total weight in radial basis interpolation".to_string(),
            });
        }

        Ok(CieXyY {
            x: weighted_x / total_weight,
            y: weighted_y / total_weight,
            y_luminance: weighted_y / total_weight,
        })
    }

    /// Refine Munsell specification using gradient estimation.
    fn refine_munsell_specification(
        &self, spec: &MunsellSpecification,
        _target_x: f64, _target_y: f64, error_x: f64, error_y: f64,
    ) -> Result<MunsellSpecification> {
        let step_size = 0.1;

        let mut refined_spec = spec.clone();

        let chroma_adjustment = (error_x * error_x + error_y * error_y).sqrt() * 2.0;
        refined_spec.chroma = (spec.chroma + chroma_adjustment * step_size).max(0.0);

        let hue_adjustment = error_x.atan2(error_y) * 180.0 / std::f64::consts::PI * 0.1;
        refined_spec.hue = (spec.hue + hue_adjustment).rem_euclid(10.0);

        Ok(refined_spec)
    }

    /// Parse Munsell hue string like "5R", "2.5GY" into hue number and family.
    pub(super) fn parse_hue_string(&self, hue_str: &str) -> Result<(f64, String)> {
        let mut split_pos = 0;
        for (i, c) in hue_str.char_indices() {
            if c.is_alphabetic() {
                split_pos = i;
                break;
            }
        }

        if split_pos == 0 {
            return Err(MunsellError::InvalidNotation {
                notation: hue_str.to_string(),
                reason: "Hue string contains no alphabetic characters".to_string(),
            });
        }

        let hue_str_num = &hue_str[..split_pos];
        let family = hue_str[split_pos..].to_string();

        let hue: f64 = hue_str_num.parse()
            .map_err(|_| MunsellError::InvalidNotation {
                notation: hue_str_num.to_string(),
                reason: "Invalid numeric value in hue".to_string(),
            })?;

        Ok((hue, family))
    }

    /// Linear interpolation between hue boundaries (LEGACY).
    #[allow(dead_code)]
    fn linear_interpolate_xy(&self, hue: f64, value: f64, chroma: f64, code: u8) -> Result<(f64, f64)> {
        self.xy_from_renotation_ovoid(hue, value, chroma, code)
    }

    /// Radial interpolation in cylindrical coordinates (LEGACY).
    #[allow(dead_code)]
    fn radial_interpolate_xy(&self, hue: f64, value: f64, chroma: f64, code: u8) -> Result<(f64, f64)> {
        self.xy_from_renotation_ovoid(hue, value, chroma, code)
    }

    /// Fallback interpolation method.
    #[allow(dead_code)]
    fn interpolate_hue_chroma_to_xy(&self, _hue: f64, value: f64, _chroma: f64, _code: u8) -> Result<(f64, f64)> {
        let (_, _, _) = self.interpolate_hue_chroma(0.31006, 0.31616, value)?;
        Ok((0.31006, 0.31616))
    }
}
