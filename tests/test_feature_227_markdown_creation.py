"""Tests for feature 227: markdown file creation with Claude API content generation.

Tests verify that:
1. Claude API generates prose content successfully
2. Generated content contains 2-3 sentences
3. Markdown file is created with proper structure
4. File has UTF-8 encoding without BOM
5. File uses Unix LF line endings
6. All validation checks pass
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

# Add src to path to enable imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


# Sample markdown content for testing (300+ bytes to match expected range)
SAMPLE_MARKDOWN = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible.\n"


@mock.patch("sheep.content_generators.get_reasoning_llm")
def test_generate_markdown_content_returns_string(mock_llm):
    """Test that generate_markdown_content() returns a non-empty string when Claude API succeeds."""
    from sheep.content_generators import generate_markdown_content

    # Mock the LLM response
    mock_instance = mock.MagicMock()
    mock_instance.call.return_value = SAMPLE_MARKDOWN
    mock_llm.return_value = mock_instance

    content = generate_markdown_content()

    assert content is not None
    assert isinstance(content, str)
    assert len(content) > 0


@mock.patch("sheep.content_generators.get_reasoning_llm")
def test_generated_content_has_h1_heading(mock_llm):
    """Test that generated content starts with H1 heading."""
    from sheep.content_generators import generate_markdown_content

    # Mock the LLM response
    mock_instance = mock.MagicMock()
    mock_instance.call.return_value = SAMPLE_MARKDOWN
    mock_llm.return_value = mock_instance

    content = generate_markdown_content()

    assert content.startswith("# "), "Content must start with '# '"


@mock.patch("sheep.content_generators.get_reasoning_llm")
def test_generated_content_contains_2_to_3_sentences(mock_llm):
    """Test that generated content contains exactly 2-3 sentences."""
    from sheep.content_generators import generate_markdown_content

    # Mock the LLM response
    mock_instance = mock.MagicMock()
    mock_instance.call.return_value = SAMPLE_MARKDOWN
    mock_llm.return_value = mock_instance

    content = generate_markdown_content()

    # Count sentences by counting periods
    sentence_count = content.count(".")
    assert sentence_count >= 2 and sentence_count <= 3, \
        f"Expected 2-3 sentences, found {sentence_count}"


@mock.patch("sheep.content_generators.get_reasoning_llm")
def test_generated_content_has_blank_line_after_heading(mock_llm):
    """Test that generated content has proper structure: heading, blank line, prose."""
    from sheep.content_generators import generate_markdown_content

    # Mock the LLM response
    mock_instance = mock.MagicMock()
    mock_instance.call.return_value = SAMPLE_MARKDOWN
    mock_llm.return_value = mock_instance

    content = generate_markdown_content()
    lines = content.split("\n")

    assert len(lines) >= 3, "Content must have at least 3 lines (heading, blank, prose)"
    assert lines[0].startswith("# "), "First line must be H1 heading"
    assert lines[1] == "", "Second line must be blank"
    assert len(lines[2]) > 0, "Third line must have prose content"


def test_write_markdown_file_creates_file():
    """Test that write_markdown_file() creates a file on disk."""
    from sheep.content_generators import write_markdown_file

    with tempfile.TemporaryDirectory() as tmpdir:
        # Change to temp directory for this test
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = write_markdown_file(SAMPLE_MARKDOWN, "test-tmp.md")

            assert Path(filepath).exists()
            assert Path(filepath).is_file()
            assert filepath.endswith("test-tmp.md")

        finally:
            os.chdir(original_cwd)


def test_file_has_utf8_encoding_without_bom():
    """Test that created file is UTF-8 encoded without BOM."""
    from sheep.content_generators import write_markdown_file

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = write_markdown_file(SAMPLE_MARKDOWN, "test-encoding.md")

            # Read file as binary and check for BOM
            with open(filepath, "rb") as f:
                binary_content = f.read()

            # UTF-8 BOM is bytes EF BB BF
            assert not binary_content.startswith(b"\xef\xbb\xbf"), \
                "File must not contain UTF-8 BOM"

            # Verify file can be decoded as UTF-8
            decoded_content = binary_content.decode("utf-8")
            assert decoded_content == SAMPLE_MARKDOWN

        finally:
            os.chdir(original_cwd)


def test_file_uses_lf_line_endings():
    """Test that created file uses Unix LF line endings, not CRLF."""
    from sheep.content_generators import write_markdown_file

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = write_markdown_file(SAMPLE_MARKDOWN, "test-lineendings.md")

            # Read file as binary and check for CRLF
            with open(filepath, "rb") as f:
                binary_content = f.read()

            assert b"\r\n" not in binary_content, \
                "File must use LF line endings, not CRLF"
            assert b"\r" not in binary_content, \
                "File must use LF line endings, not CR"

        finally:
            os.chdir(original_cwd)


def test_validate_markdown_file_passes_for_valid_file():
    """Test that validate_markdown_file() passes for properly created file."""
    from sheep.content_generators import (
        validate_markdown_file,
        write_markdown_file,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = write_markdown_file(SAMPLE_MARKDOWN, "test-validation.md")

            # This should not raise
            result = validate_markdown_file(filepath)
            assert result is True

        finally:
            os.chdir(original_cwd)


def test_file_size_in_reasonable_range():
    """Test that created file size is in the expected range (250-800 bytes)."""
    from sheep.content_generators import write_markdown_file

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = write_markdown_file(SAMPLE_MARKDOWN, "test-size.md")

            file_size = Path(filepath).stat().st_size
            assert 250 <= file_size <= 800, \
                f"File size {file_size} bytes should be in range 250-800 bytes"

        finally:
            os.chdir(original_cwd)


def test_file_ends_with_newline():
    """Test that created file ends with a newline (Unix convention)."""
    from sheep.content_generators import write_markdown_file

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = write_markdown_file(SAMPLE_MARKDOWN, "test-newline.md")

            with open(filepath, "rb") as f:
                binary_content = f.read()

            assert binary_content.endswith(b"\n"), \
                "File must end with a newline"

        finally:
            os.chdir(original_cwd)


def test_feature_227_module_imports():
    """Test that feature 227 module imports without errors."""
    from sheep.features.feature_227_markdown_file_creation import (
        FEATURE_NAME,
        FEATURE_NUMBER,
        MARKDOWN_FILENAME,
        _logger,
        create_feature_227_markdown_file,
    )

    assert FEATURE_NUMBER == 227
    assert FEATURE_NAME == "markdown-file-creation-1bf675"
    assert MARKDOWN_FILENAME == "test-arvwkm.md"
    assert create_feature_227_markdown_file is not None
    assert _logger is not None
