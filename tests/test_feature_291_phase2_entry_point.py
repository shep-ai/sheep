"""Tests for feature 291 phase 2: Implementation Entry Point.

Tests for the entry point function that orchestrates the creation of
markdown file test-6sw4o8.md with H1 heading and prose content.
"""

from unittest.mock import patch

import pytest


class TestFeature291EntryPoint:
    """Tests for feature 291 entry point function."""

    def test_entry_point_function_exists(self):
        """Test that the entry point function exists and is importable."""
        # Import the function
        from feature_291_entry import create_feature_291_markdown

        # Verify it's callable
        assert callable(create_feature_291_markdown)

    def test_entry_point_no_required_parameters(self):
        """Test that entry point function requires no parameters."""
        # Get function signature
        import inspect

        from feature_291_entry import create_feature_291_markdown
        sig = inspect.signature(create_feature_291_markdown)

        # All parameters should be optional (have defaults)
        for param in sig.parameters.values():
            assert param.default != inspect.Parameter.empty or param.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD
            ), f"Parameter {param.name} has no default value"

    def test_entry_point_has_docstring(self):
        """Test that entry point function has a docstring."""
        from feature_291_entry import create_feature_291_markdown

        assert create_feature_291_markdown.__doc__ is not None
        assert len(create_feature_291_markdown.__doc__) > 0

    @patch('feature_291_entry.create_markdown_file')
    def test_entry_point_calls_orchestration_function(self, mock_create):
        """Test that entry point calls create_markdown_file with correct parameters."""
        from feature_291_entry import create_feature_291_markdown

        # Mock return value
        mock_return = {
            'filepath': '/tmp/test-6sw4o8.md',
            'content': '# Title\n\nContent here.',
            'commit_message': 'feat(291): create markdown file test-6sw4o8.md with prose content',
            'push_result': 'success'
        }
        mock_create.return_value = mock_return

        # Call the entry point
        result = create_feature_291_markdown()

        # Verify orchestration function was called with correct parameters
        mock_create.assert_called_once()
        call_args = mock_create.call_args

        # Check that filename is correct
        assert call_args[1]['filename'] == 'test-6sw4o8.md'

        # Check that feature_number is correct
        assert call_args[1]['feature_number'] == 291

    @patch('feature_291_entry.create_markdown_file')
    def test_entry_point_returns_result_dict(self, mock_create):
        """Test that entry point returns the result dictionary from orchestration function."""
        from feature_291_entry import create_feature_291_markdown

        # Mock return value
        mock_return = {
            'filepath': '/tmp/test-6sw4o8.md',
            'content': '# Title\n\nContent here.',
            'commit_message': 'feat(291): create markdown file test-6sw4o8.md with prose content',
            'push_result': 'success'
        }
        mock_create.return_value = mock_return

        # Call the entry point
        result = create_feature_291_markdown()

        # Verify the result is the expected dictionary
        assert result is mock_return
        assert 'filepath' in result
        assert 'content' in result
        assert 'commit_message' in result
        assert 'push_result' in result

    @patch('feature_291_entry.create_markdown_file')
    def test_entry_point_result_is_not_none(self, mock_create):
        """Test that entry point returns a non-None result."""
        from feature_291_entry import create_feature_291_markdown

        # Mock return value
        mock_return = {
            'filepath': '/tmp/test-6sw4o8.md',
            'content': '# Test Title\n\nTest content with multiple sentences.',
            'commit_message': 'feat(291): create markdown file test-6sw4o8.md with prose content',
            'push_result': 'success'
        }
        mock_create.return_value = mock_return

        # Call the entry point
        result = create_feature_291_markdown()

        # Verify result is not None
        assert result is not None
        assert isinstance(result, dict)

    @patch('feature_291_entry.create_markdown_file')
    def test_entry_point_filename_is_test_6sw4o8_md(self, mock_create):
        """Test that entry point uses exact filename test-6sw4o8.md."""
        from feature_291_entry import create_feature_291_markdown

        mock_create.return_value = {}

        create_feature_291_markdown()

        # Get the call arguments
        call_kwargs = mock_create.call_args[1]
        assert call_kwargs['filename'] == 'test-6sw4o8.md'

    @patch('feature_291_entry.create_markdown_file')
    def test_entry_point_feature_number_is_291(self, mock_create):
        """Test that entry point uses feature number 291."""
        from feature_291_entry import create_feature_291_markdown

        mock_create.return_value = {}

        create_feature_291_markdown()

        # Get the call arguments
        call_kwargs = mock_create.call_args[1]
        assert call_kwargs['feature_number'] == 291


class TestFeature291EntryPointIntegration:
    """Integration tests for feature 291 entry point (with mocked orchestration)."""

    @patch('feature_291_entry.create_markdown_file')
    def test_entry_point_propagates_success(self, mock_create):
        """Test that entry point successfully propagates orchestration result."""
        from feature_291_entry import create_feature_291_markdown

        mock_return = {
            'filepath': '/tmp/test-6sw4o8.md',
            'content': '# Example Title\n\nThis is sentence one. This is sentence two. This is sentence three.\n',
            'commit_message': 'feat(291): create markdown file test-6sw4o8.md with prose content',
            'push_result': 'Successfully pushed to origin'
        }
        mock_create.return_value = mock_return

        result = create_feature_291_markdown()

        # Verify all expected keys are in result
        assert result['filepath'] == '/tmp/test-6sw4o8.md'
        assert result['content'].startswith('# ')
        assert 'feat(291)' in result['commit_message']
        assert result['push_result'] is not None

    @patch('feature_291_entry.create_markdown_file')
    def test_entry_point_exception_handling(self, mock_create):
        """Test that entry point allows exceptions from orchestration to propagate."""
        from feature_291_entry import create_feature_291_markdown

        # Make the orchestration function raise an exception
        mock_create.side_effect = ValueError("Test error")

        # Verify exception is raised
        with pytest.raises(ValueError, match="Test error"):
            create_feature_291_markdown()
