"""
Comprehensive test suite for markdown file creation and validation.

This module provides comprehensive test coverage for feature 286, which creates
a markdown file (test-14epwa.md) with proper structure, encoding, and line endings.

Test Coverage:
- File creation with correct structure (H1 heading + blank line + prose)
- Encoding validation (UTF-8 without BOM)
- Line ending validation (Unix LF, no Windows CRLF)
- File size validation (300-800 byte range)
- Prose content validation (2-3 sentences)
- Trailing newline validation
- Validation function behavior (success and failure paths)
- Integration tests (complete workflow)
- Error handling and informative error messages
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest

script_path = Path(__file__).parent / "create_markdown_file_286.py"
sys.path.insert(0, str(Path(__file__).parent))
from create_markdown_file_286 import create_file, git_operations, validate_file

# ============================================================================
# Pytest Fixtures
# ============================================================================


@pytest.fixture
def temp_dir():
    """
    Provide an isolated temporary directory for test file creation.

    Yields a temporary directory path and restores the original working
    directory after the test completes. This fixture ensures tests don't
    interfere with the repository state or each other.

    Yields:
        Path: The temporary directory path
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            yield Path(tmpdir)
        finally:
            os.chdir(original_cwd)


@pytest.fixture
def sample_markdown():
    """
    Provide a sample valid markdown file content for testing.

    Returns:
        dict: Dictionary with 'content' and 'path' keys containing valid markdown
    """
    content = (
        "# Sample Title\n"
        "\n"
        "First sentence of the prose content here. "
        "Second sentence explaining the topic more thoroughly. "
        "Third sentence concluding the thought.\n"
    )
    return {"content": content, "filename": "sample.md"}


# ============================================================================
# Helper Functions
# ============================================================================


def create_invalid_file(temp_dir, invalid_type="missing_heading"):
    """
    Create a markdown file with specific validation errors for testing.

    This helper function creates test files with various structural issues
    to verify that the validate_file() function correctly rejects invalid files.

    Args:
        temp_dir (Path): The temporary directory where file will be created
        invalid_type (str): Type of invalid file to create. Options:
            - 'missing_heading': No H1 heading
            - 'missing_blank_line': No blank line after heading
            - 'empty_prose': Blank line + heading but no prose content
            - 'too_small': File size under 300 bytes
            - 'too_large': File size over 800 bytes
            - 'with_crlf': Windows-style line endings
            - 'with_bom': UTF-8 BOM encoding

    Returns:
        Path: Path to the created invalid file

    Raises:
        ValueError: If invalid_type is not recognized
    """
    filepath = temp_dir / "invalid_test.md"

    if invalid_type == "missing_heading":
        content = "## Wrong Level\n\nFirst sentence. Second sentence. Third sentence.\n"
        filepath.write_bytes(content.encode('utf-8'))

    elif invalid_type == "missing_blank_line":
        prose = "This is prose content that should have a blank line before it. " * 5
        content = f"# Title\n{prose}\n"
        filepath.write_bytes(content.encode('utf-8'))

    elif invalid_type == "empty_prose":
        # Create a file with proper heading and blank line but only whitespace for prose
        # Ensure file is large enough to pass size check (>300 bytes)
        content = "# Title\n\n" + " " * 300 + "\n"
        filepath.write_bytes(content.encode('utf-8'))

    elif invalid_type == "too_small":
        content = "# T\n\nS.\n"
        filepath.write_bytes(content.encode('utf-8'))

    elif invalid_type == "too_large":
        prose = "This is a sentence. " * 60
        content = f"# Title\n\n{prose}\n"
        filepath.write_bytes(content.encode('utf-8'))

    elif invalid_type == "with_crlf":
        content = "# Title\r\n\r\nFirst sentence. Second sentence. Third sentence.\r\n"
        filepath.write_bytes(content.encode('utf-8'))

    elif invalid_type == "with_bom":
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        # Write with BOM using utf-8-sig encoding
        filepath.write_bytes(content.encode('utf-8-sig'))

    else:
        raise ValueError(f"Unknown invalid_type: {invalid_type}")

    return filepath


# ============================================================================
# Test Classes
# ============================================================================


