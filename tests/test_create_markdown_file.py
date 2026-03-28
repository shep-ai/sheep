"""Tests for feature 174: Creating markdown file test-u9soe6.md with title and prose content."""

import os
from pathlib import Path

import pytest


class TestCreateFileFunction:
    """Tests for create_file() function."""

    def test_create_file_creates_file_at_correct_path(self, tmp_path):
        """Test that create_file() creates file at correct path."""
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            # Call create_file
            result = create_file()

            # Verify file exists
            assert Path("test-u9soe6.md").exists()
            assert result == Path("test-u9soe6.md")
        finally:
            os.chdir(original_cwd)

    def test_create_file_has_h1_heading_on_first_line(self, tmp_path):
        """Test that created file has H1 heading on first line."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            content = Path("test-u9soe6.md").read_text(encoding="utf-8")
            lines = content.split("\n")

            # First line should be H1 heading
            assert lines[0].startswith("# ")
            assert len(lines[0]) > 2  # Has content after "#"
        finally:
            os.chdir(original_cwd)

    def test_create_file_has_blank_line_on_second_line(self, tmp_path):
        """Test that created file has blank line on second line."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            content = Path("test-u9soe6.md").read_text(encoding="utf-8")
            lines = content.split("\n")

            # Second line (index 1) should be blank
            assert lines[1] == ""
        finally:
            os.chdir(original_cwd)

    def test_create_file_has_prose_content(self, tmp_path):
        """Test that created file has prose content after blank line."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            content = Path("test-u9soe6.md").read_text(encoding="utf-8")
            lines = content.split("\n")

            # Should have at least 3 lines (heading, blank, prose)
            assert len(lines) >= 3

            # Prose content should exist (starting from line 2)
            prose_content = "\n".join(lines[2:]).strip()
            assert len(prose_content) > 0
        finally:
            os.chdir(original_cwd)

    def test_create_file_uses_utf8_encoding(self, tmp_path):
        """Test that created file uses UTF-8 encoding without BOM."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            binary_content = Path("test-u9soe6.md").read_bytes()

            # No UTF-8 BOM (EF BB BF)
            assert not binary_content.startswith(b"\xef\xbb\xbf")

            # Should be decodable as UTF-8
            binary_content.decode("utf-8")
        finally:
            os.chdir(original_cwd)

    def test_create_file_uses_lf_line_endings(self, tmp_path):
        """Test that created file uses LF line endings, not CRLF."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            binary_content = Path("test-u9soe6.md").read_bytes()

            # No CRLF (Windows line endings)
            assert b"\r\n" not in binary_content
        finally:
            os.chdir(original_cwd)

    def test_create_file_has_2_to_3_sentences(self, tmp_path):
        """Test that created file has 2-3 sentences of prose."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            content = Path("test-u9soe6.md").read_text(encoding="utf-8")
            lines = content.split("\n")

            # Get prose content (after heading and blank line)
            prose_content = "\n".join(lines[2:]).strip()

            # Count sentences (periods indicate sentence endings)
            sentence_count = prose_content.count(".")

            # Should have 2-3 sentences
            assert 2 <= sentence_count <= 3
        finally:
            os.chdir(original_cwd)

    def test_create_file_ends_with_newline(self, tmp_path):
        """Test that created file ends with a newline."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            content = Path("test-u9soe6.md").read_text(encoding="utf-8")

            # Should end with newline
            assert content.endswith("\n")
        finally:
            os.chdir(original_cwd)

    def test_create_file_size_in_range(self, tmp_path):
        """Test that created file size is within 400-600 bytes."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            file_size = Path("test-u9soe6.md").stat().st_size

            # File size should be in 400-600 byte range
            assert 400 <= file_size <= 600
        finally:
            os.chdir(original_cwd)


class TestModuleConstants:
    """Tests for module constants."""

    def test_filename_constant_exists(self):
        """Test that FILENAME constant is defined."""
        from create_markdown_file import FILENAME

        assert FILENAME == "test-u9soe6.md"

    def test_title_constant_exists(self):
        """Test that TITLE constant is defined."""
        from create_markdown_file import TITLE

        assert isinstance(TITLE, str)
        assert len(TITLE) > 0

    def test_prose_constant_exists(self):
        """Test that PROSE constant is defined."""
        from create_markdown_file import PROSE

        assert isinstance(PROSE, str)
        assert len(PROSE) > 0

    def test_commit_message_constant_exists(self):
        """Test that COMMIT_MESSAGE constant is defined."""
        from create_markdown_file import COMMIT_MESSAGE

        assert COMMIT_MESSAGE == "feat(174): create markdown file test-u9soe6.md with prose content"


