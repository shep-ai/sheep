#!/usr/bin/env python3
"""Test suite for Phase 4: File Validation of feature 126.

This module tests file encoding, line endings, size, and content structure validation
for the markdown file test-lqbnqn.md. Tests are organized by task:

- Task 4-1: Validate file encoding (UTF-8, no BOM) and line endings (LF only)
- Task 4-2: Validate file size (400-600 bytes) and content structure (heading, blank line, prose)
"""

import unittest
import tempfile
from pathlib import Path
import sys

# Add parent directory to path so we can import validation module
sys.path.insert(0, str(Path(__file__).parent.parent))

from validate_markdown import (
    ValidationError,
    validate_encoding,
    validate_line_endings,
    validate_structure,
    validate_file_size,
)


class TestFileEncodingValidation(unittest.TestCase):
    """Task 4-1: Test file encoding validation (UTF-8, no BOM)."""

    def test_validate_encoding_with_valid_utf8_file(self):
        """Test that validate_encoding accepts valid UTF-8 file."""
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n', delete=False
        ) as f:
            f.write('# Test\n\nSample prose.')
            temp_path = Path(f.name)

        try:
            # Should not raise any exception
            validate_encoding(temp_path)
        finally:
            temp_path.unlink()

    def test_validate_encoding_rejects_invalid_utf8(self):
        """Test that validate_encoding raises exception for non-UTF-8 file."""
        with tempfile.NamedTemporaryFile(
            mode='wb', delete=False
        ) as f:
            # Write invalid UTF-8 sequence
            f.write(b'\xff\xfe')
            temp_path = Path(f.name)

        try:
            with self.assertRaises(ValidationError) as ctx:
                validate_encoding(temp_path)
            self.assertIn('not valid UTF-8', str(ctx.exception))
        finally:
            temp_path.unlink()

    def test_validate_encoding_rejects_file_with_bom(self):
        """Test that validate_encoding raises exception for file with UTF-8 BOM."""
        with tempfile.NamedTemporaryFile(
            mode='wb', delete=False
        ) as f:
            # UTF-8 BOM is EF BB BF
            f.write(b'\xef\xbb\xbf# Title\n\nContent.')
            temp_path = Path(f.name)

        try:
            with self.assertRaises(ValidationError) as ctx:
                validate_encoding(temp_path)
            self.assertIn('BOM', str(ctx.exception))
        finally:
            temp_path.unlink()

    def test_validate_encoding_accepts_utf8_without_bom(self):
        """Test that validate_encoding accepts UTF-8 without BOM."""
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n', delete=False
        ) as f:
            # Explicit UTF-8 without BOM
            f.write('# Title\n\nSample content with no BOM.')
            temp_path = Path(f.name)

        try:
            validate_encoding(temp_path)
        finally:
            temp_path.unlink()


class TestLineEndingValidation(unittest.TestCase):
    """Task 4-1: Test line ending validation (LF only, no CRLF/CR)."""

    def test_validate_line_endings_with_lf_only(self):
        """Test that validate_line_endings accepts LF-only file."""
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n', delete=False
        ) as f:
            f.write('# Title\n\nLine 1.\nLine 2.')
            temp_path = Path(f.name)

        try:
            validate_line_endings(temp_path)
        finally:
            temp_path.unlink()

    def test_validate_line_endings_rejects_crlf(self):
        """Test that validate_line_endings raises exception for CRLF line endings."""
        with tempfile.NamedTemporaryFile(
            mode='wb', delete=False
        ) as f:
            f.write(b'# Title\r\n\r\nContent.')
            temp_path = Path(f.name)

        try:
            with self.assertRaises(ValidationError) as ctx:
                validate_line_endings(temp_path)
            self.assertIn('CRLF', str(ctx.exception))
        finally:
            temp_path.unlink()

    def test_validate_line_endings_rejects_cr_only(self):
        """Test that validate_line_endings raises exception for CR-only line endings."""
        with tempfile.NamedTemporaryFile(
            mode='wb', delete=False
        ) as f:
            f.write(b'# Title\r\rContent.')
            temp_path = Path(f.name)

        try:
            with self.assertRaises(ValidationError):
                validate_line_endings(temp_path)
        finally:
            temp_path.unlink()

    def test_validate_line_endings_detects_crlf_in_multiline(self):
        """Test that CRLF is detected even in multiline files."""
        with tempfile.NamedTemporaryFile(
            mode='wb', delete=False
        ) as f:
            f.write(b'# Title\n\nFirst line\r\nSecond line')
            temp_path = Path(f.name)

        try:
            with self.assertRaises(ValidationError) as ctx:
                validate_line_endings(temp_path)
            self.assertIn('CRLF', str(ctx.exception))
        finally:
            temp_path.unlink()


