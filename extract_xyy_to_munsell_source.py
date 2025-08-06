#!/usr/bin/env python3
"""Extract xyY_to_munsell_specification source code"""

import inspect
import colour.notation.munsell as munsell

try:
    # Get _xyY_to_munsell_specification (the actual implementation)
    source = inspect.getsource(munsell._xyY_to_munsell_specification)
    print('_xyY_to_munsell_specification source:')
    print('=' * 80)
    print(source)
    print()
    print('=' * 80)
    
    # Get wrapper function
    source = inspect.getsource(munsell.xyY_to_munsell_specification)
    print('xyY_to_munsell_specification wrapper:')
    print('=' * 80)
    print(source)
    
except Exception as e:
    print(f'Error: {e}')