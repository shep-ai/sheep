"""Tests for feature 207: Create markdown file test-jkyks3.md.

Tests cover file creation with correct format, encoding, and line endings.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

import subprocess
from unittest.mock import patch, MagicMock

from sheep.features.feature_207_markdown_file_creation import (
    FILENAME,
    PROSE_CONTENT,
    TITLE_TEXT,
    BRANCH_NAME,
    COMMIT_MESSAGE,
    create_markdown_file,
    verify_file_exists,
    validate_markdown_format,
    extract_prose_content,
    count_sentences,
    validate_sentence_count,
    validate_encoding,
    validate_line_endings,
    validate_file_size,
    validate_markdown_file,
    git_add_file,
    git_commit,
    git_push,
    main,
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


class TestValidateEncoding:
    """Tests for validate_encoding validation function."""

    def test_validate_encoding_valid_utf8(self):
        """Test that validate_encoding passes for valid UTF-8 file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should not raise
                validate_encoding(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_encoding_no_bom(self):
        """Test that validate_encoding verifies no UTF-8 BOM exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file and verify no BOM
                Path(FILENAME).write_text("# Test\n\nContent.", encoding="utf-8")
                binary = Path(FILENAME).read_bytes()
                assert not binary.startswith(b"\xef\xbb\xbf")
                # validate_encoding should pass
                validate_encoding(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_encoding_rejects_bom(self):
        """Test that validate_encoding rejects file with UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file with UTF-8 BOM
                content = "# Title\n\nProse content."
                binary_with_bom = b"\xef\xbb\xbf" + content.encode("utf-8")
                Path(FILENAME).write_bytes(binary_with_bom)
                with pytest.raises(ValueError, match="UTF-8 BOM"):
                    validate_encoding(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_encoding_rejects_invalid_utf8(self):
        """Test that validate_encoding rejects file with invalid UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file with invalid UTF-8 bytes
                invalid_bytes = b"\xff\xfe"
                Path(FILENAME).write_bytes(invalid_bytes)
                with pytest.raises(ValueError, match="invalid UTF-8"):
                    validate_encoding(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_encoding_missing_file(self):
        """Test that validate_encoding raises FileNotFoundError for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with pytest.raises(FileNotFoundError):
                    validate_encoding(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)


class TestValidateLineEndings:
    """Tests for validate_line_endings validation function."""

    def test_validate_line_endings_valid_lf(self):
        """Test that validate_line_endings passes for Unix LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should not raise
                validate_line_endings(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_line_endings_rejects_crlf(self):
        """Test that validate_line_endings rejects Windows CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file with CRLF line endings
                content = "# Title\r\n\r\nContent."
                Path(FILENAME).write_bytes(content.encode("utf-8"))
                with pytest.raises(ValueError, match="CRLF"):
                    validate_line_endings(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_line_endings_rejects_cr(self):
        """Test that validate_line_endings rejects Mac CR line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file with CR line endings
                content = "# Title\r\rContent."
                Path(FILENAME).write_bytes(content.encode("utf-8"))
                with pytest.raises(ValueError, match="CR"):
                    validate_line_endings(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_line_endings_missing_file(self):
        """Test that validate_line_endings raises FileNotFoundError for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with pytest.raises(FileNotFoundError):
                    validate_line_endings(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)


class TestValidateFileSize:
    """Tests for validate_file_size validation function."""

    def test_validate_file_size_valid_size(self):
        """Test that validate_file_size passes for file in acceptable range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should not raise
                validate_file_size(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_file_size_custom_range(self):
        """Test that validate_file_size respects custom min/max parameters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create a file with 100 bytes
                content = "x" * 100
                Path(FILENAME).write_text(content, encoding="utf-8")
                # Should pass with custom range
                validate_file_size(FILENAME, min_bytes=50, max_bytes=150)
                # Should fail with default range (too small)
                with pytest.raises(ValueError, match="below minimum"):
                    validate_file_size(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_file_size_too_small(self):
        """Test that validate_file_size rejects file below minimum size."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create a small file (less than 250 bytes)
                content = "x" * 100
                Path(FILENAME).write_text(content, encoding="utf-8")
                with pytest.raises(ValueError, match="below minimum"):
                    validate_file_size(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_file_size_too_large(self):
        """Test that validate_file_size rejects file above maximum size."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create a large file (more than 600 bytes)
                content = "x" * 700
                Path(FILENAME).write_text(content, encoding="utf-8")
                with pytest.raises(ValueError, match="exceeds maximum"):
                    validate_file_size(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_file_size_missing_file(self):
        """Test that validate_file_size raises FileNotFoundError for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with pytest.raises(FileNotFoundError):
                    validate_file_size(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)


class TestValidateMarkdownFile:
    """Tests for validate_markdown_file validation pipeline function."""

    def test_validate_markdown_file_valid_markdown(self):
        """Test that validate_markdown_file passes for valid markdown file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should not raise
                validate_markdown_file(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_file_missing_file(self):
        """Test that validate_markdown_file raises FileNotFoundError when file is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with pytest.raises(FileNotFoundError, match="does not exist"):
                    validate_markdown_file(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_file_corrupted_format(self):
        """Test that validate_markdown_file fails when markdown format is corrupted."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file without H1 heading
                Path(FILENAME).write_text("No heading here\n\nSome prose.", encoding="utf-8")
                with pytest.raises(ValueError, match="H1 heading"):
                    validate_markdown_file(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_file_invalid_sentence_count(self):
        """Test that validate_markdown_file fails with incorrect sentence count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file with only 1 sentence (invalid)
                content = "# Title\n\nOnly one sentence.\n"
                Path(FILENAME).write_text(content, encoding="utf-8")
                with pytest.raises(ValueError, match="2-3 sentences"):
                    validate_markdown_file(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_file_invalid_encoding(self):
        """Test that validate_markdown_file fails with invalid encoding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file with invalid UTF-8 bytes
                invalid_bytes = b"\xff\xfe"
                Path(FILENAME).write_bytes(invalid_bytes)
                # Invalid encoding will be caught during format validation or encoding validation
                # Both will raise an exception
                with pytest.raises((ValueError, UnicodeDecodeError)):
                    validate_markdown_file(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_file_invalid_line_endings(self):
        """Test that validate_markdown_file fails with CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file with CRLF line endings
                content = "# Title\r\n\r\nFirst sentence. Second sentence.\r\n"
                Path(FILENAME).write_bytes(content.encode("utf-8"))
                with pytest.raises(ValueError, match="CRLF"):
                    validate_markdown_file(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_file_file_too_small(self):
        """Test that validate_markdown_file fails when file size is too small."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create a valid markdown file with proper structure but too small (< 250 bytes)
                # This must have H1 heading, blank line, and 2-3 sentences to pass earlier checks
                content = "# Title\n\nA. B.\n"
                Path(FILENAME).write_text(content, encoding="utf-8")
                with pytest.raises(ValueError, match="below minimum"):
                    validate_markdown_file(FILENAME)
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_file_calls_all_checks_in_order(self):
        """Test that validate_markdown_file calls all validation checks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create a valid markdown file
                create_markdown_file()
                # Call validate_markdown_file which should call all checks
                # If any check fails, exception will be raised
                validate_markdown_file(FILENAME)
                # If we reach here, all checks passed
                assert True
            finally:
                import os

                os.chdir(original_cwd)


class TestGitAddFile:
    """Tests for git_add_file git operation function."""

    @patch("subprocess.run")
    def test_git_add_file_calls_subprocess(self, mock_run):
        """Test that git_add_file calls subprocess.run with correct arguments."""
        git_add_file(FILENAME)
        mock_run.assert_called_once_with(
            ["git", "add", FILENAME],
            check=True,
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_git_add_file_uses_default_filename(self, mock_run):
        """Test that git_add_file uses FILENAME as default parameter."""
        git_add_file()
        mock_run.assert_called_once_with(
            ["git", "add", FILENAME],
            check=True,
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_git_add_file_raises_on_git_failure(self, mock_run):
        """Test that git_add_file raises CalledProcessError when git add fails."""
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "add"], stderr="fatal: not a git repository"
        )
        with pytest.raises(subprocess.CalledProcessError):
            git_add_file(FILENAME)

    @patch("subprocess.run")
    def test_git_add_file_with_custom_filename(self, mock_run):
        """Test that git_add_file accepts custom filename parameter."""
        custom_file = "custom_file.md"
        git_add_file(custom_file)
        mock_run.assert_called_once_with(
            ["git", "add", custom_file],
            check=True,
            capture_output=True,
            text=True,
        )


class TestGitCommit:
    """Tests for git_commit git operation function."""

    @patch("subprocess.run")
    def test_git_commit_calls_subprocess(self, mock_run):
        """Test that git_commit calls subprocess.run with correct arguments."""
        git_commit(COMMIT_MESSAGE)
        mock_run.assert_called_once_with(
            ["git", "commit", "-m", COMMIT_MESSAGE],
            check=True,
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_git_commit_uses_default_message(self, mock_run):
        """Test that git_commit uses COMMIT_MESSAGE as default parameter."""
        git_commit()
        mock_run.assert_called_once_with(
            ["git", "commit", "-m", COMMIT_MESSAGE],
            check=True,
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_git_commit_raises_on_git_failure(self, mock_run):
        """Test that git_commit raises CalledProcessError when git commit fails."""
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "commit"], stderr="fatal: not a git repository"
        )
        with pytest.raises(subprocess.CalledProcessError):
            git_commit(COMMIT_MESSAGE)

    @patch("subprocess.run")
    def test_git_commit_with_custom_message(self, mock_run):
        """Test that git_commit accepts custom commit message parameter."""
        custom_message = "Custom commit message"
        git_commit(custom_message)
        mock_run.assert_called_once_with(
            ["git", "commit", "-m", custom_message],
            check=True,
            capture_output=True,
            text=True,
        )


class TestGitPush:
    """Tests for git_push git operation function."""

    @patch("subprocess.run")
    def test_git_push_calls_subprocess(self, mock_run):
        """Test that git_push calls subprocess.run with correct arguments."""
        git_push(BRANCH_NAME)
        mock_run.assert_called_once_with(
            ["git", "push", "-u", "origin", BRANCH_NAME],
            check=True,
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_git_push_uses_default_branch(self, mock_run):
        """Test that git_push uses BRANCH_NAME as default parameter."""
        git_push()
        mock_run.assert_called_once_with(
            ["git", "push", "-u", "origin", BRANCH_NAME],
            check=True,
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_git_push_raises_on_git_failure(self, mock_run):
        """Test that git_push raises CalledProcessError when git push fails."""
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "push"], stderr="fatal: Authentication failed"
        )
        with pytest.raises(subprocess.CalledProcessError):
            git_push(BRANCH_NAME)

    @patch("subprocess.run")
    def test_git_push_with_custom_branch(self, mock_run):
        """Test that git_push accepts custom branch name parameter."""
        custom_branch = "custom/branch-name"
        git_push(custom_branch)
        mock_run.assert_called_once_with(
            ["git", "push", "-u", "origin", custom_branch],
            check=True,
            capture_output=True,
            text=True,
        )


class TestMain:
    """Tests for main orchestration function."""

    def test_main_success_returns_zero(self):
        """Test that main returns 0 on successful execution."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with patch("subprocess.run"):
                    result = main()
                    assert result == 0
            finally:
                import os

                os.chdir(original_cwd)

    def test_main_creates_and_validates_file(self):
        """Test that main creates and validates the markdown file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with patch("subprocess.run"):
                    main()
                    # Verify file was created
                    assert Path(FILENAME).exists()
                    # Verify it contains expected content
                    content = Path(FILENAME).read_text()
                    assert TITLE_TEXT in content
                    assert PROSE_CONTENT in content
            finally:
                import os

                os.chdir(original_cwd)

    def test_main_calls_git_operations(self):
        """Test that main calls all git operations in sequence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with patch("subprocess.run") as mock_run:
                    main()
                    # Verify git operations were called
                    # Should have 3 git calls: add, commit, push
                    assert mock_run.call_count == 3
                    # Verify the calls were made in order: add, commit, push
                    calls = mock_run.call_args_list
                    assert calls[0][0][0] == ["git", "add", FILENAME]
                    assert calls[1][0][0][0:3] == ["git", "commit", "-m"]
                    assert calls[2][0][0] == ["git", "push", "-u", "origin", BRANCH_NAME]
            finally:
                import os

                os.chdir(original_cwd)

    def test_main_fails_on_file_not_found(self):
        """Test that main returns 1 when file creation fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with patch(
                    "sheep.features.feature_207_markdown_file_creation.create_markdown_file",
                    side_effect=FileNotFoundError("File creation failed"),
                ):
                    result = main()
                    assert result == 1
            finally:
                import os

                os.chdir(original_cwd)

    def test_main_fails_on_validation_error(self):
        """Test that main returns 1 when validation fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with patch(
                    "sheep.features.feature_207_markdown_file_creation.validate_markdown_file",
                    side_effect=ValueError("Validation failed"),
                ):
                    result = main()
                    assert result == 1
            finally:
                import os

                os.chdir(original_cwd)

    def test_main_fails_on_git_error(self):
        """Test that main returns 1 when git operations fail."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, ["git"])):
                    result = main()
                    assert result == 1
            finally:
                import os

                os.chdir(original_cwd)
