# Munsell Color Space Conversion Algorithm Specification

## Overview

This document provides the complete, authoritative specification for converting between sRGB and Munsell color notations using mathematical methods. The algorithm is based on the Python colour-science library implementation and follows ASTM D1535 standards.

**Version**: 3.0  
**Date**: 2025-01-03  
**Status**: Complete specification from systematic line-by-line analysis

## 1. Core Conversion Pipeline

```
sRGB [0-255] → Linear RGB [0-1] → XYZ (D65) → xyY → Munsell Specification → Munsell Notation
```

## 2. Constants and Parameters

### 2.1 Critical Constants
- **THRESHOLD_ACHROMATIC**: `1e-3` - Distance threshold for achromatic detection
- **CONVERGENCE_THRESHOLD**: `1e-7` - Convergence criterion (THRESHOLD_ACHROMATIC / 1e4)
- **MAX_ITERATIONS_OUTER**: `64` - Maximum outer loop iterations
- **MAX_ITERATIONS_INNER**: `16` - Maximum inner loop iterations (both hue and chroma)

### 2.2 Illuminants
- **Illuminant D65**: `[0.31270, 0.32900]` - sRGB reference white
- **Illuminant C**: `[0.31006, 0.31616]` - Munsell reference white (CCS_ILLUMINANT_MUNSELL)

### 2.3 Color Space Matrices
```
sRGB to XYZ (D65):
[0.4124564  0.3575761  0.1804375]
[0.2126729  0.7151522  0.0721750]
[0.0193339  0.1191920  0.9503041]
```

## 3. Sub-Algorithm: sRGB to xyY Conversion

### 3.1 sRGB to Linear RGB
```python
def srgb_to_linear(c):
    c_norm = c / 255.0
    if c_norm <= 0.04045:
        return c_norm / 12.92
    else:
        return ((c_norm + 0.055) / 1.055) ** 2.4
```

### 3.2 Linear RGB to XYZ
```python
def linear_rgb_to_xyz(r_linear, g_linear, b_linear):
    X = 0.4124564 * r_linear + 0.3575761 * g_linear + 0.1804375 * b_linear
    Y = 0.2126729 * r_linear + 0.7151522 * g_linear + 0.0721750 * b_linear
    Z = 0.0193339 * r_linear + 0.1191920 * g_linear + 0.9503041 * b_linear
    return [X, Y, Z]
```

### 3.3 XYZ to xyY
```python
def xyz_to_xyy(X, Y, Z):
    total = X + Y + Z
    if total == 0:
        # Use Illuminant C as default
        return [0.31006, 0.31616, 0.0]
    else:
        x = X / total
        y = Y / total
        return [x, y, Y]
```

## 4. Sub-Algorithm: ASTM D1535 Munsell Value

### 4.1 Luminance to Munsell Value
```python
def luminance_to_munsell_value(Y):
    """Y in range [0, 1], returns V in range [0, 10]"""
    Y_percent = Y * 100  # Convert to percentage
    
    # ASTM D1535 quintic polynomial
    V = (1.1914 * Y_percent 
         - 0.22533 * (Y_percent ** 2)
         + 0.23352 * (Y_percent ** 3)
         - 0.020484 * (Y_percent ** 4)
         + 0.00081939 * (Y_percent ** 5))
    
    # Round if close to integer (within float precision)
    if abs(V - round(V)) < 1e-10:  # is_integer check
        V = round(V)
    
    return V
```

### 4.2 Munsell Value to Luminance (Inverse)
Uses Newton-Raphson iteration or pre-computed lookup table with linear interpolation.

## 5. Main Algorithm: xyY to Munsell Specification

### 5.1 Input Processing and Initial Setup
```python
def xyy_to_munsell(x, y, Y):
    # Step 1: Calculate Munsell value
    value = luminance_to_munsell_value(Y)
    
    # Step 2: Get achromatic center for this value
    # CRITICAL: Achromatic center is ALWAYS Illuminant C
    x_center, y_center = [0.31006, 0.31616]
    
    # Step 3: Calculate polar coordinates relative to achromatic center
    rho_input = sqrt((x - x_center)**2 + (y - y_center)**2)
    phi_input = degrees(atan2(y - y_center, x - x_center))
    
    # Step 4: Check if achromatic
    if rho_input < THRESHOLD_ACHROMATIC:  # 1e-3
        return normalise_munsell_specification([nan, value, nan, nan])
```

### 5.2 Initial Guess Generation
```python
    # Step 5: Convert to XYZ for Lab calculation
    XYZ = xyY_to_XYZ([x, y, Y])
    
    # Step 6: CRITICAL - Create custom reference white scaled by Y
    XYZ_w = [Y * 0.31006/0.31616,  # X_w
             Y,                      # Y_w
             Y * (1-0.31006-0.31616)/0.31616]  # Z_w
    
    # Step 7: Convert to Lab using custom reference
    Lab = XYZ_to_Lab(XYZ, XYZ_w)
    LCHab = Lab_to_LCH(Lab)
    
    # Step 8: Generate initial guess
    hue_initial, code = LCHab_to_munsell_specification(LCHab)
    chroma_initial = LCHab.C / 5 * (5 / 5.5)  # Convergence factor
    
    specification_current = [hue_initial, value, chroma_initial, code]
```

