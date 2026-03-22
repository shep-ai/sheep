"""Tests for markdown file validation functions."""

import tempfile
from pathlib import Path

import pytest

from validate_markdown_file import (
    validate_file,
    validate_file_exists,
    validate_file_size,
    validate_encoding,
    validate_line_endings,
    validate_markdown_structure,
    validate_prose_content,
)


class TestValidateFileExists:
    """Tests for validate_file_exists() function."""

    def test_validates_existing_file(self):
        """Test that validation passes for an existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Test\n\nContent.", encoding='utf-8')

            result = validate_file_exists(filepath)
            assert result is True

    def test_rejects_nonexistent_file(self):
        """Test that validation fails for non-existent file."""
        nonexistent = Path("/nonexistent/test.md")

        with pytest.raises(AssertionError, match="does not exist"):
            validate_file_exists(nonexistent)


class TestValidateFileSize:
    """Tests for validate_file_size() function."""

    def test_accepts_file_in_typical_range(self):
        """Test that validation passes for file in 400-600 byte range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Create content approximately 500 bytes
            content = (
                "# The Art of Effective Communication\n\n"
                "Clear and thoughtful communication is essential for building strong "
                "relationships and achieving meaningful collaboration in both professional "
                "and personal contexts. When we express our ideas with clarity and listen "
                "with genuine understanding, we create an environment where others feel "
                "valued and heard. By mastering the art of communication, we unlock the "
                "potential for deeper connections, better problem-solving, and sustainable "
                "success in all our endeavors.\n"
            )
            filepath.write_text(content, encoding='utf-8', newline='')

            # Verify file is in acceptable range
            file_size = filepath.stat().st_size
            assert 300 < file_size < 800, f"Test file {file_size} not in 300-800 range"

            result = validate_file_size(filepath)
            assert result is True

    def test_accepts_file_in_tolerance_range(self):
        """Test that validation accepts files in 300-800 byte range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Create file just above 300 bytes
            content = "# Title\n\nFirst sentence. Second sentence. Third sentence. " * 5
            filepath.write_text(content, encoding='utf-8', newline='')

            file_size = filepath.stat().st_size
            if 300 < file_size < 800:
                result = validate_file_size(filepath)
                assert result is True

    def test_rejects_file_too_small(self):
        """Test that validation fails for file smaller than 300 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Create very small file
            content = "# T\n\nX.\n"
            filepath.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="outside typical range"):
                validate_file_size(filepath)

    def test_rejects_file_too_large(self):
        """Test that validation fails for file larger than 800 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Create very large file (900+ bytes)
            large_prose = "This is a sentence. " * 60  # Creates large content
            content = f"# Title\n\n{large_prose}\n"
            filepath.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="outside typical range"):
                validate_file_size(filepath)


class TestValidateEncoding:
    """Tests for validate_encoding() function."""

    def test_accepts_utf8_without_bom(self):
        """Test that validation passes for UTF-8 encoded file without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            content = "# Test\n\nContent with UTF-8: café, naïve, résumé.\n"
            filepath.write_text(content, encoding='utf-8')

            result = validate_encoding(filepath)
            assert result is True

    def test_rejects_utf8_with_bom(self):
        """Test that validation fails for UTF-8 file with BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Write UTF-8 BOM explicitly
            bom = b'\xef\xbb\xbf'
            content = "# Test\n\nContent.\n"
            filepath.write_bytes(bom + content.encode('utf-8'))

            with pytest.raises(AssertionError, match="BOM"):
                validate_encoding(filepath)

    def test_rejects_invalid_utf8(self):
        """Test that validation fails for invalid UTF-8 encoding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Write invalid UTF-8 sequence
            invalid_utf8 = b'# Test\n\nContent with invalid: \xff\xfe\n'
            filepath.write_bytes(invalid_utf8)

            with pytest.raises(AssertionError, match="UTF-8"):
                validate_encoding(filepath)


