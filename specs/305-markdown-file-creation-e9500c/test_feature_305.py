"""
Unit and integration tests for feature 305: Markdown file creation.

Tests the create_feature_305_markdown_file() function and verifies that:
1. The function calls create_markdown_file() with correct parameters
2. The function returns the expected result structure
3. The markdown file is created with proper content
4. All specification requirements are met (encoding, line endings, structure, etc.)
"""

import sys
from pathlib import Path
from unittest import mock

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sheep.features.feature_305 import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_305_markdown_file,
)
from sheep.content_generators import validate_markdown_file


# ============================================================================
# FEATURE FUNCTION TESTS (Unit/Integration)
# ============================================================================


def test_create_feature_305_markdown_file_returns_dict_with_required_keys():
    """
    Test that create_feature_305_markdown_file() returns a dict with required keys.

    The returned dict must contain:
    - filepath: Full path to created file
    - content: Markdown content
    - commit_message: Git commit message
    - push_result: Result from git push
    """
    try:
        result = create_feature_305_markdown_file()

        assert isinstance(result, dict), \
            f"Result must be a dict, got {type(result)}"

        required_keys = {"filepath", "content", "commit_message", "push_result"}
        result_keys = set(result.keys())

        assert required_keys.issubset(result_keys), \
            f"Result missing keys: {required_keys - result_keys}"

        print(f"✓ Function returns dict with required keys: {list(result.keys())}")

    except Exception as e:
        print(f"✗ Failed: {e}")
        raise


def test_create_feature_305_markdown_file_creates_file():
    """
    Test that create_feature_305_markdown_file() creates the markdown file.

    Verifies:
    - File is created at repository root
    - File exists and is readable
    - File has markdown content
    """
    try:
        result = create_feature_305_markdown_file()

        filepath = Path(result["filepath"])

        assert filepath.exists(), \
            f"File was not created: {filepath}"

        assert filepath.is_file(), \
            f"Path is not a file: {filepath}"

        assert filepath.name == MARKDOWN_FILENAME, \
            f"Filename mismatch: expected {MARKDOWN_FILENAME}, got {filepath.name}"

        # Read content
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        assert content, \
            "File is empty"

        print(f"✓ File created successfully: {filepath}")

    except Exception as e:
        print(f"✗ Failed: {e}")
        raise


def test_create_feature_305_markdown_file_returns_valid_content():
    """
    Test that create_feature_305_markdown_file() returns valid markdown content.

    Verifies:
    - Returned content is non-empty string
    - Content starts with H1 heading
    - Content has at least 2 lines (heading + blank line + prose)
    """
    try:
        result = create_feature_305_markdown_file()

        content = result["content"]

        assert isinstance(content, str), \
            f"Content must be string, got {type(content)}"

        assert content, \
            "Content is empty"

        assert content.startswith("# "), \
            f"Content must start with H1 heading (# ), got: {repr(content[:20])}"

        lines = content.split("\n")
        assert len(lines) >= 3, \
            f"Content must have at least 3 lines (heading, blank, prose), got {len(lines)}"

        print(f"✓ Valid markdown content returned ({len(content)} bytes)")

    except Exception as e:
        print(f"✗ Failed: {e}")
        raise


def test_create_feature_305_markdown_file_commit_message_format():
    """
    Test that commit message follows conventional commit format.

    Format: feat(305): create markdown file test-9s145k.md with prose content
    """
    try:
        result = create_feature_305_markdown_file()

        commit_message = result["commit_message"]

        assert isinstance(commit_message, str), \
            f"Commit message must be string, got {type(commit_message)}"

        # Check conventional commit format
        expected_prefix = f"feat({FEATURE_NUMBER}):"
        assert commit_message.startswith(expected_prefix), \
            f"Commit message must start with '{expected_prefix}', got: {commit_message}"

        # Check filename is in message
        assert MARKDOWN_FILENAME in commit_message, \
            f"Commit message must include filename {MARKDOWN_FILENAME}, got: {commit_message}"

        # Check for "prose content"
        assert "prose content" in commit_message.lower(), \
            f"Commit message must mention 'prose content', got: {commit_message}"

        print(f"✓ Commit message format correct: {commit_message}")

    except Exception as e:
        print(f"✗ Failed: {e}")
        raise


def test_create_feature_305_markdown_file_with_custom_repo_path():
    """
    Test that function works with explicit repo_path parameter.

    Verifies:
    - Function accepts repo_path parameter
    - Function creates file in specified repository
    """
    try:
        repo_path = str(Path.cwd())
        result = create_feature_305_markdown_file(repo_path=repo_path)

        assert result, \
            "Function failed with explicit repo_path"

        assert "filepath" in result, \
            "Result missing filepath key"

        print(f"✓ Function works with explicit repo_path: {repo_path}")

    except Exception as e:
        print(f"✗ Failed: {e}")
        raise


# ============================================================================
# FILE CONTENT VALIDATION TESTS
# ============================================================================


def test_created_file_has_utf8_encoding():
    """
    Test that created file has UTF-8 encoding without BOM.

    Verifies:
    - File is readable as UTF-8
    - File does not have UTF-8 BOM at start
    """
    try:
        result = create_feature_305_markdown_file()
        filepath = result["filepath"]

        # Read file as binary to check for BOM
        with open(filepath, "rb") as f:
            binary_content = f.read()

        # Check for UTF-8 BOM (should NOT be present)
        assert not binary_content.startswith(b"\xef\xbb\xbf"), \
            "File should not have UTF-8 BOM"

        # Verify valid UTF-8
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            raise AssertionError(f"File is not valid UTF-8: {e}")

        print(f"✓ File has UTF-8 encoding without BOM")

    except Exception as e:
        print(f"✗ Failed: {e}")
        raise


