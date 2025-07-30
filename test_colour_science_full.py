#!/usr/bin/env python3
"""
Test the Python colour-science library against the COMPLETE 4007-color reference dataset.
This is critical for properly validating which algorithm achieves the target accuracy.
"""

import csv
import colour
import numpy as np
from typing import List, Tuple
import time

def load_reference_data(filepath: str) -> List[Tuple[Tuple[int, int, int], str]]:
    """Load the complete reference sRGB to Munsell dataset."""
    data = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 4:
                r, g, b = int(row[0]), int(row[1]), int(row[2])
                munsell = row[3].strip()
                data.append(((r, g, b), munsell))
    return data

def srgb_to_munsell_d65_full(rgb: Tuple[int, int, int]) -> str:
    """Convert sRGB to Munsell using D65 illuminant with colour-science library."""
    try:
        # Convert RGB (0-255) to normalized sRGB (0-1)
        srgb = np.array([rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0])
        
        # Convert sRGB to XYZ using D65 illuminant
        xyz = colour.sRGB_to_XYZ(srgb, illuminant=colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65'])
        
        # Convert XYZ to xyY
        xyy = colour.XYZ_to_xyY(xyz)
        
        # Convert xyY to Munsell using colour-science library
        munsell_colour = colour.notation.munsell.xyY_to_munsell_colour(xyy)
        
        return munsell_colour
        
    except Exception as e:
        return f"ERROR: {str(e)}"

def test_full_dataset():
    """Test the complete 4007-color dataset - NO SHORTCUTS!"""
    print("TESTING COMPLETE 4007-COLOR DATASET")
    print("=" * 50)
    
    # Load ALL reference colors
    reference_data = load_reference_data('tests/data/srgb-to-munsell.csv')
    total_colors = len(reference_data)
    print(f"Loaded {total_colors} reference colors")
    
    if total_colors != 4007:
        print(f"WARNING: Expected 4007 colors, got {total_colors}")
    
    exact_matches = 0
    errors = 0
    close_matches = 0
    
    start_time = time.time()
    
    print("Processing all colors (this will take several minutes)...")
    
    # Store detailed results for analysis
    results = []
    error_examples = []
    exact_examples = []
    
    for i, ((r, g, b), expected) in enumerate(reference_data):
        result = srgb_to_munsell_d65_full((r, g, b))
        
        is_exact = result == expected
        is_error = result.startswith("ERROR")
        is_close = is_close_match(result, expected) if not is_error and not is_exact else False
        
        if is_exact:
            exact_matches += 1
            if len(exact_examples) < 10:
                exact_examples.append(((r, g, b), expected, result))
        elif is_error:
            errors += 1
            if len(error_examples) < 10:
                error_examples.append(((r, g, b), expected, result))
        elif is_close:
            close_matches += 1
        
        results.append({
            'rgb': (r, g, b),
            'expected': expected,
            'result': result,
            'exact': is_exact,
            'error': is_error,
            'close': is_close
        })
        
        # Progress indicator
        if (i + 1) % 500 == 0:
            elapsed = time.time() - start_time
            remaining = (elapsed / (i + 1)) * (total_colors - i - 1)
            print(f"  Processed {i + 1}/{total_colors} colors... "
                  f"(Elapsed: {elapsed:.1f}s, Est. remaining: {remaining:.1f}s)")
    
    end_time = time.time()
    
    # Calculate statistics
    accuracy = (exact_matches / total_colors) * 100
    error_rate = (errors / total_colors) * 100
    close_match_rate = (close_matches / total_colors) * 100
    combined_accuracy = ((exact_matches + close_matches) / total_colors) * 100
    
    print(f"\n{'='*60}")
    print("COMPLETE DATASET RESULTS")
    print(f"{'='*60}")
    print(f"Total colors tested: {total_colors}")
    print(f"Exact matches: {exact_matches}")
    print(f"Close matches: {close_matches}")
    print(f"Errors: {errors}")
    print(f"Complete misses: {total_colors - exact_matches - close_matches - errors}")
    print(f"")
    print(f"ACCURACY METRICS:")
    print(f"  Exact accuracy: {accuracy:.3f}%")
    print(f"  Close match rate: {close_match_rate:.3f}%")
    print(f"  Combined accuracy: {combined_accuracy:.3f}%")
    print(f"  Error rate: {error_rate:.3f}%")
    print(f"  Processing time: {end_time - start_time:.1f} seconds")
    
    # Show examples
    print(f"\nEXACT MATCH EXAMPLES:")
    for (r, g, b), expected, result in exact_examples[:5]:
        print(f"  RGB({r:3d},{g:3d},{b:3d}) -> {result} ✓")
    
    print(f"\nERROR EXAMPLES:")
    for (r, g, b), expected, result in error_examples[:5]:
        print(f"  RGB({r:3d},{g:3d},{b:3d}) -> {result}")
    
    # Save detailed results
    save_detailed_results(results, accuracy)
    
    return {
        'total': total_colors,
        'exact_matches': exact_matches,
        'close_matches': close_matches,
        'errors': errors,
        'accuracy': accuracy,
        'combined_accuracy': combined_accuracy,
        'time': end_time - start_time
    }

def is_close_match(result: str, expected: str) -> bool:
    """Check if two Munsell notations are close matches."""
    if 'ERROR' in result:
        return False
    
    try:
        # Parse both Munsell notations to compare components
        result_spec = colour.notation.munsell.munsell_colour_to_munsell_specification(result)
        expected_spec = colour.notation.munsell.munsell_colour_to_munsell_specification(expected)
        
        # Check if they're close in hue, value, and chroma
        if np.isnan(result_spec[0]) and np.isnan(expected_spec[0]):  # Both neutral
            return abs(result_spec[1] - expected_spec[1]) < 0.5  # Value difference < 0.5
        elif not (np.isnan(result_spec[0]) or np.isnan(expected_spec[0])):  # Both chromatic
            hue_diff = abs(result_spec[0] - expected_spec[0])
            value_diff = abs(result_spec[1] - expected_spec[1])
            chroma_diff = abs(result_spec[2] - expected_spec[2])
            
            return (hue_diff < 0.5 and value_diff < 0.5 and chroma_diff < 1.0)
        else:
            return False  # One neutral, one chromatic
    except:
        return False

def save_detailed_results(results: List[dict], accuracy: float):
    """Save detailed results for further analysis."""
    filename = f"colour_science_full_results_{accuracy:.1f}pct.csv"
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['R', 'G', 'B', 'Expected', 'Result', 'Exact', 'Error', 'Close'])
        
        for result in results:
            writer.writerow([
                result['rgb'][0], result['rgb'][1], result['rgb'][2],
                result['expected'], result['result'],
                result['exact'], result['error'], result['close']
            ])
    
    print(f"Detailed results saved to: {filename}")

