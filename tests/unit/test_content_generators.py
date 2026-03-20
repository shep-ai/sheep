"""Unit tests for content generators module, focusing on feature number extraction."""

import os
from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import (
    get_feature_number,
    commit_markdown_file,
    create_markdown_file,
)


class TestGetFeatureNumber:
    """Tests for get_feature_number() feature number extraction."""

    def test_extracts_feature_number_from_branch_with_number(self):
        """Test that get_feature_number() extracts number from branch name like feat/126-..."""
        with patch("sheep.content_generators.Repo") as mock_repo:
            mock_repo_instance = MagicMock()
            mock_repo_instance.head.ref.name = "feat/126-markdown-file-create-e7da08"
            mock_repo.return_value = mock_repo_instance

            result = get_feature_number()
            assert result == 126, "Should extract 126 from feat/126-markdown-file-create-e7da08"

    def test_extracts_feature_number_from_various_branches(self):
        """Test feature number extraction from different branch name formats."""
        test_cases = [
            ("feat/1-something", 1),
            ("feat/99-test", 99),
            ("feat/100-feature-name", 100),
            ("feat/999-very-long-feature-name-here", 999),
        ]

        for branch_name, expected_number in test_cases:
            with patch("sheep.content_generators.Repo") as mock_repo:
                mock_repo_instance = MagicMock()
                mock_repo_instance.head.ref.name = branch_name
                mock_repo.return_value = mock_repo_instance

                result = get_feature_number()
                assert result == expected_number, (
                    f"Should extract {expected_number} from {branch_name}, got {result}"
                )

    def test_falls_back_to_environment_variable_when_branch_no_number(self):
        """Test that get_feature_number() falls back to FEATURE_NUMBER env var."""
        with patch("sheep.content_generators.Repo") as mock_repo, patch.dict(
            os.environ, {"FEATURE_NUMBER": "126"}, clear=False
        ):
            mock_repo_instance = MagicMock()
            # Branch name without a number
            mock_repo_instance.head.ref.name = "feat/markdown-file-create-e7da08"
            mock_repo.return_value = mock_repo_instance

            result = get_feature_number()
            assert result == 126, "Should fall back to FEATURE_NUMBER env var"

    def test_returns_none_when_no_number_found(self):
        """Test that get_feature_number() returns None when feature number cannot be extracted."""
        with patch("sheep.content_generators.Repo") as mock_repo, patch.dict(
            os.environ, {}, clear=True
        ):
            mock_repo_instance = MagicMock()
            mock_repo_instance.head.ref.name = "feat/markdown-file-create-e7da08"
            mock_repo.return_value = mock_repo_instance

            result = get_feature_number()
            assert result is None, "Should return None when no feature number found"

    def test_handles_detached_head_state(self):
        """Test that get_feature_number() handles detached HEAD gracefully."""
        with patch("sheep.content_generators.Repo") as mock_repo, patch.dict(
            os.environ, {"FEATURE_NUMBER": "126"}, clear=False
        ):
            mock_repo_instance = MagicMock()
            # Simulate detached HEAD (raise error when accessing head.ref)
            mock_repo_instance.head.ref.name = "HEAD detached at abc123"
            mock_repo.return_value = mock_repo_instance

            result = get_feature_number()
            # Should fall back to env var since branch name doesn't have pattern
            assert result == 126, "Should fall back to env var in detached HEAD state"

    def test_env_var_takes_precedence_when_invalid(self):
        """Test that FEATURE_NUMBER env var is used when branch name doesn't match pattern."""
        with patch("sheep.content_generators.Repo") as mock_repo, patch.dict(
            os.environ, {"FEATURE_NUMBER": "200"}, clear=False
        ):
            mock_repo_instance = MagicMock()
            mock_repo_instance.head.ref.name = "main"  # No pattern match
            mock_repo.return_value = mock_repo_instance

            result = get_feature_number()
            assert result == 200, "Should use FEATURE_NUMBER env var when branch has no pattern"


