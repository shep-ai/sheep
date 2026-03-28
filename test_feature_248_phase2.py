"""
Test suite for feature 248 Phase 2: Validation & Verification

Tests for validating the created markdown file test-2oiio6.md to verify:
- File exists at correct path
- File has correct structure (H1 heading, blank line, 2-3 sentences)
- File has correct encoding (UTF-8 without BOM)
- File has correct line endings (Unix LF, not CRLF)
"""

import unittest
from pathlib import Path


def validate_markdown(filename: str) -> dict:
    """
    Validate markdown file structure and encoding.

    Checks:
    - File exists
    - First line is H1 heading (starts with '# ')
    - Second line is blank
    - Prose contains exactly 2-3 sentences
    - File is UTF-8 encoded without BOM
    - File uses Unix LF line endings

    Args:
        filename: Path to markdown file to validate

    Returns:
        Dictionary with validation results:
        {
            'exists': bool,
            'has_h1': bool,
            'has_blank_line': bool,
            'sentence_count': int,
            'has_utf8_encoding': bool,
            'has_no_bom': bool,
            'has_lf_endings': bool,
            'valid': bool
        }
    """
    path = Path(filename)
    result = {
        'exists': False,
        'has_h1': False,
        'has_blank_line': False,
        'sentence_count': 0,
        'has_utf8_encoding': False,
        'has_no_bom': False,
        'has_lf_endings': False,
        'valid': False,
    }

    # Check if file exists
    if not path.exists():
        return result

    result['exists'] = True

    # Check UTF-8 encoding
    try:
        content = path.read_text(encoding='utf-8')
        result['has_utf8_encoding'] = True
    except UnicodeDecodeError:
        return result

    # Check for UTF-8 BOM
    binary_content = path.read_bytes()
    has_no_bom = not binary_content.startswith(b'\xef\xbb\xbf')
    result['has_no_bom'] = has_no_bom

    # Check for LF line endings (no CRLF)
    has_lf_endings = b'\r\n' not in binary_content and b'\n' in binary_content
    result['has_lf_endings'] = has_lf_endings

    # Check file structure
    lines = content.split('\n')

    # Check for H1 heading on first line
    if len(lines) > 0 and lines[0].startswith('# '):
        result['has_h1'] = True

    # Check for blank line on second line
    if len(lines) > 1 and lines[1] == '':
        result['has_blank_line'] = True

    # Count sentences in prose (lines 2+)
    if len(lines) > 2:
        prose = '\n'.join(lines[2:]).strip()
        if prose:
            # Count sentences by splitting on periods
            sentences = [s.strip() for s in prose.split('.') if s.strip()]
            sentence_count = len(sentences)
            result['sentence_count'] = sentence_count

    # Validation is complete when all checks pass
    result['valid'] = (
        result['exists'] and
        result['has_h1'] and
        result['has_blank_line'] and
        2 <= result['sentence_count'] <= 3 and
        result['has_utf8_encoding'] and
        result['has_no_bom'] and
        result['has_lf_endings']
    )

    return result


class TestValidationFunction(unittest.TestCase):
    """Tests for the validate_markdown function"""

    def test_validation_returns_dictionary_with_required_keys(self):
        """Assert validation function returns dictionary with required keys."""
        result = validate_markdown('test-2oiio6.md')

        expected_keys = {
            'exists', 'has_h1', 'has_blank_line', 'sentence_count',
            'has_utf8_encoding', 'has_no_bom', 'has_lf_endings', 'valid'
        }
        self.assertEqual(set(result.keys()), expected_keys)

    def test_validation_returns_valid_true_for_correct_file(self):
        """Assert validation returns valid=True for correctly formatted file."""
        result = validate_markdown('test-2oiio6.md')

        # File should exist
        self.assertTrue(result['exists'], "File should exist")

        # All validation checks should pass
        self.assertTrue(result['has_h1'], "File should have H1 heading")
        self.assertTrue(result['has_blank_line'], "File should have blank line separator")
        self.assertIn(result['sentence_count'], [2, 3], "File should have 2-3 sentences")
        self.assertTrue(result['has_utf8_encoding'], "File should be UTF-8 encoded")
        self.assertTrue(result['has_no_bom'], "File should not have UTF-8 BOM")
        self.assertTrue(result['has_lf_endings'], "File should use LF line endings")

        # Overall validation should pass
        self.assertTrue(result['valid'], "File should pass validation")

    def test_validation_sentence_count_in_valid_range(self):
        """Assert sentence count is 2 or 3."""
        result = validate_markdown('test-2oiio6.md')

        self.assertGreaterEqual(result['sentence_count'], 2, "File should have at least 2 sentences")
        self.assertLessEqual(result['sentence_count'], 3, "File should have at most 3 sentences")


