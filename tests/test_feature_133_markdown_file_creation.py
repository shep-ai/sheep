"""Tests for feature 133: markdown file creation (test-az5jtn.md)."""

import os
import time
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.features.feature_133_markdown_file_creation import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    _run_step_with_logging,
    create_feature_133_markdown_file,
)


class TestModuleImports:
    """Test module imports and constants."""

    def test_imports_work(self):
        """Test that module can be imported without errors."""
        from sheep.features.feature_133_markdown_file_creation import (
            create_feature_133_markdown_file,
        )

        assert callable(create_feature_133_markdown_file)

    def test_constants_defined(self):
        """Test that required module constants are defined."""
        assert FEATURE_NUMBER == 133
        assert FEATURE_NAME == "markdown-file-creation-682344"
        assert MARKDOWN_FILENAME == "test-az5jtn.md"

    def test_logger_exists(self):
        """Test that logger is properly initialized."""
        from sheep.features.feature_133_markdown_file_creation import _logger

        # Logger should have standard logging methods
        assert hasattr(_logger, "info")
        assert hasattr(_logger, "debug")
        assert hasattr(_logger, "error")
        assert callable(_logger.info)
        assert callable(_logger.debug)
        assert callable(_logger.error)

    def test_entry_point_function_signature(self):
        """Test that entry point function has correct signature."""
        import inspect

        sig = inspect.signature(create_feature_133_markdown_file)
        params = list(sig.parameters.keys())
        assert "repo_path" in params
        assert sig.parameters["repo_path"].default is None


class TestStepLoggingHelper:
    """Test the _run_step_with_logging helper function."""

    def test_step_logging_entry(self):
        """Test that step logging captures entry event."""
        mock_func = MagicMock(return_value="result")

        with patch("sheep.features.feature_133_markdown_file_creation._logger") as mock_logger:
            _run_step_with_logging("Test Step", mock_func)

            # Verify logger.info was called for entry
            assert mock_logger.info.called
            call_args = [call[0] for call in mock_logger.info.call_args_list]
            assert any("Test Step" in str(arg) for arg in call_args)

    def test_step_logging_exit(self):
        """Test that step logging captures exit event with duration."""
        mock_func = MagicMock(return_value="result")

        with patch("sheep.features.feature_133_markdown_file_creation._logger") as mock_logger:
            _run_step_with_logging("Test Step", mock_func)

            # Verify logger.info was called for exit with duration
            assert mock_logger.info.call_count >= 2
            # Check that second call includes "Completed"
            exit_call = mock_logger.info.call_args_list[1]
            assert "Completed" in str(exit_call[0][0])

    def test_step_logging_error(self):
        """Test that step logging captures errors and re-raises."""
        test_error = ValueError("Test error")
        mock_func = MagicMock(side_effect=test_error)

        with patch("sheep.features.feature_133_markdown_file_creation._logger") as mock_logger:
            with pytest.raises(ValueError, match="Test error"):
                _run_step_with_logging("Failing Step", mock_func)

            # Verify logger.error was called
            assert mock_logger.error.called
            error_call = mock_logger.error.call_args_list[0]
            assert "Failing Step" in str(error_call[0][0])
            assert "Failed" in str(error_call[0][0])

    def test_step_logging_error_context(self):
        """Test that error logging includes error type and message."""
        test_error = RuntimeError("Specific error message")
        mock_func = MagicMock(side_effect=test_error)

        with patch("sheep.features.feature_133_markdown_file_creation._logger") as mock_logger:
            with pytest.raises(RuntimeError):
                _run_step_with_logging("Error Step", mock_func)

            # Verify error context is logged
            error_call = mock_logger.error.call_args_list[0]
            kwargs = error_call[1]
            assert "error_type" in kwargs
            assert "error_message" in kwargs
            assert kwargs["error_type"] == "RuntimeError"
            assert "Specific error message" in kwargs["error_message"]

    def test_step_logging_json_format(self):
        """Test that structured logging is JSON-compatible (has required fields)."""
        mock_func = MagicMock(return_value="result")

        with patch("sheep.features.feature_133_markdown_file_creation._logger") as mock_logger:
            _run_step_with_logging("Step Name", mock_func)

            # Verify that exit call has duration_seconds kwarg
            exit_call = mock_logger.info.call_args_list[1]
            kwargs = exit_call[1]
            assert "duration_seconds" in kwargs
            assert isinstance(kwargs["duration_seconds"], float)

    def test_step_runs_provided_function(self):
        """Test that _run_step_with_logging actually runs the provided function."""
        mock_func = MagicMock(return_value="expected_result")

        with patch("sheep.features.feature_133_markdown_file_creation._logger"):
            result = _run_step_with_logging("Test Step", mock_func, "arg1", key="value")

        assert result == "expected_result"
        mock_func.assert_called_once_with("arg1", key="value")

    def test_step_logging_duration_accuracy(self):
        """Test that logged duration is approximately correct."""
        def slow_func():
            time.sleep(0.1)
            return "done"

        with patch("sheep.features.feature_133_markdown_file_creation._logger") as mock_logger:
            _run_step_with_logging("Slow Step", slow_func)

            # Get the duration from the exit log call
            exit_call = mock_logger.info.call_args_list[1]
            duration = exit_call[1]["duration_seconds"]

            # Should be roughly 0.1 seconds (within 50-200ms of actual)
            assert 0.05 < duration < 0.3


