"""Tests for the validate_feature_137 validation module.

Tests that the validation functions properly detect both valid and invalid files,
ensuring comprehensive coverage of all validation criteria.
"""

from pathlib import Path
import pytest
from validate_feature_137 import (
    ValidationError,
    validate_encoding,
    validate_line_endings,
    validate_structure,
    validate_prose_sentences,
    validate_file_size,
    validate_file,
)


class TestValidateEncoding:
    """Tests for validate_encoding function."""

    def test_valid_utf8_without_bom(self, tmp_path):
        """Test that valid UTF-8 file without BOM passes."""
        test_file = tmp_path / "test.md"
        content = "# Title\n\nSome content. More content. Even more content.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")
        # Should not raise
        validate_encoding(test_file)

    def test_rejects_utf8_with_bom(self, tmp_path):
        """Test that UTF-8 file with BOM is rejected."""
        test_file = tmp_path / "test.md"
        # Write file with BOM using utf-8-sig encoding
        content = "# Title\n\nSome content. More content. Even more content.\n"
        test_file.write_bytes(b"\xef\xbb\xbf" + content.encode("utf-8"))
        # Should raise
        with pytest.raises(ValidationError, match="UTF-8 BOM"):
            validate_encoding(test_file)


class TestValidateLineEndings:
    """Tests for validate_line_endings function."""

    def test_valid_lf_line_endings(self, tmp_path):
        """Test that file with LF line endings passes."""
        test_file = tmp_path / "test.md"
        content = "# Title\n\nContent. More. Even more.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")
        # Should not raise
        validate_line_endings(test_file)

    def test_rejects_crlf_line_endings(self, tmp_path):
        """Test that file with CRLF line endings is rejected."""
        test_file = tmp_path / "test.md"
        # Write file with CRLF manually
        content = "# Title\r\n\r\nContent. More. Even more.\r\n"
        test_file.write_bytes(content.encode("utf-8"))
        # Should raise
        with pytest.raises(ValidationError, match="CRLF"):
            validate_line_endings(test_file)


class TestValidateStructure:
    """Tests for validate_structure function."""

    def test_valid_structure(self, tmp_path):
        """Test that properly structured file passes."""
        test_file = tmp_path / "test.md"
        content = "# Title\n\nContent. More content. Even more.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")
        # Should not raise
        validate_structure(test_file)

    def test_rejects_missing_heading(self, tmp_path):
        """Test that file without H1 heading is rejected."""
        test_file = tmp_path / "test.md"
        content = "## Secondary Heading\n\nContent. More. Even more.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")
        # Should raise
        with pytest.raises(ValidationError, match="First line must start with"):
            validate_structure(test_file)

    def test_rejects_missing_blank_line(self, tmp_path):
        """Test that file without blank line after heading is rejected."""
        test_file = tmp_path / "test.md"
        content = "# Title\nContent. More. Even more.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")
        # Should raise
        with pytest.raises(ValidationError, match="blank"):
            validate_structure(test_file)

    def test_rejects_no_prose_content(self, tmp_path):
        """Test that file without prose content is rejected."""
        test_file = tmp_path / "test.md"
        content = "# Title\n\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")
        # Should raise
        with pytest.raises(ValidationError, match="[Pp]rose"):
            validate_structure(test_file)


class TestValidateProseSentences:
    """Tests for validate_prose_sentences function."""

    def test_valid_two_sentences(self, tmp_path):
        """Test that prose with exactly 2 sentences passes."""
        test_file = tmp_path / "test.md"
        content = "# Title\n\nFirst sentence. Second sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")
        # Should not raise
        validate_prose_sentences(test_file)

    def test_valid_three_sentences(self, tmp_path):
        """Test that prose with exactly 3 sentences passes."""
        test_file = tmp_path / "test.md"
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")
        # Should not raise
        validate_prose_sentences(test_file)

    def test_rejects_one_sentence(self, tmp_path):
        """Test that prose with only 1 sentence is rejected."""
        test_file = tmp_path / "test.md"
        content = "# Title\n\nOnly one sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")
        # Should raise
        with pytest.raises(ValidationError, match="2-3 sentences"):
            validate_prose_sentences(test_file)

    def test_rejects_four_sentences(self, tmp_path):
        """Test that prose with 4 sentences is rejected."""
        test_file = tmp_path / "test.md"
        content = "# Title\n\nFirst. Second. Third. Fourth.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")
        # Should raise
        with pytest.raises(ValidationError, match="2-3 sentences"):
            validate_prose_sentences(test_file)

    def test_handles_question_and_exclamation_marks(self, tmp_path):
        """Test that questions and exclamation marks are counted as sentences."""
        test_file = tmp_path / "test.md"
        content = "# Title\n\nIs this first? This is second!\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")
        # Should not raise - counts as 2 sentences
        validate_prose_sentences(test_file)


class TestValidateFileSize:
    """Tests for validate_file_size function."""

    def test_valid_file_size(self, tmp_path):
        """Test that file within size range passes."""
        test_file = tmp_path / "test.md"
        # Use longer content to ensure it's within the 320-600 byte range
        content = "# Title\n\nThis is a comprehensive first sentence about the topic at hand with substantial content about various aspects of the subject matter. This is the second sentence providing additional information and context about the subject matter being discussed in great detail. This is the third sentence concluding our thoughts on this important topic and summarizing key concepts.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")
        # Should not raise
        validate_file_size(test_file)

    def test_rejects_too_small(self, tmp_path):
        """Test that file too small is rejected."""
        test_file = tmp_path / "test.md"
        content = "# T\n\nA. B.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")
        # Should raise
        with pytest.raises(ValidationError, match="outside acceptable range"):
            validate_file_size(test_file)

    def test_rejects_too_large(self, tmp_path):
        """Test that file too large is rejected."""
        test_file = tmp_path / "test.md"
        # Create a file larger than 600 bytes
        long_content = "a" * 650
        content = f"# Title\n\n{long_content}. {long_content}. {long_content}.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")
        # Should raise
        with pytest.raises(ValidationError, match="outside acceptable range"):
            validate_file_size(test_file)


class TestValidateFile:
    """Tests for the main validate_file function."""

    def test_valid_file_passes_all_checks(self):
        """Test that actual test-narzc3.md file passes all validation."""
        test_file = Path("test-narzc3.md")
        if test_file.exists():
            # Should not raise
            validate_file(test_file)

    def test_file_not_found(self, tmp_path):
        """Test that missing file raises ValidationError."""
        test_file = tmp_path / "nonexistent.md"
        with pytest.raises(ValidationError, match="does not exist"):
            validate_file(test_file)

    def test_comprehensive_validation_fails_on_first_issue(self, tmp_path):
        """Test that validate_file stops on first validation failure."""
        test_file = tmp_path / "test.md"
        # File with BOM - should fail encoding check before other checks
        content = "# Title\n\nContent. More. Even more.\n"
        test_file.write_bytes(b"\xef\xbb\xbf" + content.encode("utf-8"))
        with pytest.raises(ValidationError, match="BOM"):
            validate_file(test_file)

    def test_comprehensive_validation_multiple_issues(self, tmp_path):
        """Test that validate_file can detect multiple types of issues."""
        test_file = tmp_path / "test.md"
        # File with CRLF line endings
        content = "# Title\r\n\r\nContent. More.\r\n"
        test_file.write_bytes(content.encode("utf-8"))
        with pytest.raises(ValidationError):
            validate_file(test_file)
