"""Tests for markdown file writing and validation functions."""

import tempfile
from pathlib import Path

import pytest

from sheep.content_generators import validate_markdown_file, write_markdown_file


class TestWriteMarkdownFile:
    """Tests for write_markdown_file function."""

    def test_creates_file_at_specified_path(self):
        """Test that write_markdown_file creates a file at the specified path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                # Change to temp directory
                import os
                os.chdir(tmpdir)

                content = "# Test Title\n\nThis is a test sentence. This is another sentence. And a third one."
                result = write_markdown_file(content, "test.md")

                assert Path(result).exists()
                assert result.endswith("test.md")
            finally:
                os.chdir(original_cwd)

    def test_writes_content_exactly(self):
        """Test that file contains exactly the content passed to function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                expected_content = "# Machine Learning\n\nML is a field of AI. It enables learning from data. Models improve with more data.\n"
                write_markdown_file(expected_content, "test.md")

                actual_content = Path("test.md").read_text(encoding="utf-8")
                assert actual_content == expected_content
            finally:
                os.chdir(original_cwd)

    def test_uses_utf8_encoding(self):
        """Test that file is UTF-8 encoded with no BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                content = "# Unicode Test\n\nThis has special chars: é, ñ, 中文. Another sentence. Third sentence.\n"
                write_markdown_file(content, "test.md")

                # Read as binary to check for BOM
                binary_content = Path("test.md").read_bytes()
                assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

                # Verify it can be decoded as UTF-8
                decoded = binary_content.decode("utf-8")
                assert decoded == content
            finally:
                os.chdir(original_cwd)

    def test_uses_lf_line_endings(self):
        """Test that file uses Unix LF line endings, not CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                content = "# Test\n\nSentence one. Sentence two. Sentence three.\n"
                write_markdown_file(content, "test.md")

                binary_content = Path("test.md").read_bytes()
                assert b"\r\n" not in binary_content, "File should not have CRLF line endings"
                assert b"\n" in binary_content, "File should have LF line endings"
            finally:
                os.chdir(original_cwd)

    def test_returns_file_path_on_success(self):
        """Test that function returns file path on success."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                content = "# Test\n\nSentence one. Sentence two. Sentence three.\n"
                result = write_markdown_file(content, "test.md")

                assert isinstance(result, str)
                assert "test.md" in result
            finally:
                os.chdir(original_cwd)

    def test_rejects_path_traversal_filenames(self):
        """Test that function rejects filenames with path traversal attempts."""
        content = "# Test\n\nSentence one. Sentence two. Sentence three.\n"

        with pytest.raises(ValueError, match="Invalid filename"):
            write_markdown_file(content, "../malicious.md")

        with pytest.raises(ValueError, match="Invalid filename"):
            write_markdown_file(content, "subdir/test.md")

        with pytest.raises(ValueError, match="Invalid filename"):
            write_markdown_file(content, ".hidden.md")

    def test_rejects_empty_content(self):
        """Test that writing empty content fails gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                with pytest.raises(IOError, match="empty"):
                    write_markdown_file("", "test.md")
            finally:
                os.chdir(original_cwd)


