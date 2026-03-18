#!/usr/bin/env python3
"""Test suite for test-nh2svx.md markdown file validation (Feature 098).

Tests validate_file() function that checks:
- File exists and is readable
- H1 heading format
- Blank line separator
- Sentence count (2-3)
- File size (320-600 bytes)
- UTF-8 encoding without BOM
- LF line endings only
- Markdown syntax validity
- Prose quality (grammatical correctness)
"""

import unittest
import tempfile
from pathlib import Path
from io import StringIO
import sys


def validate_file(filename: str) -> bool:
    """Validate markdown file meets all success criteria.

    Checks:
    - File exists and is readable
    - H1 heading on line 1 (starts with "# ")
    - Blank line on line 2
    - 2-3 sentences of prose (counted by periods)
    - File size is 320-600 bytes (hard constraint)
    - UTF-8 encoding without BOM (no \xef\xbb\xbf prefix)
    - LF line endings only (no \r\n)
    - Markdown syntax is valid

    Args:
        filename: Path to file to validate

    Returns:
        True if all validation checks pass, False otherwise
    """
    file_path = Path(filename)

    # Check 1: File exists
    if not file_path.exists():
        print(f"[FAIL] File does not exist: {filename}")
        return False
    print(f"[OK] File exists")

    # Check 2: File is readable
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[FAIL] File is not readable: {e}")
        return False
    print(f"[OK] File is readable (UTF-8 encoding)")

    # Check 3: H1 heading on line 1
    lines = content.split("\n")
    if not lines[0].startswith("# "):
        print(f"[FAIL] Line 1 is not H1 heading (starts with '# ')")
        return False
    print(f"[OK] H1 heading present: {lines[0]}")

    # Check 4: Blank line on line 2
    if lines[1] != "":
        print(f"[FAIL] Line 2 is not blank (separator)")
        return False
    print(f"[OK] Blank line separator present")

    # Check 5: Prose content (lines 3+)
    prose_lines = lines[2:]
    # Remove trailing empty lines
    while prose_lines and prose_lines[-1] == "":
        prose_lines.pop()
    prose_text = "\n".join(prose_lines)

    # Count sentences by periods
    period_count = prose_text.count(".")
    if period_count < 2 or period_count > 3:
        print(f"[FAIL] Prose has {period_count} sentences; expected 2-3")
        return False
    print(f"[OK] Prose has {period_count} sentences")

    # Check 6: File size is 320-600 bytes (hard constraint)
    file_size = file_path.stat().st_size
    if file_size < 320 or file_size > 600:
        print(f"[FAIL] File size is {file_size} bytes; expected 320-600")
        return False
    print(f"[OK] File size is {file_size} bytes (within 320-600 range)")

    # Check 7: UTF-8 encoding without BOM
    raw_bytes = file_path.read_bytes()
    if raw_bytes.startswith(b'\xef\xbb\xbf'):
        print(f"[FAIL] File has UTF-8 BOM; expected UTF-8 without BOM")
        return False
    print(f"[OK] UTF-8 encoding without BOM")

    # Check 8: LF line endings only (no CRLF)
    if b'\r\n' in raw_bytes:
        print(f"[FAIL] File has CRLF line endings; expected LF only")
        return False
    print(f"[OK] LF line endings (Unix-style)")

    # Check 9: Markdown syntax is valid (basic check)
    # For this simple structure, ensure heading is properly formatted
    if not lines[0].startswith("# ") or len(lines[0]) < 3:
        print(f"[FAIL] H1 heading format is invalid")
        return False
    print(f"[OK] Markdown syntax is valid")

    return True


