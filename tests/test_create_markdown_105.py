"""Tests for markdown file creation and validation for feature 105."""

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest


class TestFileCreation:
    """Tests for file creation using pathlib.Path.write_text()."""

    def test_file_does_not_exist_before_creation(self):
        """Test that file does not exist before creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test-knejqo.md"
            assert not test_file.exists()

    def test_creates_file_at_correct_path(self):
        """Test that create_markdown_file creates file at correct path."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp directory for file creation
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_knejqo.create_markdown_file()
                assert path.exists()
                assert path.name == "test-knejqo.md"
            finally:
                os.chdir(original_cwd)

    def test_file_is_created_with_correct_encoding(self):
        """Test that file is created with UTF-8 encoding."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_knejqo.create_markdown_file()
                # File should be readable as UTF-8
                content = path.read_text(encoding='utf-8')
                assert isinstance(content, str)
                assert len(content) > 0
            finally:
                os.chdir(original_cwd)

    def test_file_contains_hardcoded_prose_content(self):
        """Test that file contains the hardcoded prose content."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_knejqo.create_markdown_file()
                content = path.read_text(encoding='utf-8')
                assert "# The Beauty of Persistent Systems" in content
                assert "infrastructure" in content
            finally:
                os.chdir(original_cwd)


class TestStructureValidation:
    """Tests for markdown structure validation (H1 heading, blank line, sentences)."""

    def test_first_line_is_h1_heading(self):
        """Test that first line is H1 heading."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_knejqo.create_markdown_file()
                text_content = path.read_text(encoding='utf-8')
                lines = text_content.strip().split('\n')
                assert lines[0].startswith('# ')
            finally:
                os.chdir(original_cwd)

    def test_validates_h1_heading_correctly(self):
        """Test that validate_structure correctly identifies H1 heading."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        # Valid H1 content
        valid_content = "# Heading\n\nSentence one. Sentence two. Sentence three."
        # Should not raise
        create_test_knejqo.validate_structure(valid_content)

    def test_raises_when_h1_heading_missing(self):
        """Test that validate_structure raises when H1 heading is missing."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        invalid_content = "Not a heading\n\nSentence one. Sentence two. Sentence three."
        with pytest.raises(ValueError, match="H1 heading"):
            create_test_knejqo.validate_structure(invalid_content)

    def test_second_line_is_blank_separator(self):
        """Test that second line is blank separator."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_knejqo.create_markdown_file()
                text_content = path.read_text(encoding='utf-8')
                lines = text_content.strip().split('\n')
                assert lines[1] == ''
            finally:
                os.chdir(original_cwd)

    def test_raises_when_blank_line_missing(self):
        """Test that validate_structure raises when blank line is missing."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        invalid_content = "# Heading\nSentence one. Sentence two. Sentence three."
        with pytest.raises(ValueError, match="blank"):
            create_test_knejqo.validate_structure(invalid_content)

    def test_prose_contains_two_or_three_sentences(self):
        """Test that prose content has 2-3 sentences."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_knejqo.create_markdown_file()
                text_content = path.read_text(encoding='utf-8')
                lines = text_content.strip().split('\n')
                prose_section = '\n'.join(lines[2:])
                sentence_count = prose_section.count('.')
                assert 2 <= sentence_count <= 3
            finally:
                os.chdir(original_cwd)

    def test_raises_when_sentence_count_too_low(self):
        """Test that validate_structure raises when sentence count is less than 2."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        invalid_content = "# Heading\n\nOnly one sentence."
        with pytest.raises(ValueError, match="2-3 sentences"):
            create_test_knejqo.validate_structure(invalid_content)

    def test_raises_when_sentence_count_too_high(self):
        """Test that validate_structure raises when sentence count exceeds 3."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        invalid_content = "# Heading\n\nFirst. Second. Third. Fourth."
        with pytest.raises(ValueError, match="2-3 sentences"):
            create_test_knejqo.validate_structure(invalid_content)


