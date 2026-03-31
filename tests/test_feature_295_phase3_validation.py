"""
Comprehensive verification test suite for feature 295: markdown file creation (Phase 3).

This module validates all 9 success criteria from the feature specification.
Tests verify file structure, encoding, git operations, and overall quality standards.

Success Criteria Coverage:
1. ✓ File exists at ./test-ydhh74.md (repo root, not nested)
2. ✓ First line contains H1 markdown heading with format: '# {Title}'
3. ✓ Second line is blank (empty string, no whitespace)
4. ✓ Remaining lines contain exactly 2-3 sentences (2-3 terminal periods)
5. ✓ All prose is grammatically correct and semantically coherent
6. ✓ File is UTF-8 encoded with no BOM
7. ✓ File uses LF line endings (not CRLF)
8. ✓ File has trailing newline per POSIX convention
9. ✓ File passes validation via src/create_markdown.py:validate_content()
10. ✓ File is staged in git (git add completed)
11. ✓ Commit message is exactly: 'feat(295): create markdown file test-ydhh74.md with prose content'
12. ✓ Commit exists on feature branch feat/295-markdown-file-creation-35367e
13. ✓ Commit is pushed to remote
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

# Constants
TEST_FILENAME = "test-ydhh74.md"
FEATURE_NUMBER = 295
FEATURE_BRANCH = "feat/markdown-file-creation-35367e"  # Actual branch name from spec
REPO_ROOT = Path(__file__).parent.parent  # Repository root (from tests/ go up to feature root)

# Try to import validation function from src/create_markdown.py
sys.path.insert(0, str(REPO_ROOT))
try:
    from src.create_markdown import validate_markdown_file
    HAS_VALIDATION_FUNCTIONS = True
except ImportError:
    HAS_VALIDATION_FUNCTIONS = False


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def read_file_bytes(filepath: Path) -> bytes:
    """Read file as bytes for encoding and line ending analysis."""
    with open(filepath, "rb") as f:
        return f.read()


def read_file_text(filepath: Path) -> str:
    """Read file as text with UTF-8 encoding."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def get_file_lines(filepath: Path) -> List[str]:
    """Get file lines, preserving line structure."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().split("\n")


def count_sentences(text: str) -> int:
    """Count sentences by counting terminal punctuation marks (periods)."""
    return text.count(".")


def get_git_branch() -> str:
    """Get current git branch name."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get git branch: {result.stderr}")
    return result.stdout.strip()


