"""Tests for feature 191: Creating markdown file test-u1rtbw.md with title and prose content."""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest


class TestFeature191Constants:
    """Tests for task 1: Define file content constants."""

    def test_filename_constant(self):
        """Test that FILENAME constant is correct."""
        from sheep.features.feature_191_markdown_file_creation import FILENAME

        assert FILENAME == "test-u1rtbw.md"

    def test_title_constant_is_non_empty_string(self):
        """Test that TITLE is a non-empty string."""
        from sheep.features.feature_191_markdown_file_creation import TITLE

        assert isinstance(TITLE, str)
        assert len(TITLE) > 0

    def test_prose_constant_contains_2_to_3_sentences(self):
        """Test that PROSE contains exactly 2-3 sentences."""
        from sheep.features.feature_191_markdown_file_creation import PROSE

        # Count sentences by periods
        sentence_count = PROSE.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    def test_prose_is_substantive_not_placeholder(self):
        """Test that PROSE is meaningful content, not placeholder."""
        from sheep.features.feature_191_markdown_file_creation import PROSE

        # Check that content is substantive (contains real words, not lorem ipsum)
        assert len(PROSE) > 100, "Prose should be substantive (>100 chars)"
        assert "lorem" not in PROSE.lower(), "Should not contain lorem ipsum"

    def test_constants_exist_and_are_importable(self):
        """Test that all required constants can be imported."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            PROSE,
            TITLE,
        )

        assert FILENAME is not None
        assert TITLE is not None
        assert PROSE is not None

    def test_file_content_structure_size(self):
        """Test that constants produce content in expected size range."""
        from sheep.features.feature_191_markdown_file_creation import PROSE, TITLE

        # Simulate the content that will be written to file
        content = f"# {TITLE}\n\n{PROSE}\n"
        content_size = len(content.encode("utf-8"))

        # Feature 191 spec requires 450-550 bytes
        assert 450 <= content_size <= 550, f"Content should be 450-550 bytes, got {content_size}"


class TestFeature191FileCreation:
    """Tests for task 2: Implement markdown file creation with UTF-8 and Unix LF."""

    def setup_method(self):
        """Clean up any existing test file before each test."""
        from sheep.features.feature_191_markdown_file_creation import FILENAME

        test_file = Path(FILENAME)
        if test_file.exists():
            test_file.unlink()

    def teardown_method(self):
        """Clean up test file after each test."""
        from sheep.features.feature_191_markdown_file_creation import FILENAME

        test_file = Path(FILENAME)
        if test_file.exists():
            test_file.unlink()

    def test_create_markdown_file_creates_file(self):
        """Test that create_markdown_file() creates the file at correct path."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            create_markdown_file,
        )

        result = create_markdown_file()

        assert Path(FILENAME).exists(), f"File {FILENAME} should exist after creation"
        assert result == str(Path(FILENAME).absolute())

    def test_create_markdown_file_content_structure(self):
        """Test that file contains H1 heading, blank line, and prose."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            TITLE,
            PROSE,
            create_markdown_file,
        )

        create_markdown_file()
        content = Path(FILENAME).read_text(encoding="utf-8")

        expected_content = f"# {TITLE}\n\n{PROSE}\n"
        assert content == expected_content

    def test_create_markdown_file_utf8_encoding(self):
        """Test that file is encoded as UTF-8 without BOM."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            create_markdown_file,
        )

        create_markdown_file()
        binary_content = Path(FILENAME).read_bytes()

        # Check for UTF-8 BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

        # Verify UTF-8 decoding works
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("File must be valid UTF-8")

    def test_create_markdown_file_unix_lf_line_endings(self):
        """Test that file uses Unix LF line endings, not CRLF."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            create_markdown_file,
        )

        create_markdown_file()
        binary_content = Path(FILENAME).read_bytes()

        # Check that there are no CRLF sequences
        assert b"\r\n" not in binary_content, "File must use Unix LF line endings (no CRLF)"

        # Verify file ends with LF, not CR
        assert binary_content.endswith(b"\n"), "File must end with LF"
        assert not binary_content.endswith(b"\r\n"), "File must not end with CRLF"

    def test_create_markdown_file_raises_if_exists(self):
        """Test that create_markdown_file() raises error if file already exists."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            create_markdown_file,
        )

        # Create file once
        create_markdown_file()

        # Attempting to create again should raise error
        with pytest.raises(FileExistsError):
            create_markdown_file()

    def test_create_markdown_file_file_size_in_range(self):
        """Test that created file is in the expected size range (450-550 bytes)."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            create_markdown_file,
        )

        create_markdown_file()
        file_size = Path(FILENAME).stat().st_size

        assert 450 <= file_size <= 550, f"File size should be 450-550 bytes, got {file_size}"


class TestFeature191EncodingValidation:
    """Tests for task 3: Implement UTF-8 encoding validation (no BOM)."""

    def setup_method(self):
        """Clean up any existing test file before each test."""
        from sheep.features.feature_191_markdown_file_creation import FILENAME

        test_file = Path(FILENAME)
        if test_file.exists():
            test_file.unlink()

    def teardown_method(self):
        """Clean up test file after each test."""
        from sheep.features.feature_191_markdown_file_creation import FILENAME

        test_file = Path(FILENAME)
        if test_file.exists():
            test_file.unlink()

    def test_validate_encoding_accepts_valid_utf8(self):
        """Test that validate_encoding() accepts valid UTF-8 file without BOM."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_encoding,
        )

        # Create a simple valid UTF-8 file
        Path(FILENAME).write_text("# Test\n\nContent here.\n", encoding="utf-8", newline="\n")

        # Should not raise an exception
        validate_encoding()

    def test_validate_encoding_rejects_utf8_bom(self):
        """Test that validate_encoding() rejects files with UTF-8 BOM."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_encoding,
        )

        # Create file with UTF-8 BOM
        with open(FILENAME, "wb") as f:
            f.write(b"\xef\xbb\xbf# Test\n\nContent here.\n")

        # Should raise ValueError
        with pytest.raises(ValueError) as exc_info:
            validate_encoding()
        assert "BOM" in str(exc_info.value).upper() or "byte order mark" in str(exc_info.value).lower()

    def test_validate_encoding_rejects_invalid_utf8(self):
        """Test that validate_encoding() rejects files with invalid UTF-8 bytes."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_encoding,
        )

        # Create file with invalid UTF-8 bytes
        with open(FILENAME, "wb") as f:
            f.write(b"# Test\n\nInvalid: \xff\xfe content.\n")

        # Should raise ValueError
        with pytest.raises(ValueError) as exc_info:
            validate_encoding()
        assert "UTF-8" in str(exc_info.value) or "encoding" in str(exc_info.value).lower()


