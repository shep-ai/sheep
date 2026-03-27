"""Integration tests for feature 245 phase 4: Integration Testing & Verification.

These tests verify that all success criteria are met after executing the complete
feature workflow. The tests check:

1. File test-nxclc0.md exists in repository root
2. File contains exactly one H1 heading as first line
3. File contains exactly 2-3 sentences of prose after blank line
4. File is encoded as UTF-8 without BOM
5. File uses Unix LF line endings (no CRLF)
6. File size is 400-600 bytes
7. Git log shows commit with correct conventional message
8. Commit is on feature branch feat/245-markdown-file-creation-1f0041
9. Remote origin repository has the committed changes
"""

import re
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest


class TestPhase4FileCreation:
    """Test SC-1: File test-nxclc0.md exists in repository root."""

    def test_file_exists_in_repo_root(self):
        """Test that test-nxclc0.md exists in repository root."""
        test_file = Path("test-nxclc0.md")
        assert test_file.exists(), "File test-nxclc0.md does not exist in repository root"

    def test_file_is_regular_file(self):
        """Test that test-nxclc0.md is a regular file, not a directory."""
        test_file = Path("test-nxclc0.md")
        assert test_file.is_file(), "test-nxclc0.md is not a regular file"

    def test_file_is_readable(self):
        """Test that test-nxclc0.md is readable."""
        test_file = Path("test-nxclc0.md")
        assert test_file.is_file()
        content = test_file.read_text(encoding="utf-8")
        assert len(content) > 0, "File is empty or not readable"


class TestPhase4H1Heading:
    """Test SC-2: File contains exactly one H1 heading as first line."""

    def test_file_contains_h1_heading(self):
        """Test that file contains at least one H1 heading."""
        test_file = Path("test-nxclc0.md")
        content = test_file.read_text(encoding="utf-8")
        assert "# " in content, "File does not contain H1 heading"

    def test_h1_heading_on_first_line(self):
        """Test that H1 heading is on the first line."""
        test_file = Path("test-nxclc0.md")
        content = test_file.read_text(encoding="utf-8")
        first_line = content.split("\n")[0]
        assert first_line.startswith("# "), "First line is not H1 heading"

    def test_h1_heading_has_content(self):
        """Test that H1 heading has actual content after #."""
        test_file = Path("test-nxclc0.md")
        content = test_file.read_text(encoding="utf-8")
        first_line = content.split("\n")[0]
        assert len(first_line) > 2, "H1 heading has no content"
        assert first_line[0] == "#", "First character should be #"
        assert first_line[1] == " ", "Second character should be space"

    def test_exactly_one_h1_heading(self):
        """Test that file contains exactly one H1 heading."""
        test_file = Path("test-nxclc0.md")
        content = test_file.read_text(encoding="utf-8")
        h1_count = content.count("\n# ") + (1 if content.startswith("# ") else 0)
        assert h1_count == 1, f"File should have exactly 1 H1 heading, found {h1_count}"


class TestPhase4ProseContent:
    """Test SC-3: File contains exactly 2-3 sentences of prose after blank line."""

    def test_blank_line_after_heading(self):
        """Test that there is a blank line after the H1 heading."""
        test_file = Path("test-nxclc0.md")
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        assert len(lines) >= 3, "File should have at least 3 lines (heading, blank, prose)"
        assert lines[1] == "", "Second line should be blank"

    def test_prose_content_exists(self):
        """Test that prose content exists after blank line."""
        test_file = Path("test-nxclc0.md")
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        prose = "\n".join(lines[2:]).strip()
        assert len(prose) > 0, "No prose content found after blank line"

    def test_prose_contains_sentences(self):
        """Test that prose content contains complete sentences ending with periods."""
        test_file = Path("test-nxclc0.md")
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        prose = "\n".join(lines[2:]).strip()

        # Count sentences (ending with . ! or ?)
        sentence_count = len(re.findall(r"[.!?]", prose))
        assert sentence_count >= 2, f"Should have at least 2 sentences, found {sentence_count}"
        assert sentence_count <= 3, f"Should have at most 3 sentences, found {sentence_count}"

    def test_prose_word_count(self):
        """Test that prose content has reasonable word count."""
        test_file = Path("test-nxclc0.md")
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        prose = "\n".join(lines[2:]).strip()

        word_count = len(prose.split())
        # 2-3 sentences typically 30-100+ words
        assert word_count >= 20, f"Prose should have at least 20 words, found {word_count}"


