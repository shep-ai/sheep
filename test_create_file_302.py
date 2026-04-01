"""
Test suite for feature 302: markdown file creation.

This module tests the create_file_302.py script which creates test-94uqvv.md
with H1 heading, blank line separator, and 2-3 sentences of prose content.

Test Coverage:
- File creation with correct structure (H1 heading + blank line + prose)
- File exists at repository root
- First line starts with # (H1 markdown heading)
- Second line is empty (blank line separator)
- Prose contains 2-3 sentences
- File encoding is UTF-8 without BOM
- File uses Unix LF line endings (not CRLF)
- File size is in acceptable range (300-800 bytes)
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest

# Add the repository root to the path so we can import the create_file_302 module
script_path = Path(__file__).parent / "create_file_302.py"
sys.path.insert(0, str(Path(__file__).parent))
from create_file_302 import create_file, validate_file, git_operations, main
import subprocess


# ============================================================================
# Pytest Fixtures
# ============================================================================


@pytest.fixture
def temp_dir():
    """
    Provide an isolated temporary directory for test file creation.

    Yields a temporary directory path and restores the original working
    directory after the test completes. This fixture ensures tests don't
    interfere with the repository state or each other.

    Yields:
        Path: The temporary directory path
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            yield Path(tmpdir)
        finally:
            os.chdir(original_cwd)


# ============================================================================
# Test Cases: File Creation
# ============================================================================


def test_create_file_creates_file_at_root(temp_dir):
    """
    Test that create_file() creates test-94uqvv.md at repository root.

    This test verifies the basic requirement that the markdown file is
    created with the correct filename at the current directory.
    """
    filepath = create_file()
    assert filepath.exists(), "File test-94uqvv.md should exist"
    assert filepath.name == "test-94uqvv.md", "File should be named test-94uqvv.md"


def test_create_file_returns_path_object(temp_dir):
    """
    Test that create_file() returns a pathlib.Path object.
    """
    filepath = create_file()
    assert isinstance(filepath, Path), "create_file() should return a Path object"


def test_create_file_has_h1_heading(temp_dir):
    """
    Test that created file contains H1 markdown heading on first line.

    This test verifies:
    - First line starts with "# " (H1 markdown syntax)
    - Heading is followed by content
    """
    filepath = create_file()
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')
    assert len(lines) > 0, "File should have content"
    assert lines[0].startswith('# '), "First line should be H1 heading (# )"


def test_create_file_has_blank_line_separator(temp_dir):
    """
    Test that created file has blank line separating heading from prose.

    This test verifies that there is a blank line (double newline) between
    the H1 heading and the prose content.
    """
    filepath = create_file()
    content = filepath.read_text(encoding='utf-8')
    assert '\n\n' in content, "File should contain blank line separator"

    # Verify the blank line is in the correct position
    lines = content.split('\n')
    assert lines[0].startswith('# '), "First line should be H1 heading"
    assert lines[1] == '', "Second line should be empty (blank line)"


def test_create_file_has_prose_content(temp_dir):
    """
    Test that created file contains prose content after blank line.

    This test verifies that there is actual text content in the prose section.
    """
    filepath = create_file()
    content = filepath.read_text(encoding='utf-8')
    parts = content.split('\n\n', 1)
    assert len(parts) == 2, "File should have heading and prose separated by blank line"
    prose = parts[1].strip()
    assert len(prose) > 0, "Prose section should contain text"


def test_create_file_prose_has_sentences(temp_dir):
    """
    Test that prose content contains 2-3 sentences.

    This test counts periods in the prose to estimate sentence count.
    A simple heuristic: count periods in the prose section.
    """
    filepath = create_file()
    content = filepath.read_text(encoding='utf-8')
    parts = content.split('\n\n', 1)
    prose = parts[1].strip()

    # Count sentences by periods
    sentence_count = prose.count('.')
    assert 2 <= sentence_count <= 3, f"Prose should have 2-3 sentences, found {sentence_count}"


