//! Helper functions needed for the Python port
//! These are utility functions used by the main algorithm

use std::f64;

/// Calculate Euclidean distance between two 2D points
pub fn euclidean_distance(p1: [f64; 2], p2: [f64; 2]) -> f64 {
    ((p1[0] - p2[0]).powi(2) + (p1[1] - p2[1]).powi(2)).sqrt()
}

/// Convert XYZ to Lab color space
/// Using given white point xy chromaticity
pub fn xyz_to_lab(xyz: [f64; 3], white_point: [f64; 2]) -> [f64; 3] {
    // Convert white point xy to XYZ (assuming Y=1)
    let wp_sum = white_point[0] + white_point[1] + (1.0 - white_point[0] - white_point[1]);
    let xn = white_point[0] / white_point[1];
    let yn = 1.0;
    let zn = (1.0 - white_point[0] - white_point[1]) / white_point[1];
    
    // Normalize XYZ by white point
    let x_norm = xyz[0] / xn;
    let y_norm = xyz[1] / yn;
    let z_norm = xyz[2] / zn;
    
    // Apply Lab transformation
    let epsilon = 216.0 / 24389.0;
    let kappa = 24389.0 / 27.0;
    
    let fx = if x_norm > epsilon {
        x_norm.powf(1.0 / 3.0)
    } else {
        (kappa * x_norm + 16.0) / 116.0
    };
    
    let fy = if y_norm > epsilon {
        y_norm.powf(1.0 / 3.0)
    } else {
        (kappa * y_norm + 16.0) / 116.0
    };
    
    let fz = if z_norm > epsilon {
        z_norm.powf(1.0 / 3.0)
    } else {
        (kappa * z_norm + 16.0) / 116.0
    };
    
    let l = 116.0 * fy - 16.0;
    let a = 500.0 * (fx - fy);
    let b = 200.0 * (fy - fz);
    
    [l, a, b]
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
/// Initial approximation for starting the iterative algorithm
pub fn lchab_to_munsell_specification(lch: [f64; 3]) -> [f64; 4] {
    // Convert hue angle to Munsell hue
    let hue_angle = lch[2];
    let (hue, code) = crate::python_port::hue_angle_to_hue(hue_angle);
    
    // Very rough initial approximation
    // Value from lightness (roughly)
    let value = lch[0] / 10.0;  // L* is 0-100, Munsell value is 0-10
    
    // Chroma from C* (very rough)
    let chroma = lch[1] / 5.5;  // This scaling factor is from Python
    
    [hue, value, chroma, code as f64]
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
/// For Munsell, this checks if the color is physically realizable
pub fn is_within_macadam_limits(xyy: [f64; 3], illuminant: &str) -> bool {
    let (x, y, _) = (xyy[0], xyy[1], xyy[2]);
    
    // Basic sanity checks
    if x < 0.0 || x > 1.0 || y < 0.0 || y > 1.0 {
        return false;
    }
    
    // Check if point is inside the spectral locus
    // This is a simplified check - full implementation would use
    // the actual MacAdam limits boundary
    
    // For now, use a simple triangle check that encompasses
    // most real colors
    let vertices = [
        (0.17, 0.00),  // Blue corner
        (0.00, 0.83),  // Green corner  
        (0.73, 0.27),  // Red corner
    ];
    
    // Check if point is inside the triangle
    // Using barycentric coordinates
    let v0 = (vertices[2].0 - vertices[0].0, vertices[2].1 - vertices[0].1);
    let v1 = (vertices[1].0 - vertices[0].0, vertices[1].1 - vertices[0].1);
    let v2 = (x - vertices[0].0, y - vertices[0].1);
    
    let dot00 = v0.0 * v0.0 + v0.1 * v0.1;
    let dot01 = v0.0 * v1.0 + v0.1 * v1.1;
    let dot02 = v0.0 * v2.0 + v0.1 * v2.1;
    let dot11 = v1.0 * v1.0 + v1.1 * v1.1;
    let dot12 = v1.0 * v2.0 + v1.1 * v2.1;
    
    let inv_denom = 1.0 / (dot00 * dot11 - dot01 * dot01);
    let u = (dot11 * dot02 - dot01 * dot12) * inv_denom;
    let v = (dot00 * dot12 - dot01 * dot02) * inv_denom;
    
    // Check if point is in triangle
    (u >= 0.0) && (v >= 0.0) && (u + v <= 1.0)
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