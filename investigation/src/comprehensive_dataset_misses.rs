//! Comprehensive Conversion Dataset - Mismatches Analysis
//! 
//! Rust-only ISCC-NBS classification analysis:
//! - ISCC-NBS Descriptor Generation: Use iscc_nbs_descriptor() accessor from classification results  
//! - Unknown Classifications: Track and investigate why colors return "Unknown"
//! - Report Structure: Clear separation of datasets with proper accuracy calculation
//! - Distance Calculation: Show shortest distance to correct polygon in Value/Chroma coordinates

use munsellspace::iscc::ISCC_NBS_Classifier as IsccNbsClassifier;
use munsellspace::mathematical::{
    MathematicalMunsellConverter,
    Illuminant as MathIlluminant,
    ChromaticAdaptation as MathChromaticAdaptation
};
use std::collections::HashMap;
use std::fmt::Write;
use std::fs;
use csv::ReaderBuilder;
use serde::Deserialize;
use geo::prelude::*;
use geo::{Point, LineString, Polygon};
use geo::algorithm::euclidean_distance::EuclideanDistance;

#[derive(Debug, Deserialize, Clone)]
struct W3IsccColor {
    #[serde(rename = "sRGB ")]
    srgb: String,
    #[serde(rename = "ISCC-NBS Name")]
    iscc_nbs_color_name: String,
    #[serde(rename = " modifier ")]
    iscc_nbs_modifier: String,
    #[serde(rename = "color ")]
    revised_color_name: String,
}

#[derive(Debug, Deserialize, Clone)]
struct CentoreIsccColor {
    number: u16,
    #[serde(rename = "name")]
    iscc_nbs_color_name: String,
    r: u8,
    g: u8,
    b: u8,
}

#[derive(Debug, Clone)]
struct TestResult {
    rgb: [u8; 3],
    illuminant: String,
    expected_name: String,
    munsell_notation: String,
    rust_iscc: String,
    rust_match: bool,
    rust_unknown: bool,
}

#[derive(Debug, Default)]
struct Statistics {
    total_unique_colors: usize,
    
    // Per-illuminant tracking
    rust_matches: HashMap<String, usize>,
    rust_unknowns: HashMap<String, usize>,
}

/// Helper function to parse Munsell notation into hue, value, chroma
fn parse_munsell_notation(notation: &str) -> Option<(String, f64, f64)> {
    let notation = notation.trim();
    
    // Handle neutral colors with all formats:
    // "N3.6", "N 3.6", "N3.6/", "N 3.6/", "N3.6/0", "N 3.6/0", etc.
    // Also "0N3.6", "0N 3.6", "0.0N3.6", "0.0N 3.6", etc.
    if notation.contains('N') {
        // Find the position of 'N'
        if let Some(n_pos) = notation.find('N') {
            // Check if what comes before N is numeric or empty
            let prefix = &notation[..n_pos];
            if prefix.is_empty() || prefix.chars().all(|c| c.is_ascii_digit() || c == '.') {
                // This is a neutral color
                let after_n = &notation[n_pos + 1..].trim();
                
                // Parse value and optional chroma
                let (value_str, chroma_str) = if let Some(slash_pos) = after_n.find('/') {
                    (&after_n[..slash_pos].trim(), after_n[slash_pos + 1..].trim())
                } else {
                    (after_n, "0")
                };
                
                if let Ok(value) = value_str.parse::<f64>() {
                    let chroma = chroma_str.parse::<f64>().unwrap_or(0.0);
                    return Some(("N".to_string(), value, chroma));
                }
            }
        }
    }
    
    // Parse regular chromatic Munsell notation
    // Try to find where the hue ends and value begins
    // Hue format: number + letters (e.g., "5R", "2.5YR", "10RP")
    // Look for the last letter that's part of the hue family
    
    let mut hue_end = 0;
    let mut found_letter = false;
    for (i, c) in notation.char_indices() {
        if c.is_ascii_alphabetic() && c != 'N' {
            found_letter = true;
            hue_end = i + c.len_utf8();
        } else if found_letter && (c.is_ascii_digit() || c == '.' || c == '/' || c.is_whitespace()) {
            break;
        }
    }
    
    if hue_end == 0 {
        return None;
    }
    
    let hue = notation[..hue_end].to_string();
    let value_chroma = notation[hue_end..].trim();
    
    // Parse value/chroma part
    let vc_parts: Vec<&str> = value_chroma.split('/').collect();
    if vc_parts.is_empty() {
        return None;
    }
    
    let value = vc_parts[0].trim().parse::<f64>().ok()?;
    let chroma = if vc_parts.len() > 1 {
        vc_parts[1].trim().parse::<f64>().ok()?
    } else {
        0.0
    };
    
    Some((hue, value, chroma))
}


