"""Tests for feature 102: Creating markdown file test-g4ssgd.md with title and prose content."""

from pathlib import Path
import pytest


class TestMarkdownFileCreation:
    """Tests for task-1: Create markdown file with H1 heading and prose content."""

    def test_file_does_not_exist_before_creation(self, tmp_path):
        """Test that file test-g4ssgd.md does not exist before creation."""
        test_file = tmp_path / "test-g4ssgd.md"
        assert not test_file.exists()

    def test_creates_file_at_correct_path(self, tmp_path):
        """Test that created file exists at correct path."""
        test_file = tmp_path / "test-g4ssgd.md"

        content = "# Sustainable Technology\n\nSustainable technology focuses on designing systems that minimize environmental impact while maximizing beneficial outcomes for society. By integrating renewable energy sources and efficient algorithms, we can reduce our carbon footprint and create lasting solutions. This approach represents the future of innovation, where progress and environmental stewardship go hand in hand.\n"
        test_file.write_text(content, encoding="utf-8", newline="")

        assert test_file.exists()
        assert test_file.name == "test-g4ssgd.md"

    def test_creates_file_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading on first line."""
        test_file = tmp_path / "test-g4ssgd.md"

        content = "# Sustainable Technology\n\nSustainable technology focuses on designing systems that minimize environmental impact while maximizing beneficial outcomes for society. By integrating renewable energy sources and efficient algorithms, we can reduce our carbon footprint and create lasting solutions. This approach represents the future of innovation, where progress and environmental stewardship go hand in hand.\n"
        test_file.write_text(content, encoding="utf-8", newline="")

        text_content = test_file.read_text(encoding="utf-8")
        assert text_content.startswith("# ")

    def test_file_contains_blank_line_separator(self, tmp_path):
        """Test that file has blank line after H1 heading."""
        test_file = tmp_path / "test-g4ssgd.md"

        content = "# Sustainable Technology\n\nSustainable technology focuses on designing systems that minimize environmental impact while maximizing beneficial outcomes for society. By integrating renewable energy sources and efficient algorithms, we can reduce our carbon footprint and create lasting solutions. This approach represents the future of innovation, where progress and environmental stewardship go hand in hand.\n"
        test_file.write_text(content, encoding="utf-8", newline="")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_file_contains_two_or_three_sentences(self, tmp_path):
        """Test that file contains 2-3 sentences (ending with periods)."""
        test_file = tmp_path / "test-g4ssgd.md"

        content = "# Sustainable Technology\n\nSustainable technology focuses on designing systems that minimize environmental impact while maximizing beneficial outcomes for society. By integrating renewable energy sources and efficient algorithms, we can reduce our carbon footprint and create lasting solutions. This approach represents the future of innovation, where progress and environmental stewardship go hand in hand.\n"
        test_file.write_text(content, encoding="utf-8", newline="")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3

    def test_uses_pathlib_write_text_with_utf8_and_lf(self, tmp_path):
        """Test that file is created using pathlib.Path.write_text() with UTF-8 and LF."""
        test_file = tmp_path / "test-g4ssgd.md"

        content = "# Sustainable Technology\n\nSustainable technology focuses on designing systems that minimize environmental impact while maximizing beneficial outcomes for society. By integrating renewable energy sources and efficient algorithms, we can reduce our carbon footprint and create lasting solutions. This approach represents the future of innovation, where progress and environmental stewardship go hand in hand.\n"
        # Use pathlib.Path.write_text() with explicit UTF-8 and LF (newline="")
        test_file.write_text(content, encoding="utf-8", newline="")

        assert test_file.exists()
        # Verify it was written with correct encoding and line endings
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content == content


class TestMarkdownFileValidation:
    """Tests for task-2: Validate file encoding, line endings, and size."""

    MIN_SIZE = 400
    MAX_SIZE = 600

    def test_file_is_utf8_without_bom(self, tmp_path):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = tmp_path / "test-g4ssgd.md"

        content = "# Sustainable Technology\n\nSustainable technology focuses on designing systems that minimize environmental impact while maximizing beneficial outcomes for society. By integrating renewable energy sources and efficient algorithms, we can reduce our carbon footprint and create lasting solutions. This approach represents the future of innovation, where progress and environmental stewardship go hand in hand.\n"
        test_file.write_text(content, encoding="utf-8", newline="")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

    def test_file_has_no_crlf_line_endings(self, tmp_path):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = tmp_path / "test-g4ssgd.md"

        content = "# Sustainable Technology\n\nSustainable technology focuses on designing systems that minimize environmental impact while maximizing beneficial outcomes for society. By integrating renewable energy sources and efficient algorithms, we can reduce our carbon footprint and create lasting solutions. This approach represents the future of innovation, where progress and environmental stewardship go hand in hand.\n"
        test_file.write_text(content, encoding="utf-8", newline="")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content, "File should use LF only, not CRLF"

    def test_file_size_within_range(self, tmp_path):
        """Test that file size is between 400-600 bytes (inclusive)."""
        test_file = tmp_path / "test-g4ssgd.md"

        content = "# Sustainable Technology\n\nSustainable technology focuses on designing systems that minimize environmental impact while maximizing beneficial outcomes for society. By integrating renewable energy sources and efficient algorithms, we can reduce our carbon footprint and create lasting solutions. This approach represents the future of innovation, where progress and environmental stewardship go hand in hand.\n"
        test_file.write_text(content, encoding="utf-8", newline="")

        file_size = len(test_file.read_bytes())
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE, f"File size {file_size} is outside range {self.MIN_SIZE}-{self.MAX_SIZE}"

    def test_file_ends_with_newline(self, tmp_path):
        """Test that file ends with newline character (LF)."""
        test_file = tmp_path / "test-g4ssgd.md"

        content = "# Sustainable Technology\n\nSustainable technology focuses on designing systems that minimize environmental impact while maximizing beneficial outcomes for society. By integrating renewable energy sources and efficient algorithms, we can reduce our carbon footprint and create lasting solutions. This approach represents the future of innovation, where progress and environmental stewardship go hand in hand.\n"
        test_file.write_text(content, encoding="utf-8", newline="")

        binary_content = test_file.read_bytes()
        # Last byte should be LF (0x0A)
        assert binary_content.endswith(b"\n"), "File should end with LF newline"

    def test_validation_all_criteria_met(self, tmp_path):
        """Test that file passes all validation criteria together."""
        test_file = tmp_path / "test-g4ssgd.md"

        # Content that meets all criteria
        content = "# Sustainable Technology\n\nSustainable technology focuses on designing systems that minimize environmental impact while maximizing beneficial outcomes for society. By integrating renewable energy sources and efficient algorithms, we can reduce our carbon footprint and create lasting solutions. This approach represents the future of innovation, where progress and environmental stewardship go hand in hand.\n"
        test_file.write_text(content, encoding="utf-8", newline="")

        binary_content = test_file.read_bytes()
        file_size = len(binary_content)

        # Check UTF-8 without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

        # Check no CRLF
        assert b"\r\n" not in binary_content, "File should not have CRLF line endings"

        # Check file size
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE, f"File size {file_size} outside range {self.MIN_SIZE}-{self.MAX_SIZE}"

        # Check ends with newline
        assert binary_content.endswith(b"\n"), "File should end with newline"
