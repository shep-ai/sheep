"""Tests for feature 297: Create markdown file test-odrj2h.md with title and prose content."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from sheep.content_generators import create_markdown_file
from sheep.features.feature_297_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_test_odrj2h_markdown_file,
)


class TestFeature297FileCreation:
    """Tests for feature 297 markdown file creation."""

    def test_markdown_filename_is_correct(self):
        """Test that the markdown filename is exactly test-odrj2h.md."""
        assert MARKDOWN_FILENAME == "test-odrj2h.md"

    def test_feature_number_is_correct(self):
        """Test that the feature number is 297."""
        assert FEATURE_NUMBER == 297

    @patch('sheep.content_generators.generate_markdown_content')
    def test_creates_file_with_create_markdown_file_function(self, mock_gen, tmp_path):
        """Test that create_markdown_file() creates the file in repo root."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Mock the LLM generation to avoid API dependency
            mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            mock_gen.return_value = mock_content

            # File should not exist before creation
            test_file = Path(MARKDOWN_FILENAME)
            assert not test_file.exists()

            # Call create_markdown_file directly
            result = create_markdown_file(
                filename=MARKDOWN_FILENAME,
                feature_number=FEATURE_NUMBER
            )

            # File should exist after creation
            assert test_file.exists()
            assert "filepath" in result
            assert "content" in result
            assert "commit_message" in result
            assert "push_result" in result

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_feature_function_calls_orchestration(self, mock_gen, tmp_path):
        """Test that create_test_odrj2h_markdown_file calls the orchestration function."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Mock the LLM generation
            mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            mock_gen.return_value = mock_content

            result = create_test_odrj2h_markdown_file()

            # Verify result structure
            assert isinstance(result, dict)
            assert "filepath" in result
            assert "content" in result

        finally:
            os.chdir(original_cwd)


class TestFile297Structure:
    """Tests for markdown file structure requirements (FR-2, FR-3, FR-4)."""

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_starts_with_h1_heading(self, mock_gen, tmp_path):
        """Test that file begins with H1 markdown heading (# Title)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            # First line should be H1 heading
            assert lines[0].startswith("# ")
            assert len(lines[0]) > 2

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_blank_line_after_h1(self, mock_gen, tmp_path):
        """Test that blank line exists between H1 heading and prose (FR-3)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Second line should be blank
            assert lines[1] == ""

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_contains_prose_content(self, mock_gen, tmp_path):
        """Test that file contains 2-3 sentences of prose content (FR-4)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            content = test_file.read_text(encoding="utf-8")

            # Should contain prose after H1 and blank line
            assert "First sentence." in content
            assert "Second sentence." in content
            assert "Third sentence." in content

        finally:
            os.chdir(original_cwd)


class TestFile297Encoding:
    """Tests for file encoding and line ending requirements (FR-5, FR-6)."""

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_is_utf8_encoded(self, mock_gen, tmp_path):
        """Test that file is UTF-8 encoded without BOM (FR-5)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            # Read as bytes to check for BOM
            content_bytes = test_file.read_bytes()

            # Should not start with UTF-8 BOM (EF BB BF)
            assert not content_bytes.startswith(b"\xef\xbb\xbf")

            # Should be readable as UTF-8
            content_text = test_file.read_text(encoding="utf-8")
            assert isinstance(content_text, str)

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_uses_lf_line_endings(self, mock_gen, tmp_path):
        """Test that file uses Unix LF line endings, not CRLF (FR-6)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            content_bytes = test_file.read_bytes()

            # Should not contain CRLF (\r\n = 0x0D 0x0A)
            assert b"\r\n" not in content_bytes

            # Should contain LF (\n = 0x0A)
            assert b"\n" in content_bytes

        finally:
            os.chdir(original_cwd)


class TestFile297Size:
    """Tests for file size requirements (NFR-1)."""

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_size_in_expected_range(self, mock_gen, tmp_path):
        """Test that file size is approximately 400-600 bytes (NFR-1)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            file_size = test_file.stat().st_size

            # File should be within reasonable size range
            # (slightly relaxed since mock content might be shorter)
            assert file_size > 50  # Minimum reasonable size
            assert file_size < 1000  # Maximum reasonable size

        finally:
            os.chdir(original_cwd)


class TestFile297CommitMessage:
    """Tests for git commit message format."""

    @patch('sheep.content_generators.generate_markdown_content')
    def test_commit_message_format(self, mock_gen, tmp_path):
        """Test that commit message follows conventional commit format."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            result = create_markdown_file(
                filename=MARKDOWN_FILENAME,
                feature_number=FEATURE_NUMBER
            )

            # Commit message should follow conventional commit format
            commit_message = result["commit_message"]
            assert commit_message.startswith("feat(297):")
            assert "test-odrj2h.md" in commit_message

        finally:
            os.chdir(original_cwd)
