//! Renotation ovoid interpolation — xy coordinate computation from Munsell specs.

use crate::error::Result;
use super::hue_conversions::{hue_to_hue_angle, bounding_hues_from_renotation};
use super::interpolation_methods::interpolation_method_from_renotation_ovoid;
use super::renotation_lookup::{xyy_from_renotation, maximum_chroma_from_renotation};
use super::specification::{
    is_grey_munsell_colour, normalise_munsell_specification,
    luminance_astmd1535, cartesian_to_cylindrical, polar_to_cartesian,
};
use super::lerp;

/// Convert Munsell specification to xy chromaticity with full interpolation.
pub fn xy_from_renotation_ovoid_interpolated(spec: &[f64; 4]) -> Result<[f64; 2]> {
    let spec = normalise_munsell_specification(spec);

    if is_grey_munsell_colour(&spec) {
        return Ok(crate::constants::ILLUMINANT_C);
    }

    let value = spec[1];
    let chroma = spec[2];

    // Handle very low chromas by interpolating with grey
    if chroma < 2.0 {
        return interpolate_low_chroma(&spec, value, chroma);
    }

    // Handle value interpolation for non-integer values
    if (value - value.round()).abs() > 1e-10 {
        return interpolate_fractional_value(&spec, value);
    }

    // Special case for value=10 (ideal white)
    if value >= 10.0 {
        return Ok(crate::constants::ILLUMINANT_C);
    }

    // Check maximum available chroma
    let max_chroma = maximum_chroma_from_renotation(spec[0], value, spec[3] as u8)?;

    // Handle chromas beyond available data
    if chroma > max_chroma {
        return extrapolate_high_chroma(&spec, value, chroma, max_chroma);
    }

    // Handle non-even chromas
    if (2.0 * (chroma / 2.0 - (chroma / 2.0).round())).abs() > 1e-10 {
        return interpolate_odd_chroma(&spec, value, chroma, max_chroma);
    }

    // Standard specification: try direct lookup
    let is_standard_hue = (spec[0] % 2.5).abs() < 1e-10;
    let is_integer_value = (value - value.round()).abs() < 1e-10;
    let is_even_chroma = (chroma % 2.0).abs() < 1e-10;

    if is_standard_hue && is_integer_value && is_even_chroma {
        standard_spec_lookup(&spec, value, chroma)
    } else {
        non_standard_spec_interpolation(&spec, value)
    }
}

/// Interpolate between grey and chroma=2 for low-chroma colors.
fn interpolate_low_chroma(spec: &[f64; 4], value: f64, chroma: f64) -> Result<[f64; 2]> {
    let xy_grey = crate::constants::ILLUMINANT_C;

    let xy_chroma2 = if (value - value.round()).abs() < 1e-10 {
        let spec_c2 = [spec[0], value, 2.0, spec[3]];
        xy_from_renotation_ovoid_interpolated(&spec_c2)?
    } else if value > 9.0 {
        interpolate_above_9_at_chroma2(spec, value)?
    } else {
        interpolate_fractional_value_at_chroma2(spec, value)?
    };

    let t = chroma / 2.0;
    Ok([
        xy_grey[0] * (1.0 - t) + xy_chroma2[0] * t,
        xy_grey[1] * (1.0 - t) + xy_chroma2[1] * t,
    ])
}

fn interpolate_above_9_at_chroma2(spec: &[f64; 4], value: f64) -> Result<[f64; 2]> {
    let spec_9 = [spec[0], 9.0, 2.0, spec[3]];
    let xy_9 = xy_from_renotation_ovoid_interpolated(&spec_9)?;
    let xy_10 = crate::constants::ILLUMINANT_C;

    let y_current = luminance_astmd1535(value);
    let y_9 = luminance_astmd1535(9.0);
    let y_10 = luminance_astmd1535(10.0);
    let t = (y_current - y_9) / (y_10 - y_9);

    Ok([
        xy_9[0] + t * (xy_10[0] - xy_9[0]),
        xy_9[1] + t * (xy_10[1] - xy_9[1]),
    ])
}

