#!/usr/bin/env python3
"""
Traced Python Munsell Conversion Functions

This file contains instrumented versions of key Munsell conversion functions 
from the colour-science library with detailed trace logging to debug the 
Rust implementation.

Trace format: <function_name>:<line_no> | vars: <var1>=<val1>, <var2>=<val2> | action: <operation_type> <details>
"""

import numpy as np
import sys
from typing import List, Any, Tuple, Optional
import inspect

# Import original functions from colour-science and save references
try:
    import colour.notation.munsell as munsell_module
    from colour.notation.munsell import (
        xyY_to_munsell_specification,
        LCHab_to_munsell_specification,
        munsell_value,
        _xyY_to_munsell_specification,
        xy_from_renotation_ovoid,
        maximum_chroma_from_renotation,
        hue_to_hue_angle,
        hue_angle_to_hue,
        bounding_hues_from_renotation,
        interpolation_method_from_renotation_ovoid,
    )
    from colour import XYZ_to_Lab, Lab_to_LCHab, sRGB_to_XYZ, XYZ_to_xyY
    COLOUR_AVAILABLE = True
    
    # Save original functions before monkey patching
    ORIGINALS = {
        '_xyY_to_munsell_specification': munsell_module._xyY_to_munsell_specification,
        'xy_from_renotation_ovoid': munsell_module.xy_from_renotation_ovoid,
        'maximum_chroma_from_renotation': munsell_module.maximum_chroma_from_renotation,
        'hue_to_hue_angle': munsell_module.hue_to_hue_angle,
        'hue_angle_to_hue': munsell_module.hue_angle_to_hue,
        'bounding_hues_from_renotation': munsell_module.bounding_hues_from_renotation,
        'interpolation_method_from_renotation_ovoid': munsell_module.interpolation_method_from_renotation_ovoid,
        'munsell_value': munsell_module.munsell_value,
    }
    
except ImportError as e:
    print(f"Warning: colour-science not available: {e}")
    COLOUR_AVAILABLE = False
    ORIGINALS = {}

# Global trace storage
TRACE_LOG: List[str] = []
TRACING_ENABLED = False

def trace(func_name: str, line_no: int, variables: dict, action: str, details: str = ""):
    """Add a trace entry to the log"""
    if not TRACING_ENABLED:
        return
        
    # Format variables with proper truncation for large arrays
    var_items = []
    for k, v in variables.items():
        if isinstance(v, (list, np.ndarray)):
            if len(str(v)) > 100:
                var_items.append(f"{k}=[...array len={len(v)}...]")
            else:
                var_items.append(f"{k}={v}")
        else:
            var_items.append(f"{k}={v}")
    
    var_str = ", ".join(var_items)
    trace_entry = f"{func_name}:{line_no} | vars: {var_str} | action: {action} {details}"
    TRACE_LOG.append(trace_entry)
    print(trace_entry)

def clear_trace():
    """Clear the trace log"""
    global TRACE_LOG
    TRACE_LOG = []

def save_trace_to_file(filename: str):
    """Save trace log to a file"""
    with open(filename, 'w') as f:
        for entry in TRACE_LOG:
            f.write(entry + '\n')

def enable_tracing():
    """Enable detailed tracing"""
    global TRACING_ENABLED
    TRACING_ENABLED = True

def disable_tracing():
    """Disable detailed tracing"""
    global TRACING_ENABLED
    TRACING_ENABLED = False

# Monkey-patched functions with detailed tracing

def traced_internal_xyY_to_munsell_specification(*args, **kwargs):
    """Traced version of _xyY_to_munsell_specification with detailed internal tracing"""
    func_name = "_xyY_to_munsell_specification"
    
    # Log entry
    xyY = args[0] if len(args) > 0 else kwargs.get('xyY')
    trace(func_name, 1, {"xyY": xyY.tolist() if hasattr(xyY, 'tolist') else xyY}, "ENTER", "internal algorithm entry")
    
    try:
        # Call original with tracing
        result = ORIGINALS['_xyY_to_munsell_specification'](*args, **kwargs)
        trace(func_name, 999, {"result": result.tolist() if hasattr(result, 'tolist') else result}, "RETURN", "internal algorithm complete")
        return result
    except Exception as e:
        trace(func_name, 999, {"error": str(e)}, "ERROR", f"exception in internal algorithm: {e}")
        raise

