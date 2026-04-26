"""Integration tests for feature 277: Complete workflow validation.

Tests the end-to-end workflow: file creation, git staging, committing, and pushing.
Verifies all success criteria from the feature specification are met.
"""

import subprocess
from pathlib import Path

import pytest


class TestEndToEndWorkflow:
    """Integration tests for complete feature 277 workflow."""

    def test_file_exists_in_repository_root(self):
        """Test that test-yziemx.md file exists in repository root."""
        test_file = Path("test-yziemx.md")
        assert test_file.exists(), "test-yziemx.md must exist in repository root"

    def test_file_has_correct_structure(self):
        """Test that file has correct structure: H1 heading, blank line, prose."""
        test_file = Path("test-yziemx.md")
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")

        # First line must be H1 heading
        assert lines[0].startswith("# "), "First line must be H1 heading"
        # Second line must be blank
        assert lines[1] == "", "Second line must be blank"
        # Third line must be prose (non-empty)
        assert len(lines) > 2, "File must have prose content"
        assert lines[2].strip() != "", "Prose content must not be empty"

    def test_file_encoding_is_utf8_without_bom(self):
        """Test that file encoding is UTF-8 without BOM."""
        test_file = Path("test-yziemx.md")
        binary_content = test_file.read_bytes()
        # UTF-8 BOM signature: 0xEF 0xBB 0xBF
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File must not have UTF-8 BOM"

    def test_file_has_lf_line_endings(self):
        """Test that file uses LF (Unix-style) line endings, not CRLF."""
        test_file = Path("test-yziemx.md")
        binary_content = test_file.read_bytes()
        # CRLF sequence: 0x0D 0x0A
        assert b"\r\n" not in binary_content, "File must use LF line endings, not CRLF"

    def test_file_size_in_expected_range(self):
        """Test that file size is approximately 400-600 bytes."""
        test_file = Path("test-yziemx.md")
        file_size = test_file.stat().st_size
        # Typical range for properly formatted markdown
        assert 350 <= file_size <= 650, f"File size {file_size} bytes should be 350-650 bytes"

    def test_file_content_is_valid_markdown(self):
        """Test that file content is valid CommonMark markdown."""
        test_file = Path("test-yziemx.md")
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Check H1 heading format: # Title
        assert lines[0].startswith("# "), "H1 heading must start with '# '"
        assert len(lines[0]) > 2, "H1 heading must have text after '# '"

        # Check blank line separator
        assert lines[1] == "", "Blank line separator required"

        # Check prose content has 2-3 sentences
        prose_content = "\n".join(lines[2:]).strip()
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3, f"Prose must have 2-3 sentences, found {sentence_count}"

    def test_file_is_tracked_in_git(self):
        """Test that file is tracked in git."""
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, "git ls-files must succeed"
        assert "test-yziemx.md" in result.stdout, "test-yziemx.md must be tracked in git"

    def test_commit_exists_with_correct_message(self):
        """Test that commit with correct message exists in git log."""
        result = subprocess.run(
            ["git", "log", "--oneline", "-10"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, "git log must succeed"

        expected_msg = "feat(277): create markdown file test-yziemx.md with title and prose content"
        assert expected_msg in result.stdout, f"Commit message '{expected_msg}' not found in recent git log"

    def test_file_content_matches_specification(self):
        """Test that file content matches feature specification requirements."""
        test_file = Path("test-yziemx.md")
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Extract components
        heading = lines[0]
        blank_line = lines[1]
        prose = "\n".join(lines[2:]).strip()

        # Verify each component
        assert heading.startswith("# "), "H1 heading required"
        assert len(heading) > 2, "H1 heading must have text"
        assert blank_line == "", "Blank line separator required"
        assert len(prose) > 0, "Prose content required"

        # Count sentences
        sentence_count = prose.count(".")
        assert 2 <= sentence_count <= 3, "Prose must have 2-3 sentences"

    def test_git_workflow_functions_exist(self):
        """Test that git workflow module and functions exist."""
        try:
            import sys
            sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
            import git_workflow_277

            # Verify all required functions exist
            assert hasattr(git_workflow_277, 'stage_file'), "stage_file function must exist"
            assert hasattr(git_workflow_277, 'create_commit'), "create_commit function must exist"
            assert hasattr(git_workflow_277, 'push_to_branch'), "push_to_branch function must exist"
            assert hasattr(git_workflow_277, 'run_all_git_workflow'), "run_all_git_workflow function must exist"
            assert hasattr(git_workflow_277, 'verify_file_tracked'), "verify_file_tracked function must exist"
            assert hasattr(git_workflow_277, 'verify_commit_exists'), "verify_commit_exists function must exist"
            assert hasattr(git_workflow_277, 'verify_working_tree_clean'), "verify_working_tree_clean function must exist"
            assert hasattr(git_workflow_277, 'verify_all_git_state'), "verify_all_git_state function must exist"
        except ImportError as e:
            pytest.fail(f"Failed to import git_workflow_277: {e}")

    def test_working_tree_is_clean(self):
        """Test that working tree is clean (no uncommitted changes)."""
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, "git status must succeed"
        # Filter out any untracked files in specs directory
        uncommitted = [line for line in result.stdout.strip().split('\n')
                      if line and not line.startswith('?? specs/')]
        assert not uncommitted, f"Working tree must be clean, but has changes:\n{chr(10).join(uncommitted)}"

    def test_success_criteria_all_met(self):
        """Test that all success criteria from feature specification are met."""
        # Criterion 1: File test-yziemx.md created in repository root directory
        test_file = Path("test-yziemx.md")
        assert test_file.exists(), "✓ File test-yziemx.md must exist in repository root"

        # Criterion 2: File contains exactly one H1 markdown heading
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        assert lines[0].startswith("# "), "✓ File must contain H1 markdown heading"

        # Criterion 3: File contains 2-3 sentences of prose content
        prose = "\n".join(lines[2:]).strip()
        sentence_count = prose.count(".")
        assert 2 <= sentence_count <= 3, f"✓ File must contain 2-3 sentences, found {sentence_count}"

        # Criterion 4: File uses UTF-8 character encoding without BOM
        binary_content = test_file.read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "✓ File must use UTF-8 without BOM"

        # Criterion 5: File uses LF (Unix-style) line endings, not CRLF
        assert b"\r\n" not in binary_content, "✓ File must use LF line endings"

        # Criterion 6: Markdown syntax is valid per CommonMark specification
        # (checked by format verification)
        assert lines[0].startswith("# "), "✓ Markdown H1 syntax is valid"

        # Criterion 7: File is staged in git
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
        )
        assert "test-yziemx.md" in result.stdout, "✓ File must be staged in git"

        # Criterion 8: Commit created with conventional commit message
        result = subprocess.run(
            ["git", "log", "--oneline", "-10"],
            capture_output=True,
            text=True,
        )
        expected_msg = "feat(277): create markdown file test-yziemx.md with title and prose content"
        assert expected_msg in result.stdout, f"✓ Commit with message '{expected_msg}' must exist"

        # Criterion 9: Commit pushed to remote feature branch
        result = subprocess.run(
            ["git", "branch", "-r"],
            capture_output=True,
            text=True,
        )
        assert "origin/feat/277-markdown-file-creation-760875" in result.stdout or \
               "origin/feat/markdown-file-creation-760875" in result.stdout, \
               "✓ Commit must be pushed to remote feature branch"

        # Criterion 10: File size is approximately 400-600 bytes
        file_size = test_file.stat().st_size
        assert 350 <= file_size <= 650, f"✓ File size {file_size} bytes must be 350-650 bytes"
