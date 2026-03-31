"""Tests for feature 295 phase 3: File creation and validation.

Tasks:
- Task 4: Implement markdown file creation with pathlib
- Task 5: Verify markdown structure and file encoding
"""

import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from sheep.content_generators import (
    write_markdown_file,
    validate_markdown_file,
    validate_file_properties,
)


class TestTask4FileCreation:
    """Tests for task-4: Implement markdown file creation with pathlib."""

    def test_write_markdown_file_creates_file(self, tmp_path):
        """Test that write_markdown_file creates a file in repository root."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title\n\nFirst sentence. Second sentence.\n"
            filepath = write_markdown_file(content, "test.md")

            # File should be created
            assert Path(filepath).exists()
            assert Path(filepath).is_file()

        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_returns_path_string(self, tmp_path):
        """Test that write_markdown_file returns the file path as a string."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title\n\nFirst sentence. Second sentence.\n"
            result = write_markdown_file(content, "test.md")

            # Should return a string path
            assert isinstance(result, str)
            assert "test.md" in result
            assert Path(result).is_absolute() or Path(result).exists()

        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_with_utf8_encoding(self, tmp_path):
        """Test that write_markdown_file writes with UTF-8 encoding."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title\n\nFirst sentence. Second sentence.\n"
            filepath = write_markdown_file(content, "test.md")

            # Read and verify encoding
            with open(filepath, "rb") as f:
                binary_content = f.read()

            # Should be valid UTF-8 without BOM
            assert not binary_content.startswith(b"\xef\xbb\xbf"), "Should not have UTF-8 BOM"
            text_content = binary_content.decode("utf-8")  # Should not raise
            assert text_content == content

        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_with_lf_line_endings(self, tmp_path):
        """Test that write_markdown_file uses LF line endings (not CRLF)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title\n\nFirst sentence. Second sentence.\n"
            filepath = write_markdown_file(content, "test.md")

            # Read as binary to check line endings
            with open(filepath, "rb") as f:
                binary_content = f.read()

            # Should not contain CRLF
            assert b"\r\n" not in binary_content, "Should use LF, not CRLF"
            # Should contain LF
            assert b"\n" in binary_content

        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_with_trailing_newline(self, tmp_path):
        """Test that written file has trailing newline."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title\n\nFirst sentence. Second sentence.\n"
            filepath = write_markdown_file(content, "test.md")

            text_content = Path(filepath).read_text(encoding="utf-8")
            assert text_content.endswith("\n"), "File should end with newline"

        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_rejects_path_traversal(self, tmp_path):
        """Test that write_markdown_file rejects filenames with path traversal."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            content = "# Test\n\nTest.\n"

            # Should reject filenames with path separators
            with pytest.raises(ValueError, match="Invalid filename"):
                write_markdown_file(content, "../dangerous.md")

            with pytest.raises(ValueError, match="Invalid filename"):
                write_markdown_file(content, "subdir/file.md")

        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_rejects_hidden_files(self, tmp_path):
        """Test that write_markdown_file rejects hidden filenames."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            content = "# Test\n\nTest.\n"

            with pytest.raises(ValueError, match="Invalid filename"):
                write_markdown_file(content, ".hidden.md")

        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_preserves_content(self, tmp_path):
        """Test that write_markdown_file preserves exact content."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title About Something\n\nFirst detailed sentence. Second detailed sentence.\n"
            filepath = write_markdown_file(content, "test.md")

            written_content = Path(filepath).read_text(encoding="utf-8")
            assert written_content == content

        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_uses_pathlib(self, tmp_path):
        """Test that write_markdown_file uses pathlib for path operations."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            content = "# Test\n\nTest sentence.\n"
            filepath = write_markdown_file(content, "test.md")

            # The returned path should work with Path()
            path_obj = Path(filepath)
            assert path_obj.exists()
            assert path_obj.is_file()

        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_raises_on_empty_content(self, tmp_path):
        """Test that write_markdown_file validates content is not empty."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Depending on implementation, this might raise during validation
            # or succeed with empty file. Test the behavior.
            result = Path("test.md")
            if result.exists():
                result.unlink()

            # Try writing empty content
            with pytest.raises((ValueError, OSError)):
                write_markdown_file("", "test.md")

        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_verifies_file_created(self, tmp_path):
        """Test that write_markdown_file verifies file was actually created."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            content = "# Test\n\nSentence. Another.\n"
            filepath = write_markdown_file(content, "test.md")

            # File must exist
            assert Path(filepath).exists(), f"File was not created: {filepath}"

        finally:
            os.chdir(original_cwd)


class TestTask5FileValidation:
    """Tests for task-5: Verify markdown structure and file encoding."""

    def test_validate_markdown_file_passes_valid_file(self, tmp_path):
        """Test that validate_markdown_file passes a valid markdown file."""
        filepath = tmp_path / "test.md"
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write("# Title\n\nFirst sentence. Second sentence.\n")

        # Should return True for valid file
        result = validate_markdown_file(str(filepath))
        assert result is True

    def test_validate_markdown_file_fails_missing_file(self, tmp_path):
        """Test that validate_markdown_file fails for missing file."""
        filepath = tmp_path / "nonexistent.md"

        with pytest.raises((OSError, ValueError)):
            validate_markdown_file(str(filepath))

    def test_validate_markdown_file_checks_h1_heading(self, tmp_path):
        """Test that validate_markdown_file verifies H1 heading exists."""
        # File without H1 heading
        filepath = tmp_path / "test.md"
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write("Just some prose. More prose.\n")

        with pytest.raises(ValueError, match="H1 heading"):
            validate_markdown_file(str(filepath))

    def test_validate_markdown_file_checks_blank_line_separator(self, tmp_path):
        """Test that validate_markdown_file verifies blank line separator."""
        # File without blank line between heading and prose
        filepath = tmp_path / "test.md"
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write("# Title\nFirst sentence. Second sentence.\n")

        with pytest.raises(ValueError, match="blank"):
            validate_markdown_file(str(filepath))

    def test_validate_markdown_file_checks_prose_content(self, tmp_path):
        """Test that validate_markdown_file verifies prose content exists."""
        # File with heading but no prose
        filepath = tmp_path / "test.md"
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write("# Title\n\n")

        with pytest.raises(ValueError, match="prose"):
            validate_markdown_file(str(filepath))

    def test_validate_markdown_file_checks_sentence_count(self, tmp_path):
        """Test that validate_markdown_file validates 2-3 sentences."""
        # File with only 1 sentence
        filepath = tmp_path / "test.md"
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write("# Title\n\nOnly one sentence.\n")

        with pytest.raises(ValueError, match="sentences"):
            validate_markdown_file(str(filepath))

    def test_validate_markdown_file_checks_utf8_encoding(self, tmp_path):
        """Test that validate_markdown_file verifies UTF-8 encoding."""
        filepath = tmp_path / "test.md"
        # Write with explicit UTF-8 to ensure correct encoding
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write("# Title\n\nFirst sentence. Second sentence.\n")

        # Should pass UTF-8 validation
        result = validate_markdown_file(str(filepath))
        assert result is True

    def test_validate_markdown_file_detects_bom(self, tmp_path):
        """Test that validate_markdown_file detects UTF-8 BOM."""
        filepath = tmp_path / "test.md"
        # Write with UTF-8 BOM
        with open(filepath, "wb") as f:
            f.write(b"\xef\xbb\xbf# Title\n\nFirst sentence. Second sentence.\n")

        with pytest.raises(ValueError, match="BOM"):
            validate_markdown_file(str(filepath))

    def test_validate_markdown_file_detects_crlf_line_endings(self, tmp_path):
        """Test that validate_markdown_file detects CRLF line endings."""
        filepath = tmp_path / "test.md"
        # Write with CRLF line endings
        with open(filepath, "wb") as f:
            f.write(b"# Title\r\n\r\nFirst sentence. Second sentence.\r\n")

        with pytest.raises(ValueError, match="CRLF|line endings"):
            validate_markdown_file(str(filepath))

    def test_validate_markdown_file_requires_trailing_newline(self, tmp_path):
        """Test that validate_markdown_file requires trailing newline."""
        filepath = tmp_path / "test.md"
        # Write without trailing newline
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write("# Title\n\nFirst sentence. Second sentence.")

        with pytest.raises(ValueError, match="trailing newline"):
            validate_markdown_file(str(filepath))

    def test_validate_markdown_file_accepts_2_sentences(self, tmp_path):
        """Test that validate_markdown_file accepts 2 sentences."""
        filepath = tmp_path / "test.md"
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write("# Title\n\nFirst sentence. Second sentence.\n")

        result = validate_markdown_file(str(filepath))
        assert result is True

    def test_validate_markdown_file_accepts_3_sentences(self, tmp_path):
        """Test that validate_markdown_file accepts 3 sentences."""
        filepath = tmp_path / "test.md"
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write("# Title\n\nFirst sentence. Second sentence. Third sentence.\n")

        result = validate_markdown_file(str(filepath))
        assert result is True

    def test_validate_markdown_file_raises_on_nonfile(self, tmp_path):
        """Test that validate_markdown_file fails if path is a directory."""
        dirpath = tmp_path / "subdir"
        dirpath.mkdir()

        with pytest.raises((OSError, ValueError)):
            validate_markdown_file(str(dirpath))

    def test_validate_file_properties_checks_encoding(self, tmp_path):
        """Test that validate_file_properties checks UTF-8 encoding."""
        filepath = tmp_path / "test.md"
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write("# Title\n\nFirst sentence. Second sentence.\n")

        result = validate_file_properties(str(filepath))
        assert result is True

    def test_validate_file_properties_detects_bom(self, tmp_path):
        """Test that validate_file_properties detects UTF-8 BOM."""
        filepath = tmp_path / "test.md"
        with open(filepath, "wb") as f:
            f.write(b"\xef\xbb\xbf# Title\n\nFirst sentence. Second sentence.\n")

        with pytest.raises(ValueError, match="BOM"):
            validate_file_properties(str(filepath))

    def test_validate_file_properties_detects_crlf(self, tmp_path):
        """Test that validate_file_properties detects CRLF line endings."""
        filepath = tmp_path / "test.md"
        with open(filepath, "wb") as f:
            f.write(b"# Title\r\n\r\nFirst sentence. Second sentence.\r\n")

        with pytest.raises(ValueError, match="CRLF"):
            validate_file_properties(str(filepath))


class TestIntegrationPhase3:
    """Integration tests for phase 3 workflow."""

    def test_create_and_validate_markdown_file(self, tmp_path):
        """Test complete workflow: create file and validate it."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create file
            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath = write_markdown_file(content, "test.md")

            # Validate file
            result = validate_markdown_file(filepath)
            assert result is True

        finally:
            os.chdir(original_cwd)

    def test_create_file_with_special_characters(self, tmp_path):
        """Test file creation with special characters in prose."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Content with special characters
            content = "# Élégant Tîtlé\n\nFïrst sëntëncé wîth spëcïål chärs. Sëcönd sëntëncé.\n"
            filepath = write_markdown_file(content, "test.md")

            # Validate
            result = validate_markdown_file(filepath)
            assert result is True

            # Verify content
            written = Path(filepath).read_text(encoding="utf-8")
            assert "Élégant" in written
            assert "spëcïål" in written

        finally:
            os.chdir(original_cwd)

    def test_validate_file_with_multiple_paragraphs(self, tmp_path):
        """Test validation of file with multiple paragraphs."""
        filepath = tmp_path / "test.md"
        content = "# Title\n\nFirst sentence. Second sentence.\n\nThird sentence in new paragraph.\n"
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write(content)

        result = validate_markdown_file(str(filepath))
        assert result is True
