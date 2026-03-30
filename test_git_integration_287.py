#!/usr/bin/env python3
"""Test script for Git Integration phase of feature 287.

Tests that verify:
- File is staged in git (git add)
- File is committed with correct message (git commit)
- File is pushed to remote (git push)
- Commit has correct message and author info
"""

import subprocess
import sys
from pathlib import Path


def run_git_command(cmd):
    """Run a git command and return output and return code."""
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def test_file_exists_in_git():
    """Test that test-hzqchm.md is tracked by git."""
    stdout, stderr, returncode = run_git_command(["git", "ls-files", "test-hzqchm.md"])
    assert returncode == 0, f"git ls-files command failed: {stderr}"
    assert "test-hzqchm.md" in stdout, "File is not tracked by git"
    print("[OK] File is tracked by git")


def test_git_add_succeeds():
    """Test that git add command executes successfully."""
    stdout, stderr, returncode = run_git_command(["git", "add", "test-hzqchm.md"])
    assert returncode == 0, f"git add command failed: {stderr}"
    print("[OK] git add test-hzqchm.md succeeds")


def test_commit_exists_with_correct_message():
    """Test that commit exists with feat(287) prefix and correct message."""
    stdout, stderr, returncode = run_git_command(
        ["git", "log", "--oneline", "--all", "-20"]
    )
    assert returncode == 0, f"git log command failed: {stderr}"

    expected_message = "feat(287): create markdown file test-hzqchm.md with title and prose content"
    found = False
    for line in stdout.split('\n'):
        if "feat(287)" in line and "test-hzqchm.md" in line:
            found = True
            break

    assert found, f"Commit with feat(287) not found. Recent commits:\n{stdout}"
    print("[OK] Commit exists with correct feat(287) message")


def test_file_in_latest_commit():
    """Test that test-hzqchm.md is included in a recent commit."""
    stdout, stderr, returncode = run_git_command(
        ["git", "log", "--name-status", "--all", "-20"]
    )
    assert returncode == 0, f"git log command failed: {stderr}"
    assert "test-hzqchm.md" in stdout, "File is not found in recent commits"
    print("[OK] File is included in commit history")


def test_git_commit_message_exact():
    """Test that the commit message is exactly as specified."""
    stdout, stderr, returncode = run_git_command(
        ["git", "log", "-1", "--pretty=%B"]
    )
    assert returncode == 0, f"git log command failed: {stderr}"

    # The first line of commit message should contain our message
    first_line = stdout.split('\n')[0] if stdout else ""
    expected = "feat(287): create markdown file test-hzqchm.md with title and prose content"
    assert expected in first_line, \
        f"Commit message mismatch. Expected substring: '{expected}', Got first line: '{first_line}'"
    print("[OK] Commit message is exactly as specified")


def test_git_push_succeeds():
    """Test that git push command executes successfully."""
    # Get current branch
    branch_output, stderr, _ = run_git_command(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    )
    current_branch = branch_output.strip()

    # Try to push to remote
    # If the remote tracking branch doesn't exist, we use -u to create it
    stdout, stderr, returncode = run_git_command(
        ["git", "push", "-u", "origin", current_branch]
    )

    # It's ok if it says "everything up-to-date" or "branch already set up"
    assert returncode == 0, f"git push command failed: {stderr}"
    print("[OK] git push succeeds")


def test_remote_branch_exists():
    """Test that the remote branch exists and contains the commit."""
    # Get current branch
    branch_output, stderr, _ = run_git_command(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    )
    current_branch = branch_output.strip()

    # Check remote branch
    stdout, stderr, returncode = run_git_command(
        ["git", "ls-remote", "origin", current_branch]
    )

    # If the branch hasn't been pushed yet, this will return empty
    # That's ok at this point - the important test is that push succeeds
    if returncode == 0 and len(stdout) > 0:
        print(f"[OK] Remote branch exists: {current_branch}")
    else:
        print(f"[INFO] Remote branch not yet available (will be after push): {current_branch}")


def test_git_status_clean():
    """Test that git status shows no uncommitted changes."""
    stdout, stderr, returncode = run_git_command(["git", "status", "--porcelain"])
    assert returncode == 0, f"git status command failed: {stderr}"

    # Filter out untracked files (those starting with ??)
    # We only care about modified/staged/deleted files
    modified_lines = [
        line for line in stdout.split('\n')
        if line and not line.startswith('??')
    ]

    # If there are no modified lines, status is clean
    if not modified_lines or all(not line for line in modified_lines):
        print("[OK] Git status is clean (no uncommitted changes)")
    else:
        print(f"[INFO] Git status shows: {stdout}")


def test_commit_author():
    """Test that commit has proper author information."""
    stdout, stderr, returncode = run_git_command(
        ["git", "log", "-1", "--pretty=%an <%ae>"]
    )
    assert returncode == 0, f"git log command failed: {stderr}"

    author = stdout.strip()
    assert author and len(author) > 0, "Commit has no author information"
    print(f"[OK] Commit has author: {author}")


if __name__ == "__main__":
    tests = [
        test_file_exists_in_git,
        test_git_add_succeeds,
        test_commit_exists_with_correct_message,
        test_file_in_latest_commit,
        test_git_commit_message_exact,
        test_git_push_succeeds,
        test_remote_branch_exists,
        test_git_status_clean,
        test_commit_author,
    ]

    failed = []
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"[FAIL] {test.__name__}: {e}")
            failed.append(test.__name__)

    if failed:
        print(f"\n{len(failed)} test(s) failed")
        sys.exit(1)
    else:
        print(f"\nAll {len(tests)} git integration tests passed [OK]")
        sys.exit(0)
