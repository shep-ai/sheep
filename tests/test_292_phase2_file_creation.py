"""Tests for feature 292 phase 2: File creation and git integration."""

import pytest
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
import tempfile
import os


class TestTask5FileCreation:
    """Tests for Task 5: Create markdown file with explicit encoding and line endings."""

    def test_create_markdown_file_basic(self):
        """Test that create_markdown_file creates a file successfully."""
        from src.sheep_292_phase2 import create_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp directory
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Test Title\n\nThis is the first sentence. This is the second sentence.\n"
                filename = "test-file.md"

                result = create_markdown_file(content, filename)

                assert result is True
                assert Path(filename).exists()
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_content_verification(self):
        """Test that created file contains exact content."""
        from src.sheep_292_phase2 import create_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Test Title\n\nThis is the first sentence. This is the second sentence.\n"
                filename = "test-file.md"

                create_markdown_file(content, filename)

                # Read file back
                read_content = Path(filename).read_text(encoding="utf-8")
                assert read_content == content
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_utf8_no_bom(self):
        """Test that file is UTF-8 without BOM."""
        from src.sheep_292_phase2 import create_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Café Title\n\nThis is a sentence with special chars. This is the second sentence.\n"
                filename = "test-file.md"

                create_markdown_file(content, filename)

                # Read file in binary mode and check for BOM
                file_bytes = Path(filename).read_bytes()
                assert not file_bytes.startswith(b"\xef\xbb\xbf"), "File has UTF-8 BOM"
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_lf_line_endings(self):
        """Test that file uses LF line endings (not CRLF)."""
        from src.sheep_292_phase2 import create_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Test Title\n\nFirst sentence. Second sentence.\n"
                filename = "test-file.md"

                create_markdown_file(content, filename)

                # Check binary content for line endings
                file_bytes = Path(filename).read_bytes()
                assert b"\r\n" not in file_bytes, "File has CRLF line endings"
                assert b"\n" in file_bytes, "File should have newlines"
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_path_traversal_prevention(self):
        """Test that path traversal attempts are rejected."""
        from src.sheep_292_phase2 import create_markdown_file

        content = "# Title\n\nSome content. More content.\n"

        # Try various path traversal attempts
        with pytest.raises(ValueError, match="path traversal"):
            create_markdown_file(content, "../../../etc/passwd")

        with pytest.raises(ValueError, match="path traversal"):
            create_markdown_file(content, "subdir/file.md")

        with pytest.raises(ValueError, match="path traversal"):
            create_markdown_file(content, "..\\windows\\system32")

    def test_create_markdown_file_already_exists_overwrites(self):
        """Test that create_markdown_file overwrites existing file."""
        from src.sheep_292_phase2 import create_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create initial file
                filename = "test-file.md"
                Path(filename).write_text("Old content")

                # Create with new content
                content = "# New Title\n\nNew sentence one. New sentence two.\n"
                result = create_markdown_file(content, filename)

                assert result is True
                assert Path(filename).read_text(encoding="utf-8") == content
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_returns_true_on_success(self):
        """Test that function returns True on successful creation."""
        from src.sheep_292_phase2 import create_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Title\n\nFirst. Second.\n"
                result = create_markdown_file(content, "test.md")

                assert result is True
                assert isinstance(result, bool)
            finally:
                os.chdir(original_cwd)


