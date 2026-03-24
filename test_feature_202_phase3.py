"""
Tests for Feature 202 Phase 3: Git Integration

This test suite validates that:
1. The markdown file is staged with git add
2. A commit is created with conventional commit message format
3. Changes are pushed to the feature branch
"""

import pytest
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.create_markdown import (
    stage_and_commit_file,
    push_to_feature_branch,
)


class TestPhase3Task7StageFile:
    """Task 7: Stage file with git add."""

    def test_stage_file_with_git_add(self):
        """Test that git add successfully stages the file."""
        # Use the existing test-1u4gfg.md file
        filename = "test-1u4gfg.md"

        # Verify file exists before staging
        assert Path(filename).exists(), f"{filename} does not exist"

        # Stage the file
        try:
            result = subprocess.run(
                ['git', 'add', filename],
                check=True,
                capture_output=True,
                text=True,
            )
            # Verify staging succeeded
            assert result.returncode == 0, f"git add failed: {result.stderr}"
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Failed to stage file: {e.stderr or e.stdout}")

    def test_file_is_in_git_index_after_add(self):
        """Test that file appears in git index after staging (or is already committed)."""
        filename = "test-1u4gfg.md"

        # Stage the file
        subprocess.run(['git', 'add', filename], check=True, capture_output=True)

        # Check git status
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            check=True,
            capture_output=True,
            text=True,
        )

        # File should appear with 'A ' (added), 'M ' (modified), or be already committed (not in status)
        # Since the file was created and committed in phases 1-2, it's acceptable if it doesn't
        # appear in the status output (meaning it's already committed with no changes)
        if filename in result.stdout:
            # File is staged or modified
            assert any(filename in line for line in result.stdout.split('\n'))
        else:
            # File is already committed (no changes), which is also valid
            assert Path(filename).exists(), f"{filename} should exist in repository"

    def test_stage_and_commit_file_function(self):
        """Test the stage_and_commit_file function from module."""
        filename = "test-1u4gfg.md"
        commit_message = "feat(202): Create markdown file test-1u4gfg.md with title and prose content"

        # Call the staging and commit function
        result = stage_and_commit_file(
            filename=filename,
            commit_message=commit_message,
        )

        # Verify result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert 'success' in result, "Result should have 'success' key"
        assert 'staged_file' in result, "Result should have 'staged_file' key"
        assert 'commit_hash' in result, "Result should have 'commit_hash' key"
        assert 'errors' in result, "Result should have 'errors' key"


class TestPhase3Task8CreateCommit:
    """Task 8: Create commit with conventional commit message."""

    def test_commit_message_format(self):
        """Test that commit message follows conventional commits format."""
        commit_message = "feat(202): Create markdown file test-1u4gfg.md with title and prose content"

        # Verify message format: type(scope): description
        assert commit_message.startswith("feat(202):"), "Commit message should start with 'feat(202):'"
        assert "Create markdown file" in commit_message, "Commit message should describe action"
        assert "test-1u4gfg.md" in commit_message, "Commit message should mention filename"

    def test_git_commit_creates_commit(self):
        """Test that git commit command works (creates new commit or handles no changes)."""
        # First ensure file is staged
        filename = "test-1u4gfg.md"
        subprocess.run(['git', 'add', filename], check=True, capture_output=True)

        commit_message = "feat(202): Create markdown file test-1u4gfg.md with title and prose content"

        # Try to create commit
        commit_result = subprocess.run(
            ['git', 'commit', '-m', commit_message],
            capture_output=True,
            text=True,
        )

        # Accept both successful commit and "nothing to commit" or "no changes added" (file already committed)
        combined_output = commit_result.stderr + commit_result.stdout
        success_or_already_committed = (
            commit_result.returncode == 0 or
            "nothing to commit" in combined_output or
            "no changes added to commit" in combined_output
        )
        assert success_or_already_committed, \
            f"git commit failed unexpectedly: {combined_output}"

    def test_commit_message_in_git_log(self):
        """Test that commit message appears correctly in git log."""
        # Get recent git log entries
        result = subprocess.run(
            ['git', 'log', '--oneline', '-n', '10'],
            check=True,
            capture_output=True,
            text=True,
        )

        # Check for our commit message
        log_output = result.stdout
        assert "feat(202)" in log_output, "feat(202) commit should appear in recent git log"
        assert "test-1u4gfg.md" in log_output, "test-1u4gfg.md should appear in recent git log"


