#!/usr/bin/env python3
"""
Trace Analysis Script for MunsellSpace

Compares trace logs from Python and Rust implementations to identify divergence points.
Focuses on mathematical conversion accuracy debugging.

Usage:
    python analyze_traces.py [python_trace] [rust_trace]
    
Default files:
    - munsell_conversion_trace.txt (Python trace)
    - rust_trace_ddeeee.txt (Rust trace)
"""

import re
import csv
import sys
import os
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TraceLine:
    """Represents a parsed trace line."""
    line_number: int
    function_name: str
    internal_line: int
    variables: Dict[str, Any]
    action: str
    raw_line: str
    
    def __str__(self):
        return f"{self.line_number}→{self.function_name}:{self.internal_line} | {self.action}"


class TraceParser:
    """Parses trace files and extracts structured data."""
    
    def __init__(self):
        # Regex patterns for parsing trace lines
        # Both trace formats use: "function:line | vars: ... | action: ..."
        self.trace_pattern = re.compile(
            r'\s*([^:]+):(\d+)\s*\|\s*vars:\s*(.*?)\s*\|\s*action:\s*(.+)'
        )
        self.float_tolerance = 1e-10
        
        # Function name mapping between Python and Rust
        self.function_mapping = {
            '_xyY_to_munsell_specification': 'xyy_to_munsell_specification',
            '_xy_from_renotation_ovoid': 'xy_from_renotation_ovoid_interpolated',
            'sRGB_to_xyY': 'srgb_to_xyy',
            'XYZ_to_xyY': 'xyz_to_xyy',
            'xyY_to_xyz': 'xyy_to_xyz',
        }
    
    def parse_variables(self, var_string: str) -> Dict[str, Any]:
        """Parse variable string into dictionary."""
        variables = {}
        if not var_string.strip():
            return variables
            
        # Handle single variable case like "rgb_normalized=[0.86, 0.93, 0.93]"
        if '=' in var_string and var_string.count('=') == 1:
            parts = var_string.split('=', 1)
            var_name = parts[0].strip()
            var_value = parts[1].strip()
            variables[var_name] = self.parse_value(var_value)
            return variables
        
        # Handle multiple variables separated by commas
        # More complex regex to handle arrays and nested structures
        current_pos = 0
        while current_pos < len(var_string):
            # Find variable name
            match = re.match(r'\s*(\w+)=', var_string[current_pos:])
            if not match:
                break
                
            var_name = match.group(1)
            value_start = current_pos + match.end()
            
            # Find the end of this variable's value
            if value_start < len(var_string):
                if var_string[value_start] == '[':
                    # Find matching closing bracket
                    bracket_count = 1
                    value_end = value_start + 1
                    while value_end < len(var_string) and bracket_count > 0:
                        if var_string[value_end] == '[':
                            bracket_count += 1
                        elif var_string[value_end] == ']':
                            bracket_count -= 1
                        value_end += 1
                else:
                    # Find next comma or end of string
                    value_end = var_string.find(',', value_start)
                    if value_end == -1:
                        value_end = len(var_string)
                
                var_value = var_string[value_start:value_end].strip()
                variables[var_name] = self.parse_value(var_value)
                
                # Move to next variable (skip comma if present)
                current_pos = value_end
                if current_pos < len(var_string) and var_string[current_pos] == ',':
                    current_pos += 1
            else:
                break
        
        return variables
    
    def parse_value(self, value_str: str) -> Any:
        """Parse a value string into appropriate Python type."""
        value_str = value_str.strip()
        
        # Handle arrays/lists
        if value_str.startswith('[') and value_str.endswith(']'):
            # Parse array content
            content = value_str[1:-1].strip()
            if not content:
                return []
            
            # Split by comma and parse each element
            elements = []
            for item in content.split(','):
                item = item.strip()
                elements.append(self.parse_single_value(item))
            return elements
        
        return self.parse_single_value(value_str)
    
    def parse_single_value(self, value_str: str) -> Any:
        """Parse a single value (not an array)."""
        value_str = value_str.strip()
        
        # Handle boolean values
        if value_str.lower() in ('true', 'false'):
            return value_str.lower() == 'true'
        
        # Handle None/null
        if value_str.lower() in ('none', 'null'):
            return None
        
        # Handle strings
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]
        
        # Try to parse as number
        try:
            if '.' in value_str or 'e' in value_str.lower():
                return float(value_str)
            else:
                return int(value_str)
        except ValueError:
            # Return as string if parsing fails
            return value_str
    
    def parse_file(self, filepath: str, is_rust: bool = None) -> List[TraceLine]:
        """Parse a trace file and return list of TraceLine objects."""
        trace_lines = []
        
        if not os.path.exists(filepath):
            print(f"Warning: File {filepath} not found")
            return trace_lines
        
        # Auto-detect format if not specified
        if is_rust is None:
            is_rust = 'rust' in filepath.lower()
        
        with open(filepath, 'r') as f:
            line_counter = 0
            for raw_line in f:
                raw_line = raw_line.rstrip('\n\r')
                if not raw_line.strip():
                    continue
                
                line_counter += 1
                
                match = self.trace_pattern.match(raw_line)
                if match:
                    func_name, internal_line, vars_str, action = match.groups()
                    line_num = line_counter  # Use sequential line numbers
                else:
                    print(f"Warning: Could not parse line: {raw_line}")
                    continue
                
                variables = self.parse_variables(vars_str)
                
                trace_line = TraceLine(
                    line_number=line_num,
                    function_name=func_name,
                    internal_line=int(internal_line),
                    variables=variables,
                    action=action,
                    raw_line=raw_line
                )
                
                trace_lines.append(trace_line)
        
        return trace_lines
    
    def normalize_function_name(self, func_name: str, is_rust: bool = False) -> str:
        """Normalize function names for comparison."""
        if is_rust:
            # Rust function names are already in the target format
            return func_name
        else:
            # Convert Python function names
            return self.function_mapping.get(func_name, func_name)


