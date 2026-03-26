#!/usr/bin/env python3
"""
Test suite for feature 222: markdown-file-creation-3cd3fb
Tests create_file() function, git operations, and module constants.
No validation layer per spec requirement.
"""

import os
import subprocess
import tempfile
from pathlib import Path

import pytest
from create_markdown_file_222 import (
    COMMIT_MESSAGE,
    FILENAME,
    PROSE,
    TITLE,
    create_file,
    git_add,
    git_commit,
    git_push,
)


class TestConstants:
    """Test suite for module-level constants."""

    def test_filename_is_correct(self):
        """Test that FILENAME constant is exactly 'test-tmmd9v.md'."""
        assert FILENAME == "test-tmmd9v.md"

    def test_title_is_meaningful(self):
        """Test that TITLE is a meaningful non-empty string."""
        assert isinstance(TITLE, str)
        assert len(TITLE) > 0
        assert not TITLE.isspace()

    def test_prose_is_not_empty(self):
        """Test that PROSE is a meaningful non-empty string."""
        assert isinstance(PROSE, str)
        assert len(PROSE) > 0
        assert not PROSE.isspace()

    def test_prose_sentence_count(self):
        """Test that PROSE contains exactly 2-3 sentences."""
        sentence_count = PROSE.count('.')
        assert 2 <= sentence_count <= 3

    def test_commit_message_format(self):
        """Test that COMMIT_MESSAGE follows conventional commits format."""
        assert COMMIT_MESSAGE.startswith("feat(222):")
        assert "test-tmmd9v.md" in COMMIT_MESSAGE


class TestCreateFile:
    """Test suite for create_file function."""

    def test_create_file_returns_path_on_success(self):
        """Test that create_file returns Path when file is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                result = create_file()
                assert result is not None
                assert isinstance(result, Path)
                assert Path(FILENAME).exists()
            finally:
                os.chdir(original_dir)

    def test_create_file_returns_existing_if_exists(self):
        """Test that create_file returns existing file without raising error if file already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / FILENAME
            # Create file first
            test_file.write_text("# Title\n\nContent.\n")
            # Now try to create again
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                result = create_file()
                # Should return the existing file path without raising error
                assert result is not None
                assert isinstance(result, Path)
                assert Path(FILENAME).exists()
            finally:
                os.chdir(original_dir)

    def test_create_file_contains_h1_heading(self):
        """Test that created file contains H1 heading with TITLE."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                content = Path(FILENAME).read_text(encoding="utf-8")
                assert content.startswith(f"# {TITLE}\n")
            finally:
                os.chdir(original_dir)

    def test_create_file_contains_blank_line_after_heading(self):
        """Test that created file has blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                content = Path(FILENAME).read_text(encoding="utf-8")
                lines = content.split("\n")
                assert lines[0].startswith("# ")
                assert lines[1] == ""
            finally:
                os.chdir(original_dir)

    def test_create_file_contains_prose(self):
        """Test that created file contains PROSE content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                content = Path(FILENAME).read_text(encoding="utf-8")
                assert PROSE in content
            finally:
                os.chdir(original_dir)

    def test_create_file_uses_utf8_encoding(self):
        """Test that created file uses UTF-8 encoding without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                binary = Path(FILENAME).read_bytes()
                # Should not start with UTF-8 BOM (EF BB BF)
                assert not binary.startswith(b"\xef\xbb\xbf")
                # Should decode as UTF-8
                content = binary.decode("utf-8")
                assert content is not None
            finally:
                os.chdir(original_dir)

    def test_create_file_uses_lf_line_endings(self):
        """Test that created file uses Unix LF line endings only."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                binary = Path(FILENAME).read_bytes()
                # Should not contain CRLF (0x0D 0x0A)
                assert b"\r\n" not in binary
                # Should contain LF (0x0A)
                assert b"\n" in binary
            finally:
                os.chdir(original_dir)

    def test_create_file_ends_with_newline(self):
        """Test that created file ends with newline character."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                content = Path(FILENAME).read_text(encoding="utf-8")
                assert content.endswith("\n")
            finally:
                os.chdir(original_dir)

    def test_create_file_size_in_range(self):
        """Test that created file size is between 300-500 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                file_size = Path(FILENAME).stat().st_size
                assert 300 <= file_size <= 500
            finally:
                os.chdir(original_dir)

    def test_create_file_structure(self):
        """Test that created file has correct markdown structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                content = Path(FILENAME).read_text(encoding="utf-8")
                # Structure should be: # Title\n\nProse\n
                lines = content.split("\n")
                assert len(lines) >= 3  # heading, blank line, prose, newline
                assert lines[0].startswith("# ")  # H1 heading
                assert lines[1] == ""  # Blank line
                assert PROSE in content  # Prose content present
            finally:
                os.chdir(original_dir)


