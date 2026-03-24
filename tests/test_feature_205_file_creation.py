"""Tests for Feature 205: File Creation & Encoding (Phase 3).

This test suite covers file creation with UTF-8 encoding and Unix LF line endings.
Tests focus on the create_markdown_file() function and its UTF-8/LF properties.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from sheep.features.feature_205_markdown_file_creation import (
    FILENAME,
    create_markdown_file,
    validate_encoding,
    validate_line_endings,
)


class TestFileCreationEncoding:
    """Tests for file creation with proper encoding and line endings."""

    def test_create_markdown_file_creates_file_at_root(self):
        """Test that create_markdown_file creates file at repository root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Mock the generation functions to return fixed content
                with patch('sheep.features.feature_205_markdown_file_creation.generate_title') as mock_title, \
                     patch('sheep.features.feature_205_markdown_file_creation.generate_prose') as mock_prose:
                    mock_title.return_value = "Test Title"
                    mock_prose.return_value = "First sentence. Second sentence. Third sentence."

                    result = create_markdown_file()

                    # Verify file was created
                    assert Path(FILENAME).exists()
                    assert result.endswith(FILENAME)
                    assert Path(result).exists()
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_uses_utf8_encoding(self):
        """Test that file is UTF-8 encoded without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                with patch('sheep.features.feature_205_markdown_file_creation.generate_title') as mock_title, \
                     patch('sheep.features.feature_205_markdown_file_creation.generate_prose') as mock_prose:
                    mock_title.return_value = "UTF-8 Test"
                    mock_prose.return_value = "First sentence. Second sentence. Third sentence."

                    create_markdown_file()

                    # Read file as binary and check for BOM
                    binary_content = Path(FILENAME).read_bytes()
                    assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

                    # Verify it can be decoded as UTF-8
                    decoded = binary_content.decode("utf-8")
                    assert isinstance(decoded, str)
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_uses_lf_line_endings(self):
        """Test that file uses Unix LF line endings, not CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                with patch('sheep.features.feature_205_markdown_file_creation.generate_title') as mock_title, \
                     patch('sheep.features.feature_205_markdown_file_creation.generate_prose') as mock_prose:
                    mock_title.return_value = "Line Ending Test"
                    mock_prose.return_value = "First sentence. Second sentence. Third sentence."

                    create_markdown_file()

                    binary_content = Path(FILENAME).read_bytes()
                    assert b"\r\n" not in binary_content, "File should not have CRLF line endings"
                    assert b"\r" not in binary_content, "File should not have CR line endings"
                    assert b"\n" in binary_content, "File should have LF line endings"
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_content_structure(self):
        """Test that file has correct markdown structure: H1 heading, blank line, prose."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                with patch('sheep.features.feature_205_markdown_file_creation.generate_title') as mock_title, \
                     patch('sheep.features.feature_205_markdown_file_creation.generate_prose') as mock_prose:
                    mock_title.return_value = "My Title"
                    mock_prose.return_value = "Prose line one. Prose line two. Prose line three."

                    create_markdown_file()

                    content = Path(FILENAME).read_text(encoding="utf-8")
                    lines = content.split("\n")

                    # First line should be H1 heading
                    assert lines[0].startswith("# "), "First line should start with '# '"
                    assert "My Title" in lines[0], "Title should be in first line"

                    # Second line should be blank
                    assert lines[1] == "", "Second line should be blank"

                    # Third line should start prose content
                    assert "Prose line one" in lines[2], "Prose should start at line 3"
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_raises_error_if_exists(self):
        """Test that FileExistsError is raised if file already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create file first
                Path(FILENAME).write_text("# Existing\n\nContent here.", encoding="utf-8")

                # Try to create it again
                with patch('sheep.features.feature_205_markdown_file_creation.generate_title') as mock_title:
                    mock_title.return_value = "Should Fail"

                    with pytest.raises(FileExistsError, match="already exists"):
                        create_markdown_file()
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_returns_absolute_path(self):
        """Test that function returns absolute path to created file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                with patch('sheep.features.feature_205_markdown_file_creation.generate_title') as mock_title, \
                     patch('sheep.features.feature_205_markdown_file_creation.generate_prose') as mock_prose:
                    mock_title.return_value = "Path Test"
                    mock_prose.return_value = "First. Second. Third."

                    result = create_markdown_file()

                    assert isinstance(result, str)
                    assert Path(result).is_absolute(), "Should return absolute path"
                    assert result.endswith(FILENAME)
            finally:
                os.chdir(original_cwd)


class TestFileEncodingValidation:
    """Tests for validate_encoding function."""

    def test_validate_encoding_accepts_utf8_no_bom(self):
        """Test that UTF-8 without BOM passes validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            content = "# Title\n\nFirst. Second. Third.\n"
            path.write_text(content, encoding="utf-8")

            # Should not raise
            validate_encoding(str(path))

    def test_validate_encoding_rejects_utf8_with_bom(self):
        """Test that UTF-8 with BOM is rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            content = "# Title\n\nFirst. Second. Third.\n"
            binary_content = b"\xef\xbb\xbf" + content.encode("utf-8")
            path.write_bytes(binary_content)

            with pytest.raises(ValueError, match="BOM"):
                validate_encoding(str(path))

    def test_validate_encoding_rejects_invalid_utf8(self):
        """Test that non-UTF-8 encoding is rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Write with latin-1 encoding (not UTF-8)
            content = "# Title\n\nFirst café. Second naïve. Third façade.\n"
            path.write_bytes(content.encode("latin-1"))

            with pytest.raises(ValueError, match="UTF-8"):
                validate_encoding(str(path))


