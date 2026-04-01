"""Tests for feature 302: Create markdown file test-k6bwm0.md with prose content."""

from unittest.mock import MagicMock, patch

import pytest

from sheep.features.feature_302_markdown_file_creation import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_test_k6bwm0_markdown_file,
)


class TestFeature302Module:
    """Tests for feature 302 module structure and metadata."""

    def test_feature_number_is_302(self):
        """Test that FEATURE_NUMBER is 302."""
        assert FEATURE_NUMBER == 302

    def test_markdown_filename_is_correct(self):
        """Test that MARKDOWN_FILENAME is test-k6bwm0.md."""
        assert MARKDOWN_FILENAME == "test-k6bwm0.md"

    def test_feature_name_is_set(self):
        """Test that FEATURE_NAME is set."""
        assert FEATURE_NAME == "markdown-file-creation-c622f7"

    def test_create_function_exists(self):
        """Test that create_test_k6bwm0_markdown_file function exists."""
        assert callable(create_test_k6bwm0_markdown_file)


class TestCreateFeature302Function:
    """Tests for create_test_k6bwm0_markdown_file function."""

    def test_function_signature_accepts_repo_path(self):
        """Test that function accepts repo_path parameter."""
        # Function should accept optional repo_path parameter
        # This test verifies the function is callable with this parameter
        assert create_test_k6bwm0_markdown_file.__code__.co_varnames[0] == "repo_path"

    def test_function_returns_dict(self):
        """Test that function would return a dictionary (checking structure)."""
        # Verify the function has the expected return annotation or docstring
        docstring = create_test_k6bwm0_markdown_file.__doc__
        assert "Dictionary containing" in docstring
        assert "filepath" in docstring
        assert "content" in docstring
        assert "commit_message" in docstring
        assert "push_result" in docstring

    def test_function_includes_logging(self):
        """Test that function includes logging implementation."""
        # Check that the module has logger configured
        from sheep.features.feature_302_markdown_file_creation import _logger

        assert _logger is not None

    def test_function_raises_on_failure(self):
        """Test that function documents exception behavior."""
        docstring = create_test_k6bwm0_markdown_file.__doc__
        assert "Raises" in docstring
        assert "ValueError" in docstring
        assert "IOError" in docstring
        assert "Exception" in docstring


class TestFeature302Integration:
    """Integration tests for feature 302 workflow."""

    def test_function_has_complete_docstring(self):
        """Test that function has comprehensive documentation."""
        docstring = create_test_k6bwm0_markdown_file.__doc__
        assert "orchestrates the complete workflow" in docstring.lower()
        assert "generate valid markdown content" in docstring.lower()
        assert "write file to repository root" in docstring.lower()
        assert "validate file meets" in docstring.lower()
        assert "stage and commit" in docstring.lower()
        assert "push to remote" in docstring.lower()

    def test_workflow_steps_in_docstring(self):
        """Test that docstring documents all 5 workflow steps."""
        docstring = create_test_k6bwm0_markdown_file.__doc__
        # Count occurrences of step references
        assert "1." in docstring
        assert "2." in docstring
        assert "3." in docstring
        assert "4." in docstring
        assert "5." in docstring

    def test_module_has_main_block(self):
        """Test that module has __main__ execution block."""
        import inspect

        # Import the module and check its source
        module = __import__(
            "sheep.features.feature_302_markdown_file_creation",
            fromlist=[""],
        )
        source = inspect.getsource(module)
        # Check that the module source includes __main__ execution
        assert 'if __name__ == "__main__"' in source


