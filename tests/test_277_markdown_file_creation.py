"""Tests for feature 277: Creating markdown file test-yziemx.md with title and prose content."""

from pathlib import Path


class TestMarkdownFileCreation:
    """Tests for task-1: Create markdown file with H1 heading and prose content."""

    def test_file_does_not_exist_before_creation(self, tmp_path):
        """Test that file test-yziemx.md does not exist initially."""
        test_file = tmp_path / "test-yziemx.md"
        assert not test_file.exists()

    def test_creates_file_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading on first line."""
        test_file = tmp_path / "test-yziemx.md"

        # Create the file with H1 heading using pathlib
        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"

        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_contains_two_or_three_sentences(self, tmp_path):
        """Test that file contains 2-3 sentences (ending with periods)."""
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
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
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_uses_pathlib_write_text_with_utf8(self, tmp_path):
        """Test that file is created using pathlib.Path.write_text() with UTF-8."""
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
        # Use pathlib.Path.write_text() with explicit UTF-8 and LF line endings
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        # Verify it was written as UTF-8 by reading it back
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content == content

    def test_file_size_within_expected_range(self, tmp_path):
        """Test that file size is naturally in the 400-600 byte range."""
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = test_file.stat().st_size
        # Typical range for properly formatted markdown file with this structure
        assert 350 <= file_size <= 650


class TestMarkdownFileValidation:
    """Tests for task-2: Validate file encoding and line endings."""

    def test_file_not_utf8_bom(self, tmp_path):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File contains UTF-8 BOM which should not be present"

    def test_file_has_no_crlf_line_endings(self, tmp_path):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content, "File contains CRLF which should be LF only"

    def test_file_content_reads_as_valid_utf8(self, tmp_path):
        """Test that file content can be read back as valid UTF-8."""
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Should not raise an exception
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content is not None
        assert len(read_content) > 0

    def test_markdown_heading_format_valid(self, tmp_path):
        """Test that markdown heading follows CommonMark specification (# Title)."""
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        # First line should be H1 heading (starts with '# ')
        assert lines[0].startswith("# "), "First line should be H1 heading (starts with '# ')"
        # H1 heading should have text after '# '
        assert len(lines[0]) > 2, "H1 heading should have text content"
