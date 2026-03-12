"""
Pattern Matcher - Fallback NLP for when AI is unavailable
Uses regex and keyword matching to understand natural language commands
"""

import re
from typing import Dict, List, Tuple, Optional
from enum import Enum


class Intent(Enum):
    """Command intents"""
    READ = "read"
    LIST = "list"
    SEARCH = "search"
    WRITE = "write"
    CREATE = "create"
    DELETE = "delete"
    EXIT = "exit"
    HELP = "help"
    UNKNOWN = "unknown"


class PatternMatcher:
    """Pattern-based NLP for fallback mode"""

    def __init__(self):
        # Intent patterns (keyword -> intent)
        self.intent_patterns = {
            # Read patterns
            Intent.READ: [
                r"show.*me",
                r"what'?s.*in",
                r"read.*file",
                r"display",
                r"view",
                r"open",
                r"cat"
            ],
            # List patterns
            Intent.LIST: [
                r"list",
                r"show.*files",
                r"what.*files",
                r"ls",
                r"dir"
            ],
            # Search patterns
            Intent.SEARCH: [
                r"search",
                r"find",
                r"look for",
                r"where.*is",
                r"grep"
            ],
            # Write patterns
            Intent.WRITE: [
                r"write",
                r"save",
                r"output"
            ],
            # Create patterns
            Intent.CREATE: [
                r"create",
                r"make",
                r"new.*file",
                r"add.*file",
                r"generate"
            ],
            # Delete patterns
            Intent.DELETE: [
                r"delete",
                r"remove",
                r"rm"
            ],
            # Exit patterns
            Intent.EXIT: [
                r"exit",
                r"quit",
                r"bye",
                r"stop"
            ],
            # Help patterns
            Intent.HELP: [
                r"help",
                r"how.*do",
                r"what.*can",
                r"commands"
            ]
        }

        # File path patterns
        self.file_patterns = [
            r'[a-zA-Z0-9_/\\\-]+\.(py|js|ts|java|go|rb|php|html|css|json|yaml|yml|md|txt|sql)',
            r'[a-zA-Z0-9_/\\\-]+/',  # Directory path
            r'["\']([^"\']+)["\']',  # Quoted paths
        ]

        # Search term patterns
        self.search_patterns = [
            r'"([^"]+)"',  # Quoted search term
            r"for\s+(.+?)(?:\s+in|\s*$)",  # "search for X in ..."
            r"find\s+(.+?)(?:\s+in|\s*$)",  # "find X in ..."
            r"search\s+(.+?)(?:\s+in|\s*$)",  # "search X in ..."
        ]

    def detect_intent(self, command: str) -> Intent:
        """
        Detect the intent of a natural language command

        Args:
            command: User's natural language command

        Returns:
            Detected Intent
        """
        command = command.lower().strip()

        # Check each intent pattern
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, command, re.IGNORECASE):
                    return intent

        return Intent.UNKNOWN

    def extract_file_path(self, command: str) -> Optional[str]:
        """
        Extract file path from command

        Args:
            command: User's command

        Returns:
            File path or None
        """
        for pattern in self.file_patterns:
            match = re.search(pattern, command)
            if match:
                path = match.group(0).strip('"\'')
                # Clean up path
                path = path.replace('\\', '/')
                return path
        return None

    def extract_search_term(self, command: str) -> Optional[str]:
        """
        Extract search term from command

        Args:
            command: User's command

        Returns:
            Search term or None
        """
        for pattern in self.search_patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                term = match.group(1).strip('"\'')
                return term
        return None

    def extract_directory(self, command: str) -> Optional[str]:
        """
        Extract directory path from command

        Args:
            command: User's command

        Returns:
            Directory path or None
        """
        # Look for "in X directory" or similar patterns
        patterns = [
            r"in\s+(.+?)\s+direct",
            r"in\s+(.+?)\s*$",
            r"directory\s+(.+?)\s*$"
        ]

        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                dir_path = match.group(1).strip('"\'')
                return dir_path

        # Try to extract any path-like string
        return self.extract_file_path(command)

    def extract_content(self, command: str) -> Optional[str]:
        """
        Extract content for file creation

        Args:
            command: User's command

        Returns:
            Content string or None
        """
        # Look for content after "write file: content" or similar
        patterns = [
            r":\s*(.+?)(?:\s*$)",  # "write file.py: content"
            r"with\s+(.+?)(?:\s*$)",  # "write file with content"
            r"content\s*[:=]\s*(.+?)(?:\s*$)",  # "content: ..."
        ]

        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                content = match.group(1).strip('"\'')
                return content
        return None

    def parse_command(self, command: str) -> Dict[str, any]:
        """
        Parse a natural language command into structured data

        Args:
            command: User's command

        Returns:
            Dict with keys: intent, file_path, search_term, directory, content
        """
        return {
            "intent": self.detect_intent(command),
            "file_path": self.extract_file_path(command),
            "search_term": self.extract_search_term(command),
            "directory": self.extract_directory(command),
            "content": self.extract_content(command),
            "raw_command": command
        }

    def get_command_suggestion(self, command: str) -> str:
        """
        Get a CLI command suggestion for the natural language command

        Args:
            command: User's command

        Returns:
            Suggested CLI command
        """
        parsed = self.parse_command(command)
        intent = parsed["intent"]

        if intent == Intent.READ:
            file_path = parsed["file_path"] or "[file]"
            return f"read {file_path}"

        elif intent == Intent.LIST:
            directory = parsed["directory"] or ""
            return f"list {directory}"

        elif intent == Intent.SEARCH:
            term = parsed["search_term"] or "[search_term]"
            directory = parsed["directory"] or ""
            if directory:
                return f"search {term} in {directory}"
            return f"search {term}"

        elif intent == Intent.WRITE or intent == Intent.CREATE:
            file_path = parsed["file_path"] or "[file]"
            return f"write {file_path}"

        elif intent == Intent.DELETE:
            file_path = parsed["file_path"] or "[file]"
            return f"delete {file_path}"

        elif intent == Intent.HELP:
            return "help"

        elif intent == Intent.EXIT:
            return "exit"

        else:
            return f"# Unknown command: {command}"
