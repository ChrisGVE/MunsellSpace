//! Reference dataset loading and reference point construction.

use serde::{Deserialize, Serialize};

use crate::error::{MunsellError, Result};
use crate::types::MunsellColor;

use super::MunsellConverter;

/// Reference data entry for color conversion.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub(crate) struct ReferenceEntry {
    pub(crate) rgb: [u8; 3],
    pub(crate) munsell: String,
}

/// Enhanced reference point for spatial interpolation.
#[derive(Debug, Clone)]
#[allow(dead_code)]
pub(crate) struct MunsellReferencePoint {
    pub(crate) rgb: [u8; 3],
    pub(crate) xyy: [f64; 3],
    pub(crate) hue: f64,
    pub(crate) value: f64,
    pub(crate) chroma: f64,
    pub(crate) notation: String,
}

/// Temporary converter for building reference points.
struct TempConverter;

impl TempConverter {
    fn srgb_to_linear_rgb(&self, srgb: [f64; 3]) -> [f64; 3] {
        let mut linear = [0.0; 3];
        for i in 0..3 {
            linear[i] = if srgb[i] <= 0.04045 {
                srgb[i] / 12.92
            } else {
                ((srgb[i] + 0.055) / 1.055).powf(2.4)
            };
        }
        linear
    }

    fn linear_rgb_to_xyz_d65(&self, linear_rgb: [f64; 3]) -> [f64; 3] {
        let matrix = [
            [0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1191920, 0.9503041],
        ];

        let mut xyz = [0.0; 3];
        for i in 0..3 {
            xyz[i] = matrix[i][0] * linear_rgb[0] +
                     matrix[i][1] * linear_rgb[1] +
                     matrix[i][2] * linear_rgb[2];
        }
        xyz
    }

    fn xyz_to_xyy(&self, xyz: [f64; 3]) -> [f64; 3] {
        let sum = xyz[0] + xyz[1] + xyz[2];
        if sum == 0.0 {
            [0.0, 0.0, 0.0]
        } else {
            [xyz[0] / sum, xyz[1] / sum, xyz[1]]
        }
    }
}

impl MunsellConverter {
    /// Load reference data from embedded CSV dataset.
    pub(super) fn load_reference_data() -> Result<Vec<ReferenceEntry>> {
        let csv_data = include_str!("../../tests/data/srgb-to-munsell.csv");

        let mut reference_data = Vec::new();
        let mut csv_reader = csv::Reader::from_reader(csv_data.as_bytes());

        for (line_num, result) in csv_reader.records().enumerate() {
            let record = result.map_err(|e| MunsellError::ReferenceDataError {
                message: format!("CSV parsing error at line {}: {}", line_num + 2, e),
            })?;

            if record.len() < 4 {
                continue;
            }

            let r = Self::parse_csv_u8(&record, 0, line_num)?;
            let g = Self::parse_csv_u8(&record, 1, line_num)?;
            let b = Self::parse_csv_u8(&record, 2, line_num)?;

            let munsell_str = record.get(3).ok_or_else(|| MunsellError::ReferenceDataError {
                message: format!("Missing Munsell value at line {}", line_num + 2),
            })?;
            let munsell = munsell_str.trim().to_string();

            MunsellColor::from_notation(&munsell).map_err(|e| MunsellError::ReferenceDataError {
                message: format!("Invalid Munsell notation '{}' at line {}: {}", munsell, line_num + 2, e),
            })?;

            reference_data.push(ReferenceEntry {
                rgb: [r, g, b],
                munsell,
            });
        }

        if reference_data.is_empty() {
            return Err(MunsellError::ReferenceDataError {
                message: "No valid reference data found in CSV".to_string(),
            });
        }

        Ok(reference_data)
    }

    /// Parse a u8 value from a CSV record column.
    fn parse_csv_u8(
        record: &csv::StringRecord,
        col: usize,
        line_num: usize,
    ) -> Result<u8> {
        let col_name = ["R", "G", "B"][col];
        let val_str = record.get(col).ok_or_else(|| MunsellError::ReferenceDataError {
            message: format!("Missing {} value at line {}", col_name, line_num + 2),
        })?;
        val_str.trim().parse().map_err(|_| MunsellError::ReferenceDataError {
            message: format!("Invalid {} value '{}' at line {}", col_name, val_str, line_num + 2),
        })
    }

    /// Build enhanced reference points for spatial interpolation.
    pub(super) fn build_reference_points(
        reference_data: &[ReferenceEntry],
    ) -> Result<Vec<MunsellReferencePoint>> {
        let mut reference_points = Vec::with_capacity(reference_data.len());

        for entry in reference_data {
            let srgb_norm = [
                entry.rgb[0] as f64 / 255.0,
                entry.rgb[1] as f64 / 255.0,
                entry.rgb[2] as f64 / 255.0,
            ];

            let temp_converter = TempConverter;
            let linear_rgb = temp_converter.srgb_to_linear_rgb(srgb_norm);
            let xyz = temp_converter.linear_rgb_to_xyz_d65(linear_rgb);
            let xyy = temp_converter.xyz_to_xyy(xyz);

            let munsell_color = MunsellColor::from_notation(&entry.munsell)?;
            let hue = Self::extract_hue_angle(&munsell_color);

            reference_points.push(MunsellReferencePoint {
                rgb: entry.rgb,
                xyy,
                hue,
                value: munsell_color.value,
                chroma: munsell_color.chroma.unwrap_or(0.0),
                notation: entry.munsell.clone(),
            });
        }

        Ok(reference_points)
    }

    /// Extract hue angle in degrees from a MunsellColor.
    fn extract_hue_angle(munsell_color: &MunsellColor) -> f64 {
        if let Some(h) = &munsell_color.hue {
            let family = h.chars().filter(|c| c.is_alphabetic()).collect::<String>();
            let step_str = h.chars().filter(|c| c.is_numeric() || *c == '.').collect::<String>();
            let step = step_str.parse::<f64>().unwrap_or(5.0);

            let family_start_degrees = match family.as_str() {
                "R" => 0.0,
                "YR" => 36.0,
                "Y" => 72.0,
                "GY" => 108.0,
                "G" => 144.0,
                "BG" => 180.0,
                "B" => 216.0,
                "PB" => 252.0,
                "P" => 288.0,
                "RP" => 324.0,
                _ => 0.0,
            };

            let step_within_family = (step - 1.0) * 3.6;
            family_start_degrees + step_within_family
        } else {
            0.0 // Neutral colors
        }
    }
}