/// Calculate distance to the correct polygon for the expected color
fn calculate_distance_to_correct_polygon(
    rust_munsell: &str,
    expected_name: &str,
    classifier: &IsccNbsClassifier
) -> String {
    // Parse the Rust Munsell notation
    let (rust_hue, rust_value, rust_chroma) = match parse_munsell_notation(rust_munsell) {
        Some(parsed) => parsed,
        None => return String::new(),
    };
    
    // Handle neutral colors
    if rust_hue == "N" {
        return String::new();
    }
    
    // Get the polygon for the expected descriptor in the same wedge
    let polygon = match classifier.get_polygon_in_wedge(&rust_hue, expected_name) {
        Some(p) => p,
        None => return String::new(), // No polygon found in this wedge for expected color
    };
    
    // Calculate the distance from the point to the polygon
    let (value_dist, chroma_dist) = calculate_polygon_distance(
        rust_value,
        rust_chroma,
        &polygon.polygon
    );
    
    // Format the result - show signed distances
    if value_dist.abs() < 0.01 && chroma_dist.abs() < 0.01 {
        "(0.0, 0.0)".to_string() // Point is inside or on the boundary
    } else {
        format!("({:+.1}, {:+.1})", value_dist, chroma_dist)
    }
}

/// Calculate the shortest distance from a point to a polygon boundary
/// Returns (value_distance, chroma_distance) as signed values
fn calculate_polygon_distance(
    point_value: f64, 
    point_chroma: f64,
    target_polygon: &Polygon<f64>
) -> (f64, f64) {
    let test_point = Point::new(point_chroma, point_value); // Note: geo uses (x,y) = (chroma, value)
    
    // Check if point is inside polygon
    if target_polygon.contains(&test_point) {
        return (0.0, 0.0); // Already inside
    }
    
    // Find the closest point on the polygon boundary
    let exterior = target_polygon.exterior();
    let mut min_distance = f64::MAX;
    let mut closest_point = test_point;
    
    // Check each edge of the polygon
    for line in exterior.lines() {
        // Get the closest point on this line segment to our test point
        let line_string = LineString::from(vec![line.start, line.end]);
        
        // Calculate point-to-line distance
        for coord in line_string.coords() {
            let boundary_point = Point::new(coord.x, coord.y);
            let dist = EuclideanDistance::euclidean_distance(&test_point, &boundary_point);
            
            if dist < min_distance {
                min_distance = dist;
                closest_point = boundary_point;
            }
        }
        
        // Also check projection onto line segment
        let start = Point::new(line.start.x, line.start.y);
        let end = Point::new(line.end.x, line.end.y);
        
        // Vector from start to end
        let dx = end.x() - start.x();
        let dy = end.y() - start.y();
        
        // Vector from start to test point
        let px = test_point.x() - start.x();
        let py = test_point.y() - start.y();
        
        // Project test point onto line
        let dot = px * dx + py * dy;
        let len_sq = dx * dx + dy * dy;
        
        if len_sq > 0.0 {
            let t = (dot / len_sq).max(0.0).min(1.0);
            let projected = Point::new(
                start.x() + t * dx,
                start.y() + t * dy
            );
            
            let dist = EuclideanDistance::euclidean_distance(&test_point, &projected);
            if dist < min_distance {
                min_distance = dist;
                closest_point = projected;
            }
        }
    }
    
    // Return signed distances (closest_point - test_point)
    let chroma_dist = closest_point.x() - test_point.x();
    let value_dist = closest_point.y() - test_point.y();
    
    (value_dist, chroma_dist)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 Generating Comprehensive Conversion Dataset - Mismatches Analysis");
    println!("====================================================================");
    println!("Rust-only ISCC-NBS classification analysis:");
    println!("- ISCC-NBS Generation: Use ISCC-NBS descriptors for consistency"); 
    println!("- Unknown Classifications: Track and investigate causes");
    println!();
    
    // Load datasets
    let w3_colors = load_w3_dataset()?;
    let centore_colors = load_centore_dataset()?;
    
    println!("📊 Loaded {} W3 colors and {} Centore colors", w3_colors.len(), centore_colors.len());
    
    // Test configurations - XYZScaling only, with C/D65/F7
    let configurations = vec![
        (MathIlluminant::C, "C"),
        (MathIlluminant::D65, "D65"),
        (MathIlluminant::F7, "F7"),
    ];
    
    // Initialize classifier
    let classifier = IsccNbsClassifier::new()?;
    
    let mut all_test_data = Vec::new();
    
    // Collect all test combinations
    // W3 dataset - only with Illuminant C
    for color in &w3_colors {
        let rgb = parse_rgb(&color.srgb)?;
        let id = format!("W3_C_{}", color.srgb.trim());
        
        // Use the ISCC-NBS color name directly - it's already the correct descriptor
        let expected_name = color.iscc_nbs_color_name.clone();
        all_test_data.push((id, rgb, "C".to_string(), expected_name, "W3"));
    }
    
    // Centore dataset - only with Illuminant D65
    for color in &centore_colors {
        let rgb = [color.r, color.g, color.b];
        let id = format!("Centore_D65_{}", color.number);
        all_test_data.push((id, rgb, "D65".to_string(), color.iscc_nbs_color_name.clone(), "Centore"));
    }

    // Analyze results with comprehensive tracking
    let mut w3_stats = Statistics::default();
    let mut centore_stats = Statistics::default();
    let mut w3_results: HashMap<String, Vec<TestResult>> = HashMap::new();
    let mut centore_results: HashMap<String, Vec<TestResult>> = HashMap::new();
    
    w3_stats.total_unique_colors = w3_colors.len();
    centore_stats.total_unique_colors = centore_colors.len();
    
    println!("\n🔍 Analyzing conversions with Rust mathematical converter...");
    println!("   Using iscc_nbs_descriptor() accessor for ISCC-NBS naming");
    
    for (_id, rgb, illum_name, expected_name, dataset) in all_test_data {
        let illuminant = match illum_name.as_str() {
            "C" => MathIlluminant::C,
            "D65" => MathIlluminant::D65,
            "F7" => MathIlluminant::F7,
            _ => continue,
        };
        
        // Create converter with proper illuminant support
        let converter = MathematicalMunsellConverter::with_illuminants(
            MathIlluminant::D65,  // source (sRGB is D65)
            illuminant,            // target
            MathChromaticAdaptation::XYZScaling
        )?;
        
        // Convert with Rust
        let rust_spec = converter.srgb_to_munsell(rgb)?;
        let rust_notation = converter.format_munsell_notation(&rust_spec);
        
        // Use proper ISCC-NBS classification with revised descriptor
        let rust_classification_result = classifier.classify_munsell(
            &format!("{:.1}{}", rust_spec.hue, rust_spec.family), 
            rust_spec.value, 
            rust_spec.chroma
        );
        
        let (rust_iscc, rust_unknown) = match rust_classification_result {
            Ok(Some(result)) => {
                // Use the ISCC-NBS descriptor instead of revised descriptor
                (result.iscc_nbs_descriptor().to_string(), false)
            },
            Ok(None) => ("Unknown".to_string(), true),
            Err(_) => ("Unknown".to_string(), true),
        };
        
        // Check matches with case-insensitive comparison
        let rust_match = rust_iscc.to_lowercase() == expected_name.to_lowercase();

        // Update statistics
        let stats = if dataset == "W3" { &mut w3_stats } else { &mut centore_stats };
        let results = if dataset == "W3" { &mut w3_results } else { &mut centore_results };
        
        // Count matches
        if rust_match {
            *stats.rust_matches.entry(illum_name.clone()).or_insert(0) += 1;
        }
        
        // Track Unknown classifications for investigation
        if rust_unknown {
            *stats.rust_unknowns.entry(illum_name.clone()).or_insert(0) += 1;
        }
        
        // Store result
        let result = TestResult {
            rgb,
            illuminant: illum_name.clone(),
            expected_name: expected_name.clone(),
            munsell_notation: rust_notation,
            rust_iscc,
            rust_match,
            rust_unknown,
        };
        
        results.entry(illum_name.clone())
            .or_insert_with(Vec::new)
            .push(result);
    }
    
    // Generate report
    let mut report = String::new();
    writeln!(&mut report, "# Comprehensive Conversion Dataset - Mismatches Analysis")?;
    writeln!(&mut report)?;
    
    // ========== W3 DATASET SECTION ==========
    writeln!(&mut report, "## W3 Dataset")?;
    writeln!(&mut report)?;
    
    // W3 Summary Statistics Table
    writeln!(&mut report, "### Summary Statistics")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Illuminant | Total | Rust Correct | Rust Unknown | Rust Accuracy |")?;
    writeln!(&mut report, "|------------|-------|--------------|--------------|---------------|")?;
    
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65", 
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        let rust_matches = w3_stats.rust_matches.get(illum_name).unwrap_or(&0);
        let rust_unknowns = w3_stats.rust_unknowns.get(illum_name).unwrap_or(&0);
        
        let rust_acc = (*rust_matches as f64 / w3_stats.total_unique_colors as f64) * 100.0;
        
        writeln!(&mut report, "| {:10} | {:5} | {:12} | {:12} | {:12.1}% |",
            illum_name, w3_stats.total_unique_colors, rust_matches, rust_unknowns, rust_acc)?;
    }
    writeln!(&mut report)?;
    
    // W3 Detailed Mismatches (only show illuminants where Rust doesn't match)
    writeln!(&mut report, "### Detailed Mismatches")?;
    writeln!(&mut report)?;
    
    // Collect unique colors that have Rust mismatches
    let mut unique_colors = std::collections::HashSet::new();
    let mut color_results = Vec::new();
    
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        if let Some(results) = w3_results.get(illum_name) {
            for result in results.iter()
                .filter(|r| !r.rust_match) // Only care about Rust mismatches
            {
                let color_key = format!("{:02X}{:02X}{:02X}", result.rgb[0], result.rgb[1], result.rgb[2]);
                if unique_colors.insert(color_key.clone()) {
                    color_results.push((color_key, result.expected_name.clone(), result.rgb));
                }
            }
        }
    }
    
    // Display each unique color with ONLY illuminants where Rust doesn't match
    let mut color_count = 0;
    for (hex_key, expected_name, rgb) in color_results.iter() {
        color_count += 1;
        
        writeln!(&mut report, "#### Color {}: {}", color_count, expected_name)?;
        writeln!(&mut report)?;
        writeln!(&mut report, "**Hex:** #{}", hex_key)?;
        writeln!(&mut report)?;
        writeln!(&mut report, "| Illuminant | Rust Munsell | Rust descriptor | Dist polygon |")?;
        writeln!(&mut report, "|------------|--------------|-----------------|--------------|")?;
        
        // Only show illuminants where Rust doesn't match
        for (illuminant, _) in &configurations {
            let illum_name = match illuminant {
                MathIlluminant::C => "C",
                MathIlluminant::D65 => "D65",
                MathIlluminant::F7 => "F7",
                _ => continue,
            };
            
            if let Some(results) = w3_results.get(illum_name) {
                if let Some(result) = results.iter()
                    .find(|r| r.rgb == *rgb)
                {
                    // Only show this row if Rust doesn't match
                    if !result.rust_match {
                        let rust_descriptor = if result.rust_unknown {
                            "(Unknown)".to_string()
                        } else if result.rust_iscc.is_empty() || result.rust_iscc == "Unknown" {
                            "(No match)".to_string()
                        } else {
                            result.rust_iscc.clone()
                        };
                        
                        // Calculate polygon distance
                        let dist_str = calculate_distance_to_correct_polygon(
                            &result.munsell_notation,
                            expected_name,
                            &classifier
                        );
                        
                        writeln!(&mut report, "| {:10} | {:12} | {:15} | {:12} |",
                            illum_name,
                            result.munsell_notation,
                            rust_descriptor,
                            dist_str
                        )?;
                    }
                }
            }
        }
        writeln!(&mut report)?;
    }
    
    // ========== CENTORE DATASET SECTION ==========
    writeln!(&mut report, "## Centore Dataset")?;
    writeln!(&mut report)?;
    
    // Centore Summary Statistics Table
    writeln!(&mut report, "### Summary Statistics")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Illuminant | Total | Rust Correct | Rust Unknown | Rust Accuracy |")?;
    writeln!(&mut report, "|------------|-------|--------------|--------------|---------------|")?;
    
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7", 
            _ => continue,
        };
        
        let rust_matches = centore_stats.rust_matches.get(illum_name).unwrap_or(&0);
        let rust_unknowns = centore_stats.rust_unknowns.get(illum_name).unwrap_or(&0);
        
        let rust_acc = (*rust_matches as f64 / centore_stats.total_unique_colors as f64) * 100.0;
        
        writeln!(&mut report, "| {:10} | {:5} | {:12} | {:12} | {:12.1}% |",
            illum_name, centore_stats.total_unique_colors, rust_matches, rust_unknowns, rust_acc)?;
    }
    writeln!(&mut report)?;
    
    // Centore Detailed Mismatches (only show illuminants where Rust doesn't match)
    writeln!(&mut report, "### Detailed Mismatches")?;
    writeln!(&mut report)?;
    
    // Collect unique colors that have Rust mismatches
    let mut unique_colors = std::collections::HashSet::new();
    let mut color_results = Vec::new();
    
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        if let Some(results) = centore_results.get(illum_name) {
            for result in results.iter()
                .filter(|r| !r.rust_match) // Only care about Rust mismatches
            {
                let color_key = format!("{:02X}{:02X}{:02X}", result.rgb[0], result.rgb[1], result.rgb[2]);
                if unique_colors.insert(color_key.clone()) {
                    color_results.push((color_key, result.expected_name.clone(), result.rgb));
                }
            }
        }
    }
    
    // Display each unique color with ONLY illuminants where Rust doesn't match
    let mut color_count = 0;
    for (hex_key, expected_name, rgb) in color_results.iter() {
        color_count += 1;
        
        writeln!(&mut report, "#### Color {}: {}", color_count, expected_name)?;
        writeln!(&mut report)?;
        writeln!(&mut report, "**Hex:** #{}", hex_key)?;
        writeln!(&mut report)?;
        writeln!(&mut report, "| Illuminant | Rust Munsell | Rust descriptor | Dist polygon |")?;
        writeln!(&mut report, "|------------|--------------|-----------------|--------------|")?;
        
        // Only show illuminants where Rust doesn't match
        for (illuminant, _) in &configurations {
            let illum_name = match illuminant {
                MathIlluminant::C => "C",
                MathIlluminant::D65 => "D65",
                MathIlluminant::F7 => "F7",
                _ => continue,
            };
            
            if let Some(results) = centore_results.get(illum_name) {
                if let Some(result) = results.iter()
                    .find(|r| r.rgb == *rgb)
                {
                    // Only show this row if Rust doesn't match
                    if !result.rust_match {
                        let rust_descriptor = if result.rust_unknown {
                            "(Unknown)".to_string()
                        } else if result.rust_iscc.is_empty() || result.rust_iscc == "Unknown" {
                            "(No match)".to_string()
                        } else {
                            result.rust_iscc.clone()
                        };
                        
                        // Calculate polygon distance
                        let dist_str = calculate_distance_to_correct_polygon(
                            &result.munsell_notation,
                            expected_name,
                            &classifier
                        );
                        
                        writeln!(&mut report, "| {:10} | {:12} | {:15} | {:12} |",
                            illum_name,
                            result.munsell_notation,
                            rust_descriptor,
                            dist_str
                        )?;
                    }
                }
            }
        }
        writeln!(&mut report)?;
    }
    
    // Create reports directory if it doesn't exist
    std::fs::create_dir_all("investigation/reports")?;
    
    // Write report
    let output_path = "investigation/reports/comprehensive_dataset_misses.md";
    fs::write(output_path, report)?;
    
    println!("\n✅ Report generated: {}", output_path);
    println!("\n📊 Summary:");
    
    // Print accuracies
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        let w3_rust_matches = w3_stats.rust_matches.get(illum_name).unwrap_or(&0);
        let centore_rust_matches = centore_stats.rust_matches.get(illum_name).unwrap_or(&0);
        
        println!("  {} Illuminant:", illum_name);
        println!("    W3 Rust: {:.1}% ({}/{})", 
            *w3_rust_matches as f64 / w3_stats.total_unique_colors as f64 * 100.0, 
            w3_rust_matches, w3_stats.total_unique_colors);
        println!("    Centore Rust: {:.1}% ({}/{})", 
            *centore_rust_matches as f64 / centore_stats.total_unique_colors as f64 * 100.0,
            centore_rust_matches, centore_stats.total_unique_colors);
    }
    
    Ok(())
}


