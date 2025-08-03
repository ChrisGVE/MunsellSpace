#!/bin/bash

echo "Testing mathematical Munsell conversion against Python:"
echo ""

echo "Red (255,0,0):"
./target/release/mathematical_convert_rgb 255 0 0 2>/dev/null | grep -v "^TRACE"
echo "Expected: 7.9R 5.2/20.4"
echo ""

echo "Green (0,255,0):"
./target/release/mathematical_convert_rgb 0 255 0 2>/dev/null | grep -v "^TRACE"
echo "Expected: 9.9GY 8.7/19.4"
echo ""

echo "Orange (255,165,0):"
./target/release/mathematical_convert_rgb 255 165 0 2>/dev/null | grep -v "^TRACE"
echo "Expected: 8.5YR 7.4/13.3"
echo ""

echo "Purple (128,0,128):"
./target/release/mathematical_convert_rgb 128 0 128 2>/dev/null | grep -v "^TRACE"
echo "Expected: 9.3P 2.9/13.8"
echo ""

echo "Cyan (0,255,255):"
./target/release/mathematical_convert_rgb 0 255 255 2>/dev/null | grep -v "^TRACE"
echo "Expected: 6.6BG 9.1/10.9"
echo ""

echo "Magenta (255,0,255):"
./target/release/mathematical_convert_rgb 255 0 255 2>/dev/null | grep -v "^TRACE"
echo "Expected: 8.5P 5.9/25.1"