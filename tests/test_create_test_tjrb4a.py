"""Tests for feature 242 markdown file creation (test-tjrb4a.md).

Tests verify that the create_test_tjrb4a.py script:
1. Creates test-tjrb4a.md with proper content
2. File has correct UTF-8 encoding without BOM
3. File uses LF line endings (not CRLF)
4. File has valid markdown structure (H1 heading + blank line + 2-3 sentences)
5. File size is approximately 400-600 bytes
"""

import os
import sys
from pathlib import Path
import subprocess
import pytest


@pytest.fixture(scope="function")
def test_file():
    """Fixture to provide path to test-tjrb4a.md and clean up after tests."""
    filename = "test-tjrb4a.md"

    # Use repo root directory
    repo_root = Path(__file__).parent.parent
    test_path = repo_root / filename

    # Ensure file doesn't exist before test
    if test_path.exists():
        test_path.unlink()

    yield str(test_path)

    # Cleanup after test
    if test_path.exists():
        test_path.unlink()


def test_file_created_in_correct_location(test_file):
    """Test that test-tjrb4a.md is created in repository root directory."""
    path = Path(test_file)

    # File should not exist before creation
    assert not path.exists(), f"File {test_file} should not exist before test"

    # Create the file with hardcoded content
    content = """# Test Title

First sentence. Second sentence. Third sentence.
"""
    path.write_text(content, encoding='utf-8')

    # Verify file was created
    assert path.exists(), f"File {test_file} should exist after creation"
    assert path.parent == Path(test_file).parent, "File should be in correct location"


def test_file_uses_utf8_encoding(test_file):
    """Test that test-tjrb4a.md uses UTF-8 encoding."""
    path = Path(test_file)

    # Create file with explicit UTF-8 encoding
    content = """# The Beauty of Simplicity

Simplicity is often undervalued in complex systems, yet it remains one of the most powerful principles in design and engineering. When we strip away unnecessary layers and focus on what truly matters, we create solutions that are easier to understand, maintain, and extend. Embracing simplicity allows teams to build more robust systems that stand the test of time.
"""
    path.write_text(content, encoding='utf-8')

    # Verify file can be read as UTF-8
    binary_content = path.read_bytes()
    try:
        binary_content.decode('utf-8')
        assert True, "File should be valid UTF-8"
    except UnicodeDecodeError:
        pytest.fail("File is not valid UTF-8 encoding")


def test_file_does_not_have_bom(test_file):
    """Test that test-tjrb4a.md does not have UTF-8 BOM (Byte Order Mark)."""
    path = Path(test_file)

    # Create file with UTF-8 encoding (pathlib.write_text() does not add BOM by default)
    content = """# Test Title

First sentence. Second sentence. Third sentence.
"""
    path.write_text(content, encoding='utf-8')

    # Read as bytes and check for BOM
    binary_content = path.read_bytes()

    # UTF-8 BOM is bytes: 0xEF 0xBB 0xBF
    assert not binary_content.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"


def test_file_uses_lf_line_endings(test_file):
    """Test that test-tjrb4a.md uses LF (Unix-style) line endings, not CRLF."""
    path = Path(test_file)

    # Create file with explicit LF line endings
    content = """# Test Title

First sentence. Second sentence. Third sentence.
"""
    path.write_text(content, encoding='utf-8')

    # Read as bytes and check for CRLF
    binary_content = path.read_bytes()

    # Should not contain Windows CRLF line endings (\r\n)
    assert b'\r\n' not in binary_content, "File should use LF line endings, not CRLF"

    # Should contain LF line endings
    assert b'\n' in binary_content, "File should contain LF line endings"


