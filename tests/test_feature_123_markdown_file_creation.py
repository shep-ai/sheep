"""Tests for feature 123: markdown file creation (test-b3x0s1.md)."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import (
    generate_markdown_content,
    write_markdown_file,
)
from sheep.feature_123_markdown_file_creation import (
    task_2_generate_markdown_content,
    task_3_write_markdown_file_to_disk,
    task_4_commit_changes,
    task_5_push_changes,
    main,
)


class TestTask2GenerateMarkdownContent:
    """Task 2: Generate markdown content with H1 heading and 2-3 sentences."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_task2_returns_non_empty_string(self, mock_get_llm):
        """Test that task_2_generate_markdown_content returns a non-empty string."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Creative Writing\n\nCreative writing is the art of crafting original stories. It requires imagination and skill. Writers express their ideas through narrative forms."
        }
        mock_get_llm.return_value = mock_llm

        content = task_2_generate_markdown_content()
        assert isinstance(content, str)
        assert len(content) > 0

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_task2_content_starts_with_h1_heading(self, mock_get_llm):
        """Test that task2 content starts with H1 heading marker."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Renewable Energy\n\nRenewable energy sources include solar and wind. These sustainable alternatives reduce carbon emissions. Countries worldwide are investing in clean energy infrastructure."
        }
        mock_get_llm.return_value = mock_llm

        content = task_2_generate_markdown_content()
        # Should start with H1 heading
        assert content.lstrip().startswith("# ")

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_task2_validates_sentence_count_2_to_3(self, mock_get_llm):
        """Test that task2 validates content contains 2-3 sentences."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Space Exploration\n\nSpace exploration drives technological innovation. It expands human knowledge of the universe. Missions to Mars represent the next frontier."
        }
        mock_get_llm.return_value = mock_llm

        content = task_2_generate_markdown_content()
        # Count sentences by periods
        sentence_count = content.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_task2_raises_error_on_too_few_sentences(self, mock_get_llm):
        """Test that task2 raises ValueError if content has fewer than 2 sentences."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Bad Content\n\nThis has only one sentence."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 should raise ValueError because validation fails
        with pytest.raises(ValueError):
            task_2_generate_markdown_content()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_task2_raises_error_on_too_many_sentences(self, mock_get_llm):
        """Test that task2 raises ValueError if content has more than 3 sentences."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Bad Content\n\nFirst sentence. Second sentence. Third sentence. Fourth sentence."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 should raise ValueError because validation fails
        with pytest.raises(ValueError):
            task_2_generate_markdown_content()


class TestTask3WriteMarkdownFileToDisk:
    """Task 3: Write markdown file to disk with UTF-8 encoding and LF line endings."""

    def test_task3_creates_file_with_correct_name(self):
        """Test that task3 creates file test-b3x0s1.md in repo root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Sample Title\n\nThis is a test sentence. This is another test sentence. This is the third test sentence.\n"
                filepath = task_3_write_markdown_file_to_disk(content)

                assert Path(filepath).exists()
                assert filepath.endswith("test-b3x0s1.md")
            finally:
                os.chdir(original_cwd)

    def test_task3_file_is_readable(self):
        """Test that created file is readable and not corrupted."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Sample Title\n\nThis is a test sentence. This is another test sentence. This is the third test sentence.\n"
                filepath = task_3_write_markdown_file_to_disk(content)

                # Should be readable without errors
                file_content = Path(filepath).read_text(encoding="utf-8")
                assert file_content == content
            finally:
                os.chdir(original_cwd)

    def test_task3_file_contains_markdown_content(self):
        """Test that file contains the markdown content exactly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                expected_content = "# Test Topic\n\nFirst sentence about the topic. Second sentence with more details. Third sentence concluding the thought.\n"
                filepath = task_3_write_markdown_file_to_disk(expected_content)

                actual_content = Path(filepath).read_text(encoding="utf-8")
                assert actual_content == expected_content
            finally:
                os.chdir(original_cwd)

    def test_task3_raises_error_if_file_exists(self):
        """Test that task3 raises error if file already exists (fail-fast)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Test\n\nFirst sentence. Second sentence. Third sentence.\n"

                # Create the file first
                Path("test-b3x0s1.md").write_text(content, encoding="utf-8")

                # Task 3 should raise ValueError because file exists
                with pytest.raises(ValueError, match="File already exists"):
                    task_3_write_markdown_file_to_disk(content)
            finally:
                os.chdir(original_cwd)

    def test_task3_file_size_is_nonzero(self):
        """Test that created file is not empty (non-zero size)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Sample Title\n\nThis is a test sentence. This is another test sentence. This is the third test sentence.\n"
                filepath = task_3_write_markdown_file_to_disk(content)

                file_size = Path(filepath).stat().st_size
                assert file_size > 0, "File should not be empty"
                # Content should be at least 50 bytes
                assert file_size > 50, f"File too small: {file_size} bytes"
            finally:
                os.chdir(original_cwd)

    def test_task3_file_is_utf8_encoded(self):
        """Test that file can be successfully opened and decoded as UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# UTF8 Test\n\nThis file uses UTF-8 encoding. It should decode without errors. Special characters work fine.\n"
                filepath = task_3_write_markdown_file_to_disk(content)

                # Should decode successfully as UTF-8
                binary_content = Path(filepath).read_bytes()
                decoded = binary_content.decode("utf-8")
                assert decoded == content
            finally:
                os.chdir(original_cwd)

    def test_task3_file_uses_lf_line_endings(self):
        """Test that file uses Unix-style LF line endings, not CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Sample Title\n\nThis is a test sentence. This is another test sentence. This is the third test sentence.\n"
                filepath = task_3_write_markdown_file_to_disk(content)

                binary_content = Path(filepath).read_bytes()
                # Should have LF line endings
                assert b"\r\n" not in binary_content, "File should not have CRLF line endings"
            finally:
                os.chdir(original_cwd)


