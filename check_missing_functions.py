#!/usr/bin/env python3
"""Check which critical functions are missing from our Rust port"""

import inspect
import colour.notation.munsell as munsell

# Critical functions we need for accurate conversion
critical_functions = [
    # Core conversion functions
    'xyY_to_munsell_specification',
    'munsell_specification_to_xyY',
    'munsell_specification_to_xy',
    'xyY_to_munsell_colour',
    'munsell_colour_to_xyY',
    
    # String parsing functions
    'parse_munsell_colour',
    'munsell_colour_to_munsell_specification', 
    'munsell_specification_to_munsell_colour',
    
    # Lab color space functions
    'LCHab_to_munsell_specification',
    'XYZ_to_Lab',
    'Lab_to_LCHab',
    
    # Data access functions
    'xyY_from_renotation',
    'xy_from_renotation_ovoid',
    'maximum_chroma_from_renotation',
    
    # Helper functions
    'is_grey_munsell_colour',
    'is_specification_in_renotation',
    'normalise_munsell_specification',
    'bounding_hues_from_renotation',
    'interpolation_method_from_renotation_ovoid',
    
    # Value computation functions
    'munsell_value_ASTMD1535',
    'luminance_ASTMD1535',
    'munsell_value',
    
    # Angle conversions
    'hue_to_ASTM_hue',
    'hue_angle_to_hue',
    'hue_to_hue_angle',
    
    # MacAdam limits
    'is_within_macadam_limits',
]

print("Checking implementation status of critical functions:")
print("="*80)

for func_name in critical_functions:
    if hasattr(munsell, func_name):
        func = getattr(munsell, func_name)
        sig = inspect.signature(func)
        doc = inspect.getdoc(func)
        first_line = doc.split('\n')[0] if doc else "No documentation"
        
        print(f"\n{func_name}{sig}")
        print(f"  Purpose: {first_line}")
        
        # Check if it's already in our Rust implementation
        # This is a manual check - you'd need to verify against python_port.rs
        print(f"  TODO: Verify if ported to python_port.rs")

# Now let's look at the internal _xyY_to_munsell_specification
print("\n" + "="*80)
print("INTERNAL FUNCTION DETAILS:")
print("="*80)

# Get the actual implementation
if hasattr(munsell, '_xyY_to_munsell_specification'):
    print("\n_xyY_to_munsell_specification exists (internal implementation)")
    
# Check for array handling functions
print("\nArray handling functions needed:")
for func in ['as_float_array', 'tsplit', 'tstack']:
    if hasattr(munsell, func):
        print(f"  - {func}: Available")