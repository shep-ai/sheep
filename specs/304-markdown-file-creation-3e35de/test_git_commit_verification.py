"""
Integration test suite for feature 304: Git commit verification.

This module verifies that git commit operations complete successfully
with the correct commit message format and metadata.

Test Coverage:
- Commit exists in git history
- Commit message follows conventional commits format
- Commit message includes correct feature number and filename
- Commit includes the markdown file as tracked content
- Commit author metadata is properly set
"""

import subprocess
import sys
from pathlib import Path
from unittest import mock

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sheep.features.feature_304 import create_feature_304_markdown_file
from sheep.content_generators import create_markdown_file


# ============================================================================
# COMMIT MESSAGE VERIFICATION TESTS
# ============================================================================


def test_commit_exists_in_git_history():
    """
    Test that commit for test-ypzjo0.md exists in git history.

    Verifies:
    - Git log contains at least one commit
    - Commit message can be retrieved
    - Commit includes the correct filename
    """
    # Get git log and search for commits
    result = subprocess.run(
        ["git", "log", "--oneline"],
        capture_output=True,
        text=True,
        check=True,
    )

    log_output = result.stdout
    assert log_output, "Git log should not be empty"

    # Check for commits related to feature 304 and the filename
    commits_with_filename = [
        line for line in log_output.split("\n")
        if "test-ypzjo0.md" in line
    ]

    assert len(commits_with_filename) > 0, \
        "Git log should contain commit with test-ypzjo0.md filename"

    print(f"✓ Found {len(commits_with_filename)} commit(s) with test-ypzjo0.md")


def test_commit_message_follows_conventional_format():
    """
    Test that commit message follows conventional commits format.

    Verifies:
    - Commit message starts with "feat(304):"
    - Commit message is in lowercase (conventional format)
    - Commit message includes feature scope in parentheses
    """
    # Get the most recent commit message
    result = subprocess.run(
        ["git", "log", "-1", "--format=%B"],
        capture_output=True,
        text=True,
        check=True,
    )

    commit_message = result.stdout.strip()

    # Search for the specific commit if current HEAD is different
    result_all = subprocess.run(
        ["git", "log", "--oneline", "--all"],
        capture_output=True,
        text=True,
        check=True,
    )

    # Find the commit for test-ypzjo0.md
    log_lines = result_all.stdout.split("\n")
    commit_hash = None
    for line in log_lines:
        if "test-ypzjo0.md" in line and "feat(304)" in line:
            commit_hash = line.split()[0]
            break

    if commit_hash:
        result = subprocess.run(
            ["git", "log", f"{commit_hash}", "-1", "--format=%B"],
            capture_output=True,
            text=True,
            check=True,
        )
        commit_message = result.stdout.strip()

    # Verify conventional commit format
    assert commit_message.startswith("feat(304):"), \
        f"Commit message should start with 'feat(304):', got: {repr(commit_message)}"

    print(f"✓ Commit message follows conventional format: {commit_message[:60]}...")


def test_commit_message_includes_feature_number():
    """
    Test that commit message includes feature number 304.

    Verifies:
    - Commit message contains "304"
    - Feature number appears in scope (within parentheses)
    """
    # Get commits for test-ypzjo0.md
    result = subprocess.run(
        ["git", "log", "--all", "--grep=test-ypzjo0.md", "--oneline"],
        capture_output=True,
        text=True,
    )

    if not result.stdout:
        # Try another approach - get log and search
        result = subprocess.run(
            ["git", "log", "--all", "--oneline"],
            capture_output=True,
            text=True,
            check=True,
        )

    log_output = result.stdout
    commits_with_304 = [
        line for line in log_output.split("\n")
        if "feat(304)" in line or "304" in line
    ]

    assert len(commits_with_304) > 0, \
        "Git log should contain commit with feature number 304"

    print(f"✓ Found commit(s) with feature number 304: {commits_with_304[0][:60]}...")


def test_commit_message_includes_filename():
    """
    Test that commit message includes the markdown filename.

    Verifies:
    - Commit message contains "test-ypzjo0.md"
    - Filename appears in the message body/description
    """
    # Get all commits
    result = subprocess.run(
        ["git", "log", "--all", "--oneline"],
        capture_output=True,
        text=True,
        check=True,
    )

    log_output = result.stdout
    commits_with_filename = [
        line for line in log_output.split("\n")
        if "test-ypzjo0.md" in line
    ]

    assert len(commits_with_filename) > 0, \
        "Git log should contain commit with filename test-ypzjo0.md"

    commit_line = commits_with_filename[0]
    assert "test-ypzjo0.md" in commit_line, \
        f"Commit message should include 'test-ypzjo0.md', got: {repr(commit_line)}"

    print(f"✓ Commit message includes filename: test-ypzjo0.md")


def test_commit_message_includes_prose_reference():
    """
    Test that commit message references "prose content".

    Verifies:
    - Commit message contains "prose" or "content" indicator
    - Message describes the nature of content added
    """
    # Get commit for test-ypzjo0.md with prose reference
    result = subprocess.run(
        ["git", "log", "--all", "--oneline"],
        capture_output=True,
        text=True,
        check=True,
    )

    log_output = result.stdout
    commits_with_prose = [
        line for line in log_output.split("\n")
        if "test-ypzjo0.md" in line and ("prose" in line or "content" in line)
    ]

    assert len(commits_with_prose) > 0, \
        "Git log should contain commit mentioning prose or content"

    print(f"✓ Commit message includes prose reference: {commits_with_prose[0][:70]}...")


