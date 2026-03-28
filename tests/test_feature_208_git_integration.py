"""Tests for feature 208 git integration functionality.

Tests verify that:
1. git_add_file() stages file with 'git add'
2. git_commit() creates commit with conventional message
3. git_push() pushes to remote branch
4. Git operations handle errors properly
5. main() orchestrates all phases correctly
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch


def setup_module():
    """Set up test environment by adding src to path."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


def test_git_add_file_calls_subprocess_run():
    """Test that git_add_file() calls subprocess.run with correct arguments."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        git_add_file,
    )

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        git_add_file(FILENAME)

        # Verify subprocess.run was called with correct arguments
        mock_run.assert_called_once_with(
            ["git", "add", FILENAME],
            check=True,
            capture_output=True,
            text=True,
        )


def test_git_add_file_raises_on_failure():
    """Test that git_add_file() raises CalledProcessError on failure."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        git_add_file,
    )

    with patch("subprocess.run") as mock_run:
        # Simulate git add failure
        mock_run.side_effect = subprocess.CalledProcessError(
            1, "git add", stderr="error message"
        )

        try:
            git_add_file(FILENAME)
            assert False, "Should have raised CalledProcessError"
        except subprocess.CalledProcessError:
            pass  # Expected


def test_git_commit_calls_subprocess_run():
    """Test that git_commit() calls subprocess.run with correct arguments."""
    from sheep.features.feature_208_markdown_file_creation import (
        COMMIT_MESSAGE,
        git_commit,
    )

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        git_commit(COMMIT_MESSAGE)

        # Verify subprocess.run was called with correct arguments
        mock_run.assert_called_once_with(
            ["git", "commit", "-m", COMMIT_MESSAGE],
            check=True,
            capture_output=True,
            text=True,
        )


def test_git_commit_with_custom_message():
    """Test that git_commit() accepts custom commit message."""
    from sheep.features.feature_208_markdown_file_creation import git_commit

    custom_message = "test: Custom commit message"

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        git_commit(custom_message)

        # Verify subprocess.run was called with custom message
        mock_run.assert_called_once_with(
            ["git", "commit", "-m", custom_message],
            check=True,
            capture_output=True,
            text=True,
        )


def test_git_commit_raises_on_failure():
    """Test that git_commit() raises CalledProcessError on failure."""
    from sheep.features.feature_208_markdown_file_creation import (
        COMMIT_MESSAGE,
        git_commit,
    )

    with patch("subprocess.run") as mock_run:
        # Simulate git commit failure
        mock_run.side_effect = subprocess.CalledProcessError(
            1, "git commit", stderr="nothing to commit"
        )

        try:
            git_commit(COMMIT_MESSAGE)
            assert False, "Should have raised CalledProcessError"
        except subprocess.CalledProcessError:
            pass  # Expected


