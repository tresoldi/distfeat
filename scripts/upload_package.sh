#!/bin/bash

# Package upload script for distfeat

set -e  # Exit on any error

echo "🚀 Uploading distfeat to PyPI..."
echo "================================="

# Change to project root
cd "$(dirname "$0")/.."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if dist/ exists
if [ ! -d "dist/" ] || [ -z "$(ls -A dist/)" ]; then
    echo -e "${RED}❌ No distribution files found. Run build first:${NC}"
    echo "   ./scripts/build_package.sh"
    exit 1
fi

# List files to upload
echo -e "${BLUE}📦 Files to upload:${NC}"
ls -la dist/

# Check files
echo -e "${BLUE}🔍 Checking package integrity...${NC}"
python -m twine check dist/*

# Ask for confirmation
echo
echo -e "${YELLOW}⚠️  Upload destination:${NC}"
if [ "${TEST_PYPI:-false}" == "true" ]; then
    echo "   🧪 Test PyPI (https://test.pypi.org/)"
    REPO_ARGS="--repository testpypi"
else
    echo "   🌍 Production PyPI (https://pypi.org/)"
    REPO_ARGS=""
fi

echo
read -p "Continue with upload? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🚫 Upload cancelled${NC}"
    exit 0
fi

# Upload
echo -e "${BLUE}🚀 Uploading...${NC}"
if [ "${TEST_PYPI:-false}" == "true" ]; then
    python -m twine upload --repository testpypi dist/*
    echo -e "${GREEN}✅ Uploaded to Test PyPI!${NC}"
    echo
    echo "Test install with:"
    echo "   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ distfeat"
else
    python -m twine upload dist/*
    echo -e "${GREEN}✅ Uploaded to PyPI!${NC}"
    echo
    echo "Install with:"
    echo "   pip install distfeat"
fi

echo
echo -e "${BLUE}📋 Next steps:${NC}"
if [ "${TEST_PYPI:-false}" == "true" ]; then
    echo "1. Test the installation from Test PyPI"
    echo "2. If everything works, upload to production:"
    echo "   ./scripts/upload_package.sh"
else
    echo "1. Update documentation with new version"
    echo "2. Create GitHub release with tag v0.2.0"
    echo "3. Announce the release"
fi

echo
echo -e "${GREEN}🎉 Upload complete!${NC}"