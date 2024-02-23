#!/bin/bash

# Get the current directory.
current_directory="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
run_path="${current_directory}/run.sh"

# Set execute permissions for run.sh.
chmod +x "${run_path}"

# Create a symbolic link.
sudo ln -s "${run_path}" /usr/local/bin/i2c-stress-test

# Install dependencies using Requirements.txt.
pip3 install -r "${current_directory}/Requirements.txt"

# Setup Kivy configuration.
python3 "${current_directory}/settings/kivy_config.py"