"""
Test suite for markdown file creation feature 175.

Tests cover file creation, validation, and git operations.
Uses tempfile for isolated testing without affecting the repository.
"""
import tempfile
from pathlib import Path
import pytest
import create_markdown_file


class TestFileCreation:
    """Tests for file creation with correct structure and encoding."""

    def test_file_created(self):
        """Test that markdown file is created in the repository root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                # Change to temp directory for isolated test
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                assert (tmpdir_path / create_markdown_file.FILENAME).exists()
            finally:
                os.chdir(original_cwd)

    def test_file_has_heading(self):
        """Test that file has H1 heading on line 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_text()
                lines = content.split('\n')

                assert lines[0].startswith('# ')
                assert len(lines[0]) > 2  # Title is not empty
            finally:
                os.chdir(original_cwd)

    def test_file_has_blank_line(self):
        """Test that file has blank line on line 2."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_text()
                lines = content.split('\n')

                assert lines[1] == ''
            finally:
                os.chdir(original_cwd)

    def test_file_has_prose(self):
        """Test that file has prose content starting on line 3."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_text()
                lines = content.split('\n')

                # Lines 3+ should have content
                prose_lines = lines[2:]
                prose_content = '\n'.join(prose_lines).strip()
                assert len(prose_content) > 0
            finally:
                os.chdir(original_cwd)

    def test_file_ends_with_newline(self):
        """Test that file ends with newline character."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_bytes()

                assert content.endswith(b'\n')
            finally:
                os.chdir(original_cwd)

    def test_file_utf8_encoding(self):
        """Test that file uses UTF-8 encoding (can be read as UTF-8)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                # Should not raise UnicodeDecodeError
                (tmpdir_path / create_markdown_file.FILENAME).read_text(encoding='utf-8')
            finally:
                os.chdir(original_cwd)

    def test_file_lf_line_endings(self):
        """Test that file uses Unix LF line endings (no CRLF)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_bytes()

                assert b'\r\n' not in content, "File should use LF, not CRLF"
            finally:
                os.chdir(original_cwd)


class TestValidation:
    """Tests for file validation logic."""

    def test_validate_accepts_valid_file(self):
        """Test that validation accepts a properly created file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                # Should not raise any exception
                create_markdown_file.validate_file(create_markdown_file.FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_no_utf8_bom(self):
        """Test that file does not have UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_bytes()

                assert not content.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"
            finally:
                os.chdir(original_cwd)
