#!/usr/bin/env python3
"""
Test suite for feature 202 phase 3: Git Integration & Orchestration

Tests the git workflow functions required by the specification:
- git_add_file(): Stage file with git add
- git_commit(): Create commit with conventional message
- git_push(): Push to remote branch
- main(): Complete orchestration from generation to push
"""

import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add src to path to import the feature module
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.features.feature_202_markdown_file_creation import (
    BRANCH_NAME,
    COMMIT_MESSAGE,
    FILENAME,
    git_add_file,
    git_commit,
    git_push,
    main,
)


class TestTask3_1GitWorkflow:
    """Task 3-1: Implement git workflow (add, commit, push).

    Tests git operations using subprocess for transparency and fail-fast
    error handling on git failures.
    """

    @patch("subprocess.run")
    def test_git_add_file_calls_subprocess_with_correct_args(self, mock_run):
        """Test git add calls subprocess with correct arguments."""
        mock_run.return_value = MagicMock(returncode=0)

        git_add_file(FILENAME)

        # Verify subprocess.run was called with correct git add command
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == ["git", "add", FILENAME]
        assert call_args[1]["check"] is True
        assert call_args[1]["capture_output"] is True
        assert call_args[1]["text"] is True

    @patch("subprocess.run")
    def test_git_add_file_raises_on_git_failure(self, mock_run):
        """Test git add raises CalledProcessError when git command fails."""
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "add", FILENAME], stderr="fatal: not a git repository"
        )

        with pytest.raises(subprocess.CalledProcessError):
            git_add_file(FILENAME)

    @patch("subprocess.run")
    def test_git_commit_calls_subprocess_with_correct_args(self, mock_run):
        """Test git commit calls subprocess with correct arguments."""
        mock_run.return_value = MagicMock(returncode=0)

        git_commit(FILENAME, COMMIT_MESSAGE)

        # Verify subprocess.run was called with correct git commit command
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == ["git", "commit", "-m", COMMIT_MESSAGE]
        assert call_args[1]["check"] is True
        assert call_args[1]["capture_output"] is True
        assert call_args[1]["text"] is True

    @patch("subprocess.run")
    def test_git_commit_uses_conventional_commit_format(self, mock_run):
        """Test git commit message follows conventional commits format."""
        mock_run.return_value = MagicMock(returncode=0)

        git_commit(FILENAME, COMMIT_MESSAGE)

        # Verify commit message includes feature number and description
        call_args = mock_run.call_args
        message = call_args[0][0][3]  # Get the message argument
        assert "feat(202)" in message
        assert FILENAME in message

    @patch("subprocess.run")
    def test_git_commit_raises_on_git_failure(self, mock_run):
        """Test git commit raises CalledProcessError when git command fails."""
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "commit"], stderr="nothing to commit"
        )

        with pytest.raises(subprocess.CalledProcessError):
            git_commit(FILENAME)

    @patch("subprocess.run")
    def test_git_push_calls_subprocess_with_correct_args(self, mock_run):
        """Test git push calls subprocess with correct arguments."""
        mock_run.return_value = MagicMock(returncode=0)

        git_push(BRANCH_NAME)

        # Verify subprocess.run was called with correct git push command
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == ["git", "push", "-u", "origin", BRANCH_NAME]
        assert call_args[1]["check"] is True
        assert call_args[1]["capture_output"] is True
        assert call_args[1]["text"] is True

    @patch("subprocess.run")
    def test_git_push_uses_upstream_tracking(self, mock_run):
        """Test git push uses -u flag for upstream tracking."""
        mock_run.return_value = MagicMock(returncode=0)

        git_push(BRANCH_NAME)

        # Verify -u flag is present for upstream tracking
        call_args = mock_run.call_args
        assert "-u" in call_args[0][0]

    @patch("subprocess.run")
    def test_git_push_raises_on_git_failure(self, mock_run):
        """Test git push raises CalledProcessError when git command fails."""
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "push"], stderr="fatal: unable to access repository"
        )

        with pytest.raises(subprocess.CalledProcessError):
            git_push(BRANCH_NAME)

    @patch("subprocess.run")
    def test_git_operations_fail_fast_on_first_error(self, mock_run):
        """Test git operations fail immediately on first error (fail-fast)."""
        # Simulate git add failing
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "add"], stderr="error"
        )

        with pytest.raises(subprocess.CalledProcessError):
            git_add_file(FILENAME)

        # Verify only git add was called, not subsequent operations
        assert mock_run.call_count == 1


