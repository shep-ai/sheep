#!/usr/bin/env python3
"""
Git Repository State Validation for feature 126, Phase 1, Task 1-1.

This module provides validation functions to ensure the git repository is ready
for markdown file creation:
- Git is initialized
- Current branch is feat/126-markdown-file-create-cea132
- Working tree is clean (no uncommitted changes)
- Git user.name and user.email are configured
"""

import subprocess
import sys


def validate_git_state():
    """
    Validate that the git repository is ready for feature implementation.

    Returns:
        True if all validations pass.

    Raises:
        ValueError: If any validation check fails with a descriptive error message.
    """
    try:
        _check_git_initialized()
        _check_current_branch()
        _check_working_tree_clean()
        _check_git_user_configured()
        return True
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Git command failed: {e.stderr}") from e


def _check_git_initialized():
    """Check that git is initialized in the current directory."""
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise ValueError("Git is not initialized in the current directory")


def _check_current_branch():
    """Check that current branch is feat/126-markdown-file-create-cea132."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True
    )
    current_branch = result.stdout.strip()
    expected_branch = "feat/markdown-file-create-cea132"
    if current_branch != expected_branch:
        raise ValueError(
            f"Expected branch '{expected_branch}', but currently on '{current_branch}'"
        )


def _check_working_tree_clean():
    """Check that working tree is clean (no uncommitted changes)."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True
    )
    status_output = result.stdout.strip()

    # Filter out untracked files (lines starting with "??")
    # We only care about modified, staged, deleted files, etc.
    tracked_changes = [
        line for line in status_output.split("\n")
        if line and not line.startswith("??")
    ]

    if tracked_changes:
        changes_str = "\n".join(tracked_changes)
        raise ValueError(
            f"Working tree is dirty (has uncommitted changes):\n{changes_str}"
        )


def _check_git_user_configured():
    """Check that git user.name and user.email are configured."""
    # Check user.name
    result_name = subprocess.run(
        ["git", "config", "user.name"],
        capture_output=True,
        text=True
    )
    user_name = result_name.stdout.strip()
    if not user_name:
        raise ValueError("Git user.name is not configured")

    # Check user.email
    result_email = subprocess.run(
        ["git", "config", "user.email"],
        capture_output=True,
        text=True
    )
    user_email = result_email.stdout.strip()
    if not user_email:
        raise ValueError("Git user.email is not configured")


def main():
    """Main entry point for git validation."""
    try:
        validate_git_state()
        print("[OK] Git repository state is valid:")
        print("  - Git is initialized")
        print("  - Current branch is feat/markdown-file-create-cea132")
        print("  - Working tree is clean")
        print("  - Git user is configured")
        return 0
    except ValueError as e:
        print(f"[ERROR] Git validation failed: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
