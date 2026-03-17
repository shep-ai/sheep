"""
Test suite for markdown file creation feature (test-gwplv4.md).

Tests verify that test-gwplv4.md file:
- Exists and is readable
- Contains correct markdown structure (heading + prose)
- Uses proper encoding (UTF-8) and line endings (LF)
- Has meaningful, grammatically correct content
- Falls within acceptable file size range
"""

import os
import re
import unittest
from pathlib import Path


class TestMarkdownFileCreation(unittest.TestCase):
    """Test cases for test-gwplv4.md markdown file creation."""

    FILENAME = "test-gwplv4.md"

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

    def test_file_encoding_is_utf8(self):
        """Test that file encoding is UTF-8 (no BOM)."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                f.read()
        except UnicodeDecodeError:
            self.fail(f"{self.FILENAME} is not valid UTF-8 encoded")

        # Check for UTF-8 BOM
        with open(self.file_path, 'rb') as f:
            raw_bytes = f.read()
        self.assertFalse(
            raw_bytes.startswith(b'\xef\xbb\xbf'),
            f"{self.FILENAME} has UTF-8 BOM (should not)"
        )

    def test_file_line_endings_are_lf(self):
        """Test that file uses LF line endings (not CRLF or CR)."""
        with open(self.file_path, 'rb') as f:
            raw_bytes = f.read()

        self.assertNotIn(
            b'\r\n',
            raw_bytes,
            f"{self.FILENAME} contains CRLF line endings (should be LF)"
        )
        self.assertNotIn(
            b'\r',
            raw_bytes,
            f"{self.FILENAME} contains CR line endings (should be LF)"
        )

    def test_file_contains_level1_heading(self):
        """Test that file contains exactly one level-1 heading (#)."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Count level-1 headings (lines starting with single #)
        heading_count = len(re.findall(r'^\#\s+', content, re.MULTILINE))
        self.assertEqual(
            heading_count,
            1,
            f"Expected exactly 1 level-1 heading, found {heading_count}"
        )

    def test_heading_is_first_line(self):
        """Test that level-1 heading is on the first line."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()

        self.assertTrue(
            first_line.startswith('# '),
            f"First line should be a level-1 heading starting with '# ', got: {first_line!r}"
        )

    def test_blank_line_after_heading(self):
        """Test that there is exactly one blank line after the heading."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        self.assertGreaterEqual(
            len(lines),
            3,
            f"File should have at least 3 lines (heading + blank + prose), has {len(lines)}"
        )
        self.assertEqual(
            lines[1].strip(),
            '',
            f"Second line should be blank, got: {lines[1]!r}"
        )

    def test_prose_content_exists(self):
        """Test that file contains prose content after the heading."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        prose_lines = [line for line in lines[2:] if line.strip()]
        self.assertGreater(
            len(prose_lines),
            0,
            "File should contain prose content after heading and blank line"
        )

    def test_contains_2_or_3_sentences(self):
        """Test that prose contains 2-3 sentences."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Get prose content (everything after heading and blank line)
        prose = ''.join(lines[2:]).strip()

        # Count sentences: count periods as sentence markers
        sentence_count = prose.count('.')
        self.assertGreaterEqual(
            sentence_count,
            2,
            f"Expected at least 2 sentences, found {sentence_count}"
        )
        self.assertLessEqual(
            sentence_count,
            3,
            f"Expected at most 3 sentences, found {sentence_count}"
        )

    def test_prose_is_grammatically_correct(self):
        """Test that prose starts with a capital letter and is well-formed."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        prose = ''.join(lines[2:]).strip()

        self.assertGreater(
            len(prose),
            0,
            "Prose content is empty"
        )
        self.assertTrue(
            prose[0].isupper(),
            f"Prose should start with capital letter, starts with: {prose[0]!r}"
        )

    def test_prose_content_is_meaningful(self):
        """Test that prose content is not empty placeholder text."""
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

    def test_file_size_is_in_range(self):
        """Test that file size is between 350-650 bytes."""
        file_size = self.file_path.stat().st_size
        self.assertGreater(
            file_size,
            350,
            f"File size {file_size} bytes is at or below 350-byte minimum"
        )
        self.assertLess(
            file_size,
            650,
            f"File size {file_size} bytes is at or above 650-byte maximum"
        )

    def test_markdown_syntax_is_valid(self):
        """Test that file contains valid markdown (no unmatched brackets/parens)."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for unmatched brackets
        self.assertEqual(
            content.count('['),
            content.count(']'),
            "Unmatched square brackets in markdown"
        )


if __name__ == '__main__':
    unittest.main()
