"""Tests for feature 241: Creating markdown file test-g0s8t1.md with title and prose content."""

from pathlib import Path


class TestMarkdownFileCreation:
    """Tests for task-1: Create markdown file with H1 heading and prose content."""

    def test_file_exists_at_repository_root(self):
        """Test that file test-g0s8t1.md exists at repository root."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists(), "File test-g0s8t1.md does not exist at repository root"

    def test_creates_file_with_h1_heading(self):
        """Test that created file contains H1 heading on first line."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists()
        content = test_file.read_text(encoding="utf-8")
        assert content.startswith("# "), "File does not start with H1 heading (# )"

    def test_file_contains_two_or_three_sentences(self):
        """Test that file contains 2-3 sentences (ending with periods)."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists()
        text_content = test_file.read_text(encoding="utf-8")

        # Extract prose content (skip heading and blank line)
        lines = text_content.split("\n")
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    def test_file_has_blank_line_separator(self):
        """Test that file has blank line after H1 heading."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists()
        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# "), "First line should be H1 heading"
        assert lines[1] == "", f"Second line should be blank, got: {repr(lines[1])}"

    def test_file_size_within_expected_range(self):
        """Test that file size is naturally in the 400-600 byte range."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists()
        file_size = test_file.stat().st_size
        # Typical range for properly formatted markdown file with this structure
        assert 350 <= file_size <= 650, f"File size {file_size} is outside expected range 350-650"


class TestMarkdownFileValidation:
    """Tests for task-1: Validate file encoding and line endings."""

    def test_file_not_utf8_bom(self):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists()
        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File contains UTF-8 BOM which should not be present"

    def test_file_has_lf_line_endings_not_crlf(self):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists()
        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content, "File contains CRLF which should be LF only"

    def test_file_content_reads_as_valid_utf8(self):
        """Test that file content can be read back as valid UTF-8."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists()
        # Should not raise an exception
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content is not None
        assert len(read_content) > 0


class TestGitWorkflow:
    """Tests for task-2: Git workflow integration (stage, commit, push)."""

    def test_file_is_in_git_index_or_committed(self):
        """Test that test-g0s8t1.md is either staged or already committed."""
        import subprocess
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert "test-g0s8t1.md" in result.stdout, "File should be tracked in git"

    def test_commit_message_format_is_conventional(self):
        """Test that commit message follows conventional commit format."""
        import subprocess
        result = subprocess.run(
            ["git", "log", "--format=%s"],
            capture_output=True,
            text=True,
            check=True,
        )
        # First line should be the most recent commit with our feat message
        commits = result.stdout.strip().split("\n")
        assert any(
            "feat(241): Create markdown file test-g0s8t1.md" in commit
            for commit in commits
        ), "Commit message should follow conventional format: feat(241): Create markdown file..."

    def test_exact_commit_message(self):
        """Test that commit has exact specified message."""
        import subprocess
        result = subprocess.run(
            ["git", "log", "--all", "--format=%s"],
            capture_output=True,
            text=True,
            check=True,
        )
        expected_message = "feat(241): Create markdown file test-g0s8t1.md with prose content"
        assert (
            expected_message in result.stdout
        ), f"Expected exact commit message: {expected_message}"

    def test_feature_branch_has_clean_commit_history(self):
        """Test that feature branch has commit that created test file."""
        import subprocess
        # Check if test-g0s8t1.md appears in git log for current branch
        result = subprocess.run(
            ["git", "log", "--name-status", "HEAD"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            check=True,
        )
        assert "test-g0s8t1.md" in result.stdout, "Git history should include a commit that added test-g0s8t1.md"

    def test_git_author_configured(self):
        """Test that git is configured with user.name and user.email."""
        import subprocess
        name_result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
        )
        email_result = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True,
            text=True,
        )
        assert name_result.returncode == 0 and name_result.stdout.strip(), "git user.name must be configured"
        assert email_result.returncode == 0 and email_result.stdout.strip(), "git user.email must be configured"


class TestIntegration:
    """Tests for task-3: End-to-end integration testing and final verification."""

    def test_complete_file_and_git_integration(self):
        """Test that file exists and is committed with correct message."""
        import subprocess
        test_file = Path("test-g0s8t1.md")

        # File must exist
        assert test_file.exists(), "File test-g0s8t1.md must exist"

        # File must be tracked in git
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert "test-g0s8t1.md" in result.stdout, "File must be tracked in git"

    def test_no_unintended_file_modifications(self):
        """Test that only test-g0s8t1.md was created, no other files modified."""
        import subprocess
        # Get the list of files changed in commits related to this feature
        result = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-status", "-r", "HEAD"],
            capture_output=True,
            text=True,
        )

        # Check that we only added test-g0s8t1.md (and possibly test file)
        changed_files = result.stdout.strip().split("\n") if result.stdout.strip() else []

        # Filter to only status lines (ignore empty lines)
        changed_files = [f.strip() for f in changed_files if f.strip()]

        # All changed files should be either test-g0s8t1.md or tests/
        for file_entry in changed_files:
            assert (
                "test-g0s8t1.md" in file_entry or "tests/" in file_entry
            ), f"Unexpected file modified: {file_entry}"

    def test_source_code_not_modified(self):
        """Test that no source code in /src/sheep/ was modified."""
        import subprocess
        # Get the files changed in the current commit, looking at file names only
        result = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )

        # Check that no changed files are in src/sheep/
        changed_files = result.stdout.strip().split("\n") if result.stdout.strip() else []
        for file_path in changed_files:
            assert not file_path.startswith("src/sheep/"), f"No source code should be modified, but found: {file_path}"

    def test_file_content_correct_and_accessible(self):
        """Test that file has correct structure: H1, blank line, 2-3 sentences."""
        test_file = Path("test-g0s8t1.md")
        assert test_file.exists()

        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Check structure
        assert lines[0].startswith("# "), "First line should be H1 heading"
        assert lines[1] == "", "Second line should be blank"

        # Check content is prose (not empty after heading)
        prose = "\n".join(lines[2:]).strip()
        assert len(prose) > 0, "File should contain prose content"

        # Check 2-3 sentences
        sentence_count = prose.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    def test_git_status_clean_except_untracked_specs(self):
        """Test that git status is clean (only untracked specs files if any)."""
        import subprocess
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        )

        # Should only have untracked files (??), and they should be specs files only
        lines = [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
        for line in lines:
            # Lines starting with ?? are untracked
            if line.startswith("??"):
                assert "specs/" in line, f"Untracked files should only be specs files, got: {line}"
