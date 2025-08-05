# Python colour-science Functions to Port 1:1

This document lists all functions from Python's colour-science library that need to be ported exactly to achieve 100% accuracy.

## Core Conversion Functions

### 1. `_xyY_to_munsell_specification` (Main algorithm)
- **Status**: Mostly ported, but needs verification
- **Location**: `colour/notation/munsell.py`
- **Key aspects**:
  - Dual-loop iterative algorithm
  - Convergence criteria
  - Initial guess generation
  - Hue and chroma refinement

### 2. `_xy_from_renotation_ovoid` 
- **Status**: Partially ported, interpolation differs
- **Location**: `colour/notation/munsell.py`
- **Key aspects**:
  - Hue interpolation between boundaries
  - Chroma interpolation
  - Value plane interpolation
  - Exact data lookup logic

### 3. `_bounding_hues_from_renotation`
- **Status**: Ported but needs verification
- **Location**: `colour/notation/munsell.py`
- **Key aspects**:
  - Finding clockwise/counter-clockwise boundaries
  - Handling wraparound (e.g., from PB to B)
  - Standard hue definitions

### 4. `_maximum_chroma_from_renotation`
- **Status**: Custom implementation, not 1:1 port
- **Location**: `colour/notation/munsell.py`
- **Key aspects**:
  - Finding maximum chroma for given hue/value
  - Interpolation when exact match not found
  - Default values when no data available

### 5. `_munsell_specification_to_xyY`
- **Status**: Needs verification
- **Location**: `colour/notation/munsell.py`
- **Key aspects**:
  - Value interpolation between planes
  - Coordinate transformation
  - Illuminant handling

### 6. `_munsell_value_to_Y`
- **Status**: Ported (ASTM polynomial)
- **Location**: `colour/notation/munsell.py`
- **Key aspects**:
  - ASTM D1535 polynomial
  - Scaling factors

### 7. `_Y_to_munsell_value`
- **Status**: Ported (Newton-Raphson)
- **Location**: `colour/notation/munsell.py`
- **Key aspects**:
  - Newton-Raphson iteration
  - Convergence criteria
  - Initial guess

## Interpolation Functions

### 8. `_interpolation_method_from_renotation_ovoid`
- **Status**: Not properly ported
- **Location**: `colour/notation/munsell.py`
- **Returns**: Interpolation method based on data availability

### 9. Linear interpolation logic
- **Status**: Custom implementation
- **Key aspects**:
  - Exact Python numpy.interp behavior
  - Boundary handling
  - Extrapolation rules

## Data Access Functions

### 10. Renotation data access
- **Status**: Need to verify data matches exactly
- **Key aspects**:
  - Data structure format
  - Key formatting (e.g., "2.5R 5/10")
  - Coordinate values precision

## Helper Functions

### 11. `_hue_to_hue_angle` / `_hue_angle_to_hue`
- **Status**: Ported but had bugs
- **Key aspects**:
  - Modulo arithmetic
  - Family code handling

### 12. `_normalise_munsell_specification`
- **Status**: Ported
- **Key aspects**:
  - 0YR → 10R conversion
  - Hue wraparound

## Testing Strategy

For each function:
1. Create a Python script that calls the function with various inputs
2. Save the outputs to a file
3. Create a Rust unit test that compares against these outputs
4. Ensure 100% match including edge cases

## Priority Order

1. `_xy_from_renotation_ovoid` - Most critical difference
2. `_maximum_chroma_from_renotation` - Affects convergence
3. `_interpolation_method_from_renotation_ovoid` - Determines interpolation
4. `_bounding_hues_from_renotation` - Verify correctness
5. Data verification - Ensure renotation data matches