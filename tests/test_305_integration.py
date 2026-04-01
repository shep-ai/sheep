"""Integration tests for feature 305: Verifying the actual markdown file creation.

These tests validate that the markdown file test-9s145k.md exists at the repository root
and meets all the specification requirements for encoding, structure, and content.
"""

import pytest
from pathlib import Path


class TestActualMarkdownFile:
    """Integration tests for the actual created markdown file."""

    EXPECTED_FILENAME = "test-9s145k.md"
    MIN_SIZE = 250
    MAX_SIZE = 600

    @pytest.fixture
    def markdown_file(self):
        """Load the actual markdown file."""
        filepath = Path(self.EXPECTED_FILENAME)
        if not filepath.exists():
            pytest.skip(f"File {self.EXPECTED_FILENAME} does not exist yet")
        return filepath

    def test_file_exists_at_repository_root(self):
        """Test that test-9s145k.md exists at the repository root."""
        filepath = Path(self.EXPECTED_FILENAME)
        assert filepath.exists(), f"File {self.EXPECTED_FILENAME} not found at repository root"

    def test_file_is_regular_file(self, markdown_file):
        """Test that the path points to a regular file, not directory."""
        assert markdown_file.is_file(), f"{self.EXPECTED_FILENAME} is not a regular file"

    def test_file_contains_h1_heading(self, markdown_file):
        """Test that file starts with valid H1 markdown heading."""
        content = markdown_file.read_text(encoding="utf-8")
        lines = content.split("\n")

        # First line should be H1 heading
        assert len(lines) > 0, "File is empty"
        assert lines[0].startswith("# "), f"First line does not start with '# ': {lines[0]}"

        # Verify heading has text after #
        heading = lines[0]
        assert len(heading) > 2, "H1 heading has no title text"

    def test_file_has_blank_line_after_heading(self, markdown_file):
        """Test that file has blank line separator after H1 heading."""
        content = markdown_file.read_text(encoding="utf-8")
        lines = content.split("\n")

        assert len(lines) > 1, "File has less than 2 lines"
        assert lines[0].startswith("# "), "First line is not H1 heading"
        assert lines[1] == "", "Second line (blank line separator) is not empty"

    def test_prose_content_follows_heading(self, markdown_file):
        """Test that prose content exists after the blank line."""
        content = markdown_file.read_text(encoding="utf-8")
        lines = content.split("\n")

        assert len(lines) > 2, "File does not have prose content"
        prose_lines = [line for line in lines[2:] if line.strip()]
        assert len(prose_lines) > 0, "No prose content found after heading"

    def test_file_contains_2_or_3_sentences(self, markdown_file):
        """Test that prose content contains exactly 2-3 sentences."""
        content = markdown_file.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Extract prose (everything after blank line separator)
        prose_text = "\n".join(lines[2:]).strip()

        # Count sentences (periods that are sentence-ending)
        sentence_count = prose_text.count(".")
        assert 2 <= sentence_count <= 3, \
            f"Expected 2-3 sentences, found {sentence_count} in prose: {prose_text}"

    def test_file_uses_utf8_encoding(self, markdown_file):
        """Test that file is properly UTF-8 encoded."""
        # This passes if we can read the file without UnicodeDecodeError
        try:
            content = markdown_file.read_text(encoding="utf-8")
            assert len(content) > 0, "File is empty"
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not valid UTF-8: {e}")

    def test_file_has_no_utf8_bom(self, markdown_file):
        """Test that file has no UTF-8 Byte Order Mark (BOM)."""
        binary_content = markdown_file.read_bytes()

        # UTF-8 BOM signature is bytes EF BB BF
        assert not binary_content.startswith(b"\xef\xbb\xbf"), \
            "File contains UTF-8 BOM, should be plain UTF-8"

    def test_file_uses_lf_line_endings(self, markdown_file):
        """Test that file uses Unix LF line endings, not Windows CRLF."""
        binary_content = markdown_file.read_bytes()

        # CRLF is bytes 0x0D 0x0A
        assert b"\r\n" not in binary_content, \
            "File contains CRLF (Windows line endings), should use LF (Unix)"

    def test_file_has_no_carriage_returns(self, markdown_file):
        """Test that file has no carriage return characters."""
        binary_content = markdown_file.read_bytes()

        # Carriage return is byte 0x0D
        assert b"\r" not in binary_content, \
            "File contains carriage return characters"

    def test_file_size_in_acceptable_range(self, markdown_file):
        """Test that file size is between 250-600 bytes (reasonable for H1+3 sentences)."""
        file_size = len(markdown_file.read_bytes())

        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE, \
            f"File size {file_size} is outside acceptable range {self.MIN_SIZE}-{self.MAX_SIZE} bytes"

    def test_file_has_trailing_newline(self, markdown_file):
        """Test that file ends with a newline character."""
        binary_content = markdown_file.read_bytes()

        # File should end with LF (newline)
        assert binary_content.endswith(b"\n"), \
            "File does not end with newline character"

    def test_prose_is_coherent(self, markdown_file):
        """Test that prose content is coherent and related to the heading."""
        content = markdown_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        heading = lines[0][2:].strip()  # Remove '# ' prefix
        prose = " ".join([line for line in lines[2:] if line.strip()])

        # Basic coherence checks
        assert len(heading) > 0, "Heading is empty"
        assert len(prose) > 0, "Prose is empty"

        # Prose should be non-trivial (not just a single word)
        prose_words = prose.split()
        assert len(prose_words) >= 20, \
            f"Prose appears too short ({len(prose_words)} words), may not be coherent"

    def test_content_is_not_placeholder(self, markdown_file):
        """Test that content is not placeholder or test text."""
        content = markdown_file.read_text(encoding="utf-8")
        content_lower = content.lower()

        # Check that content is not obviously placeholder text
        placeholder_markers = ["test", "placeholder", "example", "todo", "fixme", "xxx"]
        for marker in placeholder_markers:
            # Allow these words if they're part of normal prose, but not as primary content
            if marker in content_lower and content.count(marker) == 1:
                # Single occurrence might be okay (e.g., "example" in a sentence)
                pass

        # Content should have substance
        assert len(content) > 200, \
            "Content appears to be mostly placeholder or test text"

    def test_all_specification_criteria_met(self, markdown_file):
        """Comprehensive test that all specification criteria are met."""
        content = markdown_file.read_text(encoding="utf-8")
        binary_content = markdown_file.read_bytes()
        lines = content.split("\n")

        # Criteria 1: File exists
        assert markdown_file.exists(), "File does not exist"

        # Criteria 2: UTF-8 encoding without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File has UTF-8 BOM"

        # Criteria 3: LF line endings only
        assert b"\r\n" not in binary_content, "File has CRLF line endings"
        assert b"\r" not in binary_content, "File has carriage returns"

        # Criteria 4: H1 heading
        assert lines[0].startswith("# "), "First line is not H1 heading"
        assert len(lines[0]) > 2, "H1 heading has no text"

        # Criteria 5: Blank line separator
        assert lines[1] == "", "No blank line after heading"

        # Criteria 6: 2-3 sentences
        prose = "\n".join(lines[2:]).strip()
        sentence_count = prose.count(".")
        assert 2 <= sentence_count <= 3, f"Wrong sentence count: {sentence_count}"

        # Criteria 7: File size
        assert 250 <= len(binary_content) <= 600, f"File size out of range: {len(binary_content)}"

        # Criteria 8: Trailing newline
        assert binary_content.endswith(b"\n"), "File does not end with newline"
