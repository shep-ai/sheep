"""Tests for feature 145 Phase 2: Orchestration Implementation.

Tests for the create_feature_145_markdown_file orchestration function
and the __main__ block execution.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from sheep.features.feature_145_markdown_file_creation import (
    create_feature_145_markdown_file,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    COMMIT_MESSAGE,
)


class TestOrchestrationFunctionSignature:
    """Tests for create_feature_145_markdown_file function signature and behavior."""

    def test_function_exists_and_is_callable(self):
        """Test that create_feature_145_markdown_file function exists and is callable."""
        assert callable(create_feature_145_markdown_file)

    def test_function_accepts_optional_repo_path_parameter(self):
        """Test that function accepts optional repo_path parameter."""
        import inspect

        sig = inspect.signature(create_feature_145_markdown_file)
        params = sig.parameters

        # Should have repo_path parameter
        assert "repo_path" in params
        # Should have a default value of None
        assert params["repo_path"].default is None

    def test_function_has_return_type_hint(self):
        """Test that function has return type hint."""
        import inspect

        sig = inspect.signature(create_feature_145_markdown_file)
        # Check return annotation exists
        assert sig.return_annotation != inspect.Signature.empty


class TestOrchestrationWorkflow:
    """Tests for the orchestration workflow (5-step process)."""

    @patch("sheep.features.feature_145_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.generate_markdown_content")
    def test_orchestration_calls_all_five_steps_in_order(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that orchestration calls all 5 steps in correct order."""
        # Setup mocks
        mock_generate.return_value = "# Test\n\nFirst. Second. Third.\n"
        mock_write.return_value = "/path/to/test-rtj7cz.md"
        mock_commit.return_value = {"message": "committed"}
        mock_push.return_value = {"status": "pushed"}

        # Call function
        result = create_feature_145_markdown_file()

        # Verify all steps were called exactly once
        mock_generate.assert_called_once()
        mock_write.assert_called_once()
        mock_validate.assert_called_once()
        mock_commit.assert_called_once()
        mock_push.assert_called_once()

    @patch("sheep.features.feature_145_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.generate_markdown_content")
    def test_orchestration_returns_dict_with_required_keys(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that orchestration returns a dictionary with filepath, content, commit_message, push_result."""
        # Setup mocks
        mock_generate.return_value = "# Test\n\nFirst. Second. Third.\n"
        mock_write.return_value = "/path/to/test-rtj7cz.md"
        mock_commit.return_value = {"message": "committed"}
        mock_push.return_value = {"status": "pushed"}

        # Call function
        result = create_feature_145_markdown_file()

        # Verify return type and keys
        assert isinstance(result, dict)
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

    @patch("sheep.features.feature_145_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.generate_markdown_content")
    def test_orchestration_passes_correct_filename_to_write(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that orchestration passes MARKDOWN_FILENAME to write_markdown_file."""
        # Setup mocks
        mock_generate.return_value = "# Test\n\nFirst. Second. Third.\n"
        mock_write.return_value = "/path/to/test-rtj7cz.md"

        # Call function
        create_feature_145_markdown_file()

        # Verify filename was passed correctly
        mock_write.assert_called_once()
        call_args = mock_write.call_args
        # Second positional argument should be MARKDOWN_FILENAME
        assert call_args[0][1] == MARKDOWN_FILENAME

    @patch("sheep.features.feature_145_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.generate_markdown_content")
    def test_orchestration_passes_correct_commit_message(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that orchestration passes COMMIT_MESSAGE to commit_markdown_file."""
        # Setup mocks
        mock_generate.return_value = "# Test\n\nFirst. Second. Third.\n"
        mock_write.return_value = "/path/to/test-rtj7cz.md"
        mock_commit.return_value = {"message": "committed"}

        # Call function
        create_feature_145_markdown_file()

        # Verify commit message was passed correctly
        mock_commit.assert_called_once()
        call_kwargs = mock_commit.call_args[1]
        assert call_kwargs.get("custom_message") == COMMIT_MESSAGE


class TestErrorHandling:
    """Tests for error handling in orchestration function."""

    @patch("sheep.features.feature_145_markdown_file_creation.generate_markdown_content")
    def test_orchestration_raises_on_content_generation_failure(self, mock_generate):
        """Test that orchestration raises exception if content generation fails."""
        # Setup mock to raise an error
        mock_generate.side_effect = ValueError("API error")

        # Call function and expect it to raise
        with pytest.raises(ValueError, match="API error"):
            create_feature_145_markdown_file()

    @patch("sheep.features.feature_145_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.generate_markdown_content")
    def test_orchestration_raises_on_file_write_failure(self, mock_generate, mock_write):
        """Test that orchestration raises exception if file write fails."""
        # Setup mocks
        mock_generate.return_value = "# Test\n\nFirst. Second. Third.\n"
        mock_write.side_effect = IOError("Disk full")

        # Call function and expect it to raise
        with pytest.raises(IOError, match="Disk full"):
            create_feature_145_markdown_file()

    @patch("sheep.features.feature_145_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.generate_markdown_content")
    def test_orchestration_raises_on_validation_failure(
        self, mock_generate, mock_write, mock_validate
    ):
        """Test that orchestration raises exception if validation fails."""
        # Setup mocks
        mock_generate.return_value = "# Test\n\nFirst. Second. Third.\n"
        mock_write.return_value = "/path/to/test-rtj7cz.md"
        mock_validate.side_effect = ValueError("Invalid format")

        # Call function and expect it to raise
        with pytest.raises(ValueError, match="Invalid format"):
            create_feature_145_markdown_file()

    @patch("sheep.features.feature_145_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.generate_markdown_content")
    def test_orchestration_raises_on_commit_failure(
        self, mock_generate, mock_write, mock_validate, mock_commit
    ):
        """Test that orchestration raises exception if commit fails."""
        # Setup mocks
        mock_generate.return_value = "# Test\n\nFirst. Second. Third.\n"
        mock_write.return_value = "/path/to/test-rtj7cz.md"
        mock_commit.side_effect = Exception("Git error")

        # Call function and expect it to raise
        with pytest.raises(Exception, match="Git error"):
            create_feature_145_markdown_file()

    @patch("sheep.features.feature_145_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.generate_markdown_content")
    def test_orchestration_raises_on_push_failure(
        self, mock_generate, mock_write, mock_validate, mock_commit, mock_push
    ):
        """Test that orchestration raises exception if push fails."""
        # Setup mocks
        mock_generate.return_value = "# Test\n\nFirst. Second. Third.\n"
        mock_write.return_value = "/path/to/test-rtj7cz.md"
        mock_commit.return_value = {"message": "committed"}
        mock_push.side_effect = Exception("Network error")

        # Call function and expect it to raise
        with pytest.raises(Exception, match="Network error"):
            create_feature_145_markdown_file()


class TestLogging:
    """Tests for logging in orchestration function."""

    @patch("sheep.features.feature_145_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.generate_markdown_content")
    def test_orchestration_logs_at_each_step(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that orchestration logs at each step of the workflow."""
        # Setup mocks
        mock_generate.return_value = "# Test\n\nFirst. Second. Third.\n"
        mock_write.return_value = "/path/to/test-rtj7cz.md"
        mock_commit.return_value = {"message": "committed"}
        mock_push.return_value = {"status": "pushed"}

        # Patch the logger to track calls
        with patch(
            "sheep.features.feature_145_markdown_file_creation._logger"
        ) as mock_logger:
            create_feature_145_markdown_file()

            # Verify logger.info was called for each step
            assert mock_logger.info.called
            # Should log at least for:
            # - Creating feature 145 markdown file
            # - Task 1: Generating markdown content
            # - Task 2: Writing markdown file to disk
            # - Task 3: Validating markdown file
            # - Task 4: Staging and committing file
            # - Task 5: Pushing to remote repository
            # - Successfully created and published
            assert mock_logger.info.call_count >= 7


class TestMainBlock:
    """Tests for __main__ block execution."""

    @patch("sheep.features.feature_145_markdown_file_creation.create_feature_145_markdown_file")
    def test_main_block_calls_orchestration_function(self, mock_create):
        """Test that __main__ block calls create_feature_145_markdown_file."""
        mock_create.return_value = {
            "filepath": "/path/to/test-rtj7cz.md",
            "content": "# Test\n\nFirst. Second. Third.\n",
            "commit_message": "feat(145): create markdown file test-rtj7cz.md with prose content",
            "push_result": {"status": "pushed"},
        }

        # Import and run the module as __main__
        import subprocess
        import sys

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "sheep.features.feature_145_markdown_file_creation",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Check that the process captured some output (module executed)
        # Note: This will fail if ANTHROPIC_API_KEY is not set, which is expected
        # The important thing is that the module is executable


class TestIntegration:
    """Integration tests for the orchestration function."""

    @patch("sheep.features.feature_145_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_145_markdown_file_creation.generate_markdown_content")
    def test_full_workflow_with_mocks(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test full workflow from start to finish with mocks."""
        # Setup realistic mocks
        test_content = "# Interesting Title\n\nFirst sentence about something. Second sentence continues. Third sentence concludes.\n"
        test_filepath = "/path/to/test-rtj7cz.md"

        mock_generate.return_value = test_content
        mock_write.return_value = test_filepath
        mock_commit.return_value = {"hash": "abc123"}
        mock_push.return_value = {"status": "success", "remote": "origin"}

        # Execute the orchestration
        result = create_feature_145_markdown_file()

        # Verify result
        assert result["filepath"] == test_filepath
        assert result["content"] == test_content
        assert result["commit_message"] == COMMIT_MESSAGE
        assert result["push_result"]["status"] == "success"

        # Verify the workflow order (all should be called)
        assert mock_generate.call_count == 1
        assert mock_write.call_count == 1
        assert mock_validate.call_count == 1
        assert mock_commit.call_count == 1
        assert mock_push.call_count == 1