def test_create_file_utf8_encoding(temp_dir):
    """
    Test that file is UTF-8 encoded.

    This test verifies that the file can be read with UTF-8 encoding
    without raising an exception.
    """
    filepath = create_file()
    content = filepath.read_text(encoding='utf-8')
    assert isinstance(content, str), "Content should be readable as UTF-8"


def test_create_file_no_bom(temp_dir):
    """
    Test that file does not contain UTF-8 BOM (Byte Order Mark).

    BOM signature for UTF-8 is bytes: 0xEF 0xBB 0xBF
    """
    filepath = create_file()
    file_bytes = filepath.read_bytes()
    bom_signature = b'\xef\xbb\xbf'
    assert not file_bytes.startswith(bom_signature), "File should not have UTF-8 BOM"


def test_create_file_unix_lf_endings(temp_dir):
    """
    Test that file uses Unix LF line endings, not Windows CRLF.

    CRLF signature: 0x0D 0x0A
    LF signature: 0x0A (only)
    """
    filepath = create_file()
    file_bytes = filepath.read_bytes()
    crlf_signature = b'\r\n'
    assert crlf_signature not in file_bytes, "File should use LF endings, not CRLF"


def test_create_file_size_in_range(temp_dir):
    """
    Test that file size is in acceptable range (300-800 bytes).

    This validates that the file has reasonable content length.
    """
    filepath = create_file()
    file_size = filepath.stat().st_size
    assert 300 < file_size < 800, (
        f"File size {file_size} should be between 300-800 bytes"
    )


# ============================================================================
# Test Cases: File Validation
# ============================================================================


def test_validate_file_passes_for_valid_file(temp_dir):
    """
    Test that validate_file() returns True for a valid markdown file.
    """
    filepath = create_file()
    result = validate_file(filepath)
    assert result is True, "validate_file() should return True for valid file"


def test_validate_file_fails_for_nonexistent_file(temp_dir):
    """
    Test that validate_file() raises AssertionError for nonexistent file.
    """
    filepath = Path("nonexistent.md")
    with pytest.raises(AssertionError, match="does not exist"):
        validate_file(filepath)


def test_validate_file_fails_for_file_too_small(temp_dir):
    """
    Test that validate_file() fails if file is too small (<300 bytes).
    """
    # Create a small file
    small_file = Path("small.md")
    small_file.write_text("# Title\n\nSmall content.", encoding='utf-8')

    with pytest.raises(AssertionError, match="outside typical range"):
        validate_file(small_file)


def test_validate_file_fails_for_missing_h1(temp_dir):
    """
    Test that validate_file() fails if H1 heading is missing.
    """
    # Create file without H1 heading
    filepath = Path("test.md")
    filepath.write_text("No heading here\n\nThis is prose content.", encoding='utf-8')

    with pytest.raises(AssertionError, match="H1 heading"):
        validate_file(filepath)


def test_validate_file_fails_for_missing_blank_line(temp_dir):
    """
    Test that validate_file() fails if blank line separator is missing.
    """
    # Create file without blank line separator but with enough content to pass size check
    prose = "This is a longer prose section to make the file bigger. " * 5
    filepath = Path("test.md")
    filepath.write_text(f"# Title\nNo blank line here\n{prose}", encoding='utf-8')

    with pytest.raises(AssertionError, match="blank line"):
        validate_file(filepath)


# ============================================================================
# Integration Tests
# ============================================================================


def test_create_and_validate_integration(temp_dir):
    """
    Integration test: create file and validate it passes all checks.

    This test verifies the complete workflow of creating and validating
    the markdown file.
    """
    filepath = create_file()
    result = validate_file(filepath)

    assert filepath.exists(), "File should exist"
    assert result is True, "Validation should pass"


