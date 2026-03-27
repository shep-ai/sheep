"""Tests for feature 241: Creating markdown file test-g0s8t1.md with title and prose content."""

from pathlib import Path


class TestMarkdownFileCreation:
    """Tests for task-1: Create markdown file with H1 heading and prose content."""

    def test_file_exists_at_repository_root(self):
        """Test that file test-g0s8t1.md exists at repository root."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists(), "File test-g0s8t1.md does not exist at repository root"

    def test_creates_file_with_h1_heading(self):
        """Test that created file contains H1 heading on first line."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists()
        content = test_file.read_text(encoding="utf-8")
        assert content.startswith("# "), "File does not start with H1 heading (# )"

    def test_file_contains_two_or_three_sentences(self):
        """Test that file contains 2-3 sentences (ending with periods)."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists()
        text_content = test_file.read_text(encoding="utf-8")

        # Extract prose content (skip heading and blank line)
        lines = text_content.split("\n")
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    def test_file_has_blank_line_separator(self):
        """Test that file has blank line after H1 heading."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists()
        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# "), "First line should be H1 heading"
        assert lines[1] == "", f"Second line should be blank, got: {repr(lines[1])}"

    def test_file_size_within_expected_range(self):
        """Test that file size is naturally in the 400-600 byte range."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists()
        file_size = test_file.stat().st_size
        # Typical range for properly formatted markdown file with this structure
        assert 350 <= file_size <= 650, f"File size {file_size} is outside expected range 350-650"


class TestMarkdownFileValidation:
    """Tests for task-1: Validate file encoding and line endings."""

    def test_file_not_utf8_bom(self):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists()
        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File contains UTF-8 BOM which should not be present"

    def test_file_has_lf_line_endings_not_crlf(self):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists()
        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content, "File contains CRLF which should be LF only"

    def test_file_content_reads_as_valid_utf8(self):
        """Test that file content can be read back as valid UTF-8."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists()
        # Should not raise an exception
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content is not None
        assert len(read_content) > 0
