use geo::{Polygon, Point, Coordinate, LineString};
use geo::{Contains, Intersects};

fn main() {
    // Color 182 polygon 2: 5PB-7PB (value 5-9, chroma 3-5.5)
    let poly182_coords = vec![
        Coordinate { x: 3.0, y: 5.0 },   // bottom-left
        Coordinate { x: 4.5, y: 5.0 },   // bottom-middle  
        Coordinate { x: 4.5, y: 7.0 },   // middle
        Coordinate { x: 5.5, y: 7.0 },   // right-middle
        Coordinate { x: 5.5, y: 9.0 },   // top-right
        Coordinate { x: 3.0, y: 9.0 },   // top-left
    ];
    
    // Color 199 polygon 1: 5PB-7PB (value 5-7, chroma 4.5-7.5)
    let poly199_coords = vec![
        Coordinate { x: 4.5, y: 5.0 },   // bottom-left
        Coordinate { x: 7.5, y: 5.0 },   // bottom-right
        Coordinate { x: 7.5, y: 7.0 },   // top-right
        Coordinate { x: 4.5, y: 7.0 },   // top-left
    ];
    
    let poly182 = Polygon::new(LineString::from(poly182_coords), vec![]);
    let poly199 = Polygon::new(LineString::from(poly199_coords), vec![]);
    
    // Test points
    let test_points = vec![
        (5.5f64, 7.0f64, "5.5/7"),  // value=5.5, chroma=7
        (5.0f64, 7.0f64, "5.0/7"),  // value=5.0, chroma=7
    ];
    
    for (value, chroma, label) in test_points {
        let point = Point::new(chroma, value);  // geo uses (x=chroma, y=value)
        
        println!("\nPoint {} (value={}, chroma={}):", label, value, chroma);
        println!("  Color 182:");
        println!("    Contains: {}", poly182.contains(&point));
        println!("    On boundary: {}", poly182.exterior().intersects(&point));
        
        println!("  Color 199:");
        println!("    Contains: {}", poly199.contains(&point));
        println!("    On boundary: {}", poly199.exterior().intersects(&point));
        
        // Check segments for 182
        println!("\n  Segments for Color 182:");
        let coords182: Vec<_> = poly182.exterior().coords().cloned().collect();
        for i in 0..coords182.len() - 1 {
            let p1 = coords182[i];
            let p2 = coords182[i + 1];
            
            // Check horizontal segments at this value
            if (p1.y - value).abs() < 1e-10 && (p2.y - value).abs() < 1e-10 {
                let min_x = p1.x.min(p2.x);
                let max_x = p1.x.max(p2.x);
                if chroma >= min_x - 1e-10 && chroma <= max_x + 1e-10 {
                    println!("    Horizontal segment: chroma [{}, {}]", min_x, max_x);
                }
            }
            
            // Check vertical segments at this chroma
            if (p1.x - chroma).abs() < 1e-10 && (p2.x - chroma).abs() < 1e-10 {
                let min_y = p1.y.min(p2.y);
                let max_y = p1.y.max(p2.y);
                if value >= min_y - 1e-10 && value <= max_y + 1e-10 {
                    println!("    Vertical segment: value [{}, {}]", min_y, max_y);
                }
            }
        }
        
        // Check segments for 199
        println!("\n  Segments for Color 199:");
        let coords199: Vec<_> = poly199.exterior().coords().cloned().collect();
        for i in 0..coords199.len() - 1 {
            let p1 = coords199[i];
            let p2 = coords199[i + 1];
            
            // Check horizontal segments at this value
            if (p1.y - value).abs() < 1e-10 && (p2.y - value).abs() < 1e-10 {
                let min_x = p1.x.min(p2.x);
                let max_x = p1.x.max(p2.x);
                if chroma >= min_x - 1e-10 && chroma <= max_x + 1e-10 {
                    println!("    Horizontal segment: chroma [{}, {}]", min_x, max_x);
                }
            }
            
            // Check vertical segments at this chroma  
            if (p1.x - chroma).abs() < 1e-10 && (p2.x - chroma).abs() < 1e-10 {
                let min_y = p1.y.min(p2.y);
                let max_y = p1.y.max(p2.y);
                if value >= min_y - 1e-10 && value <= max_y + 1e-10 {
                    println!("    Vertical segment: value [{}, {}]", min_y, max_y);
                }
            }
        }
    }
}