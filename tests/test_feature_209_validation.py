"""Tests for feature 209 validation functions.

Tests cover:
1. validate_markdown_format() - H1 heading, blank line, single heading
2. extract_prose_content() - Extract text after blank line
3. count_sentences() - Count punctuation in prose
4. validate_sentence_count() - Exactly 2-3 sentences
5. validate_encoding() - UTF-8 without BOM
6. validate_line_endings() - Unix LF only
7. validate_file_size() - 300-800 bytes
8. validate_markdown_file() - Master orchestration
"""

import sys
from pathlib import Path
import tempfile
import os
import pytest


def setup_module():
    """Set up test environment by adding src to path."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


# ===== Tests for verify_file_exists() =====

def test_verify_file_exists_valid():
    """Test that verify_file_exists() returns None for existing file."""
    from sheep.features.feature_209_markdown_file_creation import (
        verify_file_exists,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create a file
            Path(FILENAME).write_text("# Title\n\nContent.\n", encoding="utf-8")

            # Should not raise
            result = verify_file_exists(FILENAME)
            assert result is None
        finally:
            os.chdir(original_cwd)


def test_verify_file_exists_missing():
    """Test that verify_file_exists() raises FileNotFoundError for missing file."""
    from sheep.features.feature_209_markdown_file_creation import (
        verify_file_exists,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # File doesn't exist
            with pytest.raises(FileNotFoundError):
                verify_file_exists(FILENAME)
        finally:
            os.chdir(original_cwd)


# ===== Tests for validate_markdown_format() =====

def test_validate_markdown_format_valid():
    """Test that validate_markdown_format() returns None for valid format."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_markdown_format,
        FILENAME,
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
    from sheep.features.feature_209_markdown_file_creation import (
        validate_markdown_format,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create markdown file without H1
            invalid_content = "No heading here\n\nSome content.\n"
            Path(FILENAME).write_text(invalid_content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError, match="must start with H1 heading"):
                validate_markdown_format(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_markdown_format_no_blank_line():
    """Test that validate_markdown_format() raises if second line not blank."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_markdown_format,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create markdown file without blank line
            invalid_content = "# Title\nNo blank line.\n"
            Path(FILENAME).write_text(invalid_content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError, match="blank line"):
                validate_markdown_format(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_markdown_format_multiple_h1():
    """Test that validate_markdown_format() raises if multiple H1 headings."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_markdown_format,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create markdown file with multiple H1
            invalid_content = "# Title\n\nContent.\n\n# Another Title\n\nMore content.\n"
            Path(FILENAME).write_text(invalid_content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError, match="exactly one H1"):
                validate_markdown_format(FILENAME)
        finally:
            os.chdir(original_cwd)


# ===== Tests for extract_prose_content() =====

def test_extract_prose_content_basic():
    """Test extract_prose_content() returns text after blank line."""
    from sheep.features.feature_209_markdown_file_creation import (
        extract_prose_content,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            content = "# Title\n\nFirst sentence. Second sentence.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            prose = extract_prose_content(FILENAME)
            assert prose == "First sentence. Second sentence."
        finally:
            os.chdir(original_cwd)


def test_extract_prose_content_multiline():
    """Test extract_prose_content() with multiline content."""
    from sheep.features.feature_209_markdown_file_creation import (
        extract_prose_content,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            content = "# Title\n\nFirst sentence.\nSecond sentence.\nThird sentence.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            prose = extract_prose_content(FILENAME)
            # Should preserve newlines and be stripped of trailing whitespace
            assert "First sentence." in prose
            assert "Second sentence." in prose
            assert "Third sentence." in prose
        finally:
            os.chdir(original_cwd)


# ===== Tests for count_sentences() =====

def test_count_sentences_periods():
    """Test count_sentences() counts periods correctly."""
    from sheep.features.feature_209_markdown_file_creation import count_sentences

    assert count_sentences("First sentence. Second sentence.") == 2
    assert count_sentences("One. Two. Three.") == 3
    assert count_sentences("No sentences") == 0


def test_count_sentences_mixed_punctuation():
    """Test count_sentences() counts all punctuation types."""
    from sheep.features.feature_209_markdown_file_creation import count_sentences

    assert count_sentences("What is this?") == 1
    assert count_sentences("Amazing!") == 1
    assert count_sentences("What? Amazing! Statement.") == 3


def test_count_sentences_empty():
    """Test count_sentences() returns 0 for empty string."""
    from sheep.features.feature_209_markdown_file_creation import count_sentences

    assert count_sentences("") == 0


# ===== Tests for validate_sentence_count() =====

def test_validate_sentence_count_two_sentences():
    """Test validate_sentence_count() passes with 2 sentences."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_sentence_count,
        FILENAME,
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


def test_validate_sentence_count_three_sentences():
    """Test validate_sentence_count() passes with 3 sentences."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_sentence_count,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            content = "# Title\n\nFirst. Second. Third.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should not raise
            result = validate_sentence_count(FILENAME)
            assert result is None
        finally:
            os.chdir(original_cwd)


def test_validate_sentence_count_one_sentence():
    """Test validate_sentence_count() raises with only 1 sentence."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_sentence_count,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            content = "# Title\n\nOnly one sentence.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError, match="2 or 3 sentences"):
                validate_sentence_count(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_sentence_count_four_sentences():
    """Test validate_sentence_count() raises with 4 sentences."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_sentence_count,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            content = "# Title\n\nFirst. Second. Third. Fourth.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError, match="2 or 3 sentences"):
                validate_sentence_count(FILENAME)
        finally:
            os.chdir(original_cwd)


# ===== Tests for validate_encoding() =====

def test_validate_encoding_valid_utf8():
    """Test validate_encoding() passes for valid UTF-8."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_encoding,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            content = "# Title\n\nContent with UTF-8 ñ é ü.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should not raise
            result = validate_encoding(FILENAME)
            assert result is None
        finally:
            os.chdir(original_cwd)


def test_validate_encoding_with_bom():
    """Test validate_encoding() raises for file with UTF-8 BOM."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_encoding,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Write file with UTF-8 BOM
            bom = b"\xef\xbb\xbf"
            content = b"# Title\n\nContent.\n"
            Path(FILENAME).write_bytes(bom + content)

            # Should raise ValueError
            with pytest.raises(ValueError, match="BOM"):
                validate_encoding(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_encoding_invalid_utf8():
    """Test validate_encoding() raises for invalid UTF-8."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_encoding,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Write invalid UTF-8 bytes
            Path(FILENAME).write_bytes(b"\x80\x81\x82\x83")

            # Should raise ValueError
            with pytest.raises(ValueError, match="UTF-8"):
                validate_encoding(FILENAME)
        finally:
            os.chdir(original_cwd)


# ===== Tests for validate_line_endings() =====

def test_validate_line_endings_lf_only():
    """Test validate_line_endings() passes for LF only."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_line_endings,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Write with explicit LF endings
            Path(FILENAME).write_bytes(b"# Title\n\nContent.\n")

            # Should not raise
            result = validate_line_endings(FILENAME)
            assert result is None
        finally:
            os.chdir(original_cwd)


def test_validate_line_endings_crlf():
    """Test validate_line_endings() raises for CRLF."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_line_endings,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Write with CRLF endings
            Path(FILENAME).write_bytes(b"# Title\r\n\r\nContent.\r\n")

            # Should raise ValueError
            with pytest.raises(ValueError, match="CRLF"):
                validate_line_endings(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_line_endings_cr():
    """Test validate_line_endings() raises for CR."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_line_endings,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Write with CR endings
            Path(FILENAME).write_bytes(b"# Title\r\rContent.\r")

            # Should raise ValueError
            with pytest.raises(ValueError, match="CR"):
                validate_line_endings(FILENAME)
        finally:
            os.chdir(original_cwd)


# ===== Tests for validate_file_size() =====

def test_validate_file_size_within_range():
    """Test validate_file_size() passes for files within range."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_file_size,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create file of 500 bytes (within 300-800)
            content = "# Title\n\n" + "x" * 480 + "\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should not raise
            result = validate_file_size(FILENAME)
            assert result is None
        finally:
            os.chdir(original_cwd)


def test_validate_file_size_too_small():
    """Test validate_file_size() raises for files < 300 bytes."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_file_size,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create small file (< 300 bytes)
            content = "# Title\n\nSmall.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError, match="too small"):
                validate_file_size(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_file_size_too_large():
    """Test validate_file_size() raises for files > 800 bytes."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_file_size,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create large file (> 800 bytes)
            content = "# Title\n\n" + "x" * 1000 + "\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError, match="too large"):
                validate_file_size(FILENAME)
        finally:
            os.chdir(original_cwd)


# ===== Tests for validate_markdown_file() =====

def test_validate_markdown_file_valid():
    """Test validate_markdown_file() passes with valid file."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_markdown_file,
        FILENAME,
        create_markdown_file,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create file using the actual feature function
            create_markdown_file()

            # Should not raise
            result = validate_markdown_file(FILENAME)
            assert result is None
        finally:
            os.chdir(original_cwd)


def test_validate_markdown_file_missing():
    """Test validate_markdown_file() fails fast on missing file."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_markdown_file,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # File doesn't exist
            with pytest.raises(FileNotFoundError):
                validate_markdown_file(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_markdown_file_invalid_format():
    """Test validate_markdown_file() fails on invalid format."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_markdown_file,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create file with invalid format
            content = "No heading\n\nContent.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError):
                validate_markdown_file(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_markdown_file_invalid_sentences():
    """Test validate_markdown_file() fails on invalid sentence count."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_markdown_file,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create file with only 1 sentence
            content = "# Title\n\nOnly one sentence.\n"
            Path(FILENAME).write_text(content, encoding="utf-8")

            # Should raise ValueError
            with pytest.raises(ValueError):
                validate_markdown_file(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_validate_markdown_file_fail_fast():
    """Test validate_markdown_file() stops at first error."""
    from sheep.features.feature_209_markdown_file_creation import (
        validate_markdown_file,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create file that will fail on first check (missing)
            # validate_markdown_file should raise FileNotFoundError, not check other validations
            with pytest.raises(FileNotFoundError):
                validate_markdown_file("nonexistent.md")
        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
