"""
Test suite for markdown file creation - feature 224, phase 1.

Tests the creation and validation of test-pz9pb9.md with proper structure,
encoding, and line endings.
"""

import os
import tempfile
from pathlib import Path

import pytest

# ============================================================================
# Helper Functions
# ============================================================================

def create_markdown_file():
    """
    Create test-pz9pb9.md at repository root with proper structure.

    Returns:
        Path: Path to the created markdown file
    """
    heading = "# The Power of Continuous Learning"
    prose = (
        "Continuous learning is essential for personal and professional growth "
        "in an ever-changing world where knowledge and skills rapidly evolve. "
        "By embracing a mindset of curiosity and lifelong development, individuals "
        "can adapt to new challenges and unlock greater opportunities for success. "
        "Investing time in learning new technologies, methodologies, and perspectives "
        "ensures we remain relevant and effective in our endeavors."
    )

    # Construct content with explicit \n (LF line endings)
    content = f"{heading}\n\n{prose}\n"

    # Write file with UTF-8 encoding (no BOM)
    filepath = Path("test-pz9pb9.md")
    filepath.write_text(content, encoding="utf-8")

    return filepath


def validate_markdown_file(filepath):
    """
    Validate that markdown file meets all requirements.

    Args:
        filepath (Path): Path to the markdown file to validate

    Returns:
        bool: True if file is valid

    Raises:
        AssertionError: If validation fails
    """
    # File must exist
    assert filepath.exists(), f"File {filepath} does not exist"

    # Read binary content to check encoding and line endings
    binary_content = filepath.read_bytes()

    # Check UTF-8 without BOM
    assert not binary_content.startswith(b'\xef\xbb\xbf'), \
        "File should not have UTF-8 BOM"

    # Check for CRLF (should not be present)
    assert b'\r\n' not in binary_content, \
        "File should use LF line endings, not CRLF"

    # Check for LF line endings
    assert b'\n' in binary_content, \
        "File should have LF line endings"

    # Decode as UTF-8 text
    text_content = filepath.read_text(encoding='utf-8')

    # Check for H1 heading on first line
    lines = text_content.split('\n')
    assert lines[0].startswith('# '), \
        "File must start with H1 heading (# )"

    # Check for blank line after heading
    assert len(lines) > 1 and lines[1] == '', \
        "File must have blank line after heading"

    # Check for prose content (lines 2+)
    prose = '\n'.join(lines[2:]).strip()
    assert prose, "File must contain prose content"

    # Count sentences (periods)
    period_count = prose.count('.')
    assert period_count >= 2, \
        f"Prose should contain at least 2 sentences, found {period_count}"

    # Check file size (should be in 400-600 byte range, tolerance 300-800)
    file_size = filepath.stat().st_size
    assert 300 < file_size < 800, \
        f"File size {file_size} bytes outside typical range (300-800 bytes)"

    # Check trailing newline
    assert binary_content.endswith(b'\n'), \
        "File should end with newline"

    return True


# ============================================================================
# Test Class
# ============================================================================

