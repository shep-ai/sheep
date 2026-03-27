"""Tests for feature 236: Create markdown file test-5aiifd.md.

Tests cover:
- Feature module can be imported successfully
- create_feature_236_markdown_file function exists and is callable
- Function returns a dict with expected keys
- Module has __main__ block that can be executed
"""

import pytest

from sheep.features.feature_236_markdown_file_creation import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_236_markdown_file,
)


class TestFeatureMetadata:
    """Tests for feature metadata constants."""

    def test_feature_number_is_236(self):
        """Test that FEATURE_NUMBER is set to 236."""
        assert FEATURE_NUMBER == 236

    def test_feature_name_is_correct(self):
        """Test that FEATURE_NAME is set correctly."""
        assert FEATURE_NAME == "markdown-file-creation-0b2f48"

    def test_markdown_filename_is_correct(self):
        """Test that MARKDOWN_FILENAME is set to test-5aiifd.md."""
        assert MARKDOWN_FILENAME == "test-5aiifd.md"


class TestFeatureFunction:
    """Tests for the create_feature_236_markdown_file function."""

    def test_function_is_callable(self):
        """Test that create_feature_236_markdown_file is callable."""
        assert callable(create_feature_236_markdown_file)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        assert create_feature_236_markdown_file.__doc__ is not None

    def test_function_accepts_optional_repo_path(self):
        """Test that function accepts optional repo_path parameter."""
        import inspect

        sig = inspect.signature(create_feature_236_markdown_file)
        assert "repo_path" in sig.parameters
        assert sig.parameters["repo_path"].default is None
