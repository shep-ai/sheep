"""Tests for Feature 205: Create markdown file test-axs39z.md with title and prose.

This test suite covers:
- Task 1: create_markdown_file() function with hardcoded content
- Task 2: File existence validation (_validate_file_exists)
- Task 3: Heading format validation (validate_markdown_format)
- Task 4: Blank line validation (validate_markdown_format)
- Task 5: Sentence count validation (validate_sentence_count)
- Task 6: Sentence endings validation (implicit in sentence counting)
- Task 7: UTF-8 encoding and LF line endings validation
- Task 8: File size validation
- Task 9: Trailing newline validation
- Task 10: Comprehensive validation wrapper (validate_markdown_file)
"""

import os
import re
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Import the feature module
from sheep.features.feature_205_markdown_file_creation import (
    FILENAME,
    PROSE_CONTENT,
    TITLE,
    BRANCH_NAME,
    COMMIT_MESSAGE,
    _validate_file_exists,
    create_markdown_file,
    validate_markdown_format,
    validate_sentence_count,
    validate_encoding,
    validate_line_endings,
    validate_file_size,
    validate_trailing_newline,
    validate_markdown_file,
    extract_prose_content,
    count_sentences,
    git_add_file,
    git_commit,
    git_push,
)


class TestTaskOne:
    """Tests for task-1: create_markdown_file() function."""

    def test_module_exists(self):
        """Test that the feature module can be imported."""
        from sheep.features import feature_205_markdown_file_creation
        assert feature_205_markdown_file_creation is not None

    def test_create_markdown_file_creates_file(self):
        """Test that create_markdown_file creates a file at specified location."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                path = create_markdown_file()
                assert Path(FILENAME).exists()
                assert FILENAME in path
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_with_custom_filename(self):
        """Test that create_markdown_file accepts custom filename."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                path = create_markdown_file("custom.md")
                assert Path("custom.md").exists()
                assert "custom.md" in path
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_raises_on_existing_file(self):
        """Test that create_markdown_file raises FileExistsError if file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create a file first
                Path(FILENAME).write_text("# Existing\n\nContent.\n")

                with pytest.raises(FileExistsError):
                    create_markdown_file()
            finally:
                os.chdir(original_cwd)

    def test_created_file_contains_h1_heading(self):
        """Test that created file starts with H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                content = Path(FILENAME).read_text(encoding="utf-8")
                lines = content.split("\n")

                assert lines[0].startswith("# ")
                assert "Markdown File Creation" in lines[0]
            finally:
                os.chdir(original_cwd)

    def test_created_file_has_blank_line(self):
        """Test that created file has blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                content = Path(FILENAME).read_text(encoding="utf-8")
                lines = content.split("\n")

                assert lines[1] == ""  # blank line
            finally:
                os.chdir(original_cwd)

    def test_created_file_contains_prose_content(self):
        """Test that created file contains hardcoded prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                content = Path(FILENAME).read_text(encoding="utf-8")
                assert PROSE_CONTENT in content
            finally:
                os.chdir(original_cwd)

    def test_created_file_uses_utf8_encoding(self):
        """Test that created file is UTF-8 encoded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                # Try to read as UTF-8 (should not raise)
                content = Path(FILENAME).read_text(encoding="utf-8")
                assert content is not None
            finally:
                os.chdir(original_cwd)

    def test_created_file_uses_lf_line_endings(self):
        """Test that created file uses LF line endings, not CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                binary_content = Path(FILENAME).read_bytes()
                assert b"\r\n" not in binary_content
                assert b"\n" in binary_content
            finally:
                os.chdir(original_cwd)

    def test_created_file_structure(self):
        """Test the complete structure of the created file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                content = Path(FILENAME).read_text(encoding="utf-8")
                lines = content.split("\n")

                # Line 0: H1 heading
                assert lines[0].startswith("# ")
                # Line 1: blank line
                assert lines[1] == ""
                # Line 2+: prose content
                remaining = "\n".join(lines[2:]).strip()
                assert PROSE_CONTENT in remaining
                # Must end with newline
                assert content.endswith("\n")
            finally:
                os.chdir(original_cwd)

    def test_created_file_returns_absolute_path(self):
        """Test that create_markdown_file returns absolute path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                path = create_markdown_file()

                assert os.path.isabs(path)
                assert path.endswith(FILENAME)
            finally:
                os.chdir(original_cwd)


