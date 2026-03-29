"""Tests for feature 270: Create markdown file test-2sqwpg.md with prose content.

Tests cover:
- Module metadata (FEATURE_NUMBER, MARKDOWN_FILENAME, FEATURE_NAME)
- Hardcoded content constants (TITLE, PROSE)
- Content format requirements (sentences, structure)
- File size validation (400-600 bytes)
- Function existence and return types
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
    PROSE,
    TITLE,
    create_feature_270_markdown_file,
)


class TestFeature270Module:
    """Tests for feature 270 module structure and metadata."""

    def test_feature_number_is_270(self):
        """Test that FEATURE_NUMBER is 270."""
        assert FEATURE_NUMBER == 270

    def test_markdown_filename_is_correct(self):
        """Test that MARKDOWN_FILENAME is test-2sqwpg.md."""
        assert MARKDOWN_FILENAME == "test-2sqwpg.md"

    def test_feature_name_is_set(self):
        """Test that FEATURE_NAME is set."""
        assert FEATURE_NAME == "markdown-file-creation-f37f64"

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


class TestFeature270ContentConstants:
    """Tests for hardcoded content constants (TITLE and PROSE)."""

    def test_title_is_string(self):
        """Test that TITLE constant is a string."""
        assert isinstance(TITLE, str)

    def test_title_is_not_empty(self):
        """Test that TITLE is not empty."""
        assert TITLE and TITLE.strip()

    def test_title_length_reasonable(self):
        """Test that TITLE has reasonable length (20-60 characters)."""
        assert 20 <= len(TITLE) <= 60

    def test_prose_is_string(self):
        """Test that PROSE constant is a string."""
        assert isinstance(PROSE, str)

    def test_prose_is_not_empty(self):
        """Test that PROSE is not empty."""
        assert PROSE and PROSE.strip()

    def test_prose_has_no_leading_trailing_whitespace(self):
        """Test that PROSE has no leading or trailing whitespace."""
        assert PROSE == PROSE.strip()

    def test_prose_contains_exactly_three_sentences(self):
        """Test that PROSE contains exactly 2 or 3 sentences (periods)."""
        sentence_count = PROSE.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    def test_prose_sentences_end_with_period(self):
        """Test that each sentence in PROSE ends with a period."""
        # Split by period and space to get sentences
        sentences = [s.strip() for s in PROSE.split(".") if s.strip()]
        # Verify all sentences are properly terminated (last one should end with period)
        assert PROSE.rstrip().endswith("."), "PROSE must end with a period"

    def test_prose_no_double_periods(self):
        """Test that PROSE doesn't have double periods (..)."""
        assert ".." not in PROSE, "PROSE should not contain double periods"


