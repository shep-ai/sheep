#!/usr/bin/env python3
"""
Test suite for feature 204 phase 3: Git Integration & End-to-End Testing

Tests the git integration functions and main orchestration:
- git_add_file(): Stages file using git add
- git_commit(): Creates conventional commit
- git_push(): Pushes to feature branch
- main(): Orchestrates complete workflow
- End-to-end integration testing
"""

import pytest
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock, call
import sys

# Add src to path to import the feature module
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.features.feature_204_markdown_file_creation import (
    git_add_file,
    git_commit,
    git_push,
    create_markdown_file,
    validate_markdown_file,
    main,
    FILENAME,
    BRANCH_NAME,
    COMMIT_MESSAGE,
)


class TestGitAddFile:
    """Test suite for git_add_file function.

    Tests git add operation using mocked subprocess.
    """

    @patch("sheep.features.feature_204_markdown_file_creation.subprocess.run")
    def test_git_add_file_calls_git_add(self, mock_run):
        """Test that git_add_file calls subprocess with correct git add command."""
        mock_run.return_value = MagicMock(returncode=0)

        git_add_file("test.md")

        # Verify subprocess.run was called with git add command
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert args[0] == ["git", "add", "test.md"]
        assert kwargs.get("check") is True

    @patch("sheep.features.feature_204_markdown_file_creation.subprocess.run")
    def test_git_add_file_captures_output(self, mock_run):
        """Test that git_add_file captures stdout and stderr."""
        mock_run.return_value = MagicMock(returncode=0)

        git_add_file("test.md")

        args, kwargs = mock_run.call_args
        assert kwargs.get("capture_output") is True
        assert kwargs.get("text") is True

    @patch("sheep.features.feature_204_markdown_file_creation.subprocess.run")
    def test_git_add_file_raises_on_failure(self, mock_run):
        """Test that git_add_file raises CalledProcessError if git add fails."""
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "add", "test.md"], output="error"
        )

        with pytest.raises(subprocess.CalledProcessError):
            git_add_file("test.md")

    @patch("sheep.features.feature_204_markdown_file_creation.subprocess.run")
    def test_git_add_file_uses_default_filename(self, mock_run):
        """Test that git_add_file uses FILENAME constant when no argument provided."""
        mock_run.return_value = MagicMock(returncode=0)

        git_add_file()

        args, kwargs = mock_run.call_args
        assert args[0] == ["git", "add", FILENAME]


class TestGitCommit:
    """Test suite for git_commit function.

    Tests git commit operation using mocked subprocess.
    """

    @patch("sheep.features.feature_204_markdown_file_creation.subprocess.run")
    def test_git_commit_calls_git_commit(self, mock_run):
        """Test that git_commit calls subprocess with correct git commit command."""
        mock_run.return_value = MagicMock(returncode=0)

        git_commit("test.md", "feat: test commit")

        # Verify subprocess.run was called with git commit command
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert args[0] == ["git", "commit", "-m", "feat: test commit"]
        assert kwargs.get("check") is True

    @patch("sheep.features.feature_204_markdown_file_creation.subprocess.run")
    def test_git_commit_captures_output(self, mock_run):
        """Test that git_commit captures stdout and stderr."""
        mock_run.return_value = MagicMock(returncode=0)

        git_commit("test.md", "feat: test commit")

        args, kwargs = mock_run.call_args
        assert kwargs.get("capture_output") is True
        assert kwargs.get("text") is True

    @patch("sheep.features.feature_204_markdown_file_creation.subprocess.run")
    def test_git_commit_raises_on_failure(self, mock_run):
        """Test that git_commit raises CalledProcessError if git commit fails."""
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "commit", "-m", "test"], output="error"
        )

        with pytest.raises(subprocess.CalledProcessError):
            git_commit("test.md", "feat: test commit")

    @patch("sheep.features.feature_204_markdown_file_creation.subprocess.run")
    def test_git_commit_uses_default_message(self, mock_run):
        """Test that git_commit uses COMMIT_MESSAGE constant when no message provided."""
        mock_run.return_value = MagicMock(returncode=0)

        git_commit()

        args, kwargs = mock_run.call_args
        assert COMMIT_MESSAGE in args[0]


