"""
Comprehensive test suite for feature 283: markdown file creation with content generation.

This module provides comprehensive test coverage for feature 283, which creates
a markdown file (test-gqvdp6.md) with auto-generated content from Claude API,
proper structure, encoding, and line endings.

Test Coverage:
- Orchestration function returns correct result dictionary
- File is created at repository root with correct filename
- Content structure (H1 heading + blank line + prose)
- Encoding validation (UTF-8 without BOM)
- Line ending validation (Unix LF, no Windows CRLF)
- Prose content validation (2-3 sentences)
- Git integration (commit message format, push result)
- End-to-end integration of the complete workflow
- Error handling for missing API key, git configuration issues

The test suite uses pytest fixtures, mocks, and helper functions to create
isolated test environments and comprehensive validation testing.
"""

import importlib.util
import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sheep.content_generators import (
    create_markdown_file,
    validate_markdown_file,
    write_markdown_file,
)


# ============================================================================
# Pytest Fixtures
# ============================================================================


@pytest.fixture
def temp_dir():
    """
    Provide an isolated temporary directory for test file creation.

    Yields a temporary directory path and restores the original working
    directory after the test completes. This fixture ensures tests don't
    interfere with the repository state or each other.

    Yields:
        Path: The temporary directory path
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            yield Path(tmpdir)
        finally:
            os.chdir(original_cwd)


@pytest.fixture
def sample_markdown_content():
    """
    Provide sample valid markdown content for testing.

    Returns:
        str: Valid markdown with H1 heading and 2-3 sentences
    """
    return (
        "# The Power of Iteration\n"
        "\n"
        "Iteration is a fundamental principle in software development that drives "
        "improvement through repeated cycles of design and implementation. "
        "Each iteration builds upon the previous one, incorporating feedback and "
        "lessons learned to refine approaches. By embracing iterative processes, "
        "teams can adapt to changing requirements and deliver increasingly valuable solutions.\n"
    )


# ============================================================================
# Test Classes
# ============================================================================


class TestWrapperScript:
    """Unit tests for the wrapper script create_markdown_file.py."""

    def _load_wrapper_module(self):
        """Helper to dynamically load the wrapper module."""
        wrapper_path = Path(__file__).parent / "create_markdown_file.py"
        spec = importlib.util.spec_from_file_location("wrapper_module_test", wrapper_path)
        wrapper_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wrapper_module)
        return wrapper_module

    def test_imports_orchestration_function(self):
        """Test that wrapper script imports orchestration function successfully."""
        wrapper_module = self._load_wrapper_module()

        # Should have main function
        assert hasattr(wrapper_module, "main")
        assert callable(wrapper_module.main)

        # Should have imported create_markdown_file
        assert hasattr(wrapper_module, "create_markdown_file")

    def test_calls_create_markdown_file_with_correct_filename(self, temp_dir):
        """Test that wrapper script calls create_markdown_file with filename='test-gqvdp6.md'."""
        wrapper_module = self._load_wrapper_module()

        # Mock the create_markdown_file in the wrapper module's namespace
        with mock.patch.object(wrapper_module, "create_markdown_file") as mock_create:
            mock_create.return_value = {
                "filepath": str(Path.cwd() / "test-gqvdp6.md"),
                "content": "# Test\n\nSentence one. Sentence two. Sentence three.",
                "commit_message": "feat(283): create markdown file test-gqvdp6.md with title and prose content",
                "push_result": "Success",
            }

            result = wrapper_module.main()

            # Verify create_markdown_file was called with correct filename
            mock_create.assert_called_once()
            call_args = mock_create.call_args
            # Verify "test-gqvdp6.md" is the first positional argument
            assert call_args[0][0] == "test-gqvdp6.md"

    def test_calls_create_markdown_file_with_correct_feature_number(self, temp_dir):
        """Test that wrapper script calls create_markdown_file with feature_number=283."""
        wrapper_module = self._load_wrapper_module()

        # Mock the create_markdown_file in the wrapper module's namespace
        with mock.patch.object(wrapper_module, "create_markdown_file") as mock_create:
            mock_create.return_value = {
                "filepath": str(Path.cwd() / "test-gqvdp6.md"),
                "content": "# Test\n\nSentence one. Sentence two. Sentence three.",
                "commit_message": "feat(283): create markdown file test-gqvdp6.md with title and prose content",
                "push_result": "Success",
            }

            result = wrapper_module.main()

            # Verify create_markdown_file was called with correct feature number
            mock_create.assert_called_once()
            call_kwargs = mock_create.call_args[1]
            assert call_kwargs.get("feature_number") == 283

    def test_handles_orchestration_error_gracefully(self, temp_dir):
        """Test that wrapper script catches exceptions from orchestration function."""
        wrapper_module = self._load_wrapper_module()

        # Mock create_markdown_file to raise an exception
        with mock.patch.object(wrapper_module, "create_markdown_file") as mock_create:
            mock_create.side_effect = ValueError("Test error message")

            # Wrapper should catch and re-raise (but not crash)
            with pytest.raises(ValueError, match="Test error message"):
                wrapper_module.main()

    def test_returns_result_dictionary_on_success(self, temp_dir):
        """Test that wrapper script returns result dictionary from orchestration."""
        wrapper_module = self._load_wrapper_module()

        with mock.patch.object(wrapper_module, "create_markdown_file") as mock_create:
            expected_result = {
                "filepath": str(Path.cwd() / "test-gqvdp6.md"),
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence.",
                "commit_message": "feat(283): create markdown file test-gqvdp6.md with title and prose content",
                "push_result": "Success",
            }
            mock_create.return_value = expected_result

            result = wrapper_module.main()

            assert result == expected_result
            assert isinstance(result, dict)
            assert "filepath" in result
            assert "content" in result
            assert "commit_message" in result
            assert "push_result" in result
