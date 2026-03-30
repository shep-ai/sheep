#!/usr/bin/env python3
"""
Verification tests for feature 272: File content, encoding, and git integration.

This test suite validates all success criteria for the markdown file creation:
- File existence and location
- Content structure (H1 heading, 2-3 sentences)
- Encoding (UTF-8 without BOM)
- Line endings (Unix LF only)
- File size
- Git commit message format
- Git upstream tracking

Tasks covered:
- task-3: Verify File Content and Encoding
- task-4: Verify Git Commit and Push
"""

import re
import subprocess
from pathlib import Path


class TestFileContentAndEncoding:
    """Task-3: Verify file content and encoding requirements."""

    @staticmethod
    def test_file_exists():
        """Test that test-visstj.md exists at repository root."""
        filepath = Path.cwd() / "test-visstj.md"
        assert filepath.exists(), f"File {filepath} does not exist"
        print(f"✓ File exists at {filepath}")

    @staticmethod
    def test_file_has_h1_heading():
        """Test that file contains exactly one H1 heading (# Title)."""
        filepath = Path.cwd() / "test-visstj.md"
        content = filepath.read_text(encoding="utf-8")
        lines = content.split("\n")

        assert len(lines) > 0, "File is empty"
        first_line = lines[0]

        assert first_line.startswith("# "), f"First line is not H1 heading, got: {first_line}"
        assert len(first_line) > 2, "H1 heading has no title text"
        print(f"✓ File has H1 heading: {first_line}")

    @staticmethod
    def test_file_has_blank_line_separator():
        """Test that file has blank line separator after H1 heading."""
        filepath = Path.cwd() / "test-visstj.md"
        content = filepath.read_text(encoding="utf-8")
        lines = content.split("\n")

        assert len(lines) >= 2, "File does not have enough lines for blank separator"
        assert lines[1] == "", f"Second line is not blank, got: {lines[1]!r}"
        print("✓ File has blank line separator after heading")

    @staticmethod
    def test_file_has_prose_content():
        """Test that file contains prose content after blank line."""
        filepath = Path.cwd() / "test-visstj.md"
        content = filepath.read_text(encoding="utf-8")
        lines = content.split("\n")

        assert len(lines) > 2, "File does not have prose content after heading"
        prose = "\n".join(lines[2:]).strip()
        assert len(prose) > 0, "Prose content is empty"
        print(f"✓ File has prose content ({len(prose)} characters)")

    @staticmethod
    def test_file_has_2_to_3_sentences():
        """Test that file contains exactly 2-3 sentences in prose content."""
        filepath = Path.cwd() / "test-visstj.md"
        content = filepath.read_text(encoding="utf-8")
        lines = content.split("\n")

        prose = "\n".join(lines[2:]).strip()

        # Count sentences by periods (simple heuristic)
        sentence_count = prose.count(".")

        assert 2 <= sentence_count <= 3, (
            f"Prose should have 2-3 sentences, found {sentence_count} periods. "
            f"Content: {prose}"
        )
        print(f"✓ File has {sentence_count} sentences")

    @staticmethod
    def test_file_utf8_no_bom():
        """Test that file uses UTF-8 encoding without BOM."""
        filepath = Path.cwd() / "test-visstj.md"

        # Read file in binary mode to check for BOM
        with open(filepath, "rb") as f:
            data = f.read()

        # UTF-8 BOM is 0xEF 0xBB 0xBF
        assert not data.startswith(b'\xef\xbb\xbf'), "File has UTF-8 BOM (should not have BOM)"

        # Verify file can be decoded as UTF-8
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as e:
            raise AssertionError(f"File is not valid UTF-8: {e}")

        print("✓ File uses UTF-8 encoding without BOM")

    @staticmethod
    def test_file_lf_line_endings():
        """Test that file uses Unix LF line endings, not CRLF."""
        filepath = Path.cwd() / "test-visstj.md"

        # Read file in binary mode to check line endings
        with open(filepath, "rb") as f:
            data = f.read()

        # Check for CRLF (0x0D 0x0A)
        assert b'\r\n' not in data, "File contains CRLF line endings (should be LF only)"

        # Verify no stray CR characters
        assert b'\r' not in data, "File contains CR characters (should be LF only)"

        print("✓ File uses Unix LF line endings")

    @staticmethod
    def test_file_trailing_newline():
        """Test that file ends with newline character."""
        filepath = Path.cwd() / "test-visstj.md"

        with open(filepath, "rb") as f:
            data = f.read()

        assert data.endswith(b'\n'), "File does not end with newline"
        print("✓ File ends with newline")

    @staticmethod
    def test_file_size_in_range():
        """Test that file size is approximately 250-600 bytes."""
        filepath = Path.cwd() / "test-visstj.md"

        file_size = filepath.stat().st_size
        assert 250 <= file_size <= 600, (
            f"File size {file_size} bytes is outside expected range (250-600 bytes)"
        )
        print(f"✓ File size is {file_size} bytes (within 250-600 byte range)")

    @staticmethod
    def test_markdown_structure_valid():
        """Test that markdown structure is valid per CommonMark."""
        filepath = Path.cwd() / "test-visstj.md"
        content = filepath.read_text(encoding="utf-8")

        # Basic CommonMark validation
        lines = content.split("\n")

        # Check H1 heading
        assert lines[0].startswith("# "), "Missing H1 heading"

        # Check blank line
        assert lines[1] == "", "Missing blank line separator"

        # Check prose
        prose = "\n".join(lines[2:]).strip()
        assert len(prose) > 0, "Missing prose content"

        # Check that prose doesn't have invalid markdown syntax
        # (basic check: no unmatched brackets, no invalid emphasis markers)
        assert prose.count("[") == prose.count("]"), "Unmatched brackets in prose"
        assert prose.count("(") == prose.count(")"), "Unmatched parentheses in prose"

        print("✓ Markdown structure is valid")


