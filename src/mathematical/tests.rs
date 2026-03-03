//! Tests for the mathematical Munsell converter.

use super::*;

#[test]
fn test_mathematical_converter_creation() {
    let converter = MathematicalMunsellConverter::new().unwrap();
    assert_eq!(converter.renotation_data.len(), 4995);
}

#[test]
fn test_srgb_to_xyy_conversion() {
    let converter = MathematicalMunsellConverter::new().unwrap();

    // Test pure red
    let xyy = converter.srgb_to_xyy([255, 0, 0]).unwrap();
    assert!(xyy.x > 0.6); // Red should have high x chromaticity
    assert!(xyy.y > 0.3 && xyy.y < 0.4); // Reasonable y chromaticity
    assert!(xyy.y_luminance > 0.2 && xyy.y_luminance < 0.3); // Reasonable luminance
}

#[test]
fn test_astm_polynomial() {
    let converter = MathematicalMunsellConverter::new().unwrap();

    // Test known values
    assert!((converter.astm_polynomial(0.0) - 0.0).abs() < 1e-10);
    assert!(converter.astm_polynomial(5.0) > 0.1); // Should be positive

    // The ASTM polynomial gives Y values on a 0-100 scale
    // At V=10.0, it should give the maximum reflectance
    assert!(converter.astm_polynomial(10.0) > 0.9); // Should be close to but possibly > 1.0
}

#[test]
fn test_luminance_to_munsell_value() {
    let converter = MathematicalMunsellConverter::new().unwrap();

    // Test edge cases
    assert!((converter.luminance_to_munsell_value(0.0).unwrap() - 0.0).abs() < 1e-10);
    assert!((converter.luminance_to_munsell_value(1.0).unwrap() - 10.0).abs() < 1e-10);

    // Test round-trip consistency
    let test_value = 5.0;
    let luminance = converter.munsell_value_to_luminance(test_value).unwrap();
    let recovered_value = converter.luminance_to_munsell_value(luminance).unwrap();
    assert!((recovered_value - test_value).abs() < 1e-6);
}

#[test]
fn test_achromatic_detection() {
    let converter = MathematicalMunsellConverter::new().unwrap();

    // Test Illuminant C coordinates (should be achromatic)
    assert!(converter.is_achromatic(ILLUMINANT_C[0], ILLUMINANT_C[1]));

    // Test clearly chromatic coordinates
    assert!(!converter.is_achromatic(0.7, 0.3)); // Red region
    assert!(!converter.is_achromatic(0.3, 0.6)); // Green region
}

#[test]
fn test_hue_string_parsing() {
    let converter = MathematicalMunsellConverter::new().unwrap();

    let (hue, family) = converter.parse_hue_string("5R").unwrap();
    assert_eq!(hue, 5.0);
    assert_eq!(family, "R");

    let (hue, family) = converter.parse_hue_string("2.5GY").unwrap();
    assert_eq!(hue, 2.5);
    assert_eq!(family, "GY");
}

#[test]
fn test_munsell_notation_formatting() {
    let converter = MathematicalMunsellConverter::new().unwrap();

    // Test neutral color
    let neutral = MunsellSpecification {
        hue: 0.0,
        family: "N".to_string(),
        value: 5.0,
        chroma: 0.0,
    };
    assert_eq!(converter.format_munsell_notation(&neutral), "N 5.0");

    // Test chromatic color
    let chromatic = MunsellSpecification {
        hue: 5.0,
        family: "R".to_string(),
        value: 4.0,
        chroma: 12.0,
    };
    assert_eq!(converter.format_munsell_notation(&chromatic), "5.0R 4.0/12.0");
}

#[test]
fn test_black_color_conversion() {
    let converter = MathematicalMunsellConverter::new().unwrap();

    // Test pure black
    let munsell = converter.srgb_to_munsell([0, 0, 0]).unwrap();

    assert!(munsell.value < 1.0); // Should be very dark
    assert!(munsell.chroma < 1.0); // Should have very low chroma
}
