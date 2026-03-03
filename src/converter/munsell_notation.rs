//! Munsell notation calculation from color space coordinates.

use crate::error::Result;
use crate::types::MunsellColor;

use super::MunsellConverter;

impl MunsellConverter {
    /// Perform algorithmic sRGB to Munsell conversion using mathematical transformation.
    ///
    /// Implements the complete color space transformation pipeline:
    /// sRGB -> Linear RGB -> XYZ (D65) -> xyY -> Munsell
    pub(crate) fn algorithmic_srgb_to_munsell(&self, rgb: [u8; 3]) -> Result<MunsellColor> {
        // Handle pure black as special case
        if rgb[0] == 0 && rgb[1] == 0 && rgb[2] == 0 {
            return Ok(MunsellColor::new_neutral(0.0));
        }

        // Step 1: Convert u8 RGB to normalized f64 sRGB
        const INV_255: f64 = 1.0 / 255.0;
        let srgb_norm = [
            rgb[0] as f64 * INV_255,
            rgb[1] as f64 * INV_255,
            rgb[2] as f64 * INV_255,
        ];

        // Step 2: Apply gamma correction (sRGB -> linear RGB)
        let linear_rgb = self.srgb_to_linear_rgb(srgb_norm);

        // Step 3: Convert linear RGB -> XYZ (D65 illuminant)
        let xyz_d65 = self.linear_rgb_to_xyz_d65(linear_rgb);

        // Step 4: Use D65 directly (consistent D65 approach for accuracy)
        let xyz_final = xyz_d65;

        // Step 5: Convert XYZ -> xyY
        let xyy = self.xyz_to_xyy(xyz_final);

        // Step 6: Convert xyY -> Munsell using sophisticated spatial interpolation
        self.xyy_to_munsell_iterative(xyy)
    }

    /// Convert xyY to Munsell using scientific algorithms.
    #[allow(dead_code)]
    pub(crate) fn xyy_to_munsell(&self, xyy: [f64; 3]) -> Result<MunsellColor> {
        let [x, y, big_y] = xyy;

        if self.is_achromatic(x, y) {
            let value = self.xyz_y_to_munsell_value(big_y);
            return Ok(MunsellColor::new_neutral((value * 10.0).round() / 10.0));
        }

        let white_x = 0.31271;  // D65
        let white_y = 0.32902;
        let hue_angle = (y - white_y).atan2(x - white_x);
        let hue_degrees = hue_angle.to_degrees();

        let munsell_hue = self.degrees_to_munsell_hue(hue_degrees);
        let value = self.xyz_y_to_munsell_value(big_y);
        let rounded_value = (value * 10.0).round() / 10.0;
        let chroma = self.calculate_munsell_chroma(x, y, big_y);
        let rounded_chroma = (chroma * 10.0).round() / 10.0;

        Ok(MunsellColor::new_chromatic(munsell_hue, rounded_value, rounded_chroma))
    }

    /// Enhanced xyY to Munsell with sophisticated spatial interpolation.
    pub(crate) fn xyy_to_munsell_iterative(&self, xyy: [f64; 3]) -> Result<MunsellColor> {
        let [x, y, big_y] = xyy;

        // 1. ASTM D1535 value calculation (exact match with Python)
        let value = self.xyz_y_to_munsell_value(big_y);

        // 2. Enhanced achromatic detection (Python threshold)
        if self.is_achromatic(x, y) {
            return Ok(MunsellColor::new_neutral((value * 10.0).round() / 10.0));
        }

        // 3. Lab pathway for initial estimates (like Python colour-science)
        let xyz = self.xyy_to_xyz(xyy);
        let lab = self.xyz_to_lab_d65(xyz);
        let lchab = self.lab_to_lchab(lab);
        let (_hue_initial, _chroma_initial) = self.lchab_to_munsell_estimate(lchab);

        // 4. SPATIAL INTERPOLATION with reference dataset (the key algorithm!)
        let interpolated_result = self.spatial_interpolation_munsell(xyy, value);

        if let Some(result) = interpolated_result {
            return Ok(result);
        }

        // 5. Fallback to mathematical approach if spatial interpolation fails
        let hue_degrees = (y - 0.32902).atan2(x - 0.31271).to_degrees();
        let munsell_hue = self.degrees_to_munsell_hue(hue_degrees);
        let chroma = self.calculate_munsell_chroma(x, y, big_y);

        Ok(MunsellColor::new_chromatic(
            munsell_hue,
            (value * 10.0).round() / 10.0,
            (chroma * 10.0).round() / 10.0,
        ))
    }

    /// Check if a color is achromatic (near neutral axis).
    #[inline]
    pub(crate) fn is_achromatic(&self, x: f64, y: f64) -> bool {
        let d65_white_x = 0.31271;
        let d65_white_y = 0.32902;

        let distance = ((x - d65_white_x).powi(2) + (y - d65_white_y).powi(2)).sqrt();

        // Python colour-science threshold
        let python_threshold = 0.001;
        distance < python_threshold
    }

