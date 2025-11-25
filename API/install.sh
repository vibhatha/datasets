#!/bin/bash

# Installation script for opendata package

echo "Installing opendata package..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.8 or higher is required. Found: $python_version"
    exit 1
fi

# Install in development mode
echo "Installing in development mode..."
pip3 install -e .

echo "Installation completed!"
echo ""
echo "You can now use the opendata package:"
echo "  python3 -c 'import opendata; print(opendata.__version__)'"
echo "  python3 example_usage.py"
