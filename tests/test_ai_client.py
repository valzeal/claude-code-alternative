"""
Test AI Client - Iteration 0.1
Tests z.ai (GLM) client and fallback pattern matching
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp.ai_client import create_ai_client
from nlp.pattern_matcher import PatternMatcher, Intent


def test_pattern_matcher():
    """Test pattern matcher (fallback mode)"""
    print("=" * 60)
    print("Testing Pattern Matcher (Fallback Mode)")
    print("=" * 60)

    matcher = PatternMatcher()

    test_commands = [
        "show me main.py",
        "what files are in src/",
        "find functions that handle auth",
        "create a new file called utils.py",
        "where is the database connection?",
        "exit"
    ]

    for cmd in test_commands:
        print(f"\n📝 Command: '{cmd}'")
        parsed = matcher.parse_command(cmd)
        print(f"   Intent: {parsed['intent'].value}")
        print(f"   Suggestion: {matcher.get_command_suggestion(cmd)}")


def test_zai_client():
    """Test z.ai client"""
    print("\n" + "=" * 60)
    print("Testing z.ai (GLM) Client")
    print("=" * 60)

    # Check for API key
    api_key = os.environ.get("ZAI_API_KEY")

    if not api_key:
        print("⚠️  ZAI_API_KEY not found in environment")
        print("   Set it with: export ZAI_API_KEY='your-key-here'")
        print("   Skipping z.ai test...")
        return

    try:
        print("✅ ZAI_API_KEY found")
        print("   Creating z.ai client...")

        client = create_ai_client(
            provider="zai",
            model="glm-4"
        )

        print("✅ Client created successfully")
        model_info = client.get_model_info()
        print(f"   Provider: {model_info['provider']}")
        print(f"   Model: {model_info['model']}")
        print(f"   Available models: {', '.join(model_info['available_models'])}")

        # Test simple completion
        print("\n🧪 Testing simple completion...")
        test_prompt = "What is 2 + 2? Give a short answer."
        response = client.complete(test_prompt)

        print(f"   Prompt: {test_prompt}")
        print(f"   Response: {response[:100]}...")

        print("\n✅ z.ai client test PASSED")

    except Exception as e:
        print(f"\n❌ z.ai client test FAILED")
        print(f"   Error: {str(e)}")


def test_ai_client_factory():
    """Test AI client factory function"""
    print("\n" + "=" * 60)
    print("Testing AI Client Factory")
    print("=" * 60)

    providers = ["zai", "openai", "anthropic", "ollama"]

    for provider in providers:
        print(f"\n📦 Testing provider: {provider}")
        try:
            if provider == "ollama":
                # Ollama doesn't need API key
                client = create_ai_client(provider=provider)
                print(f"   ✅ {provider} client created")
            else:
                # Check if API key exists
                env_var = f"{provider.upper()}_API_KEY"
                if os.environ.get(env_var):
                    client = create_ai_client(provider=provider)
                    print(f"   ✅ {provider} client created")
                else:
                    print(f"   ⚠️  {env_var} not found, skipping...")

        except ValueError as e:
            print(f"   ⚠️  {e}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")


if __name__ == "__main__":
    print("\n" + "🚀" * 30)
    print("Zeal Code - AI Client Test Suite (Iteration 0.1)")
    print("🚀" * 30 + "\n")

    # Test 1: Pattern matcher (always works)
    test_pattern_matcher()

    # Test 2: AI client factory
    test_ai_client_factory()

    # Test 3: z.ai client (requires API key)
    test_zai_client()

    print("\n" + "=" * 60)
    print("✅ Test Suite Complete")
    print("=" * 60)
