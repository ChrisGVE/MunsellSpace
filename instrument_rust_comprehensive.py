#!/usr/bin/env python3
"""Comprehensively instrument Rust code with detailed bread crumbs"""

import re

# Read the current implementation
with open('src/python_port.rs', 'r') as f:
    content = f.read()

# Function to add trace at specific line
def add_trace_after_pattern(content, pattern, trace_stmt, flags=re.MULTILINE):
    """Add a trace statement after a pattern match"""
    def replacer(match):
        return match.group(0) + '\n    ' + trace_stmt
    return re.sub(pattern, replacer, content, count=1, flags=flags)

# Add comprehensive traces
traces = [
    # === Entry point ===
    ('pub fn xyy_to_munsell_specification\(xyy: \[f64; 3\]\) -> Result<\[f64; 4\]> \{',
     'eprintln!("RUST_TRACE|xyy_to_munsell_specification:ENTRY|xyy=[{:.6},{:.6},{:.6}]", xyy[0], xyy[1], xyy[2]);'),
    
    # === Lab/LCHab conversion ===
    ('let xyz = xyy_to_xyz\(xyy\);',
     'eprintln!("RUST_TRACE|xyy_to_munsell:XYZ|xyz=[{:.6},{:.6},{:.6}]", xyz[0], xyz[1], xyz[2]);'),
    
    ('let lab = xyz_to_lab\(xyz, &ILLUMINANT_C_2_XYZ\);',
     'eprintln!("RUST_TRACE|xyy_to_munsell:LAB|lab=[{:.6},{:.6},{:.6}]", lab[0], lab[1], lab[2]);'),
    
    ('let lchab = lab_to_lchab\(lab\);',
     'eprintln!("RUST_TRACE|xyy_to_munsell:LCHAB|lchab=[{:.6},{:.6},{:.6}]", lchab[0], lchab[1], lchab[2]);'),
    
    # === Initial specification ===
    ('let initial_spec = lchab_to_munsell_specification\(lchab\);',
     'eprintln!("RUST_TRACE|xyy_to_munsell:INITIAL_SPEC_PRE|lchab=[{:.6},{:.6},{:.6}]", lchab[0], lchab[1], lchab[2]);'),
    
    ('let initial_spec = lchab_to_munsell_specification\(lchab\);',
     'let initial_spec = lchab_to_munsell_specification(lchab);\n    eprintln!("RUST_TRACE|xyy_to_munsell:INITIAL_SPEC|spec=[{:.6},{:.6},{:.6},{:.0}]", initial_spec[0], initial_spec[1], initial_spec[2], initial_spec[3]);'),
    
    # === Main convergence loop ===
    ('for iterations in 1..=iterations_maximum \{',
     'eprintln!("RUST_TRACE|CONVERGENCE:ITER_{}|spec=[{:.6},{:.6},{:.6},{:.0}]", iterations, specification_current[0], specification_current[1], specification_current[2], specification_current[3]);'),
    
    # === Hue refinement ===
    ('let hue_angle_new = linear_interpolator.interpolate\(phi_input\);',
     'eprintln!("RUST_TRACE|HUE_REFINE:ANGLE_NEW|phi_input={:.6}, hue_angle_new={:.6}", phi_input, hue_angle_new);'),
    
    ('let hue_new = hue_angle_to_hue\(hue_angle_new, code_new\);',
     'eprintln!("RUST_TRACE|HUE_REFINE:HUE_NEW|angle={:.6}, code={}, hue={:.6}", hue_angle_new, code_new, hue_new);'),
    
    # === Chroma refinement check ===
    ('if \(rho_current - rho_input\)\.abs\(\) < 1e-10 \{',
     'eprintln!("RUST_TRACE|CHROMA:CHECK|rho_current={:.9}, rho_input={:.9}, diff={:.9}, skip_refinement={}", rho_current, rho_input, (rho_current - rho_input).abs(), (rho_current - rho_input).abs() < 1e-10);'),
    
    # === Chroma refinement loop ===
    ('while !\(rho_min < rho_input && rho_input < rho_max\) \{',
     'eprintln!("RUST_TRACE|CHROMA:LOOP_ITER_{}|rho_min={:.9}, rho_input={:.9}, rho_max={:.9}, continue={}", iterations_inner, rho_min, rho_input, rho_max, !(rho_min < rho_input && rho_input < rho_max));'),
    
    ('let chroma_inner = if chroma_current < chroma_maximum',
     'eprintln!("RUST_TRACE|CHROMA:CALC|current={:.6}, max={:.6}, method={}", chroma_current, chroma_maximum, if chroma_current < chroma_maximum {"interpolate"} else {"extrapolate"});'),
    
    # === Convergence check ===
    ('let difference = euclidean_distance\(\[x, y\], \[x_current, y_current\]\);',
     'eprintln!("RUST_TRACE|CONVERGENCE:CHECK|target=[{:.9},{:.9}], current=[{:.9},{:.9}], diff={:.12}", x, y, x_current, y_current, difference);'),
    
    ('if difference < convergence_threshold \{',
     'eprintln!("RUST_TRACE|CONVERGENCE:RESULT|converged={}, threshold={:.12}", difference < convergence_threshold, convergence_threshold);'),
]

# Apply all traces
modified = content
for pattern, trace in traces:
    # Check if pattern exists
    if re.search(pattern, modified):
        modified = add_trace_after_pattern(modified, pattern, trace)
    else:
        print(f"Warning: Pattern not found: {pattern[:50]}...")

# Add trace flag at the beginning if not present
if 'const ENABLE_TRACE: bool' not in modified:
    modified = 'const ENABLE_TRACE: bool = true;\n\n' + modified

# Save the instrumented version
with open('src/python_port_instrumented.rs', 'w') as f:
    f.write(modified)

print("Created src/python_port_instrumented.rs with comprehensive tracing")
print("\nTo use it:")
print("1. Back up src/python_port.rs: cp src/python_port.rs src/python_port.rs.backup")
print("2. Replace with instrumented: cp src/python_port_instrumented.rs src/python_port.rs")
print("3. Rebuild and run: cargo build --release")
print("4. Run test and capture traces: cargo run --release --bin test_rgb221_direct 2>rust_trace.txt")