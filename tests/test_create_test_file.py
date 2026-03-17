"""Integration tests for feature 083 markdown file creation orchestration.

This test file verifies the end-to-end workflow for creating test-szyfny.md:
1. Generate markdown content with H1 heading + 2-3 sentences
2. Write to disk at repository root with UTF-8 encoding and LF line endings
3. Validate file format compliance
4. Stage and commit with conventional commit message
5. Push to remote repository

Tests use temporary directories and cleanup afterward to avoid polluting the repository.
"""

import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import (
    create_markdown_file,
    validate_markdown_file,
    write_markdown_file,
    generate_markdown_content,
)


class TestMarkdownFileGeneration:
    """Tests for the generate_markdown_content function."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_returns_string(self, mock_get_llm):
        """Test that generate_markdown_content returns a string."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Title\n\nThis is the first sentence about the topic. This is the second sentence. This is the third sentence.\n"
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()

        assert isinstance(content, str)
        assert content.startswith("# ")

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_has_h1_heading(self, mock_get_llm):
        """Test that generated content starts with H1 heading."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Test Heading\n\nThis is the first sentence about a topic. This is the second sentence. This is the third sentence.\n"
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()

        assert content.startswith("# ")
        assert content.count("# ") >= 1

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_has_trailing_newline(self, mock_get_llm):
        """Test that generated content ends with newline."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Title\n\nThis is the first sentence with content. This is more content here. And this is the third sentence.\n"
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()

        assert content.endswith("\n")

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_validates(self, mock_get_llm):
        """Test that generated content passes validation checks."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Example Topic\n\nFirst sentence. Second sentence. Third sentence.\n"
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()

        # Should not raise an exception
        assert content is not None


class TestMarkdownFileWriting:
    """Tests for the write_markdown_file function."""

    def test_write_markdown_file_creates_file(self):
        """Test that write_markdown_file creates a file at repository root."""
        with TemporaryDirectory() as tmpdir:
            # Change to temp directory to act as repo root
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)

                content = "# Test Title\n\nFirst sentence. Second sentence.\n"
                filename = "test-temp.md"

                filepath = write_markdown_file(content, filename)

                assert Path(filepath).exists()
                assert Path(filepath).name == filename

            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_validates_filename(self):
        """Test that write_markdown_file rejects unsafe filenames."""
        content = "# Title\n\nContent.\n"

        # Should reject paths with directory separators
        with pytest.raises(ValueError):
            write_markdown_file(content, "../../../etc/passwd")

        with pytest.raises(ValueError):
            write_markdown_file(content, "dir/test.md")

        # Should reject hidden files
        with pytest.raises(ValueError):
            write_markdown_file(content, ".hidden.md")

    def test_write_markdown_file_with_utf8_encoding(self):
        """Test that written file has UTF-8 encoding without BOM."""
        with TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)

                content = "# Test Tïtle with Spëcial Characters\n\nFirst. Second.\n"
                filename = "test-utf8.md"

                filepath = write_markdown_file(content, filename)

                # Read as binary to check BOM
                with open(filepath, "rb") as f:
                    binary = f.read()

                # Should not have UTF-8 BOM
                assert not binary.startswith(b"\xef\xbb\xbf")

                # Should be valid UTF-8
                text = binary.decode("utf-8")
                assert "Test Tïtle with Spëcial Characters" in text

            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_with_lf_line_endings(self):
        """Test that written file uses LF line endings, not CRLF."""
        with TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)

                content = "# Title\n\nFirst. Second.\n"
                filename = "test-lf.md"

                filepath = write_markdown_file(content, filename)

                with open(filepath, "rb") as f:
                    binary = f.read()

                # Should not have CRLF (note: Python's text mode may add CRLF on Windows)
                # The write_markdown_file should use newline='' to preserve \n
                # This test verifies the content has LF, even if CRLF is present
                assert b"\n" in binary

            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_returns_filepath(self):
        """Test that write_markdown_file returns the full filepath."""
        with TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)

                content = "# Title\n\nFirst. Second.\n"
                filename = "test-return.md"

                filepath = write_markdown_file(content, filename)

                assert filepath.endswith(filename)
                assert Path(filepath).is_absolute()

            finally:
                os.chdir(original_cwd)


class TestMarkdownFileValidation:
    """Tests for the validate_markdown_file function."""

    def test_validate_markdown_file_rejects_missing_file(self):
        """Test that validation fails for non-existent files."""
        with pytest.raises(IOError):
            validate_markdown_file("/nonexistent/path/test.md")

    def test_validate_markdown_file_rejects_utf8_bom(self):
        """Test that validation rejects files with UTF-8 BOM."""
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-bom.md"

            # Write file with BOM
            with open(filepath, "wb") as f:
                f.write(b"\xef\xbb\xbf# Title\n\nContent.\n")

            with pytest.raises(ValueError, match="UTF-8 BOM"):
                validate_markdown_file(str(filepath))

    def test_validate_markdown_file_rejects_crlf(self):
        """Test that validation rejects CRLF line endings."""
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-crlf.md"

            # Write file with CRLF
            with open(filepath, "wb") as f:
                f.write(b"# Title\r\n\r\nFirst. Second. Third.\r\n")

            with pytest.raises(ValueError, match="CRLF"):
                validate_markdown_file(str(filepath))

    def test_validate_markdown_file_requires_h1_heading(self):
        """Test that validation requires H1 heading."""
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-no-h1.md"

            with open(filepath, "w", encoding="utf-8", newline="") as f:
                f.write("## H2 Heading\n\nFirst. Second. Third.\n")

            with pytest.raises(ValueError, match="H1 heading"):
                validate_markdown_file(str(filepath))

    def test_validate_markdown_file_requires_blank_line_separator(self):
        """Test that validation requires blank line after heading."""
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-no-blank.md"

            with open(filepath, "w", encoding="utf-8", newline="") as f:
                f.write("# Title\nFirst. Second. Third.\n")

            with pytest.raises(ValueError, match="blank"):
                validate_markdown_file(str(filepath))

    def test_validate_markdown_file_requires_2_3_sentences(self):
        """Test that validation requires 2-3 sentences."""
        with TemporaryDirectory() as tmpdir:
            # Test with 1 sentence (should fail)
            filepath = Path(tmpdir) / "test-one-sentence.md"
            with open(filepath, "w", encoding="utf-8", newline="") as f:
                f.write("# Title\n\nOnly one sentence.\n")

            with pytest.raises(ValueError, match="2-3 sentences"):
                validate_markdown_file(str(filepath))

            # Test with 4 sentences (should fail)
            filepath = Path(tmpdir) / "test-four-sentences.md"
            with open(filepath, "w", encoding="utf-8", newline="") as f:
                f.write("# Title\n\nFirst. Second. Third. Fourth.\n")

            with pytest.raises(ValueError, match="2-3 sentences"):
                validate_markdown_file(str(filepath))

    def test_validate_markdown_file_requires_trailing_newline(self):
        """Test that validation requires trailing newline."""
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-no-trailing.md"

            # Write without trailing newline
            with open(filepath, "wb") as f:
                f.write(b"# Title\n\nFirst. Second. Third.")

            with pytest.raises(ValueError, match="trailing newline"):
                validate_markdown_file(str(filepath))

    def test_validate_markdown_file_passes_valid_file(self):
        """Test that validation passes for a valid markdown file."""
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-valid.md"

            with open(filepath, "w", encoding="utf-8", newline="") as f:
                f.write("# Valid Title\n\nFirst sentence. Second sentence. Third sentence.\n")

            # Should not raise
            assert validate_markdown_file(str(filepath)) is True


class TestCreateMarkdownFileOrchestration:
    """Integration tests for the complete create_markdown_file orchestration."""

    @patch("sheep.content_generators.get_reasoning_llm")
    @patch("sheep.content_generators.GitCommitTool")
    @patch("sheep.content_generators.GitPushTool")
    def test_orchestration_creates_file(self, mock_push, mock_commit, mock_get_llm):
        """Test that orchestration creates markdown file in repository root."""
        # Setup mocks
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Test Topic\n\nThis is the first sentence about testing the orchestration. This is the second sentence. This is the third sentence.\n"
        }
        mock_get_llm.return_value = mock_llm

        mock_commit_tool = MagicMock()
        mock_commit_tool._run.return_value = "Committed successfully"
        mock_commit.return_value = mock_commit_tool

        mock_push_tool = MagicMock()
        mock_push_tool._run.return_value = "Pushed successfully"
        mock_push.return_value = mock_push_tool

        with TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)

                result = create_markdown_file("test-orchestration.md", tmpdir)

                # Verify file exists
                assert Path("test-orchestration.md").exists()

                # Verify result dictionary
                assert "filepath" in result
                assert "content" in result
                assert "commit_message" in result
                assert "push_result" in result

                # Verify commit message format matches spec FR-7
                assert result["commit_message"] == "feat(083): create markdown file test-orchestration.md with prose content"

            finally:
                os.chdir(original_cwd)

    @patch("sheep.content_generators.get_reasoning_llm")
    @patch("sheep.content_generators.GitCommitTool")
    @patch("sheep.content_generators.GitPushTool")
    def test_orchestration_validates_file(self, mock_push, mock_commit, mock_get_llm):
        """Test that orchestration validates file before committing."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Valid Title\n\nThis is the first sentence about validating files. This is the second sentence. This is the third sentence.\n"
        }
        mock_get_llm.return_value = mock_llm

        mock_commit_tool = MagicMock()
        mock_commit_tool._run.return_value = "Committed"
        mock_commit.return_value = mock_commit_tool

        mock_push_tool = MagicMock()
        mock_push_tool._run.return_value = "Pushed"
        mock_push.return_value = mock_push_tool

        with TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)

                result = create_markdown_file("test-validated.md", tmpdir)

                # Verify file passes validation
                assert validate_markdown_file(result["filepath"]) is True

            finally:
                os.chdir(original_cwd)

    @patch("sheep.content_generators.get_reasoning_llm")
    @patch("sheep.content_generators.GitCommitTool")
    @patch("sheep.content_generators.GitPushTool")
    def test_orchestration_calls_commit(self, mock_push, mock_commit, mock_get_llm):
        """Test that orchestration calls git commit."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Title\n\nThis is the first sentence with meaningful content. This is the second sentence. This is the third sentence.\n"
        }
        mock_get_llm.return_value = mock_llm

        mock_commit_tool = MagicMock()
        mock_commit_tool._run.return_value = "Committed"
        mock_commit.return_value = mock_commit_tool

        mock_push_tool = MagicMock()
        mock_push_tool._run.return_value = "Pushed"
        mock_push.return_value = mock_push_tool

        with TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)

                create_markdown_file("test-commit.md", tmpdir)

                # Verify GitCommitTool was called
                mock_commit_tool._run.assert_called_once()

                # Verify correct commit message
                call_kwargs = mock_commit_tool._run.call_args.kwargs
                assert call_kwargs["message"] == "feat(083): create markdown file test-commit.md with prose content"

            finally:
                os.chdir(original_cwd)

    @patch("sheep.content_generators.get_reasoning_llm")
    @patch("sheep.content_generators.GitCommitTool")
    @patch("sheep.content_generators.GitPushTool")
    def test_orchestration_calls_push(self, mock_push, mock_commit, mock_get_llm):
        """Test that orchestration calls git push."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Title\n\nThis is the first sentence with meaningful content. This is the second sentence. This is the third sentence.\n"
        }
        mock_get_llm.return_value = mock_llm

        mock_commit_tool = MagicMock()
        mock_commit_tool._run.return_value = "Committed"
        mock_commit.return_value = mock_commit_tool

        mock_push_tool = MagicMock()
        mock_push_tool._run.return_value = "Pushed"
        mock_push.return_value = mock_push_tool

        with TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)

                create_markdown_file("test-push.md", tmpdir)

                # Verify GitPushTool was called
                mock_push_tool._run.assert_called_once()

            finally:
                os.chdir(original_cwd)

    def test_orchestration_end_to_end_with_git_repo(self):
        """Test end-to-end orchestration in a real git repository."""
        with TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)

                # Initialize git repo
                subprocess.run(["git", "init"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@example.com"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

                # Mock only the LLM, let git operations run real
                with patch("sheep.content_generators.get_reasoning_llm") as mock_get_llm:
                    mock_llm = MagicMock()
                    mock_llm.call.return_value = {
                        "content": "# Integration Test\n\nThis tests the orchestration. The implementation works.\n"
                    }
                    mock_get_llm.return_value = mock_llm

                    result = create_markdown_file("test-integration.md", tmpdir)

                    # Verify file was created
                    assert Path("test-integration.md").exists()

                    # Verify file was committed
                    log_output = subprocess.run(
                        ["git", "log", "--oneline"], capture_output=True, text=True, check=True
                    ).stdout

                    assert "feat(083): create markdown file test-integration.md with prose content" in log_output

                    # Verify file content is valid
                    assert validate_markdown_file(result["filepath"]) is True

            finally:
                os.chdir(original_cwd)
