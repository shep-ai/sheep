"""Phase 1: Orchestration Function Verification for feature 295.

This test suite verifies that the sheep.content_generators.create_markdown_file()
orchestration function exists, is importable, and has the correct interface.

The orchestration function is a proven, reliable function that has been used
successfully in features 289-294, encapsulating the entire workflow:
1. Content generation via Claude API
2. File creation with UTF-8 encoding
3. Comprehensive validation
4. Git operations (add, commit, push)
"""

import inspect
from typing import Callable

import pytest

from sheep.content_generators import create_markdown_file


class TestOrchestrationFunctionVerification:
    """Phase 1 verification tests for the orchestration function."""

    def test_create_markdown_file_is_importable(self):
        """Test that create_markdown_file can be imported without errors."""
        # The import at the top of this file would fail if this doesn't pass
        # This test explicitly documents that the function is importable
        assert create_markdown_file is not None

    def test_create_markdown_file_is_callable(self):
        """Test that create_markdown_file is a callable function."""
        assert callable(create_markdown_file)
        assert isinstance(create_markdown_file, Callable)

    def test_create_markdown_file_has_correct_signature(self):
        """Test that create_markdown_file has the expected parameters."""
        sig = inspect.signature(create_markdown_file)
        params = list(sig.parameters.keys())

        # Function should accept these parameters
        assert "filename" in params, "Function should have 'filename' parameter"
        assert "repo_path" in params, "Function should have 'repo_path' parameter"
        assert "feature_number" in params, "Function should have 'feature_number' parameter"

    def test_create_markdown_file_parameters_have_correct_defaults(self):
        """Test that optional parameters have appropriate defaults."""
        sig = inspect.signature(create_markdown_file)

        # filename is required (no default)
        assert sig.parameters["filename"].default == inspect.Parameter.empty

        # repo_path is optional (defaults to None)
        assert sig.parameters["repo_path"].default is None

        # feature_number is optional (defaults to None)
        assert sig.parameters["feature_number"].default is None

    def test_create_markdown_file_has_docstring(self):
        """Test that create_markdown_file has documentation."""
        assert create_markdown_file.__doc__ is not None
        assert len(create_markdown_file.__doc__) > 0

    def test_create_markdown_file_docstring_describes_return_value(self):
        """Test that docstring documents the return value structure."""
        docstring = create_markdown_file.__doc__
        assert "Returns" in docstring, "Docstring should document return value"
        # Should mention dictionary structure
        assert "dict" in docstring.lower() or "dictionary" in docstring.lower()

    def test_create_markdown_file_docstring_describes_parameters(self):
        """Test that docstring documents the parameters."""
        docstring = create_markdown_file.__doc__
        assert "Args" in docstring, "Docstring should document parameters"
        assert "filename" in docstring, "Docstring should mention filename parameter"
        assert "feature_number" in docstring, "Docstring should mention feature_number parameter"

    def test_create_markdown_file_module_location(self):
        """Test that the function is in the correct module."""
        # Function should be in sheep.content_generators module
        assert create_markdown_file.__module__ == "sheep.content_generators"

    def test_create_markdown_file_docstring_mentions_workflow(self):
        """Test that docstring describes the complete workflow."""
        docstring = create_markdown_file.__doc__
        # Should mention the key workflow steps
        workflow_keywords = ["content", "markdown", "commit", "push"]
        doc_lower = docstring.lower()
        matching_keywords = [kw for kw in workflow_keywords if kw in doc_lower]
        assert (
            len(matching_keywords) >= 2
        ), "Docstring should mention workflow steps (content generation, file creation, git operations)"


class TestOrchestrationFunctionPrerequisites:
    """Verify that prerequisites for the orchestration function are available."""

    def test_pathlib_is_available(self):
        """Test that pathlib module is available (required for file I/O)."""
        from pathlib import Path
        assert Path is not None

    def test_subprocess_is_available(self):
        """Test that subprocess module is available (required for git operations)."""
        import subprocess
        assert subprocess is not None

    def test_sheep_config_llm_is_available(self):
        """Test that sheep.config.llm module is available for LLM access."""
        from sheep.config.llm import get_reasoning_llm
        assert get_reasoning_llm is not None
        assert callable(get_reasoning_llm)

    def test_sheep_observability_logging_is_available(self):
        """Test that sheep.observability.logging module is available for structured logging."""
        from sheep.observability.logging import get_logger
        assert get_logger is not None
        assert callable(get_logger)

    def test_git_tools_are_available(self):
        """Test that Git tools are available for commit and push operations."""
        from sheep.tools import GitCommitTool, GitPushTool
        assert GitCommitTool is not None
        assert GitPushTool is not None

    def test_helper_functions_are_available(self):
        """Test that helper functions used by orchestration are available."""
        from sheep.content_generators import (
            generate_markdown_content,
            write_markdown_file,
            validate_markdown_file,
            commit_markdown_file,
            push_markdown_file,
        )

        assert callable(generate_markdown_content)
        assert callable(write_markdown_file)
        assert callable(validate_markdown_file)
        assert callable(commit_markdown_file)
        assert callable(push_markdown_file)


class TestOrchestrationFunctionInterfaceDocumentation:
    """Document the orchestration function interface for reference."""

    def test_document_function_interface(self):
        """Document the orchestration function interface for implementation reference."""
        sig = inspect.signature(create_markdown_file)

        # Create interface documentation
        interface_doc = {
            "function_name": "create_markdown_file",
            "module": "sheep.content_generators",
            "parameters": {
                param_name: {
                    "type": str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any",
                    "default": param.default,
                    "required": param.default == inspect.Parameter.empty,
                }
                for param_name, param in sig.parameters.items()
            },
            "return_type": str(sig.return_annotation) if sig.return_annotation != inspect.Signature.empty else "dict",
        }

        # Verify expected interface
        assert interface_doc["parameters"]["filename"]["required"] is True
        assert interface_doc["parameters"]["repo_path"]["required"] is False
        assert interface_doc["parameters"]["feature_number"]["required"] is False

        # Return type should be dict
        assert "dict" in interface_doc["return_type"].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
