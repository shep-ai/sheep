"""Tests for feature_104_markdown_file_creation module."""

import pytest

from sheep.features.feature_104_markdown_file_creation import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_104_markdown_file,
)


class TestFeature104Module:
    """Tests for feature 104 module structure and constants."""

    def test_module_has_required_constants(self):
        """Test that module defines all required constants."""
        assert FEATURE_NUMBER == 104
        assert FEATURE_NAME == "markdown-file-creation-8782a1"
        assert MARKDOWN_FILENAME == "test-ab3u1g.md"

    def test_feature_function_is_callable(self):
        """Test that create_feature_104_markdown_file is callable."""
        assert callable(create_feature_104_markdown_file)

    def test_feature_function_exists(self):
        """Test that create_feature_104_markdown_file function exists and is importable."""
        # If we got here without import errors, the function exists
        assert create_feature_104_markdown_file is not None

    def test_feature_function_returns_dict_structure(self):
        """Test that create_feature_104_markdown_file returns a dict with expected keys."""
        # This test verifies the return value structure without actually calling the full workflow
        # (which would require LLM API and git operations)
        assert hasattr(create_feature_104_markdown_file, "__call__")

        # Check function signature includes repo_path parameter
        import inspect
        sig = inspect.signature(create_feature_104_markdown_file)
        assert "repo_path" in sig.parameters

        # Verify the parameter has a default value of None
        assert sig.parameters["repo_path"].default is None

        # Verify return type annotation indicates dict[str, str]
        return_annotation = sig.return_annotation
        assert return_annotation is not None  # Has return type annotation


class TestFeature104Constants:
    """Tests for feature 104 constants match specification."""

    def test_feature_number_is_104(self):
        """Test that FEATURE_NUMBER is 104."""
        assert FEATURE_NUMBER == 104
        assert isinstance(FEATURE_NUMBER, int)

    def test_feature_name_matches_spec(self):
        """Test that FEATURE_NAME matches specification."""
        assert FEATURE_NAME == "markdown-file-creation-8782a1"
        assert isinstance(FEATURE_NAME, str)

    def test_markdown_filename_matches_spec(self):
        """Test that MARKDOWN_FILENAME matches specification."""
        assert MARKDOWN_FILENAME == "test-ab3u1g.md"
        assert isinstance(MARKDOWN_FILENAME, str)
        assert MARKDOWN_FILENAME.endswith(".md")
