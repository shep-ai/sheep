"""Tests for feature 208 module structure and constants.

Tests verify that the feature_208_markdown_file_creation module:
1. Can be imported without errors
2. Has all required constants defined
3. Constants have correct values and types
4. Logger is properly initialized
5. Claude API prompt is defined
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
        FILENAME,
        FEATURE_NUMBER,
        BRANCH_NAME,
        COMMIT_MESSAGE,
        _logger,
    )

    # Verify all constants exist
    assert FILENAME is not None
    assert FEATURE_NUMBER is not None
    assert BRANCH_NAME is not None
    assert COMMIT_MESSAGE is not None
    assert _logger is not None


def test_filename_is_correct():
    """Test that FILENAME constant has the correct value for feature 208."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import FILENAME

    assert FILENAME == "test-mujic0.md"


def test_feature_number_is_correct():
    """Test that FEATURE_NUMBER constant has the correct value."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import FEATURE_NUMBER

    assert FEATURE_NUMBER == 208


def test_branch_name_is_correct():
    """Test that BRANCH_NAME constant has the correct value."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import BRANCH_NAME

    assert BRANCH_NAME == "feat/markdown-file-creation-9f7556"


def test_commit_message_format():
    """Test that COMMIT_MESSAGE follows conventional commits format."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import COMMIT_MESSAGE

    assert "feat(208)" in COMMIT_MESSAGE
    assert "test-mujic0.md" in COMMIT_MESSAGE


def test_constants_are_strings():
    """Test that all text constants are strings."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        BRANCH_NAME,
        COMMIT_MESSAGE,
    )

    assert isinstance(FILENAME, str)
    assert isinstance(BRANCH_NAME, str)
    assert isinstance(COMMIT_MESSAGE, str)


def test_markdown_generation_prompt_exists():
    """Test that MARKDOWN_GENERATION_PROMPT is defined."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import (
        MARKDOWN_GENERATION_PROMPT,
    )

    assert MARKDOWN_GENERATION_PROMPT is not None
    assert isinstance(MARKDOWN_GENERATION_PROMPT, str)
    assert len(MARKDOWN_GENERATION_PROMPT) > 0
