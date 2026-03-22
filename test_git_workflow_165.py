"""Tests for git workflow (stage, commit, push) for feature 165."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest


class TestStageFile:
    """Tests for stage_file function."""

    @patch("subprocess.run")
    def test_stage_file_success(self, mock_run):
        """Test that stage_file successfully calls git add."""
        import git_workflow_165

        mock_run.return_value = MagicMock(returncode=0)

        # Should not raise
        git_workflow_165.stage_file()

        # Verify subprocess.run was called with git add command
        mock_run.assert_called_once_with(
            ["git", "add", "test-wqo87w.md"],
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_stage_file_raises_on_failure(self, mock_run):
        """Test that stage_file raises RuntimeError when git add fails."""
        import git_workflow_165

        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="fatal: not a git repository"
        )

        with pytest.raises(RuntimeError, match="git add failed"):
            git_workflow_165.stage_file()


class TestCreateCommit:
    """Tests for create_commit function."""

    @patch("subprocess.run")
    def test_create_commit_success(self, mock_run):
        """Test that create_commit successfully calls git commit."""
        import git_workflow_165

        mock_run.return_value = MagicMock(returncode=0)

        # Should not raise
        git_workflow_165.create_commit()

        # Verify subprocess.run was called with git commit command
        mock_run.assert_called_once_with(
            ["git", "commit", "-m", "feat(165): Create markdown file test-wqo87w.md with prose content"],
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_create_commit_uses_conventional_format(self, mock_run):
        """Test that commit message follows conventional commit format."""
        import git_workflow_165

        mock_run.return_value = MagicMock(returncode=0)

        git_workflow_165.create_commit()

        # Verify conventional commit format
        call_args = mock_run.call_args[0][0]
        message = call_args[3]  # -m parameter value
        assert message.startswith("feat(165):")
        assert "Create markdown file test-wqo87w.md with prose content" in message

    @patch("subprocess.run")
    def test_create_commit_raises_on_failure(self, mock_run):
        """Test that create_commit raises RuntimeError when git commit fails."""
        import git_workflow_165

        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="nothing staged for commit"
        )

        with pytest.raises(RuntimeError, match="git commit failed"):
            git_workflow_165.create_commit()


class TestPushToBranch:
    """Tests for push_to_branch function."""

    @patch("subprocess.run")
    def test_push_to_branch_success(self, mock_run):
        """Test that push_to_branch successfully calls git push."""
        import git_workflow_165

        mock_run.return_value = MagicMock(returncode=0)

        # Should not raise
        git_workflow_165.push_to_branch()

        # Verify subprocess.run was called with git push command
        mock_run.assert_called_once_with(
            ["git", "push", "-u", "origin", "HEAD"],
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_push_to_branch_uses_upstream_flag(self, mock_run):
        """Test that git push uses -u flag for upstream tracking."""
        import git_workflow_165

        mock_run.return_value = MagicMock(returncode=0)

        git_workflow_165.push_to_branch()

        # Verify -u flag is used
        call_args = mock_run.call_args[0][0]
        assert "-u" in call_args
        assert "origin" in call_args
        assert "HEAD" in call_args

    @patch("subprocess.run")
    def test_push_to_branch_raises_on_failure(self, mock_run):
        """Test that push_to_branch raises RuntimeError when git push fails."""
        import git_workflow_165

        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="fatal: Could not read from remote repository"
        )

        with pytest.raises(RuntimeError, match="git push failed"):
            git_workflow_165.push_to_branch()


class TestRunAllGitWorkflow:
    """Tests for run_all_git_workflow function."""

    @patch("git_workflow_165.push_to_branch")
    @patch("git_workflow_165.create_commit")
    @patch("git_workflow_165.stage_file")
    def test_runs_all_steps_in_order(self, mock_stage, mock_commit, mock_push):
        """Test that run_all_git_workflow executes all steps in sequence."""
        import git_workflow_165

        git_workflow_165.run_all_git_workflow()

        # Verify all functions were called in order
        assert mock_stage.call_count == 1
        assert mock_commit.call_count == 1
        assert mock_push.call_count == 1

    @patch("git_workflow_165.push_to_branch")
    @patch("git_workflow_165.create_commit")
    @patch("git_workflow_165.stage_file")
    def test_stops_on_stage_error(self, mock_stage, mock_commit, mock_push):
        """Test that workflow stops if stage_file fails."""
        import git_workflow_165

        mock_stage.side_effect = RuntimeError("git add failed")

        with pytest.raises(RuntimeError, match="git add failed"):
            git_workflow_165.run_all_git_workflow()

        # Verify only stage_file was called
        assert mock_stage.call_count == 1
        assert mock_commit.call_count == 0
        assert mock_push.call_count == 0

    @patch("git_workflow_165.push_to_branch")
    @patch("git_workflow_165.create_commit")
    @patch("git_workflow_165.stage_file")
    def test_stops_on_commit_error(self, mock_stage, mock_commit, mock_push):
        """Test that workflow stops if create_commit fails."""
        import git_workflow_165

        mock_commit.side_effect = RuntimeError("git commit failed")

        with pytest.raises(RuntimeError, match="git commit failed"):
            git_workflow_165.run_all_git_workflow()

        # Verify stage and commit were called, but not push
        assert mock_stage.call_count == 1
        assert mock_commit.call_count == 1
        assert mock_push.call_count == 0

    @patch("git_workflow_165.push_to_branch")
    @patch("git_workflow_165.create_commit")
    @patch("git_workflow_165.stage_file")
    def test_stops_on_push_error(self, mock_stage, mock_commit, mock_push):
        """Test that workflow stops if push_to_branch fails."""
        import git_workflow_165

        mock_push.side_effect = RuntimeError("git push failed")

        with pytest.raises(RuntimeError, match="git push failed"):
            git_workflow_165.run_all_git_workflow()

        # Verify all three were called
        assert mock_stage.call_count == 1
        assert mock_commit.call_count == 1
        assert mock_push.call_count == 1


class TestVerifyFileTracked:
    """Tests for verify_file_tracked function."""

    @patch("subprocess.run")
    def test_passes_when_file_tracked(self, mock_run):
        """Test that verify_file_tracked passes when file is in git."""
        import git_workflow_165

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="test-wqo87w.md\n"
        )

        # Should not raise
        git_workflow_165.verify_file_tracked()

    @patch("subprocess.run")
    def test_raises_when_file_not_tracked(self, mock_run):
        """Test that verify_file_tracked raises when file not in git."""
        import git_workflow_165

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=""  # Empty output
        )

        with pytest.raises(AssertionError, match="not tracked in git"):
            git_workflow_165.verify_file_tracked()


class TestVerifyCommitExists:
    """Tests for verify_commit_exists function."""

    @patch("subprocess.run")
    def test_passes_when_commit_message_found(self, mock_run):
        """Test that verify_commit_exists passes when commit message found."""
        import git_workflow_165

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="abc123 feat(165): Create markdown file test-wqo87w.md with prose content\n"
        )

        # Should not raise
        git_workflow_165.verify_commit_exists()

    @patch("subprocess.run")
    def test_raises_when_commit_message_not_found(self, mock_run):
        """Test that verify_commit_exists raises when message not found."""
        import git_workflow_165

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="abc123 some other commit message\n"
        )

        with pytest.raises(AssertionError, match="Commit message not found"):
            git_workflow_165.verify_commit_exists()


class TestVerifyWorkingTreeClean:
    """Tests for verify_working_tree_clean function."""

    @patch("subprocess.run")
    def test_passes_when_tree_clean(self, mock_run):
        """Test that verify_working_tree_clean passes when tree is clean."""
        import git_workflow_165

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=""  # Empty output means clean
        )

        # Should not raise
        git_workflow_165.verify_working_tree_clean()

    @patch("subprocess.run")
    def test_raises_when_uncommitted_changes(self, mock_run):
        """Test that verify_working_tree_clean raises when changes exist."""
        import git_workflow_165

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=" M test-file.py\n"  # Modified file
        )

        with pytest.raises(AssertionError, match="not clean"):
            git_workflow_165.verify_working_tree_clean()


class TestVerifyAllGitState:
    """Tests for verify_all_git_state function."""

    @patch("git_workflow_165.verify_working_tree_clean")
    @patch("git_workflow_165.verify_commit_exists")
    @patch("git_workflow_165.verify_file_tracked")
    def test_calls_all_verification_functions(self, mock_tracked, mock_commit, mock_clean):
        """Test that verify_all_git_state calls all verification functions."""
        import git_workflow_165

        git_workflow_165.verify_all_git_state()

        # Verify all functions were called
        assert mock_tracked.call_count == 1
        assert mock_commit.call_count == 1
        assert mock_clean.call_count == 1

    @patch("git_workflow_165.verify_working_tree_clean")
    @patch("git_workflow_165.verify_commit_exists")
    @patch("git_workflow_165.verify_file_tracked")
    def test_raises_on_tracked_verification_failure(self, mock_tracked, mock_commit, mock_clean):
        """Test that verify_all_git_state fails if verify_file_tracked fails."""
        import git_workflow_165

        mock_tracked.side_effect = AssertionError("File not tracked")

        with pytest.raises(AssertionError, match="not tracked"):
            git_workflow_165.verify_all_git_state()

        # Only the first check should be called
        assert mock_tracked.call_count == 1
        assert mock_commit.call_count == 0
        assert mock_clean.call_count == 0

    @patch("git_workflow_165.verify_working_tree_clean")
    @patch("git_workflow_165.verify_commit_exists")
    @patch("git_workflow_165.verify_file_tracked")
    def test_raises_on_commit_verification_failure(self, mock_tracked, mock_commit, mock_clean):
        """Test that verify_all_git_state fails if verify_commit_exists fails."""
        import git_workflow_165

        mock_commit.side_effect = AssertionError("Commit message not found")

        with pytest.raises(AssertionError, match="not found"):
            git_workflow_165.verify_all_git_state()

        # First two should be called
        assert mock_tracked.call_count == 1
        assert mock_commit.call_count == 1
        assert mock_clean.call_count == 0

    @patch("git_workflow_165.verify_working_tree_clean")
    @patch("git_workflow_165.verify_commit_exists")
    @patch("git_workflow_165.verify_file_tracked")
    def test_raises_on_clean_tree_verification_failure(self, mock_tracked, mock_commit, mock_clean):
        """Test that verify_all_git_state fails if verify_working_tree_clean fails."""
        import git_workflow_165

        mock_clean.side_effect = AssertionError("Working tree not clean")

        with pytest.raises(AssertionError, match="not clean"):
            git_workflow_165.verify_all_git_state()

        # All three should be called
        assert mock_tracked.call_count == 1
        assert mock_commit.call_count == 1
        assert mock_clean.call_count == 1
