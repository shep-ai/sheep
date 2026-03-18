"""
Test suite for feature 100 markdown file creation.

Tests verify that test-aear8n.md file:
- Exists and is readable
- Contains correct markdown structure (heading + prose)
- Uses proper encoding (UTF-8 without BOM) and line endings (LF only)
- Has meaningful content within acceptable file size range (320-600 bytes)
"""

import os
import re
import unittest
from pathlib import Path


class TestMarkdownFileCreation(unittest.TestCase):
    """Test cases for test-aear8n.md markdown file creation."""

    FILENAME = "test-aear8n.md"

    def setUp(self):
        """Set up test fixtures."""
        self.file_path = Path(self.FILENAME)

    def test_file_exists(self):
        """Test that the markdown file exists at repository root."""
        self.assertTrue(
            self.file_path.exists(),
            f"File {self.FILENAME} does not exist at repository root"
        )

    def test_file_is_readable(self):
        """Test that the markdown file is readable."""
        self.assertTrue(
            self.file_path.is_file(),
            f"{self.FILENAME} is not a regular file"
        )
        self.assertTrue(
            os.access(self.file_path, os.R_OK),
            f"{self.FILENAME} is not readable"
        )

    def test_file_encoding_is_utf8_without_bom(self):
        """Test that file encoding is UTF-8 without BOM."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                f.read()
        except UnicodeDecodeError:
            self.fail(f"{self.FILENAME} is not valid UTF-8 encoded")

        # Check for UTF-8 BOM (should not be present)
        with open(self.file_path, 'rb') as f:
            raw_bytes = f.read()
        self.assertFalse(
            raw_bytes.startswith(b'\xef\xbb\xbf'),
            f"{self.FILENAME} has UTF-8 BOM (should not)"
        )

    def test_file_line_endings_are_lf_only(self):
        """Test that file uses LF line endings (not CRLF or CR)."""
        with open(self.file_path, 'rb') as f:
            raw_bytes = f.read()

        # Should not contain CRLF (Windows line endings)
        self.assertNotIn(
            b'\r\n',
            raw_bytes,
            f"{self.FILENAME} contains CRLF line endings (should be LF)"
        )
        # Should not contain CR (old Mac line endings)
        self.assertNotIn(
            b'\r',
            raw_bytes,
            f"{self.FILENAME} contains CR line endings (should be LF)"
        )

    def test_contains_h1_heading(self):
        """Test that file contains H1 heading (# Title)."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()

        self.assertTrue(
            first_line.startswith('# '),
            f"First line should be H1 heading (# Title), got: {first_line!r}"
        )

    def test_blank_line_after_heading(self):
        """Test that there is a blank line separating heading from prose."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        self.assertGreaterEqual(
            len(lines),
            3,
            "File should have at least 3 lines (heading + blank + prose)"
        )
        self.assertEqual(
            lines[1].strip(),
            '',
            f"Second line should be blank, got: {lines[1]!r}"
        )

    def test_contains_2_or_3_sentences(self):
        """Test that prose contains 2-3 sentences."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Get prose content (everything after heading and blank line)
        prose = ''.join(lines[2:]).strip()

        # Count sentences: split on periods, exclamation marks, question marks
        sentences = re.split(r'[.!?]+\s+', prose)
        # Filter out empty strings
        sentences = [s.strip() for s in sentences if s.strip()]

        self.assertGreaterEqual(
            len(sentences),
            2,
            f"Expected at least 2 sentences, found {len(sentences)}"
        )
        self.assertLessEqual(
            len(sentences),
            3,
            f"Expected at most 3 sentences, found {len(sentences)}"
        )

    def test_file_size_in_range(self):
        """Test that file size is between 320-600 bytes (NFR-3)."""
        file_size = self.file_path.stat().st_size
        self.assertGreaterEqual(
            file_size,
            320,
            f"File size {file_size} bytes is below 320-byte minimum"
        )
        self.assertLessEqual(
            file_size,
            600,
            f"File size {file_size} bytes exceeds 600-byte maximum"
        )

    def test_prose_is_meaningful(self):
        """Test that prose content is meaningful (not placeholder text)."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        prose = ''.join(lines[2:]).strip()

        # Content should not be obvious placeholder text
        placeholder_patterns = [
            r'^\s*lorem ipsum',
            r'todo|tbd|placeholder',
            r'to\s+be\s+filled|to\s+fill',
            r'^\s*\.\.\.',
        ]

        for pattern in placeholder_patterns:
            self.assertIsNone(
                re.search(pattern, prose, re.IGNORECASE),
                f"Prose contains placeholder pattern: {pattern}"
            )


if __name__ == '__main__':
    unittest.main()
