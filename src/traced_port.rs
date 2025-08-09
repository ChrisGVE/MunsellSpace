//! Traced version of Python port functions for debugging
//! Contains instrumented versions of key functions to generate trace logs

use crate::error::Result;
use crate::python_port::{cartesian_to_cylindrical, normalise_munsell_specification};
use crate::python_port_helpers::{xyy_to_xyz, xyz_to_xy, xyz_to_lab, lab_to_lchab, is_within_macadam_limits};
use std::sync::Mutex;
use lazy_static::lazy_static;

lazy_static! {
    /// Global trace log storage
    pub static ref TRACE_LOG: Mutex<Vec<String>> = Mutex::new(Vec::new());
}

/// Clear the trace log
pub fn clear_trace() {
    TRACE_LOG.lock().unwrap().clear();
}

/// Get a copy of the current trace log
pub fn get_trace() -> Vec<String> {
    TRACE_LOG.lock().unwrap().clone()
}

/// Save trace to file
pub fn save_trace_to_file(filename: &str) -> std::io::Result<()> {
    use std::io::Write;
    let trace = get_trace();
    let mut file = std::fs::File::create(filename)?;
    for line in trace {
        writeln!(file, "{}", line)?;
    }
    Ok(())
}

/// Macro for consistent trace formatting
macro_rules! trace {
    ($func_name:expr, $line_no:expr, $vars:expr, $action:expr, $details:expr) => {
        {
            let msg = format!("{}:{} | vars: {} | action: {} {}", 
                            $func_name, $line_no, $vars, $action, $details);
            TRACE_LOG.lock().unwrap().push(msg);
        }
    };
    ($func_name:expr, $line_no:expr, $vars:expr, $action:expr) => {
        {
            let msg = format!("{}:{} | vars: {} | action: {}", 
                            $func_name, $line_no, $vars, $action);
            TRACE_LOG.lock().unwrap().push(msg);
        }
    };
}

/// Helper function to format variables
fn format_vars(vars: &[(&str, String)]) -> String {
    vars.iter()
        .map(|(name, value)| format!("{}={}", name, value))
        .collect::<Vec<_>>()
        .join(", ")
}

/// Helper function to format f64 values consistently
fn fmt_f64(val: f64) -> String {
    if val.is_nan() {
        "nan".to_string()
    } else if val.is_infinite() {
        if val.is_sign_positive() {
            "inf".to_string()
        } else {
            "-inf".to_string()
        }
    } else {
        format!("{:.10}", val)
    }
}

/// Helper function to format f64 array
fn fmt_f64_array(arr: &[f64]) -> String {
    let formatted: Vec<String> = arr.iter().map(|&x| fmt_f64(x)).collect();
    format!("[{}]", formatted.join(", "))
}

