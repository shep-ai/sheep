"""Tests for feature 171 phase 3: File I/O and Git Integration.

Tests for the file I/O and git integration phase of feature 171:
- write_markdown_file(): Write markdown content to disk with UTF-8 encoding and Unix LF line endings
- git_add(): Stage file with git add command
- git_commit(): Create git commit with conventional message
- git_push(): Push commits to remote repository
"""

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestWriteMarkdownFile:
    """Tests for write_markdown_file() function."""

    def test_write_markdown_file_creates_file_at_specified_path(self):
        """Test that write_markdown_file() creates file at specified path."""
        from sheep.features.feature_171 import write_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            content = "# Test Title\n\nTest content. More content. And more.\n"
            filepath = write_markdown_file(content, "test.md", tmpdir)

            # File should exist at the returned path
            assert Path(filepath).exists()
            assert Path(filepath).name == "test.md"
            assert str(tmpdir) in filepath

    def test_write_markdown_file_content_matches_input(self):
        """Test that file content matches input string exactly."""
        from sheep.features.feature_171 import write_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            content = "# Test Title\n\nTest content. More content. And more.\n"
            filepath = write_markdown_file(content, "test.md", tmpdir)

            # Read file and verify content matches exactly
            file_content = Path(filepath).read_text(encoding='utf-8')
            assert file_content == content

    def test_write_markdown_file_uses_utf8_encoding(self):
        """Test that file uses UTF-8 encoding."""
        from sheep.features.feature_171 import write_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            # Use content with UTF-8 characters
            content = "# Tëst Tïtlé\n\nContent with café. More content. And more.\n"
            filepath = write_markdown_file(content, "test.md", tmpdir)

            # Read as binary and verify it's valid UTF-8
            binary_content = Path(filepath).read_bytes()
            decoded = binary_content.decode('utf-8')
            assert decoded == content

    def test_write_markdown_file_no_bom(self):
        """Test that file has no BOM (Byte Order Mark)."""
        from sheep.features.feature_171 import write_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            content = "# Test Title\n\nTest content. More content. And more.\n"
            filepath = write_markdown_file(content, "test.md", tmpdir)

            # Read as binary and check for BOM
            binary_content = Path(filepath).read_bytes()
            assert not binary_content.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"

    def test_write_markdown_file_uses_lf_line_endings(self):
        """Test that file uses Unix LF line endings, not CRLF."""
        from sheep.features.feature_171 import write_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath = write_markdown_file(content, "test.md", tmpdir)

            # Read as binary and check for CRLF
            binary_content = Path(filepath).read_bytes()
            assert b'\r\n' not in binary_content, "File should use LF, not CRLF"
            assert b'\n' in binary_content, "File should have LF line endings"

    def test_write_markdown_file_overwrite_existing_file(self):
        """Test that write_markdown_file() overwrites existing file."""
        from sheep.features.feature_171 import write_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create initial file
            initial_content = "# Old Title\n\nOld content. More old. And more.\n"
            filepath = write_markdown_file(initial_content, "test.md", tmpdir)
            assert Path(filepath).read_text(encoding='utf-8') == initial_content

            # Overwrite with new content
            new_content = "# New Title\n\nNew content. More new. And more.\n"
            filepath = write_markdown_file(new_content, "test.md", tmpdir)
            assert Path(filepath).read_text(encoding='utf-8') == new_content

    def test_write_markdown_file_rejects_path_traversal(self):
        """Test that write_markdown_file() rejects filenames with path traversal."""
        from sheep.features.feature_171 import write_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            content = "# Test\n\nContent. More. And more.\n"

            # Should reject filenames with / or \
            with pytest.raises(ValueError, match="Invalid filename"):
                write_markdown_file(content, "../outside.md", tmpdir)

            with pytest.raises(ValueError, match="Invalid filename"):
                write_markdown_file(content, "..\\outside.md", tmpdir)

            with pytest.raises(ValueError, match="Invalid filename"):
                write_markdown_file(content, ".hidden/file.md", tmpdir)

    def test_write_markdown_file_returns_filepath(self):
        """Test that write_markdown_file() returns the full filepath."""
        from sheep.features.feature_171 import write_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            content = "# Test\n\nContent. More. And more.\n"
            filepath = write_markdown_file(content, "test.md", tmpdir)

            assert isinstance(filepath, str)
            assert filepath.endswith("test.md")

    def test_write_markdown_file_defaults_to_cwd(self):
        """Test that write_markdown_file() defaults to current working directory."""
        from sheep.features.feature_171 import write_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp directory
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                content = "# Test\n\nContent. More. And more.\n"
                filepath = write_markdown_file(content, "test.md")

                # File should be in current directory
                assert Path(filepath).exists()
                # Compare resolved paths to handle Windows short path names
                assert Path(filepath).resolve().parent == Path(tmpdir).resolve()
            finally:
                os.chdir(old_cwd)


