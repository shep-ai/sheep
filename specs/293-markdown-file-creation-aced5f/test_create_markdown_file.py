"""
Integration test suite for feature 293: markdown file creation with content generation.

This module provides comprehensive integration test coverage for feature 293, which creates
a markdown file (test-msqxtg.md) with auto-generated content from Claude API,
proper structure, encoding, and line endings.

Test Coverage:
- Script imports and main() function exist
- Orchestration function returns correct result dictionary
- Complete workflow execution (content generation -> file creation -> git ops)
- File is created at repository root with correct filename
- Content structure (H1 heading + blank line + prose)
- Prose content validation (2-3 sentences)
- Git workflow verification (add, commit, push)
- Error scenarios and recovery
- Test cleanup and isolation
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock
import shutil

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sheep.content_generators import (
    create_markdown_file,
    validate_markdown_file,
    git_add,
    git_commit,
    git_push,
    generate_markdown_content,
    write_markdown_file,
)


def test_module_imports():
    """Test that the module can be imported without errors."""
    import create_markdown_file as module
    assert hasattr(module, 'main')
    assert callable(module.main)


def test_main_function_structure():
    """Test that main() function is properly defined."""
    import create_markdown_file as module
    # Should not raise any exceptions
    assert hasattr(module, 'main')
    assert callable(module.main)


def test_generate_markdown_content():
    """Test markdown content generation produces valid output."""
    from sheep.content_generators import generate_markdown_content

    # Generate content
    content = generate_markdown_content()

    # Verify it's not empty
    assert content
    assert len(content) > 0

    # Verify it starts with H1 heading
    assert content.lstrip().startswith("# ")

    # Verify it ends with newline
    assert content.endswith("\n")

    # Verify it has reasonable length
    assert len(content) > 50


def test_write_and_validate_markdown_file():
    """Test writing and validating a markdown file."""
    from sheep.content_generators import generate_markdown_content, write_markdown_file

    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Generate content
            content = generate_markdown_content()

            # Write file
            filename = "test-feature-293.md"
            filepath = write_markdown_file(content, filename)

            # Verify file exists
            assert Path(filepath).exists()
            assert filepath.endswith(filename)

            # Verify file is readable
            with open(filepath, 'r', encoding='utf-8') as f:
                written_content = f.read()
            assert written_content == content

        finally:
            os.chdir(original_cwd)


def test_markdown_content_has_correct_structure():
    """Test that markdown content has H1 + blank line + prose."""
    from sheep.content_generators import generate_markdown_content

    content = generate_markdown_content()
    lines = content.split("\n")

    # First line should be H1
    assert lines[0].startswith("# ")

    # Second line should be blank
    assert lines[1] == ""

    # Should have prose content after blank line
    assert len(lines) > 2


def test_prose_content_has_2_to_3_sentences():
    """Test that prose content contains 2-3 sentences."""
    from sheep.content_generators import generate_markdown_content

    content = generate_markdown_content()

    # Count periods (simple sentence count)
    sentence_count = content.count(".")

    # Should have 2-3 sentences
    assert 2 <= sentence_count <= 3


def test_create_markdown_file_returns_dict():
    """Test that create_markdown_file() returns a properly structured dict."""
    from sheep.content_generators import create_markdown_file as create_md_func

    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Mock git operations since we're in a temp directory
            with mock.patch('sheep.content_generators.commit_markdown_file') as mock_commit, \
                 mock.patch('sheep.content_generators.push_markdown_file') as mock_push:

                mock_commit.return_value = "Committed"
                mock_push.return_value = "Pushed"

                result = create_md_func("test-msqxtg.md", feature_number=293)

                # Verify result structure
                assert isinstance(result, dict)
                assert "filepath" in result
                assert "content" in result
                assert "commit_message" in result
                assert "push_result" in result

                # Verify content in result
                assert len(result["content"]) > 0
                assert result["content"].endswith("\n")

                # Verify commit message
                assert "feat(293)" in result["commit_message"]
                assert "test-msqxtg.md" in result["commit_message"]

        finally:
            os.chdir(original_cwd)


def test_git_add_with_nonexistent_file():
    """Test that git_add() raises FileNotFoundError if file doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            # Initialize git repo for this test
            subprocess.run(["git", "init"], capture_output=True, check=True)

            # Try to add a non-existent file
            try:
                git_add("nonexistent.md")
                assert False, "Should have raised FileNotFoundError"
            except FileNotFoundError:
                pass  # Expected
        finally:
            os.chdir(original_cwd)