class TestLineEndingsValidation:
    """Tests for validate_line_endings function."""

    def test_validate_line_endings_accepts_lf(self):
        """Test that Unix LF line endings pass validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            content = "# Title\n\nFirst. Second. Third.\n"
            path.write_text(content, encoding="utf-8")

            # Should not raise
            validate_line_endings(str(path))

    def test_validate_line_endings_rejects_crlf(self):
        """Test that CRLF line endings are rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            binary_content = b"# Title\r\n\r\nFirst. Second. Third.\r\n"
            path.write_bytes(binary_content)

            with pytest.raises(ValueError, match="CRLF"):
                validate_line_endings(str(path))

    def test_validate_line_endings_rejects_cr(self):
        """Test that CR line endings are rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            binary_content = b"# Title\r\r\nFirst. Second. Third.\r"
            path.write_bytes(binary_content)

            with pytest.raises(ValueError, match="CR"):
                validate_line_endings(str(path))


class TestIntegrationPhase3:
    """Integration tests for phase 3: file creation and encoding."""

    def test_file_creation_with_unicode_content(self):
        """Test that file creation handles Unicode content correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                with patch('sheep.features.feature_205_markdown_file_creation.generate_title') as mock_title, \
                     patch('sheep.features.feature_205_markdown_file_creation.generate_prose') as mock_prose:
                    mock_title.return_value = "Unicode Test: 中文 Français"
                    mock_prose.return_value = "First sentence. Second sentence with é. Third sentence with ñ."

                    create_markdown_file()

                    # Verify file exists and can be read with UTF-8
                    content = Path(FILENAME).read_text(encoding="utf-8")
                    assert "中文" in content
                    assert "é" in content
                    assert "ñ" in content

                    # Verify no BOM and LF endings
                    binary = Path(FILENAME).read_bytes()
                    assert not binary.startswith(b"\xef\xbb\xbf")
                    assert b"\r\n" not in binary
            finally:
                os.chdir(original_cwd)

    def test_created_file_passes_encoding_validation(self):
        """Test that created file passes encoding validation checks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                with patch('sheep.features.feature_205_markdown_file_creation.generate_title') as mock_title, \
                     patch('sheep.features.feature_205_markdown_file_creation.generate_prose') as mock_prose:
                    mock_title.return_value = "Validation Test"
                    mock_prose.return_value = "First. Second. Third."

                    create_markdown_file()

                    # File should pass both encoding and line ending validations
                    validate_encoding(FILENAME)
                    validate_line_endings(FILENAME)
            finally:
                os.chdir(original_cwd)
