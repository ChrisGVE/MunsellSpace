#!/usr/bin/env python3
"""List ALL functions from Python's colour-science Munsell module"""

import inspect
import colour.notation.munsell as munsell_module

# Get all members of the module
all_members = inspect.getmembers(munsell_module)

# Filter for functions and classes
functions = []
classes = []

for name, obj in all_members:
    if inspect.isfunction(obj):
        functions.append((name, obj))
    elif inspect.isclass(obj):
        classes.append((name, obj))

print("="*80)
print("ALL FUNCTIONS IN colour.notation.munsell:")
print("="*80)

for name, func in sorted(functions):
    # Skip private functions starting with _
    if not name.startswith('_'):
        doc = inspect.getdoc(func)
        first_line = doc.split('\n')[0] if doc else "No documentation"
        print(f"\n{name}")
        print(f"  Purpose: {first_line}")
        
print("\n" + "="*80)
print("ALL CLASSES IN colour.notation.munsell:")
print("="*80)

for name, cls in sorted(classes):
    doc = inspect.getdoc(cls)
    first_line = doc.split('\n')[0] if doc else "No documentation"
    print(f"\n{name}")
    print(f"  Purpose: {first_line}")
    
# Now check what's actually being used internally
print("\n" + "="*80)
print("CHECKING INTERNAL DEPENDENCIES:")
print("="*80)

# Check the actual source of key functions
key_functions = [
    'xyY_to_munsell_specification',
    'munsell_specification_to_xyY',
    'munsell_colour_to_xyY',
    'xyY_to_munsell_colour',
]

for func_name in key_functions:
    if hasattr(munsell_module, func_name):
        func = getattr(munsell_module, func_name)
        source = inspect.getsource(func)
        print(f"\n{func_name} dependencies:")
        # Look for function calls in the source
        import re
        called_funcs = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', source)
        unique_calls = sorted(set(called_funcs))
        for call in unique_calls[:20]:  # Limit output
            print(f"  - {call}")