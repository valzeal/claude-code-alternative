"""
AI Client for Zeal Code - BYOK (Bring Your Own Key) Implementation
Supports: z.ai (GLM), OpenAI, Anthropic, Ollama
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import os
import json


class AIClient(ABC):
    """Base class for AI provider clients"""

    def __init__(self, api_key: str, model: str, **kwargs):
        self.api_key = api_key
        self.model = model
        self.config = kwargs

    @abstractmethod
    def complete(self, prompt: str, **kwargs) -> str:
        """Complete a prompt and return the response"""
        pass

    @abstractmethod
    def chat(self, messages: list, **kwargs) -> str:
        """Chat with the AI using a message history"""
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        pass


class ZaiClient(AIClient):
    """z.ai (GLM) AI Client - Priority Provider"""

    def __init__(self, api_key: str, model: str = "glm-4", base_url: str = None, **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.base_url = base_url or "https://open.bigmodel.cn/api/paas/v4"
        self._client = None
        self._init_client()

    def _init_client(self):
        """Initialize z.ai client"""
        try:
            from zhipuai import ZhipuAI
            self._client = ZhipuAI(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "zhipuai package not installed. Install with: pip install zhipuai"
            )

    def complete(self, prompt: str, **kwargs) -> str:
        """Complete a prompt using z.ai"""
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"z.ai API error: {str(e)}")

    def chat(self, messages: list, **kwargs) -> str:
        """Chat with z.ai using message history"""
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"z.ai API error: {str(e)}")

    def get_model_info(self) -> Dict[str, Any]:
        """Get z.ai model information"""
        return {
            "provider": "z.ai",
            "model": self.model,
            "base_url": self.base_url,
            "available_models": ["glm-4", "glm-5", "glm-3-turbo"]
        }


class OpenAIClient(AIClient):
    """OpenAI AI Client"""

    def __init__(self, api_key: str, model: str = "gpt-4", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self._client = None
        self._init_client()

    def _init_client(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            self._client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "openai package not installed. Install with: pip install openai"
            )

    def complete(self, prompt: str, **kwargs) -> str:
        """Complete a prompt using OpenAI"""
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def chat(self, messages: list, **kwargs) -> str:
        """Chat with OpenAI using message history"""
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def get_model_info(self) -> Dict[str, Any]:
        """Get OpenAI model information"""
        return {
            "provider": "OpenAI",
            "model": self.model,
            "available_models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
        }


class AnthropicClient(AIClient):
    """Anthropic AI Client"""

    def __init__(self, api_key: str, model: str = "claude-3-opus", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self._client = None
        self._init_client()

    def _init_client(self):
        """Initialize Anthropic client"""
        try:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "anthropic package not installed. Install with: pip install anthropic"
            )

    def complete(self, prompt: str, **kwargs) -> str:
        """Complete a prompt using Anthropic"""
        try:
            response = self._client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", 4096),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")

    def chat(self, messages: list, **kwargs) -> str:
        """Chat with Anthropic using message history"""
        try:
            response = self._client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", 4096),
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")

    def get_model_info(self) -> Dict[str, Any]:
        """Get Anthropic model information"""
        return {
            "provider": "Anthropic",
            "model": self.model,
            "available_models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]
        }


class OllamaClient(AIClient):
    """Ollama AI Client - Local Models"""

    def __init__(self, model: str = "llama2", base_url: str = None, **kwargs):
        super().__init__(api_key="", model=model, **kwargs)
        self.base_url = base_url or "http://localhost:11434"
        self._client = None
        self._init_client()

    def _init_client(self):
        """Initialize Ollama client"""
        try:
            from ollama import Client
            self._client = Client(host=self.base_url)
        except ImportError:
            raise ImportError(
                "ollama package not installed. Install with: pip install ollama"
            )

    def complete(self, prompt: str, **kwargs) -> str:
        """Complete a prompt using Ollama"""
        try:
            response = self._client.chat(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")

    def chat(self, messages: list, **kwargs) -> str:
        """Chat with Ollama using message history"""
        try:
            response = self._client.chat(
                model=self.model,
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")

    def get_model_info(self) -> Dict[str, Any]:
        """Get Ollama model information"""
        return {
            "provider": "Ollama",
            "model": self.model,
            "base_url": self.base_url,
            "available_models": ["llama2", "mistral", "codellama", "phi"]
        }


def create_ai_client(
    provider: str,
    api_key: str = None,
    model: str = None,
    **kwargs
) -> AIClient:
    """
    Factory function to create AI client based on provider

    Args:
        provider: AI provider name (zai, openai, anthropic, ollama)
        api_key: API key (not needed for Ollama)
        model: Model name
        **kwargs: Additional provider-specific config

    Returns:
        AIClient instance

    Raises:
        ValueError: If provider is not supported
    """
    provider = provider.lower()

    if provider == "zai":
        if not api_key:
            api_key = os.environ.get("ZAI_API_KEY")
        if not api_key:
            raise ValueError("z.ai API key required. Set ZAI_API_KEY environment variable or pass api_key parameter.")
        model = model or "glm-4"
        return ZaiClient(api_key=api_key, model=model, **kwargs)

    elif provider == "openai":
        if not api_key:
            api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        model = model or "gpt-4"
        return OpenAIClient(api_key=api_key, model=model, **kwargs)

    elif provider == "anthropic":
        if not api_key:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Anthropic API key required. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter.")
        model = model or "claude-3-opus"
        return AnthropicClient(api_key=api_key, model=model, **kwargs)

    elif provider == "ollama":
        model = model or "llama2"
        return OllamaClient(model=model, **kwargs)

    else:
        raise ValueError(f"Unsupported provider: {provider}. Supported providers: zai, openai, anthropic, ollama")
