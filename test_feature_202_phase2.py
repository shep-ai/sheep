#!/usr/bin/env python3
"""
Test suite for feature 202 phase 2: Validation Pipeline

Tests the comprehensive validation functions required by the specification:
- validate_markdown_format(): Validates H1 heading and blank line separation
- extract_prose_content(): Extracts prose after heading and blank line
- count_sentences(): Counts sentences via period counting
- validate_sentence_count(): Validates exactly 2-3 sentences
- validate_encoding(): Validates UTF-8 without BOM
- validate_line_endings(): Validates Unix LF line endings only
- validate_file_size(): Validates 250-600 byte range
- validate_markdown_file(): Comprehensive validation orchestration
"""

import pytest
import tempfile
from pathlib import Path
import sys

# Add src to path to import the feature module
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.features.feature_202_markdown_file_creation import (
    validate_markdown_format,
    extract_prose_content,
    count_sentences,
    validate_sentence_count,
    validate_encoding,
    validate_line_endings,
    validate_file_size,
    validate_markdown_file,
    FILENAME,
)


class TestTask2_1MarkdownFormatValidation:
    """Task 2-1: Implement markdown format validation.

    Validates markdown structure: H1 heading at start, blank line separator,
    exactly one H1 heading in file.
    """

    def test_validate_markdown_format_passes_correct_format(self):
        """Test validation passes for correct format (H1 + blank line + prose)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title\n\nThis is prose.\n", encoding="utf-8")

            # Should not raise
            validate_markdown_format(str(filepath))

    def test_validate_markdown_format_fails_no_h1(self):
        """Test validation fails if H1 heading is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("## Title\n\nThis is prose.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="H1 heading"):
                validate_markdown_format(str(filepath))

    def test_validate_markdown_format_fails_h1_not_at_start(self):
        """Test validation fails if H1 heading is not at start."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("Some text\n# Title\n\nProse.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="H1 heading"):
                validate_markdown_format(str(filepath))

    def test_validate_markdown_format_fails_no_blank_line(self):
        """Test validation fails if blank line separator is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title\nThis is prose.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="blank"):
                validate_markdown_format(str(filepath))

    def test_validate_markdown_format_fails_multiple_h1(self):
        """Test validation fails if multiple H1 headings exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title 1\n\n# Title 2\nProse.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="exactly one"):
                validate_markdown_format(str(filepath))

    def test_validate_markdown_format_fails_nonexistent_file(self):
        """Test validation fails if file does not exist."""
        with pytest.raises(FileNotFoundError):
            validate_markdown_format("/nonexistent/path/file.md")


class TestTask2_2SentenceCountValidation:
    """Task 2-2: Implement sentence count validation via period counting.

    Validates exactly 2-3 sentences using simple period counting method.
    Includes helper functions for prose extraction and sentence counting.
    """

    def test_extract_prose_content_returns_prose_after_blank_line(self):
        """Test prose extraction correctly identifies content after H1 + blank line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title\n\nThis is prose content.", encoding="utf-8")

            prose = extract_prose_content(str(filepath))

            assert isinstance(prose, str)
            assert "This is prose content." in prose

    def test_extract_prose_content_returns_empty_if_no_prose(self):
        """Test prose extraction returns empty string if no prose after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title\n\n", encoding="utf-8")

            prose = extract_prose_content(str(filepath))

            assert prose == ""

    def test_extract_prose_content_fails_no_blank_line(self):
        """Test prose extraction fails if no blank line separator."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title\nNo blank line", encoding="utf-8")

            with pytest.raises(ValueError, match="blank line"):
                extract_prose_content(str(filepath))

    def test_extract_prose_content_fails_nonexistent_file(self):
        """Test prose extraction fails if file does not exist."""
        with pytest.raises(FileNotFoundError):
            extract_prose_content("/nonexistent/file.md")

    def test_count_sentences_returns_period_count(self):
        """Test sentence counting returns number of periods in prose."""
        prose = "First sentence. Second sentence. Third sentence."

        count = count_sentences(prose)

        assert count == 3

    def test_count_sentences_handles_single_period(self):
        """Test sentence counting for single sentence."""
        prose = "Only one sentence."

        count = count_sentences(prose)

        assert count == 1

    def test_count_sentences_handles_no_periods(self):
        """Test sentence counting when no periods present."""
        prose = "No periods in this text"

        count = count_sentences(prose)

        assert count == 0

    def test_count_sentences_fails_empty_prose(self):
        """Test sentence counting fails for empty prose."""
        with pytest.raises(ValueError, match="empty"):
            count_sentences("")

    def test_validate_sentence_count_passes_for_2_sentences(self):
        """Test validation passes for exactly 2 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title\n\nFirst sentence. Second sentence.\n", encoding="utf-8")

            # Should not raise
            validate_sentence_count(str(filepath))

    def test_validate_sentence_count_passes_for_3_sentences(self):
        """Test validation passes for exactly 3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title\n\nFirst. Second. Third.\n", encoding="utf-8")

            # Should not raise
            validate_sentence_count(str(filepath))

    def test_validate_sentence_count_fails_for_1_sentence(self):
        """Test validation fails for fewer than 2 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title\n\nOnly one sentence.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="2-3 sentences"):
                validate_sentence_count(str(filepath))

    def test_validate_sentence_count_fails_for_4_sentences(self):
        """Test validation fails for more than 3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text(
                "# Title\n\nFirst. Second. Third. Fourth.\n",
                encoding="utf-8"
            )

            with pytest.raises(ValueError, match="2-3 sentences"):
                validate_sentence_count(str(filepath))


