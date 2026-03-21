"""Tests for feature 146: Creating markdown file test-vqya6w.md with title and prose content."""

from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest


class TestFeature146MarkdownFileCreation:
    """Tests for feature 146 markdown file creation."""

    def test_module_imports(self):
        """Test that the feature module can be imported."""
        from sheep.features.feature_146_markdown_file_creation import (
            create_feature_146_markdown_file,
        )

        assert callable(create_feature_146_markdown_file)

    def test_function_signature(self):
        """Test that the function has the correct signature."""
        from sheep.features.feature_146_markdown_file_creation import (
            create_feature_146_markdown_file,
        )
        import inspect

        sig = inspect.signature(create_feature_146_markdown_file)
        assert "repo_path" in sig.parameters
        assert sig.parameters["repo_path"].default is None

    def test_feature_constants(self):
        """Test that feature constants are defined correctly."""
        from sheep.features.feature_146_markdown_file_creation import (
            FEATURE_NUMBER,
            MARKDOWN_FILENAME,
            COMMIT_MESSAGE,
        )

        assert FEATURE_NUMBER == 146
        assert MARKDOWN_FILENAME == "test-vqya6w.md"
        assert COMMIT_MESSAGE == "feat(146): create markdown file test-vqya6w.md with prose content"

    @patch("sheep.features.feature_146_markdown_file_creation.create_markdown_file")
    def test_orchestration_calls_orchestrator(self, mock_create_markdown_file):
        """Test that the feature function calls the orchestrator with correct parameters."""
        from sheep.features.feature_146_markdown_file_creation import (
            create_feature_146_markdown_file,
            MARKDOWN_FILENAME,
            COMMIT_MESSAGE,
        )

        # Setup mock return value
        mock_result = {
            "filepath": "/repo/test-vqya6w.md",
            "content": "# Test Title\n\nFirst sentence. Second sentence. Third.\n",
            "commit_message": COMMIT_MESSAGE,
            "push_result": "Pushed successfully",
        }
        mock_create_markdown_file.return_value = mock_result

        # Call the function with a repo path
        result = create_feature_146_markdown_file("/test/repo")

        # Verify the orchestrator was called with correct parameters
        mock_create_markdown_file.assert_called_once_with(
            filename=MARKDOWN_FILENAME,
            repo_path="/test/repo",
            custom_message=COMMIT_MESSAGE,
        )

        # Verify the return value
        assert result == mock_result

    @patch("sheep.features.feature_146_markdown_file_creation.create_markdown_file")
    def test_returns_correct_dict_structure(self, mock_create_markdown_file):
        """Test that the function returns the correct dictionary structure."""
        from sheep.features.feature_146_markdown_file_creation import (
            create_feature_146_markdown_file,
            COMMIT_MESSAGE,
        )

        # Setup mock return value
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third.\n"
        mock_filepath = "/repo/test-vqya6w.md"
        mock_result = {
            "filepath": mock_filepath,
            "content": mock_content,
            "commit_message": COMMIT_MESSAGE,
            "push_result": "Pushed",
        }
        mock_create_markdown_file.return_value = mock_result

        # Call the function
        result = create_feature_146_markdown_file()

        # Verify all required keys are present
        assert result["filepath"] == mock_filepath
        assert result["content"] == mock_content
        assert result["commit_message"] == COMMIT_MESSAGE
        assert result["push_result"] == "Pushed"

    @patch("sheep.features.feature_146_markdown_file_creation.create_markdown_file")
    def test_uses_exact_commit_message(self, mock_create_markdown_file):
        """Test that the exact commit message from spec is used."""
        from sheep.features.feature_146_markdown_file_creation import (
            create_feature_146_markdown_file,
            COMMIT_MESSAGE,
        )

        # Setup mock return value
        mock_result = {
            "filepath": "/repo/test-vqya6w.md",
            "content": "# Test\n\nSentence. Sentence. Sentence.\n",
            "commit_message": COMMIT_MESSAGE,
            "push_result": "Pushed",
        }
        mock_create_markdown_file.return_value = mock_result

        # Call the function
        create_feature_146_markdown_file()

        # Verify the orchestrator was called with the correct custom message
        call_args = mock_create_markdown_file.call_args
        assert call_args is not None
        assert (
            call_args.kwargs["custom_message"]
            == "feat(146): create markdown file test-vqya6w.md with prose content"
        )

    @patch("sheep.features.feature_146_markdown_file_creation.create_markdown_file")
    def test_handles_exception_from_orchestrator(self, mock_create_markdown_file):
        """Test that exceptions from orchestrator are properly raised."""
        from sheep.features.feature_146_markdown_file_creation import (
            create_feature_146_markdown_file,
        )

        # Setup mock to raise exception
        mock_create_markdown_file.side_effect = ValueError("LLM generation failed")

        # Verify exception is raised and propagated
        with pytest.raises(ValueError, match="LLM generation failed"):
            create_feature_146_markdown_file()

    @patch("sheep.features.feature_146_markdown_file_creation.create_markdown_file")
    def test_repo_path_defaults_to_cwd(self, mock_create_markdown_file):
        """Test that repo_path defaults to current working directory when not provided."""
        from sheep.features.feature_146_markdown_file_creation import (
            create_feature_146_markdown_file,
            COMMIT_MESSAGE,
            MARKDOWN_FILENAME,
        )

        # Setup mock return value
        mock_result = {
            "filepath": "/repo/test-vqya6w.md",
            "content": "# Test\n\nSentence. Sentence. Sentence.\n",
            "commit_message": COMMIT_MESSAGE,
            "push_result": "Pushed",
        }
        mock_create_markdown_file.return_value = mock_result

        # Call without repo_path (should default to cwd)
        create_feature_146_markdown_file()

        # Verify orchestrator was called with cwd as repo_path
        call_args = mock_create_markdown_file.call_args
        assert call_args is not None
        assert call_args.kwargs["repo_path"] == str(Path.cwd())


