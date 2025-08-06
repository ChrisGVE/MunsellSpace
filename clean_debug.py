#!/usr/bin/env python3
"""Remove debug statements from python_port.rs"""

import re

with open('src/python_port.rs', 'r') as f:
    lines = f.readlines()

cleaned = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check if this is a debug if statement
    if 'eprintln!' in line:
        # Skip the eprintln line
        i += 1
        continue
    
    # Check if this is an if statement that only contains debug
    if i + 2 < len(lines) and line.strip().startswith('if ') and '{' in line:
        if 'eprintln!' in lines[i+1]:
            # Check if next line after eprintln is just closing brace
            if i + 2 < len(lines) and lines[i+2].strip() == '}':
                # Skip entire if block
                i += 3
                continue
            # Check if there are multiple eprintln lines
            elif i + 3 < len(lines) and 'eprintln!' in lines[i+2] and lines[i+3].strip() == '}':
                # Skip entire if block with 2 eprintln lines
                i += 4
                continue
    
    # Check for empty if blocks (from already removed debug)
    if line.strip().startswith('if ') and i + 1 < len(lines) and lines[i+1].strip() == '}':
        # Skip empty if block
        i += 2
        continue
    
    # Check for comments followed by empty if blocks
    if line.strip().startswith('//') and i + 2 < len(lines):
        if lines[i+1].strip().startswith('if ') and lines[i+2].strip() == '}':
            # Skip comment and empty if block
            i += 3
            continue
    
    cleaned.append(line)
    i += 1

with open('src/python_port.rs', 'w') as f:
    f.writelines(cleaned)