#!/usr/bin/env python3
"""Automatic tracing using hunter library for Python Munsell conversion"""

import sys
import numpy as np

# Install hunter if not available
try:
    import hunter
except ImportError:
    print("Installing hunter...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "hunter"])
    import hunter

from colour.notation import munsell
from colour import RGB_to_XYZ, XYZ_to_xyY
from colour.models import RGB_COLOURSPACE_sRGB

# Configure hunter to trace only the munsell module and key functions
# We'll trace all function calls, lines, and returns in the munsell module
hunter.trace(
    # Only trace munsell module and our conversion functions
    hunter.Q(
        module_startswith="colour.notation.munsell",
        kind="call"
    ) | hunter.Q(
        module_startswith="colour.notation.munsell", 
        kind="return"
    ) | hunter.Q(
        module_startswith="colour.notation.munsell",
        kind="line",
        # Filter to only important lines (those with assignments or function calls)
        function_in=[
            "xyY_to_munsell_specification",
            "munsell_specification_to_xy",
            "_munsell_value_ASTM_D1535",
            "xy_from_renotation_ovoid",
            "maximum_chroma_from_renotation",
            "hue_to_hue_angle",
            "hue_angle_to_hue",
        ]
    ),
    # Action: print with depth, show locals for key functions
    action=hunter.CallPrinter(
        stream=sys.stderr,
        force_colors=True,
        repr_limit=100,
        depth_limit=10
    )
)

# Test RGB(221, 238, 238)
print("Testing RGB(221, 238, 238) with automatic tracing")
print("=" * 60)

rgb = np.array([221/255.0, 238/255.0, 238/255.0])
print(f"Input RGB: {rgb}")

# Convert to XYZ and xyY
XYZ = RGB_to_XYZ(rgb, RGB_COLOURSPACE_sRGB)
xyY = XYZ_to_xyY(XYZ)
print(f"XYZ: {XYZ}")
print(f"xyY: {xyY}")

# This will be traced automatically
print("\n--- Starting traced Munsell conversion ---")
try:
    result = munsell.xyY_to_munsell_colour(xyY)
    print(f"\nResult: {result}")
except Exception as e:
    print(f"Error: {e}")
    
hunter.stop()