def traced_internal_xy_from_renotation_ovoid(*args, **kwargs):
    """Traced version of xy_from_renotation_ovoid"""
    func_name = "xy_from_renotation_ovoid"
    
    spec = args[0] if len(args) > 0 else kwargs.get('specification')
    xy_target = args[1] if len(args) > 1 else kwargs.get('xy', None)
    
    trace(func_name, 1, {
        "specification": spec.tolist() if hasattr(spec, 'tolist') else spec,
        "xy_target": xy_target.tolist() if xy_target is not None and hasattr(xy_target, 'tolist') else xy_target
    }, "ENTER", "xy coordinate calculation")
    
    try:
        result = ORIGINALS['xy_from_renotation_ovoid'](*args, **kwargs)
        trace(func_name, 999, {"result": result.tolist() if hasattr(result, 'tolist') else result}, "RETURN", "xy coordinates calculated")
        return result
    except Exception as e:
        trace(func_name, 999, {"error": str(e)}, "ERROR", f"exception in xy calculation: {e}")
        raise

def traced_internal_maximum_chroma_from_renotation(*args, **kwargs):
    """Traced version of maximum_chroma_from_renotation"""
    func_name = "maximum_chroma_from_renotation"
    
    hue = args[0] if len(args) > 0 else kwargs.get('hue')
    value = args[1] if len(args) > 1 else kwargs.get('value')
    
    trace(func_name, 1, {"hue": hue, "value": value}, "ENTER", "maximum chroma lookup")
    
    try:
        result = ORIGINALS['maximum_chroma_from_renotation'](*args, **kwargs)
        trace(func_name, 999, {"result": result}, "RETURN", "maximum chroma found")
        return result
    except Exception as e:
        trace(func_name, 999, {"error": str(e)}, "ERROR", f"exception in maximum chroma: {e}")
        raise

def traced_internal_hue_to_hue_angle(*args, **kwargs):
    """Traced version of hue_to_hue_angle"""
    func_name = "hue_to_hue_angle"
    
    hue = args[0] if len(args) > 0 else kwargs.get('hue')
    trace(func_name, 1, {"hue": hue}, "ENTER", "hue to angle conversion")
    
    try:
        result = ORIGINALS['hue_to_hue_angle'](*args, **kwargs)
        trace(func_name, 999, {"result": result}, "RETURN", "angle calculated")
        return result
    except Exception as e:
        trace(func_name, 999, {"error": str(e)}, "ERROR", f"exception in hue to angle: {e}")
        raise

def traced_internal_hue_angle_to_hue(*args, **kwargs):
    """Traced version of hue_angle_to_hue"""  
    func_name = "hue_angle_to_hue"
    
    angle = args[0] if len(args) > 0 else kwargs.get('hue_angle')
    trace(func_name, 1, {"hue_angle": angle}, "ENTER", "angle to hue conversion")
    
    try:
        result = ORIGINALS['hue_angle_to_hue'](*args, **kwargs)
        trace(func_name, 999, {"result": result}, "RETURN", "hue calculated")
        return result
    except Exception as e:
        trace(func_name, 999, {"error": str(e)}, "ERROR", f"exception in angle to hue: {e}")
        raise

def traced_internal_bounding_hues_from_renotation(*args, **kwargs):
    """Traced version of bounding_hues_from_renotation"""
    func_name = "bounding_hues_from_renotation"
    
    hue = args[0] if len(args) > 0 else kwargs.get('hue')
    trace(func_name, 1, {"hue": hue}, "ENTER", "bounding hues calculation")
    
    try:
        result = ORIGINALS['bounding_hues_from_renotation'](*args, **kwargs)
        trace(func_name, 999, {"result": result.tolist() if hasattr(result, 'tolist') else result}, "RETURN", "bounding hues found")
        return result
    except Exception as e:
        trace(func_name, 999, {"error": str(e)}, "ERROR", f"exception in bounding hues: {e}")
        raise

