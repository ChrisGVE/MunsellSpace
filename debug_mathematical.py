#!/usr/bin/env python3

import subprocess
import json

def test_single_color():
    """Test a single color to debug the mathematical conversion"""
    
    # Test color: RGB [57, 12, 140] 
    # Python result: "2.2P 4.1/16.8"
    # Rust result: "7.5PB 2.0/4.0"
    
    rust_binary = "./target/release/examples/mathematical_debug"
    
    # Call Rust mathematical debug
    result = subprocess.run([rust_binary, "57", "12", "140"], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error running Rust binary: {result.stderr}")
        return
        
    print("🔬 DEBUGGING MATHEMATICAL CONVERSION")
    print(f"Test color: RGB [57, 12, 140]")
    print(f"Expected (Python): 2.2P 4.1/16.8")
    print()
    print("🦀 RUST DEBUG OUTPUT:")
    print(result.stdout)

if __name__ == "__main__":
    test_single_color()