use munsellspace::IsccNbsClassifier;

#[test]
fn debug_available_plane_keys() {
    println!("=== DEBUGGING AVAILABLE PLANE KEYS ===");
    
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    
    // We can't access private fields directly, so let's test some specific lookups
    // and try to understand the plane key structure
    
    let test_cases = vec![
        ("4.5R", 7.0, 7.7, "Should work - found in previous test"),
        ("9.4R", 8.6, 3.5, "Failing case"),
        ("7.6R", 7.3, 4.7, "Failing case"),
        ("8Y", 9.2, 1.1, "Failing case"),
        ("10YR", 7.4, 1.1, "Failing case"),
        ("5R", 5.0, 10.0, "Standard case"),
        ("1R", 3.0, 8.0, "Standard case"),
        ("1YR", 5.0, 6.0, "Standard case"),
        ("1Y", 5.0, 6.0, "Standard case"),
    ];
    
    let mut working_cases = Vec::new();
    let mut failing_cases = Vec::new();
    
    for (hue, value, chroma, description) in test_cases {
        println!("\nTesting: {} {:.1}/{:.1} ({})", hue, value, chroma, description);
        
        match classifier.classify_munsell(hue, value, chroma) {
            Ok(Some(result)) => {
                println!("  ✅ FOUND: {}", result.revised_descriptor());
                working_cases.push((hue, value, chroma));
            }
            Ok(None) => {
                println!("  ❌ NO CLASSIFICATION found");
                failing_cases.push((hue, value, chroma));
            }
            Err(e) => {
                println!("  ❌ ERROR: {}", e);
                failing_cases.push((hue, value, chroma));
            }
        }
    }
    
    println!("\n=== SUMMARY ===");
    println!("Working cases: {}/{}", working_cases.len(), working_cases.len() + failing_cases.len());
    println!("Failing cases: {}/{}", failing_cases.len(), working_cases.len() + failing_cases.len());
    
    if !working_cases.is_empty() {
        println!("\n✅ Working hues:");
        for (hue, _, _) in working_cases {
            println!("  - {}", hue);
        }
    }
    
    if !failing_cases.is_empty() {
        println!("\n❌ Failing hues:");
        for (hue, _, _) in failing_cases {
            println!("  - {}", hue);
        }
    }
}