def main():
    """Main test function."""
    print("CRITICAL VALIDATION: Testing Python colour-science on ALL 4007 colors")
    print("This is essential for understanding the true performance of the algorithm")
    print("")
    
    # Test the complete dataset
    results = test_full_dataset()
    
    print(f"\n{'='*60}")
    print("FINAL ASSESSMENT")
    print(f"{'='*60}")
    
    if results['accuracy'] >= 95.0:
        print("🎯 EXCELLENT: Algorithm achieves >95% accuracy")
        print("✅ Ready for Rust implementation with these exact parameters")
    elif results['accuracy'] >= 80.0:
        print("✅ GOOD: Algorithm achieves >80% accuracy")
        print("💡 Good foundation, may need minor refinements")
    elif results['accuracy'] >= 50.0:
        print("⚠️ MODERATE: Algorithm achieves >50% accuracy")
        print("🔧 Significant improvements needed")
    else:
        print("❌ POOR: Algorithm accuracy <50%")
        print("🚨 Major issues - need different approach")
    
    print(f"\nNext steps:")
    print(f"1. Analyze the {results['exact_matches']} exact matches to understand patterns")
    print(f"2. Investigate the {results['errors']} errors to identify edge cases")
    print(f"3. Extract the exact mathematical formulas from colour-science")
    print(f"4. Implement refined algorithm in Rust")

if __name__ == "__main__":
    main()