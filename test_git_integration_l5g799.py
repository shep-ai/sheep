#!/usr/bin/env python3
"""
Test suite for git integration (phase 4) of feature 198.

Tests validate:
- git add command is called with correct arguments
- git commit command is called with conventional message format
- git push command is called with correct branch
- Exceptions are raised on git command failures
- Error messages are informative and indicate which operation failed
"""

import unittest
from unittest.mock import patch, MagicMock, call
import subprocess
from pathlib import Path
import tempfile
import os

from git_integration_l5g799 import (
    git_add_file,
    git_commit,
    git_push,
    execute_git_workflow,
    GitOperationError,
)


class TestGitAdd(unittest.TestCase):
    """Test suite for git_add_file function."""

    @patch("git_integration_l5g799.subprocess.run")
    def test_git_add_called_with_correct_args(self, mock_run):
        """Test that git add is called with correct filename argument."""
        mock_run.return_value = MagicMock()

        git_add_file("test-l5g799.md")

        # Verify subprocess.run was called with correct arguments
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        self.assertEqual(
            call_args[0][0],
            ["git", "add", "test-l5g799.md"],
            "git add should be called with filename argument",
        )
        self.assertTrue(
            call_args[1]["check"],
            "git add should have check=True to raise on failure",
        )

    @patch("git_integration_l5g799.subprocess.run")
    def test_git_add_uses_safe_list_format(self, mock_run):
        """Test that git add uses list argument format (prevents shell injection)."""
        mock_run.return_value = MagicMock()

        git_add_file("test-l5g799.md")

        # Verify argument is a list (not string) - prevents shell injection
        call_args = mock_run.call_args[0][0]
        self.assertIsInstance(
            call_args,
            list,
            "Arguments should be list (safe format), not string",
        )
        self.assertNotIsInstance(
            call_args,
            str,
            "Arguments should not be string (vulnerable to shell injection)",
        )

    @patch("git_integration_l5g799.subprocess.run")
    def test_git_add_captures_output(self, mock_run):
        """Test that git add captures stdout and stderr."""
        mock_run.return_value = MagicMock()

        git_add_file("test-l5g799.md")

        call_args = mock_run.call_args[1]
        self.assertTrue(
            call_args["capture_output"],
            "Should capture output for error reporting",
        )

    @patch("git_integration_l5g799.subprocess.run")
    def test_git_add_raises_on_process_error(self, mock_run):
        """Test that git add raises GitOperationError when git command fails."""
        # Simulate git command failure
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd="git add",
            stderr="fatal: not a git repository",
        )

        with self.assertRaises(GitOperationError) as cm:
            git_add_file("test-l5g799.md")

        error = cm.exception
        self.assertEqual(
            error.operation,
            "add",
            "Error should indicate 'add' operation failed",
        )
        self.assertIn(
            "test-l5g799.md",
            error.message,
            "Error message should include filename",
        )

    @patch("git_integration_l5g799.subprocess.run")
    def test_git_add_raises_on_git_not_found(self, mock_run):
        """Test that git add raises GitOperationError when git is not found."""
        mock_run.side_effect = FileNotFoundError("git not found")

        with self.assertRaises(GitOperationError) as cm:
            git_add_file("test-l5g799.md")

        error = cm.exception
        self.assertEqual(error.operation, "add")
        self.assertIn("git command not found", error.message)


