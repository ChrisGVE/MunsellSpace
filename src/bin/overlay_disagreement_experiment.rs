//! Experiment: Compare ISCC-NBS base colors with Centore's overlay classifications
//!
//! This script analyzes disagreements between the ISCC-NBS color system and
//! Centore's semantic overlay system for the same Munsell coordinates.
//!
//! Run with: cargo run --bin overlay_disagreement_experiment

use munsellspace::{
    IsccNbsClassifier,
    semantic_overlay::hue_number_to_string,
    constants::centore_polyhedra::*,
};

/// Convert Cartesian (x, y, z) to Munsell spec (hue_number, value, chroma)
///
/// The polyhedron vertices use:
/// - x = chroma * cos(theta), where theta = hue_number * 9 degrees
/// - y = chroma * sin(theta)
/// - z = value
fn cartesian_to_munsell_spec(x: f64, y: f64, z: f64) -> (f64, f64, f64) {
    let chroma = (x * x + y * y).sqrt();
    let value = z;

    // Handle achromatic case
    if chroma < 0.01 {
        return (0.0, value, chroma);
    }

    // Get hue angle in radians, then convert to degrees
    let hue_angle_radians = y.atan2(x);
    let hue_angle_degrees = hue_angle_radians.to_degrees();

    // Convert to Centore's 0-40 hue number (hue_number * 9 = degrees)
    // Normalize to positive range
    let hue_number = ((hue_angle_degrees / 9.0) + 40.0) % 40.0;

    (hue_number, value, chroma)
}
use std::collections::HashMap;
use std::fs::File;
use std::io::Write;

/// Extract the base color from an ISCC-NBS color name
/// e.g., "vivid red" -> "red", "light grayish blue" -> "blue"
fn extract_base_color(iscc_name: &str) -> String {
    let name_lower = iscc_name.to_lowercase();

    // List of base colors in ISCC-NBS
    let base_colors = [
        "pink", "red", "orange", "brown", "yellow", "olive",
        "green", "blue", "violet", "purple", "white", "gray", "black"
    ];

    // Find which base color is in the name (check from end)
    for base in &base_colors {
        if name_lower.ends_with(base) || name_lower.contains(&format!(" {}", base)) {
            return base.to_string();
        }
    }

    // Special cases
    if name_lower.contains("yellowish") && name_lower.contains("green") {
        return "green".to_string();
    }
    if name_lower.contains("greenish") && name_lower.contains("yellow") {
        return "yellow".to_string();
    }

    // Return the last word as fallback
    name_lower.split_whitespace().last().unwrap_or("unknown").to_string()
}

/// Check if an overlay name exists in ISCC-NBS (valid for comparison)
fn is_comparable_overlay(overlay_name: &str) -> bool {
    matches!(overlay_name,
        "blue" | "brown" | "gray" | "green" | "orange" |
        "pink" | "purple" | "red" | "white" | "yellow"
    )
}

/// Map overlay names to their ISCC-NBS base color (only for comparable colors)
fn overlay_to_base_color(overlay_name: &str) -> Option<&'static str> {
    match overlay_name {
        // Only the 10 colors that exist in both systems
        "blue" => Some("blue"),
        "brown" => Some("brown"),
        "gray" => Some("gray"),
        "green" => Some("green"),
        "orange" => Some("orange"),
        "pink" => Some("pink"),
        "purple" => Some("purple"),
        "red" => Some("red"),
        "white" => Some("white"),
        "yellow" => Some("yellow"),
        // Non-basic colors have no ISCC-NBS equivalent - not comparable
        _ => None,
    }
}

#[derive(Debug)]
struct DisagreementRecord {
    overlay_name: String,
    munsell_notation: String,
    hue_number: f64,
    value: f64,
    chroma: f64,
    iscc_nbs_full: String,
    iscc_nbs_base: String,
    overlay_expected_base: String,
    disagreement_type: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("=== Overlay vs ISCC-NBS Disagreement Experiment ===\n");

    let classifier = IsccNbsClassifier::new()?;

