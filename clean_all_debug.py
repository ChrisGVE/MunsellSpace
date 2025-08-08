#!/usr/bin/env python3
"""Remove all incomplete debug statements from python_port.rs"""

import re

# Read the file
with open('src/python_port.rs', 'r') as f:
    content = f.read()

# Pattern to match incomplete debug statements
# These are lines that look like debug output but are not complete print statements
patterns = [
    r'\s+if is_debug_color \|\| is_grey_debug \{[^}]*?\n\s*}',  # Empty or incomplete debug blocks
    r'\s+hue_new, chroma_current, code_new, chroma_maximum\);',  # Incomplete print arguments
    r'\s+rho_current, rho_min, chroma_current\);',  # Incomplete print arguments
    r'\s+iterations_inner, chroma_inner, chroma_inner_unclamped,[^;]+\);',  # Incomplete print arguments
    r'\s+x_inner, y_inner, rho_inner,[^;]+\);',  # Incomplete print arguments
    r'\s+\*chroma_bounds_data\.iter\(\)\.max_by[^;]+\);',  # Incomplete print arguments
    r'\s+rho_min < rho_input && rho_input < rho_max\);',  # Incomplete print arguments
    r'\s+spec\[0\], spec\[1\], spec\[2\], spec\[3\][^;]*\);',  # Incomplete print arguments
    r'\s+is_standard_hue, is_integer_value, is_even_chroma\);',  # Incomplete print arguments
    r'\s+hue, hue_minus, code_minus, hue_plus, code_plus\);',  # Incomplete print arguments
    r'\s+spec_minus\[0\], spec_minus\[1\], spec_minus\[2\], spec_minus\[3\][^;]*\);',  # Incomplete print arguments
    r'\s+spec_plus\[0\], spec_plus\[1\], spec_plus\[2\], spec_plus\[3\][^;]*\);',  # Incomplete print arguments
    r'\s+phi_differences_sorted, hue_angles_differences_sorted\);',  # Incomplete print arguments
    r'\s+hue_angle_difference_new,[^;]+\);',  # Incomplete print arguments
    r'\s+hue_angle_inner, hue_angle_difference_inner, phi_inner_difference\);',  # Incomplete print arguments
]

# Remove all these patterns
for pattern in patterns:
    content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)

# Also remove any lines that are just closing parens from incomplete statements
content = re.sub(r'^\s*\);\s*$', '', content, flags=re.MULTILINE)

# Clean up excessive blank lines
content = re.sub(r'\n{3,}', '\n\n', content)

# Write back
with open('src/python_port.rs', 'w') as f:
    f.write(content)

print("Cleaned up all incomplete debug statements")