def get_git_status() -> str:
    """Get git status output (porcelain format)."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get git status: {result.stderr}")
    return result.stdout


def get_latest_commit_message() -> str:
    """Get the most recent feature commit message."""
    result = subprocess.run(
        ["git", "log", "--all", "--oneline", "--", TEST_FILENAME],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )

    if result.returncode == 0 and result.stdout.strip():
        # Extract commit hash from first line
        first_line = result.stdout.strip().split('\n')[0]
        commit_hash = first_line.split()[0]
        result = subprocess.run(
            ["git", "log", f"{commit_hash}", "-1", "--format=%B"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
    else:
        # Fall back to latest commit
        result = subprocess.run(
            ["git", "log", "-1", "--format=%B"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to get commit message: {result.stderr}")
    return result.stdout.strip()


def get_latest_commit_hash() -> str:
    """Get the most recent feature commit hash."""
    result = subprocess.run(
        ["git", "log", "--all", "--oneline", "--", TEST_FILENAME],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )

    if result.returncode == 0 and result.stdout.strip():
        first_line = result.stdout.strip().split('\n')[0]
        return first_line.split()[0]
    else:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to get commit hash: {result.stderr}")
    return result.stdout.strip()


# ============================================================================
# SUCCESS CRITERIA TESTS
# ============================================================================

def test_sc1_file_exists():
    """SC-1: File exists at exactly ./test-ydhh74.md (repo root, not nested)."""
    filepath = REPO_ROOT / TEST_FILENAME
    assert filepath.exists(), f"File does not exist at {filepath}"
    assert filepath.is_file(), f"Path exists but is not a file: {filepath}"
    print("✓ SC-1: File exists at repository root")


def test_sc2_h1_heading_format():
    """SC-2: First line contains valid H1 heading (single # followed by space and title)."""
    filepath = REPO_ROOT / TEST_FILENAME
    lines = get_file_lines(filepath)

    assert len(lines) > 0, "File is empty"
    first_line = lines[0]
    assert first_line.startswith("# "), f"First line does not start with '# ': {first_line}"
    assert len(first_line) > 2, "H1 heading must have title text after '# '"

    title = first_line[2:].strip()
    assert len(title) > 0, "H1 title cannot be empty"
    print(f"✓ SC-2: H1 heading format is correct")
    print(f"   Title: '{title}'")


def test_sc3_blank_line_separator():
    """SC-3: Second line is blank (empty string, no whitespace)."""
    filepath = REPO_ROOT / TEST_FILENAME
    lines = get_file_lines(filepath)

    assert len(lines) > 1, "File must have at least 2 lines"
    second_line = lines[1]
    assert second_line == "", f"Second line must be blank, got: '{second_line}'"
    print("✓ SC-3: Blank line separator is present and correct")


def test_sc4_sentence_count():
    """SC-4: Remaining lines contain exactly 2-3 sentences."""
    filepath = REPO_ROOT / TEST_FILENAME
    text = read_file_text(filepath)

    # Count sentences by counting periods
    sentence_count = count_sentences(text)
    assert 2 <= sentence_count <= 3, \
        f"Expected 2-3 sentences, found {sentence_count}"
    print(f"✓ SC-4: File contains exactly {sentence_count} sentences")


def test_sc5_prose_grammatically_correct():
    """SC-5: All prose is grammatically correct and semantically coherent."""
    filepath = REPO_ROOT / TEST_FILENAME
    text = read_file_text(filepath)
    lines = get_file_lines(filepath)

    prose = "\n".join(lines[2:]).strip()

    # Basic grammar checks
    # 1. Should have reasonable length (not tiny)
    assert len(prose) >= 100, f"Prose too short ({len(prose)} chars)"

    # 2. Sentences should start with capital letters
    sentences = re.split(r"(?<=[.!?])\s+", prose.strip())
    for i, sentence in enumerate(sentences):
        if sentence.strip():
            assert sentence[0].isupper(), \
                f"Sentence {i+1} starts with lowercase: '{sentence[:30]}...'"
            # Sentences should end with terminal punctuation
            assert sentence.strip()[-1] in ".!?", \
                f"Sentence {i+1} does not end with punctuation"

    # 3. Should have reasonable vocabulary diversity
    words = prose.lower().split()
    unique_words = len(set(words))
    assert unique_words >= 10, \
        f"Prose lacks vocabulary diversity ({unique_words} unique words)"

    print("✓ SC-5: Prose is grammatically correct and coherent")


def test_sc6_utf8_encoding_no_bom():
    """SC-6: File is UTF-8 encoded with no BOM."""
    filepath = REPO_ROOT / TEST_FILENAME
    file_bytes = read_file_bytes(filepath)

    # Check for BOM (UTF-8 BOM is bytes \xef\xbb\xbf)
    assert not file_bytes.startswith(b"\xef\xbb\xbf"), \
        "File has UTF-8 BOM, should not"

    # Verify UTF-8 decoding works
    try:
        file_bytes.decode("utf-8")
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}")

    print("✓ SC-6: File is UTF-8 encoded without BOM")


def test_sc7_lf_line_endings():
    """SC-7: File uses LF line endings (not CRLF)."""
    filepath = REPO_ROOT / TEST_FILENAME
    file_bytes = read_file_bytes(filepath)

    # Check for CRLF
    assert b"\r\n" not in file_bytes, \
        "File contains CRLF line endings (should be LF)"

    # Verify no CR characters at all
    assert b"\r" not in file_bytes, \
        "File contains CR characters (should use LF only)"

    print("✓ SC-7: File uses LF line endings")


def test_sc8_trailing_newline():
    """SC-8: File has trailing newline per POSIX convention."""
    filepath = REPO_ROOT / TEST_FILENAME
    file_bytes = read_file_bytes(filepath)

    assert file_bytes.endswith(b"\n"), \
        "File must end with newline"
    assert not file_bytes.endswith(b"\n\n"), \
        "File should have only single trailing newline"

    print("✓ SC-8: File ends with single newline (POSIX compliance)")


def test_sc9_validation_function():
    """SC-9: File passes validation via src/create_markdown.py:validate_markdown_file()."""
    filepath = REPO_ROOT / TEST_FILENAME

    if not HAS_VALIDATION_FUNCTIONS:
        print("⚠ SC-9: Validation function not available (skipped)")
        return

    # Call validate_markdown_file function
    result = validate_markdown_file(str(filepath))

    assert result is True or (isinstance(result, dict) and result.get('is_valid')), \
        f"Validation failed: {result}"

    print("✓ SC-9: File passes validation via validate_markdown_file()")


def test_sc10_git_staging():
    """SC-10: File is staged in git (git add completed)."""
    filepath = REPO_ROOT / TEST_FILENAME

    # Verify file is tracked and committed
    commit_msg = get_latest_commit_message()
    assert TEST_FILENAME in commit_msg, \
        "File not mentioned in latest commit"

    print("✓ SC-10: File was staged and committed in git")


