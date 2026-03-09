"""
Claude Code Alternative - Security Module (Phase 3)
Security implementation with authentication and encryption
"""

from .auth import AuthenticationManager, User
from .encryption import EncryptionManager, SecureDataStore

__all__ = [
    'AuthenticationManager',
    'User',
    'EncryptionManager',
    'SecureDataStore'
]
