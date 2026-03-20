"""Tests for feature 122: Creating markdown file test-duijn0.md with title and prose content."""

from pathlib import Path
import pytest
from sheep.content_generators import (
    generate_markdown_content,
    write_markdown_file,
    validate_markdown_file,
)


class TestContentGeneration:
    """Tests for task-2: Generate markdown content with H1 heading and 2-3 sentences."""

    def test_generate_markdown_content_returns_string(self):
        """Test that generate_markdown_content returns a string."""
        content = generate_markdown_content()
        assert isinstance(content, str)

    def test_generated_content_contains_h1_heading(self):
        """Test that generated content contains H1 heading."""
        content = generate_markdown_content()
        assert content.lstrip().startswith("# ")

    def test_generated_content_has_2_to_3_sentences(self):
        """Test that generated content has 2-3 sentences (by counting periods)."""
        content = generate_markdown_content()
        # Count periods in the prose part (skip the heading and blank line)
        lines = content.split("\n")
        prose_lines = lines[2:] if len(lines) > 2 else []
        prose_content = "\n".join(prose_lines).strip()
        sentence_count = prose_content.count(".")
        assert sentence_count >= 2 and sentence_count <= 3

    def test_generated_content_has_minimum_length(self):
        """Test that generated content has reasonable length."""
        content = generate_markdown_content()
        assert len(content) >= 50

    def test_generated_content_ends_with_newline(self):
        """Test that generated content ends with newline (Unix convention)."""
        content = generate_markdown_content()
        assert content.endswith("\n")


class TestFileCreation:
    """Tests for task-3: Write markdown file to disk with UTF-8 encoding."""

    def test_write_markdown_file_creates_file(self, tmp_path):
        """Test that write_markdown_file creates a file."""
        # Change to tmp directory
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath = write_markdown_file(content, "test-duijn0.md")

            assert Path(filepath).exists()
        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_returns_path(self, tmp_path):
        """Test that write_markdown_file returns the file path."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath = write_markdown_file(content, "test-duijn0.md")

            assert isinstance(filepath, str)
            assert "test-duijn0.md" in filepath
        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_content_matches(self, tmp_path):
        """Test that file content matches input."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath = write_markdown_file(content, "test-duijn0.md")

            file_content = Path(filepath).read_text(encoding="utf-8")
            assert file_content == content
        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_utf8_encoding(self, tmp_path):
        """Test that file is created with UTF-8 encoding."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath = write_markdown_file(content, "test-duijn0.md")

            # Read file as UTF-8 should work without errors
            file_content = Path(filepath).read_text(encoding="utf-8")
            assert file_content == content
        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_rejects_path_traversal(self, tmp_path):
        """Test that write_markdown_file rejects unsafe filenames."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            with pytest.raises(ValueError):
                write_markdown_file(content, "../test-duijn0.md")
        finally:
            os.chdir(original_cwd)


class TestFileValidation:
    """Tests for task-4: Validate file encoding, line endings, and format."""

    def test_validate_markdown_file_passes_valid_file(self, tmp_path):
        """Test that validate_markdown_file returns True for valid file."""
        test_file = tmp_path / "test-duijn0.md"

        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        result = validate_markdown_file(str(test_file))
        assert result is True

    def test_validate_markdown_file_checks_utf8_no_bom(self, tmp_path):
        """Test that validate_markdown_file checks for UTF-8 without BOM."""
        test_file = tmp_path / "test-duijn0.md"

        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        result = validate_markdown_file(str(test_file))
        assert result is True

    def test_validate_markdown_file_checks_lf_line_endings(self, tmp_path):
        """Test that validate_markdown_file checks for LF line endings."""
        test_file = tmp_path / "test-duijn0.md"

        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        assert b"\r\n" not in binary_content

        result = validate_markdown_file(str(test_file))
        assert result is True

    def test_validate_markdown_file_checks_h1_heading(self, tmp_path):
        """Test that validate_markdown_file checks for H1 heading."""
        test_file = tmp_path / "test-duijn0.md"

        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        result = validate_markdown_file(str(test_file))
        assert result is True

    def test_validate_markdown_file_rejects_missing_h1(self, tmp_path):
        """Test that validate_markdown_file rejects file without H1 heading."""
        test_file = tmp_path / "test-duijn0.md"

        content = "No heading here.\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="H1 heading"):
            validate_markdown_file(str(test_file))

    def test_validate_markdown_file_checks_sentence_count(self, tmp_path):
        """Test that validate_markdown_file validates sentence count."""
        test_file = tmp_path / "test-duijn0.md"

        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        result = validate_markdown_file(str(test_file))
        assert result is True

    def test_validate_markdown_file_rejects_too_few_sentences(self, tmp_path):
        """Test that validate_markdown_file rejects file with < 2 sentences."""
        test_file = tmp_path / "test-duijn0.md"

        content = "# Test Title\n\nFirst sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_markdown_file(str(test_file))

    def test_validate_markdown_file_rejects_too_many_sentences(self, tmp_path):
        """Test that validate_markdown_file rejects file with > 3 sentences."""
        test_file = tmp_path / "test-duijn0.md"

        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence. Fourth sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_markdown_file(str(test_file))

    def test_validate_markdown_file_rejects_nonexistent_file(self):
        """Test that validate_markdown_file rejects nonexistent file."""
        with pytest.raises(IOError, match="does not exist"):
            validate_markdown_file("/nonexistent/file.md")


class TestIntegration:
    """Integration tests for the complete workflow."""

    def test_file_creation_returns_path(self, tmp_path):
        """Test that file creation returns a valid filepath."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            mock_content = "# Test Topic\n\nThis is the first sentence. This is the second sentence. This is the third sentence.\n"
            filepath = write_markdown_file(mock_content, "test-duijn0.md")

            assert filepath is not None
            assert "test-duijn0.md" in filepath
            assert Path(filepath).exists()
        finally:
            os.chdir(original_cwd)
