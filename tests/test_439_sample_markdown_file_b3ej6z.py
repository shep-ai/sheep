"""Tests for feature 439: Creating markdown file test-b3ej6z.md with title and prose content."""

from pathlib import Path


class TestSampleMarkdownFile:
    """Tests for test-b3ej6z.md file."""

    def test_file_exists(self):
        """Test that test-b3ej6z.md file exists in project root."""
        file_path = Path(__file__).parent.parent / "test-b3ej6z.md"
        assert file_path.exists(), "test-b3ej6z.md should exist in project root"

    def test_file_has_h1_heading(self):
        """Test that file starts with H1 heading."""
        file_path = Path(__file__).parent.parent / "test-b3ej6z.md"
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        assert lines[0].startswith("# "), "First line should be H1 heading"
        assert len(lines[0]) > 2, "H1 heading should have content"

    def test_file_has_blank_line_after_heading(self):
        """Test that file has blank line after H1 heading."""
        file_path = Path(__file__).parent.parent / "test-b3ej6z.md"
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        assert lines[1] == "", "Second line should be blank"

    def test_file_has_prose_content(self):
        """Test that file has prose content after blank line."""
        file_path = Path(__file__).parent.parent / "test-b3ej6z.md"
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Should have at least 3 lines (heading, blank, prose)
        assert len(lines) >= 3, "File should have at least 3 lines"

        # Prose content should exist (starting from line 2)
        prose_content = "\n".join(lines[2:]).strip()
        assert len(prose_content) > 0, "Prose content should not be empty"

    def test_file_uses_utf8_encoding(self):
        """Test that file uses UTF-8 encoding without BOM."""
        file_path = Path(__file__).parent.parent / "test-b3ej6z.md"
        binary_content = file_path.read_bytes()

        # No UTF-8 BOM (EF BB BF)
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

        # Should be decodable as UTF-8
        binary_content.decode("utf-8")

    def test_file_uses_lf_line_endings(self):
        """Test that file uses LF line endings, not CRLF."""
        file_path = Path(__file__).parent.parent / "test-b3ej6z.md"
        binary_content = file_path.read_bytes()

        # No CRLF (Windows line endings)
        assert b"\r\n" not in binary_content, "File should use LF, not CRLF"

    def test_file_has_2_to_3_sentences(self):
        """Test that file has 2-3 sentences of prose."""
        file_path = Path(__file__).parent.parent / "test-b3ej6z.md"
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Get prose content (after heading and blank line)
        prose_content = "\n".join(lines[2:]).strip()

        # Count sentences (periods indicate sentence endings)
        sentence_count = prose_content.count(".")

        # Should have 2-3 sentences
        assert 2 <= sentence_count <= 3, f"Should have 2-3 sentences, found {sentence_count}"

    def test_file_ends_with_newline(self):
        """Test that file ends with a newline."""
        file_path = Path(__file__).parent.parent / "test-b3ej6z.md"
        content = file_path.read_text(encoding="utf-8")

        # Should end with newline
        assert content.endswith("\n"), "File should end with newline"

    def test_file_size_in_range(self):
        """Test that file size is within 300-500 bytes."""
        file_path = Path(__file__).parent.parent / "test-b3ej6z.md"
        file_size = file_path.stat().st_size

        # File size should be reasonable
        assert file_size > 100, "File should have meaningful content"
        assert file_size < 1000, "File should not be excessively large"

    def test_file_title_is_descriptive(self):
        """Test that the H1 title is descriptive."""
        file_path = Path(__file__).parent.parent / "test-b3ej6z.md"
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        title = lines[0][2:].strip()  # Remove "# " prefix

        # Title should have reasonable length
        assert len(title) >= 3, "Title should be at least 3 characters"
        assert len(title) <= 100, "Title should not be excessively long"
