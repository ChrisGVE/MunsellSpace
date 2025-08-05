//! 1:1 Port of Python colour-science Munsell conversion implementation
//! 
//! This module is a direct port of the Python colour-science library's
//! _xyY_to_munsell_specification function to ensure exact matching behavior.

use crate::constants::*;
use crate::error::{MunsellError, Result};
use std::f64::consts::PI;

// Critical constants from Python colour-science
const THRESHOLD_INTEGER: f64 = 1e-3;  // Grey/achromatic detection threshold
const TOLERANCE_ABSOLUTE_DEFAULT: f64 = 1e-8;
const MAX_OUTER_ITERATIONS: usize = 64;
const MAX_INNER_ITERATIONS: usize = 16;

// Illuminant C chromaticity coordinates
const ILLUMINANT_C_X: f64 = 0.31006;
const ILLUMINANT_C_Y: f64 = 0.31616;

/// Mathematical Munsell specification representation
#[derive(Debug, Clone, PartialEq)]
pub struct MunsellSpecification {
    pub hue: f64,           // 0.0-10.0
    pub value: f64,         // 0.0-10.0 (lightness)
    pub chroma: f64,        // 0.0+ (saturation)
    pub code: u8,           // Hue family code (1-10)
}

/// CIE xyY color space representation
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct CieXyY {
    pub x: f64,            // Chromaticity x
    pub y: f64,            // Chromaticity y  
    pub Y: f64,            // Luminance Y
}

/// CIE XYZ color space representation
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct CieXYZ {
    pub X: f64,
    pub Y: f64,
    pub Z: f64,
}

/// CIE Lab color space representation
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct CieLab {
    pub L: f64,  // Lightness
    pub a: f64,  // Green-Red axis
    pub b: f64,  // Blue-Yellow axis
}

/// CIE LCHab color space representation
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct CieLCHab {
    pub L: f64,  // Lightness
    pub C: f64,  // Chroma
    pub h: f64,  // Hue angle in degrees
}

/// Convert xyY to XYZ
fn xyY_to_XYZ(xyy: CieXyY) -> CieXYZ {
    if xyy.y.abs() < 1e-15 {
        // Handle edge case where y = 0
        CieXYZ { X: 0.0, Y: xyy.Y, Z: 0.0 }
    } else {
        let X = xyy.x * xyy.Y / xyy.y;
        let Z = (1.0 - xyy.x - xyy.y) * xyy.Y / xyy.y;
        CieXYZ { X, Y: xyy.Y, Z }
    }
}

/// Convert XYZ to xyY
fn XYZ_to_xyY(xyz: CieXYZ) -> CieXyY {
    let sum = xyz.X + xyz.Y + xyz.Z;
    if sum < 1e-15 {
        // Handle black/near-black colors
        CieXyY { x: 0.0, y: 0.0, Y: xyz.Y }
    } else {
        CieXyY {
            x: xyz.X / sum,
            y: xyz.Y / sum,
            Y: xyz.Y,
        }
    }
}

/// Convert XYZ to Lab
/// Uses Illuminant C as reference white for Munsell
fn XYZ_to_Lab(xyz: CieXYZ) -> CieLab {
    // Illuminant C white point in XYZ
    let x_n = ILLUMINANT_C_X;
    let y_n = ILLUMINANT_C_Y;
    let Y_n = 1.0;  // Normalized
    
    // Convert to XYZ for Illuminant C
    let X_n = x_n * Y_n / y_n;
    let Z_n = (1.0 - x_n - y_n) * Y_n / y_n;
    
    // Normalize
    let x_r = xyz.X / X_n;
    let y_r = xyz.Y / Y_n;
    let z_r = xyz.Z / Z_n;
    
    // Apply the f function
    let f = |t: f64| -> f64 {
        if t > (24.0 / 116.0).powi(3) {
            t.powf(1.0 / 3.0)
        } else {
            (841.0 / 108.0) * t + 16.0 / 116.0
        }
    };
    
    let f_x = f(x_r);
    let f_y = f(y_r);
    let f_z = f(z_r);
    
    CieLab {
        L: 116.0 * f_y - 16.0,
        a: 500.0 * (f_x - f_y),
        b: 200.0 * (f_y - f_z),
    }
}

