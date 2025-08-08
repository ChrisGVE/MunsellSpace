#!/usr/bin/env python3
"""Add direct trace statements to the Rust code"""

import re

# Read the current file
with open('src/python_port.rs', 'r') as f:
    lines = f.readlines()

# Find key locations and insert traces
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Add the current line first
    new_lines.append(line)
    
    # Check for key patterns and add traces AFTER them
    
    # Entry to main conversion function
    if 'pub fn xyy_to_munsell_specification(xyy: [f64; 3])' in line:
        # Find the opening brace
        while i < len(lines) and '{' not in lines[i]:
            i += 1
            new_lines.append(lines[i])
        # Add trace after opening brace
        new_lines.append('    eprintln!("TRACE|xyy_to_munsell:ENTRY|xyy={{:.6}},{:.6},{:.6}", xyy[0], xyy[1], xyy[2]);\n')
    
    # XYZ conversion
    elif 'let xyz = xyy_to_xyz(xyy);' in line:
        new_lines.append('    eprintln!("TRACE|xyy_to_munsell:XYZ|xyz={{:.6}},{:.6},{:.6}", xyz[0], xyz[1], xyz[2]);\n')
    
    # Lab conversion
    elif 'let lab = xyz_to_lab(xyz' in line:
        new_lines.append('    eprintln!("TRACE|xyy_to_munsell:LAB|lab={{:.6}},{:.6},{:.6}", lab[0], lab[1], lab[2]);\n')
    
    # LCHab conversion
    elif 'let lchab = lab_to_lchab(lab);' in line:
        new_lines.append('    eprintln!("TRACE|xyy_to_munsell:LCHAB|L={{:.6}},C={{:.6}},H={{:.6}}", lchab[0], lchab[1], lchab[2]);\n')
    
    # Initial specification
    elif 'let initial_spec = lchab_to_munsell_specification(lchab);' in line:
        new_lines.append('    eprintln!("TRACE|xyy_to_munsell:INITIAL_SPEC|hue={{:.6}},value={{:.6}},chroma={{:.6}},code={{:.0}}", initial_spec[0], initial_spec[1], initial_spec[2], initial_spec[3]);\n')
    
    # Start of convergence loop
    elif 'for iterations in 1..=iterations_maximum {' in line:
        # Add trace at start of loop body
        new_lines.append('        eprintln!("TRACE|ITER_{{}}:START|spec={{:.6}},{:.6},{:.6},{:.0}", iterations, specification_current[0], specification_current[1], specification_current[2], specification_current[3]);\n')
    
    # Hue calculation
    elif 'let hue_new = hue_angle_to_hue(hue_angle_new, code_new);' in line:
        new_lines.append('        eprintln!("TRACE|ITER:HUE_CALC|angle={{:.6}},code={{}},hue={{:.6}}", hue_angle_new, code_new, hue_new);\n')
    
    # Chroma check
    elif 'if (rho_current - rho_input).abs() < 1e-10 {' in line:
        new_lines.append('        eprintln!("TRACE|ITER:CHROMA_CHECK|rho_current={{:.9}},rho_input={{:.9}},skip={{}}", rho_current, rho_input, (rho_current - rho_input).abs() < 1e-10);\n')
    
    # Convergence check
    elif 'let difference = euclidean_distance([x, y], [x_current, y_current]);' in line:
        new_lines.append('        eprintln!("TRACE|ITER:CONVERGENCE|xy_target={{:.9}},{:.9},xy_current={{:.9}},{:.9},diff={{:.12}}", x, y, x_current, y_current, difference);\n')
    
    # Convergence decision
    elif 'if difference < convergence_threshold {' in line:
        new_lines.append('        eprintln!("TRACE|ITER:CONVERGED|diff={{:.12}},threshold={{:.12}},converged={{}}", difference, convergence_threshold, difference < convergence_threshold);\n')
    
    i += 1

# Write the instrumented code
with open('src/python_port_traced_direct.rs', 'w') as f:
    f.writelines(new_lines)

print("Created src/python_port_traced_direct.rs with direct trace statements")
print("\nTo use:")
print("1. cp src/python_port.rs src/python_port_backup.rs")
print("2. cp src/python_port_traced_direct.rs src/python_port.rs")
print("3. cargo build --release --bin test_rgb221_direct")
print("4. cargo run --release --bin test_rgb221_direct 2>rust_traces.txt")