#!/usr/bin/env python3
"""
Test Python colour-science library with a representative sample from all 4007 colors.
Uses systematic sampling to ensure results represent the complete dataset.
"""

import csv
import colour
import numpy as np
from typing import List, Tuple
import time
import warnings

# Suppress verbose warnings
warnings.filterwarnings('ignore')

def load_representative_sample(filepath: str, sample_size: int = 1000) -> List[Tuple[Tuple[int, int, int], str]]:
    """Load a representative sample from the complete dataset using systematic sampling."""
    # First, load all data
    all_data = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 4:
                r, g, b = int(row[0]), int(row[1]), int(row[2])
                munsell = row[3].strip()
                all_data.append(((r, g, b), munsell))
    
    total_colors = len(all_data)
    print(f"Total dataset: {total_colors} colors")
    
    # Use systematic sampling to get representative sample
    step = total_colors // sample_size
    sample_data = []
    
    for i in range(0, total_colors, step):
        if len(sample_data) < sample_size:
            sample_data.append(all_data[i])
    
    print(f"Selected representative sample: {len(sample_data)} colors")
    return sample_data

def test_representative_sample():
    """Test representative sample to extrapolate full dataset performance."""
    print("REPRESENTATIVE SAMPLING TEST - ALL 4007 COLORS")
    print("=" * 50)
    
    # Load representative sample
    sample_data = load_representative_sample('tests/data/srgb-to-munsell.csv', 1000)
    
    exact_matches = 0
    errors = 0
    close_matches = 0
    total = len(sample_data)
    
    # Store examples
    exact_examples = []
    error_examples = []
    miss_examples = []
    
    start_time = time.time()
    
    print("Processing representative sample...")
    
    for i, ((r, g, b), expected) in enumerate(sample_data):
        try:
            # Convert using colour-science
            srgb = np.array([r/255.0, g/255.0, b/255.0])
            xyz = colour.sRGB_to_XYZ(srgb)
            xyy = colour.XYZ_to_xyY(xyz)
            result = colour.notation.munsell.xyY_to_munsell_colour(xyy)
            
            is_exact = result == expected
            is_error = result.startswith("ERROR")
            is_close = is_close_match(result, expected) if not is_error and not is_exact else False
            
            if is_exact:
                exact_matches += 1
                if len(exact_examples) < 20:
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
            
        except Exception as e:
            errors += 1
            if len(error_examples) < 10:
                error_examples.append((r, g, b, expected, f"EXCEPTION: {str(e)[:50]}"))
        
        # Progress
        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{total} colors...")
    
    end_time = time.time()
    
    # Calculate statistics
    accuracy = (exact_matches / total) * 100
    error_rate = (errors / total) * 100
    close_match_rate = (close_matches / total) * 100
    combined_accuracy = ((exact_matches + close_matches) / total) * 100
    
    # Extrapolate to full dataset
    estimated_exact_4007 = int((exact_matches / total) * 4007)
    estimated_close_4007 = int((close_matches / total) * 4007)
    estimated_errors_4007 = int((errors / total) * 4007)
    
    print(f"\n{'='*60}")
    print("REPRESENTATIVE SAMPLE RESULTS")
    print(f"{'='*60}")
    print(f"Sample size: {total} colors (from 4007 total)")
    print(f"Exact matches: {exact_matches}")
    print(f"Close matches: {close_matches}")
    print(f"Errors: {errors}")
    print(f"Complete misses: {total - exact_matches - close_matches - errors}")
    print(f"")
    print(f"SAMPLE ACCURACY METRICS:")
    print(f"  Exact accuracy: {accuracy:.3f}%")
    print(f"  Close match rate: {close_match_rate:.3f}%")
    print(f"  Combined accuracy: {combined_accuracy:.3f}%")
    print(f"  Error rate: {error_rate:.3f}%")
    print(f"  Processing time: {end_time - start_time:.1f} seconds")
    
    print(f"\n{'='*60}")
    print("EXTRAPOLATED FULL DATASET (4007 colors)")
    print(f"{'='*60}")
    print(f"Estimated exact matches: {estimated_exact_4007}")
    print(f"Estimated close matches: {estimated_close_4007}")
    print(f"Estimated errors: {estimated_errors_4007}")
    print(f"Estimated total accurate: {estimated_exact_4007 + estimated_close_4007}")
    
    # Show examples
    print(f"\nEXACT MATCH EXAMPLES:")
    for r, g, b, expected, result in exact_examples[:8]:
        print(f"  RGB({r:3d},{g:3d},{b:3d}) -> {result} ✓")
    
    print(f"\nERROR EXAMPLES:")
    for r, g, b, expected, result in error_examples[:3]:
        print(f"  RGB({r:3d},{g:3d},{b:3d}) -> {result}")
    
    print(f"\nMISS EXAMPLES:")
    for r, g, b, expected, result in miss_examples[:3]:
        print(f"  RGB({r:3d},{g:3d},{b:3d}) -> {result} (expected: {expected})")
    
    # Final assessment
    print(f"\n{'='*60}")
    print("PYTHON COLOUR-SCIENCE ASSESSMENT")
    print(f"{'='*60}")
    
    if accuracy >= 95.0:
        status = "🏆 OUTSTANDING"
        recommendation = "PERFECT reference - implement exact algorithm in Rust"
    elif accuracy >= 85.0:
        status = "🎯 EXCELLENT"
        recommendation = "Excellent reference - extract algorithm for Rust"
    elif accuracy >= 75.0:
        status = "✅ VERY GOOD"
        recommendation = "Strong reference - good foundation for Rust implementation"
    elif accuracy >= 65.0:
        status = "✅ GOOD" 
        recommendation = "Good reference - better than current Rust (0.025%)"
    elif accuracy >= 50.0:
        status = "⚠️  MODERATE"
        recommendation = "Moderate - still much better than current Rust"
    else:
        status = "❌ POOR"
        recommendation = "Poor - investigate issues"
    
    print(f"Status: {status}")
    print(f"Exact Accuracy: {accuracy:.1f}% (vs current Rust: 0.025%)")
    print(f"Combined Accuracy: {combined_accuracy:.1f}%")
    print(f"Recommendation: {recommendation}")
    
    # Compare with current Rust performance
    improvement_factor = accuracy / 0.025
    print(f"\nImprovement over current Rust: {improvement_factor:.0f}x better")
    
    if accuracy > 70:
        print(f"\n✅ CONCLUSION: Python colour-science is SUITABLE as reference")
        print(f"   - Achieves {accuracy:.1f}% exact accuracy on representative sample")
        print(f"   - Estimated {estimated_exact_4007} exact matches out of 4007 total colors")
        print(f"   - {improvement_factor:.0f}x better than current Rust implementation")
        print(f"   - Ready to extract algorithm for Rust implementation")
    else:
        print(f"\n⚠️  CONCLUSION: Python colour-science has limitations")
        print(f"   - Only {accuracy:.1f}% exact accuracy")
        print(f"   - Need to investigate algorithmic differences")
    
    return {
        'sample_size': total,
        'exact_matches': exact_matches,
        'close_matches': close_matches,
        'errors': errors,
        'accuracy': accuracy,
        'combined_accuracy': combined_accuracy,
        'estimated_exact_4007': estimated_exact_4007,
        'improvement_factor': improvement_factor
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
            return abs(result_spec[1] - expected_spec[1]) < 0.5
        elif not (np.isnan(result_spec[0]) or np.isnan(expected_spec[0])):  # Both chromatic
            hue_diff = abs(result_spec[0] - expected_spec[0])
            value_diff = abs(result_spec[1] - expected_spec[1])
            chroma_diff = abs(result_spec[2] - expected_spec[2])
            
            return (hue_diff < 0.5 and value_diff < 0.5 and chroma_diff < 1.0)
        else:
            return False
    except:
        return False

def main():
    """Main test function."""
    print("REPRESENTATIVE SAMPLING OF COMPLETE 4007-COLOR DATASET")
    print("Testing Python colour-science library with statistically valid sample")
    print("")
    
    results = test_representative_sample()
    
    # Save summary
    with open('representative_test_results.txt', 'w') as f:
        f.write(f"Representative Sample Results (from 4007 total colors)\n")
        f.write(f"Sample size: {results['sample_size']}\n")
        f.write(f"Exact accuracy: {results['accuracy']:.3f}%\n")
        f.write(f"Combined accuracy: {results['combined_accuracy']:.3f}%\n")
        f.write(f"Estimated exact matches on full dataset: {results['estimated_exact_4007']}\n")
        f.write(f"Improvement over current Rust: {results['improvement_factor']:.0f}x\n")
    
    print(f"\nResults saved to: representative_test_results.txt")

if __name__ == "__main__":
    main()