/// Convert Lab to LCHab
fn Lab_to_LCHab(lab: CieLab) -> CieLCHab {
    let C = (lab.a * lab.a + lab.b * lab.b).sqrt();
    let h_rad = lab.b.atan2(lab.a);
    let h_deg = h_rad * 180.0 / PI;
    
    // Normalize to [0, 360)
    let h = if h_deg < 0.0 { h_deg + 360.0 } else { h_deg };
    
    CieLCHab {
        L: lab.L,
        C,
        h,
    }
}

/// Convert LCHab to approximate Munsell specification
/// Direct port from Python colour-science
fn LCHab_to_munsell_specification(lch: CieLCHab) -> (f64, f64, f64, u8) {
    let hab = lch.h;
    
    // Determine code based on LCH hue angle
    let code = if hab == 0.0 {
        8  // RP
    } else if hab <= 36.0 {
        7  // R
    } else if hab <= 72.0 {
        6  // YR
    } else if hab <= 108.0 {
        5  // Y
    } else if hab <= 144.0 {
        4  // GY
    } else if hab <= 180.0 {
        3  // G
    } else if hab <= 216.0 {
        2  // BG
    } else if hab <= 252.0 {
        1  // B
    } else if hab <= 288.0 {
        10 // PB
    } else if hab <= 324.0 {
        9  // P
    } else {
        8  // RP
    };
    
    // Linear interpolation for hue: maps [0, 36] to [0, 10]
    let hab_mod = hab % 36.0;
    let mut hue = (hab_mod / 36.0) * 10.0;
    if hue == 0.0 {
        hue = 10.0;
    }
    
    // Direct conversions from Python
    let value = lch.L / 10.0;
    let chroma = lch.C / 5.0;
    
    (hue, value, chroma, code)
}

/// Convert hue angle (0-360°) to Munsell hue and family code
/// Direct port from Python colour-science
fn hue_angle_to_hue(hue_angle: f64) -> (f64, u8) {
    // Python's LinearInterpolator with exact table from colour-science
    let x_points = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0];
    let y_points = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0];
    
    // Linear interpolation
    let single_hue = linear_interpolate(&x_points, &y_points, hue_angle);
    
    // Determine code based on single_hue ranges
    let code = if single_hue <= 0.5 {
        7  // R
    } else if single_hue <= 1.5 {
        6  // YR
    } else if single_hue <= 2.5 {
        5  // Y
    } else if single_hue <= 3.5 {
        4  // GY
    } else if single_hue <= 4.5 {
        3  // G
    } else if single_hue <= 5.5 {
        2  // BG
    } else if single_hue <= 6.5 {
        1  // B
    } else if single_hue <= 7.5 {
        10 // PB
    } else if single_hue <= 8.5 {
        9  // P
    } else if single_hue <= 9.5 {
        8  // RP
    } else {
        7  // R (wraps around)
    };
    
    // Calculate hue from single_hue
    let mut hue = (10.0 * (single_hue % 1.0) + 5.0) % 10.0;
    if hue == 0.0 {
        hue = 10.0;
    }
    
    (hue, code)
}

/// Linear interpolation helper
fn linear_interpolate(x_points: &[f64], y_points: &[f64], x: f64) -> f64 {
    // Handle edge cases
    if x <= x_points[0] {
        return y_points[0];
    }
    if x >= x_points[x_points.len() - 1] {
        return y_points[y_points.len() - 1];
    }
    
    // Find the right interval
    for i in 0..x_points.len() - 1 {
        if x >= x_points[i] && x <= x_points[i + 1] {
            let t = (x - x_points[i]) / (x_points[i + 1] - x_points[i]);
            return y_points[i] + t * (y_points[i + 1] - y_points[i]);
        }
    }
    
    // Should not reach here
    y_points[y_points.len() - 1]
}

/// Convert Munsell hue and code to hue angle
/// Direct port from Python colour-science
fn hue_to_hue_angle(hue: f64, code: u8) -> f64 {
    // Calculate single_hue using Python's exact formula
    let single_hue = ((17.0 - code as f64) % 10.0 + (hue / 10.0) - 0.5) % 10.0;
    
    // Python's LinearInterpolator with exact table
    let x_points = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0];
    let y_points = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0];
    
    linear_interpolate(&x_points, &y_points, single_hue)
}

/// Cartesian to cylindrical coordinate conversion
fn cartesian_to_cylindrical(x: f64, y: f64, z: f64) -> (f64, f64, f64) {
    let rho = (x * x + y * y).sqrt();
    let phi = y.atan2(x);  // Returns [-π, π]
    (rho, phi, z)
}

