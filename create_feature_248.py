#!/usr/bin/env python3
"""
Implementation script for feature 248: markdown-file-creation-87cda7
Phase 3: Git Integration

This script implements the git workflow for the markdown file test-0c8bhn.md:
1. Stage the file with git add
2. Commit with conventional commit message
3. Push to feature branch

The markdown file was created in previous phases and is ready for git integration.
"""

import subprocess
import sys
from pathlib import Path

# Constants
FILENAME = "test-0c8bhn.md"
COMMIT_MESSAGE = "feat(248): create markdown file test-0c8bhn.md with prose content"
BRANCH = "feat/markdown-file-creation-87cda7"


def verify_file_exists():
    """
    Verify the markdown file exists before git operations.

    Returns:
        Path object to the file if it exists.

    Raises:
        FileNotFoundError: If file does not exist.
    """
    file_path = Path(FILENAME)
    if not file_path.exists():
        raise FileNotFoundError(f"File {FILENAME} does not exist. Was it created in Phase 1?")
    if not file_path.is_file():
        raise ValueError(f"{FILENAME} exists but is not a file (may be a directory)")
    print(f"✓ File {FILENAME} exists and is ready for git integration")
    return file_path


def git_add(filename):
    """
    Stage the markdown file with git add.

    Executes: git add <filename>

    Args:
        filename: Name of the file to stage.

    Raises:
        subprocess.CalledProcessError: If git add fails.
    """
    try:
        result = subprocess.run(
            ["git", "add", filename],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"✓ Staged {filename} with git add")
    except subprocess.CalledProcessError as e:
        error_msg = f"git add failed with exit code {e.returncode}"
        if e.stderr:
            error_msg += f": {e.stderr}"
        print(error_msg, file=sys.stderr)
        raise


def git_commit(message):
    """
    Commit the staged file with a conventional commit message.

    Executes: git commit -m "<message>"

    Args:
        message: Conventional commit message.

    Raises:
        subprocess.CalledProcessError: If git commit fails.
    """
    try:
        result = subprocess.run(
            ["git", "commit", "-m", message],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"✓ Committed with message: {message}")
    except subprocess.CalledProcessError as e:
        error_msg = f"git commit failed with exit code {e.returncode}"
        if e.stderr:
            error_msg += f": {e.stderr}"
        print(error_msg, file=sys.stderr)
        raise


def git_push(branch):
    """
    Push the commit to the remote feature branch.

    Executes: git push origin <branch>

    Args:
        branch: Name of the feature branch to push to.

    Raises:
        subprocess.CalledProcessError: If git push fails.
    """
    try:
        result = subprocess.run(
            ["git", "push", "origin", branch],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"✓ Pushed commit to remote branch {branch}")
    except subprocess.CalledProcessError as e:
        error_msg = f"git push failed with exit code {e.returncode}"
        if e.stderr:
            error_msg += f": {e.stderr}"
        print(error_msg, file=sys.stderr)
        raise


def verify_git_workflow():
    """
    Verify that git operations completed successfully.

    Checks:
    - File is tracked by git (git ls-files)
    - Commit exists with correct message (git log)
    - Current branch is the feature branch

    Raises:
        RuntimeError: If verification fails.
    """
    # Check file is tracked
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        text=True,
    )
    if FILENAME not in result.stdout:
        raise RuntimeError(f"File {FILENAME} is not tracked by git")

    # Check commit message
    result = subprocess.run(
        ["git", "log", "-1", "--format=%s"],
        check=True,
        capture_output=True,
        text=True,
    )
    commit_msg = result.stdout.strip()
    if commit_msg != COMMIT_MESSAGE:
        raise RuntimeError(
            f"Commit message mismatch. Expected '{COMMIT_MESSAGE}', got '{commit_msg}'"
        )

    # Check current branch
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    current_branch = result.stdout.strip()
    if current_branch != BRANCH:
        raise RuntimeError(
            f"Not on feature branch. Expected {BRANCH}, on {current_branch}"
        )

    print(f"✓ Git workflow verification complete:")
    print(f"  - File {FILENAME} is tracked")
    print(f"  - Commit message: {commit_msg}")
    print(f"  - Branch: {current_branch}")


def main():
    """
    Main orchestration: verify file, add, commit, push, verify success.

    Raises:
        FileNotFoundError: If file does not exist.
        subprocess.CalledProcessError: If any git operation fails.
        RuntimeError: If verification fails.
    """
    try:
        print("Starting feature 248 Phase 3: Git Integration...\n")

        # Verify file exists
        print("Phase 3a: File verification...")
        verify_file_exists()

        # Git workflow
        print("\nPhase 3b: Git operations...")
        git_add(FILENAME)
        git_commit(COMMIT_MESSAGE)
        git_push(BRANCH)

        # Verify success
        print("\nPhase 3c: Verification...")
        verify_git_workflow()

        print("\n✓ Feature 248 Phase 3 (Git Integration) complete!")
    except Exception as e:
        print(f"\n✗ Failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