class TestValidationReportsStructureIssues(unittest.TestCase):
    """Tests for validation detecting structure problems"""

    def test_validation_detects_missing_file(self):
        """Assert validation detects when file doesn't exist."""
        result = validate_markdown('nonexistent-file.md')

        self.assertFalse(result['exists'])
        self.assertFalse(result['valid'])

    def test_validation_detects_missing_h1_heading(self):
        """Assert validation detects missing H1 heading."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-bad.md"
            # Create file without H1 heading
            filepath.write_text("No heading\n\nJust prose here.", encoding='utf-8', newline='\n')

            result = validate_markdown(str(filepath))

            self.assertTrue(result['exists'])
            self.assertFalse(result['has_h1'])
            self.assertFalse(result['valid'])

    def test_validation_detects_missing_blank_line(self):
        """Assert validation detects missing blank line separator."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-bad.md"
            # Create file without blank line after heading
            filepath.write_text("# Heading\nJust prose here.", encoding='utf-8', newline='\n')

            result = validate_markdown(str(filepath))

            self.assertTrue(result['exists'])
            self.assertTrue(result['has_h1'])
            self.assertFalse(result['has_blank_line'])
            self.assertFalse(result['valid'])

    def test_validation_detects_wrong_sentence_count(self):
        """Assert validation detects when sentence count is not 2-3."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-bad.md"
            # Create file with only 1 sentence
            filepath.write_text("# Heading\n\nOnly one sentence.", encoding='utf-8', newline='\n')

            result = validate_markdown(str(filepath))

            self.assertTrue(result['exists'])
            self.assertEqual(result['sentence_count'], 1)
            self.assertFalse(result['valid'])


class TestValidationReportsEncodingIssues(unittest.TestCase):
    """Tests for validation detecting encoding problems"""

    def test_validation_detects_crlf_line_endings(self):
        """Assert validation detects CRLF line endings."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-bad.md"
            # Create file with CRLF line endings
            filepath.write_bytes(b"# Heading\r\n\r\nProses here. Another sentence. Third sentence.")

            result = validate_markdown(str(filepath))

            self.assertTrue(result['exists'])
            self.assertFalse(result['has_lf_endings'], "File should not use CRLF")
            self.assertFalse(result['valid'])

    def test_validation_detects_utf8_bom(self):
        """Assert validation detects UTF-8 BOM."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test-bad.md"
            # Create file with UTF-8 BOM
            content = "# Heading\n\nSome prose here. Another sentence. Third one."
            filepath.write_bytes(b'\xef\xbb\xbf' + content.encode('utf-8'))

            result = validate_markdown(str(filepath))

            self.assertTrue(result['exists'])
            self.assertFalse(result['has_no_bom'], "File should not have BOM")
            self.assertFalse(result['valid'])


class TestValidationOutputFormat(unittest.TestCase):
    """Tests for validation output format and accuracy"""

    def test_validation_output_has_correct_types(self):
        """Assert validation output has correct value types."""
        result = validate_markdown('test-2oiio6.md')

        # Boolean values
        self.assertIsInstance(result['exists'], bool)
        self.assertIsInstance(result['has_h1'], bool)
        self.assertIsInstance(result['has_blank_line'], bool)
        self.assertIsInstance(result['has_utf8_encoding'], bool)
        self.assertIsInstance(result['has_no_bom'], bool)
        self.assertIsInstance(result['has_lf_endings'], bool)
        self.assertIsInstance(result['valid'], bool)

        # Integer value
        self.assertIsInstance(result['sentence_count'], int)

    def test_validation_sentence_count_is_accurate(self):
        """Assert sentence count is accurately counted."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            # Test with exactly 2 sentences
            filepath = Path(tmpdir) / "test-2sent.md"
            filepath.write_text("# Heading\n\nFirst sentence. Second sentence.", encoding='utf-8', newline='\n')
            result = validate_markdown(str(filepath))
            self.assertEqual(result['sentence_count'], 2)

            # Test with exactly 3 sentences
            filepath = Path(tmpdir) / "test-3sent.md"
            filepath.write_text("# Heading\n\nFirst sentence. Second sentence. Third sentence.", encoding='utf-8', newline='\n')
            result = validate_markdown(str(filepath))
            self.assertEqual(result['sentence_count'], 3)


if __name__ == "__main__":
    unittest.main()