fn interpolate_fractional_value_at_chroma2(spec: &[f64; 4], value: f64) -> Result<[f64; 2]> {
    let value_floor = value.floor();
    let value_ceil = value.ceil();

    let (val_low, val_high) = if value_floor < 1.0 {
        (1.0, 2.0)
    } else {
        (value_floor, value_ceil)
    };

    let xy_low = xy_from_renotation_ovoid_interpolated(&[spec[0], val_low, 2.0, spec[3]])?;
    let xy_high = xy_from_renotation_ovoid_interpolated(&[spec[0], val_high, 2.0, spec[3]])?;

    let t = (value - val_low) / (val_high - val_low);
    Ok([
        xy_low[0] + t * (xy_high[0] - xy_low[0]),
        xy_low[1] + t * (xy_high[1] - xy_low[1]),
    ])
}

/// Interpolate between floor and ceil integer values.
fn interpolate_fractional_value(spec: &[f64; 4], value: f64) -> Result<[f64; 2]> {
    // Clamp floor to MINIMUM_RENOTATION_VALUE: the dataset has no entries at
    // Value 0.0, so floor(V) for V in (0.2, 1.0) must use 0.2 as lower bound.
    let value_floor = value.floor().max(crate::constants::MINIMUM_RENOTATION_VALUE);
    let value_ceil = value.ceil();

    if value_ceil > 9.0 {
        return interpolate_above_9(spec, value);
    }

    let xy_floor = xy_from_renotation_ovoid_interpolated(&[spec[0], value_floor, spec[2], spec[3]])?;
    let xy_ceil = xy_from_renotation_ovoid_interpolated(&[spec[0], value_ceil, spec[2], spec[3]])?;

    let t = value - value_floor;
    Ok([
        xy_floor[0] * (1.0 - t) + xy_ceil[0] * t,
        xy_floor[1] * (1.0 - t) + xy_ceil[1] * t,
    ])
}

fn interpolate_above_9(spec: &[f64; 4], value: f64) -> Result<[f64; 2]> {
    if spec[2] > 0.0 {
        let xy_9 = xy_from_renotation_ovoid_interpolated(&[spec[0], 9.0, spec[2], spec[3]])?;
        let xy_10 = crate::constants::ILLUMINANT_C;

        let y_current = luminance_astmd1535(value);
        let y_9 = luminance_astmd1535(9.0);
        let y_10 = luminance_astmd1535(10.0);
        let t = (y_current - y_9) / (y_10 - y_9);

        Ok([
            xy_9[0] + t * (xy_10[0] - xy_9[0]),
            xy_9[1] + t * (xy_10[1] - xy_9[1]),
        ])
    } else {
        Ok(crate::constants::ILLUMINANT_C)
    }
}

/// Extrapolate beyond max available chroma.
fn extrapolate_high_chroma(
    spec: &[f64; 4], value: f64, chroma: f64, max_chroma: f64,
) -> Result<[f64; 2]> {
    let mut highest = (max_chroma / 2.0).floor() * 2.0;
    if highest > max_chroma {
        highest -= 2.0;
    }
    let second = highest - 2.0;

    if second < 2.0 {
        return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Cannot extrapolate chroma {} with max available {}", chroma, max_chroma),
        ));
    }

    let xy_high = xy_from_renotation_ovoid(&[spec[0], value, highest, spec[3]])?;
    let xy_second = xy_from_renotation_ovoid(&[spec[0], value, second, spec[3]])?;

    let steps = (chroma - highest) / 2.0;
    Ok([
        xy_high[0] + steps * (xy_high[0] - xy_second[0]),
        xy_high[1] + steps * (xy_high[1] - xy_second[1]),
    ])
}

/// Interpolate between bounding even chromas.
fn interpolate_odd_chroma(
    spec: &[f64; 4], value: f64, chroma: f64, max_chroma: f64,
) -> Result<[f64; 2]> {
    let chroma_lower = 2.0 * (chroma / 2.0).floor();
    let chroma_upper = chroma_lower + 2.0;

    if chroma_upper > max_chroma {
        return extrapolate_odd_chroma(spec, value, chroma, chroma_lower);
    }

    let xy_lower = xy_from_renotation_ovoid(&[spec[0], value, chroma_lower, spec[3]])?;
    let xy_upper = xy_from_renotation_ovoid(&[spec[0], value, chroma_upper, spec[3]])?;

    let t = (chroma - chroma_lower) / 2.0;
    Ok([
        xy_lower[0] * (1.0 - t) + xy_upper[0] * t,
        xy_lower[1] * (1.0 - t) + xy_upper[1] * t,
    ])
}

