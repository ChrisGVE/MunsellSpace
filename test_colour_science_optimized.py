#!/usr/bin/env python3
"""
Optimized test of Python colour-science library on ALL 4007 colors.
Uses batch processing and reduced verbosity for faster execution.
"""

import csv
import colour
import numpy as np
from typing import List, Tuple
import time
import warnings

# Suppress verbose warnings to speed up processing
warnings.filterwarnings('ignore')

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

def batch_convert_srgb_to_munsell(rgb_list: List[Tuple[int, int, int]], batch_size: int = 50) -> List[str]:
    """Convert RGB colors to Munsell in batches for efficiency."""
    results = []
    
    for i in range(0, len(rgb_list), batch_size):
        batch = rgb_list[i:i + batch_size]
        batch_results = []
        
        for rgb in batch:
            try:
                # Convert RGB (0-255) to normalized sRGB (0-1)
                srgb = np.array([rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0])
                
                # Convert sRGB to XYZ using D65 illuminant
                xyz = colour.sRGB_to_XYZ(srgb)
                
                # Convert XYZ to xyY
                xyy = colour.XYZ_to_xyY(xyz)
                
                # Convert xyY to Munsell
                munsell_colour = colour.notation.munsell.xyY_to_munsell_colour(xyy)
                batch_results.append(munsell_colour)
                
            except Exception as e:
                batch_results.append(f"ERROR: {str(e)[:50]}")
        
        results.extend(batch_results)
        
        # Progress update every 1000 colors
        if i % 1000 == 0:
            print(f"  Processed {min(i + batch_size, len(rgb_list))}/{len(rgb_list)} colors...")
    
    return results

