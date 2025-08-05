#!/usr/bin/env python3
"""Find the private implementation functions"""

import colour.notation.munsell as munsell

# List all functions in the module
functions = [name for name in dir(munsell) if callable(getattr(munsell, name))]

print("=== All functions in colour.notation.munsell ===")
for func in sorted(functions):
    if not func.startswith('__'):
        print(f"  {func}")

print("\n=== Private functions (starting with _) ===")
private_funcs = [f for f in functions if f.startswith('_') and not f.startswith('__')]
for func in sorted(private_funcs):
    print(f"  {func}")

# Check if we can access the source
print("\n=== Checking _xyY_to_munsell_specification ===")
if hasattr(munsell, '_xyY_to_munsell_specification'):
    print("Found! This is the main implementation function.")
    import inspect
    # Try to get source
    try:
        source = inspect.getsource(munsell._xyY_to_munsell_specification)
        print(f"Source code length: {len(source.splitlines())} lines")
        # Save to file
        with open('python_xyy_to_munsell_impl.py', 'w') as f:
            f.write("# Python colour-science _xyY_to_munsell_specification implementation\n")
            f.write(source)
        print("Saved to: python_xyy_to_munsell_impl.py")
    except:
        print("Could not get source code")