fn extrapolate_odd_chroma(
    spec: &[f64; 4], value: f64, chroma: f64, chroma_lower: f64,
) -> Result<[f64; 2]> {
    let chroma_second = chroma_lower - 2.0;
    if chroma_second < 2.0 {
        return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Cannot interpolate chroma {}", chroma),
        ));
    }

    let xy_lower = xy_from_renotation_ovoid(&[spec[0], value, chroma_lower, spec[3]])?;
    let xy_second = xy_from_renotation_ovoid(&[spec[0], value, chroma_second, spec[3]])?;

    let t = (chroma - chroma_lower) / 2.0;
    Ok([
        xy_lower[0] + t * (xy_lower[0] - xy_second[0]),
        xy_lower[1] + t * (xy_lower[1] - xy_second[1]),
    ])
}

/// Handle standard (2.5-step hue, integer value, even chroma) specifications.
fn standard_spec_lookup(spec: &[f64; 4], value: f64, chroma: f64) -> Result<[f64; 2]> {
    match xyy_from_renotation(spec) {
        Ok(xyy) => Ok([xyy[0], xyy[1]]),
        Err(_) => extrapolate_standard_spec(spec, value, chroma),
    }
}

fn extrapolate_standard_spec(spec: &[f64; 4], value: f64, chroma: f64) -> Result<[f64; 2]> {
    let max_chroma = maximum_chroma_from_renotation(spec[0], spec[1], spec[3] as u8)?;

    if chroma > max_chroma {
        let mut highest = (max_chroma / 2.0).floor() * 2.0;
        if highest > max_chroma {
            highest -= 2.0;
        }
        let second = highest - 2.0;

        if second < 2.0 {
            return Err(crate::error::MunsellError::InvalidMunsellColor(
                format!("Cannot extrapolate chroma {} with max available {}", chroma, max_chroma),
            ));
        }

        let xyy_high = xyy_from_renotation(&[spec[0], value, highest, spec[3]])?;
        let xyy_second = xyy_from_renotation(&[spec[0], value, second, spec[3]])?;

        let steps = (chroma - highest) / 2.0;
        Ok([
            xyy_high[0] + steps * (xyy_high[0] - xyy_second[0]),
            xyy_high[1] + steps * (xyy_high[1] - xyy_second[1]),
        ])
    } else {
        Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Specification {:?} not found despite being within range", spec),
        ))
    }
}

/// Handle non-standard specifications via value interpolation.
fn non_standard_spec_interpolation(spec: &[f64; 4], value: f64) -> Result<[f64; 2]> {
    let value_floor = value.floor();
    let value_ceil = value.ceil();

    if (value - value_floor).abs() > 1e-10 && value_floor != value_ceil {
        let val_ceil = value_ceil.min(9.0);
        let val_floor = value_floor.max(1.0);

        let xy_floor = xy_from_renotation_ovoid(&[spec[0], val_floor, spec[2], spec[3]])?;
        let xy_ceil = xy_from_renotation_ovoid(&[spec[0], val_ceil, spec[2], spec[3]])?;

        let t = value - value_floor;
        Ok([
            xy_floor[0] + t * (xy_ceil[0] - xy_floor[0]),
            xy_floor[1] + t * (xy_ceil[1] - xy_floor[1]),
        ])
    } else {
        xy_from_renotation_ovoid(spec)
    }
}

// ─── xy_from_renotation_ovoid ───────────────────────────────────────────

