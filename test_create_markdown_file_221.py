#!/usr/bin/env python3
"""
Test suite for feature 221: markdown-file-creation-766ea9
Tests create_file() function and module constants.
No validation layer per spec requirement.
"""

import tempfile
from pathlib import Path

import pytest
from create_markdown_file_221 import COMMIT_MESSAGE, FILENAME, PROSE, TITLE, create_file


class TestConstants:
    """Test suite for module-level constants."""

    def test_filename_is_correct(self):
        """Test that FILENAME constant is exactly 'test-5vnehe.md'."""
        assert FILENAME == "test-5vnehe.md"

    def test_title_is_meaningful(self):
        """Test that TITLE is a meaningful non-empty string."""
        assert isinstance(TITLE, str)
        assert len(TITLE) > 0
        assert not TITLE.isspace()

    def test_prose_is_not_empty(self):
        """Test that PROSE is a meaningful non-empty string."""
        assert isinstance(PROSE, str)
        assert len(PROSE) > 0
        assert not PROSE.isspace()

    def test_prose_sentence_count(self):
        """Test that PROSE contains exactly 2-3 sentences."""
        sentence_count = PROSE.count('.')
        assert 2 <= sentence_count <= 3

    def test_commit_message_format(self):
        """Test that COMMIT_MESSAGE follows conventional commits format."""
        assert COMMIT_MESSAGE.startswith("feat(221):")
        assert "test-5vnehe.md" in COMMIT_MESSAGE


class TestCreateFile:
    """Test suite for create_file function."""

    def test_create_file_returns_path_on_success(self):
        """Test that create_file returns Path when file is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                result = create_file()
                assert result is not None
                assert isinstance(result, Path)
                assert Path(FILENAME).exists()
            finally:
                os.chdir(original_dir)

    def test_create_file_raises_if_exists(self):
        """Test that create_file raises FileExistsError if file already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / FILENAME
            # Create file first
            test_file.write_text("# Title\n\nContent.\n")
            # Now try to create again
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                with pytest.raises(FileExistsError):
                    create_file()
            finally:
                os.chdir(original_dir)

    def test_create_file_contains_h1_heading(self):
        """Test that created file contains H1 heading with TITLE."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                content = Path(FILENAME).read_text(encoding="utf-8")
                assert content.startswith(f"# {TITLE}\n")
            finally:
                os.chdir(original_dir)

    def test_create_file_contains_blank_line_after_heading(self):
        """Test that created file has blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                content = Path(FILENAME).read_text(encoding="utf-8")
                lines = content.split("\n")
                assert lines[0].startswith("# ")
                assert lines[1] == ""
            finally:
                os.chdir(original_dir)

    def test_create_file_contains_prose(self):
        """Test that created file contains PROSE content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                content = Path(FILENAME).read_text(encoding="utf-8")
                assert PROSE in content
            finally:
                os.chdir(original_dir)

    def test_create_file_uses_utf8_encoding(self):
        """Test that created file uses UTF-8 encoding without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                binary = Path(FILENAME).read_bytes()
                # Should not start with UTF-8 BOM (EF BB BF)
                assert not binary.startswith(b"\xef\xbb\xbf")
                # Should decode as UTF-8
                content = binary.decode("utf-8")
                assert content is not None
            finally:
                os.chdir(original_dir)

    def test_create_file_uses_lf_line_endings(self):
        """Test that created file uses Unix LF line endings only."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                binary = Path(FILENAME).read_bytes()
                # Should not contain CRLF (0x0D 0x0A)
                assert b"\r\n" not in binary
                # Should contain LF (0x0A)
                assert b"\n" in binary
            finally:
                os.chdir(original_dir)

    def test_create_file_ends_with_newline(self):
        """Test that created file ends with newline character."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                content = Path(FILENAME).read_text(encoding="utf-8")
                assert content.endswith("\n")
            finally:
                os.chdir(original_dir)

    def test_create_file_size_in_range(self):
        """Test that created file size is between 300-500 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                file_size = Path(FILENAME).stat().st_size
                assert 300 <= file_size <= 500
            finally:
                os.chdir(original_dir)

    def test_create_file_structure(self):
        """Test that created file has correct markdown structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                content = Path(FILENAME).read_text(encoding="utf-8")
                # Structure should be: # Title\n\nProse\n
                lines = content.split("\n")
                assert len(lines) >= 3  # heading, blank line, prose, newline
                assert lines[0].startswith("# ")  # H1 heading
                assert lines[1] == ""  # Blank line
                assert PROSE in content  # Prose content present
            finally:
                os.chdir(original_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
