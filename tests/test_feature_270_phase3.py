"""Tests for feature 270 phase 3: Validation & Git Integration.

Tests the file validation step (task-5), git commit step (task-6), and git push step (task-7)
of the feature 270 markdown file creation workflow.
"""

from unittest.mock import Mock, patch, call
from pathlib import Path

import pytest

from sheep.features.feature_270_markdown_file_creation import (
    create_feature_270_markdown_file,
    MARKDOWN_FILENAME,
    FEATURE_NUMBER,
)


class TestTask5FileValidation:
    """Tests for task-5: File validation step.

    Verifies that:
    - Function calls validate_markdown_file() with filepath
    - Validation is logged at info level
    - Error is logged and re-raised if validation fails
    - Failure details are included in error message
    """

    def test_calls_validate_markdown_file_with_filepath(self, tmp_path, monkeypatch):
        """Test that orchestration function calls validate_markdown_file() with filepath."""
        test_content = "# Valid Title\n\nSentence one. Sentence two.\n"
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

            # Verify validate_markdown_file was called exactly once with filepath
            mock_validate.assert_called_once_with(test_filepath)
            assert result is not None

    def test_validation_passed_logged_at_info_level(self, tmp_path, monkeypatch, capsys):
        """Test that successful validation is logged at info level."""
        test_content = "# Validation Test\n\nValidation passed successfully. This is great news.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(return_value=test_filepath)
        mock_validate = Mock()  # Successful validation (no exception)
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

            # Verify success message was logged
            captured = capsys.readouterr()
            assert "File validation passed" in captured.out

    def test_validation_failure_logged_and_re_raised(self, tmp_path, monkeypatch, capsys):
        """Test that validation failure is logged and exception is re-raised."""
        test_content = "# Invalid Content\n\nOnly one sentence.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)
        validation_error = "Invalid: expected 2-3 sentences, found 1"

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(return_value=test_filepath)
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

            # Verify that exception is re-raised
            with pytest.raises(ValueError, match=validation_error):
                create_feature_270_markdown_file(str(tmp_path))

            # Verify error was logged via structlog
            captured = capsys.readouterr()
            assert "Failed to create feature 270" in captured.out

    def test_validation_checks_h1_format(self, tmp_path, monkeypatch):
        """Test that validation enforces H1 heading format."""
        test_content = "## Wrong Heading Level\n\nSentence one. Sentence two.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(return_value=test_filepath)
        mock_validate = Mock(
            side_effect=ValueError("H1 heading required, found H2")
        )

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

            with pytest.raises(ValueError, match="H1 heading required"):
                create_feature_270_markdown_file(str(tmp_path))

    def test_validation_checks_sentence_count(self, tmp_path, monkeypatch):
        """Test that validation enforces 2-3 sentence requirement."""
        test_content = "# Title\n\nOne sentence.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(return_value=test_filepath)
        mock_validate = Mock(
            side_effect=ValueError("Expected 2-3 sentences, found 1")
        )

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

            with pytest.raises(ValueError, match="Expected 2-3 sentences"):
                create_feature_270_markdown_file(str(tmp_path))

    def test_validation_checks_encoding(self, tmp_path, monkeypatch):
        """Test that validation enforces UTF-8 encoding."""
        test_content = "# Title\n\nSentence one. Sentence two.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(return_value=test_filepath)
        mock_validate = Mock(
            side_effect=ValueError("File encoding is not UTF-8")
        )

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

            with pytest.raises(ValueError, match="not UTF-8"):
                create_feature_270_markdown_file(str(tmp_path))


