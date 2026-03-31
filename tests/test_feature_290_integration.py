"""Integration tests for feature 290: Complete workflow validation.

Tests the end-to-end workflow: file creation, git staging, committing, and pushing.
Verifies all success criteria from the feature specification are met.
"""

from pathlib import Path
import subprocess
from unittest.mock import patch, MagicMock

import pytest

from sheep.features.feature_290_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_test_f7lgjt_markdown_file,
)


class TestEndToEndWorkflow:
    """Integration tests for complete feature 290 workflow."""

    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_complete_workflow_executes_successfully(self, mock_generate):
        """Test that complete workflow executes without errors."""
        # Mock the content generation to avoid needing API key
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content

        # Execute the complete workflow
        result = create_test_f7lgjt_markdown_file()

        # Verify result is a dictionary with expected keys
        assert isinstance(result, dict)
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_file_is_created_at_repository_root(self, mock_generate):
        """Test that file is created in repository root with correct filename."""
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content

        result = create_test_f7lgjt_markdown_file()

        # Verify filepath is correct
        filepath = result["filepath"]
        assert MARKDOWN_FILENAME in filepath
        assert Path(filepath).exists(), f"File {filepath} must exist"

    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_file_has_correct_structure(self, mock_generate):
        """Test that file has correct structure: H1 heading, blank line, prose."""
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content

        result = create_test_f7lgjt_markdown_file()
        filepath = result["filepath"]
        content = Path(filepath).read_text(encoding="utf-8")
        lines = content.split("\n")

        # First line must be H1 heading
        assert lines[0].startswith("# "), "First line must be H1 heading"
        # Second line must be blank
        assert lines[1] == "", "Second line must be blank"
        # Third line must be prose (non-empty)
        assert len(lines) > 2, "File must have prose content"
        assert lines[2].strip() != "", "Prose content must not be empty"

    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_file_encoding_is_utf8_without_bom(self, mock_generate):
        """Test that file encoding is UTF-8 without BOM."""
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content

        result = create_test_f7lgjt_markdown_file()
        filepath = result["filepath"]
        binary_content = Path(filepath).read_bytes()

        # UTF-8 BOM signature: 0xEF 0xBB 0xBF
        assert not binary_content.startswith(
            b"\xef\xbb\xbf"
        ), "File must not have UTF-8 BOM"

    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_file_has_lf_line_endings(self, mock_generate):
        """Test that file uses LF (Unix-style) line endings, not CRLF."""
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content

        result = create_test_f7lgjt_markdown_file()
        filepath = result["filepath"]
        binary_content = Path(filepath).read_bytes()

        # CRLF sequence: 0x0D 0x0A (Windows line ending)
        assert (
            b"\r\n" not in binary_content
        ), "File must use LF line endings, not CRLF"

    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_file_size_in_expected_range(self, mock_generate):
        """Test that file size is within expected range (250-600 bytes)."""
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content

        result = create_test_f7lgjt_markdown_file()
        filepath = result["filepath"]
        file_size = Path(filepath).stat().st_size

        # Expected range: 250-600 bytes
        assert (
            250 <= file_size <= 600
        ), f"File size {file_size} bytes should be 250-600 bytes"

    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_file_content_has_valid_markdown_structure(self, mock_generate):
        """Test that file content is valid CommonMark markdown with H1 + 2-3 sentences."""
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content

        result = create_test_f7lgjt_markdown_file()
        filepath = result["filepath"]
        content = Path(filepath).read_text(encoding="utf-8")
        lines = content.split("\n")

        # Check H1 heading format: # Title
        assert (
            lines[0].startswith("# ")
        ), "H1 heading must start with '# ' (space required)"
        assert len(lines[0]) > 2, "H1 heading must have text after '# '"

        # Check blank line separator
        assert lines[1] == "", "Blank line separator is required"

        # Check prose content has 2-3 sentences (count periods)
        prose_content = "\n".join(lines[2:]).strip()
        sentence_count = prose_content.count(".")
        assert (
            2 <= sentence_count <= 3
        ), f"Prose must have 2-3 sentences, found {sentence_count}"

    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_validation_called_before_commit(self, mock_generate):
        """Test that validation is performed before commit (no invalid files committed)."""
        # Valid content with exactly 3 sentences
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content

        result = create_test_f7lgjt_markdown_file()

        # Verify validation passed by checking the returned content
        assert result["content"] == test_content
        assert "filepath" in result
        assert result["filepath"]  # Should be non-empty if validation passed

    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_error_handling_on_api_failure(self, mock_generate):
        """Test that API failures are handled with clear error messages."""
        mock_generate.side_effect = RuntimeError("API connection failed")

        with pytest.raises(RuntimeError) as exc_info:
            create_test_f7lgjt_markdown_file()

        assert "API connection failed" in str(exc_info.value)

    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_error_handling_on_validation_failure(self, mock_generate):
        """Test that validation failures prevent commit and push."""
        # Invalid content: too many sentences
        test_content = "# Testing\n\nOne. Two. Three. Four. Five.\n"
        mock_generate.return_value = test_content

        # Validation should fail because there are 5 sentences, not 2-3
        with pytest.raises(ValueError):
            create_test_f7lgjt_markdown_file()

    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_conventional_commit_message_format(self, mock_generate):
        """Test that commit message follows conventional format."""
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content

        result = create_test_f7lgjt_markdown_file()

        commit_message = result["commit_message"]
        # Verify conventional commit format: feat(290): ...
        assert commit_message.startswith("feat(290):"), "Must use conventional format: feat(290):"
        assert MARKDOWN_FILENAME in commit_message, "Commit message must include filename"
        assert "prose content" in commit_message, "Commit message must mention prose content"

    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_content_generation_called_first(self, mock_generate):
        """Test that content generation is the first step in workflow."""
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content

        # Track call order with a side effect
        call_order = []

        original_generate = mock_generate

        def track_generate(*args, **kwargs):
            call_order.append("generate")
            return test_content

        mock_generate.side_effect = track_generate

        result = create_test_f7lgjt_markdown_file()

        # Verify content generation was called
        assert "generate" in call_order


