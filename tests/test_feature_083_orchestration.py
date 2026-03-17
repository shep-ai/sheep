"""Tests for feature 083 orchestration script (create_test_file.py)."""

import importlib.util
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


def load_create_test_file_module():
    """Load the create_test_file.py module dynamically."""
    script_path = (
        Path(__file__).parent.parent
        / "specs"
        / "083-markdown-file-creation-efd4d5"
        / "scripts"
        / "create_test_file.py"
    )
    spec = importlib.util.spec_from_file_location(
        "create_test_file", script_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestCreateTestFileOrchestration:
    """Tests for the create_test_file.py orchestration script."""

    def test_script_file_exists(self):
        """Test that the orchestration script file exists."""
        script_path = (
            Path(__file__).parent.parent
            / "specs"
            / "083-markdown-file-creation-efd4d5"
            / "scripts"
            / "create_test_file.py"
        )
        assert script_path.exists(), f"Script not found: {script_path}"

    def test_module_imports_successfully(self):
        """Test that create_test_file module can be imported."""
        # Should not raise an exception
        module = load_create_test_file_module()
        assert module is not None

    def test_main_function_is_callable(self):
        """Test that main() function exists and is callable."""
        module = load_create_test_file_module()
        assert hasattr(module, "main")
        assert callable(module.main)

    @patch("sheep.content_generators.create_markdown_file")
    def test_main_returns_zero_on_success(self, mock_create):
        """Test that main() returns 0 on successful file creation."""
        mock_create.return_value = {
            "filepath": "/repo/test-szyfny.md",
            "content": "# Title\n\nSentence. Sentence. Sentence.\n",
            "commit_message": "feat(083): create markdown file test-szyfny.md with prose content",
            "push_result": "Pushed successfully",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            module = load_create_test_file_module()
            result = module.main(filename="test-szyfny.md", repo_path=tmpdir)

            assert result == 0

    @patch("sheep.content_generators.create_markdown_file")
    def test_main_returns_nonzero_on_ioerror(self, mock_create):
        """Test that main() returns non-zero on file I/O error."""
        mock_create.side_effect = IOError("Permission denied")

        module = load_create_test_file_module()
        result = module.main(filename="test-szyfny.md", repo_path="/repo")

        assert result != 0

    @patch("sheep.content_generators.create_markdown_file")
    def test_main_returns_nonzero_on_valueerror(self, mock_create):
        """Test that main() returns non-zero on validation error."""
        mock_create.side_effect = ValueError("Invalid filename")

        module = load_create_test_file_module()
        result = module.main(filename="test-szyfny.md", repo_path="/repo")

        assert result != 0

    @patch("sheep.content_generators.create_markdown_file")
    def test_main_returns_nonzero_on_general_exception(self, mock_create):
        """Test that main() returns non-zero on unexpected errors."""
        mock_create.side_effect = RuntimeError("Unexpected error")

        module = load_create_test_file_module()
        result = module.main(filename="test-szyfny.md", repo_path="/repo")

        assert result != 0

    def test_main_handles_missing_repo_path(self):
        """Test that main() handles missing repo_path gracefully."""
        module = load_create_test_file_module()

        # Call with non-existent repo_path
        result = module.main(
            filename="test-szyfny.md", repo_path="/nonexistent/path"
        )

        # Should return error code 2 (configuration error)
        assert result == 2

    def test_main_handles_file_not_directory(self):
        """Test that main() handles file path (not directory) gracefully."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            module = load_create_test_file_module()

            # Call with file path instead of directory
            result = module.main(
                filename="test-szyfny.md", repo_path=tmp_path
            )

            # Should return error code 2 (configuration error)
            assert result == 2
        finally:
            # Clean up
            Path(tmp_path).unlink(missing_ok=True)

    @patch("sheep.content_generators.create_markdown_file")
    def test_main_calls_create_markdown_file_with_correct_args(
        self, mock_create
    ):
        """Test that main() calls create_markdown_file with correct arguments."""
        mock_create.return_value = {
            "filepath": "/repo/test-szyfny.md",
            "content": "# Title\n\nContent.\n",
            "commit_message": "feat(083): ...",
            "push_result": "Pushed",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            module = load_create_test_file_module()
            module.main(filename="test-szyfny.md", repo_path=tmpdir)

            # Verify create_markdown_file was called with correct arguments
            mock_create.assert_called_once_with("test-szyfny.md", tmpdir)

    @patch("sheep.content_generators.create_markdown_file")
    def test_main_uses_default_filename(self, mock_create):
        """Test that main() uses default filename when not specified."""
        mock_create.return_value = {
            "filepath": "/repo/test-szyfny.md",
            "content": "# Title\n\nContent.\n",
            "commit_message": "feat(083): ...",
            "push_result": "Pushed",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            module = load_create_test_file_module()
            module.main(repo_path=tmpdir)

            # Should use default filename "test-szyfny.md"
            call_args = mock_create.call_args
            assert call_args[0][0] == "test-szyfny.md"
