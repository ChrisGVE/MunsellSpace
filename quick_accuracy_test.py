#!/usr/bin/env python3
"""Quick accuracy test"""

def parse_munsell(notation):
    if not notation or notation == 'N/A' or notation.startswith('ERROR'):
        return None
    notation = notation.strip()
    if notation.startswith('N '):
        return {'family': 'N', 'hue': 0.0, 'value': float(notation.split()[1]), 'chroma': 0.0}
    parts = notation.split(' ')
    if len(parts) != 2:
        return None
    hue_part = parts[0]
    value_chroma = parts[1].split('/')
    hue_num = ''
    for char in hue_part:
        if char.isdigit() or char == '.':
            hue_num += char
        else:
            family = hue_part[len(hue_num):]
            break
    return {
        'family': family,
        'hue': float(hue_num) if hue_num else 0.0,
        'value': float(value_chroma[0]),
        'chroma': float(value_chroma[1]) if len(value_chroma) > 1 else 0.0
    }

python_results = []
with open('python_4007_final.txt', 'r') as f:
    for line in f:
        python_results.append(line.strip())

rust_results = []
with open('rust_4007_fixed.txt', 'r') as f:
    for line in f:
        rust_results.append(line.strip())

exact_matches = 0
family_mismatches = 0
for i in range(min(len(rust_results), len(python_results))):
    rust = parse_munsell(rust_results[i])
    python = parse_munsell(python_results[i])
    if not rust or not python:
        continue
    if rust == python:
        exact_matches += 1
    elif rust['family'] != python['family']:
        family_mismatches += 1

print(f'Exact matches: {exact_matches}/{len(rust_results)} ({100*exact_matches/len(rust_results):.2f}%)')
print(f'Family mismatches: {family_mismatches}')