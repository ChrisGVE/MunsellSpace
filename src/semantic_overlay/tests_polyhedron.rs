//! Tests for polyhedron and coordinate conversion functionality.

use super::*;

// ========================================================================
// Point-in-Polyhedron Tests
// ========================================================================

/// Create a unit cube centered at origin for testing.
fn unit_cube() -> ConvexPolyhedron {
    let vertices = vec![
        (-0.5, -0.5, -0.5),
        (0.5, -0.5, -0.5),
        (0.5, 0.5, -0.5),
        (-0.5, 0.5, -0.5),
        (-0.5, -0.5, 0.5),
        (0.5, -0.5, 0.5),
        (0.5, 0.5, 0.5),
        (-0.5, 0.5, 0.5),
    ];

    let faces = vec![
        (0, 2, 1), (0, 3, 2), // Bottom
        (4, 5, 6), (4, 6, 7), // Top
        (0, 1, 5), (0, 5, 4), // Front
        (2, 3, 7), (2, 7, 6), // Back
        (0, 4, 7), (0, 7, 3), // Left
        (1, 2, 6), (1, 6, 5), // Right
    ];

    ConvexPolyhedron::from_arrays(&vertices, &faces)
}

/// Create a tetrahedron for testing.
fn tetrahedron() -> ConvexPolyhedron {
    let vertices = vec![
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.5, 0.866, 0.0),
        (0.5, 0.289, 0.816),
    ];

    let faces = vec![
        (0, 2, 1), // Bottom
        (0, 1, 3), // Front
        (1, 2, 3), // Right
        (2, 0, 3), // Left
    ];

    ConvexPolyhedron::from_arrays(&vertices, &faces)
}

#[test]
fn test_cube_contains_center() {
    let cube = unit_cube();
    let center = MunsellCartesian::new(0.0, 0.0, 0.0);
    assert!(cube.contains_point(&center));
}

#[test]
fn test_cube_contains_interior_points() {
    let cube = unit_cube();

    let points = vec![
        MunsellCartesian::new(0.1, 0.1, 0.1),
        MunsellCartesian::new(-0.2, 0.3, -0.1),
        MunsellCartesian::new(0.4, -0.4, 0.4),
    ];

    for point in &points {
        assert!(cube.contains_point(point), "Point {:?} should be inside cube", point);
    }
}

#[test]
fn test_cube_excludes_exterior_points() {
    let cube = unit_cube();

    let points = vec![
        MunsellCartesian::new(1.0, 0.0, 0.0),
        MunsellCartesian::new(0.0, 1.0, 0.0),
        MunsellCartesian::new(0.0, 0.0, 1.0),
        MunsellCartesian::new(-1.0, -1.0, -1.0),
    ];

    for point in &points {
        assert!(!cube.contains_point(point), "Point {:?} should be outside cube", point);
    }
}

#[test]
fn test_tetrahedron_contains_centroid() {
    let tet = tetrahedron();
    let centroid = tet.centroid();
    assert!(tet.contains_point(&centroid));
}

#[test]
fn test_tetrahedron_excludes_exterior() {
    let tet = tetrahedron();
    let outside = MunsellCartesian::new(2.0, 2.0, 2.0);
    assert!(!tet.contains_point(&outside));
}

#[test]
fn test_centroid_calculation() {
    let cube = unit_cube();
    let centroid = cube.centroid();

    assert!(centroid.x.abs() < 0.001);
    assert!(centroid.y.abs() < 0.001);
    assert!(centroid.z.abs() < 0.001);
}

#[test]
fn test_point_in_polyhedron_function() {
    let vertices = vec![
        (-1.0, -1.0, -1.0),
        (1.0, -1.0, -1.0),
        (1.0, 1.0, -1.0),
        (-1.0, 1.0, -1.0),
        (-1.0, -1.0, 1.0),
        (1.0, -1.0, 1.0),
        (1.0, 1.0, 1.0),
        (-1.0, 1.0, 1.0),
    ];

    let faces = vec![
        (0, 2, 1), (0, 3, 2),
        (4, 5, 6), (4, 6, 7),
        (0, 1, 5), (0, 5, 4),
        (2, 3, 7), (2, 7, 6),
        (0, 4, 7), (0, 7, 3),
        (1, 2, 6), (1, 6, 5),
    ];

    let inside = MunsellCartesian::new(0.0, 0.0, 0.0);
    let outside = MunsellCartesian::new(5.0, 5.0, 5.0);

    assert!(point_in_polyhedron(&inside, &vertices, &faces));
    assert!(!point_in_polyhedron(&outside, &vertices, &faces));
}

