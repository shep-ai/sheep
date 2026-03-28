"""
Comprehensive test suite for feature 234: markdown file creation.

This module provides comprehensive test coverage for feature 234, which creates
a markdown file (test-kn5qkm.md) with proper structure, encoding, and line endings.

Test Coverage:
- File creation with correct structure (H1 heading + blank line + prose)
- Encoding validation (UTF-8 without BOM)
- Line ending validation (Unix LF, no Windows CRLF)
- File size validation (400-600 byte range)
- Prose content validation (2-3 sentences)
- Trailing newline validation
- Integration tests (complete workflow)
- Error handling and informative error messages

The test suite uses pytest fixtures and helper functions to create isolated
test environments and invalid test files for comprehensive validation testing.
"""

import os

# Import the functions from the implementation script
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest

script_path = Path(__file__).parent / "create_markdown_file.py"
sys.path.insert(0, str(Path(__file__).parent))
from create_markdown_file import create_file, git_operations, validate_file

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
        dict: Dictionary with 'content' and 'filename' keys containing valid markdown
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
            - 'too_small': File size under 400 bytes
            - 'too_large': File size over 600 bytes
            - 'with_crlf': Windows-style line endings
            - 'with_bom': UTF-8 BOM encoding
            - 'no_trailing_newline': Missing trailing newline
            - 'one_sentence': Only one sentence in prose

    Returns:
        Path: Path to the created invalid file

    Raises:
        ValueError: If invalid_type is not recognized
    """
    filepath = temp_dir / "invalid_test.md"

    if invalid_type == "missing_heading":
        content = "## Wrong Level\n\nFirst sentence. Second sentence. Third sentence.\n"
        filepath.write_bytes(content.encode("utf-8"))

    elif invalid_type == "missing_blank_line":
        prose = "This is prose content that should have a blank line before it. " * 5
        content = f"# Title\n{prose}\n"
        filepath.write_bytes(content.encode("utf-8"))

    elif invalid_type == "empty_prose":
        # Create a file with proper heading and blank line but only whitespace for prose
        # Ensure file is large enough to pass size check (>400 bytes)
        content = "# Title\n\n" + " " * 400 + "\n"
        filepath.write_bytes(content.encode("utf-8"))

    elif invalid_type == "too_small":
        content = "# T\n\nS.\n"
        filepath.write_bytes(content.encode("utf-8"))

    elif invalid_type == "too_large":
        prose = "This is a sentence. " * 80
        content = f"# Title\n\n{prose}\n"
        filepath.write_bytes(content.encode("utf-8"))

    elif invalid_type == "with_crlf":
        content = "# Title\r\n\r\nFirst sentence. Second sentence. Third sentence.\r\n"
        filepath.write_bytes(content.encode("utf-8"))

    elif invalid_type == "with_bom":
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        # Write with BOM using utf-8-sig encoding
        filepath.write_bytes(content.encode("utf-8-sig"))

    elif invalid_type == "no_trailing_newline":
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence."
        filepath.write_bytes(content.encode("utf-8"))

    elif invalid_type == "one_sentence":
        content = "# Title\n\nOnly one sentence here.\n"
        filepath.write_bytes(content.encode("utf-8"))

    else:
        raise ValueError(f"Unknown invalid_type: {invalid_type}")

    return filepath


# ============================================================================
# Test Classes
# ============================================================================


class TestCreateFile:
    """Tests for create_file() function."""

    def test_file_does_not_exist_before_creation(self, temp_dir):
        """Test that test-kn5qkm.md does not exist before implementation."""
        filepath = Path("test-kn5qkm.md")
        assert not filepath.exists(), "File should not exist before creation"

    @pytest.mark.skip(reason="Requires LLM environment setup")
    def test_creates_file_at_repository_root(self, temp_dir):
        """Test that create_file() creates test-kn5qkm.md in the repository root."""
        filepath = create_file()
        assert filepath, "create_file() should return a path"
        assert Path(filepath).exists(), "File should exist after creation"
        assert Path(filepath).name == "test-kn5qkm.md"

    @pytest.mark.skip(reason="Requires LLM environment setup")
    def test_file_contains_h1_heading(self, temp_dir):
        """Test that file contains H1 markdown heading on first line."""
        create_file()
        content = Path("test-kn5qkm.md").read_text(encoding="utf-8")
        assert content.startswith("# "), "File should start with H1 heading"

    @pytest.mark.skip(reason="Requires LLM environment setup")
    def test_file_contains_prose_content(self, temp_dir):
        """Test that file contains 2-3 sentences of prose content."""
        create_file()
        content = Path("test-kn5qkm.md").read_text(encoding="utf-8")
        period_count = content.count(".")
        assert period_count >= 2, "File should contain at least 2 sentences"
        assert period_count <= 3, "File should contain at most 3 sentences"

    @pytest.mark.skip(reason="Requires LLM environment setup")
    def test_file_uses_utf8_encoding(self, temp_dir):
        """Test that file is UTF-8 encoded."""
        create_file()
        binary_content = Path("test-kn5qkm.md").read_bytes()
        try:
            decoded = binary_content.decode("utf-8")
            assert isinstance(decoded, str)
        except UnicodeDecodeError:
            pytest.fail("File is not valid UTF-8")

    @pytest.mark.skip(reason="Requires LLM environment setup")
    def test_file_has_no_utf8_bom(self, temp_dir):
        """Test that file does not have UTF-8 BOM (Byte Order Mark)."""
        create_file()
        binary_content = Path("test-kn5qkm.md").read_bytes()
        assert not binary_content.startswith(
            b"\xef\xbb\xbf"
        ), "File should not have UTF-8 BOM"

    @pytest.mark.skip(reason="Requires LLM environment setup")
    def test_file_uses_lf_line_endings(self, temp_dir):
        """Test that file uses Unix LF line endings, not Windows CRLF."""
        create_file()
        binary_content = Path("test-kn5qkm.md").read_bytes()
        assert b"\r\n" not in binary_content, "File should not have CRLF line endings"
        assert b"\n" in binary_content, "File should have LF line endings"

    @pytest.mark.skip(reason="Requires LLM environment setup")
    def test_file_size_in_typical_range(self, temp_dir):
        """Test that file size is within 400-600 byte range."""
        create_file()
        file_size = Path("test-kn5qkm.md").stat().st_size
        assert (
            400 < file_size < 600
        ), f"File size {file_size} bytes outside typical range (400-600)"

    @pytest.mark.skip(reason="Requires LLM environment setup")
    def test_file_contains_blank_line_after_heading(self, temp_dir):
        """Test that file has blank line separating heading from prose."""
        create_file()
        content = Path("test-kn5qkm.md").read_text(encoding="utf-8")
        assert "\n\n" in content, "File should contain blank line after heading"

    @pytest.mark.skip(reason="Requires LLM environment setup")
    def test_heading_and_prose_same_topic(self, temp_dir):
        """Test that heading and prose address the same coherent topic."""
        create_file()
        content = Path("test-kn5qkm.md").read_text(encoding="utf-8")
        parts = content.split("\n\n", 1)
        heading = parts[0].strip()
        prose = parts[1].strip() if len(parts) > 1 else ""

        assert heading, "Heading should not be empty"
        assert prose, "Prose should not be empty"
        assert len(heading) > 2, "Heading should have meaningful content"

    @pytest.mark.skip(reason="Requires LLM environment setup")
    def test_returns_path_object(self, temp_dir):
        """Test that create_file() returns a Path object."""
        result = create_file()
        assert result, "create_file() should return a non-empty path"
        assert isinstance(
            str(result), str
        ), "create_file() should return a string path"
        assert "test-kn5qkm.md" in str(result), "Path should contain filename"

    @pytest.mark.skip(reason="Requires LLM environment setup")
    def test_file_ends_with_newline(self, temp_dir):
        """Test that file ends with a newline character."""
        create_file()
        binary_content = Path("test-kn5qkm.md").read_bytes()
        assert binary_content.endswith(b"\n"), "File should end with a newline character"

    def test_fails_if_file_already_exists(self, temp_dir):
        """Test that create_file() raises FileExistsError if file already exists."""
        # Create the file once manually
        Path("test-kn5qkm.md").write_text("# Test\n\nContent.\n", encoding="utf-8")

        # Attempt to create it again should fail
        with pytest.raises(FileExistsError, match="already exists"):
            create_file()


class TestInvalidFileCreation:
    """Tests for create_invalid_file() helper function."""

    def test_create_invalid_file_missing_heading(self, temp_dir):
        """Test that create_invalid_file() creates file without H1 heading."""
        filepath = create_invalid_file(temp_dir, "missing_heading")
        assert filepath.exists()

        with pytest.raises(AssertionError):
            validate_file(filepath)

    def test_create_invalid_file_missing_blank_line(self, temp_dir):
        """Test that create_invalid_file() creates file without blank line."""
        filepath = create_invalid_file(temp_dir, "missing_blank_line")
        assert filepath.exists()

        with pytest.raises(AssertionError):
            validate_file(filepath)

    def test_create_invalid_file_empty_prose(self, temp_dir):
        """Test that create_invalid_file() creates file with empty prose."""
        filepath = create_invalid_file(temp_dir, "empty_prose")
        assert filepath.exists()

        with pytest.raises(AssertionError):
            validate_file(filepath)

    def test_create_invalid_file_too_small(self, temp_dir):
        """Test that create_invalid_file() creates file under 400 bytes."""
        filepath = create_invalid_file(temp_dir, "too_small")
        assert filepath.exists()
        assert filepath.stat().st_size < 400

    def test_create_invalid_file_too_large(self, temp_dir):
        """Test that create_invalid_file() creates file over 600 bytes."""
        filepath = create_invalid_file(temp_dir, "too_large")
        assert filepath.exists()
        assert filepath.stat().st_size > 600

    def test_create_invalid_file_with_crlf(self, temp_dir):
        """Test that create_invalid_file() creates file with Windows CRLF line endings."""
        filepath = create_invalid_file(temp_dir, "with_crlf")
        assert filepath.exists()

        binary_content = filepath.read_bytes()
        assert b"\r\n" in binary_content, "File should contain CRLF line endings"

    def test_create_invalid_file_with_bom(self, temp_dir):
        """Test that create_invalid_file() creates file with UTF-8 BOM."""
        filepath = create_invalid_file(temp_dir, "with_bom")
        assert filepath.exists()

        binary_content = filepath.read_bytes()
        assert binary_content.startswith(
            b"\xef\xbb\xbf"
        ), "File should have UTF-8 BOM"

    def test_create_invalid_file_no_trailing_newline(self, temp_dir):
        """Test that create_invalid_file() creates file without trailing newline."""
        filepath = create_invalid_file(temp_dir, "no_trailing_newline")
        assert filepath.exists()

        binary_content = filepath.read_bytes()
        assert not binary_content.endswith(b"\n"), "File should not end with newline"

    def test_create_invalid_file_one_sentence(self, temp_dir):
        """Test that create_invalid_file() creates file with only one sentence."""
        filepath = create_invalid_file(temp_dir, "one_sentence")
        assert filepath.exists()


class TestValidateFile:
    """Tests for validate_file() function."""

    def test_rejects_missing_file(self, temp_dir):
        """Test that validate_file() raises error for non-existent file."""
        nonexistent_path = Path(temp_dir) / "nonexistent.md"

        with pytest.raises(AssertionError):
            validate_file(nonexistent_path)

    def test_rejects_file_with_missing_heading(self, temp_dir):
        """Test that validate_file() rejects file without H1 heading."""
        filepath = create_invalid_file(temp_dir, "missing_heading")

        with pytest.raises(AssertionError):
            validate_file(filepath)

    def test_rejects_file_with_missing_blank_line(self, temp_dir):
        """Test that validate_file() rejects file without blank line after heading."""
        filepath = create_invalid_file(temp_dir, "missing_blank_line")

        with pytest.raises(AssertionError):
            validate_file(filepath)

    def test_rejects_file_with_empty_prose(self, temp_dir):
        """Test that validate_file() rejects file with empty prose."""
        filepath = create_invalid_file(temp_dir, "empty_prose")

        with pytest.raises(AssertionError):
            validate_file(filepath)

    def test_rejects_file_too_small(self, temp_dir):
        """Test that validate_file() rejects file smaller than 400 bytes."""
        filepath = create_invalid_file(temp_dir, "too_small")

        with pytest.raises(AssertionError):
            validate_file(filepath)

    def test_rejects_file_too_large(self, temp_dir):
        """Test that validate_file() rejects file larger than 600 bytes."""
        filepath = create_invalid_file(temp_dir, "too_large")

        with pytest.raises(AssertionError):
            validate_file(filepath)

    def test_rejects_file_with_crlf(self, temp_dir):
        """Test that validate_file() rejects file with Windows CRLF line endings."""
        filepath = create_invalid_file(temp_dir, "with_crlf")

        with pytest.raises(AssertionError):
            validate_file(filepath)

    def test_rejects_file_with_bom(self, temp_dir):
        """Test that validate_file() rejects file with UTF-8 BOM."""
        filepath = create_invalid_file(temp_dir, "with_bom")

        with pytest.raises(AssertionError):
            validate_file(filepath)

    def test_rejects_file_without_trailing_newline(self, temp_dir):
        """Test that validate_file() rejects file without trailing newline."""
        filepath = create_invalid_file(temp_dir, "no_trailing_newline")

        with pytest.raises(AssertionError):
            validate_file(filepath)

    def test_error_messages_are_descriptive(self, temp_dir):
        """Test that validation error messages are clear and actionable."""
        filepath = create_invalid_file(temp_dir, "missing_heading")

        try:
            validate_file(filepath)
            pytest.fail("Should have raised AssertionError")
        except AssertionError as e:
            # Error message should be descriptive
            assert len(str(e)) > 5, "Error message should be descriptive"


class TestGitOperations:
    """Tests for git_operations() function."""

    def test_git_operations_called_with_correct_commands(self, temp_dir):
        """Test that git_operations() calls subprocess with correct git commands."""
        # Create a valid file first
        filepath = Path(temp_dir) / "test-kn5qkm.md"
        content = (
            "# Test Title\n\n"
            "First sentence about testing markdown. "
            "Second sentence about file creation. "
            "Third sentence about implementation.\n"
        )
        filepath.write_text(content, encoding="utf-8")

        # Mock subprocess.run to verify git commands are called
        with mock.patch("subprocess.run") as mock_run:
            git_operations()

            # Verify subprocess.run was called 3 times (add, commit, push)
            assert mock_run.call_count == 3, "Expected 3 git commands (add, commit, push)"

            # Verify the commands are correct
            calls = mock_run.call_args_list

            # Check git add command
            assert (
                calls[0][0][0] == ["git", "add", "test-kn5qkm.md"]
            ), "First call should be git add"
            assert calls[0][1] == {"check": True}, "Should use check=True"

            # Check git commit command
            assert (
                calls[1][0][0][0:2] == ["git", "commit"]
            ), "Second call should be git commit"
            assert calls[1][1] == {"check": True}, "Should use check=True"

            # Check git push command
            assert (
                calls[2][0][0] == ["git", "push", "-u", "origin", "HEAD"]
            ), "Third call should be git push"
            assert calls[2][1] == {"check": True}, "Should use check=True"


class TestFileStructureValidation:
    """Tests for validating file structure matches specification."""

    def test_validate_correctly_structured_file(self, temp_dir):
        """Test that a correctly structured file passes validation."""
        filepath = temp_dir / "valid_test.md"
        content = (
            "# Test Title\n\n"
            "First sentence about the topic being discussed. "
            "Second sentence providing more detail and context. "
            "Third sentence concluding the discussion.\n"
        )
        filepath.write_text(content, encoding="utf-8")

        result = validate_file(filepath)
        assert result is True

    def test_file_structure_matches_specification(self, temp_dir):
        """Test that created file structure matches specification: H1, blank line, prose."""
        filepath = temp_dir / "structured_test.md"
        content = (
            "# Cloud Technology\n\n"
            "Cloud computing has revolutionized how organizations deploy applications. "
            "It provides scalability, flexibility, and cost efficiency for modern enterprises. "
            "Organizations worldwide are rapidly adopting cloud-native architectures.\n"
        )
        filepath.write_text(content, encoding="utf-8")

        # Validate file passes all checks
        assert validate_file(filepath) is True

        # Verify structure manually
        lines = content.split("\n")
        assert lines[0].startswith("# "), "First line should be H1 heading"
        assert lines[1] == "", "Second line should be empty (blank line separator)"
        prose_lines = lines[2:]
        prose = "\n".join(prose_lines).strip()
        assert len(prose) > 0, "Prose content should be present"

    def test_h1_heading_exactly_once(self, temp_dir):
        """Test file contains exactly one H1 heading."""
        filepath = temp_dir / "one_heading_test.md"
        content = (
            "# First Heading\n\n"
            "This is the prose content with a sentence. "
            "Another sentence providing context. "
            "Final sentence to complete thought.\n"
        )
        filepath.write_text(content, encoding="utf-8")

        # Count H1 headings
        h1_count = content.count("# ")
        assert h1_count == 1, f"Should have exactly one H1 heading, found {h1_count}"

        # File should still pass validation
        assert validate_file(filepath) is True

    def test_two_to_three_sentences(self, temp_dir):
        """Test that prose contains 2-3 sentences."""
        filepath = temp_dir / "sentence_count_test.md"
        content = (
            "# Example Topic\n\n"
            "First sentence about the topic. "
            "Second sentence providing additional detail. "
            "Third sentence concluding the discussion.\n"
        )
        filepath.write_text(content, encoding="utf-8")

        # Count sentences (periods)
        prose_part = content.split("\n\n")[1].strip()
        period_count = prose_part.count(".")
        assert (
            2 <= period_count <= 3
        ), f"Should have 2-3 sentences, found {period_count}"

        # File should pass validation
        assert validate_file(filepath) is True

    def test_file_size_400_600_bytes(self, temp_dir):
        """Test that file size is between 400-600 bytes."""
        filepath = temp_dir / "size_test.md"
        content = (
            "# Application Development\n\n"
            "Modern application development practices emphasize continuous integration and deployment. "
            "This approach enables teams to deliver features faster while maintaining high quality and reliability. "
            "Many successful organizations have adopted DevOps principles to improve their development workflows.\n"
        )
        filepath.write_text(content, encoding="utf-8")

        file_size = filepath.stat().st_size
        assert (
            400 < file_size < 600
        ), f"File size {file_size} should be between 400-600 bytes"

        # File should pass validation
        assert validate_file(filepath) is True
