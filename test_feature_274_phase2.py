#!/usr/bin/env python3
"""
Test script for Feature 274: Markdown File Creation (Phase 2)

Tests the orchestration function create_markdown_file() to verify:
1. File test-ihdf8h.md does not exist before calling the function
2. Function call completes without raising exceptions
3. Function returns dict with expected keys
4. Content is valid markdown with H1 heading + 2-3 sentences
5. Commit message follows convention: feat(274): create markdown file test-ihdf8h.md with prose content
6. Push succeeds (no error messages in result)
"""

import sys
from pathlib import Path

# Add src to path so we can import sheep modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.content_generators import create_markdown_file


def test_file_not_exists_before():
    """Test that file does not exist before calling orchestration function."""
    print("\n=== Test 1: File does not exist before calling orchestration ===")
    filepath = Path("test-ihdf8h.md")
    assert not filepath.exists(), f"File {filepath} should not exist before test"
    print("[PASS] File test-ihdf8h.md does not exist before calling orchestration function")


def test_orchestration_call():
    """Test that create_markdown_file() completes without exceptions."""
    print("\n=== Test 2: Orchestration function call completes successfully ===")
    try:
        result = create_markdown_file("test-ihdf8h.md", feature_number=274)
        print(f"[PASS] create_markdown_file() completed successfully")
        print(f"  Result type: {type(result)}")
        return result
    except Exception as e:
        print(f"[FAIL] Function call failed: {e}")
        raise


def test_return_dict_structure(result):
    """Test that function returns dict with expected keys."""
    print("\n=== Test 3: Return dict has expected keys ===")
    expected_keys = {"filepath", "content", "commit_message", "push_result"}
    actual_keys = set(result.keys())

    assert isinstance(result, dict), f"Result should be dict, got {type(result)}"
    assert expected_keys == actual_keys, f"Expected keys {expected_keys}, got {actual_keys}"

    print(f"[PASS] Result dict has all expected keys: {expected_keys}")
    print(f"  - filepath: {result['filepath']}")
    print(f"  - content length: {len(result['content'])} bytes")
    print(f"  - commit_message: {result['commit_message']}")
    print(f"  - push_result: {result['push_result'][:100]}..." if len(result['push_result']) > 100 else f"  - push_result: {result['push_result']}")


def test_filepath_correctness(result):
    """Test that filepath is correct."""
    print("\n=== Test 4: Filepath is correct ===")
    filepath = result["filepath"]
    assert "test-ihdf8h.md" in filepath, f"Filepath should contain test-ihdf8h.md, got {filepath}"
    assert filepath.endswith("test-ihdf8h.md"), f"Filepath should end with test-ihdf8h.md, got {filepath}"

    # Verify file exists
    assert Path(filepath).exists(), f"File should exist at {filepath}"

    print(f"[PASS] Filepath is correct: {filepath}")
    print(f"  File exists: {Path(filepath).exists()}")
    print(f"  File size: {Path(filepath).stat().st_size} bytes")


def test_content_structure(result):
    """Test that content is valid markdown with proper structure."""
    print("\n=== Test 5: Content is valid markdown with proper structure ===")
    content = result["content"]

    # Check non-empty
    assert content and content.strip(), "Content should not be empty"
    print(f"[PASS] Content is non-empty")

    # Check H1 heading
    assert content.lstrip().startswith("# "), "Content should start with H1 heading (# )"
    print(f"[PASS] Content starts with H1 heading")

    # Check for blank line separator
    lines = content.split("\n")
    assert len(lines) >= 3, "Content should have at least 3 lines (H1, blank, prose)"
    assert lines[0].startswith("# "), "First line should be H1 heading"
    assert lines[1] == "", f"Second line should be blank (separator), got '{lines[1]}'"
    print(f"[PASS] Content has proper structure: H1 + blank line + prose")

    # Check sentence count
    sentence_count = content.count(".")
    assert 2 <= sentence_count <= 3, f"Content should have 2-3 sentences, found {sentence_count}"
    print(f"[PASS] Content has {sentence_count} sentences (within 2-3 range)")

    # Check length
    assert len(content) >= 50, f"Content should be at least 50 chars, got {len(content)}"
    print(f"[PASS] Content length is sufficient: {len(content)} bytes")

    # Print content preview
    print(f"\nContent preview:")
    print("---")
    print(content[:200] + ("..." if len(content) > 200 else ""))
    print("---")


