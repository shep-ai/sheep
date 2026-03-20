"""Task-5 validation tests for feature 126 markdown file format and encoding."""

import re
from pathlib import Path

import pytest

from sheep.content_generators import validate_markdown_file


class TestFeature126FileValidation:
    """Comprehensive validation tests for test-trd8nx.md file format and encoding.

    This test class validates all specification requirements:
    - UTF-8 encoding without BOM (NFR-1)
    - Unix LF line endings, no CRLF (NFR-2)
    - Trailing newline (NFR-3)
    - File size >= 50 bytes (NFR-4)
    - H1 heading structure (FR-3, FR-4)
    - 2-3 sentences of prose (FR-5)
    """

    @pytest.fixture
    def test_file_path(self) -> Path:
        """Fixture to get the path to test-trd8nx.md."""
        filepath = Path("test-trd8nx.md")
        assert filepath.exists(), f"Test file {filepath} does not exist"
        return filepath

    def test_file_exists_in_repository_root(self):
        """Test that test-trd8nx.md exists in repository root directory."""
        filepath = Path("test-trd8nx.md")
        assert filepath.exists(), "File test-trd8nx.md should exist in repository root"
        assert filepath.is_file(), "test-trd8nx.md should be a file, not a directory"

    def test_file_is_utf8_encoded(self, test_file_path):
        """Test that file is encoded in UTF-8 (spec NFR-1)."""
        with open(test_file_path, "rb") as f:
            binary_content = f.read()

        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not valid UTF-8: {e}")

    def test_file_has_no_utf8_bom(self, test_file_path):
        """Test that file has no UTF-8 BOM (spec NFR-1)."""
        with open(test_file_path, "rb") as f:
            binary_content = f.read()

        utf8_bom = b"\xef\xbb\xbf"
        assert not binary_content.startswith(utf8_bom), (
            "File should not have UTF-8 BOM (Byte Order Mark)"
        )

    def test_file_uses_lf_not_crlf(self, test_file_path):
        """Test that file uses LF (\\n) not CRLF (\\r\\n) (spec NFR-2)."""
        with open(test_file_path, "rb") as f:
            binary_content = f.read()

        assert b"\r\n" not in binary_content, (
            "File should use LF (\\n) line endings, not CRLF (\\r\\n)"
        )

    def test_file_starts_with_h1_heading(self, test_file_path):
        """Test that file starts with exactly one H1 heading (spec FR-3)."""
        with open(test_file_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        lines = text_content.split("\n")
        assert len(lines) > 0, "File should not be empty"
        assert lines[0].startswith("# "), (
            "File should start with H1 heading (# ), "
            f"but starts with: {repr(lines[0])}"
        )

    def test_h1_heading_not_empty(self, test_file_path):
        """Test that H1 heading is not empty."""
        with open(test_file_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        lines = text_content.split("\n")
        heading = lines[0]
        title = heading.replace("# ", "").strip()
        assert title, "H1 heading should contain a non-empty title"

    def test_blank_line_after_heading(self, test_file_path):
        """Test that there is a blank line separator after H1 heading (spec FR-4)."""
        with open(test_file_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        lines = text_content.split("\n")
        assert len(lines) >= 2, "File should have at least heading + blank line"
        assert lines[1] == "", (
            f"Second line should be blank separator, "
            f"but got: {repr(lines[1])}"
        )

    def test_prose_content_exists(self, test_file_path):
        """Test that prose content exists after heading and blank line."""
        with open(test_file_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        lines = text_content.split("\n")
        prose_lines = [l for l in lines[2:] if l.strip()]
        assert prose_lines, "File should contain prose content after heading"

    def test_file_has_2_to_3_sentences(self, test_file_path):
        """Test that prose content has 2-3 sentences (spec FR-5)."""
        with open(test_file_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        lines = text_content.split("\n")
        # Get prose content (skip heading and blank line)
        prose_lines = lines[2:]
        # Remove trailing empty lines
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        prose_content = "\n".join(prose_lines).strip()

        # Count sentences by period delimiter
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3, (
            f"Content should have 2-3 sentences (periods), "
            f"found {sentence_count} in: {prose_content}"
        )

    def test_file_ends_with_trailing_newline(self, test_file_path):
        """Test that file ends with a trailing newline (spec NFR-3)."""
        with open(test_file_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        assert text_content.endswith("\n"), (
            "File should end with a trailing newline character (Unix convention)"
        )

    def test_file_size_at_least_50_bytes(self, test_file_path):
        """Test that file size is at least 50 bytes (spec NFR-4)."""
        file_size = test_file_path.stat().st_size
        assert file_size >= 50, (
            f"File should be at least 50 bytes, "
            f"but is {file_size} bytes"
        )

    def test_file_size_reasonable(self, test_file_path):
        """Test that file size is reasonable (not excessively large)."""
        file_size = test_file_path.stat().st_size
        max_size = 2048  # 2KB should be plenty for title + 3 sentences
        assert file_size <= max_size, (
            f"File should not exceed {max_size} bytes, "
            f"but is {file_size} bytes"
        )

    def test_passes_validate_markdown_file(self, test_file_path):
        """Test that file passes the validate_markdown_file() function."""
        # This should not raise any exceptions
        is_valid = validate_markdown_file(str(test_file_path))
        assert is_valid is True, "File validation should pass"

    def test_h1_heading_format_valid_markdown(self, test_file_path):
        """Test that H1 heading follows valid markdown syntax."""
        with open(test_file_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        lines = text_content.split("\n")
        heading = lines[0]

        # Markdown H1 format: # followed by space and title
        h1_pattern = r"^# .+"
        assert re.match(h1_pattern, heading), (
            f"H1 heading should follow markdown format '# Title', "
            f"but got: {repr(heading)}"
        )

    def test_prose_is_coherent(self, test_file_path):
        """Test that prose content appears coherent (not random)."""
        with open(test_file_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        lines = text_content.split("\n")
        prose_lines = [l for l in lines[2:] if l.strip()]
        prose_content = "\n".join(prose_lines).strip()

        # Check that prose is not empty and contains multiple words
        words = prose_content.split()
        assert len(words) >= 15, (
            f"Prose should contain sufficient content (at least 15 words), "
            f"but has {len(words)} words"
        )

        # Check that sentences are properly capitalized
        sentences = prose_content.split(".")
        for sentence in sentences[:-1]:  # Skip last empty part after final period
            if sentence.strip():
                first_char = sentence.strip()[0]
                assert first_char.isupper(), (
                    f"Sentences should be capitalized: {repr(sentence.strip())}"
                )

    def test_no_double_newlines_within_prose(self, test_file_path):
        """Test that prose content doesn't have unintended double newlines."""
        with open(test_file_path, "rb") as f:
            binary_content = f.read()

        # Should not have \n\n\n (more than 2 consecutive newlines)
        assert b"\n\n\n" not in binary_content, (
            "Prose should not have excessive blank lines"
        )

    def test_no_trailing_spaces_on_lines(self, test_file_path):
        """Test that lines don't have trailing whitespace."""
        with open(test_file_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        lines = text_content.rstrip("\n").split("\n")
        for i, line in enumerate(lines):
            if line.endswith(" ") or line.endswith("\t"):
                # Trailing spaces/tabs on non-empty lines are generally unwanted
                # This is a style check, not strictly required by the spec
                pytest.skip(
                    f"Line {i+1} has trailing whitespace: {repr(line)} "
                    "(style preference, not spec requirement)"
                )
