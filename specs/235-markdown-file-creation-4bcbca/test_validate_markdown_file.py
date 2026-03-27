"""
Comprehensive test suite for feature 235: markdown file validation.

This module provides comprehensive test coverage for the validation module
which validates markdown files created as part of feature 235.

Test Coverage:
- File existence validation
- Encoding validation (UTF-8 without BOM)
- Line ending validation (Unix LF, no Windows CRLF)
- File size validation (400-600 byte range)
- H1 heading validation (exactly one on first line)
- Blank line separator validation
- Prose content validation (substantive, not whitespace)
- Sentence count validation (2-3 sentences)
- Trailing newline validation
- Error handling and descriptive error messages
- Sentence counting functionality

The test suite uses pytest fixtures and helper functions to create isolated
test environments and invalid test files for comprehensive validation testing.
"""

import os
import tempfile
from pathlib import Path

import pytest

# Import the validation functions
import sys

script_path = Path(__file__).parent / "validate_markdown_file.py"
sys.path.insert(0, str(Path(__file__).parent))
from validate_markdown_file import (
    validate_file,
    validate_encoding,
    validate_line_endings,
    validate_trailing_newline,
    validate_file_size,
    validate_h1_heading,
    validate_blank_line_separator,
    validate_prose_content,
    count_sentences,
    validate_sentence_count,
)


# ============================================================================
# Pytest Fixtures
# ============================================================================


@pytest.fixture
def temp_dir():
    """
    Provide an isolated temporary directory for test file creation.

    Yields a temporary directory path and restores the original working
    directory after the test completes. This fixture ensures tests don't
    interfere with each other.

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
            - 'empty_prose': Blank line + heading but only whitespace for prose
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


class TestEncodeValidation:
    """Tests for validate_encoding() function."""

    def test_accepts_valid_utf8_content(self, temp_dir):
        """Test that UTF-8 content without BOM is accepted."""
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        binary = content.encode("utf-8")
        # Should not raise any exception
        validate_encoding(binary)

    def test_rejects_utf8_with_bom(self, temp_dir):
        """Test that UTF-8 content with BOM is rejected."""
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        binary = content.encode("utf-8-sig")  # Adds BOM

        with pytest.raises(AssertionError, match="UTF-8 BOM"):
            validate_encoding(binary)

    def test_rejects_non_utf8_encoding(self, temp_dir):
        """Test that non-UTF-8 encoded content is rejected."""
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        # Encode as Latin-1 (not valid UTF-8)
        binary = content.encode("latin-1")

        # Note: Most Latin-1 text is also valid UTF-8, so we need invalid UTF-8
        invalid_utf8 = b"\x80\x81\x82"
        with pytest.raises(AssertionError, match="not valid UTF-8"):
            validate_encoding(invalid_utf8)


class TestLineEndingValidation:
    """Tests for validate_line_endings() function."""

    def test_accepts_lf_line_endings(self, temp_dir):
        """Test that Unix LF line endings are accepted."""
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        # Should not raise any exception
        validate_line_endings(content)

    def test_rejects_crlf_line_endings(self, temp_dir):
        """Test that Windows CRLF line endings are rejected."""
        content = "# Title\r\n\r\nFirst sentence. Second sentence. Third sentence.\r\n"

        with pytest.raises(AssertionError, match="CRLF"):
            validate_line_endings(content)

    def test_rejects_no_line_endings(self, temp_dir):
        """Test that content without line endings is rejected."""
        content = "# Title sentence. sentence. sentence."

        with pytest.raises(AssertionError, match="does not contain any line endings"):
            validate_line_endings(content)


class TestTrailingNewlineValidation:
    """Tests for validate_trailing_newline() function."""

    def test_accepts_trailing_newline(self, temp_dir):
        """Test that file ending with newline is accepted."""
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        binary = content.encode("utf-8")
        # Should not raise any exception
        validate_trailing_newline(binary)

    def test_rejects_missing_trailing_newline(self, temp_dir):
        """Test that file without trailing newline is rejected."""
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence."
        binary = content.encode("utf-8")

        with pytest.raises(AssertionError, match="should end with a newline"):
            validate_trailing_newline(binary)


class TestFileSizeValidation:
    """Tests for validate_file_size() function."""

    def test_accepts_size_in_valid_range(self, temp_dir):
        """Test that file size between 400-600 bytes is accepted."""
        # Typical file should be around 450 bytes
        size = 450
        # Should not raise any exception
        validate_file_size(size)

    def test_rejects_size_too_small(self, temp_dir):
        """Test that file size under 400 bytes is rejected."""
        size = 350

        with pytest.raises(AssertionError, match="outside typical range"):
            validate_file_size(size)

    def test_rejects_size_too_large(self, temp_dir):
        """Test that file size over 600 bytes is rejected."""
        size = 650

        with pytest.raises(AssertionError, match="outside typical range"):
            validate_file_size(size)

    def test_rejects_size_exactly_400(self, temp_dir):
        """Test that file size exactly 400 bytes is rejected (boundary)."""
        size = 400

        with pytest.raises(AssertionError, match="outside typical range"):
            validate_file_size(size)

    def test_rejects_size_exactly_600(self, temp_dir):
        """Test that file size exactly 600 bytes is rejected (boundary)."""
        size = 600

        with pytest.raises(AssertionError, match="outside typical range"):
            validate_file_size(size)


class TestH1HeadingValidation:
    """Tests for validate_h1_heading() function."""

    def test_accepts_valid_h1_heading(self, temp_dir):
        """Test that valid H1 heading is accepted."""
        lines = ["# Valid Heading", "", "Prose content here. More prose. Final prose."]
        # Should not raise any exception
        validate_h1_heading(lines)

    def test_rejects_h2_heading(self, temp_dir):
        """Test that H2 heading is rejected."""
        lines = ["## Wrong Level", "", "Prose content here. More prose. Final prose."]

        with pytest.raises(AssertionError, match="Missing H1 heading"):
            validate_h1_heading(lines)

    def test_rejects_plain_text_heading(self, temp_dir):
        """Test that plain text without # is rejected."""
        lines = ["Plain text heading", "", "Prose content here. More prose. Final prose."]

        with pytest.raises(AssertionError, match="Missing H1 heading"):
            validate_h1_heading(lines)

    def test_rejects_empty_heading(self, temp_dir):
        """Test that H1 with no text after # is rejected."""
        lines = ["#", "", "Prose content here. More prose. Final prose."]

        with pytest.raises(AssertionError, match="Missing H1 heading"):
            validate_h1_heading(lines)

    def test_rejects_empty_file(self, temp_dir):
        """Test that empty file is rejected."""
        lines = []

        with pytest.raises(AssertionError, match="File is empty"):
            validate_h1_heading(lines)


