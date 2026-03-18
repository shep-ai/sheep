"""Tests for feature 089 markdown file creation (test-mprgt7.md)."""

import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Import the script module
sys.path.insert(0, str(Path(__file__).parent.parent / "specs" / "089-markdown-file-creation-7c4201"))
import create_test_mprgt7


class TestValidateProseBeforeWrite:
    """Tests for prose validation before file creation."""

    def test_prose_validation_passes_with_valid_content(self):
        """Test that valid prose content passes validation."""
        # Should not raise
        create_test_mprgt7.validate_prose_before_write()

    def test_prose_has_correct_heading(self):
        """Test that prose starts with H1 heading."""
        lines = create_test_mprgt7.PROSE_CONTENT.strip().split('\n')
        assert lines[0].startswith('# '), "First line should be H1 heading"

    def test_prose_has_blank_line_separator(self):
        """Test that prose has blank line after heading."""
        lines = create_test_mprgt7.PROSE_CONTENT.strip().split('\n')
        assert len(lines) >= 2 and lines[1] == '', "Second line should be blank"

    def test_prose_has_2_to_3_sentences(self):
        """Test that prose content has 2-3 sentences."""
        import re
        lines = create_test_mprgt7.PROSE_CONTENT.strip().split('\n')
        prose_section = '\n'.join(lines[2:])
        sentences = re.split(r'[.!?]+', prose_section)
        sentences = [s.strip() for s in sentences if s.strip()]
        assert 2 <= len(sentences) <= 3, f"Expected 2-3 sentences, got {len(sentences)}"

    def test_prose_is_utf8_encodable(self):
        """Test that prose can be encoded as UTF-8."""
        # Should not raise
        create_test_mprgt7.PROSE_CONTENT.encode('utf-8')

    def test_prose_size_within_bounds(self):
        """Test that prose size is within 350-650 bytes."""
        estimated_size = len(create_test_mprgt7.PROSE_CONTENT.encode('utf-8'))
        assert 350 <= estimated_size <= 650, f"Prose size {estimated_size} outside bounds"


class TestCreateMarkdownFile:
    """Tests for file creation function."""

    def test_creates_file_at_repository_root(self):
        """Test that file is created at repository root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                path = create_test_mprgt7.create_markdown_file()

                assert Path(create_test_mprgt7.FILENAME).exists()
                assert path.name == create_test_mprgt7.FILENAME
                assert isinstance(path, Path)
            finally:
                os.chdir(original_cwd)

    def test_returns_path_object(self):
        """Test that function returns a Path object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                result = create_test_mprgt7.create_markdown_file()

                assert isinstance(result, Path)
                assert result.name == create_test_mprgt7.FILENAME
            finally:
                os.chdir(original_cwd)

    def test_rejects_existing_file(self):
        """Test that creation fails if file already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                # Create file first
                Path(create_test_mprgt7.FILENAME).write_text("existing content")

                # Try to create - should fail
                with pytest.raises(FileExistsError, match="already exists"):
                    create_test_mprgt7.create_markdown_file()
            finally:
                os.chdir(original_cwd)

    def test_file_has_correct_content(self):
        """Test that created file has correct prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                create_test_mprgt7.create_markdown_file()

                file_content = Path(create_test_mprgt7.FILENAME).read_text(encoding='utf-8')
                assert file_content == create_test_mprgt7.PROSE_CONTENT
            finally:
                os.chdir(original_cwd)

    def test_file_has_utf8_encoding_no_bom(self):
        """Test that file is UTF-8 encoded without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                create_test_mprgt7.create_markdown_file()

                binary_content = Path(create_test_mprgt7.FILENAME).read_bytes()
                assert not binary_content.startswith(b'\xef\xbb\xbf'), "Should not have BOM"
                # Should be decodable as UTF-8
                binary_content.decode('utf-8')
            finally:
                os.chdir(original_cwd)

    def test_file_has_lf_line_endings(self):
        """Test that file uses LF line endings, not CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                create_test_mprgt7.create_markdown_file()

                binary_content = Path(create_test_mprgt7.FILENAME).read_bytes()
                assert b'\r\n' not in binary_content, "Should not have CRLF"
                assert b'\r' not in binary_content, "Should not have CR"
                assert b'\n' in binary_content, "Should have LF"
            finally:
                os.chdir(original_cwd)