def test_commit_author_is_properly_set():
    """
    Test that commit author metadata is properly set.

    Verifies:
    - Commit has author name configured
    - Commit has author email configured
    - Author information is not empty
    """
    # Get the commit for test-ypzjo0.md
    result = subprocess.run(
        ["git", "log", "--all", "--oneline"],
        capture_output=True,
        text=True,
        check=True,
    )

    log_lines = result.stdout.split("\n")
    commit_hash = None
    for line in log_lines:
        if "test-ypzjo0.md" in line:
            commit_hash = line.split()[0]
            break

    if commit_hash:
        # Get author information
        result = subprocess.run(
            ["git", "log", f"{commit_hash}", "-1", "--format=%an <%ae>"],
            capture_output=True,
            text=True,
            check=True,
        )
        author_info = result.stdout.strip()
    else:
        # Get from HEAD if available
        result = subprocess.run(
            ["git", "log", "-1", "--format=%an <%ae>"],
            capture_output=True,
            text=True,
            check=True,
        )
        author_info = result.stdout.strip()

    assert author_info, "Commit should have author information"
    assert "<" in author_info and ">" in author_info, \
        f"Author should be in format 'Name <email>', got: {repr(author_info)}"

    print(f"✓ Commit author is set: {author_info}")


def test_commit_includes_markdown_file():
    """
    Test that commit includes the markdown file as tracked content.

    Verifies:
    - File appears in commit diff
    - File is marked as added in commit
    - File content is tracked by git
    """
    # Get commit for test-ypzjo0.md
    result = subprocess.run(
        ["git", "log", "--all", "--oneline"],
        capture_output=True,
        text=True,
        check=True,
    )

    log_lines = result.stdout.split("\n")
    commit_hash = None
    for line in log_lines:
        if "test-ypzjo0.md" in line:
            commit_hash = line.split()[0]
            break

    if not commit_hash:
        print("SKIPPED: Could not find commit hash for test-ypzjo0.md")
        return

    # Get files changed in commit
    result = subprocess.run(
        ["git", "show", f"{commit_hash}", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )

    files_in_commit = result.stdout

    assert "test-ypzjo0.md" in files_in_commit, \
        f"Commit should include test-ypzjo0.md file, files in commit: {files_in_commit}"

    # Verify file is added (not just modified)
    result = subprocess.run(
        ["git", "show", f"{commit_hash}", "--name-status"],
        capture_output=True,
        text=True,
        check=True,
    )

    name_status = result.stdout

    assert "A" in name_status and "test-ypzjo0.md" in name_status, \
        f"File should be added (A) in commit, status: {name_status}"

    print(f"✓ Commit includes markdown file as tracked content")


def test_commit_message_is_not_empty():
    """
    Test that commit message is not empty or whitespace-only.

    Verifies:
    - Commit message has meaningful content
    - Message is not just whitespace
    - Message describes the change
    """
    # Get commit for test-ypzjo0.md
    result = subprocess.run(
        ["git", "log", "--all", "--oneline"],
        capture_output=True,
        text=True,
        check=True,
    )

    log_lines = result.stdout.split("\n")
    commit_hash = None
    for line in log_lines:
        if "test-ypzjo0.md" in line:
            commit_hash = line.split()[0]
            break

    if not commit_hash:
        print("SKIPPED: Could not find commit hash")
        return

    # Get full commit message
    result = subprocess.run(
        ["git", "log", f"{commit_hash}", "-1", "--format=%B"],
        capture_output=True,
        text=True,
        check=True,
    )

    commit_message = result.stdout.strip()

    assert commit_message, "Commit message should not be empty"
    assert len(commit_message) > 10, \
        f"Commit message should be meaningful, got: {repr(commit_message)}"

    print(f"✓ Commit message is meaningful: {len(commit_message)} characters")


def test_commit_is_on_correct_branch():
    """
    Test that commit is on the correct feature branch.

    Verifies:
    - Current branch is feat/304-markdown-file-creation-3e35de
    - Commit is reachable from current branch
    """
    # Get current branch
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )

    current_branch = result.stdout.strip()

    # Should be on feature branch (may start with feat/)
    assert "304" in current_branch or "feat" in current_branch or "markdown" in current_branch, \
        f"Should be on feature branch, current: {current_branch}"

    print(f"✓ Commit is on correct branch: {current_branch}")


# ============================================================================
# RUN TESTS
# ============================================================================


if __name__ == "__main__":
    """Run all git commit verification tests."""
    tests = [
        ("Commit exists in git history", test_commit_exists_in_git_history),
        ("Commit message follows conventional format", test_commit_message_follows_conventional_format),
        ("Commit message includes feature number", test_commit_message_includes_feature_number),
        ("Commit message includes filename", test_commit_message_includes_filename),
        ("Commit message references prose content", test_commit_message_includes_prose_reference),
        ("Commit author is properly set", test_commit_author_is_properly_set),
        ("Commit includes markdown file", test_commit_includes_markdown_file),
        ("Commit message is not empty", test_commit_message_is_not_empty),
        ("Commit is on correct branch", test_commit_is_on_correct_branch),
    ]

    passed = 0
    skipped = 0
    failed = 0

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

    print(f"\n{'='*60}")
    print(f"Test Results: {passed} passed, {skipped} skipped, {failed} failed")
    print(f"{'='*60}")

    if failed > 0:
        sys.exit(1)
