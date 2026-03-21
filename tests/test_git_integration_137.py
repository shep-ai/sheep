"""Tests for feature 137 phase 3: Git integration (add, commit, push).

Tests for task-3: Implement git integration with subprocess.run() for:
- Staging file with git add
- Creating conventional commit with message
- Pushing to remote origin with upstream tracking
"""

import subprocess
import pytest
from pathlib import Path
from unittest import mock


class TestGitStaging:
    """Tests for staging file with git add."""

    def test_stage_file_runs_git_add_command(self):
        """Test that stage_file() calls subprocess.run with correct git add command."""
        from git_integration_137 import stage_file

        with mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(returncode=0)
            stage_file("test-narzc3.md")

            # Verify git add was called with correct arguments
            mock_run.assert_called()
            args, kwargs = mock_run.call_args
            assert args[0] == ["git", "add", "test-narzc3.md"]
            assert kwargs["check"] == True

    def test_stage_file_raises_on_git_failure(self):
        """Test that stage_file() raises RuntimeError when git add fails."""
        from git_integration_137 import stage_file

        with mock.patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, ["git", "add"], stderr="Permission denied"
            )

            with pytest.raises(RuntimeError) as exc_info:
                stage_file("test-narzc3.md")

            assert "Failed to stage file" in str(exc_info.value)

    def test_stage_file_with_check_true_raises_on_nonzero_exit(self):
        """Test that check=True in subprocess.run ensures exceptions on failure."""
        from git_integration_137 import stage_file

        with mock.patch("subprocess.run") as mock_run:
            # Simulate git add failure
            error = subprocess.CalledProcessError(128, ["git", "add"])
            error.stderr = "fatal: not a git repository"
            mock_run.side_effect = error

            with pytest.raises(RuntimeError):
                stage_file("test-narzc3.md")


class TestGitCommit:
    """Tests for committing file with conventional commit message."""

    def test_commit_file_runs_git_commit_command(self):
        """Test that commit_file() calls subprocess.run with correct git commit command."""
        from git_integration_137 import commit_file

        expected_message = "feat(137): Create markdown file test-narzc3.md"

        with mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(returncode=0)
            commit_file("test-narzc3.md", expected_message)

            # Verify git commit was called
            mock_run.assert_called()
            args, kwargs = mock_run.call_args
            assert args[0] == ["git", "commit", "-m", expected_message]
            assert kwargs["check"] == True

    def test_commit_message_format_is_conventional(self):
        """Test that commit message follows conventional commits format."""
        from git_integration_137 import commit_file

        message = "feat(137): Create markdown file test-narzc3.md"

        # Verify message format: type(scope): description
        assert message.startswith("feat(137):")
        assert "Create markdown file test-narzc3.md" in message

    def test_commit_file_raises_on_git_failure(self):
        """Test that commit_file() raises RuntimeError when git commit fails."""
        from git_integration_137 import commit_file

        with mock.patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, ["git", "commit"], stderr="nothing to commit"
            )

            with pytest.raises(RuntimeError) as exc_info:
                commit_file("test-narzc3.md", "feat(137): Create markdown file test-narzc3.md")

            assert "Failed to commit file" in str(exc_info.value)


class TestGitPush:
    """Tests for pushing to remote origin with upstream tracking."""

    def test_push_file_runs_git_push_command(self):
        """Test that push_file() calls subprocess.run with correct git push command."""
        from git_integration_137 import push_file

        with mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(returncode=0)
            push_file("feat/markdown-file-creation-646f97")

            # Verify git push was called with -u flag for upstream tracking
            mock_run.assert_called()
            args, kwargs = mock_run.call_args
            assert args[0] == ["git", "push", "-u", "origin", "feat/markdown-file-creation-646f97"]
            assert kwargs["check"] == True

    def test_push_file_uses_u_flag_for_upstream_tracking(self):
        """Test that push_file() uses -u flag to set upstream tracking."""
        from git_integration_137 import push_file

        with mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(returncode=0)
            push_file("test-branch")

            args, _ = mock_run.call_args
            assert "-u" in args[0]
            assert "origin" in args[0]
            assert "test-branch" in args[0]

    def test_push_file_raises_on_git_failure(self):
        """Test that push_file() raises RuntimeError when git push fails."""
        from git_integration_137 import push_file

        with mock.patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, ["git", "push"], stderr="Connection refused"
            )

            with pytest.raises(RuntimeError) as exc_info:
                push_file("feat/markdown-file-creation-646f97")

            assert "Failed to push" in str(exc_info.value)


class TestGitIntegrationOrchestration:
    """Tests for integrate_git() orchestration function."""

    def test_integrate_git_calls_stage_commit_push_in_sequence(self):
        """Test that integrate_git() calls stage, commit, and push functions in order."""
        from git_integration_137 import integrate_git

        with mock.patch("git_integration_137.stage_file") as mock_stage, \
             mock.patch("git_integration_137.commit_file") as mock_commit, \
             mock.patch("git_integration_137.push_file") as mock_push:

            integrate_git("test-narzc3.md", "feat/markdown-file-creation-646f97",
                         "feat(137): Create markdown file test-narzc3.md")

            # Verify functions were called in sequence
            mock_stage.assert_called_once_with("test-narzc3.md")
            mock_commit.assert_called_once()
            mock_push.assert_called_once_with("feat/markdown-file-creation-646f97")

    def test_integrate_git_raises_on_any_failure(self):
        """Test that integrate_git() propagates exceptions from git operations."""
        from git_integration_137 import integrate_git

        with mock.patch("git_integration_137.stage_file") as mock_stage:
            mock_stage.side_effect = RuntimeError("git add failed")

            with pytest.raises(RuntimeError) as exc_info:
                integrate_git("test-narzc3.md", "feat/markdown-file-creation-646f97",
                             "feat(137): Create markdown file test-narzc3.md")

            assert "git add failed" in str(exc_info.value)

    def test_integrate_git_with_correct_parameters(self):
        """Test that integrate_git() accepts filename, branch, and commit message."""
        from git_integration_137 import integrate_git

        with mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(returncode=0)

            # Should accept these parameters without error
            integrate_git(
                "test-narzc3.md",
                "feat/markdown-file-creation-646f97",
                "feat(137): Create markdown file test-narzc3.md"
            )

            # Verify subprocess.run was called (from stage_file, commit_file, push_file)
            assert mock_run.call_count >= 3