class TestGitAdd:
    """Test suite for git_add function (Phase 2)."""

    def test_git_add_stages_file(self):
        """Test that git_add stages the file in git index."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo
                subprocess.run(["git", "init"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@example.com"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

                # Create file
                create_file()

                # Verify file is untracked before git_add
                result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
                assert "?? " in result.stdout  # Untracked files shown with "??"

                # Add file
                git_add()

                # Verify file is now staged
                result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
                assert "A  " in result.stdout  # Staged files shown with "A "
            finally:
                os.chdir(original_dir)

    def test_git_add_raises_if_file_not_found(self):
        """Test that git_add raises CalledProcessError if file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo
                subprocess.run(["git", "init"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@example.com"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

                # Try to add non-existent file
                with pytest.raises(subprocess.CalledProcessError):
                    git_add()
            finally:
                os.chdir(original_dir)


class TestGitCommit:
    """Test suite for git_commit function (Phase 2)."""

    def test_git_commit_creates_commit(self):
        """Test that git_commit creates a commit with correct message."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo
                subprocess.run(["git", "init"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@example.com"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

                # Create file and stage it
                create_file()
                git_add()

                # Get commit count before
                result = subprocess.run(["git", "log", "--oneline"], capture_output=True, text=True)
                commits_before = len([line for line in result.stdout.strip().split("\n") if line])

                # Create commit
                git_commit()

                # Get commit count after
                result = subprocess.run(["git", "log", "--oneline"], capture_output=True, text=True)
                commits_after = len([line for line in result.stdout.strip().split("\n") if line])

                # Verify new commit was created
                assert commits_after == commits_before + 1
            finally:
                os.chdir(original_dir)

    def test_git_commit_message_format(self):
        """Test that git_commit uses correct conventional commit message."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo
                subprocess.run(["git", "init"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@example.com"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

                # Create file and stage it
                create_file()
                git_add()

                # Create commit
                git_commit()

                # Verify commit message
                result = subprocess.run(["git", "log", "--oneline", "-1"], capture_output=True, text=True)
                assert COMMIT_MESSAGE in result.stdout
            finally:
                os.chdir(original_dir)

    def test_git_commit_raises_if_no_changes(self):
        """Test that git_commit raises CalledProcessError if there are no changes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo
                subprocess.run(["git", "init"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@example.com"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

                # Try to commit without any changes
                with pytest.raises(subprocess.CalledProcessError):
                    git_commit()
            finally:
                os.chdir(original_dir)


class TestGitPush:
    """Test suite for git_push function (Phase 2).

    Note: These tests check that the function can be called and handles
    errors appropriately. Full integration tests with actual remote push
    are tested in TestFullIntegration.
    """

    def test_git_push_raises_if_no_remote(self):
        """Test that git_push raises CalledProcessError if no remote is configured."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo without remote
                subprocess.run(["git", "init"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@example.com"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

                # Create file and commit
                create_file()
                git_add()
                git_commit()

                # Try to push without remote
                with pytest.raises(subprocess.CalledProcessError):
                    git_push()
            finally:
                os.chdir(original_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
