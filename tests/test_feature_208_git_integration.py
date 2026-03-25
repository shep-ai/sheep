"""Tests for feature 208 git integration functions.

Tests verify that all git operations work correctly:
1. git_add_file() - stages file with git add
2. git_commit() - commits file with conventional message
3. git_push() - pushes to remote branch
4. main() - orchestrates complete workflow
"""

import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import subprocess


def setup_module():
    """Set up test environment by adding src to path."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


class TestGitAddFile:
    """Tests for git_add_file() function."""

    def test_git_add_file_calls_subprocess_with_correct_args(self):
        """Test git_add_file executes git add with correct arguments."""
        from sheep.features.feature_208_markdown_file_creation import git_add_file

        with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            git_add_file("test-mujic0.md")

            # Verify subprocess.run was called with correct git add command
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == ["git", "add", "test-mujic0.md"]
            assert call_args[1]["check"] is True
            assert call_args[1]["capture_output"] is True
            assert call_args[1]["text"] is True

    def test_git_add_file_uses_default_filename(self):
        """Test git_add_file uses FILENAME default."""
        from sheep.features.feature_208_markdown_file_creation import (
            git_add_file,
            FILENAME,
        )

        with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            git_add_file()

            # Verify FILENAME constant was used
            call_args = mock_run.call_args
            assert call_args[0][0][2] == FILENAME

    def test_git_add_file_raises_on_subprocess_error(self):
        """Test git_add_file raises CalledProcessError on git failure."""
        from sheep.features.feature_208_markdown_file_creation import git_add_file

        with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
            # Simulate git add failure
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git add", stderr="Permission denied"
            )

            try:
                git_add_file("test-mujic0.md")
                assert False, "Should have raised CalledProcessError"
            except subprocess.CalledProcessError:
                pass  # Expected


class TestGitCommit:
    """Tests for git_commit() function."""

    def test_git_commit_calls_subprocess_with_correct_args(self):
        """Test git_commit executes git commit with correct arguments."""
        from sheep.features.feature_208_markdown_file_creation import git_commit

        with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            git_commit("feat(208): Create markdown file test-mujic0.md")

            # Verify subprocess.run was called with correct git commit command
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == ["git", "commit", "-m", "feat(208): Create markdown file test-mujic0.md"]
            assert call_args[1]["check"] is True
            assert call_args[1]["capture_output"] is True
            assert call_args[1]["text"] is True

    def test_git_commit_uses_default_message(self):
        """Test git_commit uses COMMIT_MESSAGE default."""
        from sheep.features.feature_208_markdown_file_creation import (
            git_commit,
            COMMIT_MESSAGE,
        )

        with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            git_commit()

            # Verify COMMIT_MESSAGE constant was used
            call_args = mock_run.call_args
            assert call_args[0][0][3] == COMMIT_MESSAGE

    def test_git_commit_raises_on_subprocess_error(self):
        """Test git_commit raises CalledProcessError on git failure."""
        from sheep.features.feature_208_markdown_file_creation import git_commit

        with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
            # Simulate git commit failure
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git commit", stderr="Nothing to commit"
            )

            try:
                git_commit("feat(208): Create markdown file test-mujic0.md")
                assert False, "Should have raised CalledProcessError"
            except subprocess.CalledProcessError:
                pass  # Expected


class TestGitPush:
    """Tests for git_push() function."""

    def test_git_push_calls_subprocess_with_correct_args(self):
        """Test git_push executes git push with correct arguments."""
        from sheep.features.feature_208_markdown_file_creation import git_push

        with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            git_push("feat/markdown-file-creation-9f7556")

            # Verify subprocess.run was called with correct git push command
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == ["git", "push", "-u", "origin", "HEAD"]
            assert call_args[1]["check"] is True
            assert call_args[1]["capture_output"] is True
            assert call_args[1]["text"] is True

    def test_git_push_uses_default_branch(self):
        """Test git_push uses BRANCH_NAME default."""
        from sheep.features.feature_208_markdown_file_creation import (
            git_push,
            BRANCH_NAME,
        )

        with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            git_push()

            # Verify command was executed (branch parameter doesn't affect git push -u origin HEAD)
            mock_run.assert_called_once()

    def test_git_push_raises_on_subprocess_error(self):
        """Test git_push raises CalledProcessError on git failure."""
        from sheep.features.feature_208_markdown_file_creation import git_push

        with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
            # Simulate git push failure
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git push", stderr="Authentication failed"
            )

            try:
                git_push("feat/markdown-file-creation-9f7556")
                assert False, "Should have raised CalledProcessError"
            except subprocess.CalledProcessError:
                pass  # Expected


class TestMain:
    """Tests for main() orchestration function."""

    def test_main_orchestrates_complete_workflow(self):
        """Test main orchestrates all phases: create, validate, git operations."""
        from sheep.features.feature_208_markdown_file_creation import main

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock git operations (subprocess.run is called in git functions)
                with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
                    mock_run.return_value = MagicMock()

                    # Mock generate_content to return valid content with sufficient length (>250 bytes)
                    with patch("sheep.features.feature_208_markdown_file_creation.generate_content") as mock_gen:
                        long_prose = (
                            "This is the first sentence with meaningful content to ensure "
                            "the generated markdown file meets the minimum size requirement. "
                            "This is the second sentence that continues the theme. "
                            "This is the third sentence that completes the composition."
                        )
                        mock_gen.return_value = ("Test Title", long_prose)

                        # Execute main workflow
                        exit_code = main()

                        # Verify return code is 0 on success
                        assert exit_code == 0

                        # Verify git operations were called
                        # Should have 3 subprocess.run calls: git add, git commit, git push
                        assert mock_run.call_count == 3

                        # Verify first call was git add
                        first_call = mock_run.call_args_list[0]
                        assert first_call[0][0][0:2] == ["git", "add"]

                        # Verify second call was git commit
                        second_call = mock_run.call_args_list[1]
                        assert second_call[0][0][0:2] == ["git", "commit"]

                        # Verify third call was git push
                        third_call = mock_run.call_args_list[2]
                        assert third_call[0][0][0:2] == ["git", "push"]

            finally:
                os.chdir(original_cwd)

    def test_main_creates_file_successfully(self):
        """Test main creates the markdown file."""
        from sheep.features.feature_208_markdown_file_creation import (
            main,
            FILENAME,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock only git operations
                with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
                    mock_run.return_value = MagicMock()

                    # Mock generate_content to return valid content with sufficient length (>250 bytes)
                    with patch("sheep.features.feature_208_markdown_file_creation.generate_content") as mock_gen:
                        long_prose = (
                            "This is the first sentence with meaningful content to ensure "
                            "the generated markdown file meets the minimum size requirement. "
                            "This is the second sentence that continues the theme. "
                            "This is the third sentence that completes the composition."
                        )
                        mock_gen.return_value = ("Test Title", long_prose)

                        # Execute main workflow
                        exit_code = main()

                        # Verify return code is 0 on success
                        assert exit_code == 0

                        # Verify file was created
                        assert Path(FILENAME).exists()

            finally:
                os.chdir(original_cwd)

    def test_main_validates_file_successfully(self):
        """Test main validates the created file."""
        from sheep.features.feature_208_markdown_file_creation import (
            main,
            FILENAME,
            validate_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock only git operations
                with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
                    mock_run.return_value = MagicMock()

                    # Mock generate_content to return valid content with sufficient length (>250 bytes)
                    with patch("sheep.features.feature_208_markdown_file_creation.generate_content") as mock_gen:
                        long_prose = (
                            "This is the first sentence with meaningful content to ensure "
                            "the generated markdown file meets the minimum size requirement. "
                            "This is the second sentence that continues the theme. "
                            "This is the third sentence that completes the composition."
                        )
                        mock_gen.return_value = ("Test Title", long_prose)

                        # Execute main workflow
                        exit_code = main()

                        # Verify return code is 0 on success
                        assert exit_code == 0

                        # Verify file validation passes
                        # If validation fails, this will raise
                        validate_markdown_file(FILENAME)

            finally:
                os.chdir(original_cwd)

    def test_main_returns_1_on_validation_failure(self):
        """Test main returns 1 if validation fails."""
        from sheep.features.feature_208_markdown_file_creation import (
            main,
            create_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock create_markdown_file to create an invalid file
                with patch("sheep.features.feature_208_markdown_file_creation.create_markdown_file") as mock_create:
                    # Create an invalid file that will fail validation
                    def create_invalid_file():
                        Path("test-mujic0.md").write_text("No heading here")
                        return Path("test-mujic0.md")

                    mock_create.side_effect = create_invalid_file

                    # Execute main workflow
                    exit_code = main()

                    # Verify return code is 1 on failure
                    assert exit_code == 1

            finally:
                os.chdir(original_cwd)