class TraceComparator:
    """Compares two trace sequences and identifies divergences."""
    
    def __init__(self, float_tolerance: float = 1e-10):
        self.float_tolerance = float_tolerance
        self.parser = TraceParser()
    
    def compare_values(self, val1: Any, val2: Any) -> Tuple[bool, str]:
        """Compare two values with appropriate tolerance."""
        if type(val1) != type(val2):
            return False, f"Type mismatch: {type(val1).__name__} vs {type(val2).__name__}"
        
        if isinstance(val1, float) and isinstance(val2, float):
            diff = abs(val1 - val2)
            if diff <= self.float_tolerance:
                return True, "Match"
            else:
                return False, f"Float diff: {diff:.2e}"
        
        elif isinstance(val1, list) and isinstance(val2, list):
            if len(val1) != len(val2):
                return False, f"Array length mismatch: {len(val1)} vs {len(val2)}"
            
            for i, (item1, item2) in enumerate(zip(val1, val2)):
                match, reason = self.compare_values(item1, item2)
                if not match:
                    return False, f"Array element {i}: {reason}"
            
            return True, "Match"
        
        else:
            if val1 == val2:
                return True, "Match"
            else:
                return False, f"Value mismatch: {val1} vs {val2}"
    
    def find_corresponding_line(self, target_line: TraceLine, candidate_lines: List[TraceLine], 
                              start_idx: int = 0) -> Optional[Tuple[int, TraceLine]]:
        """Find the corresponding line in the other trace."""
        target_func = self.parser.normalize_function_name(target_line.function_name)
        
        for i, candidate in enumerate(candidate_lines[start_idx:], start_idx):
            candidate_func = self.parser.normalize_function_name(candidate.function_name, is_rust=True)
            
            # Match by function name and action type
            if (target_func == candidate_func and 
                self.action_type_match(target_line.action, candidate.action)):
                return i, candidate
        
        return None
    
    def action_type_match(self, action1: str, action2: str) -> bool:
        """Check if two actions are of the same type."""
        # Define action type keywords
        action_types = {
            'enter': ['ENTER', 'enter'],
            'return': ['RETURN', 'return'],
            'call': ['CALL', 'call'],
            'calc': ['CALC', 'calc'],
            'branch': ['BRANCH', 'branch'],
            'loop': ['LOOP', 'loop']
        }
        
        def get_action_type(action: str) -> str:
            action_upper = action.upper()
            for action_type, keywords in action_types.items():
                if any(keyword.upper() in action_upper for keyword in keywords):
                    return action_type
            return 'unknown'
        
        return get_action_type(action1) == get_action_type(action2)
    
    def compare_traces(self, python_lines: List[TraceLine], rust_lines: List[TraceLine]) -> Dict:
        """Compare two trace sequences and return analysis."""
        comparison_result = {
            'total_python_lines': len(python_lines),
            'total_rust_lines': len(rust_lines),
            'matched_lines': 0,
            'divergent_lines': 0,
            'first_divergence': None,
            'line_comparisons': [],
            'function_call_stats': {},
            'variable_differences': []
        }
        
        rust_idx = 0
        
        for py_idx, py_line in enumerate(python_lines):
            comparison = {
                'python_line': py_line.line_number,
                'python_function': py_line.function_name,
                'python_action': py_line.action,
                'rust_line': None,
                'rust_function': None,
                'rust_action': None,
                'match_status': 'no_corresponding_rust_line',
                'variable_matches': {},
                'notes': []
            }
            
            # Find corresponding Rust line
            corresponding = self.find_corresponding_line(py_line, rust_lines, rust_idx)
            
            if corresponding:
                rust_idx, rust_line = corresponding
                comparison.update({
                    'rust_line': rust_line.line_number,
                    'rust_function': rust_line.function_name,
                    'rust_action': rust_line.action,
                    'match_status': 'found_corresponding'
                })
                
                # Compare variables
                all_vars_match = True
                for var_name, py_value in py_line.variables.items():
                    if var_name in rust_line.variables:
                        rust_value = rust_line.variables[var_name]
                        match, reason = self.compare_values(py_value, rust_value)
                        comparison['variable_matches'][var_name] = {
                            'python_value': py_value,
                            'rust_value': rust_value,
                            'match': match,
                            'reason': reason
                        }
                        
                        if not match:
                            all_vars_match = False
                            if comparison_result['first_divergence'] is None:
                                comparison_result['first_divergence'] = {
                                    'python_line': py_line,
                                    'rust_line': rust_line,
                                    'variable': var_name,
                                    'python_value': py_value,
                                    'rust_value': rust_value,
                                    'reason': reason
                                }
                    else:
                        comparison['variable_matches'][var_name] = {
                            'python_value': py_value,
                            'rust_value': 'MISSING',
                            'match': False,
                            'reason': 'Variable not found in Rust trace'
                        }
                        all_vars_match = False
                
                if all_vars_match:
                    comparison['match_status'] = 'complete_match'
                    comparison_result['matched_lines'] += 1
                else:
                    comparison['match_status'] = 'variable_mismatch'
                    comparison_result['divergent_lines'] += 1
            else:
                comparison_result['divergent_lines'] += 1
            
            comparison_result['line_comparisons'].append(comparison)
        
        return comparison_result


