"""Tests for feature 207 file creation functionality.

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
    from sheep.features.feature_207_markdown_file_creation import (
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
    from sheep.features.feature_207_markdown_file_creation import (
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
    from sheep.features.feature_207_markdown_file_creation import (
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
    from sheep.features.feature_207_markdown_file_creation import (
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
            assert len(lines) >= 2, "File should have at least 2 lines"
            assert lines[1].strip() == "", f"Second line should be blank, got: '{lines[1]}'"
        finally:
            os.chdir(original_cwd)


def test_create_markdown_file_contains_prose():
    """Test that created file contains PROSE_CONTENT."""
    from sheep.features.feature_207_markdown_file_creation import (
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

            assert PROSE_CONTENT in content, f"File should contain PROSE_CONTENT"
        finally:
            os.chdir(original_cwd)


def test_create_markdown_file_uses_utf8_encoding():
    """Test that created file uses UTF-8 encoding without BOM."""
    from sheep.features.feature_207_markdown_file_creation import (
        create_markdown_file,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            create_markdown_file()
            binary_content = Path(FILENAME).read_bytes()

            # Check no UTF-8 BOM
            assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

            # Check valid UTF-8
            binary_content.decode("utf-8")  # Should not raise
        finally:
            os.chdir(original_cwd)


def test_create_markdown_file_uses_lf_line_endings():
    """Test that created file uses Unix LF line endings."""
    from sheep.features.feature_207_markdown_file_creation import (
        create_markdown_file,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            create_markdown_file()
            binary_content = Path(FILENAME).read_bytes()

            # Check no CRLF (Windows line endings)
            assert b"\r\n" not in binary_content, "File should not contain CRLF line endings"

            # Check no CR (old Mac line endings)
            assert b"\r" not in binary_content, "File should not contain CR line endings"
        finally:
            os.chdir(original_cwd)


def test_create_markdown_file_size_in_range():
    """Test that created file size is within specification (300-800 bytes)."""
    from sheep.features.feature_207_markdown_file_creation import (
        create_markdown_file,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            create_markdown_file()
            file_size = Path(FILENAME).stat().st_size

            assert (
                300 <= file_size <= 800
            ), f"File size {file_size} bytes should be between 300-800 bytes"
        finally:
            os.chdir(original_cwd)
