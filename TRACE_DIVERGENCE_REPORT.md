# Trace Divergence Analysis Report

## Summary Statistics

- **Python trace lines**: 506
- **Rust trace lines**: 2940
- **Matched lines**: 0
- **Divergent lines**: 506
- **Match rate**: 0.00%

## First Divergence Point

**Python Line 8**: `hue_to_hue_angle:1`
```
hue_to_hue_angle:1 | vars: hue=[5.2525664279057658, 3.0] | action: ENTER hue to angle conversion
```

**Rust Line 17**: `hue_to_hue_angle:1`
```
hue_to_hue_angle:1 | vars: hue=5.2417998371, code=3 | action: ENTER 
```

**Divergent Variable**: `hue`
- Python value: `[5.252566427905766, 3.0]`
- Rust value: `5.2417998371`
- Reason: Type mismatch: list vs float

### Context (5 lines before and after)

See detailed line-by-line comparison in the CSV output.

## Detailed Line Analysis

### Divergence 1

**Python**: Line 1 - `sRGB_to_xyY` - CALC normalized RGB from 0-255 to 0-1
**Rust**: No corresponding line found
**Status**: no_corresponding_rust_line


### Divergence 2

**Python**: Line 2 - `sRGB_to_xyY` - ENTER converting sRGB to xyY
**Rust**: No corresponding line found
**Status**: no_corresponding_rust_line


### Divergence 3

**Python**: Line 3 - `sRGB_to_xyY` - CALL calling sRGB_to_XYZ
**Rust**: No corresponding line found
**Status**: no_corresponding_rust_line


### Divergence 4

**Python**: Line 4 - `sRGB_to_xyY` - CALC XYZ calculated
**Rust**: No corresponding line found
**Status**: no_corresponding_rust_line


### Divergence 5

**Python**: Line 5 - `sRGB_to_xyY` - CALL calling XYZ_to_xyY
**Rust**: No corresponding line found
**Status**: no_corresponding_rust_line


### Divergence 6

**Python**: Line 6 - `sRGB_to_xyY` - RETURN xyY calculated
**Rust**: No corresponding line found
**Status**: no_corresponding_rust_line


### Divergence 7

**Python**: Line 7 - `_xyY_to_munsell_specification` - ENTER internal algorithm entry
**Rust**: Line 1 - `xyy_to_munsell_specification` - ENTER 
**Status**: variable_mismatch

**Variable Comparisons**:
- `xyY`: Python=`[0.3016456112282535, 0.3289687107839026, 0.8269427000458324]`, Rust=`MISSING` - Variable not found in Rust trace

### Divergence 8

**Python**: Line 8 - `hue_to_hue_angle` - ENTER hue to angle conversion
**Rust**: Line 17 - `hue_to_hue_angle` - ENTER 
**Status**: variable_mismatch

**Variable Comparisons**:
- `hue`: Python=`[5.252566427905766, 3.0]`, Rust=`5.2417998371` - Type mismatch: list vs float

### Divergence 9

**Python**: Line 9 - `hue_to_hue_angle` - RETURN angle calculated
**Rust**: Line 28 - `hue_to_hue_angle` - RETURN interpolated angle
**Status**: variable_mismatch

**Variable Comparisons**:
- `result`: Python=`135.6314160697644`, Rust=`135.6044995926` - Float diff: 2.69e-02

### Divergence 10

**Python**: Line 10 - `maximum_chroma_from_renotation` - ENTER maximum chroma lookup
**Rust**: Line 30 - `maximum_chroma_from_renotation` - ENTER 
**Status**: variable_mismatch

**Variable Comparisons**:
- `hue`: Python=`[5.252566427905766, 9.277406395397769, 3.0]`, Rust=`5.2417998371` - Type mismatch: list vs float
- `value`: Python=`None`, Rust=`9.2773635406` - Type mismatch: NoneType vs float

... (remaining divergences truncated, see CSV for complete data)

## Recommendations

1. Focus investigation on the first divergence point
2. Check mathematical formula implementation in Rust
3. Verify floating point precision handling
4. Compare intermediate calculation steps
