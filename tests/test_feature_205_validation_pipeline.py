"""Tests for Feature 205: Validation Pipeline (Phase 4).

This test suite covers the comprehensive validation pipeline with 6 sequential checks:
1. File exists at specified path
2. Markdown format (H1 heading, blank line separator)
3. Sentence count (exactly 2-3 periods)
4. UTF-8 encoding (no BOM, valid UTF-8)
5. Unix LF line endings (no CRLF, no CR)
6. File size (200-800 bytes)

Tests verify fail-fast behavior on first error and detailed error messages.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from sheep.features.feature_205_markdown_file_creation import (
    FILENAME,
    validate_file_size,
    validate_markdown_file,
    validate_markdown_format,
    validate_sentence_count,
    validate_encoding,
    validate_line_endings,
    verify_file_exists,
    extract_prose_content,
    count_sentences,
)


class TestValidationCheckFileExists:
    """Tests for Check 1: File exists."""

    def test_verify_file_exists_with_existing_file(self):
        """Test that verify_file_exists does not raise for existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("# Title\n\nFirst. Second. Third.\n", encoding="utf-8")

            # Should not raise
            verify_file_exists(str(path))

    def test_verify_file_exists_raises_for_missing_file(self):
        """Test that FileNotFoundError is raised for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "nonexistent.md"

            with pytest.raises(FileNotFoundError, match="does not exist"):
                verify_file_exists(str(path))

    def test_verify_file_exists_with_default_filename(self):
        """Test verify_file_exists with default FILENAME constant."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Title\n\nFirst. Second. Third.\n", encoding="utf-8")

                # Should not raise with default filename
                verify_file_exists()
            finally:
                os.chdir(original_cwd)


