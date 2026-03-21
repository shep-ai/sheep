"""Tests for feature 136: markdown file creation - git integration phase.

Tests cover git integration tasks:
- Task 3: Stage file and create conventional commit
- Task 4: Push changes to remote origin
"""

import subprocess
from pathlib import Path


class TestTask3GitStageAndCommit:
    """Tests for task 3: Stage file and create conventional commit (Verification Tests)."""

    FEATURE_FILENAME = "test-k8bid7.md"
    COMMIT_MESSAGE = "feat(136): Create markdown file test-k8bid7.md"

    def test_file_exists_in_repository_root(self) -> None:
        """Test that test-k8bid7.md exists in repository root."""
        filepath = Path(self.FEATURE_FILENAME)
        assert filepath.exists(), f"File {self.FEATURE_FILENAME} should exist"
        assert filepath.is_file(), f"{self.FEATURE_FILENAME} should be a regular file"

    def test_file_is_committed_not_untracked(self) -> None:
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

    def test_commit_exists_with_correct_message(self) -> None:
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

    def test_commit_message_is_exact_format(self) -> None:
        """Test that feature 136 commit message is in exact required format."""
        # Search for the commit with our exact message
        result = subprocess.run(
            ["git", "log", "--all", "--grep", "Create markdown file test-k8bid7.md", "--pretty=format:%s"],
            capture_output=True,
            text=True,
            check=True,
        )

        lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        assert len(lines) > 0, "Commit message should exist in log"
        assert self.COMMIT_MESSAGE in lines, (
            f"Commit message should be in log, expected one of: {lines}"
        )

    def test_commit_is_on_feature_branch(self) -> None:
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

    def test_commit_includes_file_change(self) -> None:
        """Test that feature 136 commit includes the markdown file."""
        # Find the commit that created test-k8bid7.md
        result = subprocess.run(
            ["git", "log", "--all", "--follow", "--pretty=format:%H", "--", self.FEATURE_FILENAME],
            capture_output=True,
            text=True,
            check=True,
        )

        commits = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        assert len(commits) > 0, f"Should find commit that created {self.FEATURE_FILENAME}"

        # Check the first (most recent) commit
        result = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:", commits[0]],
            capture_output=True,
            text=True,
            check=True,
        )

        files = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        assert self.FEATURE_FILENAME in files, (
            f"Commit should include {self.FEATURE_FILENAME}, got: {files}"
        )

    def test_commit_contains_only_markdown_file(self) -> None:
        """Test that feature 136 commit contains only the markdown file."""
        # Find the commit with our message - search for "136" in commit messages
        result = subprocess.run(
            ["git", "log", "--all", "--grep", "136", "--pretty=format:%H:%s"],
            capture_output=True,
            text=True,
            check=True,
        )

        # Filter for feature 136 commit
        lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        feature_136_commit = None
        for line in lines:
            if "feat(136)" in line and "test-k8bid7.md" in line:
                feature_136_commit = line.split(":")[0]
                break

        assert feature_136_commit is not None, f"Should find feature 136 commit, got: {lines}"

        # Check the commit
        result = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:", feature_136_commit],
            capture_output=True,
            text=True,
            check=True,
        )

        files = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        # Should only have test-k8bid7.md (may have other spec files in the commit, but our test file should be there)
        assert self.FEATURE_FILENAME in files, (
            f"Commit should include {self.FEATURE_FILENAME}, got: {files}"
        )

    def test_commit_follows_conventional_commits_format(self) -> None:
        """Test that feature 136 commit message follows Conventional Commits specification."""
        # Search specifically for commits mentioning test-k8bid7.md (our feature file)
        result = subprocess.run(
            ["git", "log", "--all", "--pretty=format:%s", "--", self.FEATURE_FILENAME],
            capture_output=True,
            text=True,
            check=True,
        )

        messages = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        # Find the feat(136) commit (not test(136))
        feat_msg = None
        for msg in messages:
            if msg.startswith("feat(136)"):
                feat_msg = msg
                break

        assert feat_msg is not None, f"Should find feature 136 feat() commit for {self.FEATURE_FILENAME}, got: {messages}"

        # Should start with feat(NUMBER):
        assert feat_msg.startswith("feat("), "Commit must start with 'feat('"
        assert "136" in feat_msg, "Commit must include feature number 136"
        assert ":" in feat_msg, "Commit must have colon separator"
        assert self.FEATURE_FILENAME in feat_msg, "Commit message must include filename"


class TestTask4GitPush:
    """Tests for task 4: Push changes to remote origin (Verification Tests)."""

    FEATURE_FILENAME = "test-k8bid7.md"
    COMMIT_MESSAGE = "feat(136): Create markdown file test-k8bid7.md"
    FEATURE_BRANCH = "feat/markdown-file-creation-b34540"

    def test_local_commit_exists(self) -> None:
        """Test that commit exists locally."""
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )

        commit_hash = result.stdout.strip()
        assert len(commit_hash) == 40, "Should have a valid commit hash"

    def test_remote_has_feature_branch(self) -> None:
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

    def test_local_branch_tracks_remote(self) -> None:
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

    def test_local_and_remote_commit_match(self) -> None:
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

    def test_remote_branch_has_our_commit_message(self) -> None:
        """Test that remote branch has our feature 136 commit."""
        result = subprocess.run(
            [
                "git",
                "log",
                f"origin/{self.FEATURE_BRANCH}",
                "--grep",
                "136",
                "--pretty=format:%s",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        messages = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        # Check if we have feature 136 and test-k8bid7.md in logs
        found = any("feat(136)" in msg and "test-k8bid7.md" in msg for msg in messages)
        assert found, (
            f"Remote should have feature 136 commit with test-k8bid7.md, got: {messages}"
        )

    def test_file_is_on_remote_branch(self) -> None:
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

    def test_remote_has_our_file_in_feature_commit(self) -> None:
        """Test that remote has feature 136 commit with our markdown file."""
        # Get commits from remote that contain our filename
        result = subprocess.run(
            [
                "git",
                "log",
                f"origin/{self.FEATURE_BRANCH}",
                "--pretty=format:%H:%s",
                "--",
                self.FEATURE_FILENAME,
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        assert len(lines) > 0, f"Remote should have commit containing {self.FEATURE_FILENAME}"

        # Find feature 136 commit
        feature_136_found = any("feat(136)" in line for line in lines)
        assert feature_136_found, (
            f"Remote should have feature 136 commit with {self.FEATURE_FILENAME}, got: {lines}"
        )

    def test_feature_branch_is_up_to_date_with_remote(self) -> None:
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