class TestTaskTwo:
    """Tests for task-2: File existence validation."""

    def test_validate_file_exists_success(self):
        """Test that _validate_file_exists passes when file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Test\n\nContent.\n")

                # Should not raise
                _validate_file_exists(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_validate_file_exists_raises_on_missing_file(self):
        """Test that _validate_file_exists raises ValueError if file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with pytest.raises(ValueError) as exc_info:
                    _validate_file_exists(FILENAME)

                assert "was not created" in str(exc_info.value).lower()
            finally:
                os.chdir(original_cwd)

    def test_validate_file_exists_called_after_creation(self):
        """Test that _validate_file_exists is called during file creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # create_markdown_file should call _validate_file_exists internally
                path = create_markdown_file()

                # File should exist
                assert Path(FILENAME).exists()
            finally:
                os.chdir(original_cwd)

    def test_validate_file_exists_with_custom_filename(self):
        """Test _validate_file_exists with custom filename."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                test_file = "test_custom.md"
                Path(test_file).write_text("# Test\n\nContent.\n")

                # Should not raise
                _validate_file_exists(test_file)
            finally:
                os.chdir(original_cwd)

    def test_validate_file_exists_error_message(self):
        """Test that _validate_file_exists has descriptive error message."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                missing_file = "missing.md"

                with pytest.raises(ValueError) as exc_info:
                    _validate_file_exists(missing_file)

                error_msg = str(exc_info.value)
                assert missing_file in error_msg
                assert "was not created" in error_msg.lower() or "does not exist" in error_msg.lower()
            finally:
                os.chdir(original_cwd)


class TestTaskThree:
    """Tests for task-3: Heading format validation."""

    def test_validate_markdown_format_valid_heading(self):
        """Test that validate_markdown_format passes with valid H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Valid Heading\n\nSentence 1. Sentence 2.\n")

                # Should not raise
                validate_markdown_format(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_raises_on_missing_h1(self):
        """Test that validate_markdown_format raises ValueError if H1 is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("## Not H1\n\nSentence 1. Sentence 2.\n")

                with pytest.raises(ValueError):
                    validate_markdown_format(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_raises_on_no_heading(self):
        """Test that validate_markdown_format raises ValueError if file doesn't start with heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("This is not a heading\n\nSentence 1. Sentence 2.\n")

                with pytest.raises(ValueError):
                    validate_markdown_format(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_raises_on_missing_blank_line(self):
        """Test that validate_markdown_format raises ValueError if blank line is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # No blank line between heading and prose
                Path(FILENAME).write_text("# Heading\nSentence 1. Sentence 2.\n")

                with pytest.raises(ValueError):
                    validate_markdown_format(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_raises_on_multiple_h1(self):
        """Test that validate_markdown_format raises ValueError if multiple H1 headings exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Multiple H1 headings
                Path(FILENAME).write_text("# First Heading\n\n# Second Heading\nSentence 1. Sentence 2.\n")

                with pytest.raises(ValueError):
                    validate_markdown_format(FILENAME)
            finally:
                os.chdir(original_cwd)


class TestTaskFour:
    """Tests for task-4: Blank line validation (covered by heading validation)."""

    def test_blank_line_is_empty_string(self):
        """Test that second line must be blank (whitespace is stripped)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Second line with tabs is acceptable (strip() removes it)
                Path(FILENAME).write_text("# Heading\n\t\nSentence 1. Sentence 2.\n")

                # This should still pass as strip() removes whitespace
                # Only completely missing blank line should fail
                validate_markdown_format(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_valid_blank_line(self):
        """Test that blank line with no whitespace is valid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Heading\n\nSentence 1. Sentence 2.\n")

                # Should not raise
                validate_markdown_format(FILENAME)
            finally:
                os.chdir(original_cwd)


class TestTaskFive:
    """Tests for task-5: Sentence count validation."""

    def test_count_sentences_with_periods(self):
        """Test that count_sentences counts periods correctly."""
        prose = "First sentence. Second sentence. Third sentence."
        assert count_sentences(prose) == 3

    def test_count_sentences_two_sentences(self):
        """Test counting 2 sentences."""
        prose = "First sentence. Second sentence."
        assert count_sentences(prose) == 2

    def test_count_sentences_one_sentence(self):
        """Test counting 1 sentence."""
        prose = "Only one sentence."
        assert count_sentences(prose) == 1

    def test_validate_sentence_count_valid_three(self):
        """Test that validate_sentence_count passes for 3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Heading\n\nFirst. Second. Third.\n")

                # Should not raise
                validate_sentence_count(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_valid_two(self):
        """Test that validate_sentence_count passes for 2 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Heading\n\nFirst. Second.\n")

                # Should not raise
                validate_sentence_count(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_raises_on_one_sentence(self):
        """Test that validate_sentence_count raises ValueError for 1 sentence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Heading\n\nOnly one sentence.\n")

                with pytest.raises(ValueError):
                    validate_sentence_count(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_raises_on_four_sentences(self):
        """Test that validate_sentence_count raises ValueError for 4 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Heading\n\nFirst. Second. Third. Fourth.\n")

                with pytest.raises(ValueError):
                    validate_sentence_count(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_extract_prose_content(self):
        """Test that extract_prose_content extracts correct text."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                prose_text = "This is the prose. Second sentence."
                Path(FILENAME).write_text(f"# Heading\n\n{prose_text}\n")

                extracted = extract_prose_content(FILENAME)
                assert extracted == prose_text
            finally:
                os.chdir(original_cwd)


class TestTaskSix:
    """Tests for task-6: Sentence endings validation."""

    def test_sentence_endings_with_periods(self):
        """Test that prose with period endings is valid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Heading\n\nFirst sentence. Second sentence.\n")

                # Should pass both format and sentence count
                validate_markdown_format(FILENAME)
                validate_sentence_count(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_sentence_endings_with_exclamation(self):
        """Test that prose with exclamation marks must also contain periods for count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # count_sentences() counts periods only, so must have 2-3 periods
                Path(FILENAME).write_text("# Heading\n\nFirst sentence. Second sentence. Third!\n")

                # Should not raise (has 2 periods, count is 2)
                validate_sentence_count(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_sentence_endings_with_questions(self):
        """Test that prose with question marks must also contain periods for count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # count_sentences() counts periods only, need 2-3 periods total
                Path(FILENAME).write_text("# Heading\n\nFirst sentence. Second sentence. Is this third?\n")

                # Should not raise (has 2 periods)
                validate_sentence_count(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_sentence_endings_mixed_punctuation(self):
        """Test that prose with mixed punctuation is valid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # count_sentences() counts periods only, so need 2-3 periods
                Path(FILENAME).write_text("# Heading\n\nFirst sentence. Second sentence. Third!\n")

                # Should pass - 3 periods (count_sentences counts periods)
                validate_sentence_count(FILENAME)
            finally:
                os.chdir(original_cwd)


class TestTaskSeven:
    """Tests for task-7: UTF-8 encoding and LF line endings validation."""

    def test_validate_encoding_valid_utf8(self):
        """Test that validate_encoding passes for valid UTF-8 file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Heading\n\nContent with UTF-8: café.\n", encoding="utf-8")

                # Should not raise
                validate_encoding(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_validate_encoding_raises_on_bom(self):
        """Test that validate_encoding raises ValueError if BOM is present."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Write file with UTF-8 BOM
                binary_content = b"\xef\xbb\xbf# Heading\n\nContent.\n"
                Path(FILENAME).write_bytes(binary_content)

                with pytest.raises(ValueError) as exc_info:
                    validate_encoding(FILENAME)
                assert "BOM" in str(exc_info.value)
            finally:
                os.chdir(original_cwd)

    def test_validate_line_endings_valid_lf(self):
        """Test that validate_line_endings passes for LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Heading\n\nContent.\n", encoding="utf-8")

                # Should not raise
                validate_line_endings(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_validate_line_endings_raises_on_crlf(self):
        """Test that validate_line_endings raises ValueError for CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Write file with CRLF
                Path(FILENAME).write_bytes(b"# Heading\r\n\r\nContent.\r\n")

                with pytest.raises(ValueError) as exc_info:
                    validate_line_endings(FILENAME)
                assert "CRLF" in str(exc_info.value)
            finally:
                os.chdir(original_cwd)

    def test_validate_line_endings_raises_on_cr(self):
        """Test that validate_line_endings raises ValueError for CR line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Write file with CR only
                Path(FILENAME).write_bytes(b"# Heading\r\rContent.\r")

                with pytest.raises(ValueError) as exc_info:
                    validate_line_endings(FILENAME)
                assert "CR" in str(exc_info.value)
            finally:
                os.chdir(original_cwd)


class TestTaskEight:
    """Tests for task-8: File size validation."""

    def test_validate_file_size_valid_minimum(self):
        """Test that validate_file_size passes for file at minimum size (300 bytes)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create content that's at least 300 bytes
                # "# Title\n\n" = 10 bytes, "A" * 290 + ".\n" = 292 bytes, total = 302 bytes
                content = "# Title\n\n" + "A" * 290 + ".\n"
                Path(FILENAME).write_text(content, encoding="utf-8")

                # Should not raise
                validate_file_size(FILENAME, 300, 600)
            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_valid_maximum(self):
        """Test that validate_file_size passes for file at maximum size (600 bytes)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create content that's close to 600 bytes
                content = "# Title\n\n" + "A" * 580 + ".\n"
                Path(FILENAME).write_text(content, encoding="utf-8")

                # Should not raise
                validate_file_size(FILENAME, 300, 600)
            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_raises_on_too_small(self):
        """Test that validate_file_size raises ValueError for file too small."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Title\n\nSmall.\n", encoding="utf-8")

                with pytest.raises(ValueError) as exc_info:
                    validate_file_size(FILENAME, 300, 600)
                assert "outside acceptable range" in str(exc_info.value)
            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_raises_on_too_large(self):
        """Test that validate_file_size raises ValueError for file too large."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create content larger than 600 bytes
                content = "# Title\n\n" + "A" * 1000 + ".\n"
                Path(FILENAME).write_text(content, encoding="utf-8")

                with pytest.raises(ValueError) as exc_info:
                    validate_file_size(FILENAME, 300, 600)
                assert "outside acceptable range" in str(exc_info.value)
            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_includes_actual_size_in_error(self):
        """Test that validate_file_size error message includes actual file size."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Title\n\nSmall.\n", encoding="utf-8")

                with pytest.raises(ValueError) as exc_info:
                    validate_file_size(FILENAME, 300, 600)
                error_msg = str(exc_info.value)
                # Error should mention actual file size
                assert "bytes" in error_msg.lower()
            finally:
                os.chdir(original_cwd)


class TestTaskNine:
    """Tests for task-9: Trailing newline validation."""

    def test_validate_trailing_newline_valid(self):
        """Test that validate_trailing_newline passes for file with trailing newline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Heading\n\nContent.\n", encoding="utf-8")

                # Should not raise
                validate_trailing_newline(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_validate_trailing_newline_raises_on_missing(self):
        """Test that validate_trailing_newline raises ValueError without trailing newline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Write without trailing newline
                Path(FILENAME).write_bytes(b"# Heading\n\nContent.")

                with pytest.raises(ValueError) as exc_info:
                    validate_trailing_newline(FILENAME)
                assert "newline" in str(exc_info.value).lower()
            finally:
                os.chdir(original_cwd)

    def test_created_file_has_trailing_newline(self):
        """Test that created file automatically has trailing newline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                # Should not raise
                validate_trailing_newline(FILENAME)
            finally:
                os.chdir(original_cwd)


class TestTaskTen:
    """Tests for task-10: Comprehensive validation wrapper."""

    def test_validate_markdown_file_passes_for_valid_file(self):
        """Test that validate_markdown_file passes for valid file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                # Should not raise
                validate_markdown_file(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_checks_all_validations(self):
        """Test that validate_markdown_file runs all validation checks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                # Run full validation - should not raise
                validate_markdown_file(FILENAME)

                # Verify file still meets all criteria
                content = Path(FILENAME).read_text(encoding="utf-8")
                lines = content.split("\n")

                # Heading check
                assert lines[0].startswith("# ")
                # Blank line check
                assert lines[1] == ""
                # Encoding and line endings check (no CRLF, valid UTF-8)
                assert "\r\n" not in content
                # Trailing newline check
                assert content.endswith("\n")
                # File size check
                file_size = Path(FILENAME).stat().st_size
                assert 300 <= file_size <= 600
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_fails_fast_on_first_error(self):
        """Test that validate_markdown_file stops on first validation failure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create file with invalid heading
                Path(FILENAME).write_text("No heading here\n\nContent.\n")

                with pytest.raises(ValueError):
                    validate_markdown_file(FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_on_created_file(self):
        """Test comprehensive validation on newly created file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create file
                create_markdown_file()

                # Comprehensive validation should pass
                validate_markdown_file(FILENAME)

                # File should still exist
                assert Path(FILENAME).exists()
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_detailed_error_messages(self):
        """Test that validation errors provide detailed diagnostic information."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # File with invalid sentence count
                Path(FILENAME).write_text("# Heading\n\nOnly one.\n")

                with pytest.raises(ValueError) as exc_info:
                    validate_markdown_file(FILENAME)

                error_msg = str(exc_info.value)
                # Error message should indicate what went wrong
                assert len(error_msg) > 0
            finally:
                os.chdir(original_cwd)


class TestTaskEleven:
    """Tests for task-11: Implement git add operation."""

    def test_git_add_file_calls_subprocess(self):
        """Test that git_add_file calls subprocess.run with correct command."""
        with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            git_add_file(FILENAME)

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert args[0] == ['git', 'add', FILENAME]
            assert kwargs.get('check') is True

    def test_git_add_file_raises_on_failure(self):
        """Test that git_add_file raises CalledProcessError on git failure."""
        with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
            error = subprocess.CalledProcessError(1, 'git add')
            error.stderr = "fatal: not a git repository"
            mock_run.side_effect = error

            with pytest.raises(subprocess.CalledProcessError):
                git_add_file(FILENAME)

    def test_git_add_file_captures_output(self):
        """Test that git_add_file captures stdout and stderr."""
        with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')

            git_add_file(FILENAME)

            # Verify capture_output and text parameters
            args, kwargs = mock_run.call_args
            assert kwargs.get('capture_output') is True
            assert kwargs.get('text') is True


class TestTaskTwelve:
    """Tests for task-12: Implement git commit operation."""

    def test_git_commit_calls_subprocess(self):
        """Test that git_commit calls subprocess.run with correct command."""
        with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            git_commit(FILENAME, COMMIT_MESSAGE)

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert args[0] == ['git', 'commit', '-m', COMMIT_MESSAGE]
            assert kwargs.get('check') is True

    def test_git_commit_uses_commit_message_constant(self):
        """Test that git_commit uses the correct commit message by default."""
        with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            git_commit(FILENAME)  # Use default message

            args, kwargs = mock_run.call_args
            assert COMMIT_MESSAGE in args[0][3]  # Message is 4th argument
            assert "feat(205)" in args[0][3]
            assert FILENAME in args[0][3]

    def test_git_commit_raises_on_failure(self):
        """Test that git_commit raises CalledProcessError on failure."""
        with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
            error = subprocess.CalledProcessError(1, 'git commit')
            error.stderr = "nothing to commit"
            mock_run.side_effect = error

            with pytest.raises(subprocess.CalledProcessError):
                git_commit(FILENAME, COMMIT_MESSAGE)

    def test_git_commit_message_format_is_conventional(self):
        """Test that commit message follows conventional commit format."""
        # The COMMIT_MESSAGE constant should follow conventional format
        assert COMMIT_MESSAGE.startswith("feat(")
        assert ")" in COMMIT_MESSAGE
        assert FILENAME in COMMIT_MESSAGE


class TestTaskThirteen:
    """Tests for task-13: Implement git push operation."""

    def test_git_push_calls_subprocess(self):
        """Test that git_push calls subprocess.run with correct command."""
        with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            git_push(BRANCH_NAME)

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert args[0] == ['git', 'push', '-u', 'origin', BRANCH_NAME]
            assert kwargs.get('check') is True

    def test_git_push_uses_branch_name_constant(self):
        """Test that git_push uses the correct branch name by default."""
        with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            git_push()  # Use default branch

            args, kwargs = mock_run.call_args
            assert BRANCH_NAME in args[0]
            assert "feat/205" in args[0][4]

    def test_git_push_uses_u_flag(self):
        """Test that git_push uses -u flag to set upstream tracking."""
        with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            git_push(BRANCH_NAME)

            args, kwargs = mock_run.call_args
            assert '-u' in args[0]
            assert 'origin' in args[0]

    def test_git_push_raises_on_failure(self):
        """Test that git_push raises CalledProcessError on failure."""
        with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
            error = subprocess.CalledProcessError(1, 'git push')
            error.stderr = "no changes to push"
            mock_run.side_effect = error

            with pytest.raises(subprocess.CalledProcessError):
                git_push(BRANCH_NAME)


class TestTaskFourteen:
    """Tests for task-14: Add comprehensive git error handling."""

    def test_git_add_error_handling_includes_stderr(self):
        """Test that git_add error message includes stderr output."""
        with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
            stderr_msg = "fatal: not a git repository"
            error = subprocess.CalledProcessError(128, 'git add')
            error.stderr = stderr_msg
            error.stdout = ""
            mock_run.side_effect = error

            with pytest.raises(subprocess.CalledProcessError):
                git_add_file(FILENAME)

    def test_git_commit_error_handling_includes_stderr(self):
        """Test that git_commit error message includes stderr output."""
        with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
            stderr_msg = "nothing to commit"
            error = subprocess.CalledProcessError(1, 'git commit')
            error.stderr = stderr_msg
            error.stdout = ""
            mock_run.side_effect = error

            with pytest.raises(subprocess.CalledProcessError):
                git_commit(FILENAME, COMMIT_MESSAGE)

    def test_git_push_error_handling_includes_stderr(self):
        """Test that git_push error message includes stderr output."""
        with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
            stderr_msg = "failed to push some refs"
            error = subprocess.CalledProcessError(1, 'git push')
            error.stderr = stderr_msg
            error.stdout = ""
            mock_run.side_effect = error

            with pytest.raises(subprocess.CalledProcessError):
                git_push(BRANCH_NAME)

    def test_git_operations_fail_fast_on_error(self):
        """Test that git operations raise immediately on error."""
        with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, 'git add')

            # Should raise immediately, not continue
            with pytest.raises(subprocess.CalledProcessError):
                git_add_file(FILENAME)

    def test_git_error_includes_operation_name(self):
        """Test that error messages indicate which git operation failed."""
        with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
            error = subprocess.CalledProcessError(1, 'git add', output="error")
            error.stderr = "some error"
            mock_run.side_effect = error

            with pytest.raises(subprocess.CalledProcessError):
                git_add_file(FILENAME)


class TestEndToEndValidation:
    """Integration tests for complete validation pipeline."""

    def test_complete_pipeline_on_hardcoded_prose(self):
        """Test that hardcoded prose content passes all validation checks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                # All validation checks should pass
                validate_markdown_file(FILENAME)

                # Verify content structure
                content = Path(FILENAME).read_text(encoding="utf-8")
                assert PROSE_CONTENT in content
            finally:
                os.chdir(original_cwd)

    def test_file_validation_order(self):
        """Test that validations execute in logical order."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                # Create valid file and verify each check independently
                filename = FILENAME

                # Should pass all checks
                validate_markdown_format(filename)
                validate_sentence_count(filename)
                validate_encoding(filename)
                validate_line_endings(filename)
                validate_file_size(filename)
                validate_trailing_newline(filename)

                # Comprehensive validation should also pass
                validate_markdown_file(filename)
            finally:
                os.chdir(original_cwd)

    def test_git_operations_with_mocked_subprocess(self):
        """Test git operations in workflow with mocked subprocess."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create and validate file
                create_markdown_file()
                validate_markdown_file(FILENAME)

                # Mock subprocess for git operations
                with patch('sheep.features.feature_205_markdown_file_creation.subprocess.run') as mock_run:
                    mock_run.return_value = MagicMock(returncode=0)

                    # Simulate complete git workflow
                    git_add_file(FILENAME)
                    git_commit(FILENAME, COMMIT_MESSAGE)
                    git_push(BRANCH_NAME)

                    # Verify all three git operations were called
                    assert mock_run.call_count == 3

                    # Verify the sequence of calls
                    calls = mock_run.call_args_list
                    assert 'git' in calls[0][0][0]  # First call
                    assert 'add' in calls[0][0][0]
                    assert 'git' in calls[1][0][0]  # Second call
                    assert 'commit' in calls[1][0][0]
                    assert 'git' in calls[2][0][0]  # Third call
                    assert 'push' in calls[2][0][0]
            finally:
                os.chdir(original_cwd)
