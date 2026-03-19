"""Tests for feature 105: Creating markdown file test-rc1h43.md with title and prose content."""

from pathlib import Path
import pytest


class TestFileCreation:
    """Tests for markdown file creation with proper structure."""

    @pytest.fixture
    def test_file_path(self):
        """Return the path to the test markdown file."""
        return Path("test-rc1h43.md")

    def test_file_exists(self, test_file_path):
        """Test that file test-rc1h43.md exists in repository root."""
        assert test_file_path.exists(), f"File {test_file_path} should exist"
        assert test_file_path.is_file(), f"{test_file_path} should be a file"

    def test_file_contains_h1_heading(self, test_file_path):
        """Test that file contains H1 heading starting with '# '."""
        content = test_file_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        assert len(lines) > 0, "File should have content"
        assert lines[0].startswith("# "), f"First line should be H1 heading (# ), got: {lines[0]}"

    def test_file_contains_blank_line_separator(self, test_file_path):
        """Test that file has blank line after H1 heading."""
        content = test_file_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        assert len(lines) >= 2, "File should have at least 2 lines"
        assert lines[1] == "", f"Second line should be blank separator, got: {lines[1]}"

    def test_file_contains_two_or_three_sentences(self, test_file_path):
        """Test that file contains 2-3 sentences (periods)."""
        content = test_file_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        # Extract prose content (skip heading and blank line)
        prose_lines = lines[2:] if len(lines) > 2 else []
        prose_content = "\n".join(prose_lines).strip()
        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3, (
            f"Prose should have 2-3 sentences, found {sentence_count}. "
            f"Content: {prose_content}"
        )


class TestFileEncoding:
    """Tests for file encoding and line endings."""

    @pytest.fixture
    def test_file_path(self):
        """Return the path to the test markdown file."""
        return Path("test-rc1h43.md")

    def test_file_is_utf8_encoded(self, test_file_path):
        """Test that file can be read as UTF-8 without encoding errors."""
        try:
            content = test_file_path.read_text(encoding="utf-8")
            assert len(content) > 0, "File should have content"
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not valid UTF-8: {e}")

    def test_file_no_utf8_bom(self, test_file_path):
        """Test that file encoding is UTF-8 without BOM (no 0xEF 0xBB 0xBF)."""
        binary_content = test_file_path.read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

    def test_file_uses_lf_line_endings(self, test_file_path):
        """Test that file uses LF line endings (not CRLF)."""
        binary_content = test_file_path.read_bytes()
        assert b"\r\n" not in binary_content, "File should use LF, not CRLF line endings"

    def test_file_ends_with_newline(self, test_file_path):
        """Test that file ends with newline character."""
        binary_content = test_file_path.read_bytes()
        assert binary_content.endswith(b"\n"), "File should end with newline"


class TestFileSize:
    """Tests for file size validation."""

    MIN_SIZE = 320
    MAX_SIZE = 600

    @pytest.fixture
    def test_file_path(self):
        """Return the path to the test markdown file."""
        return Path("test-rc1h43.md")

    def test_file_size_within_range(self, test_file_path):
        """Test that file size is within expected range (320-600 bytes)."""
        file_size = len(test_file_path.read_bytes())
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE, (
            f"File size {file_size} should be between {self.MIN_SIZE}-{self.MAX_SIZE} bytes"
        )
