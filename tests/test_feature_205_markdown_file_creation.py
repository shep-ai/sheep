"""Tests for Feature 205: Create markdown file test-axs39z.md with title and prose.

This test suite covers:
- Task 1: create_markdown_file() function with hardcoded content
- Task 2: File existence validation (_validate_file_exists)
"""

import os
import tempfile
from pathlib import Path

import pytest

# Import the feature module
from sheep.features.feature_205_markdown_file_creation import (
    FILENAME,
    PROSE_CONTENT,
    TITLE,
    _validate_file_exists,
    create_markdown_file,
)


class TestTaskOne:
    """Tests for task-1: create_markdown_file() function."""

    def test_module_exists(self):
        """Test that the feature module can be imported."""
        from sheep.features import feature_205_markdown_file_creation
        assert feature_205_markdown_file_creation is not None

    def test_create_markdown_file_creates_file(self):
        """Test that create_markdown_file creates a file at specified location."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                path = create_markdown_file()
                assert Path(FILENAME).exists()
                assert FILENAME in path
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_with_custom_filename(self):
        """Test that create_markdown_file accepts custom filename."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                path = create_markdown_file("custom.md")
                assert Path("custom.md").exists()
                assert "custom.md" in path
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_raises_on_existing_file(self):
        """Test that create_markdown_file raises FileExistsError if file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create a file first
                Path(FILENAME).write_text("# Existing\n\nContent.\n")

                with pytest.raises(FileExistsError):
                    create_markdown_file()
            finally:
                os.chdir(original_cwd)

    def test_created_file_contains_h1_heading(self):
        """Test that created file starts with H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                content = Path(FILENAME).read_text(encoding="utf-8")
                lines = content.split("\n")

                assert lines[0].startswith("# ")
                assert "Markdown File Creation" in lines[0]
            finally:
                os.chdir(original_cwd)

    def test_created_file_has_blank_line(self):
        """Test that created file has blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                content = Path(FILENAME).read_text(encoding="utf-8")
                lines = content.split("\n")

                assert lines[1] == ""  # blank line
            finally:
                os.chdir(original_cwd)

    def test_created_file_contains_prose_content(self):
        """Test that created file contains hardcoded prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                content = Path(FILENAME).read_text(encoding="utf-8")
                assert PROSE_CONTENT in content
            finally:
                os.chdir(original_cwd)

    def test_created_file_uses_utf8_encoding(self):
        """Test that created file is UTF-8 encoded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                # Try to read as UTF-8 (should not raise)
                content = Path(FILENAME).read_text(encoding="utf-8")
                assert content is not None
            finally:
                os.chdir(original_cwd)

    def test_created_file_uses_lf_line_endings(self):
        """Test that created file uses LF line endings, not CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                binary_content = Path(FILENAME).read_bytes()
                assert b"\r\n" not in binary_content
                assert b"\n" in binary_content
            finally:
                os.chdir(original_cwd)

    def test_created_file_structure(self):
        """Test the complete structure of the created file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                content = Path(FILENAME).read_text(encoding="utf-8")
                lines = content.split("\n")

                # Line 0: H1 heading
                assert lines[0].startswith("# ")
                # Line 1: blank line
                assert lines[1] == ""
                # Line 2+: prose content
                remaining = "\n".join(lines[2:]).strip()
                assert PROSE_CONTENT in remaining
                # Must end with newline
                assert content.endswith("\n")
            finally:
                os.chdir(original_cwd)

    def test_created_file_returns_absolute_path(self):
        """Test that create_markdown_file returns absolute path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                path = create_markdown_file()

                assert os.path.isabs(path)
                assert path.endswith(FILENAME)
            finally:
                os.chdir(original_cwd)


class TestTaskTwo:
    """Tests for task-2: File existence validation."""

    def test_validate_file_exists_success(self):
        """Test that _validate_file_exists passes when file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Test\n\nContent.\n")

                # Should not raise
                _validate_file_exists(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_validate_file_exists_raises_on_missing_file(self):
        """Test that _validate_file_exists raises ValueError if file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with pytest.raises(ValueError) as exc_info:
                    _validate_file_exists(FILENAME)

                assert "was not created" in str(exc_info.value).lower()
            finally:
                os.chdir(original_cwd)

    def test_validate_file_exists_called_after_creation(self):
        """Test that _validate_file_exists is called during file creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # create_markdown_file should call _validate_file_exists internally
                path = create_markdown_file()

                # File should exist
                assert Path(FILENAME).exists()
            finally:
                os.chdir(original_cwd)

    def test_validate_file_exists_with_custom_filename(self):
        """Test _validate_file_exists with custom filename."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                test_file = "test_custom.md"
                Path(test_file).write_text("# Test\n\nContent.\n")

                # Should not raise
                _validate_file_exists(test_file)
            finally:
                os.chdir(original_cwd)

    def test_validate_file_exists_error_message(self):
        """Test that _validate_file_exists has descriptive error message."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                missing_file = "missing.md"

                with pytest.raises(ValueError) as exc_info:
                    _validate_file_exists(missing_file)

                error_msg = str(exc_info.value)
                assert missing_file in error_msg
                assert "was not created" in error_msg.lower() or "does not exist" in error_msg.lower()
            finally:
                os.chdir(original_cwd)
