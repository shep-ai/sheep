"""
Tests for Task 2: Write markdown file to disk with UTF-8 encoding and LF line endings

Tests verify that write_markdown_file():
- Creates file at repository root with correct filename
- Writes exact content passed to function
- Uses UTF-8 encoding without BOM
- Uses Unix LF line endings (no CRLF)
- File is non-empty and correctly sized
"""

import tempfile
from pathlib import Path

import pytest

from task_2_write_markdown_file import (
    MARKDOWN_FILENAME,
    SAMPLE_CONTENT,
    task_2_write_markdown_file,
)


class TestTask2WritMarkdownFile:
    """Tests for task-2: Write markdown file with proper encoding."""

    @pytest.fixture
    def temp_dir(self):
        """Fixture to run tests in isolated temporary directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                yield tmpdir
            finally:
                import os
                os.chdir(original_cwd)

    def test_file_does_not_exist_before_write(self, temp_dir):
        """Test that file does not exist before write operation."""
        assert not Path(MARKDOWN_FILENAME).exists()

    def test_write_markdown_file_creates_file(self, temp_dir):
        """Test that write_markdown_file creates the file."""
        result = task_2_write_markdown_file(SAMPLE_CONTENT)
        assert Path(MARKDOWN_FILENAME).exists()
        assert result.endswith(MARKDOWN_FILENAME)

    def test_file_exists_at_expected_path(self, temp_dir):
        """Test that file exists at expected path via Path.exists()."""
        task_2_write_markdown_file(SAMPLE_CONTENT)
        assert Path(MARKDOWN_FILENAME).exists()

    def test_file_contains_exact_content(self, temp_dir):
        """Test that file contains exact content passed to write_markdown_file."""
        task_2_write_markdown_file(SAMPLE_CONTENT)
        written_content = Path(MARKDOWN_FILENAME).read_text(encoding='utf-8')
        assert written_content == SAMPLE_CONTENT

    def test_file_size_in_expected_range(self, temp_dir):
        """Test that file size is reasonable for H1 heading + 2-3 sentences (~300-600 bytes)."""
        task_2_write_markdown_file(SAMPLE_CONTENT)
        file_size = Path(MARKDOWN_FILENAME).stat().st_size
        # Typically 400-600 bytes for this format, but allow 300-700 to be flexible
        assert 300 <= file_size <= 700, f"File size {file_size} not in reasonable range 300-700"

    def test_file_utf8_encoding_no_bom(self, temp_dir):
        """Test that file uses UTF-8 encoding without BOM."""
        task_2_write_markdown_file(SAMPLE_CONTENT)
        binary_content = Path(MARKDOWN_FILENAME).read_bytes()

        # Verify no UTF-8 BOM (0xEF 0xBB 0xBF)
        assert not binary_content.startswith(b'\xef\xbb\xbf'), \
            "File contains UTF-8 BOM"

        # Verify valid UTF-8 encoding
        try:
            binary_content.decode('utf-8')
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not valid UTF-8: {e}")

    def test_file_uses_lf_line_endings(self, temp_dir):
        """Test that file uses Unix LF line endings (no CRLF)."""
        task_2_write_markdown_file(SAMPLE_CONTENT)
        binary_content = Path(MARKDOWN_FILENAME).read_bytes()

        # Verify no CRLF line endings
        assert b'\r\n' not in binary_content, \
            "File contains CRLF line endings (Windows style)"

        # Verify no CR-only line endings
        assert b'\r' not in binary_content, \
            "File contains CR line endings (old Mac style)"

    def test_file_ends_with_newline(self, temp_dir):
        """Test that file ends with trailing newline."""
        task_2_write_markdown_file(SAMPLE_CONTENT)
        content = Path(MARKDOWN_FILENAME).read_text(encoding='utf-8')
        assert content.endswith('\n'), \
            "File does not end with trailing newline"

    def test_file_is_non_empty(self, temp_dir):
        """Test that file is non-empty."""
        task_2_write_markdown_file(SAMPLE_CONTENT)
        file_size = Path(MARKDOWN_FILENAME).stat().st_size
        assert file_size > 0, "File is empty"

    def test_content_with_markdown_heading(self, temp_dir):
        """Test write_markdown_file with content containing markdown H1 heading."""
        markdown_with_heading = """# Test Heading

This is a test sentence. This is another test sentence. This is a third test sentence.
"""
        result = task_2_write_markdown_file(markdown_with_heading)
        assert Path(result).exists()
        written_content = Path(result).read_text(encoding='utf-8')
        assert written_content.startswith('# ')

    def test_return_value_is_filepath(self, temp_dir):
        """Test that write_markdown_file returns the filepath."""
        result = task_2_write_markdown_file(SAMPLE_CONTENT)
        assert isinstance(result, str)
        assert MARKDOWN_FILENAME in result
        assert Path(result).exists()
