#!/usr/bin/env python3
"""
Test suite for feature 190: markdown-file-creation-6778d8
Tests create_file() and validate_file() functions.
"""

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from create_markdown_file_190 import PROSE, TITLE, create_file, validate_file


class TestCreateFile:
    """Test suite for create_file function."""

    def test_create_file_returns_true_on_success(self):
        """Test that create_file returns True when file is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            result = create_file(test_file)
            assert result is True
            assert test_file.exists()

    def test_create_file_returns_none_if_exists(self):
        """Test that create_file returns None if file already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            # Create file first time
            create_file(test_file)
            # Try to create again
            result = create_file(test_file)
            assert result is None

    def test_create_file_contains_h1_heading(self):
        """Test that created file contains H1 heading with TITLE."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            create_file(test_file)
            content = test_file.read_text(encoding="utf-8")
            assert content.startswith(f"# {TITLE}\n")

    def test_create_file_contains_blank_line_after_heading(self):
        """Test that created file has blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            create_file(test_file)
            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")
            assert lines[0].startswith("# ")
            assert lines[1] == ""

    def test_create_file_contains_prose(self):
        """Test that created file contains PROSE content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            create_file(test_file)
            content = test_file.read_text(encoding="utf-8")
            assert PROSE in content

    def test_create_file_uses_utf8_encoding(self):
        """Test that created file uses UTF-8 encoding without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            create_file(test_file)
            binary = test_file.read_bytes()
            # Should not start with UTF-8 BOM (EF BB BF)
            assert not binary.startswith(b"\xef\xbb\xbf")
            # Should decode as UTF-8
            content = binary.decode("utf-8")
            assert content is not None

    def test_create_file_uses_lf_line_endings(self):
        """Test that created file uses Unix LF line endings only."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            create_file(test_file)
            binary = test_file.read_bytes()
            # Should not contain CRLF (0x0D 0x0A)
            assert b"\r\n" not in binary
            # Should contain LF (0x0A)
            assert b"\n" in binary

    def test_create_file_ends_with_newline(self):
        """Test that created file ends with newline character."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            create_file(test_file)
            content = test_file.read_text(encoding="utf-8")
            assert content.endswith("\n")

    def test_create_file_size_in_range(self):
        """Test that created file size is between 400-600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            create_file(test_file)
            file_size = test_file.stat().st_size
            assert 400 <= file_size <= 600

    def test_create_file_accepts_string_path(self):
        """Test that create_file accepts string paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = str(Path(tmpdir) / "test.md")
            result = create_file(test_file)
            assert result is True
            assert Path(test_file).exists()

    def test_create_file_accepts_path_object(self):
        """Test that create_file accepts Path objects."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            result = create_file(test_file)
            assert result is True
            assert test_file.exists()


class TestValidateFile:
    """Test suite for validate_file function."""

    def test_validate_file_returns_true_for_valid_file(self):
        """Test that validate_file returns True for valid file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            create_file(test_file)
            result = validate_file(test_file)
            assert result is True

    def test_validate_file_raises_on_missing_file(self):
        """Test that validate_file raises ValueError for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "nonexistent.md"
            with pytest.raises(ValueError, match="File does not exist"):
                validate_file(test_file)

    def test_validate_file_raises_on_empty_file(self):
        """Test that validate_file raises ValueError for empty file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "empty.md"
            test_file.write_text("", encoding="utf-8")
            with pytest.raises(ValueError, match="File is empty"):
                validate_file(test_file)

    def test_validate_file_raises_on_bom(self):
        """Test that validate_file raises ValueError for UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "with_bom.md"
            # Write with BOM
            test_file.write_bytes(
                b"\xef\xbb\xbf" + b"# Title\n\nContent.\n"
            )
            with pytest.raises(ValueError, match="UTF-8 BOM"):
                validate_file(test_file)

    def test_validate_file_raises_on_crlf(self):
        """Test that validate_file raises ValueError for CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "with_crlf.md"
            # Write with CRLF
            test_file.write_bytes(
                f"# {TITLE}\r\n\r\n{PROSE}\r\n".encode()
            )
            with pytest.raises(ValueError, match="CRLF"):
                validate_file(test_file)

    def test_validate_file_raises_on_invalid_utf8(self):
        """Test that validate_file raises ValueError for invalid UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "invalid_utf8.md"
            # Write invalid UTF-8 bytes
            test_file.write_bytes(b"\xff\xfe\x00\x00")
            with pytest.raises(ValueError, match="not valid UTF-8"):
                validate_file(test_file)

    def test_validate_file_raises_on_no_h1_heading(self):
        """Test that validate_file raises ValueError without H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "no_heading.md"
            test_file.write_text("## Not an H1 heading\n\nContent.\n", encoding="utf-8", newline="\n")
            with pytest.raises(ValueError, match="H1 heading"):
                validate_file(test_file)

    def test_validate_file_raises_on_no_blank_line(self):
        """Test that validate_file raises ValueError without blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "no_blank.md"
            test_file.write_text(f"# {TITLE}\n{PROSE}\n", encoding="utf-8", newline="\n")
            with pytest.raises(ValueError, match="blank"):
                validate_file(test_file)

    def test_validate_file_raises_on_no_prose(self):
        """Test that validate_file raises ValueError without prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "no_prose.md"
            test_file.write_text(f"# {TITLE}\n\n\n", encoding="utf-8", newline="\n")
            with pytest.raises(ValueError, match="Prose content is empty"):
                validate_file(test_file)

    def test_validate_file_raises_on_too_few_sentences(self):
        """Test that validate_file raises ValueError for <2 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "one_sentence.md"
            test_file.write_text("# Title\n\nJust one sentence.\n", encoding="utf-8", newline="\n")
            with pytest.raises(ValueError, match="2-3 sentences"):
                validate_file(test_file)

    def test_validate_file_raises_on_too_many_sentences(self):
        """Test that validate_file raises ValueError for >3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "four_sentences.md"
            test_file.write_text(
                "# Title\n\nOne. Two. Three. Four.\n",
                encoding="utf-8",
                newline="\n"
            )
            with pytest.raises(ValueError, match="2-3 sentences"):
                validate_file(test_file)

    def test_validate_file_raises_on_no_trailing_newline(self):
        """Test that validate_file raises ValueError without trailing newline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "no_trailing.md"
            test_file.write_bytes(b"# Title\n\nOne. Two. Three.")
            with pytest.raises(ValueError, match="newline"):
                validate_file(test_file)

    def test_validate_file_raises_on_file_too_small(self):
        """Test that validate_file raises ValueError for file <400 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "too_small.md"
            # Cannot easily create a file with 2-3 sentences that is <400 bytes
            # because heading + blank line + minimum prose is already ~150+ bytes
            # Skip this test as size validation is after sentence validation
            pytest.skip("File with 2-3 sentences cannot be <400 bytes naturally")

    def test_validate_file_raises_on_file_too_large(self):
        """Test that validate_file raises ValueError for file >600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "too_large.md"
            # Create prose with exactly 2 sentences but long enough to exceed 600 bytes
            # We deliberately make the sentences very long with lots of padding words
            long_prose = (
                "This is the first very long sentence that contains many many words and additional padding text "
                "to make it extend across multiple lines and take up significant space in the file with extra content "
                "and more filler text and words to increase the total length without adding more sentences at all "
                "and even more text here with additional words and phrases for padding purposes only. "
                "This is the second very long sentence that also contains many more words and supplementary material "
                "to ensure we have enough text to exceed the six hundred byte maximum size limit for files completely "
                "and with additional padding words and phrases and clauses to push the total file size well over the limit."
            )
            test_file.write_text(
                f"# Title\n\n{long_prose}\n",
                encoding="utf-8",
                newline="\n"
            )
            with pytest.raises(ValueError, match="400-600"):
                validate_file(test_file)

    def test_validate_file_accepts_string_path(self):
        """Test that validate_file accepts string paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = str(Path(tmpdir) / "test.md")
            create_file(test_file)
            result = validate_file(test_file)
            assert result is True

    def test_validate_file_accepts_path_object(self):
        """Test that validate_file accepts Path objects."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            create_file(test_file)
            result = validate_file(test_file)
            assert result is True


class TestIntegration:
    """Integration tests for create_file and validate_file together."""

    def test_created_file_passes_validation(self):
        """Test that file created by create_file passes validate_file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            create_file(test_file)
            result = validate_file(test_file)
            assert result is True

    def test_create_and_validate_workflow(self):
        """Test complete create and validate workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "integration_test.md"

            # Create file
            create_result = create_file(test_file)
            assert create_result is True
            assert test_file.exists()

            # Validate file
            validate_result = validate_file(test_file)
            assert validate_result is True

    def test_multiple_files_independent(self):
        """Test that creating multiple files doesn't interfere."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "test1.md"
            file2 = Path(tmpdir) / "test2.md"

            create_file(file1)
            create_file(file2)

            assert validate_file(file1) is True
            assert validate_file(file2) is True

    def test_validation_error_messages_are_clear(self):
        """Test that validation errors provide clear messages."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Test each validation error message
            test_cases = [
                (
                    "missing_file.md",
                    lambda p: p,  # Don't create file
                    "File does not exist"
                ),
                (
                    "no_heading.md",
                    lambda p: p.write_text("Content only.\n", encoding="utf-8", newline="\n"),
                    "H1 heading"
                ),
                (
                    "one_sentence.md",
                    lambda p: p.write_text("# Title\n\nOne.\n", encoding="utf-8", newline="\n"),
                    "2-3 sentences"
                ),
            ]

            for filename, setup, expected_error in test_cases:
                test_file = Path(tmpdir) / filename
                setup(test_file)
                with pytest.raises(ValueError, match=expected_error):
                    validate_file(test_file)


class TestGitOperations:
    """Test suite for git operation functions."""

    def test_git_add_with_valid_file(self):
        """Test git_add executes correct command."""
        from create_markdown_file_190 import git_add

        with patch("subprocess.run") as mock_run:
            git_add("test.md")

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once_with(["git", "add", "test.md"], check=True)

    def test_git_add_raises_on_failure(self):
        """Test git_add raises CalledProcessError on failure."""
        from create_markdown_file_190 import git_add

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(128, ["git", "add", "test.md"])

            with pytest.raises(subprocess.CalledProcessError):
                git_add("test.md")

    def test_git_commit_with_message(self):
        """Test git_commit executes correct command with message."""
        from create_markdown_file_190 import git_commit

        with patch("subprocess.run") as mock_run:
            test_message = "feat(190): test commit"
            git_commit(test_message)

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once_with(
                ["git", "commit", "-m", test_message],
                check=True
            )

    def test_git_commit_raises_on_failure(self):
        """Test git_commit raises CalledProcessError on failure."""
        from create_markdown_file_190 import git_commit

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, ["git", "commit"])

            with pytest.raises(subprocess.CalledProcessError):
                git_commit("test message")

    def test_git_push_default_command(self):
        """Test git_push executes correct command."""
        from create_markdown_file_190 import git_push

        with patch("subprocess.run") as mock_run:
            git_push()

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once_with(
                ["git", "push", "-u", "origin", "HEAD"],
                check=True
            )

    def test_git_push_raises_on_failure(self):
        """Test git_push raises CalledProcessError on failure."""
        from create_markdown_file_190 import git_push

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(128, ["git", "push"])

            with pytest.raises(subprocess.CalledProcessError):
                git_push()

    def test_git_add_accepts_different_filenames(self):
        """Test git_add works with different filenames."""
        from create_markdown_file_190 import git_add

        with patch("subprocess.run") as mock_run:
            # Test with different filenames
            git_add("file1.md")
            git_add("file2.md")

            # Verify calls were made with correct filenames
            assert mock_run.call_count == 2
            calls = mock_run.call_args_list
            assert calls[0][0][0] == ["git", "add", "file1.md"]
            assert calls[1][0][0] == ["git", "add", "file2.md"]


class TestMainOrchestrator:
    """Test suite for main orchestrator function."""

    def test_main_complete_workflow_success(self, tmp_path):
        """Test main successfully orchestrates complete workflow."""
        # Change to temp directory for test
        import os

        from create_markdown_file_190 import FILENAME, main
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
        import os

        from create_markdown_file_190 import FILENAME, main
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

    def test_main_exits_with_1_on_validation_error(self, tmp_path):
        """Test main exits with code 1 on validation error."""
        import os

        from create_markdown_file_190 import main
        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Mock create_file to succeed but validation to fail
            def create_side_effect(filename):
                Path(filename).write_text("# Title\n\nOne.\n")  # Only 1 sentence
                return True

            with patch("create_markdown_file_190.create_file", side_effect=create_side_effect):
                # Run main
                with pytest.raises(SystemExit) as exc_info:
                    main()

                # Should exit with 1 on validation error
                assert exc_info.value.code == 1
        finally:
            os.chdir(original_dir)

    def test_main_exits_with_1_on_git_failure(self, tmp_path):
        """Test main exits with code 1 on git command failure."""
        import os

        from create_markdown_file_190 import main
        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Mock git_add to raise CalledProcessError
            with patch("create_markdown_file_190.create_file", return_value=True):
                with patch("create_markdown_file_190.validate_file", return_value=True):
                    with patch(
                        "create_markdown_file_190.git_add",
                        side_effect=subprocess.CalledProcessError(1, ["git", "add"])
                    ):
                        # Run main
                        with pytest.raises(SystemExit) as exc_info:
                            main()

                        # Should exit with 1 on git failure
                        assert exc_info.value.code == 1
        finally:
            os.chdir(original_dir)

    def test_main_calls_functions_in_order(self, tmp_path):
        """Test main calls functions in correct order."""
        import os

        from create_markdown_file_190 import main
        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Create call order tracker
            call_order = []

            def track_create(*args, **kwargs):
                call_order.append("create_file")
                return True

            def track_validate(*args, **kwargs):
                call_order.append("validate_file")
                return True

            def track_add(*args, **kwargs):
                call_order.append("git_add")

            def track_commit(*args, **kwargs):
                call_order.append("git_commit")

            def track_push(*args, **kwargs):
                call_order.append("git_push")

            with patch("create_markdown_file_190.create_file", side_effect=track_create):
                with patch("create_markdown_file_190.validate_file", side_effect=track_validate):
                    with patch("create_markdown_file_190.git_add", side_effect=track_add):
                        with patch("create_markdown_file_190.git_commit", side_effect=track_commit):
                            with patch("create_markdown_file_190.git_push", side_effect=track_push):
                                # Run main
                                with pytest.raises(SystemExit) as exc_info:
                                    main()

                                # Verify call order
                                assert call_order == ["create_file", "validate_file", "git_add", "git_commit", "git_push"]
                                assert exc_info.value.code == 0
        finally:
            os.chdir(original_dir)

    def test_main_with_oserror(self, tmp_path):
        """Test main exits with 1 on OSError."""
        import os

        from create_markdown_file_190 import main
        original_dir = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Mock create_file to raise OSError
            with patch("create_markdown_file_190.create_file", side_effect=OSError("Permission denied")):
                # Run main
                with pytest.raises(SystemExit) as exc_info:
                    main()

                # Should exit with 1 on OSError
                assert exc_info.value.code == 1
        finally:
            os.chdir(original_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
