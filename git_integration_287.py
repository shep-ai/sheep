#!/usr/bin/env python3
"""Git Integration implementation for feature 287.

Implements the git workflow:
1. Stage the markdown file with git add
2. Commit with conventional commit message
3. Push to the feature branch on remote origin
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True):
    """Execute a command and return the result.

    Args:
        cmd: List of command arguments
        check: If True, raise on non-zero exit code

    Returns:
        CompletedProcess result
    """
    result = subprocess.run(cmd, capture_output=True, text=True)

    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\n"
            f"Return code: {result.returncode}\n"
            f"Stderr: {result.stderr}"
        )

    return result


def stage_file():
    """Stage the markdown file using git add."""
    print("Staging test-hzqchm.md...")
    result = run_command(["git", "add", "test-hzqchm.md"], check=True)
    print("[OK] File staged successfully")
    return result


def commit_file():
    """Commit the staged file with conventional commit message."""
    commit_message = "feat(287): create markdown file test-hzqchm.md with title and prose content"
    print(f"Committing with message: {commit_message}")

    result = run_command(
        ["git", "commit", "-m", commit_message],
        check=False  # Don't raise if nothing to commit
    )

    if result.returncode == 0:
        print("[OK] File committed successfully")
    elif "nothing added to commit" in result.stdout or "nothing to commit" in result.stdout:
        print("[INFO] Nothing to commit (file already committed)")
    elif result.returncode != 0:
        # Handle other error cases
        raise RuntimeError(
            f"Commit failed with return code {result.returncode}\n"
            f"Stderr: {result.stderr}\n"
            f"Stdout: {result.stdout}"
        )
    else:
        print("[OK] File committed successfully")

    return result


def get_current_branch():
    """Get the current branch name."""
    result = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], check=True)
    return result.stdout.strip()


def push_to_remote():
    """Push the commit to the remote feature branch."""
    current_branch = get_current_branch()
    print(f"Pushing to remote: origin/{current_branch}")

    # Use -u to create upstream tracking if it doesn't exist
    result = run_command(
        ["git", "push", "-u", "origin", current_branch],
        check=True
    )

    print("[OK] Changes pushed to remote successfully")
    return result


def verify_commit():
    """Verify that the commit exists with the correct message."""
    result = run_command(["git", "log", "-1", "--pretty=%B"], check=True)
    commit_message = result.stdout.strip()

    expected = "feat(287): create markdown file test-hzqchm.md with title and prose content"
    if expected in commit_message:
        print(f"[OK] Commit message verified: {commit_message.split(chr(10))[0]}")
    else:
        raise RuntimeError(
            f"Commit message mismatch.\n"
            f"Expected substring: {expected}\n"
            f"Got: {commit_message}"
        )


def verify_file_in_git():
    """Verify that the file is tracked by git."""
    result = run_command(["git", "ls-files", "test-hzqchm.md"], check=True)
    if "test-hzqchm.md" in result.stdout:
        print("[OK] File is tracked by git")
    else:
        raise RuntimeError("File is not tracked by git")


def main():
    """Execute the complete git integration workflow."""
    try:
        print("=" * 60)
        print("Git Integration Workflow for Feature 287")
        print("=" * 60)

        # Verify file exists and is tracked
        verify_file_in_git()

        # Stage the file
        stage_file()

        # Commit the file
        commit_file()

        # Verify commit
        verify_commit()

        # Push to remote
        push_to_remote()

        print("\n" + "=" * 60)
        print("Git Integration Complete [OK]")
        print("=" * 60)
        return 0

    except Exception as e:
        print(f"\n[FAIL] Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
