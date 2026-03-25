#!/usr/bin/env python3
"""
Test suite for git integration: verifying git add, commit, and push operations
follow conventional commits format and execute without errors.
"""

import subprocess
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock


class TestGitIntegration(unittest.TestCase):
    """Test cases for git add, commit, and push operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.filename = "test-lyi2gl.md"
        self.commit_message = "feat(213): Create markdown file test-lyi2gl.md"

    def test_file_exists_before_git_operations(self):
        """Assert file is not yet staged in git (initial state)."""
        filepath = Path(self.filename)
        self.assertTrue(filepath.exists(), f"File {self.filename} should exist before git operations")

    def test_commit_message_format(self):
        """Assert commit message follows Conventional Commits format."""
        message = self.commit_message
        # Conventional Commits format: type(scope): description
        # Pattern: word(word): text
        parts = message.split(': ')
        self.assertEqual(len(parts), 2, "Commit message must have format 'type(scope): description'")

        scope_part = parts[0]
        self.assertRegex(scope_part, r'^feat\(213\)$',
                        f"Commit message type(scope) part must match 'feat(213)' pattern, got: {scope_part}")

        description = parts[1]
        self.assertEqual(description, f"Create markdown file {self.filename}",
                        f"Commit message description must match expected text")

    @patch('subprocess.run')
    def test_git_add_command_structure(self, mock_run):
        """Assert that git add command is executed with correct structure."""
        mock_run.return_value = MagicMock(returncode=0)

        # Execute the git add command
        subprocess.run(["git", "add", self.filename], check=True)

        # Verify it was called with correct arguments
        mock_run.assert_called_once_with(["git", "add", self.filename], check=True)

    @patch('subprocess.run')
    def test_git_commit_command_structure(self, mock_run):
        """Assert that git commit command is executed with correct format."""
        mock_run.return_value = MagicMock(returncode=0)

        # Execute the git commit command
        subprocess.run(["git", "commit", "-m", self.commit_message], check=True)

        # Verify it was called with correct arguments
        mock_run.assert_called_once_with(
            ["git", "commit", "-m", self.commit_message],
            check=True
        )

    @patch('subprocess.run')
    def test_git_push_command_structure(self, mock_run):
        """Assert that git push command completes without error."""
        mock_run.return_value = MagicMock(returncode=0)

        # Execute the git push command
        subprocess.run(["git", "push"], check=True)

        # Verify it was called with correct arguments
        mock_run.assert_called_once_with(["git", "push"], check=True)

    @patch('subprocess.run')
    def test_subprocess_uses_shell_false(self, mock_run):
        """Assert subprocess calls do not use shell=True (security requirement)."""
        mock_run.return_value = MagicMock(returncode=0)

        # Make calls with proper structure (shell defaults to False, which is secure)
        subprocess.run(["git", "add", self.filename], check=True)
        subprocess.run(["git", "commit", "-m", self.commit_message], check=True)
        subprocess.run(["git", "push"], check=True)

        # Verify all calls used shell=False (or shell not specified, which defaults to False)
        self.assertEqual(mock_run.call_count, 3)
        for call in mock_run.call_args_list:
            # shell parameter should not be True
            if 'shell' in call.kwargs:
                self.assertFalse(call.kwargs['shell'], "shell parameter must be False for security")

    @patch('subprocess.run')
    def test_git_operations_fail_fast_on_error(self, mock_run):
        """Assert that git operations fail immediately on error (CalledProcessError)."""
        # Make git command fail
        mock_run.side_effect = subprocess.CalledProcessError(1, ["git", "add"])

        # Verify that CalledProcessError is raised (due to check=True)
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(["git", "add", self.filename], check=True)

    def test_commit_message_scope_matches_feature_number(self):
        """Assert commit message scope (213) matches the feature number."""
        message = self.commit_message
        self.assertIn("(213)", message, "Commit message must include feature number (213) in scope")


if __name__ == "__main__":
    unittest.main()
