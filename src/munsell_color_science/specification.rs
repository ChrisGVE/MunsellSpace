//! Munsell specification helpers and ASTM D1535 value/luminance functions.

/// Check if a Munsell specification represents a grey color.
pub fn is_grey_munsell_colour(spec: &[f64; 4]) -> bool {
    spec[0].is_nan() || spec[2] == 0.0
}

/// Normalize Munsell specification (handle wraparound).
pub fn normalise_munsell_specification(spec: &[f64; 4]) -> [f64; 4] {
    if spec[0].is_nan() && spec[2].is_nan() {
        return *spec;
    }

    let mut hue = spec[0];
    let value = spec[1];
    let chroma = spec[2];
    let mut code = if spec[3].is_nan() { 1 } else { spec[3] as u8 };

    if hue == 0.0 {
        hue = 10.0;
        code += 1;
        if code > 10 {
            code = 1;
        }
    }

    if chroma == 0.0 {
        return [f64::NAN, value, f64::NAN, f64::NAN];
    }

    [hue, value, chroma, code as f64]
}

/// Convert from Munsell value to CIE Y luminance using ASTM D1535 polynomial.
pub fn luminance_astmd1535(value: f64) -> f64 {
    let v = value;
    let v2 = v * v;
    let v3 = v2 * v;
    let v4 = v3 * v;
    let v5 = v4 * v;

    1.1914 * v - 0.22533 * v2 + 0.23352 * v3 - 0.020484 * v4 + 0.00081939 * v5
}

/// Convert from CIE Y luminance to Munsell value using Newton-Raphson.
pub fn munsell_value_astmd1535(y: f64) -> f64 {
    let mut value = 10.0 * y.powf(0.5);

    for _ in 0..100 {
        let y_current = luminance_astmd1535(value);
        let error = y_current - y;

        if error.abs() < 1e-10 {
            break;
        }

        let v = value;
        let v2 = v * v;
        let v3 = v2 * v;
        let v4 = v3 * v;
        let derivative = 1.1914 - 2.0 * 0.22533 * v + 3.0 * 0.23352 * v2
            - 4.0 * 0.020484 * v3 + 5.0 * 0.00081939 * v4;

        value -= error / derivative;
        value = value.clamp(0.0, 10.0);
    }

    value
}

/// Convert cartesian to cylindrical coordinates.
pub fn cartesian_to_cylindrical(x: f64, y: f64, z: f64) -> (f64, f64, f64) {
    let rho = (x * x + y * y).sqrt();
    let phi = y.atan2(x);
    (rho, phi, z)
}

/// Convert polar to cartesian coordinates.
pub fn polar_to_cartesian(rho: f64, phi: f64) -> (f64, f64) {
    (rho * phi.cos(), rho * phi.sin())
}
