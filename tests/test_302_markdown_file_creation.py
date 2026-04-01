"""Tests for feature 302: Create markdown file test-94uqvv.md with comprehensive validation."""

import os
import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

# Add parent directory to path to import create_file_302
sys.path.insert(0, str(Path(__file__).parent.parent))

from create_file_302 import (
    FILENAME,
    create_file,
    validate_encoding,
    validate_structure,
    git_operations,
    main,
)


class TestFile302Encoding:
    """Tests for file encoding validation (task-2: validate_encoding)."""

    def test_file_without_bom(self, tmp_path):
        """Test that file does not contain UTF-8 BOM (0xEF 0xBB 0xBF)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create the file
            filepath = create_file()

            # Validate encoding
            assert validate_encoding(filepath) is True

            # Verify no BOM in file bytes
            content_bytes = filepath.read_bytes()
            assert not content_bytes.startswith(b"\xef\xbb\xbf"), "File should not contain UTF-8 BOM"

        finally:
            os.chdir(original_cwd)

    def test_file_uses_lf_not_crlf(self, tmp_path):
        """Test that file uses Unix LF (0x0A) not CRLF (0x0D 0x0A) line endings."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create the file
            filepath = create_file()

            # Validate encoding
            assert validate_encoding(filepath) is True

            # Verify LF only, no CRLF
            content_bytes = filepath.read_bytes()
            assert b"\r\n" not in content_bytes, "File should not contain CRLF line endings"
            assert b"\n" in content_bytes, "File should contain LF line endings"

        finally:
            os.chdir(original_cwd)

    def test_validate_encoding_detects_bom(self, tmp_path):
        """Test that validate_encoding() detects and rejects files with BOM."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create a file with BOM
            filepath = Path(FILENAME)
            content_with_bom = b"\xef\xbb\xbf" + "# Test\n\nContent here.\n".encode("utf-8")
            filepath.write_bytes(content_with_bom)

            # Validation should fail
            with pytest.raises(AssertionError, match="BOM"):
                validate_encoding(filepath)

        finally:
            os.chdir(original_cwd)

    def test_validate_encoding_detects_crlf(self, tmp_path):
        """Test that validate_encoding() detects and rejects files with CRLF line endings."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create a file with CRLF
            filepath = Path(FILENAME)
            content_with_crlf = "# Test\r\n\r\nContent here.\r\n".encode("utf-8")
            filepath.write_bytes(content_with_crlf)

            # Validation should fail
            with pytest.raises(AssertionError, match="CRLF|line ending"):
                validate_encoding(filepath)

        finally:
            os.chdir(original_cwd)