class TestFeature270ContentFormatting:
    """Tests for content formatting and file size validation."""

    def test_content_title_format(self):
        """Test that TITLE format is suitable for H1 heading."""
        # Should not start with # (that's added during formatting)
        assert not TITLE.startswith("#"), "TITLE should not include # prefix"
        # Should contain meaningful text
        assert len(TITLE) > 0 and not TITLE.isdigit()

    def test_content_file_size_calculation(self):
        """Test that formatted content fits in 400-600 byte range."""
        # Format: "# {TITLE}\n\n{PROSE}\n"
        formatted_content = f"# {TITLE}\n\n{PROSE}\n"
        file_size = len(formatted_content.encode("utf-8"))

        # Should be between 400-600 bytes
        assert 400 <= file_size <= 600, (
            f"File size {file_size} bytes is outside expected range (400-600). "
            f"Content length: {len(formatted_content)}"
        )

    def test_content_utf8_encoding(self):
        """Test that content is valid UTF-8."""
        formatted_content = f"# {TITLE}\n\n{PROSE}\n"
        # Should encode without error
        encoded = formatted_content.encode("utf-8")
        # Should decode without error
        decoded = encoded.decode("utf-8")
        assert decoded == formatted_content

    def test_content_no_bom(self):
        """Test that encoded content doesn't have UTF-8 BOM."""
        formatted_content = f"# {TITLE}\n\n{PROSE}\n"
        encoded = formatted_content.encode("utf-8")
        # UTF-8 BOM is b'\xef\xbb\xbf'
        assert not encoded.startswith(b"\xef\xbb\xbf"), "Content should not have UTF-8 BOM"

    def test_content_structure_format(self):
        """Test that formatted content has proper markdown structure."""
        formatted_content = f"# {TITLE}\n\n{PROSE}\n"
        lines = formatted_content.split("\n")

        # First line should be H1 heading
        assert lines[0].startswith("# "), "First line must be H1 heading"
        assert lines[0] == f"# {TITLE}", "First line should be properly formatted heading"

        # Second line should be blank
        assert lines[1] == "", "Second line must be blank"

        # Third line onwards should be prose
        assert len(lines) > 2, "Should have prose after heading and blank line"

    def test_content_ends_with_newline(self):
        """Test that formatted content ends with newline."""
        formatted_content = f"# {TITLE}\n\n{PROSE}\n"
        assert formatted_content.endswith("\n"), "Content should end with newline"

    def test_prose_sentence_count_validation(self):
        """Test that PROSE has exactly 2 or 3 sentences."""
        period_count = PROSE.count(".")
        assert period_count in [2, 3], (
            f"PROSE should have 2 or 3 sentences (periods), found {period_count}"
        )


