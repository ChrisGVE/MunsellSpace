#!/usr/bin/env python3
"""Compare Python and Rust execution traces side by side"""

import subprocess
import sys
import re

def run_python_trace():
    """Run Python with tracing and capture output"""
    result = subprocess.run(
        ["python3", "trace_with_settrace.py"],
        capture_output=True,
        text=True
    )
    return result.stderr.split('\n')

def run_rust_trace():
    """Run Rust with tracing and capture output"""
    result = subprocess.run(
        ["./target/release/test_with_tracing"],
        capture_output=True,
        text=True,
        env={"RUST_LOG": "trace"}
    )
    # Filter out the non-trace lines
    lines = []
    for line in result.stderr.split('\n'):
        if 'TRACE|' in line or 'DEBUG:' in line or 'CALL' in line or 'RETURN' in line:
            lines.append(line)
    return lines

def parse_trace_line(line):
    """Parse a trace line to extract key information"""
    # Python format: "  CALL function_name(args...)"
    # Rust format: "TRACE|label|data"
    
    if 'CALL' in line:
        match = re.search(r'CALL (\w+)\((.*?)\)', line)
        if match:
            return ('call', match.group(1), match.group(2))
    elif 'RETURN' in line:
        match = re.search(r'RETURN (\w+) => (.*)', line)
        if match:
            return ('return', match.group(1), match.group(2))
    elif 'TRACE|' in line:
        parts = line.split('|')
        if len(parts) >= 3:
            return ('trace', parts[1], parts[2])
    return None

def compare_traces():
    """Compare Python and Rust traces"""
    print("Running Python trace...")
    python_lines = run_python_trace()
    
    print("Running Rust trace...")
    rust_lines = run_rust_trace()
    
    print("\n" + "=" * 80)
    print("TRACE COMPARISON")
    print("=" * 80)
    
    # Extract key events from both traces
    python_events = []
    for line in python_lines:
        parsed = parse_trace_line(line)
        if parsed:
            python_events.append(parsed)
    
    rust_events = []
    for line in rust_lines:
        if 'TRACE|' in line:
            # Parse Rust trace format
            parts = line.split('|')
            if len(parts) >= 3:
                label = parts[1]
                data = parts[2]
                rust_events.append(('trace', label, data))
    
    # Print key comparisons
    print("\n--- Initial Values ---")
    for event in python_events[:5]:
        if event[0] == 'call' and 'xyY_to_munsell' in event[1]:
            print(f"Python: {event[1]} with {event[2][:50]}...")
            break
    
    for event in rust_events:
        if event[1] == 'xyy_to_munsell:ENTRY':
            print(f"Rust:   xyy_to_munsell with {event[2]}")
            break
    
    print("\n--- Lab/LCHab Values ---")
    for event in rust_events:
        if event[1] in ['xyy_to_munsell:LAB', 'xyy_to_munsell:LCHAB']:
            print(f"Rust:   {event[1].split(':')[1]} = {event[2]}")
    
    print("\n--- Initial Specification ---")
    for event in rust_events:
        if event[1] == 'xyy_to_munsell:INITIAL_SPEC':
            print(f"Rust:   {event[2]}")
    
    # Find first few iterations
    print("\n--- Convergence Iterations ---")
    iter_count = 0
    for event in python_events:
        if event[0] == 'call' and 'munsell_specification_to_xy' in event[1]:
            spec_match = re.search(r'array\((.*?)\)', event[2])
            if spec_match and iter_count < 5:
                print(f"Python Iter {iter_count+1}: spec={spec_match.group(1)[:50]}...")
                iter_count += 1
    
    iter_count = 0
    for event in rust_events:
        if 'ITER_' in event[1] and 'START' in event[1]:
            if iter_count < 5:
                print(f"Rust   Iter {iter_count+1}: {event[2]}")
                iter_count += 1
    
    print("\n--- Final Convergence ---")
    for event in rust_events:
        if 'CONVERGED' in event[1]:
            print(f"Rust:   {event[2]}")
    
    # Count function calls
    python_calls = {}
    for event in python_events:
        if event[0] == 'call':
            func = event[1]
            python_calls[func] = python_calls.get(func, 0) + 1
    
    print("\n--- Function Call Counts ---")
    print("Python:")
    for func, count in sorted(python_calls.items(), key=lambda x: -x[1])[:10]:
        print(f"  {func:40} : {count:3} calls")

if __name__ == "__main__":
    compare_traces()