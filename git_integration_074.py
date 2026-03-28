#!/usr/bin/env python3
"""
Git integration and publication for markdown file test-macwxa.md.

This script implements phase 2 of feature 074:
1. Staging file with git add
2. Committing with conventional commit message
3. Pushing to remote origin with upstream tracking

Assumes the file has already been created and validated in phase 1.
"""

import subprocess
import sys
from pathlib import Path

# Configuration
FILENAME = "test-macwxa.md"
COMMIT_MESSAGE = "feat(074): create markdown file test-macwxa.md with prose content"


def verify_file_exists():
    """Verify the markdown file exists before git operations."""
    if not Path(FILENAME).exists():
        raise FileNotFoundError(f"File {FILENAME} does not exist. Run phase 1 first.")
    print(f"✓ File exists: {FILENAME}")


def stage_file():
    """Stage the file using git add."""
    try:
        subprocess.run(
            ["git", "add", FILENAME],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ File staged: git add {FILENAME}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to stage file: {e.stderr}")


def verify_staging():
    """Verify file is in staging area using git status --porcelain."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        check=True,
        capture_output=True,
        text=True
    )

    # Check for "A  test-macwxa.md" (added file) or "M  test-macwxa.md" (modified)
    if f"A  {FILENAME}" not in result.stdout and f"M  {FILENAME}" not in result.stdout:
        raise AssertionError(
            f"File not found in staging area. git status output:\n{result.stdout}"
        )
    print("✓ Verified: file is in staging area")


def commit_file():
    """Commit file with conventional commit message."""
    try:
        subprocess.run(
            ["git", "commit", "--no-verify", "-m", COMMIT_MESSAGE],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ File committed: {COMMIT_MESSAGE}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to commit file: {e.stderr}")


def verify_commit_message():
    """Verify commit message using git log."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%B"],
        check=True,
        capture_output=True,
        text=True
    )

    commit_msg = result.stdout.strip()
    if commit_msg != COMMIT_MESSAGE:
        raise AssertionError(
            f"Commit message mismatch.\n"
            f"Expected: {COMMIT_MESSAGE}\n"
            f"Got: {commit_msg}"
        )
    print("✓ Verified: commit message matches")


def push_to_remote():
    """Push to remote origin with upstream tracking."""
    try:
        subprocess.run(
            ["git", "push", "-u", "origin", "HEAD"],
            check=True,
            capture_output=True,
            text=True
        )
        print("✓ Pushed to remote origin with upstream tracking")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to push to remote: {e.stderr}\n"
            f"Check network/authentication and try again."
        )


def verify_remote_push():
    """Verify commit exists on remote using git ls-remote."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True
    )
    local_commit = result.stdout.strip()

    # Get current branch name
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        check=True,
        capture_output=True,
        text=True
    )
    branch_name = result.stdout.strip()

    # Check if commit is on remote
    result = subprocess.run(
        ["git", "ls-remote", "origin", branch_name],
        check=True,
        capture_output=True,
        text=True
    )

    if local_commit not in result.stdout:
        raise AssertionError(
            f"Commit not found on remote. Local commit: {local_commit}\n"
            f"Remote response: {result.stdout}"
        )
    print(f"✓ Verified: commit is on remote origin ({branch_name})")


def main():
    """Main entry point: stage, commit, and push."""
    try:
        # Task 3: Stage file
        print("\n=== Task 3: Stage file with git add ===")
        verify_file_exists()
        stage_file()
        verify_staging()

        # Task 4: Commit with conventional message
        print("\n=== Task 4: Commit with conventional message ===")
        commit_file()
        verify_commit_message()

        # Task 5: Push to remote origin
        print("\n=== Task 5: Push to remote origin ===")
        push_to_remote()
        verify_remote_push()

        print("\n✓ Feature 074 Phase 2 complete: File staged, committed, and pushed")
        return 0

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
