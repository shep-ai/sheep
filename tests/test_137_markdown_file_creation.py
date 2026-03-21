"""Tests for feature 137: Creating markdown file test-narzc3.md with title and prose content."""

from pathlib import Path
import pytest


class TestMarkdownFileCreation:
    """Tests for task-1: Create markdown file with H1 heading and prose content."""

    def test_file_exists(self):
        """Test that file test-narzc3.md exists at repository root."""
        test_file = Path("test-narzc3.md")
        assert test_file.exists(), "File test-narzc3.md does not exist"

    def test_file_has_h1_heading(self):
        """Test that created file contains H1 heading on first line."""
        test_file = Path("test-narzc3.md")
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        assert lines[0].startswith("# "), f"First line must start with '# ', got: {lines[0]!r}"

    def test_file_has_blank_line_separator(self):
        """Test that file has blank line after H1 heading."""
        test_file = Path("test-narzc3.md")
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        assert len(lines) >= 3, "File must have at least 3 lines (heading, blank, prose)"
        assert lines[1] == "", f"Line 2 must be blank, got: {lines[1]!r}"

    def test_file_contains_prose_content(self):
        """Test that file contains prose content after heading and blank line."""
        test_file = Path("test-narzc3.md")
        content = test_file.read_text(encoding="utf-8")
        prose_content = content.split("\n\n", 1)
        assert len(prose_content) >= 2, "File must have prose content after blank line"
        assert prose_content[1].strip(), "Prose content must not be empty"


class TestMarkdownFileValidation:
    """Tests for task-2: Validate file encoding, line endings, and structure."""

    MIN_SIZE = 320
    MAX_SIZE = 600

    def test_file_not_utf8_bom(self):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = Path("test-narzc3.md")
        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(
            b"\xef\xbb\xbf"
        ), "File contains UTF-8 BOM (Byte Order Mark), which is not allowed"

    def test_file_has_no_crlf_line_endings(self):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = Path("test-narzc3.md")
        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content, (
            "File contains Windows-style CRLF line endings; must use Unix LF"
        )

    def test_file_size_within_range(self):
        """Test that file size is between 320-600 bytes (inclusive)."""
        test_file = Path("test-narzc3.md")
        file_size = len(test_file.read_bytes())
        assert (
            self.MIN_SIZE <= file_size <= self.MAX_SIZE
        ), f"File size {file_size} bytes is outside acceptable range ({self.MIN_SIZE}-{self.MAX_SIZE} bytes)"

    def test_prose_contains_two_or_three_sentences(self):
        """Test that prose contains 2-3 sentences."""
        test_file = Path("test-narzc3.md")
        content = test_file.read_text(encoding="utf-8")

        # Extract prose content (skip heading and blank line)
        prose_content = content.split("\n\n", 1)[1].strip()

        # Count sentences (periods, question marks, exclamation marks)
        sentence_count = prose_content.count(".") + prose_content.count("?") + prose_content.count("!")

        assert 2 <= sentence_count <= 3, (
            f"Prose must contain 2-3 sentences, found {sentence_count}"
        )

    def test_validation_all_criteria_met(self):
        """Test that file passes all validation criteria together."""
        test_file = Path("test-narzc3.md")

        # Check file exists
        assert test_file.exists(), "File test-narzc3.md does not exist"

        binary_content = test_file.read_bytes()
        file_size = len(binary_content)
        text_content = test_file.read_text(encoding="utf-8")

        # Check UTF-8 without BOM
        assert not binary_content.startswith(
            b"\xef\xbb\xbf"
        ), "File contains UTF-8 BOM"

        # Check no CRLF
        assert b"\r\n" not in binary_content, "File contains CRLF line endings"

        # Check file size
        assert (
            self.MIN_SIZE <= file_size <= self.MAX_SIZE
        ), f"File size {file_size} is outside acceptable range"

        # Check structure
        lines = text_content.split("\n")
        assert lines[0].startswith("# "), "First line must be H1 heading"
        assert lines[1] == "", "Second line must be blank"

        # Check prose sentences
        prose_content = text_content.split("\n\n", 1)[1].strip()
        sentence_count = prose_content.count(".") + prose_content.count("?") + prose_content.count("!")
        assert 2 <= sentence_count <= 3, f"Prose must have 2-3 sentences, found {sentence_count}"