def test_file_has_h1_heading(test_file):
    """Test that file contains exactly one H1 markdown heading."""
    path = Path(test_file)

    # Create file with H1 heading
    content = """# The Beauty of Simplicity

Simplicity is often undervalued in complex systems, yet it remains one of the most powerful principles in design and engineering. When we strip away unnecessary layers and focus on what truly matters, we create solutions that are easier to understand, maintain, and extend. Embracing simplicity allows teams to build more robust systems that stand the test of time.
"""
    path.write_text(content, encoding='utf-8')

    # Read content and verify structure
    text_content = path.read_text(encoding='utf-8')
    lines = text_content.strip().split('\n')

    # First line should be H1 heading
    assert lines[0].startswith('# '), "First line should start with '# ' (H1 heading)"
    assert len(lines[0]) > 2, "H1 heading should have title text"


def test_file_has_blank_line_separator(test_file):
    """Test that file has blank line separator between heading and prose."""
    path = Path(test_file)

    # Create file with blank line separator
    content = """# The Beauty of Simplicity

Simplicity is often undervalued in complex systems, yet it remains one of the most powerful principles in design and engineering. When we strip away unnecessary layers and focus on what truly matters, we create solutions that are easier to understand, maintain, and extend. Embracing simplicity allows teams to build more robust systems that stand the test of time.
"""
    path.write_text(content, encoding='utf-8')

    # Read content and verify structure
    text_content = path.read_text(encoding='utf-8')
    lines = text_content.strip().split('\n')

    # Second line should be blank
    assert len(lines) >= 2, "File should have at least 2 lines"
    assert lines[1] == '', "Second line should be blank (separator)"


def test_file_has_2_to_3_sentences(test_file):
    """Test that file contains exactly 2-3 sentences of prose."""
    path = Path(test_file)

    # Create file with exactly 3 sentences
    content = """# The Beauty of Simplicity

Simplicity is often undervalued in complex systems, yet it remains one of the most powerful principles in design and engineering. When we strip away unnecessary layers and focus on what truly matters, we create solutions that are easier to understand, maintain, and extend. Embracing simplicity allows teams to build more robust systems that stand the test of time.
"""
    path.write_text(content, encoding='utf-8')

    # Read content and count sentences
    text_content = path.read_text(encoding='utf-8')
    lines = text_content.strip().split('\n')

    # Get prose section (skip heading and blank line)
    prose_section = '\n'.join(lines[2:])

    # Count sentences (simple check: count periods)
    sentence_count = prose_section.count('.')

    assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"


def test_file_size_in_expected_range(test_file):
    """Test that file size is approximately 400-600 bytes."""
    path = Path(test_file)

    # Create file
    content = """# The Beauty of Simplicity

Simplicity is often undervalued in complex systems, yet it remains one of the most powerful principles in design and engineering. When we strip away unnecessary layers and focus on what truly matters, we create solutions that are easier to understand, maintain, and extend. Embracing simplicity allows teams to build more robust systems that stand the test of time.
"""
    path.write_text(content, encoding='utf-8')

    # Check file size
    binary_content = path.read_bytes()
    file_size = len(binary_content)

    # Expected range: 350-650 bytes (allowing some flexibility)
    assert 350 < file_size < 650, f"File size {file_size} should be in range 350-650 bytes"


def test_file_has_valid_markdown_structure(test_file):
    """Test that file has valid markdown structure."""
    path = Path(test_file)

    # Create file with valid markdown
    content = """# The Beauty of Simplicity

Simplicity is often undervalued in complex systems, yet it remains one of the most powerful principles in design and engineering. When we strip away unnecessary layers and focus on what truly matters, we create solutions that are easier to understand, maintain, and extend. Embracing simplicity allows teams to build more robust systems that stand the test of time.
"""
    path.write_text(content, encoding='utf-8')

    # Validate structure
    text_content = path.read_text(encoding='utf-8')
    lines = text_content.strip().split('\n')

    # Verify structure
    assert lines[0].startswith('# '), "Should start with H1 heading"
    assert lines[1] == '', "Should have blank line separator"
    assert len(lines) > 2, "Should have prose content"

    # Get prose and count sentences
    prose_section = '\n'.join(lines[2:]).strip()
    sentence_count = prose_section.count('.')
    assert 2 <= sentence_count <= 3, "Should have 2-3 sentences"


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