/// Traced version of hue_to_hue_angle
pub fn hue_to_hue_angle(hue: f64, code: u8) -> f64 {
    let func_name = "hue_to_hue_angle";
    
    trace!(func_name, 1, format_vars(&[("hue", fmt_f64(hue)), ("code", code.to_string())]), "ENTER", "");
    
    // Line 47: First calculate single_hue using the complex formula
    let raw = (17.0 - code as f64) % 10.0 + (hue / 10.0) - 0.5;
    trace!(func_name, 2, format_vars(&[("raw", fmt_f64(raw))]), "CALC", "raw = (17 - code) % 10 + (hue / 10) - 0.5");
    
    let single_hue = if raw < 0.0 {
        trace!(func_name, 3, format_vars(&[("raw", fmt_f64(raw))]), "BRANCH", "raw < 0.0: true");
        let result = (raw % 10.0) + 10.0;
        trace!(func_name, 4, format_vars(&[("result", fmt_f64(result))]), "CALC", "(raw % 10) + 10");
        result
    } else {
        trace!(func_name, 5, format_vars(&[("raw", fmt_f64(raw))]), "BRANCH", "raw < 0.0: false");
        let result = raw % 10.0;
        trace!(func_name, 6, format_vars(&[("result", fmt_f64(result))]), "CALC", "raw % 10");
        result
    };
    trace!(func_name, 7, format_vars(&[("single_hue", fmt_f64(single_hue))]), "CALC", "single_hue calculated");
    
    // Line 55: Then interpolate using breakpoints
    let breakpoints = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0];
    let angles = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0];
    
    // Line 58: Find the two bounding points
    for i in 0..breakpoints.len()-1 {
        trace!(func_name, 8, format_vars(&[("i", i.to_string()), ("single_hue", fmt_f64(single_hue)), ("breakpoint_i", fmt_f64(breakpoints[i])), ("breakpoint_i1", fmt_f64(breakpoints[i+1]))]), "LOOP", format!("iteration {}", i));
        
        if single_hue >= breakpoints[i] && single_hue <= breakpoints[i+1] {
            trace!(func_name, 9, format_vars(&[("condition", "true".to_string())]), "BRANCH", "found bounding points");
            
            let t = (single_hue - breakpoints[i]) / (breakpoints[i+1] - breakpoints[i]);
            trace!(func_name, 10, format_vars(&[("t", fmt_f64(t))]), "CALC", "interpolation parameter t");
            
            let result = angles[i] + t * (angles[i+1] - angles[i]);
            trace!(func_name, 11, format_vars(&[("result", fmt_f64(result))]), "RETURN", "interpolated angle");
            return result;
        }
    }
    
    // Default case (should not happen)
    trace!(func_name, 12, format_vars(&[]), "RETURN", "default case: 360.0");
    360.0
}

/// Traced version of hue_angle_to_hue
pub fn hue_angle_to_hue(hue_angle: f64) -> (f64, u8) {
    let func_name = "hue_angle_to_hue";
    
    trace!(func_name, 1, format_vars(&[("hue_angle", fmt_f64(hue_angle))]), "ENTER", "");
    
    // Line 73-75: LinearInterpolator arrays
    let angles = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0];
    let values = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0];
    
    // Line 77: Linear interpolation to get single_hue
    let mut single_hue = 0.0;
    for i in 0..angles.len()-1 {
        trace!(func_name, 2, format_vars(&[("i", i.to_string()), ("hue_angle", fmt_f64(hue_angle)), ("angle_i", fmt_f64(angles[i])), ("angle_i1", fmt_f64(angles[i+1]))]), "LOOP", format!("iteration {}", i));
        
        if hue_angle >= angles[i] && hue_angle <= angles[i+1] {
            trace!(func_name, 3, format_vars(&[("condition", "true".to_string())]), "BRANCH", "found interpolation range");
            
            let t = (hue_angle - angles[i]) / (angles[i+1] - angles[i]);
            single_hue = values[i] + t * (values[i+1] - values[i]);
            trace!(func_name, 4, format_vars(&[("t", fmt_f64(t)), ("single_hue", fmt_f64(single_hue))]), "CALC", "interpolated single_hue");
            break;
        }
    }
    
    // Line 87: Determine code based on single_hue value
    let code = if single_hue <= 0.5 {
        trace!(func_name, 5, format_vars(&[("single_hue", fmt_f64(single_hue))]), "BRANCH", "single_hue <= 0.5: R");
        7  // R
    } else if single_hue <= 1.5 {
        trace!(func_name, 6, format_vars(&[("single_hue", fmt_f64(single_hue))]), "BRANCH", "single_hue <= 1.5: YR");
        6  // YR
    } else if single_hue <= 2.5 {
        trace!(func_name, 7, format_vars(&[("single_hue", fmt_f64(single_hue))]), "BRANCH", "single_hue <= 2.5: Y");
        5  // Y
    } else if single_hue <= 3.5 {
        trace!(func_name, 8, format_vars(&[("single_hue", fmt_f64(single_hue))]), "BRANCH", "single_hue <= 3.5: GY");
        4  // GY
    } else if single_hue <= 4.5 {
        trace!(func_name, 9, format_vars(&[("single_hue", fmt_f64(single_hue))]), "BRANCH", "single_hue <= 4.5: G");
        3  // G
    } else if single_hue <= 5.5 {
        trace!(func_name, 10, format_vars(&[("single_hue", fmt_f64(single_hue))]), "BRANCH", "single_hue <= 5.5: BG");
        2  // BG
    } else if single_hue <= 6.5 {
        trace!(func_name, 11, format_vars(&[("single_hue", fmt_f64(single_hue))]), "BRANCH", "single_hue <= 6.5: B");
        1  // B
    } else if single_hue <= 8.5 {
        trace!(func_name, 12, format_vars(&[("single_hue", fmt_f64(single_hue))]), "BRANCH", "single_hue <= 8.5: PB");
        0  // PB
    } else if single_hue <= 9.5 {
        trace!(func_name, 13, format_vars(&[("single_hue", fmt_f64(single_hue))]), "BRANCH", "single_hue <= 9.5: P");
        9  // P
    } else {
        trace!(func_name, 14, format_vars(&[("single_hue", fmt_f64(single_hue))]), "BRANCH", "default: RP");
        8  // RP
    };
    
    // Calculate hue within the family
    let hue = ((single_hue + 0.5) % 1.0) * 10.0;
    trace!(func_name, 15, format_vars(&[("hue", fmt_f64(hue)), ("code", code.to_string())]), "CALC", "final hue calculation");
    
    trace!(func_name, 16, format_vars(&[("hue", fmt_f64(hue)), ("code", code.to_string())]), "RETURN", "");
    (hue, code)
}

