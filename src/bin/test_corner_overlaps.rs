use geo::{Polygon, Point, Coordinate, LineString};
use geo::Contains;

fn main() {
    println!("Testing corner overlap cases\n");
    println!("=============================\n");
    
    // Test Case 1: Colors 39 and 53 at point (6.5/7.0) in wedge 3YR
    println!("Case 1: Colors 39 and 53 at (6.5/7.0) in wedge 3YR");
    println!("----------------------------------------------------");
    
    // Color 39 polygon 1.3: corners at (5,4.5), (5,6.5), (7,6.5), (7,4.5)
    let poly39_coords = vec![
        Coordinate { x: 4.5, y: 5.0 },   // (V=5, C=4.5)
        Coordinate { x: 6.5, y: 5.0 },   // (V=5, C=6.5)
        Coordinate { x: 6.5, y: 7.0 },   // (V=7, C=6.5)
        Coordinate { x: 4.5, y: 7.0 },   // (V=7, C=4.5)
        Coordinate { x: 4.5, y: 5.0 },   // close
    ];
    
    // Color 53 polygon 1.2: corners at (7,5.5), (7,6.5), (6,6.5), (6,7.5), (10,7.5), (10,5.5)
    // But we need polygon that includes point at V=6.5, C=7
    // From data: 53,1.2 has (7,5.5) to (7,6.5) which means V=7, C=5.5 to C=6.5
    // But point is at V=6.5, C=7... let me recalculate
    
    // Actually, looking at the CSV format: it's value,chroma pairs
    // 53,1.2: "7,6.5" means the corner is at value=7, chroma=6.5
    // But our test point is (6.5/7.0) which means value=6.5, chroma=7.0
    
    // Let me reconstruct based on the actual data
    // Color 39 polygon 1: hue 8R-3YR, corners: (5,4.5), (5,6.5), (7,6.5), (7,4.5)
    let poly39_v1_coords = vec![
        Coordinate { x: 4.5, y: 5.0 },
        Coordinate { x: 6.5, y: 5.0 },
        Coordinate { x: 6.5, y: 7.0 },
        Coordinate { x: 4.5, y: 7.0 },
        Coordinate { x: 4.5, y: 5.0 },
    ];
    
    // Color 53 polygon 1: hue 2YR-3YR
    // From CSV: corners at (7,5.5), (7,6.5), (6,6.5), (6,7.5), (10,7.5), (10,5.5)
    let poly53_v1_coords = vec![
        Coordinate { x: 5.5, y: 7.0 },
        Coordinate { x: 6.5, y: 7.0 },
        Coordinate { x: 6.5, y: 6.0 },
        Coordinate { x: 7.5, y: 6.0 },
        Coordinate { x: 7.5, y: 10.0 },
        Coordinate { x: 5.5, y: 10.0 },
        Coordinate { x: 5.5, y: 7.0 },
    ];
    
    let poly39 = Polygon::new(LineString::from(poly39_v1_coords), vec![]);
    let poly53 = Polygon::new(LineString::from(poly53_v1_coords), vec![]);
    
    let test_point = Point::new(7.0, 6.5);  // (chroma=7.0, value=6.5)
    
    println!("Test point: V=6.5, C=7.0 -> Point(x=7.0, y=6.5)");
    println!("\nColor 39 polygon:");
    print_polygon_info(&poly39, &test_point);
    println!("\nColor 53 polygon:");
    print_polygon_info(&poly53, &test_point);
    
    // Apply boundary rules
    println!("\nBoundary rule analysis:");
    analyze_boundary_rules(&poly39, &test_point, 39);
    analyze_boundary_rules(&poly53, &test_point, 53);
    
    println!("\n");
    
    // Test Case 2: Colors 65 and 96 at point (1.5/1.0)
    println!("Case 2: Colors 65 and 96 at (1.5/1.0)");
    println!("---------------------------------------");
    
    // Color 65: corners at (0.5,0), (0.5,1.5), (1,1.5), (1,0)
    let poly65_coords = vec![
        Coordinate { x: 0.0, y: 0.5 },
        Coordinate { x: 1.5, y: 0.5 },
        Coordinate { x: 1.5, y: 1.0 },
        Coordinate { x: 0.0, y: 1.0 },
        Coordinate { x: 0.0, y: 0.5 },
    ];
    
    // Color 96: corners at (1,0), (1,1.5), (0.5,1.5), (0.5,2.5), (50,2.5), (50,0)
    // Note: 50 is likely a typo for 5.0
    let poly96_coords = vec![
        Coordinate { x: 0.0, y: 1.0 },
        Coordinate { x: 1.5, y: 1.0 },
        Coordinate { x: 1.5, y: 0.5 },
        Coordinate { x: 2.5, y: 0.5 },
        Coordinate { x: 2.5, y: 5.0 },  // Assuming 50 is typo for 5.0
        Coordinate { x: 0.0, y: 5.0 },
        Coordinate { x: 0.0, y: 1.0 },
    ];
    
    let poly65 = Polygon::new(LineString::from(poly65_coords), vec![]);
    let poly96 = Polygon::new(LineString::from(poly96_coords), vec![]);
    
    let test_point2 = Point::new(1.0, 1.5);  // (chroma=1.0, value=1.5)
    
    println!("Test point: V=1.5, C=1.0 -> Point(x=1.0, y=1.5)");
    println!("\nColor 65 polygon:");
    print_polygon_info(&poly65, &test_point2);
    println!("\nColor 96 polygon:");
    print_polygon_info(&poly96, &test_point2);
    
    // Apply boundary rules
    println!("\nBoundary rule analysis:");
    analyze_boundary_rules(&poly65, &test_point2, 65);
    analyze_boundary_rules(&poly96, &test_point2, 96);
}

