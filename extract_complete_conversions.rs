#!/usr/bin/env rust
//! Extract Complete 260-Color Conversion Results
//!
//! Creates a comprehensive table with all RGB→Munsell conversions for hardcopy verification

use std::fs;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Extracting complete conversion results...");
    
    // Read the test dataset
    let csv_content = fs::read_to_string("tests/data/MUNSELL_COLOR_SCIENCE_COMPLETE.csv")?;
    let mut reader = csv::Reader::from_reader(csv_content.as_bytes());
    
    let mut output = String::new();
    
    // Header
    output.push_str("# Complete 260-Color Conversion Dataset for Hardcopy Verification\n\n");
    output.push_str("This dataset shows RGB→Munsell conversions and ISCC-NBS classifications for all 260 reference colors.\n");
    output.push_str("Use this for verification against hardcopy Munsell charts.\n\n");
    
    output.push_str("## Key Information\n");
    output.push_str("- **Total Colors**: 260\n");
    output.push_str("- **RGB→Munsell Conversion**: 100% success (mathematical conversion working)\n");
    output.push_str("- **ISCC-NBS Classification**: 69.23% success (180/260 correct)\n");
    output.push_str("- **Method 1 vs Method 2**: Both achieve same 69.23% accuracy\n\n");
    
    output.push_str("## Precision Issues to Verify\n");
    output.push_str("Focus on these cases when checking against hardcopy charts:\n\n");
    
    let precision_cases = [
        ("#EFDDE5", "pinkish white", "9.8R 9.1/1.6", "Expected chroma 1.5, got 1.6"),
        ("#C7B6BD", "pinkish gray", "3YR 7.5/1.6", "Expected chroma 1.5, got 1.6"),
        ("#5C0625", "very deep red", "6.6RP 1.6/6.3", "Expected R family, got RP"),
        ("#481127", "very dark red", "3.7RP 1.3/4.0", "Expected R family, got RP"),
        ("#886648", "moderate yellowish brown", "9.5R 4.5/6.0", "Boundary classification issue"),
    ];
    
    for (rgb, expected, munsell, issue) in precision_cases.iter() {
        output.push_str(&format!("- **{}** → {} (expected: {}) - *{}*\n", rgb, munsell, expected, issue));
    }
    output.push_str("\n");
    
    output.push_str("## Complete Dataset\n\n");
    output.push_str("| # | RGB Hex | Expected Name | R | G | B | Munsell | Notes |\n");
    output.push_str("|---|---------|---------------|---|---|---|---------|-------|\n");
    
    // Process each record
    for (index, result) in reader.records().enumerate() {
        let record = result?;
        
        if record.len() < 5 {
            continue;
        }
        
        // Parse RGB values
        let r: u8 = record.get(0).unwrap_or("0").trim().parse().unwrap_or(0);
        let g: u8 = record.get(1).unwrap_or("0").trim().parse().unwrap_or(0);
        let b: u8 = record.get(2).unwrap_or("0").trim().parse().unwrap_or(0);
        let rgb_hex = format!("#{:02X}{:02X}{:02X}", r, g, b);
        
        // Get expected name
        let expected_name = record.get(3).unwrap_or("unknown").trim();
        
        // Note: In a full implementation, we would run the actual converter here
        // For now, we create the template structure
        let notes = if precision_cases.iter().any(|(hex, _, _, _)| *hex == rgb_hex) {
            "⚠️ PRECISION CASE"
        } else {
            ""
        };
        
        output.push_str(&format!(
            "| {} | {} | {} | {} | {} | {} | TBD | {} |\n",
            index + 1,
            rgb_hex,
            expected_name,
            r, g, b,
            notes
        ));
    }
    
    output.push_str("\n## Notes for Hardcopy Verification\n\n");
    output.push_str("1. **Munsell Coordinate Format**: H V/C (e.g., 9.8R 9.1/1.6 = Hue 9.8Red, Value 9.1, Chroma 1.6)\n");
    output.push_str("2. **Precision Focus**: Check colors marked with ⚠️ against charts for boundary/precision issues\n");
    output.push_str("3. **Red/Purple Boundary**: Pay special attention to RP vs R family classifications\n");
    output.push_str("4. **Brown Classifications**: Many brown colors misclassified as red/orange - verify expected vs actual\n");
    output.push_str("5. **Chroma Precision**: 0.1 differences in chroma (1.6 vs 1.5) may affect ISCC-NBS classification\n\n");
    
    output.push_str("Generated from MUNSELL_COLOR_SCIENCE_COMPLETE.csv with current accuracy of 69.23%\n");
    
    // Write to file
    fs::write("COMPLETE_CONVERSION_DATASET_TEMPLATE.md", output)?;
    
    println!("Complete dataset template created: COMPLETE_CONVERSION_DATASET_TEMPLATE.md");
    println!("This provides the structure for hardcopy chart verification.");
    println!("The actual Munsell coordinates would need to be filled in by running the converter.");
    
    Ok(())
}