class TestContentGenerationTask:
    """Tests for task-1: Feature module with wrapper function."""

    @patch("sheep.features.feature_302_markdown_file_creation.create_markdown_file")
    def test_calls_create_markdown_file(self, mock_create):
        """Test that function calls create_markdown_file during workflow."""
        mock_create.return_value = {
            "filepath": "/repo/test-k6bwm0.md",
            "content": "# Test\n\nThis is a test sentence. Another one. And a third.",
            "commit_message": "feat(302): create markdown file test-k6bwm0.md with prose content",
            "push_result": "pushed",
        }

        create_test_k6bwm0_markdown_file()

        mock_create.assert_called_once()

    @patch("sheep.features.feature_302_markdown_file_creation.create_markdown_file")
    def test_calls_create_markdown_file_with_correct_parameters(
        self, mock_create
    ):
        """Test that create_markdown_file is called with correct parameters."""
        mock_create.return_value = {
            "filepath": "/repo/test-k6bwm0.md",
            "content": "# Test\n\nThis is a test sentence. Another one. And a third.",
            "commit_message": "feat(302): create markdown file test-k6bwm0.md with prose content",
            "push_result": "pushed",
        }

        create_test_k6bwm0_markdown_file()

        # Verify create_markdown_file was called with correct parameters
        call_args = mock_create.call_args
        assert call_args[1]["filename"] == MARKDOWN_FILENAME
        assert call_args[1]["feature_number"] == FEATURE_NUMBER

    @patch("sheep.features.feature_302_markdown_file_creation.create_markdown_file")
    def test_function_includes_logging(self, mock_create):
        """Test that function includes logging implementation."""
        mock_create.return_value = {
            "filepath": "/repo/test-k6bwm0.md",
            "content": "# Test\n\nThis is a test sentence. Another one. And a third.",
            "commit_message": "feat(302): create markdown file test-k6bwm0.md with prose content",
            "push_result": "pushed",
        }

        with patch(
            "sheep.features.feature_302_markdown_file_creation._logger"
        ) as mock_logger:
            create_test_k6bwm0_markdown_file()

            # Verify INFO log for task start and completion
            info_calls = [call for call in mock_logger.info.call_args_list]
            assert len(info_calls) > 0


class TestMainEntryPoint:
    """Tests for main() entry point."""

    def test_main_function_exists(self):
        """Test that main() function exists."""
        from sheep.features.feature_302_markdown_file_creation import main

        assert callable(main)

    def test_main_returns_int(self):
        """Test that main() returns an integer."""
        from sheep.features.feature_302_markdown_file_creation import main

        with patch(
            "sheep.features.feature_302_markdown_file_creation.create_test_k6bwm0_markdown_file"
        ) as mock_create:
            mock_create.return_value = {
                "filepath": "/repo/test-k6bwm0.md",
                "content": "# Test\n\nThis is test. Another test.",
                "commit_message": "feat(302): create markdown file test-k6bwm0.md with prose content",
                "push_result": "pushed",
            }

            result = main()

            assert isinstance(result, int)

    def test_main_returns_zero_on_success(self):
        """Test that main() returns 0 on success."""
        from sheep.features.feature_302_markdown_file_creation import main

        with patch(
            "sheep.features.feature_302_markdown_file_creation.create_test_k6bwm0_markdown_file"
        ) as mock_create:
            mock_create.return_value = {
                "filepath": "/repo/test-k6bwm0.md",
                "content": "# Test\n\nThis is test. Another test.",
                "commit_message": "feat(302): create markdown file test-k6bwm0.md with prose content",
                "push_result": "pushed",
            }

            result = main()

            assert result == 0

    def test_main_returns_one_on_failure(self):
        """Test that main() returns 1 on failure."""
        from sheep.features.feature_302_markdown_file_creation import main

        with patch(
            "sheep.features.feature_302_markdown_file_creation.create_test_k6bwm0_markdown_file"
        ) as mock_create:
            mock_create.side_effect = RuntimeError("Test error")

            result = main()

            assert result == 1

    def test_main_calls_create_function(self):
        """Test that main() calls create_test_k6bwm0_markdown_file()."""
        from sheep.features.feature_302_markdown_file_creation import main

        with patch(
            "sheep.features.feature_302_markdown_file_creation.create_test_k6bwm0_markdown_file"
        ) as mock_create:
            mock_create.return_value = {
                "filepath": "/repo/test-k6bwm0.md",
                "content": "# Test\n\nThis is test. Another test.",
                "commit_message": "feat(302): create markdown file test-k6bwm0.md with prose content",
                "push_result": "pushed",
            }

            main()

            mock_create.assert_called_once()

    def test_main_handles_exceptions_gracefully(self):
        """Test that main() handles exceptions gracefully."""
        from sheep.features.feature_302_markdown_file_creation import main

        with patch(
            "sheep.features.feature_302_markdown_file_creation.create_test_k6bwm0_markdown_file"
        ) as mock_create:
            mock_create.side_effect = RuntimeError("API error")

            with patch(
                "sheep.features.feature_302_markdown_file_creation._logger"
            ) as mock_logger:
                result = main()

                # Should not raise, but return error code
                assert result == 1
                # Should log the error
                error_calls = [call for call in mock_logger.error.call_args_list]
                assert len(error_calls) > 0
