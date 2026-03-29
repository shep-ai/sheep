#!/usr/bin/env python3
"""
Test suite for feature 261: markdown-file-creation-91527e
Tests file creation, encoding, line endings, and content structure.
"""

import pathlib
import re


def test_file_exists():
    """Test that test-m6or7y.md file exists in repository root."""
    file_path = pathlib.Path("test-m6or7y.md")
    assert file_path.exists(), "File test-m6or7y.md does not exist in repository root"
    assert file_path.is_file(), "test-m6or7y.md is not a regular file"


def test_file_encoding():
    """Test that file is encoded in UTF-8 without BOM."""
    file_path = pathlib.Path("test-m6or7y.md")
    content = file_path.read_bytes()

    # Check for UTF-8 BOM (EF BB BF in hex)
    assert not content.startswith(b'\xef\xbb\xbf'), "File contains UTF-8 BOM"

    # Verify content can be decoded as UTF-8
    try:
        file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise AssertionError("File is not valid UTF-8 encoded")


def test_line_endings():
    """Test that file uses Unix LF line endings, not CRLF."""
    file_path = pathlib.Path("test-m6or7y.md")
    content = file_path.read_bytes()

    # Check for CRLF (Windows line endings)
    assert b'\r\n' not in content, "File contains CRLF line endings (Windows format), should use LF (Unix format)"

    # Verify it uses LF
    assert b'\n' in content, "File does not contain any line endings"


def test_h1_heading_present():
    """Test that file contains exactly one H1 heading."""
    file_path = pathlib.Path("test-m6or7y.md")
    content = file_path.read_text(encoding="utf-8")

    # Count H1 headings (lines starting with "# ")
    h1_count = len([line for line in content.split('\n') if line.startswith('# ')])
    assert h1_count == 1, f"Expected exactly 1 H1 heading, found {h1_count}"


def test_h1_heading_format():
    """Test that H1 heading uses correct markdown format (# Title)."""
    file_path = pathlib.Path("test-m6or7y.md")
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')

    assert lines[0].startswith('# '), "First line should start with '# ' (H1 heading)"
    assert len(lines[0]) > 2, "H1 heading should have title text after '# '"


def test_h1_heading_is_descriptive():
    """Test that H1 heading title is descriptive (not generic)."""
    file_path = pathlib.Path("test-m6or7y.md")
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')

    title = lines[0][2:].strip()  # Remove "# " prefix

    # Should not be trivially generic
    generic_titles = {"test", "content", "title", "file", "test file", "markdown"}
    assert title.lower() not in generic_titles, f"Title '{title}' is too generic, should be descriptive"
    assert len(title) >= 3, f"Title '{title}' is too short to be descriptive"


def test_blank_line_after_heading():
    """Test that H1 heading is followed by a blank line."""
    file_path = pathlib.Path("test-m6or7y.md")
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')

    assert len(lines) >= 2, "File is too short (missing content)"
    assert lines[1] == '', "Second line should be blank (after H1 heading)"


def test_prose_sentence_count():
    """Test that file contains exactly 2-3 sentences of prose."""
    file_path = pathlib.Path("test-m6or7y.md")
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')

    # Prose starts at line 2 (after heading and blank line)
    prose_lines = [line for line in lines[2:] if line.strip()]
    prose = ' '.join(prose_lines).strip()

    # Count sentences (ending with . ! ?)
    sentences = [s.strip() for s in re.split(r'[.!?]+', prose) if s.strip()]

    assert 2 <= len(sentences) <= 3, f"Expected 2-3 sentences, found {len(sentences)}"


def test_prose_grammar():
    """Test that prose content is grammatically correct (basic checks)."""
    file_path = pathlib.Path("test-m6or7y.md")
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')

    # Prose starts at line 2
    prose_lines = [line for line in lines[2:] if line.strip()]
    prose = ' '.join(prose_lines).strip()

    # Basic grammar checks
    # 1. Sentences should start with capital letter
    sentences = [s.strip() for s in re.split(r'[.!?]+', prose) if s.strip()]
    for i, sentence in enumerate(sentences):
        if sentence:
            first_char = sentence[0]
            assert first_char.isupper(), f"Sentence {i+1} should start with capital letter: '{sentence[:20]}...'"

    # 2. Prose should not have excessive spaces or formatting errors
    assert '  ' not in prose, "Prose contains double spaces"


def test_prose_coherence():
    """Test that prose content is coherent and intelligible."""
    file_path = pathlib.Path("test-m6or7y.md")
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')

    prose_lines = [line for line in lines[2:] if line.strip()]
    prose = ' '.join(prose_lines).strip()

    # Prose should be reasonably long and meaningful
    words = prose.split()
    assert len(words) >= 20, f"Prose is too short to be coherent ({len(words)} words)"

    # Should have reasonable average word length (not all single chars or gibberish)
    avg_word_len = sum(len(w) for w in words) / len(words)
    assert avg_word_len >= 3, f"Average word length {avg_word_len:.1f} suggests non-coherent content"


def test_file_size():
    """Test that file size is approximately 350-550 bytes (typical for this pattern)."""
    file_path = pathlib.Path("test-m6or7y.md")
    size = file_path.stat().st_size

    assert 300 <= size <= 650, f"File size {size} bytes is outside typical range (350-550)"


def test_trailing_newline():
    """Test that file ends with a newline character."""
    file_path = pathlib.Path("test-m6or7y.md")
    content = file_path.read_bytes()

    assert content.endswith(b'\n'), "File should end with a newline character"


def test_commonmark_validity():
    """Test that content is valid CommonMark markdown."""
    file_path = pathlib.Path("test-m6or7y.md")
    content = file_path.read_text(encoding="utf-8")

    # Basic CommonMark validation (more thorough checks)
    # 1. No unmatched brackets or code blocks
    assert content.count('[') >= content.count(']') - 1, "Unmatched closing brackets"

    # 2. No unclosed code fences (if any)
    if '```' in content or '~~~' in content:
        backtick_count = content.count('```')
        tilde_count = content.count('~~~')
        assert backtick_count % 2 == 0, "Unmatched backtick code fences"
        assert tilde_count % 2 == 0, "Unmatched tilde code fences"


if __name__ == "__main__":
    # Run all tests
    test_file_exists()
    print("[PASS] File exists")

    test_file_encoding()
    print("[PASS] File encoding is UTF-8 without BOM")

    test_line_endings()
    print("[PASS] File uses Unix LF line endings")

    test_h1_heading_present()
    print("[PASS] File contains exactly one H1 heading")

    test_h1_heading_format()
    print("[PASS] H1 heading uses correct format")

    test_h1_heading_is_descriptive()
    print("[PASS] H1 heading is descriptive")

    test_blank_line_after_heading()
    print("[PASS] Blank line follows H1 heading")

    test_prose_sentence_count()
    print("[PASS] Prose contains 2-3 sentences")

    test_prose_grammar()
    print("[PASS] Prose is grammatically correct")

    test_prose_coherence()
    print("[PASS] Prose is coherent and intelligible")

    test_file_size()
    print("[PASS] File size is within typical range")

    test_trailing_newline()
    print("[PASS] File ends with newline")

    test_commonmark_validity()
    print("[PASS] Content is valid CommonMark markdown")

    print("\n[OK] All tests passed!")
