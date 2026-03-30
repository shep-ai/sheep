"""
Comprehensive test suite for feature 283: markdown file creation.

This module provides complete test coverage for feature 283, which creates
a markdown file (test-5gqu96.md) with hard-coded content, proper structure,
encoding, and line endings.

Test Coverage:
- File exists at repository root with correct filename
- Content structure (H1 heading + blank line + prose)
- Encoding validation (UTF-8 without BOM)
- Line ending validation (Unix LF, no Windows CRLF)
- Prose content validation (2-3 sentences)
- File size validation (400-600 bytes)
- End-to-end integration of the complete workflow
"""

from pathlib import Path

import pytest


class TestMarkdownFileCreation:
    """Tests for the markdown file creation feature 283."""

    @pytest.fixture
    def repo_root(self):
        """Get the repository root directory."""
        return Path.cwd()

    @pytest.fixture
    def test_file_path(self, repo_root):
        """Return the expected test file path."""
        return repo_root / "test-5gqu96.md"

    def test_file_exists(self, test_file_path):
        """Test that the markdown file exists in the repository root."""
        assert test_file_path.exists(), f"File does not exist: {test_file_path}"

    def test_file_is_regular_file(self, test_file_path):
        """Test that the markdown file is a regular file, not a directory."""
        assert test_file_path.is_file(), f"Path is not a file: {test_file_path}"

    def test_file_has_correct_name(self, test_file_path):
        """Test that the file has the exact name test-5gqu96.md."""
        assert test_file_path.name == "test-5gqu96.md"

    def test_file_is_in_repository_root(self, test_file_path, repo_root):
        """Test that the file is located in the repository root."""
        assert test_file_path.parent == repo_root


class TestMarkdownStructure:
    """Tests for the markdown structure (H1 heading + prose)."""

    @pytest.fixture
    def test_file_path(self):
        """Return the expected test file path."""
        return Path.cwd() / "test-5gqu96.md"

    @pytest.fixture
    def file_content(self, test_file_path):
        """Read and return the file content as text."""
        return test_file_path.read_text(encoding="utf-8")

    @pytest.fixture
    def file_lines(self, file_content):
        """Split file content into lines."""
        return file_content.split("\n")

    def test_file_contains_h1_heading(self, file_content):
        """Test that file starts with H1 markdown heading."""
        assert file_content.startswith("# "), "File must start with H1 heading (# )"

    def test_file_has_blank_line_separator(self, file_content):
        """Test that file has blank line after heading."""
        assert "\n\n" in file_content, "File must have blank line after heading"

    def test_first_line_is_heading(self, file_lines):
        """Test that the first line is an H1 heading."""
        assert file_lines[0].startswith("# "), "First line must be H1 heading"

    def test_second_line_is_empty(self, file_lines):
        """Test that the second line is empty (blank line separator)."""
        assert file_lines[1] == "", "Second line must be empty (separator)"

    def test_prose_starts_at_third_line(self, file_lines):
        """Test that prose content starts at line 3."""
        # Line 0: heading, Line 1: blank, Line 2+: prose
        assert len(file_lines) >= 3, "File must have prose content after heading"
        assert file_lines[2].strip(), "Third line must have prose content"

    def test_heading_is_not_empty(self, file_lines):
        """Test that the heading has actual text (not just '# ')."""
        heading = file_lines[0]
        heading_text = heading.replace("# ", "").strip()
        assert heading_text, "Heading must have actual text"

    def test_prose_content_exists(self, file_lines):
        """Test that prose content exists after heading and blank line."""
        prose_lines = file_lines[2:]
        # Remove trailing empty lines
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        assert len(prose_lines) > 0, "File must have prose content"
        prose = "\n".join(prose_lines).strip()
        assert len(prose) > 0, "Prose content must not be empty"


class TestMarkdownEncoding:
    """Tests for file encoding (UTF-8 without BOM)."""

    @pytest.fixture
    def test_file_path(self):
        """Return the expected test file path."""
        return Path.cwd() / "test-5gqu96.md"

    @pytest.fixture
    def file_bytes(self, test_file_path):
        """Read file as bytes."""
        return test_file_path.read_bytes()

    def test_file_has_no_utf8_bom(self, file_bytes):
        """Test that file does not have UTF-8 BOM (0xEF 0xBB 0xBF)."""
        assert not file_bytes.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

    def test_file_is_valid_utf8(self, file_bytes):
        """Test that file is valid UTF-8 encoding."""
        try:
            file_bytes.decode("utf-8")
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not valid UTF-8: {e}")

    def test_file_can_be_read_as_utf8(self, test_file_path):
        """Test that file can be read as UTF-8 text."""
        try:
            test_file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError as e:
            pytest.fail(f"Cannot read file as UTF-8: {e}")


