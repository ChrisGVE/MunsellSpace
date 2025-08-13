use munsellspace::{ISCC_NBS_Classifier, MechanicalWedgeSystem};
use geo::{Polygon, Point, Coordinate, LineString};

fn main() {
    println!("Testing actual overlap cases with production code\n");
    println!("==================================================\n");
    
    // Initialize the classifier
    let classifier = ISCC_NBS_Classifier::new().unwrap();
    
    // Test Case 1: Point (6.5/7.0) in wedge 3YR
    println!("Case 1: Testing point V=6.5, C=7.0 in wedge 3YR");
    println!("------------------------------------------------");
    
    // This should be in wedge 3YR since we're testing hue 2.5YR
    let hue = "2.5YR";  // Clearly in wedge 3YR
    let value = 6.5;
    let chroma = 7.0;
    
    println!("Hue: {}, Value: {}, Chroma: {}", hue, value, chroma);
    
    // Find all colors at this point
    let colors = classifier.find_all_colors_at_point(hue, value, chroma).unwrap();
    println!("Colors found at this point: {:?}", colors);
    
    // Test with the mechanical wedge system directly
    let mut wedge_system = MechanicalWedgeSystem::new();
    
    // We need to populate it with test data for colors 39 and 53
    // First, create polygon for color 39 (hue range 8R-3YR)
    let poly39_coords = vec![
        Coordinate { x: 5.0, y: 4.5 },   // C=5, V=4.5
        Coordinate { x: 5.0, y: 6.5 },   // C=5, V=6.5
        Coordinate { x: 7.0, y: 6.5 },   // C=7, V=6.5
        Coordinate { x: 7.0, y: 4.5 },   // C=7, V=4.5
        Coordinate { x: 5.0, y: 4.5 },   // close
    ];
    let poly39 = Polygon::new(LineString::from(poly39_coords.clone()), vec![]);
    
    // Create polygon for color 53 (hue range 2YR-3YR)
    let poly53_coords = vec![
        Coordinate { x: 7.0, y: 5.5 },   // C=7, V=5.5
        Coordinate { x: 7.0, y: 6.5 },   // C=7, V=6.5
        Coordinate { x: 6.0, y: 6.5 },   // C=6, V=6.5
        Coordinate { x: 6.0, y: 7.5 },   // C=6, V=7.5
        Coordinate { x: 10.0, y: 7.5 },  // C=10, V=7.5
        Coordinate { x: 10.0, y: 5.5 },  // C=10, V=5.5
        Coordinate { x: 7.0, y: 5.5 },   // close
    ];
    let poly53 = Polygon::new(LineString::from(poly53_coords.clone()), vec![]);
    
    println!("\nPolygon analysis:");
    println!("Color 39 vertices: {:?}", poly39_coords);
    println!("Color 53 vertices: {:?}", poly53_coords);
    
    // Test the specific corner point
    let test_point = Point::new(7.0, 6.5);  // C=7.0, V=6.5
    println!("\nTesting point (C={}, V={}):", 7.0, 6.5);
    
    // Check containment with geo library
    use geo::Contains;
    println!("  Color 39 contains (geo): {}", poly39.contains(&test_point));
    println!("  Color 53 contains (geo): {}", poly53.contains(&test_point));
    
    // Check if point is exactly on a vertex
    let on_39_vertex = poly39_coords.iter().any(|c| (c.x - 7.0f64).abs() < 1e-10 && (c.y - 6.5f64).abs() < 1e-10);
    let on_53_vertex = poly53_coords.iter().any(|c| (c.x - 7.0f64).abs() < 1e-10 && (c.y - 6.5f64).abs() < 1e-10);
    println!("  On Color 39 vertex: {}", on_39_vertex);
    println!("  On Color 53 vertex: {}", on_53_vertex);
    
    println!("\n");
    
    // Test Case 2: Point (1.5/1.0) 
    println!("Case 2: Testing point V=1.5, C=1.0");
    println!("-----------------------------------");
    
    let hue2 = "2.5Y";  // Should be in wedges 2Y, 3Y
    let value2 = 1.5;
    let chroma2 = 1.0;
    
    println!("Hue: {}, Value: {}, Chroma: {}", hue2, value2, chroma2);
    
    // Find all colors at this point
    let colors2 = classifier.find_all_colors_at_point(hue2, value2, chroma2).unwrap();
    println!("Colors found at this point: {:?}", colors2);
    
    // Create polygons for colors 65 and 96
    // Color 65: 1YR-4Y
    let poly65_coords = vec![
        Coordinate { x: 0.5, y: 0.0 },   // C=0.5, V=0
        Coordinate { x: 0.5, y: 1.5 },   // C=0.5, V=1.5
        Coordinate { x: 1.0, y: 1.5 },   // C=1.0, V=1.5
        Coordinate { x: 1.0, y: 0.0 },   // C=1.0, V=0
        Coordinate { x: 0.5, y: 0.0 },   // close
    ];
    
    // Color 96: 1Y-4Y (note the typo in CSV: 50 should be 5.0)
    let poly96_coords = vec![
        Coordinate { x: 1.0, y: 0.0 },   // C=1.0, V=0
        Coordinate { x: 1.0, y: 1.5 },   // C=1.0, V=1.5
        Coordinate { x: 0.5, y: 1.5 },   // C=0.5, V=1.5
        Coordinate { x: 0.5, y: 2.5 },   // C=0.5, V=2.5
        Coordinate { x: 5.0, y: 2.5 },   // C=5.0 (not 50), V=2.5
        Coordinate { x: 5.0, y: 0.0 },   // C=5.0, V=0
        Coordinate { x: 1.0, y: 0.0 },   // close
    ];
    
    let poly65 = Polygon::new(LineString::from(poly65_coords.clone()), vec![]);
    let poly96 = Polygon::new(LineString::from(poly96_coords.clone()), vec![]);
    
    println!("\nPolygon analysis:");
    println!("Color 65 vertices: {:?}", poly65_coords);
    println!("Color 96 vertices: {:?}", poly96_coords);
    
    // Test the specific corner point
    let test_point2 = Point::new(1.0, 1.5);  // C=1.0, V=1.5
    println!("\nTesting point (C={}, V={}):", 1.0, 1.5);
    
    println!("  Color 65 contains (geo): {}", poly65.contains(&test_point2));
    println!("  Color 96 contains (geo): {}", poly96.contains(&test_point2));
    
    // Check if point is exactly on a vertex
    let on_65_vertex = poly65_coords.iter().any(|c| (c.x - 1.0f64).abs() < 1e-10 && (c.y - 1.5f64).abs() < 1e-10);
    let on_96_vertex = poly96_coords.iter().any(|c| (c.x - 1.0f64).abs() < 1e-10 && (c.y - 1.5f64).abs() < 1e-10);
    println!("  On Color 65 vertex: {}", on_65_vertex);
    println!("  On Color 96 vertex: {}", on_96_vertex);
    
    println!("\n====================================");
    println!("Summary:");
    println!("Both cases involve shared vertices where two polygons meet.");
    println!("The boundary rules need clarification for shared vertices.");
    println!("\nCurrent rule: ");
    println!("- If min=0: [0, max] closed");
    println!("- Otherwise: (min, max] half-open");
    println!("\nFor shared vertices, we need to determine which polygon 'owns' the vertex.");
}