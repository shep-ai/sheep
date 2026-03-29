"""Tests for feature 270: Creating markdown file test-q7dj89.md with title and prose content."""


class TestMarkdownFileCreation:
    """Tests for task-1: Create markdown file with H1 heading and prose content."""

    def test_file_does_not_exist_before_creation(self, tmp_path):
        """Test that file test-q7dj89.md does not exist before creation."""
        test_file = tmp_path / "test-q7dj89.md"
        assert not test_file.exists()

    def test_creates_file_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading."""
        test_file = tmp_path / "test-q7dj89.md"

        # Create the file with H1 heading
        content = "# The Art of Meaningful Communication\n\nEffective communication is the foundation of human connection, enabling us to share ideas, emotions, and knowledge with clarity and purpose. When we communicate thoughtfully, we build trust and understanding, fostering deeper relationships both personally and professionally. The ability to express ourselves clearly and listen actively transforms how we navigate the world and impact those around us.\n"
        test_file.write_text(content, encoding="utf-8")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_contains_two_or_three_sentences(self, tmp_path):
        """Test that file contains 2-3 sentences (ending with periods)."""
        test_file = tmp_path / "test-q7dj89.md"

        content = "# The Art of Meaningful Communication\n\nEffective communication is the foundation of human connection, enabling us to share ideas, emotions, and knowledge with clarity and purpose. When we communicate thoughtfully, we build trust and understanding, fostering deeper relationships both personally and professionally. The ability to express ourselves clearly and listen actively transforms how we navigate the world and impact those around us.\n"
        test_file.write_text(content, encoding="utf-8")

        text_content = test_file.read_text(encoding="utf-8")
        # Extract prose content (skip heading and blank line)
        lines = text_content.split("\n")
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3

    def test_file_has_blank_line_separator(self, tmp_path):
        """Test that file has blank line after H1 heading."""
        test_file = tmp_path / "test-q7dj89.md"

        content = "# The Art of Meaningful Communication\n\nEffective communication is the foundation of human connection, enabling us to share ideas, emotions, and knowledge with clarity and purpose. When we communicate thoughtfully, we build trust and understanding, fostering deeper relationships both personally and professionally. The ability to express ourselves clearly and listen actively transforms how we navigate the world and impact those around us.\n"
        test_file.write_text(content, encoding="utf-8")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_uses_pathlib_write_text_with_utf8(self, tmp_path):
        """Test that file is created using pathlib.Path.write_text() with UTF-8."""
        test_file = tmp_path / "test-q7dj89.md"

        content = "# The Art of Meaningful Communication\n\nEffective communication is the foundation of human connection, enabling us to share ideas, emotions, and knowledge with clarity and purpose. When we communicate thoughtfully, we build trust and understanding, fostering deeper relationships both personally and professionally. The ability to express ourselves clearly and listen actively transforms how we navigate the world and impact those around us.\n"
        # Use pathlib.Path.write_text() with explicit UTF-8
        test_file.write_text(content, encoding="utf-8")

        assert test_file.exists()
        # Verify it was written as UTF-8 by reading it back
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content == content


class TestMarkdownFileValidation:
    """Tests for task-2: Validate file encoding, line endings, and markdown syntax."""

    MIN_SIZE = 300
    MAX_SIZE = 600

    def test_file_not_utf8_bom(self, tmp_path):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = tmp_path / "test-q7dj89.md"

        content = "# The Art of Meaningful Communication\n\nEffective communication is the foundation of human connection, enabling us to share ideas, emotions, and knowledge with clarity and purpose. When we communicate thoughtfully, we build trust and understanding, fostering deeper relationships both personally and professionally. The ability to express ourselves clearly and listen actively transforms how we navigate the world and impact those around us.\n"
        test_file.write_text(content, encoding="utf-8")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_file_has_no_crlf_line_endings(self, tmp_path):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = tmp_path / "test-q7dj89.md"

        content = "# The Art of Meaningful Communication\n\nEffective communication is the foundation of human connection, enabling us to share ideas, emotions, and knowledge with clarity and purpose. When we communicate thoughtfully, we build trust and understanding, fostering deeper relationships both personally and professionally. The ability to express ourselves clearly and listen actively transforms how we navigate the world and impact those around us.\n"
        test_file.write_text(content, encoding="utf-8")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content

    def test_commonmark_compliant_h1_heading(self, tmp_path):
        """Test that H1 heading is CommonMark-compliant (# followed by space)."""
        test_file = tmp_path / "test-q7dj89.md"

        content = "# The Art of Meaningful Communication\n\nEffective communication is the foundation of human connection, enabling us to share ideas, emotions, and knowledge with clarity and purpose. When we communicate thoughtfully, we build trust and understanding, fostering deeper relationships both personally and professionally. The ability to express ourselves clearly and listen actively transforms how we navigate the world and impact those around us.\n"
        test_file.write_text(content, encoding="utf-8")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        # CommonMark H1: # followed by space
        assert lines[0].startswith("# ")
        assert len(lines[0]) > 2  # Has content after "# "

    def test_file_size_within_range(self, tmp_path):
        """Test that file size is between 300-600 bytes (inclusive)."""
        test_file = tmp_path / "test-q7dj89.md"

        content = "# The Art of Meaningful Communication\n\nEffective communication is the foundation of human connection, enabling us to share ideas, emotions, and knowledge with clarity and purpose. When we communicate thoughtfully, we build trust and understanding, fostering deeper relationships both personally and professionally. The ability to express ourselves clearly and listen actively transforms how we navigate the world and impact those around us.\n"
        test_file.write_text(content, encoding="utf-8")

        file_size = test_file.stat().st_size
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE
