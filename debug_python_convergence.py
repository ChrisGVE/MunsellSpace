#!/usr/bin/env python3
"""Debug Python's convergence for RGB(68,102,68)."""

import sys
sys.path.insert(0, 'venv_comparison/lib/python3.13/site-packages')

from colour import sRGB_to_XYZ, XYZ_to_xyY
from colour.notation.munsell import xyY_to_munsell_specification, xy_from_renotation_ovoid
import numpy as np

# Test RGB(68,102,68)
r, g, b = 68, 102, 68
srgb = [r/255, g/255, b/255]
XYZ = sRGB_to_XYZ(srgb)
xyY = XYZ_to_xyY(XYZ)

print(f"RGB({r},{g},{b}):")
print(f"  xyY: x={xyY[0]:.6f}, y={xyY[1]:.6f}, Y={xyY[2]:.6f}")

# Get Python's converged specification
spec = xyY_to_munsell_specification(xyY)
print(f"  Final spec: hue={spec[0]:.6f}, value={spec[1]:.6f}, chroma={spec[2]:.6f}, code={spec[3]}")

# Check what xy coordinates this spec produces
xy_final = xy_from_renotation_ovoid(spec)
print(f"  Final xy: x={xy_final[0]:.6f}, y={xy_final[1]:.6f}")

# Calculate the error
error = np.sqrt((xy_final[0] - xyY[0])**2 + (xy_final[1] - xyY[1])**2)
print(f"  Final error: {error:.10f}")

# Now test what Rust converged to
rust_spec = [0.0038722545, 3.9124191302, 4.6613351008, 3.0]
print(f"\nRust spec: hue={rust_spec[0]:.6f}, value={rust_spec[1]:.6f}, chroma={rust_spec[2]:.6f}, code={rust_spec[3]}")

# Check what xy this produces
xy_rust = xy_from_renotation_ovoid(rust_spec)
print(f"  Rust's xy: x={xy_rust[0]:.6f}, y={xy_rust[1]:.6f}")

# Calculate Rust's error
rust_error = np.sqrt((xy_rust[0] - xyY[0])**2 + (xy_rust[1] - xyY[1])**2)
print(f"  Rust's error: {rust_error:.10f}")

# Now test the alternative interpretation that Python converged to
# Python got hue=9.9968, code=4 (GY)
python_actual = [9.9968, 3.9125, 4.6511, 4.0]
print(f"\nPython actual: hue={python_actual[0]:.6f}, value={python_actual[1]:.6f}, chroma={python_actual[2]:.6f}, code={python_actual[3]}")

# Check what xy this produces
xy_python = xy_from_renotation_ovoid(python_actual)
print(f"  Python's xy: x={xy_python[0]:.6f}, y={xy_python[1]:.6f}")

# Calculate Python's error
python_error = np.sqrt((xy_python[0] - xyY[0])**2 + (xy_python[1] - xyY[1])**2)
print(f"  Python's error: {python_error:.10f}")

print("\nCONCLUSION:")
print(f"  Both converged to nearly identical xy coordinates!")
print(f"  Python: hue=9.9968 in GY (code=4)")
print(f"  Rust:   hue=0.0039 in G (code=3)")
print(f"  These are essentially the same point at the GY/G boundary")