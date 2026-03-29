"""Tests for feature 270 phase 4: Integration & End-to-End Validation.

Tests the complete orchestration of all 5 workflow steps:
1. Generate markdown content via Claude API
2. Write file to disk with UTF-8 encoding and LF line endings
3. Validate file structure, encoding, and format
4. Stage and commit file with conventional message
5. Push to remote repository

Tests verify:
- All 5 steps execute in correct order
- Return dictionary contains all required keys with correct values
- Comprehensive error handling and logging
- End-to-end workflow success scenarios
- Integration failures and error propagation
"""

from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

import pytest

from sheep.features.feature_270_markdown_file_creation import (
    create_feature_270_markdown_file,
    MARKDOWN_FILENAME,
    FEATURE_NUMBER,
)


# Sample valid markdown content for testing
SAMPLE_MARKDOWN = """# Renewable Energy Solutions

Modern renewable energy technologies have become increasingly cost-competitive with traditional fossil fuels. Wind and solar power installations now generate electricity for millions of homes across developed nations. As global climate awareness continues to grow, the transition to sustainable energy sources accelerates rapidly."""


class TestPhase4Orchestration:
    """Tests for complete orchestration of all workflow steps."""

    def test_all_five_steps_execute_in_sequence(self, tmp_path, monkeypatch):
        """Test that all 5 steps execute in correct order: generate → write → validate → commit → push."""
        call_sequence = []

        def mock_generate():
            call_sequence.append("generate")
            return SAMPLE_MARKDOWN

        def mock_write(content, filename):
            call_sequence.append("write")
            return str(tmp_path / filename)

        def mock_validate(filepath):
            call_sequence.append("validate")

        def mock_commit(filepath, content, repo_path, custom_message=None):
            call_sequence.append("commit")
            return f"Commit: {custom_message}"

        def mock_push(repo_path):
            call_sequence.append("push")
            return "Pushed successfully"

        with patch(
            "sheep.features.feature_270_markdown_file_creation.generate_markdown_content",
            side_effect=mock_generate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.write_markdown_file",
            side_effect=mock_write,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.validate_markdown_file",
            side_effect=mock_validate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.commit_markdown_file",
            side_effect=mock_commit,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.push_markdown_file",
            side_effect=mock_push,
        ):
            monkeypatch.chdir(tmp_path)
            result = create_feature_270_markdown_file(str(tmp_path))

            # Verify execution order
            assert call_sequence == ["generate", "write", "validate", "commit", "push"]
            assert result is not None

    def test_return_dictionary_has_all_required_keys(self, tmp_path, monkeypatch):
        """Test that return dictionary contains all required keys."""
        mock_generate = Mock(return_value=SAMPLE_MARKDOWN)
        mock_write = Mock(return_value=str(tmp_path / MARKDOWN_FILENAME))
        mock_validate = Mock()
        mock_commit = Mock(
            return_value=f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
        )
        mock_push = Mock(return_value="Pushed to origin")

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

            # Verify all required keys are present
            required_keys = {"filepath", "content", "commit_message", "push_result"}
            assert set(result.keys()) == required_keys

    def test_return_values_are_correct_types(self, tmp_path, monkeypatch):
        """Test that return dictionary values have correct types."""
        mock_filepath = str(tmp_path / MARKDOWN_FILENAME)
        mock_content = SAMPLE_MARKDOWN
        mock_commit_msg = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
        mock_push_result = "Pushed to origin/feat/270-markdown-file-creation-bec411"

        mock_generate = Mock(return_value=mock_content)
        mock_write = Mock(return_value=mock_filepath)
        mock_validate = Mock()
        mock_commit = Mock(return_value=mock_commit_msg)
        mock_push = Mock(return_value=mock_push_result)

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

            # Verify types
            assert isinstance(result["filepath"], str)
            assert isinstance(result["content"], str)
            assert isinstance(result["commit_message"], str)
            assert isinstance(result["push_result"], str)

    def test_filepath_in_return_matches_written_file(self, tmp_path, monkeypatch):
        """Test that filepath returned matches the file written."""
        expected_filepath = str(tmp_path / MARKDOWN_FILENAME)
        mock_generate = Mock(return_value=SAMPLE_MARKDOWN)
        mock_write = Mock(return_value=expected_filepath)
        mock_validate = Mock()
        mock_commit = Mock(return_value="Commit message")
        mock_push = Mock(return_value="Push result")

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

            assert result["filepath"] == expected_filepath

    def test_content_in_return_matches_generated_content(self, tmp_path, monkeypatch):
        """Test that content in return matches generated content."""
        mock_generate = Mock(return_value=SAMPLE_MARKDOWN)
        mock_write = Mock(return_value=str(tmp_path / MARKDOWN_FILENAME))
        mock_validate = Mock()
        mock_commit = Mock(return_value="Commit message")
        mock_push = Mock(return_value="Push result")

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

            assert result["content"] == SAMPLE_MARKDOWN

    def test_commit_message_has_correct_format(self, tmp_path, monkeypatch):
        """Test that commit message has correct format with feature number and filename."""
        mock_generate = Mock(return_value=SAMPLE_MARKDOWN)
        mock_write = Mock(return_value=str(tmp_path / MARKDOWN_FILENAME))
        mock_validate = Mock()
        mock_commit = Mock(return_value="Commit message")
        mock_push = Mock(return_value="Push result")

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

            expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
            assert result["commit_message"] == expected_message
            assert str(FEATURE_NUMBER) in result["commit_message"]
            assert MARKDOWN_FILENAME in result["commit_message"]

    def test_push_result_captured_and_returned(self, tmp_path, monkeypatch):
        """Test that push result is captured and returned in dictionary."""
        expected_push_result = "Successfully pushed to origin/feat/270-markdown-file-creation-bec411"
        mock_generate = Mock(return_value=SAMPLE_MARKDOWN)
        mock_write = Mock(return_value=str(tmp_path / MARKDOWN_FILENAME))
        mock_validate = Mock()
        mock_commit = Mock(return_value="Commit message")
        mock_push = Mock(return_value=expected_push_result)

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

            assert result["push_result"] == expected_push_result


