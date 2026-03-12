"""
NLP Module for Zeal Code
Provides AI-powered natural language processing with BYOK support.

Priority: z.ai (GLM) > OpenAI > Anthropic > Ollama
"""

from .ai_client import AIClient, create_ai_client
from .pattern_matcher import PatternMatcher

__all__ = ['AIClient', 'create_ai_client', 'PatternMatcher']
