"""Tests for feature 255: markdown file creation with Claude API content generation.

Tests verify that:
1. Feature module imports successfully
2. Module constants are defined correctly
3. Logger is instantiated at module level
4. Main function is properly defined and callable
"""

import sys
from pathlib import Path

# Add src to path to enable imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def test_feature_255_module_imports():
    """Test that feature 255 module imports without errors."""
    from sheep.features.feature_255_markdown_file_creation import (
        FEATURE_NAME,
        FEATURE_NUMBER,
        MARKDOWN_FILENAME,
        _logger,
        create_feature_255_markdown_file,
    )

    assert FEATURE_NUMBER == 255
    assert FEATURE_NAME == "markdown-file-creation-acee8f"
    assert MARKDOWN_FILENAME == "test-zbl9x9.md"
    assert create_feature_255_markdown_file is not None
    assert _logger is not None


def test_feature_255_logger_is_available():
    """Test that logger is instantiated at module level."""
    from sheep.features.feature_255_markdown_file_creation import _logger

    # Logger should be available and callable
    assert hasattr(_logger, "info")
    assert hasattr(_logger, "debug")
    assert hasattr(_logger, "error")


def test_feature_255_function_signature():
    """Test that create_feature_255_markdown_file function has correct signature."""
    import inspect

    from sheep.features.feature_255_markdown_file_creation import (
        create_feature_255_markdown_file,
    )

    sig = inspect.signature(create_feature_255_markdown_file)

    # Function should accept optional repo_path parameter
    assert "repo_path" in sig.parameters
    param = sig.parameters["repo_path"]
    assert param.default is None


def test_feature_255_feature_number_constant():
    """Test that FEATURE_NUMBER constant is correct."""
    from sheep.features.feature_255_markdown_file_creation import FEATURE_NUMBER

    assert FEATURE_NUMBER == 255
    assert isinstance(FEATURE_NUMBER, int)


def test_feature_255_markdown_filename_constant():
    """Test that MARKDOWN_FILENAME constant is correct."""
    from sheep.features.feature_255_markdown_file_creation import MARKDOWN_FILENAME

    assert MARKDOWN_FILENAME == "test-zbl9x9.md"
    assert isinstance(MARKDOWN_FILENAME, str)
    assert MARKDOWN_FILENAME.endswith(".md")


def test_feature_255_feature_name_constant():
    """Test that FEATURE_NAME constant is correct."""
    from sheep.features.feature_255_markdown_file_creation import FEATURE_NAME

    assert FEATURE_NAME == "markdown-file-creation-acee8f"
    assert isinstance(FEATURE_NAME, str)


def test_feature_255_module_has_docstring():
    """Test that module has a proper docstring."""
    from sheep.features import feature_255_markdown_file_creation

    assert feature_255_markdown_file_creation.__doc__ is not None
    assert "feature 255" in feature_255_markdown_file_creation.__doc__.lower()
    assert "test-zbl9x9.md" in feature_255_markdown_file_creation.__doc__


def test_feature_255_function_has_docstring():
    """Test that create_feature_255_markdown_file function has a proper docstring."""
    from sheep.features.feature_255_markdown_file_creation import (
        create_feature_255_markdown_file,
    )

    assert create_feature_255_markdown_file.__doc__ is not None
    assert "feature 255" in create_feature_255_markdown_file.__doc__.lower()


