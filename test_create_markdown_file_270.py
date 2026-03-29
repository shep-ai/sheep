"""
Test suite for feature 270: markdown file creation (test-n3o2vi.md)

Tests for Phase 1: File Creation & Validation

This module provides test coverage for:
- File creation with correct structure (H1 heading + blank line + prose)
- Encoding validation (UTF-8 without BOM)
- Line ending validation (Unix LF, no Windows CRLF)
- Prose content validation (2-3 sentences)
- Validation function behavior (success and failure paths)
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Import the functions from the script
sys.path.insert(0, str(Path(__file__).parent))
from create_markdown_file import create_file, validate_file


@pytest.fixture
def temp_dir():
    """Provide an isolated temporary directory for test file creation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            yield Path(tmpdir)
        finally:
            os.chdir(original_cwd)


class TestCreateFile:
    """Tests for create_file() function."""

    def test_creates_file_at_repository_root(self, temp_dir):
        """Test that create_file() creates test-n3o2vi.md in the repository root."""
        filepath = create_file()
        assert filepath.exists()
        assert filepath.name == "test-n3o2vi.md"

    def test_file_contains_h1_heading(self, temp_dir):
        """Test that file contains H1 markdown heading on first line."""
        create_file()
        content = Path("test-n3o2vi.md").read_text(encoding='utf-8')
        assert content.startswith("# "), "File should start with H1 heading"

    def test_file_contains_prose_content(self, temp_dir):
        """Test that file contains 2-3 sentences of prose content."""
        create_file()
        content = Path("test-n3o2vi.md").read_text(encoding='utf-8')
        # Count periods to estimate sentence count
        period_count = content.count('.')
        assert period_count >= 2, f"File should contain at least 2 sentences, found {period_count} periods"
        assert period_count <= 4, f"File should contain at most 3 sentences, found {period_count} periods"

    def test_file_uses_utf8_encoding(self, temp_dir):
        """Test that file is UTF-8 encoded."""
        create_file()
        binary_content = Path("test-n3o2vi.md").read_bytes()

        # Verify it can be decoded as UTF-8
        try:
            decoded = binary_content.decode('utf-8')
            assert isinstance(decoded, str)
        except UnicodeDecodeError:
            pytest.fail("File is not valid UTF-8")

    def test_file_has_no_utf8_bom(self, temp_dir):
        """Test that file does not have UTF-8 BOM (Byte Order Mark)."""
        create_file()
        binary_content = Path("test-n3o2vi.md").read_bytes()
        # UTF-8 BOM is b'\xef\xbb\xbf'
        assert not binary_content.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"

    def test_file_uses_lf_line_endings(self, temp_dir):
        """Test that file uses Unix LF line endings, not Windows CRLF."""
        create_file()
        binary_content = Path("test-n3o2vi.md").read_bytes()
        # Should not contain CRLF (\r\n)
        assert b'\r\n' not in binary_content, "File should not have CRLF line endings"
        # Should contain LF (\n)
        assert b'\n' in binary_content, "File should have LF line endings"

    def test_file_size_in_typical_range(self, temp_dir):
        """Test that file size is approximately 400-600 bytes."""
        create_file()
        file_size = Path("test-n3o2vi.md").stat().st_size
        # Typical range: 300-800 bytes for flexibility
        assert 300 < file_size < 800, (
            f"File size {file_size} bytes outside typical range (300-800). "
            f"Expected 400-600 as soft guideline."
        )

    def test_file_contains_blank_line_after_heading(self, temp_dir):
        """Test that file has blank line separating heading from prose."""
        create_file()
        content = Path("test-n3o2vi.md").read_text(encoding='utf-8')
        # Should contain double newline (blank line)
        assert '\n\n' in content, "File should contain blank line after heading"

    def test_returns_path_object(self, temp_dir):
        """Test that create_file() returns a Path object."""
        result = create_file()
        assert isinstance(result, Path)
        assert result.name == "test-n3o2vi.md"

    def test_file_ends_with_newline(self, temp_dir):
        """Test that file ends with a newline character."""
        create_file()
        binary_content = Path("test-n3o2vi.md").read_bytes()
        # File must end with LF (\n, which is b'\n' in binary)
        assert binary_content.endswith(b'\n'), "File should end with a newline character"


