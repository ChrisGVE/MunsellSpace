# Key Algorithm Differences Found

## 1. Center Coordinates (Grey Point)
**Python**: Uses xy coordinates of neutral Munsell at target value (which equals Illuminant C)
**Our Bug**: Was using ILLUMINANT_D65 in some places, ILLUMINANT_C in others

## 2. Hue Angle Inner Loop
**Python**:
```python
hue_angle_inner = (hue_angle_current + iterations_inner * (phi_input - phi_current)) % 360
```
- Steps by `(phi_input - phi_current)` each iteration
- Continues until phi_differences change sign OR 2+ points collected
- Then uses Extrapolator(LinearInterpolator) to find where phi_difference = 0

**Our Bug**: 
- Fixed 2-degree steps from -16 to +14 degrees
- Not adapting step size based on current error

## 3. Chroma Refinement Inner Loop
**Python**:
```python
chroma_inner = ((rho_input / rho_current) ** iterations_inner) * chroma_current
```
- Exponential scaling based on ratio of radii
- Continues until rho_input is between min/max of collected rho_bounds

**Our Bug**:
- Linear scaling from 0.5x to 2.0x
- Not using the correct exponential formula

## 4. Convergence Check
Both use euclidean distance between target and current xy, but the path to get there is very different.

## Fix Required
Reimplement the entire dual-loop algorithm to match Python exactly:
1. Fix center point to always use Illuminant C
2. Fix hue angle search to use adaptive stepping
3. Fix chroma refinement to use exponential scaling
4. Use proper extrapolation when needed