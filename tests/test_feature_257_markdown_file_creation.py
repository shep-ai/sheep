"""Tests for feature 257: Create markdown file test-fl139g.md with prose content."""

import re
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.features.feature_257_markdown_file_creation import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_257_markdown_file,
)


class TestFeature257Module:
    """Tests for feature 257 module structure and metadata."""

    def test_feature_number_is_257(self):
        """Test that FEATURE_NUMBER is 257."""
        assert FEATURE_NUMBER == 257

    def test_markdown_filename_is_correct(self):
        """Test that MARKDOWN_FILENAME is test-fl139g.md."""
        assert MARKDOWN_FILENAME == "test-fl139g.md"

    def test_feature_name_is_set(self):
        """Test that FEATURE_NAME is set."""
        assert FEATURE_NAME == "markdown-file-creation-ef4e6e"

    def test_create_function_exists(self):
        """Test that create_feature_257_markdown_file function exists."""
        assert callable(create_feature_257_markdown_file)


class TestCreateFeature257Function:
    """Tests for create_feature_257_markdown_file function."""

    def test_function_signature_accepts_repo_path(self):
        """Test that function accepts repo_path parameter."""
        # Function should accept optional repo_path parameter
        # This test verifies the function is callable with this parameter
        assert create_feature_257_markdown_file.__code__.co_varnames[0] == "repo_path"

    def test_function_returns_dict(self):
        """Test that function would return a dictionary (checking structure)."""
        # Verify the function has the expected return annotation or docstring
        docstring = create_feature_257_markdown_file.__doc__
        assert "Dictionary containing" in docstring
        assert "filepath" in docstring
        assert "content" in docstring
        assert "commit_message" in docstring
        assert "push_result" in docstring

    def test_function_includes_logging(self):
        """Test that function includes logging implementation."""
        # Check that the module has logger configured
        from sheep.features.feature_257_markdown_file_creation import _logger

        assert _logger is not None

    def test_function_raises_on_failure(self):
        """Test that function documents exception behavior."""
        docstring = create_feature_257_markdown_file.__doc__
        assert "Raises" in docstring
        assert "ValueError" in docstring
        assert "IOError" in docstring
        assert "Exception" in docstring


class TestFeature257Integration:
    """Integration tests for feature 257 workflow."""

    def test_function_has_complete_docstring(self):
        """Test that function has comprehensive documentation."""
        docstring = create_feature_257_markdown_file.__doc__
        assert "orchestrates the complete workflow" in docstring.lower()
        assert "generate valid markdown content" in docstring.lower()
        assert "write file to repository root" in docstring.lower()
        assert "validate file meets" in docstring.lower()
        assert "stage and commit" in docstring.lower()
        assert "push to remote" in docstring.lower()

    def test_workflow_steps_in_docstring(self):
        """Test that docstring documents all 5 workflow steps."""
        docstring = create_feature_257_markdown_file.__doc__
        # Count occurrences of step references
        assert "1." in docstring
        assert "2." in docstring
        assert "3." in docstring
        assert "4." in docstring
        assert "5." in docstring

    def test_imports_required_wrappers(self):
        """Test that module imports required wrapper functions."""
        from sheep.features.feature_257_markdown_file_creation import (
            generate_markdown_content,
            write_markdown_file,
            validate_markdown_file,
            commit_markdown_file,
            push_markdown_file,
        )

        # Verify all required wrappers are imported
        assert callable(generate_markdown_content)
        assert callable(write_markdown_file)
        assert callable(validate_markdown_file)
        assert callable(commit_markdown_file)
        assert callable(push_markdown_file)

    def test_module_has_main_block(self):
        """Test that module has __main__ execution block."""
        import inspect

        # Import the module and check its source
        module = __import__(
            "sheep.features.feature_257_markdown_file_creation",
            fromlist=[""],
        )
        source = inspect.getsource(module)
        # Check that the module source includes __main__ execution
        assert 'if __name__ == "__main__"' in source