class TestGitCommit(unittest.TestCase):
    """Test suite for git_commit function."""

    @patch("git_integration_l5g799.subprocess.run")
    def test_git_commit_called_with_correct_message(self, mock_run):
        """Test that git commit is called with conventional commit message."""
        mock_run.return_value = MagicMock()

        git_commit("test-l5g799.md", feature_number=198)

        call_args = mock_run.call_args[0][0]
        expected_message = "feat(198): Create markdown file test-l5g799.md with title and prose content"
        self.assertEqual(
            call_args,
            ["git", "commit", "-m", expected_message],
            "Commit message should follow conventional commits format",
        )

    @patch("git_integration_l5g799.subprocess.run")
    def test_git_commit_uses_safe_list_format(self, mock_run):
        """Test that git commit uses list argument format."""
        mock_run.return_value = MagicMock()

        git_commit("test-l5g799.md")

        call_args = mock_run.call_args[0][0]
        self.assertIsInstance(call_args, list)

    @patch("git_integration_l5g799.subprocess.run")
    def test_git_commit_message_format_conventions(self, mock_run):
        """Test that commit message follows conventional commits format."""
        mock_run.return_value = MagicMock()

        git_commit("test-l5g799.md", feature_number=198)

        call_args = mock_run.call_args[0][0]
        message = call_args[3]  # Fourth element is the message

        # Check format: feat(NNN): ...
        self.assertTrue(
            message.startswith("feat(198):"),
            "Message should start with 'feat(NNN):'",
        )
        self.assertIn(
            "test-l5g799.md",
            message,
            "Message should include filename",
        )
        self.assertIn(
            "title and prose content",
            message,
            "Message should describe what was created",
        )

    @patch("git_integration_l5g799.subprocess.run")
    def test_git_commit_different_feature_numbers(self, mock_run):
        """Test that commit message includes correct feature number."""
        mock_run.return_value = MagicMock()

        # Test with custom feature number
        git_commit("test-custom.md", feature_number=999)

        call_args = mock_run.call_args[0][0]
        message = call_args[3]
        self.assertIn("feat(999):", message)

    @patch("git_integration_l5g799.subprocess.run")
    def test_git_commit_raises_on_failure(self, mock_run):
        """Test that git commit raises GitOperationError on failure."""
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd="git commit",
            stderr="nothing to commit, working tree clean",
        )

        with self.assertRaises(GitOperationError) as cm:
            git_commit("test-l5g799.md")

        error = cm.exception
        self.assertEqual(error.operation, "commit")
        self.assertIn("test-l5g799.md", error.message)


class TestGitPush(unittest.TestCase):
    """Test suite for git_push function."""

    @patch("git_integration_l5g799.subprocess.run")
    def test_git_push_called_with_correct_branch(self, mock_run):
        """Test that git push is called with correct branch argument."""
        mock_run.return_value = MagicMock()

        git_push("feat/markdown-file-creation-903bd5")

        call_args = mock_run.call_args[0][0]
        self.assertEqual(
            call_args,
            ["git", "push", "origin", "feat/markdown-file-creation-903bd5"],
            "git push should include correct branch",
        )

    @patch("git_integration_l5g799.subprocess.run")
    def test_git_push_uses_safe_list_format(self, mock_run):
        """Test that git push uses list argument format."""
        mock_run.return_value = MagicMock()

        git_push("feat/198-markdown-file-creation-903bd5")

        call_args = mock_run.call_args[0][0]
        self.assertIsInstance(call_args, list)

    @patch("git_integration_l5g799.subprocess.run")
    def test_git_push_uses_origin_remote(self, mock_run):
        """Test that git push pushes to origin remote."""
        mock_run.return_value = MagicMock()

        git_push("feat/198-markdown-file-creation-903bd5")

        call_args = mock_run.call_args[0][0]
        self.assertEqual(
            call_args[1],
            "push",
            "Second argument should be 'push'",
        )
        self.assertEqual(
            call_args[2],
            "origin",
            "Should push to 'origin' remote",
        )

    @patch("git_integration_l5g799.subprocess.run")
    def test_git_push_raises_on_network_error(self, mock_run):
        """Test that git push raises GitOperationError on failure."""
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd="git push",
            stderr="fatal: could not read Password for 'https://github.com'",
        )

        with self.assertRaises(GitOperationError) as cm:
            git_push("feat/markdown-file-creation-903bd5")

        error = cm.exception
        self.assertEqual(error.operation, "push")
        self.assertIn("feat/markdown-file-creation-903bd5", error.message)


