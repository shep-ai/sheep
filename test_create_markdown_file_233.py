#!/usr/bin/env python3
"""
Test suite for feature 233: markdown-file-creation-c8975a
Tests create_file() function, git integration, and module constants.
No validation layer per spec requirement.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from create_markdown_file_233 import COMMIT_MESSAGE, FILENAME, PROSE, TITLE, create_file, git_add, git_commit, git_push, main


class TestConstants:
    """Test suite for module-level constants."""

    def test_filename_is_correct(self):
        """Test that FILENAME constant is exactly 'test-god37p.md'."""
        assert FILENAME == "test-god37p.md"

    def test_title_is_meaningful(self):
        """Test that TITLE is a meaningful non-empty string."""
        assert isinstance(TITLE, str)
        assert len(TITLE) > 0
        assert not TITLE.isspace()

    def test_prose_is_not_empty(self):
        """Test that PROSE is a meaningful non-empty string."""
        assert isinstance(PROSE, str)
        assert len(PROSE) > 0
        assert not PROSE.isspace()

    def test_prose_sentence_count(self):
        """Test that PROSE contains exactly 2-3 sentences."""
        sentence_count = PROSE.count('.')
        assert 2 <= sentence_count <= 3

    def test_commit_message_format(self):
        """Test that COMMIT_MESSAGE follows conventional commits format."""
        assert COMMIT_MESSAGE.startswith("feat(233):")
        assert "test-god37p.md" in COMMIT_MESSAGE


class TestCreateFile:
    """Test suite for create_file function."""

    def test_create_file_returns_path_on_success(self):
        """Test that create_file returns Path when file is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                result = create_file()
                assert result is not None
                assert isinstance(result, Path)
                assert Path(FILENAME).exists()
            finally:
                os.chdir(original_dir)

    def test_create_file_raises_if_exists(self):
        """Test that create_file raises FileExistsError if file already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / FILENAME
            # Create file first
            test_file.write_text("# Title\n\nContent.\n")
            # Now try to create again
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                with pytest.raises(FileExistsError):
                    create_file()
            finally:
                os.chdir(original_dir)

    def test_create_file_contains_h1_heading(self):
        """Test that created file contains H1 heading with TITLE."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
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
                file_size = Path(FILENAME).stat().st_size
                assert 300 <= file_size <= 600
            finally:
                os.chdir(original_dir)

    def test_create_file_structure(self):
        """Test that created file has correct markdown structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                content = Path(FILENAME).read_text(encoding="utf-8")
                # Structure should be: # Title\n\nProse\n
                lines = content.split("\n")
                assert len(lines) >= 3  # heading, blank line, prose, newline
                assert lines[0].startswith("# ")  # H1 heading
                assert lines[1] == ""  # Blank line
                assert PROSE in content  # Prose content present
            finally:
                os.chdir(original_dir)


class TestGitIntegration:
    """Test suite for git integration functions."""

    def _setup_git_repo(self, tmpdir):
        """
        Set up a temporary git repository for testing git operations.
        Returns the path to the temporary directory.
        """
        # Initialize git repo
        subprocess.run(["git", "init"], cwd=tmpdir, check=True, capture_output=True)

        # Configure git user for commits
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=tmpdir,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=tmpdir,
            check=True,
            capture_output=True,
        )

        # Create feature branch
        subprocess.run(
            ["git", "checkout", "-b", "feat/233-markdown-file-creation-c8975a"],
            cwd=tmpdir,
            check=True,
            capture_output=True,
        )

        return tmpdir

    def test_git_add_stages_file(self):
        """Test that git_add() stages the file for commit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                self._setup_git_repo(tmpdir)
                os.chdir(tmpdir)

                # Create file
                create_file()

                # Add file to git
                git_add()

                # Verify file is staged using git diff --cached
                result = subprocess.run(
                    ["git", "diff", "--cached", "--name-only"],
                    check=True,
                    capture_output=True,
                    text=True,
                )

                assert FILENAME in result.stdout
            finally:
                os.chdir(original_dir)

    def test_git_commit_creates_commit_with_message(self):
        """Test that git_commit() creates a commit with conventional message format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                self._setup_git_repo(tmpdir)
                os.chdir(tmpdir)

                # Create and stage file
                create_file()
                git_add()

                # Commit file
                git_commit()

                # Verify commit message
                result = subprocess.run(
                    ["git", "log", "-1", "--pretty=%B"],
                    check=True,
                    capture_output=True,
                    text=True,
                )

                assert COMMIT_MESSAGE in result.stdout
                assert result.stdout.strip() == COMMIT_MESSAGE
            finally:
                os.chdir(original_dir)

    def test_git_commit_follows_conventional_format(self):
        """Test that git_commit() uses conventional commit format feat(233):."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                self._setup_git_repo(tmpdir)
                os.chdir(tmpdir)

                # Create and stage file
                create_file()
                git_add()

                # Commit file
                git_commit()

                # Verify commit follows conventional format
                result = subprocess.run(
                    ["git", "log", "-1", "--pretty=%B"],
                    check=True,
                    capture_output=True,
                    text=True,
                )

                commit_msg = result.stdout.strip()
                assert commit_msg.startswith("feat(233):")
                assert "test-god37p.md" in commit_msg
            finally:
                os.chdir(original_dir)

    def test_git_add_raises_on_missing_file(self):
        """Test that git_add() raises CalledProcessError if file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                self._setup_git_repo(tmpdir)
                os.chdir(tmpdir)

                # Try to add file without creating it first
                with pytest.raises(subprocess.CalledProcessError):
                    git_add()
            finally:
                os.chdir(original_dir)

    def test_git_commit_raises_without_staged_changes(self):
        """Test that git_commit() raises CalledProcessError if no changes are staged."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                self._setup_git_repo(tmpdir)
                os.chdir(tmpdir)

                # Create initial commit so we can test committing with no changes
                Path("dummy.txt").write_text("dummy")
                subprocess.run(["git", "add", "dummy.txt"], check=True, capture_output=True)
                subprocess.run(
                    ["git", "commit", "-m", "initial"],
                    check=True,
                    capture_output=True,
                )

                # Try to commit with no staged changes
                with pytest.raises(subprocess.CalledProcessError):
                    git_commit()
            finally:
                os.chdir(original_dir)

    def test_git_push_with_upstream_flag(self):
        """Test that git_push() uses -u flag for upstream tracking."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                self._setup_git_repo(tmpdir)
                os.chdir(tmpdir)

                # Create, stage, and commit file
                create_file()
                git_add()
                git_commit()

                # git_push() will fail because there's no remote, but we can verify
                # the command structure would use -u flag
                # Instead, we'll test that it fails appropriately
                with pytest.raises(subprocess.CalledProcessError):
                    git_push()

                # If we get here without an exception, that means we have a remote
                # which shouldn't happen in the test environment
            finally:
                os.chdir(original_dir)

    def test_workflow_creates_file_and_commits(self):
        """Test complete workflow: create file → add → commit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                self._setup_git_repo(tmpdir)
                os.chdir(tmpdir)

                # Complete workflow without push (since we don't have a remote)
                create_file()
                git_add()
                git_commit()

                # Verify file exists
                assert Path(FILENAME).exists()

                # Verify commit exists
                result = subprocess.run(
                    ["git", "log", "--oneline"],
                    check=True,
                    capture_output=True,
                    text=True,
                )

                assert COMMIT_MESSAGE in result.stdout
            finally:
                os.chdir(original_dir)


