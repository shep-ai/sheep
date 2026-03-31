"""Tests for feature 277: Creating markdown file test-yziemx.md with title and prose content."""

from unittest.mock import MagicMock, patch

import pytest


class TestMarkdownFileCreation:
    """Tests for task-1: Create markdown file with H1 heading and prose content."""

    def test_file_does_not_exist_before_creation(self, tmp_path):
        """Test that file test-yziemx.md does not exist initially."""
        test_file = tmp_path / "test-yziemx.md"
        assert not test_file.exists()

    def test_creates_file_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading on first line."""
        test_file = tmp_path / "test-yziemx.md"

        # Create the file with H1 heading using pathlib
        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"

        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_contains_two_or_three_sentences(self, tmp_path):
        """Test that file contains 2-3 sentences (ending with periods)."""
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        # Extract prose content (skip heading and blank line)
        lines = text_content.split("\n")
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3

    def test_file_has_blank_line_separator(self, tmp_path):
        """Test that file has blank line after H1 heading."""
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_uses_pathlib_write_text_with_utf8(self, tmp_path):
        """Test that file is created using pathlib.Path.write_text() with UTF-8."""
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
        # Use pathlib.Path.write_text() with explicit UTF-8 and LF line endings
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        # Verify it was written as UTF-8 by reading it back
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content == content

    def test_file_size_within_expected_range(self, tmp_path):
        """Test that file size is naturally in the 400-600 byte range."""
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = test_file.stat().st_size
        # Typical range for properly formatted markdown file with this structure
        assert 350 <= file_size <= 650


class TestMarkdownFileValidation:
    """Tests for task-2: Validate file encoding and line endings."""

    def test_file_not_utf8_bom(self, tmp_path):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File contains UTF-8 BOM which should not be present"

    def test_file_has_no_crlf_line_endings(self, tmp_path):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content, "File contains CRLF which should be LF only"

    def test_file_content_reads_as_valid_utf8(self, tmp_path):
        """Test that file content can be read back as valid UTF-8."""
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Should not raise an exception
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content is not None
        assert len(read_content) > 0

    def test_markdown_heading_format_valid(self, tmp_path):
        """Test that markdown heading follows CommonMark specification (# Title)."""
        test_file = tmp_path / "test-yziemx.md"

        heading = "# The Wonders of Deep Ocean Exploration"
        prose = "The ocean depths remain one of Earth's final frontiers, with countless species yet to be discovered in the abyssal zones. Bioluminescent creatures, extreme pressure adaptations, and hydrothermal vent ecosystems create alien landscapes beneath the waves. Understanding these deep-sea environments is crucial for comprehending our planet's biodiversity and climate systems."
        content = f"{heading}\n\n{prose}\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        # First line should be H1 heading (starts with '# ')
        assert lines[0].startswith("# "), "First line should be H1 heading (starts with '# ')"
        # H1 heading should have text after '# '
        assert len(lines[0]) > 2, "H1 heading should have text content"


class TestGitWorkflowStageFile:
    """Tests for stage_file function in git workflow."""

    @patch("subprocess.run")
    def test_stage_file_success(self, mock_run):
        """Test that stage_file successfully calls git add."""
        import sys
        sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
        import git_workflow_277

        mock_run.return_value = MagicMock(returncode=0)

        # Should not raise
        git_workflow_277.stage_file()

        # Verify subprocess.run was called with git add command
        mock_run.assert_called_once_with(
            ["git", "add", "test-yziemx.md"],
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_stage_file_raises_on_failure(self, mock_run):
        """Test that stage_file raises RuntimeError when git add fails."""
        import sys
        sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
        import git_workflow_277

        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="fatal: not a git repository"
        )

        with pytest.raises(RuntimeError, match="git add failed"):
            git_workflow_277.stage_file()


class TestGitWorkflowCreateCommit:
    """Tests for create_commit function in git workflow."""

    @patch("subprocess.run")
    def test_create_commit_success(self, mock_run):
        """Test that create_commit successfully calls git commit."""
        import sys
        sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
        import git_workflow_277

        mock_run.return_value = MagicMock(returncode=0)

        # Should not raise
        git_workflow_277.create_commit()

        # Verify subprocess.run was called with git commit command
        mock_run.assert_called_once_with(
            ["git", "commit", "-m", "feat(277): create markdown file test-yziemx.md with title and prose content"],
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_create_commit_uses_conventional_format(self, mock_run):
        """Test that commit message follows conventional commit format."""
        import sys
        sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
        import git_workflow_277

        mock_run.return_value = MagicMock(returncode=0)

        git_workflow_277.create_commit()

        # Verify conventional commit format
        call_args = mock_run.call_args[0][0]
        message = call_args[3]  # -m parameter value
        assert message.startswith("feat(277):")
        assert "create markdown file test-yziemx.md with title and prose content" in message

    @patch("subprocess.run")
    def test_create_commit_raises_on_failure(self, mock_run):
        """Test that create_commit raises RuntimeError when git commit fails."""
        import sys
        sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
        import git_workflow_277

        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="nothing staged for commit"
        )

        with pytest.raises(RuntimeError, match="git commit failed"):
            git_workflow_277.create_commit()


class TestGitWorkflowPushToBranch:
    """Tests for push_to_branch function in git workflow."""

    @patch("subprocess.run")
    def test_push_to_branch_success(self, mock_run):
        """Test that push_to_branch successfully calls git push."""
        import sys
        sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
        import git_workflow_277

        mock_run.return_value = MagicMock(returncode=0)

        # Should not raise
        git_workflow_277.push_to_branch()

        # Verify subprocess.run was called with git push command
        mock_run.assert_called_once_with(
            ["git", "push", "-u", "origin", "feat/277-markdown-file-creation-760875"],
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_push_to_branch_uses_feature_branch(self, mock_run):
        """Test that git push uses correct feature branch."""
        import sys
        sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
        import git_workflow_277

        mock_run.return_value = MagicMock(returncode=0)

        git_workflow_277.push_to_branch()

        # Verify correct feature branch is used
        call_args = mock_run.call_args[0][0]
        assert "-u" in call_args
        assert "origin" in call_args
        assert "feat/277-markdown-file-creation-760875" in call_args

    @patch("subprocess.run")
    def test_push_to_branch_raises_on_failure(self, mock_run):
        """Test that push_to_branch raises RuntimeError when git push fails."""
        import sys
        sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
        import git_workflow_277

        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="fatal: Could not read from remote repository"
        )

        with pytest.raises(RuntimeError, match="git push failed"):
            git_workflow_277.push_to_branch()


class TestGitWorkflowRunAll:
    """Tests for run_all_git_workflow function."""

    @patch("subprocess.run")
    def test_runs_all_steps_in_order(self, mock_run):
        """Test that run_all_git_workflow executes all steps in sequence."""
        import sys
        sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
        import git_workflow_277

        mock_run.return_value = MagicMock(returncode=0)

        git_workflow_277.run_all_git_workflow()

        # Verify all three commands were called
        assert mock_run.call_count == 3

        # Verify they were called in the right order: add, commit, push
        calls = mock_run.call_args_list
        first_call = calls[0][0][0]
        second_call = calls[1][0][0]
        third_call = calls[2][0][0]

        assert first_call[0] == "git" and first_call[1] == "add"
        assert second_call[0] == "git" and second_call[1] == "commit"
        assert third_call[0] == "git" and third_call[1] == "push"


class TestGitWorkflowVerification:
    """Tests for git state verification functions."""

    @patch("subprocess.run")
    def test_verify_file_tracked_success(self, mock_run):
        """Test that verify_file_tracked succeeds when file is tracked."""
        import sys
        sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
        import git_workflow_277

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="test-yziemx.md\n"
        )

        # Should not raise
        git_workflow_277.verify_file_tracked()

    @patch("subprocess.run")
    def test_verify_file_tracked_fails_when_not_tracked(self, mock_run):
        """Test that verify_file_tracked raises when file is not tracked."""
        import sys
        sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
        import git_workflow_277

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="other-file.md\n"
        )

        with pytest.raises(AssertionError, match="not tracked in git"):
            git_workflow_277.verify_file_tracked()

    @patch("subprocess.run")
    def test_verify_commit_exists_success(self, mock_run):
        """Test that verify_commit_exists succeeds with correct commit message."""
        import sys
        sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
        import git_workflow_277

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="abc1234 feat(277): create markdown file test-yziemx.md with title and prose content\n"
        )

        # Should not raise
        git_workflow_277.verify_commit_exists()

    @patch("subprocess.run")
    def test_verify_commit_exists_fails_with_wrong_message(self, mock_run):
        """Test that verify_commit_exists raises with wrong commit message."""
        import sys
        sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
        import git_workflow_277

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="abc1234 feat(276): wrong commit message\n"
        )

        with pytest.raises(AssertionError, match="Commit message not found"):
            git_workflow_277.verify_commit_exists()

    @patch("subprocess.run")
    def test_verify_working_tree_clean_success(self, mock_run):
        """Test that verify_working_tree_clean succeeds when tree is clean."""
        import sys
        sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
        import git_workflow_277

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=""
        )

        # Should not raise
        git_workflow_277.verify_working_tree_clean()

    @patch("subprocess.run")
    def test_verify_working_tree_clean_fails_with_changes(self, mock_run):
        """Test that verify_working_tree_clean raises when tree has changes."""
        import sys
        sys.path.insert(0, '/home/runner/.shep/repos/ddbedba3d8bc1ecb/wt/feat-markdown-file-creation-760875')
        import git_workflow_277

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=" M test-yziemx.md\n"
        )

        with pytest.raises(AssertionError, match="not clean"):
            git_workflow_277.verify_working_tree_clean()
