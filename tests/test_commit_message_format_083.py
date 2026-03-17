"""Tests for feature 083 commit message format matching specification FR-7."""

from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import commit_markdown_file


class TestCommitMessageFormatFeature083:
    """Tests for commit message format matching specification FR-7."""

    @patch("sheep.content_generators.GitCommitTool")
    def test_commit_message_format_matches_spec_fr7(self, mock_git_commit):
        """Test that commit message matches spec FR-7: feat(083): create markdown file {filename} with prose content."""
        mock_tool_instance = MagicMock()
        mock_tool_instance._run.return_value = "Committed successfully"
        mock_git_commit.return_value = mock_tool_instance

        filepath = "/path/to/test-szyfny.md"
        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        repo_path = "/repo"

        commit_markdown_file(filepath, content, repo_path)

        # Verify commit message matches spec format exactly
        call_args = mock_tool_instance._run.call_args
        message = call_args.kwargs["message"]

        # Should be: feat(083): create markdown file test-szyfny.md with prose content
        assert message == "feat(083): create markdown file test-szyfny.md with prose content"

    @patch("sheep.content_generators.GitCommitTool")
    def test_commit_message_includes_feature_number_in_parentheses(self, mock_git_commit):
        """Test that feature number 083 is in parentheses as per conventional commits convention."""
        mock_tool_instance = MagicMock()
        mock_tool_instance._run.return_value = "Committed"
        mock_git_commit.return_value = mock_tool_instance

        filepath = "/path/to/test.md"
        content = "# Topic\n\nFirst. Second. Third.\n"
        repo_path = "/repo"

        commit_markdown_file(filepath, content, repo_path)

        call_args = mock_tool_instance._run.call_args
        message = call_args.kwargs["message"]

        # Check feature number is in parentheses
        assert message.startswith("feat(083):")

    @patch("sheep.content_generators.GitCommitTool")
    def test_commit_message_uses_lowercase_create(self, mock_git_commit):
        """Test that commit message uses lowercase 'create' not 'Create'."""
        mock_tool_instance = MagicMock()
        mock_tool_instance._run.return_value = "Committed"
        mock_git_commit.return_value = mock_tool_instance

        filepath = "/path/to/test.md"
        content = "# Topic\n\nFirst. Second. Third.\n"
        repo_path = "/repo"

        commit_markdown_file(filepath, content, repo_path)

        call_args = mock_tool_instance._run.call_args
        message = call_args.kwargs["message"]

        # Should use lowercase 'create'
        assert "create markdown file" in message
        assert "Create" not in message

    @patch("sheep.content_generators.GitCommitTool")
    def test_commit_message_does_not_include_topic(self, mock_git_commit):
        """Test that commit message does not include topic name, uses 'with prose content' instead."""
        mock_tool_instance = MagicMock()
        mock_tool_instance._run.return_value = "Committed"
        mock_git_commit.return_value = mock_tool_instance

        filepath = "/path/to/test.md"
        topic_name = "Quantum Computing"
        content = f"# {topic_name}\n\nFirst. Second. Third.\n"
        repo_path = "/repo"

        commit_markdown_file(filepath, content, repo_path)

        call_args = mock_tool_instance._run.call_args
        message = call_args.kwargs["message"]

        # Should NOT include the topic name
        assert "Quantum Computing" not in message
        # Should use the generic "with prose content"
        assert "with prose content" in message

    @patch("sheep.content_generators.GitCommitTool")
    def test_commit_message_includes_filename(self, mock_git_commit):
        """Test that commit message includes the markdown filename."""
        mock_tool_instance = MagicMock()
        mock_tool_instance._run.return_value = "Committed"
        mock_git_commit.return_value = mock_tool_instance

        filepath = "/path/to/test-szyfny.md"
        content = "# Any Title\n\nFirst. Second. Third.\n"
        repo_path = "/repo"

        commit_markdown_file(filepath, content, repo_path)

        call_args = mock_tool_instance._run.call_args
        message = call_args.kwargs["message"]

        # Should include the filename
        assert "test-szyfny.md" in message

    @patch("sheep.content_generators.GitCommitTool")
    def test_commit_message_format_with_different_filenames(self, mock_git_commit):
        """Test that commit message format works with different filenames."""
        mock_tool_instance = MagicMock()
        mock_tool_instance._run.return_value = "Committed"
        mock_git_commit.return_value = mock_tool_instance

        # Test with various filenames
        test_cases = [
            "test-abc123.md",
            "test-xyz789.md",
            "test-8lzq5l.md",
        ]

        for filename in test_cases:
            filepath = f"/path/to/{filename}"
            content = "# Title\n\nFirst. Second. Third.\n"
            repo_path = "/repo"

            commit_markdown_file(filepath, content, repo_path)

            call_args = mock_tool_instance._run.call_args
            message = call_args.kwargs["message"]

            # Verify format: feat(083): create markdown file {filename} with prose content
            expected = f"feat(083): create markdown file {filename} with prose content"
            assert message == expected
