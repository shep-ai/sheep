"""
Tests for Task 3: Pre-commit Validation - Validate markdown file structure, encoding, and content

Tests verify that validate_markdown_file():
- File exists and is readable
- File uses UTF-8 encoding without BOM (Byte Order Mark)
- File uses Unix LF line endings (no CRLF)
- File starts with H1 heading (# )
- File contains blank line separator after heading
- File contains exactly 2-3 sentences of prose content
- File ends with trailing newline
- Returns True if all checks pass
- Raises descriptive ValueError if any check fails
"""

from pathlib import Path
import pytest
from sheep.content_generators import validate_markdown_file


class TestTask3ValidateMarkdownFile:
    """Tests for task-3: Validate markdown file meets all requirements."""

    def test_validate_existing_file_test_o09hnk(self):
        """Test that validate_markdown_file() passes for test-o09hnk.md."""
        filepath = Path("test-o09hnk.md")

        # File should exist (created by task-2)
        assert filepath.exists(), "test-o09hnk.md should exist (created by task-2)"

        # Validation should pass and return True
        result = validate_markdown_file(str(filepath))
        assert result is True, "validate_markdown_file should return True for valid file"

    def test_validate_markdown_file_no_exception_on_valid_file(self):
        """Test that validate_markdown_file() does not raise exception for valid file."""
        filepath = Path("test-o09hnk.md")

        # Should not raise any exception
        try:
            result = validate_markdown_file(str(filepath))
            assert result is True
        except Exception as e:
            pytest.fail(f"validate_markdown_file should not raise exception for valid file: {e}")

    def test_file_has_h1_heading(self):
        """Test that file starts with H1 heading (# )."""
        filepath = Path("test-o09hnk.md")
        content = filepath.read_text(encoding='utf-8')

        assert content.startswith("# "), \
            "File should start with H1 heading (# )"

    def test_file_has_blank_line_separator(self):
        """Test that file has blank line after heading."""
        filepath = Path("test-o09hnk.md")
        lines = filepath.read_text(encoding='utf-8').split("\n")

        assert len(lines) >= 2, "File should have at least 2 lines"
        assert lines[0].startswith("# "), "First line should be H1 heading"
        assert lines[1] == "", "Second line should be blank (separator)"

    def test_file_has_prose_content(self):
        """Test that file contains 2-3 sentences of prose."""
        filepath = Path("test-o09hnk.md")
        content = filepath.read_text(encoding='utf-8')

        # Count periods to estimate sentence count
        sentence_count = content.count(".")
        assert sentence_count >= 2 and sentence_count <= 3, \
            f"File should contain 2-3 sentences, found {sentence_count}"

    def test_file_uses_utf8_encoding(self):
        """Test that file is valid UTF-8 encoded."""
        filepath = Path("test-o09hnk.md")
        binary_content = filepath.read_bytes()

        # Should decode without error
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not valid UTF-8: {e}")

    def test_file_has_no_utf8_bom(self):
        """Test that file does not have UTF-8 BOM (Byte Order Mark)."""
        filepath = Path("test-o09hnk.md")
        binary_content = filepath.read_bytes()

        # UTF-8 BOM is b'\xef\xbb\xbf'
        assert not binary_content.startswith(b'\xef\xbb\xbf'), \
            "File should not have UTF-8 BOM"

    def test_file_uses_lf_line_endings(self):
        """Test that file uses Unix LF line endings (no CRLF)."""
        filepath = Path("test-o09hnk.md")
        binary_content = filepath.read_bytes()

        # Should not contain CRLF (\r\n)
        assert b'\r\n' not in binary_content, \
            "File should not have CRLF line endings (Windows style)"

        # Should not contain CR-only (\r)
        assert b'\r' not in binary_content, \
            "File should not have CR line endings (old Mac style)"

    def test_file_ends_with_newline(self):
        """Test that file ends with trailing newline."""
        filepath = Path("test-o09hnk.md")
        content = filepath.read_text(encoding='utf-8')

        assert content.endswith('\n'), \
            "File should end with trailing newline"

    def test_file_is_readable(self):
        """Test that file exists and is readable."""
        filepath = Path("test-o09hnk.md")

        assert filepath.exists(), "File should exist"
        assert filepath.is_file(), "Path should be a file"
        assert filepath.stat().st_size > 0, "File should not be empty"

    def test_file_size_in_expected_range(self):
        """Test that file size falls in typical range for this structure."""
        filepath = Path("test-o09hnk.md")
        file_size = filepath.stat().st_size

        # Typically 300-600 bytes for H1 heading + 2-3 sentences
        assert 300 <= file_size <= 600, \
            f"File size {file_size} bytes outside typical range (300-600)"

    def test_validate_function_returns_bool(self):
        """Test that validate_markdown_file() returns a boolean."""
        filepath = Path("test-o09hnk.md")
        result = validate_markdown_file(str(filepath))

        assert isinstance(result, bool), "Function should return a boolean"
        assert result is True, "Function should return True for valid file"

    def test_nonexistent_file_raises_error(self):
        """Test that validate_markdown_file() raises error for non-existent file."""
        filepath = "nonexistent_file.md"

        with pytest.raises((ValueError, OSError)):
            validate_markdown_file(filepath)

    def test_validation_catches_missing_heading(self):
        """Test that validation detects missing H1 heading."""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create invalid file without H1 heading
                test_file = Path(tmpdir) / "invalid_test.md"
                content = "## Second Level\n\nFirst sentence. Second sentence. Third sentence.\n"
                test_file.write_text(content, encoding='utf-8')

                with pytest.raises(ValueError, match="H1 heading"):
                    validate_markdown_file(str(test_file))
            finally:
                os.chdir(original_cwd)

    def test_validation_catches_missing_blank_line(self):
        """Test that validation detects missing blank line after heading."""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create invalid file without blank line
                test_file = Path(tmpdir) / "invalid_test.md"
                prose = "First sentence about testing and validation. " * 6
                content = f"# Title\n{prose}\n"
                test_file.write_text(content, encoding='utf-8')

                with pytest.raises(ValueError, match="blank"):
                    validate_markdown_file(str(test_file))
            finally:
                os.chdir(original_cwd)

    def test_validation_catches_wrong_sentence_count(self):
        """Test that validation detects wrong number of sentences."""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create invalid file with only 1 sentence
                test_file = Path(tmpdir) / "invalid_test.md"
                content = "# Title\n\nOnly one sentence.\n"
                test_file.write_text(content, encoding='utf-8')

                with pytest.raises(ValueError, match="2-3 sentences"):
                    validate_markdown_file(str(test_file))
            finally:
                os.chdir(original_cwd)

    def test_validation_catches_crlf_line_endings(self):
        """Test that validation detects CRLF line endings."""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create invalid file with CRLF line endings
                test_file = Path(tmpdir) / "invalid_test.md"
                content = "# Title\r\n\r\nFirst sentence. Second sentence. Third sentence.\r\n"
                test_file.write_bytes(content.encode('utf-8'))

                with pytest.raises(ValueError, match="CRLF"):
                    validate_markdown_file(str(test_file))
            finally:
                os.chdir(original_cwd)

    def test_validation_catches_utf8_bom(self):
        """Test that validation detects UTF-8 BOM."""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create invalid file with UTF-8 BOM
                test_file = Path(tmpdir) / "invalid_test.md"
                content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
                # Write with BOM using utf-8-sig encoding
                test_file.write_bytes(content.encode('utf-8-sig'))

                with pytest.raises(ValueError, match="BOM"):
                    validate_markdown_file(str(test_file))
            finally:
                os.chdir(original_cwd)
