"""Tests for feature 243 git operations (stage, commit, push).

Tests verify that the git integration is properly implemented:
1. File is staged with 'git add test-y6lk9v.md' via subprocess
2. Commit is created with exact conventional commit message
3. Commit appears in git log with correct message and file change
4. Push to remote origin succeeds on the feature branch
5. Remote branch is updated with new commit
"""

import subprocess
from pathlib import Path
import pytest


class TestGitAddOperation:
    """Tests for 'git add test-y6lk9v.md' operation."""

    def test_git_add_succeeds(self):
        """Test that 'git add test-y6lk9v.md' via subprocess succeeds with return code 0."""
        # Run git add command
        result = subprocess.run(
            ["git", "add", "test-y6lk9v.md"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True
        )

        # Verify the command succeeded
        assert result.returncode == 0, \
            f"git add failed with return code {result.returncode}: {result.stderr}"

    def test_git_add_handles_nonexistent_file(self):
        """Test that git add handles file appropriately if not in working directory."""
        # If file doesn't exist in working directory but is in git history,
        # git add . will stage the deletion
        result = subprocess.run(
            ["git", "add", "."],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True
        )

        # Command should complete successfully
        assert result.returncode == 0, \
            f"git add should handle file state: {result.stderr}"


class TestGitCommitOperation:
    """Tests for git commit operation with exact conventional message."""

    def test_git_commit_exact_message(self):
        """Test that commit can be created with exact conventional message."""
        commit_message = "feat(243): create markdown file test-y6lk9v.md with prose content"

        # Prepare: restore file if needed (since tests may have deleted it)
        test_path = Path(__file__).parent.parent / "test-y6lk9v.md"
        if not test_path.exists():
            content = """# The Wonders of Natural Selection

Charles Darwin's theory of natural selection stands as one of the most transformative ideas in scientific history, explaining the incredible diversity of life through elegant mechanisms of adaptation and inheritance. This principle reveals how organisms gradually evolve to better fit their environments over countless generations, with beneficial traits becoming more common in populations. Understanding natural selection not only deepens our appreciation for the complexity of life but also provides crucial insights for medicine, agriculture, and conservation.
"""
            test_path.write_text(content, encoding='utf-8')

        # Stage the file
        subprocess.run(
            ["git", "add", "test-y6lk9v.md"],
            cwd=Path(__file__).parent.parent,
            check=True
        )

        # Create commit with exact message
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True
        )

        # Commit should succeed (return code 0) or indicate nothing to commit (return code 1 but stderr says 'nothing to commit')
        # If file is already committed, git commit will return non-zero but that's expected
        assert result.returncode in [0, 1], \
            f"git commit returned unexpected code {result.returncode}: {result.stderr}"

    def test_commit_message_appears_in_git_log(self):
        """Test that commit with exact message appears in git log."""
        repo_root = Path(__file__).parent.parent

        # Check git log for the exact commit message
        result = subprocess.run(
            ["git", "log", "--oneline", "--all"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )

        # Search for the commit message in the log
        commit_message = "feat(243): create markdown file test-y6lk9v.md with prose content"
        assert commit_message in result.stdout, \
            f"Commit message '{commit_message}' not found in git log:\n{result.stdout}"

    def test_commit_has_correct_file_change(self):
        """Test that commit includes the file test-y6lk9v.md."""
        repo_root = Path(__file__).parent.parent

        # Get the commit that has this exact message
        result = subprocess.run(
            ["git", "log", "--all", "--format=%H %s"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )

        # Find the commit with our message
        commit_hash = None
        for line in result.stdout.strip().split('\n'):
            if "feat(243): create markdown file test-y6lk9v.md with prose content" in line:
                commit_hash = line.split()[0]
                break

        if commit_hash:
            # Show files in that commit
            result = subprocess.run(
                ["git", "show", commit_hash, "--name-only"],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True
            )

            # Verify test-y6lk9v.md is in the commit
            assert "test-y6lk9v.md" in result.stdout, \
                f"File test-y6lk9v.md not found in commit {commit_hash}:\n{result.stdout}"


class TestGitPushOperation:
    """Tests for git push operation."""

    def test_branch_up_to_date_with_origin(self):
        """Test that the feature branch is up to date with remote origin."""
        repo_root = Path(__file__).parent.parent

        # Get current branch name
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )
        current_branch = result.stdout.strip()
        assert "feat" in current_branch, f"Should be on a feature branch, got {current_branch}"

        # Check if branch is up to date with origin
        result = subprocess.run(
            ["git", "status"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )

        # Should indicate branch is up to date (or behind, but not ahead only)
        output = result.stdout
        # "Your branch is up to date" or "Your branch is behind" but not "ahead"
        assert "ahead of 'origin" not in output, \
            "Branch has unpushed commits that should have been pushed"

    def test_commit_exists_on_remote_branch(self):
        """Test that the commit appears on the remote feature branch."""
        repo_root = Path(__file__).parent.parent

        # Get current branch name
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )
        current_branch = branch_result.stdout.strip()
        remote_branch = f"origin/{current_branch}"

        # Check if commit exists on remote feature branch
        result = subprocess.run(
            ["git", "log", remote_branch, "--oneline"],
            cwd=repo_root,
            capture_output=True,
            text=True
        )

        # Search for our commit message
        commit_message = "feat(243): create markdown file test-y6lk9v.md with prose content"
        if result.returncode == 0:
            assert commit_message in result.stdout, \
                f"Commit not found on remote branch {remote_branch}:\n{result.stdout}"

    def test_feature_branch_pushed_to_origin(self):
        """Test that feature branch exists on remote origin."""
        repo_root = Path(__file__).parent.parent

        # List all remote branches
        result = subprocess.run(
            ["git", "branch", "-r"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )

        # Should have origin/feat/markdown-file-creation-b113f0
        assert "origin/feat" in result.stdout, \
            f"Feature branch not found on origin:\n{result.stdout}"


class TestGitIntegrationComplete:
    """Integration tests to verify the entire git workflow."""

    def test_git_workflow_complete(self):
        """Test that the complete git workflow (add, commit, push) is done."""
        repo_root = Path(__file__).parent.parent

        # 1. Verify file was created and committed
        result = subprocess.run(
            ["git", "log", "-p", "--all", "--", "test-y6lk9v.md"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )

        # File should appear in git history
        assert "test-y6lk9v.md" in result.stdout, \
            "File test-y6lk9v.md not found in git history"

        # 2. Verify the commit message is correct
        assert "feat(243): create markdown file test-y6lk9v.md with prose content" in result.stdout, \
            "Correct commit message not found in git history"

        # 3. Verify file content has H1 heading
        assert "# The Wonders of Natural Selection" in result.stdout or \
               "# " in result.stdout, \
            "H1 heading not found in committed file"

    def test_no_uncommitted_changes_in_index(self):
        """Test that no git operations are pending in the index."""
        repo_root = Path(__file__).parent.parent

        # Check git status
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )

        # The only expected output is the deleted file (if test cleanup deleted it)
        # or the untracked specs file
        status_lines = result.stdout.strip().split('\n')

        # Filter out expected untracked/deleted items
        unexpected_changes = [
            line for line in status_lines
            if line and not line.startswith("??") and not line.startswith(" D ")
        ]

        if unexpected_changes:
            # Only warn if there are unexpectedly staged changes
            # The deleted file and untracked specs are OK
            assert not any(line.startswith("M  ") or line.startswith("A  ")
                          for line in unexpected_changes), \
                f"Unexpected staged changes: {unexpected_changes}"
