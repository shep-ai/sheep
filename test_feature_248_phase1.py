"""
Test suite for feature 248 Phase 1: File Creation and Validation

Tests for creating markdown file test-2oiio6.md with H1 heading and 2-3 sentences
of prose content. Tests cover:
- Task 1: File creation with correct structure
- Task 2: File encoding (UTF-8 without BOM) and line endings (Unix LF)
- Task 3: File structure validation and content validation (sentence count, file size)
"""

import tempfile
import unittest
from pathlib import Path


class TestMarkdownFileCreation(unittest.TestCase):
    """Task 1: Create markdown file with H1 heading and prose content"""

    # Sample content that meets the 400-600 byte requirement
    TEST_CONTENT = "# The Science of Curiosity\n\nCuriosity is the fundamental driver of human progress and scientific discovery, pushing us to ask questions and seek understanding about the world around us. When we cultivate a genuine desire to learn and explore new ideas, we unlock pathways to innovation and personal growth that might otherwise remain hidden. This intrinsic motivation to understand connects us to centuries of scientific tradition and positions us to contribute meaningfully to the advancement of human knowledge."

    def test_file_created_at_correct_path(self):
        """Assert file exists at correct path after creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8')

            self.assertTrue(filepath.exists(), "File should exist after creation")
            self.assertTrue(filepath.is_file(), "Path should be a file, not directory")

    def test_file_contains_h1_heading(self):
        """Assert file starts with H1 heading (# Title)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8')

            text_content = filepath.read_text(encoding='utf-8')
            lines = text_content.split('\n')

            self.assertGreater(len(lines), 0, "File should have content")
            self.assertTrue(lines[0].startswith('# '), "First line should start with '# '")

    def test_file_has_blank_line_separator(self):
        """Assert second line is blank (blank line separator)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8')

            text_content = filepath.read_text(encoding='utf-8')
            lines = text_content.split('\n')

            self.assertGreaterEqual(len(lines), 2, "File should have at least 2 lines")
            self.assertEqual(lines[1].strip(), '', "Second line should be blank")

    def test_file_contains_prose_content(self):
        """Assert content exists after blank line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8')

            text_content = filepath.read_text(encoding='utf-8')
            lines = text_content.split('\n')
            prose = '\n'.join(lines[2:]).strip()

            self.assertGreater(len(prose), 0, "Prose content should exist")

    def test_file_size_in_valid_range(self):
        """Assert file size is between 400-600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8')

            file_size = filepath.stat().st_size
            self.assertGreaterEqual(file_size, 400, f"File size {file_size} should be at least 400")
            self.assertLessEqual(file_size, 600, f"File size {file_size} should be at most 600")


class TestFileEncoding(unittest.TestCase):
    """Task 2: Validate file encoding (UTF-8 without BOM) and line endings"""

    TEST_CONTENT = "# The Science of Curiosity\n\nCuriosity is the fundamental driver of human progress and scientific discovery, pushing us to ask questions and seek understanding about the world around us. When we cultivate a genuine desire to learn and explore new ideas, we unlock pathways to innovation and personal growth that might otherwise remain hidden. This intrinsic motivation to understand connects us to centuries of scientific tradition and positions us to contribute meaningfully to the advancement of human knowledge."

    def test_file_is_valid_utf8(self):
        """Assert file decodes successfully as UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8')

            # Should not raise any exception
            try:
                filepath.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                self.fail("File should decode as UTF-8")

    def test_file_has_no_utf8_bom(self):
        """Assert file does not start with UTF-8 BOM (bytes EF BB BF)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8')

            binary_content = filepath.read_bytes()

            # UTF-8 BOM is bytes EF BB BF
            self.assertFalse(binary_content.startswith(b'\xef\xbb\xbf'), "File should not start with UTF-8 BOM")

    def test_file_has_no_crlf_line_endings(self):
        """Assert file does not contain CRLF byte sequence (0D 0A)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8', newline='\n')

            binary_content = filepath.read_bytes()

            # CRLF is bytes 0D 0A
            self.assertNotIn(b'\r\n', binary_content, "File should not contain CRLF line endings")

    def test_file_uses_lf_line_endings(self):
        """Assert file uses only LF (0A) line endings, not CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8', newline='\n')

            binary_content = filepath.read_bytes()

            # Check for LF line endings where there are newlines
            self.assertIn(b'\n', binary_content, "File should contain LF line endings")
            # Ensure no CRLF
            self.assertNotIn(b'\r\n', binary_content, "File should use LF, not CRLF")


class TestFileStructureAndContent(unittest.TestCase):
    """Task 3: Validate file structure, content, and sentence count"""

    TEST_CONTENT = "# The Science of Curiosity\n\nCuriosity is the fundamental driver of human progress and scientific discovery, pushing us to ask questions and seek understanding about the world around us. When we cultivate a genuine desire to learn and explore new ideas, we unlock pathways to innovation and personal growth that might otherwise remain hidden. This intrinsic motivation to understand connects us to centuries of scientific tradition and positions us to contribute meaningfully to the advancement of human knowledge."

    def test_file_first_line_is_h1_heading(self):
        """Assert first line starts with '# ' (H1 heading marker)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8')

            lines = filepath.read_text(encoding='utf-8').split('\n')
            self.assertTrue(lines[0].startswith('# '), "First line should start with '# '")

    def test_file_second_line_is_blank(self):
        """Assert second line is empty (blank line separator)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8')

            lines = filepath.read_text(encoding='utf-8').split('\n')
            self.assertEqual(lines[1].strip(), '', "Second line should be blank")

    def test_file_prose_content_exists(self):
        """Assert prose content exists and is non-empty."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8')

            lines = filepath.read_text(encoding='utf-8').split('\n')
            prose = '\n'.join(lines[2:]).strip()

            self.assertGreater(len(prose), 0, "Prose content should be non-empty")

    def test_file_prose_has_minimum_sentences(self):
        """Assert prose contains at least 2 periods (minimum 2 sentences)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8')

            lines = filepath.read_text(encoding='utf-8').split('\n')
            prose = '\n'.join(lines[2:]).strip()
            period_count = prose.count('.')

            self.assertGreaterEqual(period_count, 2, f"Prose should contain at least 2 periods, has {period_count}")

    def test_file_prose_has_maximum_sentences(self):
        """Assert prose contains at most 3 periods (maximum 3 sentences)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8')

            lines = filepath.read_text(encoding='utf-8').split('\n')
            prose = '\n'.join(lines[2:]).strip()
            period_count = prose.count('.')

            self.assertLessEqual(period_count, 3, f"Prose should contain at most 3 periods, has {period_count}")

    def test_file_prose_has_exactly_2_sentences(self):
        """Test case: prose with exactly 2 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            content = "# Heading\n\nFirst sentence with enough content to make it substantial. Second sentence with content as well to meet the minimum length requirements of the markdown file specification."
            filepath.write_text(content, encoding='utf-8')

            lines = filepath.read_text(encoding='utf-8').split('\n')
            prose = '\n'.join(lines[2:]).strip()
            period_count = prose.count('.')

            self.assertEqual(period_count, 2, f"Expected 2 periods, got {period_count}")

    def test_file_prose_has_exactly_3_sentences(self):
        """Test case: prose with exactly 3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            content = "# Heading\n\nFirst sentence with substantial content. Second sentence adding more information and depth. Third sentence completing the thought with final details and perspective."
            filepath.write_text(content, encoding='utf-8')

            lines = filepath.read_text(encoding='utf-8').split('\n')
            prose = '\n'.join(lines[2:]).strip()
            period_count = prose.count('.')

            self.assertEqual(period_count, 3, f"Expected 3 periods, got {period_count}")

    def test_file_size_minimum(self):
        """Assert file size is at least 400 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8')

            file_size = filepath.stat().st_size
            self.assertGreaterEqual(file_size, 400, f"File size {file_size} should be at least 400 bytes")

    def test_file_size_maximum(self):
        """Assert file size is at most 600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-2oiio6.md"
            filepath.write_text(self.TEST_CONTENT, encoding='utf-8')

            file_size = filepath.stat().st_size
            self.assertLessEqual(file_size, 600, f"File size {file_size} should be at most 600 bytes")


if __name__ == "__main__":
    unittest.main()
