#!/usr/bin/env python3
"""
Test suite for markdown file creation and validation for feature 300.

Tests cover:
- File creation with proper structure
- H1 heading validation (exactly one)
- Prose structure validation (2-3 sentences, 100-300 characters)
- Encoding and line ending validation (UTF-8 no BOM, LF only)
"""

import re
import tempfile
from pathlib import Path

import pytest


# Prose content: 2-3 sentences about software testing
# This content has 3 sentences and ~280 characters (within 100-300 range)
PROSE_CONTENT = """# Understanding Software Testing

Software testing ensures code behaves correctly under various conditions and edge cases. By validating both expected behavior and unusual scenarios, developers build confidence their systems will perform reliably. This discipline prevents costly failures and enables teams to iterate with confidence."""


def compose_markdown_content(title: str, sentences: str) -> str:
    """
    Compose markdown content with H1 heading and prose.

    Args:
        title: Title for the H1 heading
        sentences: Prose sentences

    Returns:
        Formatted markdown content with proper structure
    """
    return f"# {title}\n\n{sentences}\n"


def create_markdown_file(content: str, filepath: str) -> Path:
    """
    Create markdown file at specified path with UTF-8 encoding and LF line endings.

    Args:
        content: Markdown content to write
        filepath: Path where file should be created

    Returns:
        Path object pointing to created file

    Raises:
        FileExistsError: If file already exists
        ValueError: If content is empty or invalid
    """
    path = Path(filepath)

    # Check if file already exists
    if path.exists():
        raise FileExistsError(f"File {filepath} already exists")

    # Validate content is not empty
    if not content or not content.strip():
        raise ValueError("Content cannot be empty")

    # Write file with explicit UTF-8 encoding (no BOM) and LF line endings
    # Use newline='' to prevent Python from converting \n to \r\n on Windows
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    return path


def validate_h1_heading(content: str) -> bool:
    """
    Validate that content contains exactly one H1 markdown heading.

    Args:
        content: Markdown content to validate

    Returns:
        True if exactly one H1 heading is found

    Raises:
        AssertionError: If H1 count is not exactly 1
    """
    # Pattern: line starting with '# ' (single hash, space, text)
    h1_pattern = r'^# [^#]'
    matches = re.findall(h1_pattern, content, re.MULTILINE)

    h1_count = len(matches)
    assert h1_count == 1, f"Expected exactly 1 H1 heading, found {h1_count}"

    return True


def count_sentences(prose: str) -> int:
    """
    Count sentences in prose using sentence boundary detection.

    Uses regex to split on periods, question marks, and exclamation marks.

    Args:
        prose: Text content to analyze

    Returns:
        Number of sentences found
    """
    # Split on sentence-ending punctuation
    sentence_pattern = r'[.!?]+'
    sentences = re.split(sentence_pattern, prose.strip())

    # Filter out empty strings
    sentences = [s.strip() for s in sentences if s.strip()]

    return len(sentences)


def validate_prose_structure(content: str) -> bool:
    """
    Validate prose content has 2-3 sentences and 100-300 characters.

    Args:
        content: Markdown content to validate

    Returns:
        True if prose structure is valid

    Raises:
        AssertionError: If sentence count or character length is invalid
    """
    # Extract prose (skip H1 heading and blank line)
    lines = content.split('\n')

    # Find H1 heading (first line)
    if lines[0].startswith('# '):
        prose_lines = lines[2:]  # Skip heading and blank line
    else:
        raise AssertionError("No H1 heading found at start of content")

    # Join prose and strip trailing/leading whitespace and empty lines
    prose = '\n'.join(prose_lines).strip()

    # Remove any trailing newline that might be in content
    if prose.endswith('\n'):
        prose = prose[:-1]

    # Validate sentence count: 2-3 sentences
    sentence_count = count_sentences(prose)
    assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    # Validate character count: 100-300 characters (excluding newlines in the text itself)
    # Count only the prose text, not internal formatting
    char_count = len(prose)
    assert 100 <= char_count <= 300, f"Expected 100-300 characters, found {char_count}"

    return True