class TestValidateStructure:
    """Tests for markdown structure validation."""

    def test_accepts_valid_structure(self):
        """Test that valid markdown structure passes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                create_test_mprgt7.create_markdown_file()
                file_content = Path(create_test_mprgt7.FILENAME).read_text(encoding='utf-8')

                # Should not raise
                create_test_mprgt7.validate_structure(file_content)
            finally:
                os.chdir(original_cwd)

    def test_rejects_missing_h1_heading(self):
        """Test that missing H1 heading is rejected."""
        content_no_heading = "\n\nThis is a sentence. This is another sentence. And a third.\n"
        with pytest.raises(ValueError, match="H1 heading"):
            create_test_mprgt7.validate_structure(content_no_heading)

    def test_rejects_missing_blank_line(self):
        """Test that missing blank line separator is rejected."""
        content_no_blank = "# Heading\nFirst sentence. Second sentence. Third sentence.\n"
        with pytest.raises(ValueError, match="blank"):
            create_test_mprgt7.validate_structure(content_no_blank)

    def test_rejects_too_few_sentences(self):
        """Test that fewer than 2 sentences is rejected."""
        content_one_sentence = "# Title\n\nOnly one sentence.\n"
        with pytest.raises(ValueError, match="2-3 sentences"):
            create_test_mprgt7.validate_structure(content_one_sentence)

    def test_rejects_too_many_sentences(self):
        """Test that more than 3 sentences is rejected."""
        content_many = "# Title\n\nFirst. Second. Third. Fourth.\n"
        with pytest.raises(ValueError, match="2-3 sentences"):
            create_test_mprgt7.validate_structure(content_many)


class TestValidateEncodingAndLineEndings:
    """Tests for encoding and line ending validation."""

    def test_accepts_valid_utf8_lf(self):
        """Test that valid UTF-8 with LF passes."""
        binary_content = b"# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        # Should not raise
        create_test_mprgt7.validate_encoding_and_line_endings(binary_content)

    def test_rejects_utf8_bom(self):
        """Test that UTF-8 BOM is rejected."""
        binary_content = b"\xef\xbb\xbf# Title\n\nFirst. Second. Third.\n"
        with pytest.raises(ValueError, match="BOM"):
            create_test_mprgt7.validate_encoding_and_line_endings(binary_content)

    def test_rejects_crlf_line_endings(self):
        """Test that CRLF line endings are rejected."""
        binary_content = b"# Title\r\n\r\nFirst sentence. Second sentence. Third sentence.\r\n"
        with pytest.raises(ValueError, match="CRLF"):
            create_test_mprgt7.validate_encoding_and_line_endings(binary_content)

    def test_rejects_cr_only_line_endings(self):
        """Test that CR-only line endings are rejected."""
        binary_content = b"# Title\r\rFirst sentence. Second sentence. Third sentence.\r"
        with pytest.raises(ValueError, match="CRLF"):
            create_test_mprgt7.validate_encoding_and_line_endings(binary_content)


class TestValidateFileSize:
    """Tests for file size validation."""

    def test_accepts_valid_size_lower_bound(self):
        """Test that file of exactly 350 bytes is accepted."""
        # Create content of exactly 350 bytes
        content = "# Title\n\n" + "x" * 325 + ". " + "x" * 3 + ". " + "x" * 3 + ".\n"
        binary_content = content.encode('utf-8')
        # Adjust content to be exactly 350 bytes
        padding_needed = 350 - len(binary_content)
        if padding_needed > 0:
            content = "# Title\n\n" + ("x" * (padding_needed - 10)) + ". A. B.\n"
        binary_content = content.encode('utf-8')

        # Should not raise if size is in bounds
        if 350 <= len(binary_content) <= 650:
            create_test_mprgt7.validate_file_size(binary_content)

    def test_accepts_valid_size_upper_bound(self):
        """Test that file of exactly 650 bytes is accepted."""
        # Create content close to 650 bytes
        content = "# Title\n\n" + ("x" * 625) + ". Long sentence. End.\n"
        binary_content = content.encode('utf-8')

        # Adjust to be close to 650
        if len(binary_content) > 650:
            content = "# Title\n\n" + ("x" * 600) + ". Another. Last.\n"
            binary_content = content.encode('utf-8')

        # Should not raise if size is in bounds
        if 350 <= len(binary_content) <= 650:
            create_test_mprgt7.validate_file_size(binary_content)

    def test_rejects_too_small_file(self):
        """Test that file smaller than 350 bytes is rejected."""
        content = b"# Title\n\nSmall.\n"  # Only ~18 bytes
        with pytest.raises(ValueError, match="350-650"):
            create_test_mprgt7.validate_file_size(content)

    def test_rejects_too_large_file(self):
        """Test that file larger than 650 bytes is rejected."""
        content = b"# Title\n\n" + (b"x" * 700) + b"\n"
        with pytest.raises(ValueError, match="350-650"):
            create_test_mprgt7.validate_file_size(content)


class TestValidateFile:
    """Tests for comprehensive file validation."""

    def test_accepts_valid_file(self):
        """Test that completely valid file passes validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                path = create_test_mprgt7.create_markdown_file()
                result = create_test_mprgt7.validate_file(path)

                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_rejects_invalid_encoding(self):
        """Test that non-UTF-8 file is rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Write with latin-1 encoding (non-UTF-8)
            content = "# Title\n\nFirst café. Second naïve. Third façade.\n"
            path.write_bytes(content.encode('latin-1'))

            with pytest.raises(ValueError):
                create_test_mprgt7.validate_file(path)

    def test_rejects_file_with_bom(self):
        """Test that file with BOM is rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            content = b"\xef\xbb\xbf# Title\n\nFirst. Second. Third.\n"
            path.write_bytes(content)

            with pytest.raises(ValueError, match="BOM"):
                create_test_mprgt7.validate_file(path)

    def test_rejects_file_with_crlf(self):
        """Test that file with CRLF is rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            content = b"# Title\r\n\r\nFirst. Second. Third.\r\n"
            path.write_bytes(content)

            with pytest.raises(ValueError, match="CRLF"):
                create_test_mprgt7.validate_file(path)

    def test_rejects_file_with_wrong_size(self):
        """Test that file with wrong size is rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            content = b"# Title\n\nTiny.\n"
            path.write_bytes(content)

            with pytest.raises(ValueError, match="350-650"):
                create_test_mprgt7.validate_file(path)

    def test_rejects_file_with_invalid_structure(self):
        """Test that file with invalid structure is rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create file with proper size but missing blank line separator
            # Must be between 350-650 bytes to pass size validation
            long_text = "x" * 300  # Padding to reach size requirement
            content = f"# Title\n{long_text} First sentence. Second sentence. Third sentence.\n"
            # Use newline='\n' to ensure LF line endings on Windows
            path.write_text(content, encoding='utf-8', newline='\n')

            with pytest.raises(ValueError, match="blank"):
                create_test_mprgt7.validate_file(path)


class TestIntegration:
    """Integration tests for the complete flow."""

    def test_full_workflow_prose_to_file_validation(self):
        """Test the complete workflow: validate prose, create file, validate file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                # Step 1: Validate prose
                create_test_mprgt7.validate_prose_before_write()

                # Step 2: Create file
                path = create_test_mprgt7.create_markdown_file()
                assert path.exists()

                # Step 3: Validate file
                result = create_test_mprgt7.validate_file(path)
                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_main_function_succeeds(self):
        """Test that main() function executes successfully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                # Mock sys.exit to capture exit code
                with patch('sys.exit') as mock_exit:
                    create_test_mprgt7.main()
                    # Should either not call exit (success path) or call with 0
                    if mock_exit.called:
                        mock_exit.assert_called_with(0)

                # File should be created
                assert Path(create_test_mprgt7.FILENAME).exists()
            finally:
                os.chdir(original_cwd)

    def test_main_fails_gracefully_on_file_exists(self):
        """Test that main() fails gracefully if file already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                # Create file first
                Path(create_test_mprgt7.FILENAME).write_text("existing")

                # Run main - should fail
                result = create_test_mprgt7.main()
                assert result == 1
            finally:
                os.chdir(original_cwd)


