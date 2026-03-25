"""Tests for feature 208 verify_file_exists() functionality.

Tests verify that:
1. verify_file_exists() returns None when file exists
2. verify_file_exists() raises FileNotFoundError when file missing
3. Error message is clear and identifies the missing file
4. Function accepts custom filename parameter
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


def test_verify_file_exists_returns_none():
    """Test that verify_file_exists() returns None when file exists."""
    from sheep.features.feature_208_markdown_file_creation import (
        verify_file_exists,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create a test file
            Path(FILENAME).write_text("test content")

            # Should not raise, should return None
            result = verify_file_exists(FILENAME)
            assert result is None
        finally:
            os.chdir(original_cwd)


def test_verify_file_exists_raises_when_missing():
    """Test that verify_file_exists() raises FileNotFoundError when file missing."""
    from sheep.features.feature_208_markdown_file_creation import (
        verify_file_exists,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # File should not exist
            assert not Path(FILENAME).exists()

            # Should raise FileNotFoundError
            with pytest.raises(FileNotFoundError):
                verify_file_exists(FILENAME)
        finally:
            os.chdir(original_cwd)


def test_verify_file_exists_error_message():
    """Test that error message is clear and identifies the missing file."""
    from sheep.features.feature_208_markdown_file_creation import (
        verify_file_exists,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Try to verify non-existent file
            with pytest.raises(FileNotFoundError) as exc_info:
                verify_file_exists(FILENAME)

            # Error message should mention the filename
            assert FILENAME in str(exc_info.value)
        finally:
            os.chdir(original_cwd)


def test_verify_file_exists_custom_filename():
    """Test that function accepts custom filename parameter."""
    from sheep.features.feature_208_markdown_file_creation import (
        verify_file_exists,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            custom_filename = "custom-file.md"

            # Create the custom file
            Path(custom_filename).write_text("test content")

            # Should work with custom filename
            result = verify_file_exists(custom_filename)
            assert result is None
        finally:
            os.chdir(original_cwd)


def test_verify_file_exists_default_filename():
    """Test that function uses FILENAME default when no parameter provided."""
    from sheep.features.feature_208_markdown_file_creation import (
        verify_file_exists,
        FILENAME,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Create the default filename
            Path(FILENAME).write_text("test content")

            # Should work with default parameter
            result = verify_file_exists()
            assert result is None
        finally:
            os.chdir(original_cwd)