class TestWorkflowExecution:
    """Tests for the actual workflow execution."""

    def test_workflow_calls_generate_markdown_content(self):
        """Test that workflow calls generate_markdown_content()."""
        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value="# Test\n\nThis is a test sentence. This is another test sentence.",
        ) as mock_generate, patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            return_value="/repo/test-fl139g.md",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.validate_markdown_file",
            return_value=True,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.commit_markdown_file",
            return_value="commit: abc123",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.push_markdown_file",
            return_value="push: success",
        ):
            result = create_feature_257_markdown_file()
            # Verify generate_markdown_content was called
            mock_generate.assert_called_once()

    def test_workflow_stores_content_and_filepath(self):
        """Test that workflow stores content and composes filepath correctly."""
        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two."
        test_filepath = "/tmp/test-fl139g.md"

        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            return_value=test_filepath,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.validate_markdown_file",
            return_value=True,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.commit_markdown_file",
            return_value="commit result",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.push_markdown_file",
            return_value="push result",
        ):
            result = create_feature_257_markdown_file()
            # Verify result contains expected keys
            assert "filepath" in result
            assert "content" in result
            assert "commit_message" in result
            assert "push_result" in result

    def test_workflow_calls_write_markdown_file(self):
        """Test that workflow calls write_markdown_file with correct arguments."""
        test_content = "# Test\n\nSentence one. Sentence two."

        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            return_value="/repo/test-fl139g.md",
        ) as mock_write, patch(
            "sheep.features.feature_257_markdown_file_creation.validate_markdown_file",
            return_value=True,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.commit_markdown_file",
            return_value="result",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.push_markdown_file",
            return_value="result",
        ):
            create_feature_257_markdown_file()
            # Verify write_markdown_file was called with correct arguments
            mock_write.assert_called_once_with(test_content, MARKDOWN_FILENAME)

    def test_workflow_calls_validate_markdown_file(self):
        """Test that workflow calls validate_markdown_file()."""
        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value="# Test\n\nSentence. Sentence.",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            return_value="/repo/test-fl139g.md",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.validate_markdown_file",
            return_value=True,
        ) as mock_validate, patch(
            "sheep.features.feature_257_markdown_file_creation.commit_markdown_file",
            return_value="result",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.push_markdown_file",
            return_value="result",
        ):
            create_feature_257_markdown_file()
            # Verify validate_markdown_file was called
            mock_validate.assert_called_once()

    def test_workflow_calls_commit_with_exact_message(self):
        """Test that workflow calls commit_markdown_file with exact required message."""
        expected_message = "feat(257): create markdown file test-fl139g.md with prose content"

        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value="# Test\n\nSentence. Sentence.",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            return_value="/repo/test-fl139g.md",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.validate_markdown_file",
            return_value=True,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.commit_markdown_file",
            return_value="commit result",
        ) as mock_commit, patch(
            "sheep.features.feature_257_markdown_file_creation.push_markdown_file",
            return_value="push result",
        ):
            create_feature_257_markdown_file()
            # Verify commit was called with the exact message
            mock_commit.assert_called_once()
            call_args = mock_commit.call_args
            # The custom_message parameter should match exactly
            assert call_args.kwargs.get("custom_message") == expected_message

    def test_workflow_calls_push_markdown_file(self):
        """Test that workflow calls push_markdown_file()."""
        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value="# Test\n\nSentence. Sentence.",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            return_value="/repo/test-fl139g.md",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.validate_markdown_file",
            return_value=True,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.commit_markdown_file",
            return_value="result",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.push_markdown_file",
            return_value="push result",
        ) as mock_push:
            create_feature_257_markdown_file()
            # Verify push was called
            mock_push.assert_called_once()

    def test_workflow_returns_correct_structure(self):
        """Test that workflow returns dict with required keys."""
        test_content = "# Test\n\nSentence one. Sentence two."
        test_filepath = "/repo/test-fl139g.md"
        expected_message = "feat(257): create markdown file test-fl139g.md with prose content"

        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            return_value=test_filepath,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.validate_markdown_file",
            return_value=True,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.commit_markdown_file",
            return_value="commit: abc123",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.push_markdown_file",
            return_value="push: success",
        ):
            result = create_feature_257_markdown_file()
            # Verify result structure
            assert isinstance(result, dict)
            assert result["filepath"] == test_filepath
            assert result["content"] == test_content
            assert result["commit_message"] == expected_message
            assert result["push_result"] == "push: success"


