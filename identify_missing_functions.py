#!/usr/bin/env python3
"""Identify all functions in Python colour-science Munsell module that need to be ported"""

import inspect
from colour.notation import munsell
from colour.algebra import LinearInterpolator, Extrapolator
import colour.utilities

# Get all functions from munsell module
munsell_functions = []
for name, obj in inspect.getmembers(munsell):
    if inspect.isfunction(obj):
        munsell_functions.append(name)

# Get utility functions we might need
utility_functions = []
for name, obj in inspect.getmembers(colour.utilities):
    if inspect.isfunction(obj) and name in [
        'as_float_array', 'as_float', 'as_int', 'as_int_array',
        'is_numeric', 'is_integer', 'tsplit', 'tstack',
        'filter_kwargs', 'filter_mapping', 'first_key_from_value',
        'validate_method', 'optional', 'attest', 'usage_warning',
        'runtime_warning', 'ColourWarning', 'ColourUsageWarning',
        'ColourRuntimeWarning', 'message_box', 'show_warning',
        'filter_warnings', 'suppress_warnings', 'numpy_print_options',
        'EPSILON', 'INTEGER_THRESHOLD', 'RESOLUTION'
    ]:
        utility_functions.append(name)

print("=" * 80)
print("MUNSELL MODULE FUNCTIONS TO PORT:")
print("=" * 80)
for func in sorted(munsell_functions):
    # Check if it's a public function (not starting with _)
    if not func.startswith('_'):
        print(f"- {func}")

print("\n" + "=" * 80)
print("UTILITY FUNCTIONS THAT MAY BE NEEDED:")
print("=" * 80)
for func in sorted(utility_functions):
    print(f"- {func}")

# Now check what constants are defined
print("\n" + "=" * 80)
print("MUNSELL MODULE CONSTANTS:")
print("=" * 80)
for name, obj in inspect.getmembers(munsell):
    if not inspect.isfunction(obj) and not inspect.isclass(obj) and not name.startswith('_'):
        if not inspect.ismodule(obj):
            print(f"- {name}: {type(obj).__name__}")

# Check for classes
print("\n" + "=" * 80)
print("CLASSES TO PORT:")
print("=" * 80)
for name, obj in inspect.getmembers(munsell):
    if inspect.isclass(obj):
        print(f"- {name}")
        
# Check interpolation classes
print("\n" + "=" * 80)
print("INTERPOLATION CLASSES:")
print("=" * 80)
print(f"- LinearInterpolator")
print(f"- Extrapolator")

# Get more detail on key functions
print("\n" + "=" * 80)
print("KEY FUNCTION SIGNATURES:")
print("=" * 80)

key_functions = [
    'munsell_colour_to_munsell_specification',
    'munsell_specification_to_munsell_colour',
    'xyY_to_munsell_colour',
    'munsell_colour_to_xyY',
    'parse_munsell_colour',
    'munsell_value',
    'munsell_colour_to_munsell_specification',
    'munsell_specification_to_xyY',
    'xyY_to_munsell_specification',
    'is_grey_munsell_colour',
    'normalise_munsell_specification',
    'munsell_specification_to_renotation',
    'renotation_to_munsell_specification',
    'xy_from_renotation_ovoid',
    'hue_to_hue_angle',
    'hue_angle_to_hue',
    'hue_to_ASTM_hue',
    'interpolation_method_from_renotation_ovoid',
    'xy_from_renotation_ovoid_interpolated'
]

for func_name in key_functions:
    if hasattr(munsell, func_name):
        func = getattr(munsell, func_name)
        sig = inspect.signature(func)
        print(f"\n{func_name}{sig}")