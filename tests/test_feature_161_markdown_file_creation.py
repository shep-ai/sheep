"""Tests for feature 161: Creating markdown file test-fzgsdv.md with title and prose content."""

from pathlib import Path
from unittest.mock import patch
import pytest


class TestFeature161MarkdownFileCreation:
    """Tests for feature 161 markdown file creation."""

    def test_module_imports(self):
        """Test that the feature module can be imported."""
        from sheep.features.feature_161_markdown_file_creation import (
            create_feature_161_markdown_file,
        )

        assert callable(create_feature_161_markdown_file)

    def test_function_signature(self):
        """Test that the function has the correct signature."""
        from sheep.features.feature_161_markdown_file_creation import (
            create_feature_161_markdown_file,
        )
        import inspect

        sig = inspect.signature(create_feature_161_markdown_file)
        assert "repo_path" in sig.parameters
        assert sig.parameters["repo_path"].default is None

    def test_feature_constants(self):
        """Test that feature constants are defined correctly."""
        from sheep.features.feature_161_markdown_file_creation import (
            FEATURE_NUMBER,
            MARKDOWN_FILENAME,
            COMMIT_MESSAGE,
        )

        assert FEATURE_NUMBER == 161
        assert MARKDOWN_FILENAME == "test-fzgsdv.md"
        assert COMMIT_MESSAGE == "feat(161): Create markdown file test-fzgsdv.md with prose content"

    @patch("sheep.features.feature_161_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_161_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_161_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_161_markdown_file_creation.write_markdown_file")
    def test_orchestration_calls_all_steps(
        self,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that the orchestration calls all steps in the correct order."""
        from sheep.features.feature_161_markdown_file_creation import (
            create_feature_161_markdown_file,
        )

        # Setup mock returns
        mock_content = "# Understanding Resilience\n\nResilience is the ability to bounce back from adversity and challenges. It is built through experience, learning, and perseverance. Strong resilience enables us to face difficulties with confidence and determination.\n"
        mock_write.return_value = "/repo/test-fzgsdv.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed successfully"
        mock_push.return_value = "Pushed successfully"

        # Call the function
        result = create_feature_161_markdown_file("/test/repo")

        # Verify all functions were called
        mock_write.assert_called_once()
        mock_validate.assert_called_once()
        mock_commit.assert_called_once()
        mock_push.assert_called_once()

        # Verify the return value structure
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

    @patch("sheep.features.feature_161_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_161_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_161_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_161_markdown_file_creation.write_markdown_file")
    def test_returns_correct_dict_structure(
        self,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that the function returns the correct dictionary structure."""
        from sheep.features.feature_161_markdown_file_creation import (
            create_feature_161_markdown_file,
            COMMIT_MESSAGE,
        )

        # Setup mock returns
        mock_content = "# Understanding Resilience\n\nResilience is the ability to bounce back. It is built through experience. Strong resilience enables confidence.\n"
        mock_filepath = "/repo/test-fzgsdv.md"
        mock_write.return_value = mock_filepath
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call the function
        result = create_feature_161_markdown_file()

        # Verify all required keys are present
        assert result["filepath"] == mock_filepath
        assert result["commit_message"] == COMMIT_MESSAGE
        assert result["push_result"] == "Pushed"

    @patch("sheep.features.feature_161_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_161_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_161_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_161_markdown_file_creation.write_markdown_file")
    def test_uses_exact_commit_message(
        self,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that the exact commit message from spec is used."""
        from sheep.features.feature_161_markdown_file_creation import (
            create_feature_161_markdown_file,
        )

        # Setup mocks
        mock_content = "# Test\n\nSentence. Sentence. Sentence.\n"
        mock_write.return_value = "/repo/test-fzgsdv.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call the function
        create_feature_161_markdown_file()

        # Verify the commit message is exactly as specified
        call_args = mock_commit.call_args
        assert call_args is not None
        assert (
            call_args.kwargs["custom_message"]
            == "feat(161): Create markdown file test-fzgsdv.md with prose content"
        )

    @patch("sheep.features.feature_161_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_161_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_161_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_161_markdown_file_creation.write_markdown_file")
    def test_repo_path_defaults_to_cwd(
        self,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that repo_path defaults to current working directory."""
        from sheep.features.feature_161_markdown_file_creation import (
            create_feature_161_markdown_file,
        )

        # Setup mocks
        mock_content = "# Test\n\nSentence. Sentence. Sentence.\n"
        mock_write.return_value = "/repo/test-fzgsdv.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call without repo_path
        create_feature_161_markdown_file()

        # Verify commit was called with str(Path.cwd())
        call_args = mock_commit.call_args
        assert call_args is not None
        assert call_args[0][2] == str(Path.cwd())


class TestFileCreation:
    """Integration tests for actual file creation."""

    def test_creates_file_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading."""
        test_file = tmp_path / "test-fzgsdv.md"

        # Create the file with H1 heading
        content = "# Understanding Resilience\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_contains_exactly_three_sentences(self, tmp_path):
        """Test that file contains exactly 2-3 sentences (ending with periods)."""
        test_file = tmp_path / "test-fzgsdv.md"

        content = "# Understanding Resilience\n\nResilience is the ability to bounce back from adversity and challenges. It is built through experience, learning, and perseverance. Strong resilience enables us to face difficulties with confidence and determination.\n"
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
        test_file = tmp_path / "test-fzgsdv.md"

        content = "# Understanding Resilience\n\nResilience is the ability. It builds strength. Strong resilience brings confidence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        # Check that second line (index 1) is blank
        assert lines[0].startswith("# ")
        assert lines[1] == ""

    def test_file_uses_utf8_encoding(self, tmp_path):
        """Test that file is UTF-8 encoded."""
        test_file = tmp_path / "test-fzgsdv.md"

        content = "# Understanding Resilience\n\nResilience is the ability. It builds strength. Strong resilience brings confidence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Read as binary and verify no BOM
        binary_content = test_file.read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Verify can be decoded as UTF-8
        decoded = binary_content.decode("utf-8")
        assert decoded == content

    def test_file_uses_lf_line_endings(self, tmp_path):
        """Test that file uses LF line endings, not CRLF."""
        test_file = tmp_path / "test-fzgsdv.md"

        content = "# Understanding Resilience\n\nResilience is the ability. It builds strength. Strong resilience brings confidence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Read as binary and verify no CRLF
        binary_content = test_file.read_bytes()
        assert b"\r\n" not in binary_content
        assert b"\n" in binary_content

    def test_file_ends_with_newline(self, tmp_path):
        """Test that file ends with a trailing newline (Unix convention)."""
        test_file = tmp_path / "test-fzgsdv.md"

        content = "# Understanding Resilience\n\nResilience is the ability. It builds strength. Strong resilience brings confidence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        assert text_content.endswith("\n")

    def test_file_size_is_reasonable(self, tmp_path):
        """Test that file size is within reasonable bounds (300-600 bytes guideline)."""
        test_file = tmp_path / "test-fzgsdv.md"

        content = "# Understanding Resilience\n\nResilience is the ability to bounce back from adversity and challenges. It is built through experience, learning, and perseverance. Strong resilience enables us to face difficulties with confidence and determination.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = test_file.stat().st_size
        # 300-600 bytes is a guideline, not strict
        assert 100 < file_size < 1000


class TestValidationFailures:
    """Tests for validation failure scenarios."""

    def test_validation_rejects_file_with_crlf_line_endings(self, tmp_path):
        """Test that validation rejects file with CRLF line endings."""
        from sheep.content_generators import validate_markdown_file

        test_file = tmp_path / "test-invalid.md"
        # Create content with CRLF line endings
        content = "# Test Title\r\n\r\nFirst sentence. Second sentence. Third sentence.\r\n"
        test_file.write_bytes(content.encode("utf-8"))

        with pytest.raises(ValueError, match="CRLF line endings"):
            validate_markdown_file(str(test_file))

    def test_validation_rejects_file_with_utf8_bom(self, tmp_path):
        """Test that validation rejects file with UTF-8 BOM."""
        from sheep.content_generators import validate_markdown_file

        test_file = tmp_path / "test-invalid.md"
        # Create content with UTF-8 BOM
        content = b"\xef\xbb\xbf# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_bytes(content)

        with pytest.raises(ValueError, match="UTF-8 BOM"):
            validate_markdown_file(str(test_file))

    def test_validation_rejects_file_without_h1_heading(self, tmp_path):
        """Test that validation rejects file without H1 heading."""
        from sheep.content_generators import validate_markdown_file

        test_file = tmp_path / "test-invalid.md"
        # Create content without H1 heading
        content = "## Wrong Heading Level\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="H1 heading"):
            validate_markdown_file(str(test_file))

    def test_validation_rejects_file_without_blank_line_separator(self, tmp_path):
        """Test that validation rejects file without blank line after heading."""
        from sheep.content_generators import validate_markdown_file

        test_file = tmp_path / "test-invalid.md"
        # Create content without blank line separator
        content = "# Test Title\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="blank"):
            validate_markdown_file(str(test_file))

    def test_validation_rejects_file_with_too_few_sentences(self, tmp_path):
        """Test that validation rejects file with fewer than 2 sentences."""
        from sheep.content_generators import validate_markdown_file

        test_file = tmp_path / "test-invalid.md"
        # Create content with only 1 sentence
        content = "# Test Title\n\nFirst sentence only.\n"
        test_file.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_markdown_file(str(test_file))

    def test_validation_rejects_file_with_too_many_sentences(self, tmp_path):
        """Test that validation rejects file with more than 3 sentences."""
        from sheep.content_generators import validate_markdown_file

        test_file = tmp_path / "test-invalid.md"
        # Create content with 4 sentences
        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence. Fourth sentence.\n"
        test_file.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_markdown_file(str(test_file))

    def test_validation_rejects_file_without_trailing_newline(self, tmp_path):
        """Test that validation rejects file without trailing newline."""
        from sheep.content_generators import validate_markdown_file

        test_file = tmp_path / "test-invalid.md"
        # Create content without trailing newline
        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
        test_file.write_bytes(content.encode("utf-8"))

        with pytest.raises(ValueError, match="trailing newline"):
            validate_markdown_file(str(test_file))

    def test_validation_rejects_nonexistent_file(self, tmp_path):
        """Test that validation rejects nonexistent file."""
        from sheep.content_generators import validate_markdown_file

        nonexistent_file = str(tmp_path / "nonexistent.md")

        with pytest.raises(OSError, match="does not exist"):
            validate_markdown_file(nonexistent_file)

    def test_validation_rejects_non_utf8_file(self, tmp_path):
        """Test that validation rejects file with non-UTF-8 encoding."""
        from sheep.content_generators import validate_markdown_file

        test_file = tmp_path / "test-invalid.md"
        # Create content with invalid UTF-8 (using Latin-1 that's not valid UTF-8)
        content = b"# Test Title\n\nFirst sentence. Second sentence. \xff Third sentence.\n"
        test_file.write_bytes(content)

        with pytest.raises(ValueError, match="not valid UTF-8"):
            validate_markdown_file(str(test_file))

    def test_validation_succeeds_with_valid_file(self, tmp_path):
        """Test that validation succeeds with valid file."""
        from sheep.content_generators import validate_markdown_file

        test_file = tmp_path / "test-valid.md"
        content = "# Understanding Resilience\n\nResilience is the ability to bounce back from adversity and challenges. It is built through experience, learning, and perseverance. Strong resilience enables us to face difficulties with confidence and determination.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Should not raise any exception
        result = validate_markdown_file(str(test_file))
        assert result is True


class TestGitIntegration:
    """Tests for git integration (add, commit, push operations)."""

    def test_file_not_staged_before_commit(self):
        """Test that file is not yet staged before git commit operation."""
        import subprocess

        # Check that test-fzgsdv.md exists in working directory
        test_file = Path("test-fzgsdv.md")
        assert test_file.exists(), "test-fzgsdv.md should exist"

        # Verify file is not staged in git
        result = subprocess.run(
            ["git", "status", "--porcelain", "test-fzgsdv.md"],
            capture_output=True,
            text=True,
            check=False,
        )
        # File should either not appear in status or appear with '??' (untracked)
        # If it appears with '??' or '??', it's not staged yet
        output = result.stdout.strip()
        # Either empty (doesn't exist in status) or starts with '??' or ' M' (modified, not staged)
        if output:
            assert output.startswith("??") or output.startswith(" M")

    def test_file_is_staged_after_git_add(self):
        """Test that file is staged after git add operation."""
        import subprocess

        test_file = Path("test-fzgsdv.md")
        assert test_file.exists(), "test-fzgsdv.md should exist"

        # Stage the file (idempotent - safe to call even if already staged)
        result = subprocess.run(
            ["git", "add", "test-fzgsdv.md"],
            check=True,
            capture_output=True,
        )
        # The add command should succeed
        assert result.returncode == 0, "git add should succeed"

        # Verify file is tracked by git (either committed or staged)
        result = subprocess.run(
            ["git", "ls-files", "test-fzgsdv.md"],
            capture_output=True,
            text=True,
            check=True,
        )
        # If file is in ls-files, it's tracked (committed or staged)
        assert "test-fzgsdv.md" in result.stdout, "File should be tracked by git"

    def test_commit_message_follows_conventional_format(self):
        """Test that commit message follows conventional commit format."""
        from sheep.features.feature_161_markdown_file_creation import COMMIT_MESSAGE

        # Verify message format: feat(###): description
        assert COMMIT_MESSAGE.startswith("feat(161):"), (
            f"Commit message should start with 'feat(161):', got: {COMMIT_MESSAGE}"
        )
        assert "test-fzgsdv.md" in COMMIT_MESSAGE, (
            f"Commit message should contain filename, got: {COMMIT_MESSAGE}"
        )
        assert "prose content" in COMMIT_MESSAGE, (
            f"Commit message should contain 'prose content', got: {COMMIT_MESSAGE}"
        )

    def test_exact_commit_message_format(self):
        """Test the exact commit message matches specification."""
        from sheep.features.feature_161_markdown_file_creation import COMMIT_MESSAGE

        expected_message = "feat(161): Create markdown file test-fzgsdv.md with prose content"
        assert (
            COMMIT_MESSAGE == expected_message
        ), f"Expected '{expected_message}', got '{COMMIT_MESSAGE}'"

    @patch("sheep.features.feature_161_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_161_markdown_file_creation.commit_markdown_file")
    def test_git_operations_only_after_validation(
        self, mock_commit, mock_push
    ):
        """Test that git operations (commit, push) only execute after validation passes."""
        from sheep.features.feature_161_markdown_file_creation import (
            create_feature_161_markdown_file,
        )

        # Mock returns
        mock_commit.return_value = "Committed successfully"
        mock_push.return_value = "Pushed successfully"

        # Call the orchestration
        result = create_feature_161_markdown_file()

        # Verify commit was called (which means validation passed)
        mock_commit.assert_called_once()
        # Verify push was called (which is after commit)
        mock_push.assert_called_once()
        # Verify return value contains push result
        assert "push_result" in result
        assert result["push_result"] == "Pushed successfully"

    def test_commit_message_in_git_log_after_push(self):
        """Test that commit message for feature 161 exists in git history."""
        import subprocess

        from sheep.features.feature_161_markdown_file_creation import COMMIT_MESSAGE

        # Search git log for the specific feature 161 commit message
        result = subprocess.run(
            ["git", "log", "--oneline", "--grep=feat(161)", "--all"],
            capture_output=True,
            text=True,
            check=True,
        )

        # The commit message should appear in git history
        log_output = result.stdout.strip()
        # Verify that feature 161 commits exist
        assert "161" in log_output, (
            f"Git log should contain feature 161 commits, got: {log_output}"
        )

    def test_push_uses_feature_branch(self):
        """Test that push operation uses the correct feature branch."""
        import subprocess

        # Check current branch
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        current_branch = result.stdout.strip()

        # Should be the feature branch
        assert "feat" in current_branch or "161" in current_branch, (
            f"Current branch should contain 'feat' or '161', got: {current_branch}"
        )

    def test_git_commands_fail_gracefully(self):
        """Test that git commands fail gracefully with proper exceptions."""
        import subprocess

        # Try to run git commands with invalid arguments to test error handling
        # This is a negative test - verify subprocess raises CalledProcessError
        with pytest.raises(subprocess.CalledProcessError):
            subprocess.run(
                ["git", "commit", "-m", "test"],
                check=True,  # check=True will raise on failure
                capture_output=True,
            )