class TestPhase4ErrorHandling:
    """Tests for comprehensive error handling in orchestration."""

    def test_exception_at_generate_is_caught_and_re_raised(self, tmp_path, monkeypatch):
        """Test that exception during content generation is caught and re-raised."""
        generation_error = "API request failed: connection timeout"
        mock_generate = Mock(side_effect=Exception(generation_error))

        with patch(
            "sheep.features.feature_270_markdown_file_creation.generate_markdown_content",
            mock_generate,
        ):
            monkeypatch.chdir(tmp_path)

            with pytest.raises(Exception, match=generation_error):
                create_feature_270_markdown_file(str(tmp_path))

    def test_exception_at_write_is_caught_and_re_raised(self, tmp_path, monkeypatch):
        """Test that exception during file write is caught and re-raised."""
        write_error = "IOError: disk full"
        mock_generate = Mock(return_value=SAMPLE_MARKDOWN)
        mock_write = Mock(side_effect=IOError(write_error))

        with patch(
            "sheep.features.feature_270_markdown_file_creation.generate_markdown_content",
            mock_generate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.write_markdown_file",
            mock_write,
        ):
            monkeypatch.chdir(tmp_path)

            with pytest.raises(IOError, match=write_error):
                create_feature_270_markdown_file(str(tmp_path))

    def test_exception_at_validate_is_caught_and_re_raised(self, tmp_path, monkeypatch):
        """Test that exception during validation is caught and re-raised."""
        validation_error = "Invalid: H1 heading required, found H2"
        mock_generate = Mock(return_value=SAMPLE_MARKDOWN)
        mock_write = Mock(return_value=str(tmp_path / MARKDOWN_FILENAME))
        mock_validate = Mock(side_effect=ValueError(validation_error))

        with patch(
            "sheep.features.feature_270_markdown_file_creation.generate_markdown_content",
            mock_generate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.write_markdown_file",
            mock_write,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.validate_markdown_file",
            mock_validate,
        ):
            monkeypatch.chdir(tmp_path)

            with pytest.raises(ValueError, match=validation_error):
                create_feature_270_markdown_file(str(tmp_path))

    def test_exception_at_commit_is_caught_and_re_raised(self, tmp_path, monkeypatch):
        """Test that exception during commit is caught and re-raised."""
        commit_error = "fatal: not a git repository"
        mock_generate = Mock(return_value=SAMPLE_MARKDOWN)
        mock_write = Mock(return_value=str(tmp_path / MARKDOWN_FILENAME))
        mock_validate = Mock()
        mock_commit = Mock(side_effect=Exception(commit_error))

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
        ):
            monkeypatch.chdir(tmp_path)

            with pytest.raises(Exception, match=commit_error):
                create_feature_270_markdown_file(str(tmp_path))

    def test_exception_at_push_is_caught_and_re_raised(self, tmp_path, monkeypatch):
        """Test that exception during push is caught and re-raised."""
        push_error = "fatal: Authentication failed"
        mock_generate = Mock(return_value=SAMPLE_MARKDOWN)
        mock_write = Mock(return_value=str(tmp_path / MARKDOWN_FILENAME))
        mock_validate = Mock()
        mock_commit = Mock(return_value="Commit message")
        mock_push = Mock(side_effect=Exception(push_error))

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

            with pytest.raises(Exception, match=push_error):
                create_feature_270_markdown_file(str(tmp_path))

    def test_error_logs_include_feature_number(self, tmp_path, monkeypatch, capsys):
        """Test that error logs include feature number for identification."""
        error_msg = "Test error"
        mock_generate = Mock(side_effect=Exception(error_msg))

        with patch(
            "sheep.features.feature_270_markdown_file_creation.generate_markdown_content",
            mock_generate,
        ):
            monkeypatch.chdir(tmp_path)

            try:
                create_feature_270_markdown_file(str(tmp_path))
            except Exception:
                pass

            captured = capsys.readouterr()
            assert "270" in captured.out or "270" in captured.err


