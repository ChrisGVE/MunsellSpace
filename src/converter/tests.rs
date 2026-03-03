//! Tests for the MunsellConverter module.

use super::*;

#[test]
fn test_converter_creation() {
    let converter = MunsellConverter::new().unwrap();
    assert!(converter.reference_count() > 0);
}

#[test]
fn test_basic_conversions() {
    let converter = MunsellConverter::new().unwrap();

    let black = converter.srgb_to_munsell([0, 0, 0]).unwrap();
    assert_eq!(black.notation, "N 0.0");
    assert!(black.is_neutral());

    let blue = converter.srgb_to_munsell([0, 68, 119]).unwrap();
    println!("Blue result: {} (expected: 2.9PB 2.8/7.0)", blue.notation);
    assert!(blue.is_chromatic());
    assert!(blue.notation.contains("PB"));
    assert!(blue.value >= 2.5 && blue.value <= 3.5);
}

#[test]
fn test_batch_conversion() {
    let converter = MunsellConverter::new().unwrap();
    let colors = vec![[0, 0, 0], [0, 68, 119], [0, 102, 68]];
    let results = converter.convert_batch(&colors).unwrap();

    assert_eq!(results.len(), 3);
    assert_eq!(results[0].notation, "N 0.0");

    println!("Batch results:");
    println!("  Black: {} (expected: N 0.0)", results[0].notation);
    println!("  Blue: {} (expected: 2.9PB 2.8/7.0)", results[1].notation);
    println!("  Green: {} (expected: 3.4G 3.7/7.0)", results[2].notation);

    assert!(results[1].notation.contains("PB"));
    assert!(results[2].notation.contains("G"));
}

#[test]
fn test_lab_api_entry_point() {
    let converter = MunsellConverter::new().unwrap();

    let rgb = [0, 68, 119];
    let srgb_result = converter.srgb_to_munsell(rgb).unwrap();

    let srgb_norm = [rgb[0] as f64 / 255.0, rgb[1] as f64 / 255.0, rgb[2] as f64 / 255.0];
    let linear_rgb = converter.srgb_to_linear_rgb(srgb_norm);
    let xyz = converter.linear_rgb_to_xyz_d65(linear_rgb);
    let lab = converter.xyz_to_lab_d65(xyz);

    println!("Test Lab coordinates: [{:.3}, {:.3}, {:.3}]", lab[0], lab[1], lab[2]);

    let lab_result = converter.lab_to_munsell(lab).unwrap();

    println!("sRGB->Munsell: {}", srgb_result.notation);
    println!("Lab->Munsell:  {}", lab_result.notation);

    assert_eq!(lab_result.is_chromatic(), srgb_result.is_chromatic());
    assert!(lab_result.notation.contains("PB"));
}

#[test]
fn test_spatial_interpolation_debug() {
    let converter = MunsellConverter::new().unwrap();

    let rgb = [10, 70, 120];

    let srgb_norm = [rgb[0] as f64 / 255.0, rgb[1] as f64 / 255.0, rgb[2] as f64 / 255.0];
    let linear_rgb = converter.srgb_to_linear_rgb(srgb_norm);
    let xyz = converter.linear_rgb_to_xyz_d65(linear_rgb);
    let xyy = converter.xyz_to_xyy(xyz);
    let value = converter.xyz_y_to_munsell_value(xyy[2]);

    println!("Testing spatial interpolation:");
    println!("  xyY: [{:.6}, {:.6}, {:.6}]", xyy[0], xyy[1], xyy[2]);
    println!("  Computed value: {:.3}", value);

    let spatial_result = converter.spatial_interpolation_munsell(xyy, value);

    match spatial_result {
        Some(result) => {
            println!("  Spatial interpolation SUCCESS: {}", result.notation);
            assert!(result.notation.contains("PB"));
        }
        None => {
            println!("  Spatial interpolation FAILED - falling back to mathematical");
            println!("  Total reference points: {}", converter.reference_points.len());

            let nearest = converter.find_nearest_reference_points(xyy, 5);
            println!("  Found {} nearest points:", nearest.len());
            for (i, (distance, point)) in nearest.iter().enumerate() {
                println!("    {}: distance={:.6}, notation={}, value={:.1}",
                         i, distance, point.notation, point.value);
            }
        }
    }
}

