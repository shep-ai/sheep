#!/usr/bin/env python3
"""
Test suite for Phase 2: Git Integration and Push

Tests verify that all git operations (add, commit, push) have been completed
successfully and meet acceptance criteria.

Tests cover:
- Task 4: File is staged in git (git add)
- Task 5: File is committed with conventional message
- Task 6: Commit is pushed to remote feature branch
"""

import re
import subprocess
import sys
from pathlib import Path


class TestPhase2GitIntegration:
    """Test suite for git integration and push operations."""

    FILENAME = "test-xoqnko.md"
    EXPECTED_COMMIT_MESSAGE = "feat(251): create markdown file test-xoqnko.md with prose content"
    EXPECTED_BRANCH = "feat/251-markdown-file-creation-5b29b2"
    COMMIT_MESSAGE_PATTERN = re.compile(r"^feat\(251\): create markdown file test-xoqnko\.md with prose content$")

    @staticmethod
    def run_git_command(cmd_list):
        """
        Execute a git command safely.

        Args:
            cmd_list: List of command arguments (e.g., ['git', 'status'])

        Returns:
            tuple: (return_code, stdout, stderr)
        """
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
        )
        return result.returncode, result.stdout, result.stderr

    def test_file_exists(self):
        """Test that test-xoqnko.md exists in repository root."""
        file_path = Path(self.FILENAME)
        assert file_path.exists(), f"File {self.FILENAME} does not exist"
        print(f"[PASS] File exists: {self.FILENAME}")

    def test_file_is_in_git_index(self):
        """Test that file is tracked by git (in index)."""
        returncode, stdout, stderr = self.run_git_command(["git", "ls-files", self.FILENAME])
        assert returncode == 0, f"git ls-files failed: {stderr}"
        assert self.FILENAME in stdout, f"File {self.FILENAME} is not in git index"
        print(f"[PASS] File is tracked by git: {self.FILENAME}")

    def test_file_is_not_untracked(self):
        """Test that file does not appear as untracked in git status."""
        returncode, stdout, stderr = self.run_git_command(["git", "status", "--porcelain"])
        assert returncode == 0, f"git status failed: {stderr}"
        # If file appears with "??" it's untracked
        for line in stdout.split("\n"):
            if self.FILENAME in line:
                assert not line.startswith("??"), f"File {self.FILENAME} is untracked"
        print(f"[PASS] File is not untracked in git status")

    def test_commit_message_format(self):
        """Test that commit message follows conventional commit format."""
        # Find the commit that created test-xoqnko.md
        returncode, stdout, stderr = self.run_git_command(
            ["git", "log", "--pretty=format:%s", "--", self.FILENAME]
        )
        assert returncode == 0, f"git log failed: {stderr}"
        commit_messages = stdout.strip().split("\n")
        assert len(commit_messages) > 0, f"No commits found for {self.FILENAME}"

        # Check that at least one commit message matches expected format
        found_matching_message = False
        for msg in commit_messages:
            if self.COMMIT_MESSAGE_PATTERN.match(msg):
                found_matching_message = True
                print(f"[PASS] Found commit with expected message: {msg}")
                break

        assert found_matching_message, (
            f"No commit found with message matching pattern: {self.COMMIT_MESSAGE_PATTERN.pattern}\n"
            f"Commits found: {commit_messages}"
        )

    def test_commit_contains_feature_number(self):
        """Test that commit message contains feature number (251)."""
        returncode, stdout, stderr = self.run_git_command(
            ["git", "log", "--pretty=format:%s", "--", self.FILENAME]
        )
        assert returncode == 0, f"git log failed: {stderr}"
        commit_messages = stdout.strip().split("\n")

        found_feature_number = False
        for msg in commit_messages:
            if "(251)" in msg:
                found_feature_number = True
                break

        assert found_feature_number, f"No commit message contains feature number (251)"
        print(f"[PASS] Commit message contains feature number (251)")

    def test_file_not_modified(self):
        """Test that file has no uncommitted modifications."""
        returncode, stdout, stderr = self.run_git_command(["git", "status", "--porcelain"])
        assert returncode == 0, f"git status failed: {stderr}"

        # File should not appear with "M" (modified) or "D" (deleted) or "??" (untracked)
        for line in stdout.split("\n"):
            if self.FILENAME in line:
                assert not line.startswith("M "), f"File {self.FILENAME} has uncommitted modifications"
                assert not line.startswith("D "), f"File {self.FILENAME} is deleted"
                assert not line.startswith("??"), f"File {self.FILENAME} is untracked"

        print(f"[PASS] File has no uncommitted modifications")

    def test_commit_exists_in_log(self):
        """Test that commit exists in git log."""
        returncode, stdout, stderr = self.run_git_command(["git", "log", "--oneline"])
        assert returncode == 0, f"git log failed: {stderr}"

        # Look for the commit that mentions test-xoqnko.md
        found_commit = False
        for line in stdout.split("\n"):
            if "test-xoqnko.md" in line and "251" in line:
                found_commit = True
                print(f"[PASS] Found commit in git log: {line}")
                break

        assert found_commit, f"Commit for {self.FILENAME} not found in git log"

    def test_file_is_on_remote(self):
        """Test that commit is present on remote branch."""
        # Get current branch name to check correct remote
        returncode, branch_name, stderr = self.run_git_command(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        )
        assert returncode == 0, f"git rev-parse failed: {stderr}"
        branch_name = branch_name.strip()

        # Try the current branch remote first
        returncode, stdout, stderr = self.run_git_command(
            ["git", "log", "--oneline", f"origin/{branch_name}"]
        )

        # If that fails, try the feature branch directly
        if returncode != 0:
            returncode, stdout, stderr = self.run_git_command(
                ["git", "log", "--oneline", f"origin/{self.EXPECTED_BRANCH}"]
            )

        assert returncode == 0, f"git log failed: {stderr}"

        # Look for the commit that mentions test-xoqnko.md
        found_on_remote = False
        for line in stdout.split("\n"):
            if "test-xoqnko.md" in line and "251" in line:
                found_on_remote = True
                print(f"[PASS] Found commit on remote: {line}")
                break

        assert found_on_remote, f"Commit for {self.FILENAME} not found on remote branch"

    def test_branch_is_up_to_date(self):
        """Test that local branch is up-to-date with remote."""
        returncode, stdout, stderr = self.run_git_command(["git", "status", "--porcelain", "-b"])
        assert returncode == 0, f"git status failed: {stderr}"

        # First line contains branch info
        first_line = stdout.split("\n")[0] if stdout else ""

        # Should indicate branch is up-to-date with remote (no ahead/behind)
        # Format: "## branch_name...origin/branch_name" or "## branch_name...origin/branch_name [ahead N]" or "[behind N]"
        assert first_line.startswith("##"), "Could not parse branch status"

        # If branch is behind, commit hasn't been pushed yet
        assert "behind" not in first_line.lower(), (
            f"Local branch is behind remote: {first_line}. "
            "Commit has not been pushed to remote branch."
        )

        print(f"[PASS] Local branch is up-to-date with remote")

    def run_all_tests(self):
        """Execute all tests in sequence."""
        tests = [
            self.test_file_exists,
            self.test_file_is_in_git_index,
            self.test_file_is_not_untracked,
            self.test_commit_message_format,
            self.test_commit_contains_feature_number,
            self.test_file_not_modified,
            self.test_commit_exists_in_log,
            self.test_file_is_on_remote,
            self.test_branch_is_up_to_date,
        ]

        print("=" * 70)
        print("Phase 2 Git Integration Verification Tests")
        print("=" * 70)

        passed = 0
        failed = 0

        for test_func in tests:
            try:
                test_func()
                passed += 1
            except AssertionError as e:
                print(f"[FAIL] {test_func.__name__}: {e}", file=sys.stderr)
                failed += 1
            except Exception as e:
                print(f"[ERROR] {test_func.__name__}: {e}", file=sys.stderr)
                failed += 1

        print()
        print("=" * 70)
        print(f"Test Results: {passed} passed, {failed} failed")
        print("=" * 70)

        return failed == 0


def main():
    """Run all Phase 2 verification tests."""
    tester = TestPhase2GitIntegration()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
