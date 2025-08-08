#!/bin/bash
# Run a test with stderr redirected to /dev/null

cargo build --release --quiet 2>/dev/null

# Create test program
cat > src/bin/test_one.rs << 'EOF'
use munsellspace::{MunsellColor, RgbColor};

fn main() {
    // Test RGB(221, 238, 238)
    let rgb = RgbColor::new(221, 238, 238).unwrap();
    match rgb.to_munsell_mathematical() {
        Ok(munsell) => {
            println!("{}", munsell);
        }
        Err(_) => {
            println!("ERROR");
        }
    }
}
EOF

timeout 3 cargo run --bin test_one --release --quiet 2>/dev/null

rm src/bin/test_one.rs