class TestFileSizeValidation(unittest.TestCase):
    """Task 4-2: Test file size validation (400-600 bytes)."""

    def test_validate_file_size_with_valid_size(self):
        """Test that validate_file_size accepts files in 400-600 byte range."""
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n', delete=False
        ) as f:
            # Create file that's approximately 450 bytes
            f.write('# The Art of Fermentation\n\n')
            f.write('Fermentation is a centuries-old technique that has been used ')
            f.write('to preserve food while enhancing its flavor and nutritional value. ')
            f.write('From sauerkraut to kombucha, fermented foods play a crucial role ')
            f.write('in cuisines around the world. This ancient process demonstrates ')
            f.write('how microorganisms can transform simple ingredients into complex, ')
            f.write('delicious dishes. Throughout history, fermented beverages and foods ')
            f.write('have provided essential nutrients and probiotics.')
            temp_path = Path(f.name)

        try:
            file_size = len(temp_path.read_bytes())
            self.assertGreaterEqual(file_size, 400)
            self.assertLessEqual(file_size, 600)
            validate_file_size(temp_path)
        finally:
            temp_path.unlink()

    def test_validate_file_size_rejects_file_below_400_bytes(self):
        """Test that validate_file_size raises exception for file < 400 bytes."""
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n', delete=False
        ) as f:
            # Create small file (less than 400 bytes)
            f.write('# Title\n\nShort prose.')
            temp_path = Path(f.name)

        try:
            file_size = len(temp_path.read_bytes())
            self.assertLess(file_size, 400)
            with self.assertRaises(ValidationError) as ctx:
                validate_file_size(temp_path)
            self.assertIn('outside acceptable range', str(ctx.exception))
        finally:
            temp_path.unlink()

    def test_validate_file_size_rejects_file_above_600_bytes(self):
        """Test that validate_file_size raises exception for file > 600 bytes."""
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n', delete=False
        ) as f:
            # Create large file (more than 600 bytes)
            f.write('# Title\n\n')
            f.write('A' * 700)
            temp_path = Path(f.name)

        try:
            file_size = len(temp_path.read_bytes())
            self.assertGreater(file_size, 600)
            with self.assertRaises(ValidationError) as ctx:
                validate_file_size(temp_path)
            self.assertIn('outside acceptable range', str(ctx.exception))
        finally:
            temp_path.unlink()

    def test_validate_file_size_minimum_boundary(self):
        """Test validate_file_size at minimum boundary (400 bytes)."""
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n', delete=False
        ) as f:
            # Create file that's exactly around 400 bytes by padding
            content = 'X' * 350  # Adjust to get close to 400 with the heading
            f.write(f'# Title\n\n{content}')
            temp_path = Path(f.name)

        try:
            # Just verify it doesn't raise for file near lower boundary
            validate_file_size(temp_path)
        finally:
            temp_path.unlink()

    def test_validate_file_size_maximum_boundary(self):
        """Test validate_file_size at maximum boundary (600 bytes)."""
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n', delete=False
        ) as f:
            # Create file that's exactly around 600 bytes
            content = 'X' * 550  # Adjust to get close to 600 with the heading
            f.write(f'# Title\n\n{content}')
            temp_path = Path(f.name)

        try:
            validate_file_size(temp_path)
        finally:
            temp_path.unlink()