#[test]
fn test_accuracy_validation() {
    let converter = MunsellConverter::new().unwrap();
    let stats = converter.validate_regression().unwrap();

    println!("Accuracy Stats:");
    println!("  Total colors: {}", stats.total_colors);
    println!("  Exact matches: {}", stats.exact_matches);
    println!("  Close matches: {}", stats.close_matches);
    println!("  Accuracy: {:.3}%", stats.accuracy_percentage);
    println!("  Close match %: {:.3}%", stats.close_match_percentage);

    let test_colors = [
        ([0, 0, 0], "N 0.0"),
        ([0, 68, 119], "2.9PB 2.8/7.0"),
        ([0, 102, 68], "3.4G 3.7/7.0"),
    ];

    for (rgb, expected) in test_colors.iter() {
        match converter.srgb_to_munsell(*rgb) {
            Ok(result) => {
                println!("RGB{:?} -> {} (expected: {})", rgb, result.notation, expected);
            }
            Err(e) => {
                println!("RGB{:?} -> ERROR: {}", rgb, e);
            }
        }
    }

    let test_rgb = [0, 68, 119];
    println!("\nDetailed conversion trace for RGB{:?}:", test_rgb);

    let srgb_norm = [
        test_rgb[0] as f64 / 255.0,
        test_rgb[1] as f64 / 255.0,
        test_rgb[2] as f64 / 255.0,
    ];
    println!("  1. sRGB normalized: [{:.6}, {:.6}, {:.6}]", srgb_norm[0], srgb_norm[1], srgb_norm[2]);

    let linear_rgb = converter.srgb_to_linear_rgb(srgb_norm);
    println!("  2. Linear RGB: [{:.6}, {:.6}, {:.6}]", linear_rgb[0], linear_rgb[1], linear_rgb[2]);

    let xyz_d65 = converter.linear_rgb_to_xyz_d65(linear_rgb);
    println!("  3. XYZ (D65): [{:.6}, {:.6}, {:.6}]", xyz_d65[0], xyz_d65[1], xyz_d65[2]);

    let xyz_final = xyz_d65;
    println!("  4. XYZ (final): [{:.6}, {:.6}, {:.6}]", xyz_final[0], xyz_final[1], xyz_final[2]);

    let xyy = converter.xyz_to_xyy(xyz_final);
    println!("  5. xyY: [{:.6}, {:.6}, {:.6}]", xyy[0], xyy[1], xyy[2]);

    let is_achromatic = converter.is_achromatic(xyy[0], xyy[1]);
    println!("  6. Is achromatic: {}", is_achromatic);

    if !is_achromatic {
        let white_x = 0.31271;
        let white_y = 0.32902;
        let hue_angle = (xyy[1] - white_y).atan2(xyy[0] - white_x);
        let hue_degrees = hue_angle.to_degrees();
        println!("  7. Hue angle: {:.2}\u{b0}", hue_degrees);

        let munsell_hue = converter.degrees_to_munsell_hue(hue_degrees);
        println!("  8. Munsell hue: {}", munsell_hue);

        let value = converter.xyz_y_to_munsell_value(xyy[2]);
        println!("  9. Munsell value: {:.1}", value);

        let chroma = converter.calculate_munsell_chroma(xyy[0], xyy[1], xyy[2]);
        println!("  10. Munsell chroma: {:.1}", chroma);
    }

    assert!(stats.total_colors > 0);
}

#[test]
fn test_algorithmic_accuracy() {
    let converter = MunsellConverter::new().unwrap();
    let stats = converter.validate_algorithmic_accuracy().unwrap();

    println!("Algorithmic accuracy (bypassing HashMap lookup):");
    println!("  Total: {}", stats.total_colors);
    println!("  Exact: {} ({:.1}%)", stats.exact_matches, stats.accuracy_percentage);
    println!("  Close: {} ({:.1}%)", stats.close_matches, stats.close_match_percentage);

    assert!(
        stats.close_match_percentage > 50.0,
        "Algorithmic path should be at least 50% close-match accurate"
    );
}

#[test]
fn test_regression_is_100_percent() {
    let converter = MunsellConverter::new().unwrap();
    let stats = converter.validate_regression().unwrap();

    assert_eq!(
        stats.exact_matches, stats.total_colors,
        "Regression test should be 100% exact with HashMap lookup"
    );
}

#[test]
fn test_converter_error_handling() {
    let converter = MunsellConverter::new().unwrap();

    assert!(converter.srgb_to_munsell([0, 0, 0]).is_ok());
    assert!(converter.srgb_to_munsell([255, 255, 255]).is_ok());
    assert!(converter.srgb_to_munsell([128, 64, 192]).is_ok());
}