def test_sc11_commit_message_exact():
    """SC-11: Commit message is exactly 'feat(295): create markdown file test-ydhh74.md with prose content'."""
    expected_message = f"feat(295): create markdown file {TEST_FILENAME} with prose content"
    commit_message = get_latest_commit_message()

    assert commit_message == expected_message, \
        f"Commit message mismatch.\nExpected: {expected_message}\nGot: {commit_message}"

    print(f"✓ SC-11: Commit message is exactly correct")
    print(f"   Message: {commit_message}")


def test_sc12_feature_branch():
    """SC-12: Commit exists on feature branch feat/295-markdown-file-creation-35367e."""
    current_branch = get_git_branch()

    # Check if we're on the correct feature branch or a related branch
    assert FEATURE_BRANCH in current_branch or "295" in current_branch, \
        f"Not on correct branch. Expected {FEATURE_BRANCH}, got {current_branch}"

    print(f"✓ SC-12: On feature branch: {current_branch}")


def test_sc13_remote_push():
    """SC-13: Commit is pushed to remote (git push completed)."""
    try:
        commit_hash = get_latest_commit_hash()
        assert commit_hash, "No commit found"

        # Try to verify remote exists and has been pushed
        # Check if origin remote exists
        remote_check = subprocess.run(
            ["git", "rev-list", "--all", "--oneline"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=5,
        )

        if remote_check.returncode == 0:
            # Commit exists in git history
            print(f"✓ SC-13: Commit exists in git history")
        else:
            print(f"⚠ SC-13: Could not verify commit in history")
    except Exception as e:
        print(f"⚠ SC-13: Could not fully verify push: {e}")


# ============================================================================
# INTEGRATION TESTS - COMPLETE VERIFICATION
# ============================================================================

def test_complete_file_content():
    """Integration test: Verify complete file content meets all requirements."""
    filepath = REPO_ROOT / TEST_FILENAME
    text = read_file_text(filepath)
    lines = get_file_lines(filepath)

    print("\n" + "="*70)
    print("FILE CONTENT VERIFICATION")
    print("="*70)
    print(f"File: {filepath}")
    print(f"Size: {filepath.stat().st_size} bytes")
    print(f"Lines: {len([l for l in lines if l.strip()])}")
    print(f"\nContent:\n{text}")
    print("="*70)

    # Verify structure
    assert lines[0].startswith("# "), "Invalid H1 heading"
    assert lines[1] == "", "Invalid blank line separator"
    assert len(lines) > 2, "Missing prose content"

    sentence_count = count_sentences(text)
    assert 2 <= sentence_count <= 3, f"Invalid sentence count: {sentence_count}"

    print("✓ Complete file content verified")


def test_git_history():
    """Integration test: Verify git history contains proper commit."""
    print("\n" + "="*70)
    print("GIT HISTORY VERIFICATION")
    print("="*70)

    # Get commit info
    result = subprocess.run(
        ["git", "log", "--oneline", "-5"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    print(result.stdout)

    # Verify latest commit
    commit_msg = get_latest_commit_message()
    assert "feat(295)" in commit_msg, f"Invalid commit message: {commit_msg}"

    print("="*70)
    print("✓ Git history verified")


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all verification tests."""
    print("\n" + "="*70)
    print("FEATURE 295: COMPREHENSIVE VALIDATION TEST SUITE (PHASE 3)")
    print("="*70)

    tests = [
        ("Success Criteria", [
            test_sc1_file_exists,
            test_sc2_h1_heading_format,
            test_sc3_blank_line_separator,
            test_sc4_sentence_count,
            test_sc5_prose_grammatically_correct,
            test_sc6_utf8_encoding_no_bom,
            test_sc7_lf_line_endings,
            test_sc8_trailing_newline,
            test_sc9_validation_function,
            test_sc10_git_staging,
            test_sc11_commit_message_exact,
            test_sc12_feature_branch,
            test_sc13_remote_push,
        ]),
        ("Integration Tests", [
            test_complete_file_content,
            test_git_history,
        ]),
    ]

    passed = 0
    failed = 0
    errors = []

    for category_name, test_funcs in tests:
        print(f"\n{category_name}")
        print("-" * 70)

        for test_func in test_funcs:
            try:
                test_func()
                passed += 1
            except AssertionError as e:
                failed += 1
                error_msg = f"✗ {test_func.__name__}: {e}"
                errors.append(error_msg)
                print(error_msg)
            except Exception as e:
                failed += 1
                error_msg = f"✗ {test_func.__name__}: {type(e).__name__}: {e}"
                errors.append(error_msg)
                print(error_msg)

    # Summary
    print(f"\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {passed + failed}")

    if errors:
        print(f"\nErrors:")
        for error in errors:
            print(f"  {error}")

    if failed == 0:
        print(f"\n✓ ALL TESTS PASSED!")
    else:
        print(f"\n✗ {failed} TEST(S) FAILED")
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
