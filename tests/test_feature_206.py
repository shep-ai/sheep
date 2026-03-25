"""Tests for feature 206: Markdown file creation with hard-coded content."""

from pathlib import Path

import pytest

from sheep.features.feature_206_markdown_file_creation import (
    FILENAME,
    PROSE_CONTENT,
    TITLE_TEXT,
    create_markdown_file,
    validate_blank_separator,
    validate_encoding,
    validate_file_size,
    validate_h1_format,
    validate_line_endings,
    validate_markdown_file,
    validate_sentence_count,
)


class TestCreateMarkdownFile:
    """Test suite for create_markdown_file() function."""

    def test_file_does_not_exist_initially(self):
        """Verify file does not exist before calling create_markdown_file()."""
        file_path = Path(FILENAME)
        # File should not exist from a clean state (or we clean it up first)
        if file_path.exists():
            file_path.unlink()
        assert not file_path.exists()

    def test_create_markdown_file_creates_file(self):
        """Test that create_markdown_file() creates the file."""
        file_path = Path(FILENAME)
        # Clean up first if it exists
        if file_path.exists():
            file_path.unlink()

        # Call function
        result = create_markdown_file()

        # Assert file now exists
        assert file_path.exists()
        assert result == file_path

    def test_create_markdown_file_correct_name(self):
        """Test that created file has the correct filename."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()

        assert file_path.exists()
        assert file_path.name == FILENAME

    def test_create_markdown_file_correct_content_format(self):
        """Test that file has correct content format: # Title\n\nProse\n"""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()

        content = file_path.read_text(encoding="utf-8")

        # Verify format: # Title, blank line, prose, trailing newline
        lines = content.split("\n")
        assert lines[0] == f"# {TITLE_TEXT}"
        assert lines[1] == ""
        assert PROSE_CONTENT in content
        assert content.endswith("\n")

    def test_create_markdown_file_utf8_encoding(self):
        """Test that file is created with UTF-8 encoding."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()

        # Verify can be read as UTF-8
        content = file_path.read_text(encoding="utf-8")
        assert content  # File has content
        assert isinstance(content, str)

    def test_create_markdown_file_no_bom(self):
        """Test that file does not start with UTF-8 BOM."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()

        binary_content = file_path.read_bytes()
        # UTF-8 BOM is 0xEF 0xBB 0xBF
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_create_markdown_file_returns_path(self):
        """Test that function returns a Path object."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        result = create_markdown_file()

        assert isinstance(result, Path)
        assert result.name == FILENAME

    def teardown_method(self):
        """Clean up test file after each test."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()


class TestValidateH1Format:
    """Test suite for validate_h1_format() function."""

    def test_valid_h1_format(self):
        """Test that valid H1 format passes validation."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()
        assert validate_h1_format(file_path) is True

    def test_invalid_h1_no_hash(self):
        """Test that H1 without # fails validation."""
        file_path = Path(FILENAME)
        file_path.write_text("The Art of Problem Solving Through Code\n\nProse.\n")

        with pytest.raises(ValueError) as exc_info:
            validate_h1_format(file_path)
        assert "H1 heading not found" in str(exc_info.value)

    def test_invalid_h1_no_space_after_hash(self):
        """Test that H1 without space after # fails validation."""
        file_path = Path(FILENAME)
        file_path.write_text("#Title\n\nProse.\n")

        with pytest.raises(ValueError) as exc_info:
            validate_h1_format(file_path)
        assert "H1 heading not found" in str(exc_info.value)

    def test_invalid_h1_empty_file(self):
        """Test that empty file fails H1 validation."""
        file_path = Path(FILENAME)
        file_path.write_text("")

        with pytest.raises(ValueError) as exc_info:
            validate_h1_format(file_path)
        assert "h1 heading" in str(exc_info.value).lower()

    def teardown_method(self):
        """Clean up test file after each test."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()


class TestValidateBlankSeparator:
    """Test suite for validate_blank_separator() function."""

    def test_valid_blank_separator(self):
        """Test that valid blank separator passes validation."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()
        assert validate_blank_separator(file_path) is True

    def test_invalid_text_on_second_line(self):
        """Test that text on second line fails validation."""
        file_path = Path(FILENAME)
        file_path.write_text("# Title\nSome text here\nProse.\n")

        with pytest.raises(ValueError) as exc_info:
            validate_blank_separator(file_path)
        assert "Expected blank line" in str(exc_info.value)

    def test_invalid_file_with_one_line(self):
        """Test that file with only one line fails validation."""
        file_path = Path(FILENAME)
        # Write a file with only one line (no trailing newline to ensure only 1 element when split)
        file_path.write_text("# Title")

        with pytest.raises(ValueError) as exc_info:
            validate_blank_separator(file_path)
        assert "fewer than 2 lines" in str(exc_info.value)

    def teardown_method(self):
        """Clean up test file after each test."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()


class TestValidateSentenceCount:
    """Test suite for validate_sentence_count() function."""

    def test_valid_two_sentences(self):
        """Test that prose with 2 sentences passes validation."""
        file_path = Path(FILENAME)
        file_path.write_text("# Title\n\nFirst sentence. Second sentence.\n")
        assert validate_sentence_count(file_path) is True

    def test_valid_three_sentences(self):
        """Test that prose with 3 sentences passes validation."""
        file_path = Path(FILENAME)
        file_path.write_text(
            "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        )
        assert validate_sentence_count(file_path) is True

    def test_invalid_one_sentence(self):
        """Test that prose with 1 sentence fails validation."""
        file_path = Path(FILENAME)
        file_path.write_text("# Title\n\nOnly one sentence.\n")

        with pytest.raises(ValueError) as exc_info:
            validate_sentence_count(file_path)
        assert "Expected 2-3 sentences" in str(exc_info.value)
        assert "found 1 periods" in str(exc_info.value)

    def test_invalid_four_sentences(self):
        """Test that prose with 4 sentences fails validation."""
        file_path = Path(FILENAME)
        file_path.write_text(
            "# Title\n\nFirst. Second. Third. Fourth.\n"
        )

        with pytest.raises(ValueError) as exc_info:
            validate_sentence_count(file_path)
        assert "Expected 2-3 sentences" in str(exc_info.value)
        assert "found 4 periods" in str(exc_info.value)

    def teardown_method(self):
        """Clean up test file after each test."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()


