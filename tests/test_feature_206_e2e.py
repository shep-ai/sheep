"""End-to-end integration tests for feature 206: Complete workflow verification.

These tests verify that the complete feature 206 workflow works correctly from
start to finish: file creation → validation → git operations.

Tests verify:
- File creation with correct content
- File encoding and line endings
- File size within bounds
- All validation checks pass
- Git operations succeed in sequence
- All success criteria from the feature specification are met
"""

import subprocess
from pathlib import Path
from unittest.mock import patch

from sheep.features.feature_206_markdown_file_creation import (
    BRANCH_NAME,
    FEATURE_NUMBER,
    FILENAME,
    MAX_FILE_SIZE,
    MIN_FILE_SIZE,
    PROSE_CONTENT,
    TITLE_TEXT,
    create_markdown_file,
    main,
    validate_markdown_file,
)


class TestMainOrchestration:
    """Test suite for main() orchestration function."""

    def test_main_returns_zero_on_success(self):
        """Test that main() returns 0 when workflow completes successfully."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        # Mock git operations to avoid actual git calls
        with patch(
            "sheep.features.feature_206_markdown_file_creation.git_add"
        ), patch(
            "sheep.features.feature_206_markdown_file_creation.git_commit"
        ), patch(
            "sheep.features.feature_206_markdown_file_creation.git_push"
        ):
            result = main()

        # Assert success
        assert result == 0
        # Clean up
        if file_path.exists():
            file_path.unlink()

    def test_main_returns_one_on_file_creation_failure(self):
        """Test that main() returns 1 when file creation fails."""
        # Mock create_markdown_file to raise an error
        with patch(
            "sheep.features.feature_206_markdown_file_creation.create_markdown_file"
        ) as mock_create:
            mock_create.side_effect = OSError("Disk full")

            result = main()

        # Assert failure
        assert result == 1

    def test_main_returns_one_on_validation_failure(self):
        """Test that main() returns 1 when validation fails."""
        file_path = Path(FILENAME)
        # Create an invalid file (too small)
        file_path.write_text("# T\n\nS.\n")

        try:
            result = main()

            # Assert failure (validation should catch the size issue)
            assert result == 1
        finally:
            if file_path.exists():
                file_path.unlink()

    def test_main_returns_one_on_git_add_failure(self):
        """Test that main() returns 1 when git add fails."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        # Mock git_add to raise an error
        with patch(
            "sheep.features.feature_206_markdown_file_creation.git_add"
        ) as mock_git_add:
            mock_git_add.side_effect = subprocess.CalledProcessError(
                1, ["git", "add"], stderr="not a git repository"
            )

            result = main()

        # Assert failure
        assert result == 1
        # Clean up
        if file_path.exists():
            file_path.unlink()

    def test_main_returns_one_on_git_commit_failure(self):
        """Test that main() returns 1 when git commit fails."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        # Mock git_commit to raise an error
        with patch(
            "sheep.features.feature_206_markdown_file_creation.git_commit"
        ) as mock_git_commit:
            mock_git_commit.side_effect = subprocess.CalledProcessError(
                1, ["git", "commit"], stderr="nothing to commit"
            )

            result = main()

        # Assert failure
        assert result == 1
        # Clean up
        if file_path.exists():
            file_path.unlink()

    def test_main_returns_one_on_git_push_failure(self):
        """Test that main() returns 1 when git push fails."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        # Mock git_push to raise an error
        with patch(
            "sheep.features.feature_206_markdown_file_creation.git_push"
        ) as mock_git_push:
            mock_git_push.side_effect = subprocess.CalledProcessError(
                1, ["git", "push"], stderr="connection refused"
            )

            result = main()

        # Assert failure
        assert result == 1
        # Clean up
        if file_path.exists():
            file_path.unlink()

    def test_main_logs_workflow_steps(self):
        """Test that main() logs each workflow step."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        with patch(
            "sheep.features.feature_206_markdown_file_creation.git_add"
        ), patch(
            "sheep.features.feature_206_markdown_file_creation.git_commit"
        ), patch(
            "sheep.features.feature_206_markdown_file_creation.git_push"
        ), patch(
            "sheep.features.feature_206_markdown_file_creation._logger"
        ) as mock_logger:
            main()

            # Verify logging calls for each step
            # Should have info logs for starting, steps, and completion
            assert mock_logger.info.call_count >= 6

        # Clean up
        if file_path.exists():
            file_path.unlink()


class TestEndToEndWorkflow:
    """Comprehensive end-to-end workflow tests verifying all success criteria."""

    def test_e2e_file_creation_and_validation(self):
        """Test that file is created and passes all validation checks."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        # Create file
        created_path = create_markdown_file()

        # Assert file exists
        assert file_path.exists()
        assert created_path == file_path

        # Assert file validation passes
        assert validate_markdown_file(file_path) is True

        # Clean up
        if file_path.exists():
            file_path.unlink()

    def test_e2e_file_has_correct_name(self):
        """Test that created file has the correct filename."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()

        assert file_path.exists()
        assert file_path.name == "test-afcl8i.md"

        # Clean up
        if file_path.exists():
            file_path.unlink()

    def test_e2e_file_has_correct_content_structure(self):
        """Test that file has correct markdown structure: H1 + blank + prose."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()

        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Verify structure
        assert lines[0] == f"# {TITLE_TEXT}"
        assert lines[1] == ""
        assert PROSE_CONTENT in content
        assert content.endswith("\n")

        # Clean up
        if file_path.exists():
            file_path.unlink()

    def test_e2e_file_is_utf8_without_bom(self):
        """Test that file is encoded in UTF-8 without BOM."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()

        # Check UTF-8 encoding
        content = file_path.read_text(encoding="utf-8")
        assert isinstance(content, str)

        # Check no BOM
        binary_content = file_path.read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Clean up
        if file_path.exists():
            file_path.unlink()

    def test_e2e_file_uses_lf_line_endings(self):
        """Test that file uses Unix LF line endings, not CRLF or CR."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()

        binary_content = file_path.read_bytes()

        # Verify LF only (no CRLF or CR)
        assert b"\r\n" not in binary_content
        assert b"\r" not in binary_content

        # Clean up
        if file_path.exists():
            file_path.unlink()

    def test_e2e_file_size_within_bounds(self):
        """Test that file size is within 100-600 bytes as specified."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()

        file_size = file_path.stat().st_size
        assert MIN_FILE_SIZE <= file_size <= MAX_FILE_SIZE

        # Clean up
        if file_path.exists():
            file_path.unlink()

    def test_e2e_file_contains_two_to_three_sentences(self):
        """Test that prose contains exactly 2-3 sentences (2-3 periods)."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()

        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        prose = "\n".join(lines[2:])

        period_count = prose.count(".")
        assert 2 <= period_count <= 3

        # Clean up
        if file_path.exists():
            file_path.unlink()

    def test_e2e_all_validation_checks_pass(self):
        """Test that all validation checks pass on created file."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        create_markdown_file()

        # Run comprehensive validation
        result = validate_markdown_file(file_path)
        assert result is True

        # Clean up
        if file_path.exists():
            file_path.unlink()

    def test_e2e_commit_message_follows_conventional_format(self):
        """Test that git commit message follows conventional commits format."""
        from sheep.features.feature_206_markdown_file_creation import COMMIT_MESSAGE

        # Verify format: feat(206): description
        assert COMMIT_MESSAGE.startswith("feat(206):")
        assert FILENAME in COMMIT_MESSAGE

    def test_e2e_branch_name_is_correct(self):
        """Test that the feature branch name is correct."""
        expected_branch = "feat/206-markdown-file-creation-f7d8d3"
        assert expected_branch == BRANCH_NAME

    def test_e2e_feature_number_is_206(self):
        """Test that feature number is 206."""
        assert FEATURE_NUMBER == 206

    def test_e2e_main_success_path_with_mocked_git(self):
        """Test the complete success path with mocked git operations."""
        file_path = Path(FILENAME)
        if file_path.exists():
            file_path.unlink()

        # Run main with mocked git operations
        with patch(
            "sheep.features.feature_206_markdown_file_creation.git_add"
        ), patch(
            "sheep.features.feature_206_markdown_file_creation.git_commit"
        ), patch(
            "sheep.features.feature_206_markdown_file_creation.git_push"
        ):
            result = main()

        # Assert success
        assert result == 0

        # Assert file exists and is valid
        assert file_path.exists()
        assert validate_markdown_file(file_path) is True

        # Clean up
        if file_path.exists():
            file_path.unlink()
