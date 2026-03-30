"""Tests for feature 272: Creating markdown file test-6poz5r.md with title and prose content."""

import sys
from pathlib import Path

# Test module structure and imports
def test_feature_module_can_be_imported():
    """Test that the feature module can be imported without errors."""
    import sheep.features.feature_272_markdown_file_creation as feature_module
    assert feature_module is not None


def test_feature_number_constant():
    """Test that FEATURE_NUMBER constant is defined and equals 272."""
    from sheep.features.feature_272_markdown_file_creation import FEATURE_NUMBER
    assert FEATURE_NUMBER == 272


def test_feature_name_constant():
    """Test that FEATURE_NAME constant is defined and equals markdown-file-creation-f39da9."""
    from sheep.features.feature_272_markdown_file_creation import FEATURE_NAME
    assert FEATURE_NAME == "markdown-file-creation-f39da9"


def test_markdown_filename_constant():
    """Test that MARKDOWN_FILENAME constant is defined and equals test-6poz5r.md."""
    from sheep.features.feature_272_markdown_file_creation import MARKDOWN_FILENAME
    assert MARKDOWN_FILENAME == "test-6poz5r.md"


def test_function_exists_and_is_callable():
    """Test that create_feature_272_markdown_file function exists and is callable."""
    from sheep.features.feature_272_markdown_file_creation import create_feature_272_markdown_file
    assert callable(create_feature_272_markdown_file)


def test_function_has_docstring():
    """Test that create_feature_272_markdown_file has a docstring."""
    from sheep.features.feature_272_markdown_file_creation import create_feature_272_markdown_file
    assert create_feature_272_markdown_file.__doc__ is not None
    assert "Create markdown file for feature 272" in create_feature_272_markdown_file.__doc__


def test_all_necessary_imports_present():
    """Test that all necessary imports are available in the feature module."""
    from sheep.features import feature_272_markdown_file_creation

    # Check that required modules are imported
    assert hasattr(feature_272_markdown_file_creation, 'Path')
    assert hasattr(feature_272_markdown_file_creation, 'generate_markdown_content')
    assert hasattr(feature_272_markdown_file_creation, 'write_markdown_file')
    assert hasattr(feature_272_markdown_file_creation, 'validate_markdown_file')
    assert hasattr(feature_272_markdown_file_creation, 'commit_markdown_file')
    assert hasattr(feature_272_markdown_file_creation, 'push_markdown_file')
    assert hasattr(feature_272_markdown_file_creation, 'get_logger')


def test_logger_is_initialized():
    """Test that the logger is initialized."""
    from sheep.features import feature_272_markdown_file_creation
    assert hasattr(feature_272_markdown_file_creation, '_logger')
    assert feature_272_markdown_file_creation._logger is not None
