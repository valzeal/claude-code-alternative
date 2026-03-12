#!/bin/bash
# Quick Test Script for Zeal Code AI Client
# Usage: ./quick_test.sh [provider]
# Provider options: zai, openai, anthropic (default: zai)

PROVIDER=${1:-zai}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "Zeal Code AI Client Quick Test"
echo "=========================================="
echo ""

# Check if we're in the project directory
if [ ! -f "$SCRIPT_DIR/nlp/ai_client.py" ]; then
    echo "❌ Error: Must run from claude-code-alternative directory"
    echo "   Current directory: $(pwd)"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found"
    exit 1
fi

# Test 1: Pattern Matcher (always works)
echo "🧪 Test 1: Pattern Matcher (Fallback Mode)"
echo "------------------------------------------"
cd "$SCRIPT_DIR"
python3 -c "
from nlp.pattern_matcher import PatternMatcher
matcher = PatternMatcher()
tests = ['show me main.py', 'what files in src/', 'find auth functions']
for test in tests:
    parsed = matcher.parse_command(test)
    print(f'✅ \"{test}\" → {parsed[\"intent\"].value}')
"
echo ""

# Test 2: AI Client Factory
echo "🧪 Test 2: AI Client Factory"
echo "------------------------------------------"
case "$PROVIDER" in
    zai)
        ENV_VAR="ZAI_API_KEY"
        ;;
    openai)
        ENV_VAR="OPENAI_API_KEY"
        ;;
    anthropic)
        ENV_VAR="ANTHROPIC_API_KEY"
        ;;
    *)
        echo "❌ Unknown provider: $PROVIDER"
        echo "   Supported: zai, openai, anthropic"
        exit 1
        ;;
esac

if [ -z "${!ENV_VAR}" ]; then
    echo "⚠️  $ENV_VAR not set"
    echo "   Set it with: export $ENV_VAR='your-api-key'"
    echo "   Skipping AI client test..."
else
    echo "✅ $ENV_VAR found"
    python3 -c "
from nlp.ai_client import create_ai_client
try:
    client = create_ai_client(provider='$PROVIDER')
    info = client.get_model_info()
    print(f'✅ Client created successfully')
    print(f'   Provider: {info[\"provider\"]}')
    print(f'   Model: {info[\"model\"]}')
    print(f'   Available: {', '.join(info[\"available_models\"])}')
except Exception as e:
    print(f'❌ Error: {e}')
"
fi

echo ""
echo "=========================================="
echo "✅ Quick Test Complete"
echo "=========================================="
echo ""
echo "📚 For full test suite: python3 tests/test_ai_client.py"
echo "📖 For roadmap: cat ZEAL_CODE_ROADMAP.md"
echo "📝 For iteration details: cat ITERATION_0.1.md"