class TestGitPush:
    """Test suite for git_push function.

    Tests git push operation using mocked subprocess.
    """

    @patch("sheep.features.feature_204_markdown_file_creation.subprocess.run")
    def test_git_push_calls_git_push(self, mock_run):
        """Test that git_push calls subprocess with correct git push command."""
        mock_run.return_value = MagicMock(returncode=0)

        git_push("feat/test-branch")

        # Verify subprocess.run was called with git push command
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert args[0] == ["git", "push", "-u", "origin", "feat/test-branch"]
        assert kwargs.get("check") is True

    @patch("sheep.features.feature_204_markdown_file_creation.subprocess.run")
    def test_git_push_uses_upstream_flag(self, mock_run):
        """Test that git_push uses -u flag for upstream tracking."""
        mock_run.return_value = MagicMock(returncode=0)

        git_push("feat/test-branch")

        args, kwargs = mock_run.call_args
        assert "-u" in args[0]

    @patch("sheep.features.feature_204_markdown_file_creation.subprocess.run")
    def test_git_push_captures_output(self, mock_run):
        """Test that git_push captures stdout and stderr."""
        mock_run.return_value = MagicMock(returncode=0)

        git_push("feat/test-branch")

        args, kwargs = mock_run.call_args
        assert kwargs.get("capture_output") is True
        assert kwargs.get("text") is True

    @patch("sheep.features.feature_204_markdown_file_creation.subprocess.run")
    def test_git_push_raises_on_failure(self, mock_run):
        """Test that git_push raises CalledProcessError if git push fails."""
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["git", "push", "-u", "origin", "feat/test"], output="error"
        )

        with pytest.raises(subprocess.CalledProcessError):
            git_push("feat/test")

    @patch("sheep.features.feature_204_markdown_file_creation.subprocess.run")
    def test_git_push_uses_default_branch(self, mock_run):
        """Test that git_push uses BRANCH_NAME constant when no branch provided."""
        mock_run.return_value = MagicMock(returncode=0)

        git_push()

        args, kwargs = mock_run.call_args
        assert BRANCH_NAME in args[0]


