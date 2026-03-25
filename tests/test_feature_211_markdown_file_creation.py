"""Tests for feature 211 file creation functionality.

Tests verify that:
1. create_markdown_file() creates a file with the correct name
2. File contains H1 heading with TITLE_TEXT
3. File contains blank line separator
4. File contains PROSE_CONTENT
5. File uses UTF-8 encoding without BOM
6. File uses Unix LF line endings
7. File size is within specification (300-800 bytes)
"""

import sys
from pathlib import Path
import tempfile
import os


def setup_module():
    """Set up test environment by adding src to path."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


def test_create_markdown_file_returns_path():
    """Test that create_markdown_file() returns a Path object."""
    from sheep.features.feature_211_markdown_file_creation import (
        create_markdown_file,
        FILENAME,
    )

    # Change to a temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            result = create_markdown_file()
            assert isinstance(result, Path), "create_markdown_file() should return a Path object"
            assert result.name == FILENAME
        finally:
            os.chdir(original_cwd)


def test_create_markdown_file_creates_file():
    """Test that create_markdown_file() actually creates a file."""
    from sheep.features.feature_211_markdown_file_creation import (
        create_markdown_file,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # File should not exist before creation
            assert not Path(FILENAME).exists(), f"File {FILENAME} should not exist before creation"

            # Create the file
            create_markdown_file()

            # File should exist after creation
            assert Path(FILENAME).exists(), f"File {FILENAME} was not created"
        finally:
            os.chdir(original_cwd)


def test_create_markdown_file_contains_h1_heading():
    """Test that created file contains H1 heading with TITLE_TEXT."""
    from sheep.features.feature_211_markdown_file_creation import (
        create_markdown_file,
        FILENAME,
        TITLE_TEXT,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            create_markdown_file()
            content = Path(FILENAME).read_text(encoding="utf-8")

            # Check file starts with H1 heading
            expected_heading = f"# {TITLE_TEXT}"
            assert content.startswith(expected_heading), f"File should start with {expected_heading}"
        finally:
            os.chdir(original_cwd)


def test_create_markdown_file_contains_blank_line():
    """Test that created file has blank line separator."""
    from sheep.features.feature_211_markdown_file_creation import (
        create_markdown_file,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            create_markdown_file()
            content = Path(FILENAME).read_text(encoding="utf-8")
            lines = content.split("\n")

            # Check second line is blank
            assert len(lines) >= 2, "File should have at least 2 lines (heading + blank line)"
            assert lines[1] == "", "Second line should be blank"
        finally:
            os.chdir(original_cwd)


def test_create_markdown_file_contains_prose():
    """Test that created file contains prose content."""
    from sheep.features.feature_211_markdown_file_creation import (
        create_markdown_file,
        FILENAME,
        PROSE_CONTENT,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            create_markdown_file()
            content = Path(FILENAME).read_text(encoding="utf-8")

            # Check file contains prose content
            assert PROSE_CONTENT in content, "File should contain PROSE_CONTENT"
        finally:
            os.chdir(original_cwd)


def test_create_markdown_file_utf8_encoding():
    """Test that created file uses UTF-8 encoding without BOM."""
    from sheep.features.feature_211_markdown_file_creation import (
        create_markdown_file,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            create_markdown_file()

            # Read file as binary to check for BOM
            binary_content = Path(FILENAME).read_bytes()

            # Check for UTF-8 BOM (EF BB BF)
            assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

            # Check file is valid UTF-8
            binary_content.decode("utf-8")  # Should not raise
        finally:
            os.chdir(original_cwd)


def test_create_markdown_file_lf_line_endings():
    """Test that created file uses Unix LF line endings."""
    from sheep.features.feature_211_markdown_file_creation import (
        create_markdown_file,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            create_markdown_file()

            # Read file as binary to check line endings
            binary_content = Path(FILENAME).read_bytes()

            # Check for Windows CRLF
            assert b"\r\n" not in binary_content, "File should not have CRLF line endings"

            # Check for Mac CR
            assert b"\r" not in binary_content, "File should not have CR line endings"
        finally:
            os.chdir(original_cwd)


def test_create_markdown_file_size():
    """Test that created file size is within specification (300-800 bytes)."""
    from sheep.features.feature_211_markdown_file_creation import (
        create_markdown_file,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            create_markdown_file()

            file_size = Path(FILENAME).stat().st_size

            assert file_size >= 300, f"File size {file_size} is too small (minimum 300 bytes)"
            assert file_size <= 800, f"File size {file_size} is too large (maximum 800 bytes)"
        finally:
            os.chdir(original_cwd)


def test_validate_markdown_format_passes():
    """Test that validate_markdown_format() passes for valid file."""
    from sheep.features.feature_211_markdown_file_creation import (
        create_markdown_file,
        validate_markdown_format,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            create_markdown_file()
            validate_markdown_format(FILENAME)  # Should not raise
        finally:
            os.chdir(original_cwd)


def test_validate_markdown_format_rejects_missing_heading():
    """Test that validate_markdown_format() rejects file without H1 heading."""
    from sheep.features.feature_211_markdown_file_creation import (
        validate_markdown_format,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create file without H1 heading
            Path(FILENAME).write_text("No heading here\n\nJust prose.", encoding="utf-8")

            try:
                validate_markdown_format(FILENAME)
                assert False, "Should have raised ValueError for missing H1 heading"
            except ValueError as e:
                assert "H1 heading" in str(e)
        finally:
            os.chdir(original_cwd)


def test_validate_sentence_count_passes():
    """Test that validate_sentence_count() passes for 2-3 sentences."""
    from sheep.features.feature_211_markdown_file_creation import (
        create_markdown_file,
        validate_sentence_count,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            create_markdown_file()
            validate_sentence_count(FILENAME)  # Should not raise
        finally:
            os.chdir(original_cwd)


def test_validate_sentence_count_rejects_one_sentence():
    """Test that validate_sentence_count() rejects file with 1 sentence."""
    from sheep.features.feature_211_markdown_file_creation import (
        validate_sentence_count,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create file with only 1 sentence
            Path(FILENAME).write_text("# Title\n\nOnly one sentence.", encoding="utf-8")

            try:
                validate_sentence_count(FILENAME)
                assert False, "Should have raised ValueError for 1 sentence"
            except ValueError as e:
                assert "2 or 3 sentences" in str(e)
        finally:
            os.chdir(original_cwd)


def test_validate_sentence_count_rejects_four_sentences():
    """Test that validate_sentence_count() rejects file with 4 sentences."""
    from sheep.features.feature_211_markdown_file_creation import (
        validate_sentence_count,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create file with 4 sentences
            Path(FILENAME).write_text(
                "# Title\n\nFirst sentence. Second sentence. Third sentence. Fourth sentence.",
                encoding="utf-8"
            )

            try:
                validate_sentence_count(FILENAME)
                assert False, "Should have raised ValueError for 4 sentences"
            except ValueError as e:
                assert "2 or 3 sentences" in str(e)
        finally:
            os.chdir(original_cwd)


def test_validate_encoding_passes():
    """Test that validate_encoding() passes for valid UTF-8."""
    from sheep.features.feature_211_markdown_file_creation import (
        create_markdown_file,
        validate_encoding,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            create_markdown_file()
            validate_encoding(FILENAME)  # Should not raise
        finally:
            os.chdir(original_cwd)


def test_validate_line_endings_passes():
    """Test that validate_line_endings() passes for LF only."""
    from sheep.features.feature_211_markdown_file_creation import (
        create_markdown_file,
        validate_line_endings,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            create_markdown_file()
            validate_line_endings(FILENAME)  # Should not raise
        finally:
            os.chdir(original_cwd)


def test_validate_line_endings_rejects_crlf():
    """Test that validate_line_endings() rejects CRLF."""
    from sheep.features.feature_211_markdown_file_creation import (
        validate_line_endings,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create file with CRLF
            Path(FILENAME).write_bytes(b"# Title\r\n\r\nProse content.")

            try:
                validate_line_endings(FILENAME)
                assert False, "Should have raised ValueError for CRLF"
            except ValueError as e:
                assert "LF line endings" in str(e)
        finally:
            os.chdir(original_cwd)


def test_count_sentences():
    """Test count_sentences() function."""
    from sheep.features.feature_211_markdown_file_creation import count_sentences

    assert count_sentences("First. Second.") == 2
    assert count_sentences("One. Two. Three.") == 3
    assert count_sentences("Single.") == 1
    assert count_sentences("No periods here") == 0
