"""Integration tests for feature 207: Complete markdown file creation workflow.

These tests verify the entire feature 207 workflow from start to finish:
1. File creation (Phase 1)
2. File validation (Phase 2)
3. Git operations (Phase 3)

Integration tests ensure all phases work together correctly.
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


class TestMainIntegration:
    """Integration tests for main() orchestration function."""

    def test_main_returns_0_on_complete_success(self):
        """Integration test: main() returns 0 on complete success.

        This test verifies that when all phases complete successfully,
        main() returns 0 indicating success.
        """
        from sheep.features.feature_207_markdown_file_creation import main

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock git operations
                with patch("sheep.features.feature_207_markdown_file_creation.subprocess.run") as mock_run:
                    mock_run.return_value = MagicMock()

                    # Execute complete workflow
                    exit_code = main()

                    # Verify success return code
                    assert exit_code == 0, "main() should return 0 on success"

            finally:
                os.chdir(original_cwd)

    def test_main_returns_1_on_file_creation_failure(self):
        """Integration test: main() returns 1 on file creation failure."""
        from sheep.features.feature_207_markdown_file_creation import main

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock create_markdown_file to raise an error
                with patch("sheep.features.feature_207_markdown_file_creation.create_markdown_file") as mock_create:
                    mock_create.side_effect = OSError("Cannot write file")

                    # Execute workflow
                    exit_code = main()

                    # Verify failure return code
                    assert exit_code == 1, "main() should return 1 on file creation failure"

            finally:
                os.chdir(original_cwd)

    def test_main_returns_1_on_validation_failure(self):
        """Integration test: main() returns 1 on validation failure."""
        from sheep.features.feature_207_markdown_file_creation import main

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock create_markdown_file to create an invalid file
                with patch("sheep.features.feature_207_markdown_file_creation.create_markdown_file") as mock_create:
                    def create_invalid_file():
                        Path("test-ywcbdk.md").write_text("Invalid file\nNo heading")
                        return Path("test-ywcbdk.md")

                    mock_create.side_effect = create_invalid_file

                    # Execute workflow
                    exit_code = main()

                    # Verify failure return code
                    assert exit_code == 1, "main() should return 1 on validation failure"

            finally:
                os.chdir(original_cwd)

    def test_main_returns_1_on_git_add_failure(self):
        """Integration test: main() returns 1 on git add failure."""
        from sheep.features.feature_207_markdown_file_creation import main

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock subprocess.run to fail on git add
                with patch("sheep.features.feature_207_markdown_file_creation.subprocess.run") as mock_run:
                    # Fail on first call (git add)
                    mock_run.side_effect = subprocess.CalledProcessError(
                        1, "git add", stderr="Permission denied"
                    )

                    # Execute workflow
                    exit_code = main()

                    # Verify failure return code
                    assert exit_code == 1, "main() should return 1 on git add failure"

            finally:
                os.chdir(original_cwd)

    def test_main_returns_1_on_git_commit_failure(self):
        """Integration test: main() returns 1 on git commit failure."""
        from sheep.features.feature_207_markdown_file_creation import main

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock subprocess.run to fail on second call (git commit)
                with patch("sheep.features.feature_207_markdown_file_creation.subprocess.run") as mock_run:
                    def side_effect(*args, **kwargs):
                        # First call (git add) succeeds
                        if mock_run.call_count == 1:
                            return MagicMock()
                        # Second call (git commit) fails
                        raise subprocess.CalledProcessError(
                            1, "git commit", stderr="Nothing to commit"
                        )

                    mock_run.side_effect = side_effect

                    # Execute workflow
                    exit_code = main()

                    # Verify failure return code
                    assert exit_code == 1, "main() should return 1 on git commit failure"

            finally:
                os.chdir(original_cwd)

    def test_main_returns_1_on_git_push_failure(self):
        """Integration test: main() returns 1 on git push failure."""
        from sheep.features.feature_207_markdown_file_creation import main

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock subprocess.run to fail on third call (git push)
                with patch("sheep.features.feature_207_markdown_file_creation.subprocess.run") as mock_run:
                    def side_effect(*args, **kwargs):
                        # First two calls (git add, git commit) succeed
                        if mock_run.call_count <= 2:
                            return MagicMock()
                        # Third call (git push) fails
                        raise subprocess.CalledProcessError(
                            1, "git push", stderr="Authentication failed"
                        )

                    mock_run.side_effect = side_effect

                    # Execute workflow
                    exit_code = main()

                    # Verify failure return code
                    assert exit_code == 1, "main() should return 1 on git push failure"

            finally:
                os.chdir(original_cwd)

    def test_file_exists_after_main_succeeds(self):
        """Integration test: File exists after create phase completes."""
        from sheep.features.feature_207_markdown_file_creation import (
            main,
            FILENAME,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock git operations
                with patch("sheep.features.feature_207_markdown_file_creation.subprocess.run") as mock_run:
                    mock_run.return_value = MagicMock()

                    # Verify file doesn't exist before
                    assert not Path(FILENAME).exists()

                    # Execute workflow
                    exit_code = main()

                    # Verify success
                    assert exit_code == 0

                    # Verify file exists after
                    assert Path(FILENAME).exists(), f"File {FILENAME} should exist after main() succeeds"

            finally:
                os.chdir(original_cwd)

    def test_validation_passes_after_main_succeeds(self):
        """Integration test: Validation passes after file creation."""
        from sheep.features.feature_207_markdown_file_creation import (
            main,
            FILENAME,
            validate_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock git operations
                with patch("sheep.features.feature_207_markdown_file_creation.subprocess.run") as mock_run:
                    mock_run.return_value = MagicMock()

                    # Execute workflow
                    exit_code = main()

                    # Verify success
                    assert exit_code == 0

                    # Verify validation passes (should not raise)
                    validate_markdown_file(FILENAME)

            finally:
                os.chdir(original_cwd)

    def test_file_is_staged_after_git_operations(self):
        """Integration test: File is committed after git operations complete."""
        from sheep.features.feature_207_markdown_file_creation import main, FILENAME, COMMIT_MESSAGE

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Initialize git repo
                subprocess.run(
                    ["git", "init"],
                    check=True,
                    capture_output=True,
                    cwd=tmpdir
                )

                # Configure git user
                subprocess.run(
                    ["git", "config", "user.email", "test@example.com"],
                    check=True,
                    capture_output=True,
                    cwd=tmpdir
                )
                subprocess.run(
                    ["git", "config", "user.name", "Test User"],
                    check=True,
                    capture_output=True,
                    cwd=tmpdir
                )

                # Create initial commit
                Path(".gitkeep").touch()
                subprocess.run(
                    ["git", "add", ".gitkeep"],
                    check=True,
                    capture_output=True,
                    cwd=tmpdir
                )
                subprocess.run(
                    ["git", "commit", "-m", "Initial commit"],
                    check=True,
                    capture_output=True,
                    cwd=tmpdir
                )

                # Create branch
                subprocess.run(
                    ["git", "checkout", "-b", "feat/markdown-file-creation-94cf63"],
                    check=True,
                    capture_output=True,
                    cwd=tmpdir
                )

                # Mock only git push (which would fail without a real origin)
                with patch("sheep.features.feature_207_markdown_file_creation.git_push") as mock_push:
                    mock_push.return_value = MagicMock()

                    # Execute main workflow
                    exit_code = main()

                    # Verify success
                    assert exit_code == 0

                    # Check git log to verify file was committed
                    result = subprocess.run(
                        ["git", "log", "--oneline"],
                        check=True,
                        capture_output=True,
                        text=True,
                        cwd=tmpdir
                    )

                    # Verify commit message is in log
                    assert COMMIT_MESSAGE in result.stdout or "Create markdown file" in result.stdout, \
                        f"Commit message should be in git log. Log: {result.stdout}"

                    # Verify file exists in git tree
                    result = subprocess.run(
                        ["git", "ls-tree", "-r", "HEAD"],
                        check=True,
                        capture_output=True,
                        text=True,
                        cwd=tmpdir
                    )

                    assert FILENAME in result.stdout, \
                        f"File {FILENAME} should be in git tree. Tree: {result.stdout}"

            finally:
                os.chdir(original_cwd)

    def test_main_orchestrates_phases_in_order(self):
        """Integration test: Verify phases are executed in correct order.

        Verify that:
        1. File creation happens before validation
        2. Validation happens before git operations
        3. Git operations happen in order: add, commit, push
        """
        from sheep.features.feature_207_markdown_file_creation import main

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Track execution order
                execution_order = []

                def track_create(*args, **kwargs):
                    execution_order.append("create")
                    return MagicMock()

                def track_validate(*args, **kwargs):
                    execution_order.append("validate")
                    return MagicMock()

                def track_subprocess(*args, **kwargs):
                    if args[0][1] == "add":
                        execution_order.append("git_add")
                    elif args[0][1] == "commit":
                        execution_order.append("git_commit")
                    elif args[0][1] == "push":
                        execution_order.append("git_push")
                    return MagicMock()

                # Mock functions to track execution
                with patch("sheep.features.feature_207_markdown_file_creation.create_markdown_file") as mock_create, \
                     patch("sheep.features.feature_207_markdown_file_creation.validate_markdown_file") as mock_validate, \
                     patch("sheep.features.feature_207_markdown_file_creation.subprocess.run") as mock_subprocess:

                    mock_create.side_effect = track_create
                    mock_validate.side_effect = track_validate
                    mock_subprocess.side_effect = track_subprocess

                    # Execute workflow
                    exit_code = main()

                    # Verify success
                    assert exit_code == 0

                    # Verify execution order: create, validate, git operations
                    expected_order = ["create", "validate", "git_add", "git_commit", "git_push"]
                    assert execution_order == expected_order, \
                        f"Expected execution order {expected_order}, got {execution_order}"

            finally:
                os.chdir(original_cwd)
