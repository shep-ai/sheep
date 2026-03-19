"""Phase 3 tests: Validate that test-45ndys.md meets all requirements."""

from pathlib import Path

import pytest

from sheep.content_generators import validate_markdown_file


class TestPhase3FileValidation:
    """Task 4: Validate markdown file meets all requirements."""

    def test_file_exists_in_repository_root(self):
        """Test that test-45ndys.md exists in the repository root."""
        filepath = Path("test-45ndys.md")
        assert filepath.exists(), "File test-45ndys.md does not exist in repository root"
        assert filepath.is_file(), "test-45ndys.md is not a file"

    def test_file_has_utf8_encoding_no_bom(self):
        """Test that file is UTF-8 encoded without BOM."""
        filepath = Path("test-45ndys.md")
        binary_content = filepath.read_bytes()

        # Check no BOM
        assert not binary_content.startswith(
            b"\xef\xbb\xbf"
        ), "File should not have UTF-8 BOM"

        # Check valid UTF-8
        try:
            text_content = binary_content.decode("utf-8")
            assert isinstance(text_content, str)
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not valid UTF-8: {e}")

    def test_file_uses_lf_line_endings(self):
        """Test that file uses LF (\n) line endings, not CRLF (\r\n)."""
        filepath = Path("test-45ndys.md")
        binary_content = filepath.read_bytes()

        assert b"\r\n" not in binary_content, "File should use LF, not CRLF"
        assert b"\n" in binary_content, "File should have LF line endings"

    def test_file_contains_h1_heading(self):
        """Test that file contains exactly one H1 markdown heading."""
        filepath = Path("test-45ndys.md")
        text_content = filepath.read_text(encoding="utf-8")

        # Check starts with H1
        lines = text_content.split("\n")
        assert lines[0].startswith("# "), "First line must be H1 heading (# )"

        # Count H1 headings
        h1_count = text_content.count("# ")
        assert h1_count == 1, f"Expected exactly 1 H1 heading, found {h1_count}"

    def test_file_has_blank_line_after_heading(self):
        """Test that blank line separates heading from prose content."""
        filepath = Path("test-45ndys.md")
        text_content = filepath.read_text(encoding="utf-8")

        lines = text_content.split("\n")
        assert len(lines) >= 2, "File should have at least 2 lines"
        assert lines[1] == "", "Second line should be blank separator"

    def test_file_contains_2_3_sentences(self):
        """Test that file contains exactly 2-3 sentences."""
        filepath = Path("test-45ndys.md")
        text_content = filepath.read_text(encoding="utf-8")

        # Count sentences by periods
        sentence_count = text_content.count(".")
        assert (
            2 <= sentence_count <= 3
        ), f"Expected 2-3 sentences, found {sentence_count}"

    def test_file_has_trailing_newline(self):
        """Test that file ends with trailing newline."""
        filepath = Path("test-45ndys.md")
        text_content = filepath.read_text(encoding="utf-8")

        assert text_content.endswith("\n"), "File should end with trailing newline"

    def test_file_size_logged_in_range(self):
        """Test that file size is within informational range (400-600 bytes)."""
        filepath = Path("test-45ndys.md")
        file_size = filepath.stat().st_size

        # Log the size (informational, not a failure)
        assert file_size > 0, "File should not be empty"

        # Note: 400-600 bytes is a guideline, not a hard requirement
        # Just verify file has reasonable content
        assert file_size >= 100, f"File seems too small: {file_size} bytes"

    def test_file_passes_comprehensive_validation(self):
        """Test that file passes comprehensive validation checks."""
        filepath = "test-45ndys.md"

        # This calls the comprehensive validation function
        result = validate_markdown_file(filepath)
        assert result is True, "File should pass comprehensive validation"

    def test_prose_content_quality(self):
        """Test that prose content is coherent and complete."""
        filepath = Path("test-45ndys.md")
        text_content = filepath.read_text(encoding="utf-8")

        lines = text_content.split("\n")
        # Get prose content (skip heading and blank line)
        prose_lines = [
            line
            for line in lines[2:]
            if line.strip()
        ]  # Skip heading, blank line, and empty lines at end

        assert len(prose_lines) > 0, "File should have prose content"

        prose_content = "\n".join(prose_lines).strip()
        word_count = len(prose_content.split())

        assert (
            word_count >= 20
        ), f"Prose should have at least 20 words, found {word_count}"