/// Traced version of maximum_chroma_from_renotation
pub fn maximum_chroma_from_renotation(hue: f64, value: f64, code: u8) -> Result<f64> {
    let func_name = "maximum_chroma_from_renotation";
    
    trace!(func_name, 1, format_vars(&[("hue", fmt_f64(hue)), ("value", fmt_f64(value)), ("code", code.to_string())]), "ENTER", "");
    
    // Use the actual implementation from python_port.rs
    // This is a simplified version - in reality we'd need to instrument the full function
    let result = crate::python_port::maximum_chroma_from_renotation(hue, value, code)?;
    
    trace!(func_name, 2, format_vars(&[("result", fmt_f64(result))]), "CALL", "crate::python_port::maximum_chroma_from_renotation");
    trace!(func_name, 3, format_vars(&[("result", fmt_f64(result))]), "RETURN", "");
    
    Ok(result)
}

/// Traced version of bounding_hues_from_renotation
pub fn bounding_hues_from_renotation(hue: f64, code: u8) -> ((f64, u8), (f64, u8)) {
    let func_name = "bounding_hues_from_renotation";
    
    trace!(func_name, 1, format_vars(&[("hue", fmt_f64(hue)), ("code", code.to_string())]), "ENTER", "");
    
    // Use the actual implementation from python_port.rs
    let result = crate::python_port::bounding_hues_from_renotation(hue, code);
    
    trace!(func_name, 2, format_vars(&[("result", format!("{:?}", result))]), "CALL", "crate::python_port::bounding_hues_from_renotation");
    trace!(func_name, 3, format_vars(&[("result", format!("{:?}", result))]), "RETURN", "");
    
    result
}

/// Traced version of munsell_value_astmd1535
pub fn munsell_value_astmd1535(y: f64) -> f64 {
    let func_name = "munsell_value_astmd1535";
    
    trace!(func_name, 1, format_vars(&[("y", fmt_f64(y))]), "ENTER", "");
    
    // Use the actual implementation from python_port.rs
    let result = crate::python_port::munsell_value_astmd1535(y);
    
    trace!(func_name, 2, format_vars(&[("result", fmt_f64(result))]), "CALL", "crate::python_port_helpers::munsell_value_astmd1535");
    trace!(func_name, 3, format_vars(&[("result", fmt_f64(result))]), "RETURN", "");
    
    result
}

