#!/usr/bin/env python3
"""Create comprehensive test data from Python colour-science for 1:1 port validation"""

import numpy as np
import json
from colour.notation.munsell import (
    hue_to_ASTM_hue,
    hue_to_hue_angle,
    hue_angle_to_hue,
    bounding_hues_from_renotation,
    maximum_chroma_from_renotation,
    interpolation_method_from_renotation_ovoid,
    xy_from_renotation_ovoid,
    xyY_from_renotation,
    munsell_specification_to_xyY,
    munsell_value_ASTMD1535,  # This is the actual function name
    luminance_ASTMD1535,       # Y to munsell value
    normalise_munsell_specification,
    is_grey_munsell_colour,
    munsell_colour_to_munsell_specification,
    munsell_specification_to_munsell_colour,
    xyY_to_munsell_specification
)

# Create test cases for each function
test_data = {}

# 1. Test hue_to_ASTM_hue
print("Testing hue_to_ASTM_hue...")
test_data['hue_to_ASTM_hue'] = []
for code in range(10):  # All hue families
    for hue in [0.0, 2.5, 5.0, 7.5, 8.548, 10.0]:
        try:
            result = hue_to_ASTM_hue([hue, code])
            test_data['hue_to_ASTM_hue'].append({
                'input': [hue, code],
                'output': float(result)
            })
        except:
            pass

# 2. Test ASTM_hue_to_hue - NOT AVAILABLE IN PYTHON
# We'll implement the reverse function ourselves
# print("Testing ASTM_hue_to_hue...")
# test_data['ASTM_hue_to_hue'] = []

# 3. Test hue_to_hue_angle
print("Testing hue_to_hue_angle...")
test_data['hue_to_hue_angle'] = []
for code in range(10):
    for hue in [0.0, 2.5, 5.0, 7.5, 8.548, 10.0]:
        try:
            result = hue_to_hue_angle([hue, code])
            test_data['hue_to_hue_angle'].append({
                'input': [hue, code],
                'output': float(result)
            })
        except:
            pass

# 4. Test hue_angle_to_hue
print("Testing hue_angle_to_hue...")
test_data['hue_angle_to_hue'] = []
for angle in [0, 45, 70, 86.25, 93.062, 102.5, 135, 160, 225, 255, 315, 360]:
    try:
        result = hue_angle_to_hue(angle)
        test_data['hue_angle_to_hue'].append({
            'input': angle,
            'output': [float(result[0]), int(result[1])]
        })
    except:
        pass

# 5. Test bounding_hues_from_renotation
print("Testing bounding_hues_from_renotation...")
test_data['bounding_hues_from_renotation'] = []
for code in range(10):
    for hue in [0.0, 1.0, 2.5, 3.75, 5.0, 7.5, 8.548, 9.5, 10.0]:
        try:
            result = bounding_hues_from_renotation([hue, code])
            test_data['bounding_hues_from_renotation'].append({
                'input': [hue, code],
                'output': [[float(result[0][0]), int(result[0][1])], 
                          [float(result[1][0]), int(result[1][1])]]
            })
        except:
            pass

# 6. Test maximum_chroma_from_renotation
print("Testing maximum_chroma_from_renotation...")
test_data['maximum_chroma_from_renotation'] = []
for value in range(1, 10):
    for code in [0, 3, 4, 5]:  # Sample some families
        for hue in [2.5, 5.0, 7.5, 10.0]:
            try:
                result = maximum_chroma_from_renotation([hue, value, code])
                test_data['maximum_chroma_from_renotation'].append({
                    'input': [hue, value, code],
                    'output': float(result)
                })
            except:
                pass