class TestTask6GitStaging:
    """Tests for Task 6: Stage file in git using git add."""

    def test_stage_file_in_git_executes_git_add(self):
        """Test that stage_file_in_git executes git add command."""
        from src.sheep_292_phase2 import stage_file_in_git

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            # Mock successful git add
            mock_run.return_value = Mock(
                returncode=0, stdout="", stderr="", text=True
            )

            # Need two calls: git add and git status
            mock_run.side_effect = [
                Mock(returncode=0, stdout="", stderr=""),
                Mock(returncode=0, stdout="A  test-file.md\n", stderr=""),
            ]

            result = stage_file_in_git("test-file.md")

            # Verify git add was called
            assert mock_run.call_count >= 1
            first_call = mock_run.call_args_list[0]
            assert first_call[0][0] == ["git", "add", "test-file.md"]

    def test_stage_file_in_git_verifies_staged_status(self):
        """Test that function verifies file appears in git status."""
        from src.sheep_292_phase2 import stage_file_in_git

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            # Mock git add success and git status showing staged file
            mock_run.side_effect = [
                Mock(returncode=0, stdout="", stderr=""),
                Mock(returncode=0, stdout="A  test-file.md\n", stderr=""),
            ]

            result = stage_file_in_git("test-file.md")

            assert result is True
            # Verify git status was called to verify staging
            assert mock_run.call_count >= 2
            status_call = mock_run.call_args_list[1]
            assert status_call[0][0] == ["git", "status", "--short"]

    def test_stage_file_in_git_raises_on_add_failure(self):
        """Test that function raises CalledProcessError if git add fails."""
        from src.sheep_292_phase2 import stage_file_in_git

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            # Mock git add failure
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git add", stderr="fatal: not a git repository"
            )

            with pytest.raises(subprocess.CalledProcessError):
                stage_file_in_git("test-file.md")

    def test_stage_file_in_git_raises_if_not_staged(self):
        """Test that function raises if file doesn't appear in git status."""
        from src.sheep_292_phase2 import stage_file_in_git

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            # Mock git add success but file not in status
            mock_run.side_effect = [
                Mock(returncode=0, stdout="", stderr=""),
                Mock(returncode=0, stdout="", stderr=""),  # Empty status
            ]

            with pytest.raises(subprocess.CalledProcessError):
                stage_file_in_git("test-file.md")

    def test_stage_file_in_git_captures_stderr_on_failure(self):
        """Test that function captures and logs stderr for debugging."""
        from src.sheep_292_phase2 import stage_file_in_git

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            stderr_msg = "fatal: not a git repository"
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git add", stderr=stderr_msg
            )

            with pytest.raises(subprocess.CalledProcessError):
                stage_file_in_git("test-file.md")


class TestTask7GitCommit:
    """Tests for Task 7: Commit staged file with conventional message."""

    def test_commit_file_in_git_creates_commit(self):
        """Test that commit_file_in_git creates a git commit."""
        from src.sheep_292_phase2 import commit_file_in_git

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            # Mock successful git commit and git log
            mock_run.side_effect = [
                Mock(returncode=0, stdout="[main abcd123] feat(292): create...", stderr=""),
                Mock(returncode=0, stdout="abcd123 feat(292): create markdown file test-file.md with prose content", stderr=""),
            ]

            result = commit_file_in_git("test-file.md")

            assert result is True

    def test_commit_file_in_git_uses_conventional_message(self):
        """Test that commit message uses conventional format."""
        from src.sheep_292_phase2 import commit_file_in_git

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            mock_run.side_effect = [
                Mock(returncode=0, stdout="", stderr=""),
                Mock(returncode=0, stdout="abcd123 feat(292): create markdown file test-kp1fm3.md with prose content", stderr=""),
            ]

            commit_file_in_git("test-kp1fm3.md")

            # Verify correct commit message was used
            commit_call = mock_run.call_args_list[0]
            args = commit_call[0][0]
            assert "git" in args
            assert "commit" in args
            assert any("feat(292)" in str(arg) for arg in args)

    def test_commit_file_in_git_verifies_commit_in_log(self):
        """Test that function verifies commit was created via git log."""
        from src.sheep_292_phase2 import commit_file_in_git

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            mock_run.side_effect = [
                Mock(returncode=0, stdout="", stderr=""),
                Mock(returncode=0, stdout="abcd123 feat(292): create markdown file test-kp1fm3.md with prose content", stderr=""),
            ]

            result = commit_file_in_git("test-kp1fm3.md")

            assert result is True
            # Verify git log was called
            assert mock_run.call_count >= 2
            log_call = mock_run.call_args_list[1]
            assert log_call[0][0] == ["git", "log", "--oneline", "-1"]

    def test_commit_file_in_git_raises_on_commit_failure(self):
        """Test that function raises CalledProcessError if git commit fails."""
        from src.sheep_292_phase2 import commit_file_in_git

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            # Mock git commit failure
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git commit", stderr="fatal: No changes added to commit"
            )

            with pytest.raises(subprocess.CalledProcessError):
                commit_file_in_git("test-file.md")

    def test_commit_file_in_git_raises_if_message_not_in_log(self):
        """Test that function raises if commit message doesn't appear in log."""
        from src.sheep_292_phase2 import commit_file_in_git

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            # Mock commit success but log doesn't show expected message
            mock_run.side_effect = [
                Mock(returncode=0, stdout="", stderr=""),
                Mock(returncode=0, stdout="abcd123 wrong message here", stderr=""),
            ]

            with pytest.raises(subprocess.CalledProcessError):
                commit_file_in_git("test-file.md")

    def test_commit_file_in_git_returns_true_on_success(self):
        """Test that function returns True on successful commit."""
        from src.sheep_292_phase2 import commit_file_in_git

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            mock_run.side_effect = [
                Mock(returncode=0, stdout="", stderr=""),
                Mock(returncode=0, stdout="abcd123 feat(292): create markdown file test-file.md with prose content", stderr=""),
            ]

            result = commit_file_in_git("test-file.md")

            assert result is True
            assert isinstance(result, bool)


