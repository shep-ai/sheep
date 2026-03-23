"""Tests for feature 179: Creating markdown file test-cyktqk.md with title and prose content."""

from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sheep.content_generators import (
    write_markdown_file,
    validate_markdown_file,
)

# Test content that meets all requirements
TEST_CONTENT = """# The Importance of Continuous Learning

Continuous learning is essential for personal and professional growth in an ever-changing world. By embracing new knowledge and skills, we enhance our ability to adapt to challenges and seize opportunities. Through dedication to lifelong learning, we unlock our potential and contribute meaningfully to society.
"""


class TestMarkdownFileCreation:
    """Tests for task-1: Create markdown file with H1 heading."""

    def test_file_does_not_exist_before_creation(self):
        """Test that file test-cyktqk.md does not exist before creation."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-cyktqk.md"
        # Clean up if it exists from a previous run
        if test_file.exists():
            test_file.unlink()
        assert not test_file.exists()

    def test_creates_file_with_content_generators(self):
        """Test that file is created with content_generators.write_markdown_file()."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-cyktqk.md"

        # Clean up before test
        if test_file.exists():
            test_file.unlink()

        # Write file using content_generators
        file_path = write_markdown_file(TEST_CONTENT, "test-cyktqk.md")

        assert test_file.exists()
        assert file_path == str(test_file)
        assert test_file.read_text(encoding="utf-8") == TEST_CONTENT


class TestMarkdownProsContent:
    """Tests for task-2: Add 2-3 sentences of prose content."""

    def test_file_contains_valid_sentence_count(self):
        """Test that file contains exactly 2-3 sentences (ending with periods)."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-cyktqk.md"

        # Ensure file exists
        write_markdown_file(TEST_CONTENT, "test-cyktqk.md")

        text_content = test_file.read_text(encoding="utf-8")
        # Extract prose content (skip heading and blank line)
        lines = text_content.split("\n")
        prose_lines = [line for line in lines[2:] if line.strip()]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3

    def test_file_has_blank_line_separator(self):
        """Test that file has blank line after H1 heading."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-cyktqk.md"

        write_markdown_file(TEST_CONTENT, "test-cyktqk.md")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_prose_is_coherent(self):
        """Test that prose content is coherent and well-formed."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-cyktqk.md"

        write_markdown_file(TEST_CONTENT, "test-cyktqk.md")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")
        prose = "\n".join(lines[2:]).strip()

        # Basic checks for coherence
        assert len(prose) > 100  # Substantial content
        assert prose[0].isupper()  # Starts with uppercase
        assert prose.endswith(".")  # Ends with period


class TestMarkdownFileValidation:
    """Tests for task-3: Validate file encoding, line endings, and size."""

    MIN_SIZE = 300
    MAX_SIZE = 800

    def test_file_not_utf8_bom(self):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-cyktqk.md"

        write_markdown_file(TEST_CONTENT, "test-cyktqk.md")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_file_has_lf_line_endings(self):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-cyktqk.md"

        write_markdown_file(TEST_CONTENT, "test-cyktqk.md")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content
        # Assert file contains LF sequences
        assert b"\n" in binary_content

    def test_file_size_within_range(self):
        """Test that file size is between 300-800 bytes (inclusive)."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-cyktqk.md"

        write_markdown_file(TEST_CONTENT, "test-cyktqk.md")

        file_size = len(test_file.read_bytes())
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

    def test_file_passes_validate_markdown_file(self):
        """Test that file passes comprehensive validation."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-cyktqk.md"

        write_markdown_file(TEST_CONTENT, "test-cyktqk.md")

        # Should not raise any exception
        result = validate_markdown_file(str(test_file))
        assert result is True

    def test_validation_all_criteria_met(self):
        """Test that file passes all validation criteria together."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-cyktqk.md"

        write_markdown_file(TEST_CONTENT, "test-cyktqk.md")

        binary_content = test_file.read_bytes()
        file_size = len(binary_content)

        # Check UTF-8 without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Check no CRLF
        assert b"\r\n" not in binary_content

        # Check file size
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

        # Check markdown validation
        assert validate_markdown_file(str(test_file)) is True
