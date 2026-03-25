"""Tests for feature 207: Create markdown file test-ylivjf.md with hard-coded content."""

from pathlib import Path
from unittest.mock import patch
import subprocess
import pytest

from sheep.features.feature_207_markdown_file_creation import (
    FILENAME,
    FEATURE_NUMBER,
    BRANCH_NAME,
    COMMIT_MESSAGE,
    TITLE_TEXT,
    PROSE_CONTENT,
    create_markdown_file,
    verify_file_exists,
    validate_markdown_format,
    validate_sentence_count,
    validate_encoding,
    validate_line_endings,
    validate_file_size,
    validate_markdown_file,
    extract_prose_content,
    count_sentences,
    git_add_file,
    git_commit,
    git_push,
    main,
)


class TestCreateMarkdownFile:
    """Tests for create_markdown_file() function."""

    def test_create_markdown_file_creates_file_on_disk(self, tmp_path):
        """Test that create_markdown_file() creates a file on disk."""
        # Change to temp directory
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            # File should not exist before creation
            test_file = Path(FILENAME)
            assert not test_file.exists()

            # Create file
            result = create_markdown_file()

            # File should exist after creation
            assert result.exists()
            assert test_file.exists()

        finally:
            import os
            os.chdir(original_cwd)

    def test_create_markdown_file_returns_path(self, tmp_path):
        """Test that create_markdown_file() returns a Path object."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            result = create_markdown_file()
            assert isinstance(result, Path)
            assert result.name == FILENAME

        finally:
            import os
            os.chdir(original_cwd)

    def test_create_markdown_file_content_format(self, tmp_path):
        """Test that created file has correct markdown structure."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_markdown_file()
            test_file = Path(FILENAME)

            # Read and verify content
            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            # First line should be H1 title
            assert lines[0] == f"# {TITLE_TEXT}"

            # Second line should be blank
            assert lines[1] == ""

            # Prose content should be in remaining lines
            prose_content = "\n".join(lines[2:]).strip()
            assert PROSE_CONTENT in prose_content

        finally:
            import os
            os.chdir(original_cwd)

    def test_create_markdown_file_utf8_encoding(self, tmp_path):
        """Test that created file is UTF-8 encoded."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_markdown_file()
            test_file = Path(FILENAME)

            # Should be readable as UTF-8
            content = test_file.read_text(encoding="utf-8")
            assert content is not None

            # Should not have BOM
            binary = test_file.read_bytes()
            assert not binary.startswith(b"\xef\xbb\xbf")

        finally:
            import os
            os.chdir(original_cwd)

    def test_create_markdown_file_size(self, tmp_path):
        """Test that created file is within acceptable size range."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_markdown_file()
            test_file = Path(FILENAME)

            file_size = test_file.stat().st_size
            # Should be between 200-700 bytes
            assert 200 <= file_size <= 700

        finally:
            import os
            os.chdir(original_cwd)


class TestVerifyFileExists:
    """Tests for verify_file_exists() function."""

    def test_verify_file_exists_passes(self, tmp_path):
        """Test verify_file_exists() when file exists."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nContent.")

        # Should not raise
        verify_file_exists(str(test_file))

    def test_verify_file_exists_fails_missing_file(self, tmp_path):
        """Test verify_file_exists() raises FileNotFoundError when file missing."""
        test_file = tmp_path / FILENAME

        with pytest.raises(FileNotFoundError):
            verify_file_exists(str(test_file))


class TestValidateMarkdownFormat:
    """Tests for validate_markdown_format() function."""

    def test_validate_markdown_format_passes_valid_file(self, tmp_path):
        """Test validate_markdown_format() with valid markdown structure."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test Title\n\nFirst sentence. Second sentence.")

        # Should not raise
        validate_markdown_format(str(test_file))

    def test_validate_markdown_format_fails_missing_h1(self, tmp_path):
        """Test validate_markdown_format() fails without H1 heading."""
        test_file = tmp_path / FILENAME
        test_file.write_text("No heading here\n\nFirst sentence. Second sentence.")

        with pytest.raises(ValueError, match="H1"):
            validate_markdown_format(str(test_file))

    def test_validate_markdown_format_fails_missing_blank_line(self, tmp_path):
        """Test validate_markdown_format() fails without blank line separator."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test Title\nFirst sentence. Second sentence.")

        with pytest.raises(ValueError, match="blank"):
            validate_markdown_format(str(test_file))

    def test_validate_markdown_format_fails_multiple_h1(self, tmp_path):
        """Test validate_markdown_format() fails with multiple H1 headings."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test Title\n\n# Another H1\n\nFirst sentence. Second sentence.")

        with pytest.raises(ValueError, match="exactly one"):
            validate_markdown_format(str(test_file))


