"""Tests for feature 299: Create markdown file test-o2fx99.md with prose content."""

from unittest.mock import MagicMock, patch

import pytest

from sheep.features.feature_299_markdown_file_creation import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_test_o2fx99_markdown_file,
)


class TestFeature299Module:
    """Tests for feature 299 module structure and metadata."""

    def test_feature_number_is_299(self):
        """Test that FEATURE_NUMBER is 299."""
        assert FEATURE_NUMBER == 299

    def test_markdown_filename_is_correct(self):
        """Test that MARKDOWN_FILENAME is test-o2fx99.md."""
        assert MARKDOWN_FILENAME == "test-o2fx99.md"

    def test_feature_name_is_set(self):
        """Test that FEATURE_NAME is set."""
        assert FEATURE_NAME == "markdown-file-creation-1944c2"

    def test_create_function_exists(self):
        """Test that create_test_o2fx99_markdown_file function exists."""
        assert callable(create_test_o2fx99_markdown_file)


class TestCreateFeature299Function:
    """Tests for create_test_o2fx99_markdown_file function."""

    def test_function_signature_accepts_repo_path(self):
        """Test that function accepts repo_path parameter."""
        # Function should accept optional repo_path parameter
        # This test verifies the function is callable with this parameter
        assert create_test_o2fx99_markdown_file.__code__.co_varnames[0] == "repo_path"

    def test_function_returns_dict(self):
        """Test that function would return a dictionary (checking structure)."""
        # Verify the function has the expected return annotation or docstring
        docstring = create_test_o2fx99_markdown_file.__doc__
        assert "Dictionary containing" in docstring
        assert "filepath" in docstring
        assert "content" in docstring
        assert "commit_message" in docstring
        assert "push_result" in docstring

    def test_function_includes_logging(self):
        """Test that function includes logging implementation."""
        # Check that the module has logger configured
        from sheep.features.feature_299_markdown_file_creation import _logger

        assert _logger is not None

    def test_function_raises_on_failure(self):
        """Test that function documents exception behavior."""
        docstring = create_test_o2fx99_markdown_file.__doc__
        assert "Raises" in docstring
        assert "ValueError" in docstring
        assert "IOError" in docstring
        assert "Exception" in docstring


class TestFeature299Integration:
    """Integration tests for feature 299 workflow."""

    def test_function_has_complete_docstring(self):
        """Test that function has comprehensive documentation."""
        docstring = create_test_o2fx99_markdown_file.__doc__
        assert "orchestrates the complete workflow" in docstring.lower()
        assert "generate valid markdown content" in docstring.lower()
        assert "write file to repository root" in docstring.lower()
        assert "validate file meets" in docstring.lower()
        assert "stage and commit" in docstring.lower()
        assert "push to remote" in docstring.lower()

    def test_workflow_steps_in_docstring(self):
        """Test that docstring documents all 5 workflow steps."""
        docstring = create_test_o2fx99_markdown_file.__doc__
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
            "sheep.features.feature_299_markdown_file_creation",
            fromlist=[""],
        )
        source = inspect.getsource(module)
        # Check that the module source includes __main__ execution
        assert 'if __name__ == "__main__"' in source


