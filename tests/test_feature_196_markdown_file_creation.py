"""Tests for feature 196: Creating markdown file test-niog0h.md with title and prose content.

This module contains comprehensive tests for:
- Task 3: File creation with UTF-8 encoding and Unix line endings
- Task 4: Comprehensive validation (5 checks)
"""

import os
import sys
from pathlib import Path
import tempfile
import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sheep.features.feature_196_markdown_file_creation import (
    FILENAME,
    TITLE,
    PROSE,
    check_file_does_not_exist,
    create_markdown_file,
    validate_encoding,
    validate_line_endings,
    count_sentences,
    validate_structure,
    validate_file_size,
    main,
)


class TestContentConstants:
    """Tests for feature 196 constants."""

    def test_filename_is_correct(self):
        """Test that filename constant matches specification."""
        assert FILENAME == "test-niog0h.md"

    def test_title_is_meaningful(self):
        """Test that title is meaningful and substantial."""
        assert isinstance(TITLE, str)
        assert len(TITLE) > 0
        assert len(TITLE) > 10  # Substantial title
        # Title should be capitalized
        assert TITLE[0].isupper()

    def test_prose_is_meaningful(self):
        """Test that prose is meaningful and substantial."""
        assert isinstance(PROSE, str)
        assert len(PROSE) > 100  # Substantial prose
        # Should end with period (last sentence)
        assert PROSE.rstrip().endswith(".")

    def test_prose_has_three_sentences(self):
        """Test that prose contains exactly 3 sentences."""
        sentence_count = PROSE.count(".")
        assert sentence_count == 3


class TestFileCreation:
    """Tests for task-3: File creation with UTF-8 encoding and Unix line endings."""

    def setup_method(self):
        """Clean up test file before each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def teardown_method(self):
        """Clean up test file after each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def test_create_markdown_file_creates_file(self):
        """Test that create_markdown_file() function creates the file."""
        file_path = create_markdown_file()
        assert Path(FILENAME).exists()
        assert file_path == str(Path(FILENAME).absolute())

    def test_file_contains_h1_heading(self):
        """Test that file contains H1 heading as first line."""
        create_markdown_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        lines = content.split("\n")
        assert lines[0].startswith("# ")
        assert lines[0] == f"# {TITLE}"

    def test_file_has_blank_line_after_heading(self):
        """Test that file has blank line after H1 heading."""
        create_markdown_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        lines = content.split("\n")
        assert len(lines) >= 3
        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_file_contains_prose_content(self):
        """Test that file contains the prose content."""
        create_markdown_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        assert PROSE in content

    def test_file_ends_with_newline(self):
        """Test that file ends with trailing newline (Unix convention)."""
        create_markdown_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        assert content.endswith("\n")

    def test_file_uses_utf8_encoding(self):
        """Test that file is UTF-8 encoded."""
        create_markdown_file()
        # Read as binary and verify can be decoded as UTF-8
        binary_content = Path(FILENAME).read_bytes()
        decoded = binary_content.decode("utf-8")
        assert isinstance(decoded, str)
        assert len(decoded) > 0

    def test_file_uses_lf_line_endings(self):
        """Test that file uses LF line endings, not CRLF."""
        create_markdown_file()
        binary_content = Path(FILENAME).read_bytes()
        # Should contain LF
        assert b"\n" in binary_content
        # Should NOT contain CRLF
        assert b"\r\n" not in binary_content

    def test_file_size_is_reasonable(self):
        """Test that file size is within expected range (250-600 bytes)."""
        create_markdown_file()
        file_size = Path(FILENAME).stat().st_size
        assert 250 <= file_size <= 600

    def test_creates_file_with_correct_content_format(self):
        """Test that file is created with correct content format."""
        create_markdown_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        expected_content = f"# {TITLE}\n\n{PROSE}\n"
        assert content == expected_content

    def test_check_file_does_not_exist_before_creation(self):
        """Test that check_file_does_not_exist() raises FileExistsError if file exists."""
        create_markdown_file()
        with pytest.raises(FileExistsError):
            check_file_does_not_exist()


