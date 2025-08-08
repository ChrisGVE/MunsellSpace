//! Traced version of the Python port with automatic instrumentation using tracing crate

use tracing::{instrument, trace, debug, info};
use crate::error::Result;

// Re-export all the original functions but with tracing instrumentation
pub use crate::python_port::*;

/// Traced version of xyY to Munsell specification conversion
#[instrument(level = "debug", ret, err)]
pub fn xyy_to_munsell_specification_traced(xyy: [f64; 3]) -> Result<[f64; 4]> {
    trace!("Starting xyY to Munsell conversion");
    trace!("Input xyY: [{:.6}, {:.6}, {:.6}]", xyy[0], xyy[1], xyy[2]);
    
    let result = crate::python_port::xyy_to_munsell_specification(xyy)?;
    
    debug!("Conversion result: hue={:.2}, value={:.2}, chroma={:.2}, code={}", 
           result[0], result[1], result[2], result[3] as u8);
    
    Ok(result)
}

/// Traced version of Munsell specification to xyY conversion
#[instrument(level = "debug", ret, err)]
pub fn munsell_specification_to_xyy_traced(specification: &[f64; 4]) -> Result<[f64; 3]> {
    trace!("Starting Munsell to xyY conversion");
    trace!("Input specification: [{:.2}, {:.2}, {:.2}, {}]", 
           specification[0], specification[1], specification[2], specification[3] as u8);
    
    let result = crate::python_port::munsell_specification_to_xyy(specification)?;
    
    debug!("Conversion result: xyY=[{:.6}, {:.6}, {:.6}]", 
           result[0], result[1], result[2]);
    
    Ok(result)
}

/// Traced version of xy_from_renotation_ovoid
#[instrument(level = "trace", ret)]
pub fn xy_from_renotation_ovoid_traced(
    specification: &[f64; 4],
    out_of_gamut: bool,
) -> Result<[f64; 2]> {
    trace!("Computing xy from renotation ovoid");
    trace!("Specification: [{:.2}, {:.2}, {:.2}, {}]", 
           specification[0], specification[1], specification[2], specification[3] as u8);
    trace!("Out of gamut: {}", out_of_gamut);
    
    let result = crate::python_port::xy_from_renotation_ovoid(specification, out_of_gamut)?;
    
    trace!("Result xy: [{:.6}, {:.6}]", result[0], result[1]);
    
    Ok(result)
}

/// Traced version of maximum_chroma_from_renotation
#[instrument(level = "trace", ret)]
pub fn maximum_chroma_from_renotation_traced(
    hue: f64,
    value: f64,
    code: u8,
) -> Result<f64> {
    trace!("Computing maximum chroma from renotation");
    
    let result = crate::python_port::maximum_chroma_from_renotation(hue, value, code)?;
    
    trace!("Maximum chroma: {:.4}", result);
    
    Ok(result)
}

/// Traced version of hue_to_hue_angle
#[instrument(level = "trace", ret)]
pub fn hue_to_hue_angle_traced(hue: f64, code: u8) -> f64 {
    let result = crate::python_port::hue_to_hue_angle(hue, code);
    trace!("Hue {} with code {} -> angle {:.2}°", hue, code, result);
    result
}

/// Traced version of hue_angle_to_hue
#[instrument(level = "trace", ret)]
pub fn hue_angle_to_hue_traced(hue_angle: f64) -> [f64; 2] {
    let result = crate::python_port::hue_angle_to_hue(hue_angle);
    trace!("Angle {:.2}° -> hue {:.2} with code {}", 
           hue_angle, result[0], result[1] as u8);
    result
}

/// Traced version of munsell_value_astmd1535
#[instrument(level = "trace", ret)]
pub fn munsell_value_astmd1535_traced(y: f64) -> f64 {
    let result = crate::python_port::munsell_value_astmd1535(y);
    trace!("Y={:.4} -> Munsell value={:.4}", y, result);
    result
}