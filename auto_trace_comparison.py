#!/usr/bin/env python3
"""Automatic trace comparison using instrumentation libraries"""

import subprocess
import sys
import json
import tempfile
import os

def run_python_with_hunter():
    """Run Python with hunter tracing library"""
    
    # Create a Python script that uses hunter
    script = '''
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to use hunter if available
try:
    import hunter
    hunter.trace(
        module='munsell',
        action=hunter.CallPrinter(
            stream=sys.stderr,
            force_colors=False
        )
    )
except ImportError:
    print("Hunter not installed, using basic tracing", file=sys.stderr)

import munsell
import numpy as np

# Test RGB(221, 238, 238)
rgb = np.array([221, 238, 238]) / 255.0

# Convert using colour library
from colour import sRGB_to_XYZ
xyz = sRGB_to_XYZ(rgb)
total = xyz[0] + xyz[1] + xyz[2]
xyy = np.array([xyz[0]/total, xyz[1]/total, xyz[1]])

print(f"Input xyY: {xyy}", file=sys.stderr)

# Convert to Munsell
spec = munsell.xyY_to_munsell_specification(xyy)
print(f"Result: {spec}", file=sys.stderr)
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(script)
        script_path = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        return result.stderr
    finally:
        os.unlink(script_path)

def run_rust_with_env_logger():
    """Run Rust with RUST_LOG environment variable for tracing"""
    
    # Build with instrumentation features if needed
    subprocess.run(
        ["cargo", "build", "--release", "--bin", "test_with_tracing"],
        capture_output=True
    )
    
    result = subprocess.run(
        ["./target/release/test_with_tracing"],
        capture_output=True,
        text=True,
        env={**os.environ, "RUST_LOG": "trace,munsellspace=trace"}
    )
    
    return result.stderr

def extract_key_events(trace_output, language):
    """Extract key events from trace output"""
    
    events = []
    
    if language == "python":
        # Parse hunter output or fallback trace
        for line in trace_output.split('\n'):
            if 'xyY_to_munsell_specification' in line:
                events.append(('call', 'xyY_to_munsell_specification', line))
            elif 'munsell_specification_to_xyY' in line:
                events.append(('call', 'munsell_specification_to_xyY', line))
            elif 'xy_from_renotation_ovoid' in line:
                events.append(('call', 'xy_from_renotation_ovoid', line))
            elif 'Input xyY:' in line:
                events.append(('input', 'xyY', line))
            elif 'Result:' in line:
                events.append(('result', 'specification', line))
    
    elif language == "rust":
        # Parse Rust trace output
        for line in trace_output.split('\n'):
            if 'TRACE|' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    events.append(('trace', parts[1], parts[2]))
            elif 'DEBUG:' in line:
                events.append(('debug', 'message', line))
            elif 'Result:' in line:
                events.append(('result', 'munsell', line))
    
    return events

def compare_executions():
    """Compare Python and Rust execution traces"""
    
    print("="*80)
    print("AUTOMATIC TRACE COMPARISON")
    print("="*80)
    
    print("\nRunning Python with tracing...")
    python_trace = run_python_with_hunter()
    
    print("Running Rust with tracing...")
    rust_trace = run_rust_with_env_logger()
    
    # Extract key events
    python_events = extract_key_events(python_trace, "python")
    rust_events = extract_key_events(rust_trace, "rust")
    
    print("\n--- Python Key Events ---")
    for event_type, name, data in python_events[:10]:
        print(f"  {event_type:8} {name:30} {str(data)[:80]}")
    
    print("\n--- Rust Key Events ---")
    for event_type, name, data in rust_events[:10]:
        print(f"  {event_type:8} {name:30} {str(data)[:80]}")
    
    # Compare specific values
    print("\n--- Value Comparison ---")
    
    # Find input xyY
    for event in python_events:
        if event[0] == 'input' and event[1] == 'xyY':
            print(f"Python input: {event[2]}")
            break
    
    for event in rust_events:
        if event[0] == 'trace' and 'ENTRY' in event[1]:
            print(f"Rust input:   {event[2]}")
            break
    
    # Find results
    for event in python_events:
        if event[0] == 'result':
            print(f"Python result: {event[2]}")
            break
    
    for event in rust_events:
        if event[0] == 'result':
            print(f"Rust result:   {event[2]}")
            break
    
    # Count iterations
    python_iter_count = sum(1 for e in python_events if 'munsell_specification_to_xyY' in str(e))
    rust_iter_count = sum(1 for e in rust_events if 'ITER_' in str(e[1]) and 'START' in str(e[1]))
    
    print(f"\n--- Iteration Counts ---")
    print(f"Python: {python_iter_count} calls to munsell_specification_to_xyY")
    print(f"Rust:   {rust_iter_count} iterations")
    
    # Save full traces for analysis
    with open('python_trace.txt', 'w') as f:
        f.write(python_trace)
    
    with open('rust_trace.txt', 'w') as f:
        f.write(rust_trace)
    
    print("\nFull traces saved to python_trace.txt and rust_trace.txt")

if __name__ == "__main__":
    # First check if hunter is available
    try:
        import hunter
        print("Hunter tracing library is available")
    except ImportError:
        print("Hunter not installed. Install with: pip install hunter")
        print("Continuing with basic tracing...")
    
    compare_executions()