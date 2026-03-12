#!/bin/bash
# Quick Test Script for Configuration System - Iteration 0.2
# Usage: ./quick_test_config.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "Zeal Code Configuration System Test"
echo "=========================================="
echo ""

# Check if we're in project directory
if [ ! -f "$SCRIPT_DIR/cli/config.py" ]; then
    echo "❌ Error: Must run from claude-code-alternative directory"
    echo "   Current directory: $(pwd)"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found"
    exit 1
fi

echo "🧪 Running Configuration System Tests..."
echo ""

cd "$SCRIPT_DIR"
python3 tests/test_config.py

echo ""
echo "=========================================="
echo "✅ Quick Test Complete"
echo "=========================================="
echo ""
echo "📚 Documentation:"
echo "   - ITERATION_0.2.md: Iteration details"
echo "   - cli/config.py: Configuration module"
echo "   - cli/workspace.py: Workspace module"