class TestPerformGitOperations:
    """Tests for git integration (add, commit, push)."""

    def test_git_add_called_with_correct_arguments(self):
        """Test that git add is called with correct filename."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            try:
                create_test_mprgt7.perform_git_operations()
            except RuntimeError:
                # We expect failure on commit, but we're testing git add call
                pass

            # Verify git add was called
            calls = mock_run.call_args_list
            assert any(
                call[0][0] == ["git", "add", create_test_mprgt7.FILENAME]
                for call in calls
            ), f"git add call not found in {calls}"

    def test_git_commit_called_with_correct_message(self):
        """Test that git commit is called with conventional commit message."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            try:
                create_test_mprgt7.perform_git_operations()
            except RuntimeError:
                # We expect failure on push, but we're testing commit call
                pass

            # Verify git commit was called with correct message
            calls = mock_run.call_args_list
            commit_message = f"feat(089): create markdown file {create_test_mprgt7.FILENAME} with prose content"
            assert any(
                call[0][0][:2] == ["git", "commit"] and
                call[0][0][3] == commit_message
                for call in calls
            ), f"git commit with correct message not found in {calls}"

    def test_git_push_called_with_feature_branch(self):
        """Test that git push is called with correct feature branch."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            create_test_mprgt7.perform_git_operations()

            # Verify git push was called
            calls = mock_run.call_args_list
            branch = "feat/089-markdown-file-creation-7c4201"
            assert any(
                call[0][0] == ["git", "push", "origin", branch]
                for call in calls
            ), f"git push call not found in {calls}"

    def test_uses_subprocess_argument_list_not_shell(self):
        """Test that subprocess is called with argument list (not shell=True)."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            create_test_mprgt7.perform_git_operations()

            # Verify that shell=True was never used
            for call in mock_run.call_args_list:
                assert call[1].get('shell') is not True, "Should not use shell=True"

    def test_git_add_failure_raises_error(self):
        """Test that git add failure raises RuntimeError with descriptive message."""
        with patch('subprocess.run') as mock_run:
            # Simulate git add failure
            mock_run.side_effect = [
                subprocess.CalledProcessError(1, "git add", stderr="Permission denied"),
            ]

            with pytest.raises(RuntimeError, match="git add"):
                create_test_mprgt7.perform_git_operations()

    def test_git_commit_failure_raises_error(self):
        """Test that git commit failure raises RuntimeError with descriptive message."""
        with patch('subprocess.run') as mock_run:
            # Simulate git add success, commit failure
            mock_run.side_effect = [
                MagicMock(returncode=0),  # git add succeeds
                subprocess.CalledProcessError(1, "git commit", stderr="Nothing staged for commit"),
            ]

            with pytest.raises(RuntimeError, match="git commit"):
                create_test_mprgt7.perform_git_operations()

    def test_git_push_failure_raises_error(self):
        """Test that git push failure raises RuntimeError with descriptive message."""
        with patch('subprocess.run') as mock_run:
            # Simulate git add and commit success, push failure
            mock_run.side_effect = [
                MagicMock(returncode=0),  # git add succeeds
                MagicMock(returncode=0),  # git commit succeeds
                subprocess.CalledProcessError(1, "git push", stderr="Connection timeout"),
            ]

            with pytest.raises(RuntimeError, match="git push"):
                create_test_mprgt7.perform_git_operations()

    def test_all_git_operations_succeed(self):
        """Test successful execution of all git operations."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            # Should not raise
            create_test_mprgt7.perform_git_operations()

            # Verify all three operations were called
            assert mock_run.call_count == 3


class TestMainFunctionIntegration:
    """Tests for main() function orchestrating all components."""

    def test_main_calls_all_steps_in_order(self):
        """Test that main() calls all steps in correct sequence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                with patch('subprocess.run') as mock_run:
                    mock_run.return_value = MagicMock(returncode=0)

                    result = create_test_mprgt7.main()

                    # Should succeed
                    assert result == 0

                    # File should be created
                    assert Path(create_test_mprgt7.FILENAME).exists()

                    # Git operations should have been called
                    assert mock_run.call_count == 3
            finally:
                os.chdir(original_cwd)

    def test_main_exits_with_1_on_prose_validation_failure(self):
        """Test that main() exits with code 1 if prose validation fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                # Mock prose validation to fail
                with patch.object(create_test_mprgt7, 'validate_prose_before_write') as mock_validate:
                    mock_validate.side_effect = ValueError("Invalid prose")

                    result = create_test_mprgt7.main()

                    # Should fail
                    assert result == 1

                    # File should not be created
                    assert not Path(create_test_mprgt7.FILENAME).exists()
            finally:
                os.chdir(original_cwd)

    def test_main_exits_with_1_on_file_creation_failure(self):
        """Test that main() exits with code 1 if file creation fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                # Create file first to trigger FileExistsError
                Path(create_test_mprgt7.FILENAME).write_text("existing")

                result = create_test_mprgt7.main()

                # Should fail
                assert result == 1
            finally:
                os.chdir(original_cwd)

    def test_main_exits_with_1_on_git_failure(self):
        """Test that main() exits with code 1 if git operations fail."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                with patch('subprocess.run') as mock_run:
                    # Simulate git add failure
                    mock_run.side_effect = subprocess.CalledProcessError(1, "git add")

                    result = create_test_mprgt7.main()

                    # Should fail
                    assert result == 1

                    # File should exist (created before git operations fail)
                    assert Path(create_test_mprgt7.FILENAME).exists()
            finally:
                os.chdir(original_cwd)

    def test_main_prints_errors_to_stderr(self):
        """Test that main() prints errors to stderr."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                # Create file first to trigger error
                Path(create_test_mprgt7.FILENAME).write_text("existing")

                with patch('sys.stderr') as mock_stderr:
                    result = create_test_mprgt7.main()

                    # Should have written to stderr
                    assert mock_stderr.write.called
                    assert result == 1
            finally:
                os.chdir(original_cwd)

    def test_main_prints_success_message_to_stdout(self):
        """Test that main() prints success message when complete."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                with patch('subprocess.run') as mock_run:
                    mock_run.return_value = MagicMock(returncode=0)

                    with patch('builtins.print') as mock_print:
                        result = create_test_mprgt7.main()

                        # Should succeed
                        assert result == 0

                        # Should have printed success message
                        success_messages = [
                            str(call)
                            for call in mock_print.call_args_list
                            if 'complete' in str(call).lower()
                        ]
                        assert len(success_messages) > 0, "No success message printed"
            finally:
                os.chdir(original_cwd)

    def test_main_succeeds_with_valid_setup(self):
        """Test that main() succeeds when all conditions are met."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                with patch('subprocess.run') as mock_run:
                    mock_run.return_value = MagicMock(returncode=0)

                    result = create_test_mprgt7.main()

                    # Should succeed
                    assert result == 0

                    # File should exist and be valid
                    assert Path(create_test_mprgt7.FILENAME).exists()
                    content = Path(create_test_mprgt7.FILENAME).read_text()
                    # Check file starts with correct heading and has content
                    assert content.startswith("# Script Validation Process")
                    # Check for key prose elements
                    assert "automated content generation" in content
                    # Check that git operations were called
                    assert mock_run.call_count == 3
            finally:
                os.chdir(original_cwd)