class TestFile302Structure:
    """Tests for file structure validation (task-3: validate_structure)."""

    def test_h1_heading_on_line_1(self, tmp_path):
        """Test that H1 heading exists on line 1."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            filepath = create_file()
            assert validate_structure(filepath) is True

            # Verify H1 heading
            content = filepath.read_text(encoding="utf-8")
            lines = content.split("\n")
            assert lines[0].startswith("# "), "First line should start with '# ' (H1 heading)"

        finally:
            os.chdir(original_cwd)

    def test_blank_line_separator(self, tmp_path):
        """Test that blank line exists between heading and prose (line 2)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            filepath = create_file()
            assert validate_structure(filepath) is True

            # Verify blank line
            content = filepath.read_text(encoding="utf-8")
            lines = content.split("\n")
            assert lines[1] == "", "Line 2 should be blank (blank line separator)"

        finally:
            os.chdir(original_cwd)

    def test_sentence_count_2_to_3(self, tmp_path):
        """Test that prose contains 2-3 sentences (detected by period count)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            filepath = create_file()
            assert validate_structure(filepath) is True

            # Verify sentence count
            content = filepath.read_text(encoding="utf-8")
            # Extract prose (after first blank line)
            parts = content.split("\n\n", 1)
            if len(parts) > 1:
                prose = parts[1].strip()
                sentence_count = prose.count(".")
                assert 2 <= sentence_count <= 3, f"Prose should have 2-3 sentences, found {sentence_count}"

        finally:
            os.chdir(original_cwd)

    def test_file_size_in_range(self, tmp_path):
        """Test that file size is between 300-800 bytes."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            filepath = create_file()
            assert validate_structure(filepath) is True

            # Verify file size
            file_size = filepath.stat().st_size
            assert 300 < file_size < 800, f"File size {file_size} should be between 300-800 bytes"

        finally:
            os.chdir(original_cwd)

    def test_validate_structure_rejects_missing_h1(self, tmp_path):
        """Test that validate_structure() rejects files without H1 heading."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create file without H1
            filepath = Path(FILENAME)
            filepath.write_text("No heading here.\n\nJust prose content here.\n", encoding="utf-8")

            # Validation should fail
            with pytest.raises(AssertionError, match="H1|heading"):
                validate_structure(filepath)

        finally:
            os.chdir(original_cwd)

    def test_validate_structure_rejects_missing_blank_line(self, tmp_path):
        """Test that validate_structure() rejects files without blank line separator."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create file without blank line
            filepath = Path(FILENAME)
            filepath.write_text("# Title\nProse content.\n", encoding="utf-8")

            # Validation should fail
            with pytest.raises(AssertionError, match="blank line|line 2"):
                validate_structure(filepath)

        finally:
            os.chdir(original_cwd)

    def test_validate_structure_rejects_too_few_sentences(self, tmp_path):
        """Test that validate_structure() rejects prose with fewer than 2 sentences."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create file with only 1 sentence
            filepath = Path(FILENAME)
            filepath.write_text("# Title\n\nOnly one sentence.\n", encoding="utf-8")

            # Validation should fail
            with pytest.raises(AssertionError, match="2-3 sentences|sentence"):
                validate_structure(filepath)

        finally:
            os.chdir(original_cwd)

    def test_validate_structure_rejects_too_many_sentences(self, tmp_path):
        """Test that validate_structure() rejects prose with more than 3 sentences."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create file with 4 sentences
            filepath = Path(FILENAME)
            filepath.write_text(
                "# Title\n\nFirst sentence. Second sentence. Third sentence. Fourth sentence.\n",
                encoding="utf-8"
            )

            # Validation should fail
            with pytest.raises(AssertionError, match="2-3 sentences|sentence"):
                validate_structure(filepath)

        finally:
            os.chdir(original_cwd)

    def test_validate_structure_rejects_file_too_small(self, tmp_path):
        """Test that validate_structure() rejects files smaller than 300 bytes."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create a small file
            filepath = Path(FILENAME)
            filepath.write_text("# T\n\nA. B.\n", encoding="utf-8")

            # Validation should fail
            with pytest.raises(AssertionError, match="size|bytes"):
                validate_structure(filepath)

        finally:
            os.chdir(original_cwd)

    def test_validate_structure_rejects_file_too_large(self, tmp_path):
        """Test that validate_structure() rejects files larger than 800 bytes."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create a large file with 2-3 sentences to pass sentence count check
            filepath = Path(FILENAME)
            large_content = "# Title\n\n" + ("A " * 250) + ". " + ("B " * 250) + ". " + ("C " * 50) + ".\n"
            filepath.write_text(large_content, encoding="utf-8")

            # Validation should fail
            with pytest.raises(AssertionError, match="size|bytes"):
                validate_structure(filepath)

        finally:
            os.chdir(original_cwd)