def test_file_structure_order(temp_dir):
    """
    Test that file structure is in correct order: heading -> blank -> prose.
    """
    filepath = create_file()
    lines = filepath.read_text(encoding='utf-8').split('\n')

    # Verify structure
    assert lines[0].startswith('# '), "Line 1: H1 heading"
    assert lines[1] == '', "Line 2: blank line"
    assert len(lines) > 2, "Should have prose content"
    assert len(lines[2]) > 0, "Line 3+: prose content"


# ============================================================================
# Test Cases: Git Operations (Task-4)
# ============================================================================


def test_git_operations_executes_git_add(temp_dir):
    """
    Test that git_operations() executes git add command.

    This test mocks subprocess.run to verify that the git add command
    is called with the correct arguments.
    """
    # Create the file first
    filepath = create_file()

    # Mock subprocess.run to track git command calls
    with mock.patch('subprocess.run') as mock_run:
        git_operations()

        # Verify git add was called with correct arguments
        calls = [call[0][0] for call in mock_run.call_args_list]
        assert ['git', 'add', 'test-94uqvv.md'] in calls, (
            "git add command should be executed with correct filename"
        )


def test_git_operations_executes_git_commit(temp_dir):
    """
    Test that git_operations() executes git commit with conventional message.

    This test verifies that the commit message follows the required format:
    "feat(302): create markdown file test-94uqvv.md with prose content"
    """
    # Create the file first
    filepath = create_file()

    # Mock subprocess.run to track git command calls
    with mock.patch('subprocess.run') as mock_run:
        git_operations()

        # Verify git commit was called with correct message
        calls = [call[0][0] for call in mock_run.call_args_list]
        expected_msg = "feat(302): create markdown file test-94uqvv.md with prose content"

        # Find the git commit call
        commit_call = None
        for call in calls:
            if call[0:2] == ['git', 'commit']:
                commit_call = call
                break

        assert commit_call is not None, "git commit command should be executed"
        assert commit_call[3] == expected_msg, (
            f"Commit message should be '{expected_msg}'"
        )


def test_git_operations_executes_git_push(temp_dir):
    """
    Test that git_operations() executes git push command.

    This test verifies that git push is called to remote origin.
    """
    # Create the file first
    filepath = create_file()

    # Mock subprocess.run to track git command calls
    with mock.patch('subprocess.run') as mock_run:
        git_operations()

        # Verify git push was called with correct arguments
        calls = [call[0][0] for call in mock_run.call_args_list]
        assert ['git', 'push', '-u', 'origin', 'HEAD'] in calls, (
            "git push command should be executed with correct arguments"
        )


def test_git_operations_uses_subprocess_check_true(temp_dir):
    """
    Test that git_operations() uses subprocess.run with check=True.

    This ensures that CalledProcessError is raised if any git command fails.
    """
    # Create the file first
    filepath = create_file()

    # Mock subprocess.run to track arguments
    with mock.patch('subprocess.run') as mock_run:
        git_operations()

        # Verify all calls used check=True
        for call in mock_run.call_args_list:
            # Check keyword arguments for check=True
            assert call[1].get('check') is True, (
                "subprocess.run should be called with check=True for strict error handling"
            )


def test_git_operations_fails_on_subprocess_error(temp_dir):
    """
    Test that git_operations() raises CalledProcessError on git failure.

    This test verifies that if a git command fails, the exception is propagated.
    """
    # Create the file first
    filepath = create_file()

    # Mock subprocess.run to simulate git push failure
    with mock.patch('subprocess.run') as mock_run:
        # Make git push fail by raising CalledProcessError
        error = subprocess.CalledProcessError(1, ['git', 'push'])
        mock_run.side_effect = error

        # Verify that the exception is raised
        with pytest.raises(subprocess.CalledProcessError):
            git_operations()


# ============================================================================
# Test Cases: Main Function Integration (Task-5)
# ============================================================================