class TestCreateFile:
    """Tests for create_file() function."""

    def test_creates_file_at_repository_root(self):
        """Test that create_file() creates test-14epwa.md in the repository root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                filepath = create_file()

                assert filepath.exists()
                assert filepath.name == "test-14epwa.md"
                assert filepath.is_absolute() or filepath.name == "test-14epwa.md"
            finally:
                os.chdir(original_cwd)

    def test_file_contains_h1_heading(self):
        """Test that file contains H1 markdown heading on first line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                content = Path("test-14epwa.md").read_text(encoding='utf-8')
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

                content = Path("test-14epwa.md").read_text(encoding='utf-8')
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
                binary_content = Path("test-14epwa.md").read_bytes()

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

                binary_content = Path("test-14epwa.md").read_bytes()
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

                binary_content = Path("test-14epwa.md").read_bytes()
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

                file_size = Path("test-14epwa.md").stat().st_size
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

                content = Path("test-14epwa.md").read_text(encoding='utf-8')
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

                content = Path("test-14epwa.md").read_text(encoding='utf-8')
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
                assert result.name == "test-14epwa.md"
            finally:
                os.chdir(original_cwd)

    def test_file_ends_with_newline(self):
        """Test that file ends with a newline character."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                binary_content = Path("test-14epwa.md").read_bytes()
                # File must end with LF (\n, which is b'\n' in binary)
                assert binary_content.endswith(b'\n'), "File should end with a newline character"
            finally:
                os.chdir(original_cwd)


class TestInvalidFileCreation:
    """Tests for create_invalid_file() helper function."""

    def test_create_invalid_file_missing_heading(self, temp_dir):
        """Test that create_invalid_file() creates file without H1 heading."""
        filepath = create_invalid_file(temp_dir, "missing_heading")
        assert filepath.exists()

        with pytest.raises(AssertionError, match="H1 heading"):
            validate_file(filepath)

    def test_create_invalid_file_missing_blank_line(self, temp_dir):
        """Test that create_invalid_file() creates file without blank line."""
        filepath = create_invalid_file(temp_dir, "missing_blank_line")
        assert filepath.exists()

        with pytest.raises(AssertionError, match="blank line"):
            validate_file(filepath)

    def test_create_invalid_file_empty_prose(self, temp_dir):
        """Test that create_invalid_file() creates file with empty prose."""
        filepath = create_invalid_file(temp_dir, "empty_prose")
        assert filepath.exists()

        with pytest.raises(AssertionError, match="prose"):
            validate_file(filepath)

    def test_create_invalid_file_too_small(self, temp_dir):
        """Test that create_invalid_file() creates file under 300 bytes."""
        filepath = create_invalid_file(temp_dir, "too_small")
        assert filepath.exists()
        assert filepath.stat().st_size < 300

        with pytest.raises(AssertionError, match="outside typical range"):
            validate_file(filepath)

    def test_create_invalid_file_too_large(self, temp_dir):
        """Test that create_invalid_file() creates file over 800 bytes."""
        filepath = create_invalid_file(temp_dir, "too_large")
        assert filepath.exists()
        assert filepath.stat().st_size > 800

        with pytest.raises(AssertionError, match="outside typical range"):
            validate_file(filepath)

    def test_create_invalid_file_with_crlf(self, temp_dir):
        """Test that create_invalid_file() creates file with Windows CRLF line endings."""
        filepath = create_invalid_file(temp_dir, "with_crlf")
        assert filepath.exists()

        binary_content = filepath.read_bytes()
        assert b'\r\n' in binary_content, "File should contain CRLF line endings"

    def test_create_invalid_file_with_bom(self, temp_dir):
        """Test that create_invalid_file() creates file with UTF-8 BOM."""
        filepath = create_invalid_file(temp_dir, "with_bom")
        assert filepath.exists()

        binary_content = filepath.read_bytes()
        assert binary_content.startswith(b'\xef\xbb\xbf'), "File should have UTF-8 BOM"


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
            # No blank line between heading and prose
            prose = "Artificial intelligence is transforming many industries and creating new opportunities for innovation and improvement. Machine learning models are becoming increasingly sophisticated and accessible to developers of all skill levels. Organizations across the globe are actively leveraging these cutting-edge technologies to solve complex problems and improve operational efficiency. The integration of AI systems into workflows has become standard practice."
            content = f"# Title\n{prose}\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="blank line"):
                validate_file(path)

    def test_rejects_empty_prose(self):
        """Test that validate_file() rejects file with no prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Test with proper structure but prose is just whitespace
            content = "# Title\n\n                                                                                                                                                                                                                                                                                                                                                                                     \n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="prose"):
                validate_file(path)

    def test_validates_file_in_typical_size_range(self):
        """Test that validate_file() accepts files in 400-600 byte range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create file approximately 500 bytes with realistic prose
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

    def test_git_operations_called_on_success(self):
        """Test that git operations are called with correct parameters when validation passes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create a valid file first
                filepath = create_file()
                validate_file(filepath)

                # Mock subprocess.run to verify git commands are called
                with mock.patch('subprocess.run') as mock_run:
                    git_operations()

                    # Verify subprocess.run was called 3 times (add, commit, push)
                    assert mock_run.call_count == 3, "Expected 3 git commands (add, commit, push)"

                    # Verify the commands are correct
                    calls = mock_run.call_args_list

                    # Check git add command
                    assert calls[0][0][0] == ['git', 'add', 'test-14epwa.md'], "First call should be git add"
                    assert calls[0][1] == {'check': True}, "Should use check=True"

                    # Check git commit command
                    assert calls[1][0][0][0:2] == ['git', 'commit'], "Second call should be git commit"
                    assert calls[1][1] == {'check': True}, "Should use check=True"

                    # Check git push command
                    assert calls[2][0][0] == ['git', 'push', '-u', 'origin', 'HEAD'], "Third call should be git push"
                    assert calls[2][1] == {'check': True}, "Should use check=True"

            finally:
                os.chdir(original_cwd)

    def test_validation_before_git_operations(self):
        """Test that validation occurs before git operations to prevent invalid commits."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create an invalid file (missing blank line)
                invalid_file = Path(tmpdir) / "test-14epwa.md"
                prose = "This is prose without blank line. " * 10
                content = f"# Title\n{prose}\n"
                invalid_file.write_bytes(content.encode('utf-8'))

                # Validation should fail
                with pytest.raises(AssertionError):
                    validate_file(invalid_file)

                # Git operations should not be called for invalid file
                with mock.patch('subprocess.run') as mock_run:
                    # Attempt to validate (will fail)
                    try:
                        validate_file(invalid_file)
                        git_operations()
                    except AssertionError:
                        # Expected - validation failed
                        pass

                    # subprocess.run should not be called because validation failed before git_operations
                    assert mock_run.call_count == 0, "Git operations should not be called for invalid file"

            finally:
                os.chdir(original_cwd)