class TestEntryPointFunction:
    """Test the main create_feature_133_markdown_file function."""

    @patch("sheep.features.feature_133_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.generate_markdown_content")
    def test_entry_point_exists_and_callable(
        self, mock_gen, mock_write, mock_validate, mock_commit, mock_push
    ):
        """Test that entry point function exists and is callable."""
        mock_gen.return_value = "# Test\n\nContent here. More content. Final content.\n"
        mock_write.return_value = "/path/to/test-az5jtn.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        result = create_feature_133_markdown_file()
        assert isinstance(result, dict)

    @patch("sheep.features.feature_133_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.generate_markdown_content")
    def test_workflow_calls_all_five_steps(
        self, mock_gen, mock_write, mock_validate, mock_commit, mock_push
    ):
        """Test that workflow calls all five steps in order."""
        mock_gen.return_value = "# Test\n\nContent. More. Last.\n"
        mock_write.return_value = "/path/to/test-az5jtn.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        create_feature_133_markdown_file()

        # Verify all steps were called
        assert mock_gen.called
        assert mock_write.called
        assert mock_validate.called
        assert mock_commit.called
        assert mock_push.called

    @patch("sheep.features.feature_133_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.generate_markdown_content")
    def test_workflow_steps_called_in_correct_order(
        self, mock_gen, mock_write, mock_validate, mock_commit, mock_push
    ):
        """Test that workflow steps are called in the correct order."""
        call_order = []

        def track_gen():
            call_order.append("gen")
            return "# Test\n\nContent. More. Last.\n"

        def track_write(*args, **kwargs):
            call_order.append("write")
            return "/path/to/test-az5jtn.md"

        def track_validate(*args, **kwargs):
            call_order.append("validate")
            return True

        def track_commit(*args, **kwargs):
            call_order.append("commit")
            return "Committed"

        def track_push(*args, **kwargs):
            call_order.append("push")
            return "Pushed"

        mock_gen.side_effect = track_gen
        mock_write.side_effect = track_write
        mock_validate.side_effect = track_validate
        mock_commit.side_effect = track_commit
        mock_push.side_effect = track_push

        create_feature_133_markdown_file()

        assert call_order == ["gen", "write", "validate", "commit", "push"]

    @patch("sheep.features.feature_133_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.generate_markdown_content")
    def test_entry_point_returns_dict_with_required_keys(
        self, mock_gen, mock_write, mock_validate, mock_commit, mock_push
    ):
        """Test that entry point returns dict with all required keys."""
        mock_gen.return_value = "# Test\n\nContent. More. Last.\n"
        mock_write.return_value = "/path/to/test-az5jtn.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        result = create_feature_133_markdown_file()

        assert isinstance(result, dict)
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

    @patch("sheep.features.feature_133_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.generate_markdown_content")
    def test_commit_message_format(
        self, mock_gen, mock_write, mock_validate, mock_commit, mock_push
    ):
        """Test that commit message has correct format with feature number."""
        mock_gen.return_value = "# Test\n\nContent. More. Last.\n"
        mock_write.return_value = "/path/to/test-az5jtn.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        result = create_feature_133_markdown_file()

        commit_message = result["commit_message"]
        # Should start with feat(133):
        assert commit_message.startswith("feat(133):")
        # Should include the filename
        assert "test-az5jtn.md" in commit_message

    @patch("sheep.features.feature_133_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.generate_markdown_content")
    def test_entry_point_with_custom_repo_path(
        self, mock_gen, mock_write, mock_validate, mock_commit, mock_push
    ):
        """Test that entry point accepts custom repo_path parameter."""
        mock_gen.return_value = "# Test\n\nContent. More. Last.\n"
        mock_write.return_value = "/path/to/test-az5jtn.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        custom_path = "/custom/repo/path"
        result = create_feature_133_markdown_file(repo_path=custom_path)

        # Verify commit was called with custom repo_path
        assert mock_commit.called
        commit_call = mock_commit.call_args
        assert custom_path in str(commit_call)

    @patch("sheep.features.feature_133_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.generate_markdown_content")
    def test_entry_point_propagates_generation_errors(
        self, mock_gen, mock_write, mock_validate, mock_commit, mock_push
    ):
        """Test that generation errors are propagated."""
        mock_gen.side_effect = ValueError("Generation failed")

        with pytest.raises(ValueError, match="Generation failed"):
            create_feature_133_markdown_file()

    @patch("sheep.features.feature_133_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.generate_markdown_content")
    def test_entry_point_propagates_validation_errors(
        self, mock_gen, mock_write, mock_validate, mock_commit, mock_push
    ):
        """Test that validation errors are propagated."""
        mock_gen.return_value = "# Test\n\nContent. More. Last.\n"
        mock_write.return_value = "/path/to/test-az5jtn.md"
        mock_validate.side_effect = ValueError("Validation failed")

        with pytest.raises(ValueError, match="Validation failed"):
            create_feature_133_markdown_file()

    @patch("sheep.features.feature_133_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.generate_markdown_content")
    def test_entry_point_propagates_commit_errors(
        self, mock_gen, mock_write, mock_validate, mock_commit, mock_push
    ):
        """Test that commit errors are propagated."""
        mock_gen.return_value = "# Test\n\nContent. More. Last.\n"
        mock_write.return_value = "/path/to/test-az5jtn.md"
        mock_validate.return_value = True
        mock_commit.side_effect = Exception("Commit failed")

        with pytest.raises(Exception, match="Commit failed"):
            create_feature_133_markdown_file()

    @patch("sheep.features.feature_133_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_133_markdown_file_creation.generate_markdown_content")
    def test_entry_point_propagates_push_errors(
        self, mock_gen, mock_write, mock_validate, mock_commit, mock_push
    ):
        """Test that push errors are propagated."""
        mock_gen.return_value = "# Test\n\nContent. More. Last.\n"
        mock_write.return_value = "/path/to/test-az5jtn.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.side_effect = Exception("Push failed")

        with pytest.raises(Exception, match="Push failed"):
            create_feature_133_markdown_file()
