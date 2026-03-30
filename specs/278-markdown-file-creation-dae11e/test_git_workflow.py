"""
Tests for git_workflow module.

Tests verify that git operations (add, commit, push) are executed correctly
with proper error handling.
"""

from unittest.mock import MagicMock, patch

import pytest
from git_workflow import COMMIT_MESSAGE, FEATURE_BRANCH, GitWorkflow, GitWorkflowError

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def git_workflow():
    """Provide a GitWorkflow instance for testing."""
    return GitWorkflow()


# ============================================================================
# Tests for git add command
# ============================================================================


class TestGitAdd:
    """Tests for add_file() method."""

    @patch("git_workflow.subprocess.run")
    def test_add_file_calls_git_add_with_correct_filename(self, mock_run):
        """Test that add_file invokes git add with correct filename."""
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        workflow = GitWorkflow()

        workflow.add_file()

        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert call_args == ["git", "add", "test-6ektaf.md"]

    @patch("git_workflow.subprocess.run")
    def test_add_file_returns_true_on_success(self, mock_run):
        """Test that add_file returns True when git add succeeds."""
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        workflow = GitWorkflow()

        result = workflow.add_file()

        assert result is True

    @patch("git_workflow.subprocess.run")
    def test_add_file_raises_error_on_failure(self, mock_run):
        """Test that add_file raises GitWorkflowError when git add fails."""
        mock_run.return_value = MagicMock(returncode=1, stderr="fatal: error")
        workflow = GitWorkflow()

        with pytest.raises(GitWorkflowError):
            workflow.add_file()

    @patch("git_workflow.subprocess.run")
    def test_add_file_error_message_includes_stderr(self, mock_run):
        """Test that error message includes stderr output."""
        error_msg = "fatal: not a git repository"
        mock_run.return_value = MagicMock(returncode=128, stderr=error_msg)
        workflow = GitWorkflow()

        with pytest.raises(GitWorkflowError) as exc_info:
            workflow.add_file()

        assert error_msg in str(exc_info.value)

    @patch("git_workflow.subprocess.run")
    def test_add_file_uses_capture_output(self, mock_run):
        """Test that add_file uses capture_output=True."""
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        workflow = GitWorkflow()

        workflow.add_file()

        kwargs = mock_run.call_args[1]
        assert kwargs.get("capture_output") is True
        assert kwargs.get("text") is True


# ============================================================================
# Tests for git commit command
# ============================================================================


class TestGitCommit:
    """Tests for commit_changes() method."""

    @patch("git_workflow.subprocess.run")
    def test_commit_calls_git_commit_with_message(self, mock_run):
        """Test that commit_changes invokes git commit with correct message."""
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        workflow = GitWorkflow()

        workflow.commit_changes()

        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert call_args[0] == "git"
        assert call_args[1] == "commit"
        assert call_args[2] == "-m"
        assert "feat(278)" in call_args[3]
        assert "test-6ektaf.md" in call_args[3]

    @patch("git_workflow.subprocess.run")
    def test_commit_uses_conventional_commit_format(self, mock_run):
        """Test that commit message follows conventional commits format."""
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        workflow = GitWorkflow()

        workflow.commit_changes()

        call_args = mock_run.call_args[0][0]
        message = call_args[3]
        assert message == COMMIT_MESSAGE
        assert message.startswith("feat(278):")

    @patch("git_workflow.subprocess.run")
    def test_commit_returns_true_on_success(self, mock_run):
        """Test that commit_changes returns True when git commit succeeds."""
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        workflow = GitWorkflow()

        result = workflow.commit_changes()

        assert result is True

    @patch("git_workflow.subprocess.run")
    def test_commit_raises_error_on_failure(self, mock_run):
        """Test that commit_changes raises GitWorkflowError when git commit fails."""
        mock_run.return_value = MagicMock(returncode=1, stderr="fatal: error")
        workflow = GitWorkflow()

        with pytest.raises(GitWorkflowError):
            workflow.commit_changes()

    @patch("git_workflow.subprocess.run")
    def test_commit_error_message_includes_stderr(self, mock_run):
        """Test that error message includes stderr output."""
        error_msg = "fatal: nothing to commit"
        mock_run.return_value = MagicMock(returncode=1, stderr=error_msg)
        workflow = GitWorkflow()

        with pytest.raises(GitWorkflowError) as exc_info:
            workflow.commit_changes()

        assert error_msg in str(exc_info.value)


# ============================================================================
# Tests for git push command
# ============================================================================


