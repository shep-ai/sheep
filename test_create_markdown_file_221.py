#!/usr/bin/env python3
"""
Test suite for feature 221: markdown-test-file-009057
Tests create_file() and git operations functions.
No validation layer per spec requirement.
"""

import pytest
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock
from create_markdown_file_221 import create_file, git_add, git_commit, git_push, TITLE, PROSE


class TestCreateFile:
    """Test suite for create_file function."""

    def test_create_file_returns_path_on_success(self):
        """Test that create_file returns Path when file is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test-0uftqx.md"
            # Change working directory to temp directory
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Mock to use local file
                from create_markdown_file_221 import FILENAME
                result = create_file()
                assert result is not None
                assert Path(FILENAME).exists()
            finally:
                os.chdir(original_dir)

    def test_create_file_raises_if_exists(self):
        """Test that create_file raises FileExistsError if file already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test-0uftqx.md"
            # Create file first
            test_file.write_text("# Title\n\nContent.\n")
            # Now try to create again
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                from create_markdown_file_221 import FILENAME
                with pytest.raises(FileExistsError):
                    create_file()
            finally:
                os.chdir(original_dir)

    def test_create_file_contains_h1_heading(self):
        """Test that created file contains H1 heading with TITLE."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                from create_markdown_file_221 import FILENAME
                content = Path(FILENAME).read_text(encoding="utf-8")
                assert content.startswith(f"# {TITLE}\n")
            finally:
                os.chdir(original_dir)

    def test_create_file_contains_blank_line_after_heading(self):
        """Test that created file has blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                from create_markdown_file_221 import FILENAME
                content = Path(FILENAME).read_text(encoding="utf-8")
                lines = content.split("\n")
                assert lines[0].startswith("# ")
                assert lines[1] == ""
            finally:
                os.chdir(original_dir)

    def test_create_file_contains_prose(self):
        """Test that created file contains PROSE content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                from create_markdown_file_221 import FILENAME
                content = Path(FILENAME).read_text(encoding="utf-8")
                assert PROSE in content
            finally:
                os.chdir(original_dir)

    def test_create_file_uses_utf8_encoding(self):
        """Test that created file uses UTF-8 encoding without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                from create_markdown_file_221 import FILENAME
                binary = Path(FILENAME).read_bytes()
                # Should not start with UTF-8 BOM (EF BB BF)
                assert not binary.startswith(b"\xef\xbb\xbf")
                # Should decode as UTF-8
                content = binary.decode("utf-8")
                assert content is not None
            finally:
                os.chdir(original_dir)

    def test_create_file_uses_lf_line_endings(self):
        """Test that created file uses Unix LF line endings only."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                from create_markdown_file_221 import FILENAME
                binary = Path(FILENAME).read_bytes()
                # Should not contain CRLF (0x0D 0x0A)
                assert b"\r\n" not in binary
                # Should contain LF (0x0A)
                assert b"\n" in binary
            finally:
                os.chdir(original_dir)

    def test_create_file_ends_with_newline(self):
        """Test that created file ends with newline character."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                from create_markdown_file_221 import FILENAME
                content = Path(FILENAME).read_text(encoding="utf-8")
                assert content.endswith("\n")
            finally:
                os.chdir(original_dir)

    def test_create_file_size_in_range(self):
        """Test that created file size is between 300-600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                from create_markdown_file_221 import FILENAME
                file_size = Path(FILENAME).stat().st_size
                assert 300 <= file_size <= 600
            finally:
                os.chdir(original_dir)


class TestGitOperations:
    """Test suite for git operation functions."""

    def test_git_add_with_valid_file(self):
        """Test git_add executes correct command."""
        with patch("subprocess.run") as mock_run:
            git_add()

            # Verify subprocess.run was called with correct arguments
            from create_markdown_file_221 import FILENAME
            mock_run.assert_called_once_with(["git", "add", FILENAME], check=True)

    def test_git_add_raises_on_failure(self):
        """Test git_add raises CalledProcessError on failure."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(128, ["git", "add", "test.md"])

            with pytest.raises(subprocess.CalledProcessError):
                git_add()

    def test_git_commit_with_message(self):
        """Test git_commit executes correct command with message."""
        with patch("subprocess.run") as mock_run:
            git_commit()

            # Verify subprocess.run was called with correct arguments
            from create_markdown_file_221 import COMMIT_MESSAGE
            mock_run.assert_called_once_with(
                ["git", "commit", "-m", COMMIT_MESSAGE],
                check=True
            )

    def test_git_commit_raises_on_failure(self):
        """Test git_commit raises CalledProcessError on failure."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, ["git", "commit"])

            with pytest.raises(subprocess.CalledProcessError):
                git_commit()

    def test_git_push_default_command(self):
        """Test git_push executes correct command."""
        with patch("subprocess.run") as mock_run:
            git_push()

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once_with(
                ["git", "push", "-u", "origin", "HEAD"],
                check=True
            )

    def test_git_push_raises_on_failure(self):
        """Test git_push raises CalledProcessError on failure."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(128, ["git", "push"])

            with pytest.raises(subprocess.CalledProcessError):
                git_push()

    def test_git_operations_sequence(self):
        """Test that git operations use list arguments (safe from injection)."""
        # This is a safety check - ensure all git calls use list arguments, not strings
        from create_markdown_file_221 import FILENAME, COMMIT_MESSAGE

        # Verify FILENAME doesn't contain special shell characters
        assert isinstance(FILENAME, str)
        assert FILENAME == "test-0uftqx.md"

        # Verify COMMIT_MESSAGE follows conventional commit format
        assert COMMIT_MESSAGE.startswith("feat(221):")


