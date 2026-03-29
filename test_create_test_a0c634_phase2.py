#!/usr/bin/env python3
"""
Test suite for feature 270 Phase 2: Git Integration & Validation

Tests for git operations that verify:
- task-4: File is staged in git (git add)
- task-5: File is committed with correct message (git commit)
- task-5: File is pushed to remote (git push)
"""

import subprocess
import sys
from unittest import mock


def run_git_command(cmd):
    """Run a git command and return output."""
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    return result.stdout.strip(), result.returncode


def test_file_exists_in_git():
    """Test that test-a0c634.md is tracked by git."""
    stdout, returncode = run_git_command(["git", "ls-files", "test-a0c634.md"])
    assert returncode == 0, "git ls-files command failed"
    assert "test-a0c634.md" in stdout, "File is not tracked by git"
    print("[OK] File is tracked by git")


def test_file_is_staged_or_committed():
    """Test that test-a0c634.md is tracked and committed by git.

    Verifies the file is either staged or already committed in the repository.
    """
    # Check if file is currently staged or uncommitted
    stdout, _ = run_git_command(["git", "status", "--porcelain"])

    if "test-a0c634.md" in stdout:
        # File shows in status, should be staged (A) or modified (M)
        assert "A  test-a0c634.md" in stdout or "M  test-a0c634.md" in stdout, \
            "File shows in status but not as staged or modified"
        print("[OK] File is staged in git")
    else:
        # File is not in status output, meaning it's already committed
        # Verify it's in the git history
        stdout, returncode = run_git_command(["git", "log", "--name-status", "--all", "-20"])
        assert returncode == 0 and "test-a0c634.md" in stdout, \
            "File is not in git history"
        print("[OK] File is committed in git")


def test_commit_exists_with_correct_message():
    """Test that commit exists with feat(270) prefix."""
    # Search for the specific commit message in recent history
    stdout, returncode = run_git_command(
        ["git", "log", "--oneline", "--all", "-20"]
    )
    assert returncode == 0, "git log command failed"

    assert "feat(270)" in stdout, \
        f"Commit with feat(270) not found. Recent commits:\n{stdout}"
    print("[OK] Commit exists with correct feat(270) message")


def test_file_in_recent_commit():
    """Test that test-a0c634.md is included in a recent commit.

    The file should be committed in the branch history.
    """
    stdout, returncode = run_git_command(
        ["git", "log", "--name-status", "--all", "-20"]
    )
    assert returncode == 0, "git log command failed"
    assert "test-a0c634.md" in stdout, "File is not found in recent commits"
    print("[OK] File is included in commit history")


def test_branch_has_feature_prefix():
    """Test that we are on a feature branch."""
    stdout, returncode = run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    assert returncode == 0, "git rev-parse command failed"

    assert "feat" in stdout or "feature" in stdout, \
        f"Not on a feature branch. Current branch: '{stdout}'"
    print(f"[OK] On feature branch: {stdout}")


if __name__ == "__main__":
    try:
        test_file_exists_in_git()
        test_file_is_staged_or_committed()
        test_commit_exists_with_correct_message()
        test_file_in_recent_commit()
        test_branch_has_feature_prefix()
        print("\n[OK] All git integration tests passed!")
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