class TestBlankLineSeparatorValidation:
    """Tests for validate_blank_line_separator() function."""

    def test_accepts_valid_blank_line(self, temp_dir):
        """Test that proper blank line separator is accepted."""
        lines = ["# Title", "", "Prose content here. More prose. Final prose."]
        # Should not raise any exception
        validate_blank_line_separator(lines)

    def test_rejects_missing_blank_line(self, temp_dir):
        """Test that missing blank line is rejected."""
        lines = ["# Title", "Prose content here. More prose. Final prose."]

        with pytest.raises(AssertionError, match="Missing blank line"):
            validate_blank_line_separator(lines)

    def test_rejects_non_empty_second_line(self, temp_dir):
        """Test that non-empty second line is rejected."""
        lines = ["# Title", "Some text", "Prose content here. More prose. Final prose."]

        with pytest.raises(AssertionError, match="Missing blank line"):
            validate_blank_line_separator(lines)

    def test_rejects_file_with_only_heading(self, temp_dir):
        """Test that file with only heading is rejected."""
        lines = ["# Title"]

        with pytest.raises(AssertionError, match="more than just a heading"):
            validate_blank_line_separator(lines)


class TestProseContentValidation:
    """Tests for validate_prose_content() function."""

    def test_accepts_valid_prose(self, temp_dir):
        """Test that valid prose content is accepted."""
        lines = ["# Title", "", "First sentence. Second sentence. Third sentence."]
        # Should not raise any exception
        validate_prose_content(lines)

    def test_rejects_empty_prose(self, temp_dir):
        """Test that empty prose is rejected."""
        lines = ["# Title", "", "   "]

        with pytest.raises(AssertionError, match="should contain prose content"):
            validate_prose_content(lines)

    def test_rejects_whitespace_only_prose(self, temp_dir):
        """Test that whitespace-only prose is rejected."""
        lines = ["# Title", "", "        "]

        with pytest.raises(AssertionError, match="should contain prose content"):
            validate_prose_content(lines)

    def test_accepts_prose_with_special_characters(self, temp_dir):
        """Test that prose with special characters is accepted."""
        lines = ["# Title", "", "First sentence with (parentheses). Second sentence. Third sentence."]
        # Should not raise any exception
        validate_prose_content(lines)