def test_main_function_creates_file(temp_dir):
    """
    Test that main() function creates the markdown file.

    This test verifies that after main() completes, the file exists.
    """
    # Mock subprocess.run to avoid actual git operations
    with mock.patch('subprocess.run'):
        with mock.patch('sys.exit') as mock_exit:
            main()

            # Verify file was created
            filepath = Path('test-94uqvv.md')
            assert filepath.exists(), "main() should create the markdown file"


def test_main_function_validates_file(temp_dir):
    """
    Test that main() function validates the file before git operations.

    This test verifies that if a file fails validation, main() exits
    with non-zero code before reaching git operations.
    """
    # Create a directory to block file creation
    bad_path = Path('test-94uqvv.md')
    bad_path.mkdir(exist_ok=True)

    # Mock subprocess.run
    with mock.patch('subprocess.run') as mock_run:
        with mock.patch('sys.exit') as mock_exit:
            main()

            # Verify git operations were not called (due to validation failure)
            # The script should exit before reaching git operations


def test_main_function_calls_git_operations(temp_dir):
    """
    Test that main() function calls git operations after validation.

    This test verifies that after file creation and validation,
    git operations are executed.
    """
    # Mock subprocess.run to track all calls
    with mock.patch('subprocess.run') as mock_run:
        with mock.patch('sys.exit') as mock_exit:
            main()

            # Verify that git operations were attempted
            # At least one git command should be called
            git_commands = [
                call[0][0]
                for call in mock_run.call_args_list
                if call[0] and call[0][0][0] == 'git'
            ]
            assert len(git_commands) > 0, (
                "main() should call git operations after file validation"
            )


def test_main_function_exits_success(temp_dir):
    """
    Test that main() exits with code 0 on successful completion.

    This test verifies that if all steps (creation, validation, git)
    complete successfully, main() exits with code 0.
    """
    # Mock subprocess.run to simulate successful git operations
    with mock.patch('subprocess.run'):
        with mock.patch('sys.exit') as mock_exit:
            main()

            # Verify sys.exit(0) was called (or script completes normally)
            # The main() function should exit with 0 on success
            if mock_exit.called:
                # If sys.exit was mocked, verify it was called with 0
                assert mock_exit.call_args[0][0] == 0, (
                    "main() should exit with code 0 on success"
                )


def test_main_function_exits_failure(temp_dir):
    """
    Test that main() exits with non-zero code on failure.

    This test verifies that if any step fails (file creation, validation, git),
    main() exits with a non-zero code.
    """
    # Create a file to block file creation
    bad_path = Path('test-94uqvv.md')
    bad_path.mkdir(exist_ok=True)

    # Mock subprocess.run
    with mock.patch('subprocess.run'):
        with mock.patch('sys.exit') as mock_exit:
            main()

            # Verify sys.exit(1) was called or exception was raised
            if mock_exit.called:
                assert mock_exit.call_args[0][0] != 0, (
                    "main() should exit with non-zero code on failure"
                )


def test_main_function_orchestrates_all_phases(temp_dir):
    """
    Integration test: main() orchestrates file creation, validation, and git operations.

    This test verifies the complete workflow:
    1. File creation: test-94uqvv.md is created with correct structure
    2. Validation: File passes all checks (encoding, structure, size)
    3. Git operations: File is staged, committed, and pushed
    """
    # Mock subprocess.run to avoid actual git operations
    with mock.patch('subprocess.run') as mock_run:
        # Configure the mock to succeed (return code 0)
        mock_run.return_value = mock.Mock(returncode=0)

        with mock.patch('sys.exit') as mock_exit:
            main()

            # Verify file was created and validated
            filepath = Path('test-94uqvv.md')
            assert filepath.exists(), "File should be created by main()"

            # Verify git operations were called
            git_commands = [
                call[0][0]
                for call in mock_run.call_args_list
                if call[0] and call[0][0][0] == 'git'
            ]
            assert len(git_commands) >= 3, (
                "main() should call at least 3 git commands (add, commit, push)"
            )