/// Main xyY to Munsell specification conversion
/// Direct port of Python's _xyY_to_munsell_specification
pub fn xyY_to_munsell_specification(xyy: CieXyY) -> Result<MunsellSpecification> {
    // Line 29: Y = to_domain_1(Y) - Python normalizes Y to [0,1]
    let Y = xyy.Y;  // Assuming Y is already in [0,1]
    
    // Line 38: Calculate Munsell value using ASTM D1535 polynomial
    let value = munsell_value_ASTMD1535(Y * 100.0);
    
    // Line 40-41: Round if integer
    let value = if (value - value.round()).abs() < 1e-10 {
        value.round()
    } else {
        value
    };
    
    // Line 44: Get xyY for the achromatic color at this value
    let (x_center, y_center) = (ILLUMINANT_C_X, ILLUMINANT_C_Y);
    let Y_center = Y;  // Use same Y as input
    
    // Line 46-48: Convert to cylindrical coordinates relative to achromatic center
    let (rho_input, phi_input_rad, _) = cartesian_to_cylindrical(
        xyy.x - x_center,
        xyy.y - y_center,
        Y_center
    );
    let phi_input = phi_input_rad * 180.0 / PI;  // Convert to degrees
    
    // Line 51-53: Check if color is grey/achromatic
    if rho_input < THRESHOLD_INTEGER {
        // Return achromatic specification
        return Ok(MunsellSpecification {
            hue: 0.0,
            value,
            chroma: 0.0,
            code: 0,  // N for neutral
        });
    }
    
    // Line 55-74: Initial guess using Lab/LCH conversion
    let xyz = xyY_to_XYZ(xyy);
    let lab = XYZ_to_Lab(xyz);
    let lch = Lab_to_LCHab(lab);
    
    // Get initial Munsell specification from LCH
    let (hue_initial, _, chroma_initial, code_initial) = LCHab_to_munsell_specification(lch);
    
    // Line 69-74: Set up initial specification with scaled chroma
    let mut specification_current = [
        hue_initial,
        value,
        (5.0 / 5.5) * chroma_initial,  // Scale factor from Python
        code_initial as f64,
    ];
    
    // Line 76: Convergence threshold
    let convergence_threshold = THRESHOLD_INTEGER / 1e4;  // 1e-7
    
    // Line 77-78: Start outer iteration loop
    let mut iterations = 0;
    
    // Main outer loop (lines 80-301)
    while iterations <= MAX_OUTER_ITERATIONS {
        iterations += 1;
        
        // Extract current specification
        let hue_current = specification_current[0];
        let _value_current = specification_current[1];
        let mut chroma_current = specification_current[2];
        let code_current = specification_current[3] as u8;
        
        // Line 89: Get current hue angle
        let hue_angle_current = hue_to_hue_angle(hue_current, code_current);
        
        // Line 91-95: Check maximum chroma
        // TODO: Implement maximum_chroma_from_renotation
        // For now, use a placeholder max chroma
        let chroma_maximum = 50.0;  // Placeholder
        if chroma_current > chroma_maximum {
            chroma_current = chroma_maximum;
            specification_current[2] = chroma_maximum;
        }
        
        // Line 98-100: Convert current specification to xyY
        // TODO: Implement munsell_specification_to_xyY
        // For now, use placeholder
        let (x_current, y_current) = (0.3, 0.3);  // Placeholder
        
        // Line 102-110: Calculate phi difference
        let (rho_current, phi_current_rad, _) = cartesian_to_cylindrical(
            x_current - x_center,
            y_current - y_center,
            Y_center
        );
        let phi_current = phi_current_rad * 180.0 / PI;
        let mut phi_current_difference = (360.0 - phi_input + phi_current) % 360.0;
        if phi_current_difference > 180.0 {
            phi_current_difference -= 360.0;
        }
        
        // Line 112-114: Initialize data arrays
        let mut phi_differences_data = vec![phi_current_difference];
        let mut hue_angles_differences_data = vec![0.0];
        let mut hue_angles = vec![hue_angle_current];
        
        // Line 116-118: Inner hue loop setup
        let mut iterations_inner = 0;
        let mut extrapolate = false;
        
        // Line 120-172: Inner hue loop
        while phi_differences_data.iter().all(|&d| d >= 0.0) || 
              phi_differences_data.iter().all(|&d| d <= 0.0) {
            if extrapolate {
                break;
            }
            
            iterations_inner += 1;
            
            if iterations_inner > MAX_INNER_ITERATIONS {
                return Err(MunsellError::ConvergenceFailed);
            }
            
            // Line 136-144: Calculate inner hue angle
            let hue_angle_inner = (hue_angle_current + iterations_inner as f64 * (phi_input - phi_current)) % 360.0;
            let mut hue_angle_difference_inner = (iterations_inner as f64 * (phi_input - phi_current)) % 360.0;
            if hue_angle_difference_inner > 180.0 {
                hue_angle_difference_inner -= 360.0;
            }
            
            // Line 145: Convert angle to hue
            let (hue_inner, code_inner) = hue_angle_to_hue(hue_angle_inner);
            
            // Line 157-158: Check if we should extrapolate
            if phi_differences_data.len() >= 2 {
                extrapolate = true;
            }
            
            if !extrapolate {
                // Line 147-155: Get xy for inner specification
                // TODO: Implement conversion
                let (x_inner, y_inner) = (0.3, 0.3);  // Placeholder
                
                // Line 161-167: Calculate inner phi
                let (rho_inner, phi_inner_rad, _) = cartesian_to_cylindrical(
                    x_inner - x_center,
                    y_inner - y_center,
                    Y_center
                );
                let phi_inner = phi_inner_rad * 180.0 / PI;
                let mut phi_inner_difference = (360.0 - phi_input + phi_inner) % 360.0;
                if phi_inner_difference > 180.0 {
                    phi_inner_difference -= 360.0;
                }
                
                // Line 169-171: Append to data arrays
                phi_differences_data.push(phi_inner_difference);
                hue_angles.push(hue_angle_inner);
                hue_angles_differences_data.push(hue_angle_difference_inner);
            }
        }
        
        // Line 173-180: Sort and interpolate
        // TODO: Implement proper sorting and interpolation
        let hue_angle_difference_new = 0.0;  // Placeholder for interpolation at 0
        
        // Line 185-190: Update specification
        let hue_angle_new = (hue_angle_current + hue_angle_difference_new) % 360.0;
        let (hue_new, code_new) = hue_angle_to_hue(hue_angle_new);
        specification_current = [hue_new, value, chroma_current, code_new as f64];
        
        // Line 192-204: Check convergence
        // TODO: Get actual x_current, y_current from specification
        let distance = ((xyy.x - x_current).powi(2) + (xyy.y - y_current).powi(2)).sqrt();
        if distance < convergence_threshold {
            return Ok(MunsellSpecification {
                hue: specification_current[0],
                value: specification_current[1],
                chroma: specification_current[2],
                code: specification_current[3] as u8,
            });
        }
        
        // Line 206-282: Inner chroma loop
        // TODO: Implement inner chroma loop
        
        // Line 283-294: Final convergence check
        // TODO: Implement final convergence check
    }
    
    // Line 299-301: Max iterations exceeded
    Err(MunsellError::ConvergenceFailed)
}

