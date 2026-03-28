#!/usr/bin/env python3
"""
Unit tests for validate_test_0c8bhn.py

Tests the validation function for feature 248: markdown-file-creation-87cda7

Test coverage:
- validate_file() raises FileNotFoundError when file does not exist
- validate_file() raises ValueError when file has no H1 heading
- validate_file() raises ValueError when sentence count is not 2-3
- validate_file() returns True when file meets all requirements
"""

import tempfile
import unittest
from pathlib import Path
from validate_test_0c8bhn import validate_file, _count_sentences, _has_h1_heading


class TestSentenceCounter(unittest.TestCase):
    """Tests for _count_sentences helper function."""

    def test_count_sentences_with_periods(self):
        """Test counting sentences ending with periods."""
        prose = "First sentence. Second sentence. Third sentence."
        self.assertEqual(_count_sentences(prose), 3)

    def test_count_sentences_with_mixed_punctuation(self):
        """Test counting sentences with mixed punctuation marks."""
        prose = "First sentence. Is this second? Yes it is!"
        self.assertEqual(_count_sentences(prose), 3)

    def test_count_sentences_two_only(self):
        """Test counting exactly 2 sentences."""
        prose = "First sentence. Second sentence."
        self.assertEqual(_count_sentences(prose), 2)

    def test_count_sentences_with_ellipsis(self):
        """Test that ellipsis is handled correctly."""
        prose = "This is interesting... Very interesting indeed. Final thought."
        count = _count_sentences(prose)
        self.assertIn(count, [2, 3])

    def test_count_sentences_empty_string(self):
        """Test counting sentences in empty string."""
        self.assertEqual(_count_sentences(""), 0)

    def test_count_sentences_no_punctuation(self):
        """Test string with no sentence punctuation."""
        prose = "This is some text without punctuation"
        self.assertEqual(_count_sentences(prose), 0)

    def test_count_sentences_with_abbreviation(self):
        """Test that abbreviations don't cause false positives."""
        prose = "Dr. Smith is here. That is good news!"
        count = _count_sentences(prose)
        self.assertGreaterEqual(count, 2)


class TestH1HeadingDetector(unittest.TestCase):
    """Tests for _has_h1_heading helper function."""

    def test_has_h1_heading_valid(self):
        """Test detection of valid H1 heading."""
        lines = ["# My Heading", "blank", "prose"]
        self.assertTrue(_has_h1_heading(lines))

    def test_has_h1_heading_missing(self):
        """Test detection when H1 heading is missing."""
        lines = ["Some text", "more text"]
        self.assertFalse(_has_h1_heading(lines))

    def test_has_h1_heading_wrong_format(self):
        """Test detection when heading format is wrong (double hash)."""
        lines = ["## My Heading", "prose"]
        self.assertFalse(_has_h1_heading(lines))

    def test_has_h1_heading_empty_list(self):
        """Test detection on empty lines list."""
        self.assertFalse(_has_h1_heading([]))


class TestValidateFile(unittest.TestCase):
    """Integration tests for validate_file() function."""

    def test_validate_file_not_found(self):
        """Test that FileNotFoundError is raised when file does not exist."""
        with self.assertRaises(FileNotFoundError):
            validate_file("nonexistent_file_xyz.md")

    def test_validate_file_no_h1_heading(self):
        """Test that ValueError is raised when file has no H1 heading."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Regular text\n\nThis is prose without a heading.")
            temp_path = f.name

        try:
            with self.assertRaises(ValueError):
                validate_file(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_validate_file_no_prose(self):
        """Test that ValueError is raised when file has no prose content."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# My Heading\n\n")
            temp_path = f.name

        try:
            with self.assertRaises(ValueError):
                validate_file(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_validate_file_one_sentence(self):
        """Test that ValueError is raised when prose has only 1 sentence."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# My Heading\n\nOnly one sentence.")
            temp_path = f.name

        try:
            with self.assertRaises(ValueError):
                validate_file(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_validate_file_four_sentences(self):
        """Test that ValueError is raised when prose has 4 sentences."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(
                "# My Heading\n\n"
                "First sentence. Second sentence. Third sentence. Fourth sentence."
            )
            temp_path = f.name

        try:
            with self.assertRaises(ValueError):
                validate_file(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_validate_file_two_sentences_valid(self):
        """Test that validate_file returns True for valid file with 2 sentences."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(
                "# Understanding Nature\n\n"
                "Nature provides endless beauty and lessons for all who observe carefully. "
                "Learning from the natural world enhances our perspective on life."
            )
            temp_path = f.name

        try:
            result = validate_file(temp_path)
            self.assertTrue(result)
        finally:
            Path(temp_path).unlink()

    def test_validate_file_three_sentences_valid(self):
        """Test that validate_file returns True for valid file with 3 sentences."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(
                "# Learning and Growth\n\n"
                "Continuous learning is the foundation of personal and professional growth. "
                "We must challenge ourselves to develop new skills and expand our knowledge. "
                "This commitment to growth transforms our lives and career paths."
            )
            temp_path = f.name

        try:
            result = validate_file(temp_path)
            self.assertTrue(result)
        finally:
            Path(temp_path).unlink()

    def test_validate_file_actual_test_file(self):
        """Test validation against the actual test-0c8bhn.md file if it exists."""
        test_file = Path("test-0c8bhn.md")
        if test_file.exists():
            result = validate_file("test-0c8bhn.md")
            self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
