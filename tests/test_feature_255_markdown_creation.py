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
    from sheep.features.feature_255_markdown_file_creation import (
        create_feature_255_markdown_file,
    )
    import inspect

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