class TestValidateFile:
    """Tests for validate_file() function."""

    def test_validates_correctly_created_file(self, temp_dir):
        """Test that validate_file() passes for a correctly created file."""
        filepath = create_file()
        result = validate_file(filepath)
        assert result is True

    def test_rejects_missing_file(self):
        """Test that validate_file() raises error for non-existent file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nonexistent_path = Path(tmpdir) / "nonexistent.md"
            with pytest.raises(AssertionError, match="does not exist"):
                validate_file(nonexistent_path)

    def test_rejects_missing_h1_heading(self, temp_dir):
        """Test that validate_file() rejects file without H1 heading."""
        path = Path(temp_dir) / "test.md"
        # No heading - use H2 instead
        content = "## Second Level\n\nFirst sentence. Second sentence. Third sentence.\n"
        path.write_bytes(content.encode('utf-8'))

        with pytest.raises(AssertionError, match="H1 heading"):
            validate_file(path)

    def test_rejects_missing_blank_line(self, temp_dir):
        """Test that validate_file() rejects file without blank line after heading."""
        path = Path(temp_dir) / "test.md"
        # No blank line between heading and prose
        prose = "This is prose without a blank line. Second sentence here. Third sentence."
        content = f"# Title\n{prose}\n"
        path.write_bytes(content.encode('utf-8'))

        with pytest.raises(AssertionError, match="Second line must be blank"):
            validate_file(path)

    def test_rejects_incorrect_sentence_count_too_few(self, temp_dir):
        """Test that validate_file() rejects file with fewer than 2 sentences."""
        path = Path(temp_dir) / "test.md"
        # Only one sentence (one period)
        content = "# Title\n\nOnly one sentence.\n"
        path.write_bytes(content.encode('utf-8'))

        with pytest.raises(AssertionError, match="2-3 sentences"):
            validate_file(path)

    def test_rejects_incorrect_sentence_count_too_many(self, temp_dir):
        """Test that validate_file() rejects file with more than 3 sentences."""
        path = Path(temp_dir) / "test.md"
        # Four sentences (four periods)
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence. Fourth sentence.\n"
        path.write_bytes(content.encode('utf-8'))

        with pytest.raises(AssertionError, match="2-3 sentences"):
            validate_file(path)

    def test_validates_file_with_proper_structure(self, temp_dir):
        """Test that validate_file() accepts file with proper structure."""
        path = Path(temp_dir) / "test.md"
        content = "# Cloud Computing Architecture\n\nCloud computing has fundamentally transformed how organizations design and deploy modern applications by providing unprecedented scalability and flexibility. It provides multiple layers of abstraction including infrastructure, platform, and software services, enabling developers to focus on business logic. Modern enterprises are leveraging cloud services to achieve cost efficiency and rapid innovation.\n"
        path.write_bytes(content.encode('utf-8'))

        result = validate_file(path)
        assert result is True

    def test_rejects_file_with_crlf_line_endings(self, temp_dir):
        """Test that validate_file() rejects file with Windows CRLF line endings."""
        path = Path(temp_dir) / "test.md"
        content = "# Title\r\n\r\nFirst sentence. Second sentence. Third sentence.\r\n"
        path.write_bytes(content.encode('utf-8'))

        with pytest.raises(AssertionError, match="CRLF|LF"):
            validate_file(path)

    def test_rejects_file_with_bom(self, temp_dir):
        """Test that validate_file() rejects file with UTF-8 BOM."""
        path = Path(temp_dir) / "test.md"
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        # Write with UTF-8 BOM using utf-8-sig encoding
        path.write_bytes(content.encode('utf-8-sig'))

        with pytest.raises(AssertionError, match="BOM"):
            validate_file(path)

    def test_error_messages_are_descriptive(self, temp_dir):
        """Test that validation error messages are clear and actionable."""
        path = Path(temp_dir) / "test.md"
        content = "Some content without heading\n\nMore content.\n"
        path.write_bytes(content.encode('utf-8'))

        try:
            validate_file(path)
            pytest.fail("Should have raised AssertionError")
        except AssertionError as e:
            # Error message should be descriptive
            assert len(str(e)) > 10, "Error message should be descriptive"


class TestIntegration:
    """Integration tests for file creation and validation."""

    def test_create_and_validate_workflow(self, temp_dir):
        """Test complete workflow: create file and validate it."""
        # Create file
        filepath = create_file()
        assert filepath.exists()

        # Validate file
        result = validate_file(filepath)
        assert result is True

    def test_multiple_validations_pass(self, temp_dir):
        """Test that a created file passes validation multiple times."""
        filepath = create_file()

        # Validate multiple times
        for i in range(3):
            result = validate_file(filepath)
            assert result is True, f"Validation failed on attempt {i+1}"

    def test_file_structure_matches_specification(self, temp_dir):
        """Test that created file matches specification requirements."""
        filepath = create_file()
        content = filepath.read_text(encoding='utf-8')

        # Specification: # Heading\n\n<2-3 sentences>\n
        lines = content.split('\n')

        # First line should be heading
        assert lines[0].startswith('# '), "First line should be H1 heading"

        # Second line should be empty (blank line)
        assert lines[1] == '', "Second line should be empty (blank line separator)"

        # File should end with newline
        assert content.endswith('\n'), "File should end with newline"

        # Overall validation should pass
        assert validate_file(filepath) is True
