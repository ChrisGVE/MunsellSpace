//! Renotation data lookup and maximum chroma functions.

use crate::error::Result;
use super::hue_conversions::bounding_hues_from_renotation;
use super::specification::{is_grey_munsell_colour, normalise_munsell_specification, luminance_astmd1535};

/// Find xyY from renotation data by direct lookup.
pub fn xyy_from_renotation(spec: &[f64; 4]) -> Result<[f64; 3]> {
    use crate::constants::MUNSELL_RENOTATION_DATA;

    if is_grey_munsell_colour(spec) {
        let value = spec[1];
        let y_lum = luminance_astmd1535(value) / 100.0;
        return Ok([
            crate::constants::ILLUMINANT_C[0],
            crate::constants::ILLUMINANT_C[1],
            y_lum,
        ]);
    }

    let spec = normalise_munsell_specification(spec);
    let hue = spec[0];
    let value = spec[1];
    let chroma = spec[2];
    let code = spec[3] as u8;

    let family = code_to_family(code)?;
    let hue_str = format_hue_string(hue, family);

    for entry in MUNSELL_RENOTATION_DATA {
        if entry.0 .0 == hue_str
            && (entry.0 .1 - value).abs() < 1e-8
            && (entry.0 .2 - chroma).abs() < 1e-8
        {
            return Ok([entry.1 .0, entry.1 .1, entry.1 .2]);
        }
    }

    Err(crate::error::MunsellError::InvalidMunsellColor(format!(
        "Specification {:?} not found in renotation data",
        [hue, value, chroma, code as f64]
    )))
}

/// Get maximum chroma from renotation data.
pub fn maximum_chroma_from_renotation(hue: f64, value: f64, code: u8) -> Result<f64> {
    use crate::constants::maximum_chromas_data::MAXIMUM_CHROMAS;

    if value >= 9.99 {
        return Ok(0.0);
    }

    let (value_minus, value_plus) = if value % 1.0 == 0.0 {
        (value, value)
    } else {
        (value.floor(), value.floor() + 1.0)
    };

    let ((hue_cw, code_cw), (hue_ccw, code_ccw)) = bounding_hues_from_renotation(hue, code);

    let (mut ma_mcw, mut ma_mccw, mut ma_pcw, mut ma_pccw) = (0.0, 0.0, 0.0, 0.0);

    for &((h, v, c), max_chroma) in MAXIMUM_CHROMAS {
        if (h - hue_cw).abs() < 1e-6 && c == code_cw && (v - value_minus).abs() < 1e-6 {
            ma_mcw = max_chroma;
        }
        if (h - hue_ccw).abs() < 1e-6 && c == code_ccw && (v - value_minus).abs() < 1e-6 {
            ma_mccw = max_chroma;
        }
        if value_plus <= 9.0 {
            if (h - hue_cw).abs() < 1e-6 && c == code_cw && (v - value_plus).abs() < 1e-6 {
                ma_pcw = max_chroma;
            }
            if (h - hue_ccw).abs() < 1e-6 && c == code_ccw && (v - value_plus).abs() < 1e-6 {
                ma_pccw = max_chroma;
            }
        }
    }

    if value_plus <= 9.0 {
        Ok(ma_mcw.min(ma_mccw).min(ma_pcw).min(ma_pccw))
    } else {
        interpolate_max_chroma_above_9(value, ma_mcw, ma_mccw)
    }
}

/// Interpolate max chroma for values > 9 using luminance-based linear interpolation.
fn interpolate_max_chroma_above_9(
    value: f64, ma_limit_cw: f64, ma_limit_ccw: f64,
) -> Result<f64> {
    let l = luminance_astmd1535(value);
    let l9 = luminance_astmd1535(9.0);
    let l10 = luminance_astmd1535(10.0);

    use crate::color_interpolation::LinearInterpolator;
    let interp_cw = LinearInterpolator::new(vec![l9, l10], vec![ma_limit_cw, 0.0])?;
    let chroma_cw = interp_cw.interpolate(l);

    let interp_ccw = LinearInterpolator::new(vec![l9, l10], vec![ma_limit_ccw, 0.0])?;
    let chroma_ccw = interp_ccw.interpolate(l);

    Ok(chroma_cw.min(chroma_ccw))
}

/// Convert hue code to family string.
fn code_to_family(code: u8) -> Result<&'static str> {
    match code {
        1 => Ok("B"),
        2 => Ok("BG"),
        3 => Ok("G"),
        4 => Ok("GY"),
        5 => Ok("Y"),
        6 => Ok("YR"),
        7 => Ok("R"),
        8 => Ok("RP"),
        9 => Ok("P"),
        10 => Ok("PB"),
        _ => Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Invalid code: {}", code),
        )),
    }
}

/// Format hue string for renotation lookup.
fn format_hue_string(hue: f64, family: &str) -> String {
    if (hue - 2.5).abs() < 1e-6 {
        format!("2.5{}", family)
    } else if (hue - 5.0).abs() < 1e-6 {
        format!("5{}", family)
    } else if (hue - 7.5).abs() < 1e-6 {
        format!("7.5{}", family)
    } else if (hue - 10.0).abs() < 1e-6 || hue.abs() < 1e-6 {
        format!("10{}", family)
    } else {
        format!("{:.1}{}", hue, family)
    }
}
