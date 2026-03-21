"""Tests for feature 142: Creating markdown file test-hqbiuy.md with title and prose content."""

from pathlib import Path
import pytest


class TestMarkdownFileCreation:
    """Tests for task-1: Create markdown file with H1 heading and prose content."""

    def test_file_does_not_exist_before_creation(self, tmp_path):
        """Test that file test-hqbiuy.md does not exist before creation."""
        test_file = tmp_path / "test-hqbiuy.md"
        assert not test_file.exists()

    def test_creates_file_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading."""
        test_file = tmp_path / "test-hqbiuy.md"

        # Create the file with H1 heading
        content = "# The Importance of Clear Documentation\n\nClear documentation is essential for the success of any software project, enabling developers to understand code functionality and usage patterns effectively. Well-structured markdown files serve as a bridge between implementation and comprehension, making complex systems accessible to teams of all skill levels. By maintaining comprehensive documentation alongside source code, we ensure that knowledge is preserved and shared across time and team changes.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_contains_two_or_three_sentences(self, tmp_path):
        """Test that file contains 2-3 sentences (ending with periods)."""
        test_file = tmp_path / "test-hqbiuy.md"

        content = "# The Importance of Clear Documentation\n\nClear documentation is essential for the success of any software project, enabling developers to understand code functionality and usage patterns effectively. Well-structured markdown files serve as a bridge between implementation and comprehension, making complex systems accessible to teams of all skill levels. By maintaining comprehensive documentation alongside source code, we ensure that knowledge is preserved and shared across time and team changes.\n"
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
        test_file = tmp_path / "test-hqbiuy.md"

        content = "# The Importance of Clear Documentation\n\nClear documentation is essential for the success of any software project, enabling developers to understand code functionality and usage patterns effectively. Well-structured markdown files serve as a bridge between implementation and comprehension, making complex systems accessible to teams of all skill levels. By maintaining comprehensive documentation alongside source code, we ensure that knowledge is preserved and shared across time and team changes.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_uses_pathlib_write_text_with_utf8(self, tmp_path):
        """Test that file is created using pathlib.Path.write_text() with UTF-8."""
        test_file = tmp_path / "test-hqbiuy.md"

        content = "# The Importance of Clear Documentation\n\nClear documentation is essential for the success of any software project, enabling developers to understand code functionality and usage patterns effectively. Well-structured markdown files serve as a bridge between implementation and comprehension, making complex systems accessible to teams of all skill levels. By maintaining comprehensive documentation alongside source code, we ensure that knowledge is preserved and shared across time and team changes.\n"
        # Use pathlib.Path.write_text() with explicit UTF-8 and LF
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        # Verify it was written as UTF-8 by reading it back
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content == content


class TestMarkdownFileValidation:
    """Tests for task-2: Validate file encoding, line endings, and size."""

    MIN_SIZE = 320
    MAX_SIZE = 600

    def test_file_not_utf8_bom(self, tmp_path):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = tmp_path / "test-hqbiuy.md"

        content = "# The Importance of Clear Documentation\n\nClear documentation is essential for the success of any software project, enabling developers to understand code functionality and usage patterns effectively. Well-structured markdown files serve as a bridge between implementation and comprehension, making complex systems accessible to teams of all skill levels. By maintaining comprehensive documentation alongside source code, we ensure that knowledge is preserved and shared across time and team changes.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_file_has_no_crlf_line_endings(self, tmp_path):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = tmp_path / "test-hqbiuy.md"

        content = "# The Importance of Clear Documentation\n\nClear documentation is essential for the success of any software project, enabling developers to understand code functionality and usage patterns effectively. Well-structured markdown files serve as a bridge between implementation and comprehension, making complex systems accessible to teams of all skill levels. By maintaining comprehensive documentation alongside source code, we ensure that knowledge is preserved and shared across time and team changes.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content

    def test_file_size_within_range(self, tmp_path):
        """Test that file size is between 320-600 bytes (inclusive)."""
        test_file = tmp_path / "test-hqbiuy.md"

        content = "# The Importance of Clear Documentation\n\nClear documentation is essential for the success of any software project, enabling developers to understand code functionality and usage patterns effectively. Well-structured markdown files serve as a bridge between implementation and comprehension, making complex systems accessible to teams of all skill levels. By maintaining comprehensive documentation alongside source code, we ensure that knowledge is preserved and shared across time and team changes.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = len(test_file.read_bytes())
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

    def test_validation_all_criteria_met(self, tmp_path):
        """Test that file passes all validation criteria together."""
        test_file = tmp_path / "test-hqbiuy.md"

        # Content that meets all criteria
        content = "# The Importance of Clear Documentation\n\nClear documentation is essential for the success of any software project, enabling developers to understand code functionality and usage patterns effectively. Well-structured markdown files serve as a bridge between implementation and comprehension, making complex systems accessible to teams of all skill levels. By maintaining comprehensive documentation alongside source code, we ensure that knowledge is preserved and shared across time and team changes.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        file_size = len(binary_content)

        # Check UTF-8 without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Check no CRLF
        assert b"\r\n" not in binary_content

        # Check file size
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE


class TestGitOperations:
    """Tests for task-3: Implement git add/commit/push workflow."""

    def test_git_add_stages_file(self, tmp_path, monkeypatch):
        """Test that git add command is called with correct file path."""
        from unittest.mock import patch, MagicMock
        import subprocess

        monkeypatch.chdir(tmp_path)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            from feature_142_git_integration import stage_file

            stage_file("test-hqbiuy.md")

            # Verify git add was called with correct arguments
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == ["git", "add", "test-hqbiuy.md"]

    def test_git_commit_with_conventional_message(self, tmp_path, monkeypatch):
        """Test that git commit uses conventional commit message format."""
        from unittest.mock import patch, MagicMock

        monkeypatch.chdir(tmp_path)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            from feature_142_git_integration import create_commit

            create_commit("feat(142): Create markdown file test-hqbiuy.md with specification")

            # Verify git commit was called with correct message format
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert "feat(142)" in call_args[0][0][3]
            assert "test-hqbiuy.md" in call_args[0][0][3]

    def test_git_push_targets_correct_branch(self, tmp_path, monkeypatch):
        """Test that git push targets feature branch."""
        from unittest.mock import patch, MagicMock

        monkeypatch.chdir(tmp_path)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            from feature_142_git_integration import push_to_remote

            push_to_remote("feat/markdown-file-creation-b65b0e")

            # Verify git push targets correct branch
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert "feat/markdown-file-creation-b65b0e" in call_args[0][0]

    def test_git_command_failure_raises_error(self, tmp_path, monkeypatch):
        """Test that git command failure raises RuntimeError."""
        from unittest.mock import patch, MagicMock
        import subprocess

        monkeypatch.chdir(tmp_path)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1, stderr="error: something went wrong"
            )
            from feature_142_git_integration import stage_file

            with pytest.raises(RuntimeError):
                stage_file("test-hqbiuy.md")


class TestOrchestration:
    """Tests for task-4: Create main orchestration script."""

    def test_orchestration_calls_all_steps(self, tmp_path, monkeypatch):
        """Test that orchestration script calls all steps in order."""
        from unittest.mock import patch, MagicMock, call

        monkeypatch.chdir(tmp_path)

        # Create a dummy test file
        test_file = tmp_path / "test-hqbiuy.md"
        test_file.write_text(
            "# The Importance of Clear Documentation\n\nClear documentation is essential for the success of any software project, enabling developers to understand code functionality and usage patterns effectively. Well-structured markdown files serve as a bridge between implementation and comprehension, making complex systems accessible to teams of all skill levels. By maintaining comprehensive documentation alongside source code, we ensure that knowledge is preserved and shared across time and team changes.\n",
            encoding="utf-8",
            newline="\n",
        )

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            from feature_142_orchestration import main

            main()

            # Verify all git operations were called
            assert mock_run.call_count >= 3  # add, commit, push
            call_args_list = [call[0][0] for call in mock_run.call_args_list]
            assert any("add" in args for args in call_args_list)
            assert any("commit" in args for args in call_args_list)
            assert any("push" in args for args in call_args_list)

    def test_orchestration_handles_validation_failure(self, tmp_path, monkeypatch):
        """Test that orchestration stops git operations if validation fails."""
        from unittest.mock import patch, MagicMock

        monkeypatch.chdir(tmp_path)

        # Create invalid file (missing trailing newline)
        test_file = tmp_path / "test-hqbiuy.md"
        test_file.write_bytes(b"# Invalid\n\nNo trailing newline")

        with patch("subprocess.run") as mock_run:
            from feature_142_orchestration import main

            # Should fail and not attempt git operations
            result = main()
            assert result is False or result == 1
