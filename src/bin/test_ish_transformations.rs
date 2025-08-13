/// Test program to verify "-ish" color transformations in ISCC-NBS naming
use munsellspace::ISCC_NBS_Classifier;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Testing ISCC-NBS '-ish' Color Transformations");
    println!("=============================================\n");
    
    let classifier = ISCC_NBS_Classifier::new()?;
    
    // Test cases from the CSV showing olive gray (not olivish gray)
    let test_cases = vec![
        // Olive cases - should remain "olive"
        ("8Y", 5.5, 1.0, "light olive gray"),  // Color 112
        ("8Y", 3.5, 1.0, "olive gray"),        // Color 113
        ("6Y", 0.75, 0.75, "olive black"),     // Color 114
        
        // Other -ish transformations
        ("2RP", 9.0, 0.75, "pinkish white"),   // Color 9
        ("2RP", 7.5, 0.75, "pinkish gray"),    // Color 10
        ("5R", 5.5, 1.0, "reddish gray"),      // Color 22
        ("5R", 3.5, 1.0, "dark reddish gray"), // Color 23
        ("4YR", 5.5, 1.0, "light brownish gray"), // Color 63
        ("3YR", 3.5, 1.0, "brownish gray"),    // Color 64
        ("8YR", 9.0, 1.0, "yellowish white"),  // Color 92
        ("8YR", 7.5, 1.0, "yellowish gray"),   // Color 93
        ("7GY", 9.0, 0.75, "greenish white"),  // Color 153
        ("7GY", 7.5, 0.75, "light greenish gray"), // Color 154
        ("7GY", 5.5, 0.75, "greenish gray"),   // Color 155
        ("5B", 9.0, 1.0, "bluish white"),      // Color 189
        ("5B", 7.5, 1.0, "light bluish gray"), // Color 190
        ("5B", 5.5, 1.0, "bluish gray"),       // Color 191
        ("4PB", 9.0, 1.0, "purplish white"),   // Color 231
        ("4PB", 7.5, 1.0, "light purplish gray"), // Color 232
        ("4PB", 5.5, 1.0, "purplish gray"),    // Color 233
    ];
    
    println!("Testing specific color transformations:");
    println!("---------------------------------------");
    
    let mut correct = 0;
    let mut total = 0;
    
    for (hue, value, chroma, expected_name) in test_cases {
        total += 1;
        match classifier.classify_munsell(hue, value, chroma) {
            Ok(Some(result)) => {
                let name = &result.revised_descriptor;
                
                let status = if name == expected_name {
                    correct += 1;
                    "✓"
                } else {
                    "✗"
                };
                
                println!("{} {} {}/{} → {} (expected: {})",
                    status, hue, value, chroma, name, expected_name);
            },
            Ok(None) => {
                println!("✗ {} {}/{} → No match (expected: {})",
                    hue, value, chroma, expected_name);
            },
            Err(e) => {
                println!("✗ {} {}/{} → Error: {} (expected: {})",
                    hue, value, chroma, e, expected_name);
            }
        }
    }
    
    println!("\n---------------------------------------");
    println!("Results: {}/{} correct ({:.1}%)", 
        correct, total, (correct as f64 / total as f64) * 100.0);
    
    // Test the transformation function directly (if we could access it)
    println!("\n\nConversion Dictionary Summary:");
    println!("------------------------------");
    println!("Standard -ish transformations:");
    println!("  brown → brownish");
    println!("  blue → bluish");
    println!("  red → reddish");
    println!("  green → greenish");
    println!("  yellow → yellowish");
    println!("  purple → purplish");
    println!("  pink → pinkish");
    println!("  orange → orangish");
    println!("  gray → grayish");
    println!("  grey → greyish");
    println!("\nSpecial cases (no -ish):");
    println!("  olive → olive (NOT olivish)");
    println!("  white → whitish (rarely used)");
    println!("  black → blackish (rarely used)");
    
    Ok(())
}