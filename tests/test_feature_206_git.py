"""Tests for git operations in feature 206: git add, commit, and push."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from sheep.features.feature_206_markdown_file_creation import (
    BRANCH_NAME,
    FILENAME,
    git_add,
    git_commit,
    git_push,
)


class TestGitAdd:
    """Test suite for git_add() function."""

    @patch("sheep.features.feature_206_markdown_file_creation.subprocess.run")
    def test_git_add_calls_subprocess_correctly(self, mock_run):
        """Test that git_add() calls subprocess.run with correct arguments."""
        # Setup mock to succeed
        mock_run.return_value = MagicMock(returncode=0)

        # Call function
        git_add()

        # Verify subprocess.run was called with correct arguments
        mock_run.assert_called_once_with(
            ["git", "add", FILENAME],
            check=True,
            capture_output=True,
            text=True,
        )

    @patch("sheep.features.feature_206_markdown_file_creation.subprocess.run")
    def test_git_add_raises_on_failure(self, mock_run):
        """Test that git_add() raises CalledProcessError on git failure."""
        # Setup mock to fail
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "add"], stderr="fatal: not a git repository"
        )

        # Call function and expect exception
        with pytest.raises(subprocess.CalledProcessError):
            git_add()

    @patch("sheep.features.feature_206_markdown_file_creation.subprocess.run")
    def test_git_add_includes_filename_in_command(self, mock_run):
        """Test that git_add() includes the filename in the git command."""
        mock_run.return_value = MagicMock(returncode=0)

        git_add()

        # Verify FILENAME is in the command list
        call_args = mock_run.call_args
        assert FILENAME in call_args[0][0]


class TestGitCommit:
    """Test suite for git_commit() function."""

    @patch("sheep.features.feature_206_markdown_file_creation.subprocess.run")
    def test_git_commit_calls_subprocess_correctly(self, mock_run):
        """Test that git_commit() calls subprocess.run with correct arguments."""
        # Setup mock to succeed
        mock_run.return_value = MagicMock(returncode=0)

        # Call function
        git_commit()

        # Verify subprocess.run was called with correct arguments
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0][:2] == ["git", "commit"]
        assert "-m" in call_args[0][0]
        assert call_args[1]["check"] is True
        assert call_args[1]["capture_output"] is True
        assert call_args[1]["text"] is True

    @patch("sheep.features.feature_206_markdown_file_creation.subprocess.run")
    def test_git_commit_uses_conventional_format(self, mock_run):
        """Test that git_commit() uses conventional commit format."""
        mock_run.return_value = MagicMock(returncode=0)

        git_commit()

        # Verify the commit message follows conventional commits format (feat(206):)
        call_args = mock_run.call_args
        commit_msg = call_args[0][0][3]  # Fourth element is the message
        assert commit_msg.startswith("feat(206):")

    @patch("sheep.features.feature_206_markdown_file_creation.subprocess.run")
    def test_git_commit_raises_on_failure(self, mock_run):
        """Test that git_commit() raises CalledProcessError on git failure."""
        # Setup mock to fail
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "commit"], stderr="nothing to commit"
        )

        # Call function and expect exception
        with pytest.raises(subprocess.CalledProcessError):
            git_commit()


class TestGitPush:
    """Test suite for git_push() function."""

    @patch("sheep.features.feature_206_markdown_file_creation.subprocess.run")
    def test_git_push_calls_subprocess_correctly(self, mock_run):
        """Test that git_push() calls subprocess.run with correct arguments."""
        # Setup mock to succeed
        mock_run.return_value = MagicMock(returncode=0)

        # Call function
        git_push()

        # Verify subprocess.run was called with correct arguments
        mock_run.assert_called_once_with(
            ["git", "push", "-u", "origin", BRANCH_NAME],
            check=True,
            capture_output=True,
            text=True,
        )

    @patch("sheep.features.feature_206_markdown_file_creation.subprocess.run")
    def test_git_push_includes_upstream_flag(self, mock_run):
        """Test that git_push() includes -u flag for upstream tracking."""
        mock_run.return_value = MagicMock(returncode=0)

        git_push()

        # Verify -u flag is in the command
        call_args = mock_run.call_args
        assert "-u" in call_args[0][0]

    @patch("sheep.features.feature_206_markdown_file_creation.subprocess.run")
    def test_git_push_uses_correct_branch(self, mock_run):
        """Test that git_push() pushes to the correct feature branch."""
        mock_run.return_value = MagicMock(returncode=0)

        git_push()

        # Verify BRANCH_NAME is in the command
        call_args = mock_run.call_args
        assert BRANCH_NAME in call_args[0][0]

    @patch("sheep.features.feature_206_markdown_file_creation.subprocess.run")
    def test_git_push_raises_on_failure(self, mock_run):
        """Test that git_push() raises CalledProcessError on git failure."""
        # Setup mock to fail with network error
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "push"], stderr="fatal: could not read from remote"
        )

        # Call function and expect exception
        with pytest.raises(subprocess.CalledProcessError):
            git_push()
