"""Tests for git operations (commit and push) for markdown files."""

import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import (
    commit_markdown_file,
    create_markdown_file,
    extract_topic_from_content,
    push_markdown_file,
)


class TestExtractTopicFromContent:
    """Tests for extracting topic from markdown content."""

    def test_extracts_topic_from_h1_heading(self):
        """Test that topic is correctly extracted from H1 heading."""
        content = (
            "# Machine Learning\n\n"
            "ML is powerful. It learns from data. Models improve with practice.\n"
        )
        topic = extract_topic_from_content(content)
        assert topic == "Machine Learning"

    def test_strips_leading_and_trailing_whitespace(self):
        """Test that extracted topic is stripped of whitespace."""
        content = (
            "#   Distributed Systems   \n\n"
            "Systems scale. They handle failures. Coordination is key.\n"
        )
        topic = extract_topic_from_content(content)
        assert topic == "Distributed Systems"

    def test_rejects_missing_h1_heading(self):
        """Test that missing H1 heading raises error."""
        content = "## Second Level\n\nNo heading. One sentence. Two sentences.\n"
        with pytest.raises(ValueError, match="H1 heading"):
            extract_topic_from_content(content)

    def test_rejects_empty_h1_heading(self):
        """Test that empty H1 heading raises error."""
        content = "# \n\nContent. Here. Now.\n"
        with pytest.raises(ValueError, match="empty"):
            extract_topic_from_content(content)

    def test_handles_special_characters_in_topic(self):
        """Test that topics with special characters are handled correctly."""
        content = (
            "# C++ & Templates\n\n"
            "Templates enable. Generic programming works. Type safety matters.\n"
        )
        topic = extract_topic_from_content(content)
        assert topic == "C++ & Templates"


class TestCommitMarkdownFile:
    """Tests for committing markdown files with git."""

    @patch("sheep.content_generators.GitCommitTool")
    def test_calls_git_commit_tool(self, mock_git_commit):
        """Test that GitCommitTool is called with correct parameters."""
        mock_tool_instance = MagicMock()
        mock_tool_instance._run.return_value = "Committed: test message"
        mock_git_commit.return_value = mock_tool_instance

        filepath = "/path/to/test.md"
        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        repo_path = "/repo"

        result = commit_markdown_file(filepath, content, repo_path)

        # Verify GitCommitTool was instantiated
        mock_git_commit.assert_called_once()

        # Verify _run was called with correct parameters
        assert mock_tool_instance._run.called
        call_args = mock_tool_instance._run.call_args
        assert call_args.kwargs["repo_path"] == repo_path
        assert call_args.kwargs["add_all"] is True
        assert "feat: Create test.md" in call_args.kwargs["message"]

    @patch("sheep.content_generators.GitCommitTool")
    def test_commit_message_includes_topic(self, mock_git_commit):
        """Test that commit message includes the topic extracted from content."""
        mock_tool_instance = MagicMock()
        mock_tool_instance._run.return_value = "Committed"
        mock_git_commit.return_value = mock_tool_instance

        filepath = "/path/to/test.md"
        content = (
            "# Quantum Computing\n\n"
            "Quantum computers leverage. Superposition enables. "
            "Entanglement matters.\n"
        )
        repo_path = "/repo"

        commit_markdown_file(filepath, content, repo_path)

        # Verify commit message contains topic
        call_args = mock_tool_instance._run.call_args
        message = call_args.kwargs["message"]
        assert "Quantum Computing" in message
        assert "feat: Create test.md" in message

    @patch("sheep.content_generators.GitCommitTool")
    def test_uses_current_directory_as_default_repo_path(self, mock_git_commit):
        """Test that current directory is used when repo_path is not specified."""
        mock_tool_instance = MagicMock()
        mock_tool_instance._run.return_value = "Committed"
        mock_git_commit.return_value = mock_tool_instance

        filepath = "/path/to/test.md"
        content = "# Test\n\nOne. Two. Three.\n"

        commit_markdown_file(filepath, content, repo_path=None)

        # Verify _run was called with current working directory
        call_args = mock_tool_instance._run.call_args
        assert call_args.kwargs["repo_path"] == str(Path.cwd())

    @patch("sheep.content_generators.GitCommitTool")
    def test_returns_commit_result(self, mock_git_commit):
        """Test that the commit result is returned."""
        expected_result = "Committed: feat: Create test.md markdown file with Test content\n..."
        mock_tool_instance = MagicMock()
        mock_tool_instance._run.return_value = expected_result
        mock_git_commit.return_value = mock_tool_instance

        filepath = "/path/to/test.md"
        content = "# Test\n\nOne. Two. Three.\n"
        repo_path = "/repo"

        result = commit_markdown_file(filepath, content, repo_path)

        assert result == expected_result

    def test_raises_error_on_invalid_content(self):
        """Test that error is raised if content has no H1 heading."""
        filepath = "/path/to/test.md"
        content = "## No H1 heading\n\nOne. Two. Three.\n"
        repo_path = "/repo"

        with pytest.raises(ValueError, match="H1 heading"):
            commit_markdown_file(filepath, content, repo_path)


