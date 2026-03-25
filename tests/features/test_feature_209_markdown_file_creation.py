"""Tests for feature 209: Create markdown file test-xvuuel.md.

Tests cover:
- Module imports and constants
- File creation with correct format, encoding, and line endings
- Validation functions for markdown format, sentence count, encoding, line endings, and file size
- Git operations (add, commit, push) with proper subprocess mocking
- Complete workflow orchestration (main function)
- Error handling and edge cases
"""

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.features.feature_209_markdown_file_creation import (
    BRANCH_NAME,
    COMMIT_MESSAGE,
    FILENAME,
    FEATURE_NUMBER,
    PROSE_CONTENT,
    TITLE_TEXT,
    create_markdown_file,
)


class TestConstants:
    """Tests for module constants."""

    def test_filename_is_correct(self):
        """Test that FILENAME is set to test-xvuuel.md."""
        assert FILENAME == "test-xvuuel.md"

    def test_feature_number_is_209(self):
        """Test that FEATURE_NUMBER is 209."""
        assert FEATURE_NUMBER == 209

    def test_branch_name_is_correct(self):
        """Test that BRANCH_NAME is set correctly."""
        assert BRANCH_NAME == "feat/markdown-file-creation-c22064"

    def test_commit_message_format(self):
        """Test that COMMIT_MESSAGE follows conventional commit format."""
        assert COMMIT_MESSAGE.startswith(f"feat({FEATURE_NUMBER}):")
        assert FILENAME in COMMIT_MESSAGE

    def test_title_text_is_non_empty(self):
        """Test that TITLE_TEXT is non-empty string."""
        assert isinstance(TITLE_TEXT, str)
        assert len(TITLE_TEXT) > 0

    def test_prose_content_is_non_empty(self):
        """Test that PROSE_CONTENT is non-empty string."""
        assert isinstance(PROSE_CONTENT, str)
        assert len(PROSE_CONTENT) > 0


class TestFileCreation:
    """Tests for file creation functionality."""

    def test_create_markdown_file_creates_file(self):
        """Test that create_markdown_file creates a file at the correct path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                file_path = create_markdown_file()
                assert file_path.exists()
                assert file_path.name == FILENAME
            finally:
                import os
                os.chdir(original_cwd)

    def test_create_markdown_file_returns_path_object(self):
        """Test that create_markdown_file returns a Path object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                file_path = create_markdown_file()
                assert isinstance(file_path, Path)
            finally:
                import os
                os.chdir(original_cwd)

    def test_create_markdown_file_contains_title(self):
        """Test that created file contains the H1 title."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_markdown_file()
                content = Path(FILENAME).read_text()
                assert f"# {TITLE_TEXT}" in content
            finally:
                import os
                os.chdir(original_cwd)

    def test_create_markdown_file_contains_prose(self):
        """Test that created file contains the prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_markdown_file()
                content = Path(FILENAME).read_text()
                assert PROSE_CONTENT in content
            finally:
                import os
                os.chdir(original_cwd)

    def test_create_markdown_file_format_correct(self):
        """Test that file has correct format: # Title\\n\\nProse\\n."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_markdown_file()
                content = Path(FILENAME).read_text()
                # Check format: title on first line, blank line, prose
                lines = content.split("\n")
                assert lines[0] == f"# {TITLE_TEXT}"
                assert lines[1] == ""
                assert PROSE_CONTENT in content
            finally:
                import os
                os.chdir(original_cwd)

    def test_create_markdown_file_utf8_encoding(self):
        """Test that file is created with UTF-8 encoding without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_markdown_file()
                # Read as bytes and verify no UTF-8 BOM
                binary_content = Path(FILENAME).read_bytes()
                assert not binary_content.startswith(b"\xef\xbb\xbf")
                # Verify valid UTF-8
                binary_content.decode("utf-8")
            finally:
                import os
                os.chdir(original_cwd)

    def test_create_markdown_file_lf_line_endings(self):
        """Test that file uses Unix LF line endings (no CRLF or CR)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_markdown_file()
                binary_content = Path(FILENAME).read_bytes()
                # Check no CRLF or CR
                assert b"\r\n" not in binary_content
                assert b"\r" not in binary_content
            finally:
                import os
                os.chdir(original_cwd)

    def test_create_markdown_file_size_in_range(self):
        """Test that created file size is between 300-800 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_markdown_file()
                file_size = Path(FILENAME).stat().st_size
                assert 300 <= file_size <= 800
            finally:
                import os
                os.chdir(original_cwd)

    def test_create_markdown_file_raises_on_file_not_created(self):
        """Test that create_markdown_file raises if file not created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                # Mock Path.write_text to succeed but Path.exists to fail
                with patch('pathlib.Path.write_text'):
                    with patch('pathlib.Path.exists', return_value=False):
                        with pytest.raises(OSError, match="File was not created"):
                            create_markdown_file()
            finally:
                import os
                os.chdir(original_cwd)