    // Collect all vertices from all polyhedra
    let polyhedra_data: Vec<(&str, &[(f64, f64, f64)])> = vec![
        ("aqua", &POLYHEDRON_AQUA_VERTICES[..]),
        ("beige", &POLYHEDRON_BEIGE_VERTICES[..]),
        ("coral", &POLYHEDRON_CORAL_VERTICES[..]),
        ("fuchsia", &POLYHEDRON_FUCHSIA_VERTICES[..]),
        ("gold", &POLYHEDRON_GOLD_VERTICES[..]),
        ("lavender", &POLYHEDRON_LAVENDER_VERTICES[..]),
        ("lilac", &POLYHEDRON_LILAC_VERTICES[..]),
        ("magenta", &POLYHEDRON_MAGENTA_VERTICES[..]),
        ("mauve", &POLYHEDRON_MAUVE_VERTICES[..]),
        ("navy", &POLYHEDRON_NAVY_VERTICES[..]),
        ("peach", &POLYHEDRON_PEACH_VERTICES[..]),
        ("rose", &POLYHEDRON_ROSE_VERTICES[..]),
        ("rust", &POLYHEDRON_RUST_VERTICES[..]),
        ("sand", &POLYHEDRON_SAND_VERTICES[..]),
        ("tan", &POLYHEDRON_TAN_VERTICES[..]),
        ("taupe", &POLYHEDRON_TAUPE_VERTICES[..]),
        ("teal", &POLYHEDRON_TEAL_VERTICES[..]),
        ("turquoise", &POLYHEDRON_TURQUOISE_VERTICES[..]),
        ("violet", &POLYHEDRON_VIOLET_VERTICES[..]),
        ("wine", &POLYHEDRON_WINE_VERTICES[..]),
        ("blue", &POLYHEDRON_BLUE_VERTICES[..]),
        ("brown", &POLYHEDRON_BROWN_VERTICES[..]),
        ("gray", &POLYHEDRON_GRAY_VERTICES[..]),
        ("green", &POLYHEDRON_GREEN_VERTICES[..]),
        ("orange", &POLYHEDRON_ORANGE_VERTICES[..]),
        ("pink", &POLYHEDRON_PINK_VERTICES[..]),
        ("purple", &POLYHEDRON_PURPLE_VERTICES[..]),
        ("red", &POLYHEDRON_RED_VERTICES[..]),
        ("white", &POLYHEDRON_WHITE_VERTICES[..]),
        ("yellow", &POLYHEDRON_YELLOW_VERTICES[..]),
    ];

    let mut disagreements: Vec<DisagreementRecord> = Vec::new();
    let mut total_points = 0;
    let mut comparable_points = 0;
    let mut classified_points = 0;
    let mut agreement_count = 0;
    let mut disagreement_count = 0;
    let mut no_iscc_match = 0;
    let mut skipped_non_comparable = 0;

    // Statistics by overlay (only for comparable colors)
    let mut stats_by_overlay: HashMap<String, (usize, usize, usize)> = HashMap::new(); // (total, agree, disagree)