class ReportGenerator:
    """Generates various report formats from comparison results."""
    
    def __init__(self):
        self.float_precision = 10
    
    def generate_console_summary(self, analysis: Dict) -> str:
        """Generate a console-friendly summary."""
        summary = []
        summary.append("=== TRACE COMPARISON SUMMARY ===")
        summary.append(f"Python lines: {analysis['total_python_lines']}")
        summary.append(f"Rust lines: {analysis['total_rust_lines']}")
        summary.append(f"Matched lines: {analysis['matched_lines']}")
        summary.append(f"Divergent lines: {analysis['divergent_lines']}")
        
        if analysis['first_divergence']:
            div = analysis['first_divergence']
            summary.append(f"\n=== FIRST DIVERGENCE ===")
            summary.append(f"Python line {div['python_line'].line_number}: {div['python_line'].function_name}")
            summary.append(f"Rust line {div['rust_line'].line_number}: {div['rust_line'].function_name}")
            summary.append(f"Variable: {div['variable']}")
            summary.append(f"Python value: {div['python_value']}")
            summary.append(f"Rust value: {div['rust_value']}")
            summary.append(f"Reason: {div['reason']}")
        else:
            summary.append(f"\n=== NO DIVERGENCE FOUND ===")
        
        match_rate = (analysis['matched_lines'] / analysis['total_python_lines']) * 100 if analysis['total_python_lines'] > 0 else 0
        summary.append(f"\nMatch Rate: {match_rate:.2f}%")
        
        return "\n".join(summary)
    
    def generate_markdown_report(self, analysis: Dict, output_path: str = "TRACE_DIVERGENCE_REPORT.md"):
        """Generate detailed markdown report."""
        with open(output_path, 'w') as f:
            f.write("# Trace Divergence Analysis Report\n\n")
            
            # Summary statistics
            f.write("## Summary Statistics\n\n")
            f.write(f"- **Python trace lines**: {analysis['total_python_lines']}\n")
            f.write(f"- **Rust trace lines**: {analysis['total_rust_lines']}\n")
            f.write(f"- **Matched lines**: {analysis['matched_lines']}\n")
            f.write(f"- **Divergent lines**: {analysis['divergent_lines']}\n")
            
            match_rate = (analysis['matched_lines'] / analysis['total_python_lines']) * 100 if analysis['total_python_lines'] > 0 else 0
            f.write(f"- **Match rate**: {match_rate:.2f}%\n\n")
            
            # First divergence details
            if analysis['first_divergence']:
                div = analysis['first_divergence']
                f.write("## First Divergence Point\n\n")
                f.write(f"**Python Line {div['python_line'].line_number}**: `{div['python_line'].function_name}:{div['python_line'].internal_line}`\n")
                f.write(f"```\n{div['python_line'].raw_line}\n```\n\n")
                
                f.write(f"**Rust Line {div['rust_line'].line_number}**: `{div['rust_line'].function_name}:{div['rust_line'].internal_line}`\n")
                f.write(f"```\n{div['rust_line'].raw_line}\n```\n\n")
                
                f.write(f"**Divergent Variable**: `{div['variable']}`\n")
                f.write(f"- Python value: `{div['python_value']}`\n")
                f.write(f"- Rust value: `{div['rust_value']}`\n")
                f.write(f"- Reason: {div['reason']}\n\n")
                
                # Context around divergence
                f.write("### Context (5 lines before and after)\n\n")
                # This would require access to the original comparison data
                # For now, just note where to find it
                f.write("See detailed line-by-line comparison in the CSV output.\n\n")
            
            # Detailed line comparison
            f.write("## Detailed Line Analysis\n\n")
            
            divergent_count = 0
            for comparison in analysis['line_comparisons']:
                if comparison['match_status'] in ['variable_mismatch', 'no_corresponding_rust_line']:
                    divergent_count += 1
                    if divergent_count <= 10:  # Show first 10 divergences
                        f.write(f"### Divergence {divergent_count}\n\n")
                        f.write(f"**Python**: Line {comparison['python_line']} - `{comparison['python_function']}` - {comparison['python_action']}\n")
                        if comparison['rust_line']:
                            f.write(f"**Rust**: Line {comparison['rust_line']} - `{comparison['rust_function']}` - {comparison['rust_action']}\n")
                        else:
                            f.write("**Rust**: No corresponding line found\n")
                        
                        f.write(f"**Status**: {comparison['match_status']}\n\n")
                        
                        if comparison['variable_matches']:
                            f.write("**Variable Comparisons**:\n")
                            for var_name, var_comparison in comparison['variable_matches'].items():
                                if not var_comparison['match']:
                                    f.write(f"- `{var_name}`: Python=`{var_comparison['python_value']}`, Rust=`{var_comparison['rust_value']}` - {var_comparison['reason']}\n")
                        f.write("\n")
                    elif divergent_count == 11:
                        f.write("... (remaining divergences truncated, see CSV for complete data)\n\n")
            
            f.write("## Recommendations\n\n")
            if analysis['first_divergence']:
                f.write("1. Focus investigation on the first divergence point\n")
                f.write("2. Check mathematical formula implementation in Rust\n")
                f.write("3. Verify floating point precision handling\n")
                f.write("4. Compare intermediate calculation steps\n")
            else:
                f.write("1. Traces appear to match - investigate other sources of error\n")
                f.write("2. Check final output comparison\n")
                f.write("3. Verify test case selection\n")
        
        print(f"Detailed report saved to: {output_path}")
    
    def generate_csv_report(self, analysis: Dict, output_path: str = "trace_comparison.csv"):
        """Generate CSV file with line-by-line comparison."""
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Python_Line', 'Python_Function', 'Python_Action',
                'Rust_Line', 'Rust_Function', 'Rust_Action',
                'Match_Status', 'Variable_Differences', 'Notes'
            ])
            
            # Data rows
            for comparison in analysis['line_comparisons']:
                var_diffs = []
                for var_name, var_comp in comparison['variable_matches'].items():
                    if not var_comp['match']:
                        var_diffs.append(f"{var_name}: {var_comp['reason']}")
                
                writer.writerow([
                    comparison['python_line'],
                    comparison['python_function'],
                    comparison['python_action'],
                    comparison.get('rust_line', ''),
                    comparison.get('rust_function', ''),
                    comparison.get('rust_action', ''),
                    comparison['match_status'],
                    '; '.join(var_diffs),
                    '; '.join(comparison.get('notes', []))
                ])
        
        print(f"CSV comparison saved to: {output_path}")