def test_git_push_calls_subprocess_run():
    """Test that git_push() calls subprocess.run with correct arguments."""
    from sheep.features.feature_208_markdown_file_creation import (
        BRANCH_NAME,
        git_push,
    )

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        git_push(BRANCH_NAME)

        # Verify subprocess.run was called with correct git push arguments
        mock_run.assert_called_once_with(
            ["git", "push", "-u", "origin", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )


def test_git_push_raises_on_failure():
    """Test that git_push() raises CalledProcessError on failure."""
    from sheep.features.feature_208_markdown_file_creation import (
        BRANCH_NAME,
        git_push,
    )

    with patch("subprocess.run") as mock_run:
        # Simulate git push failure
        mock_run.side_effect = subprocess.CalledProcessError(
            1, "git push", stderr="network error"
        )

        try:
            git_push(BRANCH_NAME)
            assert False, "Should have raised CalledProcessError"
        except subprocess.CalledProcessError:
            pass  # Expected


def test_main_returns_zero_on_success():
    """Test that main() returns 0 on successful workflow."""
    from sheep.features.feature_208_markdown_file_creation import main

    with patch("sheep.features.feature_208_markdown_file_creation.create_markdown_file") as mock_create, \
         patch("sheep.features.feature_208_markdown_file_creation.validate_markdown_file") as mock_validate, \
         patch("sheep.features.feature_208_markdown_file_creation.git_add_file") as mock_add, \
         patch("sheep.features.feature_208_markdown_file_creation.git_commit") as mock_commit, \
         patch("sheep.features.feature_208_markdown_file_creation.git_push") as mock_push:

        # Mock all functions to succeed
        mock_create.return_value = Path("test-s4b1z3.md")
        mock_validate.return_value = None
        mock_add.return_value = None
        mock_commit.return_value = None
        mock_push.return_value = None

        result = main()

        assert result == 0, "main() should return 0 on success"
        # Verify all phases were called
        mock_create.assert_called_once()
        mock_validate.assert_called_once()
        mock_add.assert_called_once()
        mock_commit.assert_called_once()
        mock_push.assert_called_once()


def test_main_returns_one_on_file_not_found():
    """Test that main() returns 1 when file creation fails."""
    from sheep.features.feature_208_markdown_file_creation import main

    with patch("sheep.features.feature_208_markdown_file_creation.create_markdown_file") as mock_create:
        # Mock file creation failure
        mock_create.side_effect = OSError("File creation failed")

        result = main()

        assert result == 1, "main() should return 1 on failure"


def test_main_returns_one_on_validation_failure():
    """Test that main() returns 1 when validation fails."""
    from sheep.features.feature_208_markdown_file_creation import main

    with patch("sheep.features.feature_208_markdown_file_creation.create_markdown_file") as mock_create, \
         patch("sheep.features.feature_208_markdown_file_creation.validate_markdown_file") as mock_validate:

        # Mock validation failure
        mock_create.return_value = Path("test-s4b1z3.md")
        mock_validate.side_effect = ValueError("Invalid file format")

        result = main()

        assert result == 1, "main() should return 1 on validation failure"


def test_main_returns_one_on_git_add_failure():
    """Test that main() returns 1 when git add fails."""
    from sheep.features.feature_208_markdown_file_creation import main

    with patch("sheep.features.feature_208_markdown_file_creation.create_markdown_file") as mock_create, \
         patch("sheep.features.feature_208_markdown_file_creation.validate_markdown_file") as mock_validate, \
         patch("sheep.features.feature_208_markdown_file_creation.git_add_file") as mock_add:

        # Mock git add failure
        mock_create.return_value = Path("test-s4b1z3.md")
        mock_validate.return_value = None
        mock_add.side_effect = subprocess.CalledProcessError(1, "git add")

        result = main()

        assert result == 1, "main() should return 1 on git add failure"


def test_main_returns_one_on_git_commit_failure():
    """Test that main() returns 1 when git commit fails."""
    from sheep.features.feature_208_markdown_file_creation import main

    with patch("sheep.features.feature_208_markdown_file_creation.create_markdown_file") as mock_create, \
         patch("sheep.features.feature_208_markdown_file_creation.validate_markdown_file") as mock_validate, \
         patch("sheep.features.feature_208_markdown_file_creation.git_add_file") as mock_add, \
         patch("sheep.features.feature_208_markdown_file_creation.git_commit") as mock_commit:

        # Mock git commit failure
        mock_create.return_value = Path("test-s4b1z3.md")
        mock_validate.return_value = None
        mock_add.return_value = None
        mock_commit.side_effect = subprocess.CalledProcessError(1, "git commit")

        result = main()

        assert result == 1, "main() should return 1 on git commit failure"


def test_main_returns_one_on_git_push_failure():
    """Test that main() returns 1 when git push fails."""
    from sheep.features.feature_208_markdown_file_creation import main

    with patch("sheep.features.feature_208_markdown_file_creation.create_markdown_file") as mock_create, \
         patch("sheep.features.feature_208_markdown_file_creation.validate_markdown_file") as mock_validate, \
         patch("sheep.features.feature_208_markdown_file_creation.git_add_file") as mock_add, \
         patch("sheep.features.feature_208_markdown_file_creation.git_commit") as mock_commit, \
         patch("sheep.features.feature_208_markdown_file_creation.git_push") as mock_push:

        # Mock git push failure
        mock_create.return_value = Path("test-s4b1z3.md")
        mock_validate.return_value = None
        mock_add.return_value = None
        mock_commit.return_value = None
        mock_push.side_effect = subprocess.CalledProcessError(1, "git push")

        result = main()

        assert result == 1, "main() should return 1 on git push failure"


def test_main_orchestration_order():
    """Test that main() calls functions in correct order."""
    from sheep.features.feature_208_markdown_file_creation import main

    call_order = []

    def track_call(name):
        def side_effect(*args, **kwargs):
            call_order.append(name)
        return side_effect

    with patch("sheep.features.feature_208_markdown_file_creation.create_markdown_file") as mock_create, \
         patch("sheep.features.feature_208_markdown_file_creation.validate_markdown_file") as mock_validate, \
         patch("sheep.features.feature_208_markdown_file_creation.git_add_file") as mock_add, \
         patch("sheep.features.feature_208_markdown_file_creation.git_commit") as mock_commit, \
         patch("sheep.features.feature_208_markdown_file_creation.git_push") as mock_push:

        # Track calls
        mock_create.side_effect = track_call("create")
        mock_create.return_value = Path("test-s4b1z3.md")
        mock_validate.side_effect = track_call("validate")
        mock_add.side_effect = track_call("add")
        mock_commit.side_effect = track_call("commit")
        mock_push.side_effect = track_call("push")

        result = main()

        assert result == 0
        # Verify correct order: create -> validate -> add -> commit -> push
        assert call_order == ["create", "validate", "add", "commit", "push"]