### 5.3 Main Iterative Loop
```python
    iterations = 0
    while iterations <= MAX_ITERATIONS_OUTER:
        iterations += 1
        
        hue_current, _, chroma_current, code_current = specification_current
        hue_angle_current = hue_to_hue_angle(hue_current, code_current)
        
        # CRITICAL: Cap chroma at maximum (FIRST TIME)
        chroma_maximum = maximum_chroma_from_renotation(hue_current, value, code_current)
        if chroma_current > chroma_maximum:
            chroma_current = chroma_maximum
            specification_current[2] = chroma_current
```

### 5.4 First Inner Loop: Hue Refinement
```python
        # Calculate current position
        x_current, y_current = munsell_specification_to_xy(specification_current)
        rho_current = sqrt((x_current - x_center)**2 + (y_current - y_center)**2)
        phi_current = degrees(atan2(y_current - y_center, x_current - x_center))
        
        # Calculate phi difference with wraparound
        phi_current_difference = (360 - phi_input + phi_current) % 360
        if phi_current_difference > 180:
            phi_current_difference -= 360
        
        # Initialize data arrays
        phi_differences_data = [phi_current_difference]
        hue_angles_differences_data = [0]
        iterations_inner = 0
        extrapolate = False
        
        # Inner loop: Find bracketing hue angles
        while (sign(min(phi_differences_data)) == sign(max(phi_differences_data)) 
               and not extrapolate):
            iterations_inner += 1
            
            if iterations_inner > MAX_ITERATIONS_INNER:
                raise RuntimeError("Maximum inner iterations exceeded")
            
            # Calculate new hue angle
            hue_angle_inner = (hue_angle_current + 
                              iterations_inner * (phi_input - phi_current)) % 360
            hue_angle_difference_inner = (iterations_inner * 
                                         (phi_input - phi_current)) % 360
            if hue_angle_difference_inner > 180:
                hue_angle_difference_inner -= 360
            
            hue_inner, code_inner = hue_angle_to_hue(hue_angle_inner)
            
            # CRITICAL: Enable extrapolation after 2 points
            if len(phi_differences_data) >= 2:
                extrapolate = True
            
            if not extrapolate:
                # Calculate phi for this hue
                x_inner, y_inner = munsell_specification_to_xy(
                    [hue_inner, value, chroma_current, code_inner])
                phi_inner = degrees(atan2(y_inner - y_center, x_inner - x_center))
                phi_inner_difference = (360 - phi_input + phi_inner) % 360
                if phi_inner_difference > 180:
                    phi_inner_difference -= 360
                
                phi_differences_data.append(phi_inner_difference)
                hue_angles_differences_data.append(hue_angle_difference_inner)
```

### 5.5 Hue Interpolation/Extrapolation
```python
        # Sort by phi differences
        phi_differences = array(phi_differences_data)
        hue_angles_differences = array(hue_angles_differences_data)
        sort_indices = argsort(phi_differences)
        phi_differences = phi_differences[sort_indices]
        hue_angles_differences = hue_angles_differences[sort_indices]
        
        # CRITICAL: Use Extrapolator for hue to find zero crossing
        interpolator = LinearInterpolator(phi_differences, hue_angles_differences)
        extrapolator = Extrapolator(interpolator)
        hue_angle_difference_new = extrapolator(0) % 360
        hue_angle_new = (hue_angle_current + hue_angle_difference_new) % 360
        
        # Update specification with new hue
        hue_new, code_new = hue_angle_to_hue(hue_angle_new)
        specification_current = [hue_new, value, chroma_current, code_new]
        
        # Check convergence
        x_current, y_current = munsell_specification_to_xy(specification_current)
        difference = euclidean_distance([x, y], [x_current, y_current])
        if difference < CONVERGENCE_THRESHOLD:
            return normalise_munsell_specification(specification_current)
```

### 5.6 Second Inner Loop: Chroma Refinement
```python
        # CRITICAL: Cap chroma at maximum (SECOND TIME)
        hue_current, _, chroma_current, code_current = specification_current
        chroma_maximum = maximum_chroma_from_renotation(hue_current, value, code_current)
        if chroma_current > chroma_maximum:
            chroma_current = chroma_maximum
            specification_current[2] = chroma_current
        
        # Calculate current rho
        x_current, y_current = munsell_specification_to_xy(specification_current)
        rho_current = sqrt((x_current - x_center)**2 + (y_current - y_center)**2)
        
        # Initialize bounds
        rho_bounds_data = [rho_current]
        chroma_bounds_data = [chroma_current]
        iterations_inner = 0
        
        # Inner loop: Find bracketing rho values
        while not (min(rho_bounds_data) < rho_input < max(rho_bounds_data)):
            iterations_inner += 1
            
            if iterations_inner > MAX_ITERATIONS_INNER:
                raise RuntimeError("Maximum inner iterations exceeded")
            
            # Calculate new chroma using power scaling
            # CRITICAL: Use safe division mode
            if rho_current == 0:
                chroma_inner = chroma_current
            else:
                chroma_inner = ((rho_input / rho_current) ** iterations_inner) * chroma_current
            
            # Cap at maximum
            if chroma_inner > chroma_maximum:
                chroma_inner = chroma_maximum
            
            # Calculate rho for this chroma
            x_inner, y_inner = munsell_specification_to_xy(
                [hue_current, value, chroma_inner, code_current])
            rho_inner = sqrt((x_inner - x_center)**2 + (y_inner - y_center)**2)
            
            rho_bounds_data.append(rho_inner)
            chroma_bounds_data.append(chroma_inner)
```