def traced_internal_interpolation_method_from_renotation_ovoid(*args, **kwargs):
    """Traced version of interpolation_method_from_renotation_ovoid"""
    func_name = "interpolation_method_from_renotation_ovoid"
    
    spec = args[0] if len(args) > 0 else kwargs.get('specification')
    trace(func_name, 1, {"specification": spec.tolist() if hasattr(spec, 'tolist') else spec}, "ENTER", "interpolation method determination")
    
    try:
        result = ORIGINALS['interpolation_method_from_renotation_ovoid'](*args, **kwargs)
        trace(func_name, 999, {"result": result}, "RETURN", "interpolation method determined")
        return result
    except Exception as e:
        trace(func_name, 999, {"error": str(e)}, "ERROR", f"exception in interpolation method: {e}")
        raise

def traced_internal_munsell_value(*args, **kwargs):
    """Traced version of munsell_value"""
    func_name = "munsell_value"
    
    Y = args[0] if len(args) > 0 else kwargs.get('Y')
    method = kwargs.get('method', 'ASTM D1535')
    
    trace(func_name, 1, {"Y": Y, "method": method}, "ENTER", "Munsell value calculation")
    
    try:
        result = ORIGINALS['munsell_value'](*args, **kwargs)
        trace(func_name, 999, {"result": result}, "RETURN", "Munsell value calculated")
        return result
    except Exception as e:
        trace(func_name, 999, {"error": str(e)}, "ERROR", f"exception in Munsell value: {e}")
        raise

def apply_monkey_patches():
    """Apply monkey patches to enable internal tracing"""
    if not COLOUR_AVAILABLE:
        return
        
    munsell_module._xyY_to_munsell_specification = traced_internal_xyY_to_munsell_specification
    munsell_module.xy_from_renotation_ovoid = traced_internal_xy_from_renotation_ovoid  
    munsell_module.maximum_chroma_from_renotation = traced_internal_maximum_chroma_from_renotation
    munsell_module.hue_to_hue_angle = traced_internal_hue_to_hue_angle
    munsell_module.hue_angle_to_hue = traced_internal_hue_angle_to_hue
    munsell_module.bounding_hues_from_renotation = traced_internal_bounding_hues_from_renotation
    munsell_module.interpolation_method_from_renotation_ovoid = traced_internal_interpolation_method_from_renotation_ovoid
    munsell_module.munsell_value = traced_internal_munsell_value

def restore_originals():
    """Restore original functions"""
    if not COLOUR_AVAILABLE:
        return
        
    munsell_module._xyY_to_munsell_specification = ORIGINALS['_xyY_to_munsell_specification']
    munsell_module.xy_from_renotation_ovoid = ORIGINALS['xy_from_renotation_ovoid']
    munsell_module.maximum_chroma_from_renotation = ORIGINALS['maximum_chroma_from_renotation']
    munsell_module.hue_to_hue_angle = ORIGINALS['hue_to_hue_angle']
    munsell_module.hue_angle_to_hue = ORIGINALS['hue_angle_to_hue']
    munsell_module.bounding_hues_from_renotation = ORIGINALS['bounding_hues_from_renotation']
    munsell_module.interpolation_method_from_renotation_ovoid = ORIGINALS['interpolation_method_from_renotation_ovoid']
    munsell_module.munsell_value = ORIGINALS['munsell_value']

