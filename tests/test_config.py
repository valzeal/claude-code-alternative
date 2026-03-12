"""
Test Configuration System - Iteration 0.2
Tests config file management, API key handling, and workspace awareness
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.config import Config, load_config, init_config
from cli.workspace import Workspace, init_workspace


def test_config_creation():
    """Test config creation and loading"""
    print("=" * 60)
    print("Test 1: Config Creation and Loading")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yml"

        # Create config
        config = Config(config_path=config_path)

        print(f"✅ Config created: {config_path}")
        print(f"   Default provider: {config.get_provider()}")
        print(f"   Default model: {config.get_model()}")
        print(f"   CLI prompt: {config.get('cli', 'prompt')}")

        # Save config
        config.save()

        # Reload config
        config_reloaded = load_config(config_path=config_path)

        print(f"✅ Config reloaded successfully")
        print(f"   Provider matches: {config.get_provider() == config_reloaded.get_provider()}")

        return True


def test_config_api_keys():
    """Test API key handling"""
    print("\n" + "=" * 60)
    print("Test 2: API Key Handling")
    print("=" * 60)

    config = Config()

    # Test getting API keys (should return None if not set)
    zai_key = config.get_api_key("zai")
    openai_key = config.get_api_key("openai")
    anthropic_key = config.get_api_key("anthropic")

    print(f"✅ API Key Retrieval:")
    print(f"   z.ai: {'Set' if zai_key else 'Not Set'}")
    print(f"   OpenAI: {'Set' if openai_key else 'Not Set'}")
    print(f"   Anthropic: {'Set' if anthropic_key else 'Not Set'}")

    # Test API key validation
    print(f"\n✅ API Key Validation:")
    print(f"   z.ai valid format: {config.validate_api_key('zai')}")
    print(f"   OpenAI valid format: {config.validate_api_key('openai')}")
    print(f"   Anthropic valid format: {config.validate_api_key('anthropic')}")
    print(f"   Ollama (always valid): {config.validate_api_key('ollama')}")

    # Test with environment variables
    os.environ["ZAI_API_KEY"] = "test-key-for-zai-models-validation"
    config_env = Config()
    zai_key_env = config_env.get_api_key("zai")

    print(f"\n✅ Environment Variable Override:")
    print(f"   ZAI_API_KEY set: {zai_key_env is not None}")
    print(f"   Key starts with 'test-key': {zai_key_env.startswith('test-key')}")

    # Cleanup
    del os.environ["ZAI_API_KEY"]

    return True


def test_config_list_providers():
    """Test listing providers"""
    print("\n" + "=" * 60)
    print("Test 3: List Providers")
    print("=" * 60)

    config = Config()
    providers = config.list_providers()

    print(f"✅ Available Providers:")
    for provider_id, info in providers.items():
        default_marker = " [DEFAULT]" if info["default"] else ""
        print(f"\n   {info['name']}{default_marker}")
        print(f"   Models: {', '.join(info['models'])}")
        print(f"   API Key Set: {info['api_key_set']}")

    return True


def test_workspace_init():
    """Test workspace initialization"""
    print("\n" + "=" * 60)
    print("Test 4: Workspace Initialization")
    print("=" * 60)

    # Get current directory
    workspace = init_workspace()

    print(f"✅ Workspace initialized")
    print(f"   Path: {workspace.pwd()}")
    print(f"   Name: {workspace.name}")
    print(f"   Exists: {workspace.workspace_path.exists()}")
    print(f"   Is Directory: {workspace.workspace_path.is_dir()}")

    return True


def test_workspace_ls():
    """Test workspace file listing"""
    print("\n" + "=" * 60)
    print("Test 5: Workspace File Listing")
    print("=" * 60)

    workspace = init_workspace()

    try:
        files = workspace.ls()
        print(f"✅ Listed {len(files)} items in workspace")

        # Show first 5 items
        for i, file_info in enumerate(files[:5], 1):
            type_str = "DIR " if file_info["is_dir"] else "FILE"
            size_str = f"{file_info['size']} bytes" if not file_info["is_dir"] else ""
            print(f"   {i:2d}. [{type_str}] {file_info['name']:30s} {size_str}")

        if len(files) > 5:
            print(f"   ... and {len(files) - 5} more items")

        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_workspace_read():
    """Test workspace file reading"""
    print("\n" + "=" * 60)
    print("Test 6: Workspace File Reading")
    print("=" * 60)

    workspace = init_workspace()

    # Find a Python file to read
    test_files = list(workspace.workspace_path.glob("*.py"))
    if not test_files:
        print("⚠️  No Python files found in workspace")
        print(f"   Workspace path: {workspace.workspace_path}")
        return True

    test_file = test_files[0]

    try:
        lines = workspace.read(test_file.name)
        print(f"✅ Read file: {test_file.name}")
        print(f"   Lines: {len(lines)}")
        print(f"   First 3 lines:")
        for i, line in enumerate(lines[:3], 1):
            print(f"      {i:2d}. {line}")

        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_workspace_info():
    """Test workspace information"""
    print("\n" + "=" * 60)
    print("Test 7: Workspace Information")
    print("=" * 60)

    workspace = init_workspace()
    info = workspace.get_info()

    print(f"✅ Workspace Information:")
    print(f"   Path: {info['path']}")
    print(f"   Name: {info['name']}")
    print(f"   Top-level files: {info['file_count']}")
    print(f"   Top-level dirs: {info['dir_count']}")
    print(f"   Total files: {info['total_files']}")
    print(f"   Git repo: {'Yes' if info['is_git_repo'] else 'No'}")

    return True


def test_config_write():
    """Test config value setting"""
    print("\n" + "=" * 60)
    print("Test 8: Config Value Setting")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yml"
        config = Config(config_path=config_path)

        # Set some values
        config.set("ai", "provider", "openai")
        config.set("ai", "model", "gpt-4-turbo")
        config.set("cli", "prompt", ">>> ")
        config.set("output", "color", False)

        print(f"✅ Set configuration values:")
        print(f"   Provider: {config.get('ai', 'provider')}")
        print(f"   Model: {config.get('ai', 'model')}")
        print(f"   Prompt: {config.get('cli', 'prompt')}")
        print(f"   Color: {config.get('output', 'color')}")

        # Save and reload
        config.save()
        config_reloaded = load_config(config_path=config_path)

        print(f"\n✅ Saved and reloaded:")
        print(f"   Provider matches: {config.get('ai', 'provider') == config_reloaded.get('ai', 'provider')}")
        print(f"   Prompt matches: {config.get('cli', 'prompt') == config_reloaded.get('cli', 'prompt')}")

        return True


def main():
    print("\n" + "🚀" * 30)
    print("Zeal Code - Configuration System Test Suite (Iteration 0.2)")
    print("🚀" * 30 + "\n")

    tests = [
        ("Config Creation", test_config_creation),
        ("API Key Handling", test_config_api_keys),
        ("List Providers", test_config_list_providers),
        ("Workspace Init", test_workspace_init),
        ("Workspace LS", test_workspace_ls),
        ("Workspace Read", test_workspace_read),
        ("Workspace Info", test_workspace_info),
        ("Config Write", test_config_write),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with exception: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")

    if failed == 0:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {failed} test(s) failed")

    print("\n" + "=" * 60)
    print("✅ Test Suite Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