class TestFeature255Integration:
    """Integration tests for feature 255 core functionality with mocks."""

    def test_create_feature_255_returns_dict(self, tmp_path, monkeypatch):
        """Test that create_feature_255_markdown_file returns a dictionary."""
        import unittest.mock as mock

        monkeypatch.chdir(tmp_path)

        # Mock the Claude API and git operations at the module where they're used
        mock_content = "# Test Title\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with mock.patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content") as mock_gen, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.commit_markdown_file") as mock_commit, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.push_markdown_file") as mock_push:

            mock_gen.return_value = mock_content
            mock_commit.return_value = "commit result"
            mock_push.return_value = "push result"

            from sheep.features.feature_255_markdown_file_creation import (
                create_feature_255_markdown_file,
            )

            result = create_feature_255_markdown_file()

            assert isinstance(result, dict)

    def test_create_feature_255_return_value_has_required_fields(self, tmp_path, monkeypatch):
        """Test that return dict has all required fields."""
        import unittest.mock as mock

        monkeypatch.chdir(tmp_path)

        mock_content = "# Test Title\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with mock.patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content") as mock_gen, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.commit_markdown_file") as mock_commit, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.push_markdown_file") as mock_push:

            mock_gen.return_value = mock_content
            mock_commit.return_value = "commit result"
            mock_push.return_value = "push result"

            from sheep.features.feature_255_markdown_file_creation import (
                create_feature_255_markdown_file,
            )

            result = create_feature_255_markdown_file()

            required_fields = ["filepath", "content", "commit_message", "push_result"]
            for field in required_fields:
                assert field in result, f"Missing required field: {field}"

    def test_create_feature_255_file_created(self, tmp_path, monkeypatch):
        """Test that markdown file is created in repository root."""
        import unittest.mock as mock

        monkeypatch.chdir(tmp_path)

        mock_content = "# Test Title\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with mock.patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content") as mock_gen, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.commit_markdown_file") as mock_commit, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.push_markdown_file") as mock_push:

            mock_gen.return_value = mock_content
            mock_commit.return_value = "commit result"
            mock_push.return_value = "push result"

            from sheep.features.feature_255_markdown_file_creation import (
                MARKDOWN_FILENAME,
                create_feature_255_markdown_file,
            )

            result = create_feature_255_markdown_file()
            file_path = Path(result["filepath"])

            assert file_path.exists(), "File should exist after creation"
            assert file_path.name == MARKDOWN_FILENAME, "File should have correct name"

    def test_create_feature_255_generated_content_starts_with_h1(self, tmp_path, monkeypatch):
        """Test that generated content starts with H1 heading."""
        import unittest.mock as mock

        monkeypatch.chdir(tmp_path)

        mock_content = "# Test Title\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with mock.patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content") as mock_gen, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.commit_markdown_file") as mock_commit, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.push_markdown_file") as mock_push:

            mock_gen.return_value = mock_content
            mock_commit.return_value = "commit result"
            mock_push.return_value = "push result"

            from sheep.features.feature_255_markdown_file_creation import (
                create_feature_255_markdown_file,
            )

            result = create_feature_255_markdown_file()
            content = result["content"]

            assert content.startswith("# "), "Content should start with H1 heading"

    def test_create_feature_255_content_length_reasonable(self, tmp_path, monkeypatch):
        """Test that generated content has reasonable length."""
        import unittest.mock as mock

        monkeypatch.chdir(tmp_path)

        mock_content = "# Quantum Computing\n\nQuantum computing represents a fundamental shift in how we process information by leveraging the principles of quantum mechanics. This technology enables quantum bits to exist in superposition states, allowing for exponential speedup in solving certain computational problems. Applications range from cryptography and drug discovery to optimization and financial modeling.\n"

        with mock.patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content") as mock_gen, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.commit_markdown_file") as mock_commit, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.push_markdown_file") as mock_push:

            mock_gen.return_value = mock_content
            mock_commit.return_value = "commit result"
            mock_push.return_value = "push result"

            from sheep.features.feature_255_markdown_file_creation import (
                create_feature_255_markdown_file,
            )

            result = create_feature_255_markdown_file()
            content = result["content"]

            # Content should be between 50-1000 characters (reasonable range)
            assert 50 <= len(content) <= 1000, "Content length should be reasonable"

    def test_create_feature_255_commit_message_format(self, tmp_path, monkeypatch):
        """Test that commit message follows conventional format."""
        import unittest.mock as mock

        monkeypatch.chdir(tmp_path)

        mock_content = "# Test Title\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with mock.patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content") as mock_gen, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.commit_markdown_file") as mock_commit, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.push_markdown_file") as mock_push:

            mock_gen.return_value = mock_content
            mock_commit.return_value = "commit result"
            mock_push.return_value = "push result"

            from sheep.features.feature_255_markdown_file_creation import (
                create_feature_255_markdown_file,
            )

            result = create_feature_255_markdown_file()
            commit_message = result["commit_message"]

            assert commit_message.startswith("feat(255):"), "Commit message should start with feat(255):"
            assert "test-zbl9x9.md" in commit_message, "Commit message should contain filename"

    def test_create_feature_255_file_utf8_encoding(self, tmp_path, monkeypatch):
        """Test that file uses UTF-8 encoding without BOM."""
        import unittest.mock as mock

        monkeypatch.chdir(tmp_path)

        mock_content = "# Test Title\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with mock.patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content") as mock_gen, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.commit_markdown_file") as mock_commit, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.push_markdown_file") as mock_push:

            mock_gen.return_value = mock_content
            mock_commit.return_value = "commit result"
            mock_push.return_value = "push result"

            from sheep.features.feature_255_markdown_file_creation import (
                create_feature_255_markdown_file,
            )

            result = create_feature_255_markdown_file()
            file_path = Path(result["filepath"])

            # Read file as binary
            with open(file_path, "rb") as f:
                raw_bytes = f.read()

            # Check for UTF-8 BOM (should not be present)
            assert not raw_bytes.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

            # Check that file is valid UTF-8
            try:
                raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                assert False, "File should be valid UTF-8"

    def test_create_feature_255_file_lf_line_endings(self, tmp_path, monkeypatch):
        """Test that file uses Unix LF line endings only."""
        import unittest.mock as mock

        monkeypatch.chdir(tmp_path)

        mock_content = "# Test Title\n\nThis is test sentence one. This is test sentence two. This is test sentence three.\n"

        with mock.patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content") as mock_gen, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.commit_markdown_file") as mock_commit, \
             mock.patch("sheep.features.feature_255_markdown_file_creation.push_markdown_file") as mock_push:

            mock_gen.return_value = mock_content
            mock_commit.return_value = "commit result"
            mock_push.return_value = "push result"

            from sheep.features.feature_255_markdown_file_creation import (
                create_feature_255_markdown_file,
            )

            result = create_feature_255_markdown_file()
            file_path = Path(result["filepath"])

            # Read file as binary
            with open(file_path, "rb") as f:
                raw_bytes = f.read()

            # Check for Windows CRLF (should not be present)
            assert b"\r\n" not in raw_bytes, "File should not have CRLF line endings"