# 7. Test interpolation_method_from_renotation_ovoid
print("Testing interpolation_method_from_renotation_ovoid...")
test_data['interpolation_method_from_renotation_ovoid'] = []
for value in range(1, 10):
    for chroma in [2, 4, 6, 8, 10, 12]:
        for code in [3, 4]:  # GY family
            for hue in [2.5, 5.0, 7.5, 8.548, 10.0]:
                try:
                    spec = np.array([hue, value, chroma, code])
                    result = interpolation_method_from_renotation_ovoid(spec)
                    test_data['interpolation_method_from_renotation_ovoid'].append({
                        'input': [hue, value, chroma, code],
                        'output': result if result is not None else "None"
                    })
                except:
                    pass

# 8. Test xy_from_renotation_ovoid
print("Testing xy_from_renotation_ovoid...")
test_data['xy_from_renotation_ovoid'] = []
# Use specific test cases we've been debugging
test_cases = [
    (7.5, 9, 6, 4),
    (10.0, 9, 6, 4),
    (8.548, 9, 6, 4),
    (8.0, 9, 6, 4),
    (2.5, 9, 6, 4),
    (5.0, 9, 6, 4),
    (8.548, 8, 6, 4),
    (8.548, 9, 8, 4),
    (8.548, 9, 10, 4),
]
for hue, value, chroma, code in test_cases:
    try:
        spec = np.array([hue, value, chroma, code])
        result = xy_from_renotation_ovoid(spec)
        test_data['xy_from_renotation_ovoid'].append({
            'input': [hue, value, chroma, code],
            'output': [float(result[0]), float(result[1])]
        })
    except:
        pass

# 9. Test luminance_ASTMD1535 (munsell_value to Y)
print("Testing luminance_ASTMD1535...")
test_data['luminance_ASTMD1535'] = []
for value in np.linspace(0, 10, 21):
    try:
        result = luminance_ASTMD1535(value)
        test_data['luminance_ASTMD1535'].append({
            'input': float(value),
            'output': float(result)
        })
    except:
        pass

# 10. Test munsell_value_ASTMD1535 (Y to munsell_value)
print("Testing munsell_value_ASTMD1535...")
test_data['munsell_value_ASTMD1535'] = []
for Y in np.linspace(0, 1, 21):
    try:
        result = munsell_value_ASTMD1535(Y)
        test_data['munsell_value_ASTMD1535'].append({
            'input': float(Y),
            'output': float(result)
        })
    except:
        pass

# 11. Test normalise_munsell_specification
print("Testing normalise_munsell_specification...")
test_data['normalise_munsell_specification'] = []
test_specs = [
    [0.0, 5, 10, 1],    # 0YR -> 10R
    [12.5, 5, 10, 1],   # 12.5YR -> 2.5Y
    [-2.5, 5, 10, 1],   # -2.5YR -> 7.5R
    [8.548, 9, 6, 4],   # Normal case
]
for spec in test_specs:
    try:
        result = normalise_munsell_specification(spec)
        test_data['normalise_munsell_specification'].append({
            'input': spec,
            'output': [float(result[0]), float(result[1]), float(result[2]), int(result[3])]
        })
    except:
        pass

# 12. Test is_grey_munsell_colour
print("Testing is_grey_munsell_colour...")
test_data['is_grey_munsell_colour'] = []
test_specs = [
    [np.nan, 5, np.nan, np.nan],  # Grey
    [5.0, 5, 0, 1],                # Chroma = 0
    [5.0, 5, 10, 1],               # Not grey
]
for spec in test_specs:
    try:
        result = is_grey_munsell_colour(spec)
        test_data['is_grey_munsell_colour'].append({
            'input': spec,
            'output': bool(result)
        })
    except:
        pass

# Convert NaN to null for JSON compatibility
import math

def sanitize_for_json(obj):
    if isinstance(obj, float):
        if math.isnan(obj):
            return None
        return obj
    elif isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(item) for item in obj]
    return obj

# Save to JSON
with open('python_test_data.json', 'w') as f:
    json.dump(sanitize_for_json(test_data), f, indent=2)

print(f"\nGenerated test data for {len(test_data)} functions")
for func, data in test_data.items():
    print(f"  {func}: {len(data)} test cases")