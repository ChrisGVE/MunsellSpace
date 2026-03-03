//! CIE xyY to Munsell specification conversion.
//!
//! Exact 1:1 port of Python colour-science `_xyY_to_munsell_specification`.

use crate::error::Result;
use crate::color_interpolation::{LinearInterpolator, Extrapolator, ExtrapolationMethod};
use crate::color_math_utils::euclidean_distance;
use super::hue_conversions::{hue_to_hue_angle, hue_angle_to_hue};
use super::ovoid::xy_from_renotation_ovoid_interpolated;
use super::renotation_lookup::maximum_chroma_from_renotation;
use super::specification::{
    normalise_munsell_specification, munsell_value_astmd1535, cartesian_to_cylindrical,
};

/// Convert CIE xyY to Munsell specification via iterative convergence.
pub fn xyy_to_munsell_specification(xyy: [f64; 3]) -> Result<[f64; 4]> {
    let (x, y, big_y) = (xyy[0], xyy[1], xyy[2]);
    let value = round_if_close(munsell_value_astmd1535(big_y * 100.0));
    let (x_center, y_center) = (crate::constants::ILLUMINANT_C[0], crate::constants::ILLUMINANT_C[1]);

    let (rho_input, phi_input, _) =
        cartesian_to_cylindrical(x - x_center, y - y_center, big_y);
    let phi_input = phi_input.to_degrees();

    // Grey check
    if rho_input < 1e-3 {
        return Ok(normalise_munsell_specification(&[f64::NAN, value, 0.0, f64::NAN]));
    }

    // Initial guess from Lab color space
    let initial_spec = compute_initial_guess(xyy, value)?;
    let mut specification_current = initial_spec;

    // Main convergence loop
    let convergence_threshold = 1e-3 / 1e4;
    let iterations_maximum = 64;

    for _ in 0..iterations_maximum {
        let hue_current = specification_current[0];
        let code_current = nan_safe_code(specification_current[3]);
        let chroma_current = clamp_to_max_chroma(
            specification_current[2], hue_current, value, code_current,
        )?;
        specification_current[2] = chroma_current;

        if chroma_current == 0.0 {
            return Ok([f64::NAN, value, 0.0, f64::NAN]);
        }

        // Hue refinement
        let hue_angle_new = refine_hue_angle(
            &specification_current, big_y, x_center, y_center, phi_input, value,
        )?;

        let mut hue_angle_normalized = hue_angle_new % 360.0;
        if hue_angle_normalized < 0.0 {
            hue_angle_normalized += 360.0;
        }
        let (hue_new, code_new) = hue_angle_to_hue(hue_angle_normalized);
        specification_current = [hue_new, value, chroma_current, code_new as f64];

        // Chroma refinement
        specification_current = refine_chroma(
            &specification_current, big_y, x_center, y_center, rho_input,
            hue_new, value, code_new,
        )?;

        // Convergence check
        let xy_current = xy_from_renotation_ovoid_interpolated(&specification_current)?;
        let difference = euclidean_distance(&[x, y], &[xy_current[0], xy_current[1]]);

        if difference < convergence_threshold {
            return check_hue_boundary(specification_current, x, y, value, difference);
        }
    }

    Err(crate::error::MunsellError::ConversionError {
        message: "Maximum iterations reached without convergence".to_string(),
    })
}

fn round_if_close(v: f64) -> f64 {
    if (v - v.round()).abs() < 1e-10 { v.round() } else { v }
}

fn nan_safe_code(v: f64) -> u8 {
    if v.is_nan() { 0 } else { v as u8 }
}

fn clamp_to_max_chroma(chroma: f64, hue: f64, value: f64, code: u8) -> Result<f64> {
    let max = maximum_chroma_from_renotation(hue, value, code)?;
    Ok(if chroma > max { max } else { chroma })
}

/// Compute initial guess from LCHab color space.
fn compute_initial_guess(xyy: [f64; 3], value: f64) -> Result<[f64; 4]> {
    use crate::lab_color_space::{xyy_to_xyz, xyz_to_lab, lab_to_lchab, lchab_to_munsell_specification};

    let xyz = xyy_to_xyz(xyy);
    let lab = xyz_to_lab(xyz, "C");
    let lchab = lab_to_lchab(lab);
    let initial_spec = lchab_to_munsell_specification(lchab);

    let initial_chroma = if initial_spec[2].is_nan() || initial_spec[2] < 0.1 {
        1.0
    } else if initial_spec[2] > 50.0 {
        20.0
    } else {
        initial_spec[2]
    };

    let initial_hue = if initial_spec[0].is_nan() { 5.0 } else { initial_spec[0] };

    Ok([initial_hue, value, initial_chroma, initial_spec[3]])
}

