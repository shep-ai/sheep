"""Tests for feature 270: Create markdown file test-f2zwii.md with prose content.

Tests cover:
- File creation with correct name and location
- File contains H1 heading and 2-3 sentences
- File encoding (UTF-8 without BOM) and line endings (LF)
- File ends with trailing newline
- Markdown validation passes
- Git operations are executed
- Function returns correct structure
- Error handling and exception propagation
"""

import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.features.feature_270_markdown_file_creation import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_270_markdown_file,
)

# Sample valid markdown content for testing
SAMPLE_MARKDOWN = """# Machine Learning Fundamentals

Machine learning is a transformative technology that enables computers to learn from data. Neural networks and deep learning approaches continue to improve accuracy in image recognition and natural language processing. This field has applications across healthcare, finance, and autonomous systems."""


class TestFeature270Module:
    """Tests for feature 270 module structure and metadata."""

    def test_feature_number_is_270(self):
        """Test that FEATURE_NUMBER is 270."""
        assert FEATURE_NUMBER == 270

    def test_markdown_filename_is_correct(self):
        """Test that MARKDOWN_FILENAME is test-f2zwii.md."""
        assert MARKDOWN_FILENAME == "test-f2zwii.md"

    def test_feature_name_is_set(self):
        """Test that FEATURE_NAME is set."""
        assert FEATURE_NAME == "markdown-file-creation-a09312"

    def test_create_function_exists(self):
        """Test that create_feature_270_markdown_file function exists."""
        assert callable(create_feature_270_markdown_file)

    def test_function_signature(self):
        """Test that create_feature_270_markdown_file has correct signature."""
        import inspect

        sig = inspect.signature(create_feature_270_markdown_file)
        # Function accepts repo_path parameter with default None
        assert "repo_path" in sig.parameters
        assert sig.parameters["repo_path"].default is None


