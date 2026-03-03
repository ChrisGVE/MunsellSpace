//! Interpolation method lookup from renotation ovoid.
//! Exact 1:1 port of the empirical lookup table from Python colour-science.

use super::hue_conversions::hue_to_astm_hue;

/// Determine interpolation method (Linear vs Radial) from renotation ovoid.
pub fn interpolation_method_from_renotation_ovoid(
    hue: f64, value: f64, chroma: f64, code: u8,
) -> Option<&'static str> {
    if chroma == 0.0 {
        return None;
    }

    let value = value.round() as i32;
    let chroma = (2.0 * (chroma / 2.0).round()) as i32;

    if (hue % 2.5).abs() < 1e-10 {
        return None;
    }

    let astm_hue = hue_to_astm_hue(hue, code);

    match value {
        1 => value_1_method(astm_hue, chroma),
        2 => value_2_method(astm_hue, chroma),
        3 => value_3_method(astm_hue, chroma),
        4 => value_4_method(astm_hue, chroma),
        5 => value_5_method(astm_hue, chroma),
        6 => value_6_method(astm_hue, chroma),
        7 => value_7_method(astm_hue, chroma),
        8 => value_8_method(astm_hue, chroma),
        9 => value_9_method(astm_hue, chroma),
        10 => None,
        _ => Some("Linear"),
    }
}

fn value_1_method(h: f64, c: i32) -> Option<&'static str> {
    match c {
        2 => radial_if((15.0 < h && h < 30.0) || (60.0 < h && h < 85.0)),
        4 => radial_if((12.5 < h && h < 27.5) || (57.5 < h && h < 80.0)),
        6 => radial_if(55.0 < h && h < 80.0),
        8 => radial_if(67.5 < h && h < 77.5),
        _ if c >= 10 => radial_if(72.5 < h && h < 77.5),
        _ => Some("Linear"),
    }
}

fn value_2_method(h: f64, c: i32) -> Option<&'static str> {
    match c {
        2 => radial_if((15.0 < h && h < 27.5) || (77.5 < h && h < 80.0)),
        4 => radial_if((12.5 < h && h < 30.0) || (62.5 < h && h < 80.0)),
        6 => radial_if((7.5 < h && h < 22.5) || (62.5 < h && h < 80.0)),
        8 => radial_if((7.5 < h && h < 15.0) || (60.0 < h && h < 80.0)),
        _ if c >= 10 => radial_if(65.0 < h && h < 77.5),
        _ => Some("Linear"),
    }
}

fn value_3_method(h: f64, c: i32) -> Option<&'static str> {
    match c {
        2 => radial_if((10.0 < h && h < 37.5) || (65.0 < h && h < 85.0)),
        4 => radial_if((5.0 < h && h < 37.5) || (55.0 < h && h < 72.5)),
        6 | 8 | 10 => radial_if((7.5 < h && h < 37.5) || (57.5 < h && h < 82.5)),
        _ if c >= 12 => radial_if((7.5 < h && h < 42.5) || (57.5 < h && h < 80.0)),
        _ => Some("Linear"),
    }
}

fn value_4_method(h: f64, c: i32) -> Option<&'static str> {
    match c {
        2 | 4 => radial_if((7.5 < h && h < 42.5) || (57.5 < h && h < 85.0)),
        6 | 8 => radial_if((7.5 < h && h < 40.0) || (57.5 < h && h < 82.5)),
        _ if c >= 10 => radial_if((7.5 < h && h < 40.0) || (57.5 < h && h < 80.0)),
        _ => Some("Linear"),
    }
}

fn value_5_method(h: f64, c: i32) -> Option<&'static str> {
    match c {
        2 => radial_if((5.0 < h && h < 37.5) || (55.0 < h && h < 85.0)),
        4 | 6 | 8 => radial_if((2.5 < h && h < 42.5) || (55.0 < h && h < 85.0)),
        _ if c >= 10 => radial_if((2.5 < h && h < 42.5) || (55.0 < h && h < 82.5)),
        _ => Some("Linear"),
    }
}

fn value_6_method(h: f64, c: i32) -> Option<&'static str> {
    match c {
        2 | 4 => radial_if((5.0 < h && h < 37.5) || (55.0 < h && h < 87.5)),
        6 => radial_if((5.0 < h && h < 42.5) || (57.5 < h && h < 87.5)),
        8 | 10 => radial_if((5.0 < h && h < 42.5) || (60.0 < h && h < 85.0)),
        12 | 14 => radial_if((5.0 < h && h < 42.5) || (60.0 < h && h < 82.5)),
        _ if c >= 16 => radial_if((5.0 < h && h < 42.5) || (60.0 < h && h < 80.0)),
        _ => Some("Linear"),
    }
}

fn value_7_method(h: f64, c: i32) -> Option<&'static str> {
    match c {
        2 | 4 | 6 => radial_if((5.0 < h && h < 42.5) || (60.0 < h && h < 85.0)),
        8 => radial_if((5.0 < h && h < 42.5) || (60.0 < h && h < 82.5)),
        10 => radial_if(
            (30.0 < h && h < 42.5) || (5.0 < h && h < 25.0) || (60.0 < h && h < 82.5),
        ),
        12 => radial_if(
            (30.0 < h && h < 42.5) || (7.5 < h && h < 27.5) || (80.0 < h && h < 82.5),
        ),
        _ if c >= 14 => radial_if(
            (32.5 < h && h < 40.0) || (7.5 < h && h < 15.0) || (80.0 < h && h < 82.5),
        ),
        _ => Some("Linear"),
    }
}

fn value_8_method(h: f64, c: i32) -> Option<&'static str> {
    match c {
        2 | 4 | 6 | 8 | 10 | 12 => {
            radial_if((5.0 < h && h < 40.0) || (60.0 < h && h < 85.0))
        }
        _ if c >= 14 => radial_if(
            (32.5 < h && h < 40.0) || (5.0 < h && h < 15.0) || (60.0 < h && h < 85.0),
        ),
        _ => Some("Linear"),
    }
}

fn value_9_method(h: f64, c: i32) -> Option<&'static str> {
    match c {
        2 | 4 => radial_if((5.0 < h && h < 40.0) || (55.0 < h && h < 80.0)),
        6 | 8 | 10 | 12 | 14 => radial_if(5.0 < h && h < 42.5),
        _ if c >= 16 => radial_if(35.0 < h && h < 42.5),
        _ => Some("Linear"),
    }
}

/// Returns "Radial" if condition is true, otherwise "Linear".
fn radial_if(condition: bool) -> Option<&'static str> {
    if condition { Some("Radial") } else { Some("Linear") }
}
