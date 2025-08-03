#!/usr/bin/env python3
"""Remove debug output from mathematical.rs"""

import re

with open('src/mathematical.rs', 'r') as f:
    lines = f.readlines()

# Process lines
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check if this line contains eprintln!
    if 'eprintln!' in line:
        # Check if it's a multi-line eprintln
        if line.strip().endswith(','):
            # Comment out this line
            new_lines.append('            // ' + line.strip() + '\n')
            # Look for the closing );
            i += 1
            while i < len(lines) and ');' not in lines[i]:
                new_lines.append('            // ' + lines[i].strip() + '\n')
                i += 1
            if i < len(lines):
                new_lines.append('            // ' + lines[i].strip() + '\n')
        else:
            # Single line eprintln
            new_lines.append('            // ' + line.strip() + '\n')
    else:
        new_lines.append(line)
    i += 1

with open('src/mathematical.rs', 'w') as f:
    f.writelines(new_lines)

print("Debug output removed successfully")