#!/usr/bin/env python3
"""
Generate Python colour-science Munsell values for comparison with Rust implementation.
Accepts JSON input with RGB values and illuminant/adaptation parameters.
Returns JSON with Python-calculated Munsell notations.
"""

import json
import sys
import numpy as np
import colour
from colour.models import RGB_COLOURSPACE_sRGB
from colour.adaptation import chromatic_adaptation

def rgb_to_munsell(rgb, target_illuminant='C', adaptation_method='Bradford'):
    """
    Convert sRGB to Munsell using colour-science library.
    
    Parameters:
    -----------
    rgb : array-like
        RGB values in [0, 255] range
    target_illuminant : str
        Target illuminant ('C', 'D65', 'F7', etc.)
    adaptation_method : str
        Chromatic adaptation method ('Bradford', 'CAT02', 'XYZ Scaling', 'Von Kries')
    
    Returns:
    --------
    str
        Munsell notation string (e.g., "5R 5.0/14.0")
    """
    try:
        # Normalize RGB to [0, 1]
        rgb_normalized = np.array(rgb) / 255.0
        
        # Convert sRGB to XYZ (D65 white point by default)
        XYZ_D65 = colour.sRGB_to_XYZ(rgb_normalized)
        
        # Get illuminant XYZ values (not just chromaticities)
        # colour-science expects XYZ white points for chromatic adaptation
        source_white_xy = colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65']
        source_white = colour.xy_to_XYZ(np.append(source_white_xy, 1.0))  # Add Y=1
        
        # Map illuminant names
        illuminant_map = {
            'A': 'A',
            'C': 'C',
            'D50': 'D50',
            'D55': 'D55',
            'D65': 'D65',
            'D75': 'D75',
            'E': 'E',
            'F2': 'FL2',  # Fluorescent mapping
            'F7': 'FL7',
            'F11': 'FL11'
        }
        
        target_illum = illuminant_map.get(target_illuminant, target_illuminant)
        
        if target_illum in colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']:
            target_white_xy = colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer'][target_illum]
            target_white = colour.xy_to_XYZ(np.append(target_white_xy, 1.0))  # Add Y=1
        else:
            # Default to C if not found
            target_white_xy = colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C']
            target_white = colour.xy_to_XYZ(np.append(target_white_xy, 1.0))
        
        # Map adaptation methods - colour-science uses different names
        method_map = {
            'Bradford': 'Von Kries',  # Colour-science uses Von Kries for Bradford
            'CAT02': 'CMCCAT2000',    # CAT02 is called CMCCAT2000 in colour-science
            'XYZScaling': 'Von Kries', # XYZ Scaling approximates Von Kries
            'VonKries': 'Von Kries'
        }
        
        adapt_method = method_map.get(adaptation_method, 'Von Kries')
        
        # Perform chromatic adaptation if needed
        if target_illuminant != 'D65':
            XYZ_adapted = chromatic_adaptation(
                XYZ_D65,
                source_white,
                target_white,
                method=adapt_method
            )
        else:
            XYZ_adapted = XYZ_D65
        
        # Convert XYZ to xyY
        xyY = colour.XYZ_to_xyY(XYZ_adapted)
        
        # Convert xyY to Munsell
        munsell = colour.xyY_to_munsell_colour(xyY)
        
        # Format Munsell notation
        # munsell is typically in format like "5R 5.0/14.0" or could be a specification
        if isinstance(munsell, str):
            return munsell
        else:
            # If it returns a specification object, format it
            return colour.notation.munsell_colour_to_munsell_value(munsell)
            
    except Exception as e:
        return f"ERROR: {str(e)}"

def main():
    """
    Process batch of RGB values from stdin.
    
    Expected JSON format:
    {
        "conversions": [
            {
                "id": "unique_id",
                "rgb": [255, 0, 0],
                "illuminant": "C",
                "adaptation": "Bradford"
            },
            ...
        ]
    }
    
    Returns JSON:
    {
        "results": {
            "unique_id": "5R 5.0/14.0",
            ...
        }
    }
    """
    try:
        # Read JSON from stdin
        input_data = json.loads(sys.stdin.read())
        
        results = {}
        
        for item in input_data.get('conversions', []):
            id_key = item['id']
            rgb = item['rgb']
            illuminant = item.get('illuminant', 'C')
            adaptation = item.get('adaptation', 'Bradford')
            
            munsell = rgb_to_munsell(rgb, illuminant, adaptation)
            results[id_key] = munsell
        
        # Output results as JSON
        output = {"results": results}
        print(json.dumps(output, indent=2))
        
    except Exception as e:
        error_output = {"error": str(e)}
        print(json.dumps(error_output), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()