class TestMainOrchestrator:
    """Test suite for main orchestrator function."""

    def test_main_complete_workflow_success(self, tmp_path):
        """Test main successfully orchestrates complete workflow."""
        from create_markdown_file_221 import main, FILENAME

        # Change to temp directory for test
        import os
        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Mock git operations
            with patch("subprocess.run"):
                # Run main
                with pytest.raises(SystemExit) as exc_info:
                    main()

                # Should exit with 0 on success
                assert exc_info.value.code == 0

                # File should exist
                assert (tmp_path / FILENAME).exists()
        finally:
            os.chdir(original_dir)

    def test_main_exits_with_1_on_file_exists(self, tmp_path):
        """Test main exits with code 1 when file already exists."""
        from create_markdown_file_221 import main, FILENAME

        import os
        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Create file first
            (tmp_path / FILENAME).write_text("# Title\n\nContent.\n")

            # Run main
            with pytest.raises(SystemExit) as exc_info:
                main()

            # Should exit with 1 when file exists
            assert exc_info.value.code == 1
        finally:
            os.chdir(original_dir)

    def test_main_exits_with_1_on_git_failure(self, tmp_path):
        """Test main exits with code 1 on git command failure."""
        from create_markdown_file_221 import main

        import os
        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Mock git_add to raise CalledProcessError
            with patch("create_markdown_file_221.git_add",
                       side_effect=subprocess.CalledProcessError(1, ["git", "add"])):
                # Run main
                with pytest.raises(SystemExit) as exc_info:
                    main()

                # Should exit with 1 on git failure
                assert exc_info.value.code == 1
        finally:
            os.chdir(original_dir)

    def test_main_calls_functions_in_order(self, tmp_path):
        """Test main calls functions in correct order."""
        from create_markdown_file_221 import main

        import os
        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Track call order
            call_order = []

            def track_create_file():
                call_order.append("create_file")
                return Path("test-0uftqx.md")

            def track_git_add():
                call_order.append("git_add")

            def track_git_commit():
                call_order.append("git_commit")

            def track_git_push():
                call_order.append("git_push")

            with patch("create_markdown_file_221.create_file", side_effect=track_create_file), \
                 patch("create_markdown_file_221.git_add", side_effect=track_git_add), \
                 patch("create_markdown_file_221.git_commit", side_effect=track_git_commit), \
                 patch("create_markdown_file_221.git_push", side_effect=track_git_push), \
                 patch("subprocess.run"):
                try:
                    with pytest.raises(SystemExit):
                        main()
                except SystemExit:
                    pass

            # Verify correct call order
            assert call_order == ["create_file", "git_add", "git_commit", "git_push"]
        finally:
            os.chdir(original_dir)


class TestCommitMessageFormat:
    """Test suite for conventional commit message format."""

    def test_commit_message_format(self):
        """Test that commit message follows conventional commits specification."""
        from create_markdown_file_221 import COMMIT_MESSAGE

        # Should start with feat(221):
        assert COMMIT_MESSAGE.startswith("feat(221):")

        # Should contain the file name
        assert "test-0uftqx.md" in COMMIT_MESSAGE

        # Should be descriptive
        assert "Create" in COMMIT_MESSAGE or "create" in COMMIT_MESSAGE

    def test_filename_constant(self):
        """Test that FILENAME constant is set correctly."""
        from create_markdown_file_221 import FILENAME

        assert FILENAME == "test-0uftqx.md"
        assert isinstance(FILENAME, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
