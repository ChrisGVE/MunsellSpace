# Trace Divergence Analysis Report

## Summary Statistics

- **Python trace lines**: 503
- **Rust trace lines**: 2940
- **Matched lines**: 2
- **Divergent lines**: 501
- **Match rate**: 0.40%

## First Divergence Point

**Python Line 4**: `hue_to_hue_angle:1`
```
hue_to_hue_angle:1 | vars: hue=[5.2417998370553125, 3.0] | action: ENTER hue to angle conversion
```

**Rust Line 17**: `hue_to_hue_angle:1`
```
hue_to_hue_angle:1 | vars: hue=5.2417998371, code=3 | action: ENTER 
```

**Divergent Variable**: `hue`
- Python value: `[5.2417998370553125, 3.0]`
- Rust value: `5.2417998371`
- Reason: Type mismatch: list vs float

### Context (5 lines before and after)

See detailed line-by-line comparison in the CSV output.

## Detailed Line Analysis

### Divergence 1

**Python**: Line 1 - `xyY_to_munsell_specification` - ENTER main conversion function
**Rust**: No corresponding line found
**Status**: no_corresponding_rust_line


### Divergence 2

**Python**: Line 2 - `xyY_to_munsell_specification` - CALL calling original xyY_to_munsell_specification
**Rust**: No corresponding line found
**Status**: no_corresponding_rust_line


### Divergence 3

**Python**: Line 3 - `_xyY_to_munsell_specification` - ENTER internal algorithm entry
**Rust**: Line 1 - `xyy_to_munsell_specification` - ENTER 
**Status**: variable_mismatch

**Variable Comparisons**:
- `xyY`: Python=`[0.3016555411, 0.3289901051, 0.8269331673]`, Rust=`MISSING` - Variable not found in Rust trace

### Divergence 4

**Python**: Line 4 - `hue_to_hue_angle` - ENTER hue to angle conversion
**Rust**: Line 17 - `hue_to_hue_angle` - ENTER 
**Status**: variable_mismatch

**Variable Comparisons**:
- `hue`: Python=`[5.2417998370553125, 3.0]`, Rust=`5.2417998371` - Type mismatch: list vs float

### Divergence 5

**Python**: Line 6 - `maximum_chroma_from_renotation` - ENTER maximum chroma lookup
**Rust**: Line 30 - `maximum_chroma_from_renotation` - ENTER 
**Status**: variable_mismatch

**Variable Comparisons**:
- `hue`: Python=`[5.2417998370553125, 9.277363517309352, 3.0]`, Rust=`5.2417998371` - Type mismatch: list vs float
- `value`: Python=`None`, Rust=`9.2773635406` - Type mismatch: NoneType vs float

### Divergence 6

**Python**: Line 7 - `bounding_hues_from_renotation` - ENTER bounding hues calculation
**Rust**: No corresponding line found
**Status**: no_corresponding_rust_line


### Divergence 7

**Python**: Line 8 - `bounding_hues_from_renotation` - RETURN bounding hues found
**Rust**: No corresponding line found
**Status**: no_corresponding_rust_line


### Divergence 8

**Python**: Line 9 - `maximum_chroma_from_renotation` - RETURN maximum chroma found
**Rust**: Line 32 - `maximum_chroma_from_renotation` - RETURN 
**Status**: variable_mismatch

**Variable Comparisons**:
- `result`: Python=`17.82325068853272`, Rust=`17.8232501551` - Float diff: 5.33e-07

### Divergence 9

**Python**: Line 10 - `xy_from_renotation_ovoid` - ENTER xy coordinate calculation
**Rust**: No corresponding line found
**Status**: no_corresponding_rust_line


### Divergence 10

**Python**: Line 11 - `bounding_hues_from_renotation` - ENTER bounding hues calculation
**Rust**: No corresponding line found
**Status**: no_corresponding_rust_line


... (remaining divergences truncated, see CSV for complete data)

## Recommendations

1. Focus investigation on the first divergence point
2. Check mathematical formula implementation in Rust
3. Verify floating point precision handling
4. Compare intermediate calculation steps