    for (overlay_name, vertices) in &polyhedra_data {
        // Skip non-comparable overlays (those not in ISCC-NBS)
        if !is_comparable_overlay(overlay_name) {
            skipped_non_comparable += vertices.len();
            total_points += vertices.len();
            continue;
        }

        let overlay_expected = overlay_to_base_color(overlay_name).unwrap(); // Safe: we checked is_comparable
        let mut overlay_total = 0;
        let mut overlay_agree = 0;
        let mut overlay_disagree = 0;

        for &(x, y, z) in *vertices {
            total_points += 1;
            comparable_points += 1;
            overlay_total += 1;

            // Convert Cartesian (x, y, z) to Munsell spec
            let (hue_num, value, chroma) = cartesian_to_munsell_spec(x, y, z);

            // Convert hue number to string (returns (notation, family))
            let (hue_notation, _family) = hue_number_to_string(hue_num);

            // Classify with ISCC-NBS
            match classifier.classify_munsell(&hue_notation, value, chroma) {
                Ok(Some(metadata)) => {
                    classified_points += 1;

                    let iscc_base = extract_base_color(&metadata.iscc_nbs_color_name);

                    // Check for disagreement
                    let base_matches = iscc_base == overlay_expected;

                    if base_matches {
                        agreement_count += 1;
                        overlay_agree += 1;
                    } else {
                        disagreement_count += 1;
                        overlay_disagree += 1;

                        let munsell_notation = if chroma < 0.5 {
                            format!("N {:.1}", value)
                        } else {
                            format!("{} {:.1}/{:.1}", hue_notation, value, chroma)
                        };

                        disagreements.push(DisagreementRecord {
                            overlay_name: overlay_name.to_string(),
                            munsell_notation,
                            hue_number: hue_num,
                            value,
                            chroma,
                            iscc_nbs_full: metadata.iscc_nbs_descriptor(),
                            iscc_nbs_base: iscc_base.clone(),
                            overlay_expected_base: overlay_expected.to_string(),
                            disagreement_type: format!("{} vs {}", overlay_expected, iscc_base),
                        });
                    }
                }
                Ok(None) => {
                    no_iscc_match += 1;
                }
                Err(e) => {
                    eprintln!("Error classifying {}: {}", overlay_name, e);
                }
            }
        }

        stats_by_overlay.insert(overlay_name.to_string(), (overlay_total, overlay_agree, overlay_disagree));
    }

    // Print summary
    println!("=== Summary ===");
    println!("Total vertex points in all polyhedra: {}", total_points);
    println!("Skipped (non-comparable, e.g. tan, navy): {}", skipped_non_comparable);
    println!("Comparable points (10 shared colors): {}", comparable_points);
    println!("Successfully classified by ISCC-NBS: {}", classified_points);
    println!("No ISCC-NBS match: {}", no_iscc_match);
    println!();
    println!("Agreements (ISCC-NBS base = overlay name): {}", agreement_count);
    println!("Disagreements (ISCC-NBS base ≠ overlay name): {}", disagreement_count);
    if classified_points > 0 {
        println!("Agreement rate: {:.1}%", 100.0 * agreement_count as f64 / classified_points as f64);
    }
    println!();

    // Print per-overlay statistics
    println!("=== Per-Overlay Statistics ===");
    println!("{:<12} {:>6} {:>6} {:>6} {:>8}", "Overlay", "Total", "Agree", "Disagree", "Rate");
    println!("{}", "-".repeat(50));

    let mut sorted_stats: Vec<_> = stats_by_overlay.iter().collect();
    sorted_stats.sort_by(|a, b| b.1.2.cmp(&a.1.2)); // Sort by disagreements descending

    for (name, (total, agree, disagree)) in sorted_stats {
        let rate = if *total > 0 { 100.0 * *agree as f64 / *total as f64 } else { 0.0 };
        println!("{:<12} {:>6} {:>6} {:>6} {:>7.1}%", name, total, agree, disagree, rate);
    }

    // Write CSV
    let csv_path = "tmp/overlay_disagreements.csv";
    std::fs::create_dir_all("tmp")?;
    let mut csv_file = File::create(csv_path)?;

    writeln!(csv_file, "overlay_name,munsell_notation,hue_number,value,chroma,iscc_nbs_full,iscc_nbs_base,overlay_expected_base,disagreement_type")?;

    for d in &disagreements {
        writeln!(csv_file, "{},{},{:.2},{:.2},{:.2},{},{},{},{}",
            d.overlay_name,
            d.munsell_notation,
            d.hue_number,
            d.value,
            d.chroma,
            d.iscc_nbs_full.replace(",", ";"),
            d.iscc_nbs_base,
            d.overlay_expected_base,
            d.disagreement_type
        )?;
    }

    println!();
    println!("Disagreements written to: {}", csv_path);
    println!("Total disagreement records: {}", disagreements.len());

    // Show sample disagreements
    println!();
    println!("=== Sample Disagreements ===");
    for d in disagreements.iter().take(10) {
        println!("  {} @ {} -> ISCC: {} (base: {}) vs Overlay expects: {}",
            d.overlay_name, d.munsell_notation, d.iscc_nbs_full, d.iscc_nbs_base, d.overlay_expected_base);
    }

    Ok(())
}
