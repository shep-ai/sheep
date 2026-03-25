"""Tests for feature 207: Create markdown file test-5q8o2a.md with Claude API generation.

Tests cover:
- Content generation with Claude API and temperature=0
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

from sheep.features.feature_207_markdown_file_creation import (
    BRANCH_NAME,
    COMMIT_MESSAGE,
    FILENAME,
    count_sentences,
    create_markdown_file,
    extract_prose_content,
    generate_prose,
    generate_title,
    git_add_file,
    git_commit,
    git_push,
    validate_encoding,
    validate_file_size,
    validate_line_endings,
    validate_markdown_file,
    validate_markdown_format,
    validate_sentence_count,
    verify_file_exists,
)


class TestContentGeneration:
    """Tests for content generation with Claude API."""

    @patch("sheep.features.feature_207_markdown_file_creation.create_llm")
    def test_generate_title_returns_string(self, mock_create_llm):
        """Test that generate_title returns a title string."""
        mock_llm = MagicMock()
        mock_create_llm.return_value = mock_llm
        mock_llm.call.return_value = "# Test Title\n\nSentence one. Sentence two. Sentence three."

        title = generate_title()
        assert isinstance(title, str)
        assert len(title) > 0
        assert not title.startswith("#")

    @patch("sheep.features.feature_207_markdown_file_creation.create_llm")
    def test_generate_title_uses_temperature_zero(self, mock_create_llm):
        """Test that generate_title creates LLM with temperature=0."""
        mock_llm = MagicMock()
        mock_create_llm.return_value = mock_llm
        mock_llm.call.return_value = "# Title\n\nOne. Two. Three."

        generate_title()
        mock_create_llm.assert_called_once_with(temperature=0)

    @patch("sheep.features.feature_207_markdown_file_creation.create_llm")
    def test_generate_prose_returns_string(self, mock_create_llm):
        """Test that generate_prose returns prose string with 2-3 sentences."""
        mock_llm = MagicMock()
        mock_create_llm.return_value = mock_llm
        mock_llm.call.return_value = "# Title\n\nFirst sentence. Second sentence. Third sentence."

        prose = generate_prose()
        assert isinstance(prose, str)
        assert len(prose) > 0
        # Should contain 2-3 periods
        assert 2 <= prose.count(".") <= 3

    @patch("sheep.features.feature_207_markdown_file_creation.create_llm")
    def test_generate_prose_uses_temperature_zero(self, mock_create_llm):
        """Test that generate_prose creates LLM with temperature=0."""
        mock_llm = MagicMock()
        mock_create_llm.return_value = mock_llm
        mock_llm.call.return_value = "# Title\n\nOne. Two. Three."

        generate_prose()
        mock_create_llm.assert_called_once_with(temperature=0)

    @patch("sheep.features.feature_207_markdown_file_creation.create_llm")
    def test_generate_prose_validates_sentence_count(self, mock_create_llm):
        """Test that generate_prose raises on invalid sentence count."""
        mock_llm = MagicMock()
        mock_create_llm.return_value = mock_llm
        # Only one sentence
        mock_llm.call.return_value = "# Title\n\nOnly one sentence."

        with pytest.raises(ValueError, match="sentences"):
            generate_prose()


class TestFileCreation:
    """Tests for file creation functionality."""

    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title")
    def test_create_markdown_file_creates_file(self, mock_title, mock_prose):
        """Test that create_markdown_file creates a file at the correct path."""
        mock_title.return_value = "Test Title"
        mock_prose.return_value = "First sentence. Second sentence. Third sentence."

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                file_path = create_markdown_file()
                assert Path(FILENAME).exists()
            finally:
                import os

                os.chdir(original_cwd)

    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title")
    def test_create_markdown_file_contains_generated_title(self, mock_title, mock_prose):
        """Test that created file contains the generated H1 title."""
        title_text = "Generated Test Title"
        prose_text = "Sentence one. Sentence two. Sentence three."
        mock_title.return_value = title_text
        mock_prose.return_value = prose_text

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                content = Path(FILENAME).read_text()
                assert f"# {title_text}" in content
            finally:
                import os

                os.chdir(original_cwd)

    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title")
    def test_create_markdown_file_contains_generated_prose(self, mock_title, mock_prose):
        """Test that created file contains the generated prose content."""
        prose_text = "Prose one. Prose two. Prose three."
        mock_title.return_value = "Title"
        mock_prose.return_value = prose_text

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                content = Path(FILENAME).read_text()
                assert prose_text in content
            finally:
                import os

                os.chdir(original_cwd)

    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title")
    def test_create_markdown_file_utf8_encoding(self, mock_title, mock_prose):
        """Test that file is created with UTF-8 encoding without BOM."""
        mock_title.return_value = "Title"
        mock_prose.return_value = "One. Two. Three."

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

    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title")
    def test_create_markdown_file_lf_line_endings(self, mock_title, mock_prose):
        """Test that file uses Unix LF line endings."""
        mock_title.return_value = "Title"
        mock_prose.return_value = "First. Second. Third."

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
        """Test verify_file_exists with an existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Title\n\nOne. Two. Three.")
                # Should not raise
                verify_file_exists()
            finally:
                import os

                os.chdir(original_cwd)

    def test_verify_file_exists_with_missing_file(self):
        """Test verify_file_exists raises FileNotFoundError for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                with pytest.raises(FileNotFoundError):
                    verify_file_exists()
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
                Path(FILENAME).write_text("# Title\n\nProse content here.")
                # Should not raise
                validate_markdown_format()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_format_missing_h1(self):
        """Test validate_markdown_format raises on missing H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_text("## Heading 2\n\nContent.")
                with pytest.raises(ValueError, match="H1"):
                    validate_markdown_format()
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_format_missing_blank_line(self):
        """Test validate_markdown_format raises on missing blank line separator."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Title\nContent without blank line.")
                with pytest.raises(ValueError, match="blank"):
                    validate_markdown_format()
            finally:
                import os

                os.chdir(original_cwd)

    def test_extract_prose_content_valid(self):
        """Test extract_prose_content extracts text after blank line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                prose_text = "First sentence. Second sentence. Third."
                Path(FILENAME).write_text(f"# Title\n\n{prose_text}")
                result = extract_prose_content()
                assert prose_text == result
            finally:
                import os

                os.chdir(original_cwd)

    def test_count_sentences_valid(self):
        """Test count_sentences counts periods correctly."""
        prose = "One sentence. Two sentence. Three sentence."
        count = count_sentences(prose)
        assert count == 3

    def test_count_sentences_empty_raises(self):
        """Test count_sentences raises on empty prose."""
        with pytest.raises(ValueError, match="empty"):
            count_sentences("")

    def test_validate_sentence_count_valid(self):
        """Test validate_sentence_count with valid 2-3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_text("# Title\n\nFirst. Second. Third.")
                # Should not raise
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
                with pytest.raises(ValueError, match="Expected 2-3 sentences"):
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
                Path(FILENAME).write_text("# Title\n\nOne. Two. Three. Four.")
                with pytest.raises(ValueError, match="Expected 2-3 sentences"):
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
                Path(FILENAME).write_text("# Title\n\nContent.")
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
                Path(FILENAME).write_text("# Title\n\nContent.")
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

    def test_validate_file_size_valid(self):
        """Test validate_file_size with valid size (soft validation - logs warning but returns True)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                # Create file with content in expected range
                Path(FILENAME).write_text("# Title\n\nFirst sentence. Second sentence. Third sentence.")
                # Should not raise (soft validation)
                result = validate_file_size()
                assert result is True
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_file_size_soft_validation_warns_small(self):
        """Test validate_file_size logs warning for too small file but returns True."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_text("x")
                # Should not raise (soft validation), but logs warning
                result = validate_file_size()
                assert result is True
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_file_size_soft_validation_warns_large(self):
        """Test validate_file_size logs warning for too large file but returns True."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                Path(FILENAME).write_text("x" * 1000)
                # Should not raise (soft validation), but logs warning
                result = validate_file_size()
                assert result is True
            finally:
                import os

                os.chdir(original_cwd)