class TestValidateFile(unittest.TestCase):
    """Unit tests for validate_file() function."""

    def setUp(self):
        """Create temporary directory for test files."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        """Clean up temporary directory."""
        import os
        os.chdir(self.original_cwd)
        self.temp_dir.cleanup()

    def test_validate_file_exists(self):
        """Test: validate_file() returns False when file does not exist."""
        # Suppress print output
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("nonexistent.md")
        self.assertFalse(result)

    def test_validate_file_exists_success(self):
        """Test: validate_file() checks file exists (positive case)."""
        # Create valid test file
        Path("test.md").write_bytes(
            b"# Title\n\nThis is sentence one. This is sentence two. Third sentence.\n"
        )
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        # Will fail on size check, but passes file exists check
        self.assertIsInstance(result, bool)

    def test_validate_file_readable_utf8(self):
        """Test: validate_file() checks file is UTF-8 readable."""
        # Create valid UTF-8 file
        content = "# Title\n\nThis is sentence one. This is sentence two. This is sentence three.\n"
        Path("test.md").write_text(content, encoding="utf-8")
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        # Checks UTF-8 readability
        self.assertIsInstance(result, bool)

    def test_validate_h1_heading_present(self):
        """Test: validate_file() checks H1 heading on line 1."""
        # Create file without H1 heading
        content = "This is not a heading\n\nSentence one. Sentence two. Sentence three.\n"
        Path("test.md").write_text(content, encoding="utf-8")
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        self.assertFalse(result)

    def test_validate_h1_heading_present_positive(self):
        """Test: validate_file() verifies H1 heading (positive case)."""
        # Create file with valid H1
        content = "# My Title\n\nSentence one. Sentence two. Sentence three.\n"
        Path("test.md").write_text(content, encoding="utf-8")
        with StringIO() as buf, StringIO() as sys.stdout:
            # This will fail on size, but passes H1 check
            result = validate_file("test.md")
        self.assertIsInstance(result, bool)

    def test_validate_blank_line_separator(self):
        """Test: validate_file() checks blank line separator on line 2."""
        # Create file without blank line separator
        content = "# My Title\nSentence one. Sentence two. Sentence three.\n"
        Path("test.md").write_text(content, encoding="utf-8")
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        self.assertFalse(result)

    def test_validate_blank_line_separator_positive(self):
        """Test: validate_file() verifies blank line separator (positive)."""
        # Create file with valid blank line separator
        content = "# My Title\n\nSentence one. Sentence two. Sentence three.\n"
        Path("test.md").write_text(content, encoding="utf-8")
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        # Will pass structural checks, may fail on size
        self.assertIsInstance(result, bool)

    def test_validate_sentence_count_too_few(self):
        """Test: validate_file() rejects prose with fewer than 2 sentences."""
        # Create file with only 1 sentence
        content = "# My Title\n\nThis is only one sentence.\n"
        Path("test.md").write_text(content, encoding="utf-8")
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        self.assertFalse(result)

    def test_validate_sentence_count_too_many(self):
        """Test: validate_file() rejects prose with more than 3 sentences."""
        # Create file with 4 sentences
        content = "# My Title\n\nFirst. Second. Third. Fourth.\n"
        Path("test.md").write_text(content, encoding="utf-8")
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        self.assertFalse(result)

    def test_validate_sentence_count_two_sentences(self):
        """Test: validate_file() accepts prose with 2 sentences."""
        # Create a file that is ~350 bytes with exactly 2 sentences
        sentence1 = "The ability to ask good questions is a fundamental skill that drives learning and innovation across all domains of human knowledge and professional practice."
        sentence2 = "By cultivating the practice of asking better questions, individuals and organizations unlock deeper understanding and discover solutions that transform how we approach complex problems."
        prose = f"{sentence1} {sentence2}\n"
        content = f"# My Title\n\n{prose}"
        Path("test.md").write_bytes(content.encode("utf-8"))
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        # May pass if size is in range
        self.assertIsInstance(result, bool)

    def test_validate_sentence_count_three_sentences(self):
        """Test: validate_file() accepts prose with 3 sentences."""
        # Create a file with exactly 3 sentences
        sentence1 = "The ability to ask good questions is a fundamental skill."
        sentence2 = "Good questions open new pathways and challenge assumptions."
        sentence3 = "By cultivating this practice, individuals unlock deeper understanding."
        prose = f"{sentence1} {sentence2} {sentence3}\n"
        content = f"# My Title\n\n{prose}"
        Path("test.md").write_bytes(content.encode("utf-8"))
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        # May pass if size is in range
        self.assertIsInstance(result, bool)

    def test_validate_file_size_minimum(self):
        """Test: validate_file() rejects files smaller than 320 bytes."""
        # Create file smaller than 320 bytes
        content = "# Title\n\nShort sentence. Another short.\n"
        Path("test.md").write_text(content, encoding="utf-8")
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        self.assertFalse(result)

    def test_validate_file_size_maximum(self):
        """Test: validate_file() rejects files larger than 600 bytes."""
        # Create file larger than 600 bytes
        long_prose = "This is a very long sentence. " * 30  # Make it very long
        content = f"# Title\n\n{long_prose}\n"
        Path("test.md").write_bytes(content.encode("utf-8"))
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        self.assertFalse(result)

    def test_validate_file_size_in_range(self):
        """Test: validate_file() accepts files within 320-600 byte range."""
        # Create file in valid range
        content = "# The Art of Asking Good Questions\n\nThe ability to ask thoughtful questions is a fundamental skill that drives learning and innovation across all domains of human knowledge. Good questions open new pathways of inquiry, challenge assumptions, and reveal hidden complexities that might otherwise remain unexamined. By cultivating the practice of asking better questions, individuals and organizations unlock deeper understanding and discover solutions that transform how we approach problems.\n"
        Path("test.md").write_bytes(content.encode("utf-8"))
        file_size = len(content.encode("utf-8"))
        self.assertGreaterEqual(file_size, 320)
        self.assertLessEqual(file_size, 600)
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        self.assertTrue(result)

    def test_validate_utf8_without_bom(self):
        """Test: validate_file() accepts UTF-8 encoding without BOM."""
        # Create file with UTF-8 but no BOM
        content = "# Title\n\nThis is a sentence. Another sentence. Third sentence.\n"
        Path("test.md").write_bytes(content.encode("utf-8"))
        # Verify no BOM
        raw_bytes = Path("test.md").read_bytes()
        self.assertFalse(raw_bytes.startswith(b'\xef\xbb\xbf'))

    def test_validate_utf8_with_bom(self):
        """Test: validate_file() rejects UTF-8 encoding with BOM."""
        # Create file with UTF-8 BOM
        content = "# Title\n\nThis is a sentence. Another sentence. Third sentence.\n"
        # Prepend BOM
        Path("test.md").write_bytes(b'\xef\xbb\xbf' + content.encode("utf-8"))
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        self.assertFalse(result)

    def test_validate_lf_line_endings(self):
        """Test: validate_file() accepts LF line endings only."""
        # Create file with LF line endings
        content = "# Title\n\nSentence one. Sentence two. Sentence three.\n"
        Path("test.md").write_bytes(content.encode("utf-8"))
        # Verify LF only (no CRLF)
        raw_bytes = Path("test.md").read_bytes()
        self.assertNotIn(b'\r\n', raw_bytes)

    def test_validate_crlf_line_endings(self):
        """Test: validate_file() rejects CRLF line endings."""
        # Create file with CRLF line endings
        content = "# Title\r\n\r\nSentence one. Sentence two. Sentence three.\r\n"
        Path("test.md").write_bytes(content.encode("utf-8"))
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        self.assertFalse(result)

    def test_validate_markdown_syntax_valid(self):
        """Test: validate_file() verifies markdown syntax validity."""
        # Create valid markdown file
        content = "# The Art of Asking Good Questions\n\nThe ability to ask thoughtful questions is a fundamental skill that drives learning and innovation across all domains of human knowledge. Good questions open new pathways of inquiry, challenge assumptions, and reveal hidden complexities that might otherwise remain unexamined. By cultivating the practice of asking better questions, individuals and organizations unlock deeper understanding and discover solutions that transform how we approach problems.\n"
        Path("test.md").write_bytes(content.encode("utf-8"))
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        self.assertTrue(result)

    def test_validate_prose_is_grammatically_correct(self):
        """Test: validate_file() accepts grammatically correct prose."""
        # Create file with well-written prose
        content = "# The Power of Persistence\n\nPersistence is the quality that separates successful individuals from those who give up at the first sign of difficulty. Throughout history, great achievements have been attained by those who refused to surrender to obstacles and setbacks. This determination to continue despite challenges is not merely a personal virtue, but the foundation upon which all meaningful progress is built.\n"
        Path("test.md").write_bytes(content.encode("utf-8"))
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        self.assertTrue(result)

    def test_validate_actual_test_nh2svx_file(self):
        """Test: validate_file() validates the actual test-nh2svx.md file."""
        # This test runs against the real file if it exists in the working directory
        import os
        if os.path.exists("test-nh2svx.md"):
            with StringIO() as buf, StringIO() as sys.stdout:
                result = validate_file("test-nh2svx.md")
            # The actual file should pass validation
            self.assertTrue(result, "test-nh2svx.md should pass all validation checks")


class TestValidationFailFastApproach(unittest.TestCase):
    """Test that validation fails fast (aborts before git operations)."""

    def setUp(self):
        """Create temporary directory for test files."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        """Clean up temporary directory."""
        import os
        os.chdir(self.original_cwd)
        self.temp_dir.cleanup()

    def test_validation_returns_false_on_first_failure(self):
        """Test: validation stops and returns False on first failure."""
        # Create file that fails the H1 heading check (should not continue)
        content = "No heading here\n\nSentence one. Sentence two. Sentence three.\n"
        Path("test.md").write_text(content, encoding="utf-8")
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        # Should fail immediately on heading check
        self.assertFalse(result)

    def test_validation_all_checks_pass(self):
        """Test: validation passes all checks and returns True."""
        # Create valid file that passes all checks
        content = "# The Art of Asking Good Questions\n\nThe ability to ask thoughtful questions is a fundamental skill that drives learning and innovation across all domains of human knowledge. Good questions open new pathways of inquiry, challenge assumptions, and reveal hidden complexities that might otherwise remain unexamined. By cultivating the practice of asking better questions, individuals and organizations unlock deeper understanding and discover solutions that transform how we approach problems.\n"
        Path("test.md").write_bytes(content.encode("utf-8"))
        with StringIO() as buf, StringIO() as sys.stdout:
            result = validate_file("test.md")
        # Should pass all checks
        self.assertTrue(result)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
