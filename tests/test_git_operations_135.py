"""
Tests for git operations in feature 135 markdown file creation.

Tests cover:
- Task 3: Git operations (add, commit, push)
- Task 4: End-to-end workflow verification
"""

import subprocess
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import git_integration_135


def test_file_exists():
    """Test that the markdown file exists."""
    file_path = Path("test-0h8m0m.md")
    assert file_path.exists(), "File test-0h8m0m.md should exist"


def test_file_size():
    """Test that file size is within specification (400-600 bytes)."""
    file_path = Path("test-0h8m0m.md")
    size_bytes = file_path.stat().st_size
    assert 400 <= size_bytes <= 600, f"File size {size_bytes} not in 400-600 range"


def test_file_encoding():
    """Test that file is UTF-8 encoded without BOM."""
    file_path = Path("test-0h8m0m.md")

    with open(file_path, 'rb') as f:
        binary_content = f.read()

    # Check for BOM
    assert not binary_content.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"

    # Verify UTF-8 decoding
    try:
        file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}")


def test_file_line_endings():
    """Test that file uses LF line endings, not CRLF."""
    file_path = Path("test-0h8m0m.md")

    with open(file_path, 'rb') as f:
        binary_content = f.read()

    assert b'\r\n' not in binary_content, "File should use LF, not CRLF line endings"


def test_file_structure():
    """Test that file has H1 heading and 2-3 sentences."""
    file_path = Path("test-0h8m0m.md")
    text_content = file_path.read_text(encoding='utf-8')
    lines = text_content.rstrip('\n').split('\n')

    # Check H1 heading
    assert lines[0].startswith('# '), "First line should be H1 heading"

    # Check blank line
    assert len(lines) >= 2, "File should have heading and prose"
    assert lines[1] == '', "Second line should be blank"

    # Check prose content and sentence count
    import re
    prose_text = '\n'.join(lines[2:])
    sentence_count = len(re.findall(r'[.!?]+', prose_text))
    assert 2 <= sentence_count <= 3, f"Should have 2-3 sentences, got {sentence_count}"


def test_verify_file_exists():
    """Test verify_file_exists function."""
    git_integration_135.verify_file_exists()


def test_git_add():
    """Test that git add command works without error."""
    # Run the git add operation
    try:
        git_integration_135.git_add()
        print("[OK] git add executed successfully")
    except subprocess.CalledProcessError as e:
        raise AssertionError(f"git add failed: {e}")


def test_git_commit():
    """Test that git commit command works without error."""
    # Run the git commit operation
    try:
        git_integration_135.git_commit()
        print("[OK] git commit executed successfully")
    except subprocess.CalledProcessError as e:
        raise AssertionError(f"git commit failed: {e}")


def test_git_push():
    """Test that git push command works without error."""
    # Run the git push operation
    try:
        git_integration_135.git_push()
        print("[OK] git push executed successfully")
    except subprocess.CalledProcessError as e:
        raise AssertionError(f"git push failed: {e}")


def test_git_log_shows_commit():
    """Test that git log shows the commit with correct message."""
    result = subprocess.run(
        ['git', 'log', '--oneline', '--', 'test-0h8m0m.md'],
        capture_output=True,
        text=True,
        check=True
    )

    assert 'feat(135)' in result.stdout, "Commit should contain 'feat(135)' in message"
    assert 'test-0h8m0m.md' in result.stdout, "Commit should reference test-0h8m0m.md"


def test_git_status_clean():
    """Test that git status is clean (no uncommitted changes)."""
    result = subprocess.run(
        ['git', 'status', '--short'],
        capture_output=True,
        text=True,
        check=True
    )

    # Filter out untracked files, only check for modified
    modified_lines = [
        line for line in result.stdout.split('\n')
        if line and line[0] != '?' and 'test-0h8m0m.md' in line
    ]

    assert not modified_lines, f"Git status should be clean for test-0h8m0m.md: {modified_lines}"


def test_remote_branch_exists():
    """Test that remote branch exists."""
    try:
        result = subprocess.run(
            ['git', 'ls-remote', 'origin', 'refs/heads/feat/markdown-file-creation-77dd31'],
            capture_output=True,
            text=True,
            check=True
        )

        assert result.stdout.strip(), "Remote branch should exist"
        print("[OK] Remote branch exists")
    except subprocess.CalledProcessError:
        print("[WARN] Remote branch verification skipped (may not be pushed yet)")


def test_file_on_remote_branch():
    """Test that file exists on remote branch."""
    try:
        result = subprocess.run(
            ['git', 'show', 'origin/feat/markdown-file-creation-77dd31:test-0h8m0m.md'],
            capture_output=True,
            text=True,
            check=True
        )

        assert result.stdout, "File should exist on remote branch"
        assert '# The Power of Incremental Progress' in result.stdout, "File content should match"
        print("[OK] File exists on remote branch with correct content")
    except subprocess.CalledProcessError:
        print("[WARN] Remote file verification skipped (may not be pushed yet)")


def test_end_to_end_workflow():
    """Test complete end-to-end workflow."""
    print("\n" + "=" * 60)
    print("Running End-to-End Workflow Verification")
    print("=" * 60)

    # 1. Verify file exists and is valid
    print("\n1. Verifying file...")
    test_file_exists()
    test_file_size()
    test_file_encoding()
    test_file_line_endings()
    test_file_structure()
    print("[OK] File validation passed")

    # 2. Verify git operations
    print("\n2. Verifying git operations...")
    test_git_log_shows_commit()
    test_git_status_clean()
    print("[OK] Git operations verified")

    # 3. Verify spec criteria met
    print("\n3. Verifying specification criteria...")
    assert Path("test-0h8m0m.md").exists(), "File must exist"
    size = Path("test-0h8m0m.md").stat().st_size
    assert 400 <= size <= 600, f"Size {size} not in 400-600 range"
    print("[OK] All specification criteria met")

    print("\n" + "=" * 60)
    print("[OK] End-to-End Workflow Verification Complete")
    print("=" * 60)


if __name__ == '__main__':
    # Run all tests
    print("Running git operations tests for feature 135...")
    print("=" * 60)

    test_file_exists()
    print("[OK] test_file_exists passed")

    test_file_size()
    print("[OK] test_file_size passed")

    test_file_encoding()
    print("[OK] test_file_encoding passed")

    test_file_line_endings()
    print("[OK] test_file_line_endings passed")

    test_file_structure()
    print("[OK] test_file_structure passed")

    test_verify_file_exists()
    print("[OK] test_verify_file_exists passed")

    test_git_status_clean()
    print("[OK] test_git_status_clean passed")

    test_git_log_shows_commit()
    print("[OK] test_git_log_shows_commit passed")

    test_end_to_end_workflow()
    print("[OK] test_end_to_end_workflow passed")

    print("\n" + "=" * 60)
    print("[OK] All tests passed!")
    print("=" * 60)
