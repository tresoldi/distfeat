#!/bin/bash

# Minimal build script for distfeat Jupyter Book documentation

echo "Building distfeat documentation (minimal version)..."

# Change to book directory
cd /home/tiagot/tiatre/unipa/distfeat/docs/book

# Clean previous builds
echo "Cleaning previous builds..."
jupyter-book clean . --all

# Use minimal config for this build
echo "Using minimal configuration..."
cp _config_minimal.yml _config.yml

# Build the book
echo "Building Jupyter Book..."
jupyter-book build . 2>&1

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Documentation built successfully!"
    echo "📖 View at: file:///home/tiagot/tiatre/unipa/distfeat/docs/book/_build/html/index.html"
    
    # List what was built
    echo "📄 Generated files:"
    ls -la _build/html/
else
    echo "❌ Build failed. Check errors above."
    exit 1
fi