class TestEncodingValidation:
    """Tests for UTF-8 encoding validation (no BOM)."""

    def test_file_uses_utf8_encoding(self):
        """Test that file is UTF-8 encoded."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_knejqo.create_markdown_file()
                binary_content = path.read_bytes()
                # Should not have UTF-8 BOM
                assert not binary_content.startswith(b'\xef\xbb\xbf')
            finally:
                os.chdir(original_cwd)

    def test_raises_when_utf8_bom_present(self):
        """Test that validate_encoding_and_line_endings raises when BOM is present."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        # UTF-8 BOM bytes
        binary_content = b'\xef\xbb\xbf' + "# Heading\n\nSentence. Sentence. Sentence.".encode('utf-8')
        with pytest.raises(ValueError, match="BOM"):
            create_test_knejqo.validate_encoding_and_line_endings(binary_content)


class TestLineEndingValidation:
    """Tests for Unix LF line ending validation."""

    def test_file_uses_unix_lf_line_endings(self):
        """Test that file uses Unix LF line endings."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_knejqo.create_markdown_file()
                binary_content = path.read_bytes()
                # Should not have CRLF
                assert b'\r\n' not in binary_content
                # Should have LF
                assert b'\n' in binary_content
            finally:
                os.chdir(original_cwd)

    def test_raises_when_crlf_present(self):
        """Test that validate_encoding_and_line_endings raises when CRLF is present."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        binary_content = "# Heading\r\n\r\nSentence. Sentence. Sentence.\r\n".encode('utf-8')
        with pytest.raises(ValueError, match="CRLF"):
            create_test_knejqo.validate_encoding_and_line_endings(binary_content)