/// Traced version of lchab_to_munsell_specification
pub fn lchab_to_munsell_specification(lchab: [f64; 3]) -> [f64; 4] {
    let func_name = "lchab_to_munsell_specification";
    
    trace!(func_name, 1, format_vars(&[("lchab", fmt_f64_array(&lchab))]), "ENTER", "");
    
    // Use the actual implementation from python_port_lab.rs
    let result = crate::python_port_lab::lchab_to_munsell_specification(lchab);
    
    trace!(func_name, 2, format_vars(&[("result", fmt_f64_array(&result))]), "CALL", "crate::python_port_lab::lchab_to_munsell_specification");
    trace!(func_name, 3, format_vars(&[("result", fmt_f64_array(&result))]), "RETURN", "");
    
    result
}

/// Traced version of xy_from_renotation_ovoid_interpolated
pub fn xy_from_renotation_ovoid_interpolated(spec: &[f64; 4]) -> Result<[f64; 2]> {
    let func_name = "xy_from_renotation_ovoid_interpolated";
    
    trace!(func_name, 1, format_vars(&[("spec", fmt_f64_array(spec))]), "ENTER", "");
    
    // For now, use the actual implementation and just trace the call
    // In a full implementation, we would instrument every line
    let result = crate::python_port::xy_from_renotation_ovoid_interpolated(spec);
    
    match &result {
        Ok(xy) => {
            trace!(func_name, 2, format_vars(&[("result", fmt_f64_array(xy))]), "CALL", "crate::python_port::xy_from_renotation_ovoid_interpolated");
            trace!(func_name, 3, format_vars(&[("result", fmt_f64_array(xy))]), "RETURN", "Ok");
        }
        Err(e) => {
            trace!(func_name, 2, format_vars(&[("error", format!("{:?}", e))]), "CALL", "crate::python_port::xy_from_renotation_ovoid_interpolated");
            trace!(func_name, 3, format_vars(&[("error", format!("{:?}", e))]), "RETURN", "Err");
        }
    }
    
    result
}

/// Traced version of xy_from_renotation_ovoid
pub fn xy_from_renotation_ovoid(spec: &[f64; 4]) -> Result<[f64; 2]> {
    let func_name = "xy_from_renotation_ovoid";
    
    trace!(func_name, 1, format_vars(&[("spec", fmt_f64_array(spec))]), "ENTER", "");
    
    // For now, use the actual implementation and just trace the call
    let result = crate::python_port::xy_from_renotation_ovoid(spec);
    
    match &result {
        Ok(xy) => {
            trace!(func_name, 2, format_vars(&[("result", fmt_f64_array(xy))]), "CALL", "crate::python_port::xy_from_renotation_ovoid");
            trace!(func_name, 3, format_vars(&[("result", fmt_f64_array(xy))]), "RETURN", "Ok");
        }
        Err(e) => {
            trace!(func_name, 2, format_vars(&[("error", format!("{:?}", e))]), "CALL", "crate::python_port::xy_from_renotation_ovoid");
            trace!(func_name, 3, format_vars(&[("error", format!("{:?}", e))]), "RETURN", "Err");
        }
    }
    
    result
}