class TestFeature191StructureValidation:
    """Tests for task 5: Implement markdown structure validation."""

    def setup_method(self):
        """Clean up any existing test file before each test."""
        from sheep.features.feature_191_markdown_file_creation import FILENAME

        test_file = Path(FILENAME)
        if test_file.exists():
            test_file.unlink()

    def teardown_method(self):
        """Clean up test file after each test."""
        from sheep.features.feature_191_markdown_file_creation import FILENAME

        test_file = Path(FILENAME)
        if test_file.exists():
            test_file.unlink()

    def test_validate_structure_accepts_valid_h1_and_3_sentences(self):
        """Test that validate_structure() passes for file with H1 heading and 3 sentences."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_structure,
        )

        # Create a valid file with H1 and 3 sentences
        content = "# Test Title\n\nThis is sentence one. This is sentence two. This is sentence three.\n"
        Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")

        # Should not raise any exception
        validate_structure(FILENAME)

    def test_validate_structure_rejects_missing_h1_heading(self):
        """Test that validate_structure() fails for file without H1 heading."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_structure,
        )

        # Create a file without H1 heading
        content = "Regular text without heading.\n"
        Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")

        # Should raise ValueError
        with pytest.raises(ValueError, match="H1 heading"):
            validate_structure(FILENAME)

    def test_validate_structure_rejects_only_1_sentence(self):
        """Test that validate_structure() fails for file with only 1 sentence."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_structure,
        )

        # Create a file with H1 but only 1 sentence
        content = "# Test Title\n\nThis is only one sentence.\n"
        Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")

        # Should raise ValueError
        with pytest.raises(ValueError, match="sentences"):
            validate_structure(FILENAME)

    def test_validate_structure_rejects_4_or_more_sentences(self):
        """Test that validate_structure() fails for file with 4+ sentences."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_structure,
        )

        # Create a file with H1 but too many sentences
        content = "# Test Title\n\nThis is sentence one. This is sentence two. This is sentence three. This is sentence four.\n"
        Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")

        # Should raise ValueError
        with pytest.raises(ValueError, match="sentences"):
            validate_structure(FILENAME)

    def test_validate_structure_accepts_2_sentences(self):
        """Test that validate_structure() passes for file with H1 heading and 2 sentences."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_structure,
        )

        # Create a valid file with H1 and 2 sentences
        content = "# Test Title\n\nThis is sentence one. This is sentence two.\n"
        Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")

        # Should not raise any exception
        validate_structure(FILENAME)


class TestFeature191LineEndingValidation:
    """Tests for task 4: Implement Unix LF line ending validation."""

    def setup_method(self):
        """Clean up any existing test file before each test."""
        from sheep.features.feature_191_markdown_file_creation import FILENAME

        test_file = Path(FILENAME)
        if test_file.exists():
            test_file.unlink()

    def teardown_method(self):
        """Clean up test file after each test."""
        from sheep.features.feature_191_markdown_file_creation import FILENAME

        test_file = Path(FILENAME)
        if test_file.exists():
            test_file.unlink()

    def test_validate_line_endings_passes_for_unix_lf(self):
        """Test that validation passes for file with only Unix LF line endings."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_line_endings,
        )

        # Create file with Unix LF line endings
        Path(FILENAME).write_text("Line 1\nLine 2\nLine 3\n", encoding="utf-8", newline="\n")

        # Should not raise any exception
        validate_line_endings(FILENAME)

    def test_validate_line_endings_rejects_crlf(self):
        """Test that validation rejects file with Windows CRLF line endings."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_line_endings,
        )

        # Create file with CRLF line endings (write as binary to avoid platform conversion)
        Path(FILENAME).write_bytes(b"Line 1\r\nLine 2\r\nLine 3\r\n")

        # Should raise ValueError with descriptive message
        with pytest.raises(ValueError) as exc_info:
            validate_line_endings(FILENAME)
        assert "CRLF" in str(exc_info.value) or "Windows" in str(exc_info.value) or "\r\n" in str(
            exc_info.value
        )

    def test_validate_line_endings_rejects_cr_only(self):
        """Test that validation rejects file with Mac CR-only line endings."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_line_endings,
        )

        # Create file with CR-only line endings (old Mac format)
        Path(FILENAME).write_bytes(b"Line 1\rLine 2\rLine 3\r")

        # Should raise ValueError with descriptive message
        with pytest.raises(ValueError) as exc_info:
            validate_line_endings(FILENAME)
        assert "CR" in str(exc_info.value) or "carriage return" in str(exc_info.value) or "\r" in str(
            exc_info.value
        )

    def test_validate_line_endings_rejects_mixed_line_endings(self):
        """Test that validation rejects file with mixed line endings."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_line_endings,
        )

        # Create file with mixed line endings
        Path(FILENAME).write_bytes(b"Line 1\nLine 2\r\nLine 3\n")

        # Should raise ValueError
        with pytest.raises(ValueError):
            validate_line_endings(FILENAME)

    def test_validate_line_endings_handles_empty_file(self):
        """Test that validation handles empty files gracefully."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_line_endings,
        )

        # Create empty file
        Path(FILENAME).write_bytes(b"")

        # Empty file has no line endings to validate, should pass
        validate_line_endings(FILENAME)

    def test_validate_line_endings_with_single_line_no_ending(self):
        """Test that validation handles file with single line and no trailing newline."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_line_endings,
        )

        # Create file with single line without trailing newline
        Path(FILENAME).write_bytes(b"Single line without newline")

        # Should pass validation (no CRLF or CR present)
        validate_line_endings(FILENAME)

    def test_validate_line_endings_with_proper_markdown_file(self):
        """Test that validation passes for properly formatted markdown file."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            create_markdown_file,
            validate_line_endings,
        )

        create_markdown_file()
        # Should not raise any exception
        validate_line_endings(FILENAME)


