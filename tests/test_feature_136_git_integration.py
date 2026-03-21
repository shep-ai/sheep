"""Tests for feature 136: markdown file creation - git integration phase.

Tests cover git integration tasks:
- Task 3: Stage file and create conventional commit
- Task 4: Push changes to remote origin
"""

import subprocess
from pathlib import Path

import pytest


class TestTask3GitStageAndCommit:
    """Tests for task 3: Stage file and create conventional commit (Verification Tests)."""

    FEATURE_FILENAME = "test-k8bid7.md"
    COMMIT_MESSAGE = "feat(136): Create markdown file test-k8bid7.md"

    def test_file_exists_in_repository_root(self):
        """Test that test-k8bid7.md exists in repository root."""
        filepath = Path(self.FEATURE_FILENAME)
        assert filepath.exists(), f"File {self.FEATURE_FILENAME} should exist"
        assert filepath.is_file(), f"{self.FEATURE_FILENAME} should be a regular file"

    def test_file_is_committed_not_untracked(self):
        """Test that file is committed and not in untracked files."""
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        )
        # File should NOT appear in status output (it's committed)
        assert self.FEATURE_FILENAME not in result.stdout, (
            f"File should be committed, got in status: {result.stdout}"
        )

    def test_commit_exists_with_correct_message(self):
        """Test that commit exists in git log with exact required message."""
        result = subprocess.run(
            ["git", "log", "--oneline", "-20"],
            capture_output=True,
            text=True,
            check=True,
        )

        assert self.COMMIT_MESSAGE in result.stdout, (
            f"Commit message should be in log, got: {result.stdout}"
        )

    def test_commit_message_is_exact_format(self):
        """Test that most recent commit message is in exact required format."""
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%s"],
            capture_output=True,
            text=True,
            check=True,
        )

        assert result.stdout.strip() == self.COMMIT_MESSAGE, (
            f"Commit message should be exactly '{self.COMMIT_MESSAGE}', got: {result.stdout.strip()}"
        )

    def test_commit_is_on_feature_branch(self):
        """Test that commit is on the feature branch."""
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )

        branch_name = result.stdout.strip()
        assert "feat/markdown-file-creation-b34540" in branch_name, (
            f"Should be on feature branch, got: {branch_name}"
        )

    def test_commit_includes_file_change(self):
        """Test that HEAD commit includes the markdown file."""
        result = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )

        files = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        assert self.FEATURE_FILENAME in files, (
            f"Commit should include {self.FEATURE_FILENAME}, got: {files}"
        )

    def test_commit_contains_only_markdown_file(self):
        """Test that commit contains only the markdown file (no other changes)."""
        result = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )

        files = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        assert len(files) == 1, (
            f"Commit should only contain {self.FEATURE_FILENAME}, got {len(files)} files: {files}"
        )
        assert files[0] == self.FEATURE_FILENAME, (
            f"File should be {self.FEATURE_FILENAME}, got: {files[0]}"
        )

    def test_commit_follows_conventional_commits_format(self):
        """Test that commit message follows Conventional Commits specification."""
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%s"],
            capture_output=True,
            text=True,
            check=True,
        )

        msg = result.stdout.strip()
        # Should start with feat(NUMBER):
        assert msg.startswith("feat("), "Commit must start with 'feat('"
        assert "136" in msg, "Commit must include feature number 136"
        assert ":" in msg, "Commit must have colon separator"
        assert self.FEATURE_FILENAME in msg, "Commit message must include filename"


class TestTask4GitPush:
    """Tests for task 4: Push changes to remote origin (Verification Tests)."""

    FEATURE_FILENAME = "test-k8bid7.md"
    COMMIT_MESSAGE = "feat(136): Create markdown file test-k8bid7.md"
    FEATURE_BRANCH = "feat/markdown-file-creation-b34540"

    def test_local_commit_exists(self):
        """Test that commit exists locally."""
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )

        commit_hash = result.stdout.strip()
        assert len(commit_hash) == 40, "Should have a valid commit hash"

    def test_remote_has_feature_branch(self):
        """Test that remote origin has the feature branch."""
        result = subprocess.run(
            ["git", "ls-remote", "--heads", "origin", self.FEATURE_BRANCH],
            capture_output=True,
            text=True,
            check=True,
        )

        assert self.FEATURE_BRANCH in result.stdout, (
            f"Remote should have {self.FEATURE_BRANCH}, got: {result.stdout}"
        )

    def test_local_branch_tracks_remote(self):
        """Test that local branch tracks remote branch."""
        result = subprocess.run(
            ["git", "rev-parse", "@{u}"],
            capture_output=True,
            text=True,
        )

        # Should succeed (exit code 0) and return a commit hash
        assert result.returncode == 0, (
            "Local branch should have upstream tracking"
        )
        assert len(result.stdout.strip()) == 40, (
            "Upstream should be a valid commit hash"
        )

    def test_local_and_remote_commit_match(self):
        """Test that local HEAD commit matches remote branch commit."""
        result_local = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )

        result_remote = subprocess.run(
            ["git", "rev-parse", f"origin/{self.FEATURE_BRANCH}"],
            capture_output=True,
            text=True,
            check=True,
        )

        local_commit = result_local.stdout.strip()
        remote_commit = result_remote.stdout.strip()

        assert local_commit == remote_commit, (
            f"Local commit {local_commit} should match remote {remote_commit}"
        )

    def test_remote_branch_has_our_commit_message(self):
        """Test that remote branch has our commit with correct message."""
        result = subprocess.run(
            [
                "git",
                "log",
                f"origin/{self.FEATURE_BRANCH}",
                "-1",
                "--pretty=format:%s",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        assert result.stdout.strip() == self.COMMIT_MESSAGE, (
            f"Remote commit message should be '{self.COMMIT_MESSAGE}', got: {result.stdout.strip()}"
        )

    def test_file_is_on_remote_branch(self):
        """Test that our markdown file is present on remote branch."""
        result = subprocess.run(
            ["git", "ls-tree", "-r", f"origin/{self.FEATURE_BRANCH}", "--name-only"],
            capture_output=True,
            text=True,
            check=True,
        )

        assert self.FEATURE_FILENAME in result.stdout, (
            f"File should be on remote, got files: {result.stdout}"
        )

    def test_remote_has_only_our_file_in_commit(self):
        """Test that remote commit contains only our markdown file."""
        result = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:", f"origin/{self.FEATURE_BRANCH}"],
            capture_output=True,
            text=True,
            check=True,
        )

        files = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]

        assert len(files) == 1, (
            f"Remote commit should only contain {self.FEATURE_FILENAME}, got {len(files)} files: {files}"
        )
        assert files[0] == self.FEATURE_FILENAME, (
            f"File should be {self.FEATURE_FILENAME}, got: {files[0]}"
        )

    def test_feature_branch_is_up_to_date_with_remote(self):
        """Test that local branch is up to date with remote."""
        result = subprocess.run(
            ["git", "status", "--porcelain", "--branch"],
            capture_output=True,
            text=True,
            check=True,
        )

        # Should show "up to date" or no divergence
        output = result.stdout.strip()
        # The first line should indicate the branch status
        first_line = output.split("\n")[0] if output else ""

        # Should either show "gone" (deleted remote) or no "ahead/behind"
        # Since branch exists, should not show divergence
        assert "ahead" not in first_line or "behind" not in first_line, (
            f"Branch should be in sync with remote, got: {first_line}"
        )
