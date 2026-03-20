#!/usr/bin/env python3
"""Test suite for test-g4d3am.md markdown file validation."""

import unittest
from pathlib import Path


class TestG4d3amMarkdownFileValidation(unittest.TestCase):
    """Test cases for test-g4d3am.md markdown file validation (Phase 1)."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.file_path = Path("test-g4d3am.md")

    def test_file_exists(self):
        """Test that the markdown file exists."""
        self.assertTrue(self.file_path.exists(), "test-g4d3am.md must exist")

    # Task 1: File Creation & Structure Validation
    def test_h1_heading_on_first_line(self):
        """Test that first line is a valid H1 markdown heading."""
        content = self.file_path.read_text(encoding='utf-8')
        first_line = content.split('\n')[0]
        self.assertTrue(
            first_line.startswith('# '),
            f"First line should start with '# ' (H1 heading), got: {first_line!r}"
        )

    def test_blank_line_after_heading(self):
        """Test that second line is blank."""
        content = self.file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        self.assertGreaterEqual(
            len(lines),
            3,
            "File should have at least 3 lines (heading + blank + prose)"
        )
        self.assertEqual(
            lines[1],
            '',
            f"Second line should be blank, got: {lines[1]!r}"
        )

    def test_prose_content_exists(self):
        """Test that prose content exists after blank line."""
        content = self.file_path.read_text(encoding='utf-8')
        prose_parts = content.split('\n\n', 1)
        self.assertGreaterEqual(
            len(prose_parts),
            2,
            "File should have prose content after heading and blank line"
        )
        prose = prose_parts[1].strip()
        self.assertTrue(
            prose,
            "Prose content should not be empty"
        )

    def test_sentence_count_2_to_3(self):
        """Test that prose contains exactly 2-3 sentences."""
        content = self.file_path.read_text(encoding='utf-8')
        prose = content.split('\n\n', 1)[1].strip()
        # Count sentences by counting sentence-ending punctuation (periods)
        sentence_count = prose.count('.')
        self.assertGreaterEqual(
            sentence_count,
            2,
            f"Prose must contain at least 2 sentences, found {sentence_count}"
        )
        self.assertLessEqual(
            sentence_count,
            3,
            f"Prose must contain at most 3 sentences, found {sentence_count}"
        )

    # Task 2: UTF-8 Encoding and BOM Validation
    def test_utf8_encoding_valid(self):
        """Test that file is valid UTF-8 encoded."""
        try:
            self.file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError as e:
            self.fail(f"File is not valid UTF-8: {e}")

    def test_no_utf8_bom(self):
        """Test that file does not contain UTF-8 BOM."""
        file_bytes = self.file_path.read_bytes()
        self.assertFalse(
            file_bytes.startswith(b'\xef\xbb\xbf'),
            "File contains UTF-8 BOM (should not have BOM)"
        )

    # Task 3: Line Endings Validation
    def test_no_crlf_line_endings(self):
        """Test that file uses LF line endings, not CRLF."""
        file_bytes = self.file_path.read_bytes()
        self.assertNotIn(
            b'\r\n',
            file_bytes,
            "File contains CRLF line endings, should use LF only"
        )

    def test_only_lf_line_endings(self):
        """Test that file uses only LF line endings."""
        file_bytes = self.file_path.read_bytes()
        self.assertNotIn(
            b'\r',
            file_bytes,
            "File contains CR characters, should use LF only"
        )

    # Task 4: File Size Validation
    def test_file_size_minimum(self):
        """Test that file size is at least 400 bytes."""
        file_bytes = self.file_path.read_bytes()
        file_size = len(file_bytes)
        self.assertGreaterEqual(
            file_size,
            400,
            f"File size {file_size} bytes is below minimum 400 bytes"
        )

    def test_file_size_maximum(self):
        """Test that file size does not exceed 600 bytes."""
        file_bytes = self.file_path.read_bytes()
        file_size = len(file_bytes)
        self.assertLessEqual(
            file_size,
            600,
            f"File size {file_size} bytes exceeds maximum 600 bytes"
        )

    def test_file_size_in_range(self):
        """Test that file size is within 400-600 byte range."""
        file_bytes = self.file_path.read_bytes()
        file_size = len(file_bytes)
        self.assertGreaterEqual(file_size, 400)
        self.assertLessEqual(file_size, 600)

    def test_no_trailing_blank_lines(self):
        """Test that file ends with newline after prose, no trailing blank lines."""
        content = self.file_path.read_text(encoding='utf-8')
        # Strip trailing whitespace but preserve structure
        lines = content.rstrip('\n').split('\n')
        # Should have at least heading + blank + prose lines
        self.assertGreaterEqual(len(lines), 3)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
