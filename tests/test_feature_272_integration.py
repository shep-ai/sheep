"""Integration tests for feature 272: Creating markdown file test-6poz5r.md with title and prose content.

These tests validate the complete feature workflow end-to-end:
- File is created at repository root with correct filename
- File contains H1 heading as first line
- File contains blank line separator after heading
- File contains exactly 2-3 sentences of prose content
- File is encoded as UTF-8 without BOM
- File uses Unix LF line endings (not CRLF)
- File size is within expected range (150-600 bytes)
- File is properly committed to git with conventional message
- File is pushed to feature branch
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import validate_markdown_file
from sheep.features.feature_272_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_272_markdown_file,
)


@pytest.fixture
def cleanup_test_file():
    """Clean up test file after each test."""
    yield
    # Cleanup after test
    test_file = Path.cwd() / MARKDOWN_FILENAME
    if test_file.exists():
        test_file.unlink()


def create_valid_test_markdown() -> str:
    """Create valid test markdown content with H1 heading and 2-3 sentences."""
    return "# Cloud Computing Architecture\n\nCloud computing represents a fundamental shift in how organizations deploy and scale applications through distributed computing resources. Modern cloud platforms enable businesses to leverage infrastructure-as-a-service, platform-as-a-service, and software-as-a-service models for improved flexibility and cost efficiency. The adoption of cloud technologies continues to accelerate digital transformation across industries.\n"


class TestFeature272EndToEndIntegration:
    """End-to-end integration tests for the complete feature 272 workflow."""

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_create_feature_272_markdown_file_returns_dict(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that create_feature_272_markdown_file() returns dict with required keys."""
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        result = create_feature_272_markdown_file()

        # Verify return type and structure
        assert isinstance(result, dict)
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_file_created_at_repo_root_with_correct_filename(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that file is created at repository root with exact filename test-6poz5r.md."""
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        result = create_feature_272_markdown_file()

        # Verify file exists
        test_file = Path.cwd() / MARKDOWN_FILENAME
        assert test_file.exists(), f"File {MARKDOWN_FILENAME} was not created"
        assert test_file.name == MARKDOWN_FILENAME
        assert test_file.is_file()

        # Verify filepath in result
        assert MARKDOWN_FILENAME in result["filepath"]

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_file_contains_h1_heading(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that created file contains exactly one H1 heading as first line."""
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        result = create_feature_272_markdown_file()

        # Verify H1 heading in returned content
        lines = result["content"].split("\n")
        assert lines[0].startswith("# "), "First line must be H1 heading"
        assert len(lines[0]) > 2, "H1 heading must have content"

        # Verify in actual file
        test_file = Path.cwd() / MARKDOWN_FILENAME
        file_content = test_file.read_text(encoding="utf-8")
        file_lines = file_content.split("\n")
        assert file_lines[0].startswith("# ")

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_file_has_blank_line_after_heading(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that file contains blank line separator after H1 heading."""
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        result = create_feature_272_markdown_file()

        # Verify blank line in returned content
        lines = result["content"].split("\n")
        assert len(lines) >= 2, "Content must have at least heading and blank line"
        assert lines[1] == "", "Second line must be blank"

        # Verify in actual file
        test_file = Path.cwd() / MARKDOWN_FILENAME
        file_content = test_file.read_text(encoding="utf-8")
        file_lines = file_content.split("\n")
        assert file_lines[1] == ""

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_file_contains_2_to_3_sentences(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that file contains exactly 2-3 sentences of prose content."""
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        result = create_feature_272_markdown_file()

        # Count sentences (periods) in returned content
        sentence_count = result["content"].count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

        # Verify in actual file
        test_file = Path.cwd() / MARKDOWN_FILENAME
        file_content = test_file.read_text(encoding="utf-8")
        file_sentence_count = file_content.count(".")
        assert 2 <= file_sentence_count <= 3

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_file_uses_utf8_encoding_without_bom(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that file is saved with UTF-8 encoding and no BOM."""
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        result = create_feature_272_markdown_file()

        # Check encoding by reading file as binary
        test_file = Path.cwd() / MARKDOWN_FILENAME
        binary_content = test_file.read_bytes()

        # Verify not UTF-8 with BOM (BOM is EF BB BF)
        assert not binary_content.startswith(
            b"\xef\xbb\xbf"
        ), "File should not have UTF-8 BOM"

        # Verify can decode as UTF-8
        decoded = binary_content.decode("utf-8")
        assert decoded == result["content"]

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_file_uses_lf_line_endings_not_crlf(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that file uses Unix LF line endings, not CRLF."""
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        result = create_feature_272_markdown_file()

        # Check line endings by reading file as binary
        test_file = Path.cwd() / MARKDOWN_FILENAME
        binary_content = test_file.read_bytes()

        # Verify no CRLF (0x0D 0x0A)
        assert b"\r\n" not in binary_content, "File should use LF line endings, not CRLF"

        # Verify file has LF
        assert b"\n" in binary_content, "File should contain newlines"

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_file_size_in_expected_range(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that created file size is in expected range (150-600 bytes)."""
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        result = create_feature_272_markdown_file()

        # Check file size
        test_file = Path.cwd() / MARKDOWN_FILENAME
        file_size = test_file.stat().st_size
        assert 150 <= file_size <= 600, (
            f"File size {file_size} bytes outside expected range (150-600)"
        )

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_file_ends_with_trailing_newline(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that created file ends with trailing newline (Unix convention)."""
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        result = create_feature_272_markdown_file()

        # Verify trailing newline in returned content
        assert result["content"].endswith(
            "\n"
        ), "Content must end with trailing newline"

        # Verify in actual file
        test_file = Path.cwd() / MARKDOWN_FILENAME
        file_content = test_file.read_text(encoding="utf-8")
        assert file_content.endswith("\n")

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_commit_message_uses_conventional_format(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that commit message follows conventional format feat(272): ..."""
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        result = create_feature_272_markdown_file()

        # Verify commit message format
        commit_msg = result["commit_message"]
        assert commit_msg.startswith(
            f"feat({FEATURE_NUMBER}): "
        ), "Commit message must use conventional format"
        assert MARKDOWN_FILENAME in commit_msg, "Commit message must include filename"

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_content_is_meaningful_prose(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that generated content is meaningful prose, not placeholder."""
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        result = create_feature_272_markdown_file()

        # Verify prose is meaningful
        content_lower = result["content"].lower()
        assert (
            "lorem ipsum" not in content_lower
        ), "Content should not be lorem ipsum"
        assert "placeholder" not in content_lower, "Content should not be placeholder"
        assert (
            "todo" not in content_lower
        ), "Content should not contain todo markers"

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_file_structure_matches_success_criteria(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that file structure matches all success criteria format.

        Expected format:
        Line 1: # Title
        Line 2: (blank)
        Lines 3+: 2-3 sentences
        """
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        result = create_feature_272_markdown_file()

        lines = result["content"].split("\n")

        # Verify structure
        assert lines[0].startswith("# "), "First line must be H1 heading"
        assert lines[1] == "", "Second line must be blank"
        assert len(lines) > 2, "Must have content after blank line"

        # Verify prose
        prose_lines = [line for line in lines[2:] if line.strip()]
        assert len(prose_lines) > 0, "Must have prose content"
        prose_content = "\n".join(prose_lines).strip()
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3, (
            f"Must have 2-3 sentences, found {sentence_count}"
        )

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_git_commit_called_with_correct_parameters(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that commit_markdown_file() is called with correct parameters."""
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        result = create_feature_272_markdown_file()

        # Verify commit was called
        assert mock_commit.called, "commit_markdown_file() should be called"
        # Check that the custom_message parameter was passed
        call_kwargs = mock_commit.call_args[1] if mock_commit.call_args[1] else {}
        if "custom_message" in call_kwargs:
            assert f"feat({FEATURE_NUMBER})" in call_kwargs["custom_message"]

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_git_push_called_after_commit(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that push_markdown_file() is called after commit."""
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        result = create_feature_272_markdown_file()

        # Verify both commit and push were called
        assert mock_commit.called, "commit_markdown_file() should be called"
        assert mock_push.called, "push_markdown_file() should be called"

        # Verify push was called after commit (push result in return value)
        assert "push_result" in result

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_complete_workflow_integration(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Full integration test: complete workflow from generation to push."""
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        # Execute the complete feature workflow
        result = create_feature_272_markdown_file()

        # Verify all workflow steps completed
        assert result["content"] == test_content, "Content should match generated"
        assert MARKDOWN_FILENAME in result["filepath"], "Filepath should contain filename"
        assert (
            f"feat({FEATURE_NUMBER})" in result["commit_message"]
        ), "Should have conventional commit"
        assert result["push_result"] is not None, "Push result should be present"

        # Verify file was created
        test_file = Path.cwd() / MARKDOWN_FILENAME
        assert test_file.exists(), "File should be created"

        # Verify file content matches
        file_content = test_file.read_text(encoding="utf-8")
        assert file_content == test_content, "File content should match generated"

        # Verify file passes basic validation
        assert file_content.startswith("# "), "File should start with H1 heading"
        assert not file_content.startswith(
            b"\xef\xbb\xbf".decode("utf-8")
        ), "File should not have BOM"
        assert b"\r\n".decode("utf-8") not in file_content, "Should use LF not CRLF"

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_validation_called_before_commit(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that file validation passes before git operations.

        The feature should validate the file exists and is valid before committing.
        """
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        result = create_feature_272_markdown_file()

        # If we got this far with real file I/O, validation must have passed
        test_file = Path.cwd() / MARKDOWN_FILENAME
        assert test_file.exists(), "File must exist after validation"

        # Verify file can be validated
        try:
            validate_markdown_file(str(test_file))
        except Exception as e:
            pytest.fail(f"File validation failed: {e}")

    @patch("sheep.features.feature_272_markdown_file_creation.generate_markdown_content")
    @patch("sheep.features.feature_272_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_272_markdown_file_creation.push_markdown_file")
    def test_multiple_runs_create_valid_files(
        self, mock_push, mock_commit, mock_generate, cleanup_test_file
    ):
        """Test that feature can be run multiple times and produces valid files each time."""
        test_content = create_valid_test_markdown()
        mock_generate.return_value = test_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        # Run feature multiple times
        for i in range(3):
            # Clean up before each run
            test_file = Path.cwd() / MARKDOWN_FILENAME
            if test_file.exists():
                test_file.unlink()

            # Execute
            result = create_feature_272_markdown_file()

            # Verify each run produces valid result
            assert result is not None
            assert result["content"] == test_content
            assert (
                Path.cwd() / MARKDOWN_FILENAME
            ).exists(), f"Run {i + 1}: File should be created"

            # Clean up
            if test_file.exists():
                test_file.unlink()