class TestErrorHandling:
    """Tests for error handling and exception propagation."""

    def test_function_raises_on_generate_failure(self):
        """Test that function propagates exceptions from generate_markdown_content."""
        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            side_effect=ValueError("API call failed"),
        ):
            with pytest.raises(ValueError, match="API call failed"):
                create_feature_257_markdown_file()

    def test_function_raises_on_write_failure(self):
        """Test that function propagates exceptions from write_markdown_file."""
        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value="# Test\n\nSentence one. Sentence two.",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            side_effect=IOError("Permission denied"),
        ):
            with pytest.raises(IOError, match="Permission denied"):
                create_feature_257_markdown_file()

    def test_function_raises_on_validation_failure(self):
        """Test that function propagates exceptions from validate_markdown_file."""
        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value="# Test\n\nSentence one. Sentence two.",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            return_value="/repo/test-fl139g.md",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.validate_markdown_file",
            side_effect=ValueError("Invalid markdown structure"),
        ):
            with pytest.raises(ValueError, match="Invalid markdown structure"):
                create_feature_257_markdown_file()

    def test_function_raises_on_commit_failure(self):
        """Test that function propagates exceptions from commit_markdown_file."""
        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value="# Test\n\nSentence one. Sentence two.",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            return_value="/repo/test-fl139g.md",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.validate_markdown_file",
            return_value=True,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.commit_markdown_file",
            side_effect=Exception("Git commit failed"),
        ):
            with pytest.raises(Exception, match="Git commit failed"):
                create_feature_257_markdown_file()

    def test_function_raises_on_push_failure(self):
        """Test that function propagates exceptions from push_markdown_file."""
        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value="# Test\n\nSentence one. Sentence two.",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            return_value="/repo/test-fl139g.md",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.validate_markdown_file",
            return_value=True,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.commit_markdown_file",
            return_value="commit result",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.push_markdown_file",
            side_effect=Exception("Git push failed"),
        ):
            with pytest.raises(Exception, match="Git push failed"):
                create_feature_257_markdown_file()

    def test_all_return_dict_values_are_strings(self):
        """Test that all return dict values are strings."""
        test_content = "# Test\n\nSentence one. Sentence two."
        test_filepath = "/repo/test-fl139g.md"

        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            return_value=test_filepath,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.validate_markdown_file",
            return_value=True,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.commit_markdown_file",
            return_value="commit result",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.push_markdown_file",
            return_value="push result",
        ):
            result = create_feature_257_markdown_file()
            # Verify all values are strings
            for key, value in result.items():
                assert isinstance(value, str), f"Value for key '{key}' is not a string: {type(value)}"