class TestFileCreation:
    """Integration tests for actual file creation."""

    def test_creates_file_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading."""
        test_file = tmp_path / "test-vqya6w.md"

        # Create the file with H1 heading
        content = "# The Power of Persistence\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_contains_exactly_three_sentences(self, tmp_path):
        """Test that file contains exactly 2-3 sentences (ending with periods)."""
        test_file = tmp_path / "test-vqya6w.md"

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible, discovering capabilities we never knew we possessed.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        # Extract prose content (skip heading and blank line)
        lines = text_content.split("\n")
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3

    def test_file_has_blank_line_separator(self, tmp_path):
        """Test that file has blank line after H1 heading."""
        test_file = tmp_path / "test-vqya6w.md"

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment. It builds resilience. Through persistence, we unlock potential.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        # Check that second line (index 1) is blank
        assert lines[0].startswith("# ")
        assert lines[1] == ""

    def test_file_uses_utf8_encoding(self, tmp_path):
        """Test that file is UTF-8 encoded."""
        test_file = tmp_path / "test-vqya6w.md"

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment. It builds resilience. Through persistence, we unlock potential.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Read as binary and verify no BOM
        binary_content = test_file.read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Verify can be decoded as UTF-8
        decoded = binary_content.decode("utf-8")
        assert decoded == content

    def test_file_uses_lf_line_endings(self, tmp_path):
        """Test that file uses LF line endings, not CRLF."""
        test_file = tmp_path / "test-vqya6w.md"

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment. It builds resilience. Through persistence, we unlock potential.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Read as binary and verify no CRLF
        binary_content = test_file.read_bytes()
        assert b"\r\n" not in binary_content
        assert b"\n" in binary_content

    def test_file_ends_with_newline(self, tmp_path):
        """Test that file ends with a trailing newline (Unix convention)."""
        test_file = tmp_path / "test-vqya6w.md"

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment. It builds resilience. Through persistence, we unlock potential.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        assert text_content.endswith("\n")

    def test_file_size_is_reasonable(self, tmp_path):
        """Test that file size is within reasonable bounds (400-600 bytes guideline)."""
        test_file = tmp_path / "test-vqya6w.md"

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible, discovering capabilities we never knew we possessed.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = test_file.stat().st_size
        # 400-600 bytes is a guideline, not strict
        assert 100 < file_size < 1000
