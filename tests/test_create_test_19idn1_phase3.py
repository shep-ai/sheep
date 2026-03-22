"""Tests for Phase 3: Git Integration for feature 157."""

import subprocess
from unittest.mock import patch, MagicMock
import pytest


class TestPhase3GitIntegration:
    """Tests for Phase 3: Git Integration."""

    def test_git_stage_file_function_exists(self):
        """Test that git_stage_file function exists in the script."""
        import create_test_19idn1

        assert hasattr(
            create_test_19idn1, "git_stage_file"
        ), "Script should have git_stage_file() function"
        assert callable(
            create_test_19idn1.git_stage_file
        ), "git_stage_file should be callable"

    def test_git_commit_function_exists(self):
        """Test that git_commit function exists in the script."""
        import create_test_19idn1

        assert hasattr(
            create_test_19idn1, "git_commit"
        ), "Script should have git_commit() function"
        assert callable(
            create_test_19idn1.git_commit
        ), "git_commit should be callable"

    def test_git_push_function_exists(self):
        """Test that git_push function exists in the script."""
        import create_test_19idn1

        assert hasattr(
            create_test_19idn1, "git_push"
        ), "Script should have git_push() function"
        assert callable(
            create_test_19idn1.git_push
        ), "git_push should be callable"

    @patch("subprocess.run")
    def test_git_stage_file_calls_git_add_with_correct_arguments(self, mock_run):
        """Test that git_stage_file calls subprocess.run with correct git add arguments."""
        import create_test_19idn1

        mock_run.return_value = MagicMock(returncode=0)

        create_test_19idn1.git_stage_file("test-19idn1.md")

        # Verify subprocess.run was called with correct arguments
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        # Check that the call was made with git add command
        assert call_args[0][0] == ["git", "add", "test-19idn1.md"]
        assert call_args[1]["check"] is True

    @patch("subprocess.run")
    def test_git_commit_calls_git_commit_with_correct_message(self, mock_run):
        """Test that git_commit calls subprocess.run with correct commit message."""
        import create_test_19idn1

        mock_run.return_value = MagicMock(returncode=0)
        message = "feat(157): Create markdown file test-19idn1.md with prose content"

        create_test_19idn1.git_commit(message)

        # Verify subprocess.run was called with correct arguments
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        # Check that the call was made with git commit command and correct message
        assert call_args[0][0] == ["git", "commit", "--no-verify", "-m", message]
        assert call_args[1]["check"] is True

    @patch("subprocess.run")
    def test_git_commit_uses_no_verify_flag(self, mock_run):
        """Test that git_commit uses the --no-verify flag."""
        import create_test_19idn1

        mock_run.return_value = MagicMock(returncode=0)
        message = "feat(157): Create markdown file test-19idn1.md with prose content"

        create_test_19idn1.git_commit(message)

        call_args = mock_run.call_args
        # Verify --no-verify flag is present
        assert "--no-verify" in call_args[0][0]

    @patch("subprocess.run")
    def test_git_push_calls_git_push_with_correct_branch(self, mock_run):
        """Test that git_push calls subprocess.run with correct branch."""
        import create_test_19idn1

        mock_run.return_value = MagicMock(returncode=0)
        branch = "feat/markdown-file-creation-b9d0e7"

        create_test_19idn1.git_push(branch)

        # Verify subprocess.run was called with correct arguments
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        # Check that the call was made with git push command and correct branch
        assert call_args[0][0] == ["git", "push", "origin", branch]
        assert call_args[1]["check"] is True

    @patch("subprocess.run")
    def test_git_stage_file_raises_error_on_git_failure(self, mock_run):
        """Test that git_stage_file raises RuntimeError if git add fails."""
        import create_test_19idn1

        mock_run.side_effect = subprocess.CalledProcessError(1, "git add", stderr="error message")

        with pytest.raises(RuntimeError) as exc_info:
            create_test_19idn1.git_stage_file("test-19idn1.md")

        assert "git add failed" in str(exc_info.value)

    @patch("subprocess.run")
    def test_git_commit_raises_error_on_git_failure(self, mock_run):
        """Test that git_commit raises RuntimeError if git commit fails."""
        import create_test_19idn1

        mock_run.side_effect = subprocess.CalledProcessError(1, "git commit", stderr="error message")
        message = "feat(157): Create markdown file test-19idn1.md with prose content"

        with pytest.raises(RuntimeError) as exc_info:
            create_test_19idn1.git_commit(message)

        assert "git commit failed" in str(exc_info.value)

    @patch("subprocess.run")
    def test_git_push_raises_error_on_git_failure(self, mock_run):
        """Test that git_push raises RuntimeError if git push fails."""
        import create_test_19idn1

        mock_run.side_effect = subprocess.CalledProcessError(1, "git push", stderr="error message")
        branch = "feat/markdown-file-creation-b9d0e7"

        with pytest.raises(RuntimeError) as exc_info:
            create_test_19idn1.git_push(branch)

        assert "git push failed" in str(exc_info.value)

    @patch("subprocess.run")
    def test_git_stage_file_returns_true_on_success(self, mock_run):
        """Test that git_stage_file returns True on success."""
        import create_test_19idn1

        mock_run.return_value = MagicMock(returncode=0)

        result = create_test_19idn1.git_stage_file("test-19idn1.md")

        assert result is True

    @patch("subprocess.run")
    def test_git_commit_returns_true_on_success(self, mock_run):
        """Test that git_commit returns True on success."""
        import create_test_19idn1

        mock_run.return_value = MagicMock(returncode=0)
        message = "feat(157): Create markdown file test-19idn1.md with prose content"

        result = create_test_19idn1.git_commit(message)

        assert result is True

    @patch("subprocess.run")
    def test_git_push_returns_true_on_success(self, mock_run):
        """Test that git_push returns True on success."""
        import create_test_19idn1

        mock_run.return_value = MagicMock(returncode=0)
        branch = "feat/markdown-file-creation-b9d0e7"

        result = create_test_19idn1.git_push(branch)

        assert result is True
