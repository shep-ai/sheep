"""Tests for feature 206: Markdown file creation with hard-coded content."""

import tempfile
from pathlib import Path

import pytest

from sheep.features.feature_206_markdown_file_creation import (
    FILENAME,
    PROSE_CONTENT,
    TITLE_TEXT,
    create_markdown_file,
)


class TestCreateMarkdownFile:
    """Test suite for create_markdown_file() function."""

    def test_file_does_not_exist_initially(self):
        """Verify file does not exist before calling create_markdown_file()."""
        file_path = Path(FILENAME)
        # File should not exist from a clean state (or we clean it up first)
        if file_path.exists():
            file_path.unlink()
        assert not file_path.exists()

    def test_create_markdown_file_creates_file(self):
        """Test that create_markdown_file() creates the file."""
        file_path = Path(FILENAME)
        # Clean up first if it exists
        if file_path.exists():
            file_path.unlink()

        # Call function
        result = create_markdown_file()

        # Assert file now exists
        assert file_path.exists()
        assert result == file_path

    def test_create_markdown_file_correct_name(self):
        """Test that created file has the correct filename."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()

        assert file_path.exists()
        assert file_path.name == FILENAME

    def test_create_markdown_file_correct_content_format(self):
        """Test that file has correct content format: # Title\n\nProse\n"""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()

        content = file_path.read_text(encoding="utf-8")

        # Verify format: # Title, blank line, prose, trailing newline
        lines = content.split("\n")
        assert lines[0] == f"# {TITLE_TEXT}"
        assert lines[1] == ""
        assert PROSE_CONTENT in content
        assert content.endswith("\n")

    def test_create_markdown_file_utf8_encoding(self):
        """Test that file is created with UTF-8 encoding."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()

        # Verify can be read as UTF-8
        content = file_path.read_text(encoding="utf-8")
        assert content  # File has content
        assert isinstance(content, str)

    def test_create_markdown_file_no_bom(self):
        """Test that file does not start with UTF-8 BOM."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()

        binary_content = file_path.read_bytes()
        # UTF-8 BOM is 0xEF 0xBB 0xBF
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_create_markdown_file_returns_path(self):
        """Test that function returns a Path object."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        result = create_markdown_file()

        assert isinstance(result, Path)
        assert result.name == FILENAME

    def teardown_method(self):
        """Clean up test file after each test."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()
