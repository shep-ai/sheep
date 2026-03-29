"""Tests for feature 267: Create markdown file test-leaw3w.md with prose content."""

import pytest

from sheep.features.feature_267_markdown_file_creation import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_267_markdown_file,
)


class TestFeature267Module:
    """Tests for feature 267 module structure and metadata."""

    def test_feature_number_is_267(self):
        """Test that FEATURE_NUMBER is 267."""
        assert FEATURE_NUMBER == 267

    def test_markdown_filename_is_correct(self):
        """Test that MARKDOWN_FILENAME is test-leaw3w.md."""
        assert MARKDOWN_FILENAME == "test-leaw3w.md"

    def test_feature_name_is_set(self):
        """Test that FEATURE_NAME is set."""
        assert FEATURE_NAME == "markdown-file-creation-e4197f"

    def test_create_function_exists(self):
        """Test that create_feature_267_markdown_file function exists."""
        assert callable(create_feature_267_markdown_file)

    def test_function_signature(self):
        """Test that create_feature_267_markdown_file has correct signature."""
        import inspect

        sig = inspect.signature(create_feature_267_markdown_file)
        # Function accepts repo_path parameter with default None
        assert "repo_path" in sig.parameters
        assert sig.parameters["repo_path"].default is None
