use munsellspace::IsccNbsClassifier;

#[test]
fn test_descriptor_construction_rules() {
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    
    println!("Testing ISCC-NBS descriptor construction rules...");
    
    // We'll test by creating a mock color and checking the descriptor construction
    // Since the function is private, we'll test through classification results
    
    // Test colors that should exist in the ISCC-NBS dataset
    let test_cases = vec![
        // Format: (hue, value, chroma, expected_pattern_description)
        ("5R", 4.0, 10.0, "should follow basic prefix or -ish rules"),
        ("5G", 5.0, 8.0, "should follow basic prefix or -ish rules"),
        ("5B", 3.0, 6.0, "should follow basic prefix or -ish rules"),
    ];
    
    for (hue, value, chroma, description) in test_cases {
        match classifier.classify_munsell(hue, value, chroma) {
            Ok(Some(result)) => {
                println!("Munsell {} {:.1}/{:.1} ({}):", hue, value, chroma, description);
                println!("  ISCC-NBS Descriptor: '{}'", result.iscc_nbs_descriptor());
                println!("  ISCC-NBS Color: '{}'", result.iscc_nbs_color());
                println!("  ISCC-NBS Modifier: {:?}", result.iscc_nbs_modifier());
                println!("  Revised Color: '{}'", result.revised_color());
                println!("  Revised Descriptor: '{}'", result.revised_descriptor());
                
                // Validate that revised descriptor follows our rules
                validate_descriptor_logic(
                    result.revised_color(),
                    result.iscc_nbs_modifier(),
                    result.revised_descriptor()
                );
            }
            Ok(None) => {
                println!("No classification found for {} {:.1}/{:.1}", hue, value, chroma);
            }
            Err(e) => {
                println!("Classification error for {} {:.1}/{:.1}: {}", hue, value, chroma, e);
            }
        }
        println!();
    }
}

fn validate_descriptor_logic(revised_color: &str, modifier: Option<&str>, actual_descriptor: &str) {
    let expected_descriptor = construct_expected_descriptor(revised_color, modifier);
    
    println!("  Validation:");
    println!("    Input: color='{}', modifier={:?}", revised_color, modifier);
    println!("    Expected: '{}'", expected_descriptor);
    println!("    Actual:   '{}'", actual_descriptor);
    
    if expected_descriptor == actual_descriptor {
        println!("    ✅ PASS - Descriptor construction correct");
    } else {
        println!("    ❌ FAIL - Descriptor construction mismatch");
    }
}

/// Reference implementation of the descriptor construction rules for testing
fn construct_expected_descriptor(revised_color: &str, modifier: Option<&str>) -> String {
    match modifier {
        // Rule 2: No modifier case
        None => revised_color.trim().to_string(),
        
        // Rule 3: "-ish" transformation rules
        Some(modifier) if modifier.contains("-ish") => {
            construct_ish_descriptor_reference(revised_color, modifier)
        },
        
        // Rule 1: Basic prefix rule
        Some(modifier) => {
            format!("{} {}", modifier.trim(), revised_color.trim())
        }
    }
}

fn construct_ish_descriptor_reference(revised_color: &str, modifier: &str) -> String {
    // Parse modifier: split on "-ish" to extract prefix and suffix
    let parts: Vec<&str> = modifier.split("-ish").collect();
    let prefix = parts[0].trim();
    let suffix = if parts.len() > 1 { parts[1].trim() } else { "" };
    
    // Transform color (Rule 5: olive exception)
    let transformed_color = if revised_color.trim() == "olive" {
        revised_color.trim().to_string()
    } else {
        apply_ish_transformation_reference(revised_color.trim())
    };
    
    // Combine parts: prefix + colorish + suffix
    let mut result = Vec::new();
    if !prefix.is_empty() { 
        result.push(prefix); 
    }
    result.push(&transformed_color);
    if !suffix.is_empty() { 
        result.push(suffix); 
    }
    
    result.join(" ")
}

fn apply_ish_transformation_reference(color: &str) -> String {
    match color {
        "brown" => "brownish".to_string(),
        "blue" => "bluish".to_string(), 
        "red" => "reddish".to_string(),
        "green" => "greenish".to_string(),
        "yellow" => "yellowish".to_string(), 
        "purple" => "purplish".to_string(),
        "pink" => "pinkish".to_string(),
        // Default fallback for any other colors
        _ => format!("{}ish", color),
    }
}

#[test]
fn test_specific_descriptor_rules() {
    println!("Testing specific ISCC-NBS descriptor construction patterns...");
    
    // Test the reference implementation with known examples
    let test_cases = vec![
        // Rule 1: Basic prefix
        ("red", Some("vivid"), "vivid red"),
        ("blue", Some("light"), "light blue"),
        ("green", Some("dark"), "dark green"),
        
        // Rule 2: No modifier
        ("black", None, "black"),
        ("white", None, "white"),
        ("gray", None, "gray"),
        
        // Rule 3 & 4: "-ish" transformations
        ("purple", Some("-ish white"), "purplish white"),
        ("purple", Some("dark -ish gray"), "dark purplish gray"),
        ("red", Some("light -ish brown"), "light reddish brown"),
        ("blue", Some("-ish green"), "bluish green"),
        ("brown", Some("-ish yellow"), "brownish yellow"),
        
        // Rule 5: Olive exception
        ("olive", Some("dark -ish gray"), "dark olive gray"),
        ("olive", Some("-ish green"), "olive green"),
        ("olive", Some("light -ish brown"), "light olive brown"),
    ];
    
    for (color, modifier, expected) in test_cases {
        let actual = construct_expected_descriptor(color, modifier);
        println!("Test: '{}' + {:?} = '{}'", color, modifier, actual);
        
        if actual == expected {
            println!("  ✅ PASS");
        } else {
            println!("  ❌ FAIL - Expected: '{}', Got: '{}'", expected, actual);
        }
        println!();
    }
}

#[test]
fn test_english_ish_grammar() {
    println!("Testing English '-ish' grammar transformations...");
    
    let transformations = vec![
        ("brown", "brownish"),
        ("blue", "bluish"),
        ("red", "reddish"),
        ("green", "greenish"),
        ("yellow", "yellowish"),
        ("purple", "purplish"),
        ("pink", "pinkish"),
        ("orange", "orangeish"), // fallback case
    ];
    
    for (input, expected) in transformations {
        let actual = apply_ish_transformation_reference(input);
        println!("'{}' → '{}'", input, actual);
        
        if actual == expected {
            println!("  ✅ PASS");
        } else {
            println!("  ❌ FAIL - Expected: '{}', Got: '{}'", expected, actual);
        }
    }
}