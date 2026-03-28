"""Tests for git workflow (stage, commit, push) for feature 132."""

from unittest.mock import MagicMock, patch

import pytest


class TestStageFile:
    """Tests for stage_file function."""

    @patch("subprocess.run")
    def test_stage_file_success(self, mock_run):
        """Test that stage_file successfully calls git add."""
        import git_workflow_132

        mock_run.return_value = MagicMock(returncode=0)

        # Should not raise
        git_workflow_132.stage_file()

        # Verify subprocess.run was called with git add command
        mock_run.assert_called_once_with(
            ["git", "add", "test-fz0c6t.md"],
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_stage_file_raises_on_failure(self, mock_run):
        """Test that stage_file raises RuntimeError when git add fails."""
        import git_workflow_132

        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="fatal: not a git repository"
        )

        with pytest.raises(RuntimeError, match="git add failed"):
            git_workflow_132.stage_file()


class TestCreateCommit:
    """Tests for create_commit function."""

    @patch("subprocess.run")
    def test_create_commit_success(self, mock_run):
        """Test that create_commit successfully calls git commit."""
        import git_workflow_132

        mock_run.return_value = MagicMock(returncode=0)

        # Should not raise
        git_workflow_132.create_commit()

        # Verify subprocess.run was called with git commit command
        mock_run.assert_called_once_with(
            ["git", "commit", "-m", "feat(132): Create markdown file test-fz0c6t.md"],
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_create_commit_uses_conventional_format(self, mock_run):
        """Test that commit message follows conventional commit format."""
        import git_workflow_132

        mock_run.return_value = MagicMock(returncode=0)

        git_workflow_132.create_commit()

        # Verify conventional commit format
        call_args = mock_run.call_args[0][0]
        message = call_args[3]  # -m parameter value
        assert message.startswith("feat(132):")
        assert "Create markdown file test-fz0c6t.md" in message

    @patch("subprocess.run")
    def test_create_commit_raises_on_failure(self, mock_run):
        """Test that create_commit raises RuntimeError when git commit fails."""
        import git_workflow_132

        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="nothing staged for commit"
        )

        with pytest.raises(RuntimeError, match="git commit failed"):
            git_workflow_132.create_commit()


class TestPushToBranch:
    """Tests for push_to_branch function."""

    @patch("subprocess.run")
    def test_push_to_branch_success(self, mock_run):
        """Test that push_to_branch successfully calls git push."""
        import git_workflow_132

        mock_run.return_value = MagicMock(returncode=0)

        # Should not raise
        git_workflow_132.push_to_branch()

        # Verify subprocess.run was called with git push command
        mock_run.assert_called_once_with(
            ["git", "push", "-u", "origin", "HEAD"],
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_push_to_branch_uses_upstream_flag(self, mock_run):
        """Test that git push uses -u flag for upstream tracking."""
        import git_workflow_132

        mock_run.return_value = MagicMock(returncode=0)

        git_workflow_132.push_to_branch()

        # Verify -u flag is used
        call_args = mock_run.call_args[0][0]
        assert "-u" in call_args
        assert "origin" in call_args
        assert "HEAD" in call_args

    @patch("subprocess.run")
    def test_push_to_branch_raises_on_failure(self, mock_run):
        """Test that push_to_branch raises RuntimeError when git push fails."""
        import git_workflow_132

        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="fatal: Could not read from remote repository"
        )

        with pytest.raises(RuntimeError, match="git push failed"):
            git_workflow_132.push_to_branch()


class TestRunAllGitWorkflow:
    """Tests for run_all_git_workflow function."""

    @patch("git_workflow_132.push_to_branch")
    @patch("git_workflow_132.create_commit")
    @patch("git_workflow_132.stage_file")
    def test_runs_all_steps_in_order(self, mock_stage, mock_commit, mock_push):
        """Test that run_all_git_workflow executes all steps in sequence."""
        import git_workflow_132

        git_workflow_132.run_all_git_workflow()

        # Verify all functions were called in order
        assert mock_stage.call_count == 1
        assert mock_commit.call_count == 1
        assert mock_push.call_count == 1

    @patch("git_workflow_132.push_to_branch")
    @patch("git_workflow_132.create_commit")
    @patch("git_workflow_132.stage_file")
    def test_stops_on_stage_error(self, mock_stage, mock_commit, mock_push):
        """Test that workflow stops if stage_file fails."""
        import git_workflow_132

        mock_stage.side_effect = RuntimeError("git add failed")

        with pytest.raises(RuntimeError, match="git add failed"):
            git_workflow_132.run_all_git_workflow()

        # Verify only stage_file was called
        assert mock_stage.call_count == 1
        assert mock_commit.call_count == 0
        assert mock_push.call_count == 0

    @patch("git_workflow_132.push_to_branch")
    @patch("git_workflow_132.create_commit")
    @patch("git_workflow_132.stage_file")
    def test_stops_on_commit_error(self, mock_stage, mock_commit, mock_push):
        """Test that workflow stops if create_commit fails."""
        import git_workflow_132

        mock_commit.side_effect = RuntimeError("git commit failed")

        with pytest.raises(RuntimeError, match="git commit failed"):
            git_workflow_132.run_all_git_workflow()

        # Verify stage and commit were called, but not push
        assert mock_stage.call_count == 1
        assert mock_commit.call_count == 1
        assert mock_push.call_count == 0

    @patch("git_workflow_132.push_to_branch")
    @patch("git_workflow_132.create_commit")
    @patch("git_workflow_132.stage_file")
    def test_stops_on_push_error(self, mock_stage, mock_commit, mock_push):
        """Test that workflow stops if push_to_branch fails."""
        import git_workflow_132

        mock_push.side_effect = RuntimeError("git push failed")

        with pytest.raises(RuntimeError, match="git push failed"):
            git_workflow_132.run_all_git_workflow()

        # Verify all three were called
        assert mock_stage.call_count == 1
        assert mock_commit.call_count == 1
        assert mock_push.call_count == 1