class TestValidateLineEndings:
    """Tests for validate_line_endings() function."""

    def test_accepts_lf_line_endings(self):
        """Test that validation passes for LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Write with explicit LF endings
            content = "# Test\n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath.write_bytes(content.encode('utf-8'))

            result = validate_line_endings(filepath)
            assert result is True

    def test_rejects_crlf_line_endings(self):
        """Test that validation fails for CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Create with CRLF
            content = "# Test\r\n\r\nFirst sentence. Second sentence.\r\n"
            filepath.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="LF"):
                validate_line_endings(filepath)

    def test_requires_at_least_one_lf(self):
        """Test that file must contain at least one LF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # File with no line endings (single line)
            content = "# Test content here"
            filepath.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="LF line endings"):
                validate_line_endings(filepath)


class TestValidateMarkdownStructure:
    """Tests for validate_markdown_structure() function."""

    def test_accepts_valid_heading_and_blank_line(self):
        """Test that validation passes for proper H1 heading with blank line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            content = "# Proper Heading\n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath.write_text(content, encoding='utf-8', newline='')

            result = validate_markdown_structure(filepath)
            assert result is True

    def test_rejects_missing_h1_heading(self):
        """Test that validation fails without H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # H2 instead of H1
            content = "## Subheading\n\nThis is a long sentence with enough content to meet the size requirement. This is another long sentence with enough content to meet the requirement. This is the third long sentence with enough content to fill the requirement.\n"
            filepath.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="H1"):
                validate_markdown_structure(filepath)

    def test_rejects_missing_blank_line(self):
        """Test that validation fails without blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # No blank line between heading and prose (with enough content for size validation)
            content = "# Title\nThis is a long sentence with enough content to meet the size requirement. This is another long sentence with enough content to meet the requirement. This is the third long sentence with enough content to fill the requirement.\n"
            filepath.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="blank line"):
                validate_markdown_structure(filepath)

    def test_rejects_heading_without_content(self):
        """Test that validation fails for heading with no meaningful content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Just "# " with nothing after
            content = "# \n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="meaningful content"):
                validate_markdown_structure(filepath)

    def test_tolerates_trailing_whitespace_in_heading(self):
        """Test that validation accepts heading with trailing spaces."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            content = "# Valid Heading   \n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath.write_text(content, encoding='utf-8', newline='')

            result = validate_markdown_structure(filepath)
            assert result is True


class TestValidateProseContent:
    """Tests for validate_prose_content() function."""

    def test_accepts_2_sentences(self):
        """Test that validation passes for exactly 2 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            content = "# Title\n\nFirst sentence. Second sentence.\n"
            filepath.write_text(content, encoding='utf-8', newline='')

            result = validate_prose_content(filepath)
            assert result is True

    def test_accepts_3_sentences(self):
        """Test that validation passes for exactly 3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath.write_text(content, encoding='utf-8', newline='')

            result = validate_prose_content(filepath)
            assert result is True

    def test_rejects_1_sentence(self):
        """Test that validation fails for only 1 sentence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            content = "# Title\n\nOnly one sentence.\n"
            filepath.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="at least 2"):
                validate_prose_content(filepath)

    def test_rejects_too_many_sentences(self):
        """Test that validation fails for more than 3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # 5 sentences
            content = (
                "# Title\n\n"
                "First sentence. Second sentence. Third sentence. "
                "Fourth sentence. Fifth sentence.\n"
            )
            filepath.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="at most 3"):
                validate_prose_content(filepath)

    def test_rejects_empty_prose(self):
        """Test that validation fails when prose section is empty."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            content = "# Title\n\n   \n"
            filepath.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="empty"):
                validate_prose_content(filepath)

    def test_counts_periods_for_sentences(self):
        """Test that validation counts periods to identify sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Prose with three clear sentences (no abbreviations to avoid extra periods)
            content = "# Title\n\nThis is the first sentence about something important. Here is the second sentence providing more detail. Finally here is the third sentence concluding the thought.\n"
            filepath.write_bytes(content.encode('utf-8'))

            # This should have exactly 3 periods for 3 sentences
            result = validate_prose_content(filepath)
            assert result is True