/// Convert Munsell specification to xy using bounding-hue interpolation.
pub fn xy_from_renotation_ovoid(spec: &[f64; 4]) -> Result<[f64; 2]> {
    let spec = normalise_munsell_specification(spec);

    if is_grey_munsell_colour(&spec) {
        return Ok(crate::constants::ILLUMINANT_C);
    }

    let hue = spec[0];
    let value = spec[1];
    let chroma = spec[2];
    let code = spec[3] as u8;

    validate_ovoid_inputs(value, chroma)?;

    let value_for_lookup = value.min(9.0);
    let chroma = 2.0 * (chroma / 2.0).round();

    // For standard hues, try direct lookup first
    if (hue % 2.5).abs() < 1e-10 {
        let standard_hue = 2.5 * (hue / 2.5).round();
        if let Ok(xyy) = xyy_from_renotation(&[standard_hue, value_for_lookup, chroma, spec[3]]) {
            return Ok([xyy[0], xyy[1]]);
        }
    }

    // Non-standard hue: interpolate between bounding hues
    let ((hue_minus, code_minus), (hue_plus, code_plus)) =
        bounding_hues_from_renotation(hue, code);
    let (x_grey, y_grey) = (
        crate::constants::ILLUMINANT_C[0],
        crate::constants::ILLUMINANT_C[1],
    );

    let (x_minus, y_minus, y_val_minus) =
        resolve_bounding_xyy(hue_minus, value_for_lookup, value, chroma, code_minus)?;
    let (x_plus, y_plus, y_val_plus) =
        resolve_bounding_xyy(hue_plus, value_for_lookup, value, chroma, code_plus)?;

    interpolate_between_hues(
        hue, code, hue_minus, code_minus, hue_plus, code_plus,
        x_minus, y_minus, y_val_minus, x_plus, y_plus, y_val_plus,
        x_grey, y_grey, value, chroma,
    )
}

fn validate_ovoid_inputs(value: f64, chroma: f64) -> Result<()> {
    if value < 1.0 || value > 9.5 {
        return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Value {} must be in range [1, 9.5]", value),
        ));
    }
    if chroma < 2.0 {
        return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Chroma {} must be at least 2.0", chroma),
        ));
    }
    if (2.0 * (chroma / 2.0 - (chroma / 2.0).round())).abs() > 1e-10 {
        return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Chroma {} must be even", chroma),
        ));
    }
    Ok(())
}

/// Resolve xyY for a bounding hue, with extrapolation/fallback as needed.
fn resolve_bounding_xyy(
    hue: f64, value_lookup: f64, value: f64, chroma: f64, code: u8,
) -> Result<(f64, f64, f64)> {
    let max_chroma = maximum_chroma_from_renotation(hue, value_lookup, code)?;

    if chroma <= max_chroma {
        resolve_within_max_chroma(hue, value_lookup, value, chroma, code)
    } else {
        extrapolate_beyond_max(hue, value_lookup, chroma, code, max_chroma)
    }
}

fn resolve_within_max_chroma(
    hue: f64, value_lookup: f64, value: f64, chroma: f64, code: u8,
) -> Result<(f64, f64, f64)> {
    let spec = [hue, value_lookup, chroma, code as f64];
    match xyy_from_renotation(&spec) {
        Ok(xyy) => Ok((xyy[0], xyy[1], xyy[2])),
        Err(_) => fallback_chroma_search(hue, value_lookup, value, chroma, code),
    }
}

fn fallback_chroma_search(
    hue: f64, value_lookup: f64, value: f64, chroma: f64, code: u8,
) -> Result<(f64, f64, f64)> {
    let mut test_chroma = chroma;
    let mut found_xyy = None;

    while test_chroma >= 2.0 {
        let test_spec = [hue, value, test_chroma, code as f64];
        if let Ok(xyy) = xyy_from_renotation(&test_spec) {
            found_xyy = Some((xyy, test_chroma));
            break;
        }
        test_chroma -= 2.0;
    }

    match found_xyy {
        Some((xyy, tc)) if tc == chroma => Ok((xyy[0], xyy[1], xyy[2])),
        Some((xyy_high, tc)) if tc >= 4.0 => {
            let second_spec = [hue, value, tc - 2.0, code as f64];
            if let Ok(xyy_second) = xyy_from_renotation(&second_spec) {
                let steps = (chroma - tc) / 2.0;
                Ok((
                    xyy_high[0] + steps * (xyy_high[0] - xyy_second[0]),
                    xyy_high[1] + steps * (xyy_high[1] - xyy_second[1]),
                    xyy_high[2],
                ))
            } else {
                Ok((xyy_high[0], xyy_high[1], xyy_high[2]))
            }
        }
        Some((xyy, _)) => Ok((xyy[0], xyy[1], xyy[2])),
        None => {
            let (x_c, y_c) = (
                crate::constants::ILLUMINANT_C[0],
                crate::constants::ILLUMINANT_C[1],
            );
            Ok((x_c, y_c, luminance_astmd1535(value_lookup) / 100.0))
        }
    }
}

