#!/usr/bin/env python3
"""
Tests for feature 194: markdown-file-creation-8ccfcb

Tests cover:
- Task 1: File creation with proper H1 heading and prose content
- Task 2: File encoding and line endings validation
- Task 3: Markdown structure and prose quality validation
"""

import os
import tempfile
from pathlib import Path

import pytest
from feature_194_implementation import (
    FILENAME,
    TITLE,
    create_file,
    validate_encoding,
    validate_structure,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = os.getcwd()
        os.chdir(tmpdir)
        yield Path(tmpdir)
        os.chdir(original_dir)


class TestTask1FileCreation:
    """Task 1: Create markdown file with H1 heading and prose content."""

    def test_file_does_not_exist_before_creation(self, temp_dir):
        """Verify file does not exist before creation."""
        file_path = Path(FILENAME)
        assert not file_path.exists(), f"File {FILENAME} should not exist before creation"

    def test_create_file_returns_path(self, temp_dir):
        """Verify create_file returns Path object."""
        result = create_file()
        assert result is not None, "create_file should return Path object"
        assert isinstance(result, Path), "Result should be Path object"

    def test_file_exists_after_creation(self, temp_dir):
        """Verify file exists after creation."""
        create_file()
        file_path = Path(FILENAME)
        assert file_path.exists(), f"File {FILENAME} should exist after creation"

    def test_file_has_h1_heading_on_line_1(self, temp_dir):
        """Verify file begins with H1 markdown heading."""
        create_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        lines = content.split("\n")
        assert lines[0].startswith("# "), "Line 1 should start with H1 heading '# '"
        assert TITLE in lines[0], f"Heading should contain title '{TITLE}'"

    def test_file_has_blank_line_on_line_2(self, temp_dir):
        """Verify line 2 is blank for readability."""
        create_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        lines = content.split("\n")
        assert len(lines) >= 2, "File should have at least 2 lines"
        assert lines[1] == "", "Line 2 should be blank"

    def test_file_has_prose_content(self, temp_dir):
        """Verify prose content exists on lines 3+."""
        create_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        lines = content.split("\n")
        assert len(lines) >= 3, "File should have prose content after blank line"
        prose = "\n".join(lines[2:]).strip()
        assert len(prose) > 0, "Prose content should not be empty"

    def test_file_size_in_range(self, temp_dir):
        """Verify file size is between 300-600 bytes."""
        create_file()
        file_size = Path(FILENAME).stat().st_size
        assert 300 <= file_size <= 600, (
            f"File size {file_size} bytes should be in 300-600 byte range"
        )

    def test_file_cannot_be_created_twice(self, temp_dir):
        """Verify file creation fails if file already exists."""
        create_file()
        result = create_file()
        assert result is None, "create_file should return None if file already exists"


class TestTask2Encoding:
    """Task 2: Validate file encoding and line endings."""

    def test_file_has_no_utf8_bom(self, temp_dir):
        """Verify file has no UTF-8 BOM (EF BB BF bytes)."""
        create_file()
        binary_content = Path(FILENAME).read_bytes()
        assert not binary_content.startswith(
            b"\xef\xbb\xbf"
        ), "File should not have UTF-8 BOM"

    def test_file_has_no_crlf(self, temp_dir):
        """Verify file uses LF line endings, not CRLF."""
        create_file()
        binary_content = Path(FILENAME).read_bytes()
        assert b"\r\n" not in binary_content, "File should use LF, not CRLF line endings"

    def test_file_is_valid_utf8(self, temp_dir):
        """Verify file is valid UTF-8 text."""
        create_file()
        binary_content = Path(FILENAME).read_bytes()
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            pytest.fail(f"File should be valid UTF-8: {e}")

    def test_validate_encoding_passes(self, temp_dir):
        """Verify validate_encoding returns True for valid file."""
        create_file()
        result = validate_encoding(Path(FILENAME))
        assert result is True, "validate_encoding should return True"

    def test_validate_encoding_fails_with_invalid_encoding(self, temp_dir):
        """Verify validate_encoding fails for invalid UTF-8."""
        # Create a file with invalid UTF-8
        Path(FILENAME).write_bytes(b"\xff\xfe")
        with pytest.raises(ValueError, match="File is not valid UTF-8"):
            validate_encoding(Path(FILENAME))

    def test_validate_encoding_fails_with_bom(self, temp_dir):
        """Verify validate_encoding fails for UTF-8 BOM."""
        # Create a file with UTF-8 BOM
        Path(FILENAME).write_bytes(b"\xef\xbb\xbf# Test\n\nProse.\n")
        with pytest.raises(ValueError, match="UTF-8 BOM"):
            validate_encoding(Path(FILENAME))

    def test_validate_encoding_fails_with_crlf(self, temp_dir):
        """Verify validate_encoding fails for CRLF line endings."""
        # Create a file with CRLF line endings
        Path(FILENAME).write_bytes(b"# Test\r\n\r\nProse.\r\n")
        with pytest.raises(ValueError, match="CRLF"):
            validate_encoding(Path(FILENAME))


class TestTask3Structure:
    """Task 3: Validate markdown structure and prose quality."""

    def test_first_line_starts_with_h1(self, temp_dir):
        """Verify first line is H1 heading."""
        create_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        lines = content.split("\n")
        assert lines[0].startswith("# "), "First line should start with '# '"

    def test_second_line_is_blank(self, temp_dir):
        """Verify second line is blank."""
        create_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        lines = content.split("\n")
        assert lines[1] == "", "Second line should be blank"

    def test_prose_has_sentences(self, temp_dir):
        """Verify prose contains sentences."""
        create_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        lines = content.split("\n")
        prose = "\n".join(lines[2:]).strip()
        period_count = prose.count(".")
        assert period_count > 0, "Prose should contain at least one sentence (period)"

    def test_prose_has_2_to_3_sentences(self, temp_dir):
        """Verify prose contains exactly 2 or 3 sentences."""
        create_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        lines = content.split("\n")
        prose = "\n".join(lines[2:]).strip()
        sentence_count = prose.count(".")
        assert 2 <= sentence_count <= 3, (
            f"Prose should have 2-3 sentences, found {sentence_count}"
        )

    def test_file_ends_with_newline(self, temp_dir):
        """Verify file ends with newline."""
        create_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        assert content.endswith("\n"), "File should end with newline"

    def test_file_size_in_range(self, temp_dir):
        """Verify file size is in 300-600 byte range."""
        create_file()
        file_size = Path(FILENAME).stat().st_size
        assert 300 <= file_size <= 600, (
            f"File size {file_size} should be in 300-600 byte range"
        )

    def test_validate_structure_passes(self, temp_dir):
        """Verify validate_structure returns True for valid file."""
        create_file()
        result = validate_structure(Path(FILENAME))
        assert result is True, "validate_structure should return True"

    def test_validate_structure_fails_without_h1(self, temp_dir):
        """Verify validate_structure fails without H1 heading."""
        Path(FILENAME).write_text("No heading\n\nProse.\n", encoding="utf-8", newline="\n")
        with pytest.raises(ValueError, match="H1 heading"):
            validate_structure(Path(FILENAME))

    def test_validate_structure_fails_without_blank_line(self, temp_dir):
        """Verify validate_structure fails without blank line."""
        Path(FILENAME).write_text("# Heading\nNo blank line\n\nProse.\n", encoding="utf-8", newline="\n")
        with pytest.raises(ValueError, match="blank"):
            validate_structure(Path(FILENAME))

    def test_validate_structure_fails_with_wrong_sentence_count(self, temp_dir):
        """Verify validate_structure fails with wrong sentence count."""
        Path(FILENAME).write_text("# Heading\n\nJust one.\n", encoding="utf-8", newline="\n")
        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_structure(Path(FILENAME))

    def test_validate_structure_fails_without_trailing_newline(self, temp_dir):
        """Verify validate_structure fails without trailing newline."""
        # Write bytes directly to avoid automatic newline
        Path(FILENAME).write_bytes(b"# Heading\n\nSentence one. Sentence two.")
        with pytest.raises(ValueError, match="newline"):
            validate_structure(Path(FILENAME))

    def test_validate_structure_fails_with_file_too_small(self, temp_dir):
        """Verify validate_structure fails for files under 300 bytes."""
        Path(FILENAME).write_text("# H\n\nS.\n", encoding="utf-8", newline="\n")
        with pytest.raises(ValueError, match="300-600"):
            validate_structure(Path(FILENAME))


class TestIntegration:
    """Integration tests for complete workflow."""

    def test_complete_workflow(self, temp_dir):
        """Verify complete creation and validation workflow."""
        # Create file
        file_path = create_file()
        assert file_path is not None

        # Validate encoding
        validate_encoding(file_path)

        # Validate structure
        validate_structure(file_path)

        # Verify final file state
        assert file_path.exists()
        content = file_path.read_text(encoding="utf-8")
        assert content.startswith("# ")
        assert content.endswith("\n")
        assert 300 <= file_path.stat().st_size <= 600


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