#[test]
fn test_batch_conversion_edge_cases() {
    let converter = MunsellConverter::new().unwrap();

    let empty_colors: Vec<[u8; 3]> = vec![];
    let results = converter.convert_batch(&empty_colors).unwrap();
    assert_eq!(results.len(), 0);

    let single_color = vec![[255, 0, 0]];
    let results = converter.convert_batch(&single_color).unwrap();
    assert_eq!(results.len(), 1);

    let repeated_colors = vec![[0, 0, 0]; 100];
    let results = converter.convert_batch(&repeated_colors).unwrap();
    assert_eq!(results.len(), 100);
    for result in &results {
        assert_eq!(result.notation, "N 0.0");
    }
}

#[test]
fn test_converter_reference_data_access() {
    let converter = MunsellConverter::new().unwrap();

    let count = converter.reference_count();
    assert!(count > 4000);
    assert!(count < 5000);

    let points_count = converter.reference_points.len();
    assert!(points_count > 4000);
    assert!(points_count < 5000);
}

#[test]
fn test_lab_to_munsell_conversion() {
    let converter = MunsellConverter::new().unwrap();

    let white_lab = [100.0, 0.0, 0.0];
    let result = converter.lab_to_munsell(white_lab);
    assert!(result.is_ok());
    let white_munsell = result.unwrap();
    assert!(white_munsell.is_neutral() || white_munsell.value > 9.0);

    let black_lab = [0.0, 0.0, 0.0];
    let result = converter.lab_to_munsell(black_lab);
    assert!(result.is_ok());
    let black_munsell = result.unwrap();
    assert!(black_munsell.is_neutral() || black_munsell.value < 1.0);

    let red_lab = [50.0, 70.0, 50.0];
    let result = converter.lab_to_munsell(red_lab);
    assert!(result.is_ok());
    let red_munsell = result.unwrap();
    println!("Red Lab->Munsell: {}", red_munsell.notation);
}

#[test]
fn test_edge_case_colors() {
    let converter = MunsellConverter::new().unwrap();

    let red = converter.srgb_to_munsell([255, 0, 0]).unwrap();
    println!("Pure red: {}", red.notation);
    assert!(red.is_chromatic());

    let green = converter.srgb_to_munsell([0, 255, 0]).unwrap();
    println!("Pure green: {}", green.notation);
    assert!(green.is_chromatic());

    let blue = converter.srgb_to_munsell([0, 0, 255]).unwrap();
    println!("Pure blue: {}", blue.notation);
    assert!(blue.is_chromatic());

    let yellow = converter.srgb_to_munsell([255, 255, 0]).unwrap();
    println!("Pure yellow: {}", yellow.notation);
    assert!(yellow.is_chromatic());

    let cyan = converter.srgb_to_munsell([0, 255, 255]).unwrap();
    println!("Pure cyan: {}", cyan.notation);
    assert!(cyan.is_chromatic());

    let magenta = converter.srgb_to_munsell([255, 0, 255]).unwrap();
    println!("Pure magenta: {}", magenta.notation);
    assert!(magenta.is_chromatic());

    for gray_level in [0, 64, 128, 192, 255] {
        let gray = converter.srgb_to_munsell([gray_level, gray_level, gray_level]).unwrap();
        println!("Gray {}: {}", gray_level, gray.notation);
        if gray_level == 0 {
            assert_eq!(gray.notation, "N 0.0");
        }
    }
}

#[test]
fn test_color_space_conversion_functions() {
    let converter = MunsellConverter::new().unwrap();

    let srgb = [0.5, 0.25, 0.75];
    let linear = converter.srgb_to_linear_rgb(srgb);
    assert!(linear[0] > 0.0 && linear[0] < 1.0);
    assert!(linear[1] > 0.0 && linear[1] < 1.0);
    assert!(linear[2] > 0.0 && linear[2] < 1.0);

    let xyz = converter.linear_rgb_to_xyz_d65(linear);
    assert!(xyz[0] >= 0.0);
    assert!(xyz[1] >= 0.0);
    assert!(xyz[2] >= 0.0);

    let xyy = converter.xyz_to_xyy(xyz);
    assert!(xyy[0] >= 0.0 && xyy[0] <= 1.0);
    assert!(xyy[1] >= 0.0 && xyy[1] <= 1.0);
    assert!(xyy[2] >= 0.0);

    let lab = converter.xyz_to_lab_d65(xyz);
    assert!(lab[0] >= 0.0 && lab[0] <= 100.0);
}

#[test]
fn test_munsell_calculation_functions() {
    let converter = MunsellConverter::new().unwrap();

    let y_values = [0.0, 0.18, 0.5, 1.0];
    for y in y_values {
        let value = converter.xyz_y_to_munsell_value(y);
        assert!(value >= 0.0 && value <= 10.0);
    }

    let white_x = 0.31271;
    let white_y = 0.32902;
    assert!(converter.is_achromatic(white_x, white_y));
    assert!(!converter.is_achromatic(0.5, 0.3));

    let chroma = converter.calculate_munsell_chroma(0.4, 0.3, 0.5);
    assert!(chroma >= 0.0);
}