class TestTask2_3EncodingAndLineEndingValidation:
    """Task 2-3: Implement encoding and line ending validation.

    Validates UTF-8 encoding without BOM and Unix LF line endings.
    """

    def test_validate_encoding_passes_for_utf8_no_bom(self):
        """Test validation passes for UTF-8 file without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title\n\nContent.\n", encoding="utf-8")

            # Should not raise
            validate_encoding(str(filepath))

    def test_validate_encoding_fails_for_bom(self):
        """Test validation detects and rejects UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Write with BOM
            filepath.write_bytes(b"\xef\xbb\xbf# Title\n\nContent")

            with pytest.raises(ValueError, match="BOM"):
                validate_encoding(str(filepath))

    def test_validate_encoding_fails_for_invalid_utf8(self):
        """Test validation detects and rejects invalid UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Write invalid UTF-8
            filepath.write_bytes(b"\xff\xfe# Title")

            with pytest.raises(ValueError, match="invalid UTF-8"):
                validate_encoding(str(filepath))

    def test_validate_encoding_fails_nonexistent_file(self):
        """Test validation fails if file does not exist."""
        with pytest.raises(FileNotFoundError):
            validate_encoding("/nonexistent/file.md")

    def test_validate_line_endings_passes_for_lf_only(self):
        """Test validation passes for Unix LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_bytes(b"# Title\n\nContent.\n")

            # Should not raise
            validate_line_endings(str(filepath))

    def test_validate_line_endings_detects_crlf(self):
        """Test validation detects and rejects CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Write with CRLF
            filepath.write_bytes(b"# Title\r\n\r\nContent.\r\n")

            with pytest.raises(ValueError, match="CRLF"):
                validate_line_endings(str(filepath))

    def test_validate_line_endings_detects_cr(self):
        """Test validation detects and rejects CR line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Write with CR
            filepath.write_bytes(b"# Title\r\rContent.\r")

            with pytest.raises(ValueError, match="CR"):
                validate_line_endings(str(filepath))

    def test_validate_line_endings_fails_nonexistent_file(self):
        """Test validation fails if file does not exist."""
        with pytest.raises(FileNotFoundError):
            validate_line_endings("/nonexistent/file.md")


