//! Core types for Munsell Cartesian and specification representations.

use std::f64::consts::PI;
use super::parsing::hue_number_to_string;

/// Represents a point in 3D Munsell Cartesian space.
///
/// Coordinates are derived from cylindrical Munsell (H, V, C) where:
/// - x = chroma * cos(theta)
/// - y = chroma * sin(theta)
/// - z = value
///
/// Theta is calculated from hue number: theta = hue_number * 9 degrees
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct MunsellCartesian {
    /// X coordinate (chroma * cos(hue_angle))
    pub x: f64,
    /// Y coordinate (chroma * sin(hue_angle))
    pub y: f64,
    /// Z coordinate (value, 0-10)
    pub z: f64,
}

impl MunsellCartesian {
    /// Create a new Cartesian coordinate.
    pub fn new(x: f64, y: f64, z: f64) -> Self {
        Self { x, y, z }
    }

    /// Calculate Euclidean distance to another point.
    pub fn distance(&self, other: &MunsellCartesian) -> f64 {
        let dx = self.x - other.x;
        let dy = self.y - other.y;
        let dz = self.z - other.z;
        (dx * dx + dy * dy + dz * dz).sqrt()
    }
}

/// Represents a Munsell color specification with numeric hue.
///
/// This is used internally for polyhedron calculations where we need
/// the hue as a continuous number (0-40) rather than a string.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct MunsellSpec {
    /// Hue as a number from 0-40 (continuous around the hue circle).
    /// 0 = 10RP, 4 = 10R, 8 = 10YR, etc.
    /// Each integer step represents 2.5 hue units.
    pub hue_number: f64,
    /// Value (lightness) from 0-10.
    pub value: f64,
    /// Chroma (saturation) from 0+.
    pub chroma: f64,
}

impl MunsellSpec {
    /// Create a new Munsell specification.
    pub fn new(hue_number: f64, value: f64, chroma: f64) -> Self {
        Self {
            hue_number,
            value,
            chroma,
        }
    }

    /// Create a neutral (achromatic) Munsell specification.
    pub fn neutral(value: f64) -> Self {
        Self {
            hue_number: 0.0,
            value,
            chroma: 0.0,
        }
    }

    /// Convert to 3D Cartesian coordinates for polyhedron math.
    ///
    /// The conversion follows Centore's methodology:
    /// - Hue angle: theta = hue_number * 9 degrees (40 steps = 360 degrees)
    /// - x = chroma * cos(theta)
    /// - y = chroma * sin(theta)
    /// - z = value
    pub fn to_cartesian(&self) -> MunsellCartesian {
        let theta = self.hue_number * 9.0 * PI / 180.0;
        MunsellCartesian {
            x: self.chroma * theta.cos(),
            y: self.chroma * theta.sin(),
            z: self.value,
        }
    }

    /// Create from 3D Cartesian coordinates.
    ///
    /// This is the inverse of `to_cartesian()`.
    pub fn from_cartesian(cart: &MunsellCartesian) -> Self {
        let chroma = (cart.x * cart.x + cart.y * cart.y).sqrt();

        // Handle achromatic case
        if chroma < 1e-10 {
            return Self::neutral(cart.z);
        }

        // Calculate hue angle from x, y
        let mut theta = cart.y.atan2(cart.x);
        if theta < 0.0 {
            theta += 2.0 * PI;
        }

        // Convert radians to hue number (0-40)
        let hue_number = theta * 180.0 / PI / 9.0;

        Self {
            hue_number: hue_number % 40.0,
            value: cart.z,
            chroma,
        }
    }

    /// Convert to Munsell notation string.
    ///
    /// # Returns
    /// String like "5R 4.0/12.0" or "N 5.0/" for neutral colors.
    pub fn to_notation(&self) -> String {
        if self.chroma < 0.5 {
            return format!("N {:.1}/", self.value);
        }

        let (hue_str, _) = hue_number_to_string(self.hue_number);
        format!("{} {:.1}/{:.1}", hue_str, self.value, self.chroma)
    }

    /// Distance from centroid (for finding closest overlay).
    pub fn distance_from(&self, other: &MunsellSpec) -> f64 {
        self.to_cartesian().distance(&other.to_cartesian())
    }
}
