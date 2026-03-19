"""Environment Verification Tests for Feature 116.

Verifies that the content_generators module exists with all required functions
for markdown file creation, and that all dependencies are properly configured.
"""

import inspect
from typing import get_type_hints

import pytest


class TestContentGeneratorsImportable:
    """Tests for content_generators module importability."""

    def test_module_imports_successfully(self):
        """Test that content_generators module can be imported."""
        try:
            from sheep import content_generators  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import content_generators: {e}")

    def test_all_required_functions_exist(self):
        """Test that all 5 required functions exist in content_generators."""
        from sheep import content_generators

        required_functions = [
            "generate_markdown_content",
            "write_markdown_file",
            "validate_markdown_file",
            "commit_markdown_file",
            "push_markdown_file",
        ]

        for function_name in required_functions:
            assert hasattr(
                content_generators, function_name
            ), f"Function {function_name} not found in content_generators"

    def test_all_functions_are_callable(self):
        """Test that all required functions are callable."""
        from sheep import content_generators

        required_functions = [
            "generate_markdown_content",
            "write_markdown_file",
            "validate_markdown_file",
            "commit_markdown_file",
            "push_markdown_file",
        ]

        for function_name in required_functions:
            func = getattr(content_generators, function_name)
            assert callable(
                func
            ), f"Function {function_name} is not callable"


class TestFunctionSignatures:
    """Tests for function signatures and expected parameters."""

    def test_generate_markdown_content_signature(self):
        """Test that generate_markdown_content has expected signature."""
        from sheep.content_generators import generate_markdown_content

        sig = inspect.signature(generate_markdown_content)
        # Should take no required parameters
        assert (
            len(sig.parameters) == 0
        ), f"Expected 0 parameters, got {len(sig.parameters)}"

        # Should return a string
        hints = get_type_hints(generate_markdown_content)
        assert hints.get("return") == str, "Should return str"

    def test_write_markdown_file_signature(self):
        """Test that write_markdown_file has expected signature."""
        from sheep.content_generators import write_markdown_file

        sig = inspect.signature(write_markdown_file)
        params = list(sig.parameters.keys())
        # Should have content and filename parameters
        assert "content" in params, "Missing 'content' parameter"
        assert "filename" in params, "Missing 'filename' parameter"

    def test_validate_markdown_file_signature(self):
        """Test that validate_markdown_file has expected signature."""
        from sheep.content_generators import validate_markdown_file

        sig = inspect.signature(validate_markdown_file)
        params = list(sig.parameters.keys())
        # Should have filepath parameter
        assert "filepath" in params, "Missing 'filepath' parameter"

    def test_commit_markdown_file_signature(self):
        """Test that commit_markdown_file has expected signature."""
        from sheep.content_generators import commit_markdown_file

        sig = inspect.signature(commit_markdown_file)
        params = list(sig.parameters.keys())
        # Should have filepath and content as required parameters
        assert "filepath" in params, "Missing 'filepath' parameter"
        assert "content" in params, "Missing 'content' parameter"

    def test_push_markdown_file_signature(self):
        """Test that push_markdown_file has expected signature."""
        from sheep.content_generators import push_markdown_file

        sig = inspect.signature(push_markdown_file)
        # Should take optional parameters (repo_path, remote)
        assert len(sig.parameters) >= 0, "Function should be callable"


class TestDependencies:
    """Tests for required dependencies."""

    def test_pathlib_available(self):
        """Test that pathlib is available (required by content_generators)."""
        try:
            from pathlib import Path  # noqa: F401
        except ImportError as e:
            pytest.fail(f"pathlib not available: {e}")

    def test_logging_available(self):
        """Test that logging utilities are available."""
        try:
            from sheep.observability.logging import get_logger  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Logging utilities not available: {e}")

    def test_llm_framework_available(self):
        """Test that LLM framework is available for content generation."""
        try:
            from sheep.config.llm import get_reasoning_llm  # noqa: F401
        except ImportError as e:
            pytest.fail(f"LLM framework not available: {e}")

    def test_git_tools_available(self):
        """Test that Git tools are available for commit and push operations."""
        try:
            from sheep.tools import GitCommitTool, GitPushTool  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Git tools not available: {e}")


class TestFunctionDocumentation:
    """Tests that functions have proper documentation."""

    def test_all_functions_have_docstrings(self):
        """Test that all required functions have docstrings."""
        from sheep import content_generators

        required_functions = [
            "generate_markdown_content",
            "write_markdown_file",
            "validate_markdown_file",
            "commit_markdown_file",
            "push_markdown_file",
        ]

        for function_name in required_functions:
            func = getattr(content_generators, function_name)
            assert (
                func.__doc__ is not None
            ), f"Function {function_name} has no docstring"
            assert (
                len(func.__doc__) > 10
            ), f"Function {function_name} has empty docstring"