class TestGitCommitAndPush:
    """Task-4: Verify git commit message and push."""

    @staticmethod
    def test_commit_message_format():
        """Test that commit message follows conventional format."""
        # Get the most recent commit message
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=%B"],
            capture_output=True,
            text=True,
            check=True
        )
        commit_message = result.stdout.strip()

        # Pattern: feat(272): create markdown file test-visstj.md ...
        pattern = r"^feat\(272\):\s+create markdown file test-visstj\.md"
        assert re.match(pattern, commit_message), (
            f"Commit message does not match conventional format. "
            f"Expected pattern: 'feat(272): create markdown file test-visstj.md*'\n"
            f"Got: {commit_message}"
        )
        print(f"✓ Commit message follows conventional format: {commit_message.split(chr(10))[0]}")

    @staticmethod
    def test_only_test_visstj_modified():
        """Test that only test-visstj.md was modified in the commit."""
        # Get list of modified files in the most recent commit
        result = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:"],
            capture_output=True,
            text=True,
            check=True
        )

        modified_files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]

        assert len(modified_files) == 1, (
            f"Expected only 1 file modified, found {len(modified_files)}: {modified_files}"
        )
        assert modified_files[0] == "test-visstj.md", (
            f"Expected 'test-visstj.md' to be modified, found '{modified_files[0]}'"
        )
        print(f"✓ Only test-visstj.md was modified in commit")

    @staticmethod
    def test_current_branch_is_feature_branch():
        """Test that current branch is the feature branch."""
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        current_branch = result.stdout.strip()

        expected_branch = "feat/markdown-file-creation-e6052e"
        assert current_branch == expected_branch, (
            f"Current branch is '{current_branch}', expected '{expected_branch}'"
        )
        print(f"✓ Current branch is feature branch: {current_branch}")

    @staticmethod
    def test_upstream_tracking_set():
        """Test that branch has upstream tracking to origin."""
        result = subprocess.run(
            ["git", "branch", "-vv"],
            capture_output=True,
            text=True,
            check=True
        )
        branch_info = result.stdout

        # Look for current branch with upstream info
        current_branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        # Find the line with current branch
        for line in branch_info.split("\n"):
            if current_branch in line:
                # Check that it has upstream info
                assert "[origin/" in line, (
                    f"Branch {current_branch} does not have upstream tracking. "
                    f"Output: {line}"
                )
                print(f"✓ Branch has upstream tracking: {line.strip()}")
                return

        raise AssertionError(f"Could not find branch {current_branch} in git branch -vv output")

    @staticmethod
    def test_commit_on_feature_branch():
        """Test that the recent commit is on the feature branch."""
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=%D"],
            capture_output=True,
            text=True,
            check=True
        )
        branch_info = result.stdout.strip()

        # branch_info should contain the feature branch name or "HEAD -> feat/..."
        expected_pattern = "feat/272-markdown-file-creation-e6052e"
        assert expected_pattern in branch_info or "HEAD" in branch_info, (
            f"Commit does not appear to be on feature branch. "
            f"Branch info: {branch_info}"
        )
        print(f"✓ Commit is on feature branch")


