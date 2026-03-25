"""Tests for feature 207: Create markdown file test-jkyks3.md.

Tests cover file creation with correct format, encoding, and line endings.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from sheep.features.feature_207_markdown_file_creation import (
    FILENAME,
    PROSE_CONTENT,
    TITLE_TEXT,
    create_markdown_file,
)


class TestFileCreation:
    """Tests for file creation functionality."""

    def test_create_markdown_file_creates_file(self):
        """Test that create_markdown_file creates a file at the correct path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Verify file doesn't exist initially
                assert not Path(FILENAME).exists()

                # Create file
                file_path = create_markdown_file()

                # Verify file was created
                assert file_path.exists()
                assert file_path.name == FILENAME
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
                # Verify it's at the start (H1 heading should be first line)
                assert content.startswith(f"# {TITLE_TEXT}")
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

    def test_create_markdown_file_utf8_encoding(self):
        """Test that file is created with UTF-8 encoding."""
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
        """Test that file uses Unix LF line endings."""
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

    def test_create_markdown_file_returns_path(self):
        """Test that create_markdown_file returns a Path object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                result = create_markdown_file()
                assert isinstance(result, Path)
            finally:
                import os

                os.chdir(original_cwd)

    def test_create_markdown_file_has_blank_line_separator(self):
        """Test that file has blank line between title and prose."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                content = Path(FILENAME).read_text()
                lines = content.split("\n")
                # First line should be the title
                assert lines[0].startswith("# ")
                # Second line should be blank
                assert lines[1] == ""
                # Third line should be the start of prose
                assert len(lines) > 2
            finally:
                import os

                os.chdir(original_cwd)

    def test_create_markdown_file_size_in_range(self):
        """Test that created file size is within expected range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                file_size = Path(FILENAME).stat().st_size
                # Specification requires 250-600 bytes
                assert 250 <= file_size <= 600, f"File size {file_size} out of range 250-600"
            finally:
                import os

                os.chdir(original_cwd)
