"""
Comprehensive test suite for feature 223: markdown file creation and validation.

This module provides test coverage for creating test-no1878.md with proper
structure, encoding, and line endings following the pattern of 220+ existing
test files in the Sheep project.

Test Coverage:
- File creation with correct structure (H1 heading + blank line + prose)
- Encoding validation (UTF-8 without BOM)
- Line ending validation (Unix LF, no Windows CRLF)
- File size validation (300-500 byte range per NFR-2)
- Prose content validation (2-3 sentences per FR-3)
- Trailing newline validation
- Complete workflow integration
"""

import os
import tempfile
from pathlib import Path
from unittest import mock
import subprocess

import pytest

# Import functions from the implementation script
import sys
script_path = Path(__file__).parent / "create_test_file.py"
sys.path.insert(0, str(Path(__file__).parent))
from create_test_file import create_file, validate_file, git_operations


# ============================================================================
# Pytest Fixtures
# ============================================================================

@pytest.fixture
def temp_dir():
    """
    Provide an isolated temporary directory for test file creation.

    Yields a temporary directory path and restores the original working
    directory after the test completes.

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


# ============================================================================
# Test Classes for File Creation
# ============================================================================

class TestCreateFile:
    """Tests for create_file() function."""

    def test_creates_file_at_repository_root(self):
        """Test that create_file() creates test-no1878.md in the repository root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                filepath = create_file()

                assert filepath.exists(), "File should exist after creation"
                assert filepath.name == "test-no1878.md", "File name should be test-no1878.md"
            finally:
                os.chdir(original_cwd)

    def test_file_contains_h1_heading(self):
        """Test that file contains H1 markdown heading on first line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                content = Path("test-no1878.md").read_text(encoding='utf-8')
                assert content.startswith("# "), "File should start with H1 heading (# )"
            finally:
                os.chdir(original_cwd)

    def test_file_contains_prose_content(self):
        """Test that file contains 2-3 sentences of prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                content = Path("test-no1878.md").read_text(encoding='utf-8')
                # Count sentence terminators
                period_count = content.count('.')
                assert period_count >= 2, f"File should contain at least 2 sentences, found {period_count}"
                assert period_count <= 3, f"File should contain at most 3 sentences, found {period_count}"
            finally:
                os.chdir(original_cwd)

    def test_file_uses_utf8_encoding(self):
        """Test that file is UTF-8 encoded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                # Read as binary and verify it's valid UTF-8
                binary_content = Path("test-no1878.md").read_bytes()
                try:
                    decoded = binary_content.decode('utf-8')
                    assert isinstance(decoded, str), "Should decode to string"
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

                binary_content = Path("test-no1878.md").read_bytes()
                # UTF-8 BOM is b'\xef\xbb\xbf'
                assert not binary_content.startswith(b'\xef\xbb\xbf'), \
                    "File should not have UTF-8 BOM"
            finally:
                os.chdir(original_cwd)

    def test_file_uses_lf_line_endings(self):
        """Test that file uses Unix LF line endings, not Windows CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                binary_content = Path("test-no1878.md").read_bytes()
                # Should not contain CRLF (\r\n)
                assert b'\r\n' not in binary_content, \
                    "File should not have CRLF line endings"
                # Should contain LF (\n)
                assert b'\n' in binary_content, \
                    "File should have LF line endings"
                # Should not contain any CR
                assert b'\r' not in binary_content, \
                    "File should not contain carriage return characters"
            finally:
                os.chdir(original_cwd)

    def test_file_size_in_required_range(self):
        """Test that file size is between 300-500 bytes (per NFR-2)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                file_size = Path("test-no1878.md").stat().st_size
                assert 300 <= file_size <= 500, \
                    f"File size {file_size} bytes outside required range [300, 500]"
            finally:
                os.chdir(original_cwd)

    def test_file_contains_blank_line_after_heading(self):
        """Test that file has blank line separating heading from prose."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                content = Path("test-no1878.md").read_text(encoding='utf-8')
                # Should contain double newline (blank line)
                assert '\n\n' in content, \
                    "File should contain blank line after heading"
            finally:
                os.chdir(original_cwd)

    def test_file_ends_with_newline(self):
        """Test that file ends with a newline character."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file()

                binary_content = Path("test-no1878.md").read_bytes()
                # File must end with LF (\n, which is b'\n' in binary)
                assert binary_content.endswith(b'\n'), \
                    "File should end with a newline character"
            finally:
                os.chdir(original_cwd)

    def test_returns_path_object(self):
        """Test that create_file() returns a Path object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                result = create_file()

                assert isinstance(result, Path), "Should return Path object"
                assert result.name == "test-no1878.md", "Path should point to test-no1878.md"
            finally:
                os.chdir(original_cwd)

    def test_fails_if_file_already_exists(self):
        """Test that create_file() raises FileExistsError if file already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                # Create the file once
                create_file()

                # Attempt to create it again should fail
                with pytest.raises(FileExistsError, match="already exists"):
                    create_file()
            finally:
                os.chdir(original_cwd)


# ============================================================================
# Test Classes for File Validation
# ============================================================================

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
                assert result is True, "Should return True for valid file"
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

            with pytest.raises(AssertionError, match="outside acceptable range"):
                validate_file(path)

    def test_rejects_file_too_large(self):
        """Test that validate_file() rejects file larger than 500 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create very large file
            large_prose = "This is a sentence. " * 30  # Creates content > 500 bytes
            content = f"# Title\n\n{large_prose}\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="outside acceptable range"):
                validate_file(path)

    def test_rejects_missing_h1_heading(self):
        """Test that validate_file() rejects file without H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Use H2 instead of H1 - ensure file is >= 300 bytes
            prose = "First sentence about important topics. Second sentence explaining more. Third sentence concluding thoughts and ideas. " * 3
            content = f"## Second Level\n\n{prose}\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="H1 heading"):
                validate_file(path)

    def test_rejects_missing_blank_line(self):
        """Test that validate_file() rejects file without blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # No blank line between heading and prose - ensure file is >= 300 bytes
            prose = "First sentence about important topics. Second sentence explaining more. Third sentence concluding thoughts and ideas. " * 3
            content = f"# Title\n{prose}\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="blank line"):
                validate_file(path)

    def test_rejects_empty_prose(self):
        """Test that validate_file() rejects file with no prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Proper structure but prose is just whitespace/empty
            content = "# Title\n\n" + " " * 320 + "\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="sentences"):
                validate_file(path)

    def test_rejects_file_with_crlf(self):
        """Test that validate_file() rejects file with Windows CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # CRLF line endings - ensure >= 300 bytes
            prose = "First sentence about important topics and ideas. Second sentence explaining more details. Third sentence concluding thoughts. " * 3
            content = f"# Title\r\n\r\n{prose}\r\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(AssertionError, match="CRLF"):
                validate_file(path)

    def test_rejects_file_with_bom(self):
        """Test that validate_file() rejects file with UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Write with BOM using utf-8-sig encoding - ensure >= 300 bytes
            prose = "First sentence about important topics and ideas. Second sentence explaining more details. Third sentence concluding thoughts. " * 3
            content = f"# Title\n\n{prose}\n"
            path.write_bytes(content.encode('utf-8-sig'))

            with pytest.raises(AssertionError, match="BOM"):
                validate_file(path)

    def test_accepts_files_in_valid_range(self):
        """Test that validate_file() accepts files in 300-500 byte range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create file in valid range with appropriate length
            prose = "Cloud computing has fundamentally transformed how organizations design systems by providing unprecedented scalability. It provides multiple layers including infrastructure, platform, and software services. Modern enterprises are actively leveraging cloud services to optimize operations."
            content = f"# Cloud Computing\n\n{prose}\n"
            path.write_bytes(content.encode('utf-8'))

            file_size = path.stat().st_size
            assert 300 <= file_size <= 500, f"Test file size {file_size} not in range"

            result = validate_file(path)
            assert result is True, "Should validate successfully"

    def test_validates_with_two_sentences(self):
        """Test that validate_file() accepts file with exactly 2 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Exactly 2 sentences
            content = "# Title\n\nFirst sentence about topics. Second sentence concluding ideas and thoughts.\n"
            path.write_bytes(content.encode('utf-8'))

            # Adjust content if needed to get in range
            while len(content.encode('utf-8')) < 300:
                content = "# Title\n\nFirst sentence about topics and ideas. Second sentence concluding ideas and thoughts and words.\n"

            path.write_bytes(content.encode('utf-8'))
            result = validate_file(path)
            assert result is True, "Should accept file with 2 sentences"

    def test_validates_with_three_sentences(self):
        """Test that validate_file() accepts file with exactly 3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create file with exactly 3 sentences
            create_file()  # This has 3 sentences
            result = validate_file(Path("test-no1878.md"))
            assert result is True, "Should accept file with 3 sentences"


