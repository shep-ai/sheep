"""Tests for feature 178: Creating markdown file test-l2bcbe.md with title and prose content.

This test suite covers:
- Task 3: Execute feature and verify file creation
- Task 4: Validate git operations and specification compliance
"""

import inspect
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest


class TestFeature178MarkdownFileCreation:
    """Tests for feature 178 markdown file creation."""

    def test_module_imports(self):
        """Test that the feature module can be imported."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        assert callable(create_feature_178_markdown_file)

    def test_function_signature(self):
        """Test that the function has the correct signature."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        sig = inspect.signature(create_feature_178_markdown_file)
        assert "repo_path" in sig.parameters
        assert sig.parameters["repo_path"].default is None

    def test_feature_constants(self):
        """Test that feature constants are defined correctly."""
        from sheep.features.feature_178_markdown_file_creation import (
            COMMIT_MESSAGE,
            FEATURE_NUMBER,
            MARKDOWN_FILENAME,
        )

        assert FEATURE_NUMBER == 178
        assert MARKDOWN_FILENAME == "test-l2bcbe.md"
        assert COMMIT_MESSAGE == "feat(178): create markdown file test-l2bcbe.md with prose content"

    def test_all_helper_functions_accessible(self):
        """Test that all helper functions are imported and accessible."""
        from sheep.features.feature_178_markdown_file_creation import (
            generate_markdown_content,
            write_markdown_file,
            validate_markdown_file,
            commit_markdown_file,
            push_markdown_file,
        )

        assert callable(generate_markdown_content)
        assert callable(write_markdown_file)
        assert callable(validate_markdown_file)
        assert callable(commit_markdown_file)
        assert callable(push_markdown_file)

    @patch("sheep.features.feature_178_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.generate_markdown_content")
    def test_orchestration_calls_all_steps(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that the orchestration calls all steps in the correct order."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        # Setup mock returns
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-l2bcbe.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed successfully"
        mock_push.return_value = "Pushed successfully"

        # Call the function
        result = create_feature_178_markdown_file("/test/repo")

        # Verify all functions were called
        mock_generate.assert_called_once()
        mock_write.assert_called_once_with(mock_content, "test-l2bcbe.md")
        mock_validate.assert_called_once()
        mock_commit.assert_called_once()
        mock_push.assert_called_once()

        # Verify the return value structure
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result


class TestFeature178FileValidation:
    """Tests for Task 3: Execute and verify file creation."""

    @patch("sheep.features.feature_178_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.generate_markdown_content")
    def test_file_created_at_repository_root(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that file test-l2bcbe.md is created at repository root."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        # Setup mocks
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third.\n"
        mock_generate.return_value = mock_content
        expected_path = "/repo/test-l2bcbe.md"
        mock_write.return_value = expected_path

        # Execute
        result = create_feature_178_markdown_file("/repo")

        # Verify file path
        assert result["filepath"] == expected_path
        mock_write.assert_called_once_with(mock_content, "test-l2bcbe.md")

    @patch("sheep.features.feature_178_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.generate_markdown_content")
    def test_file_contains_valid_markdown_structure(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that generated file contains H1 heading and 2-3 sentences."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        # Setup mocks with valid markdown
        mock_content = "# Example Title\n\nThis is the first sentence. This is the second sentence. This is the third sentence.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-l2bcbe.md"

        # Execute
        result = create_feature_178_markdown_file("/repo")

        # Verify content structure
        assert result["content"].startswith("# ")
        assert result["content"].count(".") >= 2 and result["content"].count(".") <= 3

    @patch("sheep.features.feature_178_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.generate_markdown_content")
    def test_validation_called_on_generated_file(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that validation is called on the generated file."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        # Setup mocks
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-l2bcbe.md"

        # Execute
        create_feature_178_markdown_file("/repo")

        # Verify validation was called
        mock_validate.assert_called_once_with("/repo/test-l2bcbe.md")


class TestFeature178GitOperations:
    """Tests for Task 4: Validate git operations and specification compliance."""

    @patch("sheep.features.feature_178_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.generate_markdown_content")
    def test_file_committed_with_correct_message(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that file is committed with correct conventional commit message."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
            COMMIT_MESSAGE,
        )

        # Setup mocks
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-l2bcbe.md"
        mock_commit.return_value = {"message": COMMIT_MESSAGE, "status": "success"}

        # Execute
        result = create_feature_178_markdown_file("/repo")

        # Verify commit was called
        mock_commit.assert_called_once()
        call_args = mock_commit.call_args
        assert call_args[1]["custom_message"] == COMMIT_MESSAGE

        # Verify result includes correct message
        assert result["commit_message"] == COMMIT_MESSAGE

    @patch("sheep.features.feature_178_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.generate_markdown_content")
    def test_file_pushed_to_remote(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that file is pushed to remote repository."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        # Setup mocks
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-l2bcbe.md"
        mock_push.return_value = "Pushed successfully"

        # Execute
        result = create_feature_178_markdown_file("/repo")

        # Verify push was called
        mock_push.assert_called_once_with("/repo")

        # Verify result includes push result
        assert "push_result" in result

    @patch("sheep.features.feature_178_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_178_markdown_file_creation.generate_markdown_content")
    def test_function_completes_without_exceptions(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that function executes without exceptions."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        # Setup mocks
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-l2bcbe.md"
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Execute - should not raise any exceptions
        result = create_feature_178_markdown_file("/repo")

        # Verify we got a result
        assert result is not None
        assert isinstance(result, dict)
