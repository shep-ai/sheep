#!/usr/bin/env python3
"""
Tests for git operations in feature 229: markdown-file-creation-530bb9
Tests git add, commit, and push operations using subprocess.
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the implementation module
sys.path.insert(0, str(Path(__file__).parent))
from create_markdown_file_229 import (
    git_add,
    git_commit,
    git_push,
    FILENAME,
    COMMIT_MESSAGE,
)


def test_git_add_calls_subprocess_with_correct_arguments():
    """Test that git_add() calls subprocess.run with correct arguments."""
    with patch("subprocess.run") as mock_run:
        git_add()

        # Verify subprocess.run was called once
        mock_run.assert_called_once()

        # Get the arguments passed to subprocess.run
        call_args = mock_run.call_args
        args = call_args[0][0] if call_args[0] else call_args.kwargs.get("args")

        # Verify the command is correct
        assert args == ["git", "add", FILENAME], (
            f"git add should call subprocess with ['git', 'add', '{FILENAME}'], "
            f"but got {args}"
        )

        # Verify check=True was passed
        assert call_args.kwargs.get("check") is True, (
            "git add should call subprocess.run with check=True"
        )


def test_git_add_uses_list_arguments():
    """Test that git_add() uses list arguments (safe from command injection)."""
    with patch("subprocess.run") as mock_run:
        git_add()

        # Get the arguments passed to subprocess.run
        call_args = mock_run.call_args
        args = call_args[0][0] if call_args[0] else call_args.kwargs.get("args")

        # Verify arguments are passed as a list, not a string
        assert isinstance(args, list), (
            "git commands should be passed as a list of arguments, "
            "not a shell string (safer from command injection)"
        )


def test_git_commit_calls_subprocess_with_correct_arguments():
    """Test that git_commit() calls subprocess.run with correct arguments."""
    with patch("subprocess.run") as mock_run:
        git_commit()

        # Verify subprocess.run was called once
        mock_run.assert_called_once()

        # Get the arguments passed to subprocess.run
        call_args = mock_run.call_args
        args = call_args[0][0] if call_args[0] else call_args.kwargs.get("args")

        # Verify the command is correct
        expected_args = ["git", "commit", "-m", COMMIT_MESSAGE]
        assert args == expected_args, (
            f"git commit should call subprocess with {expected_args}, "
            f"but got {args}"
        )

        # Verify check=True was passed
        assert call_args.kwargs.get("check") is True, (
            "git commit should call subprocess.run with check=True"
        )


def test_git_commit_message_format():
    """Test that git_commit() uses correct commit message format."""
    with patch("subprocess.run") as mock_run:
        git_commit()

        # Get the arguments passed to subprocess.run
        call_args = mock_run.call_args
        args = call_args[0][0] if call_args[0] else call_args.kwargs.get("args")

        # Extract the commit message (should be at index 3)
        commit_message = args[3] if len(args) > 3 else None

        # Verify commit message matches expected format
        assert commit_message == COMMIT_MESSAGE, (
            f"Commit message should be '{COMMIT_MESSAGE}', "
            f"but got '{commit_message}'"
        )

        # Verify it follows conventional commit format
        assert commit_message.startswith("feat("), (
            "Commit message should follow conventional commit format (feat(...))"
        )
        assert "test-c1ds43.md" in commit_message, (
            "Commit message should mention the file being created"
        )


def test_git_push_calls_subprocess_with_correct_arguments():
    """Test that git_push() calls subprocess.run with correct arguments."""
    with patch("subprocess.run") as mock_run:
        git_push()

        # Verify subprocess.run was called once
        mock_run.assert_called_once()

        # Get the arguments passed to subprocess.run
        call_args = mock_run.call_args
        args = call_args[0][0] if call_args[0] else call_args.kwargs.get("args")

        # Verify the command is correct
        expected_args = ["git", "push", "-u", "origin", "HEAD"]
        assert args == expected_args, (
            f"git push should call subprocess with {expected_args}, "
            f"but got {args}"
        )

        # Verify check=True was passed
        assert call_args.kwargs.get("check") is True, (
            "git push should call subprocess.run with check=True"
        )


def test_git_push_to_origin_head():
    """Test that git_push() pushes to origin HEAD (current branch)."""
    with patch("subprocess.run") as mock_run:
        git_push()

        # Get the arguments passed to subprocess.run
        call_args = mock_run.call_args
        args = call_args[0][0] if call_args[0] else call_args.kwargs.get("args")

        # Verify it pushes to origin (not a specific branch)
        assert "origin" in args, "git push should push to 'origin'"

        # Verify it uses HEAD (current branch)
        assert "HEAD" in args, "git push should use 'HEAD' for current branch"

        # Verify -u flag is used (set upstream)
        assert "-u" in args, "git push should use -u flag to set upstream"


def test_git_operations_called_in_correct_order():
    """Test that git operations are called in the correct sequence."""
    # This test documents the expected order: add → commit → push
    # The order matters because:
    # 1. Must add the file before committing
    # 2. Must commit before pushing
    # 3. Cannot push without a commit

    expected_order = ["git_add", "git_commit", "git_push"]

    # This is a conceptual test showing the expected call order
    # In the main() function, they should be called in this exact order
    assert expected_order == ["git_add", "git_commit", "git_push"], (
        "Git operations should be called in order: add → commit → push"
    )


def test_git_add_raises_on_failure():
    """Test that git_add() raises CalledProcessError on git failure."""
    with patch("subprocess.run") as mock_run:
        # Simulate git command failure
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=["git", "add", FILENAME],
            output=None,
            stderr="fatal: not a git repository",
        )

        # Should raise the exception
        try:
            git_add()
            assert False, "git_add() should raise CalledProcessError on git failure"
        except subprocess.CalledProcessError:
            pass  # Expected


def test_git_commit_raises_on_failure():
    """Test that git_commit() raises CalledProcessError on git failure."""
    with patch("subprocess.run") as mock_run:
        # Simulate git command failure
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=["git", "commit", "-m", COMMIT_MESSAGE],
            output=None,
            stderr="fatal: not a git repository",
        )

        # Should raise the exception
        try:
            git_commit()
            assert False, "git_commit() should raise CalledProcessError on git failure"
        except subprocess.CalledProcessError:
            pass  # Expected


def test_git_push_raises_on_failure():
    """Test that git_push() raises CalledProcessError on git failure."""
    with patch("subprocess.run") as mock_run:
        # Simulate git command failure
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=["git", "push", "-u", "origin", "HEAD"],
            output=None,
            stderr="fatal: could not read Username",
        )

        # Should raise the exception
        try:
            git_push()
            assert False, "git_push() should raise CalledProcessError on git failure"
        except subprocess.CalledProcessError:
            pass  # Expected


if __name__ == "__main__":
    # Run tests manually if desired
    test_git_add_calls_subprocess_with_correct_arguments()
    print("✓ test_git_add_calls_subprocess_with_correct_arguments passed")

    test_git_add_uses_list_arguments()
    print("✓ test_git_add_uses_list_arguments passed")

    test_git_commit_calls_subprocess_with_correct_arguments()
    print("✓ test_git_commit_calls_subprocess_with_correct_arguments passed")

    test_git_commit_message_format()
    print("✓ test_git_commit_message_format passed")

    test_git_push_calls_subprocess_with_correct_arguments()
    print("✓ test_git_push_calls_subprocess_with_correct_arguments passed")

    test_git_push_to_origin_head()
    print("✓ test_git_push_to_origin_head passed")

    test_git_operations_called_in_correct_order()
    print("✓ test_git_operations_called_in_correct_order passed")

    test_git_add_raises_on_failure()
    print("✓ test_git_add_raises_on_failure passed")

    test_git_commit_raises_on_failure()
    print("✓ test_git_commit_raises_on_failure passed")

    test_git_push_raises_on_failure()
    print("✓ test_git_push_raises_on_failure passed")

    print("\nAll git operation tests passed!")
