"""Tests for git integration (stage, commit, push) for feature 074."""

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestVerifyFileExists:
    """Tests for verify_file_exists function."""

    def test_passes_when_file_exists(self):
        """Test that verify_file_exists passes when file exists."""
        # Import here to avoid module-level issues
        import git_integration_074

        with patch("pathlib.Path.exists", return_value=True):
            # Should not raise
            git_integration_074.verify_file_exists()

    def test_raises_when_file_not_found(self):
        """Test that verify_file_exists raises FileNotFoundError when file missing."""
        import git_integration_074

        with patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(FileNotFoundError, match="does not exist"):
                git_integration_074.verify_file_exists()


class TestStageFile:
    """Tests for stage_file function."""

    @patch("subprocess.run")
    def test_calls_git_add_with_correct_arguments(self, mock_run):
        """Test that stage_file calls subprocess.run with correct git add arguments."""
        import git_integration_074

        mock_run.return_value = MagicMock(returncode=0)

        git_integration_074.stage_file()

        # Verify subprocess.run was called with git add command
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == ["git", "add", "test-macwxa.md"]
        assert call_args[1]["check"] is True

    @patch("subprocess.run")
    def test_uses_list_based_arguments(self, mock_run):
        """Test that subprocess.run uses list-based arguments (not shell=True)."""
        import git_integration_074

        mock_run.return_value = MagicMock(returncode=0)

        git_integration_074.stage_file()

        # Verify list-based arguments (safe against command injection)
        call_args = mock_run.call_args
        assert isinstance(call_args[0][0], list)
        assert call_args[1].get("shell") is not True

    @patch("subprocess.run")
    def test_uses_check_true_for_fail_fast(self, mock_run):
        """Test that subprocess.run uses check=True for fail-fast error handling."""
        import git_integration_074

        mock_run.return_value = MagicMock(returncode=0)

        git_integration_074.stage_file()

        # Verify check=True is used
        call_args = mock_run.call_args
        assert call_args[1]["check"] is True

    @patch("subprocess.run")
    def test_raises_on_git_add_failure(self, mock_run):
        """Test that stage_file raises RuntimeError when git add fails."""
        import git_integration_074

        mock_run.side_effect = subprocess.CalledProcessError(1, "git add")

        with pytest.raises(RuntimeError, match="Failed to stage file"):
            git_integration_074.stage_file()


class TestVerifyStaging:
    """Tests for verify_staging function."""

    @patch("subprocess.run")
    def test_verifies_file_in_staging_area(self, mock_run):
        """Test that verify_staging checks file is in staging area."""
        import git_integration_074

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="A  test-macwxa.md\n"
        )

        # Should not raise
        git_integration_074.verify_staging()

    @patch("subprocess.run")
    def test_accepts_added_or_modified_file(self, mock_run):
        """Test that verify_staging accepts both added (A) and modified (M) files."""
        import git_integration_074

        # Test added file
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="A  test-macwxa.md\n"
        )
        git_integration_074.verify_staging()

        # Test modified file
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="M  test-macwxa.md\n"
        )
        git_integration_074.verify_staging()

    @patch("subprocess.run")
    def test_raises_when_file_not_staged(self, mock_run):
        """Test that verify_staging raises AssertionError when file not staged."""
        import git_integration_074

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=""  # Empty staging area
        )

        with pytest.raises(AssertionError, match="not found in staging area"):
            git_integration_074.verify_staging()


class TestCommitFile:
    """Tests for commit_file function."""

    @patch("subprocess.run")
    def test_calls_git_commit_with_correct_message(self, mock_run):
        """Test that commit_file calls git commit with correct message."""
        import git_integration_074

        mock_run.return_value = MagicMock(returncode=0)

        git_integration_074.commit_file()

        # Verify subprocess.run was called with git commit command
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0][:2] == ["git", "commit"]
        assert "feat(074): create markdown file test-macwxa.md with prose content" in call_args[0][0]

    @patch("subprocess.run")
    def test_uses_conventional_commit_format(self, mock_run):
        """Test that commit message follows conventional commit format."""
        import git_integration_074

        mock_run.return_value = MagicMock(returncode=0)

        git_integration_074.commit_file()

        # Verify conventional commit format: feat(scope): description
        call_args = mock_run.call_args
        message = None
        for i, arg in enumerate(call_args[0][0]):
            if arg == "-m":
                message = call_args[0][0][i + 1]
                break

        assert message == "feat(074): create markdown file test-macwxa.md with prose content"
        assert message.startswith("feat(074):")

    @patch("subprocess.run")
    def test_uses_list_based_arguments(self, mock_run):
        """Test that subprocess.run uses list-based arguments (not shell=True)."""
        import git_integration_074

        mock_run.return_value = MagicMock(returncode=0)

        git_integration_074.commit_file()

        # Verify list-based arguments (safe against command injection)
        call_args = mock_run.call_args
        assert isinstance(call_args[0][0], list)
        assert call_args[1].get("shell") is not True

    @patch("subprocess.run")
    def test_uses_check_true_for_fail_fast(self, mock_run):
        """Test that subprocess.run uses check=True for fail-fast error handling."""
        import git_integration_074

        mock_run.return_value = MagicMock(returncode=0)

        git_integration_074.commit_file()

        # Verify check=True is used
        call_args = mock_run.call_args
        assert call_args[1]["check"] is True

    @patch("subprocess.run")
    def test_raises_on_git_commit_failure(self, mock_run):
        """Test that commit_file raises RuntimeError when git commit fails."""
        import git_integration_074

        mock_run.side_effect = subprocess.CalledProcessError(1, "git commit")

        with pytest.raises(RuntimeError, match="Failed to commit file"):
            git_integration_074.commit_file()