class TestValidateEncoding:
    """Test suite for validate_encoding() function."""

    def test_valid_utf8_encoding(self):
        """Test that valid UTF-8 encoding passes validation."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()
        assert validate_encoding(file_path) is True

    def test_invalid_utf8_bom(self):
        """Test that UTF-8 BOM is detected and fails validation."""
        file_path = Path(FILENAME)
        # Write file with UTF-8 BOM
        content = "# Title\n\nProse.\n"
        bom = b"\xef\xbb\xbf"
        file_path.write_bytes(bom + content.encode("utf-8"))

        with pytest.raises(ValueError) as exc_info:
            validate_encoding(file_path)
        assert "BOM" in str(exc_info.value)

    def test_invalid_non_utf8_encoding(self):
        """Test that non-UTF-8 encoding fails validation."""
        file_path = Path(FILENAME)
        # Write file with latin-1 encoding of a non-ASCII character
        content = "# Tîtle\n\nProse.\n"
        file_path.write_bytes(content.encode("latin-1"))

        with pytest.raises(ValueError):
            validate_encoding(file_path)
        # Either "not valid UTF-8" or similar error message

    def teardown_method(self):
        """Clean up test file after each test."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()


class TestValidateLineEndings:
    """Test suite for validate_line_endings() function."""

    def test_valid_lf_line_endings(self):
        """Test that Unix LF line endings pass validation."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()
        assert validate_line_endings(file_path) is True

    def test_invalid_crlf_line_endings(self):
        """Test that CRLF line endings fail validation."""
        file_path = Path(FILENAME)
        content = "# Title\r\n\r\nProse.\r\n"
        file_path.write_bytes(content.encode("utf-8"))

        with pytest.raises(ValueError) as exc_info:
            validate_line_endings(file_path)
        assert "CRLF" in str(exc_info.value)

    def test_invalid_cr_line_endings(self):
        """Test that CR-only line endings fail validation."""
        file_path = Path(FILENAME)
        content = "# Title\r\rProse.\r"
        file_path.write_bytes(content.encode("utf-8"))

        with pytest.raises(ValueError) as exc_info:
            validate_line_endings(file_path)
        assert "CR" in str(exc_info.value)

    def teardown_method(self):
        """Clean up test file after each test."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()


class TestValidateFileSize:
    """Test suite for validate_file_size() function."""

    def test_valid_file_size_within_bounds(self):
        """Test that file size within 100-600 bytes passes validation."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()
        assert validate_file_size(file_path) is True

    def test_invalid_file_size_too_small(self):
        """Test that file size under 100 bytes fails validation."""
        file_path = Path(FILENAME)
        file_path.write_text("# T\n\nSmall.\n")  # Very small file

        with pytest.raises(ValueError) as exc_info:
            validate_file_size(file_path)
        assert "outside bounds" in str(exc_info.value)
        assert "100-600" in str(exc_info.value)

    def test_invalid_file_size_too_large(self):
        """Test that file size over 600 bytes fails validation."""
        file_path = Path(FILENAME)
        # Create file larger than 600 bytes
        large_content = "# Title\n\n" + "a" * 700 + "\n"
        file_path.write_text(large_content)

        with pytest.raises(ValueError) as exc_info:
            validate_file_size(file_path)
        assert "outside bounds" in str(exc_info.value)

    def teardown_method(self):
        """Clean up test file after each test."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()


class TestValidateMarkdownFile:
    """Test suite for validate_markdown_file() orchestration function."""

    def test_valid_markdown_file_passes_all_validations(self):
        """Test that properly created file passes comprehensive validation."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()
        assert validate_markdown_file(file_path) is True

    def test_fails_on_missing_h1(self):
        """Test that validation fails when H1 is missing."""
        file_path = Path(FILENAME)
        file_path.write_text("No heading here.\n\nProse. Another.\n")

        with pytest.raises(ValueError) as exc_info:
            validate_markdown_file(file_path)
        assert "h1 heading" in str(exc_info.value).lower()

    def test_fails_on_missing_blank_separator(self):
        """Test that validation fails when blank separator is missing."""
        file_path = Path(FILENAME)
        file_path.write_text("# Title\nText on second line\nProse. Another.\n")

        with pytest.raises(ValueError):
            validate_markdown_file(file_path)
        # Should fail on blank separator, before checking sentences

    def test_fails_on_invalid_sentence_count(self):
        """Test that validation fails when sentence count is wrong."""
        file_path = Path(FILENAME)
        file_path.write_text("# Title\n\nOnly one sentence.\n")

        with pytest.raises(ValueError) as exc_info:
            validate_markdown_file(file_path)
        assert "sentence" in str(exc_info.value).lower()

    def test_fails_on_file_not_existing(self):
        """Test that validation fails when file does not exist."""
        file_path = Path("nonexistent_file.md")

        with pytest.raises(ValueError) as exc_info:
            validate_markdown_file(file_path)
        assert "does not exist" in str(exc_info.value)

    def teardown_method(self):
        """Clean up test file after each test."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()
