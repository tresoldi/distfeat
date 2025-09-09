#!/bin/bash

# Comprehensive test runner for distfeat

echo "🧪 Running distfeat test suite..."
echo "=================================="

# Change to project directory
cd "$(dirname "$0")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to run tests with specific markers
run_test_category() {
    local category=$1
    local marker=$2
    local description=$3
    
    echo -e "${BLUE}🔍 Running $category tests${NC}"
    echo "$description"
    echo "-----------------------------------"
    
    if pytest -m "$marker" --tb=short; then
        echo -e "${GREEN}✅ $category tests PASSED${NC}"
    else
        echo -e "${RED}❌ $category tests FAILED${NC}"
        return 1
    fi
    echo
}

# Parse command line arguments
FAST_ONLY=false
COVERAGE=true
PARALLEL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --fast)
            FAST_ONLY=true
            shift
            ;;
        --no-cov)
            COVERAGE=false
            shift
            ;;
        --parallel)
            PARALLEL=true
            shift
            ;;
        --help)
            echo "distfeat test runner"
            echo ""
            echo "Options:"
            echo "  --fast      Run only fast tests (skip slow/integration)"
            echo "  --no-cov    Skip coverage reporting"
            echo "  --parallel  Run tests in parallel"
            echo "  --help      Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Build pytest command
PYTEST_ARGS=""

if [ "$COVERAGE" = true ]; then
    PYTEST_ARGS="$PYTEST_ARGS --cov=distfeat --cov-report=term-missing --cov-report=html"
fi

if [ "$PARALLEL" = true ]; then
    PYTEST_ARGS="$PYTEST_ARGS -n auto"
fi

if [ "$FAST_ONLY" = true ]; then
    echo -e "${YELLOW}⚡ Running fast tests only${NC}"
    PYTEST_ARGS="$PYTEST_ARGS -m 'not slow and not integration'"
else
    echo -e "${BLUE}🔄 Running full test suite${NC}"
fi

# Check if pytest is available
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}❌ pytest not found. Install with: pip install pytest${NC}"
    exit 1
fi

# Check if distfeat is importable
if ! python -c "import distfeat" 2>/dev/null; then
    echo -e "${RED}❌ distfeat not importable. Run: pip install -e .${NC}"
    exit 1
fi

echo "Python version: $(python --version)"
echo "Pytest version: $(pytest --version)"
echo

# Run tests
if [ "$FAST_ONLY" = false ]; then
    # Run categorized tests
    run_test_category "Unit" "unit" "Fast, isolated tests for individual components"
    
    run_test_category "Integration" "integration" "Tests with real data and cross-component validation"
    
    run_test_category "Linguistic" "linguistic" "Tests validating linguistic properties and patterns"
    
    run_test_category "I/O" "io" "File input/output and data format tests"
    
    run_test_category "Performance" "performance" "Performance benchmarks and scalability tests"
    
    # Run all other tests
    echo -e "${BLUE}🔍 Running remaining tests${NC}"
    echo "All tests not covered by specific categories"
    echo "-----------------------------------"
    
    if pytest $PYTEST_ARGS --tb=short; then
        echo -e "${GREEN}✅ All tests PASSED${NC}"
        SUCCESS=true
    else
        echo -e "${RED}❌ Some tests FAILED${NC}"
        SUCCESS=false
    fi
else
    # Run fast tests only
    echo -e "${BLUE}🔍 Running fast tests${NC}"
    echo "-----------------------------------"
    
    if pytest $PYTEST_ARGS --tb=short; then
        echo -e "${GREEN}✅ Fast tests PASSED${NC}"
        SUCCESS=true
    else
        echo -e "${RED}❌ Fast tests FAILED${NC}"
        SUCCESS=false
    fi
fi

echo
echo "=================================="

if [ "$SUCCESS" = true ]; then
    echo -e "${GREEN}🎉 Test suite completed successfully!${NC}"
    
    if [ "$COVERAGE" = true ]; then
        echo -e "${BLUE}📊 Coverage report generated in htmlcov/index.html${NC}"
    fi
    
    exit 0
else
    echo -e "${RED}💥 Test suite failed. Check the output above for details.${NC}"
    exit 1
fi