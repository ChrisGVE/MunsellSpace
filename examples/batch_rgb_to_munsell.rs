//! Batch RGB to Munsell conversion tool
//!
//! Reads RGB values from stdin (CSV format) and outputs Munsell notation with cartesian coordinates.
//!
//! Usage:
//!   cat colors.csv | cargo run --example batch_rgb_to_munsell > output.csv

use munsellspace::MunsellConverter;
use munsellspace::semantic_overlay::{MunsellSpec, parse_hue_to_number};
use std::io::{self, BufRead, Write};

fn main() {
    let stdin = io::stdin();
    let stdout = io::stdout();
    let mut stdout = stdout.lock();

    // Initialize the converter
    let converter = match MunsellConverter::new() {
        Ok(c) => c,
        Err(e) => {
            eprintln!("Failed to initialize MunsellConverter: {:?}", e);
            std::process::exit(1);
        }
    };

    // Output header
    writeln!(stdout, "name,r,g,b,hue_str,hue_num,value,chroma,munsell_notation,x,y,z").unwrap();

    for line in stdin.lock().lines() {
        let line = match line {
            Ok(l) => l,
            Err(_) => continue,
        };

        // Skip header or empty lines
        let line = line.trim();
        if line.is_empty() || line.starts_with("colorname") || line.starts_with('#') {
            continue;
        }

        // Parse CSV: colorname,count,base_pattern,is_variant,mean_r,mean_g,mean_b,hex,avg_std
        let parts: Vec<&str> = line.split(',').collect();
        if parts.len() < 7 {
            eprintln!("Skipping malformed line: {}", line);
            continue;
        }

        let name = parts[0];
        let r: f64 = match parts[4].parse() {
            Ok(v) => v,
            Err(_) => continue,
        };
        let g: f64 = match parts[5].parse() {
            Ok(v) => v,
            Err(_) => continue,
        };
        let b: f64 = match parts[6].parse() {
            Ok(v) => v,
            Err(_) => continue,
        };

        // Convert to 0-255 u8 values
        let r_u8 = r.round().clamp(0.0, 255.0) as u8;
        let g_u8 = g.round().clamp(0.0, 255.0) as u8;
        let b_u8 = b.round().clamp(0.0, 255.0) as u8;

        // Convert RGB to Munsell
        match converter.srgb_to_munsell([r_u8, g_u8, b_u8]) {
            Ok(munsell) => {
                let value = munsell.value;
                let chroma = munsell.chroma.unwrap_or(0.0);
                let hue_str = munsell.hue.clone().unwrap_or_else(|| "N".to_string());

                // Create MunsellSpec from components
                let spec = if munsell.is_neutral() {
                    MunsellSpec::neutral(value)
                } else {
                    let hue_num = parse_hue_to_number(&hue_str).unwrap_or(0.0);
                    MunsellSpec::new(hue_num, value, chroma)
                };

                // Get cartesian coordinates
                let cartesian = spec.to_cartesian();

                writeln!(
                    stdout,
                    "{},{},{},{},{},{:.2},{:.2},{:.2},{},{:.4},{:.4},{:.4}",
                    name,
                    r_u8,
                    g_u8,
                    b_u8,
                    hue_str,
                    spec.hue_number,
                    value,
                    chroma,
                    munsell,
                    cartesian.x,
                    cartesian.y,
                    cartesian.z
                )
                .unwrap();
            }
            Err(e) => {
                eprintln!("Error converting {} (RGB {},{},{}): {:?}", name, r_u8, g_u8, b_u8, e);
            }
        }
    }
}
