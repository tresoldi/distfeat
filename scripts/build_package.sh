#!/bin/bash

# Package building script for distfeat

set -e  # Exit on any error

echo "🏗️  Building distfeat package..."
echo "================================="

# Change to project root
cd "$(dirname "$0")/.."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Clean previous builds
echo -e "${BLUE}🧹 Cleaning previous builds...${NC}"
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/
find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Check if build tools are available
echo -e "${BLUE}🔍 Checking build tools...${NC}"
if ! python -m pip show build >/dev/null 2>&1; then
    echo -e "${YELLOW}📦 Installing build tools...${NC}"
    python -m pip install build twine
fi

# Lint and format check (optional)
echo -e "${BLUE}🔍 Running quality checks...${NC}"
if command -v ruff &> /dev/null; then
    echo "Running ruff checks..."
    ruff check distfeat/ || echo -e "${YELLOW}⚠️  Ruff warnings found${NC}"
fi

if command -v black &> /dev/null; then
    echo "Checking black formatting..."
    black --check distfeat/ || echo -e "${YELLOW}⚠️  Format issues found${NC}"
fi

# Run tests (optional but recommended)
if [ "${SKIP_TESTS:-false}" != "true" ]; then
    echo -e "${BLUE}🧪 Running tests...${NC}"
    if command -v pytest &> /dev/null; then
        python -m pytest tests/ --tb=short -q || {
            echo -e "${RED}❌ Tests failed. Use SKIP_TESTS=true to build anyway.${NC}"
            exit 1
        }
        echo -e "${GREEN}✅ Tests passed${NC}"
    else
        echo -e "${YELLOW}⚠️  pytest not found, skipping tests${NC}"
    fi
fi

# Build the package
echo -e "${BLUE}🏗️  Building package...${NC}"
python -m build

# Check the built package
echo -e "${BLUE}🔍 Checking built package...${NC}"
python -m twine check dist/*

# Display results
echo -e "${GREEN}✅ Package built successfully!${NC}"
echo
echo "Built files:"
ls -la dist/

echo
echo "Package info:"
python -c "
import os
files = [f for f in os.listdir('dist/') if f.endswith('.whl')]
if files:
    print(f'Wheel: {files[0]}')
    import zipfile
    with zipfile.ZipFile(f'dist/{files[0]}', 'r') as z:
        print(f'Contents: {len(z.namelist())} files')
        data_files = [f for f in z.namelist() if 'data/' in f]
        print(f'Data files: {len(data_files)} files')
"

echo
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Test install: pip install dist/*.whl"
echo "2. Test import: python -c 'import distfeat; print(distfeat.__version__)'"
echo "3. Upload to PyPI: twine upload dist/*"
echo
echo -e "${GREEN}🎉 Build complete!${NC}"