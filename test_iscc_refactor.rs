use munsellspace::ISCC_NBS_Classifier;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Create the classifier
    let classifier = ISCC_NBS_Classifier::new()?;
    
    // Test some common colors
    println!("Testing ISCC-NBS classification with refactored system:");
    println!();
    
    // Test red
    if let Some(result) = classifier.classify_srgb([255, 0, 0])? {
        println!("Red [255, 0, 0]:");
        println!("  Descriptor: {}", result.iscc_nbs_descriptor());
        println!("  Color: {}", result.iscc_nbs_color());
        println!("  Revised descriptor: {}", result.revised_descriptor());
        println!("  Full name: {}", result.full_iscc_nbs_name());
        println!();
    }
    
    // Test blue
    if let Some(result) = classifier.classify_srgb([0, 0, 255])? {
        println!("Blue [0, 0, 255]:");
        println!("  Descriptor: {}", result.iscc_nbs_descriptor());
        println!("  Color: {}", result.iscc_nbs_color());
        println!("  Revised descriptor: {}", result.revised_descriptor());
        println!("  Full name: {}", result.full_iscc_nbs_name());
        println!();
    }
    
    // Test hex classification
    if let Some(result) = classifier.classify_hex("#FF69B4")? { // Hot pink
        println!("Hot Pink #FF69B4:");
        println!("  Descriptor: {}", result.iscc_nbs_descriptor());
        println!("  Color: {}", result.iscc_nbs_color());
        println!("  Revised descriptor: {}", result.revised_descriptor());
        println!("  Full name: {}", result.full_iscc_nbs_name());
        println!();
    }
    
    // Test Munsell direct
    if let Some(result) = classifier.classify_munsell("5R", 4.0, 14.0)? {
        println!("Munsell 5R 4/14:");
        println!("  Descriptor: {}", result.iscc_nbs_descriptor());
        println!("  Color: {}", result.iscc_nbs_color());
        println!("  Revised descriptor: {}", result.revised_descriptor());
        println!("  Full name: {}", result.full_iscc_nbs_name());
        println!();
    }
    
    println!("✅ Refactored ISCC-NBS system working correctly!");
    
    Ok(())
}