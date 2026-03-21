#!/usr/bin/env python3
"""Git integration module for feature 137: markdown file test-narzc3.md.

Implements phase 3 of the feature:
1. Staging file with git add
2. Committing with conventional commit message
3. Pushing to remote origin with upstream tracking

Uses subprocess.run() with check=True for strict error handling.
Raises subprocess.CalledProcessError if any git command fails.
"""

import subprocess
import sys
from pathlib import Path


class GitIntegrationError(Exception):
    """Raised when git integration operations fail."""

    pass


def stage_file(filepath: str) -> None:
    """Stage file using git add.

    Args:
        filepath: Path to the file to stage (e.g., "test-narzc3.md").

    Raises:
        RuntimeError: If git add fails.
    """
    try:
        subprocess.run(
            ["git", "add", filepath],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to stage file {filepath}: {e.stderr or e.stdout}"
        ) from e


def commit_file(filepath: str, commit_message: str) -> None:
    """Commit file with conventional commit message.

    Args:
        filepath: Path to the file being committed (for reference).
        commit_message: Conventional commit message (e.g., "feat(137): Create markdown file test-narzc3.md").

    Raises:
        RuntimeError: If git commit fails.
    """
    try:
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to commit file {filepath}: {e.stderr or e.stdout}"
        ) from e


def push_file(branch_name: str) -> None:
    """Push to remote origin with upstream tracking.

    Args:
        branch_name: Name of the feature branch (e.g., "feat/markdown-file-creation-646f97").

    Raises:
        RuntimeError: If git push fails.
    """
    try:
        subprocess.run(
            ["git", "push", "-u", "origin", branch_name],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to push to remote origin: {e.stderr or e.stdout}"
        ) from e


def integrate_git(
    filepath: str, branch_name: str, commit_message: str
) -> None:
    """Orchestrate complete git integration: stage, commit, push.

    Calls stage_file(), commit_file(), and push_file() in sequence.
    If any operation fails, raises the exception immediately.

    Args:
        filepath: Path to the file to integrate (e.g., "test-narzc3.md").
        branch_name: Feature branch name (e.g., "feat/markdown-file-creation-646f97").
        commit_message: Conventional commit message (e.g., "feat(137): Create markdown file test-narzc3.md").

    Raises:
        RuntimeError: If any git operation fails.
    """
    stage_file(filepath)
    commit_file(filepath, commit_message)
    push_file(branch_name)


def main() -> int:
    """Main entry point for git integration.

    Returns:
        0 on success, 1 on any error.
    """
    try:
        filename = "test-narzc3.md"
        branch = "feat/markdown-file-creation-646f97"
        message = "feat(137): Create markdown file test-narzc3.md"

        print("\n=== Phase 3: Git Integration & Push ===\n")

        print(f"Staging file: {filename}")
        stage_file(filename)
        print(f"[OK] File staged with git add\n")

        print(f"Committing with message: {message}")
        commit_file(filename, message)
        print(f"[OK] File committed\n")

        print(f"Pushing to origin ({branch})")
        push_file(branch)
        print(f"[OK] Changes pushed to remote origin\n")

        print("[OK] Phase 3 complete: File staged, committed, and pushed")
        return 0

    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
