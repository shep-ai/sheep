"""Tests for feature 207: Create markdown file test-jkyks3.md.

Tests cover file creation with correct format, encoding, and line endings.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from sheep.features.feature_207_markdown_file_creation import (
    FILENAME,
    PROSE_CONTENT,
    TITLE_TEXT,
    create_markdown_file,
    verify_file_exists,
    validate_markdown_format,
    extract_prose_content,
    count_sentences,
    validate_sentence_count,
)


class TestFileCreation:
    """Tests for file creation functionality."""

    def test_create_markdown_file_creates_file(self):
        """Test that create_markdown_file creates a file at the correct path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Verify file doesn't exist initially
                assert not Path(FILENAME).exists()

                # Create file
                file_path = create_markdown_file()

                # Verify file was created
                assert file_path.exists()
                assert file_path.name == FILENAME
            finally:
                import os

                os.chdir(original_cwd)

    def test_create_markdown_file_contains_title(self):
        """Test that created file contains the H1 title."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                content = Path(FILENAME).read_text()
                assert f"# {TITLE_TEXT}" in content
                # Verify it's at the start (H1 heading should be first line)
                assert content.startswith(f"# {TITLE_TEXT}")
            finally:
                import os

                os.chdir(original_cwd)

    def test_create_markdown_file_contains_prose(self):
        """Test that created file contains the prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                content = Path(FILENAME).read_text()
                assert PROSE_CONTENT in content
            finally:
                import os

                os.chdir(original_cwd)

    def test_create_markdown_file_utf8_encoding(self):
        """Test that file is created with UTF-8 encoding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Read as bytes and verify no UTF-8 BOM
                binary_content = Path(FILENAME).read_bytes()
                assert not binary_content.startswith(b"\xef\xbb\xbf")
                # Verify valid UTF-8
                binary_content.decode("utf-8")
            finally:
                import os

                os.chdir(original_cwd)

    def test_create_markdown_file_lf_line_endings(self):
        """Test that file uses Unix LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                binary_content = Path(FILENAME).read_bytes()
                # Check no CRLF or CR
                assert b"\r\n" not in binary_content
                assert b"\r" not in binary_content
            finally:
                import os

                os.chdir(original_cwd)

    def test_create_markdown_file_returns_path(self):
        """Test that create_markdown_file returns a Path object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                result = create_markdown_file()
                assert isinstance(result, Path)
            finally:
                import os

                os.chdir(original_cwd)

    def test_create_markdown_file_has_blank_line_separator(self):
        """Test that file has blank line between title and prose."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                content = Path(FILENAME).read_text()
                lines = content.split("\n")
                # First line should be the title
                assert lines[0].startswith("# ")
                # Second line should be blank
                assert lines[1] == ""
                # Third line should be the start of prose
                assert len(lines) > 2
            finally:
                import os

                os.chdir(original_cwd)

    def test_create_markdown_file_size_in_range(self):
        """Test that created file size is within expected range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                file_size = Path(FILENAME).stat().st_size
                # Specification requires 250-600 bytes
                assert 250 <= file_size <= 600, f"File size {file_size} out of range 250-600"
            finally:
                import os

                os.chdir(original_cwd)


class TestVerifyFileExists:
    """Tests for verify_file_exists validation function."""

    def test_verify_file_exists_raises_when_file_missing(self):
        """Test that verify_file_exists raises FileNotFoundError when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with pytest.raises(FileNotFoundError):
                    verify_file_exists(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_verify_file_exists_passes_when_file_exists(self):
        """Test that verify_file_exists does not raise when file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should not raise
                verify_file_exists(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)


class TestValidateMarkdownFormat:
    """Tests for validate_markdown_format validation function."""

    def test_validate_markdown_format_valid_file(self):
        """Test that validate_markdown_format passes for valid markdown."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should not raise
                validate_markdown_format(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_format_missing_h1(self):
        """Test that validate_markdown_format fails when H1 heading is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file without H1 heading
                Path(FILENAME).write_text("No heading here\n\nSome prose.", encoding="utf-8")
                with pytest.raises(ValueError):
                    validate_markdown_format(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_format_missing_blank_line(self):
        """Test that validate_markdown_format fails when blank line separator is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file without blank line after heading
                Path(FILENAME).write_text("# Title\nProse immediately after.", encoding="utf-8")
                with pytest.raises(ValueError):
                    validate_markdown_format(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_format_multiple_h1_headings(self):
        """Test that validate_markdown_format fails with multiple H1 headings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file with multiple H1 headings
                Path(FILENAME).write_text(
                    "# Title 1\n\n# Title 2\nProse.", encoding="utf-8"
                )
                with pytest.raises(ValueError):
                    validate_markdown_format(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)


class TestExtractProseContent:
    """Tests for extract_prose_content helper function."""

    def test_extract_prose_content_valid_file(self):
        """Test that extract_prose_content returns correct prose."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                prose = extract_prose_content(FILENAME)
                assert prose == PROSE_CONTENT
            finally:
                import os

                os.chdir(original_cwd)

    def test_extract_prose_content_missing_blank_line(self):
        """Test that extract_prose_content raises when blank line is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Title\nNo blank line.", encoding="utf-8")
                with pytest.raises(ValueError):
                    extract_prose_content(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)


class TestCountSentences:
    """Tests for count_sentences helper function."""

    def test_count_sentences_valid_prose(self):
        """Test that count_sentences returns correct count."""
        prose = "First sentence. Second sentence. Third sentence."
        assert count_sentences(prose) == 3

    def test_count_sentences_two_sentences(self):
        """Test count_sentences with exactly two sentences."""
        prose = "First sentence. Second sentence."
        assert count_sentences(prose) == 2

    def test_count_sentences_empty_prose(self):
        """Test that count_sentences raises for empty prose."""
        with pytest.raises(ValueError):
            count_sentences("")

    def test_count_sentences_no_periods(self):
        """Test count_sentences with no periods."""
        prose = "This prose has no periods"
        assert count_sentences(prose) == 0


class TestValidateSentenceCount:
    """Tests for validate_sentence_count validation function."""

    def test_validate_sentence_count_valid_three_sentences(self):
        """Test that validate_sentence_count passes with 3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should not raise
                validate_sentence_count(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_sentence_count_valid_two_sentences(self):
        """Test that validate_sentence_count passes with 2 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file with exactly 2 sentences
                content = "# Title\n\nFirst sentence. Second sentence.\n"
                Path(FILENAME).write_text(content, encoding="utf-8")
                # Should not raise
                validate_sentence_count(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_sentence_count_too_few_sentences(self):
        """Test that validate_sentence_count fails with only 1 sentence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file with only 1 sentence
                content = "# Title\n\nOnly one sentence.\n"
                Path(FILENAME).write_text(content, encoding="utf-8")
                with pytest.raises(ValueError):
                    validate_sentence_count(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_sentence_count_too_many_sentences(self):
        """Test that validate_sentence_count fails with 4 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file with 4 sentences
                content = "# Title\n\nOne. Two. Three. Four.\n"
                Path(FILENAME).write_text(content, encoding="utf-8")
                with pytest.raises(ValueError):
                    validate_sentence_count(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)
