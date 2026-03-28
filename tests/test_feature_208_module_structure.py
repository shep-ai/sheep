"""Tests for feature 208 module structure and constants.

Tests verify that the feature_208_markdown_file_creation module:
1. Can be imported without errors
2. Has all required constants defined
3. Constants have correct values and types
4. Logger is properly initialized
"""

import sys
from pathlib import Path


def test_module_imports_successfully():
    """Test that feature 208 module imports without errors."""
    # Add src to path to enable imports
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import (
        BRANCH_NAME,
        COMMIT_MESSAGE,
        FEATURE_NUMBER,
        FILENAME,
        PROSE_CONTENT,
        TITLE_TEXT,
        _logger,
    )

    # Verify all constants exist
    assert FILENAME is not None
    assert FEATURE_NUMBER is not None
    assert BRANCH_NAME is not None
    assert COMMIT_MESSAGE is not None
    assert TITLE_TEXT is not None
    assert PROSE_CONTENT is not None
    assert _logger is not None


def test_filename_is_correct():
    """Test that FILENAME constant has the correct value."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import FILENAME

    assert FILENAME == "test-s4b1z3.md"


def test_feature_number_is_correct():
    """Test that FEATURE_NUMBER constant has the correct value."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import FEATURE_NUMBER

    assert FEATURE_NUMBER == 208


def test_commit_message_format():
    """Test that COMMIT_MESSAGE follows conventional commits format."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import COMMIT_MESSAGE

    assert COMMIT_MESSAGE == "feat(208): Create markdown file test-s4b1z3.md"


def test_constants_are_strings():
    """Test that all text constants are strings."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import (
        BRANCH_NAME,
        COMMIT_MESSAGE,
        FILENAME,
        PROSE_CONTENT,
        TITLE_TEXT,
    )

    assert isinstance(FILENAME, str)
    assert isinstance(BRANCH_NAME, str)
    assert isinstance(COMMIT_MESSAGE, str)
    assert isinstance(TITLE_TEXT, str)
    assert isinstance(PROSE_CONTENT, str)


def test_prose_content_is_not_empty():
    """Test that PROSE_CONTENT is not empty."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import PROSE_CONTENT

    assert len(PROSE_CONTENT) > 0


def test_title_text_is_not_empty():
    """Test that TITLE_TEXT is not empty."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import TITLE_TEXT

    assert len(TITLE_TEXT) > 0
