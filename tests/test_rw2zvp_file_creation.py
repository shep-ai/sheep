"""Tests for test-rw2zvp.md file creation."""

from pathlib import Path

import pytest


class TestRw2zvpFileCreation:
    """Tests for the test-rw2zvp.md markdown file."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        self.repo_root = Path.cwd()
        self.file_path = self.repo_root / "test-rw2zvp.md"

    def test_file_exists_at_repository_root(self):
        """Test that test-rw2zvp.md exists in the repository root."""
        assert self.file_path.exists(), f"File {self.file_path} does not exist"
        assert self.file_path.is_file(), f"Path {self.file_path} is not a file"

    def test_file_contains_level1_heading(self):
        """Test that file contains exactly one level-1 heading (#) as title."""
        content = self.file_path.read_text(encoding="utf-8")

        # Check that first line starts with "# "
        lines = content.split("\n")
        assert len(lines) > 0, "File is empty"
        assert lines[0].startswith("# "), "First line must be a level-1 heading (# )"

        # Check that heading has meaningful content
        heading_text = lines[0].replace("# ", "").strip()
        assert len(heading_text) > 0, "Heading text is empty"

    def test_file_contains_blank_line_after_heading(self):
        """Test that file has blank line separating heading from content."""
        content = self.file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        assert len(lines) > 1, "File must have more than one line"
        assert lines[1] == "", "Second line must be blank (separator after heading)"

    def test_file_contains_prose_content(self):
        """Test that file contains prose content after the heading."""
        content = self.file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Skip heading and blank line
        prose_lines = lines[2:]

        # Remove trailing empty lines
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        assert len(prose_lines) > 0, "No prose content found after heading"

    def test_file_contains_approximately_2_to_3_sentences(self):
        """Test that file contains approximately 2-3 sentences of prose."""
        content = self.file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Get prose content (skip heading and blank line)
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count sentences (periods)
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3, (
            f"Content should have 2-3 sentences, found {sentence_count}"
        )

    def test_file_uses_utf8_encoding(self):
        """Test that file is encoded in UTF-8 with no BOM."""
        binary_content = self.file_path.read_bytes()

        # Check for UTF-8 BOM (should not be present)
        assert not binary_content.startswith(b"\xef\xbb\xbf"), (
            "File should not have UTF-8 BOM"
        )

        # Verify it can be decoded as UTF-8
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not valid UTF-8: {e}")

    def test_file_uses_lf_line_endings_not_crlf(self):
        """Test that file uses LF line endings (\\n), not CRLF (\\r\\n)."""
        binary_content = self.file_path.read_bytes()

        # Check that file does not contain CRLF
        assert b"\r\n" not in binary_content, (
            "File should not have CRLF line endings"
        )

        # Check that file contains LF
        assert b"\n" in binary_content, (
            "File should have LF line endings"
        )

    def test_file_has_trailing_newline(self):
        """Test that file ends with a trailing newline."""
        content = self.file_path.read_text(encoding="utf-8")
        assert content.endswith("\n"), "File must end with a trailing newline"

    def test_file_size_is_in_expected_range(self):
        """Test that file size is approximately 400-600 bytes."""
        file_size = self.file_path.stat().st_size

        # Allow 10% margin for flexibility
        min_size = 400 * 0.9  # 360
        max_size = 600 * 1.1  # 660

        assert min_size <= file_size <= max_size, (
            f"File size {file_size} bytes is outside expected range 360-660"
        )

    def test_file_contains_valid_markdown_syntax(self):
        """Test that file contains valid markdown syntax."""
        content = self.file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Verify structure
        assert lines[0].startswith("# "), "Must have H1 heading"
        assert lines[1] == "", "Must have blank line separator"

        prose_lines = lines[2:]
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        prose_content = "\n".join(prose_lines).strip()

        # Check that prose is not empty and contains periods
        assert len(prose_content) > 0, "Prose content is empty"
        assert "." in prose_content, "Prose should contain sentence periods"

    def test_file_content_is_coherent_and_readable(self):
        """Test that file content is coherent and substantive."""
        content = self.file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Extract all content
        heading = lines[0]
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Verify heading is meaningful
        heading_text = heading.replace("# ", "").strip()
        assert len(heading_text) >= 2, "Heading text is too short"

        # Verify prose is meaningful
        prose_words = prose_content.split()
        assert len(prose_words) >= 10, "Prose content is too short to be substantive"

        # Verify no obvious placeholder content
        placeholder_keywords = ["placeholder", "TODO", "FIXME"]
        prose_lower = prose_content.lower()
        for keyword in placeholder_keywords:
            assert keyword not in prose_lower, f"Content contains placeholder: {keyword}"
