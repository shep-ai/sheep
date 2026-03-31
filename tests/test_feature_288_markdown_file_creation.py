"""Tests for feature 288: Create markdown file test-dx2xd7.md with prose content."""

from unittest.mock import MagicMock, patch

import pytest

from sheep.features.feature_288_markdown_file_creation import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_288_markdown_file,
)


class TestFeature288Module:
    """Tests for feature 288 module structure and metadata."""

    def test_feature_number_is_288(self):
        """Test that FEATURE_NUMBER is 288."""
        assert FEATURE_NUMBER == 288

    def test_markdown_filename_is_correct(self):
        """Test that MARKDOWN_FILENAME is test-dx2xd7.md."""
        assert MARKDOWN_FILENAME == "test-dx2xd7.md"

    def test_feature_name_is_set(self):
        """Test that FEATURE_NAME is set."""
        assert FEATURE_NAME == "markdown-file-creation"

    def test_create_function_exists(self):
        """Test that create_feature_288_markdown_file function exists."""
        assert callable(create_feature_288_markdown_file)


class TestCreateFeature288Function:
    """Tests for create_feature_288_markdown_file function."""

    def test_function_signature_accepts_repo_path(self):
        """Test that function accepts repo_path parameter."""
        # Function should accept optional repo_path parameter
        # This test verifies the function is callable with this parameter
        assert create_feature_288_markdown_file.__code__.co_varnames[0] == "repo_path"

    def test_function_returns_dict(self):
        """Test that function would return a dictionary (checking structure)."""
        # Verify the function has the expected return annotation or docstring
        docstring = create_feature_288_markdown_file.__doc__
        assert "Dictionary containing" in docstring
        assert "filepath" in docstring
        assert "content" in docstring
        assert "commit_message" in docstring
        assert "push_result" in docstring

    def test_function_includes_logging(self):
        """Test that function includes logging implementation."""
        # Check that the module has logger configured
        from sheep.features.feature_288_markdown_file_creation import _logger

        assert _logger is not None

    def test_function_raises_on_failure(self):
        """Test that function documents exception behavior."""
        docstring = create_feature_288_markdown_file.__doc__
        assert "Raises" in docstring
        assert "ValueError" in docstring
        assert "IOError" in docstring
        assert "Exception" in docstring


class TestFeature288Integration:
    """Integration tests for feature 288 workflow."""

    def test_function_has_complete_docstring(self):
        """Test that function has comprehensive documentation."""
        docstring = create_feature_288_markdown_file.__doc__
        assert "orchestrates the complete workflow" in docstring.lower()
        assert "generate valid markdown content" in docstring.lower()
        assert "write file to repository root" in docstring.lower()
        assert "validate file meets" in docstring.lower()
        assert "stage and commit" in docstring.lower()
        assert "push to remote" in docstring.lower()

    def test_workflow_steps_in_docstring(self):
        """Test that docstring documents all 5 workflow steps."""
        docstring = create_feature_288_markdown_file.__doc__
        # Count occurrences of step references
        assert "1." in docstring
        assert "2." in docstring
        assert "3." in docstring
        assert "4." in docstring
        assert "5." in docstring

    def test_imports_required_wrappers(self):
        """Test that module imports required wrapper functions."""
        from sheep.features.feature_288_markdown_file_creation import (
            generate_markdown_content,
            write_markdown_file,
            validate_markdown_file,
            commit_markdown_file,
            push_markdown_file,
        )

        # Verify all required wrappers are imported
        assert callable(generate_markdown_content)
        assert callable(write_markdown_file)
        assert callable(validate_markdown_file)
        assert callable(commit_markdown_file)
        assert callable(push_markdown_file)

    def test_module_has_main_block(self):
        """Test that module has __main__ execution block."""
        import inspect

        # Import the module and check its source
        module = __import__(
            "sheep.features.feature_288_markdown_file_creation",
            fromlist=[""],
        )
        source = inspect.getsource(module)
        # Check that the module source includes __main__ execution
        assert 'if __name__ == "__main__"' in source


