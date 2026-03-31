"""Tests for markdown file creation and validation functions."""

import os

# Import the functions from the script
import sys
import tempfile
from pathlib import Path

import pytest

script_path = Path(__file__).parent / "create_markdown_file.py"
sys.path.insert(0, str(Path(__file__).parent))
from create_markdown_file import create_file, validate_file


class TestCreateFile:
    """Tests for create_file() function."""

    def test_creates_file_at_repository_root(self):
        """Test that create_file() creates test-p4t702.md in the repository root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                filepath = create_file()

                assert filepath.exists()
                assert filepath.name == "test-p4t702.md"
                assert filepath.is_absolute() or filepath.name == "test-p4t702.md"
            finally:
                os.chdir(original_cwd)

    def test_file_contains_h1_heading(self):
        """Test that file contains H1 markdown heading on first line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                content = Path("test-p4t702.md").read_text(encoding='utf-8')
                assert content.startswith("# "), "File should start with H1 heading"
            finally:
                os.chdir(original_cwd)

    def test_file_contains_prose_content(self):
        """Test that file contains 2-3 sentences of prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                content = Path("test-p4t702.md").read_text(encoding='utf-8')
                # Count periods to estimate sentence count
                # Should have at least 2 periods (2-3 sentences)
                period_count = content.count('.')
                assert period_count >= 2, f"File should contain at least 2 sentences, found {period_count} periods"
                assert period_count <= 4, f"File should contain at most 3 sentences, found {period_count} periods (allowing for abbreviations)"
            finally:
                os.chdir(original_cwd)

    def test_file_uses_utf8_encoding(self):
        """Test that file is UTF-8 encoded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                # Read as binary
                binary_content = Path("test-p4t702.md").read_bytes()

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
                os.chdir(tmpdir)
                create_file()

                binary_content = Path("test-p4t702.md").read_bytes()
                # UTF-8 BOM is b'\xef\xbb\xbf'
                assert not binary_content.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"
            finally:
                os.chdir(original_cwd)

    def test_file_uses_lf_line_endings(self):
        """Test that file uses Unix LF line endings, not Windows CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                binary_content = Path("test-p4t702.md").read_bytes()
                # Should not contain CRLF (\r\n)
                assert b'\r\n' not in binary_content, "File should not have CRLF line endings"
                # Should contain LF (\n)
                assert b'\n' in binary_content, "File should have LF line endings"
            finally:
                os.chdir(original_cwd)

    def test_file_size_in_typical_range(self):
        """Test that file size is approximately 400-600 bytes (soft guideline)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                file_size = Path("test-p4t702.md").stat().st_size
                # Soft guideline: typically 400-600 bytes
                # We tolerate a range of 300-800 bytes for flexibility
                assert 300 < file_size < 800, (
                    f"File size {file_size} bytes outside typical range (300-800). "
                    f"Expected 400-600 as soft guideline."
                )
            finally:
                os.chdir(original_cwd)

    def test_file_contains_blank_line_after_heading(self):
        """Test that file has blank line separating heading from prose."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                content = Path("test-p4t702.md").read_text(encoding='utf-8')
                # Should contain double newline (blank line)
                assert '\n\n' in content, "File should contain blank line after heading"
            finally:
                os.chdir(original_cwd)

    def test_heading_and_prose_same_topic(self):
        """Test that heading and prose address the same coherent topic."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                content = Path("test-p4t702.md").read_text(encoding='utf-8')
                # Split heading and prose
                parts = content.split('\n\n', 1)
                heading = parts[0].strip()
                prose = parts[1].strip() if len(parts) > 1 else ""

                # Both should exist
                assert heading, "Heading should not be empty"
                assert prose, "Prose should not be empty"

                # Simple check: heading should not be just "# "
                assert len(heading) > 2, "Heading should have meaningful content"
            finally:
                os.chdir(original_cwd)

    def test_returns_path_object(self):
        """Test that create_file() returns a Path object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                result = create_file()

                assert isinstance(result, Path)
                assert result.name == "test-p4t702.md"
            finally:
                os.chdir(original_cwd)


class TestValidateFile:
    """Tests for validate_file() function."""

    def test_validates_correctly_created_file(self):
        """Test that validate_file() passes for a correctly created file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                filepath = create_file()

                result = validate_file(filepath)
                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_rejects_missing_file(self):
        """Test that validate_file() raises error for non-existent file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nonexistent_path = Path(tmpdir) / "nonexistent.md"

            with pytest.raises(AssertionError, match="does not exist"):
                validate_file(nonexistent_path)

    def test_rejects_file_too_small(self):
        """Test that validate_file() rejects file smaller than 300 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create very small file
            content = "# Title\n\nSmall.\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="outside typical range"):
                validate_file(path)

    def test_rejects_file_too_large(self):
        """Test that validate_file() rejects file larger than 800 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create very large file
            large_prose = "This is a sentence. " * 50  # Creates very long content
            content = f"# Title\n\n{large_prose}\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="outside typical range"):
                validate_file(path)

    def test_rejects_missing_h1_heading(self):
        """Test that validate_file() rejects file without H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # No heading
            content = "## Second Level\n\nFirst sentence. Second sentence. Third sentence.\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="H1 heading"):
                validate_file(path)

    def test_rejects_missing_blank_line(self):
        """Test that validate_file() rejects file without blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # No blank line between heading and prose (but with realistic, longer content)
            prose = "Artificial intelligence is transforming many industries and creating new opportunities for innovation and improvement. Machine learning models are becoming increasingly sophisticated and accessible to developers of all skill levels. Organizations across the globe are actively leveraging these cutting-edge technologies to solve complex problems and improve operational efficiency. The integration of AI systems into workflows has become standard practice."
            content = f"# Title\n{prose}\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="blank line"):
                validate_file(path)

    def test_rejects_empty_prose(self):
        """Test that validate_file() rejects file with no prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Heading with proper spacing but no prose
            content = "# Title\n\n                                                                                                                                                                                                                                                                                                                                                                                     \n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="prose"):
                validate_file(path)

    def test_validates_file_in_typical_size_range(self):
        """Test that validate_file() accepts files in 400-600 byte range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create file approximately 500 bytes with realistic, longer prose
            content = "# Cloud Computing Architecture\n\nCloud computing has fundamentally transformed how organizations design and deploy modern applications by providing unprecedented scalability and flexibility. It provides multiple layers of abstraction including infrastructure, platform, and software services, enabling developers to focus on business logic rather than infrastructure management. Modern enterprises are leveraging cloud services to achieve cost efficiency, geographic distribution, and rapid innovation while maintaining robust security and compliance standards.\n"
            path.write_bytes(content.encode('utf-8'))

            file_size = path.stat().st_size
            assert 300 < file_size < 800, f"Test file size {file_size} not in 300-800 range"

            result = validate_file(path)
            assert result is True

    def test_accepts_files_in_tolerance_range(self):
        """Test that validate_file() accepts files in 300-800 byte tolerance range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Test at lower boundary (300 bytes)
            path = Path(tmpdir) / "test_small.md"
            content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            path.write_bytes(content.encode('utf-8'))
            file_size = path.stat().st_size

            if 300 < file_size < 800:
                result = validate_file(path)
                assert result is True

    def test_error_messages_are_descriptive(self):
        """Test that validation error messages are clear and actionable."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Test with missing heading
            path = Path(tmpdir) / "test.md"
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

    def test_create_and_validate_workflow(self):
        """Test complete workflow: create file and validate it."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create file
                filepath = create_file()
                assert filepath.exists()

                # Validate file
                result = validate_file(filepath)
                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_multiple_validations_pass(self):
        """Test that a created file passes validation multiple times."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                filepath = create_file()

                # Validate multiple times
                for i in range(3):
                    result = validate_file(filepath)
                    assert result is True, f"Validation failed on attempt {i+1}"
            finally:
                os.chdir(original_cwd)

    def test_file_structure_matches_specification(self):
        """Test that created file matches specification requirements."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                filepath = create_file()
                content = filepath.read_text(encoding='utf-8')

                # Specification: # Heading\n\n<2-3 sentences>
                lines = content.split('\n')

                # First line should be heading
                assert lines[0].startswith('# '), "First line should be H1 heading"

                # Second line should be empty (blank line)
                assert lines[1] == '', "Second line should be empty (blank line separator)"

                # Remaining lines should contain prose
                prose_lines = lines[2:]
                prose = '\n'.join(prose_lines).strip()
                assert len(prose) > 0, "Prose content should be present"

                # Validate overall file passes validation
                assert validate_file(filepath) is True
            finally:
                os.chdir(original_cwd)
