#!/usr/bin/env python3
"""
Test suite for markdown file creation (test-9mxq6q.md).
Validates file existence, format, encoding, line endings, size, and prose quality.
"""

from pathlib import Path
import re


class TestMarkdownFileCreation:
    """Tests for test-9mxq6q.md markdown file."""

    MARKDOWN_FILE = Path("test-9mxq6q.md")
    MIN_SIZE = 320
    MAX_SIZE = 600
    MIN_WORD_COUNT = 40  # roughly 2-3 sentences
    MAX_WORD_COUNT = 160

    def test_file_exists(self):
        """File test-9mxq6q.md must exist at repository root."""
        assert self.MARKDOWN_FILE.exists(), f"File {self.MARKDOWN_FILE} does not exist"
        assert self.MARKDOWN_FILE.is_file(), f"{self.MARKDOWN_FILE} is not a file"

    def test_file_encoding_is_utf8_without_bom(self):
        """File must be UTF-8 encoded without BOM."""
        content_bytes = self.MARKDOWN_FILE.read_bytes()

        # Check for BOM (UTF-8 BOM is EF BB BF)
        assert not content_bytes.startswith(b'\xef\xbb\xbf'), "File has UTF-8 BOM, should not have one"

        # Verify UTF-8 decoding works without errors
        try:
            content_str = content_bytes.decode('utf-8')
        except UnicodeDecodeError as e:
            raise AssertionError(f"File is not valid UTF-8: {e}")

        return content_str

    def test_file_has_unix_line_endings(self):
        """File must use Unix line endings (LF: \n) only, no CRLF (\r\n)."""
        content_bytes = self.MARKDOWN_FILE.read_bytes()

        # Check for carriage returns (CRLF indicator)
        assert b'\r' not in content_bytes, "File contains CRLF line endings; must use LF only"

    def test_file_size_in_range(self):
        """File size must be between 320-600 bytes."""
        size = self.MARKDOWN_FILE.stat().st_size
        assert self.MIN_SIZE <= size <= self.MAX_SIZE, \
            f"File size {size} bytes is outside range [{self.MIN_SIZE}, {self.MAX_SIZE}]"

    def test_h1_heading_exists(self):
        """First non-empty line must be exactly one H1 heading starting with '# '."""
        content = self.MARKDOWN_FILE.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Find first non-empty line
        first_content_line = None
        for line in lines:
            if line.strip():
                first_content_line = line
                break

        assert first_content_line is not None, "File is empty or contains only whitespace"
        assert first_content_line.startswith('# '), \
            f"First line must start with '# ', got: {first_content_line}"

        return first_content_line

    def test_blank_line_after_heading(self):
        """Second line must be blank (separating heading from prose)."""
        content = self.MARKDOWN_FILE.read_text(encoding='utf-8')
        lines = content.split('\n')

        assert len(lines) >= 2, "File must have at least 2 lines (heading + blank line)"
        assert lines[1].strip() == '', \
            f"Second line must be blank, got: {repr(lines[1])}"

    def test_prose_content_exists(self):
        """File must contain prose content after heading and blank line."""
        content = self.MARKDOWN_FILE.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Prose starts after heading and blank line
        prose_lines = [l for l in lines[2:] if l.strip()]
        prose = '\n'.join(prose_lines).strip()

        assert prose, "No prose content found after heading"
        return prose

    def test_prose_is_2_to_3_sentences(self):
        """Prose must contain 2-3 sentences."""
        content = self.MARKDOWN_FILE.read_text(encoding='utf-8')
        lines = content.split('\n')
        prose_lines = [l for l in lines[2:] if l.strip()]
        prose = '\n'.join(prose_lines).strip()

        # Count sentences (ending with . ! or ?)
        sentences = re.split(r'[.!?]+', prose)
        sentence_count = len([s for s in sentences if s.strip()])

        assert 2 <= sentence_count <= 3, \
            f"Expected 2-3 sentences, found {sentence_count} in: {prose}"

    def test_prose_word_count_reasonable(self):
        """Prose should have reasonable word count for 2-3 sentences (40-160 words)."""
        content = self.MARKDOWN_FILE.read_text(encoding='utf-8')
        lines = content.split('\n')
        prose_lines = [l for l in lines[2:] if l.strip()]
        prose = '\n'.join(prose_lines).strip()

        words = prose.split()
        word_count = len(words)

        assert self.MIN_WORD_COUNT <= word_count <= self.MAX_WORD_COUNT, \
            f"Word count {word_count} is outside expected range [{self.MIN_WORD_COUNT}, {self.MAX_WORD_COUNT}]"

    def test_markdown_syntax_valid(self):
        """Markdown syntax must be valid and parseable."""
        content = self.MARKDOWN_FILE.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Check heading format (# followed by space)
        assert lines[0].startswith('# '), "H1 heading must be '# ' format"

        # Check that heading has text
        heading = lines[0][2:].strip()
        assert heading, "H1 heading must have text content"

        # Verify structure: heading, blank line, prose
        assert lines[1].strip() == '', "Second line must be blank"

        # Verify prose doesn't have markdown code blocks or invalid syntax
        prose_content = '\n'.join(lines[2:])
        assert not prose_content.startswith('#'), "Only one H1 heading allowed"

    def test_prose_quality_and_grammar(self):
        """Prose must be grammatically correct and coherent."""
        content = self.MARKDOWN_FILE.read_text(encoding='utf-8')
        lines = content.split('\n')
        prose_lines = [l for l in lines[2:] if l.strip()]
        prose = '\n'.join(prose_lines).strip()

        # Basic grammar checks:
        # - Should not have obvious grammar issues (multiple spaces, trailing spaces, etc.)
        assert '  ' not in prose, "Prose has multiple consecutive spaces"

        # - Should start with capital letter
        assert prose[0].isupper(), "Prose should start with capital letter"

        # - Should end with punctuation
        assert prose.rstrip()[-1] in '.!?', "Prose should end with . ! or ?"


def run_tests():
    """Run all tests and report results."""
    test = TestMarkdownFileCreation()
    tests = [
        ("File exists", test.test_file_exists),
        ("UTF-8 encoding without BOM", test.test_file_encoding_is_utf8_without_bom),
        ("Unix line endings (LF only)", test.test_file_has_unix_line_endings),
        ("File size 320-600 bytes", test.test_file_size_in_range),
        ("H1 heading exists", test.test_h1_heading_exists),
        ("Blank line after heading", test.test_blank_line_after_heading),
        ("Prose content exists", test.test_prose_content_exists),
        ("2-3 sentences", test.test_prose_is_2_to_3_sentences),
        ("Word count reasonable", test.test_prose_word_count_reasonable),
        ("Markdown syntax valid", test.test_markdown_syntax_valid),
        ("Prose quality and grammar", test.test_prose_quality_and_grammar),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            print(f"✓ {test_name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_name}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_name}: {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
