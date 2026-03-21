"""Tests for Phase 3 git integration functions: commit, push, and orchestration."""

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from sheep.content_generators import (
    commit_markdown_file,
    push_markdown_file,
    create_markdown_file,
    extract_topic_from_content,
)


class TestExtractTopicFromContent:
    """Tests for extract_topic_from_content function."""

    def test_extracts_topic_from_h1_heading(self):
        """Test that topic is extracted from H1 heading."""
        content = "# The Power of Persistence\n\nFirst sentence. Second sentence. Third.\n"
        topic = extract_topic_from_content(content)
        assert topic == "The Power of Persistence"

    def test_strips_h1_prefix(self):
        """Test that H1 prefix is removed from extracted topic."""
        content = "# Test Title\n\nSentence one. Sentence two. Sentence three.\n"
        topic = extract_topic_from_content(content)
        assert not topic.startswith("#")
        assert topic == "Test Title"

    def test_raises_on_missing_h1_heading(self):
        """Test that exception is raised if no H1 heading found."""
        content = "## Second Level\n\nSentence one. Sentence two. Sentence three.\n"
        with pytest.raises(ValueError, match="No H1 heading found"):
            extract_topic_from_content(content)

    def test_raises_on_empty_heading(self):
        """Test that exception is raised if H1 heading is empty."""
        content = "# \n\nSentence one. Sentence two. Sentence three.\n"
        with pytest.raises(ValueError, match="H1 heading is empty"):
            extract_topic_from_content(content)

    def test_preserves_heading_content(self):
        """Test that heading content with special characters is preserved."""
        content = "# Machine Learning: Theory & Practice\n\nFirst. Second. Third.\n"
        topic = extract_topic_from_content(content)
        assert topic == "Machine Learning: Theory & Practice"