class TestFeature191FileSizeValidation:
    """Tests for task 6: Implement file size validation (450-550 bytes)."""

    def setup_method(self):
        """Clean up any existing test file before each test."""
        from sheep.features.feature_191_markdown_file_creation import FILENAME

        test_file = Path(FILENAME)
        if test_file.exists():
            test_file.unlink()

    def teardown_method(self):
        """Clean up test file after each test."""
        from sheep.features.feature_191_markdown_file_creation import FILENAME

        test_file = Path(FILENAME)
        if test_file.exists():
            test_file.unlink()

    def test_validate_file_size_accepts_450_bytes(self):
        """Test that validate_file_size() accepts file at minimum size (450 bytes)."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_file_size,
        )

        # Create a file with exactly 450 bytes
        content = "x" * 450
        Path(FILENAME).write_text(content, encoding="utf-8")

        # Should not raise any exception
        validate_file_size(FILENAME)

    def test_validate_file_size_accepts_550_bytes(self):
        """Test that validate_file_size() accepts file at maximum size (550 bytes)."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_file_size,
        )

        # Create a file with exactly 550 bytes
        content = "x" * 550
        Path(FILENAME).write_text(content, encoding="utf-8")

        # Should not raise any exception
        validate_file_size(FILENAME)

    def test_validate_file_size_accepts_500_bytes_middle_range(self):
        """Test that validate_file_size() accepts file in middle of range."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_file_size,
        )

        # Create a file with 500 bytes
        content = "x" * 500
        Path(FILENAME).write_text(content, encoding="utf-8")

        # Should not raise any exception
        validate_file_size(FILENAME)

    def test_validate_file_size_rejects_449_bytes(self):
        """Test that validate_file_size() rejects file below minimum (449 bytes)."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_file_size,
        )

        # Create a file with 449 bytes (below minimum)
        content = "x" * 449
        Path(FILENAME).write_text(content, encoding="utf-8")

        # Should raise ValueError
        with pytest.raises(ValueError) as exc_info:
            validate_file_size(FILENAME)
        assert "size" in str(exc_info.value).lower()

    def test_validate_file_size_rejects_551_bytes(self):
        """Test that validate_file_size() rejects file above maximum (551 bytes)."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_file_size,
        )

        # Create a file with 551 bytes (above maximum)
        content = "x" * 551
        Path(FILENAME).write_text(content, encoding="utf-8")

        # Should raise ValueError
        with pytest.raises(ValueError) as exc_info:
            validate_file_size(FILENAME)
        assert "size" in str(exc_info.value).lower()

    def test_validate_file_size_error_message_includes_bounds(self):
        """Test that error message includes size bounds information."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_file_size,
        )

        # Create a file that's too small
        content = "x" * 400
        Path(FILENAME).write_text(content, encoding="utf-8")

        with pytest.raises(ValueError) as exc_info:
            validate_file_size(FILENAME)
        error_msg = str(exc_info.value)
        # Error should mention the actual size and acceptable range
        assert "400" in error_msg or "450" in error_msg

    def test_validate_file_size_rejects_empty_file(self):
        """Test that validate_file_size() rejects empty file."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            validate_file_size,
        )

        # Create an empty file
        Path(FILENAME).write_text("", encoding="utf-8")

        with pytest.raises(ValueError):
            validate_file_size(FILENAME)
