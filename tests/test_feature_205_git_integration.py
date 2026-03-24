"""Tests for Feature 205: Git Integration (Phase 5).

This test suite covers git workflow operations: adding, committing, and pushing files.
Tests verify that git commands are executed correctly using subprocess with proper error handling.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, call

import pytest

from sheep.features.feature_205_markdown_file_creation import (
    FILENAME,
    BRANCH_NAME,
    COMMIT_MESSAGE,
    git_add_file,
    git_commit,
    git_push,
)


class TestGitAddFile:
    """Tests for git_add_file function."""

    def test_git_add_file_executes_without_error(self):
        """Test that git_add_file executes git add command successfully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                os.chdir(repo_path)

                # Initialize git repo
                subprocess.run(
                    ["git", "init"],
                    capture_output=True,
                    check=True,
                )

                # Create test file
                test_file = Path(FILENAME)
                test_file.write_text("# Test\n\nContent here. More content. Final content.\n", encoding="utf-8")

                # Should not raise
                git_add_file(FILENAME)

                # Verify file is staged
                result = subprocess.run(
                    ["git", "status", "--short"],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                # File should be in staging area (A or M prefix)
                assert FILENAME in result.stdout

            finally:
                os.chdir(original_cwd)

    def test_git_add_file_with_custom_filename(self):
        """Test that git_add_file works with custom filename."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                os.chdir(repo_path)

                # Initialize git repo
                subprocess.run(
                    ["git", "init"],
                    capture_output=True,
                    check=True,
                )

                # Create custom filename
                custom_file = "custom_test.md"
                Path(custom_file).write_text("# Custom\n\nTest content. More content. Final content.\n", encoding="utf-8")

                # Should not raise
                git_add_file(custom_file)

                # Verify file is staged
                result = subprocess.run(
                    ["git", "status", "--short"],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                assert custom_file in result.stdout

            finally:
                os.chdir(original_cwd)

    def test_git_add_file_raises_on_nonexistent_file(self):
        """Test that git_add_file raises CalledProcessError for nonexistent file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                os.chdir(repo_path)

                # Initialize git repo
                subprocess.run(
                    ["git", "init"],
                    capture_output=True,
                    check=True,
                )

                # Try to add nonexistent file
                with pytest.raises(subprocess.CalledProcessError):
                    git_add_file("nonexistent_file.md")

            finally:
                os.chdir(original_cwd)

    def test_git_add_file_logs_operation(self):
        """Test that git_add_file logs the staging operation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                os.chdir(repo_path)

                # Initialize git repo
                subprocess.run(
                    ["git", "init"],
                    capture_output=True,
                    check=True,
                )

                # Create test file
                Path(FILENAME).write_text("# Test\n\nContent here. More content. Final content.\n", encoding="utf-8")

                # Mock logger to verify logging
                with patch('sheep.features.feature_205_markdown_file_creation._logger') as mock_logger:
                    git_add_file(FILENAME)

                    # Verify logging calls
                    assert mock_logger.info.called
                    # Check that at least one call mentions staging
                    calls_str = str(mock_logger.info.call_args_list)
                    assert "Staging" in calls_str or "staged" in calls_str

            finally:
                os.chdir(original_cwd)


class TestGitCommit:
    """Tests for git_commit function."""

    def test_git_commit_executes_without_error(self):
        """Test that git_commit executes git commit command successfully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                os.chdir(repo_path)

                # Initialize git repo with config
                subprocess.run(
                    ["git", "init"],
                    capture_output=True,
                    check=True,
                )
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

                # Create initial commit
                Path("README.md").write_text("# Initial\n", encoding="utf-8")
                subprocess.run(
                    ["git", "add", "README.md"],
                    capture_output=True,
                    check=True,
                )
                subprocess.run(
                    ["git", "commit", "-m", "Initial commit"],
                    capture_output=True,
                    check=True,
                )

                # Create test file and stage it
                test_file = Path(FILENAME)
                test_file.write_text("# Test\n\nContent here. More content. Final content.\n", encoding="utf-8")
                subprocess.run(
                    ["git", "add", FILENAME],
                    capture_output=True,
                    check=True,
                )

                # Should not raise
                git_commit(FILENAME, COMMIT_MESSAGE)

                # Verify commit was created
                result = subprocess.run(
                    ["git", "log", "-1", "--format=%B"],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                assert "feat(205)" in result.stdout
                assert FILENAME in result.stdout

            finally:
                os.chdir(original_cwd)

    def test_git_commit_uses_custom_message(self):
        """Test that git_commit uses provided commit message."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                os.chdir(repo_path)

                # Initialize git repo with config
                subprocess.run(
                    ["git", "init"],
                    capture_output=True,
                    check=True,
                )
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

                # Create initial commit
                Path("README.md").write_text("# Initial\n", encoding="utf-8")
                subprocess.run(
                    ["git", "add", "README.md"],
                    capture_output=True,
                    check=True,
                )
                subprocess.run(
                    ["git", "commit", "-m", "Initial commit"],
                    capture_output=True,
                    check=True,
                )

                # Create test file and stage it
                Path(FILENAME).write_text("# Test\n\nContent here. More content. Final content.\n", encoding="utf-8")
                subprocess.run(
                    ["git", "add", FILENAME],
                    capture_output=True,
                    check=True,
                )

                # Commit with custom message
                custom_message = "feat(999): Custom test message"
                git_commit(FILENAME, custom_message)

                # Verify commit message
                result = subprocess.run(
                    ["git", "log", "-1", "--format=%B"],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                assert custom_message in result.stdout

            finally:
                os.chdir(original_cwd)

    def test_git_commit_uses_default_message(self):
        """Test that git_commit uses COMMIT_MESSAGE when not overridden."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                os.chdir(repo_path)

                # Initialize git repo with config
                subprocess.run(
                    ["git", "init"],
                    capture_output=True,
                    check=True,
                )
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

                # Create initial commit
                Path("README.md").write_text("# Initial\n", encoding="utf-8")
                subprocess.run(
                    ["git", "add", "README.md"],
                    capture_output=True,
                    check=True,
                )
                subprocess.run(
                    ["git", "commit", "-m", "Initial commit"],
                    capture_output=True,
                    check=True,
                )

                # Create test file and stage it
                Path(FILENAME).write_text("# Test\n\nContent here. More content. Final content.\n", encoding="utf-8")
                subprocess.run(
                    ["git", "add", FILENAME],
                    capture_output=True,
                    check=True,
                )

                # Commit with default message
                git_commit(FILENAME)

                # Verify default message was used
                result = subprocess.run(
                    ["git", "log", "-1", "--format=%B"],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                assert "feat(205)" in result.stdout

            finally:
                os.chdir(original_cwd)

    def test_git_commit_raises_on_failure(self):
        """Test that git_commit raises CalledProcessError on git failure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                os.chdir(repo_path)

                # Initialize git repo without config (will cause commit to fail)
                subprocess.run(
                    ["git", "init"],
                    capture_output=True,
                    check=True,
                )

                # Create test file and stage it
                Path(FILENAME).write_text("# Test\n\nContent here. More content. Final content.\n", encoding="utf-8")
                subprocess.run(
                    ["git", "add", FILENAME],
                    capture_output=True,
                    check=True,
                )

                # Try to commit without user.name/user.email configured
                # This should raise CalledProcessError
                with pytest.raises(subprocess.CalledProcessError):
                    git_commit(FILENAME, COMMIT_MESSAGE)

            finally:
                os.chdir(original_cwd)

    def test_git_commit_logs_operation(self):
        """Test that git_commit logs the commit operation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                os.chdir(repo_path)

                # Initialize git repo with config
                subprocess.run(
                    ["git", "init"],
                    capture_output=True,
                    check=True,
                )
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

                # Create initial commit
                Path("README.md").write_text("# Initial\n", encoding="utf-8")
                subprocess.run(
                    ["git", "add", "README.md"],
                    capture_output=True,
                    check=True,
                )
                subprocess.run(
                    ["git", "commit", "-m", "Initial commit"],
                    capture_output=True,
                    check=True,
                )

                # Create test file and stage it
                Path(FILENAME).write_text("# Test\n\nContent here. More content. Final content.\n", encoding="utf-8")
                subprocess.run(
                    ["git", "add", FILENAME],
                    capture_output=True,
                    check=True,
                )

                # Mock logger to verify logging
                with patch('sheep.features.feature_205_markdown_file_creation._logger') as mock_logger:
                    git_commit(FILENAME, COMMIT_MESSAGE)

                    # Verify logging calls
                    assert mock_logger.info.called
                    calls_str = str(mock_logger.info.call_args_list)
                    assert "commit" in calls_str.lower() or "Creating" in calls_str

            finally:
                os.chdir(original_cwd)


class TestGitPush:
    """Tests for git_push function."""

    def test_git_push_function_signature(self):
        """Test that git_push has correct function signature."""
        import inspect

        sig = inspect.signature(git_push)
        params = list(sig.parameters.keys())

        assert "branch" in params
        assert sig.parameters["branch"].default == BRANCH_NAME

    def test_git_push_raises_on_invalid_branch(self):
        """Test that git_push raises error for nonexistent branch."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                os.chdir(repo_path)

                # Initialize git repo
                subprocess.run(
                    ["git", "init"],
                    capture_output=True,
                    check=True,
                )

                # Try to push to nonexistent remote
                with pytest.raises(subprocess.CalledProcessError):
                    git_push("nonexistent/branch")

            finally:
                os.chdir(original_cwd)

    def test_git_push_logs_operation(self):
        """Test that git_push logs the push operation."""
        with patch('sheep.features.feature_205_markdown_file_creation._logger') as mock_logger:
            # Mock subprocess to avoid actual git operations
            with patch('subprocess.run') as mock_run:
                mock_run.return_value = MagicMock(returncode=0)

                git_push(BRANCH_NAME)

                # Verify logging was called
                assert mock_logger.info.called
                calls_str = str(mock_logger.info.call_args_list)
                assert "Pushing" in calls_str or "push" in calls_str.lower()


class TestGitIntegrationErrors:
    """Tests for error handling in git operations."""

    def test_git_add_file_captures_and_logs_error_output(self):
        """Test that git_add_file captures error output and logs it."""
        with patch('subprocess.run') as mock_run:
            # Mock git add failure
            error = subprocess.CalledProcessError(128, ["git", "add", FILENAME])
            error.stderr = "fatal: not a git repository"
            mock_run.side_effect = error

            with pytest.raises(subprocess.CalledProcessError):
                git_add_file(FILENAME)

    def test_git_commit_captures_and_logs_error_output(self):
        """Test that git_commit captures error output and logs it."""
        with patch('subprocess.run') as mock_run:
            # Mock git commit failure
            error = subprocess.CalledProcessError(128, ["git", "commit", "-m", COMMIT_MESSAGE])
            error.stderr = "fatal: not a git repository"
            mock_run.side_effect = error

            with pytest.raises(subprocess.CalledProcessError):
                git_commit(FILENAME, COMMIT_MESSAGE)

    def test_git_push_captures_and_logs_error_output(self):
        """Test that git_push captures error output and logs it."""
        with patch('subprocess.run') as mock_run:
            # Mock git push failure
            error = subprocess.CalledProcessError(128, ["git", "push", "-u", "origin", BRANCH_NAME])
            error.stderr = "fatal: 'origin' does not appear to be a 'git' repository"
            mock_run.side_effect = error

            with pytest.raises(subprocess.CalledProcessError):
                git_push(BRANCH_NAME)


class TestGitSubprocessDetails:
    """Tests for subprocess configuration in git operations."""

    def test_git_add_file_uses_subprocess_run_with_correct_args(self):
        """Test that git_add_file uses subprocess.run with correct arguments."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            git_add_file("test.md")

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once()
            call_args = mock_run.call_args

            # Check command is list-based (not string)
            cmd = call_args[0][0]
            assert isinstance(cmd, list)
            assert cmd[0] == "git"
            assert cmd[1] == "add"
            assert cmd[2] == "test.md"

            # Check subprocess options
            assert call_args[1]["check"] is True
            assert call_args[1]["capture_output"] is True

    def test_git_commit_uses_subprocess_run_with_correct_args(self):
        """Test that git_commit uses subprocess.run with correct arguments."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            git_commit("test.md", "feat: test commit")

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once()
            call_args = mock_run.call_args

            # Check command is list-based
            cmd = call_args[0][0]
            assert isinstance(cmd, list)
            assert cmd[0] == "git"
            assert cmd[1] == "commit"
            assert cmd[2] == "-m"
            assert cmd[3] == "feat: test commit"

            # Check subprocess options
            assert call_args[1]["check"] is True
            assert call_args[1]["capture_output"] is True

    def test_git_push_uses_subprocess_run_with_correct_args(self):
        """Test that git_push uses subprocess.run with correct arguments."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            git_push("feat/test-branch")

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once()
            call_args = mock_run.call_args

            # Check command is list-based
            cmd = call_args[0][0]
            assert isinstance(cmd, list)
            assert cmd[0] == "git"
            assert cmd[1] == "push"
            assert cmd[2] == "-u"
            assert cmd[3] == "origin"
            assert cmd[4] == "feat/test-branch"

            # Check subprocess options
            assert call_args[1]["check"] is True
            assert call_args[1]["capture_output"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
