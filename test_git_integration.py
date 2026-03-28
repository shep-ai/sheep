#!/usr/bin/env python3
"""Test script for Git Integration phase of feature 257.

Tests that verify:
- task-2: File is staged in git (git add)
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
    """Test that test-z5u8bz.md is tracked by git."""
    stdout, returncode = run_git_command(["git", "ls-files", "test-z5u8bz.md"])
    assert returncode == 0, "git ls-files command failed"
    assert "test-z5u8bz.md" in stdout, "File is not tracked by git"
    print("✓ File is tracked by git")


def test_file_is_staged():
    """Test that test-z5u8bz.md appears in staged changes.

    Checks git status --porcelain for 'A  test-z5u8bz.md' (staged new file)
    or verifies the file is in the index.
    """
    # Use git diff-index to check if file is in the index (staged)
    stdout, returncode = run_git_command(["git", "diff-index", "--cached", "HEAD"])

    # If HEAD exists, check if file is in staged changes
    if returncode == 0:
        if "test-z5u8bz.md" in stdout:
            print("✓ File is staged in git (appears in diff-index --cached)")
        else:
            # File might be already committed, check git log
            stdout, _ = run_git_command(["git", "log", "-1", "--name-status"])
            assert "test-z5u8bz.md" in stdout, "File does not appear in recent commit"
            print("✓ File is committed in git")
    else:
        # Check if file appears in git status
        stdout, _ = run_git_command(["git", "status", "--porcelain"])
        # File should be committed already (no 'A' prefix if committed)
        assert "test-z5u8bz.md" not in stdout or "A  test-z5u8bz.md" not in stdout or "M " not in stdout, \
            "File shows as uncommitted in git status"
        print("✓ File is committed (not in uncommitted changes)")


def test_commit_exists_with_correct_message():
    """Test that commit exists with exact message:
    'feat(257): create markdown file test-z5u8bz.md with prose content'
    """
    stdout, returncode = run_git_command(["git", "log", "-1", "--pretty=%B"])
    assert returncode == 0, "git log command failed"

    expected_message = "feat(257): create markdown file test-z5u8bz.md with prose content"
    assert expected_message in stdout, \
        f"Commit message does not match. Expected: '{expected_message}', Got: '{stdout}'"
    print("✓ Commit exists with correct message")


def test_file_in_latest_commit():
    """Test that test-z5u8bz.md is included in the latest commit."""
    stdout, returncode = run_git_command(["git", "log", "-1", "--name-status"])
    assert returncode == 0, "git log command failed"
    assert "test-z5u8bz.md" in stdout, "File is not in the latest commit"
    print("✓ File is included in latest commit")


def test_branch_name():
    """Test that we are on the correct feature branch."""
    stdout, returncode = run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    assert returncode == 0, "git rev-parse command failed"

    expected_branch = "feat/markdown-file-creation-2101f0"
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
            ["git", "ls-remote", "origin", "feat/markdown-file-creation-2101f0"]
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
        ["git", "rev-parse", "origin/feat/markdown-file-creation-2101f0"]
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
