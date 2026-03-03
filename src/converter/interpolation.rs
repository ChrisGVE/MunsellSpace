//! Spatial interpolation using reference dataset for Munsell conversion.

use crate::types::MunsellColor;

use super::MunsellConverter;
use super::reference_data::MunsellReferencePoint;

impl MunsellConverter {
    /// Spatial interpolation using reference dataset (Python colour-science approach).
    pub(crate) fn spatial_interpolation_munsell(
        &self,
        target_xyy: [f64; 3],
        target_value: f64,
    ) -> Option<MunsellColor> {
        // 1. Find nearest reference points in xyY space
        let nearest_points = self.find_nearest_reference_points(target_xyy, 8);

        if nearest_points.len() < 3 {
            return None;
        }

        // 2. Filter points with similar value (within +/-0.5)
        let value_filtered: Vec<_> = nearest_points.into_iter()
            .filter(|(_, point)| (point.value - target_value).abs() <= 0.5)
            .collect();

        if value_filtered.len() < 2 {
            return None;
        }

        // 3. Weighted interpolation based on distance
        let mut total_weight = 0.0;
        let mut weighted_hue_x = 0.0;
        let mut weighted_hue_y = 0.0;
        let mut weighted_chroma = 0.0;

        for (distance, point) in value_filtered.iter().take(4) {
            let weight = if *distance < 1e-10 {
                // Extremely close to a reference point — use it directly
                return Some(MunsellColor::from_notation(&point.notation).ok()?);
            } else {
                1.0 / (distance * distance + 1e-10)
            };

            total_weight += weight;

            let hue_radians = point.hue * std::f64::consts::PI / 180.0;
            weighted_hue_x += weight * hue_radians.cos();
            weighted_hue_y += weight * hue_radians.sin();
            weighted_chroma += weight * point.chroma;
        }

        if total_weight == 0.0 {
            return None;
        }

        // 4. Calculate final interpolated values
        let final_hue_radians = weighted_hue_y.atan2(weighted_hue_x);
        let final_hue_degrees = final_hue_radians.to_degrees();
        let normalized_hue = if final_hue_degrees < 0.0 {
            final_hue_degrees + 360.0
        } else {
            final_hue_degrees
        };

        let final_chroma = weighted_chroma / total_weight;

        // 5. Convert back to Munsell notation
        let munsell_hue = self.degrees_to_munsell_hue(normalized_hue);
        let rounded_value = (target_value * 10.0).round() / 10.0;
        let rounded_chroma = (final_chroma * 10.0).round() / 10.0;

        Some(MunsellColor::new_chromatic(munsell_hue, rounded_value, rounded_chroma))
    }

    /// Find nearest reference points in xyY color space.
    pub(crate) fn find_nearest_reference_points(
        &self,
        target_xyy: [f64; 3],
        count: usize,
    ) -> Vec<(f64, &MunsellReferencePoint)> {
        let [target_x, target_y, target_big_y] = target_xyy;

        let mut distances: Vec<(f64, &MunsellReferencePoint)> = self.reference_points
            .iter()
            .map(|point| {
                let [ref_x, ref_y, ref_big_y] = point.xyy;

                // 3D Euclidean distance in xyY space with Y weighting
                let dx = target_x - ref_x;
                let dy = target_y - ref_y;
                let dy_lum = (target_big_y - ref_big_y) * 0.1;

                let distance = (dx*dx + dy*dy + dy_lum*dy_lum).sqrt();
                (distance, point)
            })
            .collect();

        distances.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());
        distances.into_iter().take(count).collect()
    }
}