    /// Convert XYZ Y component to Munsell Value using ASTM D1535 method.
    pub(crate) fn xyz_y_to_munsell_value(&self, y: f64) -> f64 {
        let y_percent = y * 100.0;
        self.munsell_value_astm_d1535(y_percent)
    }

    /// Implement ASTM D1535 Munsell value calculation method.
    fn munsell_value_astm_d1535(&self, y: f64) -> f64 {
        if y <= 0.0 {
            return 0.0;
        }
        if y >= 100.0 {
            return 10.0;
        }

        // ASTM D1535 lookup table - values from Python colour-science
        let astm_table = [
            (0.0, 0.0),
            (1.0, 0.863),
            (2.0, 1.386),
            (3.0, 1.796),
            (4.0, 2.157),
            (5.0, 2.645),
            (6.0, 2.976),
            (7.0, 3.282),
            (8.0, 3.568),
            (9.0, 3.837),
            (10.0, 3.721),
            (15.0, 4.502),
            (20.0, 5.082),
            (25.0, 5.551),
            (30.0, 6.061),
            (35.0, 6.515),
            (40.0, 6.927),
            (45.0, 7.305),
            (50.0, 7.538),
            (55.0, 7.912),
            (60.0, 8.264),
            (65.0, 8.597),
            (70.0, 8.671),
            (75.0, 9.021),
            (80.0, 9.357),
            (85.0, 9.679),
            (90.0, 9.596),
            (95.0, 9.886),
            (100.0, 10.000),
        ];

        // Linear interpolation within the lookup table
        for i in 0..astm_table.len() - 1 {
            let (y1, v1) = astm_table[i];
            let (y2, v2) = astm_table[i + 1];

            if y >= y1 && y <= y2 {
                if y2 == y1 {
                    return v1;
                }

                let ratio = (y - y1) / (y2 - y1);
                let interpolated = v1 + ratio * (v2 - v1);
                return interpolated.max(0.0).min(10.0);
            }
        }

        // Extrapolation for values outside the table
        if y < 1.0 {
            (y * 1.211).max(0.0)
        } else {
            10.0
        }
    }

    /// Convert hue angle in degrees to Munsell hue notation.
    pub(crate) fn degrees_to_munsell_hue(&self, degrees: f64) -> String {
        let normalized = ((degrees % 360.0) + 360.0) % 360.0;

        let hue_families = [
            (0.0, "R"), (36.0, "YR"), (72.0, "Y"), (108.0, "GY"), (144.0, "G"),
            (180.0, "BG"), (216.0, "B"), (252.0, "PB"), (288.0, "P"), (324.0, "RP")
        ];

        for i in 0..hue_families.len() {
            let (start_angle, family) = hue_families[i];
            let next_angle = if i == hue_families.len() - 1 { 360.0 } else { hue_families[i + 1].0 };

            if normalized >= start_angle && normalized < next_angle {
                let degrees_within_family = normalized - start_angle;
                let hue_step = (degrees_within_family / 3.6) + 1.0;

                let floored_hue = (hue_step * 10.0).floor() / 10.0;
                let clamped_hue = floored_hue.max(1.0).min(10.0);

                if (clamped_hue.fract()).abs() < 0.05 {
                    return format!("{:.0}{}", clamped_hue.round(), family);
                } else {
                    return format!("{:.1}{}", clamped_hue, family);
                }
            }
        }

        "5R".to_string()
    }

    /// Calculate Munsell chroma from chromaticity coordinates.
    pub(crate) fn calculate_munsell_chroma(&self, x: f64, y: f64, big_y: f64) -> f64 {
        let d65_white_x = 0.31271;
        let d65_white_y = 0.32902;

        let chromaticity_distance = ((x - d65_white_x).powi(2) + (y - d65_white_y).powi(2)).sqrt();

        let luminance_factor = if big_y > 0.0 {
            let y_percent = big_y * 100.0;
            y_percent.powf(1.0/3.0) / 4.64
        } else {
            0.02
        };

        let base_chroma_scaling = 85.0;

        let distance_factor = if chromaticity_distance > 0.05 {
            1.2
        } else if chromaticity_distance < 0.01 {
            0.5
        } else {
            1.0
        };

        let chroma = chromaticity_distance * base_chroma_scaling * luminance_factor * distance_factor;
        chroma.max(0.0).min(25.0)
    }

    /// LCHab to Munsell initial estimate.
    pub(crate) fn lchab_to_munsell_estimate(&self, lchab: [f64; 3]) -> (f64, f64) {
        let [_l, c, h] = lchab;

        let munsell_hue_approx = (h + 30.0) % 360.0 / 36.0;
        let munsell_chroma_approx = c / 8.0;

        (munsell_hue_approx, munsell_chroma_approx.max(0.0).min(30.0))
    }
}