class TestExecuteGitWorkflow(unittest.TestCase):
    """Test suite for complete git workflow."""

    @patch("git_integration_l5g799.git_add_file")
    @patch("git_integration_l5g799.git_commit")
    @patch("git_integration_l5g799.git_push")
    @patch("git_integration_l5g799.Path.exists")
    def test_workflow_calls_operations_in_order(
        self, mock_exists, mock_push, mock_commit, mock_add
    ):
        """Test that workflow calls git add, commit, push in correct order."""
        mock_exists.return_value = True

        execute_git_workflow()

        # Verify calls were made in order
        mock_add.assert_called_once_with("test-l5g799.md")
        mock_commit.assert_called_once_with("test-l5g799.md", 198)
        mock_push.assert_called_once_with("feat/markdown-file-creation-903bd5")

    @patch("git_integration_l5g799.git_add_file")
    @patch("git_integration_l5g799.git_commit")
    @patch("git_integration_l5g799.git_push")
    @patch("git_integration_l5g799.Path.exists")
    def test_workflow_stops_on_add_failure(
        self, mock_exists, mock_push, mock_commit, mock_add
    ):
        """Test that workflow stops if git add fails."""
        mock_exists.return_value = True
        mock_add.side_effect = GitOperationError(
            operation="add",
            message="Failed to stage file",
        )

        with self.assertRaises(GitOperationError):
            execute_git_workflow()

        # Verify later operations were not called
        mock_commit.assert_not_called()
        mock_push.assert_not_called()

    @patch("git_integration_l5g799.git_add_file")
    @patch("git_integration_l5g799.git_commit")
    @patch("git_integration_l5g799.git_push")
    @patch("git_integration_l5g799.Path.exists")
    def test_workflow_stops_on_commit_failure(
        self, mock_exists, mock_push, mock_commit, mock_add
    ):
        """Test that workflow stops if git commit fails."""
        mock_exists.return_value = True
        mock_commit.side_effect = GitOperationError(
            operation="commit",
            message="Failed to commit",
        )

        with self.assertRaises(GitOperationError):
            execute_git_workflow()

        # Verify add was called, but push was not
        mock_add.assert_called_once()
        mock_push.assert_not_called()

    @patch("git_integration_l5g799.Path.exists")
    def test_workflow_raises_if_file_not_found(self, mock_exists):
        """Test that workflow raises error if file doesn't exist."""
        mock_exists.return_value = False

        with self.assertRaises(GitOperationError) as cm:
            execute_git_workflow()

        error = cm.exception
        self.assertEqual(error.operation, "add")
        self.assertIn("does not exist", error.message)

    @patch("git_integration_l5g799.git_add_file")
    @patch("git_integration_l5g799.git_commit")
    @patch("git_integration_l5g799.git_push")
    @patch("git_integration_l5g799.Path.exists")
    def test_workflow_with_custom_parameters(
        self, mock_exists, mock_push, mock_commit, mock_add
    ):
        """Test that workflow accepts custom parameters."""
        mock_exists.return_value = True

        execute_git_workflow(
            filename="custom-file.md",
            feature_number=999,
            branch="custom/branch",
        )

        mock_add.assert_called_once_with("custom-file.md")
        mock_commit.assert_called_once_with("custom-file.md", 999)
        mock_push.assert_called_once_with("custom/branch")


class TestGitOperationError(unittest.TestCase):
    """Test suite for GitOperationError exception."""

    def test_error_formatting(self):
        """Test that error messages are formatted informatively."""
        error = GitOperationError(
            operation="add",
            message="Failed to stage file",
            stderr="fatal: not a git repository",
        )

        error_str = str(error)
        self.assertIn("Git add failed", error_str)
        self.assertIn("Failed to stage file", error_str)
        self.assertIn("fatal: not a git repository", error_str)

    def test_error_with_empty_stderr(self):
        """Test that error formatting works with no stderr."""
        error = GitOperationError(
            operation="commit",
            message="Failed to commit",
        )

        error_str = str(error)
        self.assertIn("Git commit failed", error_str)
        self.assertIn("Failed to commit", error_str)

    def test_error_operation_attribute(self):
        """Test that error stores operation for inspection."""
        error = GitOperationError(
            operation="push",
            message="Network error",
        )

        self.assertEqual(error.operation, "push")
        self.assertEqual(error.message, "Network error")


class TestIntegrationWithRealRepo(unittest.TestCase):
    """Integration tests with real git repository (uses temp directory)."""

    def setUp(self):
        """Create temporary git repository for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Initialize git repository
        subprocess.run(["git", "init"], capture_output=True, check=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            capture_output=True,
            check=True,
        )

        # Create initial commit so we have a branch to commit to
        Path("README.md").write_text("# Test Repo\n")
        subprocess.run(["git", "add", "README.md"], capture_output=True, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            capture_output=True,
            check=True,
        )

    def tearDown(self):
        """Clean up temporary directory."""
        os.chdir(self.original_cwd)
        import shutil

        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_real_git_add(self):
        """Test git add with real git repository."""
        # Create test file
        Path("test.md").write_text("# Test\n\nContent.\n")

        # Should not raise
        git_add_file("test.md")

        # Verify file is staged
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("test.md", result.stdout)

    def test_real_git_add_nonexistent_file(self):
        """Test git add with non-existent file raises error."""
        with self.assertRaises(GitOperationError) as cm:
            git_add_file("nonexistent.md")

        self.assertEqual(cm.exception.operation, "add")


if __name__ == "__main__":
    unittest.main(verbosity=2)