class TestSentenceCounting:
    """Tests for count_sentences() function."""

    def test_counts_two_sentences(self, temp_dir):
        """Test counting exactly two sentences."""
        prose = "First sentence. Second sentence."
        count = count_sentences(prose)
        assert count == 2

    def test_counts_three_sentences(self, temp_dir):
        """Test counting exactly three sentences."""
        prose = "First sentence. Second sentence. Third sentence."
        count = count_sentences(prose)
        assert count == 3

    def test_counts_one_sentence(self, temp_dir):
        """Test counting exactly one sentence."""
        prose = "Only one sentence."
        count = count_sentences(prose)
        assert count == 1

    def test_ignores_empty_segments(self, temp_dir):
        """Test that empty segments from multiple periods are ignored."""
        prose = "First sentence.. Second sentence."
        count = count_sentences(prose)
        assert count == 2  # Should ignore empty segment from ..

    def test_handles_sentence_with_whitespace(self, temp_dir):
        """Test counting with extra whitespace."""
        prose = "First sentence.  Second sentence.  Third sentence."
        count = count_sentences(prose)
        assert count == 3


class TestSentenceCountValidation:
    """Tests for validate_sentence_count() function."""

    def test_accepts_two_sentences(self, temp_dir):
        """Test that two sentences pass validation."""
        prose = "First sentence. Second sentence."
        # Should not raise any exception
        validate_sentence_count(prose)

    def test_accepts_three_sentences(self, temp_dir):
        """Test that three sentences pass validation."""
        prose = "First sentence. Second sentence. Third sentence."
        # Should not raise any exception
        validate_sentence_count(prose)

    def test_rejects_one_sentence(self, temp_dir):
        """Test that one sentence is rejected."""
        prose = "Only one sentence."

        with pytest.raises(AssertionError, match="2-3 sentences"):
            validate_sentence_count(prose)

    def test_rejects_four_sentences(self, temp_dir):
        """Test that four sentences are rejected."""
        prose = "First. Second. Third. Fourth."

        with pytest.raises(AssertionError, match="2-3 sentences"):
            validate_sentence_count(prose)


class TestInvalidFileCreation:
    """Tests for create_invalid_file() helper function."""

    def test_create_invalid_file_missing_heading(self, temp_dir):
        """Test creating file without H1 heading."""
        filepath = create_invalid_file(temp_dir, "missing_heading")
        assert filepath.exists()

    def test_create_invalid_file_missing_blank_line(self, temp_dir):
        """Test creating file without blank line."""
        filepath = create_invalid_file(temp_dir, "missing_blank_line")
        assert filepath.exists()

    def test_create_invalid_file_empty_prose(self, temp_dir):
        """Test creating file with empty prose."""
        filepath = create_invalid_file(temp_dir, "empty_prose")
        assert filepath.exists()

    def test_create_invalid_file_too_small(self, temp_dir):
        """Test creating file under 400 bytes."""
        filepath = create_invalid_file(temp_dir, "too_small")
        assert filepath.exists()
        assert filepath.stat().st_size < 400

    def test_create_invalid_file_too_large(self, temp_dir):
        """Test creating file over 600 bytes."""
        filepath = create_invalid_file(temp_dir, "too_large")
        assert filepath.exists()
        assert filepath.stat().st_size > 600

    def test_create_invalid_file_with_crlf(self, temp_dir):
        """Test creating file with Windows CRLF."""
        filepath = create_invalid_file(temp_dir, "with_crlf")
        assert filepath.exists()
        binary_content = filepath.read_bytes()
        assert b"\r\n" in binary_content

    def test_create_invalid_file_with_bom(self, temp_dir):
        """Test creating file with UTF-8 BOM."""
        filepath = create_invalid_file(temp_dir, "with_bom")
        assert filepath.exists()
        binary_content = filepath.read_bytes()
        assert binary_content.startswith(b"\xef\xbb\xbf")

    def test_create_invalid_file_no_trailing_newline(self, temp_dir):
        """Test creating file without trailing newline."""
        filepath = create_invalid_file(temp_dir, "no_trailing_newline")
        assert filepath.exists()
        binary_content = filepath.read_bytes()
        assert not binary_content.endswith(b"\n")

    def test_create_invalid_file_one_sentence(self, temp_dir):
        """Test creating file with only one sentence."""
        filepath = create_invalid_file(temp_dir, "one_sentence")
        assert filepath.exists()


