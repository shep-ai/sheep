"""Tests for feature 270 phase 2: Content generation and file persistence.

Tests the content generation step (task-3) and file writing step (task-4)
of the feature 270 markdown file creation workflow.
"""

from unittest.mock import Mock, patch
from pathlib import Path

import pytest

from sheep.features.feature_270_markdown_file_creation import (
    create_feature_270_markdown_file,
    MARKDOWN_FILENAME,
)


class TestTask3ContentGeneration:
    """Tests for task-3: Content generation step.

    Verifies that:
    - Function calls generate_markdown_content()
    - Content is returned as non-empty string
    - Error is logged and re-raised if generation fails
    """

    def test_calls_generate_markdown_content(self, tmp_path, monkeypatch):
        """Test that orchestration function calls generate_markdown_content()."""
        # Setup mocks for all content_generators functions
        mock_generate = Mock(return_value="# Test\n\nSentence 1. Sentence 2.\n")
        mock_write = Mock(return_value=str(tmp_path / MARKDOWN_FILENAME))
        mock_validate = Mock()
        mock_commit = Mock(return_value="commit_result")
        mock_push = Mock(return_value="push_result")

        # Patch the imported functions
        with patch(
            "sheep.features.feature_270_markdown_file_creation.generate_markdown_content",
            mock_generate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.write_markdown_file",
            mock_write,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.validate_markdown_file",
            mock_validate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.commit_markdown_file",
            mock_commit,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.push_markdown_file",
            mock_push,
        ):
            # Change to tmp directory to avoid side effects
            monkeypatch.chdir(tmp_path)

            # Execute the feature
            result = create_feature_270_markdown_file(str(tmp_path))

            # Verify generate_markdown_content was called exactly once
            mock_generate.assert_called_once()
            assert result is not None

    def test_content_is_non_empty_string(self, tmp_path, monkeypatch):
        """Test that generated content is returned as non-empty string."""
        test_content = "# Artificial Intelligence\n\nAI is transforming industries. Machine learning powers modern applications. Neural networks enable complex pattern recognition.\n"

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(return_value=str(tmp_path / MARKDOWN_FILENAME))
        mock_validate = Mock()
        mock_commit = Mock(return_value="commit_result")
        mock_push = Mock(return_value="push_result")

        with patch(
            "sheep.features.feature_270_markdown_file_creation.generate_markdown_content",
            mock_generate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.write_markdown_file",
            mock_write,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.validate_markdown_file",
            mock_validate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.commit_markdown_file",
            mock_commit,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.push_markdown_file",
            mock_push,
        ):
            monkeypatch.chdir(tmp_path)
            result = create_feature_270_markdown_file(str(tmp_path))

            # Verify content is non-empty string
            assert "content" in result
            assert isinstance(result["content"], str)
            assert len(result["content"]) > 0
            assert result["content"] == test_content

    def test_error_logged_and_re_raised_on_generation_failure(
        self, tmp_path, monkeypatch, capsys
    ):
        """Test that error is logged and re-raised if content generation fails."""
        error_msg = "API rate limit exceeded"
        mock_generate = Mock(side_effect=ValueError(error_msg))

        with patch(
            "sheep.features.feature_270_markdown_file_creation.generate_markdown_content",
            mock_generate,
        ):
            monkeypatch.chdir(tmp_path)

            # Verify that exception is raised
            with pytest.raises(ValueError, match=error_msg):
                create_feature_270_markdown_file(str(tmp_path))

            # Verify error was logged via structlog (captured as stdout)
            captured = capsys.readouterr()
            assert "Failed to create feature 270" in captured.out


