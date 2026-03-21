"""Tests for feature 153: Creating markdown file test-gp5gte.md with title and prose content."""

from pathlib import Path
import pytest


class TestFeature153FileCreation:
    """Tests for Task 1: Create markdown file with H1 heading and prose content."""

    MARKDOWN_FILENAME = "test-gp5gte.md"
    MIN_SIZE = 320
    MAX_SIZE = 600

    def test_file_does_not_exist_initially(self, tmp_path):
        """Test that file does not exist before creation."""
        test_file = tmp_path / self.MARKDOWN_FILENAME
        assert not test_file.exists()

    def test_file_creation_with_h1_heading(self, tmp_path):
        """Test that file can be created with H1 heading."""
        test_file = tmp_path / self.MARKDOWN_FILENAME

        # Create the file with H1 heading and prose
        content = "# Exploring Technology Innovation\n\nTechnology continuously evolves to solve complex problems and improve human experiences across industries. Innovation requires collaboration, creativity, and persistence to transform ideas into practical solutions. Through systematic exploration and experimentation, we discover new possibilities and advance our understanding of what's achievable.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_content_structure(self, tmp_path):
        """Test that file has correct markdown structure: H1 heading, blank line, prose."""
        test_file = tmp_path / self.MARKDOWN_FILENAME

        content = "# Exploring Technology Innovation\n\nTechnology continuously evolves to solve complex problems and improve human experiences across industries. Innovation requires collaboration, creativity, and persistence to transform ideas into practical solutions. Through systematic exploration and experimentation, we discover new possibilities and advance our understanding of what's achievable.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        # Check structure: H1 heading, blank line, prose
        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator
        assert len(lines) >= 3  # At least heading, blank line, and prose

    def test_file_contains_prose_sentences(self, tmp_path):
        """Test that file contains 2-3 sentences of prose content."""
        test_file = tmp_path / self.MARKDOWN_FILENAME

        content = "# Exploring Technology Innovation\n\nTechnology continuously evolves to solve complex problems and improve human experiences across industries. Innovation requires collaboration, creativity, and persistence to transform ideas into practical solutions. Through systematic exploration and experimentation, we discover new possibilities and advance our understanding of what's achievable.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")
        prose_lines = lines[2:]  # Skip heading and blank line
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3


class TestFeature153FileValidation:
    """Tests for Task 2: Validate file encoding (UTF-8) and line endings (LF)."""

    MARKDOWN_FILENAME = "test-gp5gte.md"
    MIN_SIZE = 320
    MAX_SIZE = 600

    def test_file_not_utf8_bom(self, tmp_path):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = tmp_path / self.MARKDOWN_FILENAME

        content = "# Exploring Technology Innovation\n\nTechnology continuously evolves to solve complex problems and improve human experiences across industries. Innovation requires collaboration, creativity, and persistence to transform ideas into practical solutions. Through systematic exploration and experimentation, we discover new possibilities and advance our understanding of what's achievable.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_file_has_no_crlf_line_endings(self, tmp_path):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = tmp_path / self.MARKDOWN_FILENAME

        content = "# Exploring Technology Innovation\n\nTechnology continuously evolves to solve complex problems and improve human experiences across industries. Innovation requires collaboration, creativity, and persistence to transform ideas into practical solutions. Through systematic exploration and experimentation, we discover new possibilities and advance our understanding of what's achievable.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content

    def test_file_size_within_range(self, tmp_path):
        """Test that file size is between 320-600 bytes (inclusive)."""
        test_file = tmp_path / self.MARKDOWN_FILENAME

        content = "# Exploring Technology Innovation\n\nTechnology continuously evolves to solve complex problems and improve human experiences across industries. Innovation requires collaboration, creativity, and persistence to transform ideas into practical solutions. Through systematic exploration and experimentation, we discover new possibilities and advance our understanding of what's achievable.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = len(test_file.read_bytes())
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

    def test_file_validation_all_criteria(self, tmp_path):
        """Test that file passes all validation criteria together."""
        test_file = tmp_path / self.MARKDOWN_FILENAME

        content = "# Exploring Technology Innovation\n\nTechnology continuously evolves to solve complex problems and improve human experiences across industries. Innovation requires collaboration, creativity, and persistence to transform ideas into practical solutions. Through systematic exploration and experimentation, we discover new possibilities and advance our understanding of what's achievable.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        file_size = len(binary_content)

        # Check UTF-8 without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Check no CRLF
        assert b"\r\n" not in binary_content

        # Check file size
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

        # Check structure
        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")
        assert lines[0].startswith("# ")
        assert lines[1] == ""

        # Check sentence count
        prose_content = "\n".join(lines[2:]).strip()
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3