def traced_xyY_to_munsell_specification(xyY_array):
    """
    Traced version of xyY_to_munsell_specification
    """
    if not COLOUR_AVAILABLE:
        raise RuntimeError("colour-science not available")
    
    func_name = "xyY_to_munsell_specification"
    
    # Convert input
    xyY = np.array(xyY_array, dtype=float)
    trace(func_name, 1, {"xyY_input": xyY.tolist()}, "ENTER", "main conversion function")
    
    try:
        # Call the original function
        trace(func_name, 2, {"xyY": xyY.tolist()}, "CALL", "calling original xyY_to_munsell_specification")
        result = xyY_to_munsell_specification(xyY)
        
        trace(func_name, 3, {"result": result.tolist()}, "RETURN", "conversion complete")
        return result
    
    except Exception as e:
        trace(func_name, 4, {"error": str(e)}, "ERROR", f"exception occurred: {e}")
        raise

def traced_xy_from_renotation_ovoid(specification_current, xy_target=None):
    """
    Traced version of xy_from_renotation_ovoid
    """
    if not COLOUR_AVAILABLE:
        raise RuntimeError("colour-science not available")
    
    func_name = "xy_from_renotation_ovoid"
    
    spec_list = specification_current.tolist() if hasattr(specification_current, 'tolist') else specification_current
    xy_list = xy_target.tolist() if xy_target is not None and hasattr(xy_target, 'tolist') else xy_target
    
    trace(func_name, 1, {
        "specification_current": spec_list,
        "xy_target": xy_list
    }, "ENTER", "finding xy coordinates from specification")
    
    try:
        if xy_target is None:
            trace(func_name, 2, {}, "CALL", "calling xy_from_renotation_ovoid without target")
            result = xy_from_renotation_ovoid(specification_current)
        else:
            trace(func_name, 3, {}, "CALL", "calling xy_from_renotation_ovoid with target")
            result = xy_from_renotation_ovoid(specification_current, xy_target)
        
        result_list = result.tolist() if hasattr(result, 'tolist') else result
        trace(func_name, 4, {"result": result_list}, "RETURN", "xy coordinates found")
        return result
        
    except Exception as e:
        trace(func_name, 5, {"error": str(e)}, "ERROR", f"exception occurred: {e}")
        raise

def traced_maximum_chroma_from_renotation(hue, value):
    """
    Traced version of maximum_chroma_from_renotation
    """
    if not COLOUR_AVAILABLE:
        raise RuntimeError("colour-science not available")
    
    func_name = "maximum_chroma_from_renotation"
    
    trace(func_name, 1, {"hue": hue, "value": value}, "ENTER", "finding maximum chroma")
    
    try:
        trace(func_name, 2, {}, "CALL", "calling maximum_chroma_from_renotation")
        result = maximum_chroma_from_renotation(hue, value)
        
        trace(func_name, 3, {"result": result}, "RETURN", "maximum chroma found")
        return result
        
    except Exception as e:
        trace(func_name, 4, {"error": str(e)}, "ERROR", f"exception occurred: {e}")
        raise

def traced_hue_to_hue_angle(hue):
    """
    Traced version of hue_to_hue_angle
    """
    if not COLOUR_AVAILABLE:
        raise RuntimeError("colour-science not available")
    
    func_name = "hue_to_hue_angle"
    
    trace(func_name, 1, {"hue": hue}, "ENTER", "converting hue to angle")
    
    try:
        trace(func_name, 2, {}, "CALL", "calling hue_to_hue_angle")
        result = hue_to_hue_angle(hue)
        
        trace(func_name, 3, {"result": result}, "RETURN", "hue angle calculated")
        return result
        
    except Exception as e:
        trace(func_name, 4, {"error": str(e)}, "ERROR", f"exception occurred: {e}")
        raise

def traced_hue_angle_to_hue(hue_angle):
    """
    Traced version of hue_angle_to_hue
    """
    if not COLOUR_AVAILABLE:
        raise RuntimeError("colour-science not available")
    
    func_name = "hue_angle_to_hue"
    
    trace(func_name, 1, {"hue_angle": hue_angle}, "ENTER", "converting angle to hue")
    
    try:
        trace(func_name, 2, {}, "CALL", "calling hue_angle_to_hue")
        result = hue_angle_to_hue(hue_angle)
        
        trace(func_name, 3, {"result": result}, "RETURN", "hue calculated")
        return result
        
    except Exception as e:
        trace(func_name, 4, {"error": str(e)}, "ERROR", f"exception occurred: {e}")
        raise

