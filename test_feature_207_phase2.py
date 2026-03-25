#!/usr/bin/env python3
"""
Test suite for feature 207 phase 2: Comprehensive Validation

Tests the following validation functions:
- verify_file_exists(): Check file exists
- validate_markdown_format(): Check H1 heading, blank line separator
- validate_encoding(): Check UTF-8 without BOM
- validate_line_endings(): Check Unix LF only
- validate_sentence_count(): Check 2-3 sentences
- validate_file_size(): Soft validation with warnings
- validate_markdown_file(): Orchestration function calling all validators
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch
import sys

# Add src to path to import the feature module
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.features.feature_207_markdown_file_creation import (
    verify_file_exists,
    validate_markdown_format,
    validate_encoding,
    validate_line_endings,
    extract_prose_content,
    count_sentences,
    validate_sentence_count,
    validate_file_size,
    validate_markdown_file,
    FILENAME,
)


class TestVerifyFileExists:
    """Test suite for verify_file_exists function."""

    def test_verify_file_exists_returns_true(self):
        """Test that verify_file_exists returns True for existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create a test file
                Path("test.md").write_text("# Test\n\nContent.")
                result = verify_file_exists("test.md")
                assert result is True
            finally:
                os.chdir(original_dir)

    def test_verify_file_exists_raises_on_missing_file(self):
        """Test that verify_file_exists raises FileNotFoundError for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                with pytest.raises(FileNotFoundError, match="does not exist"):
                    verify_file_exists("missing.md")
            finally:
                os.chdir(original_dir)


class TestValidateMarkdownFormat:
    """Test suite for validate_markdown_format function."""

    def test_validate_markdown_format_valid_format(self):
        """Test that validate_markdown_format returns True for correct format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                content = "# My Title\n\nThis is prose content. Second sentence. Third."
                Path("test.md").write_text(content)
                result = validate_markdown_format("test.md")
                assert result is True
            finally:
                os.chdir(original_dir)

    def test_validate_markdown_format_rejects_no_h1(self):
        """Test that validate_markdown_format rejects file without H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                content = "No heading here\n\nContent. More content. Even more."
                Path("test.md").write_text(content)
                with pytest.raises(ValueError, match="H1 heading"):
                    validate_markdown_format("test.md")
            finally:
                os.chdir(original_dir)

    def test_validate_markdown_format_rejects_h2(self):
        """Test that validate_markdown_format rejects H2 heading instead of H1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                content = "## H2 Title\n\nContent. More. More."
                Path("test.md").write_text(content)
                with pytest.raises(ValueError, match="H1 heading"):
                    validate_markdown_format("test.md")
            finally:
                os.chdir(original_dir)

    def test_validate_markdown_format_rejects_missing_blank_line(self):
        """Test that validate_markdown_format rejects missing blank line separator."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                content = "# Title\nContent. More. More."
                Path("test.md").write_text(content)
                with pytest.raises(ValueError, match="blank"):
                    validate_markdown_format("test.md")
            finally:
                os.chdir(original_dir)

    def test_validate_markdown_format_rejects_multiple_h1(self):
        """Test that validate_markdown_format rejects multiple H1 headings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                content = "# First Title\n\nContent. More. More.\n\n# Second Title\n\nMore content."
                Path("test.md").write_text(content)
                with pytest.raises(ValueError, match="exactly one H1"):
                    validate_markdown_format("test.md")
            finally:
                os.chdir(original_dir)

    def test_validate_markdown_format_raises_on_missing_file(self):
        """Test that validate_markdown_format raises FileNotFoundError for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                with pytest.raises(FileNotFoundError):
                    validate_markdown_format("missing.md")
            finally:
                os.chdir(original_dir)


class TestValidateEncoding:
    """Test suite for validate_encoding function."""

    def test_validate_encoding_utf8_without_bom(self):
        """Test that validate_encoding passes for UTF-8 without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                Path("test.md").write_text("# Test\n\nContent.", encoding="utf-8")
                result = validate_encoding("test.md")
                assert result is True
            finally:
                os.chdir(original_dir)

    def test_validate_encoding_rejects_utf8_bom(self):
        """Test that validate_encoding rejects UTF-8 with BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Write file with UTF-8 BOM
                Path("test.md").write_bytes(b"\xef\xbb\xbf# Test\n\nContent.")
                with pytest.raises(ValueError, match="BOM"):
                    validate_encoding("test.md")
            finally:
                os.chdir(original_dir)

    def test_validate_encoding_raises_on_missing_file(self):
        """Test that validate_encoding raises FileNotFoundError for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                with pytest.raises(FileNotFoundError):
                    validate_encoding("missing.md")
            finally:
                os.chdir(original_dir)


