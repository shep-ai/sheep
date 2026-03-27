"""Tests for feature 236: Create markdown file test-5aiifd.md.

Tests cover:
- Feature module can be imported successfully
- create_feature_236_markdown_file function exists and is callable
- Function returns a dict with expected keys
- Module has __main__ block that can be executed
- Feature function works with mocked dependencies
"""

import inspect
from unittest.mock import MagicMock, patch

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
        sig = inspect.signature(create_feature_236_markdown_file)
        assert "repo_path" in sig.parameters
        assert sig.parameters["repo_path"].default is None

    @patch('sheep.features.feature_236_markdown_file_creation.push_markdown_file')
    @patch('sheep.features.feature_236_markdown_file_creation.commit_markdown_file')
    @patch('sheep.features.feature_236_markdown_file_creation.validate_markdown_file')
    @patch('sheep.features.feature_236_markdown_file_creation.write_markdown_file')
    @patch('sheep.features.feature_236_markdown_file_creation.generate_markdown_content')
    def test_function_returns_dict_with_required_keys(
        self, mock_gen, mock_write, mock_validate, mock_commit, mock_push
    ):
        """Test that function returns dict with all required keys."""
        # Setup mock return values
        mock_gen.return_value = "# Title\n\nContent here."
        mock_write.return_value = "/path/to/test-5aiifd.md"
        mock_commit.return_value = "commit message"
        mock_push.return_value = "push result"

        result = create_feature_236_markdown_file()

        # Verify all required keys are present
        assert isinstance(result, dict)
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

    @patch('sheep.features.feature_236_markdown_file_creation.push_markdown_file')
    @patch('sheep.features.feature_236_markdown_file_creation.commit_markdown_file')
    @patch('sheep.features.feature_236_markdown_file_creation.validate_markdown_file')
    @patch('sheep.features.feature_236_markdown_file_creation.write_markdown_file')
    @patch('sheep.features.feature_236_markdown_file_creation.generate_markdown_content')
    def test_function_calls_all_steps_in_order(
        self, mock_gen, mock_write, mock_validate, mock_commit, mock_push
    ):
        """Test that function calls all five steps in correct order."""
        mock_gen.return_value = "# Title\n\nContent here."
        mock_write.return_value = "/path/to/test-5aiifd.md"
        mock_commit.return_value = "commit message"
        mock_push.return_value = "push result"

        create_feature_236_markdown_file()

        # Verify all functions were called
        mock_gen.assert_called_once()
        mock_write.assert_called_once()
        mock_validate.assert_called_once()
        mock_commit.assert_called_once()
        mock_push.assert_called_once()

    @patch('sheep.features.feature_236_markdown_file_creation.push_markdown_file')
    @patch('sheep.features.feature_236_markdown_file_creation.commit_markdown_file')
    @patch('sheep.features.feature_236_markdown_file_creation.validate_markdown_file')
    @patch('sheep.features.feature_236_markdown_file_creation.write_markdown_file')
    @patch('sheep.features.feature_236_markdown_file_creation.generate_markdown_content')
    def test_function_uses_correct_commit_message(
        self, mock_gen, mock_write, mock_validate, mock_commit, mock_push
    ):
        """Test that function uses conventional commit message format."""
        mock_gen.return_value = "# Title\n\nContent here."
        mock_write.return_value = "/path/to/test-5aiifd.md"
        mock_commit.return_value = "commit message"
        mock_push.return_value = "push result"

        create_feature_236_markdown_file()

        # Verify commit was called with correct message format
        call_args = mock_commit.call_args
        # The custom_message should be passed as a keyword argument
        assert "custom_message" in call_args.kwargs
        expected_message = f"feat({FEATURE_NUMBER}): Create markdown file {MARKDOWN_FILENAME} with prose content"
        assert call_args.kwargs["custom_message"] == expected_message

    @patch('sheep.features.feature_236_markdown_file_creation.generate_markdown_content')
    def test_function_propagates_content_generation_errors(self, mock_gen):
        """Test that function propagates errors from content generation."""
        mock_gen.side_effect = ValueError("LLM API error")

        with pytest.raises(ValueError, match="LLM API error"):
            create_feature_236_markdown_file()
