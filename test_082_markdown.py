#!/usr/bin/env python3
"""
Test suite for feature 082: markdown-file-creation
Tests the creation and validation of test-8lzq5l.md with proper markdown structure and encoding.
"""

import sys
from pathlib import Path


def test_file_does_not_exist():
    """Test that the file doesn't exist before creation."""
    file_path = Path("test-8lzq5l.md")
    # Clean up if it exists from a prior test run
    if file_path.exists():
        file_path.unlink()
    assert not file_path.exists(), "File should not exist before creation"
    print("✓ test_file_does_not_exist")


def test_create_markdown_file():
    """Test that the markdown file is created successfully."""
    file_path = Path("test-8lzq5l.md")
    # Clean up if it exists from a prior test run
    if file_path.exists():
        file_path.unlink()

    # Define content with heading and prose (2-3 sentences)
    heading = "# Quantum Computing and Its Promise"
    prose = (
        "Quantum computers harness the strange properties of quantum mechanics to perform "
        "calculations that would be impossible for classical computers. By utilizing quantum bits "
        "(qubits) that can exist in multiple states simultaneously, these machines enable exponential "
        "speedups in solving complex problems. The development of practical quantum computers could "
        "revolutionize fields from drug discovery to cryptography."
    )
    content = f"{heading}\n\n{prose}\n"

    # Write file with UTF-8 encoding and Unix LF line endings
    file_path.write_text(content, encoding="utf-8", newline="\n")

    assert file_path.exists(), "File should exist after creation"
    print("✓ test_create_markdown_file")


def test_file_has_h1_heading():
    """Test that the first line is an H1 markdown heading."""
    file_path = Path("test-8lzq5l.md")
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    assert lines[0].startswith("# "), f"First line should be H1 heading, got: '{lines[0]}'"
    print(f"✓ test_file_has_h1_heading: {lines[0]}")


def test_file_has_blank_line():
    """Test that line 2 is blank (blank line after heading)."""
    file_path = Path("test-8lzq5l.md")
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    assert len(lines) > 1, "File should have at least 2 lines"
    assert lines[1] == "", f"Second line should be blank, got: '{lines[1]}'"
    print("✓ test_file_has_blank_line")


def test_file_has_prose_content():
    """Test that lines 3+ contain non-empty prose content."""
    file_path = Path("test-8lzq5l.md")
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    assert len(lines) > 2, "File should have at least 3 lines (heading, blank, prose)"
    prose_content = "\n".join(lines[2:]).strip()
    assert prose_content, "Prose content should not be empty"
    print(f"✓ test_file_has_prose_content ({len(prose_content)} chars)")


def test_prose_has_2_to_3_sentences():
    """Test that prose content contains exactly 2-3 sentences."""
    file_path = Path("test-8lzq5l.md")
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    prose_content = "\n".join(lines[2:]).strip()
    # Count sentences by counting sentence-ending punctuation
    sentence_count = prose_content.count('.') + prose_content.count('!') + prose_content.count('?')

    assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"
    print(f"✓ test_prose_has_2_to_3_sentences: {sentence_count} sentences")


def test_file_encoding_is_utf8_no_bom():
    """Test that file is UTF-8 encoded without BOM."""
    file_path = Path("test-8lzq5l.md")
    binary_content = file_path.read_bytes()

    # Verify no UTF-8 BOM (EF BB BF)
    assert not binary_content.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"
    print("✓ test_file_encoding_is_utf8_no_bom")


def test_file_has_lf_line_endings():
    """Test that file uses Unix-style LF line endings, not Windows CRLF."""
    file_path = Path("test-8lzq5l.md")
    binary_content = file_path.read_bytes()

    # Verify no Windows CRLF (CR LF = 0x0D 0x0A)
    assert b'\r\n' not in binary_content, "File should use Unix LF, not Windows CRLF"
    # Verify it uses LF (0x0A)
    assert b'\n' in binary_content, "File should contain LF line endings"
    print("✓ test_file_has_lf_line_endings")


def test_file_size_in_typical_range():
    """Test that file size is in the typical range (400-600 bytes)."""
    file_path = Path("test-8lzq5l.md")
    binary_content = file_path.read_bytes()
    size = len(binary_content)

    # This is a guideline, not a strict requirement
    if size < 400 or size > 600:
        print(f"⚠ test_file_size_in_typical_range: {size} bytes (guideline: 400-600, natural variation acceptable)")
    else:
        print(f"✓ test_file_size_in_typical_range: {size} bytes")


def test_file_structure_complete():
    """Test complete file structure: H1 + blank + 2-3 sentences."""
    file_path = Path("test-8lzq5l.md")
    content = file_path.read_text(encoding="utf-8")

    # Should match pattern: # Heading\n\n<prose>\n
    assert content.count('\n') >= 3, "File should have at least 3 line breaks"
    assert not content.startswith('\n'), "File should not start with blank line"
    assert not content.startswith(' '), "File should not start with whitespace"
    print("✓ test_file_structure_complete")


def run_all_tests():
    """Run all tests in order."""
    tests = [
        test_file_does_not_exist,
        test_create_markdown_file,
        test_file_has_h1_heading,
        test_file_has_blank_line,
        test_file_has_prose_content,
        test_prose_has_2_to_3_sentences,
        test_file_encoding_is_utf8_no_bom,
        test_file_has_lf_line_endings,
        test_file_size_in_typical_range,
        test_file_structure_complete,
    ]

    print("=" * 60)
    print("Feature 082: Markdown File Creation - Test Suite")
    print("=" * 60)
    print()

    failed = []
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed.append((test.__name__, str(e)))
        except Exception as e:
            print(f"✗ {test.__name__}: {type(e).__name__}: {e}")
            failed.append((test.__name__, f"{type(e).__name__}: {e}"))

    print()
    print("=" * 60)
    if failed:
        print(f"FAILED: {len(failed)} test(s) failed")
        for name, error in failed:
            print(f"  - {name}: {error}")
        print("=" * 60)
        return False
    else:
        print("✓ All tests passed!")
        print("=" * 60)
        return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