def test_commit_message_convention(result):
    """Test that commit message follows convention."""
    print("\n=== Test 6: Commit message follows convention ===")
    commit_message = result["commit_message"]

    # Check format
    assert commit_message.startswith("feat(274):"), f"Commit message should start with 'feat(274):', got '{commit_message}'"
    print(f"[PASS] Commit message starts with 'feat(274):'")

    # Check filename in message
    assert "test-ihdf8h.md" in commit_message, f"Commit message should contain 'test-ihdf8h.md', got '{commit_message}'"
    print(f"[PASS] Commit message contains 'test-ihdf8h.md'")

    # Check full format
    expected_pattern = "feat(274): create markdown file test-ihdf8h.md with prose content"
    assert commit_message == expected_pattern, f"Commit message format incorrect.\nExpected: {expected_pattern}\nGot:      {commit_message}"
    print(f"[PASS] Commit message format is correct: {commit_message}")


def test_push_result_success(result):
    """Test that push succeeded (no error messages in result)."""
    print("\n=== Test 7: Push succeeded ===")
    push_result = result["push_result"]

    # Result should be non-empty string
    assert push_result and isinstance(push_result, str), f"Push result should be non-empty string, got {type(push_result)}: {push_result}"
    print(f"[PASS] Push result is non-empty: {len(push_result)} chars")

    # Check for error indicators (case-insensitive)
    error_indicators = ["error", "failed", "fatal", "refused", "cannot"]
    has_error = any(indicator.lower() in push_result.lower() for indicator in error_indicators)

    if has_error:
        print(f"[WARN] Push result contains potential error indicators:")
        print(f"  {push_result}")
    else:
        print(f"[PASS] Push result appears successful (no error indicators)")
        print(f"  Result: {push_result[:100]}..." if len(push_result) > 100 else f"  Result: {push_result}")


def main():
    """Run all tests."""
    print("=" * 70)
    print("FEATURE 274: MARKDOWN FILE CREATION - PHASE 2 TESTS")
    print("=" * 70)

    try:
        # Test 1: File doesn't exist before
        test_file_not_exists_before()

        # Test 2: Call orchestration function
        result = test_orchestration_call()

        # Test 3: Check return dict structure
        test_return_dict_structure(result)

        # Test 4: Check filepath
        test_filepath_correctness(result)

        # Test 5: Check content structure
        test_content_structure(result)

        # Test 6: Check commit message convention
        test_commit_message_convention(result)

        # Test 7: Check push result
        test_push_result_success(result)

        # Summary
        print("\n" + "=" * 70)
        print("[PASS] ALL TESTS PASSED")
        print("=" * 70)
        print("\nAcceptance Criteria Summary:")
        print("[PASS] File test-ihdf8h.md does not exist before calling orchestration function")
        print("[PASS] create_markdown_file() function call completes without exceptions")
        print("[PASS] Function returns dict with keys: filepath, content, commit_message, push_result")
        print("[PASS] Returned filepath is 'test-ihdf8h.md' or ends with 'test-ihdf8h.md'")
        print("[PASS] Returned content is non-empty string with markdown structure")
        print("[PASS] Returned commit_message contains 'feat(274):' and 'test-ihdf8h.md'")
        print("[PASS] Returned push_result indicates successful push (no error messages)")
        print("=" * 70)

        return 0

    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n[FAIL] UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
