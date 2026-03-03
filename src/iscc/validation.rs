//! Validation functions for ISCC-NBS polygon data integrity.

use super::color::IsccNbsColor;
use geo::Intersects;

/// Validation error types for ISCC-NBS polygon data.
#[derive(Debug, Clone)]
pub enum ValidationError {
    InvalidAngle {
        color_number: u16,
        point_index: usize,
        angle: f64,
    },
    Intersection {
        color1: u16,
        color2: u16,
    },
    Gap {
        hue_slice: String,
        region: String,
    },
}

/// Validate ISCC-NBS polygon data for integrity.
pub fn validate_polygons(colors: &[IsccNbsColor]) -> Vec<ValidationError> {
    let mut errors = Vec::new();

    // Check right angles using geo's geometric operations
    for color in colors {
        if let Err(mut angle_errors) = validate_right_angles(&color.polygon) {
            for error in &mut angle_errors {
                if let ValidationError::InvalidAngle { color_number, .. } = error {
                    *color_number = color.color_number;
                }
            }
            errors.extend(angle_errors);
        }
    }

    // Check for intersections using geo's robust intersection detection
    for i in 0..colors.len() {
        for j in (i + 1)..colors.len() {
            if colors[i].polygon.intersects(&colors[j].polygon) {
                errors.push(ValidationError::Intersection {
                    color1: colors[i].color_number,
                    color2: colors[j].color_number,
                });
            }
        }
    }

    errors
}

/// Validate that polygon has only right angles (90 and 270 degrees).
fn validate_right_angles(polygon: &geo::Polygon<f64>) -> Result<(), Vec<ValidationError>> {
    let exterior = polygon.exterior();
    let coords: Vec<_> = exterior.coords().collect();

    if coords.len() < 4 {
        return Ok(());
    }

    let mut errors = Vec::new();

    for i in 1..coords.len() - 1 {
        let p1 = coords[i - 1];
        let p2 = coords[i];
        let p3 = coords[i + 1];

        let v1 = (p1.x - p2.x, p1.y - p2.y);
        let v2 = (p3.x - p2.x, p3.y - p2.y);

        let dot = v1.0 * v2.0 + v1.1 * v2.1;
        let cross = v1.0 * v2.1 - v1.1 * v2.0;
        let angle = cross.atan2(dot).abs() * 180.0 / std::f64::consts::PI;

        let tolerance = 1.0;
        let is_right_angle =
            (angle - 90.0).abs() < tolerance || (angle - 270.0).abs() < tolerance;

        if !is_right_angle {
            errors.push(ValidationError::InvalidAngle {
                color_number: 0,
                point_index: i,
                angle,
            });
        }
    }

    if errors.is_empty() {
        Ok(())
    } else {
        Err(errors)
    }
}
