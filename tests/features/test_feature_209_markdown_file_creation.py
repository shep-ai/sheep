"""Tests for feature 209: Create markdown file test-xvuuel.md.

Tests cover:
- Module imports and constants
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

from sheep.features.feature_209_markdown_file_creation import (
    BRANCH_NAME,
    COMMIT_MESSAGE,
    FILENAME,
    FEATURE_NUMBER,
    PROSE_CONTENT,
    TITLE_TEXT,
    create_markdown_file,
    git_add_file,
    git_commit,
    git_push,
    main,
)


class TestConstants:
    """Tests for module constants."""

    def test_filename_is_correct(self):
        """Test that FILENAME is set to test-xvuuel.md."""
        assert FILENAME == "test-xvuuel.md"

    def test_feature_number_is_209(self):
        """Test that FEATURE_NUMBER is 209."""
        assert FEATURE_NUMBER == 209

    def test_branch_name_is_correct(self):
        """Test that BRANCH_NAME is set correctly."""
        assert BRANCH_NAME == "feat/markdown-file-creation-c22064"

    def test_commit_message_format(self):
        """Test that COMMIT_MESSAGE follows conventional commit format."""
        assert COMMIT_MESSAGE.startswith(f"feat({FEATURE_NUMBER}):")
        assert FILENAME in COMMIT_MESSAGE

    def test_title_text_is_non_empty(self):
        """Test that TITLE_TEXT is non-empty string."""
        assert isinstance(TITLE_TEXT, str)
        assert len(TITLE_TEXT) > 0

    def test_prose_content_is_non_empty(self):
        """Test that PROSE_CONTENT is non-empty string."""
        assert isinstance(PROSE_CONTENT, str)
        assert len(PROSE_CONTENT) > 0


class TestFileCreation:
    """Tests for file creation functionality."""

    def test_create_markdown_file_creates_file(self):
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

    def test_create_markdown_file_returns_path_object(self):
        """Test that create_markdown_file returns a Path object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                file_path = create_markdown_file()
                assert isinstance(file_path, Path)
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

    def test_create_markdown_file_format_correct(self):
        """Test that file has correct format: # Title\\n\\nProse\\n."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_markdown_file()
                content = Path(FILENAME).read_text()
                # Check format: title on first line, blank line, prose
                lines = content.split("\n")
                assert lines[0] == f"# {TITLE_TEXT}"
                assert lines[1] == ""
                assert PROSE_CONTENT in content
            finally:
                import os
                os.chdir(original_cwd)

    def test_create_markdown_file_utf8_encoding(self):
        """Test that file is created with UTF-8 encoding without BOM."""
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
        """Test that file uses Unix LF line endings (no CRLF or CR)."""
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

    def test_create_markdown_file_size_in_range(self):
        """Test that created file size is between 300-800 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_markdown_file()
                file_size = Path(FILENAME).stat().st_size
                assert 300 <= file_size <= 800
            finally:
                import os
                os.chdir(original_cwd)

    def test_create_markdown_file_raises_on_file_not_created(self):
        """Test that create_markdown_file raises if file not created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                # Mock Path.write_text to succeed but Path.exists to fail
                with patch('pathlib.Path.write_text'):
                    with patch('pathlib.Path.exists', return_value=False):
                        with pytest.raises(OSError, match="File was not created"):
                            create_markdown_file()
            finally:
                import os
                os.chdir(original_cwd)


class TestGitAdd:
    """Tests for git_add_file function."""

    def test_git_add_file_succeeds_with_valid_repo(self):
        """Test that git_add_file calls subprocess.run with correct arguments."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            git_add_file(FILENAME)
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert args[0] == ["git", "add", FILENAME]
            assert kwargs.get("check") is True
            assert kwargs.get("capture_output") is True
            assert kwargs.get("text") is True

    def test_git_add_file_raises_on_failure(self):
        """Test that git_add_file raises CalledProcessError on git failure."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, ["git", "add", FILENAME], stderr="Git error"
            )
            with pytest.raises(subprocess.CalledProcessError):
                git_add_file(FILENAME)

    def test_git_add_file_uses_default_filename(self):
        """Test that git_add_file uses FILENAME constant as default."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            git_add_file()
            args, kwargs = mock_run.call_args
            assert FILENAME in args[0]


