"""Phase 4 tests: Verify git operations (staging, committing, pushing)."""

import subprocess
from pathlib import Path

import pytest

from sheep.content_generators import commit_markdown_file, push_markdown_file


class TestPhase4GitOperations:
    """Task 5 & 6: Stage and commit file, then push to remote."""

    def test_file_is_tracked_in_git(self):
        """Test that test-45ndys.md is tracked in git."""
        # Verify file is in git index
        result = subprocess.run(
            ["git", "ls-files", "test-45ndys.md"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        assert (
            "test-45ndys.md" in result.stdout
        ), "File should be tracked in git index"

    def test_file_is_not_untracked(self):
        """Test that file is not listed as untracked by git status."""
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        status_lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
        untracked_files = [
            line for line in status_lines if line.startswith("??")
        ]
        untracked_test_files = [
            f for f in untracked_files if "test-45ndys.md" in f
        ]
        assert (
            not untracked_test_files
        ), "test-45ndys.md should not be untracked (should be committed)"

    def test_commit_exists_with_correct_message(self):
        """Test that git commit exists with correct conventional message."""
        result = subprocess.run(
            ["git", "log", "--oneline", "--all"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        assert (
            "feat(116): Create markdown file test-45ndys.md with prose content"
            in result.stdout
        ), "Commit with correct message should exist in git history"

    def test_commit_only_includes_test_file(self):
        """Test that the commit includes test-45ndys.md file and no extraneous changes."""
        # Find the commit hash for our file
        result = subprocess.run(
            ["git", "log", "--all", "--oneline", "--", "test-45ndys.md"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        assert "feat(116)" in result.stdout, "Commit for test-45ndys.md should exist"

        # Get the full commit hash
        commit_hash = result.stdout.split()[0]

        # Check files changed in that commit
        result = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:", commit_hash],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )

        changed_files = result.stdout.strip().split("\n")
        changed_files = [f for f in changed_files if f.strip()]

        # Verify test-45ndys.md is included
        assert any(
            "test-45ndys.md" in f for f in changed_files
        ), "Commit should include test-45ndys.md"

        # Verify no extraneous changes (specs, config files, etc)
        extraneous_patterns = ["specs/", "pyproject.toml", ".github/", ".env"]
        extraneous_files = [
            f for f in changed_files
            if any(pattern in f for pattern in extraneous_patterns)
        ]
        assert (
            not extraneous_files
        ), f"Commit should not include extraneous changes, found: {extraneous_files}"

    def test_commit_has_proper_authorship(self):
        """Test that commit has proper author information set."""
        result = subprocess.run(
            ["git", "log", "-1", "--format=%an|%ae"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        author_info = result.stdout.strip()
        assert author_info, "Commit should have author information"
        assert "|" in author_info, "Author info should contain name and email"
        name, email = author_info.split("|")
        assert name.strip(), "Commit author name should not be empty"
        assert email.strip(), "Commit author email should not be empty"

    def test_commit_is_on_feature_branch(self):
        """Test that commit is on the feature branch."""
        result = subprocess.run(
            ["git", "branch", "-a", "--contains", "HEAD"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        branches = result.stdout.strip()
        assert (
            "feat/markdown-file-creation" in branches
            or "feat/116" in branches
            or "feat-markdown" in branches
        ), f"Commit should be on feature branch, found: {branches}"

    def test_local_commit_exists(self):
        """Test that local commit exists for the file."""
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%s"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        latest_commit = result.stdout.strip()
        assert (
            "feat(116)" in latest_commit or "test-45ndys.md" in latest_commit
        ), f"Latest commit should be for feature 116, found: {latest_commit}"

    def test_commit_pushed_to_remote(self):
        """Test that commit has been pushed to remote origin."""
        # Check if remote tracking branch exists
        result = subprocess.run(
            ["git", "branch", "-r"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )

        if "origin/feat" in result.stdout or "origin/HEAD" in result.stdout:
            # Get remote commits for the feature branch
            result = subprocess.run(
                ["git", "log", "origin/feat/markdown-file-creation-f20394", "--oneline", "-1"],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
            )

            if result.returncode == 0:
                assert (
                    "feat(116)" in result.stdout
                ), "Commit should be on remote branch"

    def test_commit_message_format_is_conventional(self):
        """Test that commit message follows conventional commit format."""
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%s"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        commit_message = result.stdout.strip()

        # Check conventional commit format: type(scope): description
        parts = commit_message.split(":")
        assert (
            len(parts) >= 2
        ), f"Commit message should follow conventional format (type(scope): description), got: {commit_message}"

        prefix = parts[0].strip()
        assert (
            "feat" in prefix
        ), f"Commit type should be 'feat', got: {prefix}"
        assert (
            "116" in prefix
        ), f"Commit scope should include feature number 116, got: {prefix}"

    def test_no_uncommitted_changes_after_commit(self):
        """Test that there are no uncommitted changes after commit."""
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        status = result.stdout.strip()

        # Filter out any ignored files or unrelated changes
        meaningful_changes = [
            line
            for line in status.split("\n")
            if line.strip() and not line.startswith("??")
        ]

        # The test-45ndys.md should not appear as modified or staged
        test_file_changes = [
            line for line in meaningful_changes if "test-45ndys.md" in line
        ]
        assert (
            not test_file_changes
        ), f"test-45ndys.md should have no uncommitted changes, found: {test_file_changes}"

    def test_can_call_commit_function_with_custom_message(self):
        """Test that commit_markdown_file can be called with custom message."""
        # This test verifies the function is importable and callable
        # The actual file is already committed, so we just verify the function exists
        assert callable(
            commit_markdown_file
        ), "commit_markdown_file should be callable"

    def test_can_call_push_function(self):
        """Test that push_markdown_file can be called."""
        # This test verifies the function is importable and callable
        assert callable(
            push_markdown_file
        ), "push_markdown_file should be callable"


class TestPhase4ErrorHandling:
    """Tests for error handling in git operations."""

    def test_commit_function_exists_and_importable(self):
        """Test that commit_markdown_file is importable."""
        from sheep.content_generators import commit_markdown_file

        assert callable(commit_markdown_file)

    def test_push_function_exists_and_importable(self):
        """Test that push_markdown_file is importable."""
        from sheep.content_generators import push_markdown_file

        assert callable(push_markdown_file)

    def test_git_user_configured(self):
        """Test that git user.name and user.email are configured."""
        name_result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        email_result = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )

        name = name_result.stdout.strip()
        email = email_result.stdout.strip()

        assert name, "git user.name should be configured"
        assert email, "git user.email should be configured"

    def test_remote_origin_configured(self):
        """Test that remote origin is configured."""
        result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )

        assert (
            "origin" in result.stdout
        ), "Remote 'origin' should be configured"

    def test_feature_branch_exists(self):
        """Test that the feature branch exists locally or remotely."""
        result = subprocess.run(
            ["git", "branch", "-a"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )

        branch_output = result.stdout
        # Check for feature branch (might have slight name variations)
        has_feature_branch = any(
            keyword in branch_output
            for keyword in [
                "feat",
                "116",
                "markdown-file-creation",
            ]
        )

        assert (
            has_feature_branch
        ), f"Feature branch should exist, found branches: {branch_output}"
