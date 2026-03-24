#!/usr/bin/env python3
"""
Test suite for feature 194: markdown-file-creation-195fc2

Tests verify that test-omg7kb.md file:
- Exists and is readable
- Contains correct markdown structure (heading + prose)
- Uses proper encoding (UTF-8) and line endings (LF)
- Has meaningful, grammatically correct content
- Falls within acceptable file size range (300-600 bytes)
"""

import os
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

# Import functions from the implementation module
import sys
sys.path.insert(0, os.path.dirname(__file__))
from create_markdown_file_194 import (
    create_file,
    validate_file,
    FILENAME,
    TITLE,
    PROSE,
)


class TestFileCreation(unittest.TestCase):
    """Test cases for task-1: file creation function."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        """Clean up test fixtures."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def test_create_file_creates_file(self):
        """Test that create_file creates test-omg7kb.md at repository root."""
        result = create_file()
        self.assertIsNotNone(result, "create_file should return Path object")
        self.assertTrue(Path(FILENAME).exists(), f"File {FILENAME} should exist")

    def test_file_is_readable(self):
        """Test that created file is readable."""
        create_file()
        file_path = Path(FILENAME)
        self.assertTrue(file_path.is_file(), f"{FILENAME} should be a regular file")
        self.assertTrue(os.access(file_path, os.R_OK), f"{FILENAME} should be readable")

    def test_file_contains_h1_heading(self):
        """Test that file contains H1 heading on line 1."""
        create_file()
        file_path = Path(FILENAME)
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        self.assertTrue(lines[0].startswith('# '), "First line should be H1 heading")
        self.assertIn(TITLE, lines[0], "H1 should contain the title")

    def test_file_contains_blank_line(self):
        """Test that file contains blank line on line 2."""
        create_file()
        file_path = Path(FILENAME)
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        self.assertEqual(len(lines) > 1, True, "File should have multiple lines")
        self.assertEqual(lines[1], '', "Second line should be blank")

    def test_file_contains_prose(self):
        """Test that file contains 2-3 sentences of prose on lines 3+."""
        create_file()
        file_path = Path(FILENAME)
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        self.assertGreaterEqual(len(lines), 3, "File should have content after heading")
        prose = '\n'.join(lines[2:]).strip()
        self.assertGreater(len(prose), 0, "Prose content should not be empty")
        self.assertIn(PROSE, prose, "Prose should match expected content")

    def test_create_file_returns_path_object(self):
        """Test that create_file returns Path object."""
        result = create_file()
        self.assertIsInstance(result, Path, "create_file should return Path object")

    def test_file_does_not_exist_error(self):
        """Test that create_file handles existing files gracefully."""
        create_file()
        result = create_file()
        self.assertIsNone(result, "create_file should return None if file exists")


class TestEncodingValidation(unittest.TestCase):
    """Test cases for task-2: encoding and line ending validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        """Clean up test fixtures."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def test_valid_utf8_encoding(self):
        """Test that validation passes for valid UTF-8 encoding."""
        create_file()
        # Should not raise
        result = validate_file(FILENAME)
        self.assertTrue(result, "Validation should pass for valid UTF-8")

    def test_utf8_without_bom(self):
        """Test that file is UTF-8 without BOM."""
        create_file()
        file_path = Path(FILENAME)
        raw_bytes = file_path.read_bytes()
        self.assertFalse(
            raw_bytes.startswith(b'\xef\xbb\xbf'),
            "File should not have UTF-8 BOM"
        )

    def test_lf_line_endings_only(self):
        """Test that file uses LF line endings, not CRLF."""
        create_file()
        file_path = Path(FILENAME)
        raw_bytes = file_path.read_bytes()
        self.assertNotIn(
            b'\r\n',
            raw_bytes,
            "File should use LF line endings, not CRLF"
        )

    def test_validation_fails_with_bom(self):
        """Test that validation fails if BOM is present."""
        # Create file with BOM
        file_path = Path(FILENAME)
        content = f"# {TITLE}\n\n{PROSE}\n"
        bom_content = b'\xef\xbb\xbf' + content.encode('utf-8')
        file_path.write_bytes(bom_content)

        with self.assertRaises(ValueError) as context:
            validate_file(FILENAME)
        self.assertIn('BOM', str(context.exception))

    def test_validation_fails_with_crlf(self):
        """Test that validation fails if CRLF is present."""
        # Create file with CRLF
        file_path = Path(FILENAME)
        content = f"# {TITLE}\r\n\r\n{PROSE}\r\n"
        file_path.write_bytes(content.encode('utf-8'))

        with self.assertRaises(ValueError) as context:
            validate_file(FILENAME)
        self.assertIn('CRLF', str(context.exception))

    def test_validation_accepts_lf(self):
        """Test that validation accepts LF line endings."""
        create_file()
        result = validate_file(FILENAME)
        self.assertTrue(result, "Validation should accept LF line endings")