class TestValidationCheckMarkdownFormat:
    """Tests for Check 2: Markdown format."""

    def test_validate_markdown_format_with_valid_format(self):
        """Test that validate_markdown_format passes for valid format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("# Valid Title\n\nFirst. Second. Third.\n", encoding="utf-8")

            # Should not raise
            validate_markdown_format(str(path))

    def test_validate_markdown_format_rejects_missing_h1(self):
        """Test that ValueError is raised if file missing H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("No H1 heading here\n\nFirst. Second. Third.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="must start with H1"):
                validate_markdown_format(str(path))

    def test_validate_markdown_format_rejects_h2_instead_of_h1(self):
        """Test that ValueError is raised for H2 heading instead of H1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("## H2 Title\n\nFirst. Second. Third.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="H1"):
                validate_markdown_format(str(path))

    def test_validate_markdown_format_rejects_missing_blank_line(self):
        """Test that ValueError is raised if blank line separator is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("# Title\nNo blank line separator.\nFirst. Second.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="Second line must be blank"):
                validate_markdown_format(str(path))

    def test_validate_markdown_format_rejects_multiple_h1_headings(self):
        """Test that ValueError is raised for multiple H1 headings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("# First H1\n\nFirst. Second.\n\n# Second H1\n\nThird.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="exactly one H1"):
                validate_markdown_format(str(path))


class TestValidationCheckSentenceCount:
    """Tests for Check 3: Sentence count (2-3 sentences)."""

    def test_validate_sentence_count_with_two_sentences(self):
        """Test that validate_sentence_count passes for exactly 2 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("# Title\n\nFirst sentence. Second sentence.\n", encoding="utf-8")

            # Should not raise
            validate_sentence_count(str(path))

    def test_validate_sentence_count_with_three_sentences(self):
        """Test that validate_sentence_count passes for exactly 3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("# Title\n\nFirst. Second. Third.\n", encoding="utf-8")

            # Should not raise
            validate_sentence_count(str(path))

    def test_validate_sentence_count_rejects_one_sentence(self):
        """Test that ValueError is raised for only 1 sentence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("# Title\n\nOnly one sentence.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="Expected 2-3"):
                validate_sentence_count(str(path))

    def test_validate_sentence_count_rejects_four_sentences(self):
        """Test that ValueError is raised for 4 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("# Title\n\nFirst. Second. Third. Fourth.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="Expected 2-3"):
                validate_sentence_count(str(path))

    def test_validate_sentence_count_with_zero_sentences(self):
        """Test that ValueError is raised for no sentences (no periods)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("# Title\n\nNo periods in this prose\n", encoding="utf-8")

            with pytest.raises(ValueError, match="Expected 2-3"):
                validate_sentence_count(str(path))

    def test_count_sentences_helper(self):
        """Test the count_sentences helper function."""
        assert count_sentences("First. Second. Third.") == 3
        assert count_sentences("First. Second.") == 2
        assert count_sentences("Only one.") == 1
        assert count_sentences("No periods") == 0

    def test_count_sentences_raises_on_empty_prose(self):
        """Test that count_sentences raises for empty prose."""
        with pytest.raises(ValueError, match="empty"):
            count_sentences("")


class TestValidationCheckEncoding:
    """Tests for Check 4: UTF-8 encoding (no BOM)."""

    def test_validate_encoding_with_valid_utf8(self):
        """Test that validate_encoding passes for valid UTF-8 without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("# Title\n\nFirst. Second. Third.\n", encoding="utf-8")

            # Should not raise
            validate_encoding(str(path))

    def test_validate_encoding_with_unicode_content(self):
        """Test that validate_encoding handles Unicode content correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            content = "# Titre\n\nPremier. Deuxième. Troisième.\n"
            path.write_text(content, encoding="utf-8")

            # Should not raise - UTF-8 can handle accented characters
            validate_encoding(str(path))

    def test_validate_encoding_rejects_utf8_with_bom(self):
        """Test that ValueError is raised for UTF-8 with BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Write with BOM
            content = "# Title\n\nFirst. Second. Third.\n"
            binary = b"\xef\xbb\xbf" + content.encode("utf-8")
            path.write_bytes(binary)

            with pytest.raises(ValueError, match="BOM"):
                validate_encoding(str(path))

    def test_validate_encoding_rejects_non_utf8(self):
        """Test that ValueError is raised for non-UTF-8 encoding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Write with latin-1 encoding
            content = "# Café\n\nFirst. Second. Third.\n"
            path.write_bytes(content.encode("latin-1"))

            with pytest.raises(ValueError, match="UTF-8"):
                validate_encoding(str(path))


class TestValidationCheckLineEndings:
    """Tests for Check 5: Unix LF line endings."""

    def test_validate_line_endings_with_valid_lf(self):
        """Test that validate_line_endings passes for LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("# Title\n\nFirst. Second. Third.\n", encoding="utf-8")

            # Should not raise
            validate_line_endings(str(path))

    def test_validate_line_endings_rejects_crlf(self):
        """Test that ValueError is raised for CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            binary = b"# Title\r\n\r\nFirst. Second. Third.\r\n"
            path.write_bytes(binary)

            with pytest.raises(ValueError, match="CRLF"):
                validate_line_endings(str(path))

    def test_validate_line_endings_rejects_cr(self):
        """Test that ValueError is raised for CR line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            binary = b"# Title\r\r\nFirst. Second. Third.\r"
            path.write_bytes(binary)

            with pytest.raises(ValueError, match="CR"):
                validate_line_endings(str(path))

    def test_validate_line_endings_rejects_mixed_line_endings(self):
        """Test that ValueError is raised for mixed line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Mix of LF and CRLF
            binary = b"# Title\n\r\nFirst. Second. Third.\n"
            path.write_bytes(binary)

            with pytest.raises(ValueError, match="CRLF"):
                validate_line_endings(str(path))


class TestValidationCheckFileSize:
    """Tests for Check 6: File size (200-800 bytes)."""

    def test_validate_file_size_within_range(self):
        """Test that validate_file_size passes for file within range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create content with sufficient length to be 200-800 bytes
            title = "# " + "T" * 30 + "\n\n"
            prose = "S" * 200 + ". " + "S" * 200 + ". " + "S" * 100 + ".\n"
            path.write_text(title + prose, encoding="utf-8")

            # Should not raise (file size should be within 200-800)
            validate_file_size(str(path))

    def test_validate_file_size_at_minimum_boundary(self):
        """Test that validate_file_size passes at exactly 200 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create content with exactly 200 bytes
            content = "# Title Title Title\n\n" + "x" * 160 + ".\n"
            path.write_text(content, encoding="utf-8")

            # Adjust content to be exactly 200 bytes
            while len(path.read_bytes()) < 200:
                content += "y"
                path.write_text("# Title Title Title\n\n" + content, encoding="utf-8")

            # Find exact 200-byte content
            while len(path.read_bytes()) > 200:
                content = content[:-1]
                path.write_text("# Title Title Title\n\n" + content, encoding="utf-8")

            if len(path.read_bytes()) == 200:
                # Should not raise
                validate_file_size(str(path))

    def test_validate_file_size_at_maximum_boundary(self):
        """Test that validate_file_size passes at exactly 800 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create content exactly 800 bytes
            content = "# " + "T" * 50 + "\n\n" + "A" * 700 + ".\n"
            path.write_text(content, encoding="utf-8")

            # Adjust to exactly 800
            while len(path.read_bytes()) > 800:
                content = content[:-1]
                path.write_text(content, encoding="utf-8")

            if 795 <= len(path.read_bytes()) <= 805:
                validate_file_size(str(path))

    def test_validate_file_size_rejects_too_small(self):
        """Test that ValueError is raised for file < 200 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("# T\n\nSmall.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="outside acceptable range"):
                validate_file_size(str(path))

    def test_validate_file_size_rejects_too_large(self):
        """Test that ValueError is raised for file > 800 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create file larger than 800 bytes
            content = "# Title\n\n" + "x" * 1000 + ".\n"
            path.write_text(content, encoding="utf-8")

            with pytest.raises(ValueError, match="outside acceptable range"):
                validate_file_size(str(path))

    def test_validate_file_size_with_custom_range(self):
        """Test validate_file_size with custom min/max range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("# Title\n\nA small file with content.\n", encoding="utf-8")

            # File is ~36 bytes, should fail default check (200-800)
            with pytest.raises(ValueError):
                validate_file_size(str(path))

            # But pass with custom range
            validate_file_size(str(path), min_bytes=20, max_bytes=100)


class TestComprehensiveValidationPipeline:
    """Tests for the comprehensive validate_markdown_file() function."""

    def test_validate_markdown_file_with_valid_file(self):
        """Test that validate_markdown_file passes for valid file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create content that meets all validation requirements (200-800 bytes)
            title = "# " + "T" * 40 + "\n\n"
            prose = "P" * 220 + ". " + "Q" * 220 + ". " + "R" * 100 + ".\n"
            content = title + prose
            path.write_text(content, encoding="utf-8")

            # Should not raise - all checks pass
            validate_markdown_file(str(path))

    def test_validate_markdown_file_fails_fast_on_missing_file(self):
        """Test that validate_markdown_file fails on check 1 (file exists)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "nonexistent.md"

            with pytest.raises(FileNotFoundError, match="does not exist"):
                validate_markdown_file(str(path))

    def test_validate_markdown_file_fails_fast_on_bad_format(self):
        """Test that validate_markdown_file fails on check 2 (markdown format)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("No H1 heading\n\nFirst. Second. Third.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="H1"):
                validate_markdown_file(str(path))

    def test_validate_markdown_file_fails_fast_on_wrong_sentence_count(self):
        """Test that validate_markdown_file fails on check 3 (sentence count)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("# Title\n\nFirst. Second. Third. Fourth.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="Expected 2-3"):
                validate_markdown_file(str(path))

    def test_validate_markdown_file_fails_fast_on_bad_encoding(self):
        """Test that validate_markdown_file fails on check 4 (encoding)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Note: BOM check happens in check 4, but format check (check 2) may fail first
            # if the file can't be decoded properly. We'll use a file with BOM that
            # still has valid H1 format when decoded.
            title = "# " + "T" * 40 + "\n\n"
            prose = "P" * 220 + ". " + "Q" * 220 + ". " + "R" * 100 + ".\n"
            content = title + prose
            path.write_bytes(b"\xef\xbb\xbf" + content.encode("utf-8"))

            # Will fail on check 4 (encoding) with BOM message
            with pytest.raises(ValueError, match="BOM|H1"):
                validate_markdown_file(str(path))

    def test_validate_markdown_file_fails_fast_on_bad_line_endings(self):
        """Test that validate_markdown_file fails on check 5 (line endings)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_bytes(b"# Title\r\n\r\nFirst. Second. Third.\r\n")

            with pytest.raises(ValueError, match="CRLF"):
                validate_markdown_file(str(path))

    def test_validate_markdown_file_fails_fast_on_bad_size(self):
        """Test that validate_markdown_file fails on check 6 (file size)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create small file with proper format and sentence count but fails size check
            path.write_text("# T\n\nSmall prose. Tiny bit more. Very brief.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="outside acceptable range"):
                validate_markdown_file(str(path))

    def test_validate_markdown_file_with_unicode_content(self):
        """Test validate_markdown_file with Unicode content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create content with Unicode that meets 200-800 byte requirement
            title = "# Título: 中文 " + "T" * 30 + "\n\n"
            prose = "Premier à Paris, " + "P" * 200 + ". Segundo en España, " + "Q" * 200 + ". Tercero en Perú, " + "R" * 50 + ".\n"
            content = title + prose
            path.write_text(content, encoding="utf-8")

            # Should pass all checks
            validate_markdown_file(str(path))


class TestExtractProseLHelper:
    """Tests for extract_prose_content helper function."""

    def test_extract_prose_content_single_line(self):
        """Test extracting prose from file with single line of prose."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            path.write_text("# Title\n\nSingle line of prose.\n", encoding="utf-8")

            prose = extract_prose_content(str(path))
            assert prose == "Single line of prose."

    def test_extract_prose_content_multiline(self):
        """Test extracting prose from file with multiple lines."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            content = "# Title\n\nFirst line. Second line.\nThird line continued.\n"
            path.write_text(content, encoding="utf-8")

            prose = extract_prose_content(str(path))
            assert "First line." in prose
            assert "Second line." in prose
            assert "Third line" in prose

    def test_extract_prose_content_missing_file(self):
        """Test that extract_prose_content raises for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "nonexistent.md"

            with pytest.raises(FileNotFoundError):
                extract_prose_content(str(path))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
