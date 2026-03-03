//! Interpolation method selection logic.
//! MASSIVE empirical lookup table from Python colour-science.

#[allow(unused_imports)]
use super::hue_conversions::*;

#[derive(Debug, Clone, PartialEq)]
pub enum InterpolationMethod {
    None,     // No interpolation needed
    Linear,   // Linear interpolation
    Radial,   // Radial interpolation
}

/// Determine interpolation method for given Munsell specification.
/// Exact implementation of Python colour-science interpolation_method_from_renotation_ovoid
pub fn interpolation_method_from_renotation_ovoid(
    hue: f64, value: f64, chroma: f64, code: u8,
) -> InterpolationMethod {
    // Check for grey colors
    if chroma == 0.0 {
        return InterpolationMethod::None;
    }

    // Round value and chroma to integers as required
    let value = value.round() as i32;
    let chroma = (2.0 * (chroma / 2.0).round()) as i32;

    // Standard Munsell Renotation System hue, no interpolation needed
    if (hue % 2.5 - 0.0).abs() < 1e-10 {
        return InterpolationMethod::None;
    }

    let astm_hue = hue_to_astm_hue(hue, code);

    match value {
        1 => value_1_method(astm_hue, chroma),
        2 => value_2_method(astm_hue, chroma),
        3 => value_3_method(astm_hue, chroma),
        4 => value_4_method(astm_hue, chroma),
        5 => value_5_method(astm_hue, chroma),
        6 => value_6_method(astm_hue, chroma),
        7 => value_7_method(astm_hue, chroma),
        8 => value_8_method(astm_hue, chroma),
        9 => value_9_method(astm_hue, chroma),
        10 => InterpolationMethod::None,
        _ => InterpolationMethod::Linear,
    }
}