def run_all_tests():
    """Run all verification tests."""
    print("=" * 70)
    print("VERIFICATION TESTS: Feature 272 - File Content, Encoding, and Git")
    print("=" * 70)

    # Task-3: File Content and Encoding
    print("\n[TASK-3] Verifying File Content and Encoding...")
    print("-" * 70)

    file_tests = [
        ("File exists", TestFileContentAndEncoding.test_file_exists),
        ("H1 heading present", TestFileContentAndEncoding.test_file_has_h1_heading),
        ("Blank line separator", TestFileContentAndEncoding.test_file_has_blank_line_separator),
        ("Prose content present", TestFileContentAndEncoding.test_file_has_prose_content),
        ("2-3 sentences", TestFileContentAndEncoding.test_file_has_2_to_3_sentences),
        ("UTF-8 without BOM", TestFileContentAndEncoding.test_file_utf8_no_bom),
        ("LF line endings", TestFileContentAndEncoding.test_file_lf_line_endings),
        ("Trailing newline", TestFileContentAndEncoding.test_file_trailing_newline),
        ("File size in range", TestFileContentAndEncoding.test_file_size_in_range),
        ("Markdown structure valid", TestFileContentAndEncoding.test_markdown_structure_valid),
    ]

    failed_tests = []
    for test_name, test_func in file_tests:
        try:
            test_func()
        except AssertionError as e:
            print(f"✗ {test_name}: {e}")
            failed_tests.append((test_name, str(e)))

    # Task-4: Git Commit and Push
    print("\n[TASK-4] Verifying Git Commit and Push...")
    print("-" * 70)

    git_tests = [
        ("Commit message format", TestGitCommitAndPush.test_commit_message_format),
        ("Only test-visstj.md modified", TestGitCommitAndPush.test_only_test_visstj_modified),
        ("Current branch is feature branch", TestGitCommitAndPush.test_current_branch_is_feature_branch),
        ("Upstream tracking set", TestGitCommitAndPush.test_upstream_tracking_set),
        ("Commit on feature branch", TestGitCommitAndPush.test_commit_on_feature_branch),
    ]

    for test_name, test_func in git_tests:
        try:
            test_func()
        except Exception as e:
            print(f"✗ {test_name}: {e}")
            failed_tests.append((test_name, str(e)))

    # Summary
    print("\n" + "=" * 70)
    if not failed_tests:
        print("SUCCESS: All verification tests passed!")
        print("=" * 70)
        return True
    else:
        print(f"FAILURE: {len(failed_tests)} test(s) failed:")
        for test_name, error in failed_tests:
            print(f"  - {test_name}")
        print("=" * 70)
        return False


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