### 5.7 Chroma Interpolation
```python
        # Sort by rho
        rho_bounds = array(rho_bounds_data)
        chroma_bounds = array(chroma_bounds_data)
        sort_indices = argsort(rho_bounds)
        rho_bounds = rho_bounds[sort_indices]
        chroma_bounds = chroma_bounds[sort_indices]
        
        # CRITICAL: Use LinearInterpolator only (NO extrapolation for chroma)
        chroma_new = LinearInterpolator(rho_bounds, chroma_bounds)(rho_input)
        
        # Update specification
        specification_current = [hue_current, value, chroma_new, code_current]
        
        # Check convergence
        x_current, y_current = munsell_specification_to_xy(specification_current)
        difference = euclidean_distance([x, y], [x_current, y_current])
        if difference < CONVERGENCE_THRESHOLD:
            return normalise_munsell_specification(specification_current)
    
    # If we get here, maximum iterations exceeded
    raise RuntimeError("Maximum outer iterations exceeded")
```

## 6. Normalization Rules

### 6.1 Normalise Munsell Specification
```python
def normalise_munsell_specification(specification):
    hue, value, chroma, code = specification
    
    # Check if grey/achromatic
    if is_grey_munsell_colour(specification):
        return [nan, value, nan, nan]
    
    # CRITICAL: 0YR is equivalent to 10R
    if hue == 0:
        hue = 10
        code = (code + 1) % 10
    
    # CRITICAL: Zero chroma returns achromatic
    if chroma == 0:
        return [nan, value, nan, nan]
    
    return [hue, value, chroma, code]
```

### 6.2 Is Grey Munsell Colour
```python
def is_grey_munsell_colour(specification):
    # Returns True if specification contains only value (all others are nan)
    non_nan = specification[~isnan(specification)]
    return len(non_nan) == 1  # Only value is present
```

## 7. Helper Functions

### 7.1 Munsell Specification to xy
```python
def munsell_specification_to_xy(specification):
    specification = normalise_munsell_specification(specification)
    
    # CRITICAL: Grey colors return Illuminant C coordinates
    if is_grey_munsell_colour(specification):
        return [0.31006, 0.31616]
    
    # Otherwise, interpolate from renotation data
    return interpolate_from_renotation_data(specification)
```

### 7.2 Hue Angle Conversions
```python
HUE_FAMILIES = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']

def hue_to_hue_angle(hue, code):
    """Convert hue (0-10) and family code (0-9) to angle (0-360)"""
    return code * 36 + hue * 3.6

def hue_angle_to_hue(angle):
    """Convert angle (0-360) to hue (0-10) and family code (0-9)"""
    angle = angle % 360
    code = int(angle / 36)
    hue = (angle % 36) / 3.6
    return hue, code
```

## 8. Critical Implementation Details

### 8.1 Major Requirements
1. **Custom Lab Reference White**: Must scale XYZ_w by input luminance Y
2. **Achromatic Center**: Always use Illuminant C coordinates [0.31006, 0.31616]
3. **Normalization**: Implement 0YR→10R and chroma==0→achromatic rules
4. **Interpolation Strategy**: Extrapolator for hue, LinearInterpolator for chroma
5. **Chroma Capping**: Must cap TWICE per outer iteration

### 8.2 Convergence Details
- Convergence threshold: 1e-7 (euclidean distance in xy space)
- Check convergence after EACH inner loop (not just at end)
- Enable extrapolation after 2 points for hue refinement

### 8.3 Edge Cases
- Pure black [0,0,0] → "N 0.0"
- Pure white [255,255,255] → "N 9.5" (approximately)
- Zero chroma colors → Achromatic "N x.x" notation
- 0YR colors → Convert to 10R

## 9. Validation Criteria

The implementation should achieve:
- ≤0.1 difference in all dimensions (hue, value, chroma) for all 4007 reference colors
- Maximum 2 family mismatches (matching Python colour-science)
- Exact achromatic handling for grey colors

## 10. Version History

- v1.0: Initial specification
- v2.0: Added normalization rules and convergence details
- v3.0: Complete rewrite from systematic line-by-line analysis of Python implementation