/// Calculate Munsell value from Y using ASTM D1535 polynomial
fn munsell_value_ASTMD1535(Y: f64) -> f64 {
    // Python expects Y in [0, 100] range
    let y = Y / 100.0;
    
    // ASTM D1535 polynomial coefficients
    let a = 1.1914;
    let b = -0.22533;
    let c = 0.23352;
    let d = -0.020484;
    let e = 0.00081939;
    
    // Calculate polynomial
    let value = 10.0 * (a * y + b * y.powi(2) + c * y.powi(3) + d * y.powi(4) + e * y.powi(5)).sqrt();
    
    value
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_xyy_to_xyz_conversion() {
        let xyy = CieXyY { x: 0.3127, y: 0.3290, Y: 0.5 };
        let xyz = xyY_to_XYZ(xyy);
        
        assert!((xyz.X - 0.4751).abs() < 1e-4);
        assert!((xyz.Y - 0.5).abs() < 1e-10);
        assert!((xyz.Z - 0.5166).abs() < 1e-4);
    }
    
    #[test]
    fn test_lab_conversion() {
        let xyz = CieXYZ { X: 0.4751, Y: 0.5, Z: 0.5166 };
        let lab = XYZ_to_Lab(xyz);
        
        // Values will depend on the illuminant
        assert!(lab.L > 0.0);
    }
}