/// Refine hue angle via inner loop and interpolation.
fn refine_hue_angle(
    spec: &[f64; 4], big_y: f64,
    x_center: f64, y_center: f64, phi_input: f64, value: f64,
) -> Result<f64> {
    let hue_current = spec[0];
    let chroma_current = spec[2];
    let code_current = nan_safe_code(spec[3]);
    let hue_angle_current = hue_to_hue_angle(hue_current, code_current);

    let xy_current = xy_from_renotation_ovoid_interpolated(spec)?;
    let (_, phi_current, _) =
        cartesian_to_cylindrical(xy_current[0] - x_center, xy_current[1] - y_center, big_y);
    let phi_current = phi_current.to_degrees();

    let mut phi_diff = (360.0 - phi_input + phi_current) % 360.0;
    if phi_diff > 180.0 {
        phi_diff -= 360.0;
    }

    let mut phi_diffs = vec![phi_diff];
    let mut hue_angle_diffs = vec![0.0];
    let mut extrapolate = false;

    for iter in 1..=16 {
        if extrapolate {
            break;
        }
        if !(phi_diffs.iter().all(|&d| d >= 0.0) || phi_diffs.iter().all(|&d| d <= 0.0)) {
            break;
        }

        let hue_angle_inner =
            (hue_angle_current + iter as f64 * (phi_input - phi_current)) % 360.0;
        let mut ha_diff = (iter as f64 * (phi_input - phi_current)) % 360.0;
        if ha_diff > 180.0 {
            ha_diff -= 360.0;
        }

        let (hue_inner, code_inner) = hue_angle_to_hue(hue_angle_inner);
        let spec_inner = [hue_inner, value, chroma_current, code_inner as f64];

        let xy_inner = match xy_from_renotation_ovoid_interpolated(&spec_inner) {
            Ok(xy) => xy,
            Err(_) => {
                extrapolate = true;
                continue;
            }
        };

        if phi_diffs.len() >= 2 {
            extrapolate = true;
        }

        if !extrapolate {
            let (_, phi_inner, _) = cartesian_to_cylindrical(
                xy_inner[0] - x_center, xy_inner[1] - y_center, big_y,
            );
            let phi_inner = phi_inner.to_degrees();

            let mut phi_inner_diff = (360.0 - phi_input + phi_inner) % 360.0;
            if phi_inner_diff > 180.0 {
                phi_inner_diff -= 360.0;
            }

            phi_diffs.push(phi_inner_diff);
            hue_angle_diffs.push(ha_diff);
        }
    }

    interpolate_hue_angle(hue_angle_current, &phi_diffs, &hue_angle_diffs)
}

/// Sort and interpolate to find new hue angle. NaN-safe sorting.
fn interpolate_hue_angle(
    hue_angle_current: f64, phi_diffs: &[f64], hue_angle_diffs: &[f64],
) -> Result<f64> {
    if phi_diffs.is_empty() {
        return Ok(hue_angle_current);
    }

    let mut indices: Vec<usize> = (0..phi_diffs.len()).collect();
    indices.sort_by(|&i, &j| {
        phi_diffs[i]
            .partial_cmp(&phi_diffs[j])
            .unwrap_or(std::cmp::Ordering::Equal)
    });

    let phi_sorted: Vec<f64> = indices.iter().map(|&i| phi_diffs[i]).collect();
    let ha_sorted: Vec<f64> = indices.iter().map(|&i| hue_angle_diffs[i]).collect();

    let interpolator = LinearInterpolator::new(phi_sorted, ha_sorted)?;
    let extrapolator =
        Extrapolator::new(interpolator, ExtrapolationMethod::Linear, None, None);
    let mut ha_diff_new = extrapolator.extrapolate(0.0) % 360.0;

    // Limit hue angle change to prevent family jumping
    let max_change = 12.0;
    if ha_diff_new.abs() > max_change {
        ha_diff_new = max_change * ha_diff_new.signum();
    }

    Ok((hue_angle_current + ha_diff_new) % 360.0)
}