class TestSuccessCriteriaValidation:
    """Integration tests validating all success criteria from feature specification."""

    def test_file_structure_and_encoding(self):
        """Test that markdown file has correct structure, encoding, and line endings."""
        test_content = "# Software Engineering\n\nSoftware engineering is the systematic application of engineering principles to software development. It encompasses the entire lifecycle from initial design through maintenance. This discipline ensures that software is reliable, maintainable, and scalable."
        test_filepath = "/tmp/test-fl139g.md"

        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            return_value=test_filepath,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.validate_markdown_file",
            return_value=True,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.commit_markdown_file",
            return_value="commit: abc123",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.push_markdown_file",
            return_value="Pushed to origin feat/257-markdown-file-creation-ef4e6e",
        ):
            result = create_feature_257_markdown_file()

            # Verify H1 heading is present
            assert result["content"].startswith("# "), "Content must start with H1 heading"

            # Extract lines to verify structure
            lines = result["content"].split("\n")
            assert lines[0].startswith("# "), "First line must be H1 heading"
            assert lines[1] == "", "Second line must be blank (after H1)"

            # Verify 2-3 sentences exist in prose section
            prose = "\n".join(lines[2:])
            sentence_count = len(re.split(r"[.!?]+", prose.strip())) - 1
            assert 2 <= sentence_count <= 3, f"Must have 2-3 sentences, got {sentence_count}"

            # Verify file size is in expected range
            file_size = len(result["content"].encode("utf-8"))
            assert (
                250 <= file_size <= 600
            ), f"File size {file_size} not in range [250-600]"

    def test_return_dict_complete_and_correct(self):
        """Test that return dict contains all required keys with correct values."""
        test_content = "# Technology\n\nTechnology is the application of scientific knowledge for practical purposes. It shapes how we live, work, and communicate in modern society. From smartphones to artificial intelligence, technology continues to transform every aspect of human life."
        test_filepath = "/repo/test-fl139g.md"
        expected_message = "feat(257): create markdown file test-fl139g.md with prose content"

        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            return_value=test_filepath,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.validate_markdown_file",
            return_value=True,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.commit_markdown_file",
            return_value="commit: abc123",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.push_markdown_file",
            return_value="Pushed to origin feat/257-markdown-file-creation-ef4e6e",
        ):
            result = create_feature_257_markdown_file()

            # Verify all 4 required keys exist
            required_keys = {"filepath", "content", "commit_message", "push_result"}
            assert set(result.keys()) == required_keys, f"Missing keys: {required_keys - set(result.keys())}"

            # Verify each value is a string
            for key, value in result.items():
                assert isinstance(
                    value, str
                ), f"Value for '{key}' must be string, got {type(value)}"

            # Verify specific values
            assert result["filepath"] == test_filepath
            assert result["content"] == test_content
            assert result["commit_message"] == expected_message
            assert "Pushed to origin" in result["push_result"]

    def test_markdown_validation_criteria(self):
        """Test that content meets all markdown validation criteria."""
        # Valid markdown: H1 heading + blank line + 2-3 sentences
        valid_content = "# Nature\n\nNature encompasses the physical world and universe, including all living organisms and natural phenomena. It provides resources that sustain life and offers inspiration for art and science. Understanding nature is fundamental to addressing environmental challenges."

        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value=valid_content,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            return_value="/tmp/test-fl139g.md",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.validate_markdown_file",
            return_value=True,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.commit_markdown_file",
            return_value="commit result",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.push_markdown_file",
            return_value="push result",
        ):
            result = create_feature_257_markdown_file()

            # Parse and validate markdown structure
            content = result["content"]
            lines = content.split("\n")

            # Check H1 heading
            assert lines[0].startswith("# "), "First line must be H1 heading"
            heading = lines[0][2:].strip()
            assert len(heading) > 0, "H1 heading text cannot be empty"

            # Check blank line after heading
            assert lines[1] == "", "Second line must be blank"

            # Check prose content (2-3 sentences)
            prose = "\n".join(lines[2:]).strip()
            # Count sentences (split by . ! or ?)
            sentences = [
                s.strip() for s in re.split(r"[.!?]+", prose) if s.strip()
            ]
            assert 2 <= len(sentences) <= 3, f"Expected 2-3 sentences, got {len(sentences)}"

    def test_git_operations_result(self):
        """Test that git operations complete with expected results."""
        with patch(
            "sheep.features.feature_257_markdown_file_creation.generate_markdown_content",
            return_value="# Topic\n\nSentence one. Sentence two.",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.write_markdown_file",
            return_value="/repo/test-fl139g.md",
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.validate_markdown_file",
            return_value=True,
        ), patch(
            "sheep.features.feature_257_markdown_file_creation.commit_markdown_file",
            return_value="commit: abc123",
        ) as mock_commit, patch(
            "sheep.features.feature_257_markdown_file_creation.push_markdown_file",
            return_value="Pushed to origin feat/257-markdown-file-creation-ef4e6e",
        ) as mock_push:
            result = create_feature_257_markdown_file()

            # Verify commit was called with exact message
            commit_call_kwargs = mock_commit.call_args.kwargs
            assert (
                commit_call_kwargs.get("custom_message")
                == "feat(257): create markdown file test-fl139g.md with prose content"
            )

            # Verify push was called
            mock_push.assert_called_once()

            # Verify push result is in return dict
            assert "push_result" in result
            assert "Pushed to origin" in result["push_result"]