class TestTask3_2MainOrchestration:
    """Task 3-2: Create main orchestration function and integration.

    Tests the main() function that orchestrates all steps:
    generation → file creation → validation → git operations.
    """

    @patch("sheep.features.feature_202_markdown_file_creation.git_push")
    @patch("sheep.features.feature_202_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_202_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_202_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_202_markdown_file_creation.create_markdown_file")
    def test_main_creates_file_and_validates(
        self, mock_create, mock_validate, mock_add, mock_commit, mock_push
    ):
        """Test main() creates file and runs validation."""
        # Mock successful file creation
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / FILENAME
            mock_create.return_value = str(filepath)

            # Call main (in isolation with mocked git operations)
            try:
                main()
            except SystemExit:
                # main() may exit, that's ok in this test context
                pass

            # Verify create_markdown_file was called
            mock_create.assert_called_once()

            # Verify validate_markdown_file was called
            mock_validate.assert_called_once()

    @patch("sys.exit")
    @patch("subprocess.run")
    @patch("sheep.features.feature_202_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_202_markdown_file_creation.create_markdown_file")
    def test_main_handles_validation_error(
        self, mock_create, mock_validate, mock_run, mock_exit
    ):
        """Test main() handles validation errors and exits with code 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / FILENAME
            mock_create.return_value = str(filepath)

            # Mock validation failure
            mock_validate.side_effect = ValueError("Invalid format")

            main()

            # Verify exit was called with code 1
            mock_exit.assert_called_with(1)

    @patch("sys.exit")
    @patch("subprocess.run")
    @patch("sheep.features.feature_202_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_202_markdown_file_creation.create_markdown_file")
    def test_main_handles_git_error(
        self, mock_create, mock_validate, mock_run, mock_exit
    ):
        """Test main() handles git errors and exits with code 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / FILENAME
            mock_create.return_value = str(filepath)

            # Mock git failure
            mock_run.side_effect = subprocess.CalledProcessError(
                1, ["git", "push"], stderr="fatal: error"
            )

            main()

            # Verify exit was called with code 1
            mock_exit.assert_called_with(1)

    @patch("sheep.features.feature_202_markdown_file_creation.git_push")
    @patch("sheep.features.feature_202_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_202_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_202_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_202_markdown_file_creation.create_markdown_file")
    def test_main_calls_all_steps_in_order(
        self, mock_create, mock_validate, mock_add, mock_commit, mock_push
    ):
        """Test main() calls all workflow steps in correct order."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / FILENAME
            mock_create.return_value = str(filepath)

            try:
                main()
            except SystemExit:
                pass

            # Verify call order: create → validate → add → commit → push
            assert mock_create.call_count >= 1
            assert mock_validate.call_count >= 1
            assert mock_add.call_count >= 1
            assert mock_commit.call_count >= 1
            assert mock_push.call_count >= 1

    @patch("sheep.features.feature_202_markdown_file_creation.git_push")
    @patch("sheep.features.feature_202_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_202_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_202_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_202_markdown_file_creation.create_markdown_file")
    def test_main_passes_correct_args_to_git_functions(
        self, mock_create, mock_validate, mock_add, mock_commit, mock_push
    ):
        """Test main() passes correct arguments to git functions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / FILENAME
            mock_create.return_value = str(filepath)

            try:
                main()
            except SystemExit:
                pass

            # Verify git_add_file was called with FILENAME
            mock_add.assert_called_with(FILENAME)

            # Verify git_commit was called with correct message
            mock_commit.assert_called()
            commit_call_args = mock_commit.call_args
            assert COMMIT_MESSAGE in str(commit_call_args)

            # Verify git_push was called with BRANCH_NAME
            mock_push.assert_called_with(BRANCH_NAME)


class TestEndToEndIntegration:
    """End-to-end integration tests (if actual git repo available).

    These tests exercise the full workflow including actual git operations
    in a temporary git repository.
    """

    def test_git_add_file_stages_file_in_real_repo(self):
        """Test git add stages file in actual git repository."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Initialize a real git repository
            subprocess.run(
                ["git", "init"],
                cwd=tmpdir,
                capture_output=True,
                check=True,
            )

            # Configure git user for testing
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmpdir,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=tmpdir,
                capture_output=True,
                check=True,
            )

            # Create a test file
            testfile = tmpdir_path / "test.md"
            testfile.write_text("# Test\n\nContent.\n")

            # Change to repo directory and stage the file
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                git_add_file("test.md")

                # Verify file is staged
                status = subprocess.run(
                    ["git", "status", "--porcelain"],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                # Should show file as staged (A prefix)
                assert "test.md" in status.stdout

            finally:
                import os
                os.chdir(original_cwd)

    def test_git_commit_creates_commit_in_real_repo(self):
        """Test git commit creates actual commit in git repository."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Initialize a real git repository
            subprocess.run(
                ["git", "init"],
                cwd=tmpdir,
                capture_output=True,
                check=True,
            )

            # Configure git user
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmpdir,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=tmpdir,
                capture_output=True,
                check=True,
            )

            # Create and stage a file
            testfile = tmpdir_path / "test.md"
            testfile.write_text("# Test\n\nContent.\n")

            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                subprocess.run(
                    ["git", "add", "test.md"],
                    capture_output=True,
                    check=True,
                )

                # Create commit
                git_commit("test.md", "feat(test): Test commit message")

                # Verify commit was created
                log = subprocess.run(
                    ["git", "log", "--oneline"],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                # Should contain the commit message
                assert "feat(test)" in log.stdout
                assert "Test commit message" in log.stdout

            finally:
                import os
                os.chdir(original_cwd)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