class TestValidateLineEndings:
    """Test suite for validate_line_endings function."""

    def test_validate_line_endings_lf_only(self):
        """Test that validate_line_endings passes for LF-only line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                Path("test.md").write_text("# Test\n\nContent.\n", encoding="utf-8")
                result = validate_line_endings("test.md")
                assert result is True
            finally:
                os.chdir(original_dir)

    def test_validate_line_endings_rejects_crlf(self):
        """Test that validate_line_endings rejects CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Write file with CRLF
                Path("test.md").write_bytes(b"# Test\r\n\r\nContent.\r\n")
                with pytest.raises(ValueError, match="CRLF"):
                    validate_line_endings("test.md")
            finally:
                os.chdir(original_dir)

    def test_validate_line_endings_rejects_cr(self):
        """Test that validate_line_endings rejects CR line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Write file with CR only
                Path("test.md").write_bytes(b"# Test\r\rContent.\r")
                with pytest.raises(ValueError, match="CR"):
                    validate_line_endings("test.md")
            finally:
                os.chdir(original_dir)

    def test_validate_line_endings_raises_on_missing_file(self):
        """Test that validate_line_endings raises FileNotFoundError for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                with pytest.raises(FileNotFoundError):
                    validate_line_endings("missing.md")
            finally:
                os.chdir(original_dir)


class TestExtractProseContent:
    """Test suite for extract_prose_content helper function."""

    def test_extract_prose_content_valid_file(self):
        """Test that extract_prose_content extracts prose correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                content = "# My Title\n\nThis is prose. With sentences. And content."
                Path("test.md").write_text(content)
                prose = extract_prose_content("test.md")
                assert "This is prose." in prose
                assert "With sentences." in prose
            finally:
                os.chdir(original_dir)

    def test_extract_prose_content_raises_on_missing_file(self):
        """Test that extract_prose_content raises FileNotFoundError for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                with pytest.raises(FileNotFoundError):
                    extract_prose_content("missing.md")
            finally:
                os.chdir(original_dir)

    def test_extract_prose_content_raises_on_missing_blank_line(self):
        """Test that extract_prose_content raises ValueError if blank line is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                content = "# Title\nNo blank line."
                Path("test.md").write_text(content)
                with pytest.raises(ValueError, match="blank line"):
                    extract_prose_content("test.md")
            finally:
                os.chdir(original_dir)


class TestCountSentences:
    """Test suite for count_sentences helper function."""

    def test_count_sentences_two_sentences(self):
        """Test that count_sentences correctly counts 2 sentences."""
        prose = "This is the first sentence. This is the second sentence."
        assert count_sentences(prose) == 2

    def test_count_sentences_three_sentences(self):
        """Test that count_sentences correctly counts 3 sentences."""
        prose = "First. Second. Third."
        assert count_sentences(prose) == 3

    def test_count_sentences_raises_on_empty_prose(self):
        """Test that count_sentences raises ValueError for empty prose."""
        with pytest.raises(ValueError, match="empty"):
            count_sentences("")


class TestValidateSentenceCount:
    """Test suite for validate_sentence_count function."""

    def test_validate_sentence_count_two_sentences(self):
        """Test that validate_sentence_count passes with 2 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                content = "# Title\n\nFirst sentence. Second sentence."
                Path("test.md").write_text(content)
                result = validate_sentence_count("test.md")
                assert result is True
            finally:
                os.chdir(original_dir)

    def test_validate_sentence_count_three_sentences(self):
        """Test that validate_sentence_count passes with 3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                content = "# Title\n\nFirst. Second. Third."
                Path("test.md").write_text(content)
                result = validate_sentence_count("test.md")
                assert result is True
            finally:
                os.chdir(original_dir)

    def test_validate_sentence_count_rejects_one_sentence(self):
        """Test that validate_sentence_count rejects 1 sentence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                content = "# Title\n\nOnly one sentence."
                Path("test.md").write_text(content)
                with pytest.raises(ValueError, match="Expected 2-3 sentences, found 1"):
                    validate_sentence_count("test.md")
            finally:
                os.chdir(original_dir)

    def test_validate_sentence_count_rejects_four_sentences(self):
        """Test that validate_sentence_count rejects 4 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                content = "# Title\n\nFirst. Second. Third. Fourth."
                Path("test.md").write_text(content)
                with pytest.raises(ValueError, match="Expected 2-3 sentences, found 4"):
                    validate_sentence_count("test.md")
            finally:
                os.chdir(original_dir)

    def test_validate_sentence_count_raises_on_missing_file(self):
        """Test that validate_sentence_count raises FileNotFoundError for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                with pytest.raises(FileNotFoundError):
                    validate_sentence_count("missing.md")
            finally:
                os.chdir(original_dir)


