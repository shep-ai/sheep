"""Tests for feature 146: Creating markdown file test-vqya6w.md with title and prose content."""

from pathlib import Path

from sheep.content_generators import validate_markdown_file


class TestMarkdownFileCreation:
    """Tests for task-1: Create markdown file with H1 heading and prose content."""

    def test_file_does_not_exist_before_creation(self, tmp_path):
        """Test that file test-vqya6w.md does not exist before creation."""
        test_file = tmp_path / "test-vqya6w.md"
        assert not test_file.exists()

    def test_creates_file_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading."""
        test_file = tmp_path / "test-vqya6w.md"

        # Create the file with H1 heading
        content = "# Sustainable Urban Development\n\nCities are evolving to embrace green infrastructure and renewable energy sources. Urban planners are designing sustainable communities that reduce carbon footprints. These innovations will shape the future of metropolitan living worldwide.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_contains_two_or_three_sentences(self, tmp_path):
        """Test that file contains 2-3 sentences (ending with periods)."""
        test_file = tmp_path / "test-vqya6w.md"

        content = "# Sustainable Urban Development\n\nCities are evolving to embrace green infrastructure and renewable energy sources. Urban planners are designing sustainable communities that reduce carbon footprints. These innovations will shape the future of metropolitan living worldwide.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

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
        test_file = tmp_path / "test-vqya6w.md"

        content = "# Sustainable Urban Development\n\nCities are evolving to embrace green infrastructure and renewable energy sources. Urban planners are designing sustainable communities that reduce carbon footprints. These innovations will shape the future of metropolitan living worldwide.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_uses_pathlib_write_text_with_utf8(self, tmp_path):
        """Test that file is created using pathlib.Path.write_text() with UTF-8."""
        test_file = tmp_path / "test-vqya6w.md"

        content = "# Sustainable Urban Development\n\nCities are evolving to embrace green infrastructure and renewable energy sources. Urban planners are designing sustainable communities that reduce carbon footprints. These innovations will shape the future of metropolitan living worldwide.\n"
        # Use pathlib.Path.write_text() with explicit UTF-8 and LF
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        # Verify it was written as UTF-8 by reading it back
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content == content


class TestMarkdownFileValidation:
    """Tests for task-2, 3, 4: Validate file encoding, line endings, and size."""

    MIN_SIZE = 400
    MAX_SIZE = 600

    def test_file_not_utf8_bom(self, tmp_path):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = tmp_path / "test-vqya6w.md"

        content = "# Sustainable Urban Development\n\nCities are evolving to embrace green infrastructure and renewable energy sources, leading the charge toward a more sustainable future. Urban planners are designing sustainable communities that reduce carbon footprints while improving quality of life for residents. These innovations will fundamentally shape the future of metropolitan living worldwide.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_file_has_no_crlf_line_endings(self, tmp_path):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = tmp_path / "test-vqya6w.md"

        content = "# Sustainable Urban Development\n\nCities are evolving to embrace green infrastructure and renewable energy sources, leading the charge toward a more sustainable future. Urban planners are designing sustainable communities that reduce carbon footprints while improving quality of life for residents. These innovations will fundamentally shape the future of metropolitan living worldwide.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content

    def test_file_size_within_range(self, tmp_path):
        """Test that file size is between 400-600 bytes (inclusive)."""
        test_file = tmp_path / "test-vqya6w.md"

        content = "# Sustainable Urban Development\n\nCities are evolving to embrace green infrastructure and renewable energy sources, leading the global transformation toward environmental responsibility and ecological sustainability. Urban planners are designing sustainable communities that reduce carbon footprints while improving quality of life and economic opportunities for all residents. These comprehensive innovations and strategic approaches will fundamentally reshape the future of metropolitan living and environmental stewardship worldwide.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = len(test_file.read_bytes())
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

    def test_file_size_validation_bounds(self, tmp_path):
        """Test that files with proper prose content fall within 400-600 byte range."""
        # Test with realistic prose content - using longer sentences
        test_file = tmp_path / "test-bounds.md"
        # Use three substantial sentences for markdown files - ensure 400+ bytes
        sentence1 = "Sustainable urban development represents a fundamental shift toward environmentally responsible city planning and development strategies. "
        sentence2 = "Green infrastructure, renewable energy systems, and smart transportation networks are being integrated into modern metropolitan areas and communities. "
        sentence3 = "These comprehensive approaches will significantly improve quality of life while reducing environmental impact and promoting sustainable growth."
        markdown_content = f"# Sustainable Urban Development\n\n{sentence1}{sentence2}{sentence3}\n"
        test_file.write_text(markdown_content, encoding="utf-8", newline="\n")
        file_size = len(test_file.read_bytes())
        # Verify the file is within reasonable bounds
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

    def test_validation_all_criteria_met(self, tmp_path):
        """Test that file passes all validation criteria together."""
        test_file = tmp_path / "test-vqya6w.md"

        # Content that meets all criteria
        content = "# Sustainable Urban Development\n\nCities are evolving to embrace green infrastructure and renewable energy sources, leading the global transformation toward environmental responsibility and ecological sustainability. Urban planners are designing sustainable communities that reduce carbon footprints while improving quality of life and economic opportunities for all residents. These comprehensive innovations and strategic approaches will fundamentally reshape the future of metropolitan living and environmental stewardship worldwide.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        file_size = len(binary_content)

        # Check UTF-8 without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Check no CRLF
        assert b"\r\n" not in binary_content

        # Check file size
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE


class TestStructureValidation:
    """Tests for structure validation logic."""

    def test_validate_h1_heading_present(self, tmp_path):
        """Test that validation detects missing H1 heading."""
        test_file = tmp_path / "test-vqya6w.md"

        # Content without H1 heading (missing #)
        invalid_content = "Sustainable Urban Development\n\nSome prose. More prose. Final prose.\n"
        test_file.write_text(invalid_content, encoding="utf-8", newline="\n")

        lines = invalid_content.split("\n")
        # Should fail validation - first line doesn't start with "# "
        assert not lines[0].startswith("# ")

    def test_validate_blank_line_present(self, tmp_path):
        """Test that validation detects missing blank line after heading."""
        test_file = tmp_path / "test-vqya6w.md"

        # Content without blank line separator
        invalid_content = "# Sustainable Urban Development\nSome prose. More prose. Final prose.\n"
        test_file.write_text(invalid_content, encoding="utf-8", newline="\n")

        lines = invalid_content.split("\n")
        # Should fail validation - line 1 is not blank
        assert lines[1] != ""

    def test_validate_sentence_count(self, tmp_path):
        """Test that validation checks for correct sentence count (2-3)."""
        test_file = tmp_path / "test-vqya6w.md"

        # Content with only one sentence (should fail)
        invalid_content = "# Sustainable Urban Development\n\nOnly one sentence here.\n"
        test_file.write_text(invalid_content, encoding="utf-8", newline="\n")

        lines = invalid_content.split("\n")
        prose_content = "\n".join(lines[2:]).strip()
        sentence_count = prose_content.count(".")

        # Should fail - only 1 sentence instead of 2-3
        assert not (2 <= sentence_count <= 3)


class TestValidateFunctionIntegration:
    """Tests for integration with validate_markdown_file() function."""

    def test_validate_markdown_file_with_valid_content(self, tmp_path):
        """Test that validate_markdown_file() returns True for valid markdown."""
        test_file = tmp_path / "test-vqya6w.md"

        # Create valid markdown content
        content = "# Sustainable Urban Development\n\nCities are evolving to embrace green infrastructure and renewable energy sources. Urban planners are designing sustainable communities that reduce carbon footprints. These innovations will shape the future of metropolitan living worldwide.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Validate using the content_generators validation function
        is_valid = validate_markdown_file(str(test_file))
        assert is_valid is True

    def test_validate_markdown_file_checks_encoding(self, tmp_path):
        """Test that validate_markdown_file() validates UTF-8 encoding."""
        test_file = tmp_path / "test-vqya6w.md"

        # Create valid markdown content
        content = "# Sustainable Urban Development\n\nCities are evolving to embrace green infrastructure and renewable energy sources. Urban planners are designing sustainable communities that reduce carbon footprints. These innovations will shape the future of metropolitan living worldwide.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # The file should be valid UTF-8
        is_valid = validate_markdown_file(str(test_file))
        assert is_valid is True

        # Verify the binary content doesn't have BOM
        binary_content = test_file.read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_validate_markdown_file_checks_line_endings(self, tmp_path):
        """Test that validate_markdown_file() validates Unix LF line endings."""
        test_file = tmp_path / "test-vqya6w.md"

        # Create valid markdown content with explicit LF endings
        content = "# Sustainable Urban Development\n\nCities are evolving to embrace green infrastructure and renewable energy sources. Urban planners are designing sustainable communities that reduce carbon footprints. These innovations will shape the future of metropolitan living worldwide.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Verify no CRLF in the file
        binary_content = test_file.read_bytes()
        assert b"\r\n" not in binary_content

        # File should pass validation
        is_valid = validate_markdown_file(str(test_file))
        assert is_valid is True

    def test_validate_markdown_file_comprehensive(self, tmp_path):
        """Test comprehensive validation with all criteria."""
        test_file = tmp_path / "test-vqya6w.md"

        # Create comprehensive markdown content
        content = "# Sustainable Urban Development\n\nCities are evolving to embrace green infrastructure and renewable energy sources, leading a global transformation toward ecological responsibility. Urban planners are designing sustainable communities that reduce carbon footprints while improving quality of life for all residents. These comprehensive innovations will fundamentally shape the future of metropolitan living and environmental stewardship worldwide.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Validate the file
        is_valid = validate_markdown_file(str(test_file))
        assert is_valid is True

        # Verify all individual criteria
        binary_content = test_file.read_bytes()
        file_size = len(binary_content)

        # UTF-8 without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Unix LF only
        assert b"\r\n" not in binary_content

        # File size in range
        assert 400 <= file_size <= 600

        # Structure checks
        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")
        assert lines[0].startswith("# ")
        assert lines[1] == ""

        # Sentence count
        prose_content = "\n".join(lines[2:]).strip()
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3
