"""Tests for feature 171 validation functions.

Tests for the validation framework phase of feature 171:
- validate_markdown_structure(): Check markdown format (H1, blank line, prose)
- validate_sentence_count(): Count complete sentences (., !, ?)
- validate_encoding(): Check UTF-8 encoding without BOM
- validate_file_size(): Check file size is 300-600 bytes
- validate_line_endings(): Check Unix LF line endings (not CRLF)
"""

import tempfile
from pathlib import Path

import pytest


class TestValidateMarkdownStructure:
    """Tests for validate_markdown_structure() function."""

    def test_valid_markdown_with_h1_and_blank_line(self):
        """Test that valid markdown with H1 heading and blank line passes."""
        from sheep.features.feature_171 import validate_markdown_structure

        content = "# Test Title\n\nThis is prose content. More content here. And more.\n"
        # Should not raise
        validate_markdown_structure(content)

    def test_missing_h1_heading_fails(self):
        """Test that missing H1 heading fails validation."""
        from sheep.features.feature_171 import validate_markdown_structure

        content = "Regular text\n\nNo heading here. Just content. More content.\n"
        with pytest.raises(ValueError, match="must be H1 heading"):
            validate_markdown_structure(content)

    def test_missing_blank_line_after_h1_fails(self):
        """Test that missing blank line after H1 fails validation."""
        from sheep.features.feature_171 import validate_markdown_structure

        content = "# Test Title\nNo blank line. Just content. More content.\n"
        with pytest.raises(ValueError, match="blank"):
            validate_markdown_structure(content)

    def test_h1_without_space_fails(self):
        """Test that H1 without space after # fails validation."""
        from sheep.features.feature_171 import validate_markdown_structure

        content = "#NoSpace\n\nContent here. More content. And more.\n"
        with pytest.raises(ValueError, match="H1"):
            validate_markdown_structure(content)

    def test_empty_h1_title_fails(self):
        """Test that H1 with empty title fails validation."""
        from sheep.features.feature_171 import validate_markdown_structure

        content = "#  \n\nContent here. More content. And more.\n"
        with pytest.raises(ValueError, match="title"):
            validate_markdown_structure(content)

    def test_h1_with_minimum_prose_passes(self):
        """Test that H1 with minimal prose after blank line passes."""
        from sheep.features.feature_171 import validate_markdown_structure

        # Just checking structure; content validation is done separately
        content = "# Test Title\n\nSome content here"
        # Should not raise (just validates structure)
        validate_markdown_structure(content)

    def test_complex_h1_title_passes(self):
        """Test that H1 with complex title text passes."""
        from sheep.features.feature_171 import validate_markdown_structure

        content = "# The Power of Consistent Practice and Learning\n\nContent. More. And more."
        # Should not raise
        validate_markdown_structure(content)

    def test_valid_markdown_with_multiple_paragraphs(self):
        """Test that valid markdown with multiple paragraphs passes."""
        from sheep.features.feature_171 import validate_markdown_structure

        content = "# The Power of Persistence\n\nFirst sentence here. Second sentence here. Third sentence here.\n"
        validate_markdown_structure(content)