class TestStructureValidation(unittest.TestCase):
    """Test cases for task-3: structure and size validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        """Clean up test fixtures."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def test_file_size_in_range(self):
        """Test that file size is between 300-600 bytes."""
        create_file()
        file_path = Path(FILENAME)
        file_size = file_path.stat().st_size
        self.assertGreaterEqual(
            file_size, 300,
            f"File size {file_size} should be >= 300 bytes"
        )
        self.assertLessEqual(
            file_size, 600,
            f"File size {file_size} should be <= 600 bytes"
        )

    def test_validation_fails_if_size_too_small(self):
        """Test that validation fails if file size is below 300 bytes."""
        file_path = Path(FILENAME)
        # Create a small file with valid structure but too small
        file_path.write_bytes(b"# Title\n\nSmall sentence. Another.\n")

        with self.assertRaises(ValueError) as context:
            validate_file(FILENAME)
        self.assertIn('300-600', str(context.exception))

    def test_validation_fails_if_size_too_large(self):
        """Test that validation fails if file size exceeds 600 bytes."""
        file_path = Path(FILENAME)
        # Create a large file with exactly 3 sentences but over 600 bytes
        # Each sentence must contain exactly one period
        words = "word " * 80  # Create a long string of repeated words
        large_prose = f"First sentence with {words}end. Second sentence with {words}end. Third sentence with {words}end."
        content = f"# {TITLE}\n\n{large_prose}\n"
        file_path.write_bytes(content.encode('utf-8'))

        with self.assertRaises(ValueError) as context:
            validate_file(FILENAME)
        self.assertIn('300-600', str(context.exception))

    def test_h1_heading_on_line_1(self):
        """Test that H1 heading is on line 1."""
        create_file()
        result = validate_file(FILENAME)
        self.assertTrue(result, "Validation should pass with H1 on line 1")

    def test_validation_fails_without_h1(self):
        """Test that validation fails if H1 heading is missing."""
        file_path = Path(FILENAME)
        file_path.write_bytes(b"No heading here\n\nProse content here.\n")

        with self.assertRaises(ValueError) as context:
            validate_file(FILENAME)
        self.assertIn('H1', str(context.exception))

    def test_blank_line_on_line_2(self):
        """Test that blank line is on line 2."""
        create_file()
        file_path = Path(FILENAME)
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        self.assertEqual(lines[1], '', "Line 2 should be blank")

    def test_validation_fails_without_blank_line(self):
        """Test that validation fails if blank line is missing."""
        file_path = Path(FILENAME)
        content = f"# {TITLE}\n{PROSE}\n"
        file_path.write_bytes(content.encode('utf-8'))

        with self.assertRaises(ValueError) as context:
            validate_file(FILENAME)
        self.assertIn('blank', str(context.exception).lower())

    def test_prose_content_exists(self):
        """Test that prose content exists after blank line."""
        create_file()
        result = validate_file(FILENAME)
        self.assertTrue(result, "Validation should pass with prose content")

    def test_sentence_count_is_correct(self):
        """Test that prose contains 2-3 sentences."""
        create_file()
        file_path = Path(FILENAME)
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        prose = '\n'.join(lines[2:]).strip()
        sentence_count = prose.count('.')
        self.assertGreaterEqual(
            sentence_count, 2,
            f"Prose should have at least 2 sentences (has {sentence_count})"
        )
        self.assertLessEqual(
            sentence_count, 3,
            f"Prose should have at most 3 sentences (has {sentence_count})"
        )

    def test_validation_fails_with_too_few_sentences(self):
        """Test that validation fails if prose has fewer than 2 sentences."""
        file_path = Path(FILENAME)
        content = b"# Title\n\nOne sentence.\n"
        file_path.write_bytes(content)

        with self.assertRaises(ValueError) as context:
            validate_file(FILENAME)
        self.assertIn('2-3 sentences', str(context.exception))

    def test_validation_fails_with_too_many_sentences(self):
        """Test that validation fails if prose has more than 3 sentences."""
        file_path = Path(FILENAME)
        content = b"# Title\n\nOne. Two. Three. Four.\n"
        file_path.write_bytes(content)

        with self.assertRaises(ValueError) as context:
            validate_file(FILENAME)
        self.assertIn('2-3 sentences', str(context.exception))

    def test_file_ends_with_newline(self):
        """Test that file ends with newline."""
        create_file()
        file_path = Path(FILENAME)
        content = file_path.read_text(encoding='utf-8')
        self.assertTrue(
            content.endswith('\n'),
            "File should end with newline"
        )

    def test_validation_fails_without_final_newline(self):
        """Test that validation fails if file doesn't end with newline."""
        file_path = Path(FILENAME)
        content = f"# {TITLE}\n\n{PROSE}"  # No trailing newline
        file_path.write_bytes(content.encode('utf-8'))

        with self.assertRaises(ValueError) as context:
            validate_file(FILENAME)
        self.assertIn('newline', str(context.exception).lower())

    def test_combined_validation_passes(self):
        """Test that all validations pass together."""
        create_file()
        result = validate_file(FILENAME)
        self.assertTrue(result, "All validation checks should pass")


class TestIntegration(unittest.TestCase):
    """Integration tests for file creation and validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        """Clean up test fixtures."""
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def test_create_and_validate(self):
        """Test that created file passes all validations."""
        create_file()
        result = validate_file(FILENAME)
        self.assertTrue(result, "Created file should pass validation")

    def test_file_is_valid_markdown(self):
        """Test that created file is valid CommonMark markdown."""
        create_file()
        file_path = Path(FILENAME)
        content = file_path.read_text(encoding='utf-8')
        # Verify basic markdown structure
        self.assertIn('# ', content, "Should contain H1 heading")
        self.assertGreater(len(content), 50, "Content should have reasonable length")


if __name__ == '__main__':
    unittest.main()
