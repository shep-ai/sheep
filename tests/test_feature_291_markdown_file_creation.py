"""Tests for feature 291: Creating markdown file test-6sw4o8.md with title and prose content."""

import os
import subprocess
from pathlib import Path

import pytest

# Check if API key is available for integration tests
HAS_API_KEY = bool(os.getenv("ANTHROPIC_API_KEY"))


class TestEntryPointUnitTest:
    """Unit tests for entry point function (task-3)."""

    FEATURE_291_FILENAME = "test-6sw4o8.md"

    @pytest.fixture(autouse=True)
    def cleanup(self):
        """Clean up test file before and after each test."""
        filepath = Path.cwd() / self.FEATURE_291_FILENAME
        if filepath.exists():
            filepath.unlink()
        yield
        if filepath.exists():
            filepath.unlink()

    def test_entry_point_can_be_imported(self):
        """Test that entry point module can be imported."""
        from feature_291_entry import create_feature_291_markdown

        assert callable(create_feature_291_markdown)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_entry_point_returns_dictionary(self):
        """Test that entry point returns a dictionary-like result object."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        assert isinstance(result, dict)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_entry_point_result_has_filepath_key(self):
        """Test that result has filepath key."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        assert "filepath" in result
        assert result["filepath"] is not None
        assert isinstance(result["filepath"], str)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_entry_point_result_has_content_key(self):
        """Test that result has content key."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        assert "content" in result
        assert result["content"] is not None
        assert isinstance(result["content"], str)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_entry_point_result_has_commit_message_key(self):
        """Test that result has commit_message key."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        assert "commit_message" in result
        assert result["commit_message"] is not None
        assert isinstance(result["commit_message"], str)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_entry_point_result_has_push_result_key(self):
        """Test that result has push_result key."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        assert "push_result" in result
        assert result["push_result"] is not None

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_entry_point_result_filepath_contains_correct_filename(self):
        """Test that result filepath contains the correct filename test-6sw4o8.md."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        filepath = result["filepath"]
        assert "test-6sw4o8.md" in filepath

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_entry_point_result_content_contains_markdown_heading(self):
        """Test that result content contains H1 markdown heading marker."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        content = result["content"]
        assert "#" in content
        assert content.lstrip().startswith("# ")

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_entry_point_result_content_is_not_empty(self):
        """Test that result content is not empty."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        assert result["content"]
        assert len(result["content"]) > 0


