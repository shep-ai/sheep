"""Tests for feature 296: Create markdown file test-eyqdut.md with prose content."""

from unittest.mock import patch

import pytest

from sheep.features.feature_296_markdown_file_creation import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_test_eyqdut_markdown_file,
    main,
)


class TestFeature296ModuleImport:
    """Tests for feature 296 module structure and metadata."""

    def test_feature_296_import(self):
        """Test that feature 296 can be imported and contains required symbols."""
        # Import the module
        from sheep.features import feature_296_markdown_file_creation

        # Verify all required symbols exist
        assert hasattr(feature_296_markdown_file_creation, "FEATURE_NUMBER")
        assert hasattr(feature_296_markdown_file_creation, "MARKDOWN_FILENAME")
        assert hasattr(feature_296_markdown_file_creation, "create_test_eyqdut_markdown_file")
        assert hasattr(feature_296_markdown_file_creation, "main")

    def test_feature_number_is_296(self):
        """Test that FEATURE_NUMBER is 296."""
        assert FEATURE_NUMBER == 296

    def test_markdown_filename_is_correct(self):
        """Test that MARKDOWN_FILENAME is test-eyqdut.md."""
        assert MARKDOWN_FILENAME == "test-eyqdut.md"

    def test_feature_name_is_set(self):
        """Test that FEATURE_NAME is set correctly."""
        assert FEATURE_NAME == "markdown-file-creation-272c45"

    def test_create_function_is_callable(self):
        """Test that create_test_eyqdut_markdown_file function is callable."""
        assert callable(create_test_eyqdut_markdown_file)

    def test_main_function_is_callable(self):
        """Test that main function is callable."""
        assert callable(main)


class TestCreateFeature296Function:
    """Tests for create_test_eyqdut_markdown_file function."""

    def test_function_signature_accepts_repo_path(self):
        """Test that function accepts repo_path parameter."""
        # Function should accept optional repo_path parameter
        assert create_test_eyqdut_markdown_file.__code__.co_varnames[0] == "repo_path"

    def test_function_returns_dict_with_expected_keys(self):
        """Test that function has correct return type annotation in docstring."""
        docstring = create_test_eyqdut_markdown_file.__doc__
        assert "Dictionary containing" in docstring
        assert "filepath" in docstring
        assert "content" in docstring
        assert "commit_message" in docstring
        assert "push_result" in docstring

    def test_function_has_error_handling_docstring(self):
        """Test that function documents exception behavior."""
        docstring = create_test_eyqdut_markdown_file.__doc__
        assert "Raises" in docstring
        assert "ValueError" in docstring
        assert "IOError" in docstring
        assert "Exception" in docstring

    def test_function_has_comprehensive_docstring(self):
        """Test that function has proper documentation."""
        docstring = create_test_eyqdut_markdown_file.__doc__
        # Check for main workflow description
        assert "orchestrates the complete workflow" in docstring.lower()
        # Check for key workflow steps mentioned
        assert "generate valid markdown content" in docstring.lower()
        assert "write file to repository root" in docstring.lower()
        assert "validate file meets" in docstring.lower()