def validate_encoding_and_line_endings(filepath: str) -> bool:
    """
    Validate UTF-8 encoding without BOM and LF-only line endings.

    Args:
        filepath: Path to file to validate

    Returns:
        True if file passes validation

    Raises:
        AssertionError: If encoding or line endings are invalid
    """
    path = Path(filepath)

    # Read file in binary mode
    binary_content = path.read_bytes()

    # Check for UTF-8 BOM (should not be present)
    assert not binary_content.startswith(b'\xef\xbb\xbf'), "File has UTF-8 BOM (should not be present)"

    # Check for CRLF line endings (should use LF instead)
    assert b'\r' not in binary_content, "File uses CRLF line endings (should use LF)"

    # Verify the file is valid UTF-8
    try:
        binary_content.decode('utf-8')
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}")

    return True


# ============================================================================
# TESTS
# ============================================================================


class TestFileCreation:
    """Tests for markdown file creation task."""

    def test_create_file_in_temp_directory(self):
        """Test that file can be created in a temporary directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            result = create_markdown_file(PROSE_CONTENT, str(filepath))

            assert result.exists()
            assert result.is_file()
            assert result == filepath

    def test_file_has_correct_extension(self):
        """Test that created file has .md extension."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-abc123.md"
            create_markdown_file(PROSE_CONTENT, str(filepath))

            assert filepath.suffix == ".md"

    def test_file_size_in_expected_range(self):
        """Test that file size is in a reasonable range for markdown content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            create_markdown_file(PROSE_CONTENT, str(filepath))

            file_size = filepath.stat().st_size
            # File size should be reasonable for the given content (280-500 bytes)
            assert 250 <= file_size <= 500, f"File size {file_size} is outside expected range"

    def test_create_file_with_explicit_filename(self):
        """Test creating file with specific name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-tq8wxa.md"
            create_markdown_file(PROSE_CONTENT, str(filepath))

            assert filepath.exists()
            assert filepath.name == "test-tq8wxa.md"

    def test_file_exists_error_on_duplicate(self):
        """Test that FileExistsError is raised if file already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            create_markdown_file(PROSE_CONTENT, str(filepath))

            # Try to create the same file again
            with pytest.raises(FileExistsError):
                create_markdown_file(PROSE_CONTENT, str(filepath))

    def test_empty_content_raises_error(self):
        """Test that empty content raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"

            with pytest.raises(ValueError, match="Content cannot be empty"):
                create_markdown_file("", str(filepath))


class TestH1Heading:
    """Tests for H1 heading validation task."""

    def test_h1_heading_count_exactly_one(self):
        """Test that validation detects exactly one H1 heading."""
        content = "# Title\n\nSentence one. Sentence two."
        assert validate_h1_heading(content) is True

    def test_h1_heading_with_prose(self):
        """Test H1 heading validation with full markdown content."""
        assert validate_h1_heading(PROSE_CONTENT) is True

    def test_no_h1_heading_fails(self):
        """Test that validation fails if no H1 heading exists."""
        content = "## Subheading\n\nNo H1 here."
        with pytest.raises(AssertionError, match="Expected exactly 1 H1 heading, found 0"):
            validate_h1_heading(content)

    def test_multiple_h1_headings_fails(self):
        """Test that validation fails if multiple H1 headings exist."""
        content = "# First\n\n# Second\n\nContent here."
        with pytest.raises(AssertionError, match="Expected exactly 1 H1 heading, found 2"):
            validate_h1_heading(content)

    def test_h1_heading_pattern_validation(self):
        """Test that H1 must have space after hash."""
        # This should not match: '#NoSpace'
        content = "#NoSpace\n\nContent."
        with pytest.raises(AssertionError):
            validate_h1_heading(content)