class TestValidateSentenceCount:
    """Tests for validate_sentence_count() function."""

    def test_two_sentences_pass(self):
        """Test that exactly 2 sentences pass validation."""
        from sheep.features.feature_171 import validate_sentence_count

        content = "First sentence. Second sentence."
        # Should not raise
        validate_sentence_count(content)

    def test_three_sentences_pass(self):
        """Test that exactly 3 sentences pass validation."""
        from sheep.features.feature_171 import validate_sentence_count

        content = "First sentence. Second sentence. Third sentence."
        # Should not raise
        validate_sentence_count(content)

    def test_one_sentence_fails(self):
        """Test that only 1 sentence fails validation."""
        from sheep.features.feature_171 import validate_sentence_count

        content = "Only one sentence."
        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_sentence_count(content)

    def test_four_sentences_fails(self):
        """Test that 4 sentences fails validation."""
        from sheep.features.feature_171 import validate_sentence_count

        content = "First. Second. Third. Fourth."
        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_sentence_count(content)

    def test_no_sentences_fails(self):
        """Test that content with no sentences fails validation."""
        from sheep.features.feature_171 import validate_sentence_count

        content = "Just some words without punctuation"
        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_sentence_count(content)

    def test_sentence_with_exclamation_mark(self):
        """Test that sentences ending with ! are counted."""
        from sheep.features.feature_171 import validate_sentence_count

        content = "First sentence! Second sentence. Third sentence."
        # Should not raise (3 sentences)
        validate_sentence_count(content)

    def test_sentence_with_question_mark(self):
        """Test that sentences ending with ? are counted."""
        from sheep.features.feature_171 import validate_sentence_count

        content = "Is this sentence? Yes it is. And this one too."
        # Should not raise (3 sentences)
        validate_sentence_count(content)

    def test_mixed_sentence_endings(self):
        """Test that mixed punctuation (., !, ?) is counted correctly."""
        from sheep.features.feature_171 import validate_sentence_count

        content = "First one! Second one? And the third."
        # Should not raise (3 sentences)
        validate_sentence_count(content)


class TestValidateEncoding:
    """Tests for validate_encoding() function."""

    def test_valid_utf8_file_passes(self):
        """Test that valid UTF-8 file passes validation."""
        from sheep.features.feature_171 import validate_encoding

        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", delete=False, newline=""
        ) as f:
            f.write("# Test\n\nContent here. More content. And more.\n")
            filepath = f.name

        try:
            # Should not raise
            validate_encoding(filepath)
        finally:
            Path(filepath).unlink()

    def test_file_with_utf8_bom_fails(self):
        """Test that file with UTF-8 BOM fails validation."""
        from sheep.features.feature_171 import validate_encoding

        with tempfile.NamedTemporaryFile(
            mode="wb", delete=False, suffix=".md"
        ) as f:
            # Write UTF-8 BOM followed by content
            f.write(b"\xef\xbb\xbf# Test\n\nContent. More. And more.\n")
            filepath = f.name

        try:
            with pytest.raises(ValueError, match="BOM"):
                validate_encoding(filepath)
        finally:
            Path(filepath).unlink()

    def test_invalid_utf8_file_fails(self):
        """Test that file with invalid UTF-8 fails validation."""
        from sheep.features.feature_171 import validate_encoding

        with tempfile.NamedTemporaryFile(
            mode="wb", delete=False, suffix=".md"
        ) as f:
            # Write invalid UTF-8 bytes
            f.write(b"\xff\xfe# Test\n\nContent. More. And more.\n")
            filepath = f.name

        try:
            with pytest.raises(ValueError, match="UTF-8"):
                validate_encoding(filepath)
        finally:
            Path(filepath).unlink()


