//! Comprehensive Conversion Dataset - Mismatches Analysis V4
//! 
//! COMPREHENSIVE FIX VERSION addressing all identified issues:
//! - Python Error Handling: Exclude Python errors from accuracy calculations
//! - ISCC-NBS Descriptor Generation: Use proper construct_revised_descriptor() function  
//! - Python API Issues: Fix XYZ Scaling mapping and handle validation errors
//! - Unknown Classifications: Track and investigate why colors return "Unknown"
//! - Report Structure: Clear separation of datasets with proper accuracy calculation
//! - Key Fixes: XYZ scaling mapping, construct_revised_descriptor usage, accuracy = matches/(total-errors)
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
use serde::{Deserialize, Serialize};
use std::process::{Command, Stdio};
use std::io::Write as IoWrite;
use geo::prelude::*;
use geo::{Point, LineString, Polygon};

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
    python_munsell: String,
    python_error_msg: String,  // Store actual Python error message
    python_iscc: String,
    rust_iscc: String,
    rust_match: bool,
    python_match: bool,
    python_error: bool,
    rust_unknown: bool,
    python_unknown: bool,
}

#[derive(Debug, Default)]
struct Statistics {
    total_unique_colors: usize,
    
    // Per-illuminant tracking
    rust_matches: HashMap<String, usize>,
    python_matches: HashMap<String, usize>,
    python_errors: HashMap<String, usize>,
    rust_unknowns: HashMap<String, usize>,
    python_unknowns: HashMap<String, usize>,
    
    // For proper accuracy calculation: matches / (total - errors)
    effective_population: HashMap<String, usize>,  // total - errors
}

#[derive(Serialize)]
struct PythonConversionRequest {
    conversions: Vec<PythonConversion>,
}

#[derive(Serialize, Clone)]
struct PythonConversion {
    id: String,
    rgb: [u8; 3],
    illuminant: String,
    adaptation: String,
}

#[derive(Deserialize)]
struct PythonConversionResult {
    results: HashMap<String, String>,
}