class TestContentStructureValidation(unittest.TestCase):
    """Task 4-2: Test content structure validation (heading, blank line, prose)."""

    def test_validate_structure_with_valid_format(self):
        """Test that validate_structure accepts properly formatted file."""
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n', delete=False
        ) as f:
            f.write('# Test Title\n\nThis is prose content. More sentences here.')
            temp_path = Path(f.name)

        try:
            validate_structure(temp_path)
        finally:
            temp_path.unlink()

    def test_validate_structure_requires_h1_heading(self):
        """Test that validate_structure requires H1 heading on first line."""
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n', delete=False
        ) as f:
            f.write('## Not H1\n\nContent here.')
            temp_path = Path(f.name)

        try:
            with self.assertRaises(ValidationError) as ctx:
                validate_structure(temp_path)
            self.assertIn('# ', str(ctx.exception))
        finally:
            temp_path.unlink()

    def test_validate_structure_rejects_missing_heading(self):
        """Test that validate_structure rejects file without heading."""
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n', delete=False
        ) as f:
            f.write('No heading here\n\nJust content.')
            temp_path = Path(f.name)

        try:
            with self.assertRaises(ValidationError):
                validate_structure(temp_path)
        finally:
            temp_path.unlink()

    def test_validate_structure_requires_blank_line_after_heading(self):
        """Test that validate_structure requires blank line after heading."""
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n', delete=False
        ) as f:
            f.write('# Title\nNo blank line before prose.')
            temp_path = Path(f.name)

        try:
            with self.assertRaises(ValidationError) as ctx:
                validate_structure(temp_path)
            self.assertIn('blank', str(ctx.exception))
        finally:
            temp_path.unlink()

    def test_validate_structure_requires_prose_content(self):
        """Test that validate_structure requires prose content after blank line."""
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n', delete=False
        ) as f:
            f.write('# Title\n\n')  # No prose after blank line
            temp_path = Path(f.name)

        try:
            with self.assertRaises(ValidationError) as ctx:
                validate_structure(temp_path)
            self.assertIn('prose', str(ctx.exception).lower())
        finally:
            temp_path.unlink()

    def test_validate_structure_with_multiline_prose(self):
        """Test that validate_structure accepts multiline prose."""
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n', delete=False
        ) as f:
            f.write('# Title\n\nFirst paragraph. Second sentence.\n\nThird sentence.')
            temp_path = Path(f.name)

        try:
            validate_structure(temp_path)
        finally:
            temp_path.unlink()


class TestActualTestFile(unittest.TestCase):
    """Test the actual test-lqbnqn.md file created for feature 126."""

    @classmethod
    def setUpClass(cls):
        """Set up test file path."""
        # File is in repo root, not in tests directory
        cls.file_path = Path(__file__).parent.parent / 'test-lqbnqn.md'

    def test_file_exists(self):
        """Test that test-lqbnqn.md exists."""
        self.assertTrue(self.file_path.exists(), 'test-lqbnqn.md must exist')

    def test_encoding_is_utf8_without_bom(self):
        """Test that test-lqbnqn.md uses UTF-8 without BOM."""
        validate_encoding(self.file_path)

    def test_line_endings_are_lf_only(self):
        """Test that test-lqbnqn.md uses LF line endings only."""
        validate_line_endings(self.file_path)

    def test_file_size_in_range(self):
        """Test that test-lqbnqn.md is 400-600 bytes."""
        validate_file_size(self.file_path)

    def test_structure_is_valid(self):
        """Test that test-lqbnqn.md has valid structure."""
        validate_structure(self.file_path)

    def test_all_validations_pass(self):
        """Test that all validations pass for test-lqbnqn.md."""
        # Should not raise any exception
        validate_encoding(self.file_path)
        validate_line_endings(self.file_path)
        validate_structure(self.file_path)
        validate_file_size(self.file_path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
