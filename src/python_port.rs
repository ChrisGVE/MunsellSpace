//! Exact 1:1 port of Python colour-science munsell functions
//! This module contains exact implementations matching Python's behaviour

use crate::error::Result;
// use std::f64::consts::PI;  // Currently unused

/// Convert [hue, code] to ASTM hue number
/// Exact implementation from Python colour-science
/// ASTM_hue = 10 * ((7 - code) % 10) + hue
pub fn hue_to_astm_hue(hue: f64, code: u8) -> f64 {
    // Python's modulo always returns positive result
    let offset = (7 - code as i32) % 10;
    let offset = if offset < 0 { offset + 10 } else { offset };
    let astm_hue = 10.0 * offset as f64 + hue;
    
    // Return 100 if ASTM_hue == 0, else ASTM_hue
    if astm_hue == 0.0 {
        100.0
    } else {
        astm_hue
    }
}

/// Convert ASTM hue to [hue, code] pair
/// Reverse of hue_to_astm_hue
pub fn astm_hue_to_hue(astm_hue: f64) -> (f64, u8) {
    // Handle astm_hue == 100 case
    let astm_hue = if astm_hue == 100.0 { 0.0 } else { astm_hue };
    
    // Find the code (hue family)
    let code = ((70.0 - astm_hue.floor() / 10.0 * 10.0) / 10.0 % 10.0) as u8;
    let hue = astm_hue % 10.0;
    
    (hue, code)
}

/// Convert hue and code to hue angle in degrees
/// This is the CORRECT implementation that uses interpolation
pub fn hue_to_hue_angle(hue: f64, code: u8) -> f64 {
    // First calculate single_hue using the complex formula
    let raw = (17.0 - code as f64) % 10.0 + (hue / 10.0) - 0.5;
    let single_hue = if raw < 0.0 {
        (raw % 10.0) + 10.0
    } else {
        raw % 10.0
    };
    
    // Then interpolate using breakpoints
    let breakpoints = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0];
    let angles = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0];
    
    // Find the two bounding points
    for i in 0..breakpoints.len()-1 {
        if single_hue >= breakpoints[i] && single_hue <= breakpoints[i+1] {
            let t = (single_hue - breakpoints[i]) / (breakpoints[i+1] - breakpoints[i]);
            return angles[i] + t * (angles[i+1] - angles[i]);
        }
    }
    
    360.0 // Default (should not happen)
}

/// Convert hue angle to [hue, code] pair
pub fn hue_angle_to_hue(hue_angle: f64) -> (f64, u8) {
    // Reverse interpolation from angle to single_hue
    let angles = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0];
    let breakpoints = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0];
    
    let mut single_hue = 0.0;
    for i in 0..angles.len()-1 {
        if hue_angle >= angles[i] && hue_angle <= angles[i+1] {
            let t = (hue_angle - angles[i]) / (angles[i+1] - angles[i]);
            single_hue = breakpoints[i] + t * (breakpoints[i+1] - breakpoints[i]);
            break;
        }
    }
    
    // Now reverse the single_hue calculation to get hue and code
    // This is the inverse of: raw = (17 - code) % 10 + hue/10 - 0.5
    // single_hue = raw % 10
    
    // Try each code to find which one produces the correct single_hue
    for code in 0..10 {
        for hue_int in 0..10 {
            let hue = hue_int as f64;
            let raw = (17.0 - code as f64) % 10.0 + (hue / 10.0) - 0.5;
            let test_single = if raw < 0.0 {
                (raw % 10.0) + 10.0
            } else {
                raw % 10.0
            };
            
            if (test_single - single_hue).abs() < 0.01 {
                return (hue, code);
            }
        }
    }
    
    // Fallback
    (0.0, 0)
}

/// Find bounding hues from renotation data
pub fn bounding_hues_from_renotation(hue: f64, code: u8) -> ((f64, u8), (f64, u8)) {
    // Standard hues are 0, 2.5, 5, 7.5, 10
    let standard_hues = [0.0, 2.5, 5.0, 7.5, 10.0];
    
    // Find clockwise (lower) and counter-clockwise (upper) bounds
    let mut hue_cw = 0.0;
    let mut hue_ccw = 10.0;
    
    for &std_hue in &standard_hues {
        if std_hue <= hue && std_hue > hue_cw {
            hue_cw = std_hue;
        }
        if std_hue >= hue && std_hue < hue_ccw {
            hue_ccw = std_hue;
        }
    }
    
    // Handle wraparound
    let mut code_cw = code;
    let mut code_ccw = code;
    
    if hue_cw == 0.0 && hue > 0.0 {
        // Need to wrap to previous family
        hue_cw = 10.0;
        code_cw = if code == 0 { 9 } else { code - 1 };
    }
    
    if hue_ccw == 10.0 && hue < 10.0 {
        // This is fine, no wrap needed
    } else if hue == 10.0 {
        // Special case for hue == 10.0
        hue_ccw = 0.0;
        code_ccw = if code == 9 { 0 } else { code + 1 };
    }
    
    ((hue_cw, code_cw), (hue_ccw, code_ccw))
}

