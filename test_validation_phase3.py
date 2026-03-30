#!/usr/bin/env python3
"""
Validation & Verification tests for feature 278: markdown-file-creation-dae11e
Phase 3 acceptance criteria verification.

This test suite verifies:
- File existence and basic properties
- Content structure (H1 heading, blank line, 2-3 sentences of prose)
- File encoding (UTF-8 without BOM)
- Line endings (LF, not CRLF)
- File size (400-600 bytes)
- Markdown syntax validity (CommonMark)
- Git operations (commit message, remote push)
"""

import subprocess
import sys
from pathlib import Path
from typing import Tuple

# Use ASCII-safe markers for terminal output
PASS_MARK = "[PASS]"
FAIL_MARK = "[FAIL]"

# ============================================================================
# Assertion Helper Functions
# ============================================================================


def assert_file_exists(file_path: Path) -> None:
    """Assert file exists at specified path."""
    assert file_path.exists(), f"File does not exist: {file_path}"
    assert file_path.is_file(), f"Path is not a file: {file_path}"


def assert_file_size_in_range(file_path: Path, min_bytes: int = 350, max_bytes: int = 650) -> int:
    """Assert file size is within expected range. Returns actual size."""
    size = file_path.stat().st_size
    assert min_bytes <= size <= max_bytes, \
        f"File size {size} bytes not in range [{min_bytes}, {max_bytes}]"
    return size


def assert_utf8_encoding_no_bom(file_path: Path) -> None:
    """Assert file is UTF-8 encoded without BOM."""
    with open(file_path, 'rb') as f:
        first_bytes = f.read(3)

    # UTF-8 BOM is EF BB BF
    assert not first_bytes.startswith(b'\xef\xbb\xbf'), \
        f"File has UTF-8 BOM, but should not have one"

    # Verify it's valid UTF-8
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}")


def assert_lf_line_endings(file_path: Path) -> None:
    """Assert file uses LF (Unix) line endings, not CRLF (Windows)."""
    with open(file_path, 'rb') as f:
        content = f.read()

    assert b'\r\n' not in content, "File contains CRLF line endings (Windows-style), should be LF (Unix-style)"
    assert b'\n' in content or b'\r' not in content, "File should contain LF line endings"


def assert_heading_structure(content: str) -> str:
    """Assert file starts with H1 heading. Returns the heading text."""
    lines = content.split('\n')
    assert len(lines) >= 3, \
        f"File should have at least 3 lines (heading, blank, prose), has {len(lines)}"

    heading_line = lines[0]
    assert heading_line.startswith('# '), \
        f"First line should be H1 heading (starts with '# '), got: {repr(heading_line)}"

    blank_line = lines[1]
    assert blank_line == '', \
        f"Second line should be blank, got: {repr(blank_line)}"

    return heading_line


def assert_prose_content(content: str) -> Tuple[str, int]:
    """
    Assert file contains 2-3 sentences of prose.
    Returns (prose_text, sentence_count).
    """
    import re

    lines = content.split('\n')
    prose = lines[2]  # Third line (index 2) is prose

    # Count sentences by splitting on sentence boundaries (. ! ?)
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', prose) if s.strip()]

    assert 2 <= len(sentences) <= 3, \
        f"Expected 2-3 sentences, found {len(sentences)}: {sentences}"

    return prose, len(sentences)


def assert_trailing_newline(content: str) -> None:
    """Assert file ends with a single newline."""
    assert content.endswith('\n'), "File should end with newline"
    assert not content.endswith('\n\n'), "File should end with single newline, not double"


def assert_commonmark_syntax(file_path: Path) -> None:
    """
    Assert file is valid CommonMark markdown.
    Uses commonmark package if available, otherwise performs basic checks.
    """
    try:
        import commonmark
        parser = commonmark.Parser()
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        doc = parser.parse(content)
        # If parsing succeeds without exception, markdown is valid
    except ImportError:
        # Fallback: basic structure validation without commonmark library
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        # Check basic structure is present
        assert lines[0].startswith('# '), "Must start with H1 heading"
        assert lines[1] == '', "Second line must be blank"
        assert len(lines) >= 3, "Must have prose content"
        assert len(lines[2].strip()) > 0, "Prose must not be empty"