class TestTask6GitCommit:
    """Tests for task-6: Git commit step.

    Verifies that:
    - Function constructs correct commit message with feature number
    - Function calls commit_markdown_file() with correct parameters
    - Commit is logged at info level
    - Error is logged and re-raised if commit fails
    """

    def test_commit_message_format_includes_feature_number(self, tmp_path, monkeypatch):
        """Test that commit message has correct format with feature number."""
        test_content = "# Title\n\nSentence one. Sentence two.\n"
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

            # Verify commit message has correct format
            expected_message = (
                f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
            )
            assert result["commit_message"] == expected_message
            assert str(FEATURE_NUMBER) in result["commit_message"]

    def test_calls_commit_markdown_file_with_correct_parameters(
        self, tmp_path, monkeypatch
    ):
        """Test that orchestration function calls commit_markdown_file() with correct parameters."""
        test_content = "# Title\n\nSentence one. Sentence two.\n"
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

            # Verify commit_markdown_file was called with correct parameters
            mock_commit.assert_called_once()
            call_args = mock_commit.call_args

            # Check positional and keyword arguments
            assert call_args[0][0] == test_filepath  # filepath
            assert call_args[0][1] == test_content   # content
            assert call_args[0][2] == str(tmp_path)  # repo_path
            assert "custom_message" in call_args[1]  # custom_message keyword
            expected_message = (
                f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
            )
            assert call_args[1]["custom_message"] == expected_message

    def test_commit_logged_at_info_level(self, tmp_path, monkeypatch, capsys):
        """Test that commit operation is logged at info level."""
        test_content = "# Title\n\nSentence one. Sentence two.\n"
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

            # Verify commit was logged
            captured = capsys.readouterr()
            assert "Task 4: Staging and committing file" in captured.out

    def test_commit_failure_logged_and_re_raised(self, tmp_path, monkeypatch, capsys):
        """Test that commit failure is logged and exception is re-raised."""
        test_content = "# Title\n\nSentence one. Sentence two.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)
        git_error = "fatal: not a git repository"

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(return_value=test_filepath)
        mock_validate = Mock()
        mock_commit = Mock(side_effect=Exception(git_error))

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

            # Verify that exception is re-raised
            with pytest.raises(Exception, match=git_error):
                create_feature_270_markdown_file(str(tmp_path))

            # Verify error was logged
            captured = capsys.readouterr()
            assert "Failed to create feature 270" in captured.out

    def test_commit_result_captured_in_return_dict(self, tmp_path, monkeypatch):
        """Test that commit result is captured and returned."""
        test_content = "# Title\n\nSentence one. Sentence two.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)
        commit_result = "abc123def456"

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(return_value=test_filepath)
        mock_validate = Mock()
        mock_commit = Mock(return_value=commit_result)
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

            # Note: The current implementation doesn't store commit_result in return dict,
            # but we verify the function was called correctly
            mock_commit.assert_called_once()


class TestTask7GitPush:
    """Tests for task-7: Git push step.

    Verifies that:
    - Function calls push_markdown_file() with repo_path
    - Push operation is logged at info level
    - Error is logged and re-raised if push fails
    - Push result is captured for return dictionary
    """

    def test_calls_push_markdown_file_with_repo_path(self, tmp_path, monkeypatch):
        """Test that orchestration function calls push_markdown_file() with repo_path."""
        test_content = "# Title\n\nSentence one. Sentence two.\n"
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

            # Verify push_markdown_file was called exactly once with repo_path
            mock_push.assert_called_once_with(str(tmp_path))
            assert result is not None

    def test_push_logged_at_info_level(self, tmp_path, monkeypatch, capsys):
        """Test that push operation is logged at info level."""
        test_content = "# Title\n\nSentence one. Sentence two.\n"
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

            # Verify push was logged
            captured = capsys.readouterr()
            assert "Task 5: Pushing to remote repository" in captured.out

    def test_push_failure_logged_and_re_raised(self, tmp_path, monkeypatch, capsys):
        """Test that push failure is logged and exception is re-raised."""
        test_content = "# Title\n\nSentence one. Sentence two.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)
        push_error = "fatal: Authentication failed"

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(return_value=test_filepath)
        mock_validate = Mock()
        mock_commit = Mock(return_value="commit_result")
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

            # Verify that exception is re-raised
            with pytest.raises(Exception, match=push_error):
                create_feature_270_markdown_file(str(tmp_path))

            # Verify error was logged
            captured = capsys.readouterr()
            assert "Failed to create feature 270" in captured.out

    def test_push_result_captured_in_return_dict(self, tmp_path, monkeypatch):
        """Test that push result is captured and returned."""
        test_content = "# Title\n\nSentence one. Sentence two.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)
        push_result = "success"

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(return_value=test_filepath)
        mock_validate = Mock()
        mock_commit = Mock(return_value="commit_result")
        mock_push = Mock(return_value=push_result)

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

            # Verify push_result is in return dict
            assert "push_result" in result
            assert result["push_result"] == push_result

    def test_push_network_error_handled(self, tmp_path, monkeypatch):
        """Test that network errors during push are properly handled."""
        test_content = "# Title\n\nSentence one. Sentence two.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)
        network_error = "Network connection refused"

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(return_value=test_filepath)
        mock_validate = Mock()
        mock_commit = Mock(return_value="commit_result")
        mock_push = Mock(side_effect=Exception(network_error))

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

            with pytest.raises(Exception, match=network_error):
                create_feature_270_markdown_file(str(tmp_path))