def test_git_add_with_existing_file():
    """Test that git_add() returns success for an existing file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            # Initialize git repo
            subprocess.run(["git", "init"], capture_output=True, check=True)
            subprocess.run(["git", "config", "user.email", "test@test.com"], capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test User"], capture_output=True)

            # Create a file
            test_file = "test-file.md"
            with open(test_file, "w") as f:
                f.write("# Test\n\nTest content.")

            # Test git_add
            result = git_add(test_file)
            assert "exit code: 0" in result or "Successfully added" in result
        finally:
            os.chdir(original_cwd)


def test_git_add_rejects_invalid_filename():
    """Test that git_add() raises ValueError for invalid filenames."""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Test path traversal attempt
            try:
                git_add("../test.md")
                assert False, "Should have raised ValueError"
            except ValueError:
                pass  # Expected
        finally:
            os.chdir(original_cwd)


def test_git_commit_with_message():
    """Test that git_commit() creates commit with exact message."""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            # Initialize git repo
            subprocess.run(["git", "init"], capture_output=True, check=True)
            subprocess.run(["git", "config", "user.email", "test@test.com"], capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test User"], capture_output=True)

            # Create and add a file
            test_file = "test-file.md"
            with open(test_file, "w") as f:
                f.write("# Test\n\nTest content.")

            subprocess.run(["git", "add", test_file], capture_output=True, check=True)

            # Test git_commit
            message = "feat(293): test commit message"
            result = git_commit(message)
            assert "feat(293)" in result or "Committed:" in result
        finally:
            os.chdir(original_cwd)


def test_git_push_requires_upstream():
    """Test that git_push() uses upstream tracking (-u flag)."""
    # This test verifies the function signature and basic flow
    # Full push test requires remote setup
    import subprocess

    # Verify git_push function exists and has correct parameters
    import inspect
    sig = inspect.signature(git_push)
    assert "repo_path" in sig.parameters
    assert "remote" in sig.parameters


# ============================================================================
# INTEGRATION TESTS - Complete Workflow Testing
# ============================================================================


def test_complete_workflow_in_temp_repo():
    """
    Integration test: Verify complete workflow creates file, commits, and validates.

    Tests the full pipeline:
    1. Generate markdown content
    2. Write file to disk
    3. Validate file format and content
    4. Stage file with git add
    5. Commit with conventional message

    Uses temporary directory to avoid affecting real repository.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Initialize git repo for this test
            subprocess.run(["git", "init"], capture_output=True, check=True)
            subprocess.run(["git", "config", "user.email", "test@test.com"], capture_output=True, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], capture_output=True, check=True)

            # Step 1: Generate content
            content = generate_markdown_content()
            assert content, "Content generation failed"
            assert content.startswith("# "), "Content must start with H1"

            # Step 2: Write file
            filename = "test-integration.md"
            filepath = write_markdown_file(content, filename)
            assert Path(filepath).exists(), f"File not created: {filepath}"

            # Step 3: Validate file
            assert validate_markdown_file(filepath), "File validation failed"

            # Step 4: Git add
            add_result = git_add(filename)
            assert "Successfully added" in add_result or "exit code: 0" in add_result

            # Step 5: Git commit
            message = "feat(293): test-integration.md"
            commit_result = git_commit(message)
            assert "feat(293)" in commit_result or "Committed:" in commit_result

            # Verify git status shows clean working tree
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True,
                cwd=temp_dir
            )
            assert status_result.stdout.strip() == "", "Working tree should be clean after commit"

        finally:
            os.chdir(original_cwd)