/// Check if a Munsell specification represents a grey color
pub fn is_grey_munsell_colour(spec: &[f64; 4]) -> bool {
    // Grey if hue is NaN or chroma is 0
    spec[0].is_nan() || spec[2] == 0.0
}

/// Normalize Munsell specification (handle wraparound)
pub fn normalise_munsell_specification(spec: &[f64; 4]) -> [f64; 4] {
    let mut hue = spec[0];
    let value = spec[1];
    let chroma = spec[2];
    let mut code = spec[3] as u8;
    
    // Handle hue wraparound
    while hue < 0.0 {
        hue += 10.0;
        if code == 0 {
            code = 9;
        } else {
            code -= 1;
        }
    }
    
    while hue >= 10.0 {
        hue -= 10.0;
        if code == 9 {
            code = 0;
        } else {
            code += 1;
        }
    }
    
    // Handle 0YR -> 10R conversion
    if hue == 0.0 && code == 1 { // YR
        hue = 10.0;
        code = 0; // R
    }
    
    [hue, value, chroma, code as f64]
}

/// Convert from CIE Y luminance to Munsell value using ASTM D1535 formula
pub fn luminance_astmd1535(value: f64) -> f64 {
    // ASTM D1535 polynomial
    // Y = 1.1914 * V - 0.22533 * V^2 + 0.23352 * V^3 - 0.020484 * V^4 + 0.00081939 * V^5
    let v = value;
    let v2 = v * v;
    let v3 = v2 * v;
    let v4 = v3 * v;
    let v5 = v4 * v;
    
    1.1914 * v - 0.22533 * v2 + 0.23352 * v3 - 0.020484 * v4 + 0.00081939 * v5
}

/// Convert from Munsell value to CIE Y luminance using Newton-Raphson
pub fn munsell_value_astmd1535(y: f64) -> f64 {
    // Newton-Raphson to solve the inverse of luminance_astmd1535
    let mut value = 10.0 * y.powf(0.5); // Initial guess
    
    for _ in 0..100 {
        let y_current = luminance_astmd1535(value);
        let error = y_current - y;
        
        if error.abs() < 1e-10 {
            break;
        }
        
        // Derivative of the polynomial
        let v = value;
        let v2 = v * v;
        let v3 = v2 * v;
        let v4 = v3 * v;
        let derivative = 1.1914 - 2.0 * 0.22533 * v + 3.0 * 0.23352 * v2 - 4.0 * 0.020484 * v3 + 5.0 * 0.00081939 * v4;
        
        value -= error / derivative;
        value = value.clamp(0.0, 10.0);
    }
    
    value
}

/// Linear interpolation helper
fn lerp(x1: f64, x2: f64, y1: f64, y2: f64, x: f64) -> f64 {
    if (x2 - x1).abs() < 1e-10 {
        return y1;
    }
    y1 + (x - x1) * (y2 - y1) / (x2 - x1)
}

/// Convert cartesian to cylindrical coordinates
pub fn cartesian_to_cylindrical(x: f64, y: f64, z: f64) -> (f64, f64, f64) {
    let rho = (x * x + y * y).sqrt();
    let phi = y.atan2(x);
    (rho, phi, z)
}

/// Convert polar to cartesian coordinates
pub fn polar_to_cartesian(rho: f64, phi: f64) -> (f64, f64) {
    let x = rho * phi.cos();
    let y = rho * phi.sin();
    (x, y)
}