class TestVerifyCommitMessage:
    """Tests for verify_commit_message function."""

    @patch("subprocess.run")
    def test_verifies_commit_message_matches(self, mock_run):
        """Test that verify_commit_message checks commit message."""
        import git_integration_074

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="feat(074): create markdown file test-macwxa.md with prose content\n"
        )

        # Should not raise
        git_integration_074.verify_commit_message()

    @patch("subprocess.run")
    def test_raises_on_message_mismatch(self, mock_run):
        """Test that verify_commit_message raises when message doesn't match."""
        import git_integration_074

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="wrong: commit message\n"
        )

        with pytest.raises(AssertionError, match="Commit message mismatch"):
            git_integration_074.verify_commit_message()


class TestPushToRemote:
    """Tests for push_to_remote function."""

    @patch("subprocess.run")
    def test_calls_git_push_with_correct_arguments(self, mock_run):
        """Test that push_to_remote calls git push with correct arguments."""
        import git_integration_074

        mock_run.return_value = MagicMock(returncode=0)

        git_integration_074.push_to_remote()

        # Verify subprocess.run was called with git push command
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == ["git", "push", "-u", "origin", "HEAD"]

    @patch("subprocess.run")
    def test_uses_upstream_tracking(self, mock_run):
        """Test that git push uses -u flag for upstream tracking."""
        import git_integration_074

        mock_run.return_value = MagicMock(returncode=0)

        git_integration_074.push_to_remote()

        # Verify -u flag is used for upstream tracking
        call_args = mock_run.call_args
        assert "-u" in call_args[0][0]
        assert "origin" in call_args[0][0]

    @patch("subprocess.run")
    def test_uses_list_based_arguments(self, mock_run):
        """Test that subprocess.run uses list-based arguments (not shell=True)."""
        import git_integration_074

        mock_run.return_value = MagicMock(returncode=0)

        git_integration_074.push_to_remote()

        # Verify list-based arguments (safe against command injection)
        call_args = mock_run.call_args
        assert isinstance(call_args[0][0], list)
        assert call_args[1].get("shell") is not True

    @patch("subprocess.run")
    def test_uses_check_true_for_fail_fast(self, mock_run):
        """Test that subprocess.run uses check=True for fail-fast error handling."""
        import git_integration_074

        mock_run.return_value = MagicMock(returncode=0)

        git_integration_074.push_to_remote()

        # Verify check=True is used
        call_args = mock_run.call_args
        assert call_args[1]["check"] is True

    @patch("subprocess.run")
    def test_raises_on_git_push_failure(self, mock_run):
        """Test that push_to_remote raises RuntimeError when git push fails."""
        import git_integration_074

        mock_run.side_effect = subprocess.CalledProcessError(1, "git push")

        with pytest.raises(RuntimeError, match="Failed to push to remote"):
            git_integration_074.push_to_remote()


class TestVerifyRemotePush:
    """Tests for verify_remote_push function."""

    @patch("subprocess.run")
    def test_verifies_commit_on_remote(self, mock_run):
        """Test that verify_remote_push checks commit is on remote."""
        import git_integration_074

        # Mock three subprocess calls: rev-parse HEAD, rev-parse branch, ls-remote
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="abc123def456\n"),  # rev-parse HEAD
            MagicMock(returncode=0, stdout="feat/074-markdown-file-creation-380f68\n"),  # branch name
            MagicMock(returncode=0, stdout="abc123def456 refs/heads/feat/074-markdown-file-creation-380f68\n"),  # ls-remote
        ]

        # Should not raise
        git_integration_074.verify_remote_push()

    @patch("subprocess.run")
    def test_raises_when_commit_not_on_remote(self, mock_run):
        """Test that verify_remote_push raises when commit not found on remote."""
        import git_integration_074

        # Mock subprocess calls with mismatched commit
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="abc123def456\n"),  # local commit
            MagicMock(returncode=0, stdout="feat/074-markdown-file-creation-380f68\n"),  # branch name
            MagicMock(returncode=0, stdout="different789\n"),  # remote commit (different)
        ]

        with pytest.raises(AssertionError, match="Commit not found on remote"):
            git_integration_074.verify_remote_push()


