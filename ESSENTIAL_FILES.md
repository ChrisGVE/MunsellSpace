# Essential Files - DO NOT DELETE

## Core Data Files
- `tests/data/srgb-to-munsell.csv` - 4007-color reference dataset (CRITICAL)
- `ISCC-NBS-Definitions.csv` - ISCC-NBS color definitions (if present)
- `src/munsell_renotation_data_entries.rs` - Munsell renotation data

## Documentation
- `README.md` - Project documentation
- `PRD.md` - Project requirements document
- `ALGO.md` - Algorithm documentation
- `TEST_COLORS_REFERENCE.md` - Test color set documentation
- `CLAUDE.md` - AI assistant guidance (gitignored)

## Source Files
- `src/` - All Rust source code
- `python/` - Python bindings
- `Cargo.toml` - Rust project configuration
- `pyproject.toml` - Python project configuration

## Test Infrastructure
- `test_colors.py` - 12-color test suite
- `validate_sampled.py` - Sampled validation script
- `fast_test_bench.py` - Fast benchmarking script

## Temporary Files (OK to delete)
- `test_*.py` - Temporary test scripts (except test_colors.py)
- `debug_*.py` - Debug scripts
- `trace_*.py` - Trace scripts
- `*.txt` - Output files
- `*.csv` - Generated CSV files (except reference data)
- `src/mathematical.rs.bak*` - Backup files