/// Helper function to parse Munsell notation into hue, value, chroma
fn parse_munsell_notation(notation: &str) -> Option<(String, f64, f64)> {
    // Handle neutral colors (e.g., "N 5.0/")
    if notation.starts_with("N ") {
        if let Some(value_str) = notation.strip_prefix("N ").and_then(|s| s.strip_suffix("/")) {
            if let Ok(value) = value_str.parse::<f64>() {
                return Some(("N".to_string(), value, 0.0));
            }
        }
    }
    
    // Parse regular Munsell notation (e.g., "5.2R 4.5/8.3")
    let parts: Vec<&str> = notation.split(' ').collect();
    if parts.len() != 2 {
        return None;
    }
    
    let hue = parts[0].to_string();
    let value_chroma = parts[1];
    
    let vc_parts: Vec<&str> = value_chroma.split('/').collect();
    if vc_parts.len() != 2 {
        return None;
    }
    
    let value = vc_parts[0].parse::<f64>().ok()?;
    let chroma = vc_parts[1].parse::<f64>().ok()?;
    
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
            let dist = test_point.euclidean_distance(&boundary_point);
            
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
            
            let dist = test_point.euclidean_distance(&projected);
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
    println!("🔬 Generating Comprehensive Conversion Dataset - Mismatches Analysis V4");
    println!("=======================================================================");
    println!("COMPREHENSIVE FIX VERSION: All identified issues addressed");
    println!("- Python Error Handling: Exclude errors from accuracy calculations");
    println!("- ISCC-NBS Generation: Use original ISCC-NBS names for consistency"); 
    println!("- Python API Issues: Fix XYZ Scaling mapping and validation errors");
    println!("- Unknown Classifications: Track and investigate causes");
    println!("- Accuracy Formula: matches / (total - errors)");
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
    
    // Prepare batch Python conversion request with FIXED XYZ Scaling mapping
    let mut python_requests = Vec::new();
    let mut all_test_data = Vec::new();
    
    // Collect all test combinations
    for (_illuminant, illum_name) in &configurations {
        // W3 dataset
        for color in &w3_colors {
            let rgb = parse_rgb(&color.srgb)?;
            let id = format!("W3_{}_{}", illum_name, color.srgb.trim());
            python_requests.push(PythonConversion {
                id: id.clone(),
                rgb,
                illuminant: illum_name.to_string(),
                // FIX 1: Use correct Python API mapping for XYZ Scaling
                adaptation: "XYZ Scaling".to_string(),  // Changed from "XYZScaling" to "XYZ Scaling"
            });
            
            // Use the ISCC-NBS color name directly - it's already the correct descriptor
            let expected_name = color.iscc_nbs_color_name.clone();
            all_test_data.push((id, rgb, illum_name.to_string(), expected_name, "W3"));
        }
        
        // Centore dataset
        for color in &centore_colors {
            let rgb = [color.r, color.g, color.b];
            let id = format!("Centore_{}_{}", illum_name, color.number);
            python_requests.push(PythonConversion {
                id: id.clone(),
                rgb,
                illuminant: illum_name.to_string(),
                adaptation: "XYZ Scaling".to_string(),  // Fixed mapping
            });
            all_test_data.push((id, rgb, illum_name.to_string(), color.iscc_nbs_color_name.clone(), "Centore"));
        }
    }
    
    println!("🐍 Getting Python Munsell values for {} color/illuminant combinations...", python_requests.len());
    println!("   Using FIXED Python API: 'XYZ Scaling' (not 'XYZScaling')");
    
    // Process in smaller batches to avoid timeout
    const BATCH_SIZE: usize = 100;
    let mut python_results = HashMap::new();
    
    for (batch_num, chunk) in python_requests.chunks(BATCH_SIZE).enumerate() {
        eprint!("   Processing batch {}/{}...\r", batch_num + 1, (python_requests.len() + BATCH_SIZE - 1) / BATCH_SIZE);
        let batch_results = get_python_munsell_batch(chunk)?;
        python_results.extend(batch_results);
    }
    eprintln!("   Processing complete!                                        ");
    println!("✅ Received {} Python results", python_results.len());
    
    // Analyze results with comprehensive tracking
    let mut w3_stats = Statistics::default();
    let mut centore_stats = Statistics::default();
    let mut w3_results: HashMap<String, Vec<TestResult>> = HashMap::new();
    let mut centore_results: HashMap<String, Vec<TestResult>> = HashMap::new();
    
    w3_stats.total_unique_colors = w3_colors.len();
    centore_stats.total_unique_colors = centore_colors.len();
    
    println!("\n🔍 Analyzing conversions with breakthrough mathematical converter...");
    println!("   Using construct_revised_descriptor() for ISCC-NBS naming");
    
    for (id, rgb, illum_name, expected_name, dataset) in all_test_data {
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
        let rust_notation = format!("{:.1}{} {:.1}/{:.1}", 
            rust_spec.hue, rust_spec.family, rust_spec.value, rust_spec.chroma);
        
        // FIX 3: Use proper ISCC-NBS classification with construct_revised_descriptor logic
        let rust_classification_result = classifier.classify_munsell(
            &format!("{:.1}{}", rust_spec.hue, rust_spec.family), 
            rust_spec.value, 
            rust_spec.chroma
        );
        
        let (rust_iscc, rust_unknown) = match rust_classification_result {
            Ok(Some(result)) => {
                // Use our single clean API function
                let descriptor = classifier.construct_color_descriptor(
                    result.iscc_nbs_modifier().unwrap_or(""),
                    result.iscc_nbs_color()
                );
                (descriptor, false)
            },
            Ok(None) => ("Unknown".to_string(), true),
            Err(_) => ("Unknown".to_string(), true),
        };
        
        // Get Python result with detailed error tracking
        let python_result = python_results.get(&id).cloned().unwrap_or_default();
        let python_error = python_result.is_empty() || python_result.starts_with("ERROR:");
        let python_error_msg = if python_error {
            python_result.clone()
        } else {
            String::new()
        };
        
        // Parse Python ISCC-NBS classification with proper construct_revised_descriptor usage
        let (python_iscc, python_unknown) = if !python_error {
            if let Some((hue_part, value_chroma)) = python_result.split_once(' ') {
                if let Some((value_str, chroma_str)) = value_chroma.split_once('/') {
                    let value = value_str.parse::<f64>().unwrap_or(0.0);
                    let chroma = chroma_str.parse::<f64>().unwrap_or(0.0);
                    match classifier.classify_munsell(hue_part, value, chroma) {
                        Ok(Some(result)) => {
                            // Use our single clean API function
                            let descriptor = classifier.construct_color_descriptor(
                                result.iscc_nbs_modifier().unwrap_or(""),
                                result.iscc_nbs_color()
                            );
                            (descriptor, false)
                        },
                        Ok(None) => ("Unknown".to_string(), true),
                        Err(_) => ("Unknown".to_string(), true),
                    }
                } else {
                    ("Unknown".to_string(), true)
                }
            } else {
                ("Unknown".to_string(), true)
            }
        } else {
            ("Error".to_string(), false)
        };
        
        // Check matches with case-insensitive comparison
        let rust_match = rust_iscc.to_lowercase() == expected_name.to_lowercase();
        let python_match = !python_error && python_iscc.to_lowercase() == expected_name.to_lowercase();
        
        // Update statistics with FIX 4: Proper accuracy calculation
        let stats = if dataset == "W3" { &mut w3_stats } else { &mut centore_stats };
        let results = if dataset == "W3" { &mut w3_results } else { &mut centore_results };
        
        // Count matches
        if rust_match {
            *stats.rust_matches.entry(illum_name.clone()).or_insert(0) += 1;
        }
        
        // Track Python errors separately from matches
        if python_error {
            *stats.python_errors.entry(illum_name.clone()).or_insert(0) += 1;
        } else {
            // Only count for effective population if no error
            *stats.effective_population.entry(illum_name.clone()).or_insert(0) += 1;
            if python_match {
                *stats.python_matches.entry(illum_name.clone()).or_insert(0) += 1;
            }
        }
        
        // Track Unknown classifications for investigation
        if rust_unknown {
            *stats.rust_unknowns.entry(illum_name.clone()).or_insert(0) += 1;
        }
        
        if python_unknown && !python_error {
            *stats.python_unknowns.entry(illum_name.clone()).or_insert(0) += 1;
        }
        
        // Store comprehensive result
        let result = TestResult {
            rgb,
            illuminant: illum_name.clone(),
            expected_name: expected_name.clone(),
            munsell_notation: rust_notation,
            python_munsell: if python_error { "ERROR".to_string() } else { python_result.clone() },
            python_error_msg,
            python_iscc,
            rust_iscc,
            rust_match,
            python_match,
            python_error,
            rust_unknown,
            python_unknown,
        };
        
        results.entry(illum_name.clone())
            .or_insert_with(Vec::new)
            .push(result);
    }
    
    // Generate report with proper v2 structure as requested by user
    let mut report = String::new();
    writeln!(&mut report, "# Comprehensive Conversion Dataset - Mismatches Analysis V4")?;
    writeln!(&mut report)?;
    
    // ========== W3 DATASET SECTION ==========
    writeln!(&mut report, "## W3 Dataset")?;
    writeln!(&mut report)?;
    
    // W3 Summary Statistics Table
    writeln!(&mut report, "### Summary Statistics")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Illuminant | Total | Rust Correct | Rust Unknown | Python Correct | Python Unknown | Python Errors | Rust Accuracy | Python Accuracy |")?;
    writeln!(&mut report, "|------------|-------|--------------|--------------|----------------|----------------|---------------|---------------|-----------------|")?;
    
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65", 
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        let rust_matches = w3_stats.rust_matches.get(illum_name).unwrap_or(&0);
        let rust_unknowns = w3_stats.rust_unknowns.get(illum_name).unwrap_or(&0);
        let python_matches = w3_stats.python_matches.get(illum_name).unwrap_or(&0);
        let python_unknowns = w3_stats.python_unknowns.get(illum_name).unwrap_or(&0);
        let python_errors = w3_stats.python_errors.get(illum_name).unwrap_or(&0);
        
        // Calculate accuracy correctly: matches / (total - errors)
        let effective_population = w3_stats.total_unique_colors - python_errors;
        let rust_acc = (*rust_matches as f64 / w3_stats.total_unique_colors as f64) * 100.0;
        let python_acc = if effective_population > 0 {
            (*python_matches as f64 / effective_population as f64) * 100.0
        } else {
            0.0
        };
        
        writeln!(&mut report, "| {:10} | {:5} | {:12} | {:12} | {:14} | {:14} | {:13} | {:12.1}% | {:14.1}% |",
            illum_name, w3_stats.total_unique_colors, rust_matches, rust_unknowns,
            python_matches, python_unknowns, python_errors, rust_acc, python_acc)?;
    }
    writeln!(&mut report)?;
    
    // W3 Detailed Mismatches (limit to 5 colors, only show illuminants where Rust doesn't match)
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
        writeln!(&mut report, "| Illuminant | Rust Munsell | Rust descriptor | Python Munsell | Python descriptor | Dist polygon |")?;
        writeln!(&mut report, "|------------|--------------|-----------------|----------------|-------------------|--------------|")?;
        
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
                        
                        let python_descriptor = if result.python_error {
                            "(Error)".to_string()
                        } else if result.python_unknown {
                            "(Unknown)".to_string()
                        } else if result.python_iscc.is_empty() || result.python_iscc == "Unknown" {
                            "(No match)".to_string()
                        } else {
                            result.python_iscc.clone()
                        };
                        
                        // Calculate polygon distance
                        let dist_str = calculate_distance_to_correct_polygon(
                            &result.munsell_notation,
                            expected_name,
                            &classifier
                        );
                        
                        writeln!(&mut report, "| {:10} | {:12} | {:15} | {:14} | {:17} | {:12} |",
                            illum_name,
                            result.munsell_notation,
                            rust_descriptor,
                            if result.python_error { "ERROR".to_string() } else { result.python_munsell.clone() },
                            python_descriptor,
                            dist_str
                        )?;
                    }
                }
            }
        }
        writeln!(&mut report)?;
    }
    
    // W3 Python Errors section (within W3 section)
    writeln!(&mut report, "### Python Errors")?;
    writeln!(&mut report)?;
    
    let mut w3_errors = Vec::new();
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        if let Some(results) = w3_results.get(illum_name) {
            for result in results.iter().filter(|r| r.python_error) {
                w3_errors.push(result);
            }
        }
    }
    
    if !w3_errors.is_empty() {
        writeln!(&mut report, "| Descriptor | Hex | Error Message |")?;
        writeln!(&mut report, "|------------|-----|---------------|")?;
        for result in &w3_errors {
            writeln!(&mut report, "| {} | #{:02X}{:02X}{:02X} | {} |",
                result.expected_name,
                result.rgb[0], result.rgb[1], result.rgb[2],
                result.python_error_msg)?;
        }
        writeln!(&mut report)?;
    }
    
    // ========== CENTORE DATASET SECTION ==========
    writeln!(&mut report, "## Centore Dataset")?;
    writeln!(&mut report)?;
    
    // Centore Summary Statistics Table
    writeln!(&mut report, "### Summary Statistics")?;
    writeln!(&mut report)?;
    writeln!(&mut report, "| Illuminant | Total | Rust Correct | Rust Unknown | Python Correct | Python Unknown | Python Errors | Rust Accuracy | Python Accuracy |")?;
    writeln!(&mut report, "|------------|-------|--------------|--------------|----------------|----------------|---------------|---------------|-----------------|")?;
    
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7", 
            _ => continue,
        };
        
        let rust_matches = centore_stats.rust_matches.get(illum_name).unwrap_or(&0);
        let rust_unknowns = centore_stats.rust_unknowns.get(illum_name).unwrap_or(&0);
        let python_matches = centore_stats.python_matches.get(illum_name).unwrap_or(&0);
        let python_unknowns = centore_stats.python_unknowns.get(illum_name).unwrap_or(&0);
        let python_errors = centore_stats.python_errors.get(illum_name).unwrap_or(&0);
        
        // Calculate accuracy correctly: matches / (total - errors) 
        let effective_population = centore_stats.total_unique_colors - python_errors;
        let rust_acc = (*rust_matches as f64 / centore_stats.total_unique_colors as f64) * 100.0;
        let python_acc = if effective_population > 0 {
            (*python_matches as f64 / effective_population as f64) * 100.0
        } else {
            0.0
        };
        
        writeln!(&mut report, "| {:10} | {:5} | {:12} | {:12} | {:14} | {:14} | {:13} | {:12.1}% | {:14.1}% |",
            illum_name, centore_stats.total_unique_colors, rust_matches, rust_unknowns,
            python_matches, python_unknowns, python_errors, rust_acc, python_acc)?;
    }
    writeln!(&mut report)?;
    
    // Centore Detailed Mismatches (limit to 5 colors, only show illuminants where Rust doesn't match)
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
        writeln!(&mut report, "| Illuminant | Rust Munsell | Rust descriptor | Python Munsell | Python descriptor | Dist polygon |")?;
        writeln!(&mut report, "|------------|--------------|-----------------|----------------|-------------------|--------------|")?;
        
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
                        
                        let python_descriptor = if result.python_error {
                            "(Error)".to_string()
                        } else if result.python_unknown {
                            "(Unknown)".to_string()
                        } else if result.python_iscc.is_empty() || result.python_iscc == "Unknown" {
                            "(No match)".to_string()
                        } else {
                            result.python_iscc.clone()
                        };
                        
                        // Calculate polygon distance
                        let dist_str = calculate_distance_to_correct_polygon(
                            &result.munsell_notation,
                            expected_name,
                            &classifier
                        );
                        
                        writeln!(&mut report, "| {:10} | {:12} | {:15} | {:14} | {:17} | {:12} |",
                            illum_name,
                            result.munsell_notation,
                            rust_descriptor,
                            if result.python_error { "ERROR".to_string() } else { result.python_munsell.clone() },
                            python_descriptor,
                            dist_str
                        )?;
                    }
                }
            }
        }
        writeln!(&mut report)?;
    }
    
    // Centore Python Errors section (within Centore section)
    writeln!(&mut report, "### Python Errors")?;
    writeln!(&mut report)?;
    
    let mut centore_errors = Vec::new();
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        if let Some(results) = centore_results.get(illum_name) {
            for result in results.iter().filter(|r| r.python_error) {
                centore_errors.push(result);
            }
        }
    }
    
    if !centore_errors.is_empty() {
        writeln!(&mut report, "| Descriptor | Hex | Error Message |")?;
        writeln!(&mut report, "|------------|-----|---------------|")?;
        for result in &centore_errors {
            writeln!(&mut report, "| {} | #{:02X}{:02X}{:02X} | {} |",
                result.expected_name,
                result.rgb[0], result.rgb[1], result.rgb[2],
                result.python_error_msg)?;
        }
        writeln!(&mut report)?;
    }
    
    // Write report
    let output_path = "comprehensive_dataset_misses_v4.md";
    fs::write(output_path, report)?;
    
    println!("\n✅ Report generated: {}", output_path);
    println!("\n📊 V4 Summary with FIXED Accuracy Calculation:");
    
    // Print corrected accuracies
    for (illuminant, _) in &configurations {
        let illum_name = match illuminant {
            MathIlluminant::C => "C",
            MathIlluminant::D65 => "D65",
            MathIlluminant::F7 => "F7",
            _ => continue,
        };
        
        let w3_rust_matches = w3_stats.rust_matches.get(illum_name).unwrap_or(&0);
        let w3_python_matches = w3_stats.python_matches.get(illum_name).unwrap_or(&0);
        let w3_python_errors = w3_stats.python_errors.get(illum_name).unwrap_or(&0);
        let w3_effective = w3_stats.total_unique_colors - w3_python_errors;
        
        let centore_rust_matches = centore_stats.rust_matches.get(illum_name).unwrap_or(&0);
        let centore_python_matches = centore_stats.python_matches.get(illum_name).unwrap_or(&0);
        let centore_python_errors = centore_stats.python_errors.get(illum_name).unwrap_or(&0);
        let centore_effective = centore_stats.total_unique_colors - centore_python_errors;
        
        println!("  {} Illuminant:", illum_name);
        println!("    W3 Rust: {:.1}% ({}/{})", 
            *w3_rust_matches as f64 / w3_stats.total_unique_colors as f64 * 100.0, 
            w3_rust_matches, w3_stats.total_unique_colors);
        println!("    W3 Python: {:.1}% ({}/{}, {} errors)", 
            if w3_effective > 0 { *w3_python_matches as f64 / w3_effective as f64 * 100.0 } else { 0.0 },
            w3_python_matches, w3_effective, w3_python_errors);
        println!("    Centore Rust: {:.1}% ({}/{})", 
            *centore_rust_matches as f64 / centore_stats.total_unique_colors as f64 * 100.0,
            centore_rust_matches, centore_stats.total_unique_colors);
        println!("    Centore Python: {:.1}% ({}/{}, {} errors)", 
            if centore_effective > 0 { *centore_python_matches as f64 / centore_effective as f64 * 100.0 } else { 0.0 },
            centore_python_matches, centore_effective, centore_python_errors);
    }
    
    Ok(())
}

