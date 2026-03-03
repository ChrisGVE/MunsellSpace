//! Hue conversion functions — exact 1:1 ports from Python colour-science.

/// Convert [hue, code] to ASTM hue number.
/// ASTM_hue = 10 * ((7 - code) % 10) + hue
pub fn hue_to_astm_hue(hue: f64, code: u8) -> f64 {
    let offset = (7 - code as i32) % 10;
    let offset = if offset < 0 { offset + 10 } else { offset };
    let astm_hue = 10.0 * offset as f64 + hue;

    if astm_hue == 0.0 { 100.0 } else { astm_hue }
}

/// Convert ASTM hue to [hue, code] pair.
pub fn astm_hue_to_hue(astm_hue: f64) -> (f64, u8) {
    let astm_hue = if astm_hue == 100.0 { 0.0 } else { astm_hue };

    let mut code = ((17.0 - (astm_hue / 10.0).floor()) % 10.0) as u8;
    if code == 0 {
        code = 10;
    }

    let hue = astm_hue % 10.0;
    (hue, code)
}

/// Convert hue and code to hue angle in degrees using breakpoint interpolation.
pub fn hue_to_hue_angle(hue: f64, code: u8) -> f64 {
    let raw = (17.0 - code as f64) % 10.0 + (hue / 10.0) - 0.5;
    let single_hue = if raw < 0.0 {
        (raw % 10.0) + 10.0
    } else {
        raw % 10.0
    };

    let breakpoints = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0];
    let angles = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0];

    for i in 0..breakpoints.len() - 1 {
        if single_hue >= breakpoints[i] && single_hue <= breakpoints[i + 1] {
            let t = (single_hue - breakpoints[i]) / (breakpoints[i + 1] - breakpoints[i]);
            return angles[i] + t * (angles[i + 1] - angles[i]);
        }
    }

    360.0
}

/// Convert hue angle to [hue, code] pair.
pub fn hue_angle_to_hue(hue_angle: f64) -> (f64, u8) {
    let angles = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0];
    let values = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0];

    let mut single_hue = 0.0;
    for i in 0..angles.len() - 1 {
        if hue_angle >= angles[i] && hue_angle <= angles[i + 1] {
            let t = (hue_angle - angles[i]) / (angles[i + 1] - angles[i]);
            single_hue = values[i] + t * (values[i + 1] - values[i]);
            break;
        }
    }

    let code = if single_hue <= 0.5 { 7 }
    else if single_hue <= 1.5 { 6 }
    else if single_hue <= 2.5 { 5 }
    else if single_hue <= 3.5 { 4 }
    else if single_hue <= 4.5 { 3 }
    else if single_hue <= 5.5 { 2 }
    else if single_hue <= 6.5 { 1 }
    else if single_hue <= 7.5 { 10 }
    else if single_hue <= 8.5 { 9 }
    else if single_hue <= 9.5 { 8 }
    else { 7 };

    let mut hue = (10.0 * (single_hue % 1.0) + 5.0) % 10.0;
    if hue == 0.0 {
        hue = 10.0;
    }

    (hue, code)
}

/// Find bounding hues from renotation data.
pub fn bounding_hues_from_renotation(hue: f64, code: u8) -> ((f64, u8), (f64, u8)) {
    let mut hue_cw: f64;
    let code_cw: u8;
    let hue_ccw: f64;
    let code_ccw: u8;

    if (hue % 2.5).abs() < 1e-10 {
        if hue.abs() < 1e-10 {
            hue_cw = 10.0;
            code_cw = if code == 10 { 1 } else { code + 1 };
        } else {
            hue_cw = hue;
            code_cw = code;
        }
        hue_ccw = hue_cw;
        code_ccw = code_cw;
    } else {
        hue_cw = 2.5 * (hue / 2.5).floor();
        let mut temp_hue_ccw = (hue_cw + 2.5) % 10.0;
        if temp_hue_ccw.abs() < 1e-10 {
            temp_hue_ccw = 10.0;
        }
        hue_ccw = temp_hue_ccw;

        if hue_cw.abs() < 1e-10 {
            hue_cw = 10.0;
            code_cw = if code == 10 { 1 } else { code + 1 };
        } else {
            code_cw = code;
        }
        code_ccw = code;
    }

    ((hue_cw, code_cw), (hue_ccw, code_ccw))
}