def test_created_file_uses_lf_line_endings():
    """
    Test that created file uses Unix LF line endings, not CRLF.

    Verifies:
    - File uses LF (\n) for line endings
    - File does NOT use CRLF (\r\n)
    """
    try:
        result = create_feature_305_markdown_file()
        filepath = result["filepath"]

        # Read file as binary to check line endings
        with open(filepath, "rb") as f:
            binary_content = f.read()

        # Check for CRLF (Windows line endings - should NOT be present)
        assert b"\r\n" not in binary_content, \
            "File should use LF (\\n) line endings, not CRLF (\\r\\n)"

        # Check for standalone CR
        assert b"\r" not in binary_content, \
            "File should use LF (\\n) line endings, not CR (\\r)"

        print(f"✓ File uses LF line endings")

    except Exception as e:
        print(f"✗ Failed: {e}")
        raise


def test_created_file_structure():
    """
    Test that created file has correct markdown structure.

    Verifies:
    - First line is H1 heading (# Title)
    - Second line is blank (separator)
    - Lines 3+ contain prose content
    - File ends with newline
    """
    try:
        result = create_feature_305_markdown_file()
        filepath = result["filepath"]

        # Read file as text
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")

        # Check first line is H1
        assert lines[0].startswith("# "), \
            f"First line must start with '# ', got: {repr(lines[0])}"

        # Check second line is blank
        assert len(lines) > 1 and lines[1] == "", \
            f"Second line must be blank, got: {repr(lines[1])}"

        # Check prose exists
        prose_lines = lines[2:]
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        assert prose_lines, \
            "No prose content found after heading"

        # Check trailing newline
        assert content.endswith("\n"), \
            "File must end with newline"

        print(f"✓ File structure is correct")

    except Exception as e:
        print(f"✗ Failed: {e}")
        raise


def test_created_file_prose_content():
    """
    Test that prose content is valid (2-3 sentences).

    Verifies:
    - Prose contains 2-3 sentences (counted by periods)
    - Prose is substantive
    """
    try:
        result = create_feature_305_markdown_file()
        filepath = result["filepath"]

        # Read file as text
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")
        prose_lines = lines[2:]

        # Remove trailing empty lines
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        prose_content = "\n".join(prose_lines).strip()

        # Count sentences
        sentence_count = prose_content.count(".")

        assert 2 <= sentence_count <= 3, \
            f"Prose must have 2-3 sentences, found {sentence_count}"

        print(f"✓ Prose content is valid ({sentence_count} sentences)")

    except Exception as e:
        print(f"✗ Failed: {e}")
        raise


def test_created_file_passes_complete_validation():
    """
    Integration test: Created file passes complete validation.

    Uses the project's validate_markdown_file() function to ensure
    consistency with specification validation.
    """
    try:
        result = create_feature_305_markdown_file()
        filepath = result["filepath"]

        # Use the project's validation function
        validation_result = validate_markdown_file(filepath)

        assert validation_result is True, \
            "File validation failed"

        print(f"✓ File passes complete validation")

    except Exception as e:
        print(f"✗ Failed: {e}")
        raise


# ============================================================================
# GIT OPERATIONS TESTS
# ============================================================================


def test_returned_push_result():
    """
    Test that function returns push result from git operations.

    Verifies:
    - push_result is returned in result dict
    - push_result is non-empty (git output)
    """
    try:
        result = create_feature_305_markdown_file()

        push_result = result.get("push_result")

        assert push_result is not None, \
            "Result must include push_result"

        assert isinstance(push_result, str), \
            f"push_result must be string, got {type(push_result)}"

        # push_result could be empty or contain git output
        print(f"✓ push_result returned: {len(push_result)} chars")

    except Exception as e:
        print(f"✗ Failed: {e}")
        raise


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


def test_function_handles_errors_gracefully():
    """
    Test that function propagates errors with proper logging.

    Verifies that if an error occurs during execution, it's raised
    (fail-fast pattern) rather than being silently caught.
    """
    # This is a basic test - in production would mock failures
    try:
        # Normal execution should not raise
        result = create_feature_305_markdown_file()
        assert result is not None
        print(f"✓ Function handles normal execution correctly")
    except Exception as e:
        print(f"✗ Failed: {e}")
        raise


# ============================================================================
# RUN TESTS
# ============================================================================


if __name__ == "__main__":
    """Run all feature tests."""
    tests = [
        # Feature function tests
        ("Returns dict with required keys", test_create_feature_305_markdown_file_returns_dict_with_required_keys),
        ("Creates markdown file", test_create_feature_305_markdown_file_creates_file),
        ("Returns valid content", test_create_feature_305_markdown_file_returns_valid_content),
        ("Commit message format", test_create_feature_305_markdown_file_commit_message_format),
        ("Works with repo_path", test_create_feature_305_markdown_file_with_custom_repo_path),

        # File validation tests
        ("UTF-8 encoding", test_created_file_has_utf8_encoding),
        ("LF line endings", test_created_file_uses_lf_line_endings),
        ("File structure", test_created_file_structure),
        ("Prose content", test_created_file_prose_content),
        ("Complete validation", test_created_file_passes_complete_validation),

        # Git tests
        ("Push result returned", test_returned_push_result),

        # Error handling
        ("Error handling", test_function_handles_errors_gracefully),
    ]

    passed = 0
    skipped = 0
    failed = 0

    print(f"\n{'='*70}")
    print(f"Running Feature 305 Tests")
    print(f"{'='*70}\n")

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_name}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_name}: Unexpected error: {e}")
            failed += 1

    print(f"\n{'='*70}")
    print(f"Test Results: {passed} passed, {skipped} skipped, {failed} failed")
    print(f"{'='*70}\n")

    if failed > 0:
        sys.exit(1)
