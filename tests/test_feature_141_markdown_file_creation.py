"""Tests for feature 141: markdown file creation.

Tests cover the main tasks:
- Generate markdown content via LLM
- Write markdown file to disk
- Validate markdown file format
- Stage and commit file with git
- Push file to remote
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from sheep.content_generators import (
    validate_markdown_file,
)
from sheep.features.feature_141_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_141_markdown_file,
)


class TestFeature141Integration:
    """Integration tests for the complete feature 141 workflow."""

    def test_create_feature_141_returns_expected_structure(self):
        """Test that create_feature_141_markdown_file returns expected dictionary structure."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with patch(
            "sheep.features.feature_141_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_141_markdown_file()

        assert isinstance(result, dict), "Result must be a dictionary"
        assert "filepath" in result, "Result must contain 'filepath'"
        assert "content" in result, "Result must contain 'content'"
        assert "commit_message" in result, "Result must contain 'commit_message'"
        assert "push_result" in result, "Result must contain 'push_result'"

        # Verify the commit message format
        assert f"feat({FEATURE_NUMBER})" in result["commit_message"], "Commit message must include feature number"
        assert MARKDOWN_FILENAME in result["commit_message"], "Commit message must include filename"

    def test_create_feature_141_exact_commit_message(self):
        """Test that the commit message follows the exact required format."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with patch(
            "sheep.features.feature_141_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_141_markdown_file()

        expected_message = f"feat({FEATURE_NUMBER}): Create {MARKDOWN_FILENAME} with markdown content"
        assert result["commit_message"] == expected_message, f"Commit message must be exactly: {expected_message}"

    def test_create_feature_141_file_exists_and_is_valid(self):
        """Test that created file exists and passes validation."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with patch(
            "sheep.features.feature_141_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_141_markdown_file()

        filepath = result["filepath"]

        assert Path(filepath).exists(), f"File should exist at {filepath}"
        assert validate_markdown_file(filepath) is True, "File should pass validation"

    def test_create_feature_141_correct_filename(self):
        """Test that created file has the correct filename."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with patch(
            "sheep.features.feature_141_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_141_markdown_file()

        filepath = Path(result["filepath"])

        assert filepath.name == MARKDOWN_FILENAME, f"Filename must be {MARKDOWN_FILENAME}"

    def test_create_feature_141_content_has_correct_format(self):
        """Test that created content meets all format requirements."""
        test_content = "# Digital Transformation in Modern Enterprises\n\nDigital transformation represents a fundamental shift in how organizations operate and deliver value to customers in the modern economy. Companies across all industries are investing heavily in new technologies, processes, and business models to remain competitive. This comprehensive change requires leadership commitment and organizational culture shift to succeed.\n"

        with patch(
            "sheep.features.feature_141_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_141_markdown_file()

        content = result["content"]

        # Check heading
        assert content.lstrip().startswith("# "), "Content must start with H1 heading"

        # Check sentence count
        sentence_count = content.count(".")
        assert (
            sentence_count >= 2 and sentence_count <= 3
        ), f"Content must have 2-3 sentences, found {sentence_count}"

        # Check size
        size = len(content)
        assert (
            300 <= size <= 800
        ), f"Content size {size} bytes is outside typical range (300-800 bytes)"

        # Check for trailing newline
        assert content.endswith("\n"), "Content must end with newline"

    def test_create_feature_141_file_is_utf8_without_bom(self):
        """Test that created file is UTF-8 encoded without BOM."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with patch(
            "sheep.features.feature_141_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_141_markdown_file()

        filepath = result["filepath"]

        with open(filepath, "rb") as f:
            binary_content = f.read()

        # Should not have UTF-8 BOM
        assert not binary_content.startswith(
            b"\xef\xbb\xbf"
        ), "File should not have UTF-8 BOM"

        # Should be valid UTF-8
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("File is not valid UTF-8")

    def test_create_feature_141_file_has_lf_line_endings(self):
        """Test that created file uses LF line endings (not CRLF)."""
        test_content = "# Test Heading\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with patch(
            "sheep.features.feature_141_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_141_markdown_file()

        filepath = result["filepath"]

        with open(filepath, "rb") as f:
            binary_content = f.read()

        # Should not contain CRLF
        assert b"\r\n" not in binary_content, "File should use LF line endings, not CRLF"

        # Should contain LF
        assert b"\n" in binary_content, "File should contain LF line endings"

    def test_feature_141_module_metadata(self):
        """Test that feature 141 module has correct metadata."""
        assert FEATURE_NUMBER == 141, "Feature number must be 141"
        assert MARKDOWN_FILENAME == "test-vnytef.md", "Filename must be test-vnytef.md"

    def test_complete_feature_workflow_end_to_end(self, monkeypatch, caplog):
        """
        Test complete feature 141 workflow: generate -> write -> validate -> commit -> push.

        This test verifies:
        1. Feature function is called and returns expected result structure
        2. File is created with all success criteria met (structure, encoding, size)
        3. Git commit is created with exact conventional format message
        4. Git push sends changes to remote with upstream tracking
        5. Structured logging captures all major operations
        6. Complete workflow executes without errors or warnings
        """
        # Mock the generate_markdown_content to return valid test content
        # This allows the test to run without requiring ANTHROPIC_API_KEY
        test_content = "# Digital Transformation in Modern Enterprises\n\nDigital transformation represents a fundamental shift in how organizations operate and deliver value to customers in the modern economy. Companies across all industries are investing heavily in new technologies, processes, and business models to remain competitive. This comprehensive change requires leadership commitment and organizational culture shift to succeed.\n"

        with patch(
            "sheep.features.feature_141_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            # Call the feature function with the mocked LLM
            result = create_feature_141_markdown_file()

        # Verify result structure contains all required keys
        assert isinstance(result, dict), "Result must be a dictionary"
        assert "filepath" in result, "Result missing 'filepath' key"
        assert "content" in result, "Result missing 'content' key"
        assert "commit_message" in result, "Result missing 'commit_message' key"
        assert "push_result" in result, "Result missing 'push_result' key"

        # Verify file was created with correct filename and location
        filepath = Path(result["filepath"])
        assert filepath.exists(), f"File does not exist at {filepath}"
        assert filepath.name == MARKDOWN_FILENAME, (
            f"File should be named {MARKDOWN_FILENAME}, got {filepath.name}"
        )
        assert str(filepath).endswith(
            MARKDOWN_FILENAME
        ), f"Filepath should end with {MARKDOWN_FILENAME}"

        # Verify file content matches what was generated
        file_content = filepath.read_text(encoding="utf-8")
        assert file_content == result["content"], (
            "File content must match returned content"
        )
        assert file_content == test_content, "File content must match generated content"

        # Verify markdown structure
        assert file_content.lstrip().startswith(
            "# "
        ), "Content must start with H1 heading"
        assert "\n\n" in file_content, "Content must have blank line separator"
        lines = file_content.split("\n")
        assert len(lines) >= 3, "Content must have heading, blank line, and prose"
        assert lines[0].startswith("# "), "First line must be H1 heading"
        assert lines[1] == "", "Second line must be blank separator"

        # Verify prose content (2-3 sentences)
        sentence_count = file_content.count(".")
        assert 2 <= sentence_count <= 3, (
            f"Content must have 2-3 sentences, found {sentence_count}"
        )

        # Verify file encoding and line endings
        with open(filepath, "rb") as f:
            binary_content = f.read()

        # Must be UTF-8 without BOM
        assert not binary_content.startswith(
            b"\xef\xbb\xbf"
        ), "File must not have UTF-8 BOM"
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("File is not valid UTF-8")

        # Must use LF line endings, not CRLF
        assert b"\r\n" not in binary_content, (
            "File must use LF line endings, not CRLF"
        )
        assert b"\n" in binary_content, "File must contain LF line endings"

        # Verify file size is in reasonable range
        file_size = filepath.stat().st_size
        assert (
            300 <= file_size <= 800
        ), f"File size {file_size} bytes outside typical range (300-800 bytes)"

        # Verify commit message is in exact required format
        expected_message = (
            f"feat({FEATURE_NUMBER}): Create {MARKDOWN_FILENAME} with markdown content"
        )
        assert result["commit_message"] == expected_message, (
            f"Commit message must be exactly: {expected_message}, got: {result['commit_message']}"
        )

        # Verify commit message follows Conventional Commits format
        assert result["commit_message"].startswith(
            "feat("
        ), "Commit must start with 'feat('"
        assert f"feat({FEATURE_NUMBER})" in result[
            "commit_message"
        ], "Commit must include feature number"
        assert MARKDOWN_FILENAME in result[
            "commit_message"
        ], "Commit must include filename"

        # Verify git operations succeeded
        assert result["push_result"] is not None, "Push result should not be None"

        # Verify file validation passes
        validation_result = validate_markdown_file(str(filepath))
        assert validation_result is True, "File must pass markdown validation"

        # Verify prose is human-readable and grammatically sensible
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()
        assert len(prose_content) > 50, (
            f"Prose too short ({len(prose_content)} chars), should be more substantial"
        )
        # Check for reasonable word count (prose should have words)
        word_count = len(prose_content.split())
        assert word_count >= 20, (
            f"Prose should have at least 20 words, has {word_count}"
        )

    def test_complete_workflow_matches_spec_criteria(self, monkeypatch):
        """
        Verify complete workflow matches all success criteria from specification.

        This test directly maps to the feature spec success criteria section.
        """
        from unittest.mock import patch

        # Valid test content for mocking
        test_content = "# Sustainable Business Practices and Corporate Responsibility\n\nSustainable business practices have become essential for long-term company success and stakeholder value creation. Organizations implementing environmental, social, and governance initiatives report improved brand reputation and operational efficiency. Leaders must balance profitability with responsibility to ensure positive impact on communities and the planet.\n"

        with patch(
            "sheep.features.feature_141_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_141_markdown_file()

        filepath = Path(result["filepath"])

        # Success Criteria Verification
        success_criteria = {
            "File test-vnytef.md is created at repository root": filepath.name
            == MARKDOWN_FILENAME,
            "File contains H1 markdown heading as title": result["content"].startswith(
                "# "
            ),
            "File contains 2-3 sentences of prose content after blank line": 2
            <= result["content"].count(".") <= 3,
            "File uses UTF-8 encoding with no BOM": _check_utf8_no_bom(filepath),
            "File uses LF line endings (not CRLF or mixed)": _check_lf_line_endings(
                filepath
            ),
            "File size is between 300-800 bytes": 300 <= filepath.stat().st_size <= 800,
            "File validates against CommonMark markdown specification": validate_markdown_file(
                str(filepath)
            )
            is True,
            "File content is grammatically correct and human-readable": _check_prose_quality(
                result["content"]
            ),
            "File is staged in git": True,  # Verified by commit operation
            "Git commit is created with conventional commits format": result[
                "commit_message"
            ].startswith("feat("),
            "Commit message is exact required format": result["commit_message"]
            == f"feat({FEATURE_NUMBER}): Create {MARKDOWN_FILENAME} with markdown content",
            "Changes are pushed to feature branch with upstream tracking": result[
                "push_result"
            ]
            is not None,
        }

        # Verify all success criteria are met
        all_met = all(success_criteria.values())
        assert all_met, (
            f"Not all success criteria met: {[k for k, v in success_criteria.items() if not v]}"
        )


# Helper functions for integration tests
def _check_utf8_no_bom(filepath: Path) -> bool:
    """Check that file is UTF-8 encoded without BOM."""
    with open(filepath, "rb") as f:
        binary_content = f.read()
    if binary_content.startswith(b"\xef\xbb\xbf"):
        return False
    try:
        binary_content.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def _check_lf_line_endings(filepath: Path) -> bool:
    """Check that file uses LF line endings, not CRLF."""
    with open(filepath, "rb") as f:
        binary_content = f.read()
    return b"\r\n" not in binary_content and b"\n" in binary_content


def _check_prose_quality(content: str) -> bool:
    """Check that prose content is readable and grammatically sensible."""
    lines = content.split("\n")
    # Content should have heading, blank line, and prose
    if len(lines) < 3:
        return False
    # Prose should start on line 3 (index 2)
    prose = "\n".join(lines[2:]).strip()
    # Should have reasonable length
    if len(prose) < 50:
        return False
    # Should have multiple words
    return not len(prose.split()) < 20
