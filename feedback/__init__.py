"""
Claude Code Alternative - User Feedback Module (Phase 4)
Collect, manage, and analyze user feedback
"""

from .user_feedback import (
    FeedbackManager,
    Feedback,
    FeedbackType,
    FeedbackStatus,
    FeedbackPriority
)

__all__ = [
    'FeedbackManager',
    'Feedback',
    'FeedbackType',
    'FeedbackStatus',
    'FeedbackPriority'
]