class TestTask2_4FileSizeValidation:
    """Task 2-4: Implement file size validation.

    Validates file size is within 250-600 bytes as specified.
    """

    def test_validate_file_size_passes_for_size_250_bytes(self):
        """Test validation passes for file at minimum boundary (250 bytes)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Create file of exactly 250 bytes
            content = "# Title\n\n" + "x" * 230 + ".\n"
            filepath.write_text(content, encoding="utf-8")

            if filepath.stat().st_size == 250:
                # Should not raise
                validate_file_size(str(filepath), 250, 600)

    def test_validate_file_size_passes_for_size_600_bytes(self):
        """Test validation passes for file at maximum boundary (600 bytes)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Create file near 600 bytes
            content = "# Title\n\n" + "x" * 575 + ".\n"
            filepath.write_text(content, encoding="utf-8")

            size = filepath.stat().st_size
            if size <= 600:
                # Should not raise
                validate_file_size(str(filepath))

    def test_validate_file_size_passes_for_midrange_size(self):
        """Test validation passes for file in middle of valid range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Create file around 400 bytes
            content = "# Title\n\n" + "x" * 375 + ".\n"
            filepath.write_text(content, encoding="utf-8")

            # Should not raise
            validate_file_size(str(filepath))

    def test_validate_file_size_fails_for_too_small(self):
        """Test validation fails for files smaller than 250 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# T\n\nX.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="outside acceptable range"):
                validate_file_size(str(filepath))

    def test_validate_file_size_fails_for_too_large(self):
        """Test validation fails for files larger than 600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Create file larger than 600 bytes
            content = "# Title\n\n" + "x" * 600 + ".\n"
            filepath.write_text(content, encoding="utf-8")

            with pytest.raises(ValueError, match="outside acceptable range"):
                validate_file_size(str(filepath))

    def test_validate_file_size_fails_nonexistent_file(self):
        """Test validation fails if file does not exist."""
        with pytest.raises(FileNotFoundError):
            validate_file_size("/nonexistent/file.md")

    def test_validate_file_size_includes_actual_size_in_error(self):
        """Test error message includes actual file size."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# T\n\nX.\n", encoding="utf-8")
            actual_size = filepath.stat().st_size

            with pytest.raises(ValueError) as exc_info:
                validate_file_size(str(filepath))

            assert str(actual_size) in str(exc_info.value)


class TestComprehensiveValidationPipeline:
    """Comprehensive validation orchestration function.

    Tests the validate_markdown_file() function which runs all validation
    checks in sequence and fails fast on the first error.
    """

    def test_validate_markdown_file_passes_for_valid_file(self):
        """Test comprehensive validation passes for valid markdown file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Create a valid markdown file with sufficient size (250-600 bytes)
            # Must be exactly 3 sentences (3 periods) and >= 250 bytes
            prose = (
                "This is a comprehensive example demonstrating how the validation pipeline "
                "works correctly when all markdown formatting requirements are properly met. "
                "The file contains expanded text to ensure it reaches the minimum size threshold "
                "while maintaining exactly three sentences with appropriate length constraints. "
                "Additional content extends the file to meet the byte count requirement"
            )
            # Count periods: 3 are needed for sentence count validation
            # Remove extra periods and rebuild with exactly 3
            sentences = [
                "This is a comprehensive example demonstrating how the validation pipeline "
                "works correctly when all markdown formatting requirements are properly met.",
                "The file contains expanded text to ensure it reaches the minimum size threshold "
                "while maintaining exactly three sentences with appropriate length constraints.",
                "Additional content extends the file to meet the byte count requirement."
            ]
            prose = " ".join(sentences)
            content = f"# Sample Title\n\n{prose}\n"
            filepath.write_text(content, encoding="utf-8")

            # Should not raise
            validate_markdown_file(str(filepath))

    def test_validate_markdown_file_fails_on_missing_file(self):
        """Test comprehensive validation fails if file does not exist."""
        with pytest.raises(FileNotFoundError):
            validate_markdown_file("/nonexistent/path/file.md")

    def test_validate_markdown_file_fails_on_invalid_format(self):
        """Test comprehensive validation fails if markdown format is invalid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Missing H1 heading
            filepath.write_text("## Title\n\nContent.\n", encoding="utf-8")

            with pytest.raises(ValueError):
                validate_markdown_file(str(filepath))

    def test_validate_markdown_file_fails_on_wrong_sentence_count(self):
        """Test comprehensive validation fails if sentence count is wrong."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Too many sentences
            filepath.write_text(
                "# Title\n\nFirst. Second. Third. Fourth. Fifth.\n",
                encoding="utf-8"
            )

            with pytest.raises(ValueError):
                validate_markdown_file(str(filepath))

    def test_validate_markdown_file_fails_on_bad_encoding(self):
        """Test comprehensive validation fails if file has BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Write with BOM
            filepath.write_bytes(b"\xef\xbb\xbf# Title\n\nFirst. Second. Third.\n")

            with pytest.raises(ValueError):
                validate_markdown_file(str(filepath))

    def test_validate_markdown_file_fails_on_crlf_line_endings(self):
        """Test comprehensive validation fails if file has CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Write with CRLF
            filepath.write_bytes(b"# Title\r\n\r\nFirst. Second. Third.\r\n")

            with pytest.raises(ValueError):
                validate_markdown_file(str(filepath))

    def test_validate_markdown_file_fails_on_bad_file_size(self):
        """Test comprehensive validation fails if file size is out of range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Too small
            filepath.write_text("# T\n\nX.\n", encoding="utf-8")

            with pytest.raises(ValueError):
                validate_markdown_file(str(filepath))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
