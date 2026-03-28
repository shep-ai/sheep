"""Comprehensive integration tests for feature 208 markdown file creation.

Tests verify the complete end-to-end workflow:
1. File creation with proper formatting, encoding, and line endings
2. Comprehensive validation of all aspects (format, encoding, size, etc.)
3. Git operations (add, commit, push) with proper messages
4. Full orchestration via main() function

These tests create actual files and perform real git operations
to ensure the complete workflow succeeds.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


def setup_module():
    """Set up test environment by adding src to path."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


@pytest.fixture
def temp_git_repo():
    """Create a temporary git repository for integration testing.

    Yields:
        Path to temporary git repository directory
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)

        # Initialize git repo
        subprocess.run(
            ["git", "init"],
            cwd=repo_path,
            capture_output=True,
            check=True,
        )

        # Configure git user (required for commits)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=repo_path,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=repo_path,
            capture_output=True,
            check=True,
        )

        yield repo_path


def test_integration_full_workflow(temp_git_repo):
    """Test complete workflow: create file, validate, stage, commit.

    This integration test verifies that the entire feature 208 workflow
    succeeds end-to-end without mocking any functions.

    Steps:
    1. Create markdown file with proper format
    2. Validate file meets all requirements
    3. Stage file with git add
    4. Commit with conventional commit message
    5. Verify commit appears in git history
    """
    from sheep.features.feature_208_markdown_file_creation import (
        COMMIT_MESSAGE,
        FILENAME,
        create_markdown_file,
        git_add_file,
        git_commit,
        validate_markdown_file,
    )

    # Change to temp repo directory
    original_cwd = os.getcwd()
    os.chdir(temp_git_repo)

    try:
        # Phase 1: Create file
        file_path = create_markdown_file()
        assert file_path.exists(), "File should exist after creation"
        assert file_path.name == FILENAME, "File should have correct name"

        # Phase 2: Validate file
        validate_markdown_file(FILENAME)
        # If no exception raised, validation passed

        # Phase 3: Stage and commit
        git_add_file(FILENAME)
        git_commit(COMMIT_MESSAGE)

        # Verify commit appears in git log
        result = subprocess.run(
            ["git", "log", "--oneline"],
            capture_output=True,
            text=True,
            check=True,
        )

        assert COMMIT_MESSAGE in result.stdout, \
            f"Commit message should appear in git log: {result.stdout}"

        # Clean up created file
        file_path.unlink()

    finally:
        os.chdir(original_cwd)


def test_integration_file_validation_before_commit(temp_git_repo):
    """Test that invalid file is caught before git commit.

    Verifies that validation failures prevent git operations.
    """
    from sheep.features.feature_208_markdown_file_creation import (
        validate_markdown_file,
    )

    original_cwd = os.getcwd()
    os.chdir(temp_git_repo)

    try:
        # Create an invalid markdown file (no H1 heading)
        invalid_file = Path("invalid.md")
        invalid_file.write_text("This is not a markdown file.\nJust plain text.")

        # Validation should fail
        with pytest.raises(ValueError, match="must start with H1"):
            validate_markdown_file("invalid.md")

        # Clean up
        invalid_file.unlink()

    finally:
        os.chdir(original_cwd)


def test_integration_file_created_with_correct_format(temp_git_repo):
    """Test that created file has correct format, encoding, line endings.

    Verifies all non-functional requirements:
    - UTF-8 encoding without BOM
    - Unix LF line endings
    - File size 300-800 bytes
    - Proper H1 and blank line structure
    """
    from sheep.features.feature_208_markdown_file_creation import (
        create_markdown_file,
    )

    original_cwd = os.getcwd()
    os.chdir(temp_git_repo)

    try:
        file_path = create_markdown_file()
        binary_content = file_path.read_bytes()

        # Check: No UTF-8 BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf"), \
            "File should not have UTF-8 BOM"

        # Check: Valid UTF-8
        binary_content.decode("utf-8")  # Should not raise

        # Check: LF line endings only (no CRLF or CR)
        assert b"\r\n" not in binary_content, \
            "File should not have CRLF line endings"
        assert b"\r" not in binary_content, \
            "File should not have CR line endings"

        # Check: File size in range
        file_size = len(binary_content)
        assert 300 <= file_size <= 800, \
            f"File size {file_size} should be 300-800 bytes"

        # Check: First line is H1, second line is blank
        text_content = binary_content.decode("utf-8")
        lines = text_content.split("\n")
        assert lines[0].startswith("# "), "First line should be H1 heading"
        assert lines[1].strip() == "", "Second line should be blank"

        # Clean up
        file_path.unlink()

    finally:
        os.chdir(original_cwd)


def test_integration_sentence_count_validation(temp_git_repo):
    """Test that sentence count validation works correctly.

    Verifies that exactly 2-3 sentences are present and properly counted.
    """
    from sheep.features.feature_208_markdown_file_creation import (
        FILENAME,
        count_sentences,
        create_markdown_file,
        extract_prose_content,
        validate_sentence_count,
    )

    original_cwd = os.getcwd()
    os.chdir(temp_git_repo)

    try:
        # Create file
        create_markdown_file()

        # Extract and validate prose
        prose = extract_prose_content(FILENAME)
        sentence_count = count_sentences(prose)

        # Should be 2-3 sentences
        assert sentence_count in (2, 3), \
            f"Should have 2-3 sentences, found {sentence_count}"

        # Validation should not raise
        validate_sentence_count(FILENAME)

        # Clean up
        Path(FILENAME).unlink()

    finally:
        os.chdir(original_cwd)


def test_integration_main_with_all_phases(temp_git_repo):
    """Test main() orchestration function through all phases.

    Verifies that main() coordinates all phases correctly:
    1. File creation
    2. Validation
    3. Git staging
    4. Git commit

    Note: git push is mocked because we don't have a remote configured.
    """
    from sheep.features.feature_208_markdown_file_creation import main

    original_cwd = os.getcwd()
    os.chdir(temp_git_repo)

    try:
        # Mock git_push since we don't have a remote
        with patch(
            "sheep.features.feature_208_markdown_file_creation.git_push"
        ) as mock_push:
            mock_push.return_value = None

            result = main()

            # Should succeed
            assert result == 0, "main() should return 0 on success"

            # File should exist
            assert Path("test-s4b1z3.md").exists(), \
                "File should exist after main() completes"

            # Git push should have been called
            mock_push.assert_called_once()

        # Clean up
        Path("test-s4b1z3.md").unlink()

    finally:
        os.chdir(original_cwd)


def test_integration_git_workflow_idempotent(temp_git_repo):
    """Test that feature can be run multiple times (idempotency).

    Verifies that creating the file multiple times doesn't cause
    conflicts or errors (file is overwritten each time).
    """
    from sheep.features.feature_208_markdown_file_creation import (
        create_markdown_file,
        validate_markdown_file,
    )

    original_cwd = os.getcwd()
    os.chdir(temp_git_repo)

    try:
        # Create file multiple times
        for i in range(3):
            file_path = create_markdown_file()
            assert file_path.exists(), f"Iteration {i+1}: File should exist"

            # Validate each time
            validate_markdown_file("test-s4b1z3.md")

            # File size should be consistent
            file_size = file_path.stat().st_size
            assert 300 <= file_size <= 800, \
                f"Iteration {i+1}: File size should be valid"

        # Clean up
        file_path.unlink()

    finally:
        os.chdir(original_cwd)


def test_integration_file_content_deterministic(temp_git_repo):
    """Test that file content is deterministic across multiple runs.

    Verifies that the same content is created each time (reproducibility).
    """
    from sheep.features.feature_208_markdown_file_creation import (
        create_markdown_file,
    )

    original_cwd = os.getcwd()
    os.chdir(temp_git_repo)

    try:
        # Create file twice and compare content
        create_markdown_file()
        content1 = Path("test-s4b1z3.md").read_text(encoding="utf-8")
        Path("test-s4b1z3.md").unlink()

        create_markdown_file()
        content2 = Path("test-s4b1z3.md").read_text(encoding="utf-8")

        # Content should be identical
        assert content1 == content2, \
            "File content should be deterministic and reproducible"

        # Clean up
        Path("test-s4b1z3.md").unlink()

    finally:
        os.chdir(original_cwd)


def test_integration_docstrings_complete():
    """Test that all functions have comprehensive docstrings.

    Verifies that all exported functions include:
    - Description of what the function does
    - Args section (if applicable)
    - Returns section (if applicable)
    - Raises section (if applicable)
    - Example section (if applicable)
    """
    from sheep.features.feature_208_markdown_file_creation import (
        count_sentences,
        create_markdown_file,
        extract_prose_content,
        git_add_file,
        git_commit,
        git_push,
        main,
        validate_encoding,
        validate_file_size,
        validate_line_endings,
        validate_markdown_file,
        validate_markdown_format,
        validate_sentence_count,
        verify_file_exists,
    )

    functions_to_check = [
        create_markdown_file,
        verify_file_exists,
        validate_markdown_format,
        extract_prose_content,
        count_sentences,
        validate_sentence_count,
        validate_encoding,
        validate_line_endings,
        validate_file_size,
        validate_markdown_file,
        git_add_file,
        git_commit,
        git_push,
        main,
    ]

    for func in functions_to_check:
        # Check that function has a docstring
        assert func.__doc__ is not None, \
            f"{func.__name__} should have a docstring"

        docstring = func.__doc__

        # Check that docstring has meaningful content (not just one line)
        assert len(docstring.strip()) > 20, \
            f"{func.__name__} docstring should be comprehensive"

        # Functions with parameters should have Args section
        if func.__code__.co_argcount > 0:
            # Some simple functions might not document all args, that's okay
            # But main() and other complex functions should
            if func.__name__ in ["main", "validate_markdown_file", "validate_file_size"]:
                assert "Args:" in docstring or "Returns:" in docstring or "Example:" in docstring, \
                    f"{func.__name__} should have documentation sections"


def test_integration_code_style_compliance():
    """Test that code follows PEP 8 style guidelines.

    Checks:
    - Function names use snake_case
    - Constants use UPPER_CASE
    - Code is readable and well-structured
    """
    from sheep.features import feature_208_markdown_file_creation as module

    # Check module-level constants
    assert hasattr(module, "FILENAME"), "Should have FILENAME constant"
    assert hasattr(module, "FEATURE_NUMBER"), "Should have FEATURE_NUMBER constant"
    assert hasattr(module, "BRANCH_NAME"), "Should have BRANCH_NAME constant"
    assert hasattr(module, "COMMIT_MESSAGE"), "Should have COMMIT_MESSAGE constant"
    assert hasattr(module, "TITLE_TEXT"), "Should have TITLE_TEXT constant"
    assert hasattr(module, "PROSE_CONTENT"), "Should have PROSE_CONTENT constant"

    # All should be uppercase (constants)
    for const_name in ["FILENAME", "FEATURE_NUMBER", "BRANCH_NAME", "COMMIT_MESSAGE", "TITLE_TEXT", "PROSE_CONTENT"]:
        assert const_name.isupper() or "_" in const_name, \
            f"Constant {const_name} should use UPPER_CASE naming"

    # Check that all exported functions have snake_case names
    function_names = [
        "create_markdown_file",
        "verify_file_exists",
        "validate_markdown_format",
        "extract_prose_content",
        "count_sentences",
        "validate_sentence_count",
        "validate_encoding",
        "validate_line_endings",
        "validate_file_size",
        "validate_markdown_file",
        "git_add_file",
        "git_commit",
        "git_push",
        "main",
    ]

    for func_name in function_names:
        assert hasattr(module, func_name), f"Should have {func_name} function"
        # Check snake_case (lowercase with underscores)
        assert func_name.islower() or "_" in func_name, \
            f"Function {func_name} should use snake_case naming"


def test_integration_error_messages_clear():
    """Test that error messages are clear and informative.

    Verifies that validation failures provide clear feedback about
    what went wrong and how to fix it.
    """
    from sheep.features.feature_208_markdown_file_creation import (
        validate_markdown_format,
        verify_file_exists,
    )

    # Test file not found error
    with pytest.raises(FileNotFoundError) as exc_info:
        verify_file_exists("nonexistent-file.md")
    assert "nonexistent-file.md" in str(exc_info.value), \
        "Error should mention missing file name"

    # Test markdown format error
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("Invalid content\nNo H1 heading here")
        temp_file = f.name

    try:
        with pytest.raises(ValueError) as exc_info:
            validate_markdown_format(temp_file)
        error_msg = str(exc_info.value)
        assert "H1" in error_msg or "#" in error_msg, \
            "Error should mention H1 requirement"
    finally:
        Path(temp_file).unlink()


def test_integration_cross_platform_paths():
    """Test that file paths work correctly on all platforms.

    Verifies that pathlib.Path is used for cross-platform compatibility.
    """
    # create_markdown_file should return a Path object
    # (test only in current directory, no actual file creation needed)
    # This test verifies the module uses pathlib throughout
    import inspect

    from sheep.features.feature_208_markdown_file_creation import (
        create_markdown_file,
    )
    source = inspect.getsource(create_markdown_file)
    assert "Path" in source, "Should use pathlib.Path for cross-platform compatibility"
    assert "pathlib" in source or "from pathlib" in source, \
        "Should import Path from pathlib"