class TestValidateFileFunction:
    """Tests for validate_file() function."""

    def test_validate_file_passes_for_valid_file(self, tmp_path):
        """Test that validate_file() passes for properly created file."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file, validate_file

            create_file()

            # Should pass validation without raising exception
            result = validate_file("test-u9soe6.md")
            assert result is True
        finally:
            os.chdir(original_cwd)

    def test_validate_file_fails_for_missing_file(self, tmp_path):
        """Test that validate_file() raises ValueError for missing file."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import validate_file

            with pytest.raises(ValueError, match="File does not exist"):
                validate_file("nonexistent.md")
        finally:
            os.chdir(original_cwd)

    def test_validate_file_fails_for_empty_file(self, tmp_path):
        """Test that validate_file() raises ValueError for empty file."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import validate_file

            # Create empty file
            Path("empty.md").write_text("")

            with pytest.raises(ValueError, match="File is empty"):
                validate_file("empty.md")
        finally:
            os.chdir(original_cwd)

    def test_validate_file_detects_utf8_bom(self, tmp_path):
        """Test that validate_file() detects UTF-8 BOM."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import validate_file

            # Create file with UTF-8 BOM
            file_content = "# Title\n\nProse content. More content."
            Path("with_bom.md").write_bytes(
                b"\xef\xbb\xbf" + file_content.encode("utf-8")
            )

            with pytest.raises(ValueError, match="UTF-8 BOM"):
                validate_file("with_bom.md")
        finally:
            os.chdir(original_cwd)

    def test_validate_file_detects_crlf_line_endings(self, tmp_path):
        """Test that validate_file() detects CRLF line endings."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import validate_file

            # Create file with CRLF line endings
            file_content = "# Title\r\n\r\nProse content. More content.\r\n"
            Path("with_crlf.md").write_bytes(file_content.encode("utf-8"))

            with pytest.raises(ValueError, match="CRLF line endings"):
                validate_file("with_crlf.md")
        finally:
            os.chdir(original_cwd)

    def test_validate_file_fails_for_missing_h1_heading(self, tmp_path):
        """Test that validate_file() fails when H1 heading is missing."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import validate_file

            # Create file without H1 heading
            Path("no_heading.md").write_text(
                "## Not H1\n\nProse content. More content.\n"
            )

            with pytest.raises(ValueError, match="H1 heading"):
                validate_file("no_heading.md")
        finally:
            os.chdir(original_cwd)

    def test_validate_file_fails_for_missing_blank_line(self, tmp_path):
        """Test that validate_file() fails when blank line is missing."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import validate_file

            # Create file without blank line after heading
            Path("no_blank.md").write_text(
                "# Title\nProse content. More content.\n"
            )

            with pytest.raises(ValueError, match="Second line must be blank"):
                validate_file("no_blank.md")
        finally:
            os.chdir(original_cwd)

    def test_validate_file_fails_for_too_few_sentences(self, tmp_path):
        """Test that validate_file() fails for only 1 sentence."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import validate_file

            # Create file with only 1 sentence
            Path("one_sentence.md").write_text(
                "# Title\n\nJust one sentence.\n"
            )

            with pytest.raises(ValueError, match="2-3 sentences"):
                validate_file("one_sentence.md")
        finally:
            os.chdir(original_cwd)

    def test_validate_file_fails_for_too_many_sentences(self, tmp_path):
        """Test that validate_file() fails for 4+ sentences."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import validate_file

            # Create file with 4 sentences
            Path("four_sentences.md").write_text(
                "# Title\n\nFirst sentence. Second sentence. Third sentence. Fourth sentence.\n"
            )

            with pytest.raises(ValueError, match="2-3 sentences"):
                validate_file("four_sentences.md")
        finally:
            os.chdir(original_cwd)

    def test_validate_file_fails_for_missing_trailing_newline(self, tmp_path):
        """Test that validate_file() fails when file doesn't end with newline."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import validate_file

            # Create file without trailing newline
            Path("no_newline.md").write_bytes(
                b"# Title\n\nProse content. More content."
            )

            with pytest.raises(ValueError, match="must end with newline"):
                validate_file("no_newline.md")
        finally:
            os.chdir(original_cwd)

    def test_validate_file_fails_for_file_too_small(self, tmp_path):
        """Test that validate_file() fails for file < 400 bytes."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import validate_file

            # Create file that's too small (under 400 bytes)
            Path("too_small.md").write_text(
                "# T\n\nA. B.\n"  # Very short content
            )

            with pytest.raises(ValueError, match="outside 400-600 byte range"):
                validate_file("too_small.md")
        finally:
            os.chdir(original_cwd)

    def test_validate_file_fails_for_file_too_large(self, tmp_path):
        """Test that validate_file() fails for file > 600 bytes."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import validate_file

            # Create file that's too large (over 600 bytes) with exactly 2 sentences
            # Use very long sentences to exceed 600 bytes without adding extra periods
            long_sentence1 = "This is a very long prose content that contains detailed information about various topics and concepts without interruption. " * 2
            long_sentence2 = "The second sentence is also quite lengthy and provides additional context and explanation about the subject matter at hand."
            Path("too_large.md").write_text(
                f"# Title\n\n{long_sentence1}{long_sentence2}\n"
            )

            with pytest.raises(ValueError, match="outside 400-600 byte range"):
                validate_file("too_large.md")
        finally:
            os.chdir(original_cwd)

    def test_validate_file_accepts_path_object(self, tmp_path):
        """Test that validate_file() accepts Path objects."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file, validate_file

            file_path = create_file()

            # Should work with Path object
            result = validate_file(file_path)
            assert result is True
        finally:
            os.chdir(original_cwd)

    def test_validate_file_accepts_string_path(self, tmp_path):
        """Test that validate_file() accepts string paths."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file, validate_file

            create_file()

            # Should work with string path
            result = validate_file("test-u9soe6.md")
            assert result is True
        finally:
            os.chdir(original_cwd)