class TestTask4FileWriting:
    """Tests for task-4: File writing step.

    Verifies that:
    - Function calls write_markdown_file() with correct parameters
    - File is created at repository root
    - Error is logged if file write fails
    """

    def test_calls_write_markdown_file_with_correct_parameters(self, tmp_path, monkeypatch):
        """Test that orchestration function calls write_markdown_file() with correct parameters."""
        test_content = "# Test Title\n\nSentence 1. Sentence 2.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(return_value=test_filepath)
        mock_validate = Mock()
        mock_commit = Mock(return_value="commit_result")
        mock_push = Mock(return_value="push_result")

        with patch(
            "sheep.features.feature_270_markdown_file_creation.generate_markdown_content",
            mock_generate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.write_markdown_file",
            mock_write,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.validate_markdown_file",
            mock_validate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.commit_markdown_file",
            mock_commit,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.push_markdown_file",
            mock_push,
        ):
            monkeypatch.chdir(tmp_path)
            result = create_feature_270_markdown_file(str(tmp_path))

            # Verify write_markdown_file was called with correct parameters
            mock_write.assert_called_once()
            call_args = mock_write.call_args
            # Should be called with (content, filename)
            assert call_args[0][0] == test_content  # First positional argument is content
            assert call_args[0][1] == MARKDOWN_FILENAME  # Second positional argument is filename

    def test_file_created_at_repository_root(self, tmp_path, monkeypatch):
        """Test that file is created at repository root."""
        test_content = "# Repository Root\n\nFiles go in the root. This is standard practice. Location matters.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)

        # Create the actual file to verify it exists
        mock_generate = Mock(return_value=test_content)

        def mock_write(content, filename):
            filepath = tmp_path / filename
            filepath.write_text(content, encoding="utf-8")
            return str(filepath)

        mock_validate = Mock()
        mock_commit = Mock(return_value="commit_result")
        mock_push = Mock(return_value="push_result")

        with patch(
            "sheep.features.feature_270_markdown_file_creation.generate_markdown_content",
            mock_generate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.write_markdown_file",
            side_effect=mock_write,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.validate_markdown_file",
            mock_validate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.commit_markdown_file",
            mock_commit,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.push_markdown_file",
            mock_push,
        ):
            monkeypatch.chdir(tmp_path)
            result = create_feature_270_markdown_file(str(tmp_path))

            # Verify file exists at the expected path
            filepath = Path(result["filepath"])
            assert filepath.exists()
            assert filepath.name == MARKDOWN_FILENAME
            assert filepath.parent == tmp_path

    def test_error_logged_on_file_write_failure(self, tmp_path, monkeypatch, capsys):
        """Test that error is logged if file write fails."""
        test_content = "# Test\n\nSentence 1. Sentence 2.\n"
        error_msg = "Permission denied: cannot write to file"

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(side_effect=IOError(error_msg))

        with patch(
            "sheep.features.feature_270_markdown_file_creation.generate_markdown_content",
            mock_generate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.write_markdown_file",
            mock_write,
        ):
            monkeypatch.chdir(tmp_path)

            # Verify that exception is raised
            with pytest.raises(IOError, match=error_msg):
                create_feature_270_markdown_file(str(tmp_path))

            # Verify error was logged via structlog (captured as stdout)
            captured = capsys.readouterr()
            assert "Failed to create feature 270" in captured.out


class TestContentGenerationAndFileWritingIntegration:
    """Integration tests for content generation + file writing workflow.

    Tests the complete flow of task-3 and task-4 together.
    """

    def test_content_generation_followed_by_file_writing(self, tmp_path, monkeypatch):
        """Test that content generation is followed by file writing in the correct order."""
        test_content = "# Integration Test\n\nGeneration happens first. Writing follows. Order matters.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)

        call_order = []

        def mock_generate():
            call_order.append("generate")
            return test_content

        def mock_write(content, filename):
            call_order.append("write")
            filepath = tmp_path / filename
            filepath.write_text(content, encoding="utf-8")
            return str(filepath)

        mock_validate = Mock()
        mock_commit = Mock(return_value="commit_result")
        mock_push = Mock(return_value="push_result")

        with patch(
            "sheep.features.feature_270_markdown_file_creation.generate_markdown_content",
            side_effect=mock_generate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.write_markdown_file",
            side_effect=mock_write,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.validate_markdown_file",
            mock_validate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.commit_markdown_file",
            mock_commit,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.push_markdown_file",
            mock_push,
        ):
            monkeypatch.chdir(tmp_path)
            result = create_feature_270_markdown_file(str(tmp_path))

            # Verify order: generate before write
            assert call_order == ["generate", "write"]
            assert result["content"] == test_content

    def test_generated_content_written_to_file_unchanged(self, tmp_path, monkeypatch):
        """Test that generated content is written to file without modification."""
        test_content = "# Markdown File\n\nThis is the content. It should be preserved. Unchanged throughout.\n"

        mock_generate = Mock(return_value=test_content)

        def mock_write(content, filename):
            # Verify content is unchanged
            assert content == test_content
            filepath = tmp_path / filename
            filepath.write_text(content, encoding="utf-8")
            return str(filepath)

        mock_validate = Mock()
        mock_commit = Mock(return_value="commit_result")
        mock_push = Mock(return_value="push_result")

        with patch(
            "sheep.features.feature_270_markdown_file_creation.generate_markdown_content",
            mock_generate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.write_markdown_file",
            side_effect=mock_write,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.validate_markdown_file",
            mock_validate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.commit_markdown_file",
            mock_commit,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.push_markdown_file",
            mock_push,
        ):
            monkeypatch.chdir(tmp_path)
            result = create_feature_270_markdown_file(str(tmp_path))

            # Verify content in result matches original
            assert result["content"] == test_content

            # Verify file content matches
            filepath = Path(result["filepath"])
            file_content = filepath.read_text(encoding="utf-8")
            assert file_content == test_content
