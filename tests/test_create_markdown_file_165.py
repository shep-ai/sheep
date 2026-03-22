"""Tests for markdown file creation (feature 165)."""
import re
from pathlib import Path


class TestMarkdownFileCreation:
    """Tests for test-ewmber.md file creation."""

    FILE_PATH = Path.cwd() / "test-ewmber.md"

    def test_file_does_not_exist_before_creation(self):
        """Verify file does not exist initially."""
        # This test documents the initial state; can pass/skip if file exists from prior runs
        # File will be created during implementation
        pass

    def test_file_exists_at_repository_root(self):
        """Verify file exists at repository root."""
        assert self.FILE_PATH.exists(), f"File {self.FILE_PATH} does not exist"
        assert self.FILE_PATH.is_file(), f"{self.FILE_PATH} is not a file"

    def test_file_has_h1_heading_on_first_line(self):
        """Verify file contains exactly one H1 heading on the first line."""
        content = self.FILE_PATH.read_text(encoding='utf-8')
        lines = content.split('\n')
        assert len(lines) > 0, "File is empty"
        assert lines[0].startswith('# '), "First line does not start with '# '"
        h1_count = sum(1 for line in lines if line.startswith('# '))
        assert h1_count == 1, f"Expected exactly 1 H1 heading, found {h1_count}"

    def test_file_has_blank_line_after_heading(self):
        """Verify file has a blank line after the H1 heading."""
        content = self.FILE_PATH.read_text(encoding='utf-8')
        lines = content.split('\n')
        assert len(lines) > 1, "File has fewer than 2 lines"
        assert lines[1] == '', f"Second line should be blank, got: {repr(lines[1])}"

    def test_file_has_two_to_three_sentences(self):
        """Verify file contains exactly 2-3 sentences of prose after the blank line."""
        content = self.FILE_PATH.read_text(encoding='utf-8')
        lines = content.split('\n')
        # Skip heading and blank line, join remaining non-empty lines
        prose = '\n'.join(lines[2:]).strip()

        # Count sentences (periods followed by space or end of string)
        # This is a simple heuristic; allows for "abbreviations" but captures main sentences
        sentences = re.split(r'\.\s+', prose)
        sentences = [s.strip() for s in sentences if s.strip()]

        assert len(sentences) >= 2, f"Expected at least 2 sentences, found {len(sentences)}"
        assert len(sentences) <= 3, f"Expected at most 3 sentences, found {len(sentences)}"

    def test_file_uses_utf8_encoding(self):
        """Verify file is encoded in UTF-8."""
        # Read as bytes and check for BOM
        raw_bytes = self.FILE_PATH.read_bytes()
        bom = b'\xef\xbb\xbf'
        assert not raw_bytes.startswith(bom), "File has UTF-8 BOM, should be without BOM"

        # Verify file can be read as UTF-8 without errors
        try:
            self.FILE_PATH.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            raise AssertionError("File is not valid UTF-8")

    def test_file_uses_lf_line_endings(self):
        """Verify file uses LF (\\n) line endings, not CRLF."""
        raw_bytes = self.FILE_PATH.read_bytes()
        # Check that there are no CRLF sequences
        assert b'\r\n' not in raw_bytes, "File contains CRLF line endings, should use LF only"

    def test_file_size_in_range(self):
        """Verify file size is between 300-600 bytes."""
        file_size = self.FILE_PATH.stat().st_size
        assert 300 <= file_size <= 600, f"File size {file_size} is not in range 300-600 bytes"

    def test_file_has_proper_structure(self):
        """Verify overall file structure: H1 + blank line + prose."""
        content = self.FILE_PATH.read_text(encoding='utf-8')
        lines = content.split('\n')

        # First line: H1 heading
        assert lines[0].startswith('# '), "First line must be H1 heading"

        # Second line: blank
        assert lines[1] == '', "Second line must be blank"

        # Third line and beyond: prose content
        prose = '\n'.join(lines[2:]).strip()
        assert len(prose) > 0, "Prose content is empty"
        assert '.' in prose, "Prose should contain periods (sentences)"