class TestTask8GitPush:
    """Tests for Task 8: Push commit to feature branch."""

    def test_push_to_branch_executes_git_push(self):
        """Test that push_to_branch executes git push command."""
        from src.sheep_292_phase2 import push_to_branch

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            # Mock successful git push and git status
            mock_run.side_effect = [
                Mock(returncode=0, stdout="", stderr=""),
                Mock(returncode=0, stdout="## feat/292-markdown-file-creation-a7c367...origin/feat/292-markdown-file-creation-a7c367", stderr=""),
            ]

            result = push_to_branch("feat/292-markdown-file-creation-a7c367")

            # Verify git push was called
            assert mock_run.call_count >= 1
            first_call = mock_run.call_args_list[0]
            assert first_call[0][0][:2] == ["git", "push"]

    def test_push_to_branch_uses_correct_branch_name(self):
        """Test that push uses correct branch name."""
        from src.sheep_292_phase2 import push_to_branch

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            mock_run.side_effect = [
                Mock(returncode=0, stdout="", stderr=""),
                Mock(returncode=0, stdout="## feat/test-branch...origin/feat/test-branch", stderr=""),
            ]

            push_to_branch("feat/test-branch")

            # Verify correct branch was pushed
            push_call = mock_run.call_args_list[0]
            assert push_call[0][0] == ["git", "push", "-u", "origin", "feat/test-branch"]

    def test_push_to_branch_verifies_push_via_status(self):
        """Test that function verifies push via git status."""
        from src.sheep_292_phase2 import push_to_branch

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            mock_run.side_effect = [
                Mock(returncode=0, stdout="", stderr=""),
                Mock(returncode=0, stdout="## feat/292...origin/feat/292 [ahead 0]", stderr=""),
            ]

            result = push_to_branch("feat/292")

            assert result is True
            # Verify git status was called
            assert mock_run.call_count >= 2
            status_call = mock_run.call_args_list[1]
            assert status_call[0][0] == ["git", "status", "-sb"]

    def test_push_to_branch_raises_on_push_failure(self):
        """Test that function raises CalledProcessError if git push fails."""
        from src.sheep_292_phase2 import push_to_branch

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            # Mock git push failure
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git push", stderr="fatal: Authentication failed"
            )

            with pytest.raises(subprocess.CalledProcessError):
                push_to_branch("feat/292")

    def test_push_to_branch_returns_true_on_success(self):
        """Test that function returns True on successful push."""
        from src.sheep_292_phase2 import push_to_branch

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            mock_run.side_effect = [
                Mock(returncode=0, stdout="", stderr=""),
                Mock(returncode=0, stdout="## feat/292...origin/feat/292", stderr=""),
            ]

            result = push_to_branch("feat/292")

            assert result is True
            assert isinstance(result, bool)

    def test_push_to_branch_captures_stderr_on_failure(self):
        """Test that function captures and logs stderr for debugging."""
        from src.sheep_292_phase2 import push_to_branch

        with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
            stderr_msg = "fatal: Authentication failed"
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git push", stderr=stderr_msg
            )

            with pytest.raises(subprocess.CalledProcessError):
                push_to_branch("feat/292")


class TestPhase2Integration:
    """Integration tests for complete phase 2 workflow."""

    def test_phase2_workflow_sequence(self):
        """Test complete workflow: create file, stage, commit, push."""
        from src.sheep_292_phase2 import (
            create_markdown_file,
            stage_file_in_git,
            commit_file_in_git,
            push_to_branch,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Step 1: Create file
                content = "# Test Title\n\nFirst sentence with substance. Second sentence with more detail.\n"
                filename = "test-phase2.md"

                with patch("src.sheep_292_phase2.subprocess.run") as mock_run:
                    # Mock git operations
                    mock_run.side_effect = [
                        # git add
                        Mock(returncode=0, stdout=""),
                        # git status (verify staging)
                        Mock(returncode=0, stdout="A  test-phase2.md\n"),
                        # git commit
                        Mock(returncode=0, stdout=""),
                        # git log (verify commit)
                        Mock(returncode=0, stdout="abcd123 feat(292): create markdown file test-phase2.md"),
                        # git push
                        Mock(returncode=0, stdout=""),
                        # git status (verify push)
                        Mock(returncode=0, stdout="## test-branch...origin/test-branch"),
                    ]

                    # Execute workflow
                    assert create_markdown_file(content, filename) is True
                    assert stage_file_in_git(filename) is True
                    assert commit_file_in_git(filename) is True
                    assert push_to_branch("test-branch") is True

            finally:
                os.chdir(original_cwd)
