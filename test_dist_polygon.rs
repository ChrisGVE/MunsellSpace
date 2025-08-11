use munsellspace::iscc::IsccNbsClassifier;
use munsellspace::MunsellConverter;

fn main() {
    println!("Testing Dist polygon functionality...\n");
    
    // Create converter and classifier
    let converter = MunsellConverter::new();
    let classifier = IsccNbsClassifier::new()
        .expect("Failed to create ISCC-NBS classifier");
    
    // Test case 1: Color that should have a polygon in same wedge
    let rgb1 = [255, 179, 179]; // Light pinkish
    let munsell1 = converter.convert_rgb(rgb1).unwrap();
    println!("Test 1: RGB {:?} -> Munsell: {}", rgb1, munsell1);
    
    // Get ISCC-NBS classification
    let iscc1 = classifier.classify(&munsell1.to_string());
    println!("  ISCC-NBS: {:?}", iscc1);
    
    // Try to find polygon in wedge for "pale pink"  
    if let Ok(parsed) = munsell1.to_string().parse::<munsellspace::MunsellColor>() {
        let hue = format!("{}{}", parsed.hue_number, parsed.hue_family);
        println!("  Hue: {}", hue);
        
        if let Some(polygon) = classifier.get_polygon_in_wedge(&hue, "pale pink") {
            println!("  ✅ Found polygon for 'pale pink' in wedge!");
            println!("  Polygon: {} {}", polygon.descriptor, polygon.color_name);
        } else {
            println!("  ❌ No polygon found for 'pale pink' in wedge");
        }
    }
    
    println!("\nTest 2: Checking wedge detection...");
    // Test wedge detection directly
    let test_hue = "5.2R";
    println!("  Hue {} -> Wedge: {:?}", test_hue, 
        classifier.wedge_system.find_wedge_for_hue(test_hue));
}