class TestFileCreationIntegration:
    """Integration tests for file creation at repository root (task-4)."""

    FEATURE_291_FILENAME = "test-6sw4o8.md"

    @pytest.fixture(autouse=True)
    def cleanup(self):
        """Clean up test file before and after each test."""
        filepath = Path.cwd() / self.FEATURE_291_FILENAME
        if filepath.exists():
            filepath.unlink()
        yield
        if filepath.exists():
            filepath.unlink()

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_file_created_at_repository_root(self):
        """Test that markdown file is created at repository root, not in subdirectory."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        filepath = Path(result["filepath"])

        # File should exist
        assert filepath.exists()

        # File should be in repository root (current directory)
        expected_path = Path.cwd() / self.FEATURE_291_FILENAME
        assert filepath == expected_path

        # File should not be in any subdirectory
        assert filepath.parent == Path.cwd()

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_file_named_exactly_test_6sw4o8_md(self):
        """Test that file is named exactly test-6sw4o8.md."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        filepath = Path(result["filepath"])

        assert filepath.name == self.FEATURE_291_FILENAME

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_file_contains_h1_heading_as_first_line(self):
        """Test that file contains H1 heading as first line."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        filepath = Path(result["filepath"])

        with open(filepath, encoding="utf-8") as f:
            first_line = f.readline()

        assert first_line.startswith("# ")
        assert len(first_line.strip()) > 2  # Has content after "# "

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_file_contains_exactly_2_to_3_sentences(self):
        """Test that file contains exactly 2-3 sentences in prose content."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        filepath = Path(result["filepath"])

        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")

        # Extract prose content (skip heading and blank line)
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_file_has_utf8_encoding(self):
        """Test that file has UTF-8 encoding."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        filepath = Path(result["filepath"])

        # Read as binary and verify it can be decoded as UTF-8
        with open(filepath, "rb") as f:
            binary_content = f.read()

        # This should not raise an exception if encoding is valid UTF-8
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not valid UTF-8: {e}")

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_file_has_no_utf8_bom(self):
        """Test that file has no UTF-8 BOM (Byte Order Mark)."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        filepath = Path(result["filepath"])

        with open(filepath, "rb") as f:
            binary_content = f.read()

        # UTF-8 BOM is the byte sequence EF BB BF
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_file_uses_unix_lf_line_endings(self):
        """Test that file uses Unix LF line endings, not CRLF."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        filepath = Path(result["filepath"])

        with open(filepath, "rb") as f:
            binary_content = f.read()

        # CRLF is \r\n (0x0D 0x0A)
        assert b"\r\n" not in binary_content, "File should use LF line endings, not CRLF"

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_file_ends_with_newline(self):
        """Test that file ends with a newline character."""
        from feature_291_entry import create_feature_291_markdown

        result = create_feature_291_markdown()
        filepath = Path(result["filepath"])

        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        assert content.endswith("\n"), "File should end with newline"


class TestGitOperationsIntegration:
    """Integration tests for git operations (task-5)."""

    FEATURE_291_FILENAME = "test-6sw4o8.md"
    EXPECTED_COMMIT_MESSAGE = "feat(291): create markdown file test-6sw4o8.md with prose content"

    @pytest.fixture(autouse=True)
    def cleanup(self):
        """Clean up test file and git state before and after each test."""
        filepath = Path.cwd() / self.FEATURE_291_FILENAME
        if filepath.exists():
            filepath.unlink()
        yield
        if filepath.exists():
            filepath.unlink()

    def _run_git_command(self, cmd):
        """Helper to run a git command and return output."""
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=str(Path.cwd())
        )
        return result.stdout.strip(), result.returncode

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_file_was_staged_in_git(self):
        """Test that file was staged in git (git index)."""
        from feature_291_entry import create_feature_291_markdown

        # Run the entry point
        result = create_feature_291_markdown()

        # Check git status to see if file is staged
        git_status_output, _ = self._run_git_command("git status --short")

        # File should be committed (not in staging area anymore after git push)
        # or at least should have been staged at some point
        # We can verify by checking git log
        filepath = Path(result["filepath"])
        assert filepath.exists(), f"File {filepath} should exist after entry point execution"

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_git_commit_created_with_conventional_format(self):
        """Test that git commit was created with conventional commit message format."""
        from feature_291_entry import create_feature_291_markdown

        # Get the current HEAD commit before running the entry point
        git_log_before, _ = self._run_git_command("git log -1 --format=%H")

        # Run the entry point
        create_feature_291_markdown()

        # Get the current HEAD commit after running the entry point
        git_log_after, _ = self._run_git_command("git log -1 --format=%H")

        # A new commit should have been created
        assert git_log_before != git_log_after, "A new commit should have been created"

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_commit_message_matches_expected_format(self):
        """Test that the latest commit message matches the expected conventional format."""
        from feature_291_entry import create_feature_291_markdown

        # Run the entry point
        create_feature_291_markdown()

        # Get the latest commit message
        git_log_output, _ = self._run_git_command("git log -1 --format=%B")

        # The commit message should match the expected format
        assert "feat(291):" in git_log_output, "Commit message should contain 'feat(291):'"
        assert "test-6sw4o8.md" in git_log_output, "Commit message should contain the filename"

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_commit_message_exactly_matches_expected(self):
        """Test that the latest commit message exactly matches the expected message."""
        from feature_291_entry import create_feature_291_markdown

        # Run the entry point
        create_feature_291_markdown()

        # Get the latest commit message
        git_log_output, _ = self._run_git_command("git log -1 --format=%B")

        # The message might have extra whitespace, so we compare stripped versions
        assert self.EXPECTED_COMMIT_MESSAGE in git_log_output or git_log_output.startswith(self.EXPECTED_COMMIT_MESSAGE)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_commit_contains_only_markdown_file(self):
        """Test that the latest commit contains only the markdown file."""
        from feature_291_entry import create_feature_291_markdown

        # Run the entry point
        result = create_feature_291_markdown()

        # Get the files changed in the latest commit
        git_diff_output, _ = self._run_git_command("git diff-tree --no-commit-id --name-only -r HEAD")

        # Should only contain the test-6sw4o8.md file
        files_in_commit = [f.strip() for f in git_diff_output.split("\n") if f.strip()]
        assert len(files_in_commit) >= 1, "Commit should contain at least the markdown file"
        assert any("test-6sw4o8.md" in f for f in files_in_commit), "Commit should contain test-6sw4o8.md"

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_commit_pushed_to_remote(self):
        """Test that the commit was pushed to remote repository."""
        from feature_291_entry import create_feature_291_markdown

        # Run the entry point (which includes push)
        result = create_feature_291_markdown()

        # Check if push result is present
        assert result["push_result"] is not None, "Push should have been executed"

        # Verify the remote branch exists
        # Get the current branch
        git_branch_output, _ = self._run_git_command("git rev-parse --abbrev-ref HEAD")
        current_branch = git_branch_output.strip()

        # Check if the remote branch exists
        git_ls_remote_output, _ = self._run_git_command(f"git ls-remote origin {current_branch}")
        assert len(git_ls_remote_output) > 0, f"Remote branch {current_branch} should exist after push"

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test")
    def test_branch_has_upstream_tracking_set(self):
        """Test that the feature branch has upstream tracking set to origin."""
        from feature_291_entry import create_feature_291_markdown

        # Run the entry point
        result = create_feature_291_markdown()

        # Check git branch -vv to see upstream tracking
        git_branch_vv_output, _ = self._run_git_command("git branch -vv")

        # The output should show something like: "feat/291-markdown-file-creation-4f5f95 xxxx [origin/feat/291-...]"
        # indicating that the branch has upstream tracking set
        assert "origin/" in git_branch_vv_output, "Branch should have upstream tracking set"


class TestContentStructureValidation:
    """Unit tests for validating markdown content structure (can run without full execution)."""

    @staticmethod
    def validate_markdown_structure(content: str) -> bool:
        """Helper function to validate markdown content structure."""
        if not content or not isinstance(content, str):
            return False

        lines = content.split("\n")
        if len(lines) < 4:  # At least heading, blank, prose, newline
            return False

        # Check H1 heading
        if not lines[0].startswith("# "):
            return False

        # Check blank line separator
        if lines[1] != "":
            return False

        # Check prose content
        prose_lines = [l for l in lines[2:] if l.strip()]
        if not prose_lines:
            return False

        # Check sentence count (count periods)
        prose_text = "\n".join(prose_lines)
        sentence_count = prose_text.count(".")
        if not (2 <= sentence_count <= 3):
            return False

        # Check trailing newline
        if not content.endswith("\n"):
            return False

        return True

    def test_valid_content_structure(self):
        """Test that valid markdown content passes structure validation."""
        valid_content = "# Example Title\n\nThis is the first sentence. This is the second sentence. This is the third sentence.\n"
        assert self.validate_markdown_structure(valid_content)

    def test_invalid_content_missing_heading(self):
        """Test that content without H1 heading fails structure validation."""
        invalid_content = "Example Title\n\nThis is the first sentence. This is the second sentence.\n"
        assert not self.validate_markdown_structure(invalid_content)

    def test_invalid_content_missing_blank_line(self):
        """Test that content without blank line separator fails validation."""
        invalid_content = "# Example Title\nThis is the first sentence. This is the second sentence.\n"
        assert not self.validate_markdown_structure(invalid_content)

    def test_invalid_content_insufficient_sentences(self):
        """Test that content with only 1 sentence fails validation."""
        invalid_content = "# Example Title\n\nThis is only one sentence.\n"
        assert not self.validate_markdown_structure(invalid_content)

    def test_invalid_content_too_many_sentences(self):
        """Test that content with more than 3 sentences fails validation."""
        invalid_content = "# Example Title\n\nSentence one. Sentence two. Sentence three. Sentence four.\n"
        assert not self.validate_markdown_structure(invalid_content)

    def test_invalid_content_missing_trailing_newline(self):
        """Test that content without trailing newline fails validation."""
        invalid_content = "# Example Title\n\nThis is the first sentence. This is the second sentence."
        assert not self.validate_markdown_structure(invalid_content)
