#!/usr/bin/env python3
"""Add comprehensive tracing to Rust implementation"""

import re

# Read the current Rust implementation
with open('src/python_port.rs', 'r') as f:
    content = f.read()

# Define trace points to add
trace_insertions = []

# Helper to create trace macro
def trace_macro(location, vars_dict, action=""):
    vars_str = ", ".join([f"{k}={{:?}}" for k in vars_dict.keys()])
    vals_str = ", ".join(vars_dict.values())
    if action:
        return f'eprintln!("TRACE|{location}|vars: {vars_str}|action: {action}", {vals_str});'
    else:
        return f'eprintln!("TRACE|{location}|vars: {vars_str}", {vals_str});'

# Find key functions and add traces
patterns = [
    # Entry points
    (r'(pub fn xyy_to_munsell_specification\([^)]+\) -> [^{]+\{)',
     r'\1\n    eprintln!("TRACE|xyy_to_munsell_specification:ENTRY|vars: xyy={{:?}}", xyy);'),
    
    # Initial specification calculation
    (r'(let initial_spec = lchab_to_munsell_specification\([^)]+\);)',
     r'eprintln!("TRACE|xyy_to_munsell_specification:INITIAL_SPEC_CALC|vars: lchab={{:?}}", lchab);\n    \1\n    eprintln!("TRACE|xyy_to_munsell_specification:INITIAL_SPEC_RESULT|vars: initial_spec={{:?}}", initial_spec);'),
    
    # Convergence loop
    (r'(for iterations in 1..=iterations_maximum \{)',
     r'\1\n        eprintln!("TRACE|xyy_to_munsell_specification:ITERATION_START|vars: iteration={{}}, current_spec={{:?}}", iterations, specification_current);'),
    
    # Hue refinement
    (r'(let hue_new = hue_angle_to_hue\([^)]+\);)',
     r'eprintln!("TRACE|xyy_to_munsell_specification:HUE_CALC|vars: hue_angle_new={{:?}}, code_new={{:?}}", hue_angle_new, code_new);\n        \1\n        eprintln!("TRACE|xyy_to_munsell_specification:HUE_RESULT|vars: hue_new={{:?}}", hue_new);'),
    
    # Chroma refinement decision
    (r'(if \(rho_current - rho_input\)\.abs\(\) < [^{]+\{)',
     r'eprintln!("TRACE|xyy_to_munsell_specification:CHROMA_CHECK|vars: rho_current={{:?}}, rho_input={{:?}}, needs_refinement={{:?}}", rho_current, rho_input, (rho_current - rho_input).abs() >= 1e-10);\n        \1'),
    
    # Chroma refinement loop
    (r'(while !\(rho_min < rho_input && rho_input < rho_max\) \{)',
     r'eprintln!("TRACE|xyy_to_munsell_specification:CHROMA_LOOP|vars: rho_min={{:?}}, rho_input={{:?}}, rho_max={{:?}}, iterations_inner={{:?}}", rho_min, rho_input, rho_max, iterations_inner);\n            \1'),
    
    # Convergence check
    (r'(if difference < convergence_threshold \{)',
     r'eprintln!("TRACE|xyy_to_munsell_specification:CONVERGENCE_CHECK|vars: difference={{:?}}, threshold={{:?}}, converged={{:?}}", difference, convergence_threshold, difference < convergence_threshold);\n        \1'),
]

# Apply patterns
for pattern, replacement in patterns:
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)

# Add trace enable flag at the top of the file
if 'static ENABLE_TRACE:' not in content:
    content = 'static ENABLE_TRACE: bool = true;\n\n' + content
    # Wrap all eprintln! in if ENABLE_TRACE
    content = re.sub(r'eprintln!\("TRACE\|', r'if ENABLE_TRACE { eprintln!("TRACE|', content)
    content = re.sub(r'(eprintln!\("TRACE\|[^;]+;)', r'\1 }', content)

# Write the traced version
with open('src/python_port_traced.rs', 'w') as f:
    f.write(content)

print("Created src/python_port_traced.rs with comprehensive tracing")