class TestValidateFileSize:
    """Test suite for validate_file_size function."""

    def test_validate_file_size_within_range(self):
        """Test that validate_file_size returns True for file within range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file with content between 200-700 bytes
                content = "# Title\n\nThis is a reasonably sized sentence. This is another sentence. And one more."
                Path("test.md").write_text(content)
                result = validate_file_size("test.md", min_bytes=200, max_bytes=700)
                assert result is True
            finally:
                os.chdir(original_dir)

    def test_validate_file_size_below_minimum(self):
        """Test that validate_file_size returns True but logs warning for small file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create very small file
                content = "# T\n\nA."
                Path("test.md").write_text(content)
                result = validate_file_size("test.md", min_bytes=200, max_bytes=700)
                assert result is True  # Soft validation always returns True
            finally:
                os.chdir(original_dir)

    def test_validate_file_size_above_maximum(self):
        """Test that validate_file_size returns True but logs warning for large file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create very large file (over 700 bytes)
                content = "# Title\n\n" + ("A " * 400) + "."
                Path("test.md").write_text(content)
                result = validate_file_size("test.md", min_bytes=200, max_bytes=700)
                assert result is True  # Soft validation always returns True
            finally:
                os.chdir(original_dir)

    def test_validate_file_size_raises_on_missing_file(self):
        """Test that validate_file_size raises FileNotFoundError for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                with pytest.raises(FileNotFoundError):
                    validate_file_size("missing.md")
            finally:
                os.chdir(original_dir)


class TestValidateMarkdownFileOrchestration:
    """Test suite for validate_markdown_file orchestration function."""

    def test_validate_markdown_file_all_checks_pass(self):
        """Test that validate_markdown_file returns True when all checks pass."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create a valid markdown file
                content = "# My Title\n\nFirst sentence here. Second sentence here. Third sentence here."
                Path("test.md").write_text(content, encoding="utf-8")
                result = validate_markdown_file("test.md")
                assert result is True
            finally:
                os.chdir(original_dir)

    def test_validate_markdown_file_fails_on_missing_file(self):
        """Test that validate_markdown_file fails if file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                with pytest.raises(FileNotFoundError):
                    validate_markdown_file("missing.md")
            finally:
                os.chdir(original_dir)

    def test_validate_markdown_file_fails_on_invalid_format(self):
        """Test that validate_markdown_file fails fast on format error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file with invalid markdown (no H1)
                content = "No heading\n\nContent. More. More."
                Path("test.md").write_text(content)
                with pytest.raises(ValueError, match="H1 heading"):
                    validate_markdown_file("test.md")
            finally:
                os.chdir(original_dir)

    def test_validate_markdown_file_fails_on_invalid_sentence_count(self):
        """Test that validate_markdown_file fails fast on sentence count error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file with too many sentences
                content = "# Title\n\nFirst. Second. Third. Fourth."
                Path("test.md").write_text(content)
                with pytest.raises(ValueError, match="Expected 2-3 sentences"):
                    validate_markdown_file("test.md")
            finally:
                os.chdir(original_dir)

    def test_validate_markdown_file_fails_on_invalid_encoding(self):
        """Test that validate_markdown_file fails fast on encoding error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file with BOM
                Path("test.md").write_bytes(b"\xef\xbb\xbf# Title\n\nFirst. Second. Third.")
                with pytest.raises(ValueError, match="BOM"):
                    validate_markdown_file("test.md")
            finally:
                os.chdir(original_dir)

    def test_validate_markdown_file_fails_on_invalid_line_endings(self):
        """Test that validate_markdown_file fails fast on line ending error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file with CRLF
                Path("test.md").write_bytes(b"# Title\r\n\r\nFirst. Second. Third.")
                with pytest.raises(ValueError, match="CRLF"):
                    validate_markdown_file("test.md")
            finally:
                os.chdir(original_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