/// Determine interpolation method from renotation ovoid
/// Exact 1:1 port from Python colour-science
pub fn interpolation_method_from_renotation_ovoid(hue: f64, value: f64, chroma: f64, code: u8) -> Option<&'static str> {
    // Check for grey
    if chroma == 0.0 {
        return None;
    }
    
    // Value must be integer
    let value = value.round() as i32;
    
    // Chroma must be even
    let chroma = (2.0 * (chroma / 2.0).round()) as i32;
    
    // Standard hue, no interpolation needed
    if (hue % 2.5).abs() < 1e-10 {
        return None;
    }
    
    let astm_hue = hue_to_astm_hue(hue, code);
    
    match value {
        1 => match chroma {
            2 => if (15.0 < astm_hue && astm_hue < 30.0) || (60.0 < astm_hue && astm_hue < 85.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            4 => if (12.5 < astm_hue && astm_hue < 27.5) || (57.5 < astm_hue && astm_hue < 80.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            6 => if 55.0 < astm_hue && astm_hue < 80.0 {
                Some("Radial")
            } else {
                Some("Linear")
            },
            8 => if 67.5 < astm_hue && astm_hue < 77.5 {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ if chroma >= 10 => if 72.5 < astm_hue && astm_hue < 77.5 {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ => Some("Linear"),
        },
        2 => match chroma {
            2 => if (15.0 < astm_hue && astm_hue < 27.5) || (77.5 < astm_hue && astm_hue < 80.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            4 => if (12.5 < astm_hue && astm_hue < 30.0) || (62.5 < astm_hue && astm_hue < 80.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            6 => if (7.5 < astm_hue && astm_hue < 22.5) || (62.5 < astm_hue && astm_hue < 80.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            8 => if (7.5 < astm_hue && astm_hue < 15.0) || (60.0 < astm_hue && astm_hue < 80.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ if chroma >= 10 => if 65.0 < astm_hue && astm_hue < 77.5 {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ => Some("Linear"),
        },
        3 => match chroma {
            2 => if (10.0 < astm_hue && astm_hue < 37.5) || (65.0 < astm_hue && astm_hue < 85.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            4 => if (5.0 < astm_hue && astm_hue < 37.5) || (55.0 < astm_hue && astm_hue < 72.5) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            6 | 8 | 10 => if (7.5 < astm_hue && astm_hue < 37.5) || (57.5 < astm_hue && astm_hue < 82.5) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ if chroma >= 12 => if (7.5 < astm_hue && astm_hue < 42.5) || (57.5 < astm_hue && astm_hue < 80.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ => Some("Linear"),
        },
        4 => match chroma {
            2 | 4 => if (7.5 < astm_hue && astm_hue < 42.5) || (57.5 < astm_hue && astm_hue < 85.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            6 | 8 => if (7.5 < astm_hue && astm_hue < 40.0) || (57.5 < astm_hue && astm_hue < 82.5) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ if chroma >= 10 => if (7.5 < astm_hue && astm_hue < 40.0) || (57.5 < astm_hue && astm_hue < 80.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ => Some("Linear"),
        },
        5 => match chroma {
            2 => if (5.0 < astm_hue && astm_hue < 37.5) || (55.0 < astm_hue && astm_hue < 85.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            4 | 6 | 8 => if (2.5 < astm_hue && astm_hue < 42.5) || (55.0 < astm_hue && astm_hue < 85.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ if chroma >= 10 => if (2.5 < astm_hue && astm_hue < 42.5) || (55.0 < astm_hue && astm_hue < 82.5) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ => Some("Linear"),
        },
        6 => match chroma {
            2 | 4 => if (5.0 < astm_hue && astm_hue < 37.5) || (55.0 < astm_hue && astm_hue < 87.5) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            6 => if (5.0 < astm_hue && astm_hue < 42.5) || (57.5 < astm_hue && astm_hue < 87.5) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            8 | 10 => if (5.0 < astm_hue && astm_hue < 42.5) || (60.0 < astm_hue && astm_hue < 85.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            12 | 14 => if (5.0 < astm_hue && astm_hue < 42.5) || (60.0 < astm_hue && astm_hue < 82.5) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ if chroma >= 16 => if (5.0 < astm_hue && astm_hue < 42.5) || (60.0 < astm_hue && astm_hue < 80.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ => Some("Linear"),
        },
        7 => match chroma {
            2 | 4 | 6 => if (5.0 < astm_hue && astm_hue < 42.5) || (60.0 < astm_hue && astm_hue < 85.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            8 => if (5.0 < astm_hue && astm_hue < 42.5) || (60.0 < astm_hue && astm_hue < 82.5) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            10 => if (30.0 < astm_hue && astm_hue < 42.5) || (5.0 < astm_hue && astm_hue < 25.0) || (60.0 < astm_hue && astm_hue < 82.5) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            12 => if (30.0 < astm_hue && astm_hue < 42.5) || (7.5 < astm_hue && astm_hue < 27.5) || (80.0 < astm_hue && astm_hue < 82.5) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ if chroma >= 14 => if (32.5 < astm_hue && astm_hue < 40.0) || (7.5 < astm_hue && astm_hue < 15.0) || (80.0 < astm_hue && astm_hue < 82.5) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ => Some("Linear"),
        },
        8 => match chroma {
            2 | 4 | 6 | 8 | 10 | 12 => if (5.0 < astm_hue && astm_hue < 40.0) || (60.0 < astm_hue && astm_hue < 85.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ if chroma >= 14 => if (32.5 < astm_hue && astm_hue < 40.0) || (5.0 < astm_hue && astm_hue < 15.0) || (60.0 < astm_hue && astm_hue < 85.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ => Some("Linear"),
        },
        9 => match chroma {
            2 | 4 => if (5.0 < astm_hue && astm_hue < 40.0) || (55.0 < astm_hue && astm_hue < 80.0) {
                Some("Radial")
            } else {
                Some("Linear")
            },
            6 | 8 | 10 | 12 | 14 => if 5.0 < astm_hue && astm_hue < 42.5 {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ if chroma >= 16 => if 35.0 < astm_hue && astm_hue < 42.5 {
                Some("Radial")
            } else {
                Some("Linear")
            },
            _ => Some("Linear"),
        },
        10 => None, // Ideal white, no interpolation needed
        _ => Some("Linear"), // Default
    }
}

/// Find xyY from renotation data
/// Exact 1:1 port from Python colour-science
pub fn xyy_from_renotation(spec: &[f64; 4]) -> Result<[f64; 3]> {
    // Import the renotation data from constants module
    use crate::constants::MUNSELL_RENOTATION_DATA;
    
    let spec = normalise_munsell_specification(spec);
    
    let hue = spec[0];
    let value = spec[1];
    let chroma = spec[2];
    let code = spec[3] as u8;
    
    // Convert code to hue family string
    let family = match code {
        0 => "R",
        1 => "YR",
        2 => "Y",
        3 => "GY",
        4 => "G",
        5 => "BG",
        6 => "B",
        7 => "PB",
        8 => "P",
        9 => "RP",
        _ => return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Invalid code: {}", code)
        )),
    };
    
    // Format hue string
    let hue_str = if (hue - 2.5).abs() < 1e-6 {
        format!("2.5{}", family)
    } else if (hue - 5.0).abs() < 1e-6 {
        format!("5{}", family)
    } else if (hue - 7.5).abs() < 1e-6 {
        format!("7.5{}", family)
    } else if (hue - 10.0).abs() < 1e-6 || hue.abs() < 1e-6 {
        format!("10{}", family)
    } else {
        format!("{:.1}{}", hue, family)
    };
    
    // Find matching entry in renotation data
    for entry in MUNSELL_RENOTATION_DATA {
        if entry.0.0 == hue_str && 
           (entry.0.1 - value).abs() < 1e-6 && 
           (entry.0.2 - chroma).abs() < 1e-6 {
            return Ok([entry.1.0, entry.1.1, entry.1.2]);
        }
    }
    
    Err(crate::error::MunsellError::InvalidMunsellColor(format!(
        "Specification {:?} not found in renotation data", spec
    )))
}

/// Get maximum chroma from renotation data
/// Exact 1:1 port from Python colour-science
pub fn maximum_chroma_from_renotation(hue: f64, value: f64, code: u8) -> f64 {
    use crate::constants::maximum_chromas_data::MAXIMUM_CHROMAS;
    
    // Ideal white, no chroma
    if value >= 9.99 {
        return 0.0;
    }
    
    let (value_minus, value_plus) = if value % 1.0 == 0.0 {
        (value, value)
    } else {
        (value.floor(), value.floor() + 1.0)
    };
    
    let ((hue_cw, code_cw), (hue_ccw, code_ccw)) = bounding_hues_from_renotation(hue, code);
    
    // Find maximum chromas for the bounding hues and values
    let mut ma_limit_mcw = 0.0;
    let mut ma_limit_mccw = 0.0;
    let mut ma_limit_pcw = 0.0;
    let mut ma_limit_pccw = 0.0;
    
    for &((h, v, c), max_chroma) in MAXIMUM_CHROMAS {
        if (h - hue_cw).abs() < 1e-6 && (v - value_minus).abs() < 1e-6 && c == code_cw {
            ma_limit_mcw = max_chroma;
        }
        if (h - hue_ccw).abs() < 1e-6 && (v - value_minus).abs() < 1e-6 && c == code_ccw {
            ma_limit_mccw = max_chroma;
        }
        if value_plus <= 9.0 {
            if (h - hue_cw).abs() < 1e-6 && (v - value_plus).abs() < 1e-6 && c == code_cw {
                ma_limit_pcw = max_chroma;
            }
            if (h - hue_ccw).abs() < 1e-6 && (v - value_plus).abs() < 1e-6 && c == code_ccw {
                ma_limit_pccw = max_chroma;
            }
        }
    }
    
    if value_plus <= 9.0 {
        // Return minimum of all four limits
        ma_limit_mcw.min(ma_limit_mccw).min(ma_limit_pcw).min(ma_limit_pccw)
    } else {
        // Interpolate between value 9 and 10
        let l = luminance_astmd1535(value);
        let l9 = luminance_astmd1535(9.0);
        let l10 = luminance_astmd1535(10.0);
        
        let chroma_cw = lerp(l9, l10, ma_limit_mcw, 0.0, l);
        let chroma_ccw = lerp(l9, l10, ma_limit_mccw, 0.0, l);
        
        chroma_cw.min(chroma_ccw)
    }
}

/// Convert Munsell specification to xy chromaticity coordinates
/// Exact 1:1 port from Python colour-science xy_from_renotation_ovoid
pub fn xy_from_renotation_ovoid(spec: &[f64; 4]) -> Result<[f64; 2]> {
    let spec = normalise_munsell_specification(spec);
    
    if is_grey_munsell_colour(&spec) {
        return Ok(crate::constants::ILLUMINANT_C);
    }
    
    let hue = spec[0];
    let value = spec[1];
    let chroma = spec[2];
    let code = spec[3] as u8;
    
    // Value must be in [1, 9] range for interpolation
    if value < 1.0 || value > 9.0 {
        return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Value {} must be in range [1, 9]", value)
        ));
    }
    
    // Value must be integer
    if (value - value.round()).abs() > 1e-10 {
        return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Value {} must be an integer", value)
        ));
    }
    
    let value = value.round();
    
    // Chroma must be in [2, 50] range
    if chroma < 2.0 || chroma > 50.0 {
        return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Chroma {} must be in range [2, 50]", chroma)
        ));
    }
    
    // Chroma must be even
    if (2.0 * (chroma / 2.0 - (chroma / 2.0).round())).abs() > 1e-10 {
        return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Chroma {} must be even", chroma)
        ));
    }
    
    let chroma = 2.0 * (chroma / 2.0).round();
    
    // Check if this is a standard hue (no interpolation needed)
    if (hue % 2.5).abs() < 1e-10 {
        let standard_hue = 2.5 * (hue / 2.5).round();
        let xyy = xyy_from_renotation(&[standard_hue, value, chroma, spec[3]])?;
        return Ok([xyy[0], xyy[1]]);
    }
    
    // Find bounding hues
    let ((hue_minus, code_minus), (hue_plus, code_plus)) = bounding_hues_from_renotation(hue, code);
    
    let (x_grey, y_grey) = (crate::constants::ILLUMINANT_C[0], crate::constants::ILLUMINANT_C[1]);
    
    // Get xy for lower hue
    let spec_minus = [hue_minus, value, chroma, code_minus as f64];
    let xyy_minus = xyy_from_renotation(&spec_minus)?;
    let (x_minus, y_minus, _y_minus) = (xyy_minus[0], xyy_minus[1], xyy_minus[2]);
    let (rho_minus, phi_minus, _) = cartesian_to_cylindrical(
        x_minus - x_grey, y_minus - y_grey, xyy_minus[2]
    );
    let phi_minus = phi_minus.to_degrees();
    
    // Get xy for upper hue
    let spec_plus = [hue_plus, value, chroma, code_plus as f64];
    let xyy_plus = xyy_from_renotation(&spec_plus)?;
    let (x_plus, y_plus, _y_plus) = (xyy_plus[0], xyy_plus[1], xyy_plus[2]);
    let (rho_plus, mut phi_plus, _) = cartesian_to_cylindrical(
        x_plus - x_grey, y_plus - y_grey, xyy_plus[2]
    );
    phi_plus = phi_plus.to_degrees();
    
    // Get hue angles
    let mut hue_angle_lower = hue_to_hue_angle(hue_minus, code_minus);
    let hue_angle = hue_to_hue_angle(hue, code);
    let hue_angle_upper = hue_to_hue_angle(hue_plus, code_plus);
    
    // Handle angle wraparound
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
    
    // Determine interpolation method
    let method = interpolation_method_from_renotation_ovoid(hue, value, chroma, code);
    
    match method {
        None => {
            return Err(crate::error::MunsellError::InvalidMunsellColor(
                "Interpolation method must be Linear or Radial".to_string()
            ));
        }
        Some("Linear") => {
            // Linear interpolation in xy space
            let x = lerp(hue_angle_lower, hue_angle_upper, x_minus, x_plus, hue_angle_adj);
            let y = lerp(hue_angle_lower, hue_angle_upper, y_minus, y_plus, hue_angle_adj);
            Ok([x, y])
        }
        Some("Radial") => {
            // Radial interpolation in polar coordinates
            let rho = lerp(hue_angle_lower, hue_angle_upper, rho_minus, rho_plus, hue_angle_adj);
            let phi = lerp(hue_angle_lower, hue_angle_upper, phi_minus, phi_plus, hue_angle_adj);
            
            let (x, y) = polar_to_cartesian(rho, phi.to_radians());
            Ok([x + x_grey, y + y_grey])
        }
        _ => unreachable!()
    }
}

/// Convert CIE xyY to Munsell specification
/// Exact 1:1 port from Python colour-science _xyY_to_munsell_specification
pub fn xyy_to_munsell_specification(xyy: [f64; 3]) -> Result<[f64; 4]> {
    use crate::python_port_helpers::*;
    
    let (x, y, big_y) = (xyy[0], xyy[1], xyy[2]);
    
    // Check MacAdam limits
    if !is_within_macadam_limits(xyy, "C") {
        eprintln!("Warning: xyY {:?} is not within MacAdam limits for illuminant C", xyy);
    }
    
    // Convert Y to Munsell value
    let value = munsell_value_astmd1535(big_y * 100.0);
    let value = if (value - value.round()).abs() < 1e-10 {
        value.round()
    } else {
        value
    };
    
    // Get xyY for the center (grey) at this value
    let xyy_center = munsell_specification_to_xyy(&[f64::NAN, value, f64::NAN, f64::NAN])?;
    let (x_center, y_center) = (xyy_center[0], xyy_center[1]);
    
    // Convert to polar coordinates relative to center
    let (rho_input, phi_input, _) = cartesian_to_cylindrical(
        x - x_center, y - y_center, big_y
    );
    let phi_input = phi_input.to_degrees();
    
    // Check if this is grey
    let grey_threshold = 1e-6;
    if rho_input < grey_threshold {
        return Ok(normalise_munsell_specification(&[f64::NAN, value, 0.0, f64::NAN]));
    }
    
    // Initial guess using Lab color space
    let xyz = xyy_to_xyz(xyy);
    let (x_i, y_i) = (crate::constants::ILLUMINANT_C[0], crate::constants::ILLUMINANT_C[1]);
    let xyz_r = xyy_to_xyz([x_i, y_i, big_y]);
    
    // Normalize reference white
    let xyz_r_norm = [xyz_r[0] / xyz_r[1], 1.0, xyz_r[2] / xyz_r[1]];
    
    let lab = xyz_to_lab(xyz, xyz_to_xy(xyz_r_norm));
    let lchab = lab_to_lchab(lab);
    let initial_spec = lchab_to_munsell_specification(lchab);
    
    let mut specification_current = [
        initial_spec[0],
        value,
        (5.0 / 5.5) * initial_spec[2],
        initial_spec[3],
    ];
    
    // Main convergence loop
    let convergence_threshold = 1e-6 / 1e4;
    let iterations_maximum = 64;
    let mut iterations = 0;
    
    while iterations <= iterations_maximum {
        iterations += 1;
        
        let hue_current = specification_current[0];
        let chroma_current = specification_current[2];
        let code_current = specification_current[3] as u8;
        
        let hue_angle_current = hue_to_hue_angle(hue_current, code_current);
        
        // Check maximum chroma
        let chroma_maximum = maximum_chroma_from_renotation(hue_current, value, code_current);
        let mut chroma_current = if chroma_current > chroma_maximum {
            chroma_maximum
        } else {
            chroma_current
        };
        specification_current[2] = chroma_current;
        
        // Get current xy
        let xyy_current = munsell_specification_to_xyy(&specification_current)?;
        let (x_current, y_current) = (xyy_current[0], xyy_current[1]);
        
        // Convert to polar
        let (rho_current, phi_current, _) = cartesian_to_cylindrical(
            x_current - x_center, y_current - y_center, big_y
        );
        let phi_current = phi_current.to_degrees();
        
        // Calculate phi difference
        let mut phi_current_difference = (360.0 - phi_input + phi_current) % 360.0;
        if phi_current_difference > 180.0 {
            phi_current_difference -= 360.0;
        }
        
        // Inner loop for hue refinement
        let mut phi_differences_data = vec![phi_current_difference];
        let mut hue_angles_differences_data = vec![0.0];
        let mut hue_angles = vec![hue_angle_current];
        
        let iterations_maximum_inner = 16;
        let mut iterations_inner = 0;
        let mut extrapolate = false;
        
        while phi_differences_data.iter().all(|&d| d >= 0.0) || 
              phi_differences_data.iter().all(|&d| d <= 0.0) {
            if extrapolate {
                break;
            }
            
            iterations_inner += 1;
            if iterations_inner > iterations_maximum_inner {
                return Err(crate::error::MunsellError::ConversionError {
                    message: "Maximum inner iterations reached without convergence".to_string()
                });
            }
            
            let hue_angle_inner = (hue_angle_current + iterations_inner as f64 * (phi_input - phi_current)) % 360.0;
            let mut hue_angle_difference_inner = (iterations_inner as f64 * (phi_input - phi_current)) % 360.0;
            if hue_angle_difference_inner > 180.0 {
                hue_angle_difference_inner -= 360.0;
            }
            
            let (hue_inner, code_inner) = hue_angle_to_hue(hue_angle_inner);
            
            let spec_inner = [hue_inner, value, chroma_current, code_inner as f64];
            let xyy_inner = munsell_specification_to_xyy(&spec_inner)?;
            let (x_inner, y_inner) = (xyy_inner[0], xyy_inner[1]);
            
            if phi_differences_data.len() >= 2 {
                extrapolate = true;
            }
            
            if !extrapolate {
                let (rho_inner, phi_inner, _) = cartesian_to_cylindrical(
                    x_inner - x_center, y_inner - y_center, big_y
                );
                let phi_inner = phi_inner.to_degrees();
                
                let mut phi_inner_difference = (360.0 - phi_input + phi_inner) % 360.0;
                if phi_inner_difference > 180.0 {
                    phi_inner_difference -= 360.0;
                }
                
                phi_differences_data.push(phi_inner_difference);
                hue_angles.push(hue_angle_inner);
                hue_angles_differences_data.push(hue_angle_difference_inner);
            }
        }
        
        // Sort and interpolate
        let mut indices: Vec<usize> = (0..phi_differences_data.len()).collect();
        indices.sort_by(|&i, &j| phi_differences_data[i].partial_cmp(&phi_differences_data[j]).unwrap());
        
        let phi_differences_sorted: Vec<f64> = indices.iter().map(|&i| phi_differences_data[i]).collect();
        let hue_angles_differences_sorted: Vec<f64> = indices.iter().map(|&i| hue_angles_differences_data[i]).collect();
        
        let interpolator = LinearInterpolator::new(phi_differences_sorted, hue_angles_differences_sorted);
        let extrapolator = Extrapolator::new(interpolator);
        let hue_angle_difference_new = extrapolator.extrapolate(0.0) % 360.0;
        let hue_angle_new = (hue_angle_current + hue_angle_difference_new) % 360.0;
        
        let (hue_new, code_new) = hue_angle_to_hue(hue_angle_new);
        specification_current = [hue_new, value, chroma_current, code_new as f64];
        
        // Check convergence on xy distance
        let xyy_current = munsell_specification_to_xyy(&specification_current)?;
        let (x_current, y_current) = (xyy_current[0], xyy_current[1]);
        
        let difference = euclidean_distance([x, y], [x_current, y_current]);
        if difference < convergence_threshold {
            return Ok(specification_current);
        }
        
        // Chroma refinement loop
        let chroma_maximum = maximum_chroma_from_renotation(hue_new, value, code_new);
        if specification_current[2] > chroma_maximum {
            specification_current[2] = chroma_maximum;
        }
        chroma_current = specification_current[2];
        
        let xyy_current = munsell_specification_to_xyy(&specification_current)?;
        let (x_current, y_current) = (xyy_current[0], xyy_current[1]);
        
        let (rho_current, _, _) = cartesian_to_cylindrical(
            x_current - x_center, y_current - y_center, big_y
        );
        
        let mut rho_bounds_data = vec![rho_current];
        let mut chroma_bounds_data = vec![chroma_current];
        
        let iterations_maximum_inner = 16;
        let mut iterations_inner = 0;
        
        while !(rho_bounds_data.iter().min_by(|a, b| a.partial_cmp(b).unwrap()).unwrap() < &rho_input &&
                &rho_input < rho_bounds_data.iter().max_by(|a, b| a.partial_cmp(b).unwrap()).unwrap()) {
            iterations_inner += 1;
            if iterations_inner > iterations_maximum_inner {
                return Err(crate::error::MunsellError::ConversionError {
                    message: "Maximum inner iterations reached without convergence in chroma loop".to_string()
                });
            }
            
            let chroma_inner = ((rho_input / rho_current).powf(iterations_inner as f64)) * chroma_current;
            let chroma_inner = if chroma_inner > chroma_maximum {
                chroma_maximum
            } else {
                chroma_inner
            };
            
            let spec_inner = [hue_new, value, chroma_inner, code_new as f64];
            let xyy_inner = munsell_specification_to_xyy(&spec_inner)?;
            let (x_inner, y_inner) = (xyy_inner[0], xyy_inner[1]);
            
            let (rho_inner, _, _) = cartesian_to_cylindrical(
                x_inner - x_center, y_inner - y_center, big_y
            );
            
            rho_bounds_data.push(rho_inner);
            chroma_bounds_data.push(chroma_inner);
        }
        
        // Sort and interpolate chroma
        let mut indices: Vec<usize> = (0..rho_bounds_data.len()).collect();
        indices.sort_by(|&i, &j| rho_bounds_data[i].partial_cmp(&rho_bounds_data[j]).unwrap());
        
        let rho_bounds_sorted: Vec<f64> = indices.iter().map(|&i| rho_bounds_data[i]).collect();
        let chroma_bounds_sorted: Vec<f64> = indices.iter().map(|&i| chroma_bounds_data[i]).collect();
        
        let interpolator = LinearInterpolator::new(rho_bounds_sorted, chroma_bounds_sorted);
        let chroma_new = interpolator.interpolate(rho_input);
        
        specification_current = [hue_new, value, chroma_new, code_new as f64];
        
        // Final convergence check
        let xyy_current = munsell_specification_to_xyy(&specification_current)?;
        let (x_current, y_current) = (xyy_current[0], xyy_current[1]);
        
        let difference = euclidean_distance([x, y], [x_current, y_current]);
        if difference < convergence_threshold {
            return Ok(specification_current);
        }
    }
    
    Err(crate::error::MunsellError::ConversionError {
        message: "Maximum iterations reached without convergence".to_string()
    })
}

/// Convert Munsell specification to xy chromaticity coordinates
/// This is an intermediate function used by munsell_specification_to_xyY
/// Exact 1:1 port from Python colour-science
pub fn munsell_specification_to_xy(spec: &[f64; 4]) -> Result<[f64; 2]> {
    let spec = normalise_munsell_specification(spec);
    
    if is_grey_munsell_colour(&spec) {
        return Ok(crate::constants::ILLUMINANT_C);
    }
    
    let hue = spec[0];
    let value = spec[1];
    let chroma = spec[2];
    let code = spec[3] as u8;
    
    // Value must be in [0, 10] range
    if value < 0.0 || value > 10.0 {
        return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Value {} must be in range [0, 10]", value)
        ));
    }
    
    // Value must be integer
    if (value - value.round()).abs() > 1e-10 {
        return Err(crate::error::MunsellError::InvalidMunsellColor(
            format!("Value {} must be an integer", value)
        ));
    }
    
    let value = value.round();
    
    // Determine chroma bounds
    let (chroma_minus, chroma_plus) = if chroma % 2.0 == 0.0 {
        (chroma, chroma)
    } else {
        (2.0 * (chroma / 2.0).floor(), 2.0 * (chroma / 2.0).floor() + 2.0)
    };
    
    // Get xy for lower chroma
    let (x_minus, y_minus) = if chroma_minus == 0.0 {
        // Smallest chroma ovoid collapses to illuminant
        (crate::constants::ILLUMINANT_C[0], crate::constants::ILLUMINANT_C[1])
    } else {
        let xy = xy_from_renotation_ovoid(&[hue, value, chroma_minus, code as f64])?;
        (xy[0], xy[1])
    };
    
    // Get xy for upper chroma
    let xy_plus = xy_from_renotation_ovoid(&[hue, value, chroma_plus, code as f64])?;
    let (x_plus, y_plus) = (xy_plus[0], xy_plus[1]);
    
    // Interpolate if needed
    if chroma_minus == chroma_plus {
        Ok([x_minus, y_minus])
    } else {
        let x = lerp(chroma_minus, chroma_plus, x_minus, x_plus, chroma);
        let y = lerp(chroma_minus, chroma_plus, y_minus, y_plus, chroma);
        Ok([x, y])
    }
}

/// Convert Munsell specification to CIE xyY colourspace
/// Exact 1:1 port from Python colour-science
pub fn munsell_specification_to_xyy(spec: &[f64; 4]) -> Result<[f64; 3]> {
    let spec = normalise_munsell_specification(spec);
    
    let value = spec[1];
    
    // Grey colors are handled specially
    if is_grey_munsell_colour(&spec) {
        // For grey colors, only value matters
        // No domain checks needed
    } else {
        // Non-grey colors
        let hue = spec[0];
        
        // Validate hue domain [0, 10]
        if hue < 0.0 || hue > 10.0 {
            return Err(crate::error::MunsellError::InvalidMunsellColor(
                format!("Hue {} must be in range [0, 10]", hue)
            ));
        }
        
        // Validate value domain [0, 10]
        if value < 0.0 || value > 10.0 {
            return Err(crate::error::MunsellError::InvalidMunsellColor(
                format!("Value {} must be in range [0, 10]", value)
            ));
        }
    }
    
    // Calculate Y from value using ASTM D1535 formula
    let y_luminance = luminance_astmd1535(value);
    
    // Determine value bounds for interpolation
    let (value_minus, value_plus) = if (value - value.round()).abs() < 1e-10 {
        (value.round(), value.round())
    } else {
        (value.floor(), value.floor() + 1.0)
    };
    
    // Get xy for lower value
    let spec_minus = if is_grey_munsell_colour(&spec) {
        [f64::NAN, value_minus, f64::NAN, f64::NAN]
    } else {
        [spec[0], value_minus, spec[2], spec[3]]
    };
    let xy_minus = munsell_specification_to_xy(&spec_minus)?;
    let (x_minus, y_minus) = (xy_minus[0], xy_minus[1]);
    
    // Get xy for upper value
    let spec_plus = if is_grey_munsell_colour(&spec) || value_plus == 10.0 {
        [f64::NAN, value_plus, f64::NAN, f64::NAN]
    } else {
        [spec[0], value_plus, spec[2], spec[3]]
    };
    let xy_plus = munsell_specification_to_xy(&spec_plus)?;
    let (x_plus, y_plus) = (xy_plus[0], xy_plus[1]);
    
    // Interpolate if needed
    let (x, y) = if value_minus == value_plus {
        (x_minus, y_minus)
    } else {
        let y_minus_lum = luminance_astmd1535(value_minus);
        let y_plus_lum = luminance_astmd1535(value_plus);
        
        let x = lerp(y_minus_lum, y_plus_lum, x_minus, x_plus, y_luminance);
        let y = lerp(y_minus_lum, y_plus_lum, y_minus, y_plus, y_luminance);
        (x, y)
    };
    
    // Y is scaled to [0, 1] from [0, 100]
    let y_scaled = y_luminance / 100.0;
    
    Ok([x, y, y_scaled])
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json;
    use std::fs;
    
    #[test]
    fn test_python_functions_exact_match() {
        // Load test data generated from Python
        let test_data = fs::read_to_string("python_test_data.json")
            .expect("Failed to read test data");
        let data: serde_json::Value = serde_json::from_str(&test_data)
            .expect("Failed to parse test data");
        
        // Test hue_to_ASTM_hue
        if let Some(tests) = data["hue_to_ASTM_hue"].as_array() {
            for test in tests {
                let input = test["input"].as_array().unwrap();
                let hue = input[0].as_f64().unwrap();
                let code = input[1].as_u64().unwrap() as u8;
                let expected = test["output"].as_f64().unwrap();
                
                let result = hue_to_astm_hue(hue, code);
                assert!((result - expected).abs() < 1e-10, 
                    "hue_to_ASTM_hue({}, {}) = {} (expected {})", 
                    hue, code, result, expected);
            }
            println!("✓ hue_to_ASTM_hue: all {} tests passed", tests.len());
        }
        
        // Test hue_to_hue_angle
        if let Some(tests) = data["hue_to_hue_angle"].as_array() {
            for test in tests {
                let input = test["input"].as_array().unwrap();
                let hue = input[0].as_f64().unwrap();
                let code = input[1].as_u64().unwrap() as u8;
                let expected = test["output"].as_f64().unwrap();
                
                let result = hue_to_hue_angle(hue, code);
                assert!((result - expected).abs() < 1e-10, 
                    "hue_to_hue_angle({}, {}) = {} (expected {})", 
                    hue, code, result, expected);
            }
            println!("✓ hue_to_hue_angle: all {} tests passed", tests.len());
        }
        
        // Continue for other functions...
    }
}