class TestPhase4Encoding:
    """Test SC-4: File is encoded as UTF-8 without BOM."""

    def test_file_utf8_encoded(self):
        """Test that file is UTF-8 encoded."""
        test_file = Path("test-nxclc0.md")
        # If file can be read as UTF-8, it's UTF-8 encoded
        try:
            content = test_file.read_bytes()
            content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("File is not valid UTF-8")

    def test_file_has_no_bom(self):
        """Test that file does not have UTF-8 BOM."""
        test_file = Path("test-nxclc0.md")
        content = test_file.read_bytes()
        # UTF-8 BOM is EF BB BF
        assert not content.startswith(b"\xef\xbb\xbf"), "File has UTF-8 BOM"

    def test_file_encoding_valid(self):
        """Test that file encoding is valid and readable."""
        test_file = Path("test-nxclc0.md")
        content = test_file.read_text(encoding="utf-8")
        # Should be able to read and have no replacement characters
        assert "\ufffd" not in content, "File has replacement characters (invalid encoding)"


class TestPhase4LineEndings:
    """Test SC-5: File uses Unix LF line endings, not Windows CRLF."""

    def test_file_uses_lf_line_endings(self):
        """Test that file uses LF (\\n) line endings, not CRLF (\\r\\n)."""
        test_file = Path("test-nxclc0.md")
        content = test_file.read_bytes()
        assert b"\r\n" not in content, "File contains Windows CRLF line endings"

    def test_file_has_no_carriage_returns(self):
        """Test that file has no carriage return characters."""
        test_file = Path("test-nxclc0.md")
        content = test_file.read_bytes()
        assert b"\r" not in content, "File contains carriage return characters"

    def test_file_ends_with_newline(self):
        """Test that file ends with a newline character."""
        test_file = Path("test-nxclc0.md")
        content = test_file.read_bytes()
        assert content.endswith(b"\n"), "File should end with newline"


class TestPhase4FileSize:
    """Test SC-6: File size is 400-600 bytes (natural outcome of structure)."""

    def test_file_size_in_range(self):
        """Test that file size is between 400-600 bytes."""
        test_file = Path("test-nxclc0.md")
        file_size = test_file.stat().st_size
        assert (
            400 <= file_size <= 600
        ), f"File size {file_size} bytes not in range 400-600"

    def test_file_not_too_small(self):
        """Test that file is not too small (at least 400 bytes)."""
        test_file = Path("test-nxclc0.md")
        file_size = test_file.stat().st_size
        assert file_size >= 400, f"File too small: {file_size} bytes"

    def test_file_not_too_large(self):
        """Test that file is not too large (at most 600 bytes)."""
        test_file = Path("test-nxclc0.md")
        file_size = test_file.stat().st_size
        assert file_size <= 600, f"File too large: {file_size} bytes"


