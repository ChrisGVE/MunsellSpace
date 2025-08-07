#!/usr/bin/env python3
"""
Conversion Backtesting Agent - Comprehensive comparison of Python vs Rust Munsell conversion
Reusable agent for testing conversion accuracy across the full 4,007 color dataset
"""

import csv
import json
import subprocess
import numpy as np
from collections import defaultdict
from colour.notation import munsell
from colour import sRGB_to_XYZ, XYZ_to_xyY
import sys

class ConversionBacktestingAgent:
    """Agent for comprehensive conversion testing and analysis"""
    
    def __init__(self, dataset_path='tests/data/srgb-to-munsell.csv'):
        self.dataset_path = dataset_path
        self.results = []
        self.family_mismatches = defaultdict(int)
        self.total_family_mismatches = 0
        
    def test_python_conversion(self, r, g, b):
        """Test Python conversion"""
        try:
            srgb = [r/255.0, g/255.0, b/255.0]
            xyz = sRGB_to_XYZ(srgb)
            xyy = XYZ_to_xyY(xyz)
            spec = munsell.xyY_to_munsell_specification(xyy)
            notation = munsell.munsell_specification_to_munsell_colour(spec)
            return {
                'spec': spec,
                'notation': notation,
                'hue': spec[0],
                'value': spec[1],
                'chroma': spec[2],
                'code': int(spec[3]),
                'family': self.get_family_from_code(int(spec[3]))
            }
        except Exception as e:
            return None
            
    def test_rust_conversion(self, r, g, b):
        """Test Rust conversion via binary"""
        try:
            # Call Rust binary - we'll use a simple test binary
            result = subprocess.run(
                ['cargo', 'run', '--release', '--bin', 'test_rgb_cli', '--', 
                 str(r), str(g), str(b)],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0 and 'Munsell:' in result.stdout:
                # Parse output
                notation = result.stdout.split('Munsell:')[1].strip()
                
                # Convert notation back to specification for comparison
                spec = munsell.munsell_colour_to_munsell_specification(notation)
                
                return {
                    'spec': spec,
                    'notation': notation,
                    'hue': spec[0],
                    'value': spec[1],
                    'chroma': spec[2],
                    'code': int(spec[3]),
                    'family': self.get_family_from_code(int(spec[3]))
                }
        except:
            pass
        return None
    
    def get_family_from_code(self, code):
        """Get hue family letter from code"""
        families = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y',
                   6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}
        return families.get(code, 'Unknown')
    
    def calculate_differences(self, python_result, rust_result):
        """Calculate differences between Python and Rust results"""
        if not python_result or not rust_result:
            return None
            
        # Handle NaN values for grey colors
        py_hue = python_result['hue'] if not np.isnan(python_result['hue']) else 0
        py_chroma = python_result['chroma'] if not np.isnan(python_result['chroma']) else 0
        rust_hue = rust_result['hue'] if not np.isnan(rust_result['hue']) else 0
        rust_chroma = rust_result['chroma'] if not np.isnan(rust_result['chroma']) else 0
        
        return {
            'hue_diff': abs(py_hue - rust_hue),
            'value_diff': abs(python_result['value'] - rust_result['value']),
            'chroma_diff': abs(py_chroma - rust_chroma),
            'family_match': python_result['family'] == rust_result['family']
        }
    
    def run_full_test(self, limit=None):
        """Run test on full dataset or limited number of colors"""
        print(f"Loading dataset from {self.dataset_path}...")
        
        with open(self.dataset_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            
            colors = []
            for row in reader:
                r, g, b = int(row[0]), int(row[1]), int(row[2])
                expected = row[3]
                colors.append((r, g, b, expected))
                if limit and len(colors) >= limit:
                    break
        
        print(f"Testing {len(colors)} colors...")
        
        for i, (r, g, b, expected) in enumerate(colors):
            if i % 100 == 0:
                print(f"  Progress: {i}/{len(colors)}")
            
            python_result = self.test_python_conversion(r, g, b)
            rust_result = self.test_rust_conversion(r, g, b)
            
            if python_result and rust_result:
                diffs = self.calculate_differences(python_result, rust_result)
                if diffs:
                    self.results.append({
                        'rgb': (r, g, b),
                        'hex': f"#{r:02x}{g:02x}{b:02x}",
                        'expected': expected,
                        'python': python_result,
                        'rust': rust_result,
                        'differences': diffs
                    })
                    
                    # Track family mismatches
                    if not diffs['family_match']:
                        self.total_family_mismatches += 1
                        py_family = python_result['family']
                        rust_family = rust_result['family']
                        self.family_mismatches[f"{py_family}→{rust_family}"] += 1
    
    def generate_statistics(self):
        """Generate comprehensive statistics from test results"""
        if not self.results:
            return None
            
        # Extract difference arrays
        hue_diffs = [r['differences']['hue_diff'] for r in self.results]
        value_diffs = [r['differences']['value_diff'] for r in self.results]
        chroma_diffs = [r['differences']['chroma_diff'] for r in self.results]
        
        # Calculate percentiles
        percentiles = [50, 90, 95, 99, 100]
        
        stats = {
            'total_tested': len(self.results),
            'family_mismatches': {
                'total': self.total_family_mismatches,
                'percentage': (self.total_family_mismatches / len(self.results)) * 100,
                'by_transition': dict(self.family_mismatches)
            },
            'hue_differences': {
                'median': np.median(hue_diffs),
                'percentiles': {p: np.percentile(hue_diffs, p) for p in percentiles},
                'above_0.1': sum(1 for d in hue_diffs if d > 0.1),
                'max': max(hue_diffs)
            },
            'value_differences': {
                'median': np.median(value_diffs),
                'percentiles': {p: np.percentile(value_diffs, p) for p in percentiles},
                'above_0.1': sum(1 for d in value_diffs if d > 0.1),
                'max': max(value_diffs)
            },
            'chroma_differences': {
                'median': np.median(chroma_diffs),
                'percentiles': {p: np.percentile(chroma_diffs, p) for p in percentiles},
                'above_0.1': sum(1 for d in chroma_diffs if d > 0.1),
                'max': max(chroma_diffs)
            },
            'overall_accuracy': {
                'all_within_0.1': sum(1 for r in self.results 
                                     if r['differences']['hue_diff'] <= 0.1 
                                     and r['differences']['value_diff'] <= 0.1 
                                     and r['differences']['chroma_diff'] <= 0.1),
                'percentage': 0  # Will calculate below
            }
        }
        
        stats['overall_accuracy']['percentage'] = (
            stats['overall_accuracy']['all_within_0.1'] / len(self.results)
        ) * 100
        
        # Find colors with differences > 0.1
        problematic_colors = []
        for r in self.results:
            if (r['differences']['hue_diff'] > 0.1 or 
                r['differences']['value_diff'] > 0.1 or 
                r['differences']['chroma_diff'] > 0.1):
                problematic_colors.append({
                    'hex': r['hex'],
                    'rgb': r['rgb'],
                    'python': r['python']['notation'],
                    'rust': r['rust']['notation'],
                    'hue_diff': r['differences']['hue_diff'],
                    'value_diff': r['differences']['value_diff'],
                    'chroma_diff': r['differences']['chroma_diff'],
                    'family_match': r['differences']['family_match']
                })
        
        stats['problematic_colors'] = problematic_colors
        
        return stats
    
    def print_report(self, stats):
        """Print formatted report"""
        print("\n" + "="*80)
        print("CONVERSION BACKTESTING REPORT")
        print("="*80)
        
        print(f"\nTotal colors tested: {stats['total_tested']}")
        
        print(f"\n1. FAMILY MISMATCHES:")
        print(f"   Total: {stats['family_mismatches']['total']} ({stats['family_mismatches']['percentage']:.2f}%)")
        if stats['family_mismatches']['by_transition']:
            print("   By transition:")
            for transition, count in sorted(stats['family_mismatches']['by_transition'].items(), 
                                          key=lambda x: x[1], reverse=True)[:10]:
                print(f"      {transition}: {count}")
        
        print(f"\n2. HUE DIFFERENCES:")
        print(f"   Median: {stats['hue_differences']['median']:.6f}")
        print("   Percentiles:")
        for p, val in stats['hue_differences']['percentiles'].items():
            print(f"      {p}th: {val:.6f}")
        print(f"   Above 0.1: {stats['hue_differences']['above_0.1']}")
        
        print(f"\n3. VALUE DIFFERENCES:")
        print(f"   Median: {stats['value_differences']['median']:.6f}")
        print("   Percentiles:")
        for p, val in stats['value_differences']['percentiles'].items():
            print(f"      {p}th: {val:.6f}")
        print(f"   Above 0.1: {stats['value_differences']['above_0.1']}")
        
        print(f"\n4. CHROMA DIFFERENCES:")
        print(f"   Median: {stats['chroma_differences']['median']:.6f}")
        print("   Percentiles:")
        for p, val in stats['chroma_differences']['percentiles'].items():
            print(f"      {p}th: {val:.6f}")
        print(f"   Above 0.1: {stats['chroma_differences']['above_0.1']}")
        
        print(f"\n5. OVERALL ACCURACY:")
        print(f"   Colors within 0.1 tolerance: {stats['overall_accuracy']['all_within_0.1']}/{stats['total_tested']}")
        print(f"   Accuracy: {stats['overall_accuracy']['percentage']:.2f}%")
        
        if stats['problematic_colors']:
            print(f"\n6. PROBLEMATIC COLORS (differences > 0.1):")
            print(f"   Total: {len(stats['problematic_colors'])}")
            print("\n   First 10 problematic colors:")
            for i, color in enumerate(stats['problematic_colors'][:10]):
                print(f"\n   {i+1}. {color['hex']} RGB{color['rgb']}")
                print(f"      Python: {color['python']}")
                print(f"      Rust:   {color['rust']}")
                print(f"      Diffs:  H={color['hue_diff']:.3f}, V={color['value_diff']:.3f}, C={color['chroma_diff']:.3f}")
                print(f"      Family: {'✓' if color['family_match'] else '✗'}")
        
        print("\n" + "="*80)
        
    def save_results(self, filename='backtesting_results.json'):
        """Save detailed results to JSON file"""
        stats = self.generate_statistics()
        with open(filename, 'w') as f:
            json.dump(stats, f, indent=2)
        print(f"Results saved to {filename}")

def main():
    """Main entry point for the backtesting agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Conversion Backtesting Agent')
    parser.add_argument('--limit', type=int, help='Limit number of colors to test')
    parser.add_argument('--dataset', default='tests/data/srgb-to-munsell.csv', 
                       help='Path to dataset CSV')
    parser.add_argument('--save', help='Save results to JSON file')
    
    args = parser.parse_args()
    
    agent = ConversionBacktestingAgent(args.dataset)
    agent.run_full_test(limit=args.limit)
    
    stats = agent.generate_statistics()
    if stats:
        agent.print_report(stats)
        
        if args.save:
            agent.save_results(args.save)
    else:
        print("No results to report")

if __name__ == "__main__":
    main()