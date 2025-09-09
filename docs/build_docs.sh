#!/bin/bash

# Build script for distfeat Jupyter Book documentation

echo "Building distfeat documentation..."

# Change to book directory
cd book

# Clean previous builds
echo "Cleaning previous builds..."
jupyter-book clean . --all

# Build the book
echo "Building Jupyter Book..."
jupyter-book build . --all

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Documentation built successfully!"
    echo "📖 View at: book/_build/html/index.html"
    
    # Optional: Start local server
    read -p "Start local server? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Starting server at http://localhost:8000"
        cd _build/html
        python -m http.server 8000
    fi
else
    echo "❌ Build failed. Check errors above."
    exit 1
fi