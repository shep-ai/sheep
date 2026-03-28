"""Tests for feature 144 Phase 2: File Creation & Persistence.

Tests for task-3 (write_markdown_file) and task-4 (validate_file_properties).
"""

import os
import tempfile
from pathlib import Path

import pytest

from sheep.content_generators import validate_file_properties, write_markdown_file


class TestWriteMarkdownFilePhase2:
    """Phase 2 tests for write_markdown_file function (task-3)."""

    def test_write_creates_file_in_cwd(self):
        """Test: write_markdown_file(content, 'test.md') creates file in cwd()."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
                result = write_markdown_file(content, "test-ghy0tt.md")

                # Verify file was created
                assert Path("test-ghy0tt.md").exists()
                assert os.path.isfile("test-ghy0tt.md")
            finally:
                os.chdir(original_cwd)

    def test_write_returns_absolute_path(self):
        """Test: returned path is absolute and points to created file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Test\n\nFirst. Second. Third.\n"
                result = write_markdown_file(content, "test.md")

                # Verify result is absolute path
                assert Path(result).is_absolute()
                assert Path(result).exists()
                assert "test.md" in result
            finally:
                os.chdir(original_cwd)

    def test_write_rejects_slash_in_filename(self):
        """Test: rejecting filename with '/' should raise ValueError."""
        content = "# Test\n\nFirst. Second. Third.\n"
        with pytest.raises(ValueError, match="Invalid filename"):
            write_markdown_file(content, "subdir/test.md")

    def test_write_rejects_backslash_in_filename(self):
        """Test: rejecting filename with '\\' should raise ValueError."""
        content = "# Test\n\nFirst. Second. Third.\n"
        with pytest.raises(ValueError, match="Invalid filename"):
            write_markdown_file(content, "subdir\\test.md")

    def test_write_rejects_dotdot_in_filename(self):
        """Test: rejecting filename starting with '..' should raise ValueError."""
        content = "# Test\n\nFirst. Second. Third.\n"
        with pytest.raises(ValueError, match="Invalid filename"):
            write_markdown_file(content, "../malicious.md")


class TestValidateFileProperties:
    """Tests for validate_file_properties function (task-4)."""

    def test_validate_accepts_valid_utf8_no_bom_lf(self):
        """Test: valid UTF-8 file (no BOM, LF only) should return True."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            content = "# Test\n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath.write_text(content, encoding="utf-8")

            result = validate_file_properties(str(filepath))
            assert result is True

    def test_validate_rejects_file_with_bom(self):
        """Test: file with BOM should raise ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            content = "# Test\n\nFirst sentence. Second sentence. Third sentence.\n"
            # Write with UTF-8 BOM
            binary_content = b"\xef\xbb\xbf" + content.encode("utf-8")
            filepath.write_bytes(binary_content)

            with pytest.raises(ValueError, match="BOM"):
                validate_file_properties(str(filepath))

    def test_validate_rejects_file_with_crlf(self):
        """Test: file with CRLF should raise ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Write with CRLF line endings
            binary_content = b"# Test\r\n\r\nFirst sentence. Second sentence. Third sentence.\r\n"
            filepath.write_bytes(binary_content)

            with pytest.raises(ValueError, match="CRLF"):
                validate_file_properties(str(filepath))

    def test_validate_rejects_nonexistent_file(self):
        """Test: non-existent file should raise ValueError."""
        with pytest.raises(ValueError, match="does not exist"):
            validate_file_properties("/nonexistent/path/test.md")

    def test_validate_accepts_lf_line_endings(self):
        """Test: file with only LF line endings should pass."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            binary_content = b"# Test\n\nFirst. Second. Third.\n"
            filepath.write_bytes(binary_content)

            result = validate_file_properties(str(filepath))
            assert result is True

    def test_validate_accepts_unicode_content(self):
        """Test: file with unicode characters should pass."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            content = "# Unicode Test\n\nSpecial chars: é, ñ, 中文. More chars: ü, ö. Final: ç.\n"
            filepath.write_text(content, encoding="utf-8")

            result = validate_file_properties(str(filepath))
            assert result is True

    def test_validate_efficient_binary_read(self):
        """Test: validation uses efficient binary read (doesn't validate markdown structure)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Content that is NOT valid markdown (missing blank line, wrong sentence count)
            # but IS valid file encoding
            content = "This is not valid markdown. It has one sentence.\n"
            filepath.write_text(content, encoding="utf-8")

            # Should pass file properties validation (no markdown structure check)
            result = validate_file_properties(str(filepath))
            assert result is True


class TestPhase2Integration:
    """Integration tests for Phase 2: File Creation & Persistence."""

    def test_write_and_validate_properties_roundtrip(self):
        """Test: content can be written and properties validated successfully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Write file
                content = "# Test\n\nFirst. Second. Third.\n"
                filepath = write_markdown_file(content, "test-ghy0tt.md")

                # Validate file properties
                result = validate_file_properties(filepath)
                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_write_produces_valid_utf8_no_bom(self):
        """Test: write_markdown_file produces UTF-8 without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# Test\n\nFirst. Second. Third.\n"
                filepath = write_markdown_file(content, "test.md")

                # Read as binary to verify no BOM
                binary_content = Path(filepath).read_bytes()
                assert not binary_content.startswith(b"\xef\xbb\xbf")

                # Validate file properties passes
                assert validate_file_properties(filepath) is True
            finally:
                os.chdir(original_cwd)

    def test_write_produces_lf_line_endings(self):
        """Test: write_markdown_file produces LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# Test\n\nFirst. Second. Third.\n"
                filepath = write_markdown_file(content, "test.md")

                # Read as binary to verify LF only
                binary_content = Path(filepath).read_bytes()
                assert b"\r\n" not in binary_content
                assert b"\n" in binary_content

                # Validate file properties passes
                assert validate_file_properties(filepath) is True
            finally:
                os.chdir(original_cwd)