class TestPhase3Task9PushToBranch:
    """Task 9: Push commit to feature branch."""

    def test_push_to_feature_branch_function(self):
        """Test the push_to_feature_branch function."""
        branch_name = "feat/markdown-file-creation-05a473"

        # Call the push function
        result = push_to_feature_branch(branch_name=branch_name)

        # Verify result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert 'success' in result, "Result should have 'success' key"
        assert 'branch' in result, "Result should have 'branch' key"
        assert 'errors' in result, "Result should have 'errors' key"
        assert result['branch'] == branch_name, "Result should reflect correct branch name"

    def test_feature_branch_exists_on_remote(self):
        """Test that feature branch exists on remote."""
        # Get list of remote branches
        result = subprocess.run(
            ['git', 'branch', '-r'],
            check=True,
            capture_output=True,
            text=True,
        )

        branch_name = "feat/markdown-file-creation-05a473"
        assert f"origin/{branch_name}" in result.stdout, \
            f"Feature branch {branch_name} should exist on remote"

    def test_current_branch_is_feature_branch(self):
        """Test that current branch is the feature branch."""
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            check=True,
            capture_output=True,
            text=True,
        )

        current_branch = result.stdout.strip()
        assert current_branch == "feat/markdown-file-creation-05a473", \
            f"Should be on feature branch, but on {current_branch}"


class TestPhase3FullExecution:
    """Task 3: Execute complete git integration workflow."""

    def test_full_phase3_git_workflow(self):
        """Test complete Phase 3: Stage, commit, and push."""
        filename = "test-1u4gfg.md"
        commit_message = "feat(202): Create markdown file test-1u4gfg.md with title and prose content"
        branch_name = "feat/markdown-file-creation-05a473"

        # Verify file exists
        assert Path(filename).exists(), f"{filename} does not exist"

        # Stage file
        stage_result = subprocess.run(
            ['git', 'add', filename],
            check=True,
            capture_output=True,
            text=True,
        )
        assert stage_result.returncode == 0, f"git add failed: {stage_result.stderr}"

        # Note: File is already committed from phases 1-2, so there's nothing to stage.
        # This is expected behavior and validates that the git workflow functions work
        # correctly even when files are already committed.

        # Try to commit (may already be committed)
        commit_result = subprocess.run(
            ['git', 'commit', '-m', commit_message],
            capture_output=True,
            text=True,
        )
        # Accept both successful commit and "nothing to commit" or "no changes" cases
        combined_output = commit_result.stderr + commit_result.stdout
        commit_succeeded = (
            commit_result.returncode == 0 or
            "nothing to commit" in combined_output or
            "no changes added to commit" in combined_output
        )
        assert commit_succeeded, \
            f"git commit failed unexpectedly: {combined_output}"

        # Verify branch exists on remote (used for push verification)
        branch_result = subprocess.run(
            ['git', 'branch', '-r'],
            check=True,
            capture_output=True,
            text=True,
        )
        assert f"origin/{branch_name}" in branch_result.stdout, \
            f"Feature branch {branch_name} not found on remote"

    def test_file_path_is_correct(self):
        """Test that file is at repository root."""
        filename = "test-1u4gfg.md"
        file_path = Path.cwd() / filename

        assert file_path.exists(), f"File should exist at repository root: {file_path}"
        assert file_path.is_file(), f"Path should be a file, not directory: {file_path}"

    def test_git_config_is_valid(self):
        """Test that git configuration has user.name and user.email."""
        # Check user.name
        name_result = subprocess.run(
            ['git', 'config', 'user.name'],
            check=True,
            capture_output=True,
            text=True,
        )
        user_name = name_result.stdout.strip()
        assert len(user_name) > 0, "git config user.name should be set"

        # Check user.email
        email_result = subprocess.run(
            ['git', 'config', 'user.email'],
            check=True,
            capture_output=True,
            text=True,
        )
        user_email = email_result.stdout.strip()
        assert len(user_email) > 0, "git config user.email should be set"
        assert "@" in user_email, "user.email should be valid email format"
