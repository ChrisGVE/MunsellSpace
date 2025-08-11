use std::collections::HashMap;

fn main() {
    println!("Testing Dist polygon calculation...\n");
    
    // Create the ISCC-NBS classifier
    let classifier = munsellspace::iscc::ISCC_NBS_Classifier::new()
        .expect("Failed to create classifier");
    
    // Test cases
    let test_cases = vec![
        ("5.2R 4.5/12.0", "deep red"),
        ("2.5YR 6.0/10.0", "strong orange"),
        ("7.5Y 8.5/9.0", "brilliant yellow"),
        ("5.0G 5.0/6.0", "moderate green"),
        ("10.0B 4.0/8.0", "strong blue"),
    ];
    
    println!("Testing polygon distance calculations:\n");
    println!("{:<20} {:<20} {:<30}", "Munsell", "Expected", "Distance to Polygon");
    println!("{}", "-".repeat(70));
    
    for (munsell, expected) in test_cases {
        let dist = calculate_distance_to_correct_polygon(munsell, expected, &classifier);
        println!("{:<20} {:<20} {:<30}", munsell, expected, dist);
    }
}

/// Parse Munsell notation like "5.2R 4.5/12.0" into components
fn parse_munsell_notation(notation: &str) -> Option<(String, f64, f64)> {
    let parts: Vec<&str> = notation.split_whitespace().collect();
    if parts.len() != 2 {
        return None;
    }
    
    let hue = parts[0];
    let vc_parts: Vec<&str> = parts[1].split('/').collect();
    if vc_parts.len() != 2 {
        return None;
    }
    
    let value = vc_parts[0].parse::<f64>().ok()?;
    let chroma = vc_parts[1].parse::<f64>().ok()?;
    
    Some((hue.to_string(), value, chroma))
}

/// Calculate distance to the correct polygon for the expected color
fn calculate_distance_to_correct_polygon(
    rust_munsell: &str,
    expected_name: &str,
    classifier: &munsellspace::iscc::ISCC_NBS_Classifier
) -> String {
    // Parse the Rust Munsell notation
    let (rust_hue, rust_value, rust_chroma) = match parse_munsell_notation(rust_munsell) {
        Some(parsed) => parsed,
        None => return String::new(),
    };
    
    // Handle neutral colors
    if rust_hue == "N" {
        return String::new();
    }
    
    // Get the polygon for the expected descriptor in the same wedge
    let polygon = match classifier.get_polygon_in_wedge(&rust_hue, expected_name) {
        Some(p) => p,
        None => return format!("No polygon for '{}' in wedge", expected_name),
    };
    
    // Calculate the distance from the point to the polygon
    let (value_dist, chroma_dist) = calculate_polygon_distance(
        rust_value,
        rust_chroma,
        &polygon.polygon
    );
    
    // Format the result - show signed distances
    if value_dist.abs() < 0.01 && chroma_dist.abs() < 0.01 {
        "(0.0, 0.0)".to_string() // Point is inside or on the boundary
    } else {
        format!("({:+.1}, {:+.1})", value_dist, chroma_dist)
    }
}

/// Calculate the shortest distance from a point to a polygon boundary
fn calculate_polygon_distance(
    point_value: f64, 
    point_chroma: f64,
    target_polygon: &geo::Polygon<f64>
) -> (f64, f64) {
    use geo::{Point, Contains, LineString, Line};
    use geo::algorithm::EuclideanDistance;
    
    let test_point = Point::new(point_chroma, point_value); // Note: geo uses (x,y) = (chroma, value)
    
    // Check if point is inside polygon
    if target_polygon.contains(&test_point) {
        return (0.0, 0.0); // Already inside
    }
    
    // Find the closest point on the polygon boundary
    let exterior = target_polygon.exterior();
    let mut min_distance = f64::MAX;
    let mut closest_point = test_point;
    
    // Check each edge of the polygon
    for line in exterior.lines() {
        // Get the closest point on this line segment to our test point
        let line_string = LineString::from(vec![line.start, line.end]);
        
        // Calculate point-to-line distance
        for coord in line_string.coords() {
            let boundary_point = Point::new(coord.x, coord.y);
            let dist = test_point.euclidean_distance(&boundary_point);
            
            if dist < min_distance {
                min_distance = dist;
                closest_point = boundary_point;
            }
        }
        
        // Also check projection onto line segment
        let (x1, y1) = (line.start.x, line.start.y);
        let (x2, y2) = (line.end.x, line.end.y);
        let (px, py) = (test_point.x(), test_point.y());
        
        // Vector from line start to end
        let dx = x2 - x1;
        let dy = y2 - y1;
        
        // Parameter t for projection
        let t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy);
        let t_clamped = t.max(0.0).min(1.0);
        
        // Projected point
        let proj_x = x1 + t_clamped * dx;
        let proj_y = y1 + t_clamped * dy;
        let projected = Point::new(proj_x, proj_y);
        
        let dist = test_point.euclidean_distance(&projected);
        if dist < min_distance {
            min_distance = dist;
            closest_point = projected;
        }
    }
    
    // Return signed distances in Value and Chroma
    let value_dist = closest_point.y() - test_point.y();  // Value difference
    let chroma_dist = closest_point.x() - test_point.x(); // Chroma difference
    
    (value_dist, chroma_dist)
}