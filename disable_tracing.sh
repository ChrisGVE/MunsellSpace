#!/bin/bash
# Temporarily disable trace output in python_port.rs

# Create backup
cp src/python_port.rs src/python_port.rs.trace_backup

# Comment out all eprintln! statements
sed -i '' 's/^[[:space:]]*eprintln!/    \/\/ eprintln!/g' src/python_port.rs

echo "Trace statements disabled. Backup saved to src/python_port.rs.trace_backup"