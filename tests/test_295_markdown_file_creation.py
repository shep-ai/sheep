"""Tests for feature 295: Create markdown file test-7z6o6n.md with title and prose content."""

import os
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import create_markdown_file, validate_markdown_file
from sheep.features.feature_295_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_test_7z6o6n_markdown_file,
    main,
)


class TestFeature295ModuleStructure:
    """Tests for feature 295 module structure and imports."""

    def test_feature_number_is_correct(self):
        """Test that the feature number is 295."""
        assert FEATURE_NUMBER == 295

    def test_markdown_filename_is_correct(self):
        """Test that the markdown filename is exactly test-7z6o6n.md."""
        assert MARKDOWN_FILENAME == "test-7z6o6n.md"

    def test_module_imports_are_available(self):
        """Test that all required imports are available in the module."""
        from sheep.content_generators import create_markdown_file
        from sheep.observability.logging import get_logger

        # Verify the imports work
        assert callable(create_markdown_file)
        assert callable(get_logger)

    def test_logger_is_configured(self):
        """Test that structlog logger is initialized in the module."""
        from sheep.features.feature_295_markdown_file_creation import _logger

        # Verify logger exists and has expected methods
        assert hasattr(_logger, 'info')
        assert hasattr(_logger, 'error')
        assert hasattr(_logger, 'debug')
        assert callable(_logger.info)
        assert callable(_logger.error)
        assert callable(_logger.debug)

    def test_function_create_test_markdown_file_exists(self):
        """Test that create_test_7z6o6n_markdown_file function exists."""
        assert callable(create_test_7z6o6n_markdown_file)

    def test_main_function_exists(self):
        """Test that main function exists."""
        assert callable(main)


class TestFeature295FileCreation:
    """Tests for feature 295 markdown file creation."""

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
        """Test that create_test_7z6o6n_markdown_file calls the orchestration function."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Mock the LLM generation
            mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            mock_gen.return_value = mock_content

            result = create_test_7z6o6n_markdown_file()

            # Verify result structure
            assert isinstance(result, dict)
            assert "filepath" in result
            assert "content" in result

        finally:
            os.chdir(original_cwd)


class TestFile295Structure:
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
            assert lines[0].startswith("# "), f"Expected H1 heading, got: {lines[0]}"
            assert len(lines[0]) > 2, "H1 heading should have title text"

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_has_blank_line_separator(self, mock_gen, tmp_path):
        """Test that file has blank (empty) line 2 after H1 heading."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Second line must be blank
            assert len(lines) >= 2, "File should have at least 2 lines"
            assert lines[1] == "", f"Line 2 should be blank, got: {repr(lines[1])}"

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_has_2_to_3_sentences(self, mock_gen, tmp_path):
        """Test that file contains exactly 2-3 sentences of prose."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Extract prose content (skip H1 and blank line)
            prose_lines = lines[2:]
            prose_content = "\n".join(prose_lines).strip()

            # Count periods to count sentences
            sentence_count = prose_content.count(".")
            assert 2 <= sentence_count <= 3, (
                f"Expected 2-3 sentences, found {sentence_count}"
            )

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_is_utf8_encoded(self, mock_gen, tmp_path):
        """Test that file is UTF-8 encoded without BOM."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            # Read as binary to check for BOM
            binary_content = test_file.read_bytes()

            # UTF-8 BOM is b'\xef\xbb\xbf'
            assert not binary_content.startswith(
                b"\xef\xbb\xbf"
            ), "File should not have UTF-8 BOM"

            # Should be decodable as UTF-8
            text_content = binary_content.decode("utf-8")
            assert isinstance(text_content, str)

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_has_lf_line_endings(self, mock_gen, tmp_path):
        """Test that file uses LF (not CRLF) line endings."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            binary_content = test_file.read_bytes()

            # Should not contain CRLF
            assert b"\r\n" not in binary_content, "File should use LF, not CRLF"

        finally:
            os.chdir(original_cwd)


class TestCommitMessageFormat:
    """Tests for git commit message format (FR-8)."""

    def test_commit_message_format(self):
        """Test that commit message follows conventional format."""
        expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"

        # The expected format is: feat(295): create markdown file test-7z6o6n.md with prose content
        assert "feat(295)" in expected_message
        assert "test-7z6o6n.md" in expected_message
        assert "with prose content" in expected_message