#[test]
fn test_munsell_in_polyhedron() {
    let vertices = vec![
        (5.0, 0.0, 4.0),
        (10.0, 0.0, 4.0),
        (10.0, 5.0, 4.0),
        (5.0, 5.0, 4.0),
        (5.0, 0.0, 6.0),
        (10.0, 0.0, 6.0),
        (10.0, 5.0, 6.0),
        (5.0, 5.0, 6.0),
    ];

    let faces = vec![
        (0, 2, 1), (0, 3, 2),
        (4, 5, 6), (4, 6, 7),
        (0, 1, 5), (0, 5, 4),
        (2, 3, 7), (2, 7, 6),
        (0, 4, 7), (0, 7, 3),
        (1, 2, 6), (1, 6, 5),
    ];

    let inside_color = MunsellSpec::new(2.0, 5.0, 7.0);
    assert!(munsell_in_polyhedron(&inside_color, &vertices, &faces));

    let outside_color = MunsellSpec::new(2.0, 5.0, 1.0);
    assert!(!munsell_in_polyhedron(&outside_color, &vertices, &faces));

    let wrong_value = MunsellSpec::new(2.0, 8.0, 7.0);
    assert!(!munsell_in_polyhedron(&wrong_value, &vertices, &faces));
}

// ========================================================================
// Coordinate Conversion Tests
// ========================================================================

#[test]
fn test_hue_to_number_basic() {
    assert!((parse_hue_to_number("5R").unwrap() - 2.0).abs() < 0.001);
    assert!((parse_hue_to_number("5YR").unwrap() - 6.0).abs() < 0.001);
    assert!((parse_hue_to_number("5Y").unwrap() - 10.0).abs() < 0.001);
    assert!((parse_hue_to_number("5GY").unwrap() - 14.0).abs() < 0.001);
    assert!((parse_hue_to_number("5G").unwrap() - 18.0).abs() < 0.001);
    assert!((parse_hue_to_number("5BG").unwrap() - 22.0).abs() < 0.001);
    assert!((parse_hue_to_number("5B").unwrap() - 26.0).abs() < 0.001);
    assert!((parse_hue_to_number("5PB").unwrap() - 30.0).abs() < 0.001);
    assert!((parse_hue_to_number("5P").unwrap() - 34.0).abs() < 0.001);
    assert!((parse_hue_to_number("5RP").unwrap() - 38.0).abs() < 0.001);
}

#[test]
fn test_hue_to_number_boundaries() {
    assert!((parse_hue_to_number("10R").unwrap() - 4.0).abs() < 0.001);
    assert!((parse_hue_to_number("10YR").unwrap() - 8.0).abs() < 0.001);
    assert!((parse_hue_to_number("10RP").unwrap() - 0.0).abs() < 0.001);
}

#[test]
fn test_hue_to_number_fractional() {
    assert!((parse_hue_to_number("2.5R").unwrap() - 1.0).abs() < 0.001);
    assert!((parse_hue_to_number("7.5R").unwrap() - 3.0).abs() < 0.001);
    assert!((parse_hue_to_number("2.5YR").unwrap() - 5.0).abs() < 0.001);
}

#[test]
fn test_hue_to_number_invalid() {
    assert!(parse_hue_to_number("").is_none());
    assert!(parse_hue_to_number("R").is_none());
    assert!(parse_hue_to_number("11R").is_none());
    assert!(parse_hue_to_number("-1R").is_none());
    assert!(parse_hue_to_number("5X").is_none());
}

#[test]
fn test_hue_number_to_string() {
    let (hue, _) = hue_number_to_string(2.0);
    assert_eq!(hue, "5R");

    let (hue, _) = hue_number_to_string(6.0);
    assert_eq!(hue, "5YR");

    let (hue, _) = hue_number_to_string(1.0);
    assert!(hue.contains("R"));
}