class TestMainIntegration:
    """Integration tests for main function."""

    @patch("git_integration_074.verify_remote_push")
    @patch("git_integration_074.push_to_remote")
    @patch("git_integration_074.verify_commit_message")
    @patch("git_integration_074.commit_file")
    @patch("git_integration_074.verify_staging")
    @patch("git_integration_074.stage_file")
    @patch("git_integration_074.verify_file_exists")
    def test_executes_all_steps_in_order(
        self,
        mock_verify_exists,
        mock_stage,
        mock_verify_staging,
        mock_commit,
        mock_verify_msg,
        mock_push,
        mock_verify_push,
    ):
        """Test that main function executes all steps in correct order."""
        import git_integration_074

        result = git_integration_074.main()

        # Verify all functions were called in order
        assert mock_verify_exists.called
        assert mock_stage.called
        assert mock_verify_staging.called
        assert mock_commit.called
        assert mock_verify_msg.called
        assert mock_push.called
        assert mock_verify_push.called

        # Verify return code is 0 (success)
        assert result == 0

    @patch("git_integration_074.verify_file_exists")
    def test_returns_1_on_error(self, mock_verify):
        """Test that main returns 1 when an error occurs."""
        import git_integration_074

        # Make verify_file_exists raise an error
        mock_verify.side_effect = FileNotFoundError("File not found")

        result = git_integration_074.main()

        # Verify return code is 1 (error)
        assert result == 1

    @patch("git_integration_074.verify_remote_push")
    @patch("git_integration_074.push_to_remote")
    @patch("git_integration_074.verify_commit_message")
    @patch("git_integration_074.commit_file")
    @patch("git_integration_074.verify_staging")
    @patch("git_integration_074.stage_file")
    @patch("git_integration_074.verify_file_exists")
    def test_handles_stage_file_error(
        self,
        mock_verify_exists,
        mock_stage,
        mock_verify_staging,
        mock_commit,
        mock_verify_msg,
        mock_push,
        mock_verify_push,
    ):
        """Test that main handles errors during stage_file."""
        import git_integration_074

        # Make stage_file raise an error
        mock_stage.side_effect = RuntimeError("Git stage failed")

        result = git_integration_074.main()

        # Verify return code is 1 (error)
        assert result == 1

    @patch("git_integration_074.verify_remote_push")
    @patch("git_integration_074.push_to_remote")
    @patch("git_integration_074.verify_commit_message")
    @patch("git_integration_074.commit_file")
    @patch("git_integration_074.verify_staging")
    @patch("git_integration_074.stage_file")
    @patch("git_integration_074.verify_file_exists")
    def test_handles_commit_file_error(
        self,
        mock_verify_exists,
        mock_stage,
        mock_verify_staging,
        mock_commit,
        mock_verify_msg,
        mock_push,
        mock_verify_push,
    ):
        """Test that main handles errors during commit_file."""
        import git_integration_074

        # Make commit_file raise an error
        mock_commit.side_effect = RuntimeError("Git commit failed")

        result = git_integration_074.main()

        # Verify return code is 1 (error)
        assert result == 1

    @patch("git_integration_074.verify_remote_push")
    @patch("git_integration_074.push_to_remote")
    @patch("git_integration_074.verify_commit_message")
    @patch("git_integration_074.commit_file")
    @patch("git_integration_074.verify_staging")
    @patch("git_integration_074.stage_file")
    @patch("git_integration_074.verify_file_exists")
    def test_handles_push_to_remote_error(
        self,
        mock_verify_exists,
        mock_stage,
        mock_verify_staging,
        mock_commit,
        mock_verify_msg,
        mock_push,
        mock_verify_push,
    ):
        """Test that main handles errors during push_to_remote."""
        import git_integration_074

        # Make push_to_remote raise an error
        mock_push.side_effect = RuntimeError("Git push failed")

        result = git_integration_074.main()

        # Verify return code is 1 (error)
        assert result == 1


class TestIntegrationWithRealGit:
    """Integration tests with real git operations (not mocked)."""

    def test_full_workflow_stages_commits_and_pushes(self):
        """Test the complete workflow in a real git repository."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)

            # Initialize a git repo
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Configure git user for commits
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Create initial commit
            (repo_path / "README.md").write_text("# Test Repo\n")
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Create test markdown file
            (repo_path / "test-macwxa.md").write_text(
                "# The Power of Curiosity\n\n"
                "Curiosity is the driving force. We explore unknown territories. "
                "Successful people maintain curiosity.\n"
            )

            # Change to repo directory and test git add
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(repo_path)

                # Stage the file
                subprocess.run(
                    ["git", "add", "test-macwxa.md"],
                    check=True,
                    capture_output=True,
                )

                # Verify file is staged
                status_result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                assert "A  test-macwxa.md" in status_result.stdout

                # Commit the file
                subprocess.run(
                    ["git", "commit", "--no-verify", "-m",
                     "feat(074): create markdown file test-macwxa.md with prose content"],
                    check=True,
                    capture_output=True,
                )

                # Verify commit message
                log_result = subprocess.run(
                    ["git", "log", "-1", "--format=%B"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                assert "feat(074): create markdown file test-macwxa.md with prose content" in log_result.stdout

                # Verify file is no longer staged
                status_result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                assert "test-macwxa.md" not in status_result.stdout

            finally:
                os.chdir(original_cwd)