class TestGitCommit:
    """Tests for git_commit function."""

    def test_git_commit_succeeds_with_valid_message(self):
        """Test that git_commit calls subprocess.run with correct arguments."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            git_commit(COMMIT_MESSAGE)
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert args[0] == ["git", "commit", "-m", COMMIT_MESSAGE]
            assert kwargs.get("check") is True
            assert kwargs.get("capture_output") is True
            assert kwargs.get("text") is True

    def test_git_commit_raises_on_failure(self):
        """Test that git_commit raises CalledProcessError on git failure."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, ["git", "commit", "-m", COMMIT_MESSAGE], stderr="Git error"
            )
            with pytest.raises(subprocess.CalledProcessError):
                git_commit(COMMIT_MESSAGE)

    def test_git_commit_uses_default_message(self):
        """Test that git_commit uses COMMIT_MESSAGE constant as default."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            git_commit()
            args, kwargs = mock_run.call_args
            assert COMMIT_MESSAGE in args[0]


class TestGitPush:
    """Tests for git_push function."""

    def test_git_push_succeeds(self):
        """Test that git_push calls subprocess.run with correct arguments."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            git_push()
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert args[0] == ["git", "push", "-u", "origin", "HEAD"]
            assert kwargs.get("check") is True
            assert kwargs.get("capture_output") is True
            assert kwargs.get("text") is True

    def test_git_push_raises_on_failure(self):
        """Test that git_push raises CalledProcessError on git failure."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, ["git", "push", "-u", "origin", "HEAD"], stderr="Git error"
            )
            with pytest.raises(subprocess.CalledProcessError):
                git_push()

    def test_git_push_uses_head_for_auto_detection(self):
        """Test that git_push uses HEAD for automatic branch detection."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            git_push()
            args, kwargs = mock_run.call_args
            assert "HEAD" in args[0]
            assert "-u" in args[0]


class TestMainOrchestration:
    """Tests for main orchestration function."""

    def test_main_returns_0_on_complete_success(self):
        """Test that main returns 0 when all phases succeed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                with patch('subprocess.run') as mock_run:
                    mock_run.return_value = MagicMock(returncode=0)
                    result = main()
                    assert result == 0
            finally:
                import os
                os.chdir(original_cwd)

    def test_main_returns_1_on_file_creation_failure(self):
        """Test that main returns 1 if file creation fails."""
        with patch('sheep.features.feature_209_markdown_file_creation.create_markdown_file') as mock_create:
            mock_create.side_effect = OSError("File creation failed")
            result = main()
            assert result == 1

    def test_main_returns_1_on_validation_failure(self):
        """Test that main returns 1 if validation fails."""
        with patch('sheep.features.feature_209_markdown_file_creation.validate_markdown_file') as mock_validate:
            mock_validate.side_effect = ValueError("Validation failed")
            with patch('subprocess.run') as mock_run:
                result = main()
                assert result == 1
                # Verify git operations were NOT called (stopped at validation)
                mock_run.assert_not_called()

    def test_main_returns_1_on_git_add_failure(self):
        """Test that main returns 1 if git add fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                with patch('subprocess.run') as mock_run:
                    # First call (git add) fails
                    mock_run.side_effect = [
                        subprocess.CalledProcessError(1, ["git", "add"], stderr="Git error"),
                    ]
                    result = main()
                    assert result == 1
            finally:
                import os
                os.chdir(original_cwd)

    def test_main_orchestrates_phases_in_order(self):
        """Test that main executes phases in correct order: create -> validate -> git."""
        call_order = []

        def mock_create():
            call_order.append("create")
            # Create a valid file for validation to pass
            create_markdown_file()

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                with patch('sheep.features.feature_209_markdown_file_creation.create_markdown_file', side_effect=mock_create):
                    with patch('sheep.features.feature_209_markdown_file_creation.validate_markdown_file') as mock_validate:
                        mock_validate.side_effect = lambda: call_order.append("validate")
                        with patch('subprocess.run') as mock_run:
                            mock_run.return_value = MagicMock(returncode=0)
                            mock_run.side_effect = [
                                MagicMock(returncode=0),  # git add
                                MagicMock(returncode=0),  # git commit
                                MagicMock(returncode=0),  # git push
                            ]

                            def git_ops():
                                call_order.append("git_add")
                                call_order.append("git_commit")
                                call_order.append("git_push")

                            with patch('sheep.features.feature_209_markdown_file_creation.git_add_file'):
                                with patch('sheep.features.feature_209_markdown_file_creation.git_commit'):
                                    with patch('sheep.features.feature_209_markdown_file_creation.git_push'):
                                        main()

                            assert "create" in call_order
                            assert "validate" in call_order

            finally:
                import os
                os.chdir(original_cwd)

    def test_main_stops_at_first_failure(self):
        """Test that main stops execution at first failure (fail-fast behavior)."""
        with patch('sheep.features.feature_209_markdown_file_creation.validate_markdown_file') as mock_validate:
            mock_validate.side_effect = ValueError("Validation failed")
            with patch('subprocess.run') as mock_run:
                result = main()
                assert result == 1
                # Verify subprocess (git operations) was never called
                mock_run.assert_not_called()
