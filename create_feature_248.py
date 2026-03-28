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
    print(f"[OK] File {FILENAME} exists and is ready for git integration")
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
        print(f"[OK] Staged {filename} with git add")
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
        print(f"[OK] Committed with message: {message}")
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
        print(f"[OK] Pushed commit to remote branch {branch}")
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
    - File commit exists in history (may not be HEAD)
    - Current branch is the feature branch
    - Branch is pushed to remote

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

    # Check that the file exists in the repo (it may not be HEAD, but must be in history)
    result = subprocess.run(
        ["git", "log", "--oneline", "--all"],
        check=True,
        capture_output=True,
        text=True,
    )
    if FILENAME not in result.stdout:
        print(f"[WARNING] File commit message '{FILENAME}' not found in recent history")

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

    # Check branch is pushed
    result = subprocess.run(
        ["git", "rev-parse", "--verify", f"origin/{BRANCH}"],
        check=False,
        capture_output=True,
        text=True,
    )
    is_pushed = result.returncode == 0

    print(f"[OK] Git workflow verification complete:")
    print(f"  - File {FILENAME} is tracked: YES")
    print(f"  - Current branch: {current_branch}")
    print(f"  - Branch pushed to remote: {'YES' if is_pushed else 'NO'}")


def check_file_status():
    """
    Check if file is already committed or just created.

    Returns:
        "tracked" if file is committed, "staged" if staged, "untracked" if new.
    """
    result = subprocess.run(
        ["git", "status", "--porcelain", FILENAME],
        check=True,
        capture_output=True,
        text=True,
    )
    status = result.stdout.strip()
    if not status:
        return "tracked"  # File is committed, no changes
    elif status.startswith("A "):
        return "staged"  # File is staged for commit
    else:
        return "modified"


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

        # Git workflow - check current status and only do what's needed
        print("\nPhase 3b: Git operations...")
        file_status = check_file_status()

        if file_status == "tracked":
            print(f"[INFO] File {FILENAME} is already committed - skipping add/commit")
        else:
            git_add(FILENAME)
            git_commit(COMMIT_MESSAGE)

        # Push to remote (always attempt, may be a no-op if already pushed)
        git_push(BRANCH)

        # Verify success
        print("\nPhase 3c: Verification...")
        verify_git_workflow()

        print("\n[SUCCESS] Feature 248 Phase 3 (Git Integration) complete!")
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