class TestComprehensiveValidation:
    """Tests for comprehensive validation pipeline."""

    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title")
    def test_validate_markdown_file_all_checks_pass(self, mock_title, mock_prose):
        """Test validate_markdown_file with valid file."""
        mock_title.return_value = "Valid Title"
        mock_prose.return_value = "First sentence. Second sentence. Third sentence."

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                create_markdown_file()
                # Should not raise
                result = validate_markdown_file()
                assert result is True
            finally:
                import os

                os.chdir(original_cwd)

    def test_validate_markdown_file_fails_on_missing_file(self):
        """Test validate_markdown_file fails on missing file."""
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
                    b"\xef\xbb\xbf# Title\n\nFirst. Second. Third."
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
            custom_msg = "feat(207): Custom commit message"
            git_commit(custom_msg)
            mock_run.assert_called_once_with(
                ["git", "commit", "-m", custom_msg],
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

    def test_git_push_calls_git_correctly_with_head(self):
        """Test git_push calls subprocess.run with correct arguments using HEAD."""
        with patch("subprocess.run") as mock_run:
            git_push()
            # Feature 207 uses "HEAD" instead of branch name
            mock_run.assert_called_once_with(
                ["git", "push", "-u", "origin", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            )

    def test_git_push_uses_branch_name_for_logging(self):
        """Test git_push accepts branch_name parameter for logging context."""
        with patch("subprocess.run") as mock_run:
            # Branch name should be accepted as parameter but command uses HEAD
            git_push("custom-branch")
            # Still uses HEAD in the command
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

    @patch("subprocess.run")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title")
    def test_main_successful_workflow(self, mock_title, mock_prose, mock_run):
        """Test main() completes successfully with all operations."""
        mock_title.return_value = "Test Title"
        mock_prose.return_value = "First sentence. Second sentence. Third sentence."

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                from sheep.features.feature_207_markdown_file_creation import main

                main()
                # If we get here without exception, test passes
                assert Path(FILENAME).exists()
            finally:
                import os

                os.chdir(original_cwd)

    @patch("sheep.features.feature_207_markdown_file_creation.create_markdown_file")
    def test_main_exits_on_file_creation_failure(self, mock_create):
        """Test main() propagates file creation failure."""
        mock_create.side_effect = OSError("Failed to create file")
        from sheep.features.feature_207_markdown_file_creation import main

        with pytest.raises(OSError, match="Failed to create file"):
            main()

    @patch("subprocess.run")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title")
    def test_main_exits_on_validation_failure(self, mock_title, mock_prose, mock_run):
        """Test main() propagates validation failure."""
        mock_title.return_value = "Title"
        mock_prose.return_value = "One sentence."  # Invalid: only 1 sentence

        from sheep.features.feature_207_markdown_file_creation import main

        with pytest.raises(ValueError):
            main()

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("subprocess.run")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title")
    def test_main_calls_all_git_operations(self, mock_title, mock_prose, mock_run, mock_add, mock_commit, mock_push):
        """Test main() calls all git operations in sequence."""
        mock_title.return_value = "Test Title"
        mock_prose.return_value = "First. Second. Third."

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmpdir)
                from sheep.features.feature_207_markdown_file_creation import main

                main()

                # Verify all git operations were called
                mock_add.assert_called_once_with(FILENAME)
                mock_commit.assert_called_once_with(COMMIT_MESSAGE)
                mock_push.assert_called_once_with(BRANCH_NAME)
            finally:
                import os

                os.chdir(original_cwd)
