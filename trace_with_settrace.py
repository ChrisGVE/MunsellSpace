#!/usr/bin/env python3
"""Automatic tracing using sys.settrace for Python Munsell conversion"""

import sys
import numpy as np
from colour.notation import munsell
from colour import RGB_to_XYZ, XYZ_to_xyY
from colour.models import RGB_COLOURSPACE_sRGB

class MunsellTracer:
    """Custom tracer for Munsell conversion functions"""
    
    def __init__(self, trace_file=sys.stderr):
        self.trace_file = trace_file
        self.call_depth = 0
        self.trace_enabled = False
        self.important_functions = {
            'xyY_to_munsell_specification',
            'munsell_specification_to_xy', 
            'xy_from_renotation_ovoid',
            'maximum_chroma_from_renotation',
            'hue_to_hue_angle',
            'hue_angle_to_hue',
            '_munsell_value_ASTM_D1535',
            'munsell_value_ASTM_D1535',
            'cartesian_to_cylindrical',
            'cylindrical_to_cartesian',
            'convergence_criteria',
        }
        
    def trace_calls(self, frame, event, arg):
        """Trace function to be used with sys.settrace"""
        
        # Only trace munsell module
        module = frame.f_globals.get('__name__', '')
        if not (module.startswith('colour.notation.munsell') or 
                module.startswith('colour.algebra')):
            return None
            
        func_name = frame.f_code.co_name
        
        if event == 'call':
            # Only trace important functions
            if func_name in self.important_functions:
                self.call_depth += 1
                indent = "  " * self.call_depth
                
                # Get function arguments
                args = []
                for var_name in frame.f_code.co_varnames[:frame.f_code.co_argcount]:
                    value = frame.f_locals.get(var_name, 'N/A')
                    if isinstance(value, np.ndarray):
                        value = f"array({value.tolist()})"
                    elif isinstance(value, (float, int)):
                        value = f"{value:.6f}" if isinstance(value, float) else str(value)
                    args.append(f"{var_name}={value}")
                
                self.trace_file.write(
                    f"{indent}CALL {func_name}({', '.join(args[:3])}...)\n"
                )
                return self.trace_calls
                
        elif event == 'return':
            if func_name in self.important_functions:
                indent = "  " * self.call_depth
                
                # Format return value
                ret_val = arg
                if isinstance(ret_val, np.ndarray):
                    ret_val = f"array({ret_val.tolist()})"
                elif isinstance(ret_val, tuple):
                    ret_val = f"tuple({[float(x) if isinstance(x, (float, np.float64)) else x for x in ret_val]})"
                elif isinstance(ret_val, float):
                    ret_val = f"{ret_val:.6f}"
                    
                self.trace_file.write(
                    f"{indent}RETURN {func_name} => {ret_val}\n"
                )
                self.call_depth = max(0, self.call_depth - 1)
                
        elif event == 'line':
            # Optionally trace specific lines for debugging
            # This can be very verbose, so disabled by default
            pass
            
        return self.trace_calls if event == 'call' else None

# Test RGB(221, 238, 238)
print("Testing RGB(221, 238, 238) with automatic sys.settrace tracing")
print("=" * 60)

rgb = np.array([221/255.0, 238/255.0, 238/255.0])
print(f"Input RGB: {rgb}")

# Convert to XYZ and xyY
XYZ = RGB_to_XYZ(rgb, RGB_COLOURSPACE_sRGB)
xyY = XYZ_to_xyY(XYZ)
print(f"XYZ: {XYZ}")
print(f"xyY: {xyY}")

# Enable tracing
tracer = MunsellTracer()
sys.settrace(tracer.trace_calls)

print("\n--- Starting traced Munsell conversion ---")
try:
    result = munsell.xyY_to_munsell_colour(xyY)
    print(f"\nResult: {result}")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Disable tracing
    sys.settrace(None)