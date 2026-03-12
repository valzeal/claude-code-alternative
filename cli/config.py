"""
Configuration Management for Zeal Code
Handles API keys, provider settings, and CLI preferences
"""

import os
import yaml
from pathlib import Path
from typing import Optional, Dict, Any
import re


class Config:
    """Configuration manager for Zeal Code"""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration manager

        Args:
            config_path: Path to config file (default: ~/.zeal-code/config.yml)
        """
        self.config_path = config_path or Path.home() / ".zeal-code" / "config.yml"
        self.config_dir = self.config_path.parent

        # Default configuration
        self.defaults = {
            "ai": {
                "provider": "zai",  # Priority: zai, openai, anthropic, ollama
                "model": "glm-4",
                "api_key": None,
                # Provider-specific configs
                "zai": {
                    "model": "glm-4",
                    "base_url": "https://open.bigmodel.cn/api/paas/v4"
                },
                "openai": {
                    "model": "gpt-4",
                    "base_url": "https://api.openai.com/v1"
                },
                "anthropic": {
                    "model": "claude-3-opus",
                    "base_url": "https://api.anthropic.com"
                },
                "ollama": {
                    "model": "llama2",
                    "base_url": "http://localhost:11434"
                }
            },
            "cli": {
                "prompt": "> ",
                "history_file": str(Path.home() / ".zeal-code" / "history"),
                "max_context_files": 10
            },
            "files": {
                "ignore_patterns": [
                    ".git",
                    "__pycache__",
                    "node_modules",
                    ".env",
                    "*.pyc",
                    ".DS_Store"
                ],
                "show_hidden": False
            },
            "output": {
                "color": True,
                "line_numbers": True,
                "max_lines": 100
            }
        }

        # Load configuration
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file with environment variable override

        Returns:
            Configuration dictionary
        """
        # Start with defaults
        config = self.defaults.copy()

        # Load from file if exists
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    file_config = yaml.safe_load(f)
                    if file_config:
                        config = self._deep_merge(config, file_config)
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")

        # Override with environment variables
        self._apply_env_overrides(config)

        return config

    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """
        Deep merge two dictionaries

        Args:
            base: Base dictionary
            override: Override dictionary

        Returns:
            Merged dictionary
        """
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def _apply_env_overrides(self, config: Dict) -> None:
        """
        Apply environment variable overrides

        Environment variables:
        - ZAI_API_KEY: z.ai API key
        - OPENAI_API_KEY: OpenAI API key
        - ANTHROPIC_API_KEY: Anthropic API key
        - ZEAL_CODE_PROVIDER: Default provider
        - ZEAL_CODE_MODEL: Default model
        """
        env_overrides = {
            "ZAI_API_KEY": ("ai", "api_key"),
            "OPENAI_API_KEY": ("ai", "api_key"),
            "ANTHROPIC_API_KEY": ("ai", "api_key"),
            "ZEAL_CODE_PROVIDER": ("ai", "provider"),
            "ZEAL_CODE_MODEL": ("ai", "model")
        }

        for env_var, (section, key) in env_overrides.items():
            value = os.environ.get(env_var)
            if value:
                # Special handling for API keys
                if "API_KEY" in env_var:
                    provider = env_var.replace("_API_KEY", "").lower()
                    if "api" not in config["ai"]:
                        config["ai"]["api"] = {}
                    config["ai"]["api"][provider] = {"api_key": value}
                    config["ai"]["api_key"] = value
                else:
                    config[section][key] = value

    def get(self, *keys: str, default: Any = None) -> Any:
        """
        Get configuration value

        Args:
            *keys: Nested keys (e.g., get("ai", "provider"))
            default: Default value if key not found

        Returns:
            Configuration value
        """
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set(self, *keys_and_value) -> None:
        """
        Set configuration value

        Args:
            *keys_and_value: Nested keys (e.g., set("ai", "provider", "zai"))
                           Last argument is the value
        """
        if len(keys_and_value) < 2:
            raise ValueError("set() requires at least 2 arguments: keys and value")

        keys = keys_and_value[:-1]
        value = keys_and_value[-1]

        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value

    def save(self) -> None:
        """Save configuration to file"""
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Remove sensitive values before saving
        config_to_save = self._prepare_for_save(self.config)

        # Write to file
        with open(self.config_path, 'w') as f:
            yaml.dump(config_to_save, f, default_flow_style=False, sort_keys=False)

        print(f"✅ Configuration saved to {self.config_path}")

    def _prepare_for_save(self, config: Dict) -> Dict:
        """
        Prepare config for saving (remove sensitive values)

        Args:
            config: Configuration dictionary

        Returns:
            Sanitized config
        """
        config = config.copy()

        # Remove API keys (they should be in env vars)
        if "ai" in config:
            if "api_key" in config["ai"]:
                del config["ai"]["api_key"]

        return config

    def get_api_key(self, provider: str) -> Optional[str]:
        """
        Get API key for provider

        Args:
            provider: Provider name (zai, openai, anthropic)

        Returns:
            API key or None
        """
        # Try direct config first
        api_key = self.get("ai", "api_key")

        # Try provider-specific config
        if not api_key and "api" in self.get("ai"):
            provider_config = self.get("ai", "api", {})
            if provider in provider_config:
                api_key = provider_config[provider].get("api_key")

        # Try environment variable
        if not api_key:
            env_var = f"{provider.upper()}_API_KEY"
            api_key = os.environ.get(env_var)

        return api_key

    def get_provider(self) -> str:
        """
        Get configured AI provider

        Returns:
            Provider name
        """
        return self.get("ai", "provider", default="zai")

    def get_model(self) -> str:
        """
        Get configured AI model

        Returns:
            Model name
        """
        provider = self.get_provider()
        return self.get("ai", provider, "model", default=self.get("ai", "model", default="glm-4"))

    def validate_api_key(self, provider: str) -> bool:
        """
        Validate API key format for provider

        Args:
            provider: Provider name

        Returns:
            True if valid format, False otherwise
        """
        api_key = self.get_api_key(provider)

        if not api_key:
            return False

        # Provider-specific validation
        if provider == "zai":
            # z.ai keys are typically alphanumeric with dots
            return len(api_key) >= 20
        elif provider == "openai":
            # OpenAI keys start with sk-
            return api_key.startswith("sk-")
        elif provider == "anthropic":
            # Anthropic keys start with sk-ant-
            return api_key.startswith("sk-ant-")
        elif provider == "ollama":
            # Ollama doesn't use API keys
            return True

        return False

    def list_providers(self) -> Dict[str, Dict[str, Any]]:
        """
        List all configured providers

        Returns:
            Dict of provider info
        """
        providers = {
            "zai": {
                "name": "z.ai (GLM)",
                "models": ["glm-4", "glm-5", "glm-3-turbo"],
                "api_key_set": bool(self.get_api_key("zai")),
                "default": self.get_provider() == "zai"
            },
            "openai": {
                "name": "OpenAI",
                "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
                "api_key_set": bool(self.get_api_key("openai")),
                "default": self.get_provider() == "openai"
            },
            "anthropic": {
                "name": "Anthropic",
                "models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
                "api_key_set": bool(self.get_api_key("anthropic")),
                "default": self.get_provider() == "anthropic"
            },
            "ollama": {
                "name": "Ollama (Local)",
                "models": ["llama2", "mistral", "codellama", "phi"],
                "api_key_set": True,  # Ollama doesn't need API keys
                "default": self.get_provider() == "ollama"
            }
        }

        return providers

    def __repr__(self) -> str:
        """String representation"""
        return f"Config(path={self.config_path}, provider={self.get_provider()})"


def load_config(config_path: Optional[Path] = None) -> Config:
    """
    Load configuration

    Args:
        config_path: Path to config file

    Returns:
        Config instance
    """
    return Config(config_path=config_path)


def init_config() -> Config:
    """
    Initialize configuration (ensure config directory and file exist)

    Returns:
        Config instance
    """
    config = load_config()
    config.save()  # Ensure config file exists
    return config
