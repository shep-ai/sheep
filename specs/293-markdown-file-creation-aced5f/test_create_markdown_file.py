"""
Test suite for feature 293: markdown file creation with content generation.

This module provides test coverage for feature 293, which creates
a markdown file (test-msqxtg.md) with auto-generated content from Claude API,
proper structure, encoding, and line endings.

Test Coverage:
- Script imports and main() function exist
- Orchestration function returns correct result dictionary
- File is created at repository root with correct filename
- Content structure (H1 heading + blank line + prose)
- Prose content validation (2-3 sentences)
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sheep.content_generators import (
    create_markdown_file,
    validate_markdown_file,
)


def test_module_imports():
    """Test that the module can be imported without errors."""
    import create_markdown_file as module
    assert hasattr(module, 'main')
    assert callable(module.main)


def test_main_function_structure():
    """Test that main() function is properly defined."""
    import create_markdown_file as module
    # Should not raise any exceptions
    assert hasattr(module, 'main')
    assert callable(module.main)


def test_generate_markdown_content():
    """Test markdown content generation produces valid output."""
    from sheep.content_generators import generate_markdown_content

    # Generate content
    content = generate_markdown_content()

    # Verify it's not empty
    assert content
    assert len(content) > 0

    # Verify it starts with H1 heading
    assert content.lstrip().startswith("# ")

    # Verify it ends with newline
    assert content.endswith("\n")

    # Verify it has reasonable length
    assert len(content) > 50


def test_write_and_validate_markdown_file():
    """Test writing and validating a markdown file."""
    from sheep.content_generators import generate_markdown_content, write_markdown_file

    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Generate content
            content = generate_markdown_content()

            # Write file
            filename = "test-feature-293.md"
            filepath = write_markdown_file(content, filename)

            # Verify file exists
            assert Path(filepath).exists()
            assert filepath.endswith(filename)

            # Verify file is readable
            with open(filepath, 'r', encoding='utf-8') as f:
                written_content = f.read()
            assert written_content == content

        finally:
            os.chdir(original_cwd)


def test_markdown_content_has_correct_structure():
    """Test that markdown content has H1 + blank line + prose."""
    from sheep.content_generators import generate_markdown_content

    content = generate_markdown_content()
    lines = content.split("\n")

    # First line should be H1
    assert lines[0].startswith("# ")

    # Second line should be blank
    assert lines[1] == ""

    # Should have prose content after blank line
    assert len(lines) > 2


def test_prose_content_has_2_to_3_sentences():
    """Test that prose content contains 2-3 sentences."""
    from sheep.content_generators import generate_markdown_content

    content = generate_markdown_content()

    # Count periods (simple sentence count)
    sentence_count = content.count(".")

    # Should have 2-3 sentences
    assert 2 <= sentence_count <= 3


def test_create_markdown_file_returns_dict():
    """Test that create_markdown_file() returns a properly structured dict."""
    from sheep.content_generators import create_markdown_file as create_md_func

    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Mock git operations since we're in a temp directory
            with mock.patch('sheep.content_generators.commit_markdown_file') as mock_commit, \
                 mock.patch('sheep.content_generators.push_markdown_file') as mock_push:

                mock_commit.return_value = "Committed"
                mock_push.return_value = "Pushed"

                result = create_md_func("test-msqxtg.md", feature_number=293)

                # Verify result structure
                assert isinstance(result, dict)
                assert "filepath" in result
                assert "content" in result
                assert "commit_message" in result
                assert "push_result" in result

                # Verify content in result
                assert len(result["content"]) > 0
                assert result["content"].endswith("\n")

                # Verify commit message
                assert "feat(293)" in result["commit_message"]
                assert "test-msqxtg.md" in result["commit_message"]

        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    # Run tests with basic assertions
    test_module_imports()
    print("✓ test_module_imports passed")

    test_main_function_structure()
    print("✓ test_main_function_structure passed")

    test_generate_markdown_content()
    print("✓ test_generate_markdown_content passed")

    test_write_and_validate_markdown_file()
    print("✓ test_write_and_validate_markdown_file passed")

    test_markdown_content_has_correct_structure()
    print("✓ test_markdown_content_has_correct_structure passed")

    test_prose_content_has_2_to_3_sentences()
    print("✓ test_prose_content_has_2_to_3_sentences passed")

    test_create_markdown_file_returns_dict()
    print("✓ test_create_markdown_file_returns_dict passed")

    print("\nAll tests passed!")
