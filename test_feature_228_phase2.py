"""Tests for git integration (stage, commit, push) for feature 228."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestVerifyFileExists:
    """Tests for verify_file_exists function."""

    def test_passes_when_file_exists(self):
        """Test that verify_file_exists passes when file exists."""
        import feature_228_phase2

        with patch("pathlib.Path.exists", return_value=True):
            # Should not raise
            feature_228_phase2.verify_file_exists()

    def test_raises_when_file_not_found(self):
        """Test that verify_file_exists raises FileNotFoundError when file missing."""
        import feature_228_phase2

        with patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(FileNotFoundError, match="does not exist"):
                feature_228_phase2.verify_file_exists()


class TestStageFile:
    """Tests for stage_file function."""

    @patch("subprocess.run")
    def test_calls_git_add_with_correct_arguments(self, mock_run):
        """Test that stage_file calls subprocess.run with correct git add arguments."""
        import feature_228_phase2

        mock_run.return_value = MagicMock(returncode=0)

        feature_228_phase2.stage_file()

        # Verify subprocess.run was called with git add command
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == ["git", "add", "test-2kjyci.md"]
        assert call_args[1]["check"] is True

    @patch("subprocess.run")
    def test_uses_list_based_arguments(self, mock_run):
        """Test that subprocess.run uses list-based arguments (not shell=True)."""
        import feature_228_phase2

        mock_run.return_value = MagicMock(returncode=0)

        feature_228_phase2.stage_file()

        # Verify list-based arguments (safe against command injection)
        call_args = mock_run.call_args
        assert isinstance(call_args[0][0], list)
        assert call_args[1].get("shell") is not True

    @patch("subprocess.run")
    def test_uses_check_true_for_fail_fast(self, mock_run):
        """Test that subprocess.run uses check=True for fail-fast error handling."""
        import feature_228_phase2

        mock_run.return_value = MagicMock(returncode=0)

        feature_228_phase2.stage_file()

        # Verify check=True is used
        call_args = mock_run.call_args
        assert call_args[1]["check"] is True

    @patch("subprocess.run")
    def test_uses_capture_output_and_text(self, mock_run):
        """Test that subprocess.run uses capture_output=True and text=True."""
        import feature_228_phase2

        mock_run.return_value = MagicMock(returncode=0)

        feature_228_phase2.stage_file()

        # Verify capture_output and text are set
        call_args = mock_run.call_args
        assert call_args[1]["capture_output"] is True
        assert call_args[1]["text"] is True

    @patch("subprocess.run")
    def test_raises_on_git_add_failure(self, mock_run):
        """Test that stage_file raises RuntimeError when git add fails."""
        import feature_228_phase2

        mock_run.side_effect = subprocess.CalledProcessError(1, "git add")

        with pytest.raises(RuntimeError, match="Failed to stage file"):
            feature_228_phase2.stage_file()


class TestVerifyStaging:
    """Tests for verify_staging function."""

    @patch("subprocess.run")
    def test_verifies_file_in_staging_area(self, mock_run):
        """Test that verify_staging checks file is in staging area."""
        import feature_228_phase2

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="A  test-2kjyci.md\n"
        )

        # Should not raise
        feature_228_phase2.verify_staging()

    @patch("subprocess.run")
    def test_accepts_both_added_and_modified_states(self, mock_run):
        """Test that verify_staging accepts both A and M status."""
        import feature_228_phase2

        # Test with modified file (M)
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="M  test-2kjyci.md\n"
        )

        # Should not raise
        feature_228_phase2.verify_staging()

    @patch("subprocess.run")
    def test_raises_when_file_not_staged(self, mock_run):
        """Test that verify_staging raises when file is not in staging area."""
        import feature_228_phase2

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="?? test-2kjyci.md\n"
        )

        with pytest.raises(AssertionError, match="not found in staging area"):
            feature_228_phase2.verify_staging()


class TestCommitFile:
    """Tests for commit_file function."""

    @patch("subprocess.run")
    def test_calls_git_commit_with_correct_message(self, mock_run):
        """Test that commit_file calls subprocess.run with correct git commit arguments."""
        import feature_228_phase2

        mock_run.return_value = MagicMock(returncode=0)

        feature_228_phase2.commit_file()

        # Verify subprocess.run was called with git commit command
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == ["git", "commit", "-m", "feat(228): create markdown file test-2kjyci.md with prose content"]
        assert call_args[1]["check"] is True

    @patch("subprocess.run")
    def test_uses_list_based_arguments_for_commit(self, mock_run):
        """Test that commit_file uses list-based arguments."""
        import feature_228_phase2

        mock_run.return_value = MagicMock(returncode=0)

        feature_228_phase2.commit_file()

        # Verify list-based arguments
        call_args = mock_run.call_args
        assert isinstance(call_args[0][0], list)

    @patch("subprocess.run")
    def test_raises_on_git_commit_failure(self, mock_run):
        """Test that commit_file raises RuntimeError when git commit fails."""
        import feature_228_phase2

        mock_run.side_effect = subprocess.CalledProcessError(1, "git commit")

        with pytest.raises(RuntimeError, match="Failed to commit file"):
            feature_228_phase2.commit_file()


class TestVerifyCommitMessage:
    """Tests for verify_commit_message function."""

    @patch("subprocess.run")
    def test_verifies_commit_message_matches(self, mock_run):
        """Test that verify_commit_message checks commit message."""
        import feature_228_phase2

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="feat(228): create markdown file test-2kjyci.md with prose content\n"
        )

        # Should not raise
        feature_228_phase2.verify_commit_message()

    @patch("subprocess.run")
    def test_raises_on_message_mismatch(self, mock_run):
        """Test that verify_commit_message raises when message doesn't match."""
        import feature_228_phase2

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="wrong message\n"
        )

        with pytest.raises(AssertionError, match="Commit message mismatch"):
            feature_228_phase2.verify_commit_message()


