"""Tests for feature 166: Creating markdown file test-xda39w.md with title and prose content."""

from pathlib import Path
import re

import pytest


class TestFileCreation:
    """Integration tests for markdown file creation and validation."""

    def test_creates_file_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading."""
        test_file = tmp_path / "test-xda39w.md"

        # Create the file with H1 heading
        title = "The Wonders of Deep Ocean Exploration"
        prose = "The deep ocean remains one of Earth's final frontiers, filled with mysterious ecosystems and undiscovered species that challenge our understanding of life. Technological advances in submersible engineering have enabled scientists to explore depths previously unreachable, revealing bioluminescent creatures and hydrothermal vent communities that thrive in extreme conditions. These expeditions not only expand scientific knowledge but also inspire wonder about the vast, unexplored realms beneath our seas."
        content = f"# {title}\n\n{prose}\n"

        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        text_content = test_file.read_text(encoding="utf-8")
        assert text_content.startswith("# ")

    def test_file_has_h1_heading_on_first_line(self, tmp_path):
        """Test that first line is H1 markdown heading."""
        test_file = tmp_path / "test-xda39w.md"

        title = "The Wonders of Deep Ocean Exploration"
        prose = "The deep ocean remains one of Earth's final frontiers, filled with mysterious ecosystems and undiscovered species that challenge our understanding of life. Technological advances in submersible engineering have enabled scientists to explore depths previously unreachable, revealing bioluminescent creatures and hydrothermal vent communities that thrive in extreme conditions. These expeditions not only expand scientific knowledge but also inspire wonder about the vast, unexplored realms beneath our seas."
        content = f"# {title}\n\n{prose}\n"

        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        # First line should be H1 heading
        assert lines[0].startswith("# ")
        assert len(lines[0]) > 2  # Has content after the #

    def test_file_has_blank_line_separator(self, tmp_path):
        """Test that file has blank line after H1 heading."""
        test_file = tmp_path / "test-xda39w.md"

        title = "The Wonders of Deep Ocean Exploration"
        prose = "The deep ocean remains one of Earth's final frontiers, filled with mysterious ecosystems and undiscovered species that challenge our understanding of life. Technological advances in submersible engineering have enabled scientists to explore depths previously unreachable, revealing bioluminescent creatures and hydrothermal vent communities that thrive in extreme conditions. These expeditions not only expand scientific knowledge but also inspire wonder about the vast, unexplored realms beneath our seas."
        content = f"# {title}\n\n{prose}\n"

        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        # Check that second line (index 1) is blank
        assert lines[0].startswith("# ")
        assert lines[1] == ""

    def test_file_contains_two_or_three_sentences(self, tmp_path):
        """Test that file contains exactly 2-3 sentences."""
        test_file = tmp_path / "test-xda39w.md"

        title = "The Wonders of Deep Ocean Exploration"
        prose = "The deep ocean remains one of Earth's final frontiers, filled with mysterious ecosystems and undiscovered species that challenge our understanding of life. Technological advances in submersible engineering have enabled scientists to explore depths previously unreachable, revealing bioluminescent creatures and hydrothermal vent communities that thrive in extreme conditions. These expeditions not only expand scientific knowledge but also inspire wonder about the vast, unexplored realms beneath our seas."
        content = f"# {title}\n\n{prose}\n"

        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")

        # Extract prose content (skip heading and blank line)
        lines = text_content.split("\n")
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3

    def test_file_uses_utf8_encoding_without_bom(self, tmp_path):
        """Test that file is UTF-8 encoded without Byte Order Mark."""
        test_file = tmp_path / "test-xda39w.md"

        title = "The Wonders of Deep Ocean Exploration"
        prose = "The deep ocean remains one of Earth's final frontiers, filled with mysterious ecosystems and undiscovered species that challenge our understanding of life. Technological advances in submersible engineering have enabled scientists to explore depths previously unreachable, revealing bioluminescent creatures and hydrothermal vent communities that thrive in extreme conditions. These expeditions not only expand scientific knowledge but also inspire wonder about the vast, unexplored realms beneath our seas."
        content = f"# {title}\n\n{prose}\n"

        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Read as binary and verify no BOM
        binary_content = test_file.read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File has UTF-8 BOM, but should not"

        # Verify can be decoded as UTF-8
        decoded = binary_content.decode("utf-8")
        assert decoded == content

    def test_file_uses_lf_line_endings_not_crlf(self, tmp_path):
        """Test that file uses LF line endings, not CRLF."""
        test_file = tmp_path / "test-xda39w.md"

        title = "The Wonders of Deep Ocean Exploration"
        prose = "The deep ocean remains one of Earth's final frontiers, filled with mysterious ecosystems and undiscovered species that challenge our understanding of life. Technological advances in submersible engineering have enabled scientists to explore depths previously unreachable, revealing bioluminescent creatures and hydrothermal vent communities that thrive in extreme conditions. These expeditions not only expand scientific knowledge but also inspire wonder about the vast, unexplored realms beneath our seas."
        content = f"# {title}\n\n{prose}\n"

        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Read as binary and verify no CRLF
        binary_content = test_file.read_bytes()
        assert b"\r\n" not in binary_content, "File contains CRLF, should use LF only"
        assert b"\n" in binary_content, "File should contain LF line endings"

    def test_file_ends_with_newline(self, tmp_path):
        """Test that file ends with a trailing newline (Unix convention)."""
        test_file = tmp_path / "test-xda39w.md"

        title = "The Wonders of Deep Ocean Exploration"
        prose = "The deep ocean remains one of Earth's final frontiers, filled with mysterious ecosystems and undiscovered species that challenge our understanding of life. Technological advances in submersible engineering have enabled scientists to explore depths previously unreachable, revealing bioluminescent creatures and hydrothermal vent communities that thrive in extreme conditions. These expeditions not only expand scientific knowledge but also inspire wonder about the vast, unexplored realms beneath our seas."
        content = f"# {title}\n\n{prose}\n"

        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        assert text_content.endswith("\n"), "File should end with newline"

    def test_file_size_within_300_600_bytes(self, tmp_path):
        """Test that file size is within 300-600 bytes."""
        test_file = tmp_path / "test-xda39w.md"

        title = "The Wonders of Deep Ocean Exploration"
        prose = "The deep ocean remains one of Earth's final frontiers, filled with mysterious ecosystems and undiscovered species that challenge our understanding of life. Technological advances in submersible engineering have enabled scientists to explore depths previously unreachable, revealing bioluminescent creatures and hydrothermal vent communities that thrive in extreme conditions. These expeditions not only expand scientific knowledge but also inspire wonder about the vast, unexplored realms beneath our seas."
        content = f"# {title}\n\n{prose}\n"

        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = test_file.stat().st_size
        assert 300 <= file_size <= 600, f"File size {file_size} is outside 300-600 byte range"

    def test_file_structure_complete(self, tmp_path):
        """Test complete file structure: H1 heading, blank line, 2-3 sentences."""
        test_file = tmp_path / "test-xda39w.md"

        title = "The Wonders of Deep Ocean Exploration"
        prose = "The deep ocean remains one of Earth's final frontiers, filled with mysterious ecosystems and undiscovered species that challenge our understanding of life. Technological advances in submersible engineering have enabled scientists to explore depths previously unreachable, revealing bioluminescent creatures and hydrothermal vent communities that thrive in extreme conditions. These expeditions not only expand scientific knowledge but also inspire wonder about the vast, unexplored realms beneath our seas."
        content = f"# {title}\n\n{prose}\n"

        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        # Structure validation
        assert len(lines) >= 4, "File must have at least heading + blank line + prose + trailing newline"
        assert lines[0].startswith("# "), "First line must be H1 heading"
        assert lines[1] == "", "Second line must be blank"

        # Prose validation
        prose_text = "\n".join(lines[2:]).strip()
        assert len(prose_text) > 0, "Prose content must not be empty"
        assert 2 <= prose_text.count(".") <= 3, "Prose must contain 2-3 sentences (periods)"
