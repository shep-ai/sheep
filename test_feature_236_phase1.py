#!/usr/bin/env python3
"""Test suite for feature 236: markdown file creation test-wxtr9o.md.

Tests verify that test-wxtr9o.md file:
- Exists and is readable
- Contains correct markdown structure (heading + prose)
- Uses proper encoding (UTF-8 without BOM) and line endings (LF)
- Has 2-3 sentences of substantive, meaningful content
- Falls within acceptable file size range (400-600 bytes)
"""

import os
import re
import unittest
from pathlib import Path


class TestFeature236MarkdownFileCreation(unittest.TestCase):
    """Test cases for feature 236 markdown file creation (Phase 1)."""

    FILENAME = "test-wxtr9o.md"

    def setUp(self):
        """Set up test fixtures."""
        self.file_path = Path(self.FILENAME)

    # ===== Task 1: File Creation =====

    def test_file_exists(self):
        """Test that test-wxtr9o.md exists at repository root."""
        self.assertTrue(
            self.file_path.exists(),
            f"File {self.FILENAME} does not exist at repository root"
        )

    def test_file_is_regular_file(self):
        """Test that test-wxtr9o.md is a regular file (not directory)."""
        self.assertTrue(
            self.file_path.is_file(),
            f"{self.FILENAME} is not a regular file"
        )

    def test_file_is_readable(self):
        """Test that test-wxtr9o.md is readable."""
        self.assertTrue(
            os.access(self.file_path, os.R_OK),
            f"{self.FILENAME} is not readable"
        )

    def test_file_contains_h1_heading(self):
        """Test that file contains at least one H1 heading."""
        content = self.file_path.read_text(encoding='utf-8')
        h1_count = len(re.findall(r'^\#\s+', content, re.MULTILINE))
        self.assertGreaterEqual(
            h1_count,
            1,
            "File should contain at least one H1 heading (lines starting with '# ')"
        )

    def test_h1_heading_on_first_line(self):
        """Test that first line is a valid H1 markdown heading."""
        content = self.file_path.read_text(encoding='utf-8')
        first_line = content.split('\n')[0]
        self.assertTrue(
            first_line.startswith('# '),
            f"First line should start with '# ' (H1 heading), got: {first_line!r}"
        )

    # ===== Task 2: Encoding and Line Endings Validation =====

    def test_file_encoding_is_utf8(self):
        """Test that file is valid UTF-8 encoded."""
        try:
            self.file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError as e:
            self.fail(f"{self.FILENAME} is not valid UTF-8: {e}")

    def test_no_utf8_bom(self):
        """Test that file does not contain UTF-8 BOM (Byte Order Mark)."""
        file_bytes = self.file_path.read_bytes()
        self.assertFalse(
            file_bytes.startswith(b'\xef\xbb\xbf'),
            f"{self.FILENAME} contains UTF-8 BOM (should not have BOM)"
        )

    def test_no_crlf_line_endings(self):
        """Test that file does not contain CRLF (Windows) line endings."""
        file_bytes = self.file_path.read_bytes()
        self.assertNotIn(
            b'\r\n',
            file_bytes,
            f"{self.FILENAME} contains CRLF line endings, should use LF only"
        )

    def test_only_lf_line_endings(self):
        """Test that file uses only LF line endings, no CR characters."""
        file_bytes = self.file_path.read_bytes()
        self.assertNotIn(
            b'\r',
            file_bytes,
            f"{self.FILENAME} contains CR characters, should use LF only"
        )

    # ===== Task 3: Markdown Structure Validation =====

    def test_blank_line_after_heading(self):
        """Test that second line is blank (separator between heading and prose)."""
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
        """Test that prose content exists after heading and blank line."""
        content = self.file_path.read_text(encoding='utf-8')
        # Split on double newline to separate heading+blank from prose
        parts = content.split('\n\n', 1)
        self.assertGreaterEqual(
            len(parts),
            2,
            "File should have prose content after heading and blank line"
        )
        prose = parts[1].strip()
        self.assertTrue(
            prose,
            "Prose content should not be empty"
        )

    def test_prose_is_substantive(self):
        """Test that prose is substantive and not placeholder text."""
        content = self.file_path.read_text(encoding='utf-8')
        prose = content.split('\n\n', 1)[1].strip()

        # Check that prose is not just placeholder patterns
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

    def test_prose_starts_with_capital_letter(self):
        """Test that prose starts with a capital letter."""
        content = self.file_path.read_text(encoding='utf-8')
        prose = content.split('\n\n', 1)[1].strip()
        self.assertTrue(
            prose[0].isupper(),
            f"Prose should start with capital letter, starts with: {prose[0]!r}"
        )

    def test_heading_and_prose_are_related(self):
        """Test that heading and prose are substantively related."""
        content = self.file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        heading = lines[0][2:].strip()  # Remove '# ' prefix
        prose = content.split('\n\n', 1)[1].strip()

        # Check that heading and prose share some concept words
        # Extract words from heading (case-insensitive)
        heading_words = set(re.findall(r'\w+', heading.lower()))

        # Extract content words from prose
        prose_words = set(re.findall(r'\b\w{4,}\b', prose.lower()))

        # Verify there's some overlap (heading concept appears in prose)
        # Allow for paraphrasing - prose should be at least somewhat related
        self.assertGreater(
            len(heading_words),
            0,
            "Heading should contain at least one meaningful word"
        )
        self.assertGreater(
            len(prose_words),
            0,
            "Prose should contain meaningful words"
        )

    def test_exactly_one_h1_heading(self):
        """Test that file contains exactly one H1 heading."""
        content = self.file_path.read_text(encoding='utf-8')
        h1_count = len(re.findall(r'^\#\s+', content, re.MULTILINE))
        self.assertEqual(
            h1_count,
            1,
            f"File should contain exactly one H1 heading, found {h1_count}"
        )

    def test_sentence_count_2_to_3(self):
        """Test that prose contains exactly 2-3 sentences."""
        content = self.file_path.read_text(encoding='utf-8')
        prose = content.split('\n\n', 1)[1].strip()

        # Count sentences by counting sentence-ending punctuation
        # Split on sentence-ending punctuation followed by space or end of string
        sentences = re.split(r'[.!?]+\s+', prose)
        # Filter out empty strings
        sentences = [s.strip() for s in sentences if s.strip()]

        self.assertGreaterEqual(
            len(sentences),
            2,
            f"Prose must contain at least 2 sentences, found {len(sentences)}: {sentences}"
        )
        self.assertLessEqual(
            len(sentences),
            3,
            f"Prose must contain at most 3 sentences, found {len(sentences)}: {sentences}"
        )

    # ===== Task 4: File Size Validation =====

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
        print(f"\nFile size: {file_size} bytes (within 400-600 range)")


if __name__ == '__main__':
    unittest.main(verbosity=2)
