#!/usr/bin/env bash
# Build script for Render.com deployment

echo "Python version:"
python --version

# Check if Python version is 3.11.x
PYTHON_VERSION=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Detected Python version: $PYTHON_VERSION"

if [[ "$PYTHON_VERSION" != "3.11" ]]; then
    echo "ERROR: Python 3.11 is required, but found $PYTHON_VERSION"
    echo "Please set PYTHON_VERSION=3.11.8 in Render.com environment variables"
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Build completed successfully!" 