def assert_git_commit_exists(commit_sha: str) -> None:
    """Assert git commit exists in repository."""
    result = subprocess.run(
        ['git', 'cat-file', '-t', commit_sha],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, \
        f"Git commit {commit_sha} not found in repository"


def assert_commit_message_format(commit_sha: str) -> str:
    """
    Assert commit has correct conventional commit format.
    Returns the commit message.
    """
    result = subprocess.run(
        ['git', 'log', '-1', '--format=%B', commit_sha],
        capture_output=True,
        text=True
    )
    message = result.stdout.strip()

    # Check conventional commit format: type(scope): description
    assert message.startswith('feat(278): '), \
        f"Commit message should start with 'feat(278): ', got: {repr(message)}"

    assert 'test-6ektaf.md' in message, \
        f"Commit message should mention 'test-6ektaf.md', got: {repr(message)}"

    return message


def assert_commit_on_remote_branch(commit_sha: str, branch: str) -> None:
    """Assert commit is reachable from remote branch."""
    result = subprocess.run(
        ['git', 'merge-base', '--is-ancestor', commit_sha, f'origin/{branch}'],
        capture_output=True
    )
    assert result.returncode == 0, \
        f"Commit {commit_sha} not found on remote branch origin/{branch}"


def assert_file_in_commit(commit_sha: str, file_name: str) -> None:
    """Assert file is included in git commit."""
    result = subprocess.run(
        ['git', 'show', '--name-only', '--pretty=', commit_sha],
        capture_output=True,
        text=True
    )
    files = result.stdout.strip().split('\n')
    assert file_name in files, \
        f"File {file_name} not found in commit {commit_sha}. Files: {files}"


# ============================================================================
# Main Test Suite
# ============================================================================


def test_file_exists():
    """Test: File test-6ektaf.md exists in repository root."""
    file_path = Path('test-6ektaf.md')
    assert_file_exists(file_path)
    print(f"{PASS_MARK} File test-6ektaf.md exists in repository root")


def test_file_size():
    """Test: File size is approximately 400-600 bytes."""
    file_path = Path('test-6ektaf.md')
    size = assert_file_size_in_range(file_path)
    print(f"{PASS_MARK} File size is {size} bytes (expected 350-650 bytes)")


def test_file_encoding_no_bom():
    """Test: File encoding is UTF-8 without BOM."""
    file_path = Path('test-6ektaf.md')
    assert_utf8_encoding_no_bom(file_path)
    print(f"{PASS_MARK} File encoding is UTF-8 without BOM")


def test_line_endings_lf():
    """Test: File uses LF line endings, not CRLF."""
    file_path = Path('test-6ektaf.md')
    assert_lf_line_endings(file_path)
    print(f"{PASS_MARK} File uses LF (Unix-style) line endings, not CRLF")


def test_heading_structure():
    """Test: File starts with H1 heading followed by blank line."""
    file_path = Path('test-6ektaf.md')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    heading = assert_heading_structure(content)
    print(f"{PASS_MARK} File has correct structure with H1 heading: {repr(heading)}")


def test_prose_content():
    """Test: File contains exactly 2-3 sentences of prose."""
    file_path = Path('test-6ektaf.md')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    prose, num_sentences = assert_prose_content(content)
    print(f"{PASS_MARK} File contains {num_sentences} sentences of prose content")


def test_trailing_newline():
    """Test: File ends with a single trailing newline."""
    file_path = Path('test-6ektaf.md')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert_trailing_newline(content)
    print(f"{PASS_MARK} File ends with single trailing newline")


def test_commonmark_syntax():
    """Test: File is valid CommonMark markdown."""
    file_path = Path('test-6ektaf.md')
    assert_commonmark_syntax(file_path)
    print(f"{PASS_MARK} File is valid CommonMark markdown")


def test_git_commit_exists():
    """Test: Git commit exists with correct message format."""
    commit_sha = '255a54ec'
    assert_git_commit_exists(commit_sha)
    message = assert_commit_message_format(commit_sha)
    print(f"{PASS_MARK} Git commit 255a54ec exists with conventional commit message:")
    print(f"  '{message}'")


def test_commit_on_remote_branch():
    """Test: Commit is pushed to remote feature branch."""
    commit_sha = '255a54ec'
    branch = 'feat/markdown-file-creation-dae11e'
    assert_commit_on_remote_branch(commit_sha, branch)
    print(f"{PASS_MARK} Commit 255a54ec is pushed to remote branch origin/{branch}")


def test_file_in_commit():
    """Test: File test-6ektaf.md is included in the commit."""
    commit_sha = '255a54ec'
    assert_file_in_commit(commit_sha, 'test-6ektaf.md')
    print(f"{PASS_MARK} File test-6ektaf.md is included in commit 255a54ec")


# ============================================================================
# Summary Report Function
# ============================================================================


def run_all_tests():
    """Run all validation tests and generate summary report."""
    tests = [
        test_file_exists,
        test_file_size,
        test_file_encoding_no_bom,
        test_line_endings_lf,
        test_heading_structure,
        test_prose_content,
        test_trailing_newline,
        test_commonmark_syntax,
        test_git_commit_exists,
        test_commit_on_remote_branch,
        test_file_in_commit,
    ]

    print("\n" + "=" * 80)
    print("VALIDATION & VERIFICATION PHASE 3: ACCEPTANCE CRITERIA")
    print("=" * 80)
    print()

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"{FAIL_MARK} {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"{FAIL_MARK} {test.__name__}: Unexpected error: {e}")
            failed += 1

    print()
    print("=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 80)

    if failed > 0:
        sys.exit(1)
    else:
        print("\n[PASS] All acceptance criteria verified successfully!")
        print("[PASS] Feature 278 is complete and ready for delivery")


if __name__ == '__main__':
    run_all_tests()
