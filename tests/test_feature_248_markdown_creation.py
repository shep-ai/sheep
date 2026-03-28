"""Tests for feature 248: markdown file creation with Claude API content generation.

Tests verify that:
1. Feature module imports without errors
2. Feature metadata is correctly set
3. Function signature and return type are correct
4. Function can be called (basic integration test)
"""

import sys
from pathlib import Path

# Add src to path to enable imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def test_feature_248_module_imports():
    """Test that feature 248 module imports without errors."""
    from sheep.features.feature_248_markdown_file_creation import (
        FEATURE_NAME,
        FEATURE_NUMBER,
        MARKDOWN_FILENAME,
        _logger,
        create_feature_248_markdown_file,
    )

    assert FEATURE_NUMBER == 248
    assert FEATURE_NAME == "markdown-file-creation-d30daa"
    assert MARKDOWN_FILENAME == "test-0v8cee.md"
    assert create_feature_248_markdown_file is not None
    assert _logger is not None


def test_feature_248_function_signature():
    """Test that create_feature_248_markdown_file has correct signature."""
    import inspect

    from sheep.features.feature_248_markdown_file_creation import (
        create_feature_248_markdown_file,
    )

    sig = inspect.signature(create_feature_248_markdown_file)

    # Check parameters
    params = list(sig.parameters.keys())
    assert "repo_path" in params

    # Check default value for repo_path
    assert sig.parameters["repo_path"].default is None


def test_feature_248_return_type():
    """Test that create_feature_248_markdown_file returns a dictionary with expected keys."""
    import os
    import tempfile
    from unittest import mock

    from sheep.features.feature_248_markdown_file_creation import (
        create_feature_248_markdown_file,
    )

    # Sample markdown content for testing
    sample_markdown = "# Test Title\n\nThis is the first sentence. This is the second sentence. This is the third sentence.\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            # Mock the content generation and git operations
            with mock.patch("sheep.features.feature_248_markdown_file_creation.generate_markdown_content") as mock_gen, \
                 mock.patch("sheep.features.feature_248_markdown_file_creation.write_markdown_file") as mock_write, \
                 mock.patch("sheep.features.feature_248_markdown_file_creation.validate_markdown_file") as mock_validate, \
                 mock.patch("sheep.features.feature_248_markdown_file_creation.commit_markdown_file") as mock_commit, \
                 mock.patch("sheep.features.feature_248_markdown_file_creation.push_markdown_file") as mock_push:

                # Configure mocks
                mock_gen.return_value = sample_markdown
                mock_write.return_value = "test-0v8cee.md"
                mock_validate.return_value = True
                mock_commit.return_value = {"commit": "abc123"}
                mock_push.return_value = {"pushed": True}

                result = create_feature_248_markdown_file(tmpdir)

                # Verify return type and keys
                assert isinstance(result, dict)
                assert "filepath" in result
                assert "content" in result
                assert "commit_message" in result
                assert "push_result" in result

                # Verify values
                assert result["filepath"] == "test-0v8cee.md"
                assert result["content"] == sample_markdown
                assert "feat(248):" in result["commit_message"]
                assert "test-0v8cee.md" in result["commit_message"]
        finally:
            os.chdir(original_cwd)


def test_feature_248_commit_message_format():
    """Test that commit message follows conventional format."""
    import os
    import tempfile
    from unittest import mock

    from sheep.features.feature_248_markdown_file_creation import (
        FEATURE_NUMBER,
        MARKDOWN_FILENAME,
        create_feature_248_markdown_file,
    )

    sample_markdown = "# Test\n\nOne. Two. Three.\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            with mock.patch("sheep.features.feature_248_markdown_file_creation.generate_markdown_content") as mock_gen, \
                 mock.patch("sheep.features.feature_248_markdown_file_creation.write_markdown_file") as mock_write, \
                 mock.patch("sheep.features.feature_248_markdown_file_creation.validate_markdown_file") as mock_validate, \
                 mock.patch("sheep.features.feature_248_markdown_file_creation.commit_markdown_file") as mock_commit, \
                 mock.patch("sheep.features.feature_248_markdown_file_creation.push_markdown_file") as mock_push:

                mock_gen.return_value = sample_markdown
                mock_write.return_value = MARKDOWN_FILENAME
                mock_validate.return_value = True
                mock_commit.return_value = {"commit": "abc123"}
                mock_push.return_value = {"pushed": True}

                result = create_feature_248_markdown_file(tmpdir)

                # Verify conventional commit format (lowercase "create")
                expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
                assert result["commit_message"] == expected_message
        finally:
            os.chdir(original_cwd)