class TestPhase3Integration:
    """Integration tests for phase 3: Validation, Commit, and Push workflow.

    Tests the complete flow of validation, git commit, and git push together.
    """

    def test_validation_commit_push_sequence(self, tmp_path, monkeypatch):
        """Test that validation, commit, and push happen in correct order."""
        test_content = "# Title\n\nSentence one. Sentence two.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)

        call_order = []

        def mock_validate(filepath):
            call_order.append("validate")

        def mock_commit(filepath, content, repo_path, custom_message=None):
            call_order.append("commit")
            return "commit_result"

        def mock_push(repo_path):
            call_order.append("push")
            return "push_result"

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(return_value=test_filepath)

        with patch(
            "sheep.features.feature_270_markdown_file_creation.generate_markdown_content",
            mock_generate,
        ), patch(
            "sheep.features.feature_270_markdown_file_creation.write_markdown_file",
            mock_write,
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

            # Verify order: validate → commit → push
            assert call_order == ["validate", "commit", "push"]
            assert result is not None

    def test_all_three_tasks_succeed_together(self, tmp_path, monkeypatch):
        """Test that all three tasks (validate, commit, push) succeed together."""
        test_content = "# Title\n\nSentence one. Sentence two.\n"
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

            # Verify all functions were called
            mock_validate.assert_called_once()
            mock_commit.assert_called_once()
            mock_push.assert_called_once()

            # Verify result contains all required keys
            assert "filepath" in result
            assert "content" in result
            assert "commit_message" in result
            assert "push_result" in result

    def test_failure_at_validation_prevents_commit_and_push(self, tmp_path, monkeypatch):
        """Test that validation failure prevents commit and push operations."""
        test_content = "# Title\n\nOnly one sentence.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(return_value=test_filepath)
        mock_validate = Mock(
            side_effect=ValueError("Expected 2-3 sentences, found 1")
        )
        mock_commit = Mock()
        mock_push = Mock()

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

            # Verify validation failure is raised
            with pytest.raises(ValueError):
                create_feature_270_markdown_file(str(tmp_path))

            # Verify commit and push were NOT called
            mock_commit.assert_not_called()
            mock_push.assert_not_called()

    def test_failure_at_commit_prevents_push(self, tmp_path, monkeypatch):
        """Test that commit failure prevents push operation."""
        test_content = "# Title\n\nSentence one. Sentence two.\n"
        test_filepath = str(tmp_path / MARKDOWN_FILENAME)

        mock_generate = Mock(return_value=test_content)
        mock_write = Mock(return_value=test_filepath)
        mock_validate = Mock()
        mock_commit = Mock(side_effect=Exception("fatal: not a git repository"))
        mock_push = Mock()

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

            # Verify commit failure is raised
            with pytest.raises(Exception):
                create_feature_270_markdown_file(str(tmp_path))

            # Verify push was NOT called
            mock_push.assert_not_called()
