"""
Workspace Management for Zeal Code
Handles workspace directory, file operations, and context
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
import fnmatch


class Workspace:
    """Workspace manager for Zeal Code"""

    def __init__(self, workspace_path: Optional[Path] = None):
        """
        Initialize workspace manager

        Args:
            workspace_path: Path to workspace (default: current directory)
        """
        self.workspace_path = Path(workspace_path or os.getcwd()).resolve()

        if not self.workspace_path.exists():
            raise ValueError(f"Workspace path does not exist: {self.workspace_path}")

        if not self.workspace_path.is_dir():
            raise ValueError(f"Workspace path is not a directory: {self.workspace_path}")

    @property
    def path(self) -> Path:
        """Get workspace path"""
        return self.workspace_path

    @property
    def name(self) -> str:
        """Get workspace name"""
        return self.workspace_path.name

    def cd(self, path: str) -> Path:
        """
        Change to directory in workspace

        Args:
            path: Relative or absolute path

        Returns:
            New workspace path
        """
        new_path = (self.workspace_path / path).resolve()

        if not new_path.exists():
            raise ValueError(f"Path does not exist: {new_path}")

        if not new_path.is_dir():
            raise ValueError(f"Path is not a directory: {new_path}")

        self.workspace_path = new_path
        return self.workspace_path

    def pwd(self) -> str:
        """
        Get current working directory

        Returns:
            Absolute path string
        """
        return str(self.workspace_path)

    def ls(self, path: str = "", show_hidden: bool = False) -> List[Dict[str, Any]]:
        """
        List files in directory

        Args:
            path: Relative path within workspace
            show_hidden: Include hidden files

        Returns:
            List of file info dicts
        """
        target_path = self.workspace_path / path if path else self.workspace_path

        if not target_path.exists():
            raise ValueError(f"Path does not exist: {target_path}")

        if not target_path.is_dir():
            raise ValueError(f"Path is not a directory: {target_path}")

        files = []
        for item in target_path.iterdir():
            # Skip hidden files unless requested
            if not show_hidden and item.name.startswith('.'):
                continue

            # Get file info
            stat = item.stat()
            files.append({
                "name": item.name,
                "path": str(item),
                "relative_path": str(item.relative_to(self.workspace_path)),
                "is_dir": item.is_dir(),
                "size": stat.st_size,
                "modified": stat.st_mtime
            })

        # Sort: directories first, then by name
        files.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))

        return files

    def read(self, file_path: str, max_lines: Optional[int] = None) -> List[str]:
        """
        Read file contents

        Args:
            file_path: Relative or absolute file path
            max_lines: Maximum lines to read (None for all)

        Returns:
            List of lines
        """
        target_path = self.workspace_path / file_path if not Path(file_path).is_absolute() else Path(file_path)

        if not target_path.exists():
            raise FileNotFoundError(f"File not found: {target_path}")

        if not target_path.is_file():
            raise ValueError(f"Path is not a file: {target_path}")

        try:
            with open(target_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                # Limit lines if requested
                if max_lines:
                    lines = lines[:max_lines]

                # Remove trailing newlines
                lines = [line.rstrip('\n') for line in lines]

                return lines
        except UnicodeDecodeError:
            raise ValueError(f"File is not text: {target_path}")

    def write(self, file_path: str, content: str, create_dirs: bool = True) -> Path:
        """
        Write content to file

        Args:
            file_path: Relative or absolute file path
            content: Content to write
            create_dirs: Create parent directories if they don't exist

        Returns:
            Path to written file
        """
        target_path = self.workspace_path / file_path if not Path(file_path).is_absolute() else Path(file_path)

        # Create parent directories
        if create_dirs:
            target_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return target_path

    def exists(self, path: str) -> bool:
        """
        Check if path exists in workspace

        Args:
            path: Relative or absolute path

        Returns:
            True if path exists
        """
        target_path = self.workspace_path / path if not Path(path).is_absolute() else Path(path)
        return target_path.exists()

    def is_file(self, path: str) -> bool:
        """
        Check if path is a file

        Args:
            path: Relative or absolute path

        Returns:
            True if path is a file
        """
        target_path = self.workspace_path / path if not Path(path).is_absolute() else Path(path)
        return target_path.is_file() if target_path.exists() else False

    def is_dir(self, path: str) -> bool:
        """
        Check if path is a directory

        Args:
            path: Relative or absolute path

        Returns:
            True if path is a directory
        """
        target_path = self.workspace_path / path if not Path(path).is_absolute() else Path(path)
        return target_path.is_dir() if target_path.exists() else False

    def search(self, term: str, path: str = "", extensions: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search for text in files

        Args:
            term: Search term (supports regex)
            path: Relative path to search in
            extensions: File extensions to search (None for all)

        Returns:
            List of matches with context
        """
        import re

        target_path = self.workspace_path / path if path else self.workspace_path

        if not target_path.exists():
            raise ValueError(f"Path does not exist: {target_path}")

        if not target_path.is_dir():
            raise ValueError(f"Path is not a directory: {target_path}")

        matches = []

        # Search in files
        for file_path in self._find_files(target_path, extensions):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        # Check for match (case-insensitive)
                        if re.search(term, line, re.IGNORECASE):
                            matches.append({
                                "file": str(file_path.relative_to(self.workspace_path)),
                                "line": line_num,
                                "text": line.strip(),
                                "match": term
                            })
            except (UnicodeDecodeError, PermissionError):
                # Skip binary files or files we can't read
                continue

        return matches

    def _find_files(self, path: Path, extensions: Optional[List[str]]) -> List[Path]:
        """
        Find files matching extensions

        Args:
            path: Path to search
            extensions: File extensions to match (e.g., [".py", ".js"])

        Returns:
            List of file paths
        """
        files = []

        for item in path.rglob("*"):
            if item.is_file():
                # Check extension if specified
                if extensions:
                    if item.suffix.lower() not in extensions:
                        continue
                files.append(item)

        return files

    def get_info(self) -> Dict[str, Any]:
        """
        Get workspace information

        Returns:
            Dict with workspace info
        """
        # Count files and directories
        file_count = 0
        dir_count = 0

        for item in self.workspace_path.iterdir():
            if item.is_file():
                file_count += 1
            elif item.is_dir():
                dir_count += 1

        return {
            "path": str(self.workspace_path),
            "name": self.name,
            "file_count": file_count,
            "dir_count": dir_count,
            "total_files": self._count_all_files(self.workspace_path),
            "is_git_repo": (self.workspace_path / ".git").exists()
        }

    def _count_all_files(self, path: Path) -> int:
        """Count all files in directory recursively"""
        count = 0
        for item in path.rglob("*"):
            if item.is_file():
                count += 1
        return count

    def __repr__(self) -> str:
        """String representation"""
        return f"Workspace(path={self.workspace_path}, name={self.name})"


def init_workspace(workspace_path: Optional[Path] = None) -> Workspace:
    """
    Initialize workspace

    Args:
        workspace_path: Path to workspace (default: current directory)

    Returns:
        Workspace instance
    """
    return Workspace(workspace_path=workspace_path)
