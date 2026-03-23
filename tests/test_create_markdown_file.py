"""Tests for feature 174: Creating markdown file test-u9soe6.md with title and prose content."""

from pathlib import Path
import pytest
import tempfile
import os


class TestCreateFileFunction:
    """Tests for create_file() function."""

    def test_create_file_creates_file_at_correct_path(self, tmp_path):
        """Test that create_file() creates file at correct path."""
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            # Call create_file
            result = create_file()

            # Verify file exists
            assert Path("test-u9soe6.md").exists()
            assert result == Path("test-u9soe6.md")
        finally:
            os.chdir(original_cwd)

    def test_create_file_has_h1_heading_on_first_line(self, tmp_path):
        """Test that created file has H1 heading on first line."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            content = Path("test-u9soe6.md").read_text(encoding="utf-8")
            lines = content.split("\n")

            # First line should be H1 heading
            assert lines[0].startswith("# ")
            assert len(lines[0]) > 2  # Has content after "#"
        finally:
            os.chdir(original_cwd)

    def test_create_file_has_blank_line_on_second_line(self, tmp_path):
        """Test that created file has blank line on second line."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            content = Path("test-u9soe6.md").read_text(encoding="utf-8")
            lines = content.split("\n")

            # Second line (index 1) should be blank
            assert lines[1] == ""
        finally:
            os.chdir(original_cwd)

    def test_create_file_has_prose_content(self, tmp_path):
        """Test that created file has prose content after blank line."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            content = Path("test-u9soe6.md").read_text(encoding="utf-8")
            lines = content.split("\n")

            # Should have at least 3 lines (heading, blank, prose)
            assert len(lines) >= 3

            # Prose content should exist (starting from line 2)
            prose_content = "\n".join(lines[2:]).strip()
            assert len(prose_content) > 0
        finally:
            os.chdir(original_cwd)

    def test_create_file_uses_utf8_encoding(self, tmp_path):
        """Test that created file uses UTF-8 encoding without BOM."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            binary_content = Path("test-u9soe6.md").read_bytes()

            # No UTF-8 BOM (EF BB BF)
            assert not binary_content.startswith(b"\xef\xbb\xbf")

            # Should be decodable as UTF-8
            binary_content.decode("utf-8")
        finally:
            os.chdir(original_cwd)

    def test_create_file_uses_lf_line_endings(self, tmp_path):
        """Test that created file uses LF line endings, not CRLF."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            binary_content = Path("test-u9soe6.md").read_bytes()

            # No CRLF (Windows line endings)
            assert b"\r\n" not in binary_content
        finally:
            os.chdir(original_cwd)

    def test_create_file_has_2_to_3_sentences(self, tmp_path):
        """Test that created file has 2-3 sentences of prose."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            content = Path("test-u9soe6.md").read_text(encoding="utf-8")
            lines = content.split("\n")

            # Get prose content (after heading and blank line)
            prose_content = "\n".join(lines[2:]).strip()

            # Count sentences (periods indicate sentence endings)
            sentence_count = prose_content.count(".")

            # Should have 2-3 sentences
            assert 2 <= sentence_count <= 3
        finally:
            os.chdir(original_cwd)

    def test_create_file_ends_with_newline(self, tmp_path):
        """Test that created file ends with a newline."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            content = Path("test-u9soe6.md").read_text(encoding="utf-8")

            # Should end with newline
            assert content.endswith("\n")
        finally:
            os.chdir(original_cwd)

    def test_create_file_size_in_range(self, tmp_path):
        """Test that created file size is within 400-600 bytes."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from create_markdown_file import create_file

            create_file()

            file_size = Path("test-u9soe6.md").stat().st_size

            # File size should be in 400-600 byte range
            assert 400 <= file_size <= 600
        finally:
            os.chdir(original_cwd)


class TestModuleConstants:
    """Tests for module constants."""

    def test_filename_constant_exists(self):
        """Test that FILENAME constant is defined."""
        from create_markdown_file import FILENAME

        assert FILENAME == "test-u9soe6.md"

    def test_title_constant_exists(self):
        """Test that TITLE constant is defined."""
        from create_markdown_file import TITLE

        assert isinstance(TITLE, str)
        assert len(TITLE) > 0

    def test_prose_constant_exists(self):
        """Test that PROSE constant is defined."""
        from create_markdown_file import PROSE

        assert isinstance(PROSE, str)
        assert len(PROSE) > 0

    def test_commit_message_constant_exists(self):
        """Test that COMMIT_MESSAGE constant is defined."""
        from create_markdown_file import COMMIT_MESSAGE

        assert COMMIT_MESSAGE == "feat(174): create markdown file test-u9soe6.md with prose content"