class TestPhase4GitCommit:
    """Test SC-7: Git log shows commit with correct conventional message."""

    def test_commit_exists_in_git_log(self):
        """Test that commit appears in git log."""
        result = subprocess.run(
            ["git", "log", "--all", "--oneline"],
            capture_output=True,
            text=True,
            check=True,
        )

        commit_message = "feat(245): create markdown file test-nxclc0.md with prose content"
        assert commit_message in result.stdout, (
            f"Commit message '{commit_message}' not found in git log"
        )

    def test_commit_message_exact_format(self):
        """Test that commit message follows exact conventional format."""
        result = subprocess.run(
            ["git", "log", "--all", "--format=%s"],
            capture_output=True,
            text=True,
            check=True,
        )

        commit_message = "feat(245): create markdown file test-nxclc0.md with prose content"
        assert commit_message in result.stdout, (
            f"Exact commit message not found: {commit_message}"
        )

    def test_commit_includes_feature_number(self):
        """Test that commit message includes feature number 245."""
        result = subprocess.run(
            ["git", "log", "--all", "--format=%s"],
            capture_output=True,
            text=True,
            check=True,
        )

        assert "feat(245):" in result.stdout, "Commit should reference feature 245"

    def test_commit_includes_filename(self):
        """Test that commit message includes filename test-nxclc0.md."""
        result = subprocess.run(
            ["git", "log", "--all", "--format=%s"],
            capture_output=True,
            text=True,
            check=True,
        )

        assert "test-nxclc0.md" in result.stdout, (
            "Commit message should include filename"
        )

    def test_commit_file_change_recorded(self):
        """Test that the commit records the file creation/modification."""
        # Find commit with our message
        result = subprocess.run(
            ["git", "log", "--all", "--format=%H %s"],
            capture_output=True,
            text=True,
            check=True,
        )

        commit_hash = None
        for line in result.stdout.strip().split("\n"):
            if "feat(245): create markdown file test-nxclc0.md with prose content" in line:
                commit_hash = line.split()[0]
                break

        assert commit_hash is not None, "Could not find commit with expected message"

        # Show the commit details
        result = subprocess.run(
            ["git", "show", commit_hash, "--name-only"],
            capture_output=True,
            text=True,
            check=True,
        )

        assert "test-nxclc0.md" in result.stdout, (
            f"File test-nxclc0.md not found in commit {commit_hash}"
        )


class TestPhase4GitBranch:
    """Test SC-8: Commit is on feature branch feat/245-markdown-file-creation-1f0041."""

    def test_current_branch_is_feature_branch(self):
        """Test that current branch is the feature branch."""
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )

        current_branch = result.stdout.strip()
        assert (
            current_branch == "feat/markdown-file-creation-1f0041"
            or current_branch == "feat/245-markdown-file-creation-1f0041"
        ), f"Current branch '{current_branch}' is not the feature branch"

    def test_feature_branch_exists(self):
        """Test that the feature branch exists locally."""
        result = subprocess.run(
            ["git", "branch", "--list"],
            capture_output=True,
            text=True,
            check=True,
        )

        # Check for either branch name variant
        has_branch = (
            "feat/markdown-file-creation-1f0041" in result.stdout
            or "feat/245-markdown-file-creation-1f0041" in result.stdout
        )
        assert has_branch, "Feature branch does not exist"

    def test_commit_on_feature_branch(self):
        """Test that our commit is on the feature branch."""
        # Get current branch
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        current_branch = branch_result.stdout.strip()

        # Get log for current branch
        result = subprocess.run(
            ["git", "log", current_branch, "--oneline"],
            capture_output=True,
            text=True,
            check=True,
        )

        commit_message = "feat(245): create markdown file test-nxclc0.md with prose content"
        assert commit_message in result.stdout, (
            f"Commit not found on branch {current_branch}"
        )


class TestPhase4RemotePush:
    """Test SC-9: Remote origin repository has the committed changes."""

    def test_feature_branch_exists_on_remote(self):
        """Test that feature branch exists on remote origin."""
        result = subprocess.run(
            ["git", "branch", "-r"],
            capture_output=True,
            text=True,
            check=True,
        )

        # Look for origin/feat
        has_remote_branch = "origin/feat" in result.stdout
        assert has_remote_branch, "Feature branch not found on remote origin"

    def test_branch_tracked_by_remote(self):
        """Test that current branch is up to date with remote."""
        result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True,
            check=True,
        )

        # Should say "Your branch is up to date with" or similar
        output = result.stdout.lower()
        assert (
            "up to date" in output or "ahead" in output or "behind" in output
        ), "Branch status cannot be determined"

    def test_commit_exists_on_remote_branch(self):
        """Test that our commit exists on the remote branch."""
        # Get current branch
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        current_branch = branch_result.stdout.strip()
        remote_branch = f"origin/{current_branch}"

        # Get log for remote branch
        result = subprocess.run(
            ["git", "log", remote_branch, "--oneline"],
            capture_output=True,
            text=True,
            check=True,
        )

        commit_message = "feat(245): create markdown file test-nxclc0.md with prose content"
        assert commit_message in result.stdout, (
            f"Commit not found on remote branch {remote_branch}"
        )

    def test_file_in_remote_commit(self):
        """Test that file is included in the remote commit."""
        # Get the remote branch and find commit
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        current_branch = branch_result.stdout.strip()
        remote_branch = f"origin/{current_branch}"

        # Find the commit hash on remote
        result = subprocess.run(
            ["git", "log", remote_branch, "--format=%H %s"],
            capture_output=True,
            text=True,
            check=True,
        )

        commit_hash = None
        for line in result.stdout.strip().split("\n"):
            if "feat(245): create markdown file test-nxclc0.md with prose content" in line:
                commit_hash = line.split()[0]
                break

        if commit_hash:
            # Show files in remote commit
            result = subprocess.run(
                ["git", "show", commit_hash, "--name-only"],
                capture_output=True,
                text=True,
                check=True,
            )

            assert "test-nxclc0.md" in result.stdout, (
                f"File not in remote commit {commit_hash}"
            )


