use munsellspace::python_port::{xy_from_renotation_ovoid_interpolated};

fn main() {
    // Test if we can handle [7.123, 9.277, 2.0, 3]
    let spec = [7.123, 9.277, 2.0, 3.0];
    
    println!("Testing spec: [{:.3}, {:.3}, {:.1}, {}]", spec[0], spec[1], spec[2], spec[3] as i32);
    
    match xy_from_renotation_ovoid_interpolated(&spec) {
        Ok(xy) => {
            println!("SUCCESS! xy = ({:.6}, {:.6})", xy[0], xy[1]);
        }
        Err(e) => {
            println!("FAILED: {}", e);
            println!("This is why we fall back to integer values!");
            
            // Try with integer value
            let fallback_spec = [7.123, 9.0, 2.0, 3.0];
            println!("\nTrying fallback spec: [{:.3}, {:.1}, {:.1}, {}]", 
                fallback_spec[0], fallback_spec[1], fallback_spec[2], fallback_spec[3] as i32);
            
            match xy_from_renotation_ovoid_interpolated(&fallback_spec) {
                Ok(xy) => {
                    println!("Fallback SUCCESS: xy = ({:.6}, {:.6})", xy[0], xy[1]);
                }
                Err(e) => {
                    println!("Fallback also FAILED: {}", e);
                }
            }
        }
    }
    
    // Also test the exact spec Python gets
    let python_spec = [7.1207827853, 9.2774063954, 2.0837109549, 3.0];
    println!("\nTesting Python's exact spec: [{:.10}, {:.10}, {:.10}, {}]", 
        python_spec[0], python_spec[1], python_spec[2], python_spec[3] as i32);
    
    match xy_from_renotation_ovoid_interpolated(&python_spec) {
        Ok(xy) => {
            println!("Python spec SUCCESS: xy = ({:.6}, {:.6})", xy[0], xy[1]);
        }
        Err(e) => {
            println!("Python spec FAILED: {}", e);
        }
    }
}