class TestValidateSentenceCount:
    """Tests for validate_sentence_count() function."""

    def test_validate_sentence_count_passes_two_sentences(self, tmp_path):
        """Test validate_sentence_count() with exactly 2 sentences."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nFirst sentence. Second sentence.")

        # Should not raise
        validate_sentence_count(str(test_file))

    def test_validate_sentence_count_passes_three_sentences(self, tmp_path):
        """Test validate_sentence_count() with exactly 3 sentences."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nFirst sentence. Second sentence. Third sentence.")

        # Should not raise
        validate_sentence_count(str(test_file))

    def test_validate_sentence_count_fails_one_sentence(self, tmp_path):
        """Test validate_sentence_count() fails with 1 sentence."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nOnly one sentence.")

        with pytest.raises(ValueError, match="2-3"):
            validate_sentence_count(str(test_file))

    def test_validate_sentence_count_fails_four_sentences(self, tmp_path):
        """Test validate_sentence_count() fails with 4 sentences."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nFirst. Second. Third. Fourth.")

        with pytest.raises(ValueError, match="2-3"):
            validate_sentence_count(str(test_file))


class TestValidateEncoding:
    """Tests for validate_encoding() function."""

    def test_validate_encoding_passes_utf8(self, tmp_path):
        """Test validate_encoding() with valid UTF-8."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nFirst sentence. Second sentence.", encoding="utf-8")

        # Should not raise
        validate_encoding(str(test_file))

    def test_validate_encoding_fails_utf8_bom(self, tmp_path):
        """Test validate_encoding() fails with UTF-8 BOM."""
        test_file = tmp_path / FILENAME
        # Write with BOM
        test_file.write_bytes(b"\xef\xbb\xbf# Test\n\nFirst sentence. Second sentence.")

        with pytest.raises(ValueError, match="BOM"):
            validate_encoding(str(test_file))


class TestValidateLineEndings:
    """Tests for validate_line_endings() function."""

    def test_validate_line_endings_passes_lf(self, tmp_path):
        """Test validate_line_endings() with LF endings."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nFirst sentence. Second sentence.", encoding="utf-8")

        # Should not raise
        validate_line_endings(str(test_file))

    def test_validate_line_endings_fails_crlf(self, tmp_path):
        """Test validate_line_endings() fails with CRLF."""
        test_file = tmp_path / FILENAME
        test_file.write_bytes(b"# Test\r\n\r\nFirst sentence. Second sentence.")

        with pytest.raises(ValueError, match="CRLF"):
            validate_line_endings(str(test_file))

    def test_validate_line_endings_fails_cr(self, tmp_path):
        """Test validate_line_endings() fails with CR."""
        test_file = tmp_path / FILENAME
        test_file.write_bytes(b"# Test\r\rFirst sentence. Second sentence.")

        with pytest.raises(ValueError, match="CR"):
            validate_line_endings(str(test_file))


