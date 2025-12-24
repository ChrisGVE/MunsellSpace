//! Simple RGB to Munsell batch converter
//!
//! Reads name,r,g,b from stdin (one per line) and outputs Munsell data.
//!
//! Usage:
//!   cat colors.csv | cargo run --example simple_rgb_to_munsell > output.csv

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
    writeln!(
        stdout,
        "name,r,g,b,hue_str,hue_num,value,chroma,munsell_notation,x,y,z"
    )
    .unwrap();

    for line in stdin.lock().lines() {
        let line = match line {
            Ok(l) => l,
            Err(_) => continue,
        };

        // Skip header or empty lines
        let line = line.trim();
        if line.is_empty() || line.starts_with("name,") || line.starts_with('#') {
            continue;
        }

        // Parse CSV: name,r,g,b
        let parts: Vec<&str> = line.splitn(4, ',').collect();
        if parts.len() < 4 {
            eprintln!("Skipping malformed line: {}", line);
            continue;
        }

        let name = parts[0];
        let r: u8 = match parts[1].trim().parse() {
            Ok(v) => v,
            Err(_) => {
                eprintln!("Invalid R value in line: {}", line);
                continue;
            }
        };
        let g: u8 = match parts[2].trim().parse() {
            Ok(v) => v,
            Err(_) => {
                eprintln!("Invalid G value in line: {}", line);
                continue;
            }
        };
        let b: u8 = match parts[3].trim().parse() {
            Ok(v) => v,
            Err(_) => {
                eprintln!("Invalid B value in line: {}", line);
                continue;
            }
        };

        // Convert RGB to Munsell
        match converter.srgb_to_munsell([r, g, b]) {
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
                    r,
                    g,
                    b,
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
                eprintln!("Error converting {} (RGB {},{},{}): {:?}", name, r, g, b, e);
            }
        }
    }
}
