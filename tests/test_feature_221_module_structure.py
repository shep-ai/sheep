"""Tests for feature 221 script foundation and module structure.

Tests verify that the create_markdown_file_221 module:
1. Can be imported without errors
2. Has all required constants defined
3. Constants have correct values and types
4. Required functions exist and are callable
5. Script runs without immediate errors (Phase 1 foundation)
"""

import sys
import subprocess
from pathlib import Path


class TestModuleImports:
    """Tests for module import and availability."""

    def test_module_imports_successfully(self):
        """Test that create_markdown_file_221 module imports without errors."""
        # Import the script module
        import create_markdown_file_221

        # If import succeeds, we're good
        assert create_markdown_file_221 is not None

    def test_pathlib_imported(self):
        """Test that pathlib.Path is available in module."""
        import create_markdown_file_221

        # Module should have Path imported
        assert hasattr(create_markdown_file_221, "Path")

    def test_subprocess_imported(self):
        """Test that subprocess is available in module."""
        import create_markdown_file_221

        # Module should have subprocess imported
        assert hasattr(create_markdown_file_221, "subprocess")

    def test_sys_imported(self):
        """Test that sys is available in module."""
        import create_markdown_file_221

        # Module should have sys imported
        assert hasattr(create_markdown_file_221, "sys")


class TestModuleConstants:
    """Tests for module configuration constants."""

    def test_filename_constant_exists(self):
        """Test that FILENAME constant is defined."""
        from create_markdown_file_221 import FILENAME

        assert FILENAME is not None
        assert isinstance(FILENAME, str)

    def test_filename_has_correct_value(self):
        """Test that FILENAME has the correct value for feature 221."""
        from create_markdown_file_221 import FILENAME

        assert FILENAME == "test-ye16lc.md"

    def test_title_constant_exists(self):
        """Test that TITLE constant is defined."""
        from create_markdown_file_221 import TITLE

        assert TITLE is not None
        assert isinstance(TITLE, str)

    def test_title_is_not_empty(self):
        """Test that TITLE has content."""
        from create_markdown_file_221 import TITLE

        assert len(TITLE) > 0

    def test_prose_constant_exists(self):
        """Test that PROSE constant is defined."""
        from create_markdown_file_221 import PROSE

        assert PROSE is not None
        assert isinstance(PROSE, str)

    def test_prose_is_not_empty(self):
        """Test that PROSE has content."""
        from create_markdown_file_221 import PROSE

        assert len(PROSE) > 0

    def test_prose_has_multiple_sentences(self):
        """Test that PROSE has at least 2-3 sentences."""
        from create_markdown_file_221 import PROSE

        # Count sentences by periods
        sentence_count = PROSE.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, got {sentence_count}"

    def test_commit_message_constant_exists(self):
        """Test that COMMIT_MESSAGE constant is defined."""
        from create_markdown_file_221 import COMMIT_MESSAGE

        assert COMMIT_MESSAGE is not None
        assert isinstance(COMMIT_MESSAGE, str)

    def test_commit_message_follows_conventional_format(self):
        """Test that COMMIT_MESSAGE follows conventional commits format."""
        from create_markdown_file_221 import COMMIT_MESSAGE

        # Should start with 'feat(221):'
        assert COMMIT_MESSAGE.startswith("feat(221):")
        assert "test-ye16lc.md" in COMMIT_MESSAGE

    def test_branch_name_constant_exists(self):
        """Test that BRANCH_NAME constant is defined."""
        from create_markdown_file_221 import BRANCH_NAME

        assert BRANCH_NAME is not None
        assert isinstance(BRANCH_NAME, str)

    def test_branch_name_has_correct_value(self):
        """Test that BRANCH_NAME has the correct value."""
        from create_markdown_file_221 import BRANCH_NAME

        assert BRANCH_NAME == "feat/221-markdown-file-creation-213da4"

    def test_all_constants_are_strings(self):
        """Test that all text constants are strings."""
        from create_markdown_file_221 import (
            FILENAME,
            BRANCH_NAME,
            COMMIT_MESSAGE,
            TITLE,
            PROSE,
        )

        assert isinstance(FILENAME, str)
        assert isinstance(BRANCH_NAME, str)
        assert isinstance(COMMIT_MESSAGE, str)
        assert isinstance(TITLE, str)
        assert isinstance(PROSE, str)


class TestModuleFunctions:
    """Tests for module function availability."""

    def test_create_file_function_exists(self):
        """Test that create_file() function exists and is callable."""
        from create_markdown_file_221 import create_file

        assert callable(create_file)

    def test_git_add_function_exists(self):
        """Test that git_add() function exists and is callable."""
        from create_markdown_file_221 import git_add

        assert callable(git_add)

    def test_git_commit_function_exists(self):
        """Test that git_commit() function exists and is callable."""
        from create_markdown_file_221 import git_commit

        assert callable(git_commit)

    def test_git_push_function_exists(self):
        """Test that git_push() function exists and is callable."""
        from create_markdown_file_221 import git_push

        assert callable(git_push)

    def test_main_function_exists(self):
        """Test that main() function exists and is callable."""
        from create_markdown_file_221 import main

        assert callable(main)


class TestScriptExecution:
    """Tests for script execution in Phase 1 (foundation)."""

    def test_script_runs_without_error(self):
        """Test that the script runs without errors in Phase 1 mode."""
        # Run the script and capture output
        result = subprocess.run(
            [sys.executable, "create_markdown_file_221.py"],
            capture_output=True,
            text=True,
        )

        # Script should exit successfully (exit code 0)
        assert result.returncode == 0, f"Script failed: {result.stderr}"

    def test_script_output_contains_phase_marker(self):
        """Test that script output indicates Phase 1 (Script Foundation)."""
        result = subprocess.run(
            [sys.executable, "create_markdown_file_221.py"],
            capture_output=True,
            text=True,
        )

        # Output should indicate Phase 1
        assert "Phase 1" in result.stdout
        assert "Script foundation initialized" in result.stdout

    def test_script_output_contains_configuration_info(self):
        """Test that script output shows configuration variables."""
        result = subprocess.run(
            [sys.executable, "create_markdown_file_221.py"],
            capture_output=True,
            text=True,
        )

        # Output should show configuration
        assert "test-ye16lc.md" in result.stdout
        assert "feat/221-markdown-file-creation-213da4" in result.stdout