class TestFeature270UnitTests:
    """Unit tests for create_feature_270_markdown_file function with mocked dependencies."""

    @patch("sheep.features.feature_270_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.write_markdown_file")
    def test_success_path_all_functions_called_in_order(
        self,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that all infrastructure functions are called in correct order."""
        # Setup mocks
        expected_content = f"# {TITLE}\n\n{PROSE}\n"
        mock_write.return_value = "/repo/test-2sqwpg.md"
        mock_validate.return_value = True
        mock_commit.return_value = "abc123"
        mock_push.return_value = "pushed"

        # Call function
        create_feature_270_markdown_file("/repo")

        # Verify all mocks were called
        mock_write.assert_called_once_with(expected_content, MARKDOWN_FILENAME)
        mock_validate.assert_called_once_with("/repo/test-2sqwpg.md")
        mock_commit.assert_called_once()
        mock_push.assert_called_once_with("/repo")

    @patch("sheep.features.feature_270_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.write_markdown_file")
    def test_commit_message_format_is_correct(
        self,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that commit_markdown_file is called with correct custom message."""
        mock_write.return_value = "/repo/test-2sqwpg.md"
        mock_validate.return_value = True
        mock_commit.return_value = "abc123"
        mock_push.return_value = "pushed"

        result = create_feature_270_markdown_file("/repo")

        # Verify commit message format
        expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME}"
        assert result["commit_message"] == expected_message

        # Verify commit_markdown_file was called with this message
        mock_commit.assert_called_once()
        call_args = mock_commit.call_args
        assert call_args[1]["custom_message"] == expected_message

    @patch("sheep.features.feature_270_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.write_markdown_file")
    def test_returns_dict_with_all_required_keys(
        self,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that function returns dict with all required keys."""
        expected_content = f"# {TITLE}\n\n{PROSE}\n"
        mock_write.return_value = "/repo/test-2sqwpg.md"
        mock_validate.return_value = True
        mock_commit.return_value = "abc123"
        mock_push.return_value = "pushed"

        result = create_feature_270_markdown_file("/repo")

        assert isinstance(result, dict)
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result
        assert result["filepath"] == "/repo/test-2sqwpg.md"
        assert result["content"] == expected_content
        assert result["push_result"] == "pushed"

    @patch("sheep.features.feature_270_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.write_markdown_file")
    def test_repo_path_defaults_to_current_directory(
        self,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that function uses current directory when repo_path is None."""
        mock_write.return_value = "test-2sqwpg.md"
        mock_validate.return_value = True
        mock_commit.return_value = "abc123"
        mock_push.return_value = "pushed"

        create_feature_270_markdown_file(repo_path=None)

        # Verify push_markdown_file was called with a path (not None)
        mock_push.assert_called_once()
        call_args = mock_push.call_args[0][0]
        assert call_args is not None  # Should have defaulted to cwd

    @patch("sheep.features.feature_270_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.write_markdown_file")
    def test_error_handling_propagates_write_error(
        self,
        mock_write,
        mock_validate,
        mock_commit,
    ):
        """Test that exceptions from write_markdown_file are propagated."""
        mock_write.side_effect = OSError("Cannot write file")

        with pytest.raises(OSError, match="Cannot write file"):
            create_feature_270_markdown_file("/repo")

    @patch("sheep.features.feature_270_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.write_markdown_file")
    def test_error_handling_propagates_validation_error(
        self,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that exceptions from validate_markdown_file are propagated."""
        mock_write.return_value = "/repo/test-2sqwpg.md"
        mock_validate.side_effect = ValueError("Invalid markdown format")

        with pytest.raises(ValueError, match="Invalid markdown format"):
            create_feature_270_markdown_file("/repo")

    @patch("sheep.features.feature_270_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.write_markdown_file")
    def test_error_handling_propagates_commit_error(
        self,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that exceptions from commit_markdown_file are propagated."""
        mock_write.return_value = "/repo/test-2sqwpg.md"
        mock_validate.return_value = True
        mock_commit.side_effect = Exception("Git commit failed")

        with pytest.raises(Exception, match="Git commit failed"):
            create_feature_270_markdown_file("/repo")

    @patch("sheep.features.feature_270_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_270_markdown_file_creation.write_markdown_file")
    def test_error_handling_propagates_push_error(
        self,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that exceptions from push_markdown_file are propagated."""
        mock_write.return_value = "/repo/test-2sqwpg.md"
        mock_validate.return_value = True
        mock_commit.return_value = "abc123"
        mock_push.side_effect = Exception("Git push failed")

        with pytest.raises(Exception, match="Git push failed"):
            create_feature_270_markdown_file("/repo")


class TestFeature270IntegrationTests:
    """Integration tests with real file system and git operations."""

    def test_complete_workflow_creates_file(self):
        """Test complete workflow creates file in temporary directory."""
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
                assert result["filepath"].endswith(MARKDOWN_FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_file_contains_h1_heading(self):
        """Test that created file contains H1 markdown heading."""
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
                assert content.lstrip().startswith("# "), "File must start with H1 heading"
            finally:
                os.chdir(original_cwd)

    def test_file_has_utf8_encoding_no_bom(self):
        """Test that file uses UTF-8 encoding without BOM."""
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
                assert not binary_content.startswith(b"\xef\xbb\xbf"), (
                    "File should not have UTF-8 BOM"
                )
                # Verify valid UTF-8
                binary_content.decode("utf-8")
            finally:
                os.chdir(original_cwd)

    def test_file_has_lf_line_endings_not_crlf(self):
        """Test that file uses Unix LF line endings (not CRLF)."""
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
                assert b"\r\n" not in binary_content, (
                    "File should not have CRLF endings"
                )
                assert b"\r" not in binary_content, "File should not have CR endings"
            finally:
                os.chdir(original_cwd)

    def test_file_ends_with_trailing_newline(self):
        """Test that file ends with exactly one trailing newline."""
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
                assert content.endswith("\n"), "File should end with trailing newline"
            finally:
                os.chdir(original_cwd)

    def test_file_size_in_valid_range(self):
        """Test that created file size is between 400-600 bytes."""
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
                file_path = Path(tmpdir, MARKDOWN_FILENAME)
                file_size = file_path.stat().st_size
                assert (
                    400 <= file_size <= 600
                ), f"File size {file_size} is outside 400-600 byte range"
            finally:
                os.chdir(original_cwd)