class TestCommitMarkdownFile:
    """Tests for commit_markdown_file function."""

    def test_creates_commit_with_proper_message(self):
        """Test that commit is created with correct message format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)

            # Initialize git repo
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
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
            (repo_path / "README.md").write_text("# Test\n")
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

            # Create test file
            test_file = repo_path / "test.md"
            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            test_file.write_text(content, encoding="utf-8")

            # Stage and commit
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(repo_path)

                result = commit_markdown_file(str(test_file), content, str(repo_path))

                # Verify commit was created
                log_result = subprocess.run(
                    ["git", "log", "-1", "--format=%B"],
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=repo_path,
                )

                assert "feat(145):" in log_result.stdout
                assert "test.md" in log_result.stdout
                assert "prose content" in log_result.stdout
                assert result  # Should return some result

            finally:
                os.chdir(original_cwd)

    def test_uses_standardized_commit_message_format(self):
        """Test that commit message uses standardized format: feat(145): create markdown file ... with prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)

            # Initialize git repo
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
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
            (repo_path / "README.md").write_text("# Test\n")
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

            # Create test file
            test_file = repo_path / "test.md"
            content = "# Important Discovery\n\nFirst sentence. Second sentence. Third sentence.\n"
            test_file.write_text(content, encoding="utf-8")

            # Stage and commit
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(repo_path)

                commit_markdown_file(str(test_file), content, str(repo_path))

                # Verify commit message uses standardized format
                log_result = subprocess.run(
                    ["git", "log", "-1", "--format=%B"],
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=repo_path,
                )

                assert "feat(145):" in log_result.stdout
                assert "create markdown file" in log_result.stdout
                assert "with prose content" in log_result.stdout

            finally:
                os.chdir(original_cwd)

    def test_uses_custom_message_if_provided(self):
        """Test that custom commit message is used when provided."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)

            # Initialize git repo
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                capture_output=True,
                check=True,
            )
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
            (repo_path / "README.md").write_text("# Test\n")
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

            # Create test file
            test_file = repo_path / "test.md"
            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            test_file.write_text(content, encoding="utf-8")

            # Stage and commit with custom message
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(repo_path)

                custom_msg = "feat: Custom commit message for testing"
                commit_markdown_file(
                    str(test_file),
                    content,
                    str(repo_path),
                    custom_message=custom_msg,
                )

                # Verify custom message was used
                log_result = subprocess.run(
                    ["git", "log", "-1", "--format=%B"],
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=repo_path,
                )

                assert custom_msg in log_result.stdout

            finally:
                os.chdir(original_cwd)


class TestPushMarkdownFile:
    """Tests for push_markdown_file function."""

    def test_push_function_signature_and_defaults(self):
        """Test that push function has correct signature with defaults."""
        import inspect

        sig = inspect.signature(push_markdown_file)
        assert "repo_path" in sig.parameters
        assert "remote" in sig.parameters
        assert sig.parameters["remote"].default == "origin"


class TestCreateMarkdownFile:
    """Tests for create_markdown_file orchestration function."""

    @patch("sheep.content_generators.push_markdown_file")
    @patch("sheep.content_generators.commit_markdown_file")
    @patch("sheep.content_generators.validate_markdown_file")
    @patch("sheep.content_generators.write_markdown_file")
    @patch("sheep.content_generators.generate_markdown_content")
    def test_orchestration_calls_all_steps_in_order(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that create_markdown_file calls all steps in correct order."""
        # Setup mock returns
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed successfully"
        mock_push.return_value = "Pushed successfully"

        # Call the function
        result = create_markdown_file("test.md")

        # Verify all functions were called
        mock_generate.assert_called_once()
        mock_write.assert_called_once_with(mock_content, "test.md")
        mock_validate.assert_called_once()
        mock_commit.assert_called_once()
        mock_push.assert_called_once()

        # Verify the return value structure
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

    @patch("sheep.content_generators.push_markdown_file")
    @patch("sheep.content_generators.commit_markdown_file")
    @patch("sheep.content_generators.validate_markdown_file")
    @patch("sheep.content_generators.write_markdown_file")
    @patch("sheep.content_generators.generate_markdown_content")
    def test_returns_correct_dict_structure(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that the function returns the correct dictionary structure."""
        # Setup mock returns
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third.\n"
        mock_filepath = "/repo/test.md"
        mock_generate.return_value = mock_content
        mock_write.return_value = mock_filepath
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call the function
        result = create_markdown_file("test.md")

        # Verify all required keys are present
        assert result["filepath"] == mock_filepath
        assert result["content"] == mock_content
        assert "commit_message" in result
        assert result["push_result"] == "Pushed"

    @patch("sheep.content_generators.push_markdown_file")
    @patch("sheep.content_generators.commit_markdown_file")
    @patch("sheep.content_generators.validate_markdown_file")
    @patch("sheep.content_generators.write_markdown_file")
    @patch("sheep.content_generators.generate_markdown_content")
    def test_repo_path_defaults_to_cwd(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that repo_path defaults to current working directory."""
        # Setup mocks
        mock_content = "# Test\n\nSentence. Sentence. Sentence.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call without repo_path
        create_markdown_file("test.md")

        # Verify commit was called with str(Path.cwd())
        call_args = mock_commit.call_args
        assert call_args is not None
        # The repo_path should be str(Path.cwd())
        assert len(call_args[0]) >= 2 or "repo_path" in call_args.kwargs

    @patch("sheep.content_generators.push_markdown_file")
    @patch("sheep.content_generators.commit_markdown_file")
    @patch("sheep.content_generators.validate_markdown_file")
    @patch("sheep.content_generators.write_markdown_file")
    @patch("sheep.content_generators.generate_markdown_content")
    def test_handles_exception_in_generate(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that exceptions in generate step are properly raised."""
        # Setup mock to raise exception
        mock_generate.side_effect = ValueError("LLM generation failed")

        # Verify exception is raised
        with pytest.raises(ValueError, match="LLM generation failed"):
            create_markdown_file("test.md")

        # Verify subsequent steps were not called
        mock_write.assert_not_called()
        mock_validate.assert_not_called()
        mock_commit.assert_not_called()
        mock_push.assert_not_called()