fn extrapolate_beyond_max(
    hue: f64, value_lookup: f64, chroma: f64, code: u8, max_chroma: f64,
) -> Result<(f64, f64, f64)> {
    let highest_even = (max_chroma / 2.0).floor() * 2.0;
    if highest_even < 4.0 {
        return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Cannot extrapolate from chroma {}", highest_even),
        ));
    }

    let xyy_high = xyy_from_renotation(&[hue, value_lookup, highest_even, code as f64])?;
    let xyy_second =
        xyy_from_renotation(&[hue, value_lookup, highest_even - 2.0, code as f64])?;

    let steps = (chroma - highest_even) / 2.0;
    Ok((
        xyy_high[0] + steps * (xyy_high[0] - xyy_second[0]),
        xyy_high[1] + steps * (xyy_high[1] - xyy_second[1]),
        xyy_high[2],
    ))
}

/// Interpolate between bounding hues using Linear or Radial method.
#[allow(clippy::too_many_arguments)]
fn interpolate_between_hues(
    hue: f64, code: u8,
    hue_minus: f64, code_minus: u8, hue_plus: f64, code_plus: u8,
    x_minus: f64, y_minus: f64, y_val_minus: f64,
    x_plus: f64, y_plus: f64, y_val_plus: f64,
    x_grey: f64, y_grey: f64,
    value: f64, chroma: f64,
) -> Result<[f64; 2]> {
    let (rho_minus, phi_m, _) =
        cartesian_to_cylindrical(x_minus - x_grey, y_minus - y_grey, y_val_minus);
    let phi_minus = phi_m.to_degrees();

    let (rho_plus, phi_p, _) =
        cartesian_to_cylindrical(x_plus - x_grey, y_plus - y_grey, y_val_plus);
    let mut phi_plus = phi_p.to_degrees();

    let mut hue_angle_lower = hue_to_hue_angle(hue_minus, code_minus);
    let hue_angle = hue_to_hue_angle(hue, code);
    let hue_angle_upper = hue_to_hue_angle(hue_plus, code_plus);

    if phi_minus - phi_plus > 180.0 {
        phi_plus += 360.0;
    }
    if hue_angle_lower == 0.0 {
        hue_angle_lower = 360.0;
    }

    let mut hue_angle_adj = hue_angle;
    if hue_angle_lower > hue_angle_upper {
        if hue_angle_lower > hue_angle {
            hue_angle_lower -= 360.0;
        } else {
            hue_angle_lower -= 360.0;
            hue_angle_adj -= 360.0;
        }
    }

    let method = interpolation_method_from_renotation_ovoid(hue, value, chroma, code);

    match method {
        None => Err(crate::error::MunsellError::InvalidMunsellColor(
            "Interpolation method must be Linear or Radial".to_string(),
        )),
        Some("Linear") => {
            let x = lerp(hue_angle_lower, hue_angle_upper, x_minus, x_plus, hue_angle_adj);
            let y = lerp(hue_angle_lower, hue_angle_upper, y_minus, y_plus, hue_angle_adj);
            Ok([x, y])
        }
        Some("Radial") => {
            let rho = lerp(hue_angle_lower, hue_angle_upper, rho_minus, rho_plus, hue_angle_adj);
            let phi = lerp(hue_angle_lower, hue_angle_upper, phi_minus, phi_plus, hue_angle_adj);
            let (dx, dy) = polar_to_cartesian(rho, phi.to_radians());
            Ok([dx + x_grey, dy + y_grey])
        }
        _ => unreachable!(),
    }
}