class TestCreateMarkdownFileOrchestration:
    """Tests for feature 299 calling orchestration function."""

    @patch("sheep.features.feature_299_markdown_file_creation.create_markdown_file")
    def test_calls_create_markdown_file(self, mock_create):
        """Test that function calls create_markdown_file orchestration function."""
        mock_create.return_value = {
            "filepath": "/repo/test-o2fx99.md",
            "content": "# Test\n\nThis is a test sentence. Another one. And a third.",
            "commit_message": "feat(299): create markdown file test-o2fx99.md with prose content",
            "push_result": "pushed",
        }

        create_test_o2fx99_markdown_file()

        mock_create.assert_called_once()

    @patch("sheep.features.feature_299_markdown_file_creation.create_markdown_file")
    def test_passes_correct_parameters_to_create_markdown_file(self, mock_create):
        """Test that function passes correct parameters to create_markdown_file."""
        mock_create.return_value = {
            "filepath": "/repo/test-o2fx99.md",
            "content": "# Test\n\nThis is a test sentence. Another one. And a third.",
            "commit_message": "feat(299): create markdown file test-o2fx99.md with prose content",
            "push_result": "pushed",
        }

        import os
        test_repo = "/custom/repo"
        create_test_o2fx99_markdown_file(repo_path=test_repo)

        # Verify create_markdown_file was called with correct parameters
        call_args = mock_create.call_args
        assert call_args[1]["filename"] == MARKDOWN_FILENAME
        assert call_args[1]["repo_path"] == test_repo
        assert call_args[1]["feature_number"] == FEATURE_NUMBER

    @patch("sheep.features.feature_299_markdown_file_creation.create_markdown_file")
    def test_uses_current_directory_when_repo_path_not_provided(self, mock_create):
        """Test that function uses current directory when repo_path is None."""
        mock_create.return_value = {
            "filepath": "/repo/test-o2fx99.md",
            "content": "# Test\n\nThis is a test sentence. Another one. And a third.",
            "commit_message": "feat(299): create markdown file test-o2fx99.md with prose content",
            "push_result": "pushed",
        }

        create_test_o2fx99_markdown_file(repo_path=None)

        # Verify create_markdown_file was called with current directory
        call_args = mock_create.call_args
        repo_path = call_args[1]["repo_path"]
        assert repo_path is not None
        assert isinstance(repo_path, str)

    @patch("sheep.features.feature_299_markdown_file_creation.create_markdown_file")
    def test_returns_result_from_orchestration_function(self, mock_create):
        """Test that function returns result from create_markdown_file."""
        test_result = {
            "filepath": "/repo/test-o2fx99.md",
            "content": "# Test\n\nThis is a test sentence. Another one. And a third.",
            "commit_message": "feat(299): create markdown file test-o2fx99.md with prose content",
            "push_result": "pushed",
        }
        mock_create.return_value = test_result

        result = create_test_o2fx99_markdown_file()

        assert result == test_result
        assert result["filepath"] == test_result["filepath"]
        assert result["content"] == test_result["content"]
        assert result["commit_message"] == test_result["commit_message"]
        assert result["push_result"] == test_result["push_result"]

    @patch("sheep.features.feature_299_markdown_file_creation.create_markdown_file")
    @patch("sheep.features.feature_299_markdown_file_creation._logger")
    def test_logs_execution_start(self, mock_logger, mock_create):
        """Test that function logs when starting execution."""
        mock_create.return_value = {
            "filepath": "/repo/test-o2fx99.md",
            "content": "# Test\n\nSentence one. Sentence two. Sentence three.",
            "commit_message": "feat(299): create markdown file test-o2fx99.md with prose content",
            "push_result": "pushed",
        }

        create_test_o2fx99_markdown_file()

        # Verify INFO log at start
        info_calls = [call for call in mock_logger.info.call_args_list]
        assert len(info_calls) > 0
        # Should log about creating the feature
        assert any("299" in str(call) for call in info_calls)

    @patch("sheep.features.feature_299_markdown_file_creation.create_markdown_file")
    @patch("sheep.features.feature_299_markdown_file_creation._logger")
    def test_logs_successful_completion(self, mock_logger, mock_create):
        """Test that function logs successful completion."""
        mock_create.return_value = {
            "filepath": "/repo/test-o2fx99.md",
            "content": "# Test\n\nSentence one. Sentence two. Sentence three.",
            "commit_message": "feat(299): create markdown file test-o2fx99.md with prose content",
            "push_result": "pushed",
        }

        create_test_o2fx99_markdown_file()

        # Verify success log
        info_calls = [call for call in mock_logger.info.call_args_list]
        assert any("successfully" in str(call).lower() for call in info_calls)

    @patch("sheep.features.feature_299_markdown_file_creation.create_markdown_file")
    @patch("sheep.features.feature_299_markdown_file_creation._logger")
    def test_logs_error_on_failure(self, mock_logger, mock_create):
        """Test that function logs errors when create_markdown_file fails."""
        error_msg = "Test error message"
        mock_create.side_effect = RuntimeError(error_msg)

        with pytest.raises(RuntimeError):
            create_test_o2fx99_markdown_file()

        # Verify error log
        error_calls = [call for call in mock_logger.error.call_args_list]
        assert len(error_calls) > 0

    @patch("sheep.features.feature_299_markdown_file_creation.create_markdown_file")
    def test_propagates_exceptions(self, mock_create):
        """Test that function propagates exceptions from orchestration function."""
        mock_create.side_effect = ValueError("Invalid markdown content")

        with pytest.raises(ValueError):
            create_test_o2fx99_markdown_file()

    @patch("sheep.features.feature_299_markdown_file_creation.create_markdown_file")
    def test_handles_io_errors(self, mock_create):
        """Test that function propagates IOError from orchestration function."""
        mock_create.side_effect = IOError("File write failed")

        with pytest.raises(IOError):
            create_test_o2fx99_markdown_file()


class TestMainFunction:
    """Tests for main() entry point."""

    @patch("sheep.features.feature_299_markdown_file_creation.create_test_o2fx99_markdown_file")
    def test_main_returns_zero_on_success(self, mock_create_func):
        """Test that main() returns 0 on successful execution."""
        from sheep.features.feature_299_markdown_file_creation import main

        mock_create_func.return_value = {
            "filepath": "/repo/test-o2fx99.md",
            "content": "# Test\n\nSentence one. Sentence two. Sentence three.",
            "commit_message": "feat(299): create markdown file test-o2fx99.md with prose content",
            "push_result": "pushed",
        }

        with patch("builtins.print"):
            result = main()

        assert result == 0

    @patch("sheep.features.feature_299_markdown_file_creation.create_test_o2fx99_markdown_file")
    def test_main_returns_one_on_failure(self, mock_create_func):
        """Test that main() returns 1 on failure."""
        from sheep.features.feature_299_markdown_file_creation import main

        mock_create_func.side_effect = Exception("Test error")

        with patch("builtins.print"):
            result = main()

        assert result == 1

    @patch("sheep.features.feature_299_markdown_file_creation.create_test_o2fx99_markdown_file")
    def test_main_prints_results_on_success(self, mock_create_func):
        """Test that main() prints results when successful."""
        from sheep.features.feature_299_markdown_file_creation import main

        mock_create_func.return_value = {
            "filepath": "/repo/test-o2fx99.md",
            "content": "# Test\n\nSentence one. Sentence two. Sentence three.",
            "commit_message": "feat(299): create markdown file test-o2fx99.md with prose content",
            "push_result": "pushed",
        }

        with patch("builtins.print") as mock_print:
            main()

        # Verify output was printed
        assert mock_print.call_count > 0
        printed_text = str(mock_print.call_args_list)
        assert "299" in printed_text or "Feature 299" in printed_text

    @patch("sheep.features.feature_299_markdown_file_creation.create_test_o2fx99_markdown_file")
    def test_main_prints_error_on_failure(self, mock_create_func):
        """Test that main() prints error message on failure."""
        from sheep.features.feature_299_markdown_file_creation import main

        mock_create_func.side_effect = Exception("Test error")

        with patch("builtins.print") as mock_print:
            main()

        # Verify error output was printed
        assert mock_print.call_count > 0
        printed_text = str(mock_print.call_args_list)
        assert "Error" in printed_text or "Failed" in printed_text