class TestGitOperations:
    """Tests for git operations (add, commit, push)."""

    def test_git_add_function_exists(self):
        """Test that git_add() function exists and is callable."""
        from create_markdown_file import git_add

        # Function should be defined
        assert callable(git_add)

    def test_git_commit_function_exists(self):
        """Test that git_commit() function exists and is callable."""
        from create_markdown_file import git_commit

        # Function should be defined
        assert callable(git_commit)

    def test_git_push_function_exists(self):
        """Test that git_push() function exists and is callable."""
        from create_markdown_file import git_push

        # Function should be defined
        assert callable(git_push)

    def test_git_add_stages_file_in_git(self, tmp_path):
        """Test that git_add() stages the file in git."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Initialize git repo
            import subprocess

            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                check=True,
                capture_output=True,
            )

            # Create and stage file
            from create_markdown_file import create_file, git_add

            create_file()
            git_add()

            # Verify file is staged
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True,
            )

            # Output should show 'A' (added) or 'AM' for staged files
            assert "test-u9soe6.md" in result.stdout
        finally:
            os.chdir(original_cwd)

    def test_git_commit_creates_commit_with_message(self, tmp_path):
        """Test that git_commit() creates a commit with the proper message."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            import subprocess

            # Initialize git repo
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                check=True,
                capture_output=True,
            )

            # Create, stage, and commit file
            from create_markdown_file import (
                COMMIT_MESSAGE,
                create_file,
                git_add,
                git_commit,
            )

            create_file()
            git_add()
            git_commit()

            # Verify commit message
            result = subprocess.run(
                ["git", "log", "--oneline", "-1"],
                capture_output=True,
                text=True,
                check=True,
            )

            # Commit message should match expected format
            assert COMMIT_MESSAGE in result.stdout
        finally:
            os.chdir(original_cwd)

    def test_git_operations_fail_without_git_repo(self, tmp_path):
        """Test that git operations raise CalledProcessError without git repo."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            import subprocess

            from create_markdown_file import create_file, git_add

            create_file()

            # Try git_add without git repo initialized
            with pytest.raises(subprocess.CalledProcessError):
                git_add()
        finally:
            os.chdir(original_cwd)


class TestMainFunction:
    """Tests for main() orchestration function."""

    def test_main_function_exists(self):
        """Test that main() function exists and is callable."""
        from create_markdown_file import main

        assert callable(main)

    def test_main_orchestrates_complete_workflow_with_mock(self, tmp_path):
        """Test that main() orchestrates create, validate, and git operations."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            import subprocess
            from unittest.mock import patch

            from create_markdown_file import main

            # Initialize git repo
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                check=True,
                capture_output=True,
            )

            # Mock git push to avoid needing a real remote
            with patch("create_markdown_file.git_push") as mock_push:
                mock_push.return_value = None

                # Run main - should exit cleanly via sys.exit(0)
                with pytest.raises(SystemExit) as exc_info:
                    main()

                # Exit code should be 0 (success)
                assert exc_info.value.code == 0

                # Verify git_push was called
                mock_push.assert_called_once()
        finally:
            os.chdir(original_cwd)

    def test_main_handles_validation_error(self, tmp_path, capsys):
        """Test that main() handles validation errors gracefully."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from unittest.mock import patch

            from create_markdown_file import main

            # Mock validate_file to raise ValueError
            with patch("create_markdown_file.validate_file") as mock_validate:
                mock_validate.side_effect = ValueError("Test validation error")

                # Run main - should exit with code 1
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 1

                # Check stderr contains error message
                captured = capsys.readouterr()
                assert "Validation failed" in captured.err
        finally:
            os.chdir(original_cwd)

    def test_main_handles_git_error(self, tmp_path, capsys):
        """Test that main() handles git command failures gracefully."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            import subprocess
            from unittest.mock import patch

            from create_markdown_file import main

            # Mock git_add to raise CalledProcessError
            with patch("create_markdown_file.git_add") as mock_git_add:
                error = subprocess.CalledProcessError(1, ["git", "add"])
                mock_git_add.side_effect = error

                # Run main - should exit with code 1
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 1

                # Check stderr contains error message
                captured = capsys.readouterr()
                assert "Git command failed" in captured.err
        finally:
            os.chdir(original_cwd)
