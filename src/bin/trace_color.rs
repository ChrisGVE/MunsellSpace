//! Test binary to generate trace logs for color conversion
//! Converts xyY [0.3016555411, 0.3289901051, 0.8269331673] and saves trace

use munsellspace::traced_port;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Clear any existing trace
    traced_port::clear_trace();
    
    // Test color: xyY [0.3016555411, 0.3289901051, 0.8269331673]
    let xyy = [0.3016555411, 0.3289901051, 0.8269331673];
    
    println!("Converting xyY: [{:.10}, {:.10}, {:.10}]", xyy[0], xyy[1], xyy[2]);
    
    // Perform the conversion
    match traced_port::xyy_to_munsell_specification(xyy) {
        Ok(result) => {
            println!("Result: [{:.10}, {:.10}, {:.10}, {:.0}]", 
                     result[0], result[1], result[2], result[3]);
        }
        Err(e) => {
            println!("Error: {:?}", e);
        }
    }
    
    // Save the trace to file
    traced_port::save_trace_to_file("rust_trace_ddeeee.txt")?;
    println!("Trace saved to rust_trace_ddeeee.txt");
    
    // Print trace length for verification
    let trace = traced_port::get_trace();
    println!("Generated {} trace lines", trace.len());
    
    Ok(())
}