def analyze_results(reference_data: List[Tuple[Tuple[int, int, int], str]], results: List[str]):
    """Analyze the conversion results."""
    total_colors = len(reference_data)
    exact_matches = 0
    errors = 0
    close_matches = 0
    
    # Sample detailed analysis
    exact_examples = []
    error_examples = []
    miss_examples = []
    
    for i, (((r, g, b), expected), result) in enumerate(zip(reference_data, results)):
        is_exact = result == expected
        is_error = result.startswith("ERROR")
        is_close = is_close_match(result, expected) if not is_error and not is_exact else False
        
        if is_exact:
            exact_matches += 1
            if len(exact_examples) < 10:
                exact_examples.append((r, g, b, expected, result))
        elif is_error:
            errors += 1
            if len(error_examples) < 10:
                error_examples.append((r, g, b, expected, result))
        elif is_close:
            close_matches += 1
        else:
            if len(miss_examples) < 10:
                miss_examples.append((r, g, b, expected, result))
    
    # Calculate statistics
    accuracy = (exact_matches / total_colors) * 100
    error_rate = (errors / total_colors) * 100
    close_match_rate = (close_matches / total_colors) * 100
    combined_accuracy = ((exact_matches + close_matches) / total_colors) * 100
    
    return {
        'total': total_colors,
        'exact_matches': exact_matches,
        'close_matches': close_matches,
        'errors': errors,
        'accuracy': accuracy,
        'error_rate': error_rate,
        'close_match_rate': close_match_rate,
        'combined_accuracy': combined_accuracy,
        'exact_examples': exact_examples,
        'error_examples': error_examples,
        'miss_examples': miss_examples
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

def main():
    """Main test function."""
    print("COMPLETE 4007-COLOR DATASET VALIDATION")
    print("Testing Python colour-science library accuracy")
    print("=" * 50)
    
    # Load ALL reference colors
    reference_data = load_reference_data('tests/data/srgb-to-munsell.csv')
    total_colors = len(reference_data)
    print(f"Loaded {total_colors} reference colors")
    
    if total_colors != 4007:
        print(f"WARNING: Expected 4007 colors, got {total_colors}")
    
    # Extract RGB values for batch processing
    rgb_list = [rgb for rgb, _ in reference_data]
    
    print("Converting all colors with D65 illuminant...")
    start_time = time.time()
    
    # Batch convert all colors
    results = batch_convert_srgb_to_munsell(rgb_list)
    
    end_time = time.time()
    
    print(f"Conversion completed in {end_time - start_time:.1f} seconds")
    print("Analyzing results...")
    
    # Analyze results
    analysis = analyze_results(reference_data, results)
    
    # Print comprehensive results
    print(f"\n{'='*60}")
    print("COMPLETE DATASET RESULTS - ALL 4007 COLORS")
    print(f"{'='*60}")
    print(f"Total colors tested: {analysis['total']}")
    print(f"Exact matches: {analysis['exact_matches']}")
    print(f"Close matches: {analysis['close_matches']}")
    print(f"Errors: {analysis['errors']}")
    print(f"Complete misses: {analysis['total'] - analysis['exact_matches'] - analysis['close_matches'] - analysis['errors']}")
    print(f"")
    print(f"ACCURACY METRICS:")
    print(f"  Exact accuracy: {analysis['accuracy']:.3f}%")
    print(f"  Close match rate: {analysis['close_match_rate']:.3f}%")
    print(f"  Combined accuracy: {analysis['combined_accuracy']:.3f}%")
    print(f"  Error rate: {analysis['error_rate']:.3f}%")
    print(f"  Processing time: {end_time - start_time:.1f} seconds")
    
    # Show examples
    print(f"\nEXACT MATCH EXAMPLES:")
    for r, g, b, expected, result in analysis['exact_examples'][:5]:
        print(f"  RGB({r:3d},{g:3d},{b:3d}) -> {result} ✓")
    
    print(f"\nERROR EXAMPLES:")
    for r, g, b, expected, result in analysis['error_examples'][:3]:
        print(f"  RGB({r:3d},{g:3d},{b:3d}) -> {result}")
    
    print(f"\nMISS EXAMPLES (not exact, not close):")
    for r, g, b, expected, result in analysis['miss_examples'][:3]:
        print(f"  RGB({r:3d},{g:3d},{b:3d}) -> {result} (expected: {expected})")
    
    # Save results summary
    filename = f"colour_science_complete_results_{analysis['accuracy']:.1f}pct.txt"
    with open(filename, 'w') as f:
        f.write("COMPLETE 4007-COLOR DATASET RESULTS\n")
        f.write("="*50 + "\n")
        f.write(f"Total colors: {analysis['total']}\n")
        f.write(f"Exact matches: {analysis['exact_matches']}\n")
        f.write(f"Close matches: {analysis['close_matches']}\n")
        f.write(f"Errors: {analysis['errors']}\n")
        f.write(f"Exact accuracy: {analysis['accuracy']:.3f}%\n")
        f.write(f"Combined accuracy: {analysis['combined_accuracy']:.3f}%\n")
        f.write(f"Processing time: {end_time - start_time:.1f} seconds\n")
    
    print(f"\nResults summary saved to: {filename}")
    
    # Final assessment
    print(f"\n{'='*60}")
    print("CRITICAL ASSESSMENT")
    print(f"{'='*60}")
    
    if analysis['accuracy'] >= 99.0:
        print("🎯 OUTSTANDING: >99% exact accuracy - READY FOR PRODUCTION")
    elif analysis['accuracy'] >= 90.0:
        print("🏆 EXCELLENT: >90% exact accuracy - Excellent foundation")
    elif analysis['accuracy'] >= 80.0:
        print("✅ VERY GOOD: >80% exact accuracy - Strong reference implementation")
    elif analysis['accuracy'] >= 70.0:
        print("✅ GOOD: >70% exact accuracy - Good foundation for Rust implementation")
    elif analysis['accuracy'] >= 50.0:
        print("⚠️ MODERATE: >50% exact accuracy - Needs investigation")
    else:
        print("❌ POOR: <50% exact accuracy - Major issues")
    
    print(f"\nThis validates whether colour-science is suitable as reference implementation")
    print(f"Target for Rust implementation: {analysis['accuracy']:.1f}% exact accuracy")
    
    return analysis

if __name__ == "__main__":
    main()