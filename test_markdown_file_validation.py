"""
Comprehensive test suite for markdown file validation (feature 239).

This module provides test coverage for:
- File encoding validation (UTF-8 without BOM)
- Line ending validation (Unix LF, no Windows CRLF)
- File structure validation (H1 heading + blank line + prose)
- File size validation (300-600 byte range)
"""

import tempfile
from pathlib import Path
from unittest import mock

import pytest

# Import the validation functions from the implementation script
from create_test_4ulmku import create_file, validate_file, FILENAME


# ============================================================================
# Test Classes for File Encoding and Line Endings
# ============================================================================

class TestFileEncoding:
    """Tests for UTF-8 encoding validation (no BOM)."""

    def test_file_uses_utf8_encoding(self):
        """Test that created file is valid UTF-8 encoded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_file()

                # Read as binary
                binary_content = Path(FILENAME).read_bytes()

                # Verify it can be decoded as UTF-8
                try:
                    decoded = binary_content.decode('utf-8')
                    assert isinstance(decoded, str)
                except UnicodeDecodeError:
                    pytest.fail("File is not valid UTF-8")
            finally:
                os.chdir(original_cwd)

    def test_file_has_no_utf8_bom(self):
        """Test that file does not have UTF-8 BOM (Byte Order Mark)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_file()

                binary_content = Path(FILENAME).read_bytes()
                # UTF-8 BOM is b'\xef\xbb\xbf'
                assert not binary_content.startswith(b'\xef\xbb\xbf'), (
                    "File should not have UTF-8 BOM"
                )
            finally:
                os.chdir(original_cwd)

    def test_file_starts_with_heading_not_bom(self):
        """Test that file binary content starts with heading character, not BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_file()

                binary_content = Path(FILENAME).read_bytes()
                # First byte should be '#' (0x23), not BOM (0xef)
                assert binary_content[0] == 0x23, (
                    f"File should start with '#' (0x23), got 0x{binary_content[0]:02x}"
                )
            finally:
                os.chdir(original_cwd)


class TestLineEndings:
    """Tests for Unix LF line ending validation (no Windows CRLF)."""

    def test_file_uses_lf_line_endings(self):
        """Test that file uses Unix LF line endings, not Windows CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_file()

                binary_content = Path(FILENAME).read_bytes()
                # Should not contain CRLF (\r\n)
                assert b'\r\n' not in binary_content, (
                    "File should not have CRLF line endings"
                )
                # Should contain LF (\n)
                assert b'\n' in binary_content, (
                    "File should have LF line endings"
                )
            finally:
                os.chdir(original_cwd)

    def test_file_ends_with_lf_not_crlf(self):
        """Test that file ends with LF (0x0a), not CRLF (0x0d 0x0a)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_file()

                binary_content = Path(FILENAME).read_bytes()
                # Last byte should be LF (0x0a), not CR (0x0d)
                assert binary_content[-1] == 0x0a, (
                    f"File should end with LF (0x0a), got 0x{binary_content[-1]:02x}"
                )
                # Second to last should not be CR
                assert binary_content[-2] != 0x0d, (
                    "File should not end with CRLF (\\r\\n)"
                )
            finally:
                os.chdir(original_cwd)

    def test_no_carriage_returns_anywhere(self):
        """Test that file contains no carriage returns (0x0d) anywhere."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_file()

                binary_content = Path(FILENAME).read_bytes()
                # Should not contain any carriage returns
                assert b'\r' not in binary_content, (
                    "File should not contain any carriage returns (\\r, 0x0d)"
                )
            finally:
                os.chdir(original_cwd)

    def test_blank_line_is_double_lf(self):
        """Test that blank line after heading is represented as two LF bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_file()

                binary_content = Path(FILENAME).read_bytes()
                # After the heading line, there should be exactly two consecutive LF bytes
                # Heading ends with LF (0x0a), followed by blank line (another 0x0a)
                # So we should see b'\n\n' which is b'\x0a\x0a'
                assert b'\x0a\x0a' in binary_content, (
                    "File should contain blank line (two consecutive LF bytes)"
                )
            finally:
                os.chdir(original_cwd)


class TestFileStructure:
    """Tests for markdown file structure validation."""

    def test_file_has_h1_heading_on_first_line(self):
        """Test that file contains H1 heading on first line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_file()

                content = Path(FILENAME).read_text(encoding='utf-8')
                assert content.startswith("# "), "File should start with H1 heading"
            finally:
                os.chdir(original_cwd)

    def test_file_contains_blank_line_after_heading(self):
        """Test that file has blank line separating heading from prose."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_file()

                content = Path(FILENAME).read_text(encoding='utf-8')
                # Should contain double newline (blank line)
                assert '\n\n' in content, "File should contain blank line after heading"
            finally:
                os.chdir(original_cwd)

    def test_file_contains_prose_content(self):
        """Test that file contains 2-3 sentences of prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_file()

                content = Path(FILENAME).read_text(encoding='utf-8')
                # Count periods to estimate sentence count
                period_count = content.count('.')
                assert period_count >= 2, (
                    f"File should contain at least 2 sentences, found {period_count} periods"
                )
                assert period_count <= 4, (
                    f"File should contain at most 3 sentences, found {period_count} periods"
                )
            finally:
                os.chdir(original_cwd)

    def test_file_ends_with_newline(self):
        """Test that file ends with a newline character."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_file()

                binary_content = Path(FILENAME).read_bytes()
                # File must end with LF (\n, which is b'\n' in binary)
                assert binary_content.endswith(b'\n'), (
                    "File should end with a newline character"
                )
            finally:
                os.chdir(original_cwd)


class TestFileSize:
    """Tests for file size validation."""

    def test_file_size_in_typical_range(self):
        """Test that file size is approximately 300-600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                create_file()

                file_size = Path(FILENAME).stat().st_size
                # Tolerance range: 300-600 bytes
                assert 300 < file_size < 600, (
                    f"File size {file_size} bytes outside typical range (300-600)"
                )
            finally:
                os.chdir(original_cwd)


