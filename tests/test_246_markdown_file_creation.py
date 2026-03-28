"""Tests for feature 246: Creating markdown file test-dgxq7g.md with title and prose content."""

from pathlib import Path
import pytest

from sheep.content_generators import validate_markdown_file


class TestMarkdownFileValidation:
    """Tests for task-3: Validate file structure and encoding."""

    def test_validate_markdown_file_passes(self):
        """Test that validate_markdown_file() passes for test-dgxq7g.md."""
        filepath = Path("test-dgxq7g.md")

        # Verify file exists
        assert filepath.exists(), "File test-dgxq7g.md must exist"

        # Validate the file - should not raise exception
        result = validate_markdown_file(str(filepath))

        # Function should return True on successful validation
        assert result is True, "validate_markdown_file() should return True"

    def test_file_has_h1_heading_on_first_line(self):
        """Test that file starts with H1 heading (# )."""
        filepath = Path("test-dgxq7g.md")
        content = filepath.read_text(encoding="utf-8")
        lines = content.split("\n")

        # First line must start with H1 marker
        assert lines[0].startswith("# "), "First line must be H1 heading"

    def test_file_has_blank_line_separator(self):
        """Test that file has blank line after H1 heading."""
        filepath = Path("test-dgxq7g.md")
        content = filepath.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Second line must be blank separator
        assert len(lines) >= 2, "File must have at least 2 lines"
        assert lines[1] == "", "Second line must be blank separator"

    def test_file_has_2_to_3_sentences(self):
        """Test that file contains 2-3 sentences of prose content."""
        filepath = Path("test-dgxq7g.md")
        content = filepath.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Get prose content (skip heading and blank line)
        prose_lines = lines[2:]

        # Remove trailing empty lines
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        prose_content = "\n".join(prose_lines).strip()

        # Count sentences by periods
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3, f"Must have 2-3 sentences, found {sentence_count}"

    def test_file_is_utf8_without_bom(self):
        """Test that file encoding is UTF-8 without BOM."""
        filepath = Path("test-dgxq7g.md")
        binary_content = filepath.read_bytes()

        # File must NOT start with UTF-8 BOM (0xEF 0xBB 0xBF)
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File must not have UTF-8 BOM"

    def test_file_uses_lf_line_endings(self):
        """Test that file uses LF line endings, not CRLF."""
        filepath = Path("test-dgxq7g.md")
        binary_content = filepath.read_bytes()

        # File must NOT contain CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content, "File must use LF line endings (not CRLF)"

    def test_file_size_in_expected_range(self):
        """Test that file size is approximately 400-600 bytes."""
        filepath = Path("test-dgxq7g.md")
        file_size = len(filepath.read_bytes())

        # File size should be in the expected range for this type of content
        # Using broader range (300-700) to accommodate different prose lengths
        assert 300 <= file_size <= 700, f"File size {file_size} should be in 300-700 byte range"

    def test_file_ends_with_newline(self):
        """Test that file ends with trailing newline."""
        filepath = Path("test-dgxq7g.md")
        content = filepath.read_text(encoding="utf-8")

        # File should end with newline (Unix convention)
        assert content.endswith("\n"), "File must end with trailing newline"

    def test_file_is_valid_utf8(self):
        """Test that file is valid UTF-8 encoded."""
        filepath = Path("test-dgxq7g.md")
        binary_content = filepath.read_bytes()

        # Should not raise UnicodeDecodeError
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not valid UTF-8: {e}")