class TestGitPush:
    """Tests for push_to_branch() method."""

    @patch("git_workflow.subprocess.run")
    def test_push_calls_git_push_with_correct_branch(self, mock_run):
        """Test that push_to_branch invokes git push with correct branch."""
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        workflow = GitWorkflow()

        workflow.push_to_branch()

        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert call_args == ["git", "push", "origin", FEATURE_BRANCH]

    @patch("git_workflow.subprocess.run")
    def test_push_returns_true_on_success(self, mock_run):
        """Test that push_to_branch returns True when git push succeeds."""
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        workflow = GitWorkflow()

        result = workflow.push_to_branch()

        assert result is True

    @patch("git_workflow.subprocess.run")
    def test_push_raises_error_on_failure(self, mock_run):
        """Test that push_to_branch raises GitWorkflowError when git push fails."""
        mock_run.return_value = MagicMock(returncode=1, stderr="fatal: error")
        workflow = GitWorkflow()

        with pytest.raises(GitWorkflowError):
            workflow.push_to_branch()

    @patch("git_workflow.subprocess.run")
    def test_push_error_message_includes_stderr(self, mock_run):
        """Test that error message includes stderr output."""
        error_msg = "fatal: Could not read from remote repository"
        mock_run.return_value = MagicMock(returncode=128, stderr=error_msg)
        workflow = GitWorkflow()

        with pytest.raises(GitWorkflowError) as exc_info:
            workflow.push_to_branch()

        assert error_msg in str(exc_info.value)


# ============================================================================
# Tests for complete workflow
# ============================================================================


class TestCompleteWorkflow:
    """Tests for execute_workflow() method."""

    @patch("git_workflow.subprocess.run")
    def test_execute_workflow_calls_all_operations_in_order(self, mock_run):
        """Test that execute_workflow calls add, commit, push in sequence."""
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        workflow = GitWorkflow()

        workflow.execute_workflow()

        assert mock_run.call_count == 3
        call_list = mock_run.call_args_list
        # First call: git add
        assert call_list[0][0][0][1] == "add"
        # Second call: git commit
        assert call_list[1][0][0][1] == "commit"
        # Third call: git push
        assert call_list[2][0][0][1] == "push"

    @patch("git_workflow.subprocess.run")
    def test_execute_workflow_returns_true_on_success(self, mock_run):
        """Test that execute_workflow returns True when all operations succeed."""
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        workflow = GitWorkflow()

        result = workflow.execute_workflow()

        assert result is True

    @patch("git_workflow.subprocess.run")
    def test_execute_workflow_stops_on_add_failure(self, mock_run):
        """Test that workflow stops on git add failure."""
        mock_run.side_effect = [
            MagicMock(returncode=1, stderr="add failed"),
        ]
        workflow = GitWorkflow()

        with pytest.raises(GitWorkflowError):
            workflow.execute_workflow()

    @patch("git_workflow.subprocess.run")
    def test_execute_workflow_stops_on_commit_failure(self, mock_run):
        """Test that workflow stops on git commit failure."""
        mock_run.side_effect = [
            MagicMock(returncode=0, stderr=""),  # add succeeds
            MagicMock(returncode=1, stderr="commit failed"),  # commit fails
        ]
        workflow = GitWorkflow()

        with pytest.raises(GitWorkflowError):
            workflow.execute_workflow()

    @patch("git_workflow.subprocess.run")
    def test_execute_workflow_stops_on_push_failure(self, mock_run):
        """Test that workflow stops on git push failure."""
        mock_run.side_effect = [
            MagicMock(returncode=0, stderr=""),  # add succeeds
            MagicMock(returncode=0, stderr=""),  # commit succeeds
            MagicMock(returncode=1, stderr="push failed"),  # push fails
        ]
        workflow = GitWorkflow()

        with pytest.raises(GitWorkflowError):
            workflow.execute_workflow()


# ============================================================================
# Tests for initialization
# ============================================================================


class TestInitialization:
    """Tests for GitWorkflow initialization."""

    def test_initialization_with_defaults(self):
        """Test that GitWorkflow initializes with correct defaults."""
        workflow = GitWorkflow()
        assert workflow.filename == "test-6ektaf.md"
        assert workflow.branch == FEATURE_BRANCH
        assert workflow.message == COMMIT_MESSAGE

    def test_initialization_with_custom_values(self):
        """Test that GitWorkflow can be initialized with custom values."""
        workflow = GitWorkflow(
            filename="custom.md",
            branch="custom-branch",
            message="custom message"
        )
        assert workflow.filename == "custom.md"
        assert workflow.branch == "custom-branch"
        assert workflow.message == "custom message"