def main():
    """Main analysis function."""
    # Parse command line arguments
    if len(sys.argv) > 2:
        python_trace_file = sys.argv[1]
        rust_trace_file = sys.argv[2]
    else:
        python_trace_file = "munsell_conversion_trace.txt"
        rust_trace_file = "rust_trace_ddeeee.txt"
    
    print("=== MunsellSpace Trace Analysis ===")
    print(f"Python trace: {python_trace_file}")
    print(f"Rust trace: {rust_trace_file}")
    print()
    
    # Initialize components
    parser = TraceParser()
    comparator = TraceComparator()
    reporter = ReportGenerator()
    
    # Parse trace files
    print("Parsing trace files...")
    python_lines = parser.parse_file(python_trace_file, is_rust=False)
    rust_lines = parser.parse_file(rust_trace_file, is_rust=True)
    
    if not python_lines:
        print(f"Error: Could not parse Python trace file: {python_trace_file}")
        return 1
    
    if not rust_lines:
        print(f"Error: Could not parse Rust trace file: {rust_trace_file}")
        return 1
    
    print(f"Parsed {len(python_lines)} Python lines and {len(rust_lines)} Rust lines")
    
    # Perform comparison
    print("Comparing traces...")
    analysis = comparator.compare_traces(python_lines, rust_lines)
    
    # Generate reports
    print("\n" + reporter.generate_console_summary(analysis))
    
    print("\nGenerating detailed reports...")
    reporter.generate_markdown_report(analysis)
    reporter.generate_csv_report(analysis)
    
    print("\nAnalysis complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())