class TestPushMarkdownFile:
    """Tests for pushing markdown files to remote."""

    @patch("sheep.content_generators.GitPushTool")
    def test_calls_git_push_tool(self, mock_git_push):
        """Test that GitPushTool is called with correct parameters."""
        mock_tool_instance = MagicMock()
        mock_tool_instance._run.return_value = "Pushed to origin/branch"
        mock_git_push.return_value = mock_tool_instance

        repo_path = "/repo"

        result = push_markdown_file(repo_path)

        # Verify GitPushTool was instantiated
        mock_git_push.assert_called_once()

        # Verify _run was called with correct parameters
        assert mock_tool_instance._run.called
        call_args = mock_tool_instance._run.call_args
        assert call_args.kwargs["repo_path"] == repo_path
        assert call_args.kwargs["remote"] == "origin"
        assert call_args.kwargs["set_upstream"] is True

    @patch("sheep.content_generators.GitPushTool")
    def test_uses_current_directory_as_default_repo_path(self, mock_git_push):
        """Test that current directory is used when repo_path is not specified."""
        mock_tool_instance = MagicMock()
        mock_tool_instance._run.return_value = "Pushed"
        mock_git_push.return_value = mock_tool_instance

        push_markdown_file(repo_path=None)

        # Verify _run was called with current working directory
        call_args = mock_tool_instance._run.call_args
        assert call_args.kwargs["repo_path"] == str(Path.cwd())

    @patch("sheep.content_generators.GitPushTool")
    def test_uses_specified_remote(self, mock_git_push):
        """Test that specified remote is used."""
        mock_tool_instance = MagicMock()
        mock_tool_instance._run.return_value = "Pushed"
        mock_git_push.return_value = mock_tool_instance

        repo_path = "/repo"
        remote = "upstream"

        push_markdown_file(repo_path, remote)

        # Verify remote parameter was passed
        call_args = mock_tool_instance._run.call_args
        assert call_args.kwargs["remote"] == "upstream"

    @patch("sheep.content_generators.GitPushTool")
    def test_returns_push_result(self, mock_git_push):
        """Test that the push result is returned."""
        expected_result = "Pushed to origin/feat-test\n..."
        mock_tool_instance = MagicMock()
        mock_tool_instance._run.return_value = expected_result
        mock_git_push.return_value = mock_tool_instance

        repo_path = "/repo"

        result = push_markdown_file(repo_path)

        assert result == expected_result