class TestContentGenerationTask:
    """Tests for task-2: Content generation via Claude API."""

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_calls_generate_markdown_content(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that function calls generate_markdown_content during workflow."""
        mock_generate.return_value = "# Test\n\nThis is a test sentence. Another one. And a third."
        mock_write.return_value = "/repo/test-dx2xd7.md"
        mock_commit.return_value = "committed"
        mock_push.return_value = "pushed"

        create_feature_288_markdown_file()

        mock_generate.assert_called_once()

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_generated_content_is_available_for_next_steps(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that generated content is stored and available for subsequent steps."""
        test_content = "# Test\n\nThis is a test sentence. Another one. And a third."
        mock_generate.return_value = test_content
        mock_write.return_value = "/repo/test-dx2xd7.md"
        mock_commit.return_value = "committed"
        mock_push.return_value = "pushed"

        create_feature_288_markdown_file()

        # Verify that write_markdown_file was called with the generated content
        mock_write.assert_called_once()
        call_args = mock_write.call_args
        assert call_args[0][0] == test_content

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_logs_content_generation_at_appropriate_levels(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that function logs content generation at DEBUG and INFO levels."""
        mock_generate.return_value = "# Test\n\nThis is a test sentence. Another one. And a third."
        mock_write.return_value = "/repo/test-dx2xd7.md"
        mock_commit.return_value = "committed"
        mock_push.return_value = "pushed"

        with patch("sheep.features.feature_288_markdown_file_creation._logger") as mock_logger:
            create_feature_288_markdown_file()

            # Verify INFO log for task start and content generation completion
            info_calls = [call for call in mock_logger.info.call_args_list]
            debug_calls = [call for call in mock_logger.debug.call_args_list]

            # Should have INFO logs for task completion
            assert len(info_calls) > 0
            # Should have DEBUG logs for generated content details
            assert len(debug_calls) > 0

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_handles_api_errors_with_error_logging(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that API errors from content generation are logged at ERROR level."""
        mock_generate.side_effect = RuntimeError("API connection failed")

        with patch("sheep.features.feature_288_markdown_file_creation._logger") as mock_logger:
            with pytest.raises(RuntimeError):
                create_feature_288_markdown_file()

            # Verify ERROR log for failure
            error_calls = [call for call in mock_logger.error.call_args_list]
            assert len(error_calls) > 0


class TestFileCreationValidationTask:
    """Tests for task-3: File creation and validation."""

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_calls_write_markdown_file_with_correct_parameters(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that write_markdown_file is called with correct filename and content."""
        test_content = "# Test\n\nThis is a test sentence. Another one. And a third."
        mock_generate.return_value = test_content
        mock_write.return_value = "/repo/test-dx2xd7.md"
        mock_commit.return_value = "committed"
        mock_push.return_value = "pushed"

        create_feature_288_markdown_file()

        mock_write.assert_called_once_with(test_content, MARKDOWN_FILENAME)

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_calls_validate_markdown_file_after_write(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that validate_markdown_file is called after write with correct filepath."""
        test_content = "# Test\n\nThis is a test sentence. Another one. And a third."
        mock_filepath = "/repo/test-dx2xd7.md"
        mock_generate.return_value = test_content
        mock_write.return_value = mock_filepath
        mock_commit.return_value = "committed"
        mock_push.return_value = "pushed"

        create_feature_288_markdown_file()

        mock_validate.assert_called_once_with(mock_filepath)

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_fails_fast_on_validation_failure(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that function raises ValueError when validation fails."""
        mock_generate.return_value = "# Test\n\nThis is a test sentence. Another one. And a third."
        mock_write.return_value = "/repo/test-dx2xd7.md"
        mock_validate.side_effect = ValueError("Invalid markdown structure")
        mock_commit.return_value = "committed"
        mock_push.return_value = "pushed"

        with pytest.raises(ValueError):
            create_feature_288_markdown_file()

        # Verify commit was not called after validation failure
        mock_commit.assert_not_called()

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_logs_validation_failure_at_error_level(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that validation failures are logged at ERROR level."""
        mock_generate.return_value = "# Test\n\nThis is a test sentence. Another one. And a third."
        mock_write.return_value = "/repo/test-dx2xd7.md"
        mock_validate.side_effect = ValueError("Invalid markdown structure")

        with patch("sheep.features.feature_288_markdown_file_creation._logger") as mock_logger:
            with pytest.raises(ValueError):
                create_feature_288_markdown_file()

            # Verify ERROR log for validation failure
            error_calls = [call for call in mock_logger.error.call_args_list]
            assert len(error_calls) > 0


class TestGitCommitTask:
    """Tests for task-4: Git staging and commit."""

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_calls_commit_markdown_file(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that commit_markdown_file is called during workflow."""
        mock_generate.return_value = "# Test\n\nThis is a test sentence. Another one. And a third."
        mock_write.return_value = "/repo/test-dx2xd7.md"
        mock_commit.return_value = "committed"
        mock_push.return_value = "pushed"

        create_feature_288_markdown_file()

        mock_commit.assert_called_once()

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_uses_conventional_commit_message(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that commit uses conventional message format."""
        mock_generate.return_value = "# Test\n\nThis is a test sentence. Another one. And a third."
        mock_write.return_value = "/repo/test-dx2xd7.md"
        mock_commit.return_value = "committed"
        mock_push.return_value = "pushed"

        create_feature_288_markdown_file()

        # Verify commit was called with custom_message parameter
        call_args = mock_commit.call_args
        assert "custom_message" in call_args[1]
        message = call_args[1]["custom_message"]
        assert "feat(288):" in message
        assert MARKDOWN_FILENAME in message

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_logs_commit_completion(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that commit completion is logged at INFO level."""
        mock_generate.return_value = "# Test\n\nThis is a test sentence. Another one. And a third."
        mock_write.return_value = "/repo/test-dx2xd7.md"
        mock_commit.return_value = "committed"
        mock_push.return_value = "pushed"

        with patch("sheep.features.feature_288_markdown_file_creation._logger") as mock_logger:
            create_feature_288_markdown_file()

            # Verify INFO log for commit step
            info_calls = [call for call in mock_logger.info.call_args_list]
            assert any("commit" in str(call).lower() for call in info_calls)


class TestGitPushTask:
    """Tests for task-5: Git push with upstream tracking."""

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_calls_push_markdown_file(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that push_markdown_file is called during workflow."""
        mock_generate.return_value = "# Test\n\nThis is a test sentence. Another one. And a third."
        mock_write.return_value = "/repo/test-dx2xd7.md"
        mock_commit.return_value = "committed"
        mock_push.return_value = "pushed"

        create_feature_288_markdown_file()

        mock_push.assert_called_once()

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_returns_result_dict_with_expected_keys(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that function returns dict with filepath, content, commit_message, push_result."""
        test_content = "# Test\n\nThis is a test sentence. Another one. And a third."
        mock_filepath = "/repo/test-dx2xd7.md"
        mock_generate.return_value = test_content
        mock_write.return_value = mock_filepath
        mock_commit.return_value = "committed"
        mock_push.return_value = "pushed"

        result = create_feature_288_markdown_file()

        assert isinstance(result, dict)
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result
        assert result["filepath"] == mock_filepath
        assert result["content"] == test_content
        assert result["push_result"] == "pushed"

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_logs_push_completion(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that push completion is logged at INFO level."""
        mock_generate.return_value = "# Test\n\nThis is a test sentence. Another one. And a third."
        mock_write.return_value = "/repo/test-dx2xd7.md"
        mock_commit.return_value = "committed"
        mock_push.return_value = "pushed"

        with patch("sheep.features.feature_288_markdown_file_creation._logger") as mock_logger:
            create_feature_288_markdown_file()

            # Verify INFO log for push step
            info_calls = [call for call in mock_logger.info.call_args_list]
            assert any("push" in str(call).lower() for call in info_calls)


class TestWorkflowOrchestration:
    """Integration tests for complete workflow orchestration."""

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_workflow_executes_in_correct_order(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that workflow steps execute in the correct order."""
        call_order = []

        mock_generate.side_effect = lambda: (call_order.append("generate"), "# Test\n\nSentence one. Sentence two. Sentence three.")[1]
        mock_write.side_effect = lambda content, filename: (call_order.append("write"), "/repo/test-dx2xd7.md")[1]
        mock_validate.side_effect = lambda filepath: call_order.append("validate")
        mock_commit.side_effect = lambda *args, **kwargs: (call_order.append("commit"), "committed")[1]
        mock_push.side_effect = lambda *args, **kwargs: (call_order.append("push"), "pushed")[1]

        create_feature_288_markdown_file()

        assert call_order == ["generate", "write", "validate", "commit", "push"]

    @patch("sheep.features.feature_288_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_288_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_288_markdown_file_creation.push_markdown_file")
    def test_accepts_optional_repo_path_parameter(
        self,
        mock_push,
        mock_commit,
        mock_validate,
        mock_write,
        mock_generate,
    ):
        """Test that function accepts and passes repo_path to subsequent operations."""
        mock_generate.return_value = "# Test\n\nThis is a test sentence. Another one. And a third."
        mock_write.return_value = "/repo/test-dx2xd7.md"
        mock_commit.return_value = "committed"
        mock_push.return_value = "pushed"

        test_repo_path = "/custom/repo/path"
        create_feature_288_markdown_file(repo_path=test_repo_path)

        # Verify that push was called with the repo_path (as positional argument)
        call_args = mock_push.call_args
        assert call_args[0][0] == test_repo_path
