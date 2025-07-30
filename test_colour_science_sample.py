#!/usr/bin/env python3
"""
Test the Python colour-science library against a sample of our reference dataset.
This will help us understand which illuminant (D65 vs C) gives better results quickly.
"""

import csv
import colour
import numpy as np
from typing import List, Tuple
import time

def load_reference_data(filepath: str) -> List[Tuple[Tuple[int, int, int], str]]:
    """Load the reference sRGB to Munsell dataset."""
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

def srgb_to_munsell_d65(rgb: Tuple[int, int, int]) -> str:
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

def srgb_to_munsell_c(rgb: Tuple[int, int, int]) -> str:
    """Convert sRGB to Munsell using Illuminant C with colour-science library."""
    try:
        # Convert RGB (0-255) to normalized sRGB (0-1)
        srgb = np.array([rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0])
        
        # Convert sRGB to XYZ using D65 first, then adapt to Illuminant C
        xyz_d65 = colour.sRGB_to_XYZ(srgb, illuminant=colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65'])
        
        # Chromatic adaptation from D65 to Illuminant C
        xyz_c = colour.chromatic_adaptation(
            xyz_d65,
            colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65'],
            colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C']
        )
        
        # Convert XYZ to xyY
        xyy = colour.XYZ_to_xyY(xyz_c)
        
        # Convert xyY to Munsell using colour-science library
        munsell_colour = colour.notation.munsell.xyY_to_munsell_colour(xyy)
        
        return munsell_colour
        
    except Exception as e:
        return f"ERROR: {str(e)}"

def test_library_accuracy(convert_func, reference_data: List[Tuple[Tuple[int, int, int], str]], name: str, sample_size: int = 100):
    """Test a conversion function against a sample of the reference dataset."""
    print(f"\n=== Testing {name} (sample of {sample_size}) ===")
    
    exact_matches = 0
    errors = 0
    total = min(sample_size, len(reference_data))
    
    start_time = time.time()
    
    # Test sample of colors for analysis
    print("Sample conversions:")
    for i, ((r, g, b), expected) in enumerate(reference_data[:total]):
        result = convert_func((r, g, b))
        match = "✓" if result == expected else "✗"
        
        if i < 10:  # Show first 10 in detail
            print(f"  RGB({r:3d},{g:3d},{b:3d}) -> {result:<15} | Expected: {expected:<15} {match}")
        
        if result == expected:
            exact_matches += 1
        elif result.startswith("ERROR"):
            errors += 1
            if i < 10:  # Show first 10 errors
                print(f"    Error details: {result}")
                
        # Progress indicator
        if (i + 1) % 25 == 0:
            print(f"  Processed {i + 1}/{total} colors...")
    
    end_time = time.time()
    
    accuracy = (exact_matches / total) * 100
    error_rate = (errors / total) * 100
    
    print(f"\n{name} Results:")
    print(f"  Sample size: {total}")
    print(f"  Exact matches: {exact_matches}")
    print(f"  Errors: {errors}")
    print(f"  Accuracy: {accuracy:.3f}%")
    print(f"  Error rate: {error_rate:.3f}%")
    print(f"  Processing time: {end_time - start_time:.2f} seconds")
    
    return {
        'name': name,
        'exact_matches': exact_matches,
        'errors': errors,
        'accuracy': accuracy,
        'error_rate': error_rate,
        'time': end_time - start_time,
        'sample_size': total
    }

def main():
    """Main test function."""
    print("Testing Python colour-science library against sample of reference dataset")
    print("=" * 70)
    
    # Load reference data
    reference_data = load_reference_data('tests/data/srgb-to-munsell.csv')
    print(f"Loaded {len(reference_data)} reference colors")
    
    # Test both illuminants with small sample first
    sample_size = 100
    d65_results = test_library_accuracy(srgb_to_munsell_d65, reference_data, "colour-science with D65", sample_size)
    c_results = test_library_accuracy(srgb_to_munsell_c, reference_data, "colour-science with Illuminant C", sample_size)
    
    # Summary comparison
    print(f"\n{'='*70}")
    print("SUMMARY COMPARISON")
    print(f"{'='*70}")
    print(f"{'Library':<30} {'Accuracy':<12} {'Errors':<8} {'Time':<8}")
    print(f"{'-'*70}")
    print(f"{d65_results['name']:<30} {d65_results['accuracy']:>8.3f}% {d65_results['errors']:>6d} {d65_results['time']:>6.2f}s")
    print(f"{c_results['name']:<30} {c_results['accuracy']:>8.3f}% {c_results['errors']:>6d} {c_results['time']:>6.2f}s")
    
    # Determine best
    if d65_results['accuracy'] > c_results['accuracy']:
        print(f"\n🏆 WINNER: D65 illuminant ({d65_results['accuracy']:.3f}% vs {c_results['accuracy']:.3f}%)")
        best_results = d65_results
    elif c_results['accuracy'] > d65_results['accuracy']:
        print(f"\n🏆 WINNER: Illuminant C ({c_results['accuracy']:.3f}% vs {d65_results['accuracy']:.3f}%)")
        best_results = c_results
    else:
        print(f"\n🤝 TIE: Both illuminants achieve {d65_results['accuracy']:.3f}% accuracy")
        best_results = d65_results
    
    if best_results['accuracy'] > 95.0:
        print(f"✅ Excellent accuracy achieved! Ready for deep-dive analysis.")
        print(f"💡 Recommend testing full dataset with winning illuminant.")
    elif best_results['accuracy'] > 80.0:
        print(f"⚠️  Good accuracy, but may need algorithm refinement.")
        print(f"💡 Recommend investigating specific error patterns.")
    elif best_results['accuracy'] > 50.0:
        print(f"⚠️  Moderate accuracy. Need to investigate library usage.")
        print(f"💡 May need different conversion methods or parameter tuning.")
    else:
        print(f"❌ Low accuracy. Major issues with library usage or approach.")
        print(f"💡 Need to investigate conversion pipeline or try R library instead.")

if __name__ == "__main__":
    main()