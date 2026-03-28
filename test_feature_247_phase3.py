#!/usr/bin/env python3
"""
Test suite for feature 247 Phase 3: Git Integration & Completion

Tests the git workflow function:
- git_workflow(): Complete orchestration from validation to push
  - Validates markdown file before git operations (fail-fast)
  - Stages file with git add
  - Creates commit with conventional message and Co-Authored-By trailer
  - Pushes to feature branch with git push -u origin HEAD
  - Uses subprocess.run() with proper error handling
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add src to path to import the module
sys.path.insert(0, str(Path(__file__).parent / "src"))

from create_markdown import git_workflow


class TestTask3_GitWorkflow:
    """Task 3: Implement git workflow (add, commit, push) with error handling."""

    # Test data: valid markdown file content
    VALID_MARKDOWN = "# The Art of Meaningful Communication\n\nEffective communication is the foundation of human connection, enabling us to share ideas, understand different perspectives, and collaborate toward common goals. When we listen carefully and express ourselves with clarity and empathy, we transform interactions from mere exchanges of information into genuine moments of understanding. This simple yet powerful practice of clear communication bridges distances and creates lasting bonds between people.\n"

    def test_git_workflow_validates_before_git_operations(self, tmp_path):
        """Test that git_workflow calls validate_markdown_file before git operations."""
        test_file = tmp_path / "test.md"
        test_file.write_text(self.VALID_MARKDOWN, encoding="utf-8")

        with patch("subprocess.run") as mock_run:
            with patch("create_markdown.validate_markdown_file") as mock_validate:
                mock_validate.return_value = True
                mock_run.return_value = MagicMock(returncode=0)

                git_workflow(str(test_file))

                # Verify validation was called first
                mock_validate.assert_called_once_with(str(test_file))

    def test_git_workflow_skips_git_operations_if_validation_fails(self, tmp_path):
        """Test that git operations are skipped if validation fails (fail-fast)."""
        test_file = tmp_path / "test.md"
        # Invalid file (no heading)
        test_file.write_text("No heading here. Just some text.\n", encoding="utf-8")

        with patch("subprocess.run") as mock_run:
            # Validation should fail
            with pytest.raises(ValueError, match="heading|missing"):
                git_workflow(str(test_file))

            # Verify git operations were not called
            mock_run.assert_not_called()

    @patch("subprocess.run")
    def test_git_add_is_called_with_correct_arguments(self, mock_run, tmp_path):
        """Test that git add is called with correct file path."""
        test_file = tmp_path / "test.md"
        test_file.write_text(self.VALID_MARKDOWN, encoding="utf-8")

        mock_run.return_value = MagicMock(returncode=0)

        git_workflow(str(test_file))

        # First call should be git add
        first_call = mock_run.call_args_list[0]
        assert first_call[0][0] == ["git", "add", str(test_file)]
        assert first_call[1]["check"] is True
        assert first_call[1]["capture_output"] is True
        assert first_call[1]["text"] is True

    @patch("subprocess.run")
    def test_git_commit_is_called_with_correct_message(self, mock_run, tmp_path):
        """Test that git commit is called with conventional message and trailer."""
        test_file = tmp_path / "test.md"
        test_file.write_text(self.VALID_MARKDOWN, encoding="utf-8")

        mock_run.return_value = MagicMock(returncode=0)

        expected_message = "feat(247): create markdown file test.md with prose content"
        git_workflow(str(test_file), commit_message=expected_message)

        # Second call should be git commit
        second_call = mock_run.call_args_list[1]
        commit_args = second_call[0][0]
        assert commit_args[0] == "git"
        assert commit_args[1] == "commit"
        assert commit_args[2] == "-m"

        # Check that message includes the commit message and Co-Authored-By trailer
        full_message = commit_args[3]
        assert expected_message in full_message
        assert "Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>" in full_message

    @patch("subprocess.run")
    def test_git_commit_includes_coauthored_by_trailer(self, mock_run, tmp_path):
        """Test that commit message includes Co-Authored-By trailer."""
        test_file = tmp_path / "test.md"
        test_file.write_text(self.VALID_MARKDOWN, encoding="utf-8")

        mock_run.return_value = MagicMock(returncode=0)

        git_workflow(str(test_file))

        # Check commit message in second call
        second_call = mock_run.call_args_list[1]
        commit_message = second_call[0][0][3]
        assert "Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>" in commit_message

    @patch("subprocess.run")
    def test_git_push_is_called_with_correct_arguments(self, mock_run, tmp_path):
        """Test that git push is called with -u origin HEAD."""
        test_file = tmp_path / "test.md"
        test_file.write_text(self.VALID_MARKDOWN, encoding="utf-8")

        mock_run.return_value = MagicMock(returncode=0)

        git_workflow(str(test_file))

        # Third call should be git push
        third_call = mock_run.call_args_list[2]
        assert third_call[0][0] == ["git", "push", "-u", "origin", "HEAD"]
        assert third_call[1]["check"] is True
        assert third_call[1]["capture_output"] is True
        assert third_call[1]["text"] is True

    @patch("subprocess.run")
    def test_git_operations_called_in_correct_order(self, mock_run, tmp_path):
        """Test that git operations are called in order: add, commit, push."""
        test_file = tmp_path / "test.md"
        test_file.write_text(self.VALID_MARKDOWN, encoding="utf-8")

        mock_run.return_value = MagicMock(returncode=0)

        git_workflow(str(test_file))

        # Verify three calls in correct order
        assert mock_run.call_count == 3
        calls = mock_run.call_args_list

        # First: git add
        assert calls[0][0][0] == ["git", "add", str(test_file)]
        # Second: git commit
        assert calls[1][0][0][0:3] == ["git", "commit", "-m"]
        # Third: git push
        assert calls[2][0][0] == ["git", "push", "-u", "origin", "HEAD"]

    @patch("subprocess.run")
    def test_git_add_failure_raises_exception(self, mock_run, tmp_path):
        """Test that git add failure raises CalledProcessError."""
        test_file = tmp_path / "test.md"
        test_file.write_text(self.VALID_MARKDOWN, encoding="utf-8")

        # git add fails
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "add"], stderr="fatal: not a git repository"
        )

        with pytest.raises(subprocess.CalledProcessError):
            git_workflow(str(test_file))

    @patch("subprocess.run")
    def test_git_commit_failure_raises_exception(self, mock_run, tmp_path):
        """Test that git commit failure raises CalledProcessError."""
        test_file = tmp_path / "test.md"
        test_file.write_text(self.VALID_MARKDOWN, encoding="utf-8")

        # First call (git add) succeeds, second (git commit) fails
        mock_run.side_effect = [
            MagicMock(returncode=0),  # git add success
            subprocess.CalledProcessError(1, ["git", "commit"], stderr="nothing to commit"),
        ]

        with pytest.raises(subprocess.CalledProcessError):
            git_workflow(str(test_file))

    @patch("subprocess.run")
    def test_git_push_failure_raises_exception(self, mock_run, tmp_path):
        """Test that git push failure raises CalledProcessError."""
        test_file = tmp_path / "test.md"
        test_file.write_text(self.VALID_MARKDOWN, encoding="utf-8")

        # First two calls succeed, third (git push) fails
        mock_run.side_effect = [
            MagicMock(returncode=0),  # git add success
            MagicMock(returncode=0),  # git commit success
            subprocess.CalledProcessError(1, ["git", "push"], stderr="connection refused"),
        ]

        with pytest.raises(subprocess.CalledProcessError):
            git_workflow(str(test_file))

    def test_git_add_failure_includes_stderr(self, tmp_path):
        """Test that git add errors are properly handled."""
        test_file = tmp_path / "test.md"
        test_file.write_text(self.VALID_MARKDOWN, encoding="utf-8")

        with patch("subprocess.run") as mock_run:
            error_stderr = "fatal: not a git repository"
            mock_run.side_effect = subprocess.CalledProcessError(
                1, ["git", "add"], stderr=error_stderr
            )

            with pytest.raises(subprocess.CalledProcessError):
                git_workflow(str(test_file))

    def test_git_workflow_with_nonexistent_file_raises_error(self):
        """Test that git workflow raises error for nonexistent file."""
        with pytest.raises(FileNotFoundError):
            git_workflow("/nonexistent/path/test.md")

    @patch("subprocess.run")
    def test_git_workflow_uses_subprocess_not_shell(self, mock_run, tmp_path):
        """Test that git commands use subprocess.run with argument list, not shell."""
        test_file = tmp_path / "test.md"
        test_file.write_text(self.VALID_MARKDOWN, encoding="utf-8")

        mock_run.return_value = MagicMock(returncode=0)

        git_workflow(str(test_file))

        # Verify that all calls use argument lists, not shell=True
        for call_args in mock_run.call_args_list:
            # First argument should be a list (command)
            assert isinstance(call_args[0][0], list)
            # shell parameter should not be present or should be False
            if "shell" in call_args[1]:
                assert call_args[1]["shell"] is False or call_args[1]["shell"] is not True

    @patch("subprocess.run")
    def test_git_commit_message_follows_conventional_commits(self, mock_run, tmp_path):
        """Test that commit message follows conventional commits format."""
        test_file = tmp_path / "test.md"
        test_file.write_text(self.VALID_MARKDOWN, encoding="utf-8")

        mock_run.return_value = MagicMock(returncode=0)

        expected_message = "feat(247): create markdown file test.md with prose content"
        git_workflow(str(test_file), commit_message=expected_message)

        # Check commit message format
        second_call = mock_run.call_args_list[1]
        commit_message = second_call[0][0][3]

        # Should include feature number in format feat(247):
        assert "feat(247):" in commit_message
        # Should include file name
        assert "test.md" in commit_message

    @patch("subprocess.run")
    def test_default_file_path_is_test_440dhk_md(self, mock_run, tmp_path):
        """Test that default file path is test-440dhk.md."""
        # Create file at default location
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)
            test_file = tmp_path / "test-440dhk.md"
            test_file.write_text(self.VALID_MARKDOWN, encoding="utf-8")

            mock_run.return_value = MagicMock(returncode=0)

            # Call without specifying file path
            git_workflow("test-440dhk.md")

            # Verify first git add call uses the default filename
            first_call = mock_run.call_args_list[0]
            assert "test-440dhk.md" in first_call[0][0]
        finally:
            os.chdir(original_cwd)


class TestGitWorkflowIntegration:
    """Integration tests for complete git workflow."""

    VALID_MARKDOWN = "# The Art of Meaningful Communication\n\nEffective communication is the foundation of human connection, enabling us to share ideas, understand different perspectives, and collaborate toward common goals. When we listen carefully and express ourselves with clarity and empathy, we transform interactions from mere exchanges of information into genuine moments of understanding. This simple yet powerful practice of clear communication bridges distances and creates lasting bonds between people.\n"

    @patch("subprocess.run")
    def test_git_workflow_complete_success_case(self, mock_run, tmp_path):
        """Test complete successful git workflow with all operations."""
        test_file = tmp_path / "test-example.md"
        test_file.write_text(self.VALID_MARKDOWN, encoding="utf-8")

        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        # Should not raise any exception
        git_workflow(str(test_file))

        # Verify all three git operations were called
        assert mock_run.call_count == 3

    def test_git_workflow_validation_failure_before_git_operations(self, tmp_path):
        """Test that validation failure prevents any git operations."""
        # Create file with invalid structure (missing heading)
        test_file = tmp_path / "test-invalid.md"
        test_file.write_text("No heading. Just some text.\n", encoding="utf-8")

        with patch("subprocess.run") as mock_run:
            with pytest.raises(ValueError):
                git_workflow(str(test_file))

            # No git operations should have been called
            mock_run.assert_not_called()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
