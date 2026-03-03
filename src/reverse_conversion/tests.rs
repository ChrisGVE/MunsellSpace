//! Tests for the reverse conversion pipeline.

use super::*;

#[test]
fn test_parse_munsell_notation() {
    // Test chromatic color
    let spec = parse_munsell_notation("5R 4/14").unwrap();
    assert_eq!(spec.hue, 5.0);
    assert_eq!(spec.family, "R");
    assert_eq!(spec.value, 4.0);
    assert_eq!(spec.chroma, 14.0);

    // Test neutral color (Python format without space)
    let spec = parse_munsell_notation("N5").unwrap();
    assert_eq!(spec.hue, 0.0);
    assert_eq!(spec.family, "N");
    assert_eq!(spec.value, 5.0);
    assert_eq!(spec.chroma, 0.0);

    // Test decimal hue
    let spec = parse_munsell_notation("2.5YR 6/8").unwrap();
    assert_eq!(spec.hue, 2.5);
    assert_eq!(spec.family, "YR");
    assert_eq!(spec.value, 6.0);
    assert_eq!(spec.chroma, 8.0);
}

#[test]
fn test_reverse_conversion_pipeline() {
    let converter = ReverseConverter::new().unwrap();

    // Test with a known red color
    let munsell = MunsellSpecification {
        hue: 5.0,
        family: "R".to_string(),
        value: 4.0,
        chroma: 14.0,
    };

    let colors = converter.munsell_to_all_formats(&munsell).unwrap();

    // Verify all formats are present
    assert_eq!(colors.munsell.family, "R");
    assert!(colors.lab.l > 0.0);
    assert!(colors.hex.starts_with('#'));
    assert_eq!(colors.hex.len(), 7);
    assert!(colors.hsl.h >= 0.0 && colors.hsl.h < 360.0);
    assert!(colors.hsv.v > 0.0);
}

#[test]
fn test_srgb_to_hex() {
    let converter = ReverseConverter::new().unwrap();
    let hex = converter.srgb_to_hex([255, 0, 0]);
    assert_eq!(hex, "#FF0000");

    let hex = converter.srgb_to_hex([0, 255, 255]);
    assert_eq!(hex, "#00FFFF");
}

#[test]
fn test_neutral_color_conversion() {
    let converter = ReverseConverter::new().unwrap();

    let neutral = MunsellSpecification {
        hue: 0.0,
        family: "N".to_string(),
        value: 5.0,
        chroma: 0.0,
    };

    let colors = converter.munsell_to_all_formats(&neutral).unwrap();

    // Neutral colors should have low chroma in HSL/HSV
    assert!(colors.hsl.s < 10.0); // Low saturation
    assert!(colors.hsv.s < 10.0); // Low saturation

    // Should be grayish
    let [r, g, b] = colors.srgb;
    let diff = ((r as i16 - g as i16).abs()
        + (g as i16 - b as i16).abs()
        + (b as i16 - r as i16).abs()) as f64;
    assert!(diff < 50.0); // Colors should be close (grayish)
}

#[test]
fn test_comprehensive_reverse_conversion() {
    let converter = ReverseConverter::new().unwrap();

    // Test a red color
    let red_spec = MunsellSpecification {
        hue: 5.0,
        family: "R".to_string(),
        value: 4.0,
        chroma: 14.0,
    };

    // Test individual methods
    let srgb = converter.munsell_to_srgb(&red_spec).unwrap();
    let hex = converter.munsell_to_hex(&red_spec).unwrap();
    let lab = converter.munsell_to_lab(&red_spec).unwrap();
    let hsl = converter.munsell_to_hsl(&red_spec).unwrap();
    let hsv = converter.munsell_to_hsv(&red_spec).unwrap();

    // All methods should work without error
    assert!(srgb[0] > 0); // Red channel should be present
    assert!(hex.starts_with('#'));
    assert_eq!(hex.len(), 7); // Valid hex format
    assert!(lab.l > 0.0); // Positive lightness
    assert!(hsl.h >= 0.0 && hsl.h < 360.0); // Valid hue range
    assert!(hsv.v > 0.0); // Positive brightness

    // Test comprehensive method
    let colors = converter.munsell_to_all_formats(&red_spec).unwrap();

    // Results should be consistent
    assert_eq!(colors.srgb, srgb);
    assert_eq!(colors.hex, hex);
    assert_eq!(colors.lab.l, lab.l);
    assert_eq!(colors.hsl.h, hsl.h);
    assert_eq!(colors.hsv.v, hsv.v);

    // Verify the original spec is preserved
    assert_eq!(colors.munsell.hue, red_spec.hue);
    assert_eq!(colors.munsell.family, red_spec.family);
    assert_eq!(colors.munsell.value, red_spec.value);
    assert_eq!(colors.munsell.chroma, red_spec.chroma);
}