class TestCreateMarkdownFileOrchestration:
    """Integration tests for the complete create_markdown_file workflow."""

    @patch("sheep.content_generators.push_markdown_file")
    @patch("sheep.content_generators.commit_markdown_file")
    @patch("sheep.content_generators.validate_markdown_file")
    @patch("sheep.content_generators.write_markdown_file")
    @patch("sheep.content_generators.generate_markdown_content")
    def test_orchestrates_complete_workflow(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that create_markdown_file orchestrates all steps correctly."""
        # Setup mocks
        test_content = "# Test Topic\n\nFirst sentence. Second sentence. Third sentence.\n"
        mock_generate.return_value = test_content
        mock_write.return_value = "/repo/test.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed successfully"
        mock_push.return_value = "Pushed successfully"

        # Call the orchestration function
        result = create_markdown_file("test.md", "/repo")

        # Verify all functions were called
        mock_generate.assert_called_once()
        mock_write.assert_called_once_with(test_content, "test.md")
        mock_validate.assert_called_once_with("/repo/test.md")
        mock_commit.assert_called_once()
        mock_push.assert_called_once()

        # Verify result contains expected keys
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

    @patch("sheep.content_generators.push_markdown_file")
    @patch("sheep.content_generators.commit_markdown_file")
    @patch("sheep.content_generators.validate_markdown_file")
    @patch("sheep.content_generators.write_markdown_file")
    @patch("sheep.content_generators.generate_markdown_content")
    def test_returns_all_required_information(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that create_markdown_file returns all required information."""
        # Setup mocks
        test_content = (
            "# Artificial Intelligence\n\n"
            "AI is transforming. Technology advances rapidly. "
            "Innovation continues.\n"
        )
        mock_generate.return_value = test_content
        mock_write.return_value = "/repo/test-ai.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call the function
        result = create_markdown_file("test-ai.md", "/repo")

        # Verify all required keys are present
        assert result["filepath"] == "/repo/test-ai.md"
        assert result["content"] == test_content
        assert "feat: Create test-ai.md" in result["commit_message"]
        assert "Artificial Intelligence" in result["commit_message"]
        assert result["push_result"] == "Pushed"

    @patch("sheep.content_generators.push_markdown_file")
    @patch("sheep.content_generators.commit_markdown_file")
    @patch("sheep.content_generators.validate_markdown_file")
    @patch("sheep.content_generators.write_markdown_file")
    @patch("sheep.content_generators.generate_markdown_content")
    def test_uses_current_directory_by_default(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that current directory is used when repo_path is not specified."""
        # Setup mocks
        test_content = "# Test\n\nOne. Two. Three.\n"
        mock_generate.return_value = test_content
        mock_write.return_value = "test.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call without repo_path
        create_markdown_file("test.md", repo_path=None)

        # Verify commit_markdown_file was called with current directory
        call_args = mock_commit.call_args
        assert call_args[0][2] == str(Path.cwd())

    @patch("sheep.content_generators.generate_markdown_content")
    def test_propagates_generation_errors(self, mock_generate):
        """Test that errors during content generation are propagated."""
        mock_generate.side_effect = Exception("LLM API failed")

        with pytest.raises(Exception, match="LLM API failed"):
            create_markdown_file("test.md", "/repo")

    @patch("sheep.content_generators.write_markdown_file")
    @patch("sheep.content_generators.generate_markdown_content")
    def test_propagates_write_errors(self, mock_generate, mock_write):
        """Test that errors during file writing are propagated."""
        test_content = "# Test\n\nOne. Two. Three.\n"
        mock_generate.return_value = test_content
        mock_write.side_effect = OSError("Permission denied")

        with pytest.raises(IOError, match="Permission denied"):
            create_markdown_file("test.md", "/repo")

    @patch("sheep.content_generators.validate_markdown_file")
    @patch("sheep.content_generators.write_markdown_file")
    @patch("sheep.content_generators.generate_markdown_content")
    def test_propagates_validation_errors(self, mock_generate, mock_write, mock_validate):
        """Test that errors during validation are propagated."""
        test_content = "# Test\n\nOne. Two. Three.\n"
        mock_generate.return_value = test_content
        mock_write.return_value = "/repo/test.md"
        mock_validate.side_effect = ValueError("Invalid markdown format")

        with pytest.raises(ValueError, match="Invalid markdown format"):
            create_markdown_file("test.md", "/repo")

    @patch("sheep.content_generators.commit_markdown_file")
    @patch("sheep.content_generators.validate_markdown_file")
    @patch("sheep.content_generators.write_markdown_file")
    @patch("sheep.content_generators.generate_markdown_content")
    def test_propagates_commit_errors(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
    ):
        """Test that errors during commit are propagated."""
        test_content = "# Test\n\nOne. Two. Three.\n"
        mock_generate.return_value = test_content
        mock_write.return_value = "/repo/test.md"
        mock_validate.return_value = True
        mock_commit.side_effect = Exception("Git commit failed")

        with pytest.raises(Exception, match="Git commit failed"):
            create_markdown_file("test.md", "/repo")

    @patch("sheep.content_generators.push_markdown_file")
    @patch("sheep.content_generators.commit_markdown_file")
    @patch("sheep.content_generators.validate_markdown_file")
    @patch("sheep.content_generators.write_markdown_file")
    @patch("sheep.content_generators.generate_markdown_content")
    def test_propagates_push_errors(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that errors during push are propagated."""
        test_content = "# Test\n\nOne. Two. Three.\n"
        mock_generate.return_value = test_content
        mock_write.return_value = "/repo/test.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.side_effect = Exception("Git push failed")

        with pytest.raises(Exception, match="Git push failed"):
            create_markdown_file("test.md", "/repo")


class TestIntegrationWithRealGit:
    """Integration tests with real git repository (not mocked)."""

    def test_full_workflow_with_real_git_repo(self):
        """Test the complete workflow with a real git repository."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)

            # Initialize a git repo
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Configure git user for commits
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Create initial commit
            (repo_path / "README.md").write_text("# Test Repo\n")
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )

            # Change to the repo directory for file operations
            original_cwd = Path.cwd()
            try:
                os.chdir(repo_path)

                # Mock only the LLM call, use real file and git operations
                with patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
                    mock_llm_instance = MagicMock()
                    mock_llm_instance.call.return_value = {
                        "content": (
                            "# Distributed Systems\n\n"
                            "Systems scale across nodes. They tolerate failures. "
                            "Coordination ensures consistency.\n"
                        )
                    }
                    mock_llm.return_value = mock_llm_instance

                    # Create the markdown file
                    result = create_markdown_file("test-integration.md", str(repo_path))

                    # Verify file was created
                    test_file = repo_path / "test-integration.md"
                    assert test_file.exists()
                    assert test_file.is_file()

                    # Verify file content
                    content = test_file.read_text(encoding="utf-8")
                    assert content.startswith("# Distributed Systems")
                    assert "Systems scale across nodes" in content

                    # Verify git status shows committed
                    status_result = subprocess.run(
                        ["git", "status", "--porcelain"],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    # Should be empty (nothing staged or modified)
                    assert status_result.stdout.strip() == ""

                    # Verify git log shows the commit
                    log_result = subprocess.run(
                        ["git", "log", "--oneline", "-1"],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    assert "Distributed Systems" in log_result.stdout

                    # Verify result contains expected keys
                    assert "filepath" in result
                    assert "content" in result
                    assert "commit_message" in result
                    assert "push_result" in result

            finally:
                os.chdir(original_cwd)
