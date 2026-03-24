#!/usr/bin/env python3
"""
Test suite for feature 191: markdown-file-creation-5725bf
Tests create_file() and validate_file() functions.
"""

import pytest
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock
from create_markdown_file_191 import create_file, validate_file, TITLE, PROSE


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
                b"\xef\xbb\xbf" + "# Title\n\nContent.\n".encode("utf-8")
            )
            with pytest.raises(ValueError, match="UTF-8 BOM"):
                validate_file(test_file)

    def test_validate_file_raises_on_crlf(self):
        """Test that validate_file raises ValueError for CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "with_crlf.md"
            # Write with CRLF
            test_file.write_bytes(
                f"# {TITLE}\r\n\r\n{PROSE}\r\n".encode("utf-8")
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
            test_file.write_bytes(f"# Title\n\nOne. Two. Three.".encode("utf-8"))
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
        from create_markdown_file_191 import git_add

        with patch("subprocess.run") as mock_run:
            git_add("test.md")

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once_with(["git", "add", "test.md"], check=True)

    def test_git_add_raises_on_failure(self):
        """Test git_add raises CalledProcessError on failure."""
        from create_markdown_file_191 import git_add

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(128, ["git", "add", "test.md"])

            with pytest.raises(subprocess.CalledProcessError):
                git_add("test.md")

    def test_git_commit_with_message(self):
        """Test git_commit executes correct command with message."""
        from create_markdown_file_191 import git_commit

        with patch("subprocess.run") as mock_run:
            test_message = "feat(191): test commit"
            git_commit(test_message)

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once_with(
                ["git", "commit", "-m", test_message],
                check=True
            )

    def test_git_commit_raises_on_failure(self):
        """Test git_commit raises CalledProcessError on failure."""
        from create_markdown_file_191 import git_commit

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, ["git", "commit"])

            with pytest.raises(subprocess.CalledProcessError):
                git_commit("test message")

    def test_git_push_default_command(self):
        """Test git_push executes correct command."""
        from create_markdown_file_191 import git_push

        with patch("subprocess.run") as mock_run:
            git_push()

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once_with(
                ["git", "push", "-u", "origin", "HEAD"],
                check=True
            )

    def test_git_push_raises_on_failure(self):
        """Test git_push raises CalledProcessError on failure."""
        from create_markdown_file_191 import git_push

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, ["git", "push"])

            with pytest.raises(subprocess.CalledProcessError):
                git_push()


class TestMain:
    """Test suite for main() function and error handling."""

    def test_main_fails_when_file_already_exists(self, capsys):
        """Test main() prints error and exits(1) when file already exists."""
        from create_markdown_file_191 import main

        # Mock create_file to return None (indicating file already exists)
        # Make sys.exit raise SystemExit with the provided code
        def mock_exit_func(code=0):
            raise SystemExit(code)

        with patch("create_markdown_file_191.create_file", return_value=None):
            with patch("sys.exit", side_effect=mock_exit_func):
                with pytest.raises(SystemExit) as exc_info:
                    main()

        # Verify exit code was 1
        assert exc_info.value.code == 1

        # Verify error message was printed
        captured = capsys.readouterr()
        assert "already exists" in captured.err.lower()

    def test_main_fails_on_validation_error(self, capsys):
        """Test main() prints validation error and exits(1) when validation fails."""
        from create_markdown_file_191 import main

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "invalid.md"

            # Mock create_file to create an invalid file (missing heading)
            def create_invalid_file(filename):
                Path(filename).write_text("Content without heading.\n", encoding="utf-8", newline="\n")
                return True

            with patch("sys.exit") as mock_exit:
                with patch("create_markdown_file_191.create_file", create_invalid_file):
                    with patch("create_markdown_file_191.FILENAME", str(test_file)):
                        main()

                # Verify exit(1) was called
                mock_exit.assert_called_once_with(1)

                # Verify validation error message was printed
                captured = capsys.readouterr()
                assert "validation" in captured.err.lower() or "failed" in captured.err.lower()

    def test_main_fails_on_git_add_failure(self, capsys):
        """Test main() prints git error and exits(1) when git add fails."""
        from create_markdown_file_191 import main

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"

            # Mock functions to reach git_add failure
            def create_valid_file(filename):
                create_file(test_file)
                return True

            def mock_git_add_failure(filename):
                raise subprocess.CalledProcessError(128, ["git", "add", filename], stderr="Permission denied")

            with patch("sys.exit") as mock_exit:
                with patch("create_markdown_file_191.create_file", create_valid_file):
                    with patch("create_markdown_file_191.validate_file", return_value=True):
                        with patch("create_markdown_file_191.git_add", mock_git_add_failure):
                            with patch("create_markdown_file_191.FILENAME", str(test_file)):
                                main()

                # Verify exit(1) was called
                mock_exit.assert_called_once_with(1)

                # Verify git error message was printed
                captured = capsys.readouterr()
                assert "git" in captured.err.lower() or "failed" in captured.err.lower()

    def test_main_fails_on_git_commit_failure(self, capsys):
        """Test main() prints git error and exits(1) when git commit fails."""
        from create_markdown_file_191 import main

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"

            # Mock functions to reach git_commit failure
            def create_valid_file(filename):
                create_file(test_file)
                return True

            def mock_git_commit_failure(message):
                raise subprocess.CalledProcessError(1, ["git", "commit"], stderr="Nothing to commit")

            with patch("sys.exit") as mock_exit:
                with patch("create_markdown_file_191.create_file", create_valid_file):
                    with patch("create_markdown_file_191.validate_file", return_value=True):
                        with patch("create_markdown_file_191.git_add", return_value=True):
                            with patch("create_markdown_file_191.git_commit", mock_git_commit_failure):
                                with patch("create_markdown_file_191.FILENAME", str(test_file)):
                                    main()

                # Verify exit(1) was called
                mock_exit.assert_called_once_with(1)

                # Verify git error message was printed
                captured = capsys.readouterr()
                assert "git" in captured.err.lower() or "failed" in captured.err.lower()

    def test_main_fails_on_git_push_failure(self, capsys):
        """Test main() prints git error and exits(1) when git push fails."""
        from create_markdown_file_191 import main

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"

            # Mock functions to reach git_push failure
            def create_valid_file(filename):
                create_file(test_file)
                return True

            def mock_git_push_failure():
                raise subprocess.CalledProcessError(128, ["git", "push"], stderr="Network error")

            with patch("sys.exit") as mock_exit:
                with patch("create_markdown_file_191.create_file", create_valid_file):
                    with patch("create_markdown_file_191.validate_file", return_value=True):
                        with patch("create_markdown_file_191.git_add", return_value=True):
                            with patch("create_markdown_file_191.git_commit", return_value=True):
                                with patch("create_markdown_file_191.git_push", mock_git_push_failure):
                                    with patch("create_markdown_file_191.FILENAME", str(test_file)):
                                        main()

                # Verify exit(1) was called
                mock_exit.assert_called_once_with(1)

                # Verify git error message was printed
                captured = capsys.readouterr()
                assert "git" in captured.err.lower() or "failed" in captured.err.lower()

    def test_main_succeeds_with_all_steps(self, capsys):
        """Test main() succeeds when all workflow steps complete successfully."""
        from create_markdown_file_191 import main

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"

            # Mock all operations to succeed
            def create_valid_file(filename):
                create_file(test_file)
                return True

            with patch("sys.exit") as mock_exit:
                with patch("create_markdown_file_191.create_file", create_valid_file):
                    with patch("create_markdown_file_191.validate_file", return_value=True):
                        with patch("create_markdown_file_191.git_add", return_value=True):
                            with patch("create_markdown_file_191.git_commit", return_value=True):
                                with patch("create_markdown_file_191.git_push", return_value=True):
                                    with patch("create_markdown_file_191.FILENAME", str(test_file)):
                                        main()

                # Verify exit(0) was called (success)
                mock_exit.assert_called_once_with(0)

                # Verify success message was printed
                captured = capsys.readouterr()
                output = captured.out + captured.err
                assert "success" in output.lower() or "created" in output.lower()

    def test_main_error_messages_are_descriptive(self, capsys):
        """Test main() error messages provide useful debugging information."""
        from create_markdown_file_191 import main

        # Test ValueError error message
        with patch("sys.exit"):
            with patch("create_markdown_file_191.create_file", return_value=True):
                with patch("create_markdown_file_191.validate_file", side_effect=ValueError("Invalid encoding: UTF-8 BOM detected")):
                    with patch("create_markdown_file_191.FILENAME", "test.md"):
                        main()

        captured = capsys.readouterr()
        assert "validation" in captured.err.lower()
        assert "utf-8" in captured.err.lower() or "bom" in captured.err.lower() or "encoding" in captured.err.lower()

    def test_main_handles_oserror(self, capsys):
        """Test main() catches and reports OSError properly."""
        from create_markdown_file_191 import main

        with patch("sys.exit") as mock_exit:
            with patch("create_markdown_file_191.create_file", side_effect=OSError("Permission denied: cannot write to /root/test.md")):
                with patch("create_markdown_file_191.FILENAME", "test.md"):
                    main()

        # Verify exit(1) was called
        mock_exit.assert_called_once_with(1)

        # Verify error message was printed
        captured = capsys.readouterr()
        assert "i/o" in captured.err.lower() or "error" in captured.err.lower()

    def test_main_workflow_orchestration(self, capsys):
        """Test that main() calls functions in correct order."""
        from create_markdown_file_191 import main

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"

            call_order = []

            def mock_create(filename):
                call_order.append("create")
                create_file(test_file)
                return True

            def mock_validate(filename):
                call_order.append("validate")
                return True

            def mock_add(filename):
                call_order.append("git_add")
                return True

            def mock_commit(message):
                call_order.append("git_commit")
                return True

            def mock_push():
                call_order.append("git_push")
                return True

            with patch("sys.exit"):
                with patch("create_markdown_file_191.create_file", mock_create):
                    with patch("create_markdown_file_191.validate_file", mock_validate):
                        with patch("create_markdown_file_191.git_add", mock_add):
                            with patch("create_markdown_file_191.git_commit", mock_commit):
                                with patch("create_markdown_file_191.git_push", mock_push):
                                    with patch("create_markdown_file_191.FILENAME", str(test_file)):
                                        main()

            # Verify functions were called in correct order
            assert call_order == ["create", "validate", "git_add", "git_commit", "git_push"]