class TestLineEndings:
    """Tests for line endings (Unix LF, not Windows CRLF)."""

    @pytest.fixture
    def test_file_path(self):
        """Return the expected test file path."""
        return Path.cwd() / "test-5gqu96.md"

    @pytest.fixture
    def file_bytes(self, test_file_path):
        """Read file as bytes."""
        return test_file_path.read_bytes()

    def test_file_uses_lf_not_crlf(self, file_bytes):
        """Test that file uses Unix LF line endings, not Windows CRLF."""
        assert b"\r\n" not in file_bytes, "File should not use CRLF line endings"

    def test_file_contains_lf(self, file_bytes):
        """Test that file contains LF line endings."""
        assert b"\n" in file_bytes, "File should contain LF line endings"

    def test_file_has_no_carriage_returns(self, file_bytes):
        """Test that file does not contain carriage return characters."""
        assert b"\r" not in file_bytes, "File should not contain carriage returns (\\r)"

    def test_line_breaks_are_only_lf(self, file_bytes):
        """Test that line breaks use only LF (0x0A), not CRLF."""
        # If it contains CRLF, this test already failed above
        # This is a redundant test for clarity
        lf_count = file_bytes.count(b"\n")
        crlf_count = file_bytes.count(b"\r\n")
        # CRLF count should be zero
        assert crlf_count == 0, "File should not contain CRLF"
        # LF count should be greater than 0
        assert lf_count > 0, "File should contain LF line endings"


class TestProseContent:
    """Tests for prose content validation."""

    @pytest.fixture
    def test_file_path(self):
        """Return the expected test file path."""
        return Path.cwd() / "test-5gqu96.md"

    @pytest.fixture
    def file_content(self, test_file_path):
        """Read file content as text."""
        return test_file_path.read_text(encoding="utf-8")

    @pytest.fixture
    def prose_content(self, file_content):
        """Extract prose content (skip heading and blank line)."""
        lines = file_content.split("\n")
        prose_lines = lines[2:]  # Skip heading (line 0) and blank line (line 1)

        # Remove trailing empty lines
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        return "\n".join(prose_lines).strip()

    def test_prose_has_2_to_3_sentences(self, prose_content):
        """Test that prose contains exactly 2-3 sentences (periods)."""
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3, f"Prose should have 2-3 sentences, found {sentence_count}"

    def test_prose_is_not_empty(self, prose_content):
        """Test that prose content is not empty."""
        assert prose_content, "Prose content must not be empty"

    def test_prose_is_readable(self, prose_content):
        """Test that prose content is readable (has reasonable length)."""
        # Prose should be more than 50 characters (reasonable minimum)
        assert len(prose_content) > 50, "Prose content is too short to be meaningful"

    def test_prose_sentences_are_well_formed(self, prose_content):
        """Test that sentences appear to be well-formed."""
        # Each sentence should be followed by a space or end of string
        # (except the last sentence)
        sentences = prose_content.split(". ")
        # Should have 2-3 parts when split by ". "
        assert len(sentences) >= 2, "Prose should have well-formed sentences separated by periods"


class TestFileSizeRequirements:
    """Tests for file size validation."""

    @pytest.fixture
    def test_file_path(self):
        """Return the expected test file path."""
        return Path.cwd() / "test-5gqu96.md"

    def test_file_size_is_within_range(self, test_file_path):
        """Test that file size falls within 400-600 bytes."""
        file_size = test_file_path.stat().st_size
        assert 400 <= file_size <= 600, f"File size {file_size} bytes outside 400-600 byte range"

    def test_file_size_is_not_empty(self, test_file_path):
        """Test that file is not empty."""
        file_size = test_file_path.stat().st_size
        assert file_size > 0, "File must not be empty"

    def test_file_size_is_reasonable(self, test_file_path):
        """Test that file size is reasonable (not too small)."""
        # At minimum: "# Title\n\nSentence. Sentence." is about 35 bytes
        # We expect at least 100 bytes for properly formed content
        file_size = test_file_path.stat().st_size
        assert file_size >= 100, f"File size {file_size} is too small"


class TestEndingNewline:
    """Tests for trailing newline requirement."""

    @pytest.fixture
    def test_file_path(self):
        """Return the expected test file path."""
        return Path.cwd() / "test-5gqu96.md"

    @pytest.fixture
    def file_bytes(self, test_file_path):
        """Read file as bytes."""
        return test_file_path.read_bytes()

    def test_file_ends_with_newline(self, file_bytes):
        """Test that file ends with a newline character."""
        assert file_bytes.endswith(b"\n"), "File should end with a newline"

    def test_file_does_not_end_with_double_newline(self, file_bytes):
        """Test that file does not end with double newline."""
        # File should end with exactly one newline, not multiple
        assert not file_bytes.endswith(b"\n\n"), "File should end with single newline, not double"
