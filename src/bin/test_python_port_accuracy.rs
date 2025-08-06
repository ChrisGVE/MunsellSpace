//! Test the Python port accuracy against the full 4,007 color reference dataset

use munsellspace::python_converter::PythonMunsellConverter;
use std::fs::File;
use std::io::{BufRead, BufReader};

// Helper functions for direct testing
fn srgb_to_xyz_d65(rgb: [f64; 3]) -> [f64; 3] {
    // Apply gamma correction
    let linear: Vec<f64> = rgb.iter().map(|&c| {
        if c <= 0.04045 {
            c / 12.92
        } else {
            ((c + 0.055) / 1.055).powf(2.4)
        }
    }).collect();
    
    // sRGB to XYZ matrix (D65 illuminant)
    let matrix = [
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ];
    
    [
        matrix[0][0] * linear[0] + matrix[0][1] * linear[1] + matrix[0][2] * linear[2],
        matrix[1][0] * linear[0] + matrix[1][1] * linear[1] + matrix[1][2] * linear[2],
        matrix[2][0] * linear[0] + matrix[2][1] * linear[1] + matrix[2][2] * linear[2],
    ]
}

fn xyz_to_xyy(xyz: [f64; 3]) -> [f64; 3] {
    let sum = xyz[0] + xyz[1] + xyz[2];
    if sum.abs() < 1e-10 {
        // Return D65 white point for black
        [0.31271, 0.32902, 0.0]
    } else {
        [xyz[0] / sum, xyz[1] / sum, xyz[1]]
    }
}

fn main() {
    println!("Testing Python port accuracy against 4,007 reference colors...\n");
    
    let converter = PythonMunsellConverter::new();
    let file = File::open("tests/data/srgb-to-munsell.csv").expect("Failed to open reference dataset");
    let reader = BufReader::new(file);
    
    let mut total = 0;
    let mut exact_matches = 0;
    let mut close_matches = 0;
    let mut errors = 0;
    let mut mismatches = Vec::new();
    
    for (i, line) in reader.lines().enumerate() {
        if i == 0 { continue; } // Skip header
        
        let line = line.expect("Failed to read line");
        let parts: Vec<&str> = line.split(',').collect();
        if parts.len() != 4 { continue; }
        
        let r: u8 = parts[0].parse().expect("Invalid R value");
        let g: u8 = parts[1].parse().expect("Invalid G value");
        let b: u8 = parts[2].parse().expect("Invalid B value");
        let expected = parts[3].trim();
        
        total += 1;
        
        match converter.srgb_to_munsell([r, g, b]) {
            Ok(munsell) => {
                let result = munsell.notation.as_str();
                
                if result == expected {
                    exact_matches += 1;
                } else if are_close(&munsell, expected) {
                    close_matches += 1;
                    if mismatches.len() < 10 {
                        mismatches.push((
                            [r, g, b],
                            expected.to_string(),
                            result.to_string(),
                            "close"
                        ));
                    }
                } else {
                    if mismatches.len() < 10 {
                        mismatches.push((
                            [r, g, b],
                            expected.to_string(),
                            result.to_string(),
                            "mismatch"
                        ));
                    }
                }
            }
            Err(e) => {
                errors += 1;
                if errors <= 5 {
                    println!("Error converting [{}, {}, {}] (expected {}): {:?}", 
                             r, g, b, expected, e);
                    
                    // Try to get the raw specification to see what the algorithm produces
                    let rgb_f = [r as f64 / 255.0, g as f64 / 255.0, b as f64 / 255.0];
                    let xyz = srgb_to_xyz_d65(rgb_f);
                    let xyy = xyz_to_xyy(xyz);
                    match munsellspace::python_port::xyy_to_munsell_specification(xyy) {
                        Ok(spec) => {
                            println!("  Raw spec: hue={:.2}, value={:.2}, chroma={:.2}, code={}", 
                                     spec[0], spec[1], spec[2], spec[3] as u8);
                        }
                        Err(e2) => {
                            println!("  Algorithm also failed: {:?}", e2);
                        }
                    }
                }
            }
        }
        
        if total % 500 == 0 {
            println!("Processed {} colors...", total);
        }
    }
    
    // Print results
    println!("\n=== RESULTS ===");
    println!("Total colors tested: {}", total);
    println!("Exact matches: {} ({:.2}%)", exact_matches, exact_matches as f64 / total as f64 * 100.0);
    println!("Close matches: {} ({:.2}%)", close_matches, close_matches as f64 / total as f64 * 100.0);
    println!("Total accurate: {} ({:.2}%)", 
             exact_matches + close_matches, 
             (exact_matches + close_matches) as f64 / total as f64 * 100.0);
    println!("Errors: {} ({:.2}%)", errors, errors as f64 / total as f64 * 100.0);
    
    if !mismatches.is_empty() {
        println!("\n=== SAMPLE MISMATCHES ===");
        for (rgb, expected, actual, match_type) in mismatches {
            println!("[{}, {}, {}]: expected '{}', got '{}' ({})", 
                     rgb[0], rgb[1], rgb[2], expected, actual, match_type);
        }
    }
}

fn are_close(munsell: &munsellspace::MunsellColor, expected: &str) -> bool {
    // Parse expected notation
    let expected = expected.trim();
    
    // Handle neutral colors
    if expected.starts_with("N ") && munsell.notation.starts_with("N ") {
        let expected_value = parse_neutral_value(expected);
        let actual_value = munsell.value;
        return (expected_value - actual_value).abs() <= 0.1;
    }
    
    // Handle chromatic colors
    if let Some((exp_hue, exp_value, exp_chroma)) = parse_chromatic(expected) {
        if let (Some(act_hue), Some(act_chroma)) = (&munsell.hue, munsell.chroma) {
            // Check if hue families match
            let exp_family = extract_family(&exp_hue);
            let act_family = extract_family(act_hue);
            if exp_family != act_family {
                return false;
            }
            
            // Check value and chroma differences
            let value_diff = (exp_value - munsell.value).abs();
            let chroma_diff = (exp_chroma - act_chroma).abs();
            
            // Check hue difference
            let exp_hue_num = extract_hue_number(&exp_hue);
            let act_hue_num = extract_hue_number(act_hue);
            let hue_diff = (exp_hue_num - act_hue_num).abs();
            
            // Consider "close" if all differences are small
            return value_diff <= 0.1 && chroma_diff <= 0.5 && hue_diff <= 0.5;
        }
    }
    
    false
}

fn parse_neutral_value(notation: &str) -> f64 {
    notation.trim_start_matches("N ")
        .trim_end_matches('/')
        .parse()
        .unwrap_or(0.0)
}

fn parse_chromatic(notation: &str) -> Option<(String, f64, f64)> {
    let parts: Vec<&str> = notation.split_whitespace().collect();
    if parts.len() != 2 { return None; }
    
    let hue = parts[0].to_string();
    let value_chroma: Vec<&str> = parts[1].split('/').collect();
    if value_chroma.len() != 2 { return None; }
    
    let value = value_chroma[0].parse().ok()?;
    let chroma = value_chroma[1].parse().ok()?;
    
    Some((hue, value, chroma))
}

fn extract_family(hue: &str) -> String {
    hue.chars().filter(|c| c.is_alphabetic()).collect()
}

fn extract_hue_number(hue: &str) -> f64 {
    hue.chars()
        .take_while(|c| c.is_numeric() || *c == '.')
        .collect::<String>()
        .parse()
        .unwrap_or(5.0)
}