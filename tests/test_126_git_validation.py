"""Tests for feature 126, Phase 1, Task 1-1: Git Repository State Validation."""

import subprocess
import pytest
from pathlib import Path


class TestGitInitialization:
    """Tests for checking if git is initialized."""

    def test_git_initialized_in_current_repo(self):
        """Test that git is initialized in the current repository."""
        # Run git rev-parse --git-dir to verify git is initialized
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True
        )
        # If git is initialized, the command succeeds (exit code 0)
        assert result.returncode == 0, "Git is not initialized"
        assert result.stdout.strip(), "Git directory path should not be empty"


class TestCurrentBranch:
    """Tests for verifying current branch name."""

    def test_current_branch_is_feat_126(self):
        """Test that current branch is feat/126-markdown-file-create-cea132."""
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        current_branch = result.stdout.strip()
        assert current_branch == "feat/markdown-file-create-cea132", \
            f"Expected branch 'feat/markdown-file-create-cea132', got '{current_branch}'"


class TestWorkingTreeClean:
    """Tests for verifying working tree is clean."""

    def test_working_tree_is_clean(self):
        """Test that working tree has no uncommitted changes (excluding untracked files)."""
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        status_output = result.stdout.strip()

        # Filter out untracked files (lines starting with "??")
        # We only care about modified, staged, deleted files, etc.
        tracked_changes = [
            line for line in status_output.split("\n")
            if line and not line.startswith("??")
        ]

        assert not tracked_changes, \
            f"Working tree is dirty (has uncommitted changes):\n{chr(10).join(tracked_changes)}"


class TestGitUserConfiguration:
    """Tests for verifying git user configuration."""

    def test_git_user_name_configured(self):
        """Test that git user.name is configured."""
        result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True
        )
        user_name = result.stdout.strip()
        assert user_name, "Git user.name is not configured"

    def test_git_user_email_configured(self):
        """Test that git user.email is configured."""
        result = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True,
            text=True
        )
        user_email = result.stdout.strip()
        assert user_email, "Git user.email is not configured"


class TestValidateGitStateFunction:
    """Tests for the validate_git_state() function."""

    def test_validate_git_state_returns_true_when_all_checks_pass(self):
        """Test that validate_git_state() returns True when all checks pass."""
        from git_validation import validate_git_state

        result = validate_git_state()
        assert result is True

    def test_validate_git_state_raises_error_on_wrong_branch(self, monkeypatch):
        """Test that validate_git_state() raises error when on wrong branch."""
        from git_validation import validate_git_state

        # Store the original subprocess.run before mocking
        original_run = subprocess.run

        # Mock subprocess.run to return wrong branch name
        def mock_run(*args, **kwargs):
            if args[0][0:2] == ["git", "rev-parse"] and "--abbrev-ref" in args[0]:
                result = subprocess.CompletedProcess(
                    args=args[0],
                    returncode=0,
                    stdout="wrong-branch\n",
                    stderr=""
                )
                return result
            # Call the original subprocess.run for other commands
            return original_run(*args, **kwargs)

        monkeypatch.setattr(subprocess, "run", mock_run)

        with pytest.raises(ValueError, match="Expected branch 'feat/markdown-file-create-cea132'"):
            validate_git_state()

    def test_validate_git_state_raises_error_on_dirty_working_tree(self, monkeypatch):
        """Test that validate_git_state() raises error when working tree is dirty."""
        from git_validation import validate_git_state

        # Store the original subprocess.run before mocking
        original_run = subprocess.run

        # Mock subprocess.run to return dirty status
        def mock_run(*args, **kwargs):
            if args[0][0:2] == ["git", "status"]:
                result = subprocess.CompletedProcess(
                    args=args[0],
                    returncode=0,
                    stdout=" M some_file.py\n",
                    stderr=""
                )
                return result
            # Call the original subprocess.run for other commands
            return original_run(*args, **kwargs)

        monkeypatch.setattr(subprocess, "run", mock_run)

        with pytest.raises(ValueError, match="Working tree is dirty"):
            validate_git_state()

    def test_validate_git_state_raises_error_on_unconfigured_user_name(self, monkeypatch):
        """Test that validate_git_state() raises error when git user.name is not configured."""
        from git_validation import validate_git_state

        # Store the original subprocess.run before mocking
        original_run = subprocess.run

        # Mock subprocess.run to return empty user.name
        def mock_run(*args, **kwargs):
            if args[0][0:2] == ["git", "config"] and "user.name" in args[0]:
                result = subprocess.CompletedProcess(
                    args=args[0],
                    returncode=1,
                    stdout="",
                    stderr="error: key does not contain a section: user.name"
                )
                return result
            # Call the original subprocess.run for other commands
            return original_run(*args, **kwargs)

        monkeypatch.setattr(subprocess, "run", mock_run)

        with pytest.raises(ValueError, match="Git user.name is not configured"):
            validate_git_state()

    def test_validate_git_state_raises_error_on_unconfigured_user_email(self, monkeypatch):
        """Test that validate_git_state() raises error when git user.email is not configured."""
        from git_validation import validate_git_state

        # Store the original subprocess.run before mocking
        original_run = subprocess.run

        # Mock subprocess.run to return empty user.email
        def mock_run(*args, **kwargs):
            if args[0][0:2] == ["git", "config"] and "user.email" in args[0]:
                result = subprocess.CompletedProcess(
                    args=args[0],
                    returncode=1,
                    stdout="",
                    stderr="error: key does not contain a section: user.email"
                )
                return result
            # Call the original subprocess.run for other commands
            return original_run(*args, **kwargs)

        monkeypatch.setattr(subprocess, "run", mock_run)

        with pytest.raises(ValueError, match="Git user.email is not configured"):
            validate_git_state()