fn print_polygon_info(poly: &Polygon<f64>, point: &Point<f64>) {
    let coords: Vec<_> = poly.exterior().coords().collect();
    println!("  Vertices: {:?}", coords);
    println!("  Contains point (geo): {}", poly.contains(point));
    
    // Check if point is on boundary
    let on_boundary = poly.exterior().coords().any(|coord| {
        (coord.x - point.x()).abs() < 1e-10 && (coord.y - point.y()).abs() < 1e-10
    });
    println!("  Point is vertex: {}", on_boundary);
}

fn analyze_boundary_rules(poly: &Polygon<f64>, point: &Point<f64>, color_id: u16) {
    let coords: Vec<_> = poly.exterior().coords().cloned().collect();
    let (chroma, value) = (point.x(), point.y());
    
    println!("  Color {}:", color_id);
    
    // Find horizontal and vertical ranges at this point
    let mut h_min = None::<f64>;
    let mut h_max = None::<f64>;
    let mut v_min = None::<f64>;
    let mut v_max = None::<f64>;
    
    for i in 0..coords.len() - 1 {
        let p1 = coords[i];
        let p2 = coords[i + 1];
        
        // Check horizontal segments at this value
        if (p1.y - value).abs() < 1e-10 && (p2.y - value).abs() < 1e-10 {
            let min_x = p1.x.min(p2.x);
            let max_x = p1.x.max(p2.x);
            h_min = Some(h_min.map_or(min_x, |m| m.min(min_x)));
            h_max = Some(h_max.map_or(max_x, |m| m.max(max_x)));
        }
        
        // Check vertical segments at this chroma
        if (p1.x - chroma).abs() < 1e-10 && (p2.x - chroma).abs() < 1e-10 {
            let min_y = p1.y.min(p2.y);
            let max_y = p1.y.max(p2.y);
            v_min = Some(v_min.map_or(min_y, |m| m.min(min_y)));
            v_max = Some(v_max.map_or(max_y, |m| m.max(max_y)));
        }
    }
    
    if let (Some(c_min), Some(c_max)) = (h_min, h_max) {
        println!("    Horizontal segment: chroma [{}, {}]", c_min, c_max);
        let in_chroma = if c_min == 0.0 {
            println!("    Chroma rule: [0, {}] (closed)", c_max);
            chroma >= c_min && chroma <= c_max
        } else {
            println!("    Chroma rule: ({}, {}] (half-open)", c_min, c_max);
            chroma > c_min && chroma <= c_max
        };
        println!("    Chroma {} is in range: {}", chroma, in_chroma);
    } else {
        println!("    No horizontal segment at value {}", value);
    }
    
    if let (Some(v_min), Some(v_max)) = (v_min, v_max) {
        println!("    Vertical segment: value [{}, {}]", v_min, v_max);
        let in_value = if v_min == 0.0 {
            println!("    Value rule: [0, {}] (closed)", v_max);
            value >= v_min && value <= v_max
        } else {
            println!("    Value rule: ({}, {}] (half-open)", v_min, v_max);
            value > v_min && value <= v_max
        };
        println!("    Value {} is in range: {}", value, in_value);
    } else {
        println!("    No vertical segment at chroma {}", chroma);
    }
}