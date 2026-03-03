//! Coordinate transformation functions following Python colour-science.

/// Convert cartesian [x, y] to polar [rho, phi] coordinates.
/// phi is in radians [-π, π]
#[inline]
pub fn cartesian_to_polar(x: f64, y: f64) -> (f64, f64) {
    let rho = x.hypot(y);
    let phi = y.atan2(x);
    (rho, phi)
}

/// Convert polar [rho, phi] to cartesian [x, y] coordinates.
/// phi should be in radians
#[inline]
pub fn polar_to_cartesian(rho: f64, phi: f64) -> (f64, f64) {
    let x = rho * phi.cos();
    let y = rho * phi.sin();
    (x, y)
}

/// Convert cartesian [x, y, z] to cylindrical [rho, phi, z] coordinates.
/// Uses cartesian_to_polar for first two coordinates, keeps z unchanged
#[inline]
pub fn cartesian_to_cylindrical(x: f64, y: f64, z: f64) -> (f64, f64, f64) {
    let (rho, phi) = cartesian_to_polar(x, y);
    (rho, phi, z)
}

/// Convert cylindrical [rho, phi, z] to cartesian [x, y, z] coordinates
#[inline]
#[allow(dead_code)]
pub fn cylindrical_to_cartesian(rho: f64, phi: f64, z: f64) -> (f64, f64, f64) {
    let (x, y) = polar_to_cartesian(rho, phi);
    (x, y, z)
}
