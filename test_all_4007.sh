#!/bin/bash

echo "================================================================================"
echo "TESTING ALL 4,007 COLORS - Rust vs Reference Dataset"
echo "================================================================================"

# Prepare input file
echo "Preparing input file..."
tail -n +2 tests/data/srgb-to-munsell.csv | cut -d',' -f1-3 > /tmp/rgb_input.txt

# Count lines
TOTAL=$(wc -l < /tmp/rgb_input.txt | tr -d ' ')
echo "Total colors to test: $TOTAL"

# Run batch converter
echo ""
echo "Running Rust batch converter on all $TOTAL colors..."
START=$(date +%s)
./target/release/batch_convert < /tmp/rgb_input.txt > /tmp/rust_output.txt
END=$(date +%s)
ELAPSED=$((END - START))

echo "✓ Completed in $ELAPSED seconds"
echo "  Rate: $((TOTAL / ELAPSED)) colors/second"

# Extract expected values
echo ""
echo "Extracting expected values..."
tail -n +2 tests/data/srgb-to-munsell.csv | cut -d',' -f4 > /tmp/expected_output.txt

# Compare results
echo ""
echo "Comparing results..."
paste /tmp/expected_output.txt /tmp/rust_output.txt > /tmp/comparison.txt

# Count exact matches
EXACT=$(awk '$1 == $2 {count++} END {print count}' /tmp/comparison.txt)
PERCENT=$((EXACT * 100 / TOTAL))

echo ""
echo "================================================================================"
echo "RESULTS"
echo "================================================================================"
echo "Total colors tested:  $TOTAL"
echo "Exact matches:        $EXACT ($PERCENT%)"
echo "Differences:          $((TOTAL - EXACT)) ($((100 - PERCENT))%)"

# Show some examples
echo ""
echo "First 20 comparisons:"
head -20 /tmp/comparison.txt | nl

echo ""
echo "✓ VALIDATION COMPLETE!"