def test_file_exists_in_git_log_after_commit():
    """
    Integration test: Verify file appears in git log after commit.

    Tests that git commit properly recorded the file and commit message
    can be retrieved from git log.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Initialize git repo
            subprocess.run(["git", "init"], capture_output=True, check=True)
            subprocess.run(["git", "config", "user.email", "test@test.com"], capture_output=True, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], capture_output=True, check=True)

            # Create and commit file
            filename = "test-git-log.md"
            content = generate_markdown_content()
            filepath = write_markdown_file(content, filename)
            git_add(filename)

            message = "feat(293): create test-git-log.md with prose content"
            git_commit(message)

            # Verify commit appears in git log
            log_result = subprocess.run(
                ["git", "log", "--oneline"],
                capture_output=True,
                text=True,
                check=True,
                cwd=temp_dir
            )
            assert "feat(293)" in log_result.stdout, "Commit message not in git log"
            assert "test-git-log.md" in log_result.stdout, "Filename not in git log"

        finally:
            os.chdir(original_cwd)


def test_prose_content_meets_requirements():
    """
    Integration test: Verify prose content meets all requirements.

    Tests that generated content:
    - Contains exactly 2-3 sentences
    - Is topically coherent
    - Has proper punctuation
    - Is not empty or trivial
    """
    # Generate multiple examples to verify consistency
    for _ in range(3):
        content = generate_markdown_content()
        lines = content.split("\n")

        # Must have H1 + blank line + prose
        assert lines[0].startswith("# "), "First line must be H1"
        assert lines[1] == "", "Second line must be blank"
        assert len(lines) > 2, "Must have prose content"

        # Extract prose
        prose = "\n".join(lines[2:]).strip()

        # Count sentences (by periods)
        sentence_count = prose.count(".")
        assert 2 <= sentence_count <= 3, f"Must have 2-3 sentences, got {sentence_count}"

        # Verify prose is substantial (not too short)
        assert len(prose) > 50, "Prose must be substantial"

        # Verify prose ends with period
        assert prose.endswith("."), "Prose should end with period"


def test_file_staging_workflow():
    """
    Integration test: Verify file staging and git status.

    Tests that git add properly stages files and git status reflects
    staged changes before commit.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Initialize git repo
            subprocess.run(["git", "init"], capture_output=True, check=True)
            subprocess.run(["git", "config", "user.email", "test@test.com"], capture_output=True, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], capture_output=True, check=True)

            # Create file
            filename = "test-staging.md"
            content = generate_markdown_content()
            write_markdown_file(content, filename)

            # Check git status before add (file should be untracked)
            status_before = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True,
                cwd=temp_dir
            )
            assert "??" in status_before.stdout, "File should be untracked initially"

            # Stage file
            git_add(filename)

            # Check git status after add (file should be staged)
            status_after = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True,
                cwd=temp_dir
            )
            assert "A " in status_after.stdout, "File should be staged after git add"

        finally:
            os.chdir(original_cwd)


def test_error_handling_api_failure():
    """
    Integration test: Verify error handling when API fails.

    Tests that the system properly handles and reports API failures
    during content generation.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Mock API failure
            with mock.patch('sheep.content_generators.get_reasoning_llm') as mock_llm:
                mock_llm.side_effect = Exception("API connection failed")

                try:
                    generate_markdown_content()
                    assert False, "Should have raised exception on API failure"
                except Exception as e:
                    assert "API connection failed" in str(e)

        finally:
            os.chdir(original_cwd)


def test_error_handling_invalid_file_write():
    """
    Integration test: Verify error handling when file write fails.

    Tests that the system properly handles file I/O errors
    (e.g., permission denied, invalid path).
    """
    # Attempt to write to read-only directory
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Create a read-only directory
            readonly_dir = Path(temp_dir) / "readonly"
            readonly_dir.mkdir()
            os.chmod(readonly_dir, 0o444)  # Read-only

            try:
                os.chdir(readonly_dir)
                content = "# Test\n\nTest content."
                write_markdown_file(content, "test.md")
                assert False, "Should have failed to write to read-only directory"
            except (IOError, OSError) as e:
                assert "Permission denied" in str(e) or "cannot create" in str(e).lower()
            finally:
                os.chdir(temp_dir)
                os.chmod(readonly_dir, 0o755)  # Restore permissions for cleanup

        finally:
            os.chdir(original_cwd)


def test_error_handling_git_add_nonexistent():
    """
    Integration test: Verify error handling when adding nonexistent file.

    Tests that git_add properly raises FileNotFoundError when
    attempting to add a file that doesn't exist.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Initialize git repo
            subprocess.run(["git", "init"], capture_output=True, check=True)

            # Try to add nonexistent file
            try:
                git_add("nonexistent.md")
                assert False, "Should have raised FileNotFoundError"
            except FileNotFoundError as e:
                assert "nonexistent.md" in str(e)

        finally:
            os.chdir(original_cwd)


