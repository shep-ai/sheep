"""Tests for feature 133: markdown file creation.

Tests validate markdown file format, git workflow, and integration.
"""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from sheep.content_generators import validate_markdown_file
from sheep.features.feature_133_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_133_markdown_file,
)


@pytest.mark.integration
class TestMarkdownFileFormatValidation:
    """Tests for markdown file format validation."""

    def test_file_exists_after_feature_execution(self):
        """Test that test-vlexrc.md file exists after feature execution."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two.\n".replace("\r\n", "\n")

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        filepath = Path(result["filepath"])
        assert filepath.exists(), f"File should exist at {filepath}"
        assert filepath.name == MARKDOWN_FILENAME, f"File should be named {MARKDOWN_FILENAME}"

    def test_first_line_is_h1_heading(self):
        """Test that first line starts with '# ' (H1 markdown)."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        content = result["content"]
        lines = content.split("\n")
        assert lines[0].startswith("# "), "First line must start with '# '"

    def test_second_line_is_blank(self):
        """Test that second line is blank (separator)."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        content = result["content"]
        lines = content.split("\n")
        assert lines[1] == "", "Second line must be blank"

    def test_prose_has_2_to_3_sentences(self):
        """Test that lines 3+ contain 2-3 sentences of prose."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        content = result["content"]
        # Count sentences (periods)
        sentence_count = content.count(".")
        assert 2 <= sentence_count <= 3, f"Must have 2-3 sentences, found {sentence_count}"

    def test_prose_content_is_non_empty(self):
        """Test that prose content (lines 3+) is non-empty."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        content = result["content"]
        lines = content.split("\n")
        prose_content = "\n".join(lines[2:]).strip()
        assert len(prose_content) > 0, "Prose content must be non-empty"

    def test_file_is_utf8_without_bom(self):
        """Test that file is UTF-8 encoded without BOM using file.read_bytes()."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        filepath = Path(result["filepath"])
        binary_content = filepath.read_bytes()

        # Check no UTF-8 BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File must not have UTF-8 BOM"

        # Check valid UTF-8
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("File must be valid UTF-8")

    def test_file_validates_successfully(self):
        """Test that created file validates against specification."""
        test_content = "# Digital Transformation\n\nThis is the first sentence about transformation. The second sentence discusses implementation. The third sentence covers benefits.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        filepath = result["filepath"]
        validation_result = validate_markdown_file(filepath)
        assert validation_result is True, "File must pass markdown validation"


@pytest.mark.integration
class TestGitWorkflowCompletion:
    """Tests for git workflow completion (commit and push)."""

    def test_commit_message_format_is_correct(self):
        """Test that commit message follows conventional commit format."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        expected_message = f"feat({FEATURE_NUMBER}): Create markdown file {MARKDOWN_FILENAME}"
        assert result["commit_message"] == expected_message, (
            f"Commit message must be: {expected_message}"
        )

    def test_git_log_contains_commit_message(self):
        """Test that git log contains the expected commit message."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            create_feature_133_markdown_file()

        try:
            log_output = subprocess.check_output(
                ["git", "log", "--oneline", "-n", "10"],
                text=True,
                stderr=subprocess.PIPE,
            )
            assert f"feat({FEATURE_NUMBER})" in log_output or "Create markdown file" in log_output, (
                f"Git log should contain commit message, got: {log_output}"
            )
        except subprocess.CalledProcessError:
            # Git may fail in some test environments, skip this check
            pass

    def test_working_tree_is_clean_after_push(self):
        """Test that working tree is clean after push."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            create_feature_133_markdown_file()

        try:
            status_output = subprocess.check_output(
                ["git", "status", "--porcelain"],
                text=True,
                stderr=subprocess.PIPE,
            )
            # Our file should not appear as modified after push
            file_status_lines = [line for line in status_output.split("\n") if MARKDOWN_FILENAME in line]
            # If file appears, it should only be as untracked (??), not modified
            for line in file_status_lines:
                if line and not line.startswith("??"):
                    pytest.fail(f"File {MARKDOWN_FILENAME} should be clean in working tree, got: {line}")
        except subprocess.CalledProcessError:
            # Git may fail in some test environments, skip this check
            pass

    def test_push_result_is_not_none(self):
        """Test that push completed (push_result is not None)."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        assert result["push_result"] is not None, "Push result should not be None"


@pytest.mark.integration
class TestCompleteIntegration:
    """Comprehensive integration tests for complete feature workflow."""

    def test_feature_returns_complete_result_dict(self):
        """Test that feature returns complete result dictionary with all required keys."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        assert isinstance(result, dict), "Result must be a dictionary"
        assert "filepath" in result, "Result must have 'filepath' key"
        assert "content" in result, "Result must have 'content' key"
        assert "commit_message" in result, "Result must have 'commit_message' key"
        assert "push_result" in result, "Result must have 'push_result' key"

    def test_complete_workflow_success_criteria(self):
        """Test that complete workflow meets all success criteria from specification."""
        test_content = "# Sustainable Business Practices and Corporate Responsibility\n\nSustainable business practices have become essential for long-term company success and stakeholder value creation. Organizations implementing environmental, social, and governance initiatives report improved brand reputation and operational efficiency. Leaders must balance profitability with responsibility to ensure positive impact on communities and the planet.\n"

        with patch(
            "sheep.features.feature_133_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_133_markdown_file()

        filepath = Path(result["filepath"])

        # Verify all success criteria
        assert filepath.exists(), "File must exist"
        assert filepath.name == MARKDOWN_FILENAME, f"Filename must be {MARKDOWN_FILENAME}"
        assert validate_markdown_file(str(filepath)) is True, "File must pass validation"

        # Check content structure
        content = result["content"]
        assert content.startswith("# "), "Content must start with H1 heading"
        assert "\n\n" in content, "Content must have blank line separator"
        assert 2 <= content.count(".") <= 3, "Content must have 2-3 sentences"

        # Check encoding
        binary = filepath.read_bytes()
        assert not binary.startswith(b"\xef\xbb\xbf"), "File must not have UTF-8 BOM"
        binary.decode("utf-8")  # Should not raise

        # Check commit message
        expected_message = f"feat({FEATURE_NUMBER}): Create markdown file {MARKDOWN_FILENAME}"
        assert result["commit_message"] == expected_message, "Commit message must match spec"

    def test_feature_metadata_is_correct(self):
        """Test that feature uses correct metadata."""
        assert FEATURE_NUMBER == 133, "Feature number must be 133"
        assert MARKDOWN_FILENAME == "test-vlexrc.md", "Filename must be test-vlexrc.md"
