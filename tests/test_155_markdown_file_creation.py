"""Tests for feature 155: Creating markdown file test-0h4oez.md with title and prose content."""

from pathlib import Path
import pytest


class TestMarkdownFileCreation:
    """Tests for task-1: Create markdown file with H1 heading and prose content."""

    def test_file_exists(self):
        """Test that file test-0h4oez.md exists at repository root."""
        test_file = Path("test-0h4oez.md")
        assert test_file.exists(), "File test-0h4oez.md should exist at repository root"

    def test_file_contains_h1_heading(self):
        """Test that file starts with H1 heading."""
        test_file = Path("test-0h4oez.md")
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        assert lines[0].startswith("# "), "First line should be H1 heading (starts with '# ')"

    def test_file_has_blank_line_separator(self):
        """Test that file has blank line after H1 heading."""
        test_file = Path("test-0h4oez.md")
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        assert len(lines) >= 3, "File should have at least heading, blank line, and prose"
        assert lines[1] == "", "Second line should be blank (separator after heading)"

    def test_file_contains_prose_content(self):
        """Test that file contains prose content after blank line."""
        test_file = Path("test-0h4oez.md")
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        prose_lines = [line for line in lines[2:] if line.strip()]
        assert len(prose_lines) > 0, "File should contain prose content after heading"

    def test_file_contains_2_to_3_sentences(self):
        """Test that prose content contains 2-3 sentences (periods as sentence markers)."""
        test_file = Path("test-0h4oez.md")
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        prose_content = "\n".join(lines[2:]).strip()
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3, f"Should have 2-3 sentences, found {sentence_count}"


class TestMarkdownFileValidation:
    """Tests for task-2: Validate file encoding, line endings, and size."""

    MIN_SIZE = 400
    MAX_SIZE = 600

    def test_file_utf8_no_bom(self):
        """Test that file encoding is UTF-8 without BOM (no 0xEF 0xBB 0xBF prefix)."""
        test_file = Path("test-0h4oez.md")
        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

    def test_file_has_lf_line_endings_only(self):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = Path("test-0h4oez.md")
        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content, "File should use LF (\\n) not CRLF (\\r\\n)"

    def test_file_size_within_range(self):
        """Test that file size is between 400-600 bytes (inclusive)."""
        test_file = Path("test-0h4oez.md")
        file_size = len(test_file.read_bytes())
        assert (
            self.MIN_SIZE <= file_size <= self.MAX_SIZE
        ), f"File size {file_size} should be between {self.MIN_SIZE}-{self.MAX_SIZE} bytes"

    def test_markdown_syntax_valid(self):
        """Test that markdown structure is valid (heading, blank line, prose)."""
        test_file = Path("test-0h4oez.md")
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")

        # First line must be H1 heading
        assert lines[0].startswith("# "), "First line should be H1 heading"

        # Second line must be blank
        assert lines[1] == "", "Second line should be blank"

        # Third line onwards should have prose
        prose = "\n".join(lines[2:]).strip()
        assert len(prose) > 0, "Should have prose content"

    def test_all_validation_criteria_met(self):
        """Test that file passes all validation criteria together."""
        test_file = Path("test-0h4oez.md")

        # File exists
        assert test_file.exists()

        # Check binary properties
        binary_content = test_file.read_bytes()
        file_size = len(binary_content)

        # UTF-8 without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # No CRLF line endings
        assert b"\r\n" not in binary_content

        # File size in range
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

        # Markdown structure
        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")
        assert lines[0].startswith("# ")
        assert lines[1] == ""
        prose = "\n".join(lines[2:]).strip()
        assert len(prose) > 0