class TestFile302IntegrationValidation:
    """Integration tests for validate_encoding and validate_structure together."""

    def test_both_validations_pass_on_created_file(self, tmp_path):
        """Test that both validate_encoding and validate_structure pass on created file."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            filepath = create_file()

            # Both validations should pass
            assert validate_encoding(filepath) is True
            assert validate_structure(filepath) is True

        finally:
            os.chdir(original_cwd)


class TestFile302GitOperations:
    """Tests for git operations (task-4: git add, commit, push)."""

    def test_git_operations_executes_git_add(self, tmp_path):
        """Test that git_operations() executes git add command."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            filepath = create_file()

            with mock.patch('subprocess.run') as mock_run:
                git_operations()

                # Verify git add was called with correct arguments
                calls = [call[0][0] for call in mock_run.call_args_list]
                assert ['git', 'add', 'test-94uqvv.md'] in calls, (
                    "git add command should be executed with correct filename"
                )
        finally:
            os.chdir(original_cwd)

    def test_git_operations_executes_git_commit(self, tmp_path):
        """Test that git_operations() executes git commit with conventional message."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            filepath = create_file()

            with mock.patch('subprocess.run') as mock_run:
                git_operations()

                # Verify git commit was called with correct message
                calls = [call[0][0] for call in mock_run.call_args_list]
                expected_msg = "feat(302): create markdown file test-94uqvv.md with prose content"

                commit_call = None
                for call in calls:
                    if call[0:2] == ['git', 'commit']:
                        commit_call = call
                        break

                assert commit_call is not None, "git commit command should be executed"
                assert commit_call[3] == expected_msg, (
                    f"Commit message should be '{expected_msg}'"
                )
        finally:
            os.chdir(original_cwd)

    def test_git_operations_executes_git_push(self, tmp_path):
        """Test that git_operations() executes git push command."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            filepath = create_file()

            with mock.patch('subprocess.run') as mock_run:
                git_operations()

                # Verify git push was called with correct arguments
                calls = [call[0][0] for call in mock_run.call_args_list]
                assert ['git', 'push', '-u', 'origin', 'HEAD'] in calls, (
                    "git push command should be executed with correct arguments"
                )
        finally:
            os.chdir(original_cwd)

    def test_git_operations_uses_subprocess_check_true(self, tmp_path):
        """Test that git_operations() uses subprocess.run with check=True."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            filepath = create_file()

            with mock.patch('subprocess.run') as mock_run:
                git_operations()

                # Verify all calls used check=True
                for call in mock_run.call_args_list:
                    assert call[1].get('check') is True, (
                        "subprocess.run should be called with check=True for strict error handling"
                    )
        finally:
            os.chdir(original_cwd)

    def test_git_operations_fails_on_subprocess_error(self, tmp_path):
        """Test that git_operations() raises CalledProcessError on git failure."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            filepath = create_file()

            with mock.patch('subprocess.run') as mock_run:
                error = subprocess.CalledProcessError(1, ['git', 'push'])
                mock_run.side_effect = error

                with pytest.raises(subprocess.CalledProcessError):
                    git_operations()
        finally:
            os.chdir(original_cwd)


class TestFile302MainFunction:
    """Tests for main() function orchestration (task-5)."""

    def test_main_function_creates_file(self, tmp_path):
        """Test that main() function creates the markdown file."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            with mock.patch('subprocess.run'):
                with mock.patch('sys.exit'):
                    main()

                    filepath = Path('test-94uqvv.md')
                    assert filepath.exists(), "main() should create the markdown file"
        finally:
            os.chdir(original_cwd)

    def test_main_function_calls_git_operations(self, tmp_path):
        """Test that main() function calls git operations after validation."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            with mock.patch('subprocess.run') as mock_run:
                with mock.patch('sys.exit'):
                    main()

                    # Verify that git operations were attempted
                    git_commands = [
                        call[0][0]
                        for call in mock_run.call_args_list
                        if call[0] and call[0][0][0] == 'git'
                    ]
                    assert len(git_commands) > 0, (
                        "main() should call git operations after file validation"
                    )
        finally:
            os.chdir(original_cwd)

    def test_main_function_exits_success(self, tmp_path):
        """Test that main() exits with code 0 on successful completion."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            with mock.patch('subprocess.run'):
                with mock.patch('sys.exit') as mock_exit:
                    main()

                    if mock_exit.called:
                        assert mock_exit.call_args[0][0] == 0, (
                            "main() should exit with code 0 on success"
                        )
        finally:
            os.chdir(original_cwd)

    def test_main_function_exits_failure(self, tmp_path):
        """Test that main() exits with non-zero code on failure."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create a directory to block file creation
            bad_path = Path('test-94uqvv.md')
            bad_path.mkdir(exist_ok=True)

            with mock.patch('subprocess.run'):
                with mock.patch('sys.exit') as mock_exit:
                    main()

                    if mock_exit.called:
                        assert mock_exit.call_args[0][0] != 0, (
                            "main() should exit with non-zero code on failure"
                        )
        finally:
            os.chdir(original_cwd)

    def test_main_function_orchestrates_all_phases(self, tmp_path):
        """Integration test: main() orchestrates file creation, validation, and git operations."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            with mock.patch('subprocess.run') as mock_run:
                mock_run.return_value = mock.Mock(returncode=0)

                with mock.patch('sys.exit'):
                    main()

                    filepath = Path('test-94uqvv.md')
                    assert filepath.exists(), "File should be created by main()"

                    git_commands = [
                        call[0][0]
                        for call in mock_run.call_args_list
                        if call[0] and call[0][0][0] == 'git'
                    ]
                    assert len(git_commands) >= 3, (
                        "main() should call at least 3 git commands (add, commit, push)"
                    )
        finally:
            os.chdir(original_cwd)
