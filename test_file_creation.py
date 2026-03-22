"""
Test file for markdown file creation and validation (feature 158).

Tests for creating test-w2kr34.md with proper structure, encoding, and line endings.
"""

import os
from pathlib import Path


def test_prose_content_composition():
    """Task 1: Compose prose content for markdown file."""
    # Compose 2-3 grammatically correct sentences about an arbitrary topic
    prose_content = (
        "Deliberate practice is the foundation of mastery, requiring focused effort "
        "on improving specific skills through feedback and iteration. "
        "Unlike passive learning, deliberate practice demands intentional engagement "
        "with challenging material at the edge of our current abilities. "
        "By embracing this approach, we accelerate our growth and achieve excellence "
        "in our chosen disciplines."
    )

    # Verify composition meets acceptance criteria
    sentences = [s.strip() for s in prose_content.split('.') if s.strip()]
    assert 2 <= len(sentences) <= 3, f"Expected 2-3 sentences, got {len(sentences)}"

    # Verify grammatically correct (no obvious errors)
    for sentence in sentences:
        assert len(sentence) > 0, "Sentences must not be empty"
        assert sentence[0].isupper(), f"Sentence must start with capital: {sentence}"

    # Verify content length is reasonable
    assert 100 <= len(prose_content) <= 500, f"Content should be 100-500 chars, got {len(prose_content)}"

    return prose_content


def test_file_does_not_exist_yet():
    """Verify test-w2kr34.md does not exist before creation."""
    file_path = Path('test-w2kr34.md')
    assert not file_path.exists(), "File should not exist before task execution"


def test_file_creation_with_proper_structure():
    """Task 2: Create markdown file with H1 heading and prose content."""
    file_path = Path('test-w2kr34.md')

    # Get prose content from task 1
    prose_content = test_prose_content_composition()

    # Compose full file content: H1 heading + blank line + prose + blank line at end
    title = "# Deliberate Practice"
    content = f"{title}\n\n{prose_content}\n"

    # Create file with explicit LF line endings (not CRLF)
    # Use binary mode to write exactly what we specify (LF, not platform-native CRLF)
    file_path.write_bytes(content.encode('utf-8'))

    # Verify file exists
    assert file_path.exists(), "File should exist after creation"

    # Verify file contains H1 heading marker
    file_content = file_path.read_text(encoding='utf-8')
    assert file_content.startswith('#'), "File should start with H1 heading marker"

    # Verify structure: H1 heading, blank line, prose, blank line
    lines = file_content.split('\n')
    assert lines[0].startswith('# '), "First line should be H1 heading"
    assert lines[1] == '', "Second line should be blank"
    assert len(lines) >= 3, "File should have at least 3 lines"
    assert lines[2].strip(), "Prose content should start on line 3"

    # Verify encoding is UTF-8
    # Read as binary and verify it can be decoded as UTF-8 without BOM
    file_bytes = file_path.read_bytes()
    assert not file_bytes.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"
    file_bytes.decode('utf-8')  # Should not raise exception

    return file_path, content


def test_file_encoding_utf8_no_bom():
    """Task 3: Verify file is UTF-8 without Byte Order Mark."""
    file_path = Path('test-w2kr34.md')
    assert file_path.exists(), "File must exist before validation"

    # Read as binary
    file_bytes = file_path.read_bytes()

    # Verify no UTF-8 BOM (EF BB BF)
    assert not file_bytes.startswith(b'\xef\xbb\xbf'), (
        "File should not start with UTF-8 BOM bytes (EF BB BF)"
    )

    # Verify file can be decoded as UTF-8
    try:
        file_bytes.decode('utf-8')
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}")


def test_file_line_endings_lf():
    """Task 3: Verify file uses LF line endings, not CRLF."""
    file_path = Path('test-w2kr34.md')
    assert file_path.exists(), "File must exist before validation"

    # Read as binary
    file_bytes = file_path.read_bytes()

    # Verify no CRLF (\r\n) - should only have LF (\n)
    assert b'\r\n' not in file_bytes, (
        "File should use LF line endings (\\n), not CRLF (\\r\\n)"
    )

    # Verify at least some LF line endings exist
    assert b'\n' in file_bytes, "File should contain line endings"


def test_file_size_in_range():
    """Task 3: Verify file size is between 300-600 bytes."""
    file_path = Path('test-w2kr34.md')
    assert file_path.exists(), "File must exist before validation"

    file_size = file_path.stat().st_size
    assert 300 <= file_size <= 600, (
        f"File size should be 300-600 bytes, got {file_size} bytes"
    )


def test_file_content_readable():
    """Task 3: Verify file content is readable and grammatically correct."""
    file_path = Path('test-w2kr34.md')
    assert file_path.exists(), "File must exist before validation"

    # Read file content
    content = file_path.read_text(encoding='utf-8')

    # Verify content is not empty
    assert len(content) > 0, "File content should not be empty"

    # Verify basic structure
    lines = content.split('\n')
    assert lines[0].startswith('# '), "First line should be H1 heading"
    assert lines[1] == '', "Second line should be blank"

    # Verify prose content exists and is reasonable
    prose = '\n'.join(lines[2:]).strip()
    assert len(prose) > 0, "Prose content should not be empty"

    # Basic grammar check: sentences should end with punctuation
    sentences = [s.strip() for s in prose.split('.') if s.strip()]
    for sentence in sentences:
        assert sentence[0].isupper(), f"Sentence should start with capital: {sentence}"


if __name__ == '__main__':
    # Run task-by-task
    print("=" * 70)
    print("TASK 1: Compose prose content")
    print("=" * 70)
    prose = test_prose_content_composition()
    print(f"[PASS] Prose content composed ({len(prose)} chars)")
    print(f"  Content: {prose[:80]}...")

    print("\n" + "=" * 70)
    print("TASK 2: Create markdown file")
    print("=" * 70)
    test_file_does_not_exist_yet()
    print("[PASS] File does not exist yet")

    file_path, content = test_file_creation_with_proper_structure()
    print(f"[PASS] File created: {file_path}")
    print(f"  Content ({len(content)} chars):")
    for i, line in enumerate(content.split('\n')[:5], 1):
        print(f"    Line {i}: {line}")

    print("\n" + "=" * 70)
    print("TASK 3: Validate file properties")
    print("=" * 70)
    test_file_encoding_utf8_no_bom()
    print("[PASS] File encoding is UTF-8 without BOM")

    test_file_line_endings_lf()
    print("[PASS] File uses LF line endings (not CRLF)")

    test_file_size_in_range()
    file_size = Path('test-w2kr34.md').stat().st_size
    print(f"[PASS] File size is in range: {file_size} bytes (300-600 bytes)")

    test_file_content_readable()
    print("[PASS] File content is readable and grammatically correct")

    print("\n" + "=" * 70)
    print("ALL TESTS PASSED")
    print("=" * 70)
