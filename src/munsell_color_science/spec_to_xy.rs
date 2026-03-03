//! Munsell specification to CIE xy and xyY conversion.

use crate::error::Result;
use super::ovoid::xy_from_renotation_ovoid_interpolated;
use super::specification::{
    is_grey_munsell_colour, normalise_munsell_specification, luminance_astmd1535,
};
use super::lerp;

/// Convert Munsell specification to xy chromaticity coordinates.
///
/// Handles chroma interpolation between even values via the ovoid.
pub fn munsell_specification_to_xy(spec: &[f64; 4]) -> Result<[f64; 2]> {
    let spec = normalise_munsell_specification(spec);

    if is_grey_munsell_colour(&spec) {
        return Ok(crate::constants::ILLUMINANT_C);
    }

    let hue = spec[0];
    let value = spec[1];
    let chroma = spec[2];
    let code = spec[3] as u8;

    if value < 0.0 || value > 10.0 {
        return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Value {} must be in range [0, 10]", value),
        ));
    }

    let (chroma_minus, chroma_plus) =
        if (chroma / 2.0 - (chroma / 2.0).round()).abs() < 1e-10 {
            (chroma, chroma)
        } else {
            (
                2.0 * (chroma / 2.0).floor(),
                2.0 * (chroma / 2.0).floor() + 2.0,
            )
        };

    let (x_minus, y_minus) = if chroma_minus == 0.0 {
        (crate::constants::ILLUMINANT_C[0], crate::constants::ILLUMINANT_C[1])
    } else {
        let xy = xy_from_renotation_ovoid_interpolated(&[hue, value, chroma_minus, code as f64])?;
        (xy[0], xy[1])
    };

    let xy_plus = xy_from_renotation_ovoid_interpolated(&[hue, value, chroma_plus, code as f64])?;
    let (x_plus, y_plus) = (xy_plus[0], xy_plus[1]);

    if chroma_minus == chroma_plus {
        Ok([x_minus, y_minus])
    } else {
        Ok([
            lerp(chroma_minus, chroma_plus, x_minus, x_plus, chroma),
            lerp(chroma_minus, chroma_plus, y_minus, y_plus, chroma),
        ])
    }
}

/// Convert Munsell specification to CIE xyY colourspace.
///
/// Handles value interpolation using luminance-based weighting.
pub fn munsell_specification_to_xyy(spec: &[f64; 4]) -> Result<[f64; 3]> {
    let spec = normalise_munsell_specification(spec);
    let value = spec[1];

    if !is_grey_munsell_colour(&spec) {
        validate_spec_domain(&spec)?;
    }

    let y_luminance = luminance_astmd1535(value);

    let (value_minus, value_plus) = if (value - value.round()).abs() < 1e-10 {
        (value.round(), value.round())
    } else {
        (value.floor(), value.floor() + 1.0)
    };

    let spec_minus = value_boundary_spec(&spec, value_minus);
    let xy_minus = munsell_specification_to_xy(&spec_minus)?;

    let spec_plus = value_boundary_spec_upper(&spec, value_plus);
    let xy_plus = munsell_specification_to_xy(&spec_plus)?;

    let (x, y) = if value_minus == value_plus {
        (xy_minus[0], xy_minus[1])
    } else {
        let y_minus_lum = luminance_astmd1535(value_minus);
        let y_plus_lum = luminance_astmd1535(value_plus);
        (
            lerp(y_minus_lum, y_plus_lum, xy_minus[0], xy_plus[0], y_luminance),
            lerp(y_minus_lum, y_plus_lum, xy_minus[1], xy_plus[1], y_luminance),
        )
    };

    Ok([x, y, y_luminance / 100.0])
}

fn validate_spec_domain(spec: &[f64; 4]) -> Result<()> {
    let hue = spec[0];
    let value = spec[1];

    if hue < 0.0 || hue > 10.0 {
        return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Hue {} must be in range [0, 10]", hue),
        ));
    }
    if value < 0.0 || value > 10.0 {
        return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Value {} must be in range [0, 10]", value),
        ));
    }
    Ok(())
}

fn value_boundary_spec(spec: &[f64; 4], v: f64) -> [f64; 4] {
    if is_grey_munsell_colour(spec) {
        [f64::NAN, v, f64::NAN, f64::NAN]
    } else {
        [spec[0], v, spec[2], spec[3]]
    }
}

fn value_boundary_spec_upper(spec: &[f64; 4], v: f64) -> [f64; 4] {
    if is_grey_munsell_colour(spec) || v == 10.0 {
        [f64::NAN, v, f64::NAN, f64::NAN]
    } else {
        [spec[0], v, spec[2], spec[3]]
    }
}
