#!/usr/bin/env python3
"""Add tracing instrumentation macros to Rust functions"""

import re

# Read the python_port.rs file
with open('src/python_port.rs', 'r') as f:
    content = f.read()

# Functions to instrument with tracing
functions_to_instrument = [
    'xyy_to_munsell_specification',
    'munsell_specification_to_xyy',
    'xy_from_renotation_ovoid',
    'xy_from_renotation_ovoid_interpolated',
    'maximum_chroma_from_renotation',
    'chroma_from_renotation_ovoid',
    'hue_to_hue_angle',
    'hue_angle_to_hue',
    'munsell_value_astmd1535',
    'cartesian_to_cylindrical',
    'convergence_criteria',
]

# Add use statement at the top if not present
if 'use tracing::' not in content:
    # Find the last use statement
    last_use = max(m.end() for m in re.finditer(r'^use .*?;\n', content, re.MULTILINE))
    content = content[:last_use] + 'use tracing::{instrument, trace, debug};\n' + content[last_use:]

# Add #[instrument] macro before each function
for func_name in functions_to_instrument:
    # Pattern to match function definition
    pattern = rf'((?:\/\/.*\n)*)(pub fn {func_name}\b)'
    
    def add_instrument(match):
        comments = match.group(1)
        func_def = match.group(2)
        
        # Check if already instrumented
        if '#[instrument' in comments:
            return match.group(0)
        
        # Determine instrumentation level based on function
        if func_name in ['xyy_to_munsell_specification', 'munsell_specification_to_xyy']:
            level = 'debug'
        else:
            level = 'trace'
        
        # Add instrumentation
        return f'{comments}#[instrument(level = "{level}", skip(INTERPOLATION_METHODS_TABLE), ret)]\n{func_def}'
    
    content = re.sub(pattern, add_instrument, content, flags=re.MULTILINE)

# Write the instrumented version
with open('src/python_port_instrumented.rs', 'w') as f:
    f.write(content)

print("Created instrumented version at src/python_port_instrumented.rs")