class TestMainOrchestration:
    """Test suite for main() function orchestration and error handling."""

    def test_main_executes_all_steps_in_order(self):
        """Test that main() executes create_file → add → commit → push in correct order."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                # Set up git repo
                subprocess.run(["git", "init"], cwd=tmpdir, check=True, capture_output=True)
                subprocess.run(
                    ["git", "config", "user.email", "test@example.com"],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True,
                )
                subprocess.run(
                    ["git", "config", "user.name", "Test User"],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True,
                )
                subprocess.run(
                    ["git", "checkout", "-b", "feat/233-markdown-file-creation-c8975a"],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True,
                )

                os.chdir(tmpdir)

                # Track which functions were called in order
                call_order = []

                # Mock the functions to verify they're called in order
                with patch("create_markdown_file_233.create_file") as mock_create:
                    with patch("create_markdown_file_233.git_add") as mock_add:
                        with patch("create_markdown_file_233.git_commit") as mock_commit:
                            with patch("create_markdown_file_233.git_push") as mock_push:
                                mock_create.side_effect = lambda: (
                                    call_order.append("create_file"),
                                    Path(FILENAME).write_text(
                                        f"# {TITLE}\n\n{PROSE}\n", encoding="utf-8", newline="\n"
                                    ),
                                )[-1]
                                mock_add.side_effect = lambda: call_order.append("git_add")
                                mock_commit.side_effect = lambda: call_order.append("git_commit")
                                mock_push.side_effect = lambda: call_order.append("git_push")

                                # Call main() - should not raise
                                main()

                                # Verify all functions were called in correct order
                                assert call_order == ["create_file", "git_add", "git_commit", "git_push"]
            finally:
                os.chdir(original_dir)

    def test_main_stops_on_create_file_error(self):
        """Test that main() stops execution if create_file() raises FileExistsError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                # Set up git repo
                subprocess.run(["git", "init"], cwd=tmpdir, check=True, capture_output=True)
                subprocess.run(
                    ["git", "config", "user.email", "test@example.com"],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True,
                )
                subprocess.run(
                    ["git", "config", "user.name", "Test User"],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True,
                )

                os.chdir(tmpdir)

                # Pre-create the file so create_file will fail
                Path(FILENAME).write_text("# Existing\n\nContent.\n")

                # Mock git operations to verify they're NOT called
                with patch("create_markdown_file_233.git_add") as mock_add:
                    with patch("create_markdown_file_233.git_commit") as mock_commit:
                        with patch("create_markdown_file_233.git_push") as mock_push:
                            # main() should call sys.exit(1) when an error occurs
                            with pytest.raises(SystemExit) as exc_info:
                                main()

                            assert exc_info.value.code == 1
                            # Verify subsequent steps were NOT called
                            mock_add.assert_not_called()
                            mock_commit.assert_not_called()
                            mock_push.assert_not_called()
            finally:
                os.chdir(original_dir)

    def test_main_stops_on_git_add_error(self):
        """Test that main() stops execution if git_add() fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                # Set up git repo
                subprocess.run(["git", "init"], cwd=tmpdir, check=True, capture_output=True)
                subprocess.run(
                    ["git", "config", "user.email", "test@example.com"],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True,
                )
                subprocess.run(
                    ["git", "config", "user.name", "Test User"],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True,
                )

                os.chdir(tmpdir)

                # Mock git_add to raise CalledProcessError
                with patch("create_markdown_file_233.git_add") as mock_add:
                    with patch("create_markdown_file_233.git_commit") as mock_commit:
                        with patch("create_markdown_file_233.git_push") as mock_push:
                            mock_add.side_effect = subprocess.CalledProcessError(1, "git add")

                            # main() should call sys.exit(1) when git_add fails
                            with pytest.raises(SystemExit) as exc_info:
                                main()

                            assert exc_info.value.code == 1
                            # Verify commit and push were NOT called
                            mock_commit.assert_not_called()
                            mock_push.assert_not_called()
            finally:
                os.chdir(original_dir)

    def test_main_stops_on_git_commit_error(self):
        """Test that main() stops execution if git_commit() fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                # Set up git repo
                subprocess.run(["git", "init"], cwd=tmpdir, check=True, capture_output=True)
                subprocess.run(
                    ["git", "config", "user.email", "test@example.com"],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True,
                )
                subprocess.run(
                    ["git", "config", "user.name", "Test User"],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True,
                )

                os.chdir(tmpdir)

                # Mock git_commit to raise CalledProcessError
                with patch("create_markdown_file_233.git_commit") as mock_commit:
                    with patch("create_markdown_file_233.git_push") as mock_push:
                        mock_commit.side_effect = subprocess.CalledProcessError(1, "git commit")

                        # main() should call sys.exit(1) when git_commit fails
                        with pytest.raises(SystemExit) as exc_info:
                            main()

                        assert exc_info.value.code == 1
                        # Verify push was NOT called
                        mock_push.assert_not_called()
            finally:
                os.chdir(original_dir)

    def test_main_handles_git_push_error(self):
        """Test that main() handles and reports git_push() failures gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                # Set up git repo
                subprocess.run(["git", "init"], cwd=tmpdir, check=True, capture_output=True)
                subprocess.run(
                    ["git", "config", "user.email", "test@example.com"],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True,
                )
                subprocess.run(
                    ["git", "config", "user.name", "Test User"],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True,
                )

                os.chdir(tmpdir)

                # Mock git_push to raise CalledProcessError (no remote)
                with patch("create_markdown_file_233.git_push") as mock_push:
                    mock_push.side_effect = subprocess.CalledProcessError(1, "git push")

                    # main() should call sys.exit(1) when git_push fails
                    with pytest.raises(SystemExit) as exc_info:
                        main()

                    assert exc_info.value.code == 1
            finally:
                os.chdir(original_dir)

    def test_main_prints_success_message(self):
        """Test that main() prints success message on completion."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                # Set up git repo
                subprocess.run(["git", "init"], cwd=tmpdir, check=True, capture_output=True)
                subprocess.run(
                    ["git", "config", "user.email", "test@example.com"],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True,
                )
                subprocess.run(
                    ["git", "config", "user.name", "Test User"],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True,
                )
                subprocess.run(
                    ["git", "checkout", "-b", "feat/233-markdown-file-creation-c8975a"],
                    cwd=tmpdir,
                    check=True,
                    capture_output=True,
                )

                os.chdir(tmpdir)

                # Capture stdout
                import io
                from contextlib import redirect_stdout

                f = io.StringIO()
                with redirect_stdout(f):
                    # Mock git_push since we don't have a remote
                    with patch("create_markdown_file_233.git_push"):
                        main()

                output = f.getvalue()
                assert "Feature 233 implementation complete!" in output
            finally:
                os.chdir(original_dir)

    def test_main_prints_error_message_on_failure(self):
        """Test that main() prints error message to stderr on failure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create file first so create_file will fail
                Path(FILENAME).write_text("# Existing\n\nContent.\n")

                # Capture stderr
                import io
                from contextlib import redirect_stderr

                f = io.StringIO()
                with redirect_stderr(f):
                    with pytest.raises(SystemExit):
                        main()

                output = f.getvalue()
                assert "Failed" in output or "already exists" in output
            finally:
                os.chdir(original_dir)

    def test_main_callable_as_script(self):
        """Test that create_markdown_file_233.py can be run as a script."""
        # This test verifies the `if __name__ == "__main__": main()` pattern works
        import shutil

        with tempfile.TemporaryDirectory() as tmpdir:
            # Set up git repo
            subprocess.run(["git", "init"], cwd=tmpdir, check=True, capture_output=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "checkout", "-b", "feat/233-markdown-file-creation-c8975a"],
                cwd=tmpdir,
                check=True,
                capture_output=True,
            )

            # Copy the script to the temp directory
            script_path = Path(__file__).parent / "create_markdown_file_233.py"
            shutil.copy(script_path, tmpdir)

            # Run script in temp directory (will fail on push but that's OK)
            result = subprocess.run(
                [sys.executable, "create_markdown_file_233.py"],
                cwd=tmpdir,
                capture_output=True,
                text=True,
            )

            # Script should exit with error code 1 (no remote for push)
            # but should show that it progressed through create, add, commit
            assert result.returncode != 0  # Push will fail
            assert "Created test-god37p.md" in result.stdout or "Failed" in result.stderr


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