class TestFeature270UnitTests:
    """Unit tests for create_feature_270_markdown_file function with mocked dependencies."""

    @patch('sheep.features.feature_270_markdown_file_creation.push_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.commit_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.validate_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.write_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.generate_markdown_content')
    def test_success_path_all_functions_called_in_order(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that all infrastructure functions are called in correct order."""
        # Setup mocks
        mock_generate.return_value = SAMPLE_MARKDOWN
        mock_write.return_value = "/repo/test-f2zwii.md"
        mock_validate.return_value = True
        mock_commit.return_value = "abc123"
        mock_push.return_value = "pushed"

        # Call function
        create_feature_270_markdown_file("/repo")

        # Verify all mocks were called
        mock_generate.assert_called_once_with()
        mock_write.assert_called_once_with(SAMPLE_MARKDOWN, MARKDOWN_FILENAME)
        mock_validate.assert_called_once_with("/repo/test-f2zwii.md")
        mock_commit.assert_called_once()
        mock_push.assert_called_once_with("/repo")

    @patch('sheep.features.feature_270_markdown_file_creation.push_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.commit_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.validate_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.write_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.generate_markdown_content')
    def test_commit_message_format_is_correct(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that commit_markdown_file is called with correct custom message."""
        mock_generate.return_value = SAMPLE_MARKDOWN
        mock_write.return_value = "/repo/test-f2zwii.md"
        mock_validate.return_value = True
        mock_commit.return_value = "abc123"
        mock_push.return_value = "pushed"

        result = create_feature_270_markdown_file("/repo")

        # Verify commit message format
        expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
        assert result['commit_message'] == expected_message

        # Verify commit_markdown_file was called with this message
        mock_commit.assert_called_once()
        call_args = mock_commit.call_args
        assert call_args[1]['custom_message'] == expected_message

    @patch('sheep.features.feature_270_markdown_file_creation.push_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.commit_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.validate_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.write_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.generate_markdown_content')
    def test_returns_dict_with_all_required_keys(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that function returns dict with all required keys."""
        mock_generate.return_value = SAMPLE_MARKDOWN
        mock_write.return_value = "/repo/test-f2zwii.md"
        mock_validate.return_value = True
        mock_commit.return_value = "abc123"
        mock_push.return_value = "pushed"

        result = create_feature_270_markdown_file("/repo")

        assert isinstance(result, dict)
        assert 'filepath' in result
        assert 'content' in result
        assert 'commit_message' in result
        assert 'push_result' in result
        assert result['filepath'] == "/repo/test-f2zwii.md"
        assert result['content'] == SAMPLE_MARKDOWN
        assert result['push_result'] == "pushed"

    @patch('sheep.features.feature_270_markdown_file_creation.push_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.commit_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.validate_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.write_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.generate_markdown_content')
    def test_repo_path_defaults_to_current_directory(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that function uses current directory when repo_path is None."""
        mock_generate.return_value = SAMPLE_MARKDOWN
        mock_write.return_value = "test-f2zwii.md"
        mock_validate.return_value = True
        mock_commit.return_value = "abc123"
        mock_push.return_value = "pushed"

        create_feature_270_markdown_file(repo_path=None)

        # Verify push_markdown_file was called with a path (not None)
        mock_push.assert_called_once()
        call_args = mock_push.call_args[0][0]
        assert call_args is not None  # Should have defaulted to cwd

    @patch('sheep.features.feature_270_markdown_file_creation.commit_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.validate_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.write_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.generate_markdown_content')
    def test_error_handling_propagates_generate_error(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
    ):
        """Test that exceptions from generate_markdown_content are propagated."""
        mock_generate.side_effect = ValueError("LLM generation failed")

        with pytest.raises(ValueError, match="LLM generation failed"):
            create_feature_270_markdown_file("/repo")

    @patch('sheep.features.feature_270_markdown_file_creation.validate_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.write_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.generate_markdown_content')
    def test_error_handling_propagates_write_error(
        self,
        mock_generate,
        mock_write,
        mock_validate,
    ):
        """Test that exceptions from write_markdown_file are propagated."""
        mock_generate.return_value = SAMPLE_MARKDOWN
        mock_write.side_effect = OSError("Cannot write file")

        with pytest.raises(OSError, match="Cannot write file"):
            create_feature_270_markdown_file("/repo")

    @patch('sheep.features.feature_270_markdown_file_creation.push_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.commit_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.validate_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.write_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.generate_markdown_content')
    def test_error_handling_propagates_validation_error(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that exceptions from validate_markdown_file are propagated."""
        mock_generate.return_value = SAMPLE_MARKDOWN
        mock_write.return_value = "/repo/test-f2zwii.md"
        mock_validate.side_effect = ValueError("Invalid markdown format")

        with pytest.raises(ValueError, match="Invalid markdown format"):
            create_feature_270_markdown_file("/repo")

    @patch('sheep.features.feature_270_markdown_file_creation.push_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.commit_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.validate_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.write_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.generate_markdown_content')
    def test_error_handling_propagates_commit_error(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that exceptions from commit_markdown_file are propagated."""
        mock_generate.return_value = SAMPLE_MARKDOWN
        mock_write.return_value = "/repo/test-f2zwii.md"
        mock_validate.return_value = True
        mock_commit.side_effect = Exception("Git commit failed")

        with pytest.raises(Exception, match="Git commit failed"):
            create_feature_270_markdown_file("/repo")

    @patch('sheep.features.feature_270_markdown_file_creation.push_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.commit_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.validate_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.write_markdown_file')
    @patch('sheep.features.feature_270_markdown_file_creation.generate_markdown_content')
    def test_error_handling_propagates_push_error(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that exceptions from push_markdown_file are propagated."""
        mock_generate.return_value = SAMPLE_MARKDOWN
        mock_write.return_value = "/repo/test-f2zwii.md"
        mock_validate.return_value = True
        mock_commit.return_value = "abc123"
        mock_push.side_effect = Exception("Git push failed")

        with pytest.raises(Exception, match="Git push failed"):
            create_feature_270_markdown_file("/repo")


class TestFeature270IntegrationTests:
    """Integration tests with real file system and git operations."""

    @patch('sheep.content_generators.get_reasoning_llm')
    def test_complete_workflow_creates_file(self, mock_llm_factory):
        """Test complete workflow creates file in temporary directory."""
        # Setup LLM mock
        mock_llm = MagicMock()
        mock_llm.call.return_value = SAMPLE_MARKDOWN
        mock_llm_factory.return_value = mock_llm

        with tempfile.TemporaryDirectory() as tmpdir:
            # Initialize git repo
            subprocess.run(
                ["git", "init"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            # Create initial commit so feature branch can be created
            Path(tmpdir, "README.md").write_text("# Test Repo\n")
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )

            # Change to temp directory and create feature
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                result = create_feature_270_markdown_file(tmpdir)

                # Verify file exists at root
                assert Path(tmpdir, MARKDOWN_FILENAME).exists()
                assert result['filepath'].endswith(MARKDOWN_FILENAME)
            finally:
                os.chdir(original_cwd)

    @patch('sheep.content_generators.get_reasoning_llm')
    def test_file_contains_h1_heading(self, mock_llm_factory):
        """Test that created file contains H1 markdown heading."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = SAMPLE_MARKDOWN
        mock_llm_factory.return_value = mock_llm

        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                ["git", "init"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            Path(tmpdir, "README.md").write_text("# Test\n")
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )

            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_feature_270_markdown_file(tmpdir)
                content = Path(tmpdir, MARKDOWN_FILENAME).read_text()
                assert content.lstrip().startswith('# '), "File must start with H1 heading"
            finally:
                os.chdir(original_cwd)

    @patch('sheep.content_generators.get_reasoning_llm')
    def test_file_has_utf8_encoding_no_bom(self, mock_llm_factory):
        """Test that file uses UTF-8 encoding without BOM."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = SAMPLE_MARKDOWN
        mock_llm_factory.return_value = mock_llm

        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                ["git", "init"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            Path(tmpdir, "README.md").write_text("# Test\n")
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )

            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_feature_270_markdown_file(tmpdir)
                binary_content = Path(tmpdir, MARKDOWN_FILENAME).read_bytes()
                # Check no UTF-8 BOM
                assert not binary_content.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"
                # Verify valid UTF-8
                binary_content.decode('utf-8')
            finally:
                os.chdir(original_cwd)

    @patch('sheep.content_generators.get_reasoning_llm')
    def test_file_has_lf_line_endings_not_crlf(self, mock_llm_factory):
        """Test that file uses Unix LF line endings (not CRLF)."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = SAMPLE_MARKDOWN
        mock_llm_factory.return_value = mock_llm

        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                ["git", "init"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            Path(tmpdir, "README.md").write_text("# Test\n")
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )

            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_feature_270_markdown_file(tmpdir)
                binary_content = Path(tmpdir, MARKDOWN_FILENAME).read_bytes()
                # Check no CRLF or CR
                assert b'\r\n' not in binary_content, "File should not have CRLF endings"
                assert b'\r' not in binary_content, "File should not have CR endings"
            finally:
                os.chdir(original_cwd)

    @patch('sheep.content_generators.get_reasoning_llm')
    def test_file_ends_with_trailing_newline(self, mock_llm_factory):
        """Test that file ends with exactly one trailing newline."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = SAMPLE_MARKDOWN
        mock_llm_factory.return_value = mock_llm

        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                ["git", "init"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            Path(tmpdir, "README.md").write_text("# Test\n")
            subprocess.run(
                ["git", "add", "README.md"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )

            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_feature_270_markdown_file(tmpdir)
                content = Path(tmpdir, MARKDOWN_FILENAME).read_text()
                assert content.endswith('\n'), "File should end with trailing newline"
            finally:
                os.chdir(original_cwd)