class TestValidateMarkdownFile:
    """Tests for validate_markdown_file function."""

    def test_accepts_valid_markdown_file(self):
        """Test that valid markdown file passes validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            content = "# Valid Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            path.write_text(content, encoding="utf-8", newline="")

            result = validate_markdown_file(str(path))
            assert result is True

    def test_rejects_missing_h1_heading(self):
        """Test that missing H1 heading is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            content = "## Second Level Heading\n\nFirst sentence. Second sentence. Third sentence.\n"
            path.write_text(content, encoding="utf-8", newline="")

            with pytest.raises(ValueError, match="H1 heading"):
                validate_markdown_file(str(path))

    def test_rejects_missing_blank_line_separator(self):
        """Test that missing blank line after heading is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            content = "# Title\nFirst sentence. Second sentence. Third sentence.\n"
            path.write_text(content, encoding="utf-8", newline="")

            with pytest.raises(ValueError, match="blank"):
                validate_markdown_file(str(path))

    def test_rejects_too_few_sentences(self):
        """Test that fewer than 2 sentences is rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            content = "# Title\n\nOnly one sentence.\n"
            path.write_text(content, encoding="utf-8", newline="")

            with pytest.raises(ValueError, match="2-3 sentences"):
                validate_markdown_file(str(path))

    def test_rejects_too_many_sentences(self):
        """Test that more than 3 sentences is rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            content = "# Title\n\nFirst. Second. Third. Fourth.\n"
            path.write_text(content, encoding="utf-8", newline="")

            with pytest.raises(ValueError, match="2-3 sentences"):
                validate_markdown_file(str(path))

    def test_rejects_crlf_line_endings(self):
        """Test that CRLF line endings are detected and rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Write with CRLF line endings
            binary_content = b"# Title\r\n\r\nFirst sentence. Second sentence. Third sentence.\r\n"
            path.write_bytes(binary_content)

            with pytest.raises(ValueError, match="CRLF"):
                validate_markdown_file(str(path))

    def test_rejects_missing_trailing_newline(self):
        """Test that missing trailing newline is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Write without trailing newline
            binary_content = b"# Title\n\nFirst sentence. Second sentence. Third sentence."
            path.write_bytes(binary_content)

            with pytest.raises(ValueError, match="trailing newline"):
                validate_markdown_file(str(path))

    def test_rejects_non_utf8_encoding(self):
        """Test that non-UTF-8 encoding is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Write with actual non-UTF-8 bytes (latin-1 encoded with non-ASCII characters)
            # Use latin-1 specific character that is not valid UTF-8
            content = "# Title\n\nFirst café. Second naïve. Third façade.\n"
            path.write_bytes(content.encode("latin-1"))

            with pytest.raises(ValueError, match="UTF-8"):
                validate_markdown_file(str(path))

    def test_rejects_utf8_bom(self):
        """Test that UTF-8 BOM is detected and rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Write with UTF-8 BOM
            content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            binary_content = b"\xef\xbb\xbf" + content.encode("utf-8")
            path.write_bytes(binary_content)

            with pytest.raises(ValueError, match="BOM"):
                validate_markdown_file(str(path))

    def test_rejects_nonexistent_file(self):
        """Test that nonexistent file is rejected."""
        with pytest.raises(IOError, match="does not exist"):
            validate_markdown_file("/nonexistent/path/test.md")

    def test_rejects_directory_path(self):
        """Test that directory path is rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(IOError, match="not a file"):
                validate_markdown_file(tmpdir)

    def test_counts_sentences_correctly(self):
        """Test that sentence count validation works for edge cases."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Test with exactly 2 sentences (periods)
            path = Path(tmpdir) / "test2.md"
            content = "# Title\n\nFirst sentence. Second sentence.\n"
            path.write_text(content, encoding="utf-8", newline="")
            assert validate_markdown_file(str(path)) is True

            # Test with exactly 3 sentences
            path = Path(tmpdir) / "test3.md"
            content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            path.write_text(content, encoding="utf-8", newline="")
            assert validate_markdown_file(str(path)) is True

    def test_sentence_counting_is_simple(self):
        """Test that sentence counting is simple period-based (counts all periods)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Content with abbreviation will count extra periods
            path = Path(tmpdir) / "test.md"
            content = "# Title\n\nDr. Smith studied biology. His research was groundbreaking. The findings changed science.\n"
            path.write_text(content, encoding="utf-8", newline="")

            # This has 4 periods total (Dr. + 3 sentence ends) so validation will fail
            # This documents that the implementation counts all periods simply
            with pytest.raises(ValueError, match="2-3 sentences"):
                validate_markdown_file(str(path))


class TestIntegration:
    """Integration tests for writing and validating markdown files."""

    def test_write_and_validate_roundtrip(self):
        """Test that content can be written and then validated successfully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                # Generate valid content
                content = "# Distributed Systems\n\nDistributed systems enable scalability. They provide fault tolerance. Modern applications depend on them.\n"

                # Write file
                filepath = write_markdown_file(content, "test.md")

                # Validate file
                result = validate_markdown_file(filepath)
                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_invalid_content_fails_validation(self):
        """Test that invalid content fails validation after being written."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                # Content missing blank line
                content = "# Title\nFirst sentence. Second sentence. Third sentence.\n"

                # Write file
                filepath = write_markdown_file(content, "test.md")

                # Validation should fail
                with pytest.raises(ValueError):
                    validate_markdown_file(filepath)
            finally:
                os.chdir(original_cwd)
