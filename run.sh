#!/bin/bash

# Get the current directory
app_path="/home/$(whoami)/i2c_stress_test/app.py"

# Export DISPLAY=:0.0
export DISPLAY=:0.0

# Run the app
python3 "${app_path}"