#[test]
fn test_hue_angle_calculations() {
    let converter = MunsellConverter::new().unwrap();

    let test_angles = [0.0, 90.0, 180.0, 270.0, 360.0];
    for angle in test_angles {
        let hue = converter.degrees_to_munsell_hue(angle);
        println!("Angle {}\u{b0} -> Hue {}", angle, hue);
        assert!(!hue.is_empty());

        let hue_families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
        let contains_valid_family = hue_families.iter().any(|&family| hue.contains(family));
        assert!(contains_valid_family, "Hue '{}' doesn't contain valid family", hue);
    }
}

#[test]
fn test_spatial_interpolation() {
    let converter = MunsellConverter::new().unwrap();

    let test_xyy = [0.31271, 0.32902, 0.18];
    let nearest = converter.find_nearest_reference_points(test_xyy, 5);
    assert!(nearest.len() <= 5);
    assert!(!nearest.is_empty());

    for (distance, _point) in &nearest {
        assert!(*distance >= 0.0);
        assert!(*distance < 1.0);
    }

    let value = converter.xyz_y_to_munsell_value(test_xyy[2]);
    let result = converter.spatial_interpolation_munsell(test_xyy, value);
    if let Some(munsell) = result {
        println!("Spatial interpolation result: {}", munsell.notation);
        assert!(!munsell.notation.is_empty());
    }
}

#[test]
fn test_reference_lookup() {
    let converter = MunsellConverter::new().unwrap();

    let black = converter.srgb_to_munsell([0, 0, 0]).unwrap();
    assert_eq!(black.notation, "N 0.0");

    let test_colors = [
        [0, 0, 0],
    ];

    for rgb in test_colors {
        let result = converter.srgb_to_munsell(rgb);
        assert!(result.is_ok(), "Failed to convert RGB {:?}", rgb);
    }
}

#[test]
fn test_converter_consistency() {
    let converter = MunsellConverter::new().unwrap();

    let test_color = [128, 64, 192];
    let result1 = converter.srgb_to_munsell(test_color).unwrap();
    let result2 = converter.srgb_to_munsell(test_color).unwrap();
    assert_eq!(result1.notation, result2.notation);

    let srgb_result = converter.srgb_to_munsell(test_color).unwrap();

    let srgb_norm = [
        test_color[0] as f64 / 255.0,
        test_color[1] as f64 / 255.0,
        test_color[2] as f64 / 255.0,
    ];
    let linear_rgb = converter.srgb_to_linear_rgb(srgb_norm);
    let xyz = converter.linear_rgb_to_xyz_d65(linear_rgb);
    let lab = converter.xyz_to_lab_d65(xyz);
    let lab_result = converter.lab_to_munsell(lab).unwrap();

    assert_eq!(srgb_result.is_chromatic(), lab_result.is_chromatic());

    println!("sRGB->Munsell: {}", srgb_result.notation);
    println!("Lab->Munsell:  {}", lab_result.notation);
}

#[test]
#[allow(deprecated)]
fn test_srgb_to_color_name_delegates_to_iscc_classifier() {
    let converter = MunsellConverter::new().unwrap();

    let result = converter.srgb_to_color_name([255, 0, 0]);
    assert!(result.is_ok(), "srgb_to_color_name should succeed for pure red");
    let name = result.unwrap();
    assert!(
        name.color_name.to_lowercase().contains("red"),
        "Expected red, got: {}",
        name.color_name
    );
    assert!(
        !name.descriptor.is_empty(),
        "Descriptor should not be empty"
    );

    let gray_result = converter.srgb_to_color_name([128, 128, 128]);
    if let Ok(gray_name) = gray_result {
        assert!(
            gray_name.color_name.to_lowercase().contains("gray")
                || gray_name.color_name.to_lowercase().contains("grey"),
            "Expected gray, got: {}",
            gray_name.color_name
        );
    }
}

#[test]
#[allow(deprecated)]
fn test_munsell_to_iscc_nbs_name_delegates_to_iscc_classifier() {
    let converter = MunsellConverter::new().unwrap();

    let munsell = MunsellColor::from_notation("5R 4.0/14.0").unwrap();
    let result = converter.munsell_to_iscc_nbs_name(&munsell);
    assert!(
        result.is_ok(),
        "munsell_to_iscc_nbs_name should succeed for 5R 4/14"
    );
    let name = result.unwrap();
    assert!(
        name.color_name.to_lowercase().contains("red"),
        "Expected red, got: {}",
        name.color_name
    );
}
