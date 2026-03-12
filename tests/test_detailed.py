"""
Detailed AI Client Test - Shows what works and what needs API keys
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp.ai_client import create_ai_client
from nlp.pattern_matcher import PatternMatcher, Intent


def test_pattern_matcher_detailed():
    """Test pattern matcher with various commands"""
    print("=" * 60)
    print("Pattern Matcher Tests (Fallback Mode - No API Key Needed)")
    print("=" * 60)

    matcher = PatternMatcher()

    test_cases = [
        # Test read intent
        ("show me main.py", Intent.READ, "main.py"),
        ("what's in app.js", Intent.READ, "app.js"),
        ("read the config file", Intent.READ, None),
        ("display utils.py", Intent.READ, "utils.py"),

        # Test list intent
        ("list files", Intent.LIST, None),
        ("what files are in src/", Intent.LIST, "src/"),
        ("show me all files in the project", Intent.LIST, None),
        ("ls", Intent.LIST, None),

        # Test search intent
        ("find functions that handle auth", Intent.SEARCH, "functions that handle auth"),
        ("search for database", Intent.SEARCH, "database"),
        ("where is the user module?", Intent.SEARCH, None),
        ("grep for 'TODO'", Intent.SEARCH, "TODO"),

        # Test write/create intent
        ("write hello.py", Intent.WRITE, "hello.py"),
        ("save this to test.js", Intent.WRITE, "test.js"),
        ("create a new file", Intent.CREATE, None),
        ("make a file called config.json", Intent.CREATE, "config.json"),

        # Test exit intent
        ("exit", Intent.EXIT, None),
        ("quit", Intent.EXIT, None),
        ("bye", Intent.EXIT, None),

        # Test help intent
        ("help", Intent.HELP, None),
        ("what can you do?", Intent.HELP, None),
        ("how do I search?", Intent.HELP, None),
    ]

    passed = 0
    failed = 0

    for command, expected_intent, expected_file in test_cases:
        parsed = matcher.parse_command(command)

        # Check intent
        if parsed['intent'] == expected_intent:
            status = "✅"
            passed += 1
        else:
            status = "❌"
            failed += 1

        print(f"{status} '{command}'")
        print(f"   Expected intent: {expected_intent.value}")
        print(f"   Detected intent: {parsed['intent'].value}")

        # Check file path if expected
        if expected_file:
            if parsed['file_path'] == expected_file:
                print(f"   ✅ File: {parsed['file_path']}")
            else:
                print(f"   ⚠️  Expected file: {expected_file}, got: {parsed['file_path']}")

        # Show suggestion
        suggestion = matcher.get_command_suggestion(command)
        print(f"   Suggestion: {suggestion}")
        print()

    print("=" * 60)
    print(f"Pattern Matcher Results: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


def test_ai_client_availability():
    """Test which AI providers are available"""
    print("\n" + "=" * 60)
    print("AI Provider Availability Check")
    print("=" * 60)

    providers = [
        ("zai", "ZAI_API_KEY", "z.ai (GLM)"),
        ("openai", "OPENAI_API_KEY", "OpenAI"),
        ("anthropic", "ANTHROPIC_API_KEY", "Anthropic"),
    ]

    available = []
    for provider, env_var, name in providers:
        if os.environ.get(env_var):
            available.append((provider, name))
            print(f"✅ {name}: API key found ({env_var})")
        else:
            print(f"⚠️  {name}: API key not found ({env_var})")

    # Check Ollama
    print(f"⚠️  Ollama: Local model (package not installed)")

    print()
    if available:
        print("✅ Available AI Providers:")
        for provider, name in available:
            print(f"   - {name} ({provider})")
    else:
        print("⚠️  No AI providers configured")
        print("   Using Pattern Matcher (fallback mode)")

    return available


def test_zai_client():
    """Test z.ai client if API key is available"""
    print("\n" + "=" * 60)
    print("z.ai (GLM) Client Test")
    print("=" * 60)

    api_key = os.environ.get("ZAI_API_KEY")

    if not api_key:
        print("⚠️  ZAI_API_KEY not found")
        print("   Skipping z.ai test...")
        return None

    try:
        print("✅ ZAI_API_KEY found")
        print("   Creating z.ai client...")

        client = create_ai_client(
            provider="zai",
            model="glm-4"
        )

        print("✅ Client created successfully")
        model_info = client.get_model_info()
        print(f"\nModel Info:")
        print(f"   Provider: {model_info['provider']}")
        print(f"   Model: {model_info['model']}")
        print(f"   Available models: {', '.join(model_info['available_models'])}")

        # Test simple completion
        print("\n🧪 Testing simple completion...")
        test_prompt = "What is 2 + 2? Answer with just the number."
        print(f"   Prompt: {test_prompt}")

        response = client.complete(test_prompt, max_tokens=50)
        print(f"   Response: {response}")

        # Test chat
        print("\n🧪 Testing chat with history...")
        messages = [
            {"role": "user", "content": "My name is Val."},
            {"role": "assistant", "content": "Nice to meet you, Val!"},
            {"role": "user", "content": "What's my name?"}
        ]
        print(f"   Testing context preservation...")

        response = client.chat(messages, max_tokens=50)
        print(f"   Response: {response}")

        print("\n✅ z.ai client test PASSED")
        return True

    except Exception as e:
        print(f"\n❌ z.ai client test FAILED")
        print(f"   Error: {str(e)}")
        return False


def main():
    print("\n" + "🚀" * 30)
    print("Zeal Code - Detailed AI Client Test")
    print("🚀" * 30 + "\n")

    # Test 1: Pattern matcher (always works)
    pattern_ok = test_pattern_matcher_detailed()

    # Test 2: Check available providers
    available_providers = test_ai_client_availability()

    # Test 3: Test z.ai if available
    zai_ok = None
    if "zai" in [p[0] for p in available_providers]:
        zai_ok = test_zai_client()

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    print(f"\n✅ Pattern Matcher: {'PASS' if pattern_ok else 'FAIL'}")
    print(f"   - Fallback mode: Always available")

    if zai_ok is not None:
        print(f"{'✅' if zai_ok else '❌'} z.ai (GLM) Client: {'PASS' if zai_ok else 'FAIL'}")
    elif zai_ok is False:
        print(f"❌ z.ai (GLM) Client: FAIL")
    else:
        print(f"⚠️  z.ai (GLM) Client: SKIPPED (no API key)")

    print(f"\n📊 Available AI Providers: {len(available_providers)}")
    for provider, name in available_providers:
        print(f"   - {name}")

    print("\n" + "=" * 60)
    print("✅ Detailed Test Complete")
    print("=" * 60)

    print("\n📚 Documentation:")
    print("   - README.md: Overview and quick start")
    print("   - ITERATION_0.1.md: Detailed iteration docs")
    print("   - ZEAL_CODE_ROADMAP.md: Complete roadmap")
    print("   - tests/test_ai_client.py: Basic test suite")


if __name__ == "__main__":
    main()
