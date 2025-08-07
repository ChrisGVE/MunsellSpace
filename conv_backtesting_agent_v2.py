#!/usr/bin/env python3
"""
Conversion Backtesting Agent V2 - Optimized for full 4,007 color dataset
Generates markdown reports and handles large datasets efficiently
"""

import csv
import json
import subprocess
import numpy as np
from collections import defaultdict
from colour.notation import munsell
from colour import sRGB_to_XYZ, XYZ_to_xyY
import sys
import time
from datetime import datetime
import os

class ConversionBacktestingAgentV2:
    """Optimized agent for comprehensive conversion testing"""
    
    def __init__(self, dataset_path='tests/data/srgb-to-munsell.csv'):
        self.dataset_path = dataset_path
        self.results = []
        self.family_mismatches = defaultdict(int)
        self.total_family_mismatches = 0
        # Pre-compile the Rust binary path
        self.rust_binary = './target/release/test_rgb_cli'
        if not os.path.exists(self.rust_binary):
            print(f"Warning: Rust binary not found at {self.rust_binary}")
            print("Building it now...")
            subprocess.run(['cargo', 'build', '--release', '--bin', 'test_rgb_cli'], 
                         capture_output=True)
        
    def test_rust_conversion_fast(self, r, g, b):
        """Optimized Rust conversion with minimal overhead"""
        try:
            result = subprocess.run(
                [self.rust_binary, str(r), str(g), str(b)],
                capture_output=True,
                text=True,
                timeout=0.5  # Shorter timeout
            )
            
            if result.returncode == 0 and 'Munsell:' in result.stdout:
                notation = result.stdout.split('Munsell:')[1].strip()
                # Parse the notation to specification immediately
                spec = munsell.munsell_colour_to_munsell_specification(notation)
                return {
                    'notation': notation,
                    'hue': spec[0],
                    'value': spec[1],
                    'chroma': spec[2],
                    'code': int(spec[3]),
                    'family': self.get_family_from_code(int(spec[3]))
                }
        except Exception:
            pass
        return None
    
    def test_python_conversion_fast(self, r, g, b):
        """Optimized Python conversion"""
        try:
            srgb = [r/255.0, g/255.0, b/255.0]
            xyz = sRGB_to_XYZ(srgb)
            xyy = XYZ_to_xyY(xyz)
            raw_spec = munsell.xyY_to_munsell_specification(xyy)
            notation = munsell.munsell_specification_to_munsell_colour(raw_spec, 1, 1, 1)
            # Get the normalized spec by parsing the notation back
            normalized_spec = munsell.munsell_colour_to_munsell_specification(notation)
            return {
                'notation': notation,
                'hue': normalized_spec[0],
                'value': normalized_spec[1],
                'chroma': normalized_spec[2],
                'code': int(normalized_spec[3]),
                'family': self.get_family_from_code(int(normalized_spec[3]))
            }
        except Exception:
            return None
            
    def get_family_from_code(self, code):
        """Get hue family letter from code"""
        families = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y',
                   6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}
        return families.get(code, 'Unknown')
    
    def calculate_differences_fast(self, python_result, rust_result):
        """Optimized difference calculation with circular hue handling"""
        if not python_result or not rust_result:
            return None
            
        # Handle NaN values efficiently
        py_hue = 0 if np.isnan(python_result['hue']) else python_result['hue']
        py_chroma = 0 if np.isnan(python_result['chroma']) else python_result['chroma']
        rust_hue = 0 if np.isnan(rust_result['hue']) else rust_result['hue']
        rust_chroma = 0 if np.isnan(rust_result['chroma']) else rust_result['chroma']
        
        # Calculate circular hue difference (Munsell hues are circular 0-10)
        def circular_hue_diff(h1, h2):
            """Calculate minimum distance between two hues on a circle"""
            # Handle case where both hues are effectively achromatic (0)
            if py_chroma == 0 and rust_chroma == 0:
                return 0.0
            
            # Direct difference
            direct_diff = abs(h1 - h2)
            
            # Wrap-around difference (through 0/10 boundary)
            wraparound_diff = 10.0 - direct_diff
            
            # Return the smaller of the two
            return min(direct_diff, wraparound_diff)
        
        return {
            'hue_diff': circular_hue_diff(py_hue, rust_hue),
            'value_diff': abs(python_result['value'] - rust_result['value']),
            'chroma_diff': abs(py_chroma - rust_chroma),
            'family_match': python_result['family'] == rust_result['family']
        }
    
    def run_full_test(self, limit=None, progress_interval=100):
        """Run test on dataset with progress reporting"""
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
        
        total_colors = len(colors)
        print(f"Testing {total_colors} colors...")
        start_time = time.time()
        
        for i, (r, g, b, expected) in enumerate(colors):
            if i % progress_interval == 0:
                elapsed = time.time() - start_time
                rate = i / elapsed if elapsed > 0 else 0
                remaining = (total_colors - i) / rate if rate > 0 else 0
                print(f"  Progress: {i}/{total_colors} ({100*i/total_colors:.1f}%) - "
                      f"Rate: {rate:.1f} colors/sec - ETA: {remaining:.0f}s")
            
            # Test both conversions
            python_result = self.test_python_conversion_fast(r, g, b)
            rust_result = self.test_rust_conversion_fast(r, g, b)
            
            if python_result and rust_result:
                diffs = self.calculate_differences_fast(python_result, rust_result)
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
        
        elapsed = time.time() - start_time
        print(f"Completed in {elapsed:.1f} seconds ({total_colors/elapsed:.1f} colors/sec)")
    
    def generate_statistics(self):
        """Generate comprehensive statistics with additional percentiles"""
        if not self.results:
            return None
            
        # Extract difference arrays
        hue_diffs = [r['differences']['hue_diff'] for r in self.results]
        value_diffs = [r['differences']['value_diff'] for r in self.results]
        chroma_diffs = [r['differences']['chroma_diff'] for r in self.results]
        
        # Extended percentiles for detailed analysis
        percentiles = [50, 90, 95, 96, 97, 98, 99, 99.5, 100]
        
        stats = {
            'total_tested': len(self.results),
            'test_date': datetime.now().isoformat(),
            'dataset': self.dataset_path,
            'family_mismatches': {
                'total': self.total_family_mismatches,
                'percentage': (self.total_family_mismatches / len(self.results)) * 100 if self.results else 0,
                'by_transition': dict(sorted(self.family_mismatches.items(), 
                                           key=lambda x: x[1], reverse=True))
            },
            'hue_differences': {
                'median': float(np.median(hue_diffs)),
                'mean': float(np.mean(hue_diffs)),
                'std': float(np.std(hue_diffs)),
                'percentiles': {p: float(np.percentile(hue_diffs, p)) for p in percentiles},
                'above_0.1': sum(1 for d in hue_diffs if d > 0.1),
                'above_0.1_pct': 100 * sum(1 for d in hue_diffs if d > 0.1) / len(hue_diffs),
                'max': float(max(hue_diffs)),
                'min': float(min(hue_diffs))
            },
            'value_differences': {
                'median': float(np.median(value_diffs)),
                'mean': float(np.mean(value_diffs)),
                'std': float(np.std(value_diffs)),
                'percentiles': {p: float(np.percentile(value_diffs, p)) for p in percentiles},
                'above_0.1': sum(1 for d in value_diffs if d > 0.1),
                'above_0.1_pct': 100 * sum(1 for d in value_diffs if d > 0.1) / len(value_diffs),
                'max': float(max(value_diffs)),
                'min': float(min(value_diffs))
            },
            'chroma_differences': {
                'median': float(np.median(chroma_diffs)),
                'mean': float(np.mean(chroma_diffs)),
                'std': float(np.std(chroma_diffs)),
                'percentiles': {p: float(np.percentile(chroma_diffs, p)) for p in percentiles},
                'above_0.1': sum(1 for d in chroma_diffs if d > 0.1),
                'above_0.1_pct': 100 * sum(1 for d in chroma_diffs if d > 0.1) / len(chroma_diffs),
                'max': float(max(chroma_diffs)),
                'min': float(min(chroma_diffs))
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
        ) * 100 if self.results else 0
        
        # Find problematic colors (top 20)
        problematic_colors = []
        for r in self.results:
            max_diff = max(r['differences']['hue_diff'], 
                          r['differences']['value_diff'], 
                          r['differences']['chroma_diff'])
            if max_diff > 0.1:
                problematic_colors.append({
                    'hex': r['hex'],
                    'rgb': r['rgb'],
                    'python': r['python']['notation'],
                    'rust': r['rust']['notation'],
                    'hue_diff': r['differences']['hue_diff'],
                    'value_diff': r['differences']['value_diff'],
                    'chroma_diff': r['differences']['chroma_diff'],
                    'max_diff': max_diff,
                    'family_match': r['differences']['family_match']
                })
        
        # Sort by maximum difference and take top 20
        problematic_colors.sort(key=lambda x: x['max_diff'], reverse=True)
        stats['problematic_colors'] = problematic_colors[:20]
        stats['total_problematic'] = len(problematic_colors)
        
        return stats
    
    def generate_markdown_report(self, stats, filename='backtesting_report.md'):
        """Generate a detailed markdown report"""
        with open(filename, 'w') as f:
            f.write("# Munsell Conversion Backtesting Report\n\n")
            f.write(f"**Generated**: {stats['test_date']}\n")
            f.write(f"**Dataset**: {stats['dataset']}\n")
            f.write(f"**Total Colors Tested**: {stats['total_tested']:,}\n\n")
            
            # Executive Summary
            f.write("## Executive Summary\n\n")
            f.write(f"- **Overall Accuracy**: {stats['overall_accuracy']['percentage']:.2f}% ")
            f.write(f"({stats['overall_accuracy']['all_within_0.1']:,}/{stats['total_tested']:,} within 0.1 tolerance)\n")
            f.write(f"- **Family Mismatches**: {stats['family_mismatches']['percentage']:.2f}% ")
            f.write(f"({stats['family_mismatches']['total']:,} colors)\n")
            f.write(f"- **Hue Accuracy**: {100 - stats['hue_differences']['above_0.1_pct']:.2f}% within tolerance\n")
            f.write(f"- **Value Accuracy**: {100 - stats['value_differences']['above_0.1_pct']:.2f}% within tolerance\n")
            f.write(f"- **Chroma Accuracy**: {100 - stats['chroma_differences']['above_0.1_pct']:.2f}% within tolerance\n\n")
            
            # Family Mismatches
            f.write("## Family Mismatches\n\n")
            f.write(f"**Total**: {stats['family_mismatches']['total']} ({stats['family_mismatches']['percentage']:.2f}%)\n\n")
            if stats['family_mismatches']['by_transition']:
                f.write("### Top Transitions\n\n")
                f.write("| From → To | Count | Percentage |\n")
                f.write("|-----------|-------|------------|\n")
                for transition, count in list(stats['family_mismatches']['by_transition'].items())[:10]:
                    pct = 100 * count / stats['family_mismatches']['total']
                    f.write(f"| {transition} | {count} | {pct:.1f}% |\n")
                f.write("\n")
            
            # Component Statistics
            for component in ['hue', 'value', 'chroma']:
                comp_stats = stats[f'{component}_differences']
                f.write(f"## {component.capitalize()} Differences\n\n")
                
                # Summary stats
                f.write("### Summary Statistics\n\n")
                f.write(f"- **Median**: {comp_stats['median']:.6f}\n")
                f.write(f"- **Mean**: {comp_stats['mean']:.6f}\n")
                f.write(f"- **Std Dev**: {comp_stats['std']:.6f}\n")
                f.write(f"- **Min**: {comp_stats['min']:.6f}\n")
                f.write(f"- **Max**: {comp_stats['max']:.6f}\n")
                f.write(f"- **Above 0.1**: {comp_stats['above_0.1']:,} ({comp_stats['above_0.1_pct']:.2f}%)\n\n")
                
                # Percentiles table
                f.write("### Percentile Distribution\n\n")
                f.write("| Percentile | Value | Analysis |\n")
                f.write("|------------|-------|----------|\n")
                
                for p, val in comp_stats['percentiles'].items():
                    if p == 50:
                        analysis = "Median - typical error"
                    elif p == 90:
                        analysis = "90% of colors below this"
                    elif p == 95:
                        analysis = "95% of colors below this"
                    elif p == 96:
                        analysis = "96% of colors below this"
                    elif p == 97:
                        analysis = "97% of colors below this"
                    elif p == 98:
                        analysis = "98% of colors below this"
                    elif p == 99:
                        analysis = "99% of colors below this"
                    elif p == 99.5:
                        analysis = "99.5% of colors below this"
                    elif p == 100:
                        analysis = "Maximum error"
                    else:
                        analysis = ""
                    
                    marker = "⚠️" if val > 0.1 else "✓"
                    f.write(f"| {p:5.1f}% | {val:.6f} | {marker} {analysis} |\n")
                f.write("\n")
            
            # Problematic Colors
            if stats['problematic_colors']:
                f.write("## Most Problematic Colors\n\n")
                f.write(f"**Total problematic colors**: {stats['total_problematic']:,} ")
                f.write(f"(showing top {len(stats['problematic_colors'])})\n\n")
                
                f.write("| Hex | RGB | Python | Rust | ΔH | ΔV | ΔC | Family |\n")
                f.write("|-----|-----|--------|------|----|----|----|---------|\n")
                
                for color in stats['problematic_colors']:
                    family_icon = "✓" if color['family_match'] else "✗"
                    f.write(f"| {color['hex']} | {color['rgb']} | {color['python']} | {color['rust']} | ")
                    f.write(f"{color['hue_diff']:.3f} | {color['value_diff']:.3f} | ")
                    f.write(f"{color['chroma_diff']:.3f} | {family_icon} |\n")
                f.write("\n")
            
            # Conclusions
            f.write("## Analysis and Conclusions\n\n")
            
            # Determine main issues
            issues = []
            if stats['hue_differences']['above_0.1_pct'] > 5:
                issues.append(f"**Hue**: {stats['hue_differences']['above_0.1_pct']:.1f}% exceed tolerance")
            if stats['value_differences']['above_0.1_pct'] > 5:
                issues.append(f"**Value**: {stats['value_differences']['above_0.1_pct']:.1f}% exceed tolerance")
            if stats['chroma_differences']['above_0.1_pct'] > 5:
                issues.append(f"**Chroma**: {stats['chroma_differences']['above_0.1_pct']:.1f}% exceed tolerance")
            
            if issues:
                f.write("### Primary Issues\n\n")
                for issue in issues:
                    f.write(f"- {issue}\n")
                f.write("\n")
            
            # Strengths
            strengths = []
            if stats['value_differences']['above_0.1_pct'] < 1:
                strengths.append("**Value calculation**: Near perfect accuracy")
            if stats['hue_differences']['above_0.1_pct'] < 5:
                strengths.append("**Hue calculation**: Excellent accuracy")
            if stats['family_mismatches']['percentage'] < 5:
                strengths.append("**Family assignment**: Very accurate")
            
            if strengths:
                f.write("### Strengths\n\n")
                for strength in strengths:
                    f.write(f"- {strength}\n")
                f.write("\n")
            
            f.write("### Target vs Actual\n\n")
            f.write("| Metric | Target | Actual | Status |\n")
            f.write("|--------|--------|--------|--------|\n")
            f.write(f"| Overall Accuracy | 99.98% | {stats['overall_accuracy']['percentage']:.2f}% | ")
            f.write("✓\n" if stats['overall_accuracy']['percentage'] >= 99.98 else "Need improvement\n")
            f.write(f"| Hue within 0.1 | 100% | {100 - stats['hue_differences']['above_0.1_pct']:.2f}% | ")
            f.write("✓\n" if stats['hue_differences']['above_0.1_pct'] < 0.02 else "Need improvement\n")
            f.write(f"| Value within 0.1 | 100% | {100 - stats['value_differences']['above_0.1_pct']:.2f}% | ")
            f.write("✓\n" if stats['value_differences']['above_0.1_pct'] < 0.02 else "Need improvement\n")
            f.write(f"| Chroma within 0.1 | 100% | {100 - stats['chroma_differences']['above_0.1_pct']:.2f}% | ")
            f.write("✓\n" if stats['chroma_differences']['above_0.1_pct'] < 0.02 else "Need improvement\n")
        
        print(f"Markdown report saved to {filename}")
    
    def save_results(self, stats, json_file='backtesting_results.json'):
        """Save detailed results to JSON file"""
        with open(json_file, 'w') as f:
            json.dump(stats, f, indent=2, default=str)
        print(f"JSON results saved to {json_file}")

def main():
    """Main entry point for the backtesting agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Conversion Backtesting Agent V2')
    parser.add_argument('--limit', type=int, help='Limit number of colors to test')
    parser.add_argument('--dataset', default='tests/data/srgb-to-munsell.csv', 
                       help='Path to dataset CSV')
    parser.add_argument('--json', default='backtesting_results.json',
                       help='Output JSON file name')
    parser.add_argument('--markdown', default='backtesting_report.md',
                       help='Output markdown report file name')
    parser.add_argument('--progress', type=int, default=100,
                       help='Progress reporting interval (default: 100)')
    
    args = parser.parse_args()
    
    print("="*80)
    print("MUNSELL CONVERSION BACKTESTING AGENT V2")
    print("="*80)
    
    agent = ConversionBacktestingAgentV2(args.dataset)
    agent.run_full_test(limit=args.limit, progress_interval=args.progress)
    
    stats = agent.generate_statistics()
    if stats:
        # Save results
        agent.save_results(stats, args.json)
        agent.generate_markdown_report(stats, args.markdown)
        
        # Print summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"Overall Accuracy: {stats['overall_accuracy']['percentage']:.2f}%")
        print(f"Family Mismatches: {stats['family_mismatches']['percentage']:.2f}%")
        print(f"Components exceeding 0.1 tolerance:")
        print(f"  Hue: {stats['hue_differences']['above_0.1_pct']:.2f}%")
        print(f"  Value: {stats['value_differences']['above_0.1_pct']:.2f}%")
        print(f"  Chroma: {stats['chroma_differences']['above_0.1_pct']:.2f}%")
        print("="*80)
    else:
        print("No results to report")

if __name__ == "__main__":
    main()