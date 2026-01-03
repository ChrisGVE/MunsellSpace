# Extended Domain Comparison Report

Generated: 2026-01-03 13:22:55
Families analyzed: 21

## Summary: All Methods × All Domains

| Method | Domain | Mean Loss | Std Loss |
|--------|--------|-----------|----------|
| Translation+Scaling | Munsell | 0.0535 | 0.0123 |
| Affine | Munsell | 0.0776 | 0.0481 |
| Translation+Scaling | RGB | 1.4197 | 0.9419 |

## Analysis by Method

### Translation+Scaling
- Munsell: 0.0535
- RGB: 1.4197
- RGB/Munsell ratio: 26.6x

## Key Findings

1. **Best combination**: Translation+Scaling in Munsell domain (0.0535)
2. **Munsell domain is consistently better** (0.0535 vs 1.4197)

## Limitations

- RGB↔Munsell conversions are **approximate** (HSV-based)
- Exact conversion requires Munsell renotation data
- Some error in RGB domain is due to conversion, not the method
- Future work: Use MunsellSpace library for accurate conversion