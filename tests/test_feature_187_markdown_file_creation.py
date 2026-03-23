"""Tests for feature 187: Creating markdown file test-awwni7.md with title and prose content."""

import inspect
from pathlib import Path
from unittest.mock import patch

import pytest


class TestFeature187MarkdownFileCreation:
    """Tests for feature 187 markdown file creation."""

    def test_module_imports(self):
        """Test that the feature module can be imported."""
        from sheep.features.feature_187_markdown_file_creation import (
            create_feature_187_markdown_file,
        )

        assert callable(create_feature_187_markdown_file)

    def test_function_signature(self):
        """Test that the function has the correct signature."""
        from sheep.features.feature_187_markdown_file_creation import (
            create_feature_187_markdown_file,
        )

        sig = inspect.signature(create_feature_187_markdown_file)
        assert "repo_path" in sig.parameters
        assert sig.parameters["repo_path"].default is None

    def test_feature_constants(self):
        """Test that feature constants are defined correctly."""
        from sheep.features.feature_187_markdown_file_creation import (
            COMMIT_MESSAGE,
            FEATURE_NUMBER,
            MARKDOWN_FILENAME,
        )

        assert FEATURE_NUMBER == 187
        assert MARKDOWN_FILENAME == "test-awwni7.md"
        assert COMMIT_MESSAGE == "feat(187): create markdown file test-awwni7.md with prose content"

    def test_all_helper_functions_accessible(self):
        """Test that all helper functions are imported and accessible."""
        from sheep.features.feature_187_markdown_file_creation import (
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

    @patch("sheep.features.feature_187_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.generate_markdown_content")
    def test_orchestration_calls_all_steps(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that the orchestration calls all steps in the correct order."""
        from sheep.features.feature_187_markdown_file_creation import (
            create_feature_187_markdown_file,
        )

        # Setup mock returns
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-awwni7.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed successfully"
        mock_push.return_value = "Pushed successfully"

        # Call the function
        result = create_feature_187_markdown_file("/test/repo")

        # Verify all functions were called
        mock_generate.assert_called_once()
        mock_write.assert_called_once_with(mock_content, "test-awwni7.md")
        mock_validate.assert_called_once()
        mock_commit.assert_called_once()
        mock_push.assert_called_once()

        # Verify the return value structure
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

    @patch("sheep.features.feature_187_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.generate_markdown_content")
    def test_returns_correct_dict_structure(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that the function returns the correct dictionary structure."""
        from sheep.features.feature_187_markdown_file_creation import (
            COMMIT_MESSAGE,
            create_feature_187_markdown_file,
        )

        # Setup mock returns
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third.\n"
        mock_filepath = "/repo/test-awwni7.md"
        mock_generate.return_value = mock_content
        mock_write.return_value = mock_filepath
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call the function
        result = create_feature_187_markdown_file("/test/repo")

        # Verify the dictionary structure and values
        assert result["filepath"] == mock_filepath
        assert result["content"] == mock_content
        assert result["commit_message"] == COMMIT_MESSAGE
        assert result["push_result"] == "Pushed"

    @patch("sheep.features.feature_187_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.generate_markdown_content")
    def test_uses_exact_commit_message(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that the exact commit message from spec is used."""
        from sheep.features.feature_187_markdown_file_creation import (
            create_feature_187_markdown_file,
        )

        # Setup mocks
        mock_content = "# Test\n\nSentence. Sentence. Sentence.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-awwni7.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call the function
        create_feature_187_markdown_file()

        # Verify the commit message is exactly as specified
        call_args = mock_commit.call_args
        assert call_args is not None
        assert (
            call_args.kwargs["custom_message"]
            == "feat(187): create markdown file test-awwni7.md with prose content"
        )

    @patch("sheep.features.feature_187_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.generate_markdown_content")
    def test_handles_exception_in_generate(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that exceptions in generate step are properly raised."""
        from sheep.features.feature_187_markdown_file_creation import (
            create_feature_187_markdown_file,
        )

        # Setup mock to raise exception
        mock_generate.side_effect = ValueError("LLM generation failed")

        # Verify exception is raised
        with pytest.raises(ValueError, match="LLM generation failed"):
            create_feature_187_markdown_file()

        # Verify subsequent steps were not called
        mock_write.assert_not_called()
        mock_validate.assert_not_called()
        mock_commit.assert_not_called()
        mock_push.assert_not_called()

    @patch("sheep.features.feature_187_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_187_markdown_file_creation.generate_markdown_content")
    def test_repo_path_defaults_to_cwd(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that repo_path defaults to current working directory."""
        from sheep.features.feature_187_markdown_file_creation import (
            create_feature_187_markdown_file,
        )

        # Setup mocks
        mock_content = "# Test\n\nSentence. Sentence. Sentence.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-awwni7.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call without repo_path
        create_feature_187_markdown_file()

        # Verify commit was called with str(Path.cwd())
        call_args = mock_commit.call_args
        assert call_args is not None
        assert call_args[0][2] == str(Path.cwd())
