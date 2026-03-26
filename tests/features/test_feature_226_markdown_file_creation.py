"""Tests for feature 226: Create markdown file test-zicq4v.md.

Tests cover:
- File creation with correct format, encoding, and line endings
- Validation functions for markdown format, sentence count, encoding, line endings, and file size
- Git operations (add, commit, push) with proper subprocess mocking
- Complete workflow orchestration (main function)
- Error handling and edge cases
"""

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.features.feature_226_markdown_file_creation import (
    BRANCH_NAME,
    COMMIT_MESSAGE,
    FILENAME,
    PROSE_CONTENT,
    TITLE_TEXT,
    count_sentences,
    create_markdown_file,
    extract_prose_content,
    git_add_file,
    git_commit,
    git_push,
    validate_encoding,
    validate_file_exists,
    validate_file_size,
    validate_line_endings,
    validate_markdown_file,
    validate_markdown_format,
    validate_sentence_count,
    verify_file_exists,
)


class TestFileCreation:
    """Tests for file creation functionality."""

    def test_create_markdown_file_creates_file(self, tmp_path):
        """Test that create_markdown_file creates a file at the correct path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                file_path = create_markdown_file()
                assert file_path.exists()
                assert file_path.name == FILENAME
            finally:
                import os

                os.chdir(original_cwd)

    def test_create_markdown_file_contains_title(self):
        """Test that created file contains the H1 title."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                content = Path(FILENAME).read_text()
                assert f"# {TITLE_TEXT}" in content
            finally:
                import os

                os.chdir(original_cwd)

    def test_create_markdown_file_contains_prose(self):
        """Test that created file contains the prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                content = Path(FILENAME).read_text()
                assert PROSE_CONTENT in content
            finally:
                import os

                os.chdir(original_cwd)

    def test_create_markdown_file_utf8_encoding(self):
        """Test that file is created with UTF-8 encoding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Read as bytes and verify no UTF-8 BOM
                binary_content = Path(FILENAME).read_bytes()
                assert not binary_content.startswith(b"\xef\xbb\xbf")
                # Verify valid UTF-8
                binary_content.decode("utf-8")
            finally:
                import os

                os.chdir(original_cwd)

    def test_create_markdown_file_lf_line_endings(self):
        """Test that file uses Unix LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                binary_content = Path(FILENAME).read_bytes()
                # Check no CRLF or CR
                assert b"\r\n" not in binary_content
                assert b"\r" not in binary_content
            finally:
                import os

                os.chdir(original_cwd)


class TestValidationHelpers:
    """Tests for validation helper functions."""

    def test_verify_file_exists_with_existing_file(self):
        """Test validate_file_exists with an existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should not raise
                validate_file_exists()
            finally:
                import os

                os.chdir(original_cwd)

    def test_verify_file_exists_with_missing_file(self):
        """Test validate_file_exists raises FileNotFoundError for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with pytest.raises(FileNotFoundError):
                    validate_file_exists()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_file_exists_returns_true_when_file_exists(self):
        """Test validate_file_exists returns True when file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should return True
                result = validate_file_exists()
                assert result is True
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_file_exists_raises_when_file_missing(self):
        """Test validate_file_exists raises FileNotFoundError when file missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with pytest.raises(FileNotFoundError) as exc_info:
                    validate_file_exists()
                # Check error message includes filename and directory info
                error_msg = str(exc_info.value)
                assert FILENAME in error_msg
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_format_valid(self):
        """Test validate_markdown_format with valid format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should not raise
                validate_markdown_format()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_format_missing_h1(self):
        """Test validate_markdown_format raises on missing H1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_text("No heading\n\nProse content here.")
                with pytest.raises(ValueError, match="must start with H1"):
                    validate_markdown_format()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_format_missing_blank_line(self):
        """Test validate_markdown_format raises on missing blank line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Title\nDirect prose without blank line")
                with pytest.raises(ValueError, match="Second line must be blank"):
                    validate_markdown_format()
            finally:
                import os

                os.chdir(original_cwd)

    def test_extract_prose_content_valid(self):
        """Test extract_prose_content returns prose correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                prose = extract_prose_content()
                assert PROSE_CONTENT in prose
            finally:
                import os

                os.chdir(original_cwd)

    def test_count_sentences_valid(self):
        """Test count_sentences counts periods correctly."""
        text = "First sentence. Second sentence. Third sentence."
        assert count_sentences(text) == 3

    def test_count_sentences_two_sentences(self):
        """Test count_sentences with two sentences."""
        text = "First sentence. Second sentence."
        assert count_sentences(text) == 2

    def test_validate_sentence_count_valid(self):
        """Test validate_sentence_count with valid count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should not raise (PROSE_CONTENT has exactly 3 sentences)
                validate_sentence_count()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_sentence_count_too_few(self):
        """Test validate_sentence_count raises on too few sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Title\n\nOne sentence.")
                with pytest.raises(ValueError, match="exactly 2 or 3"):
                    validate_sentence_count()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_sentence_count_too_many(self):
        """Test validate_sentence_count raises on too many sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_text(
                    "# Title\n\nOne. Two. Three. Four."
                )
                with pytest.raises(ValueError, match="exactly 2 or 3"):
                    validate_sentence_count()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_encoding_valid_utf8(self):
        """Test validate_encoding with valid UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should not raise
                validate_encoding()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_encoding_detects_bom(self):
        """Test validate_encoding detects UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Write file with UTF-8 BOM
                Path(FILENAME).write_bytes(b"\xef\xbb\xbf# Title\n\nContent.")
                with pytest.raises(ValueError, match="BOM"):
                    validate_encoding()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_line_endings_valid_lf(self):
        """Test validate_line_endings with valid LF endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should not raise
                validate_line_endings()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_line_endings_detects_crlf(self):
        """Test validate_line_endings detects CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_bytes(b"# Title\r\n\r\nContent.")
                with pytest.raises(ValueError, match="CRLF"):
                    validate_line_endings()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_line_endings_detects_cr(self):
        """Test validate_line_endings detects CR."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_bytes(b"# Title\r\rContent.")
                with pytest.raises(ValueError, match="CR"):
                    validate_line_endings()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_file_size_typical_logs_info(self):
        """Test validate_file_size logs info for typical file size."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should log info and not raise (file is in 300-800 bytes range)
                with patch(
                    "sheep.features.feature_226_markdown_file_creation._logger"
                ) as mock_logger:
                    validate_file_size()
                    # Verify info log was called
                    mock_logger.info.assert_called()
                    # Verify the call mentions file size
                    call_args = str(mock_logger.info.call_args_list)
                    assert "bytes" in call_args
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_file_size_undersized_logs_warning(self):
        """Test validate_file_size logs warning for undersized file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_text("x")
                # Should log warning and not raise
                with patch(
                    "sheep.features.feature_226_markdown_file_creation._logger"
                ) as mock_logger:
                    validate_file_size()
                    # Verify warning log was called
                    mock_logger.warning.assert_called()
                    # Verify the warning mentions "smaller than typical range"
                    call_args = str(mock_logger.warning.call_args_list)
                    assert "smaller than typical range" in call_args
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_file_size_oversized_logs_warning(self):
        """Test validate_file_size logs warning for oversized file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_text("x" * 1000)
                # Should log warning and not raise
                with patch(
                    "sheep.features.feature_226_markdown_file_creation._logger"
                ) as mock_logger:
                    validate_file_size()
                    # Verify warning log was called
                    mock_logger.warning.assert_called()
                    # Verify the warning mentions "larger than typical range"
                    call_args = str(mock_logger.warning.call_args_list)
                    assert "larger than typical range" in call_args
            finally:
                import os

                os.chdir(original_cwd)