class TestValidateFile:
    """Tests for main validate_file() function."""

    def test_rejects_missing_file(self, temp_dir):
        """Test that validate_file() rejects non-existent file."""
        nonexistent_path = Path(temp_dir) / "nonexistent.md"

        with pytest.raises(AssertionError, match="does not exist"):
            validate_file(nonexistent_path)

    def test_rejects_file_with_missing_heading(self, temp_dir):
        """Test that validate_file() rejects file without H1 heading."""
        filepath = create_invalid_file(temp_dir, "missing_heading")

        with pytest.raises(AssertionError):
            validate_file(filepath)

    def test_rejects_file_with_missing_blank_line(self, temp_dir):
        """Test that validate_file() rejects file without blank line."""
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
        """Test that validate_file() rejects file with Windows CRLF."""
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


class TestFileStructureValidation:
    """Tests for validating file structure matches specification."""

    def test_validate_correctly_structured_file(self, temp_dir):
        """Test that a correctly structured file passes validation."""
        filepath = temp_dir / "valid_test.md"
        content = (
            "# Test Title and Important Concepts\n\n"
            "First sentence about the topic being discussed with substantial detail and context regarding fundamental principles. "
            "Second sentence providing more detail and context about the important concepts involved in modern systems and frameworks. "
            "Third sentence concluding the discussion with meaningful insights and perspectives about future developments and innovations.\n"
        )
        filepath.write_text(content, encoding="utf-8")

        result = validate_file(filepath)
        assert result is True

    def test_file_structure_matches_specification(self, temp_dir):
        """Test that file structure matches specification: H1, blank line, prose."""
        filepath = temp_dir / "structured_test.md"
        content = (
            "# Cloud Technology and Modern Architecture Patterns\n\n"
            "Cloud computing has fundamentally revolutionized how organizations deploy applications and manage infrastructure worldwide. "
            "It provides exceptional scalability, flexibility, and cost efficiency for modern enterprises facing increasingly complex technical challenges. "
            "Organizations worldwide are rapidly adopting cloud-native architectures and containerization technologies to improve their competitive position in today's markets.\n"
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
            "# First Heading and Important Topic for Discussion and Exploration\n\n"
            "This is the prose content with a very detailed sentence about important concepts and systems and the frameworks. "
            "Another sentence providing additional context and thoughtful analysis of relevant frameworks and methodologies involved. "
            "Final sentence to complete the thought with meaningful conclusion and future perspectives for development.\n"
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
            "# Example Topic with Comprehensive Details and Exploration for Study\n\n"
            "First sentence about the topic with substantial content and meaningful information for consideration and understanding. "
            "Second sentence providing additional detail and context for the discussion about important frameworks and methodologies. "
            "Third sentence concluding the discussion with important perspectives and insights for future implementation and exploration.\n"
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
            "# Application Development and Software Engineering Practices\n\n"
            "Modern application development practices emphasize continuous integration and deployment strategies. "
            "This comprehensive approach enables development teams to deliver features faster while maintaining high quality standards and reliability. "
            "Many successful organizations have adopted DevOps principles and practices to improve their development workflows and operational efficiency.\n"
        )
        filepath.write_text(content, encoding="utf-8")

        file_size = filepath.stat().st_size
        assert (
            400 < file_size < 600
        ), f"File size {file_size} should be between 400-600 bytes"

        # File should pass validation
        assert validate_file(filepath) is True

    def test_actual_test_qz1gsg_file_validates(self, temp_dir):
        """Test that the actual test-qz1gsg.md file passes validation."""
        # Get the actual file path
        actual_file = Path("/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-4bcbca/test-qz1gsg.md")

        if actual_file.exists():
            result = validate_file(actual_file)
            assert result is True, "Actual test-qz1gsg.md should pass validation"