class TestGitOperations:
    """Tests for git operations (git_add, git_commit, git_push)."""

    @patch('sheep.features.feature_171.subprocess.run')
    def test_git_add_stages_file(self, mock_run):
        """Test that git_add() stages file with git add command."""
        from sheep.features.feature_171 import git_add

        mock_run.return_value = MagicMock(returncode=0)

        git_add("test.md", "/test/repo")

        # Verify subprocess.run was called with correct git command
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == ['git', 'add', 'test.md']
        assert call_args[1]['cwd'] == "/test/repo"

    @patch('sheep.features.feature_171.subprocess.run')
    def test_git_add_raises_on_failure(self, mock_run):
        """Test that git_add() raises RuntimeError on git failure."""
        from sheep.features.feature_171 import git_add

        error = subprocess.CalledProcessError(1, 'git add')
        error.stderr = "fatal: not a git repository"
        mock_run.side_effect = error

        with pytest.raises(RuntimeError, match="git add failed"):
            git_add("test.md", "/test/repo")

    @patch('sheep.features.feature_171.subprocess.run')
    def test_git_add_raises_if_git_not_found(self, mock_run):
        """Test that git_add() raises RuntimeError if git command not found."""
        from sheep.features.feature_171 import git_add

        mock_run.side_effect = FileNotFoundError("git not found")

        with pytest.raises(RuntimeError, match="git command not found"):
            git_add("test.md", "/test/repo")

    @patch('sheep.features.feature_171.subprocess.run')
    def test_git_commit_creates_commit(self, mock_run):
        """Test that git_commit() creates git commit with message."""
        from sheep.features.feature_171 import git_commit

        mock_run.return_value = MagicMock(returncode=0, stdout="[main abc1234] Commit message\n")

        result = git_commit("feat(171): Test commit", "/test/repo")

        # Verify subprocess.run was called with correct git command
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == ['git', 'commit', '-m', 'feat(171): Test commit']
        assert call_args[1]['cwd'] == "/test/repo"
        assert result == "[main abc1234] Commit message\n"

    @patch('sheep.features.feature_171.subprocess.run')
    def test_git_commit_raises_on_failure(self, mock_run):
        """Test that git_commit() raises RuntimeError on git failure."""
        from sheep.features.feature_171 import git_commit

        error = subprocess.CalledProcessError(1, 'git commit')
        error.stderr = "nothing to commit"
        mock_run.side_effect = error

        with pytest.raises(RuntimeError, match="git commit failed"):
            git_commit("feat(171): Test commit", "/test/repo")

    @patch('sheep.features.feature_171.subprocess.run')
    def test_git_commit_raises_if_git_not_found(self, mock_run):
        """Test that git_commit() raises RuntimeError if git command not found."""
        from sheep.features.feature_171 import git_commit

        mock_run.side_effect = FileNotFoundError("git not found")

        with pytest.raises(RuntimeError, match="git command not found"):
            git_commit("feat(171): Test commit", "/test/repo")

    @patch('sheep.features.feature_171.subprocess.run')
    def test_git_push_pushes_to_remote(self, mock_run):
        """Test that git_push() pushes to remote repository."""
        from sheep.features.feature_171 import git_push

        mock_run.return_value = MagicMock(returncode=0, stdout="Pushing to origin...\n")

        result = git_push("/test/repo")

        # Verify subprocess.run was called with git push
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0][0:3] == ['git', 'push', '-u']
        assert 'origin' in call_args[0][0]
        assert result == "Pushing to origin...\n"

    @patch('sheep.features.feature_171.subprocess.run')
    def test_git_push_raises_on_failure(self, mock_run):
        """Test that git_push() raises RuntimeError on git failure."""
        from sheep.features.feature_171 import git_push

        error = subprocess.CalledProcessError(1, 'git push')
        error.stderr = "fatal: could not read Username"
        mock_run.side_effect = error

        with pytest.raises(RuntimeError, match="git push failed"):
            git_push("/test/repo")

    @patch('sheep.features.feature_171.subprocess.run')
    def test_git_push_raises_if_git_not_found(self, mock_run):
        """Test that git_push() raises RuntimeError if git command not found."""
        from sheep.features.feature_171 import git_push

        mock_run.side_effect = FileNotFoundError("git not found")

        with pytest.raises(RuntimeError, match="git command not found"):
            git_push("/test/repo")

    @patch('sheep.features.feature_171.subprocess.run')
    def test_git_push_uses_custom_remote(self, mock_run):
        """Test that git_push() can use custom remote name."""
        from sheep.features.feature_171 import git_push

        mock_run.return_value = MagicMock(returncode=0, stdout="Pushed\n")

        git_push("/test/repo", remote='upstream')

        call_args = mock_run.call_args
        assert 'upstream' in call_args[0][0]


class TestPhase3Integration:
    """Integration tests for phase 3 (file I/O and git operations)."""

    def test_write_and_validate_file_properties(self):
        """Test that written file passes all property validations."""
        from sheep.features.feature_171 import (
            write_markdown_file,
            validate_encoding,
            validate_line_endings,
            validate_file_size,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            content = "# The Power of Consistent Practice\n\nDeveloping any skill requires consistent, deliberate practice over extended periods. Small daily improvements compound into significant progress, transforming novices into experts through dedication. The key to mastery lies not in talent, but in the persistent application of effort toward meaningful goals.\n"
            filepath = write_markdown_file(content, "test.md", tmpdir)

            # All property validations should pass
            validate_encoding(filepath)
            validate_line_endings(filepath)
            validate_file_size(filepath)

    @patch('sheep.features.feature_171.git_push')
    @patch('sheep.features.feature_171.git_commit')
    @patch('sheep.features.feature_171.git_add')
    def test_orchestration_calls_file_and_git_operations(
        self, mock_add, mock_commit, mock_push
    ):
        """Test that orchestration calls file I/O and git operations."""
        from sheep.features.feature_171 import create_feature_171_markdown_file

        mock_commit.return_value = "[branch] commit message\n"
        mock_push.return_value = "Pushed\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            result = create_feature_171_markdown_file(tmpdir)

            # Verify git operations were called
            mock_add.assert_called_once()
            mock_commit.assert_called_once()
            mock_push.assert_called_once()

            # Verify result structure
            assert 'filepath' in result
            assert 'content' in result
            assert 'commit_message' in result
            assert 'push_result' in result

            # Verify file exists and has content
            assert Path(result['filepath']).exists()
            assert len(result['content']) > 0