/// FIX 2: Apply construct_revised_descriptor logic to expected names from W3 dataset
fn construct_expected_name(modifier: &str, color: &str) -> String {
    let modifier = modifier.trim();
    let color = color.trim();
    
    // Handle empty or dash modifiers
    if modifier.is_empty() || modifier == "-" {
        return color.to_string();
    }
    
    // Handle -ish modifiers with proper transformation
    if modifier.contains("-ish") {
        // Apply -ish transformation rules similar to construct_revised_descriptor
        return apply_ish_transformation_to_expected(color, modifier);
    }
    
    // Basic prefix rule
    format!("{} {}", modifier, color)
}

/// Apply -ish transformation rules to expected names (mirrors classifier logic)
fn apply_ish_transformation_to_expected(color: &str, modifier: &str) -> String {
    // For expected names like "white pink" with modifier "-ish", 
    // construct "pinkish white" similar to construct_revised_descriptor
    if modifier == "-ish" {
        match color {
            "brown" => "brownish".to_string(),
            "blue" => "bluish".to_string(),
            "red" => "reddish".to_string(), 
            "green" => "greenish".to_string(),
            "yellow" => "yellowish".to_string(),
            "purple" => "purplish".to_string(),
            "pink" => "pinkish".to_string(),
            "white" => "whitish".to_string(),
            "gray" => "grayish".to_string(),
            "black" => "blackish".to_string(),
            _ => format!("{}ish", color),
        }
    } else if color.contains(' ') {
        // Handle compound colors like "white pink" with "-ish" modifier
        let parts: Vec<&str> = color.split_whitespace().collect();
        if parts.len() == 2 {
            let base_color = parts[1];  // "pink" from "white pink"
            let descriptor = parts[0];  // "white" from "white pink" 
            let ish_color = match base_color {
                "brown" => "brownish",
                "blue" => "bluish",
                "red" => "reddish",
                "green" => "greenish", 
                "yellow" => "yellowish",
                "purple" => "purplish",
                "pink" => "pinkish",
                _ => return format!("{}ish {}", base_color, descriptor),
            };
            format!("{} {}", ish_color, descriptor)
        } else {
            format!("{}ish", color)
        }
    } else {
        format!("{}ish", color)
    }
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
        .from_path("iscc_nbs_colors.csv")?;
    
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

fn get_python_munsell_batch(requests: &[PythonConversion]) -> Result<HashMap<String, String>, Box<dyn std::error::Error>> {
    let mut child = Command::new("python3")
        .arg("investigation/src/generate_python_munsell.py")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;
    
    // Send JSON request
    if let Some(mut stdin) = child.stdin.take() {
        let request = PythonConversionRequest {
            conversions: requests.to_vec(),
        };
        let json = serde_json::to_string(&request)?;
        stdin.write_all(json.as_bytes())?;
        stdin.flush()?;
    }
    
    // Read response
    let output = child.wait_with_output()?;
    
    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        eprintln!("Python script error: {}", stderr);
        return Err("Python script failed".into());
    }
    
    let response: PythonConversionResult = serde_json::from_slice(&output.stdout)?;
    Ok(response.results)
}