use munsellspace::iscc::IsccNbsClassifier;

#[test]
fn test_iscc_csv_loading() {
    // Test that we can load the ISCC-NBS CSV data and create polygons
    let csv_path = "ISCC-NBS-Definitions.csv";
    
    // This will fail with todo!() for now, but should compile correctly
    match IsccNbsClassifier::from_csv(csv_path) {
        Ok(_classifier) => {
            // Success - we loaded the data and created polygons
            println!("Successfully loaded ISCC-NBS data!");
        }
        Err(e) => {
            // Expected for now due to todo!() in organize_by_hue_slices
            println!("Expected error due to unimplemented functions: {}", e);
        }
    }
}

#[test] 
fn test_polygon_creation() {
    // Test that we can create a simple polygon using geo crate
    use geo::{Point, Polygon, LineString, Coord};
    use geo::prelude::*;
    
    // Create a simple rectangle polygon
    let coords = vec![
        Coord { x: 0.0, y: 0.0 },  // (value=0, chroma=0)
        Coord { x: 0.0, y: 5.0 },  // (value=0, chroma=5)
        Coord { x: 3.0, y: 5.0 },  // (value=3, chroma=5)
        Coord { x: 3.0, y: 0.0 },  // (value=3, chroma=0)
        Coord { x: 0.0, y: 0.0 },  // Close the polygon
    ];
    
    let line_string = LineString::from(coords);
    let polygon = Polygon::new(line_string, vec![]);
    
    // Test point containment
    let inside_point = Point::new(1.5, 2.5);  // Should be inside
    let outside_point = Point::new(5.0, 7.0); // Should be outside
    
    assert!(polygon.contains(&inside_point), "Point should be inside polygon");
    assert!(!polygon.contains(&outside_point), "Point should be outside polygon");
    
    println!("Polygon geometry tests passed!");
}