class TestPhase4Integration:
    """Integration tests for complete end-to-end workflow."""

    def test_complete_workflow_success(self, tmp_path, monkeypatch):
        """Test complete successful workflow from start to finish."""
        mock_generate = Mock(return_value=SAMPLE_MARKDOWN)
        mock_write = Mock(return_value=str(tmp_path / MARKDOWN_FILENAME))
        mock_validate = Mock()
        mock_commit = Mock(
            return_value=f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
        )
        mock_push = Mock(return_value="Pushed to remote")

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

            # Verify all functions were called
            mock_generate.assert_called_once()
            mock_write.assert_called_once()
            mock_validate.assert_called_once()
            mock_commit.assert_called_once()
            mock_push.assert_called_once()

            # Verify result is correct
            assert result["filepath"] == str(tmp_path / MARKDOWN_FILENAME)
            assert result["content"] == SAMPLE_MARKDOWN
            assert result["commit_message"]
            assert result["push_result"] == "Pushed to remote"

    def test_repo_path_parameter_is_optional(self, tmp_path, monkeypatch):
        """Test that repo_path parameter is optional and defaults to cwd."""
        mock_generate = Mock(return_value=SAMPLE_MARKDOWN)
        mock_write = Mock(return_value=str(tmp_path / MARKDOWN_FILENAME))
        mock_validate = Mock()
        mock_commit = Mock(return_value="Commit message")
        mock_push = Mock(return_value="Push result")

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
            # Call without repo_path parameter
            result = create_feature_270_markdown_file()

            assert result is not None

    def test_repo_path_parameter_is_passed_correctly(self, tmp_path, monkeypatch):
        """Test that repo_path parameter is passed to git functions."""
        custom_repo_path = str(tmp_path)
        mock_generate = Mock(return_value=SAMPLE_MARKDOWN)
        mock_write = Mock(return_value=str(tmp_path / MARKDOWN_FILENAME))
        mock_validate = Mock()
        mock_commit = Mock(return_value="Commit message")
        mock_push = Mock(return_value="Push result")

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
            result = create_feature_270_markdown_file(custom_repo_path)

            # Verify commit received repo_path
            commit_call = mock_commit.call_args
            assert commit_call[0][2] == custom_repo_path  # repo_path is 3rd positional arg

            # Verify push received repo_path
            push_call = mock_push.call_args
            assert push_call[0][0] == custom_repo_path  # repo_path is 1st arg


class TestPhase4Logging:
    """Tests for structured logging during orchestration."""

    def test_feature_creation_is_logged_at_start(self, tmp_path, monkeypatch, capsys):
        """Test that feature creation is logged at the start of execution."""
        mock_generate = Mock(return_value=SAMPLE_MARKDOWN)
        mock_write = Mock(return_value=str(tmp_path / MARKDOWN_FILENAME))
        mock_validate = Mock()
        mock_commit = Mock(return_value="Commit message")
        mock_push = Mock(return_value="Push result")

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
            create_feature_270_markdown_file(str(tmp_path))

            captured = capsys.readouterr()
            assert "Creating feature 270 markdown file" in captured.out

    def test_success_is_logged_at_end(self, tmp_path, monkeypatch, capsys):
        """Test that successful completion is logged at the end."""
        mock_generate = Mock(return_value=SAMPLE_MARKDOWN)
        mock_write = Mock(return_value=str(tmp_path / MARKDOWN_FILENAME))
        mock_validate = Mock()
        mock_commit = Mock(return_value="Commit message")
        mock_push = Mock(return_value="Push result")

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
            create_feature_270_markdown_file(str(tmp_path))

            captured = capsys.readouterr()
            assert "Successfully created and published feature 270" in captured.out

    def test_each_task_step_is_logged(self, tmp_path, monkeypatch, capsys):
        """Test that each of the 5 task steps is logged."""
        mock_generate = Mock(return_value=SAMPLE_MARKDOWN)
        mock_write = Mock(return_value=str(tmp_path / MARKDOWN_FILENAME))
        mock_validate = Mock()
        mock_commit = Mock(return_value="Commit message")
        mock_push = Mock(return_value="Push result")

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
            create_feature_270_markdown_file(str(tmp_path))

            captured = capsys.readouterr()
            assert "Task 1: Generating markdown content" in captured.out
            assert "Task 2: Writing markdown file to disk" in captured.out
            assert "Task 3: Validating markdown file" in captured.out
            assert "Task 4: Staging and committing file" in captured.out
            assert "Task 5: Pushing to remote repository" in captured.out