class TestValidationEncoding:
    """Tests for task-4: validate_encoding() - UTF-8 without BOM."""

    def setup_method(self):
        """Create test file before each test."""
        create_markdown_file()

    def teardown_method(self):
        """Clean up test file after each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def test_validate_encoding_passes_for_utf8_file(self):
        """Test that validate_encoding() passes for UTF-8 encoded file."""
        # This should not raise any exception
        validate_encoding()

    def test_file_does_not_have_utf8_bom(self):
        """Test that file does not contain UTF-8 BOM."""
        binary_content = Path(FILENAME).read_bytes()
        # UTF-8 BOM is bytes: 0xEF 0xBB 0xBF
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_validate_encoding_rejects_bom(self):
        """Test that validate_encoding() rejects file with UTF-8 BOM."""
        # Create file with BOM
        bom_content = b"\xef\xbb\xbf" + Path(FILENAME).read_bytes()
        Path(FILENAME).write_bytes(bom_content)

        # validate_encoding() should raise ValueError
        with pytest.raises(ValueError, match="BOM"):
            validate_encoding()

    def test_validate_encoding_file_exists_check(self):
        """Test that validate_encoding() checks if file exists."""
        Path(FILENAME).unlink()
        with pytest.raises(FileNotFoundError):
            validate_encoding()


class TestValidationLineEndings:
    """Tests for task-4: validate_line_endings() - Unix LF only."""

    def setup_method(self):
        """Create test file before each test."""
        create_markdown_file()

    def teardown_method(self):
        """Clean up test file after each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def test_validate_line_endings_passes_for_lf_file(self):
        """Test that validate_line_endings() passes for file with LF endings."""
        # This should not raise any exception
        validate_line_endings()

    def test_file_has_only_lf_line_endings(self):
        """Test that file contains only LF, no CRLF or CR."""
        binary_content = Path(FILENAME).read_bytes()
        # Should contain LF
        assert b"\n" in binary_content
        # Should NOT contain CRLF
        assert b"\r\n" not in binary_content
        # Should NOT contain CR without LF
        assert b"\r" not in binary_content

    def test_validate_line_endings_rejects_crlf(self):
        """Test that validate_line_endings() rejects CRLF line endings."""
        # Read file and convert LF to CRLF
        content = Path(FILENAME).read_text(encoding="utf-8")
        crlf_content = content.replace("\n", "\r\n")
        Path(FILENAME).write_text(crlf_content, encoding="utf-8")

        # validate_line_endings() should raise ValueError
        with pytest.raises(ValueError, match="CRLF"):
            validate_line_endings()

    def test_validate_line_endings_rejects_cr(self):
        """Test that validate_line_endings() rejects Mac CR line endings."""
        # Read file as binary and convert to CR only (no LF)
        binary_content = Path(FILENAME).read_bytes()
        cr_content = binary_content.replace(b"\n", b"\r")
        Path(FILENAME).write_bytes(cr_content)

        # validate_line_endings() should raise ValueError
        with pytest.raises(ValueError, match="CR"):
            validate_line_endings()


class TestCountSentences:
    """Tests for helper function: count_sentences()."""

    def test_count_sentences_zero(self):
        """Test sentence counting with no periods."""
        assert count_sentences("No periods here") == 0

    def test_count_sentences_one(self):
        """Test sentence counting with one period."""
        assert count_sentences("One sentence.") == 1

    def test_count_sentences_three(self):
        """Test sentence counting with three periods."""
        assert count_sentences("First. Second. Third.") == 3

    def test_count_sentences_in_prose(self):
        """Test sentence counting in actual prose."""
        assert count_sentences(PROSE) == 3


