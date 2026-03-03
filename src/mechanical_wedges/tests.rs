//! Tests for the mechanical wedge system.

use super::*;

#[test]
fn test_hue_sequence_creation() {
    let sequence = MechanicalWedgeSystem::create_reference_hue_sequence();

    // Should have exactly 100 hues (10 families x 10 hues)
    assert_eq!(sequence.len(), 100);

    // First few should be R family
    assert_eq!(sequence[0], "1R");
    assert_eq!(sequence[1], "2R");
    assert_eq!(sequence[9], "10R");

    // Then YR family
    assert_eq!(sequence[10], "1YR");
    assert_eq!(sequence[19], "10YR");

    // Last should be 10RP
    assert_eq!(sequence[99], "10RP");
}

#[test]
fn test_wedge_container_creation() {
    let system = MechanicalWedgeSystem::new();

    // Should have exactly 100 wedge containers
    assert_eq!(system.wedge_containers.len(), 100);

    // Should have proper wedge keys
    assert!(system.wedge_containers.contains_key("1R\u{2192}2R"));
    assert!(system.wedge_containers.contains_key("10R\u{2192}1YR"));
    assert!(system.wedge_containers.contains_key("10RP\u{2192}1R")); // Wraparound
}

#[test]
fn test_hue_parsing() {
    let system = MechanicalWedgeSystem::new();

    // Test standard hues
    let (num, family) = system.parse_hue("5R").unwrap();
    assert_eq!(num, 5.0);
    assert_eq!(family, "R");

    // Test fractional hues
    let (num, family) = system.parse_hue("4.5YR").unwrap();
    assert_eq!(num, 4.5);
    assert_eq!(family, "YR");

    // Test two-letter families
    let (num, family) = system.parse_hue("7PB").unwrap();
    assert_eq!(num, 7.0);
    assert_eq!(family, "PB");
}

#[test]
fn test_containing_wedge_range_based_rules() {
    let system = MechanicalWedgeSystem::new();

    // Range-based interpretation: 1R = [0-1], 2R = (1-2], etc.

    // Values in [0, 1] belong to 1R wedge
    assert_eq!(system.find_containing_wedge("0.0R"), Some("1R\u{2192}2R".to_string()));
    assert_eq!(system.find_containing_wedge("0.5R"), Some("1R\u{2192}2R".to_string()));
    assert_eq!(system.find_containing_wedge("1.0R"), Some("1R\u{2192}2R".to_string()));

    // Values in (1, 2] belong to 2R wedge
    assert_eq!(system.find_containing_wedge("1.1R"), Some("2R\u{2192}3R".to_string()));
    assert_eq!(system.find_containing_wedge("1.5R"), Some("2R\u{2192}3R".to_string()));
    assert_eq!(system.find_containing_wedge("2.0R"), Some("2R\u{2192}3R".to_string()));

    // Values in (4, 5] belong to 5R wedge
    assert_eq!(system.find_containing_wedge("4.5R"), Some("5R\u{2192}6R".to_string()));

    // Values in (9, 10] belong to 10R wedge
    assert_eq!(system.find_containing_wedge("9.5R"), Some("10R\u{2192}1YR".to_string()));
    assert_eq!(system.find_containing_wedge("10.0R"), Some("10R\u{2192}1YR".to_string()));

    // Test different families
    assert_eq!(system.find_containing_wedge("7.2YR"), Some("8YR\u{2192}9YR".to_string()));

    // Test wraparound: values >= 10 should wrap to [0, 1] range
    assert_eq!(system.find_containing_wedge("10.5R"), Some("1R\u{2192}2R".to_string()));
    assert_eq!(system.find_containing_wedge("11.0R"), Some("1R\u{2192}2R".to_string()));
}