#[test]
fn test_roundtrip_hue_conversion() {
    let test_hues = ["5R", "2.5YR", "7.5BG", "10PB", "5RP"];

    for hue in &test_hues {
        let num = parse_hue_to_number(hue).unwrap();
        let (back, _) = hue_number_to_string(num);
        let num2 = parse_hue_to_number(&back).unwrap();
        assert!(
            (num - num2).abs() < 0.001,
            "Roundtrip failed for {}: {} -> {} -> {}", hue, num, back, num2
        );
    }
}

#[test]
fn test_cartesian_conversion() {
    let spec = MunsellSpec::new(0.0, 5.0, 10.0);
    let cart = spec.to_cartesian();

    assert!((cart.x - 10.0).abs() < 0.001);
    assert!(cart.y.abs() < 0.001);
    assert!((cart.z - 5.0).abs() < 0.001);

    let spec90 = MunsellSpec::new(10.0, 5.0, 10.0);
    let cart90 = spec90.to_cartesian();
    assert!(cart90.x.abs() < 0.001);
    assert!((cart90.y - 10.0).abs() < 0.001);
}

#[test]
fn test_cartesian_roundtrip() {
    let original = MunsellSpec::new(15.0, 6.0, 8.0);
    let cart = original.to_cartesian();
    let recovered = MunsellSpec::from_cartesian(&cart);

    assert!((original.hue_number - recovered.hue_number).abs() < 0.001);
    assert!((original.value - recovered.value).abs() < 0.001);
    assert!((original.chroma - recovered.chroma).abs() < 0.001);
}

#[test]
fn test_neutral_cartesian() {
    let neutral = MunsellSpec::neutral(5.0);
    let cart = neutral.to_cartesian();

    assert!(cart.x.abs() < 0.001);
    assert!(cart.y.abs() < 0.001);
    assert!((cart.z - 5.0).abs() < 0.001);

    let recovered = MunsellSpec::from_cartesian(&cart);
    assert!(recovered.chroma < 0.001);
}

#[test]
fn test_parse_munsell_notation() {
    let spec = parse_munsell_notation("5R 4.0/12.0").unwrap();
    assert!((spec.hue_number - 2.0).abs() < 0.001);
    assert!((spec.value - 4.0).abs() < 0.001);
    assert!((spec.chroma - 12.0).abs() < 0.001);

    let neutral = parse_munsell_notation("N 5.0/").unwrap();
    assert!(neutral.chroma < 0.001);
    assert!((neutral.value - 5.0).abs() < 0.001);
}

#[test]
fn test_to_notation() {
    let spec = MunsellSpec::new(2.0, 4.0, 12.0);
    let notation = spec.to_notation();
    assert!(notation.contains("R"));
    assert!(notation.contains("4.0"));
    assert!(notation.contains("12.0"));

    let neutral = MunsellSpec::neutral(5.0);
    let n_notation = neutral.to_notation();
    assert!(n_notation.starts_with("N"));
}

#[test]
fn test_distance() {
    let p1 = MunsellCartesian::new(0.0, 0.0, 0.0);
    let p2 = MunsellCartesian::new(3.0, 4.0, 0.0);
    assert!((p1.distance(&p2) - 5.0).abs() < 0.001);

    let p3 = MunsellCartesian::new(0.0, 0.0, 5.0);
    assert!((p1.distance(&p3) - 5.0).abs() < 0.001);
}

#[test]
fn test_centore_centroids() {
    let aqua = parse_munsell_notation("7.4BG 6.2/3.4").unwrap();
    assert!((aqua.value - 6.2).abs() < 0.001);
    assert!((aqua.chroma - 3.4).abs() < 0.001);

    let beige = parse_munsell_notation("6.7YR 6.1/3.4").unwrap();
    assert!((beige.value - 6.1).abs() < 0.001);

    let navy = parse_munsell_notation("7.3PB 2.1/3.6").unwrap();
    assert!((navy.value - 2.1).abs() < 0.001);
}