# ============================================================================
# Integration Tests
# ============================================================================

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
                assert filepath.exists(), "File should exist"

                # Validate file
                result = validate_file(filepath)
                assert result is True, "Validation should pass"
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
                assert lines[1] == '', "Second line should be empty (blank separator)"

                # Remaining lines should contain prose
                prose_lines = lines[2:]
                prose = '\n'.join(prose_lines).strip()
                assert len(prose) > 0, "Prose content should be present"

                # Validate overall file
                assert validate_file(filepath) is True, "File should pass validation"
            finally:
                os.chdir(original_cwd)

    def test_git_operations_called_correctly(self):
        """Test that git operations use correct parameters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create and validate a file first
                filepath = create_file()
                validate_file(filepath)

                # Mock subprocess.run to verify git commands are correct
                with mock.patch('subprocess.run') as mock_run:
                    git_operations()

                    # Verify subprocess.run was called 3 times
                    assert mock_run.call_count == 3, \
                        "Expected 3 git commands (add, commit, push)"

                    calls = mock_run.call_args_list

                    # Check git add command
                    assert calls[0][0][0] == ['git', 'add', 'test-no1878.md'], \
                        "First call should be git add"
                    assert calls[0][1] == {'check': True}, \
                        "Should use check=True"

                    # Check git commit command (has message argument)
                    assert calls[1][0][0][:2] == ['git', 'commit'], \
                        "Second call should be git commit"
                    assert calls[1][1] == {'check': True}, \
                        "Should use check=True"

                    # Check git push command
                    assert calls[2][0][0] == ['git', 'push', '-u', 'origin', 'HEAD'], \
                        "Third call should be git push"
                    assert calls[2][1] == {'check': True}, \
                        "Should use check=True"

            finally:
                os.chdir(original_cwd)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