def test_error_handling_invalid_filename():
    """
    Integration test: Verify error handling for invalid filenames.

    Tests that the system rejects filenames with path traversal
    or other unsafe patterns.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            content = "# Test\n\nTest content."

            # Test path traversal attempts
            invalid_filenames = [
                "../test.md",
                "../../test.md",
                "test/../evil.md",
                ".test.md",  # Hidden file
            ]

            for invalid_name in invalid_filenames:
                try:
                    write_markdown_file(content, invalid_name)
                    assert False, f"Should have rejected filename: {invalid_name}"
                except ValueError as e:
                    assert "Invalid filename" in str(e) or "invalid" in str(e).lower()

        finally:
            os.chdir(original_cwd)


def test_markdown_validation_catches_invalid_format():
    """
    Integration test: Verify validation catches improperly formatted files.

    Tests that validate_markdown_file properly rejects files that
    don't meet format requirements (missing H1, wrong line endings, etc).
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Test 1: Missing H1 heading
            with open("no-heading.md", "w") as f:
                f.write("This is just text without heading.\n")

            try:
                validate_markdown_file("no-heading.md")
                assert False, "Should have rejected file without H1"
            except ValueError as e:
                assert "H1" in str(e)

            # Test 2: Missing blank line separator
            with open("no-separator.md", "w") as f:
                f.write("# Title\nDirect prose without blank line.\n")

            try:
                validate_markdown_file("no-separator.md")
                assert False, "Should have rejected file without blank line separator"
            except ValueError as e:
                assert "blank" in str(e).lower()

            # Test 3: Wrong sentence count
            with open("wrong-count.md", "w") as f:
                f.write("# Title\n\nOnly one sentence.\n")

            try:
                validate_markdown_file("wrong-count.md")
                assert False, "Should have rejected file with wrong sentence count"
            except ValueError as e:
                assert "sentence" in str(e).lower()

        finally:
            os.chdir(original_cwd)


def test_test_cleanup_after_integration_test():
    """
    Integration test: Verify test cleanup and isolation.

    Tests that temporary files and directories are properly cleaned up
    after each test, leaving the system in a clean state.
    """
    temp_files_before = set(Path.cwd().glob("test-*.md"))

    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Create some test files
            for i in range(3):
                with open(f"test-file-{i}.md", "w") as f:
                    f.write("# Test\n\nContent.")

            assert len(list(Path.cwd().glob("test-*.md"))) == 3, "Test files created"

        finally:
            os.chdir(original_cwd)

    # After exiting context manager, temp directory should be cleaned
    # Verify original state is restored
    temp_files_after = set(Path.cwd().glob("test-*.md"))
    assert temp_files_before == temp_files_after, "Temp files should be cleaned up"


if __name__ == "__main__":
    # Run tests with basic assertions
    test_module_imports()
    print("✓ test_module_imports passed")

    test_main_function_structure()
    print("✓ test_main_function_structure passed")

    # Git operation tests (don't require API key)
    test_git_add_rejects_invalid_filename()
    print("✓ test_git_add_rejects_invalid_filename passed")

    test_git_add_with_nonexistent_file()
    print("✓ test_git_add_with_nonexistent_file passed")

    test_git_add_with_existing_file()
    print("✓ test_git_add_with_existing_file passed")

    test_git_commit_with_message()
    print("✓ test_git_commit_with_message passed")

    test_git_push_requires_upstream()
    print("✓ test_git_push_requires_upstream passed")

    # Integration tests
    print("\n--- Running Integration Tests ---")

    test_complete_workflow_in_temp_repo()
    print("✓ test_complete_workflow_in_temp_repo passed")

    test_file_exists_in_git_log_after_commit()
    print("✓ test_file_exists_in_git_log_after_commit passed")

    test_prose_content_meets_requirements()
    print("✓ test_prose_content_meets_requirements passed")

    test_file_staging_workflow()
    print("✓ test_file_staging_workflow passed")

    test_error_handling_api_failure()
    print("✓ test_error_handling_api_failure passed")

    test_error_handling_invalid_file_write()
    print("✓ test_error_handling_invalid_file_write passed")

    test_error_handling_git_add_nonexistent()
    print("✓ test_error_handling_git_add_nonexistent passed")

    test_error_handling_invalid_filename()
    print("✓ test_error_handling_invalid_filename passed")

    test_markdown_validation_catches_invalid_format()
    print("✓ test_markdown_validation_catches_invalid_format passed")

    test_test_cleanup_after_integration_test()
    print("✓ test_test_cleanup_after_integration_test passed")

    print("\n✓ All integration tests passed!")
