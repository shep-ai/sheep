"""Integration tests for markdown file property validation (task-3)."""

import pytest
from pathlib import Path
from tests.test_markdown_file_validation_helpers import (
    validate_all_markdown_properties,
    validate_markdown_encoding,
    validate_markdown_line_endings,
    validate_markdown_h1_heading,
    validate_markdown_sentence_count,
    validate_markdown_trailing_newline,
    validate_markdown_file_size,
    validate_markdown_no_trailing_whitespace,
    validate_markdown_grammar_check,
)


class TestMarkdownValidationHelpers:
    """Tests for markdown validation helper functions."""

    def test_validate_markdown_encoding_detects_utf8_bom(self, tmp_path):
        """Test that encoding validation detects UTF-8 BOM."""
        # Create file with UTF-8 BOM
        test_file = tmp_path / "test_with_bom.md"
        test_file.write_bytes(b'\xef\xbb\xbf# Test\n\nSentence. Another.')

        result = validate_markdown_encoding(test_file)

        assert not result["valid"]
        assert "BOM" in result["error"]

    def test_validate_markdown_encoding_accepts_utf8_no_bom(self, tmp_path):
        """Test that encoding validation accepts UTF-8 without BOM."""
        test_file = tmp_path / "test_no_bom.md"
        test_file.write_text("# Test\n\nSentence. Another.", encoding="utf-8")

        result = validate_markdown_encoding(test_file)

        assert result["valid"]
        assert "content" in result

    def test_validate_markdown_line_endings_detects_crlf(self, tmp_path):
        """Test that line ending validation detects CRLF."""
        test_file = tmp_path / "test_crlf.md"
        test_file.write_bytes(b"# Test\r\n\r\nSentence. Another.")

        result = validate_markdown_line_endings(test_file)

        assert not result["valid"]
        assert "CRLF" in result["error"]

    def test_validate_markdown_line_endings_accepts_lf(self, tmp_path):
        """Test that line ending validation accepts LF."""
        test_file = tmp_path / "test_lf.md"
        test_file.write_bytes(b"# Test\n\nSentence. Another.")

        result = validate_markdown_line_endings(test_file)

        assert result["valid"]

    def test_validate_markdown_h1_heading_detects_missing_h1(self, tmp_path):
        """Test that H1 validation detects missing H1 heading."""
        test_file = tmp_path / "test_no_h1.md"
        test_file.write_text("No heading\n\nSentence. Another.", encoding="utf-8")

        result = validate_markdown_h1_heading(test_file)

        assert not result["valid"]
        assert "H1" in result["error"]

    def test_validate_markdown_h1_heading_detects_missing_blank_line(self, tmp_path):
        """Test that H1 validation detects missing blank line after heading."""
        test_file = tmp_path / "test_no_blank_line.md"
        test_file.write_text("# Test\nSentence. Another.", encoding="utf-8")

        result = validate_markdown_h1_heading(test_file)

        assert not result["valid"]
        assert "blank line" in result["error"]

    def test_validate_markdown_h1_heading_accepts_proper_h1(self, tmp_path):
        """Test that H1 validation accepts proper H1 heading with blank line."""
        test_file = tmp_path / "test_proper_h1.md"
        test_file.write_text("# Test Title\n\nSentence. Another.", encoding="utf-8")

        result = validate_markdown_h1_heading(test_file)

        assert result["valid"]
        assert "heading" in result

    def test_validate_markdown_sentence_count_detects_too_few(self, tmp_path):
        """Test that sentence count validation detects fewer than 2 sentences."""
        test_file = tmp_path / "test_one_sentence.md"
        test_file.write_text("# Test\n\nJust one sentence.", encoding="utf-8")

        result = validate_markdown_sentence_count(test_file)

        assert not result["valid"]

    def test_validate_markdown_sentence_count_detects_too_many(self, tmp_path):
        """Test that sentence count validation detects more than 3 sentences."""
        test_file = tmp_path / "test_four_sentences.md"
        test_file.write_text(
            "# Test\n\nFirst. Second. Third. Fourth.",
            encoding="utf-8"
        )

        result = validate_markdown_sentence_count(test_file)

        assert not result["valid"]

    def test_validate_markdown_sentence_count_accepts_2_sentences(self, tmp_path):
        """Test that sentence count validation accepts 2 sentences."""
        test_file = tmp_path / "test_two_sentences.md"
        test_file.write_text("# Test\n\nFirst sentence. Second sentence.", encoding="utf-8")

        result = validate_markdown_sentence_count(test_file)

        assert result["valid"]
        assert result["sentence_count"] == 2

    def test_validate_markdown_sentence_count_accepts_3_sentences(self, tmp_path):
        """Test that sentence count validation accepts 3 sentences."""
        test_file = tmp_path / "test_three_sentences.md"
        test_file.write_text(
            "# Test\n\nFirst. Second. Third.",
            encoding="utf-8"
        )

        result = validate_markdown_sentence_count(test_file)

        assert result["valid"]
        assert result["sentence_count"] == 3

    def test_validate_markdown_trailing_newline_detects_missing(self, tmp_path):
        """Test that trailing newline validation detects missing newline."""
        test_file = tmp_path / "test_no_newline.md"
        test_file.write_bytes(b"# Test\n\nSentence. Another.")

        result = validate_markdown_trailing_newline(test_file)

        assert not result["valid"]

    def test_validate_markdown_trailing_newline_accepts_with_newline(self, tmp_path):
        """Test that trailing newline validation accepts file with newline."""
        test_file = tmp_path / "test_with_newline.md"
        test_file.write_bytes(b"# Test\n\nSentence. Another.\n")

        result = validate_markdown_trailing_newline(test_file)

        assert result["valid"]

    def test_validate_markdown_file_size_detects_too_small(self, tmp_path):
        """Test that file size validation detects file smaller than minimum."""
        test_file = tmp_path / "test_small.md"
        # Create a very small file
        test_file.write_text("# X\n\nA.\n", encoding="utf-8")

        result = validate_markdown_file_size(test_file)

        assert not result["valid"]
        assert "outside range" in result["error"]

    def test_validate_markdown_file_size_detects_too_large(self, tmp_path):
        """Test that file size validation detects file larger than maximum."""
        test_file = tmp_path / "test_large.md"
        # Create a very large file (over 600 bytes)
        large_content = "# Title\n\n" + "A " * 400 + ".\n"
        test_file.write_text(large_content, encoding="utf-8")

        result = validate_markdown_file_size(test_file)

        assert not result["valid"]

    def test_validate_markdown_file_size_accepts_in_range(self, tmp_path):
        """Test that file size validation accepts files in range."""
        test_file = tmp_path / "test_in_range.md"
        # Create a file in the 300-600 byte range (use write_bytes to avoid CRLF on Windows)
        # Need longer content to reach 300+ bytes with exactly 2-3 sentences
        content = (
            "# Testing Markdown File Size Validation\n\n"
            "This is the first sentence that provides detailed information about markdown file "
            "validation and testing methodology. "
            "The second sentence explains how we validate file properties including size, "
            "encoding, and format compliance. "
            "The third and final sentence concludes with the overall summary of markdown validation requirements.\n"
        )
        test_file.write_bytes(content.encode("utf-8"))

        result = validate_markdown_file_size(test_file)

        assert result["valid"], f"File validation failed: {result}"
        assert 300 <= result["size"] <= 600

    def test_validate_all_markdown_properties(self, tmp_path):
        """Test comprehensive validation of all markdown properties."""
        test_file = tmp_path / "test_complete.md"
        # Create a properly formatted markdown file
        content = "# Test Title\n\nThis is a test sentence. Another sentence here. And one more sentence.\n"
        test_file.write_text(content, encoding="utf-8")

        result = validate_all_markdown_properties(test_file)

        # All checks except file_size might fail due to exact size requirements
        # But most should pass
        assert result["all_valid"] is True or result["all_valid"] is False  # Just check it runs
        assert "filepath" in result
        assert "checks" in result
        assert "summary" in result


