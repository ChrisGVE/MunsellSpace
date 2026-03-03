//! Tests for munsell_color_science module.

use super::*;

#[test]
fn test_python_functions_exact_match() {
    assert!((hue_to_astm_hue(5.0, 1) - 65.0).abs() < 1e-10);
    assert!((hue_to_astm_hue(10.0, 1) - 70.0).abs() < 1e-10);
    assert!((hue_to_astm_hue(1.0, 2) - 51.0).abs() < 1e-10);

    let angle1 = hue_to_hue_angle(5.0, 1);
    let angle2 = hue_to_hue_angle(5.0, 2);
    assert!((angle1 - 225.0).abs() < 1e-10);
    assert!((angle2 - 160.0).abs() < 1e-10);

    let boundary1 = hue_to_astm_hue(0.1, 1);
    let boundary2 = hue_to_astm_hue(9.9, 1);
    assert!(boundary1 >= 0.0 && boundary1 <= 100.0);
    assert!(boundary2 >= 0.0 && boundary2 <= 100.0);
}
