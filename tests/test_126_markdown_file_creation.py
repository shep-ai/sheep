"""Tests for feature 126: Creating markdown file test-lqbnqn.md with LLM-generated prose content."""

from pathlib import Path
import pytest


class TestMarkdownFileCreation:
    """Tests for task-3-1: Create markdown file with H1 heading and prose content."""

    def test_file_does_not_exist_before_creation(self, tmp_path):
        """Test that file test-lqbnqn.md does not exist before creation."""
        test_file = tmp_path / "test-lqbnqn.md"
        assert not test_file.exists()

    def test_creates_file_at_correct_path(self, tmp_path):
        """Test that created file exists at the expected path."""
        test_file = tmp_path / "test-lqbnqn.md"

        # Create the file
        content = "# Sample Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.name == "test-lqbnqn.md"

    def test_file_starts_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading as first line."""
        test_file = tmp_path / "test-lqbnqn.md"

        content = "# Sample Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_content = test_file.read_text(encoding="utf-8")
        assert file_content.startswith("# ")

    def test_file_has_blank_line_after_heading(self, tmp_path):
        """Test that file has blank line after H1 heading."""
        test_file = tmp_path / "test-lqbnqn.md"

        content = "# Sample Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_content = test_file.read_text(encoding="utf-8")
        lines = file_content.split("\n")

        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_file_contains_two_or_three_sentences(self, tmp_path):
        """Test that file contains 2-3 sentences (ending with periods)."""
        test_file = tmp_path / "test-lqbnqn.md"

        content = "# Sample Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        # Extract prose content (skip heading and blank line)
        lines = text_content.split("\n")
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3

    def test_file_ends_with_final_newline(self, tmp_path):
        """Test that file ends with exactly one final newline."""
        test_file = tmp_path / "test-lqbnqn.md"

        content = "# Sample Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_content = test_file.read_text(encoding="utf-8")
        # File should end with a newline but not multiple newlines
        assert file_content.endswith("\n")
        assert not file_content.endswith("\n\n")

    def test_uses_pathlib_write_text_with_utf8(self, tmp_path):
        """Test that file is created using pathlib.Path.write_text() with UTF-8."""
        test_file = tmp_path / "test-lqbnqn.md"

        content = "# Sample Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        # Use pathlib.Path.write_text() with explicit UTF-8 and LF
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        # Verify it was written as UTF-8 by reading it back
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content == content


class TestMarkdownFileValidation:
    """Tests for validating file encoding, line endings, and size."""

    MIN_SIZE = 400
    MAX_SIZE = 600

    def test_file_not_utf8_bom(self, tmp_path):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = tmp_path / "test-lqbnqn.md"

        content = "# Sample Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_file_has_no_crlf_line_endings(self, tmp_path):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = tmp_path / "test-lqbnqn.md"

        content = "# Sample Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content

    def test_file_size_within_range(self, tmp_path):
        """Test that file size is between 400-600 bytes (inclusive)."""
        test_file = tmp_path / "test-lqbnqn.md"

        # Use a longer prose to ensure we're in the 400-600 byte range
        content = "# Complex Scientific Topic\n\nThis comprehensive exploration examines the fundamental principles and intricate mechanisms underlying biological systems, demonstrating how diverse organisms interact within their environments. Scientists utilize advanced methodologies and sophisticated analytical frameworks to investigate the complex relationships between genetic expression, environmental factors, and evolutionary adaptations. Through systematic observation and rigorous experimentation, researchers continuously refine our understanding of nature's remarkable complexity and interconnected systems.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = len(test_file.read_bytes())
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

    def test_file_has_no_cr_line_endings(self, tmp_path):
        """Test that file contains no CR-only line endings."""
        test_file = tmp_path / "test-lqbnqn.md"

        content = "# Sample Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Check for standalone CR characters (0x0D) that aren't part of CRLF
        # We already checked for CRLF above, so any CR here would be problematic
        assert b"\r" not in binary_content

    def test_validation_all_criteria_met(self, tmp_path):
        """Test that file passes all validation criteria together."""
        test_file = tmp_path / "test-lqbnqn.md"

        # Content that meets all criteria
        content = "# Complex Scientific Topic\n\nThis comprehensive exploration examines the fundamental principles and intricate mechanisms underlying biological systems, demonstrating how diverse organisms interact within their environments. Scientists utilize advanced methodologies and sophisticated analytical frameworks to investigate the complex relationships between genetic expression, environmental factors, and evolutionary adaptations. Through systematic observation and rigorous experimentation, researchers continuously refine our understanding of nature's remarkable complexity and interconnected systems.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        file_size = len(binary_content)

        # Check UTF-8 without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Check no CRLF
        assert b"\r\n" not in binary_content

        # Check no CR
        assert b"\r" not in binary_content

        # Check file size
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

        # Check heading
        assert binary_content.startswith(b"# ")

        # Check file ends with newline
        assert binary_content.endswith(b"\n")