class TestValidateFileSize:
    """Tests for validate_file_size() function."""

    def test_validate_file_size_passes_valid_size(self, tmp_path):
        """Test validate_file_size() with valid file size."""
        test_file = tmp_path / FILENAME
        content = "# Test\n\n" + "X" * 300  # Create file > 200 bytes
        test_file.write_text(content)

        # Should not raise
        validate_file_size(str(test_file))

    def test_validate_file_size_fails_too_small(self, tmp_path):
        """Test validate_file_size() fails with file too small."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nSmall.")

        with pytest.raises(ValueError, match="outside acceptable"):
            validate_file_size(str(test_file))

    def test_validate_file_size_fails_too_large(self, tmp_path):
        """Test validate_file_size() fails with file too large."""
        test_file = tmp_path / FILENAME
        content = "# Test\n\n" + "X" * 700
        test_file.write_text(content)

        with pytest.raises(ValueError, match="outside acceptable"):
            validate_file_size(str(test_file))


class TestValidateMarkdownFileOrchestration:
    """Tests for validate_markdown_file() orchestration function."""

    def test_validate_markdown_file_passes_valid_file(self, tmp_path):
        """Test validate_markdown_file() with completely valid file."""
        test_file = tmp_path / FILENAME
        # Create a valid file
        content = "# Test\n\n" + "X" * 100 + ". " + "Y" * 100 + ". " + "Z" * 50 + "."
        test_file.write_text(content, encoding="utf-8")

        # Should not raise
        validate_markdown_file(str(test_file))

    def test_validate_markdown_file_fails_on_missing_file(self, tmp_path):
        """Test validate_markdown_file() fails if file doesn't exist."""
        test_file = tmp_path / FILENAME

        with pytest.raises(FileNotFoundError):
            validate_markdown_file(str(test_file))

    def test_validate_markdown_file_fails_format_error(self, tmp_path):
        """Test validate_markdown_file() fails on format error."""
        test_file = tmp_path / FILENAME
        test_file.write_text("No heading\n\nFirst. Second.")

        with pytest.raises(ValueError):
            validate_markdown_file(str(test_file))

    def test_validate_markdown_file_fails_encoding_error(self, tmp_path):
        """Test validate_markdown_file() fails on encoding error."""
        test_file = tmp_path / FILENAME
        # Create with BOM (invalid)
        test_file.write_bytes(b"\xef\xbb\xbf# Test\n\n" + b"X" * 200 + b". " + b"Y" * 100 + b".")

        with pytest.raises(ValueError):
            validate_markdown_file(str(test_file))


class TestExtractProseContent:
    """Tests for extract_prose_content() helper function."""

    def test_extract_prose_content_valid(self, tmp_path):
        """Test extracting prose from valid markdown."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Title\n\nProse content here.")

        prose = extract_prose_content(str(test_file))
        assert prose == "Prose content here."

    def test_extract_prose_content_multiline(self, tmp_path):
        """Test extracting multiline prose."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Title\n\nFirst line.\nSecond line.")

        prose = extract_prose_content(str(test_file))
        assert "First line." in prose
        assert "Second line." in prose


class TestCountSentences:
    """Tests for count_sentences() helper function."""

    def test_count_sentences_two(self):
        """Test counting 2 sentences."""
        prose = "First sentence. Second sentence."
        count = count_sentences(prose)
        assert count == 2

    def test_count_sentences_three(self):
        """Test counting 3 sentences."""
        prose = "First sentence. Second sentence. Third sentence."
        count = count_sentences(prose)
        assert count == 3

    def test_count_sentences_empty_raises(self):
        """Test that empty prose raises ValueError."""
        with pytest.raises(ValueError):
            count_sentences("")


