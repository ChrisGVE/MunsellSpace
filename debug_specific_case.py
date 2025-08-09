#!/usr/bin/env python3
"""
Debug script for the specific case: #886648 -> 9.5R 4.5/6.0
"""

def analyze_hue_wedge_assignment():
    """Analyze how 9.5R should be assigned to wedges"""
    hue_number = 9.5
    hue_family = "R"
    
    print(f"Analyzing: {hue_number}{hue_family}")
    
    # Current logic: (9, 10] belongs to 10R
    if hue_number > 9.0 and hue_number <= 10.0:
        wedge_number = 10
        print(f"Current logic assigns to wedge: {wedge_number}R")
    
    # Expected polygon range: 8R to 2YR
    # This means it should cover wedges: 8R, 9R, 10R, 1YR
    # But the user says there are different interpretations
    
    print("\nPossible wedge interpretations for 8R-2YR polygon:")
    print("Interpretation 1: [8R, 9R, 10R, 1YR]")  
    print("Interpretation 2: [9R, 10R, 1YR, 2YR]")
    
    # For 9.5R (which should go to 10R wedge):
    print("\nFor 9.5R -> 10R wedge:")
    print("- Should be found in interpretation 1: YES (10R is included)")  
    print("- Should be found in interpretation 2: YES (10R is included)")
    
    # The polygon bounds: (3,2.5), (3,4.5), (7,4.5), (7,2.5)
    # Value=4.5, Chroma=6.0
    value, chroma = 4.5, 6.0
    print(f"\nPolygon bounds: (3,2.5), (3,4.5), (7,4.5), (7,2.5)")
    print(f"Point to test: Value={value}, Chroma={chroma}")
    
    # Check if point is in polygon
    # Chroma 6.0 should be between 3 and 7: YES
    # Value 4.5 should be between 2.5 and 4.5: YES (on boundary, included)
    print(f"Chroma {chroma} in range [3,7]: {3 <= chroma <= 7}")
    print(f"Value {value} in range [2.5,4.5]: {2.5 <= value <= 4.5}")
    
    if 3 <= chroma <= 7 and 2.5 <= value <= 4.5:
        print("Point SHOULD be classified!")
    else:
        print("Point should NOT be classified")

def trace_wedge_key_generation():
    """Trace how wedge keys are generated"""
    print("\nTracing wedge key generation:")
    
    # For 9.5R -> 10R wedge
    wedge_number = 10
    hue_family = "R"
    wedge_hue = f"{wedge_number}{hue_family}"  # "10R"
    
    print(f"Wedge hue: {wedge_hue}")
    
    # The system should look for a wedge key like "10R→1YR" 
    # This would be the wedge that starts at 10R and ends at 1YR
    
    print("Expected wedge key pattern: 10R→1YR (or similar)")
    
    print("\nTesting both interpretations:")
    print("If polygon is 8R-2YR with interpretation 1: [8R,9R,10R,1YR]")
    print("  Wedge keys would be: 8R→9R, 9R→10R, 10R→1YR, 1YR→2YR")
    print("  9.5R→10R wedge would search in: 10R→1YR") 
    
    print("\nIf polygon is 8R-2YR with interpretation 2: [9R,10R,1YR,2YR]")
    print("  Wedge keys would be: 9R→10R, 10R→1YR, 1YR→2YR")
    print("  9.5R→10R wedge would search in: 10R→1YR")
    
    print("\nBoth interpretations should work if 10R→1YR wedge exists!")

if __name__ == "__main__":
    analyze_hue_wedge_assignment()
    trace_wedge_key_generation()