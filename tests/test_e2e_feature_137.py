"""End-to-end tests for feature 137: markdown file creation and git integration.

Tests for task-4: Verify end-to-end correctness and integration.

Validates the complete workflow:
1. File test-narzc3.md exists and has correct content
2. File passes all validation checks (encoding, line endings, structure, prose)
3. File is properly staged and committed in git
4. Changes are integrated with git (stage → commit → push)
"""

import subprocess
from pathlib import Path
import pytest
from unittest import mock


class TestEndToEndFileCreation:
    """Tests verifying file creation (phase 1) was successful."""

    def test_file_exists_at_repository_root(self):
        """Test that test-narzc3.md exists at repository root."""
        test_file = Path("test-narzc3.md")
        assert test_file.exists(), "File test-narzc3.md does not exist at repository root"

    def test_file_has_correct_name(self):
        """Test that file is named exactly test-narzc3.md."""
        test_file = Path("test-narzc3.md")
        assert test_file.name == "test-narzc3.md"
        assert test_file.suffix == ".md"

    def test_file_is_markdown_format(self):
        """Test that file is readable as markdown."""
        test_file = Path("test-narzc3.md")
        content = test_file.read_text(encoding="utf-8")

        # Verify contains markdown heading
        assert content.startswith("#"), "File should start with markdown heading"
        assert "\n" in content, "File should contain newlines"


class TestEndToEndValidation:
    """Tests verifying file validation (phase 2) requirements are met."""

    def test_file_encoding_is_utf8_without_bom(self):
        """Test that file is UTF-8 encoded without BOM."""
        test_file = Path("test-narzc3.md")

        # Check not UTF-8 with BOM
        binary_content = test_file.read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf"), (
            "File contains UTF-8 BOM, which is forbidden"
        )

        # Check is valid UTF-8
        test_file.read_text(encoding="utf-8")  # Will raise if not valid UTF-8

    def test_file_uses_unix_lf_line_endings(self):
        """Test that file uses Unix LF line endings (no CRLF)."""
        test_file = Path("test-narzc3.md")
        binary_content = test_file.read_bytes()

        assert b"\r\n" not in binary_content, (
            "File contains Windows CRLF line endings; must use Unix LF"
        )

    def test_file_has_proper_markdown_structure(self):
        """Test that file has H1 heading, blank line, and prose."""
        test_file = Path("test-narzc3.md")
        content = test_file.read_text(encoding="utf-8")

        lines = content.split("\n")

        # Check H1 heading on line 1
        assert lines[0].startswith("# "), f"Line 1 should be H1 heading, got: {lines[0]!r}"

        # Check blank line on line 2
        assert lines[1] == "", f"Line 2 should be blank, got: {lines[1]!r}"

        # Check prose content exists after blank line
        prose_content = content.split("\n\n", 1)
        assert len(prose_content) >= 2, "Should have prose content after blank line"
        assert prose_content[1].strip(), "Prose should not be empty"

    def test_file_prose_contains_2_to_3_sentences(self):
        """Test that prose contains exactly 2-3 sentences."""
        test_file = Path("test-narzc3.md")
        content = test_file.read_text(encoding="utf-8")

        # Extract prose (skip heading and blank line)
        prose = content.split("\n\n", 1)[1].strip()

        # Count sentences (periods, question marks, exclamation marks)
        sentence_count = prose.count(".") + prose.count("?") + prose.count("!")

        assert 2 <= sentence_count <= 3, (
            f"Prose should have 2-3 sentences, found {sentence_count}"
        )

    def test_file_size_is_within_specification(self):
        """Test that file size is 320-600 bytes (specification requirement)."""
        test_file = Path("test-narzc3.md")
        file_size = len(test_file.read_bytes())

        assert 320 <= file_size <= 600, (
            f"File size {file_size} bytes is outside specification range (320-600)"
        )

    def test_validation_module_passes_all_checks(self):
        """Test that validation module's validate_file() passes completely."""
        from validate_feature_137 import validate_file, ValidationError

        test_file = Path("test-narzc3.md")

        # Should not raise any exception
        try:
            validate_file(test_file)
        except ValidationError as e:
            pytest.fail(f"File validation failed: {e}")


