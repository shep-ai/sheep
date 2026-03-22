"""End-to-end integration tests for markdown file creation workflow."""

import subprocess
from pathlib import Path

import pytest

from validate_markdown_file import validate_file
from git_workflow import (
    get_current_branch,
    get_commit_message,
    is_file_tracked,
    FILENAME,
    COMMIT_MESSAGE,
)


class TestEndToEndWorkflow:
    """Integration tests for the complete markdown file creation workflow."""

    def test_file_exists_at_repo_root(self):
        """Test that test-0h4oez.md exists at the repository root."""
        # Get git root directory
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        repo_root = Path(result.stdout.strip())
        file_path = repo_root / FILENAME

        assert file_path.exists(), f"File {file_path} should exist"
        assert file_path.is_file(), f"{file_path} should be a regular file"

    def test_file_passes_all_validations(self):
        """Test that test-0h4oez.md passes all validation checks."""
        # Get git root directory
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        repo_root = Path(result.stdout.strip())
        file_path = repo_root / FILENAME

        # Run comprehensive validation
        # This should not raise any exceptions
        validation_result = validate_file(file_path)
        assert validation_result is True

    def test_file_is_tracked_by_git(self):
        """Test that test-0h4oez.md is tracked by git."""
        assert is_file_tracked(FILENAME), \
            f"File {FILENAME} should be tracked by git"

    def test_file_is_committed(self):
        """Test that test-0h4oez.md is committed in git history."""
        # Check that the file appears in git log
        result = subprocess.run(
            ['git', 'log', '--all', '--pretty=format:%s', '--name-only'],
            capture_output=True,
            text=True,
            check=True
        )

        # Search for the file in commit history
        assert FILENAME in result.stdout, \
            f"{FILENAME} should appear in git commit history"

    def test_commit_has_exact_message(self):
        """Test that a commit with the exact required message exists."""
        # Search for the exact commit message in history
        result = subprocess.run(
            ['git', 'log', '--all', '--grep=test-0h4oez.md', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )

        # Should find a commit mentioning the file
        assert 'test-0h4oez.md' in result.stdout, \
            "No commit found mentioning test-0h4oez.md"

        # More specifically, check for the feature commit
        result = subprocess.run(
            ['git', 'log', '--all', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )

        assert any(COMMIT_MESSAGE in line for line in result.stdout.split('\n')), \
            f"Commit with message '{COMMIT_MESSAGE}' not found in history"

    def test_commit_is_on_feature_branch(self):
        """Test that the commit is on a feature branch."""
        current_branch = get_current_branch()

        # Should be on a feature branch (starts with feat/)
        assert current_branch.startswith("feat/"), \
            f"Should be on feature branch, currently on {current_branch}"

        # Verify feature branch exists (local)
        result = subprocess.run(
            ['git', 'branch'],
            capture_output=True,
            text=True,
            check=True
        )

        assert current_branch in result.stdout, \
            f"Feature branch {current_branch} should exist locally"

    def test_file_appears_in_git_ls_files(self):
        """Test that test-0h4oez.md appears in git ls-files output."""
        # Get git root directory
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        repo_root = result.stdout.strip()

        result = subprocess.run(
            ['git', 'ls-files', FILENAME],
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_root
        )

        assert FILENAME in result.stdout, \
            f"{FILENAME} should appear in git ls-files"

    def test_file_has_correct_content_structure(self):
        """Test that file has the required markdown structure."""
        # Get git root directory
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        repo_root = Path(result.stdout.strip())
        file_path = repo_root / FILENAME

        content = file_path.read_text(encoding='utf-8')

        # Check structure: H1 heading\n\n<prose>
        assert content.startswith('#'), "File should start with H1 heading"
        assert '\n\n' in content, "File should have blank line after heading"

        # Check for prose (should have multiple periods for sentences)
        parts = content.split('\n\n', 1)
        assert len(parts) >= 2, "File should have heading and prose sections"

        prose = parts[1]
        sentence_count = prose.count('.')
        assert sentence_count >= 2, "File should have at least 2 sentences"

    def test_file_has_correct_encoding(self):
        """Test that file uses UTF-8 encoding without BOM."""
        # Get git root directory
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        repo_root = Path(result.stdout.strip())
        file_path = repo_root / FILENAME

        binary_content = file_path.read_bytes()

        # Check for UTF-8 BOM
        utf8_bom = b'\xef\xbb\xbf'
        assert not binary_content.startswith(utf8_bom), \
            "File should not have UTF-8 BOM"

        # Verify content can be decoded as UTF-8
        try:
            binary_content.decode('utf-8')
        except UnicodeDecodeError:
            pytest.fail("File should be valid UTF-8")

    def test_file_has_correct_line_endings(self):
        """Test that file uses Unix LF line endings."""
        # Get git root directory
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        repo_root = Path(result.stdout.strip())
        file_path = repo_root / FILENAME

        binary_content = file_path.read_bytes()

        # Check for CRLF
        assert b'\r\n' not in binary_content, \
            "File should use Unix LF line endings, not Windows CRLF"

        # Verify file contains LF
        assert b'\n' in binary_content, \
            "File should contain LF line endings"

    def test_file_size_in_acceptable_range(self):
        """Test that file size is in the specified range."""
        # Get git root directory
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        repo_root = Path(result.stdout.strip())
        file_path = repo_root / FILENAME

        file_size = file_path.stat().st_size

        # Should be between 300-800 bytes (ideal 400-600)
        assert 300 < file_size < 800, \
            f"File size {file_size} bytes should be between 300-800"

    def test_remote_branch_exists_or_is_pushable(self):
        """Test that remote branch exists or file can be pushed."""
        current_branch = get_current_branch()

        # Check if remote tracking branch exists
        result = subprocess.run(
            ['git', 'branch', '-r'],
            capture_output=True,
            text=True,
            check=True
        )

        remote_branch = f"origin/{current_branch}"

        # If it exists on remote, verify commits are synced
        if remote_branch in result.stdout:
            # Check if local and remote are synced
            result = subprocess.run(
                ['git', 'log', f'origin/{current_branch}', '--oneline'],
                capture_output=True,
                text=True,
                check=True
            )

            # Remote should have the file commit
            assert FILENAME in result.stdout or 'feat(155)' in result.stdout, \
                f"Remote branch should contain the file or feature commit"

    def test_commit_has_proper_conventional_format(self):
        """Test that commit message follows conventional commits format."""
        # Get the commit message
        result = subprocess.run(
            ['git', 'log', '--all', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )

        # Find the feature commit
        lines = result.stdout.split('\n')
        feature_commits = [
            line for line in lines
            if 'feat(155)' in line and 'test-0h4oez.md' in line
        ]

        assert len(feature_commits) > 0, \
            "Should have a commit with 'feat(155)' and 'test-0h4oez.md'"

        # Check format: feat(scope): description
        commit_line = feature_commits[0]
        assert 'feat(' in commit_line, "Should have 'feat(' prefix"
        assert ':' in commit_line, "Should have ':' separator"
        assert 'markdown file' in commit_line or 'test-0h4oez' in commit_line, \
            "Should describe the file creation"