class TestTask4CommitChanges:
    """Task 4: Stage and commit the markdown file with conventional message."""

    @patch("sheep.feature_123_markdown_file_creation.commit_markdown_file")
    def test_task4_calls_commit_markdown_file(self, mock_commit):
        """Test that task_4_commit_changes calls commit_markdown_file."""
        mock_commit.return_value = "Committed: feat(123): Create markdown file test-b3x0s1.md with prose content (#192)"

        filepath = "/tmp/test-b3x0s1.md"
        content = "# Test\n\nFirst sentence. Second sentence. Third sentence.\n"

        result = task_4_commit_changes(filepath, content)

        # Verify that commit_markdown_file was called
        assert mock_commit.called
        assert isinstance(result, str)

    @patch("sheep.feature_123_markdown_file_creation.commit_markdown_file")
    def test_task4_uses_correct_commit_message(self, mock_commit):
        """Test that task_4_commit_changes uses the exact required commit message."""
        mock_commit.return_value = "Committed"

        filepath = "/tmp/test-b3x0s1.md"
        content = "# Test\n\nFirst sentence. Second sentence. Third sentence.\n"

        task_4_commit_changes(filepath, content)

        # Verify the correct commit message was passed
        expected_message = "feat(123): Create markdown file test-b3x0s1.md with prose content (#192)"
        call_args = mock_commit.call_args
        assert call_args is not None
        assert call_args.kwargs["custom_message"] == expected_message

    @patch("sheep.feature_123_markdown_file_creation.commit_markdown_file")
    def test_task4_returns_commit_result(self, mock_commit):
        """Test that task_4_commit_changes returns the commit result message."""
        expected_result = "Committed: feat(123): Create markdown file test-b3x0s1.md with prose content (#192)"
        mock_commit.return_value = expected_result

        filepath = "/tmp/test-b3x0s1.md"
        content = "# Test\n\nFirst sentence. Second sentence. Third sentence.\n"

        result = task_4_commit_changes(filepath, content)

        assert result == expected_result

    @patch("sheep.feature_123_markdown_file_creation.commit_markdown_file")
    def test_task4_raises_on_commit_failure(self, mock_commit):
        """Test that task_4_commit_changes raises exception if commit fails."""
        mock_commit.side_effect = Exception("Git config missing")

        filepath = "/tmp/test-b3x0s1.md"
        content = "# Test\n\nFirst sentence. Second sentence. Third sentence.\n"

        with pytest.raises(Exception):
            task_4_commit_changes(filepath, content)