class TestCommitMarkdownFileWithFeatureNumber:
    """Tests for commit_markdown_file() with feature number parameter."""

    @patch("sheep.content_generators.GitCommitTool")
    @patch("sheep.content_generators.get_feature_number")
    def test_includes_feature_number_when_provided(self, mock_get_feature, mock_git_tool):
        """Test that commit_markdown_file() includes feature number in message when provided."""
        mock_git_tool_instance = MagicMock()
        mock_git_tool_instance._run.return_value = "Committed: feat(126): ..."
        mock_git_tool.return_value = mock_git_tool_instance

        content = "# Test Title\n\nSentence one. Sentence two.\n"
        filepath = "/repo/test.md"

        result = commit_markdown_file(filepath, content, feature_number=126)

        # Check that the tool was called with the right message
        call_args = mock_git_tool_instance._run.call_args
        assert call_args is not None, "GitCommitTool._run should be called"

        message = call_args.kwargs.get("message") or call_args[1].get("message")
        assert "feat(126):" in message, (
            f"Commit message should include 'feat(126):', got: {message}"
        )

    @patch("sheep.content_generators.GitCommitTool")
    @patch("sheep.content_generators.get_feature_number")
    def test_calls_get_feature_number_when_not_provided(self, mock_get_feature, mock_git_tool):
        """Test that commit_markdown_file() calls get_feature_number() when not provided."""
        mock_get_feature.return_value = 126
        mock_git_tool_instance = MagicMock()
        mock_git_tool_instance._run.return_value = "Committed: feat(126): ..."
        mock_git_tool.return_value = mock_git_tool_instance

        content = "# Test Title\n\nSentence one. Sentence two.\n"
        filepath = "/repo/test.md"

        result = commit_markdown_file(filepath, content)

        # Check that get_feature_number was called
        mock_get_feature.assert_called_once()

        # Check that the message includes the feature number
        call_args = mock_git_tool_instance._run.call_args
        message = call_args.kwargs.get("message") or call_args[1].get("message")
        assert "feat(126):" in message, (
            f"Commit message should include 'feat(126):', got: {message}"
        )

    @patch("sheep.content_generators.GitCommitTool")
    @patch("sheep.content_generators.get_feature_number")
    def test_uses_custom_message_if_provided(self, mock_get_feature, mock_git_tool):
        """Test that custom_message parameter still takes precedence."""
        mock_git_tool_instance = MagicMock()
        mock_git_tool_instance._run.return_value = "Committed: custom message"
        mock_git_tool.return_value = mock_git_tool_instance

        content = "# Test Title\n\nSentence one. Sentence two.\n"
        filepath = "/repo/test.md"
        custom_message = "custom: My custom commit message"

        result = commit_markdown_file(
            filepath, content, feature_number=126, custom_message=custom_message
        )

        # Check that the custom message was used
        call_args = mock_git_tool_instance._run.call_args
        message = call_args.kwargs.get("message") or call_args[1].get("message")
        assert message == custom_message, (
            f"Should use custom_message when provided, got: {message}"
        )


class TestCreateMarkdownFileWithFeatureNumber:
    """Tests for create_markdown_file() with feature number parameter."""

    @patch("sheep.content_generators.push_markdown_file")
    @patch("sheep.content_generators.commit_markdown_file")
    @patch("sheep.content_generators.validate_markdown_file")
    @patch("sheep.content_generators.write_markdown_file")
    @patch("sheep.content_generators.generate_markdown_content")
    @patch("sheep.content_generators.get_feature_number")
    def test_passes_feature_number_to_commit(
        self,
        mock_get_feature,
        mock_gen_content,
        mock_write_file,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that create_markdown_file() passes feature number to commit_markdown_file()."""
        test_content = "# Test\n\nOne. Two.\n"
        test_path = "/repo/test.md"

        mock_gen_content.return_value = test_content
        mock_write_file.return_value = test_path
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"
        mock_get_feature.return_value = 126

        result = create_markdown_file("test.md", feature_number=126)

        # Check that commit was called with feature_number
        mock_commit.assert_called_once()
        call_args = mock_commit.call_args

        # Check if feature_number was passed
        assert call_args.kwargs.get("feature_number") == 126 or (
            len(call_args[0]) > 2 and call_args[0][2] == 126
        ), "create_markdown_file should pass feature_number to commit_markdown_file"

    @patch("sheep.content_generators.push_markdown_file")
    @patch("sheep.content_generators.commit_markdown_file")
    @patch("sheep.content_generators.validate_markdown_file")
    @patch("sheep.content_generators.write_markdown_file")
    @patch("sheep.content_generators.generate_markdown_content")
    @patch("sheep.content_generators.get_feature_number")
    def test_extracts_feature_number_when_not_provided(
        self,
        mock_get_feature,
        mock_gen_content,
        mock_write_file,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that create_markdown_file() extracts feature number when not provided."""
        test_content = "# Test\n\nOne. Two.\n"
        test_path = "/repo/test.md"

        mock_gen_content.return_value = test_content
        mock_write_file.return_value = test_path
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"
        mock_get_feature.return_value = 126

        result = create_markdown_file("test.md")

        # Check that get_feature_number was called
        mock_get_feature.assert_called()

    @patch("sheep.content_generators.push_markdown_file")
    @patch("sheep.content_generators.commit_markdown_file")
    @patch("sheep.content_generators.validate_markdown_file")
    @patch("sheep.content_generators.write_markdown_file")
    @patch("sheep.content_generators.generate_markdown_content")
    @patch("sheep.content_generators.get_feature_number")
    def test_return_value_includes_correct_commit_message(
        self,
        mock_get_feature,
        mock_gen_content,
        mock_write_file,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that returned commit message includes feature number."""
        test_content = "# Test Topic\n\nOne sentence. Two sentences.\n"
        test_path = "/repo/test.md"

        mock_gen_content.return_value = test_content
        mock_write_file.return_value = test_path
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"
        mock_get_feature.return_value = 126

        result = create_markdown_file("test.md", feature_number=126)

        # Check that commit_message includes feature number
        assert "feat(126):" in result["commit_message"], (
            f"Return commit_message should include 'feat(126):', got: {result['commit_message']}"
        )
        assert "test.md" in result["commit_message"], (
            f"Return commit_message should include filename, got: {result['commit_message']}"
        )