class TestComprehensiveValidation:
    """Tests for comprehensive validation pipeline."""

    def test_validate_markdown_file_all_checks_pass(self):
        """Test validate_markdown_file passes with valid file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should not raise
                validate_markdown_file()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_file_fails_on_missing_file(self):
        """Test validate_markdown_file fails when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with pytest.raises(FileNotFoundError):
                    validate_markdown_file()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_file_fails_on_bad_format(self):
        """Test validate_markdown_file fails on bad markdown format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_text("No heading\n\nContent.")
                with pytest.raises(ValueError):
                    validate_markdown_file()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_file_fails_on_bad_encoding(self):
        """Test validate_markdown_file fails on bad encoding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Write with BOM
                Path(FILENAME).write_bytes(
                    b"\xef\xbb\xbf# Title\n\n" + PROSE_CONTENT.encode("utf-8")
                )
                with pytest.raises(ValueError):
                    validate_markdown_file()
            finally:
                import os

                os.chdir(original_cwd)


class TestGitOperations:
    """Tests for git operations (add, commit, push)."""

    def test_git_add_file_calls_git_correctly(self):
        """Test git_add_file calls subprocess.run with correct arguments."""
        with patch("subprocess.run") as mock_run:
            git_add_file()
            mock_run.assert_called_once_with(
                ["git", "add", FILENAME],
                check=True,
                capture_output=True,
                text=True,
            )

    def test_git_add_file_custom_filename(self):
        """Test git_add_file uses custom filename parameter."""
        with patch("subprocess.run") as mock_run:
            git_add_file("custom.md")
            mock_run.assert_called_once_with(
                ["git", "add", "custom.md"],
                check=True,
                capture_output=True,
                text=True,
            )

    def test_git_add_file_raises_on_failure(self):
        """Test git_add_file raises CalledProcessError on git failure."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git add", stderr="fatal error"
            )
            with pytest.raises(subprocess.CalledProcessError):
                git_add_file()

    def test_git_commit_calls_git_correctly(self):
        """Test git_commit calls subprocess.run with correct arguments."""
        with patch("subprocess.run") as mock_run:
            git_commit()
            mock_run.assert_called_once_with(
                ["git", "commit", "-m", COMMIT_MESSAGE],
                check=True,
                capture_output=True,
                text=True,
            )

    def test_git_commit_custom_message(self):
        """Test git_commit uses custom message parameter."""
        with patch("subprocess.run") as mock_run:
            git_commit("custom message")
            mock_run.assert_called_once_with(
                ["git", "commit", "-m", "custom message"],
                check=True,
                capture_output=True,
                text=True,
            )

    def test_git_commit_raises_on_failure(self):
        """Test git_commit raises CalledProcessError on git failure."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git commit", stderr="fatal error"
            )
            with pytest.raises(subprocess.CalledProcessError):
                git_commit()

    def test_git_push_calls_git_correctly(self):
        """Test git_push calls subprocess.run with correct arguments."""
        with patch("subprocess.run") as mock_run:
            git_push()
            mock_run.assert_called_once_with(
                ["git", "push", "-u", "origin", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            )

    def test_git_push_custom_branch(self):
        """Test git_push accepts custom branch parameter but always uses HEAD."""
        with patch("subprocess.run") as mock_run:
            git_push("custom-branch")
            # git_push always uses "HEAD" in git command regardless of branch_name param
            mock_run.assert_called_once_with(
                ["git", "push", "-u", "origin", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            )

    def test_git_push_raises_on_failure(self):
        """Test git_push raises CalledProcessError on git failure."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git push", stderr="fatal error"
            )
            with pytest.raises(subprocess.CalledProcessError):
                git_push()

    def test_git_commands_use_shell_false(self):
        """Test all git commands use shell=False (no shell=True)."""
        with patch("subprocess.run") as mock_run:
            git_add_file()
            # Verify shell parameter is not set or is False
            call_kwargs = mock_run.call_args[1]
            assert "shell" not in call_kwargs or call_kwargs.get("shell") is False

            mock_run.reset_mock()
            git_commit()
            call_kwargs = mock_run.call_args[1]
            assert "shell" not in call_kwargs or call_kwargs.get("shell") is False

            mock_run.reset_mock()
            git_push()
            call_kwargs = mock_run.call_args[1]
            assert "shell" not in call_kwargs or call_kwargs.get("shell") is False


class TestOrchestration:
    """Tests for main orchestration function."""

    def test_main_successful_workflow(self):
        """Test main() completes successfully with all operations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with patch("subprocess.run"):
                    # Import main after patching to ensure subprocess is mocked
                    from sheep.features.feature_226_markdown_file_creation import (
                        main,
                    )

                    exit_code = main()
                    # If we get here without exception, test passes
                    assert Path(FILENAME).exists()
                    assert exit_code == 0
            finally:
                import os

                os.chdir(original_cwd)

    def test_main_returns_0_on_success(self):
        """Test main() returns 0 on successful workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with patch("subprocess.run"):
                    from sheep.features.feature_226_markdown_file_creation import (
                        main,
                    )

                    exit_code = main()
                    assert exit_code == 0
            finally:
                import os

                os.chdir(original_cwd)

    def test_main_returns_1_on_file_creation_failure(self):
        """Test main() returns 1 on file creation failure."""
        with patch(
            "sheep.features.feature_226_markdown_file_creation.create_markdown_file"
        ) as mock_create:
            mock_create.side_effect = OSError("Failed to create file")
            from sheep.features.feature_226_markdown_file_creation import (
                main,
            )

            exit_code = main()
            assert exit_code == 1

    def test_main_returns_1_on_validation_failure(self):
        """Test main() returns 1 on validation failure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with patch(
                    "sheep.features.feature_226_markdown_file_creation.validate_markdown_file"
                ) as mock_validate:
                    mock_validate.side_effect = ValueError("Validation failed")
                    from sheep.features.feature_226_markdown_file_creation import (
                        main,
                    )

                    exit_code = main()
                    assert exit_code == 1
            finally:
                import os

                os.chdir(original_cwd)

    def test_main_returns_1_on_git_failure(self):
        """Test main() returns 1 on git failure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with patch("subprocess.run") as mock_run:
                    mock_run.side_effect = subprocess.CalledProcessError(
                        1, "git", stderr="failed"
                    )
                    from sheep.features.feature_226_markdown_file_creation import (
                        main,
                    )

                    exit_code = main()
                    assert exit_code == 1
            finally:
                import os

                os.chdir(original_cwd)