class TestEndToEndGitIntegration:
    """Tests verifying git integration (phase 3) requirements."""

    def test_file_is_committed_in_git_history(self):
        """Test that test-narzc3.md appears in git commit history."""
        result = subprocess.run(
            ["git", "log", "--name-only", "--all", "--", "test-narzc3.md"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        assert "test-narzc3.md" in result.stdout, (
            "File test-narzc3.md not found in git history"
        )

    def test_commit_message_is_conventional_format(self):
        """Test that commit message follows conventional commits format."""
        # Get commit message for test-narzc3.md file
        result = subprocess.run(
            ["git", "log", "--oneline", "--all", "--", "test-narzc3.md"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        # Should show a commit with conventional format
        assert result.stdout, "No commit found for test-narzc3.md"

        # Expected format: feat(137): Create markdown file test-narzc3.md
        commit_lines = result.stdout.strip().split("\n")
        commit_message = commit_lines[0]  # First (most recent) commit

        # Verify conventional commit format: type(scope): description
        assert "feat(137)" in commit_message, (
            f"Commit message should contain 'feat(137)', got: {commit_message}"
        )
        assert "test-narzc3.md" in commit_message, (
            f"Commit message should mention test-narzc3.md, got: {commit_message}"
        )

    def test_file_is_not_in_untracked_files(self):
        """Test that file is tracked by git (not untracked)."""
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        # File should not appear as untracked (??) or modified (M)
        # If it appears, that would indicate it's not properly committed
        lines = result.stdout.strip().split("\n") if result.stdout.strip() else []

        for line in lines:
            if "test-narzc3.md" in line:
                # Should not be untracked (??) or modified (M) for this feature
                # (It should be committed already)
                status = line[:2] if len(line) >= 2 else ""
                assert status not in ("??", "M "), (
                    f"File test-narzc3.md has unexpected status: {status}"
                )

    def test_current_branch_is_feature_branch(self):
        """Test that we're on the feature branch."""
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        branch = result.stdout.strip()
        assert "feat" in branch or "markdown" in branch or "137" in branch, (
            f"Expected feature branch, got: {branch}"
        )


class TestEndToEndGitIntegrationFunctions:
    """Tests for the actual git integration functions orchestration."""

    def test_integrate_git_function_exists(self):
        """Test that integrate_git() function is importable."""
        from git_integration_137 import integrate_git

        assert callable(integrate_git)

    def test_integrate_git_accepts_required_parameters(self):
        """Test that integrate_git() accepts filename, branch, and message parameters."""
        from git_integration_137 import integrate_git

        # Mock git operations to avoid actual git calls
        with mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(returncode=0)

            # Should not raise TypeError about missing arguments
            integrate_git(
                "test-narzc3.md",
                "feat/markdown-file-creation-646f97",
                "feat(137): Create markdown file test-narzc3.md"
            )

    def test_stage_file_function_exists(self):
        """Test that stage_file() function is importable."""
        from git_integration_137 import stage_file

        assert callable(stage_file)

    def test_commit_file_function_exists(self):
        """Test that commit_file() function is importable."""
        from git_integration_137 import commit_file

        assert callable(commit_file)

    def test_push_file_function_exists(self):
        """Test that push_file() function is importable."""
        from git_integration_137 import push_file

        assert callable(push_file)


class TestEndToEndMainOrchestration:
    """Tests for main() orchestration function."""

    def test_main_function_exists(self):
        """Test that main() function is callable."""
        from git_integration_137 import main

        assert callable(main)

    def test_main_returns_integer_exit_code(self):
        """Test that main() returns an integer exit code."""
        from git_integration_137 import main

        with mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(returncode=0)

            result = main()

            assert isinstance(result, int), f"main() should return int, got {type(result)}"
            assert result == 0 or result == 1, f"main() should return 0 or 1, got {result}"

    def test_main_returns_zero_on_success(self):
        """Test that main() returns 0 when git operations succeed."""
        from git_integration_137 import main

        with mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(returncode=0)

            result = main()

            assert result == 0, f"main() should return 0 on success, got {result}"

    def test_main_handles_exceptions(self):
        """Test that main() catches and handles exceptions gracefully."""
        from git_integration_137 import main

        with mock.patch("subprocess.run") as mock_run:
            mock_run.side_effect = RuntimeError("Test error")

            result = main()

            # Should return non-zero exit code, not raise exception
            assert result != 0, "main() should return non-zero on error"
            assert isinstance(result, int), "main() should return int even on error"