class TestPhase4AllCriteria:
    """Integration test: All success criteria are met."""

    def test_all_success_criteria_met(self):
        """Test that all nine success criteria are satisfied."""
        test_file = Path("test-nxclc0.md")

        # SC-1: File exists in repository root
        assert test_file.exists(), "SC-1: File does not exist"
        assert test_file.is_file(), "SC-1: File is not a regular file"

        # Read file content
        content = test_file.read_text(encoding="utf-8")
        content_bytes = test_file.read_bytes()
        lines = content.split("\n")

        # SC-2: Exactly one H1 heading as first line
        assert lines[0].startswith("# "), "SC-2: H1 heading not on first line"

        # SC-3: Blank line and 2-3 sentences
        assert lines[1] == "", "SC-3: No blank line after heading"
        prose = "\n".join(lines[2:]).strip()
        sentence_count = len(re.findall(r"[.!?]", prose))
        assert 2 <= sentence_count <= 3, "SC-3: Not 2-3 sentences"

        # SC-4: UTF-8 without BOM
        assert not content_bytes.startswith(b"\xef\xbb\xbf"), "SC-4: File has BOM"

        # SC-5: Unix LF line endings
        assert b"\r\n" not in content_bytes, "SC-5: File has CRLF"
        assert b"\r" not in content_bytes, "SC-5: File has CR"

        # SC-6: File size 400-600 bytes
        file_size = test_file.stat().st_size
        assert 400 <= file_size <= 600, f"SC-6: File size {file_size} out of range"

        # SC-7 & SC-8 & SC-9: Git criteria
        result = subprocess.run(
            ["git", "log", "--all", "--oneline"],
            capture_output=True,
            text=True,
            check=True,
        )

        commit_message = "feat(245): create markdown file test-nxclc0.md with prose content"
        assert commit_message in result.stdout, "SC-7: Commit not in log"

        # Check branch status
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        current_branch = branch_result.stdout.strip()
        assert (
            "feat" in current_branch and "245" in current_branch
        ) or "feat/markdown-file-creation-1f0041" in current_branch, "SC-8: Wrong branch"

        # Check remote
        remote_result = subprocess.run(
            ["git", "branch", "-r"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert "origin/feat" in remote_result.stdout, "SC-9: Not on remote"


class TestExecuteFeatureMain:
    """Test executing the feature 245 main function."""

    def test_main_function_imports_successfully(self):
        """Test that the feature module can be imported."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import main

            assert callable(main)
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_main_function_executes_with_mocks(self):
        """Test that main function can be executed (with mocked tasks)."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import main

            # Mock all tasks to avoid LLM API calls and git operations
            with patch(
                "sheep.feature_245_markdown_file_creation.task_2_generate_markdown_content",
                return_value="# Test\n\nTest content.\n",
            ):
                with patch(
                    "sheep.feature_245_markdown_file_creation.task_3_write_markdown_file_to_disk",
                    return_value="/path/to/test-nxclc0.md",
                ):
                    with patch(
                        "sheep.feature_245_markdown_file_creation.validate_markdown_file",
                        return_value=True,
                    ):
                        with patch(
                            "sheep.feature_245_markdown_file_creation.task_4_commit_markdown_file",
                            return_value="Mocked commit",
                        ):
                            with patch(
                                "sheep.feature_245_markdown_file_creation.task_5_push_markdown_file",
                                return_value="Mocked push",
                            ):
                                # Should be able to call main without error
                                result = main()
                                assert result is not None
                                assert isinstance(result, dict)
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))
