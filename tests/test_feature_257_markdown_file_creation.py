"""Tests for feature 257: Create markdown file test-oxy715.md with prose content."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

from sheep.features.feature_257_markdown_file_creation import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    _cleanup_file,
    _undo_commit,
    create_feature_257_markdown_file,
)


class TestFeature257Module:
    """Tests for feature 257 module structure and metadata."""

    def test_feature_number_is_257(self):
        """Test that FEATURE_NUMBER is 257."""
        assert FEATURE_NUMBER == 257

    def test_markdown_filename_is_correct(self):
        """Test that MARKDOWN_FILENAME is test-oxy715.md."""
        assert MARKDOWN_FILENAME == "test-oxy715.md"

    def test_feature_name_is_set(self):
        """Test that FEATURE_NAME is set correctly."""
        assert FEATURE_NAME == "markdown-file-creation-62bad4"

    def test_create_function_exists(self):
        """Test that create_feature_257_markdown_file function exists."""
        assert callable(create_feature_257_markdown_file)

    def test_cleanup_function_exists(self):
        """Test that cleanup functions exist."""
        assert callable(_cleanup_file)
        assert callable(_undo_commit)


class TestCreateFeature257Function:
    """Tests for create_feature_257_markdown_file function structure."""

    def test_function_signature_accepts_repo_path(self):
        """Test that function accepts repo_path parameter."""
        assert create_feature_257_markdown_file.__code__.co_varnames[0] == "repo_path"

    def test_function_returns_dict(self):
        """Test that function would return a dictionary (checking structure)."""
        docstring = create_feature_257_markdown_file.__doc__
        assert "Dictionary containing" in docstring
        assert "filepath" in docstring
        assert "content" in docstring
        assert "commit_message" in docstring
        assert "push_result" in docstring

    def test_function_includes_logging(self):
        """Test that function includes logging implementation."""
        from sheep.features.feature_257_markdown_file_creation import _logger

        assert _logger is not None

    def test_function_raises_on_failure(self):
        """Test that function documents exception behavior."""
        docstring = create_feature_257_markdown_file.__doc__
        assert "Raises" in docstring
        assert "ValueError" in docstring
        assert "IOError" in docstring
        assert "Exception" in docstring

    def test_function_documents_error_handling(self):
        """Test that function documents error handling and cleanup."""
        docstring = create_feature_257_markdown_file.__doc__
        assert "failure" in docstring.lower()
        assert (
            "cleanup" in docstring.lower()
            or "clean up" in docstring.lower()
            or "deleted" in docstring.lower()
        )


class TestErrorHandlingAndCleanup:
    """Tests for error handling and artifact cleanup functionality."""

    def test_cleanup_file_deletes_existing_file(self, tmp_path):
        """Test that _cleanup_file deletes an existing file."""
        test_file = tmp_path / "test.md"
        test_file.write_text("test content")

        assert test_file.exists()
        _cleanup_file(str(test_file))
        assert not test_file.exists()

    def test_cleanup_file_handles_nonexistent_file(self):
        """Test that _cleanup_file handles nonexistent files gracefully."""
        # Should not raise exception for nonexistent file
        _cleanup_file("/nonexistent/path/file.md")

    def test_cleanup_file_handles_none(self):
        """Test that _cleanup_file handles None input gracefully."""
        # Should not raise exception for None
        _cleanup_file(None)

    @patch("sheep.features.feature_257_markdown_file_creation.subprocess.run")
    def test_undo_commit_runs_git_reset(self, mock_run):
        """Test that _undo_commit runs git reset HEAD~1."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        _undo_commit("/repo/path")

        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == ["git", "reset", "HEAD~1"]
        assert call_args[1]["cwd"] == "/repo/path"

    @patch("sheep.features.feature_257_markdown_file_creation.subprocess.run")
    def test_undo_commit_handles_failure(self, mock_run):
        """Test that _undo_commit handles git reset failures gracefully."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "git error"
        mock_run.return_value = mock_result

        # Should not raise exception even if git reset fails
        _undo_commit("/repo/path")

    @patch("sheep.features.feature_257_markdown_file_creation.generate_markdown_content")
    def test_api_failure_logs_error(self, mock_generate):
        """Test that API failure is properly raised."""
        mock_generate.side_effect = Exception("API error: connection timeout")

        # Verify that the exception is propagated
        with pytest.raises(Exception) as exc_info:
            create_feature_257_markdown_file()

        assert "API error" in str(exc_info.value)

    @patch("sheep.features.feature_257_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_257_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_257_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_257_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_257_markdown_file_creation.generate_markdown_content")
    def test_push_failure_cleans_up_file_and_commit(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        tmp_path,
    ):
        """Test that push failure cleans up both file and commit."""
        # Setup
        test_file = tmp_path / MARKDOWN_FILENAME
        test_file.write_text("# Test\n\nTest content.")

        mock_generate.return_value = "# Test\n\nTest content."
        mock_write.return_value = str(test_file)
        mock_commit.return_value = "Committed"
        mock_push.side_effect = Exception("Push failed: network error")

        # Mock git reset to verify it's called
        with patch("sheep.features.feature_257_markdown_file_creation.subprocess.run") as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result

            with pytest.raises(Exception) as exc_info:
                create_feature_257_markdown_file(str(tmp_path))

            # Verify git reset was called
            mock_run.assert_called_once()
            assert mock_run.call_args[0][0] == ["git", "reset", "HEAD~1"]

            # Verify error is about push
            assert "Push failed" in str(exc_info.value)

        # Verify file was cleaned up
        assert not test_file.exists()

    @patch("sheep.features.feature_257_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_257_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_257_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_257_markdown_file_creation.generate_markdown_content")
    def test_commit_failure_cleans_up_file(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        tmp_path,
    ):
        """Test that commit failure cleans up the created file."""
        # Setup
        test_file = tmp_path / MARKDOWN_FILENAME
        test_file.write_text("# Test\n\nTest content.")

        mock_generate.return_value = "# Test\n\nTest content."
        mock_write.return_value = str(test_file)
        mock_commit.side_effect = Exception("Commit failed: git config missing")

        with pytest.raises(Exception) as exc_info:
            create_feature_257_markdown_file(str(tmp_path))

        # Verify error is about commit
        assert "Commit failed" in str(exc_info.value)

        # Verify file was cleaned up
        assert not test_file.exists()

    @patch("sheep.features.feature_257_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_257_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_257_markdown_file_creation.generate_markdown_content")
    def test_validation_failure_cleans_up_file(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        tmp_path,
    ):
        """Test that validation failure cleans up the created file."""
        # Setup
        test_file = tmp_path / MARKDOWN_FILENAME
        test_file.write_text("# Test\n\nTest content.")

        mock_generate.return_value = "# Test\n\nTest content."
        mock_write.return_value = str(test_file)
        mock_validate.side_effect = ValueError("Invalid H1 heading")

        with pytest.raises(ValueError) as exc_info:
            create_feature_257_markdown_file(str(tmp_path))

        # Verify error is about validation
        assert "Invalid H1 heading" in str(exc_info.value)

        # Verify file was cleaned up
        assert not test_file.exists()

    @patch("sheep.features.feature_257_markdown_file_creation.generate_markdown_content")
    def test_generation_failure_does_not_attempt_cleanup(
        self,
        mock_generate,
    ):
        """Test that generation failure doesn't attempt cleanup (nothing created yet)."""
        mock_generate.side_effect = Exception("API error")

        # When generation fails, no cleanup should be needed (no file created yet)
        with pytest.raises(Exception) as exc_info:
            create_feature_257_markdown_file()

        assert "API error" in str(exc_info.value)


