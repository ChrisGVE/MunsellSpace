"""Test exact lookup values that Rust is using"""
import colour
from colour.notation.munsell import munsell_specification_to_xyY

# Test the exact lookups our Rust is doing
specs = [
    # What Rust is looking up at value 4
    ([4.13, 4.0, 18.0, 7], "4.13R 4.0/18.0"),
    ([4.13, 4.0, 20.0, 7], "4.13R 4.0/20.0"),
    # What Rust is looking up at value 5
    ([4.13, 5.0, 18.0, 7], "4.13R 5.0/18.0"),
    ([4.13, 5.0, 20.0, 7], "4.13R 5.0/20.0"),
]

print("Python lookups:")
for spec, desc in specs:
    xyY = munsell_specification_to_xyY(spec)
    print(f"{desc} -> xy=({xyY[0]:.6f}, {xyY[1]:.6f})")

# Now let's see what interpolation between 18 and 20 gives us
print("\nChroma interpolation at value 4:")
spec_18 = [4.13, 4.0, 18.0, 7]
spec_20 = [4.13, 4.0, 20.0, 7]
xyY_18 = munsell_specification_to_xyY(spec_18)
xyY_20 = munsell_specification_to_xyY(spec_20)
t = (18.159 - 18.0) / (20.0 - 18.0)
x_interp = xyY_18[0] + t * (xyY_20[0] - xyY_18[0])
y_interp = xyY_18[1] + t * (xyY_20[1] - xyY_18[1])
print(f"  Interpolated at chroma 18.159: xy=({x_interp:.6f}, {y_interp:.6f})")

print("\nChroma interpolation at value 5:")
spec_18 = [4.13, 5.0, 18.0, 7]
spec_20 = [4.13, 5.0, 20.0, 7]
xyY_18 = munsell_specification_to_xyY(spec_18)
xyY_20 = munsell_specification_to_xyY(spec_20)
t = (18.159 - 18.0) / (20.0 - 18.0)
x_interp = xyY_18[0] + t * (xyY_20[0] - xyY_18[0])
y_interp = xyY_18[1] + t * (xyY_20[1] - xyY_18[1])
print(f"  Interpolated at chroma 18.159: xy=({x_interp:.6f}, {y_interp:.6f})")

# Now let's trace what's happening with hue interpolation for non-standard hues
print("\n\nChecking hue interpolation logic:")
print("Hue 4.13 is not standard (standards are 2.5, 5.0, 7.5, 10.0)")
print("So it needs to interpolate between neighboring hues")

# What are the bounding hues for 4.13R?
# In Python's bounding_hues_from_renotation:
# For hue 4.13, the boundaries would be 2.5R and 5.0R
bounding_specs = [
    ([2.5, 4.0, 18.0, 7], "2.5R 4.0/18.0"),
    ([5.0, 4.0, 18.0, 7], "5.0R 4.0/18.0"),
    ([2.5, 4.0, 20.0, 7], "2.5R 4.0/20.0"),
    ([5.0, 4.0, 20.0, 7], "5.0R 4.0/20.0"),
]

print("\nBounding hue lookups at value 4:")
for spec, desc in bounding_specs:
    xyY = munsell_specification_to_xyY(spec)
    print(f"{desc} -> xy=({xyY[0]:.6f}, {xyY[1]:.6f})")
    
# Actually, let me check what Python's xy_from_renotation_ovoid does
print("\n\nDirect test of xy_from_renotation_ovoid:")
from colour.notation.munsell import xy_from_renotation_ovoid
import numpy as np

# Test for 4.13R 4.0/18.0
result = xy_from_renotation_ovoid(np.array([4.13, 4.0, 18.0, 7]))
print(f"xy_from_renotation_ovoid([4.13, 4.0, 18.0, 7]) = ({result[0]:.6f}, {result[1]:.6f})")

# Test for 4.13R 5.0/18.0  
result = xy_from_renotation_ovoid(np.array([4.13, 5.0, 18.0, 7]))
print(f"xy_from_renotation_ovoid([4.13, 5.0, 18.0, 7]) = ({result[0]:.6f}, {result[1]:.6f})")