/// Refine chroma via inner loop and rho bracketing. NaN-safe sorting.
fn refine_chroma(
    spec: &[f64; 4], big_y: f64,
    x_center: f64, y_center: f64, rho_input: f64,
    hue_new: f64, value: f64, code_new: u8,
) -> Result<[f64; 4]> {
    let chroma_maximum = maximum_chroma_from_renotation(hue_new, value, code_new)?;
    let chroma_current = spec[2].min(chroma_maximum);
    let spec_current = [hue_new, value, chroma_current, code_new as f64];

    let xy_current = xy_from_renotation_ovoid_interpolated(&spec_current)?;
    let (rho_current, _, _) =
        cartesian_to_cylindrical(xy_current[0] - x_center, xy_current[1] - y_center, big_y);

    if (rho_current - rho_input).abs() < 1e-10 {
        return Ok(spec_current);
    }

    let mut rho_bounds = vec![rho_current];
    let mut chroma_bounds = vec![chroma_current];

    let mut rho_min = nan_safe_min(&rho_bounds);
    let mut rho_max = nan_safe_max(&rho_bounds);

    for iter in 1..=16 {
        if rho_min < rho_input && rho_input < rho_max {
            break;
        }

        let chroma_inner =
            ((rho_input / rho_current).powf(iter as f64) * chroma_current).min(chroma_maximum);
        let spec_inner = [hue_new, value, chroma_inner, code_new as f64];
        let xy_inner = xy_from_renotation_ovoid_interpolated(&spec_inner)?;
        let (rho_inner, _, _) =
            cartesian_to_cylindrical(xy_inner[0] - x_center, xy_inner[1] - y_center, big_y);

        rho_bounds.push(rho_inner);
        chroma_bounds.push(chroma_inner);
        rho_min = nan_safe_min(&rho_bounds);
        rho_max = nan_safe_max(&rho_bounds);
    }

    if rho_min >= rho_input || rho_max <= rho_input {
        let last = chroma_bounds.len() - 1;
        return Ok([hue_new, value, chroma_bounds[last], code_new as f64]);
    }

    // Sort and interpolate — NaN-safe
    let mut indices: Vec<usize> = (0..rho_bounds.len()).collect();
    indices.sort_by(|&i, &j| {
        rho_bounds[i]
            .partial_cmp(&rho_bounds[j])
            .unwrap_or(std::cmp::Ordering::Equal)
    });

    let rho_sorted: Vec<f64> = indices.iter().map(|&i| rho_bounds[i]).collect();
    let chroma_sorted: Vec<f64> = indices.iter().map(|&i| chroma_bounds[i]).collect();

    let interpolator = LinearInterpolator::new(rho_sorted, chroma_sorted)?;
    let chroma_new = interpolator.interpolate(rho_input);

    Ok([hue_new, value, chroma_new, code_new as f64])
}

/// NaN-safe minimum.
fn nan_safe_min(data: &[f64]) -> f64 {
    data.iter().copied().fold(f64::INFINITY, f64::min)
}

/// NaN-safe maximum.
fn nan_safe_max(data: &[f64]) -> f64 {
    data.iter().copied().fold(f64::NEG_INFINITY, f64::max)
}

/// Check hue boundary and prefer Python's convention for near-boundary hues.
fn check_hue_boundary(
    spec: [f64; 4], x: f64, y: f64, value: f64, difference: f64,
) -> Result<[f64; 4]> {
    let hue = spec[0];
    let code = spec[3] as u8;

    if !(hue < 0.2 || hue > 9.8) {
        return Ok(spec);
    }

    let (alt_hue, alt_code) = if hue < 0.2 {
        (hue + 10.0, if code == 1 { 10 } else { code - 1 })
    } else {
        (hue - 10.0, if code == 10 { 1 } else { code + 1 })
    };

    let alt_spec = [alt_hue, value, spec[2], alt_code as f64];

    if let Ok(xy_alt) = xy_from_renotation_ovoid_interpolated(&alt_spec) {
        let diff_alt = euclidean_distance(&[x, y], &[xy_alt[0], xy_alt[1]]);

        let prefer_alt = if hue > 9.8 {
            diff_alt <= difference * 1.05
        } else {
            diff_alt < difference * 0.95
        };

        if prefer_alt {
            return Ok(alt_spec);
        }
    }

    Ok(spec)
}
