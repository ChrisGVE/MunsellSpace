//! Helper functions needed for the Python port
//! These are utility functions used by the main algorithm

use std::f64;

/// Calculate Euclidean distance between two 2D points
pub fn euclidean_distance(p1: [f64; 2], p2: [f64; 2]) -> f64 {
    ((p1[0] - p2[0]).powi(2) + (p1[1] - p2[1]).powi(2)).sqrt()
}

/// Convert XYZ to Lab color space
/// Using D65 illuminant
pub fn xyz_to_lab(xyz: [f64; 3], white_point: [f64; 2]) -> [f64; 3] {
    // This is a placeholder - need full implementation
    // For now, return dummy values
    [0.0, 0.0, 0.0]
}

/// Convert Lab to LCHab (cylindrical Lab)
pub fn lab_to_lchab(lab: [f64; 3]) -> [f64; 3] {
    let l = lab[0];
    let a = lab[1];
    let b = lab[2];
    
    let c = (a * a + b * b).sqrt();
    let h = b.atan2(a).to_degrees();
    let h = if h < 0.0 { h + 360.0 } else { h };
    
    [l, c, h]
}

/// Convert LCHab to Munsell specification
/// This is a rough approximation - need exact Python implementation
pub fn lchab_to_munsell_specification(lch: [f64; 3]) -> [f64; 4] {
    // Placeholder implementation
    let hue_angle = lch[2];
    let (hue, code) = crate::python_port::hue_angle_to_hue(hue_angle);
    [hue, 5.0, lch[1] / 10.0, code as f64]
}

/// Convert xyY to XYZ
pub fn xyy_to_xyz(xyy: [f64; 3]) -> [f64; 3] {
    let (x, y, big_y) = (xyy[0], xyy[1], xyy[2]);
    
    if y.abs() < 1e-10 {
        return [0.0, 0.0, 0.0];
    }
    
    let big_x = x * big_y / y;
    let big_z = (1.0 - x - y) * big_y / y;
    
    [big_x, big_y, big_z]
}

/// Convert XYZ to xy chromaticity
pub fn xyz_to_xy(xyz: [f64; 3]) -> [f64; 2] {
    let sum = xyz[0] + xyz[1] + xyz[2];
    if sum.abs() < 1e-10 {
        return [0.3127, 0.3290]; // D65 default
    }
    [xyz[0] / sum, xyz[1] / sum]
}

/// Check if xyY is within MacAdam limits
/// Placeholder - need actual implementation
pub fn is_within_macadam_limits(xyy: [f64; 3], illuminant: &str) -> bool {
    // For now, always return true
    // TODO: Implement actual MacAdam limits check
    true
}

/// Linear interpolation with extrapolation
pub struct LinearInterpolator {
    x_values: Vec<f64>,
    y_values: Vec<f64>,
}

impl LinearInterpolator {
    pub fn new(x: Vec<f64>, y: Vec<f64>) -> Self {
        Self {
            x_values: x,
            y_values: y,
        }
    }
    
    pub fn interpolate(&self, x: f64) -> f64 {
        if self.x_values.len() < 2 {
            return self.y_values[0];
        }
        
        // Find surrounding points
        let mut i = 0;
        while i < self.x_values.len() - 1 && self.x_values[i + 1] < x {
            i += 1;
        }
        
        if i == self.x_values.len() - 1 {
            // Extrapolate beyond last point
            i = self.x_values.len() - 2;
        }
        
        let x1 = self.x_values[i];
        let x2 = self.x_values[i + 1];
        let y1 = self.y_values[i];
        let y2 = self.y_values[i + 1];
        
        y1 + (x - x1) * (y2 - y1) / (x2 - x1)
    }
}

/// Extrapolator wrapper
pub struct Extrapolator {
    interpolator: LinearInterpolator,
}

impl Extrapolator {
    pub fn new(interpolator: LinearInterpolator) -> Self {
        Self { interpolator }
    }
    
    pub fn extrapolate(&self, x: f64) -> f64 {
        self.interpolator.interpolate(x)
    }
}