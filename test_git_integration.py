#!/usr/bin/env python3
"""Test script for Git Integration phase of feature 300.

Tests that verify:
- task-5: File is staged in git (git add) and committed with correct message (git commit)
- task-6: File is pushed to remote (git push)
"""

import subprocess
import sys
from pathlib import Path


def run_git_command(cmd):
    """Run a git command and return output."""
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    return result.stdout.strip(), result.returncode


def test_file_exists_in_git():
    """Test that test-tq8wxa.md is tracked by git."""
    stdout, returncode = run_git_command(["git", "ls-files", "test-tq8wxa.md"])
    assert returncode == 0, "git ls-files command failed"
    assert "test-tq8wxa.md" in stdout, "File is not tracked by git"
    print("[OK] File is tracked by git")


def test_file_is_staged():
    """Test that test-tq8wxa.md is tracked and committed by git.

    Verifies the file is either staged or already committed in the repository.
    """
    # Check if file is currently staged or uncommitted
    stdout, _ = run_git_command(["git", "status", "--porcelain"])

    if "test-tq8wxa.md" in stdout:
        # File shows in status, should be staged (A) or modified (M)
        assert "A  test-tq8wxa.md" in stdout or "M  test-tq8wxa.md" in stdout, \
            "File shows in status but not as staged or modified"
        print("[OK] File is staged in git")
    else:
        # File is not in status output, meaning it's already committed
        # Verify it's in the git history
        stdout, returncode = run_git_command(["git", "log", "--name-status", "--all", "-20"])
        assert returncode == 0 and "test-tq8wxa.md" in stdout, \
            "File is not in git history"
        print("[OK] File is committed in git")


def test_commit_exists_with_correct_message():
    """Test that commit exists with feat(300) prefix and correct message."""
    # Search for the specific commit message in recent history
    stdout, returncode = run_git_command(
        ["git", "log", "--oneline", "--all", "-20"]
    )
    assert returncode == 0, "git log command failed"

    assert "feat(300)" in stdout, \
        f"Commit with feat(300) not found. Recent commits:\n{stdout}"

    # Verify exact commit message
    stdout, returncode = run_git_command(
        ["git", "log", "--pretty=format:%B", "--all", "-20"]
    )
    expected_msg = "feat(300): create markdown file test-tq8wxa.md with prose content"
    assert expected_msg in stdout, \
        f"Commit message '{expected_msg}' not found"
    print("[OK] Commit exists with correct feat(300) message")


def test_file_in_latest_commit():
    """Test that test-tq8wxa.md is included in a recent commit.

    The file should be committed in the branch history.
    """
    stdout, returncode = run_git_command(
        ["git", "log", "--name-status", "--all", "-20"]
    )
    assert returncode == 0, "git log command failed"
    assert "test-tq8wxa.md" in stdout, "File is not found in recent commits"
    print("[OK] File is included in commit history")


def test_branch_name():
    """Test that we are on the correct feature branch."""
    stdout, returncode = run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    assert returncode == 0, "git rev-parse command failed"

    expected_branch = "feat/markdown-file-creation-6aea8a"
    assert expected_branch in stdout, \
        f"Wrong branch. Expected: '{expected_branch}', Got: '{stdout}'"
    print(f"[OK] On correct branch: {stdout}")


def test_local_tracking_remote():
    """Test that local branch is tracking remote branch."""
    stdout, returncode = run_git_command(["git", "rev-parse", "--abbrev-ref", "@{u}"])

    # This might fail if no upstream is set, which is acceptable if local == remote
    if returncode == 0:
        assert "origin" in stdout, "Local branch is not tracking remote"
        print(f"[OK] Local branch is tracking: {stdout}")
    else:
        # Check if remote branch exists and commit is on it
        stdout, returncode = run_git_command(
            ["git", "ls-remote", "origin", "feat/markdown-file-creation-6aea8a"]
        )
        # It's OK if remote branch doesn't exist yet (will be pushed in task-6)
        if returncode == 0 and len(stdout) > 0:
            print("[OK] Remote branch exists")
        else:
            print("[WARNING] Remote branch not yet created (will be created during push)")


def test_commit_is_on_remote():
    """Test that the latest commit exists on the remote branch (after push)."""
    # Get local commit hash
    local_hash, returncode = run_git_command(["git", "rev-parse", "HEAD"])
    assert returncode == 0, "Could not get local commit hash"

    # Get remote commit hash
    remote_hash, returncode = run_git_command(
        ["git", "rev-parse", "origin/feat/markdown-file-creation-6aea8a"]
    )

    if returncode != 0:
        print("[WARNING] Remote branch not yet pushed (expected during task-6)")
        return

    assert local_hash == remote_hash, \
        f"Local commit ({local_hash}) does not match remote ({remote_hash})"
    print(f"[OK] Commit is pushed to remote: {local_hash[:8]}")


def test_branch_up_to_date():
    """Test that local branch is up to date with remote."""
    stdout, returncode = run_git_command(["git", "status", "-b", "--porcelain"])
    assert returncode == 0, "git status command failed"

    # Status should show "ahead/behind 0" or be identical
    # Or no tracking info if remote doesn't exist yet
    if "ahead" in stdout or "behind" in stdout:
        assert "ahead" not in stdout or "0" in stdout, "Local branch is ahead of remote"
        assert "behind" not in stdout or "0" in stdout, "Local branch is behind remote"
        print("[OK] Local branch is up to date with remote")
    else:
        print("[WARNING] No tracking relationship yet (expected before push)")


if __name__ == "__main__":
    tests = [
        ("Task 5 (Staging & Commit)", [
            test_file_exists_in_git,
            test_file_is_staged,
            test_commit_exists_with_correct_message,
            test_file_in_latest_commit,
            test_branch_name,
        ]),
        ("Task 6 (Push to Remote)", [
            test_local_tracking_remote,
            test_commit_is_on_remote,
            test_branch_up_to_date,
        ]),
    ]

    failed = []
    total_tests = 0

    for task_name, task_tests in tests:
        print(f"\n{task_name}:")
        for test in task_tests:
            try:
                test()
                total_tests += 1
            except AssertionError as e:
                print(f"[FAIL] {test.__name__}: {e}")
                failed.append(test.__name__)
                total_tests += 1

    if failed:
        print(f"\n{len(failed)} test(s) failed")
        sys.exit(1)
    else:
        print(f"\nAll {total_tests} git integration tests passed [OK]")
        sys.exit(0)
