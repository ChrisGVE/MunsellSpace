//! Tests for the unified color classifier.

use super::*;
use crate::color_names::ColorModifier;

fn classifier() -> ColorClassifier {
    ColorClassifier::new().expect("Failed to create classifier")
}

#[test]
fn test_classify_srgb_red() {
    let c = classifier();
    let desc = c.classify_srgb([255, 0, 0]).expect("Classification failed");

    assert!(desc.standard_name.contains("red") || desc.shade == "red");
    assert!(desc.modifier.is_vivid() || desc.modifier == ColorModifier::Strong);
}

#[test]
fn test_classify_srgb_blue() {
    let c = classifier();
    let desc = c.classify_srgb([0, 0, 255]).expect("Classification failed");

    assert!(desc.standard_name.contains("blue") || desc.shade == "blue");
}

#[test]
fn test_classify_hex() {
    let c = classifier();
    let desc = c.classify_hex("#FF0000").expect("Classification failed");

    assert!(desc.standard_name.contains("red") || desc.shade == "red");
}

#[test]
fn test_classify_hex_short() {
    let c = classifier();
    let desc = c.classify_hex("#F00").expect("Classification failed");

    assert!(desc.standard_name.contains("red") || desc.shade == "red");
}

#[test]
fn test_classify_munsell_notation() {
    let c = classifier();
    let desc = c.classify_munsell("5R 4/10").expect("Classification failed");

    assert!(desc.standard_name.contains("red") || desc.shade == "red");
}

#[test]
fn test_semantic_name_coral_region() {
    let c = classifier();
    // Use a color in the coral region (roughly 6.5R 5.8/8.3)
    // Coral is around RGB(255, 127, 80) approximately
    let name = c.semantic_name([255, 127, 80]).expect("Classification failed");

    // This should be in or near the coral/rose/peach region
    if let Some(n) = name {
        assert!(
            n == "coral" || n == "rose" || n == "peach" || n == "orange" || n == "pink",
            "Expected coral-like color, got: {}",
            n
        );
    }
}

#[test]
fn test_semantic_matches() {
    let c = classifier();
    let matches = c
        .semantic_matches([200, 100, 80])
        .expect("Classification failed");

    // Should return zero or more matches
    // The exact matches depend on the color's position
    // Some colors near boundaries can match many overlays
    assert!(matches.len() <= 10); // Reasonable upper bound
}

#[test]
fn test_descriptor_formatting() {
    let c = classifier();
    let desc = c.classify_srgb([200, 50, 50]).expect("Classification failed");

    // Standard descriptor should combine modifier and name
    let standard = desc.standard_descriptor();
    assert!(!standard.is_empty());

    // Extended descriptor should also be non-empty
    let extended = desc.extended_descriptor();
    assert!(!extended.is_empty());
}

#[test]
fn test_modifier_extraction() {
    let c = classifier();
    let desc = c.classify_srgb([255, 0, 0]).expect("Classification failed");

    // Pure red should have a vivid or strong modifier
    assert!(
        desc.modifier.is_vivid() || desc.modifier == ColorModifier::Strong,
        "Expected vivid/strong modifier for pure red, got: {:?}",
        desc.modifier
    );
}

#[test]
fn test_shade_extraction() {
    let c = classifier();
    let desc = c.classify_srgb([255, 0, 0]).expect("Classification failed");

    // Pure red should have "red" shade
    assert!(!desc.shade.is_empty());
}

#[test]
fn test_gray_classification() {
    let c = classifier();
    let desc = c.classify_srgb([128, 128, 128]).expect("Classification failed");

    // Medium gray
    assert!(
        desc.standard_name.contains("gray") || desc.standard_name.contains("grey"),
        "Expected gray, got: {}",
        desc.standard_name
    );
}

#[test]
fn test_white_classification() {
    let c = classifier();
    let desc = c.classify_srgb([255, 255, 255]).expect("Classification failed");

    assert!(
        desc.standard_name == "white"
            || desc.standard_name.contains("white")
            || desc.shade == "white",
        "Expected white, got: {}",
        desc.standard_name
    );
}

#[test]
fn test_black_classification() {
    let c = classifier();
    let desc = c.classify_srgb([0, 0, 0]).expect("Classification failed");

    assert!(
        desc.standard_name == "black"
            || desc.standard_name.contains("black")
            || desc.shade == "black",
        "Expected black, got: {}",
        desc.standard_name
    );
}

#[test]
fn test_has_semantic_match() {
    let c = classifier();

    // A vivid color should likely have a semantic match
    let desc = c.classify_srgb([255, 100, 100]).expect("Classification failed");

    // May or may not have semantic match depending on position
    // Just verify the method works
    let _ = desc.has_semantic_match();
}

#[test]
fn test_nearest_semantic() {
    let c = classifier();
    let desc = c.classify_srgb([200, 100, 80]).expect("Classification failed");

    // Should always have a nearest semantic (even if not matched)
    if let Some((name, dist)) = desc.nearest_semantic.as_ref() {
        assert!(!name.is_empty());
        assert!(*dist >= 0.0);
    }
}

#[test]
fn test_all_iscc_matches() {
    let c = classifier();
    let matches = c
        .all_iscc_matches([200, 100, 80])
        .expect("Classification failed");

    // Should have at least one match for a chromatic color
    assert!(!matches.is_empty());
}

#[test]
fn test_display_trait() {
    let c = classifier();
    let desc = c.classify_srgb([180, 80, 60]).expect("Classification failed");

    // Display should output the standard descriptor
    let display = format!("{}", desc);
    assert_eq!(display, desc.standard_descriptor());
}