/// Traced version of xyy_to_munsell_specification - Main convergence loop
pub fn xyy_to_munsell_specification(xyy: [f64; 3]) -> Result<[f64; 4]> {
    let func_name = "xyy_to_munsell_specification";
    
    trace!(func_name, 1, format_vars(&[("xyy", fmt_f64_array(&xyy))]), "ENTER", "");
    
    use crate::python_port_helpers::*;
    
    let (x, y, big_y) = (xyy[0], xyy[1], xyy[2]);
    trace!(func_name, 2, format_vars(&[("x", fmt_f64(x)), ("y", fmt_f64(y)), ("big_y", fmt_f64(big_y))]), "CALC", "extract xyY components");
    
    // Check MacAdam limits
    if !is_within_macadam_limits(xyy, "C") {
        trace!(func_name, 3, format_vars(&[]), "BRANCH", "not within MacAdam limits");
    }
    
    // Convert Y to Munsell value
    let value = crate::python_port::munsell_value_astmd1535(big_y * 100.0);
    trace!(func_name, 4, format_vars(&[("value_raw", fmt_f64(value))]), "CALL", "munsell_value_astmd1535");
    
    let value = if (value - value.round()).abs() < 1e-10 {
        trace!(func_name, 5, format_vars(&[("value", fmt_f64(value.round()))]), "BRANCH", "value is integer: rounding");
        value.round()
    } else {
        trace!(func_name, 6, format_vars(&[("value", fmt_f64(value))]), "BRANCH", "value is not integer: keeping precise");
        value
    };
    
    // Get xy for the center (grey) at this value
    let (x_center, y_center) = (crate::constants::ILLUMINANT_C[0], crate::constants::ILLUMINANT_C[1]);
    trace!(func_name, 7, format_vars(&[("x_center", fmt_f64(x_center)), ("y_center", fmt_f64(y_center))]), "CALC", "illuminant C center point");
    
    // Convert to polar coordinates relative to center
    let (rho_input, phi_input, _) = cartesian_to_cylindrical(
        x - x_center, y - y_center, big_y
    );
    let phi_input = phi_input.to_degrees();
    trace!(func_name, 8, format_vars(&[("rho_input", fmt_f64(rho_input)), ("phi_input", fmt_f64(phi_input))]), "CALL", "cartesian_to_cylindrical");
    
    // Check if this is grey
    let grey_threshold = 1e-3;
    if rho_input < grey_threshold {
        trace!(func_name, 9, format_vars(&[("rho_input", fmt_f64(rho_input)), ("threshold", fmt_f64(grey_threshold))]), "BRANCH", "grey color detected");
        return Ok(normalise_munsell_specification(&[f64::NAN, value, 0.0, f64::NAN]));
    }
    
    // Initial guess using Lab color space
    let xyz = xyy_to_xyz(xyy);
    trace!(func_name, 10, format_vars(&[("xyz", fmt_f64_array(&xyz))]), "CALL", "xyy_to_xyz");
    
    let (x_i, y_i) = (crate::constants::ILLUMINANT_C[0], crate::constants::ILLUMINANT_C[1]);
    let xyz_r = xyy_to_xyz([x_i, y_i, big_y]);
    
    // Normalize reference white
    let xyz_r_norm = [xyz_r[0] / xyz_r[1], 1.0, xyz_r[2] / xyz_r[1]];
    
    let lab = xyz_to_lab(xyz, xyz_to_xy(xyz_r_norm));
    trace!(func_name, 11, format_vars(&[("lab", fmt_f64_array(&lab))]), "CALL", "xyz_to_lab");
    
    let lchab = lab_to_lchab(lab);
    trace!(func_name, 12, format_vars(&[("lchab", fmt_f64_array(&lchab))]), "CALL", "lab_to_lchab");
    
    let initial_spec = lchab_to_munsell_specification(lchab);
    trace!(func_name, 13, format_vars(&[("initial_spec", fmt_f64_array(&initial_spec))]), "CALL", "lchab_to_munsell_specification");
    
    // Ensure initial chroma is valid
    let initial_chroma = initial_spec[2];
    let initial_chroma = if initial_chroma.is_nan() || initial_chroma < 0.1 {
        trace!(func_name, 14, format_vars(&[("initial_chroma", fmt_f64(1.0))]), "BRANCH", "invalid chroma: default to 1.0");
        1.0
    } else if initial_chroma > 2.0 && value > 9.0 {
        trace!(func_name, 15, format_vars(&[("initial_chroma", fmt_f64(2.0))]), "BRANCH", "high value/chroma: limit to 2.0");
        2.0
    } else {
        trace!(func_name, 16, format_vars(&[("initial_chroma", fmt_f64(initial_chroma))]), "BRANCH", "valid chroma: keeping");
        initial_chroma
    };
    
    // Ensure initial hue is valid
    let initial_hue = if initial_spec[0].is_nan() {
        trace!(func_name, 17, format_vars(&[("initial_hue", fmt_f64(5.0))]), "BRANCH", "invalid hue: default to 5.0");
        5.0
    } else {
        trace!(func_name, 18, format_vars(&[("initial_hue", fmt_f64(initial_spec[0]))]), "BRANCH", "valid hue: keeping");
        initial_spec[0]
    };
    
    let mut specification_current = [
        initial_hue,
        value,
        initial_chroma,
        initial_spec[3],
    ];
    trace!(func_name, 19, format_vars(&[("spec_current", fmt_f64_array(&specification_current))]), "CALC", "initial specification");
    
    // Main convergence loop
    let convergence_threshold = 1e-3 / 1e4;  // THRESHOLD_INTEGER / 1e4 = 1e-7
    let iterations_maximum = 64;
    let mut iterations = 0;
    
    trace!(func_name, 20, format_vars(&[("convergence_threshold", fmt_f64(convergence_threshold)), ("iterations_maximum", iterations_maximum.to_string())]), "CALC", "convergence parameters");
    
    while iterations <= iterations_maximum {
        iterations += 1;
        trace!(func_name, 21, format_vars(&[("iterations", iterations.to_string())]), "LOOP", format!("convergence iteration {}", iterations));
        
        let hue_current = specification_current[0];
        let chroma_current = specification_current[2];
        let code_current = if specification_current[3].is_nan() { 0 } else { specification_current[3] as u8 };
        trace!(func_name, 22, format_vars(&[("hue_current", fmt_f64(hue_current)), ("chroma_current", fmt_f64(chroma_current)), ("code_current", code_current.to_string())]), "CALC", "current spec values");
        
        let hue_angle_current = hue_to_hue_angle(hue_current, code_current);
        trace!(func_name, 23, format_vars(&[("hue_angle_current", fmt_f64(hue_angle_current))]), "CALL", "hue_to_hue_angle");
        
        // Check maximum chroma
        let chroma_maximum = maximum_chroma_from_renotation(hue_current, value, code_current)?;
        trace!(func_name, 24, format_vars(&[("chroma_maximum", fmt_f64(chroma_maximum))]), "CALL", "maximum_chroma_from_renotation");
        
        let chroma_current = if chroma_current > chroma_maximum {
            trace!(func_name, 25, format_vars(&[("chroma_limited", fmt_f64(chroma_maximum))]), "BRANCH", "chroma exceeds max: limiting");
            chroma_maximum
        } else {
            trace!(func_name, 26, format_vars(&[("chroma_current", fmt_f64(chroma_current))]), "BRANCH", "chroma within max: keeping");
            chroma_current
        };
        specification_current[2] = chroma_current;
        
        // If chroma is 0, we have a grey color
        if chroma_current == 0.0 {
            trace!(func_name, 27, format_vars(&[]), "BRANCH", "grey color (chroma=0): returning");
            return Ok([f64::NAN, value, 0.0, f64::NAN]);
        }
        
        // Get current xy - Use interpolated version for iterative algorithm
        let xy_current = xy_from_renotation_ovoid_interpolated(&specification_current)?;
        let (x_current, y_current) = (xy_current[0], xy_current[1]);
        trace!(func_name, 28, format_vars(&[("x_current", fmt_f64(x_current)), ("y_current", fmt_f64(y_current))]), "CALL", "xy_from_renotation_ovoid_interpolated");
        
        // Convert to polar
        let (rho_current, phi_current, _) = cartesian_to_cylindrical(
            x_current - x_center, y_current - y_center, big_y
        );
        let phi_current = phi_current.to_degrees();
        trace!(func_name, 29, format_vars(&[("rho_current", fmt_f64(rho_current)), ("phi_current", fmt_f64(phi_current))]), "CALL", "cartesian_to_cylindrical current");
        
        // Calculate phi difference
        let mut phi_current_difference = (360.0 - phi_input + phi_current) % 360.0;
        if phi_current_difference > 180.0 {
            phi_current_difference -= 360.0;
        }
        trace!(func_name, 30, format_vars(&[("phi_current_difference", fmt_f64(phi_current_difference))]), "CALC", "phi difference");
        
        // Inner loop for hue refinement
        let mut phi_differences_data = vec![phi_current_difference];
        let mut hue_angles_differences_data = vec![0.0];
        let mut hue_angles = vec![hue_angle_current];
        
        let iterations_maximum_inner = 16;
        let mut iterations_inner = 0;
        let mut extrapolate = false;
        
        trace!(func_name, 31, format_vars(&[("iterations_maximum_inner", iterations_maximum_inner.to_string())]), "CALC", "inner loop parameters");
        
        while phi_differences_data.iter().all(|&d| d >= 0.0) || 
              phi_differences_data.iter().all(|&d| d <= 0.0) {
            if extrapolate {
                trace!(func_name, 32, format_vars(&[]), "BRANCH", "extrapolate=true: breaking inner loop");
                break;
            }
            
            iterations_inner += 1;
            trace!(func_name, 33, format_vars(&[("iterations_inner", iterations_inner.to_string())]), "LOOP", format!("inner iteration {}", iterations_inner));
            
            if iterations_inner > iterations_maximum_inner {
                trace!(func_name, 34, format_vars(&[]), "BRANCH", "max inner iterations reached: error");
                return Err(crate::error::MunsellError::ConversionError {
                    message: "Maximum inner iterations reached without convergence".to_string()
                });
            }
            
            let hue_angle_inner = (hue_angle_current + iterations_inner as f64 * (phi_input - phi_current)) % 360.0;
            let mut hue_angle_difference_inner = (iterations_inner as f64 * (phi_input - phi_current)) % 360.0;
            if hue_angle_difference_inner > 180.0 {
                hue_angle_difference_inner -= 360.0;
            }
            trace!(func_name, 35, format_vars(&[("hue_angle_inner", fmt_f64(hue_angle_inner)), ("hue_angle_difference_inner", fmt_f64(hue_angle_difference_inner))]), "CALC", "inner hue angles");
            
            let (hue_inner, code_inner) = hue_angle_to_hue(hue_angle_inner);
            trace!(func_name, 36, format_vars(&[("hue_inner", fmt_f64(hue_inner)), ("code_inner", code_inner.to_string())]), "CALL", "hue_angle_to_hue");
            
            let spec_inner = [hue_inner, value, chroma_current, code_inner as f64];
            
            // Use interpolated version for iterative algorithm
            let xy_inner = match xy_from_renotation_ovoid_interpolated(&spec_inner) {
                Ok(xy) => {
                    trace!(func_name, 37, format_vars(&[("xy_inner", fmt_f64_array(&xy))]), "CALL", "xy_from_renotation_ovoid_interpolated inner: Ok");
                    xy
                },
                Err(_) => {
                    trace!(func_name, 38, format_vars(&[]), "BRANCH", "xy_from_renotation_ovoid_interpolated inner: Err - setting extrapolate=true");
                    extrapolate = true;
                    continue;
                }
            };
            let (x_inner, y_inner) = (xy_inner[0], xy_inner[1]);
            
            // Need at least 2 points for reliable extrapolation
            if phi_differences_data.len() >= 2 {
                trace!(func_name, 39, format_vars(&[("data_points", phi_differences_data.len().to_string())]), "BRANCH", "enough data points: setting extrapolate=true");
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
                trace!(func_name, 40, format_vars(&[("phi_inner_difference", fmt_f64(phi_inner_difference))]), "CALC", "inner phi difference");
                
                phi_differences_data.push(phi_inner_difference);
                hue_angles.push(hue_angle_inner);
                hue_angles_differences_data.push(hue_angle_difference_inner);
            }
        }
        
        // Check convergence condition here (simplified for now)
        if phi_current_difference.abs() < convergence_threshold {
            trace!(func_name, 41, format_vars(&[("phi_difference", fmt_f64(phi_current_difference.abs())), ("threshold", fmt_f64(convergence_threshold))]), "BRANCH", "convergence achieved");
            break;
        }
    }
    
    trace!(func_name, 42, format_vars(&[("final_spec", fmt_f64_array(&specification_current))]), "RETURN", "convergence complete");
    Ok(specification_current)
}