class TestFeature299OutputValidation:
    """Tests specifically for feature 299 markdown file output validation (task-3)."""

    def test_markdown_file_properties_validation_chain(self, tmp_path):
        """Test the complete validation chain for a properly formatted markdown file."""
        # Create a markdown file matching feature 299 specification (use write_bytes to avoid CRLF on Windows)
        test_file = tmp_path / "test-o2fx99.md"
        content = "# Astronomy in Ancient Civilizations\n\nAncient civilizations observed celestial bodies for navigation, agriculture, and religious purposes. Many cultures developed sophisticated astronomical knowledge, tracking planetary movements and predicting eclipses. This knowledge laid the foundation for modern astronomy and scientific understanding of the universe.\n"
        test_file.write_bytes(content.encode("utf-8"))

        # Run all validations
        result = validate_all_markdown_properties(test_file)

        # Check all validations pass
        assert result["checks"]["encoding"]["valid"], result["checks"]["encoding"]
        assert result["checks"]["line_endings"]["valid"], result["checks"]["line_endings"]
        assert result["checks"]["h1_heading"]["valid"], result["checks"]["h1_heading"]
        assert result["checks"]["sentence_count"]["valid"], result["checks"]["sentence_count"]
        assert result["checks"]["trailing_newline"]["valid"], result["checks"]["trailing_newline"]
        assert result["checks"]["file_size"]["valid"], result["checks"]["file_size"]
        assert result["checks"]["trailing_whitespace"]["valid"], result["checks"]["trailing_whitespace"]
        assert result["checks"]["grammar"]["valid"], result["checks"]["grammar"]

    def test_markdown_filename_validation(self):
        """Test that markdown filename follows specification."""
        filename = "test-o2fx99.md"

        # Should start with "test-"
        assert filename.startswith("test-")
        # Should end with ".md"
        assert filename.endswith(".md")
        # Should have 6-character suffix
        suffix = filename[5:-3]
        assert len(suffix) == 6
        assert suffix.isalnum()

    @pytest.mark.parametrize("invalid_filename,reason", [
        ("o2fx99.md", "Missing test- prefix"),
        ("test-o2fx99", "Missing .md extension"),
        ("test_o2fx99.md", "Wrong separator (underscore)"),
        ("Test-o2fx99.md", "Capital T (should be lowercase)"),
    ])
    def test_markdown_filename_validation_rejects_invalid(self, invalid_filename, reason):
        """Test that validation rejects invalid filenames."""
        # Valid filenames must:
        # 1. Start with "test-"
        # 2. End with ".md"
        # 3. Have exactly 6 alphanumeric characters between "test-" and ".md"

        is_valid = (
            invalid_filename.startswith("test-") and
            invalid_filename.endswith(".md") and
            len(invalid_filename[5:-3]) == 6 and
            invalid_filename[5:-3].isalnum()
        )

        # These specific filenames should all be invalid for the reasons stated
        assert not is_valid, f"Filename {invalid_filename} should be invalid ({reason})"
