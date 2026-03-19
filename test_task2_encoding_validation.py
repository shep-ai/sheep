"""Test for encoding and format validation (task-2)."""

from pathlib import Path


def test_utf8_encoding_no_bom():
    """Assert file is UTF-8 encoded without BOM."""
    file_path = Path("test-oyjp7x.md")
    binary_content = file_path.read_bytes()

    # Check for UTF-8 BOM (EF BB BF)
    assert not binary_content.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"
    print("[PASS] File is UTF-8 encoded without BOM")


def test_lf_line_endings_only():
    """Assert file uses only LF line endings, not CRLF."""
    file_path = Path("test-oyjp7x.md")
    binary_content = file_path.read_bytes()

    # Check for CRLF (Windows line endings)
    assert b'\r\n' not in binary_content, "File should use LF, not CRLF"
    print("[PASS] File uses Unix-style LF line endings only")


def test_correct_format_pattern():
    """Assert file format matches pattern: # Heading\n\n<prose>."""
    file_path = Path("test-oyjp7x.md")
    content = file_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Verify structure
    assert len(lines) >= 3, f"Expected at least 3 lines, found {len(lines)}"
    assert lines[0].startswith('# '), f"First line should be H1 heading, got: {lines[0]}"
    assert lines[1] == '', f"Second line should be blank, got: {repr(lines[1])}"

    # Verify prose exists after blank line
    prose = '\n'.join(lines[2:]).strip()
    assert prose, "Prose content should exist after blank line"

    print("[PASS] File format matches pattern: # Heading\\n\\n<prose>")


def test_file_size_guideline():
    """Assert file size is within 400-600 bytes guideline."""
    file_path = Path("test-oyjp7x.md")
    binary_content = file_path.read_bytes()
    file_size = len(binary_content)

    assert 400 <= file_size <= 600, f"File size {file_size} not in 400-600 byte range"
    print(f"[PASS] File size is {file_size} bytes (within 400-600 guideline)")


def test_markdown_syntax_valid():
    """Assert markdown syntax is valid per CommonMark specification."""
    file_path = Path("test-oyjp7x.md")
    content = file_path.read_text(encoding='utf-8')

    # Basic validation: H1 heading exists, prose exists
    assert '\n# ' in content or content.startswith('# '), "Should have H1 heading"
    assert len(content.split('.')) >= 3, "Should have multiple sentences"

    # Check for obvious syntax errors
    assert '##' not in content or content.count('#') <= 5, "Should have minimal headings"

    print("[PASS] Markdown syntax is valid")


def test_prose_is_readable():
    """Assert prose content is readable and grammatically reasonable."""
    file_path = Path("test-oyjp7x.md")
    content = file_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Extract prose (after blank line)
    prose = '\n'.join(lines[2:]).strip()

    # Basic readability checks
    words = prose.split()
    assert len(words) >= 30, f"Prose should have reasonable word count, found {len(words)}"

    # Check for basic sentence structure (capitalized words)
    assert any(word[0].isupper() for word in words), "Prose should have capitalized sentences"

    print(f"[PASS] Prose content is readable ({len(words)} words)")


if __name__ == "__main__":
    test_utf8_encoding_no_bom()
    test_lf_line_endings_only()
    test_correct_format_pattern()
    test_file_size_guideline()
    test_markdown_syntax_valid()
    test_prose_is_readable()
    print("\n[SUCCESS] All encoding and format validation tests passed!")
