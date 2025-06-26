#!/usr/bin/env bash
# Build script for Render.com deployment

echo "Python version:"
python --version

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Build completed successfully!" 