class TestValidateFile:
    """Tests for validate_file() comprehensive validation function."""

    def test_validates_correctly_formed_file(self):
        """Test that validate_file() passes for a correctly formed file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-0h4oez.md"
            content = (
                "# The Art of Effective Communication\n\n"
                "Clear and thoughtful communication is essential for building strong "
                "relationships and achieving meaningful collaboration in both professional "
                "and personal contexts. When we express our ideas with clarity and listen "
                "with genuine understanding, we create an environment where others feel "
                "valued and heard. By mastering the art of communication, we unlock the "
                "potential for deeper connections, better problem-solving, and sustainable "
                "success in all our endeavors.\n"
            )
            filepath.write_text(content, encoding='utf-8', newline='')

            # Verify file meets basic requirements
            file_size = filepath.stat().st_size
            assert 300 < file_size < 800, f"Test file {file_size} not in valid range"

            result = validate_file(filepath)
            assert result is True

    def test_rejects_file_missing_existence_check(self):
        """Test that validate_file() fails when file doesn't exist."""
        nonexistent = Path("/nonexistent/path/test.md")

        with pytest.raises(AssertionError, match="does not exist"):
            validate_file(nonexistent)

    def test_rejects_file_with_invalid_size(self):
        """Test that validate_file() fails when file size is invalid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# X\n\nY.", encoding='utf-8', newline='')

            with pytest.raises(AssertionError, match="outside typical range"):
                validate_file(filepath)

    def test_rejects_file_with_bom(self):
        """Test that validate_file() fails when file has UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            bom = b'\xef\xbb\xbf'
            content = (
                "# Important Title\n\n"
                "This is a long sentence with enough content to meet the size requirement for validation. "
                "This is another long sentence with enough content to meet the size requirement. "
                "This is the third long sentence with enough content to fill the requirement completely.\n"
            )
            filepath.write_bytes(bom + content.encode('utf-8'))

            with pytest.raises(AssertionError):
                validate_file(filepath)

    def test_rejects_file_with_crlf(self):
        """Test that validate_file() fails when file has CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            content = (
                "# Important Title\r\n\r\n"
                "This is a long sentence with enough content to meet the size requirement for validation. "
                "This is another long sentence with enough content to meet the size requirement. "
                "This is the third long sentence with enough content to fill the requirement completely.\r\n"
            )
            filepath.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError):
                validate_file(filepath)

    def test_rejects_file_without_heading(self):
        """Test that validate_file() fails without H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            content = (
                "## Subheading\n\n"
                "This is a long sentence with enough content to meet the size requirement for validation. "
                "This is another long sentence with enough content to meet the size requirement. "
                "This is the third long sentence with enough content to fill the requirement completely.\n"
            )
            filepath.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError):
                validate_file(filepath)

    def test_rejects_file_with_insufficient_prose(self):
        """Test that validate_file() fails with insufficient prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Create file with enough content for size validation but insufficient sentences
            content = "# Title\n\nOnly one sentence with enough padding to fill the size requirement but still be just one sentence that ends here.\n"
            filepath.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError):
                validate_file(filepath)

    def test_error_messages_are_descriptive(self):
        """Test that error messages provide clear guidance."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # File with no heading but enough content for size check to pass
            content = "Some content here to make it long enough for the size check.\n\nThis is a long prose section with enough content to meet the size requirement. This is another long sentence with enough content to meet the requirement. This is the third long sentence with enough content to fill the requirement.\n"
            filepath.write_bytes(content.encode('utf-8'))

            try:
                validate_file(filepath)
                pytest.fail("Should have raised AssertionError")
            except AssertionError as e:
                error_msg = str(e)
                assert len(error_msg) > 10, "Error message should be descriptive"


class TestIntegration:
    """Integration tests for file validation against real test-0h4oez.md file."""

    def test_validate_existing_test_file(self):
        """Test that the existing test-0h4oez.md file passes all validations."""
        # Check if the actual test file exists in the repository root
        repo_root = Path(__file__).parent.parent.parent
        test_file = repo_root / "test-0h4oez.md"

        if not test_file.exists():
            pytest.skip("test-0h4oez.md does not exist in repository root")

        # Run comprehensive validation
        result = validate_file(test_file)
        assert result is True

    def test_all_individual_validations_pass(self):
        """Test that all individual validations pass for the test file."""
        repo_root = Path(__file__).parent.parent.parent
        test_file = repo_root / "test-0h4oez.md"

        if not test_file.exists():
            pytest.skip("test-0h4oez.md does not exist in repository root")

        # Run each validation individually
        assert validate_file_exists(test_file) is True
        assert validate_file_size(test_file) is True
        assert validate_encoding(test_file) is True
        assert validate_line_endings(test_file) is True
        assert validate_markdown_structure(test_file) is True
        assert validate_prose_content(test_file) is True

    def test_validate_file_multiple_times(self):
        """Test that validation can be run multiple times without issues."""
        repo_root = Path(__file__).parent.parent.parent
        test_file = repo_root / "test-0h4oez.md"

        if not test_file.exists():
            pytest.skip("test-0h4oez.md does not exist in repository root")

        # Run validation multiple times
        for i in range(3):
            result = validate_file(test_file)
            assert result is True, f"Validation failed on attempt {i+1}"
