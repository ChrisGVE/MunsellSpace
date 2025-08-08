#!/bin/bash
# Test with debug output

cat > src/bin/test_debug.rs << 'EOF'
use munsellspace::RgbColor;

fn main() {
    eprintln!("Starting test...");
    
    // Test RGB(221, 238, 238) - the problematic color
    let rgb = RgbColor::new(221, 238, 238);
    eprintln!("Created RGB color");
    
    // Try to convert
    eprintln!("Starting conversion...");
    match rgb.to_munsell_mathematical() {
        Ok(munsell) => {
            eprintln!("Success: {}", munsell);
            println!("Success: {}", munsell);
        }
        Err(e) => {
            eprintln!("Error: {}", e);
            println!("Error: {}", e);
        }
    }
    eprintln!("Test complete");
}
EOF

cargo build --bin test_debug --release 2>/dev/null
echo "Build complete, running test..."
timeout 2 cargo run --bin test_debug --release 2>&1 | head -20

rm src/bin/test_debug.rs