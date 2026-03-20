"""Tests for feature 133: markdown file creation.

Tests cover the main tasks:
- Generate markdown content via LLM
- Write markdown file to disk
- Validate markdown file format
- Stage and commit file with git
- Push file to remote
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from sheep.content_generators import (
    generate_markdown_content,
    validate_markdown_file,
    write_markdown_file,
)
from sheep.features.feature_133_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_133_markdown_file,
)


class TestFeature133ModuleExists:
    """Tests for module structure and constants."""

    def test_feature_133_module_exists(self):
        """Test that feature 133 module can be imported."""
        from sheep.features import feature_133_markdown_file_creation

        assert feature_133_markdown_file_creation is not None

    def test_feature_number_constant_defined(self):
        """Test that FEATURE_NUMBER constant is defined and has correct value."""
        assert FEATURE_NUMBER == 133, "FEATURE_NUMBER must be 133"

    def test_markdown_filename_constant_defined(self):
        """Test that MARKDOWN_FILENAME constant is defined and has correct value."""
        assert (
            MARKDOWN_FILENAME == "test-mdvgli.md"
        ), "MARKDOWN_FILENAME must be 'test-mdvgli.md'"

    def test_create_function_exists(self):
        """Test that create_feature_133_markdown_file function exists."""
        assert callable(create_feature_133_markdown_file), (
            "create_feature_133_markdown_file must be callable"
        )


class TestFeature133Integration:
    """Integration tests for the complete feature 133 workflow."""

    def test_create_feature_133_returns_expected_structure(self):
        """Test that create_feature_133_markdown_file returns expected dictionary structure."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        assert isinstance(result, dict), "Result must be a dictionary"
        assert "filepath" in result, "Result must contain 'filepath'"
        assert "content" in result, "Result must contain 'content'"
        assert "commit_message" in result, "Result must contain 'commit_message'"
        assert "push_result" in result, "Result must contain 'push_result'"

        # Verify the commit message format
        assert f"feat({FEATURE_NUMBER})" in result["commit_message"], (
            "Commit message must include feature number"
        )
        assert MARKDOWN_FILENAME in result["commit_message"], (
            "Commit message must include filename"
        )

    def test_create_feature_133_exact_commit_message(self):
        """Test that the commit message follows the exact required format."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        expected_message = f"feat({FEATURE_NUMBER}): Create markdown file {MARKDOWN_FILENAME}"
        assert result["commit_message"] == expected_message, (
            f"Commit message must be exactly: {expected_message}"
        )

    def test_create_feature_133_file_exists_and_is_valid(self):
        """Test that created file exists and passes validation."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        filepath = result["filepath"]

        assert Path(filepath).exists(), f"File should exist at {filepath}"
        assert validate_markdown_file(filepath) is True, "File should pass validation"

    def test_create_feature_133_correct_filename(self):
        """Test that created file has the correct filename."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        filepath = Path(result["filepath"])

        assert filepath.name == MARKDOWN_FILENAME, (
            f"Filename must be {MARKDOWN_FILENAME}"
        )

    def test_create_feature_133_file_is_utf8_without_bom(self):
        """Test that created file is UTF-8 encoded without BOM."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        filepath = result["filepath"]

        with open(filepath, "rb") as f:
            binary_content = f.read()

        # Should not have UTF-8 BOM
        assert not binary_content.startswith(
            b"\xef\xbb\xbf"
        ), "File should not have UTF-8 BOM"

        # Should be valid UTF-8
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("File is not valid UTF-8")

    def test_create_feature_133_file_has_lf_line_endings(self):
        """Test that created file uses LF line endings (not CRLF)."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        filepath = result["filepath"]

        with open(filepath, "rb") as f:
            binary_content = f.read()

        # Should not contain CRLF
        assert b"\r\n" not in binary_content, (
            "File should use LF line endings, not CRLF"
        )

        # Should contain LF
        assert b"\n" in binary_content, "File should contain LF line endings"