fn load_w3_dataset() -> Result<Vec<W3IsccColor>, Box<dyn std::error::Error>> {
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path("tests/data/ISCC_NBS_REFERENCE_DATASET.csv")?;
    
    let mut colors = Vec::new();
    for result in reader.deserialize() {
        let color: W3IsccColor = result?;
        colors.push(color);
    }
    Ok(colors)
}

fn load_centore_dataset() -> Result<Vec<CentoreIsccColor>, Box<dyn std::error::Error>> {
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path("tests/data/MUNSELL_COLOR_SCIENCE_COMPLETE.csv")?;
    
    let mut colors = Vec::new();
    for result in reader.deserialize() {
        let color: CentoreIsccColor = result?;
        colors.push(color);
    }
    Ok(colors)
}

fn parse_rgb(srgb_str: &str) -> Result<[u8; 3], Box<dyn std::error::Error>> {
    let trimmed = srgb_str.trim();
    
    if trimmed.starts_with('#') {
        // Parse hex format
        let hex = trimmed.trim_start_matches('#');
        let r = u8::from_str_radix(&hex[0..2], 16)?;
        let g = u8::from_str_radix(&hex[2..4], 16)?;
        let b = u8::from_str_radix(&hex[4..6], 16)?;
        Ok([r, g, b])
    } else {
        Err("Invalid RGB format".into())
    }
}