class TestValidationFunction:
    """Tests for the validate_file() function."""

    def test_validates_correctly_created_file(self):
        """Test that validate_file() passes for correctly created file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                filepath = create_file()

                result = validate_file(filepath)
                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_rejects_file_with_bom(self):
        """Test that validate_file() rejects file with UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test_with_bom.md"
            content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            # Write with BOM using utf-8-sig encoding
            path.write_bytes(content.encode('utf-8-sig'))

            with pytest.raises(AssertionError, match="BOM"):
                validate_file(path)

    def test_rejects_file_with_crlf(self):
        """Test that validate_file() rejects file with Windows CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test_with_crlf.md"
            content = "# Title\r\n\r\nFirst sentence. Second sentence. Third sentence.\r\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="CRLF"):
                validate_file(path)


class TestIntegration:
    """Integration tests for file creation and validation."""

    def test_create_and_validate_workflow(self):
        """Test complete workflow: create file and validate it."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                # Create file
                filepath = create_file()
                assert filepath.exists()

                # Validate file
                result = validate_file(filepath)
                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_encoding_and_line_endings_together(self):
        """Test that created file has correct encoding AND line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                filepath = create_file()

                binary_content = filepath.read_bytes()

                # Check encoding (no BOM)
                assert not binary_content.startswith(b'\xef\xbb\xbf'), (
                    "File should not have UTF-8 BOM"
                )

                # Check it's valid UTF-8
                try:
                    text_content = binary_content.decode('utf-8')
                    assert isinstance(text_content, str)
                except UnicodeDecodeError:
                    pytest.fail("File is not valid UTF-8")

                # Check line endings (LF only, no CRLF)
                assert b'\r\n' not in binary_content, (
                    "File should not have CRLF line endings"
                )
                assert b'\n' in binary_content, (
                    "File should have LF line endings"
                )
            finally:
                os.chdir(original_cwd)