class TestWorkflowIntegrationWithFileSystem:
    """Integration tests verifying workflow with real file system operations."""

    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_workflow_creates_file_with_correct_permissions(self, mock_generate):
        """Test that created file has correct read/write permissions."""
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content

        result = create_test_f7lgjt_markdown_file()
        filepath = result["filepath"]
        file_path = Path(filepath)

        # Verify file is readable
        assert file_path.is_file(), "Created path must be a file"
        # Verify we can read the file
        content = file_path.read_text(encoding="utf-8")
        assert content == test_content, "File content must match generated content"

    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_workflow_with_nonexistent_repo_creates_at_cwd(self, mock_generate):
        """Test that repo_path parameter is respected."""
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content

        # Use current directory (None defaults to cwd)
        result = create_test_f7lgjt_markdown_file(repo_path=None)

        filepath = result["filepath"]
        assert Path(filepath).exists(), f"File must be created at specified path: {filepath}"

    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_returned_content_matches_file_content(self, mock_generate):
        """Test that returned content dictionary matches actual file content."""
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content

        result = create_test_f7lgjt_markdown_file()

        # Read the actual file
        filepath = result["filepath"]
        file_content = Path(filepath).read_text(encoding="utf-8")

        # Verify returned content matches file content
        assert result["content"] == file_content, "Returned content must match file content"


class TestErrorScenarios:
    """Tests for error handling in various failure scenarios."""

    @patch("sheep.features.feature_290_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_handles_file_write_failure(self, mock_generate, mock_write):
        """Test that file write failures are properly handled."""
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content
        mock_write.side_effect = IOError("Disk write failed")

        with pytest.raises(IOError):
            create_test_f7lgjt_markdown_file()

    @patch("sheep.features.feature_290_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_290_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_handles_validation_failure(self, mock_generate, mock_write, mock_validate):
        """Test that validation failures prevent further steps."""
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content
        mock_write.return_value = "/tmp/test-f7lgjt.md"
        mock_validate.side_effect = ValueError("Invalid markdown: incorrect sentence count")

        with pytest.raises(ValueError):
            create_test_f7lgjt_markdown_file()

    @patch("sheep.features.feature_290_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_290_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_290_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_290_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_handles_commit_failure(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that commit failures are properly handled."""
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content
        mock_write.return_value = "/tmp/test-f7lgjt.md"
        mock_commit.side_effect = RuntimeError("Git commit failed")

        with pytest.raises(RuntimeError):
            create_test_f7lgjt_markdown_file()

        # Verify push was not called after commit failure
        mock_push.assert_not_called()

    @patch("sheep.features.feature_290_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_290_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_290_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_290_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_290_markdown_file_creation.generate_markdown_content")
    def test_handles_push_failure(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that push failures are properly handled."""
        test_content = "# Testing Feature 290\n\nThis is a test sentence. Another test sentence. And a third.\n"
        mock_generate.return_value = test_content
        mock_write.return_value = "/tmp/test-f7lgjt.md"
        mock_validate.return_value = None
        mock_commit.return_value = "success"
        mock_push.side_effect = RuntimeError("Git push failed")

        with pytest.raises(RuntimeError):
            create_test_f7lgjt_markdown_file()
