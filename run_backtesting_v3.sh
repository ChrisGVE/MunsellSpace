#!/bin/bash
# Build the release version first
echo "Building release version..."
cargo build --release --bin test_rgb_cli

# Run the backtesting agent
echo "Running backtesting agent v3..."
python3 conv_backtesting_agent_v3.py

echo "Done! Check backtesting_report_v3.md and BACKTESTING_DETAILS.md"