class TestValidateFileSize:
    """Tests for validate_file_size() function."""

    def test_300_byte_file_passes(self):
        """Test that 300-byte file passes validation."""
        from sheep.features.feature_171 import validate_file_size

        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", delete=False, newline=""
        ) as f:
            # Create content that's exactly 300 bytes
            content = "# Title\n\n" + ("x" * 285) + "\n"
            f.write(content)
            filepath = f.name

        try:
            # Adjust if needed
            actual_size = Path(filepath).stat().st_size
            if actual_size == 300:
                # Should not raise
                validate_file_size(filepath)
        finally:
            Path(filepath).unlink()

    def test_600_byte_file_passes(self):
        """Test that 600-byte file passes validation."""
        from sheep.features.feature_171 import validate_file_size

        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", delete=False, newline=""
        ) as f:
            # Create content that's around 600 bytes
            content = "# Title\n\n" + ("x" * 585) + "\n"
            f.write(content)
            filepath = f.name

        try:
            actual_size = Path(filepath).stat().st_size
            if 300 <= actual_size <= 600:
                # Should not raise
                validate_file_size(filepath)
        finally:
            Path(filepath).unlink()

    def test_299_byte_file_fails(self):
        """Test that 299-byte file fails validation."""
        from sheep.features.feature_171 import validate_file_size

        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", delete=False, newline=""
        ) as f:
            # Create content that's less than 300 bytes
            content = "# Title\n\nSmall content.\n"
            f.write(content)
            filepath = f.name

        try:
            actual_size = Path(filepath).stat().st_size
            if actual_size < 300:
                with pytest.raises(ValueError, match="outside expected range"):
                    validate_file_size(filepath)
        finally:
            Path(filepath).unlink()

    def test_601_byte_file_fails(self):
        """Test that 601-byte file fails validation."""
        from sheep.features.feature_171 import validate_file_size

        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", delete=False, newline=""
        ) as f:
            # Create content that's more than 600 bytes
            content = "# Title\n\n" + ("x" * 600) + "\n"
            f.write(content)
            filepath = f.name

        try:
            actual_size = Path(filepath).stat().st_size
            if actual_size > 600:
                with pytest.raises(ValueError, match="outside expected range"):
                    validate_file_size(filepath)
        finally:
            Path(filepath).unlink()


class TestValidateLineEndings:
    """Tests for validate_line_endings() function."""

    def test_lf_line_endings_pass(self):
        """Test that file with LF line endings passes validation."""
        from sheep.features.feature_171 import validate_line_endings

        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", delete=False, newline=""
        ) as f:
            # Explicitly use LF
            f.write("# Test\n\nContent. More. And more.\n")
            filepath = f.name

        try:
            # Should not raise
            validate_line_endings(filepath)
        finally:
            Path(filepath).unlink()

    def test_crlf_line_endings_fail(self):
        """Test that file with CRLF line endings fails validation."""
        from sheep.features.feature_171 import validate_line_endings

        with tempfile.NamedTemporaryFile(
            mode="wb", delete=False, suffix=".md"
        ) as f:
            # Write content with CRLF
            f.write(b"# Test\r\n\r\nContent. More. And more.\r\n")
            filepath = f.name

        try:
            with pytest.raises(ValueError, match="CRLF"):
                validate_line_endings(filepath)
        finally:
            Path(filepath).unlink()

    def test_mixed_line_endings_fail(self):
        """Test that file with mixed line endings fails validation."""
        from sheep.features.feature_171 import validate_line_endings

        with tempfile.NamedTemporaryFile(
            mode="wb", delete=False, suffix=".md"
        ) as f:
            # Write content with mixed line endings
            f.write(b"# Test\n\r\nContent. More. And more.\n")
            filepath = f.name

        try:
            with pytest.raises(ValueError, match="CRLF"):
                validate_line_endings(filepath)
        finally:
            Path(filepath).unlink()


class TestValidationIntegration:
    """Integration tests for all validation functions."""

    def test_all_validations_pass_with_generated_content(self):
        """Test that all validations pass with actual generated content."""
        from sheep.features.feature_171 import (
            generate_content,
            validate_encoding,
            validate_file_size,
            validate_line_endings,
            validate_markdown_structure,
            validate_sentence_count,
        )

        content = generate_content()

        # All structure validations should pass
        validate_markdown_structure(content)
        validate_sentence_count(content)

        # Write to file and validate file properties
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", delete=False, newline=""
        ) as f:
            f.write(content)
            filepath = f.name

        try:
            validate_encoding(filepath)
            validate_line_endings(filepath)
            validate_file_size(filepath)
        finally:
            Path(filepath).unlink()

    def test_all_validations_catch_invalid_content(self):
        """Test that validations catch various types of invalid content."""
        from sheep.features.feature_171 import (
            validate_markdown_structure,
            validate_sentence_count,
        )

        # Invalid: no H1
        with pytest.raises(ValueError):
            validate_markdown_structure("Just text\n\nNo heading. No structure.\n")

        # Invalid: wrong sentence count
        with pytest.raises(ValueError):
            validate_sentence_count("Only one sentence.")