class TestValidationStructure:
    """Tests for task-4: validate_structure() - H1 heading and 2-3 sentences."""

    def setup_method(self):
        """Create test file before each test."""
        create_markdown_file()

    def teardown_method(self):
        """Clean up test file after each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def test_validate_structure_passes_for_valid_file(self):
        """Test that validate_structure() passes for valid file."""
        # This should not raise any exception
        validate_structure(FILENAME)

    def test_file_has_h1_heading(self):
        """Test that file starts with H1 heading."""
        content = Path(FILENAME).read_text(encoding="utf-8")
        assert content.startswith("# ")

    def test_file_has_2_to_3_sentences(self):
        """Test that file contains 2-3 sentences."""
        content = Path(FILENAME).read_text(encoding="utf-8")
        lines = content.split("\n")
        prose_text = "\n".join(lines[2:]).strip()
        sentence_count = prose_text.count(".")
        assert 2 <= sentence_count <= 3

    def test_validate_structure_rejects_missing_h1(self):
        """Test that validate_structure() rejects file without H1 heading."""
        # Create file without H1
        bad_content = f"No heading here\n\n{PROSE}\n"
        Path(FILENAME).write_text(bad_content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="H1"):
            validate_structure(FILENAME)

    def test_validate_structure_rejects_wrong_sentence_count(self):
        """Test that validate_structure() rejects file with wrong sentence count."""
        # Create file with only one sentence
        bad_content = f"# {TITLE}\n\nOnly one sentence.\n"
        Path(FILENAME).write_text(bad_content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="sentence"):
            validate_structure(FILENAME)

    def test_validate_structure_rejects_too_many_sentences(self):
        """Test that validate_structure() rejects file with too many sentences."""
        # Create file with 4 sentences
        bad_content = f"# {TITLE}\n\nFirst. Second. Third. Fourth.\n"
        Path(FILENAME).write_text(bad_content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="sentence"):
            validate_structure(FILENAME)


class TestValidationFileSize:
    """Tests for task-4: validate_file_size() - 300-600 bytes."""

    def setup_method(self):
        """Create test file before each test."""
        create_markdown_file()

    def teardown_method(self):
        """Clean up test file after each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def test_validate_file_size_passes_for_valid_size(self):
        """Test that validate_file_size() passes for file in valid range."""
        # This should not raise any exception
        validate_file_size(FILENAME)

    def test_file_size_is_in_valid_range(self):
        """Test that file size is between 300-600 bytes."""
        file_size = Path(FILENAME).stat().st_size
        assert 300 <= file_size <= 600

    def test_validate_file_size_rejects_too_small(self):
        """Test that validate_file_size() rejects file that is too small."""
        # Create file that is too small
        small_content = "# T\n\nSmall.\n"
        Path(FILENAME).write_text(small_content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="size"):
            validate_file_size(FILENAME)

    def test_validate_file_size_rejects_too_large(self):
        """Test that validate_file_size() rejects file that is too large."""
        # Create file that is too large
        large_content = f"# {TITLE}\n\n" + ("x" * 700) + "\n"
        Path(FILENAME).write_text(large_content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="size"):
            validate_file_size(FILENAME)


class TestIntegration:
    """Integration tests for complete workflow."""

    def setup_method(self):
        """Clean up test file before each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def teardown_method(self):
        """Clean up test file after each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def test_file_passes_all_validations(self):
        """Test that created file passes all validation checks."""
        create_markdown_file()

        # Should not raise any exceptions
        validate_encoding()
        validate_line_endings()
        validate_structure(FILENAME)
        validate_file_size(FILENAME)

    def test_file_content_and_format_correct(self):
        """Test that file has correct content and format."""
        create_markdown_file()

        content = Path(FILENAME).read_text(encoding="utf-8")

        # Check structure
        lines = content.split("\n")
        assert lines[0] == f"# {TITLE}"
        assert lines[1] == ""
        assert PROSE in content

        # Check sentence count
        prose_text = "\n".join(lines[2:]).strip()
        assert prose_text.count(".") == 3

        # Check encoding and line endings
        binary_content = Path(FILENAME).read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf")
        assert b"\r\n" not in binary_content

        # Check file size
        assert 300 <= len(binary_content) <= 600
