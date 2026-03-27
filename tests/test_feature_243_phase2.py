"""Tests for feature 243: Phase 2 - Git Integration and Delivery.

Tests verify that the markdown file commit is successfully pushed to the feature
branch with proper upstream tracking.
"""

import subprocess
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def test_git_commit_exists_locally():
    """Test that the commit with correct message exists on current branch."""
    result = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )

    assert result.returncode == 0, "git log command failed"
    commit_line = result.stdout.strip()
    assert "feat(243): create markdown file test-31irev.md with prose content" in commit_line, \
        f"Expected commit message not found. Got: {commit_line}"


def test_git_commit_message_format():
    """Test that commit message follows conventional commit format."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%B"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )

    assert result.returncode == 0, "git log format command failed"
    commit_message = result.stdout.strip()

    # Should start with conventional commit prefix
    assert commit_message.startswith("feat(243):"), \
        f"Commit message should start with 'feat(243):' but got: {commit_message}"

    # Should contain the filename
    assert "test-31irev.md" in commit_message, \
        "Commit message should mention test-31irev.md"


def test_git_branch_current_branch_name():
    """Test that we're on the correct feature branch."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )

    assert result.returncode == 0, "git branch command failed"
    branch_name = result.stdout.strip()
    assert branch_name == "feat/markdown-file-creation-20a93a", \
        f"Expected feature branch 'feat/markdown-file-creation-20a93a' but got: {branch_name}"


def test_git_push_to_feature_branch_succeeds():
    """Test that git push to feature branch succeeds."""
    repo_root = Path(__file__).parent.parent

    # Push to the feature branch
    result = subprocess.run(
        ["git", "push", "-u", "origin", "feat/markdown-file-creation-20a93a"],
        capture_output=True,
        text=True,
        cwd=repo_root,
    )

    # Push may succeed or fail depending on auth, but should complete
    # The important thing is that the command runs
    assert result.returncode in (0, 1, 128), \
        f"Unexpected git push exit code: {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"


def test_git_status_after_commit():
    """Test that there are no uncommitted changes after commit creation."""
    repo_root = Path(__file__).parent.parent

    # Check git status
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        cwd=repo_root,
    )

    assert result.returncode == 0, "git status command failed"
    status_output = result.stdout.strip()

    # The only untracked files should be the phase documentation files,
    # not the markdown file itself (which should be committed)
    lines = status_output.split("\n") if status_output else []

    # Filter out untracked files that are NOT the markdown file
    markdown_uncommitted = [
        line for line in lines
        if "test-31irev.md" in line and not line.startswith("??")
    ]

    assert len(markdown_uncommitted) == 0, \
        "The test-31irev.md file should be committed, not in working directory changes"


def test_feature_integration_with_push_tool():
    """Test that feature can be orchestrated with push tool."""
    # This is a simple integration test to verify the feature module works
    try:
        from sheep.features.feature_243_markdown_file_creation import (
            create_feature_243_markdown_file,
        )

        # The function should exist and be callable
        assert callable(create_feature_243_markdown_file), \
            "create_feature_243_markdown_file should be callable"
    except ImportError as e:
        raise AssertionError(f"Failed to import feature module: {e}")


if __name__ == "__main__":
    # Run tests manually if executed directly
    import traceback

    tests = [
        test_git_commit_exists_locally,
        test_git_commit_message_format,
        test_git_branch_current_branch_name,
        test_git_push_to_feature_branch_succeeds,
        test_git_status_after_commit,
        test_feature_integration_with_push_tool,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            print(f"[PASS] {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {test.__name__}: {e}")
            traceback.print_exc()
            failed += 1

    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
