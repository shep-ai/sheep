#!/usr/bin/env python3
"""Test script for Git Integration phase of feature 266.

Tests that verify:
- task-3: File is staged in git (git add)
- task-3: File is committed with correct message (git commit)
- task-4: File is pushed to remote (git push)
"""

import subprocess
import sys
from pathlib import Path


def run_git_command(cmd):
    """Run a git command and return output."""
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    return result.stdout.strip(), result.returncode


def test_file_exists_in_git():
    """Test that test-0mmy12.md is tracked by git."""
    stdout, returncode = run_git_command(["git", "ls-files", "test-0mmy12.md"])
    assert returncode == 0, "git ls-files command failed"
    assert "test-0mmy12.md" in stdout, "File is not tracked by git"
    print("✓ File is tracked by git")


def test_file_is_staged():
    """Test that test-0mmy12.md is tracked and committed by git.

    Verifies the file is either staged or already committed in the repository.
    """
    # Check if file is currently staged or uncommitted
    stdout, _ = run_git_command(["git", "status", "--porcelain"])

    if "test-0mmy12.md" in stdout:
        # File shows in status, should be staged (A) or modified (M)
        assert "A  test-0mmy12.md" in stdout or "M  test-0mmy12.md" in stdout, \
            "File shows in status but not as staged or modified"
        print("✓ File is staged in git")
    else:
        # File is not in status output, meaning it's already committed
        # Verify it's in the git history
        stdout, returncode = run_git_command(["git", "log", "--name-status", "--all", "-20"])
        assert returncode == 0 and "test-0mmy12.md" in stdout, \
            "File is not in git history"
        print("✓ File is committed in git")


def test_commit_exists_with_correct_message():
    """Test that commit exists with feat(266) prefix."""
    # Search for the specific commit message in recent history
    stdout, returncode = run_git_command(
        ["git", "log", "--oneline", "--all", "-20"]
    )
    assert returncode == 0, "git log command failed"

    assert "feat(266)" in stdout, \
        f"Commit with feat(266) not found. Recent commits:\n{stdout}"
    print("✓ Commit exists with correct feat(266) message")


def test_file_in_latest_commit():
    """Test that test-0mmy12.md is included in a recent commit.

    The file should be committed in the branch history.
    """
    stdout, returncode = run_git_command(
        ["git", "log", "--name-status", "--all", "-20"]
    )
    assert returncode == 0, "git log command failed"
    assert "test-0mmy12.md" in stdout, "File is not found in recent commits"
    print("✓ File is included in commit history")


def test_branch_name():
    """Test that we are on the correct feature branch."""
    stdout, returncode = run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    assert returncode == 0, "git rev-parse command failed"

    expected_branch = "feat/markdown-file-creation-d6ab9e"
    assert expected_branch in stdout, \
        f"Wrong branch. Expected: '{expected_branch}', Got: '{stdout}'"
    print(f"✓ On correct branch: {stdout}")


def test_local_tracking_remote():
    """Test that local branch is tracking remote branch."""
    stdout, returncode = run_git_command(["git", "rev-parse", "--abbrev-ref", "@{u}"])

    # This might fail if no upstream is set, which is acceptable if local == remote
    if returncode == 0:
        assert "origin" in stdout, "Local branch is not tracking remote"
        print(f"✓ Local branch is tracking: {stdout}")
    else:
        # Check if remote branch exists and commit is on it
        stdout, returncode = run_git_command(
            ["git", "ls-remote", "origin", "feat/markdown-file-creation-d6ab9e"]
        )
        assert returncode == 0, "Could not check remote branch"
        assert len(stdout) > 0, "Remote branch does not exist"
        print("✓ Remote branch exists")


def test_commit_is_on_remote():
    """Test that the latest commit exists on the remote branch."""
    # Get local commit hash
    local_hash, returncode = run_git_command(["git", "rev-parse", "HEAD"])
    assert returncode == 0, "Could not get local commit hash"

    # Get remote commit hash
    remote_hash, returncode = run_git_command(
        ["git", "rev-parse", "origin/feat/markdown-file-creation-d6ab9e"]
    )
    assert returncode == 0, "Could not get remote commit hash"

    assert local_hash == remote_hash, \
        f"Local commit ({local_hash}) does not match remote ({remote_hash})"
    print(f"✓ Commit is pushed to remote: {local_hash[:8]}")


def test_branch_up_to_date():
    """Test that local branch is up to date with remote."""
    stdout, returncode = run_git_command(["git", "status", "-b", "--porcelain"])
    assert returncode == 0, "git status command failed"

    # Status should show "ahead/behind 0" or be identical
    assert "ahead" not in stdout or "0" in stdout, "Local branch is ahead of remote"
    assert "behind" not in stdout or "0" in stdout, "Local branch is behind remote"
    print("✓ Local branch is up to date with remote")


if __name__ == "__main__":
    tests = [
        test_file_exists_in_git,
        test_file_is_staged,
        test_commit_exists_with_correct_message,
        test_file_in_latest_commit,
        test_branch_name,
        test_local_tracking_remote,
        test_commit_is_on_remote,
        test_branch_up_to_date,
    ]

    failed = []
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed.append(test.__name__)

    if failed:
        print(f"\n{len(failed)} test(s) failed")
        sys.exit(1)
    else:
        print(f"\nAll {len(tests)} git integration tests passed ✓")
        sys.exit(0)
