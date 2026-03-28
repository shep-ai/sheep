"""Tests for feature 208 validation functions.

Tests cover:
1. validate_markdown_format() - H1 heading, blank line, single heading
2. extract_prose_content() - Extract text after blank line
3. count_sentences() - Count periods in prose
4. validate_sentence_count() - Exactly 2-3 sentences
5. validate_encoding() - UTF-8 without BOM
6. validate_line_endings() - Unix LF only
7. validate_file_size() - 300-800 bytes
8. validate_markdown_file() - Master orchestration
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest


def setup_module():
    """Set up test environment by adding src to path."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


# ===== Tests for validate_markdown_format() =====

def test_validate_markdown_format_valid():
    """Test that validate_markdown_format() returns None for valid format."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_markdown_format,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create a valid markdown file
            valid_content = "# Title\n\nSome prose content.\n"
            Path(FILENAME).write_text(valid_content, encoding="utf-8")

            # Should not raise
            result = validate_markdown_format(FILENAME)
            assert result is None
        finally:
            os.chdir(original_cwd)


def test_validate_markdown_format_no_h1():
    """Test that validate_markdown_format() raises if first line missing H1."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_markdown_format,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create markdown file without H1
            invalid_content = "No heading here\n\nSome content.\n"
            Path(FILENAME).write_text(invalid_content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError):
                validate_markdown_format(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_markdown_format_no_blank_line():
    """Test that validate_markdown_format() raises if second line not blank."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_markdown_format,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create markdown file without blank line
            invalid_content = "# Title\nNo blank line.\n"
            Path(FILENAME).write_text(invalid_content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError):
                validate_markdown_format(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_markdown_format_multiple_h1():
    """Test that validate_markdown_format() raises if multiple H1 headings."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_markdown_format,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create markdown file with multiple H1 headings
            invalid_content = "# Title\n\nContent.\n# Second Heading\n"
            Path(FILENAME).write_text(invalid_content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError):
                validate_markdown_format(FILENAME)
        finally:
            os.chdir(original_cwd)


# ===== Tests for extract_prose_content() =====

def test_extract_prose_content_valid():
    """Test that extract_prose_content() extracts text after blank line."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        extract_prose_content,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            content = "# Title\n\nThis is prose content."
            Path(FILENAME).write_text(content, encoding="utf-8")

            prose = extract_prose_content(FILENAME)
            assert prose == "This is prose content."
        finally:
            os.chdir(original_cwd)


def test_extract_prose_content_empty():
    """Test that extract_prose_content() returns empty string for minimal file."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        extract_prose_content,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Minimal valid markdown file with no content after blank line
            content = "# Title\n\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            prose = extract_prose_content(FILENAME)
            assert prose == ""
        finally:
            os.chdir(original_cwd)


# ===== Tests for count_sentences() =====

def test_count_sentences_two():
    """Test that count_sentences() correctly counts 2 periods."""
    from sheep.features.feature_208_markdown_file_creation import (
        count_sentences,
    )

    result = count_sentences("First sentence. Second sentence.")
    assert result == 2


def test_count_sentences_three():
    """Test that count_sentences() correctly counts 3 periods."""
    from sheep.features.feature_208_markdown_file_creation import (
        count_sentences,
    )

    result = count_sentences("One. Two. Three.")
    assert result == 3


def test_count_sentences_zero():
    """Test that count_sentences() returns 0 for text without periods."""
    from sheep.features.feature_208_markdown_file_creation import (
        count_sentences,
    )

    result = count_sentences("No periods here")
    assert result == 0


def test_count_sentences_one():
    """Test that count_sentences() counts 1 period."""
    from sheep.features.feature_208_markdown_file_creation import (
        count_sentences,
    )

    result = count_sentences("Single sentence.")
    assert result == 1


# ===== Tests for validate_sentence_count() =====

def test_validate_sentence_count_valid_two():
    """Test that validate_sentence_count() returns None for 2 sentences."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_sentence_count,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            content = "# Title\n\nFirst sentence. Second sentence.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should not raise
            result = validate_sentence_count(FILENAME)
            assert result is None
        finally:
            os.chdir(original_cwd)


def test_validate_sentence_count_valid_three():
    """Test that validate_sentence_count() returns None for 3 sentences."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_sentence_count,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            content = "# Title\n\nOne. Two. Three.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should not raise
            result = validate_sentence_count(FILENAME)
            assert result is None
        finally:
            os.chdir(original_cwd)


def test_validate_sentence_count_one_raises():
    """Test that validate_sentence_count() raises ValueError for 1 sentence."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_sentence_count,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            content = "# Title\n\nOnly one sentence.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError):
                validate_sentence_count(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_sentence_count_four_raises():
    """Test that validate_sentence_count() raises ValueError for 4 sentences."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_sentence_count,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            content = "# Title\n\nOne. Two. Three. Four.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError):
                validate_sentence_count(FILENAME)
        finally:
            os.chdir(original_cwd)


# ===== Tests for validate_encoding() =====

def test_validate_encoding_valid():
    """Test that validate_encoding() returns None for valid UTF-8 no BOM."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_encoding,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            content = "# Title\n\nSome content.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should not raise
            result = validate_encoding(FILENAME)
            assert result is None
        finally:
            os.chdir(original_cwd)


def test_validate_encoding_bom_raises():
    """Test that validate_encoding() raises ValueError for file with UTF-8 BOM."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_encoding,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Write file with UTF-8 BOM
            content = "# Title\n\nSome content.\n"
            binary_content = b"\xef\xbb\xbf" + content.encode("utf-8")
            Path(FILENAME).write_bytes(binary_content)

            # Should raise ValueError
            with pytest.raises(ValueError):
                validate_encoding(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_encoding_invalid_utf8_raises():
    """Test that validate_encoding() raises ValueError for invalid UTF-8."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_encoding,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Write file with invalid UTF-8 bytes
            invalid_bytes = b"# Title\n\n\xff\xfe Invalid UTF-8\n"
            Path(FILENAME).write_bytes(invalid_bytes)

            # Should raise ValueError
            with pytest.raises(ValueError):
                validate_encoding(FILENAME)
        finally:
            os.chdir(original_cwd)


# ===== Tests for validate_line_endings() =====

def test_validate_line_endings_valid():
    """Test that validate_line_endings() returns None for LF-only file."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_line_endings,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            content = "# Title\n\nSome content.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should not raise
            result = validate_line_endings(FILENAME)
            assert result is None
        finally:
            os.chdir(original_cwd)


def test_validate_line_endings_crlf_raises():
    """Test that validate_line_endings() raises ValueError for CRLF."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_line_endings,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Write file with CRLF line endings
            crlf_content = b"# Title\r\n\r\nSome content.\r\n"
            Path(FILENAME).write_bytes(crlf_content)

            # Should raise ValueError
            with pytest.raises(ValueError):
                validate_line_endings(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_line_endings_cr_raises():
    """Test that validate_line_endings() raises ValueError for CR."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_line_endings,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Write file with CR line endings
            cr_content = b"# Title\r\rSome content.\r"
            Path(FILENAME).write_bytes(cr_content)

            # Should raise ValueError
            with pytest.raises(ValueError):
                validate_line_endings(FILENAME)
        finally:
            os.chdir(original_cwd)


# ===== Tests for validate_file_size() =====

def test_validate_file_size_valid():
    """Test that validate_file_size() returns None for valid size (300-800)."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_file_size,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create a file with valid size (around 400+ bytes)
            content = (
                "# Title\n\n"
                "This is the first sentence with substantial content. "
                "This is the second sentence continuing the narrative. "
                "This is the third sentence adding more information. "
                "The content needs to be long enough to meet the minimum 300 byte requirement. "
                "Additional text is included here to ensure the file is sufficiently sized.\n"
            )
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should not raise
            result = validate_file_size(FILENAME)
            assert result is None
        finally:
            os.chdir(original_cwd)


def test_validate_file_size_too_small_raises():
    """Test that validate_file_size() raises ValueError for file < 300 bytes."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_file_size,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create a file smaller than 300 bytes
            content = "# Title\n\nShort.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError):
                validate_file_size(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_file_size_too_large_raises():
    """Test that validate_file_size() raises ValueError for file > 800 bytes."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_file_size,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create a file larger than 800 bytes
            content = "# Title\n\n" + "x" * 1000 + "\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError):
                validate_file_size(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_file_size_custom_range():
    """Test that validate_file_size() accepts custom min/max parameters."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_file_size,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create a file with 50 bytes
            content = "# Title\n\nSmall.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should pass with custom min/max
            result = validate_file_size(FILENAME, min_bytes=10, max_bytes=100)
            assert result is None
        finally:
            os.chdir(original_cwd)


# ===== Tests for validate_markdown_file() orchestration =====

def test_validate_markdown_file_valid():
    """Test that validate_markdown_file() returns None for valid file."""
    from sheep.features.feature_208_markdown_file_creation import (
        create_markdown_file,
        validate_markdown_file,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create a valid markdown file
            create_markdown_file()

            # Should not raise
            result = validate_markdown_file()
            assert result is None
        finally:
            os.chdir(original_cwd)


def test_validate_markdown_file_stops_at_first_error():
    """Test that validate_markdown_file() stops at first error (fail-fast)."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_markdown_file,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create a file that fails first check (no H1)
            content = "No heading\n\nSome content.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should raise and stop at format check
            with pytest.raises(ValueError):
                validate_markdown_file(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_markdown_file_missing_file_raises():
    """Test that validate_markdown_file() raises for missing file."""
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        validate_markdown_file,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Don't create the file
            # Should raise FileNotFoundError
            with pytest.raises(FileNotFoundError):
                validate_markdown_file(FILENAME)
        finally:
            os.chdir(original_cwd)