class TestProseStructure:
    """Tests for prose structure validation task."""

    def test_sentence_count_two(self):
        """Test validation with exactly two sentences."""
        content = "# Title\n\nThis is the first sentence about software development. This is the second sentence covering more details."
        assert validate_prose_structure(content) is True

    def test_sentence_count_three(self):
        """Test validation with exactly three sentences."""
        content = "# Title\n\nThis is the first sentence about software development. This is the second sentence covering more details. This is the third sentence with additional information."
        assert validate_prose_structure(content) is True

    def test_full_prose_content_validation(self):
        """Test validation with full prose content."""
        assert validate_prose_structure(PROSE_CONTENT) is True

    def test_sentence_count_too_low(self):
        """Test that validation fails with only one sentence."""
        content = "# Title\n\nOnly one sentence."
        with pytest.raises(AssertionError, match="Expected 2-3 sentences"):
            validate_prose_structure(content)

    def test_sentence_count_too_high(self):
        """Test that validation fails with four sentences."""
        content = "# Title\n\nSent one. Sent two. Sent three. Sent four."
        with pytest.raises(AssertionError, match="Expected 2-3 sentences"):
            validate_prose_structure(content)

    def test_character_count_too_low(self):
        """Test that validation fails if prose is less than 100 characters."""
        content = "# Title\n\nShort. Very short."
        with pytest.raises(AssertionError, match="Expected 100-300 characters"):
            validate_prose_structure(content)

    def test_character_count_too_high(self):
        """Test that validation fails if prose exceeds 300 characters."""
        # Create exactly 2 sentences but with combined length > 300 characters
        long_content = "This is a very long sentence with many detailed words to ensure the total character count exceeds three hundred characters which should trigger validation failure. " + "x" * 200 + ". Second sentence here."
        content = f"# Title\n\n{long_content}"
        with pytest.raises(AssertionError, match="Expected 100-300 characters"):
            validate_prose_structure(content)

    def test_sentence_count_with_multiple_punctuation(self):
        """Test that multiple sentence-ending marks work correctly."""
        content = "# Title\n\nIs this a question about software development? This is an exclamation about programming! This is a regular period-terminated sentence."
        assert validate_prose_structure(content) is True


class TestEncodingAndLineEndings:
    """Tests for encoding and line ending validation task."""

    def test_no_bom_in_file(self):
        """Test that file does not have UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            create_markdown_file(PROSE_CONTENT, str(filepath))

            assert validate_encoding_and_line_endings(str(filepath)) is True

    def test_lf_line_endings_only(self):
        """Test that file uses only LF line endings (no CRLF)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            create_markdown_file(PROSE_CONTENT, str(filepath))

            # Read binary and verify no CRLF
            binary = filepath.read_bytes()
            assert b'\r' not in binary
            assert validate_encoding_and_line_endings(str(filepath)) is True

    def test_valid_utf8_encoding(self):
        """Test that file is valid UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            create_markdown_file(PROSE_CONTENT, str(filepath))

            # Should not raise an exception
            filepath.read_bytes().decode('utf-8')
            assert validate_encoding_and_line_endings(str(filepath)) is True

    def test_file_with_bom_fails(self):
        """Test that validation fails if file has BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"

            # Write with BOM
            content_bytes = PROSE_CONTENT.encode('utf-8-sig')
            filepath.write_bytes(content_bytes)

            with pytest.raises(AssertionError, match="UTF-8 BOM"):
                validate_encoding_and_line_endings(str(filepath))

    def test_file_with_crlf_fails(self):
        """Test that validation fails if file has CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"

            # Write with CRLF
            content_bytes = PROSE_CONTENT.replace('\n', '\r\n').encode('utf-8')
            filepath.write_bytes(content_bytes)

            with pytest.raises(AssertionError, match="CRLF"):
                validate_encoding_and_line_endings(str(filepath))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