def traced_bounding_hues_from_renotation(hue):
    """
    Traced version of bounding_hues_from_renotation
    """
    if not COLOUR_AVAILABLE:
        raise RuntimeError("colour-science not available")
    
    func_name = "bounding_hues_from_renotation"
    
    trace(func_name, 1, {"hue": hue}, "ENTER", "finding bounding hues")
    
    try:
        trace(func_name, 2, {}, "CALL", "calling bounding_hues_from_renotation")
        result = bounding_hues_from_renotation(hue)
        
        result_list = result.tolist() if hasattr(result, 'tolist') else result
        trace(func_name, 3, {"result": result_list}, "RETURN", "bounding hues found")
        return result
        
    except Exception as e:
        trace(func_name, 4, {"error": str(e)}, "ERROR", f"exception occurred: {e}")
        raise

def traced_munsell_value(Y, method='ASTM D1535'):
    """
    Traced version of munsell_value
    """
    if not COLOUR_AVAILABLE:
        raise RuntimeError("colour-science not available")
    
    func_name = "munsell_value"
    
    trace(func_name, 1, {"Y": Y, "method": method}, "ENTER", "calculating Munsell value")
    
    try:
        trace(func_name, 2, {}, "CALL", f"calling munsell_value with {method}")
        result = munsell_value(Y, method=method)
        
        trace(func_name, 3, {"result": result}, "RETURN", "Munsell value calculated")
        return result
        
    except Exception as e:
        trace(func_name, 4, {"error": str(e)}, "ERROR", f"exception occurred: {e}")
        raise

def traced_LCHab_to_munsell_specification(LCHab_array):
    """
    Traced version of LCHab_to_munsell_specification
    """
    if not COLOUR_AVAILABLE:
        raise RuntimeError("colour-science not available")
    
    func_name = "LCHab_to_munsell_specification"
    
    LCHab = np.array(LCHab_array, dtype=float)
    trace(func_name, 1, {"LCHab_input": LCHab.tolist()}, "ENTER", "converting Lab to Munsell")
    
    try:
        trace(func_name, 2, {"LCHab": LCHab.tolist()}, "CALL", "calling LCHab_to_munsell_specification")
        result = LCHab_to_munsell_specification(LCHab)
        
        trace(func_name, 3, {"result": result.tolist()}, "RETURN", "Lab to Munsell conversion complete")
        return result
        
    except Exception as e:
        trace(func_name, 4, {"error": str(e)}, "ERROR", f"exception occurred: {e}")
        raise

def traced_interpolation_method_from_renotation_ovoid(specification_current):
    """
    Traced version of interpolation_method_from_renotation_ovoid
    """
    if not COLOUR_AVAILABLE:
        raise RuntimeError("colour-science not available")
    
    func_name = "interpolation_method_from_renotation_ovoid"
    
    spec_list = specification_current.tolist() if hasattr(specification_current, 'tolist') else specification_current
    trace(func_name, 1, {"specification_current": spec_list}, "ENTER", "determining interpolation method")
    
    try:
        trace(func_name, 2, {}, "CALL", "calling interpolation_method_from_renotation_ovoid")
        result = interpolation_method_from_renotation_ovoid(specification_current)
        
        trace(func_name, 3, {"result": result}, "RETURN", "interpolation method determined")
        return result
        
    except Exception as e:
        trace(func_name, 4, {"error": str(e)}, "ERROR", f"exception occurred: {e}")
        raise

# Additional helper functions that might be useful