class TestMainOrchestration:
    """Test suite for main orchestration function.

    Tests the complete workflow orchestration with mocked dependencies.
    """

    @patch("sheep.features.feature_204_markdown_file_creation.git_push")
    @patch("sheep.features.feature_204_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_204_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_204_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_204_markdown_file_creation.create_markdown_file")
    def test_main_calls_functions_in_sequence(
        self,
        mock_create,
        mock_validate,
        mock_add,
        mock_commit,
        mock_push,
    ):
        """Test that main() calls functions in correct sequence."""
        mock_create.return_value = "/path/to/file.md"

        main()

        # Verify functions were called
        mock_create.assert_called_once()
        mock_validate.assert_called_once()
        mock_add.assert_called_once()
        mock_commit.assert_called_once()
        mock_push.assert_called_once()

    @patch("sheep.features.feature_204_markdown_file_creation.git_push")
    @patch("sheep.features.feature_204_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_204_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_204_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_204_markdown_file_creation.create_markdown_file")
    def test_main_handles_file_exists_error(
        self,
        mock_create,
        mock_validate,
        mock_add,
        mock_commit,
        mock_push,
    ):
        """Test that main() handles FileExistsError gracefully."""
        mock_create.side_effect = FileExistsError("File already exists")

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    @patch("sheep.features.feature_204_markdown_file_creation.git_push")
    @patch("sheep.features.feature_204_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_204_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_204_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_204_markdown_file_creation.create_markdown_file")
    def test_main_handles_validation_error(
        self,
        mock_create,
        mock_validate,
        mock_add,
        mock_commit,
        mock_push,
    ):
        """Test that main() handles validation errors gracefully."""
        mock_create.return_value = "/path/to/file.md"
        mock_validate.side_effect = ValueError("Invalid markdown format")

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    @patch("sheep.features.feature_204_markdown_file_creation.git_push")
    @patch("sheep.features.feature_204_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_204_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_204_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_204_markdown_file_creation.create_markdown_file")
    def test_main_handles_git_add_error(
        self,
        mock_create,
        mock_validate,
        mock_add,
        mock_commit,
        mock_push,
    ):
        """Test that main() handles git add errors gracefully."""
        mock_create.return_value = "/path/to/file.md"
        mock_add.side_effect = subprocess.CalledProcessError(1, ["git", "add"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    @patch("sheep.features.feature_204_markdown_file_creation.git_push")
    @patch("sheep.features.feature_204_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_204_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_204_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_204_markdown_file_creation.create_markdown_file")
    def test_main_handles_git_commit_error(
        self,
        mock_create,
        mock_validate,
        mock_add,
        mock_commit,
        mock_push,
    ):
        """Test that main() handles git commit errors gracefully."""
        mock_create.return_value = "/path/to/file.md"
        mock_commit.side_effect = subprocess.CalledProcessError(1, ["git", "commit"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    @patch("sheep.features.feature_204_markdown_file_creation.git_push")
    @patch("sheep.features.feature_204_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_204_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_204_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_204_markdown_file_creation.create_markdown_file")
    def test_main_handles_git_push_error(
        self,
        mock_create,
        mock_validate,
        mock_add,
        mock_commit,
        mock_push,
    ):
        """Test that main() handles git push errors gracefully."""
        mock_create.return_value = "/path/to/file.md"
        mock_push.side_effect = subprocess.CalledProcessError(1, ["git", "push"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    @patch("sheep.features.feature_204_markdown_file_creation.git_push")
    @patch("sheep.features.feature_204_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_204_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_204_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_204_markdown_file_creation.create_markdown_file")
    def test_main_handles_oserror(
        self,
        mock_create,
        mock_validate,
        mock_add,
        mock_commit,
        mock_push,
    ):
        """Test that main() handles OSError gracefully."""
        mock_create.side_effect = OSError("File write failed")

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    @patch("sheep.features.feature_204_markdown_file_creation.git_push")
    @patch("sheep.features.feature_204_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_204_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_204_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_204_markdown_file_creation.create_markdown_file")
    def test_main_handles_unexpected_error(
        self,
        mock_create,
        mock_validate,
        mock_add,
        mock_commit,
        mock_push,
    ):
        """Test that main() handles unexpected errors gracefully."""
        mock_create.side_effect = RuntimeError("Unexpected error")

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1


class TestEndToEndIntegration:
    """End-to-end integration tests with real file operations.

    Tests the complete workflow with actual file creation and validation.
    """

    def test_complete_workflow_creates_valid_file(self):
        """Test that complete workflow creates a valid markdown file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp directory
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Mock only the git operations to avoid real git calls
                with patch("sheep.features.feature_204_markdown_file_creation.git_add_file"):
                    with patch("sheep.features.feature_204_markdown_file_creation.git_commit"):
                        with patch("sheep.features.feature_204_markdown_file_creation.git_push"):
                            with patch("sheep.features.feature_204_markdown_file_creation.create_llm") as mock_llm_factory:
                                # Mock LLM responses with content that meets size requirements (250-600 bytes)
                                mock_llm = MagicMock()
                                long_prose = (
                                    "This is the first sentence with substantial content to ensure the file "
                                    "meets the minimum size requirements for a valid markdown file. "
                                    "This is the second sentence that provides additional detail and context "
                                    "about the topic being discussed in this comprehensive example. "
                                    "This is the third sentence which concludes the markdown content with "
                                    "meaningful information to demonstrate the complete workflow."
                                )
                                mock_llm.call.return_value = {
                                    "content": f"# Example Title\n\n{long_prose}"
                                }
                                mock_llm_factory.return_value = mock_llm

                                main()

                # Verify file was created
                file_path = Path(FILENAME)
                assert file_path.exists()

                # Verify validation passes
                validate_markdown_file(FILENAME)

            finally:
                os.chdir(original_cwd)

    def test_workflow_file_has_correct_structure(self):
        """Test that workflow creates file with correct markdown structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_204_markdown_file_creation.git_add_file"):
                    with patch("sheep.features.feature_204_markdown_file_creation.git_commit"):
                        with patch("sheep.features.feature_204_markdown_file_creation.git_push"):
                            with patch("sheep.features.feature_204_markdown_file_creation.create_llm") as mock_llm_factory:
                                mock_llm = MagicMock()
                                long_prose = (
                                    "This is the first comprehensive sentence with substantial content that extends "
                                    "across multiple words to ensure adequate file size. "
                                    "This is the second sentence providing additional context, detail, and comprehensive information "
                                    "about the topic being discussed and explored. "
                                    "This is the third sentence concluding the markdown file with meaningful and complete content."
                                )
                                mock_llm.call.return_value = {
                                    "content": f"# Test Title\n\n{long_prose}"
                                }
                                mock_llm_factory.return_value = mock_llm

                                main()

                # Read file and verify structure
                file_path = Path(FILENAME)
                content = file_path.read_text(encoding="utf-8")
                lines = content.split("\n")

                # Check H1 heading on first line
                assert lines[0].startswith("# ")

                # Check blank line separator
                assert lines[1].strip() == ""

                # Check prose has 3 sentences
                prose = "\n".join(lines[2:]).strip()
                assert prose.count(".") == 3

            finally:
                os.chdir(original_cwd)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