fn value_1_method(astm_hue: f64, chroma: i32) -> InterpolationMethod {
    match chroma {
        2 => {
            if (15.0 < astm_hue && astm_hue < 30.0) || (60.0 < astm_hue && astm_hue < 85.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        4 => {
            if (12.5 < astm_hue && astm_hue < 27.5) || (57.5 < astm_hue && astm_hue < 80.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        6 => {
            if 55.0 < astm_hue && astm_hue < 80.0 {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        8 => {
            if 67.5 < astm_hue && astm_hue < 77.5 {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ if chroma >= 10 => {
            if 72.5 < astm_hue && astm_hue < 77.5 {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ => InterpolationMethod::Linear
    }
}

fn value_2_method(astm_hue: f64, chroma: i32) -> InterpolationMethod {
    match chroma {
        2 => {
            if (15.0 < astm_hue && astm_hue < 27.5) || (77.5 < astm_hue && astm_hue < 80.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        4 => {
            if (12.5 < astm_hue && astm_hue < 30.0) || (62.5 < astm_hue && astm_hue < 80.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        6 => {
            if (7.5 < astm_hue && astm_hue < 22.5) || (62.5 < astm_hue && astm_hue < 80.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        8 => {
            if (7.5 < astm_hue && astm_hue < 15.0) || (60.0 < astm_hue && astm_hue < 80.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ if chroma >= 10 => {
            if 65.0 < astm_hue && astm_hue < 77.5 {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ => InterpolationMethod::Linear
    }
}

fn value_3_method(astm_hue: f64, chroma: i32) -> InterpolationMethod {
    match chroma {
        2 => {
            if (10.0 < astm_hue && astm_hue < 37.5) || (65.0 < astm_hue && astm_hue < 85.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        4 => {
            if (5.0 < astm_hue && astm_hue < 37.5) || (55.0 < astm_hue && astm_hue < 72.5) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        6 | 8 | 10 => {
            if (7.5 < astm_hue && astm_hue < 37.5) || (57.5 < astm_hue && astm_hue < 82.5) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ if chroma >= 12 => {
            if (7.5 < astm_hue && astm_hue < 42.5) || (57.5 < astm_hue && astm_hue < 80.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ => InterpolationMethod::Linear
    }
}

fn value_4_method(astm_hue: f64, chroma: i32) -> InterpolationMethod {
    match chroma {
        2 | 4 => {
            if (7.5 < astm_hue && astm_hue < 42.5) || (57.5 < astm_hue && astm_hue < 85.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        6 | 8 => {
            if (7.5 < astm_hue && astm_hue < 40.0) || (57.5 < astm_hue && astm_hue < 82.5) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ if chroma >= 10 => {
            if (7.5 < astm_hue && astm_hue < 40.0) || (57.5 < astm_hue && astm_hue < 80.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ => InterpolationMethod::Linear
    }
}

fn value_5_method(astm_hue: f64, chroma: i32) -> InterpolationMethod {
    match chroma {
        2 => {
            if (5.0 < astm_hue && astm_hue < 37.5) || (55.0 < astm_hue && astm_hue < 85.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        4 | 6 | 8 => {
            if (2.5 < astm_hue && astm_hue < 42.5) || (55.0 < astm_hue && astm_hue < 85.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ if chroma >= 10 => {
            if (2.5 < astm_hue && astm_hue < 42.5) || (55.0 < astm_hue && astm_hue < 82.5) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ => InterpolationMethod::Linear
    }
}

fn value_6_method(astm_hue: f64, chroma: i32) -> InterpolationMethod {
    match chroma {
        2 | 4 => {
            if (5.0 < astm_hue && astm_hue < 37.5) || (55.0 < astm_hue && astm_hue < 87.5) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        6 => {
            if (5.0 < astm_hue && astm_hue < 42.5) || (57.5 < astm_hue && astm_hue < 87.5) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        8 | 10 => {
            if (5.0 < astm_hue && astm_hue < 42.5) || (60.0 < astm_hue && astm_hue < 85.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        12 | 14 => {
            if (5.0 < astm_hue && astm_hue < 42.5) || (60.0 < astm_hue && astm_hue < 82.5) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ if chroma >= 16 => {
            if (5.0 < astm_hue && astm_hue < 42.5) || (60.0 < astm_hue && astm_hue < 80.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ => InterpolationMethod::Linear
    }
}

fn value_7_method(astm_hue: f64, chroma: i32) -> InterpolationMethod {
    match chroma {
        2 | 4 | 6 => {
            if (5.0 < astm_hue && astm_hue < 42.5) || (60.0 < astm_hue && astm_hue < 85.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        8 => {
            if (5.0 < astm_hue && astm_hue < 42.5) || (60.0 < astm_hue && astm_hue < 82.5) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        10 => {
            if (30.0 < astm_hue && astm_hue < 42.5) || (5.0 < astm_hue && astm_hue < 25.0) || (60.0 < astm_hue && astm_hue < 82.5) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        12 => {
            if (30.0 < astm_hue && astm_hue < 42.5) || (7.5 < astm_hue && astm_hue < 27.5) || (80.0 < astm_hue && astm_hue < 82.5) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ if chroma >= 14 => {
            if (32.5 < astm_hue && astm_hue < 40.0) || (7.5 < astm_hue && astm_hue < 15.0) || (80.0 < astm_hue && astm_hue < 82.5) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ => InterpolationMethod::Linear
    }
}

fn value_8_method(astm_hue: f64, chroma: i32) -> InterpolationMethod {
    match chroma {
        2 | 4 | 6 | 8 | 10 | 12 => {
            if (5.0 < astm_hue && astm_hue < 40.0) || (60.0 < astm_hue && astm_hue < 85.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ if chroma >= 14 => {
            if (32.5 < astm_hue && astm_hue < 40.0) || (5.0 < astm_hue && astm_hue < 15.0) || (60.0 < astm_hue && astm_hue < 85.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ => InterpolationMethod::Linear
    }
}

fn value_9_method(astm_hue: f64, chroma: i32) -> InterpolationMethod {
    match chroma {
        2 | 4 => {
            if (5.0 < astm_hue && astm_hue < 40.0) || (55.0 < astm_hue && astm_hue < 80.0) {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        6 | 8 | 10 | 12 | 14 => {
            if 5.0 < astm_hue && astm_hue < 42.5 {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ if chroma >= 16 => {
            if 35.0 < astm_hue && astm_hue < 42.5 {
                InterpolationMethod::Radial
            } else {
                InterpolationMethod::Linear
            }
        }
        _ => InterpolationMethod::Linear
    }
}