def sRGB_to_xyY(rgb_array):
    """Convert sRGB to xyY using colour-science pipeline"""
    if not COLOUR_AVAILABLE:
        raise RuntimeError("colour-science not available")
    
    from colour import sRGB_to_XYZ, XYZ_to_xyY
    
    func_name = "sRGB_to_xyY"
    rgb = np.array(rgb_array, dtype=float)
    
    if rgb.max() > 1.0:
        rgb = rgb / 255.0
        trace(func_name, 1, {"rgb_normalized": rgb.tolist()}, "CALC", "normalized RGB from 0-255 to 0-1")
    
    trace(func_name, 2, {"rgb": rgb.tolist()}, "ENTER", "converting sRGB to xyY")
    
    # sRGB to XYZ
    trace(func_name, 3, {}, "CALL", "calling sRGB_to_XYZ")
    xyz = sRGB_to_XYZ(rgb)
    trace(func_name, 4, {"xyz": xyz.tolist()}, "CALC", "XYZ calculated")
    
    # XYZ to xyY
    trace(func_name, 5, {}, "CALL", "calling XYZ_to_xyY") 
    xyY = XYZ_to_xyY(xyz)
    trace(func_name, 6, {"xyY": xyY.tolist()}, "RETURN", "xyY calculated")
    
    return xyY

def run_test_conversion():
    """Test the traced functions with the provided test case"""
    if not COLOUR_AVAILABLE:
        print("ERROR: colour-science library not available")
        return
    
    print("\n" + "="*80)
    print("TRACED PYTHON MUNSELL CONVERSION TEST")
    print("="*80)
    
    # Test case: xyY [0.3016555411, 0.3289901051, 0.8269331673] (RGB 221,238,238)
    test_xyY = np.array([0.3016555411, 0.3289901051, 0.8269331673])
    
    clear_trace()
    
    print(f"\nTest input xyY: {test_xyY}")
    print("\n--- BASIC TEST: Direct function call (no internal tracing) ---")
    
    try:
        # Run basic traced conversion (no monkey patching)
        disable_tracing()
        result = traced_xyY_to_munsell_specification(test_xyY)
        
        print(f"Basic Result: {result}")
        print(f"Hue: {result[0]:.6f}, Value: {result[1]:.6f}, Chroma: {result[2]:.6f}, Family: {result[3]}")
        
    except Exception as e:
        print(f"ERROR during basic conversion: {e}")
    
    print("\n--- DETAILED TEST: Full internal tracing enabled ---")
    
    try:
        # Enable full tracing with monkey patches
        clear_trace()
        apply_monkey_patches()
        enable_tracing()
        
        print("Starting detailed traced conversion...\n")
        
        # Call through the original interface to trigger all internal calls
        result = xyY_to_munsell_specification(test_xyY)
        
        print(f"\nDetailed Result: {result}")
        print(f"Hue: {result[0]:.6f}, Value: {result[1]:.6f}, Chroma: {result[2]:.6f}, Family: {result[3]}")
        
    except Exception as e:
        print(f"ERROR during detailed conversion: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Always restore originals
        restore_originals()
        disable_tracing()
    
    print(f"\nTrace entries generated: {len(TRACE_LOG)}")
    
    # Also test with RGB input for completeness
    print("\n" + "-"*80)
    print("RGB -> xyY -> Munsell Pipeline Test")
    print("-"*80)
    
    try:
        test_rgb = [221, 238, 238]
        print(f"Test RGB: {test_rgb}")
        
        clear_trace()
        enable_tracing()
        apply_monkey_patches()
        
        # Full pipeline with tracing
        xyY_calculated = sRGB_to_xyY(test_rgb)
        print(f"Calculated xyY: {xyY_calculated}")
        
        result2 = xyY_to_munsell_specification(xyY_calculated)
        print(f"Final Munsell: {result2}")
        
    except Exception as e:
        print(f"ERROR during RGB pipeline: {e}")
    finally:
        restore_originals()
        disable_tracing()
    
    print(f"Total trace entries: {len(TRACE_LOG)}")

if __name__ == "__main__":
    # Check if we want to save trace to file
    save_to_file = len(sys.argv) > 1 and sys.argv[1] == "--save-trace"
    
    # Run the test
    run_test_conversion()
    
    # Save trace if requested
    if save_to_file:
        filename = "munsell_conversion_trace.txt"
        save_trace_to_file(filename)
        print(f"\nTrace saved to: {filename}")
    
    print("\nDone!")