class TestPushToRemote:
    """Tests for push_to_remote function."""

    @patch("subprocess.run")
    def test_calls_git_push_correctly(self, mock_run):
        """Test that push_to_remote calls subprocess.run with git push."""
        import feature_228_phase2

        mock_run.return_value = MagicMock(returncode=0)

        feature_228_phase2.push_to_remote()

        # Verify subprocess.run was called
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        # Should be git push with -u and origin HEAD to set upstream
        assert call_args[0][0] == ["git", "push", "-u", "origin", "HEAD"]

    @patch("subprocess.run")
    def test_uses_check_true_for_push(self, mock_run):
        """Test that push_to_remote uses check=True."""
        import feature_228_phase2

        mock_run.return_value = MagicMock(returncode=0)

        feature_228_phase2.push_to_remote()

        call_args = mock_run.call_args
        assert call_args[1]["check"] is True

    @patch("subprocess.run")
    def test_raises_on_git_push_failure(self, mock_run):
        """Test that push_to_remote raises RuntimeError when git push fails."""
        import feature_228_phase2

        mock_run.side_effect = subprocess.CalledProcessError(1, "git push")

        with pytest.raises(RuntimeError, match="Failed to push"):
            feature_228_phase2.push_to_remote()


class TestVerifyRemotePush:
    """Tests for verify_remote_push function."""

    @patch("subprocess.run")
    def test_verifies_commit_on_remote(self, mock_run):
        """Test that verify_remote_push checks commit is on remote."""
        import feature_228_phase2

        # Mock multiple subprocess calls
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="abc123def456\n"),  # git rev-parse HEAD
            MagicMock(returncode=0, stdout="feat/228-markdown-file-creation-7fd4b2\n"),  # current branch
            MagicMock(returncode=0, stdout="abc123def456  refs/heads/feat/228-markdown-file-creation-7fd4b2\n"),  # git ls-remote
        ]

        # Should not raise
        feature_228_phase2.verify_remote_push()

    @patch("subprocess.run")
    def test_raises_when_commit_not_on_remote(self, mock_run):
        """Test that verify_remote_push raises when commit not found on remote."""
        import feature_228_phase2

        # Mock multiple subprocess calls
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="abc123def456\n"),  # git rev-parse HEAD
            MagicMock(returncode=0, stdout="feat/228-markdown-file-creation-7fd4b2\n"),  # current branch
            MagicMock(returncode=0, stdout="different789sha  refs/heads/feat/228-markdown-file-creation-7fd4b2\n"),  # git ls-remote
        ]

        with pytest.raises(AssertionError, match="not found on remote"):
            feature_228_phase2.verify_remote_push()


class TestIntegration:
    """Integration tests for the full workflow."""

    @patch("subprocess.run")
    def test_main_executes_all_phases(self, mock_run):
        """Test that main() executes all three phases successfully."""
        import feature_228_phase2

        # Set up return values for all subprocess calls
        mock_run.side_effect = [
            # Stage file (git add)
            MagicMock(returncode=0),
            # Verify staging (git status)
            MagicMock(returncode=0, stdout="A  test-2kjyci.md\n"),
            # Commit file (git commit)
            MagicMock(returncode=0),
            # Verify commit (git log)
            MagicMock(returncode=0, stdout="feat(228): create markdown file test-2kjyci.md with prose content\n"),
            # Push to remote (git push)
            MagicMock(returncode=0),
            # Verify remote (git rev-parse)
            MagicMock(returncode=0, stdout="abc123def456\n"),
            # Verify remote (git rev-parse --abbrev-ref)
            MagicMock(returncode=0, stdout="feat/228-markdown-file-creation-7fd4b2\n"),
            # Verify remote (git ls-remote)
            MagicMock(returncode=0, stdout="abc123def456  refs/heads/feat/228-markdown-file-creation-7fd4b2\n"),
        ]

        # With file existing mocked
        with patch("pathlib.Path.exists", return_value=True):
            result = feature_228_phase2.main()

        assert result == 0