class TestCreateFeature296Integration:
    """Integration tests for feature 296 workflow."""

    @patch("sheep.features.feature_296_markdown_file_creation.create_markdown_file")
    def test_calls_create_markdown_file(self, mock_create_markdown):
        """Test that function calls create_markdown_file orchestration function."""
        mock_create_markdown.return_value = {
            "filepath": "/repo/test-eyqdut.md",
            "content": "# Title\n\nSentence one. Sentence two. Sentence three.",
            "commit_message": "feat(296): create markdown file test-eyqdut.md with prose content",
            "push_result": "pushed",
        }

        create_test_eyqdut_markdown_file()

        # Verify create_markdown_file was called exactly once
        mock_create_markdown.assert_called_once()

    @patch("sheep.features.feature_296_markdown_file_creation.create_markdown_file")
    def test_passes_correct_parameters_to_orchestration(self, mock_create_markdown):
        """Test that function passes correct parameters to create_markdown_file."""
        mock_create_markdown.return_value = {
            "filepath": "/repo/test-eyqdut.md",
            "content": "# Title\n\nSentence one. Sentence two.",
            "commit_message": "feat(296): create markdown file test-eyqdut.md with prose content",
            "push_result": "pushed",
        }

        create_test_eyqdut_markdown_file()

        # Verify the function was called with correct arguments
        call_args = mock_create_markdown.call_args
        assert call_args[1]["filename"] == MARKDOWN_FILENAME
        assert call_args[1]["feature_number"] == FEATURE_NUMBER

    @patch("sheep.features.feature_296_markdown_file_creation.create_markdown_file")
    def test_returns_orchestration_result(self, mock_create_markdown):
        """Test that function returns the result from create_markdown_file."""
        expected_result = {
            "filepath": "/repo/test-eyqdut.md",
            "content": "# Title\n\nSentence one. Sentence two.",
            "commit_message": "feat(296): create markdown file test-eyqdut.md with prose content",
            "push_result": "pushed",
        }
        mock_create_markdown.return_value = expected_result

        result = create_test_eyqdut_markdown_file()

        assert result == expected_result

    @patch("sheep.features.feature_296_markdown_file_creation.create_markdown_file")
    def test_handles_orchestration_failures(self, mock_create_markdown):
        """Test that function propagates exceptions from orchestration layer."""
        mock_create_markdown.side_effect = RuntimeError("API connection failed")

        with pytest.raises(RuntimeError, match="API connection failed"):
            create_test_eyqdut_markdown_file()

    @patch("sheep.features.feature_296_markdown_file_creation.create_markdown_file")
    def test_accepts_custom_repo_path(self, mock_create_markdown):
        """Test that function accepts and passes custom repo_path parameter."""
        mock_create_markdown.return_value = {
            "filepath": "/custom/test-eyqdut.md",
            "content": "# Title\n\nSentence.",
            "commit_message": "feat(296): create markdown file test-eyqdut.md with prose content",
            "push_result": "pushed",
        }

        custom_repo_path = "/custom/repo/path"
        create_test_eyqdut_markdown_file(repo_path=custom_repo_path)

        # Verify repo_path was passed to orchestration function
        call_args = mock_create_markdown.call_args
        assert call_args[1]["repo_path"] == custom_repo_path

    @patch("sheep.features.feature_296_markdown_file_creation.create_markdown_file")
    def test_uses_path_cwd_when_repo_path_is_none(self, mock_create_markdown):
        """Test that function uses current working directory when repo_path is None."""
        mock_create_markdown.return_value = {
            "filepath": "/repo/test-eyqdut.md",
            "content": "# Title\n\nSentence.",
            "commit_message": "feat(296): create markdown file test-eyqdut.md with prose content",
            "push_result": "pushed",
        }

        create_test_eyqdut_markdown_file(repo_path=None)

        # Verify that repo_path was provided (not None)
        call_args = mock_create_markdown.call_args
        assert call_args[1]["repo_path"] is not None
        assert isinstance(call_args[1]["repo_path"], str)


class TestMainFunction:
    """Tests for the main() entry point."""

    @patch("sheep.features.feature_296_markdown_file_creation.create_test_eyqdut_markdown_file")
    def test_main_returns_zero_on_success(self, mock_create):
        """Test that main() returns 0 when feature creation succeeds."""
        mock_create.return_value = {
            "filepath": "/repo/test-eyqdut.md",
            "content": "# Title\n\nSentence one. Sentence two.",
            "commit_message": "feat(296): create markdown file test-eyqdut.md with prose content",
            "push_result": "pushed",
        }

        result = main()

        assert result == 0

    @patch("sheep.features.feature_296_markdown_file_creation.create_test_eyqdut_markdown_file")
    def test_main_returns_one_on_failure(self, mock_create):
        """Test that main() returns 1 when feature creation fails."""
        mock_create.side_effect = RuntimeError("Feature creation failed")

        result = main()

        assert result == 1

    @patch("sheep.features.feature_296_markdown_file_creation.create_test_eyqdut_markdown_file")
    def test_main_calls_create_function(self, mock_create):
        """Test that main() calls create_test_eyqdut_markdown_file."""
        mock_create.return_value = {
            "filepath": "/repo/test-eyqdut.md",
            "content": "# Title\n\nSentence.",
            "commit_message": "feat(296): create markdown file test-eyqdut.md with prose content",
            "push_result": "pushed",
        }

        main()

        mock_create.assert_called_once()

    @patch("sheep.features.feature_296_markdown_file_creation.create_test_eyqdut_markdown_file")
    def test_main_logs_success(self, mock_create):
        """Test that main() includes logging on success."""
        mock_create.return_value = {
            "filepath": "/repo/test-eyqdut.md",
            "content": "# Title\n\nSentence.",
            "commit_message": "feat(296): create markdown file test-eyqdut.md with prose content",
            "push_result": "pushed",
        }

        with patch("sheep.features.feature_296_markdown_file_creation._logger") as mock_logger:
            main()

            # Verify logging occurred
            assert mock_logger.info.called

    @patch("sheep.features.feature_296_markdown_file_creation.create_test_eyqdut_markdown_file")
    def test_main_logs_failure(self, mock_create):
        """Test that main() includes logging on failure."""
        mock_create.side_effect = RuntimeError("Feature creation failed")

        with patch("sheep.features.feature_296_markdown_file_creation._logger") as mock_logger:
            main()

            # Verify error logging occurred
            assert mock_logger.error.called
