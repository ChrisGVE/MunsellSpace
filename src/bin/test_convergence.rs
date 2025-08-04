use munsellspace::mathematical::MathematicalMunsellConverter;

fn main() {
    println!("Testing convergence on sample colors...\n");
    
    let converter = MathematicalMunsellConverter::new().unwrap();
    
    // Test cases
    let test_cases = vec![
        ([128, 128, 128], "Medium gray"),
        ([255, 0, 0], "Pure red"),
        ([0, 255, 0], "Pure green"),
        ([0, 0, 255], "Pure blue"),
        ([255, 255, 255], "White"),
        ([0, 0, 0], "Black"),
        ([128, 64, 32], "Brown"),
    ];
    
    let mut success_count = 0;
    let mut total_time = std::time::Duration::ZERO;
    
    for (rgb, label) in test_cases.iter() {
        print!("{:15} RGB{:?} -> ", label, rgb);
        
        let start = std::time::Instant::now();
        match converter.srgb_to_munsell(*rgb) {
            Ok(spec) => {
                let elapsed = start.elapsed();
                total_time += elapsed;
                success_count += 1;
                println!("{:4.1}{} {:.1}/{:.1} ({:.2}ms)", 
                         spec.hue, spec.family, spec.value, spec.chroma,
                         elapsed.as_secs_f64() * 1000.0);
            }
            Err(e) => {
                println!("ERROR: {:?}", e);
            }
        }
    }
    
    println!("\n{}/{} colors converged successfully", success_count, test_cases.len());
    println!("Average time: {:.2}ms", total_time.as_secs_f64() * 1000.0 / test_cases.len() as f64);
}