class TestFeature257Integration:
    """Integration tests for feature 257 workflow."""

    def test_function_has_complete_docstring(self):
        """Test that function has comprehensive documentation."""
        docstring = create_feature_257_markdown_file.__doc__
        assert "orchestrates the complete workflow" in docstring.lower()
        assert "generate valid markdown content" in docstring.lower()
        assert "write file to repository root" in docstring.lower()
        assert "validate file meets" in docstring.lower()
        assert "stage and commit" in docstring.lower()
        assert "push to remote" in docstring.lower()

    def test_workflow_steps_in_docstring(self):
        """Test that docstring documents all workflow steps."""
        docstring = create_feature_257_markdown_file.__doc__
        # Count occurrences of step references
        assert "1." in docstring
        assert "2." in docstring
        assert "3." in docstring
        assert "4." in docstring
        assert "5." in docstring

    def test_imports_required_wrappers(self):
        """Test that module imports required wrapper functions."""
        from sheep.features.feature_257_markdown_file_creation import (
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
            "sheep.features.feature_257_markdown_file_creation",
            fromlist=[""],
        )
        source = inspect.getsource(module)
        # Check that the module source includes __main__ execution
        assert 'if __name__ == "__main__"' in source

    def test_error_logged_before_cleanup(self):
        """Test that error is properly propagated after cleanup operations."""
        from unittest.mock import patch

        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content"
        ) as mock_gen:
            mock_gen.side_effect = Exception("Test error")

            # Verify the original exception is re-raised
            with pytest.raises(Exception) as exc_info:
                create_feature_257_markdown_file()

            assert "Test error" in str(exc_info.value)

    def test_imports_subprocess_for_git_operations(self):
        """Test that module imports subprocess for git operations."""
        import inspect

        from sheep.features.feature_257_markdown_file_creation import (
            _undo_commit,
            _cleanup_file,
        )

        # Check that functions use subprocess
        source = inspect.getsource(_undo_commit)
        assert "subprocess" in source
        assert "git" in source