class TestFileSizeValidation:
    """Tests for file size validation (400-600 bytes)."""

    def test_file_size_is_within_expected_range(self):
        """Test that file size is between 400-600 bytes."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_knejqo.create_markdown_file()
                binary_content = path.read_bytes()
                file_size = len(binary_content)
                assert 400 <= file_size <= 600
            finally:
                os.chdir(original_cwd)

    def test_raises_when_file_size_too_small(self):
        """Test that validate_file_size raises when file is too small."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        binary_content = "# H\n\nS.".encode('utf-8')
        with pytest.raises(ValueError, match="outside expected range"):
            create_test_knejqo.validate_file_size(binary_content)

    def test_raises_when_file_size_too_large(self):
        """Test that validate_file_size raises when file is too large."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        # Create content larger than 600 bytes
        binary_content = ("# Heading\n\n" + "x" * 700).encode('utf-8')
        with pytest.raises(ValueError, match="outside expected range"):
            create_test_knejqo.validate_file_size(binary_content)


class TestValidateFileIntegration:
    """Integration tests for validate_file function."""

    def test_validate_file_passes_for_created_file(self):
        """Test that validate_file passes for file created by create_markdown_file."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_knejqo.create_markdown_file()
                # Should not raise
                result = create_test_knejqo.validate_file(path)
                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_validate_file_checks_all_properties(self):
        """Test that validate_file checks encoding, size, and structure."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_knejqo.create_markdown_file()
                # Read binary to verify properties
                binary_content = path.read_bytes()
                text_content = path.read_text(encoding='utf-8')

                # Should pass all validations
                create_test_knejqo.validate_encoding_and_line_endings(binary_content)
                create_test_knejqo.validate_file_size(binary_content)
                create_test_knejqo.validate_structure(text_content)
            finally:
                os.chdir(original_cwd)


class TestGitWorkflow:
    """Tests for git workflow functions (stage, commit, push)."""

    def test_stage_file_calls_git_add_with_correct_filename(self):
        """Test that stage_file calls git add with the correct filename."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            create_test_knejqo.stage_file("test-file.md")

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert args[0] == ["git", "add", "test-file.md"]
            assert kwargs.get("check") is True

    def test_stage_file_raises_on_git_failure(self):
        """Test that stage_file raises RuntimeError when git add fails."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git add", stderr="error message"
            )
            with pytest.raises(RuntimeError, match="git add failed"):
                create_test_knejqo.stage_file("test-file.md")

    def test_stage_file_returns_true_on_success(self):
        """Test that stage_file returns True on successful execution."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = create_test_knejqo.stage_file("test-file.md")
            assert result is True

    def test_create_commit_calls_git_commit_with_no_verify_flag(self):
        """Test that create_commit calls git commit with --no-verify flag."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            create_test_knejqo.create_commit("feat(105): test message")

            # Verify subprocess.run was called with --no-verify flag
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert "--no-verify" in args[0]
            assert "git" in args[0]
            assert "commit" in args[0]

    def test_create_commit_includes_conventional_commit_message(self):
        """Test that create_commit uses the provided message."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        message = "feat(105): create markdown file test-knejqo.md with prose content"
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            create_test_knejqo.create_commit(message)

            # Verify the message is included in the call
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert message in args[0]

    def test_create_commit_raises_on_git_failure(self):
        """Test that create_commit raises RuntimeError when git commit fails."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git commit", stderr="error message"
            )
            with pytest.raises(RuntimeError, match="git commit failed"):
                create_test_knejqo.create_commit("test message")

    def test_create_commit_returns_true_on_success(self):
        """Test that create_commit returns True on successful execution."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = create_test_knejqo.create_commit("test message")
            assert result is True

    def test_push_to_remote_calls_git_push_with_upstream_flag(self):
        """Test that push_to_remote calls git push with -u flag."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            create_test_knejqo.push_to_remote()

            # Verify subprocess.run was called with -u origin HEAD
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert args[0] == ["git", "push", "-u", "origin", "HEAD"]
            assert kwargs.get("check") is True

    def test_push_to_remote_raises_on_git_failure(self):
        """Test that push_to_remote raises RuntimeError when git push fails."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "git push", stderr="error message"
            )
            with pytest.raises(RuntimeError, match="git push failed"):
                create_test_knejqo.push_to_remote()

    def test_push_to_remote_returns_true_on_success(self):
        """Test that push_to_remote returns True on successful execution."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = create_test_knejqo.push_to_remote()
            assert result is True

    def test_run_git_workflow_executes_all_three_commands(self):
        """Test that run_git_workflow calls stage, commit, and push in order."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with patch.object(create_test_knejqo, "stage_file") as mock_stage, \
             patch.object(create_test_knejqo, "create_commit") as mock_commit, \
             patch.object(create_test_knejqo, "push_to_remote") as mock_push:

            mock_stage.return_value = True
            mock_commit.return_value = True
            mock_push.return_value = True

            create_test_knejqo.run_git_workflow("test.md", "test message")

            # Verify all three functions were called in order
            mock_stage.assert_called_once_with("test.md")
            mock_commit.assert_called_once_with("test message")
            mock_push.assert_called_once()

    def test_run_git_workflow_returns_true_on_success(self):
        """Test that run_git_workflow returns True when all steps succeed."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with patch.object(create_test_knejqo, "stage_file") as mock_stage, \
             patch.object(create_test_knejqo, "create_commit") as mock_commit, \
             patch.object(create_test_knejqo, "push_to_remote") as mock_push:

            mock_stage.return_value = True
            mock_commit.return_value = True
            mock_push.return_value = True

            result = create_test_knejqo.run_git_workflow("test.md", "test message")
            assert result is True

    def test_run_git_workflow_raises_if_stage_fails(self):
        """Test that run_git_workflow raises if stage_file fails."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with patch.object(create_test_knejqo, "stage_file") as mock_stage, \
             patch.object(create_test_knejqo, "push_to_remote"):

            mock_stage.side_effect = RuntimeError("git add failed")

            with pytest.raises(RuntimeError):
                create_test_knejqo.run_git_workflow("test.md", "test message")

    def test_run_git_workflow_raises_if_commit_fails(self):
        """Test that run_git_workflow raises if create_commit fails."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with patch.object(create_test_knejqo, "stage_file") as mock_stage, \
             patch.object(create_test_knejqo, "create_commit") as mock_commit:

            mock_stage.return_value = True
            mock_commit.side_effect = RuntimeError("git commit failed")

            with pytest.raises(RuntimeError):
                create_test_knejqo.run_git_workflow("test.md", "test message")


class TestFullIntegration:
    """Integration tests for complete workflow (create, validate, commit)."""

    def test_full_workflow_creates_validates_and_commits(self):
        """Integration test: create file, validate, and stage/commit/push."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Mock all git operations
                with patch.object(create_test_knejqo, "stage_file") as mock_stage, \
                     patch.object(create_test_knejqo, "create_commit") as mock_commit, \
                     patch.object(create_test_knejqo, "push_to_remote") as mock_push:

                    mock_stage.return_value = True
                    mock_commit.return_value = True
                    mock_push.return_value = True

                    # Phase 1: Create file
                    file_path = create_test_knejqo.create_markdown_file()
                    assert file_path.exists()

                    # Phase 2: Validate file
                    result = create_test_knejqo.validate_file(file_path)
                    assert result is True

                    # Phase 3: Git workflow
                    create_test_knejqo.run_git_workflow(
                        str(file_path),
                        "feat(105): create markdown file test-knejqo.md with prose content"
                    )

                    # Verify all git operations were called
                    mock_stage.assert_called_once()
                    mock_commit.assert_called_once()
                    mock_push.assert_called_once()

            finally:
                os.chdir(original_cwd)

    def test_full_workflow_via_main_function(self):
        """Test that main() executes the complete workflow."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Mock git operations
                with patch.object(create_test_knejqo, "stage_file") as mock_stage, \
                     patch.object(create_test_knejqo, "create_commit") as mock_commit, \
                     patch.object(create_test_knejqo, "push_to_remote") as mock_push:

                    mock_stage.return_value = True
                    mock_commit.return_value = True
                    mock_push.return_value = True

                    result = create_test_knejqo.main()
                    assert result == 0

                    # Verify file was created and git operations were called
                    assert (Path(tmpdir) / "test-knejqo.md").exists()
                    mock_stage.assert_called_once()
                    mock_commit.assert_called_once()
                    mock_push.assert_called_once()

            finally:
                os.chdir(original_cwd)


class TestMainFunction:
    """Tests for main function."""

    def test_main_returns_0_on_success(self):
        """Test that main returns 0 on successful execution."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                # Mock git operations since we can't actually push in tests
                with patch.object(create_test_knejqo, "stage_file") as mock_stage, \
                     patch.object(create_test_knejqo, "create_commit") as mock_commit, \
                     patch.object(create_test_knejqo, "push_to_remote") as mock_push:
                    mock_stage.return_value = True
                    mock_commit.return_value = True
                    mock_push.return_value = True
                    result = create_test_knejqo.main()
                    assert result == 0
                    # Verify file was created
                    assert (Path(tmpdir) / "test-knejqo.md").exists()
                    # Verify git workflow was executed
                    mock_stage.assert_called_once()
                    mock_commit.assert_called_once()
                    mock_push.assert_called_once()
            finally:
                os.chdir(original_cwd)

    def test_main_returns_1_on_error(self):
        """Test that main returns 1 when an error occurs."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                # Mock create_markdown_file to raise an error
                with patch.object(create_test_knejqo, 'create_markdown_file', side_effect=Exception("Test error")):
                    result = create_test_knejqo.main()
                    assert result == 1
            finally:
                os.chdir(original_cwd)

    def test_main_executes_create_validate_and_commit_in_order(self):
        """Test that main executes file creation, validation, and git workflow."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import create_test_knejqo

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                with patch.object(create_test_knejqo, 'validate_file') as mock_validate, \
                     patch.object(create_test_knejqo, 'stage_file') as mock_stage, \
                     patch.object(create_test_knejqo, 'create_commit') as mock_commit, \
                     patch.object(create_test_knejqo, 'push_to_remote') as mock_push:
                    mock_validate.return_value = True
                    mock_stage.return_value = True
                    mock_commit.return_value = True
                    mock_push.return_value = True
                    result = create_test_knejqo.main()
                    assert result == 0
                    # Verify all operations were called in order
                    assert mock_validate.called
                    assert mock_stage.called
                    assert mock_commit.called
                    assert mock_push.called
            finally:
                os.chdir(original_cwd)
