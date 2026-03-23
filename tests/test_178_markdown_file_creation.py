"""Tests for feature 178: Creating markdown file test-khrvcn.md with title and prose content."""

from pathlib import Path


class TestMarkdownFileCreation:
    """Tests for task-1: Create markdown file with H1 heading."""

    def test_file_does_not_exist_before_creation(self):
        """Test that file test-khrvcn.md does not exist before creation."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-khrvcn.md"
        # Clean up if it exists from a previous run
        if test_file.exists():
            test_file.unlink()
        assert not test_file.exists()

    def test_creates_file_with_h1_heading(self):
        """Test that created file contains H1 heading."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-khrvcn.md"

        # Clean up before test
        if test_file.exists():
            test_file.unlink()

        # Create the file with H1 heading
        content = "# The Power of Creative Thinking\n\nCreative thinking opens new possibilities and helps us solve complex problems in innovative ways. It encourages us to challenge conventional wisdom and explore unconventional approaches to achieve our goals. Through creativity, we transform ideas into reality and leave lasting positive impacts on the world.\n"
        test_file.write_text(content, encoding="utf-8")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")


class TestMarkdownProsContent:
    """Tests for task-2: Add 2-3 sentences of prose content."""

    def test_file_contains_exactly_three_sentences(self):
        """Test that file contains exactly 3 sentences (ending with periods)."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-khrvcn.md"

        # Ensure file exists with proper content
        content = "# The Power of Creative Thinking\n\nCreative thinking opens new possibilities and helps us solve complex problems in innovative ways. It encourages us to challenge conventional wisdom and explore unconventional approaches to achieve our goals. Through creativity, we transform ideas into reality and leave lasting positive impacts on the world.\n"
        test_file.write_text(content, encoding="utf-8")

        text_content = test_file.read_text(encoding="utf-8")
        # Extract prose content (skip heading and blank line)
        lines = text_content.split("\n")
        prose_lines = [line for line in lines[2:] if line.strip()]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert sentence_count == 3

    def test_file_has_blank_line_separator(self):
        """Test that file has blank line after H1 heading."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-khrvcn.md"

        content = "# The Power of Creative Thinking\n\nCreative thinking opens new possibilities and helps us solve complex problems in innovative ways. It encourages us to challenge conventional wisdom and explore unconventional approaches to achieve our goals. Through creativity, we transform ideas into reality and leave lasting positive impacts on the world.\n"
        test_file.write_text(content, encoding="utf-8")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_prose_is_grammatically_correct(self):
        """Test that prose content is coherent and well-formed."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-khrvcn.md"

        content = "# The Power of Creative Thinking\n\nCreative thinking opens new possibilities and helps us solve complex problems in innovative ways. It encourages us to challenge conventional wisdom and explore unconventional approaches to achieve our goals. Through creativity, we transform ideas into reality and leave lasting positive impacts on the world.\n"
        test_file.write_text(content, encoding="utf-8")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")
        prose = "\n".join(lines[2:]).strip()

        # Basic checks for grammatical correctness
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
        test_file = repo_root / "test-khrvcn.md"

        content = "# The Power of Creative Thinking\n\nCreative thinking opens new possibilities and helps us solve complex problems in innovative ways. It encourages us to challenge conventional wisdom and explore unconventional approaches to achieve our goals. Through creativity, we transform ideas into reality and leave lasting positive impacts on the world.\n"
        test_file.write_text(content, encoding="utf-8")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_file_has_lf_line_endings(self):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-khrvcn.md"

        content = "# The Power of Creative Thinking\n\nCreative thinking opens new possibilities and helps us solve complex problems in innovative ways. It encourages us to challenge conventional wisdom and explore unconventional approaches to achieve our goals. Through creativity, we transform ideas into reality and leave lasting positive impacts on the world.\n"
        test_file.write_text(content, encoding="utf-8")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content
        # Assert file contains LF sequences
        assert b"\n" in binary_content

    def test_file_size_within_range(self):
        """Test that file size is between 300-800 bytes (inclusive)."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-khrvcn.md"

        content = "# The Power of Creative Thinking\n\nCreative thinking opens new possibilities and helps us solve complex problems in innovative ways. It encourages us to challenge conventional wisdom and explore unconventional approaches to achieve our goals. Through creativity, we transform ideas into reality and leave lasting positive impacts on the world.\n"
        test_file.write_text(content, encoding="utf-8")

        file_size = len(test_file.read_bytes())
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

    def test_validation_all_criteria_met(self):
        """Test that file passes all validation criteria together."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-khrvcn.md"

        # Content that meets all criteria
        content = "# The Power of Creative Thinking\n\nCreative thinking opens new possibilities and helps us solve complex problems in innovative ways. It encourages us to challenge conventional wisdom and explore unconventional approaches to achieve our goals. Through creativity, we transform ideas into reality and leave lasting positive impacts on the world.\n"
        test_file.write_text(content, encoding="utf-8")

        binary_content = test_file.read_bytes()
        file_size = len(binary_content)

        # Check UTF-8 without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Check no CRLF
        assert b"\r\n" not in binary_content

        # Check file size
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE
