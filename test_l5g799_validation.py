#!/usr/bin/env python3
"""
Comprehensive validation test suite for test-l5g799.md markdown file.

Tests validate:
- Markdown syntax (H1 heading on first line)
- Sentence count (exactly 2-3 sentences)
- Encoding (UTF-8 without BOM)
- Line endings (LF only, no CRLF)
- File size (250-600 bytes)
- File structure and CommonMark compliance
"""

import unittest
import re
from pathlib import Path


class TestMarkdownValidation(unittest.TestCase):
    """Test suite for markdown file validation."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.file_path = Path("test-l5g799.md")

    # ========== File Existence Tests ==========

    def test_file_exists(self):
        """Test that the markdown file exists."""
        self.assertTrue(
            self.file_path.exists(),
            "test-l5g799.md must exist in repository root"
        )

    # ========== Encoding Tests ==========

    def test_utf8_encoding_valid(self):
        """Test that file is valid UTF-8 encoded."""
        try:
            content = self.file_path.read_text(encoding='utf-8')
            self.assertIsNotNone(content)
        except UnicodeDecodeError as e:
            self.fail(f"File is not valid UTF-8: {e}")

    def test_no_utf8_bom(self):
        """Test that file does not contain UTF-8 BOM (byte order mark)."""
        file_bytes = self.file_path.read_bytes()
        self.assertFalse(
            file_bytes.startswith(b'\xef\xbb\xbf'),
            "File contains UTF-8 BOM (0xEFBBBF) - should have no BOM"
        )

    # ========== Line Ending Tests ==========

    def test_no_crlf_line_endings(self):
        """Test that file does not contain CRLF (Windows) line endings."""
        file_bytes = self.file_path.read_bytes()
        self.assertNotIn(
            b'\r\n',
            file_bytes,
            "File contains CRLF line endings - should use LF only"
        )

    def test_no_cr_characters(self):
        """Test that file contains no CR (carriage return) characters."""
        file_bytes = self.file_path.read_bytes()
        self.assertNotIn(
            b'\r',
            file_bytes,
            "File contains CR characters - should use LF only"
        )

    def test_only_lf_line_endings(self):
        """Test that file uses only LF (Unix) line endings."""
        file_bytes = self.file_path.read_bytes()
        # If there's \n, check that no \r precedes it
        file_text = self.file_path.read_text(encoding='utf-8')
        # Split by LF and verify no lines contain CR
        lines = file_text.split('\n')
        for line in lines:
            self.assertNotIn(
                '\r',
                line,
                f"Line contains CR character: {line!r}"
            )

    # ========== Markdown Syntax Tests ==========

    def test_h1_heading_on_first_line(self):
        """Test that first line is a valid H1 markdown heading."""
        content = self.file_path.read_text(encoding='utf-8')
        first_line = content.split('\n')[0]
        self.assertTrue(
            first_line.startswith('# '),
            f"First line should start with '# ' (H1 heading), got: {first_line!r}"
        )

    def test_h1_heading_format(self):
        """Test that H1 heading follows proper markdown format."""
        content = self.file_path.read_text(encoding='utf-8')
        first_line = content.split('\n')[0]
        # H1 heading should be: # followed by space, then title text
        heading_pattern = r'^#\s+\w+'
        self.assertIsNotNone(
            re.match(heading_pattern, first_line),
            f"H1 heading does not match pattern '^#\\s+\\w+': {first_line!r}"
        )

    def test_blank_line_after_heading(self):
        """Test that second line is blank (after H1 heading)."""
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

    # ========== Prose Content Tests ==========

    def test_prose_content_exists(self):
        """Test that prose content exists after heading and blank line."""
        content = self.file_path.read_text(encoding='utf-8')
        prose_parts = content.split('\n\n', 1)
        self.assertEqual(
            len(prose_parts),
            2,
            "File should be split into heading and prose by blank line"
        )
        prose = prose_parts[1].strip()
        self.assertTrue(
            prose,
            "Prose content should not be empty"
        )

    def test_prose_has_minimum_length(self):
        """Test that prose content is substantial (at least 100 characters)."""
        content = self.file_path.read_text(encoding='utf-8')
        prose = content.split('\n\n', 1)[1].strip()
        self.assertGreaterEqual(
            len(prose),
            100,
            f"Prose content is too short ({len(prose)} chars), expected at least 100"
        )

    # ========== Sentence Count Tests ==========

    def test_sentence_count_minimum(self):
        """Test that prose contains at least 2 sentences."""
        content = self.file_path.read_text(encoding='utf-8')
        prose = content.split('\n\n', 1)[1].strip()

        # Count sentences using regex: terminal punctuation (. ! ?)
        # Count occurrences, handling abbreviations
        sentence_pattern = r'[.!?]'
        sentence_count = len(re.findall(sentence_pattern, prose))

        self.assertGreaterEqual(
            sentence_count,
            2,
            f"Prose must contain at least 2 sentences, found {sentence_count}"
        )

    def test_sentence_count_maximum(self):
        """Test that prose contains at most 3 sentences."""
        content = self.file_path.read_text(encoding='utf-8')
        prose = content.split('\n\n', 1)[1].strip()

        # Count sentences using regex: terminal punctuation (. ! ?)
        sentence_pattern = r'[.!?]'
        sentence_count = len(re.findall(sentence_pattern, prose))

        self.assertLessEqual(
            sentence_count,
            3,
            f"Prose must contain at most 3 sentences, found {sentence_count}"
        )

    def test_sentence_count_exact_range(self):
        """Test that prose contains exactly 2 or 3 sentences."""
        content = self.file_path.read_text(encoding='utf-8')
        prose = content.split('\n\n', 1)[1].strip()

        # Count sentences by terminal punctuation
        sentence_pattern = r'[.!?]'
        sentence_count = len(re.findall(sentence_pattern, prose))

        self.assertIn(
            sentence_count,
            [2, 3],
            f"Prose must have exactly 2 or 3 sentences, found {sentence_count}"
        )

    # ========== File Size Tests ==========

    def test_file_size_minimum(self):
        """Test that file size is at least 250 bytes."""
        file_bytes = self.file_path.read_bytes()
        file_size = len(file_bytes)
        self.assertGreaterEqual(
            file_size,
            250,
            f"File size {file_size} bytes is below minimum 250 bytes"
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
        """Test that file size is within 250-600 byte range."""
        file_bytes = self.file_path.read_bytes()
        file_size = len(file_bytes)
        self.assertGreaterEqual(file_size, 250, f"File too small: {file_size} bytes")
        self.assertLessEqual(file_size, 600, f"File too large: {file_size} bytes")

    # ========== File Structure Tests ==========

    def test_file_structure_commonmark_compliant(self):
        """Test that file structure is CommonMark compliant."""
        content = self.file_path.read_text(encoding='utf-8')
        # Should have: H1 heading + blank line + prose
        self.assertTrue(
            content.startswith('# '),
            "File must start with H1 heading (# )"
        )
        self.assertIn(
            '\n\n',
            content,
            "File must have blank line after heading"
        )

    def test_no_trailing_whitespace_on_lines(self):
        """Test that lines do not have trailing whitespace."""
        content = self.file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        for i, line in enumerate(lines):
            # Allow empty last line, but not trailing spaces on non-empty lines
            if line and not line.isspace():
                self.assertEqual(
                    line,
                    line.rstrip(),
                    f"Line {i + 1} has trailing whitespace: {line!r}"
                )

    def test_no_multiple_consecutive_blank_lines(self):
        """Test that file doesn't have multiple consecutive blank lines."""
        content = self.file_path.read_text(encoding='utf-8')
        # Should have exactly one blank line after heading, not more
        self.assertNotIn(
            '\n\n\n',
            content,
            "File should not have multiple consecutive blank lines"
        )

    # ========== Integration Tests ==========

    def test_complete_file_validation(self):
        """Integration test: validate all aspects of the file."""
        content = self.file_path.read_text(encoding='utf-8')
        file_bytes = self.file_path.read_bytes()

        # Check basic structure
        self.assertTrue(content.startswith('# '), "Must start with H1")
        self.assertIn('\n\n', content, "Must have blank line")

        # Check encoding
        self.assertFalse(file_bytes.startswith(b'\xef\xbb\xbf'), "No BOM")
        self.assertNotIn(b'\r\n', file_bytes, "No CRLF")

        # Check size
        file_size = len(file_bytes)
        self.assertTrue(250 <= file_size <= 600, f"Size {file_size} out of range")

        # Check sentences
        prose = content.split('\n\n', 1)[1].strip()
        sentence_count = len(re.findall(r'[.!?]', prose))
        self.assertTrue(2 <= sentence_count <= 3, f"Sentence count {sentence_count} invalid")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
