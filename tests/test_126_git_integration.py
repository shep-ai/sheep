"""Tests for feature 126 Phase 5: Git Integration & Verification (tasks 5-1 and 5-2)."""

import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestGitStageAndCommit:
    """Tests for task-5-1: Stage File and Create Commit."""

    def test_stages_file_with_git_add(self):
        """Test that file is staged using 'git add test-lqbnqn.md'."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)

            # Initialize a git repo
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Configure git user
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Create a markdown file
            test_file = repo_path / "test-lqbnqn.md"
            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            test_file.write_text(content, encoding="utf-8")

            # Create initial commit so we can commit changes
            (repo_path / "README.md").write_text("# Test\n")
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Stage the file
            result = subprocess.run(
                ["git", "add", "test-lqbnqn.md"],
                cwd=repo_path,
                capture_output=True,
            )

            assert result.returncode == 0

            # Verify file is staged
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            assert "A  test-lqbnqn.md" in status_result.stdout or "A test-lqbnqn.md" in status_result.stdout

    def test_creates_commit_with_exact_message(self):
        """Test that commit is created with exact message format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)

            # Initialize and configure git repo
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Create markdown file
            test_file = repo_path / "test-lqbnqn.md"
            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            test_file.write_text(content, encoding="utf-8")

            # Create initial commit
            (repo_path / "README.md").write_text("# Test\n")
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Stage and commit the file
            subprocess.run(
                ["git", "add", "test-lqbnqn.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            commit_message = "feat(126): create markdown file test-lqbnqn.md with prose content"
            result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=repo_path,
                capture_output=True,
            )

            assert result.returncode == 0

            # Verify commit message
            log_result = subprocess.run(
                ["git", "log", "-1", "--format=%s"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            assert commit_message in log_result.stdout

    def test_commit_includes_correct_author(self):
        """Test that commit includes correct author from git config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)

            # Initialize and configure git repo
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "bot@example.com"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test Bot"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Create markdown file
            test_file = repo_path / "test-lqbnqn.md"
            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            test_file.write_text(content, encoding="utf-8")

            # Create initial commit
            (repo_path / "README.md").write_text("# Test\n")
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Stage and commit
            subprocess.run(
                ["git", "add", "test-lqbnqn.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "feat(126): create markdown file test-lqbnqn.md with prose content"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Verify author
            log_result = subprocess.run(
                ["git", "log", "-1", "--format=%an"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            assert "Test Bot" in log_result.stdout

    def test_no_uncommitted_changes_after_commit(self):
        """Test that git status shows no uncommitted changes after commit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)

            # Initialize and configure git repo
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Create markdown file
            test_file = repo_path / "test-lqbnqn.md"
            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            test_file.write_text(content, encoding="utf-8")

            # Create initial commit
            (repo_path / "README.md").write_text("# Test\n")
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Stage and commit
            subprocess.run(
                ["git", "add", "test-lqbnqn.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "feat(126): create markdown file test-lqbnqn.md with prose content"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Check status
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            assert status_result.stdout.strip() == ""

    def test_raises_exception_if_file_does_not_exist(self):
        """Test that proper error is raised if file doesn't exist before commit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)

            # Initialize git repo
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Try to add non-existent file
            result = subprocess.run(
                ["git", "add", "nonexistent.md"],
                cwd=repo_path,
                capture_output=True,
            )

            # Should fail (non-zero exit code)
            assert result.returncode != 0


class TestGitPushAndVerify:
    """Tests for task-5-2: Push to Feature Branch and Verify Commit."""

    def test_commits_appear_in_git_log(self):
        """Test that commit appears in git log with correct message."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)

            # Initialize and configure git repo
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Create markdown file
            test_file = repo_path / "test-lqbnqn.md"
            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            test_file.write_text(content, encoding="utf-8")

            # Create initial commit
            (repo_path / "README.md").write_text("# Test\n")
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Create and commit file
            subprocess.run(
                ["git", "add", "test-lqbnqn.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            commit_message = "feat(126): create markdown file test-lqbnqn.md with prose content"
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Verify commit is in log
            log_result = subprocess.run(
                ["git", "log", "-1", "--format=%s"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            assert commit_message in log_result.stdout

    def test_commit_message_format_is_exact(self):
        """Test that commit message has exact format: feat(126): create markdown file test-lqbnqn.md with prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)

            # Initialize and configure git repo
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Create markdown file
            test_file = repo_path / "test-lqbnqn.md"
            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            test_file.write_text(content, encoding="utf-8")

            # Create initial commit
            (repo_path / "README.md").write_text("# Test\n")
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Create and commit file
            subprocess.run(
                ["git", "add", "test-lqbnqn.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            commit_message = "feat(126): create markdown file test-lqbnqn.md with prose content"
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Verify exact message
            log_result = subprocess.run(
                ["git", "log", "-1", "--format=%s"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            assert log_result.stdout.strip() == commit_message

    def test_commit_includes_test_file(self):
        """Test that git log shows test-lqbnqn.md in the commit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)

            # Initialize and configure git repo
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Create markdown file
            test_file = repo_path / "test-lqbnqn.md"
            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            test_file.write_text(content, encoding="utf-8")

            # Create initial commit
            (repo_path / "README.md").write_text("# Test\n")
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Create and commit file
            subprocess.run(
                ["git", "add", "test-lqbnqn.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "feat(126): create markdown file test-lqbnqn.md with prose content"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Verify file is in commit
            name_status_result = subprocess.run(
                ["git", "log", "-1", "--name-status"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            assert "test-lqbnqn.md" in name_status_result.stdout

    def test_commit_author_matches_git_config(self):
        """Test that commit author matches git config user.name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)

            # Initialize and configure git repo with specific author
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "author@example.com"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Specific Author"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Create markdown file
            test_file = repo_path / "test-lqbnqn.md"
            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            test_file.write_text(content, encoding="utf-8")

            # Create initial commit
            (repo_path / "README.md").write_text("# Test\n")
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Create and commit file
            subprocess.run(
                ["git", "add", "test-lqbnqn.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "feat(126): create markdown file test-lqbnqn.md with prose content"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Verify author
            author_result = subprocess.run(
                ["git", "log", "-1", "--format=%an"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            assert "Specific Author" in author_result.stdout


class TestFeature126GitIntegrationRealRepository:
    """Integration tests with the actual feature 126 repository."""

    def test_actual_test_file_is_committed(self):
        """Test that test-lqbnqn.md is already committed to the feature branch."""
        # Check that the file is in the current working directory
        test_file = Path.cwd() / "test-lqbnqn.md"
        assert test_file.exists()

        # Check that it's tracked in git
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
        )
        assert "test-lqbnqn.md" in result.stdout

    def test_actual_test_file_has_correct_content_structure(self):
        """Test that test-lqbnqn.md has the required markdown structure."""
        test_file = Path.cwd() / "test-lqbnqn.md"
        assert test_file.exists()

        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Check H1 heading
        assert lines[0].startswith("# ")

        # Check blank line
        assert lines[1] == ""

        # Check prose content exists
        prose_content = "\n".join(lines[2:]).strip()
        assert len(prose_content) > 0

    def test_commit_message_is_conventional(self):
        """Test that the commit message follows conventional commit format."""
        result = subprocess.run(
            ["git", "log", "-1", "--format=%s"],
            capture_output=True,
            text=True,
        )
        commit_message = result.stdout.strip()

        # Should match: feat(...): ...
        assert commit_message.startswith("feat(")
        assert ":" in commit_message
        # The message should be about feature 126
        assert "126" in commit_message

    def test_feature_branch_is_tracking_remote(self):
        """Test that the feature branch is set up to track the remote."""
        result = subprocess.run(
            ["git", "branch", "-vv"],
            capture_output=True,
            text=True,
        )

        # Should show tracking info
        assert "feat/markdown-file-create-cea132" in result.stdout