class TestMarkdownFileCreation:
    """Tests for markdown file creation - feature 224."""

    def test_file_does_not_exist_initially(self):
        """Test that test-pz9pb9.md does not exist before creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                assert not Path("test-pz9pb9.md").exists(), \
                    "File should not exist before creation"
            finally:
                os.chdir(original_cwd)

    def test_creates_file_at_repository_root(self):
        """Test that create_markdown_file() creates file in working directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                filepath = create_markdown_file()

                assert filepath.exists(), "File should exist after creation"
                assert filepath.name == "test-pz9pb9.md", \
                    "File should be named test-pz9pb9.md"
            finally:
                os.chdir(original_cwd)

    def test_file_contains_h1_heading(self):
        """Test that file contains H1 markdown heading on first line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                content = Path("test-pz9pb9.md").read_text(encoding='utf-8')
                assert content.startswith("# "), \
                    "File should start with H1 heading"
            finally:
                os.chdir(original_cwd)

    def test_file_contains_blank_line_after_heading(self):
        """Test that file has blank line separating heading from prose."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                content = Path("test-pz9pb9.md").read_text(encoding='utf-8')
                assert '\n\n' in content, \
                    "File should contain blank line after heading"
            finally:
                os.chdir(original_cwd)

    def test_file_contains_prose_content(self):
        """Test that file contains 2-3 sentences of prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                content = Path("test-pz9pb9.md").read_text(encoding='utf-8')
                # Count periods to estimate sentence count
                period_count = content.count('.')
                assert period_count >= 2, \
                    f"File should contain at least 2 sentences, found {period_count}"
            finally:
                os.chdir(original_cwd)

    def test_file_uses_utf8_encoding(self):
        """Test that file is UTF-8 encoded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                # Read as binary
                binary_content = Path("test-pz9pb9.md").read_bytes()

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
                create_markdown_file()

                binary_content = Path("test-pz9pb9.md").read_bytes()
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
                create_markdown_file()

                binary_content = Path("test-pz9pb9.md").read_bytes()
                # Should not contain CRLF (\r\n)
                assert b'\r\n' not in binary_content, \
                    "File should not have CRLF line endings"
                # Should contain LF (\n)
                assert b'\n' in binary_content, \
                    "File should have LF line endings"
            finally:
                os.chdir(original_cwd)

    def test_file_size_in_typical_range(self):
        """Test that file size is approximately 400-600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                file_size = Path("test-pz9pb9.md").stat().st_size
                # Tolerance range: 300-800 bytes
                assert 300 < file_size < 800, \
                    f"File size {file_size} bytes outside typical range (300-800)"
            finally:
                os.chdir(original_cwd)

    def test_file_ends_with_newline(self):
        """Test that file ends with a newline character."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                binary_content = Path("test-pz9pb9.md").read_bytes()
                # File must end with LF (\n)
                assert binary_content.endswith(b'\n'), \
                    "File should end with a newline character"
            finally:
                os.chdir(original_cwd)

    def test_validation_passes_for_created_file(self):
        """Test that validate_markdown_file() passes for created file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                filepath = create_markdown_file()

                result = validate_markdown_file(filepath)
                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_heading_and_prose_coherent(self):
        """Test that heading and prose address the same topic."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()

                content = Path("test-pz9pb9.md").read_text(encoding='utf-8')
                # Split heading and prose
                parts = content.split('\n\n', 1)
                heading = parts[0].strip()
                prose = parts[1].strip() if len(parts) > 1 else ""

                # Both should exist
                assert heading, "Heading should not be empty"
                assert prose, "Prose should not be empty"

                # Heading should have meaningful content
                assert len(heading) > 2, "Heading should have meaningful content"
            finally:
                os.chdir(original_cwd)

    def test_returns_path_object(self):
        """Test that create_markdown_file() returns a Path object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                result = create_markdown_file()

                assert isinstance(result, Path)
                assert result.name == "test-pz9pb9.md"
            finally:
                os.chdir(original_cwd)

    def test_markdown_structure_matches_specification(self):
        """Test that created file matches specification: # Heading\\n\\n<prose>\\n"""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                filepath = create_markdown_file()
                content = filepath.read_text(encoding='utf-8')

                # Specification: # Heading\n\n<2-3 sentences>
                lines = content.split('\n')

                # First line should be heading
                assert lines[0].startswith('# '), \
                    "First line should be H1 heading"

                # Second line should be empty (blank line)
                assert lines[1] == '', \
                    "Second line should be empty (blank line separator)"

                # Remaining lines should contain prose
                prose_lines = lines[2:]
                prose = '\n'.join(prose_lines).strip()
                assert len(prose) > 0, \
                    "Prose content should be present"
            finally:
                os.chdir(original_cwd)