class TestGitOperations:
    """Tests for git operations (mocked to avoid real git calls)."""

    @patch("sheep.features.feature_207_markdown_file_creation.subprocess.run")
    def test_git_add_file_calls_subprocess(self, mock_run):
        """Test git_add_file calls subprocess.run with correct arguments."""
        git_add_file()

        mock_run.assert_called_once_with(
            ["git", "add", FILENAME],
            check=True,
            capture_output=True,
            text=True,
        )

    @patch("sheep.features.feature_207_markdown_file_creation.subprocess.run")
    def test_git_add_file_custom_filename(self, mock_run):
        """Test git_add_file with custom filename."""
        custom_file = "custom.md"
        git_add_file(custom_file)

        call_args = mock_run.call_args[0][0]
        assert call_args[-1] == custom_file

    @patch("sheep.features.feature_207_markdown_file_creation.subprocess.run")
    def test_git_add_file_raises_on_error(self, mock_run):
        """Test git_add_file raises CalledProcessError on failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git add", stderr="error")

        with pytest.raises(subprocess.CalledProcessError):
            git_add_file()

    @patch("sheep.features.feature_207_markdown_file_creation.subprocess.run")
    def test_git_commit_calls_subprocess(self, mock_run):
        """Test git_commit calls subprocess.run with correct arguments."""
        git_commit()

        call_args = mock_run.call_args[0][0]
        assert call_args[0] == "git"
        assert call_args[1] == "commit"
        assert "-m" in call_args
        assert COMMIT_MESSAGE in call_args

    @patch("sheep.features.feature_207_markdown_file_creation.subprocess.run")
    def test_git_commit_custom_message(self, mock_run):
        """Test git_commit with custom message."""
        custom_msg = "feat(999): Custom message"
        git_commit(custom_msg)

        call_args = mock_run.call_args[0][0]
        assert custom_msg in call_args

    @patch("sheep.features.feature_207_markdown_file_creation.subprocess.run")
    def test_git_commit_raises_on_error(self, mock_run):
        """Test git_commit raises CalledProcessError on failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git commit", stderr="error")

        with pytest.raises(subprocess.CalledProcessError):
            git_commit()

    @patch("sheep.features.feature_207_markdown_file_creation.subprocess.run")
    def test_git_push_calls_subprocess(self, mock_run):
        """Test git_push calls subprocess.run with correct arguments."""
        git_push()

        call_args = mock_run.call_args[0][0]
        assert call_args[0] == "git"
        assert call_args[1] == "push"
        assert "-u" in call_args
        assert "origin" in call_args
        assert BRANCH_NAME in call_args

    @patch("sheep.features.feature_207_markdown_file_creation.subprocess.run")
    def test_git_push_custom_branch(self, mock_run):
        """Test git_push with custom branch name."""
        custom_branch = "feat/custom-branch"
        git_push(custom_branch)

        call_args = mock_run.call_args[0][0]
        assert custom_branch in call_args

    @patch("sheep.features.feature_207_markdown_file_creation.subprocess.run")
    def test_git_push_raises_on_error(self, mock_run):
        """Test git_push raises CalledProcessError on failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git push", stderr="error")

        with pytest.raises(subprocess.CalledProcessError):
            git_push()


class TestMainOrchestration:
    """Tests for main() orchestration function."""

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_207_markdown_file_creation.create_markdown_file")
    def test_main_success_returns_zero(
        self, mock_create, mock_validate, mock_add, mock_commit, mock_push
    ):
        """Test main() returns 0 on success."""
        exit_code = main()

        assert exit_code == 0
        # Verify all functions were called
        mock_create.assert_called_once()
        mock_validate.assert_called_once()
        mock_add.assert_called_once()
        mock_commit.assert_called_once()
        mock_push.assert_called_once()

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_207_markdown_file_creation.create_markdown_file")
    def test_main_returns_int(
        self, mock_create, mock_validate, mock_add, mock_commit, mock_push
    ):
        """Test main() returns an integer."""
        result = main()

        assert isinstance(result, int)
        assert result in (0, 1)

    @patch("sheep.features.feature_207_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_207_markdown_file_creation.create_markdown_file")
    def test_main_returns_one_on_validation_error(self, mock_create, mock_validate):
        """Test main() returns 1 if validation fails."""
        mock_validate.side_effect = ValueError("Invalid markdown")

        exit_code = main()

        assert exit_code == 1

    @patch("sheep.features.feature_207_markdown_file_creation.create_markdown_file")
    def test_main_returns_one_on_creation_error(self, mock_create):
        """Test main() returns 1 if file creation fails."""
        mock_create.side_effect = OSError("Cannot create file")

        exit_code = main()

        assert exit_code == 1

    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_207_markdown_file_creation.create_markdown_file")
    def test_main_returns_one_on_git_error(self, mock_create, mock_validate, mock_add):
        """Test main() returns 1 if git operations fail."""
        mock_add.side_effect = subprocess.CalledProcessError(1, "git add", stderr="error")

        exit_code = main()

        assert exit_code == 1

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_207_markdown_file_creation.create_markdown_file")
    def test_main_returns_one_on_unexpected_error(
        self, mock_create, mock_validate, mock_add, mock_commit, mock_push
    ):
        """Test main() returns 1 on unexpected exception."""
        mock_create.side_effect = RuntimeError("Unexpected error")

        exit_code = main()

        assert exit_code == 1


class TestIntegrationWorkflow:
    """Integration tests for complete workflow."""

    def test_complete_workflow_creates_valid_file(self, tmp_path):
        """Test complete workflow creates a valid markdown file."""
        import os

        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Run file creation and validation
            create_markdown_file()
            validate_markdown_file()

            # File should exist and be valid
            assert Path(FILENAME).exists()
            content = Path(FILENAME).read_text(encoding="utf-8")
            assert content.startswith("# " + TITLE_TEXT)
            assert PROSE_CONTENT in content

        finally:
            os.chdir(original_cwd)

    def test_complete_workflow_validates_all_criteria(self, tmp_path):
        """Test complete workflow validates all success criteria."""
        import os

        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create and validate file
            create_markdown_file()
            validate_markdown_file()

            # All validation should pass
            verify_file_exists()
            validate_markdown_format()
            validate_sentence_count()
            validate_encoding()
            validate_line_endings()
            validate_file_size()

        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    def test_complete_workflow_with_mocked_git(self, mock_add, mock_commit, mock_push, tmp_path):
        """Test complete workflow including git operations."""
        import os

        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Run main workflow
            exit_code = main()

            # Should succeed
            assert exit_code == 0
            # File should exist
            assert Path(FILENAME).exists()
            # Git operations should have been called
            mock_add.assert_called_once()
            mock_commit.assert_called_once()
            mock_push.assert_called_once()

        finally:
            os.chdir(original_cwd)


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_file_with_mixed_line_endings_detected(self, tmp_path):
        """Test that files with mixed line endings are detected."""
        test_file = tmp_path / FILENAME
        # Mixed endings
        test_file.write_bytes(b"# Title\n\nFirst sentence. Second sentence.\r\n")

        with pytest.raises(ValueError, match="CRLF"):
            validate_line_endings(str(test_file))

    def test_file_exactly_200_bytes_valid(self, tmp_path):
        """Test that file exactly 200 bytes is valid."""
        test_file = tmp_path / FILENAME
        # Create file that's exactly 200 bytes
        content = "# Title\n\n" + "A" * 190 + "."
        test_file.write_text(content)

        # Verify it's actually 200 bytes
        actual_bytes = len(test_file.read_bytes())
        assert actual_bytes == 200, f"Expected 200 bytes but got {actual_bytes}"

        # Should pass (200 is the minimum)
        validate_file_size(str(test_file))

    def test_file_exactly_700_bytes_valid(self, tmp_path):
        """Test that file exactly 700 bytes is valid."""
        test_file = tmp_path / FILENAME
        # Create file that's exactly 700 bytes
        content = "# Title\n\n" + "A" * 680 + "."
        # Adjust to exactly 700
        content = content[:700]
        test_file.write_text(content)

        # Should pass (700 is the maximum)
        validate_file_size(str(test_file))
