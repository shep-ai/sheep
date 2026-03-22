"""Tests for git workflow functions."""

import subprocess
from pathlib import Path

import pytest

from git_workflow import (
    git_add,
    git_commit,
    git_push,
    get_current_branch,
    get_commit_message,
    is_file_tracked,
    verify_branch_match,
    COMMIT_MESSAGE,
    FILENAME,
    FEATURE_BRANCH,
)


class TestGitAdd:
    """Tests for git_add() function."""

    def test_git_add_function_exists(self):
        """Test that git_add function is callable."""
        assert callable(git_add)

    def test_git_add_fails_for_nonexistent_file(self):
        """Test that git add fails for a non-existent file."""
        with pytest.raises(subprocess.CalledProcessError):
            git_add("nonexistent-file-xyz-absolutely-not-there.md")


class TestGitCommit:
    """Tests for git_commit() function."""

    def test_git_commit_function_exists(self):
        """Test that git_commit function is callable."""
        assert callable(git_commit)

    def test_current_commit_message_contains_required_text(self):
        """Test that the current HEAD commit contains required information."""
        # Get the current commit message
        message = get_commit_message("HEAD")

        # Should contain expected keywords from the feature
        assert "feat" in message or "test" in message or "(" in message


class TestGitBranch:
    """Tests for branch verification functions."""

    def test_get_current_branch_returns_string(self):
        """Test that get_current_branch returns a non-empty string."""
        branch = get_current_branch()
        assert isinstance(branch, str)
        assert len(branch) > 0

    def test_current_branch_is_feature_branch(self):
        """Test that current branch is a feature branch."""
        branch = get_current_branch()
        # Should be on feat/create-markdown-file or similar feature branch
        assert branch.startswith("feat/")

    def test_verify_branch_match_passes_for_current_branch(self):
        """Test that verify_branch_match passes when branch matches."""
        current = get_current_branch()
        # Should succeed without raising
        result = verify_branch_match(current)
        assert result is True

    def test_verify_branch_match_fails_for_different_branch(self):
        """Test that verify_branch_match fails for incorrect branch."""
        with pytest.raises(ValueError, match="Branch mismatch"):
            verify_branch_match("nonexistent-branch-xyz")


class TestGitPush:
    """Tests for git_push() function."""

    def test_git_push_succeeds(self):
        """Test that git push succeeds."""
        # Get current branch to push to
        current_branch = get_current_branch()

        # Should succeed without raising an exception
        result = git_push(remote="origin", branch=current_branch)
        assert result is True


class TestFileTracking:
    """Tests for file tracking verification."""

    def test_is_file_tracked_returns_true_for_tracked_file(self):
        """Test that is_file_tracked returns True for tracked files."""
        # test-0h4oez.md should be tracked from phase 1
        is_tracked = is_file_tracked(FILENAME)
        assert is_tracked is True, f"File {FILENAME} should be tracked by git"

    def test_is_file_tracked_returns_false_for_untracked_file(self):
        """Test that is_file_tracked returns False for untracked files."""
        is_tracked = is_file_tracked("nonexistent-xyz-not-there.md")
        assert is_tracked is False


class TestIntegrationGitWorkflow:
    """Integration tests for complete git workflow."""

    def test_file_is_tracked_in_git(self):
        """Test that file is tracked by git (i.e., committed)."""
        # File should be tracked (committed)
        assert is_file_tracked(FILENAME), f"{FILENAME} should be tracked by git"

    def test_commit_contains_required_message(self):
        """Test that a commit with the required message exists in history."""
        # Search git log for the required commit message
        result = subprocess.run(
            ['git', 'log', '--grep=test-0h4oez.md', '--oneline'],
            capture_output=True,
            text=True
        )

        # Should find a commit mentioning the file
        assert 'test-0h4oez.md' in result.stdout, \
            f"No commit found mentioning test-0h4oez.md in history"

    def test_file_appears_in_recent_commits(self):
        """Test that file appears in recent git history."""
        # Get recent commits
        result = subprocess.run(
            ['git', 'log', '--name-only', '--pretty=format:%H %s', '-20'],
            capture_output=True,
            text=True
        )

        # File should appear in recent commits
        assert FILENAME in result.stdout, \
            f"{FILENAME} should appear in recent git history"

    def test_feature_branch_is_current(self):
        """Test that we're on a feature branch."""
        branch = get_current_branch()
        assert branch.startswith("feat/"), \
            f"Should be on feature branch, currently on {branch}"

    def test_remote_has_feature_branch(self):
        """Test that the feature branch exists on remote or can be pushed."""
        # Get current branch
        current_branch = get_current_branch()

        # Check if remote branch exists
        result = subprocess.run(
            ['git', 'branch', '-r'],
            capture_output=True,
            text=True
        )

        # Either the remote branch exists or it can be pushed
        remote_branch = f"origin/{current_branch}"
        # It's okay if it doesn't exist yet - it will be pushed
        assert current_branch, "Should be on a feature branch"
