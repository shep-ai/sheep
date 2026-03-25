"""Tests for feature 208 helper functions.

Tests verify that the helper functions:
1. extract_prose_content() correctly extracts text after H1 heading and blank line
2. count_sentences() correctly counts periods in text
"""

import sys
from pathlib import Path
import tempfile
import os


def test_extract_prose_content_from_valid_markdown():
    """Test extracting prose content from valid markdown file."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import (
        extract_prose_content,
    )

    # Create temporary markdown file
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write("# Test Title\n\nThis is a sentence. This is another sentence.")
        temp_file = f.name

    try:
        prose = extract_prose_content(temp_file)
        assert prose == "This is a sentence. This is another sentence."
    finally:
        os.unlink(temp_file)


def test_extract_prose_content_with_multiple_paragraphs():
    """Test extracting prose content with multiple paragraphs."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import (
        extract_prose_content,
    )

    # Create temporary markdown file with multiple paragraphs
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write("# Test Title\n\nFirst paragraph. Second paragraph.\n\nMore text.")
        temp_file = f.name

    try:
        prose = extract_prose_content(temp_file)
        assert "First paragraph" in prose
        assert "Second paragraph" in prose
        assert "More text" in prose
    finally:
        os.unlink(temp_file)


def test_extract_prose_content_returns_empty_string_when_no_content():
    """Test that extract_prose_content returns empty string when no prose after blank line."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import (
        extract_prose_content,
    )

    # Create temporary markdown file with just title and blank line
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write("# Test Title\n\n")
        temp_file = f.name

    try:
        prose = extract_prose_content(temp_file)
        assert prose == ""
    finally:
        os.unlink(temp_file)


def test_count_sentences_with_two_periods():
    """Test counting sentences with two periods."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import count_sentences

    prose = "First sentence. Second sentence."
    assert count_sentences(prose) == 2


def test_count_sentences_with_three_periods():
    """Test counting sentences with three periods."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import count_sentences

    prose = "First sentence. Second sentence. Third sentence."
    assert count_sentences(prose) == 3


def test_count_sentences_with_no_periods():
    """Test counting sentences with no periods."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import count_sentences

    prose = "No periods here"
    assert count_sentences(prose) == 0


def test_count_sentences_with_empty_string():
    """Test counting sentences in empty string."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import count_sentences

    prose = ""
    assert count_sentences(prose) == 0