class TestTask5PushChanges:
    """Task 5: Push committed changes to remote origin."""

    @patch("sheep.feature_123_markdown_file_creation.push_markdown_file")
    def test_task5_calls_push_markdown_file(self, mock_push):
        """Test that task_5_push_changes calls push_markdown_file."""
        mock_push.return_value = "Pushed to origin/feat/123-markdown-file-creation-55cdca"

        result = task_5_push_changes()

        # Verify that push_markdown_file was called
        assert mock_push.called
        assert isinstance(result, str)

    @patch("sheep.feature_123_markdown_file_creation.push_markdown_file")
    def test_task5_pushes_to_origin_remote(self, mock_push):
        """Test that task_5_push_changes pushes to origin remote."""
        mock_push.return_value = "Pushed"

        task_5_push_changes()

        # Verify the correct remote was specified
        call_args = mock_push.call_args
        assert call_args is not None
        assert call_args.kwargs["remote"] == "origin"

    @patch("sheep.feature_123_markdown_file_creation.push_markdown_file")
    def test_task5_returns_push_result(self, mock_push):
        """Test that task_5_push_changes returns the push result message."""
        expected_result = "Pushed to origin/feat/123-markdown-file-creation-55cdca"
        mock_push.return_value = expected_result

        result = task_5_push_changes()

        assert result == expected_result

    @patch("sheep.feature_123_markdown_file_creation.push_markdown_file")
    def test_task5_raises_on_push_failure(self, mock_push):
        """Test that task_5_push_changes raises exception if push fails."""
        mock_push.side_effect = Exception("Network error")

        with pytest.raises(Exception):
            task_5_push_changes()


class TestMainOrchestration:
    """Integration tests for main() orchestration function."""

    @patch("sheep.feature_123_markdown_file_creation.push_markdown_file")
    @patch("sheep.feature_123_markdown_file_creation.commit_markdown_file")
    @patch("sheep.content_generators.get_reasoning_llm")
    def test_main_orchestrates_all_tasks(self, mock_get_llm, mock_commit, mock_push):
        """Test that main() successfully orchestrates all tasks 2-5."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Mock the LLM
                mock_llm = MagicMock()
                mock_llm.call.return_value = {
                    "content": "# Integration Test\n\nThis tests the workflow of generating and writing. The content flows from task 2 to task 3. This ensures seamless integration."
                }
                mock_get_llm.return_value = mock_llm

                # Mock git operations
                mock_commit.return_value = "Committed"
                mock_push.return_value = "Pushed"

                # Execute main()
                result = main()

                # Verify result structure
                assert isinstance(result, dict)
                assert "content" in result
                assert "filepath" in result
                assert "commit_result" in result
                assert "push_result" in result

                # Verify file was created
                assert Path(result["filepath"]).exists()

                # Verify content matches
                file_content = Path(result["filepath"]).read_text(encoding="utf-8")
                assert file_content == result["content"]

                # Verify git operations were called
                assert mock_commit.called
                assert mock_push.called
            finally:
                os.chdir(original_cwd)

    @patch("sheep.feature_123_markdown_file_creation.push_markdown_file")
    @patch("sheep.feature_123_markdown_file_creation.commit_markdown_file")
    @patch("sheep.content_generators.get_reasoning_llm")
    def test_main_returns_valid_file_path(self, mock_get_llm, mock_commit, mock_push):
        """Test that main() returns a valid file path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                mock_llm = MagicMock()
                mock_llm.call.return_value = {
                    "content": "# Valid Path\n\nThis should create a valid file path. The path is returned in the result. Everything works together."
                }
                mock_get_llm.return_value = mock_llm
                mock_commit.return_value = "Committed"
                mock_push.return_value = "Pushed"

                result = main()
                filepath = result["filepath"]

                assert filepath.endswith("test-b3x0s1.md")
                assert Path(filepath).exists()
                assert Path(filepath).is_file()
            finally:
                os.chdir(original_cwd)
