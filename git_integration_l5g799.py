#!/usr/bin/env python3
"""
Git integration for feature 198: markdown file creation test-l5g799.md

Implements git workflow (add, commit, push) following Conventional Commits.
Uses subprocess.run() with list-based arguments for safe command execution.

Phase 4: Git Integration
- Stage file with git add
- Create commit with conventional message
- Push to feature branch
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional


class GitOperationError(Exception):
    """Raised when a git operation fails."""

    def __init__(self, operation: str, message: str, stderr: str = ""):
        """Initialize git operation error with context."""
        self.operation = operation
        self.message = message
        self.stderr = stderr
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Format error message with operation context."""
        msg = f"Git {self.operation} failed: {self.message}"
        if self.stderr:
            msg += f"\nStderr: {self.stderr}"
        return msg


def git_add_file(filename: str) -> None:
    """
    Stage a file with git add.

    Args:
        filename: Name of file to stage (e.g., 'test-l5g799.md')

    Raises:
        GitOperationError: If git add command fails
    """
    try:
        result = subprocess.run(
            ["git", "add", filename],
            check=True,
            capture_output=True,
            text=True,
        )
        # Success: file staged
    except subprocess.CalledProcessError as e:
        raise GitOperationError(
            operation="add",
            message=f"Failed to stage {filename}",
            stderr=e.stderr,
        )
    except FileNotFoundError:
        raise GitOperationError(
            operation="add",
            message="git command not found - ensure git is installed and in PATH",
        )


def git_commit(filename: str, feature_number: int = 198) -> None:
    """
    Create a commit with conventional commit message.

    Args:
        filename: Name of file being committed
        feature_number: Feature number for commit message (default: 198)

    Raises:
        GitOperationError: If git commit command fails
    """
    # Format: feat(NNN): Create markdown file <filename> with title and prose content
    commit_message = (
        f"feat({feature_number}): Create markdown file {filename} with title and prose content"
    )

    try:
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            check=True,
            capture_output=True,
            text=True,
        )
        # Success: file committed
    except subprocess.CalledProcessError as e:
        raise GitOperationError(
            operation="commit",
            message=f"Failed to commit {filename}",
            stderr=e.stderr,
        )
    except FileNotFoundError:
        raise GitOperationError(
            operation="commit",
            message="git command not found - ensure git is installed and in PATH",
        )


def git_push(branch: str) -> None:
    """
    Push commit to remote branch.

    Args:
        branch: Branch name to push to (e.g., 'feat/198-markdown-file-creation-903bd5')

    Raises:
        GitOperationError: If git push command fails
    """
    try:
        result = subprocess.run(
            ["git", "push", "origin", branch],
            check=True,
            capture_output=True,
            text=True,
        )
        # Success: pushed to remote
    except subprocess.CalledProcessError as e:
        raise GitOperationError(
            operation="push",
            message=f"Failed to push to branch {branch}",
            stderr=e.stderr,
        )
    except FileNotFoundError:
        raise GitOperationError(
            operation="push",
            message="git command not found - ensure git is installed and in PATH",
        )


def execute_git_workflow(
    filename: str = "test-l5g799.md",
    feature_number: int = 198,
    branch: str = "feat/markdown-file-creation-903bd5",
) -> None:
    """
    Execute complete git workflow: add, commit, push.

    Args:
        filename: File to stage and commit (default: 'test-l5g799.md')
        feature_number: Feature number for commit message (default: 198)
        branch: Branch to push to (default: 'feat/198-markdown-file-creation-903bd5')

    Raises:
        GitOperationError: If any git operation fails (with descriptive context)

    Side Effects:
        - Stages file with git add
        - Creates commit with conventional message
        - Pushes commit to remote branch
    """
    # Verify file exists before attempting git operations
    file_path = Path(filename)
    if not file_path.exists():
        raise GitOperationError(
            operation="add",
            message=f"File {filename} does not exist - cannot stage non-existent file",
        )

    # Stage file
    print(f"Staging file with 'git add {filename}'...")
    git_add_file(filename)
    print(f"[OK] File staged successfully")

    # Create commit with conventional message
    print(f"Committing with conventional message...")
    git_commit(filename, feature_number)
    print(f"[OK] File committed successfully")

    # Push to remote branch
    print(f"Pushing to remote branch '{branch}'...")
    git_push(branch)
    print(f"[OK] File pushed successfully")


def main() -> int:
    """Execute git integration workflow. Exit with code 0 on success, 1 on failure."""
    try:
        execute_git_workflow()
        print("\n[SUCCESS] Phase 4 (Git Integration) complete")
        return 0
    except GitOperationError as e:
        print(f"[FAILED] {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[FAILED] Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
