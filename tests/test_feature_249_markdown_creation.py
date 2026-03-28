"""Tests for feature 249: markdown file creation with Claude API content generation.

Tests verify that:
1. Feature module imports without errors
2. Feature metadata is correctly set
3. Function signature and return type are correct
4. Function can be called (basic integration test)
"""

import sys
from pathlib import Path

# Add src to path to enable imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def test_feature_249_module_imports():
    """Test that feature 249 module imports without errors."""
    from sheep.features.feature_249_markdown_file_creation import (
        FEATURE_NAME,
        FEATURE_NUMBER,
        MARKDOWN_FILENAME,
        _logger,
        create_feature_249_markdown_file,
    )

    assert FEATURE_NUMBER == 249
    assert FEATURE_NAME == "markdown-file-creation-893e4b"
    assert MARKDOWN_FILENAME == "test-ey0s31.md"
    assert create_feature_249_markdown_file is not None
    assert _logger is not None


def test_feature_249_function_signature():
    """Test that create_feature_249_markdown_file has correct signature."""
    import inspect

    from sheep.features.feature_249_markdown_file_creation import (
        create_feature_249_markdown_file,
    )

    sig = inspect.signature(create_feature_249_markdown_file)

    # Check parameters
    params = list(sig.parameters.keys())
    assert "repo_path" in params

    # Check default value for repo_path
    assert sig.parameters["repo_path"].default is None


def test_feature_249_return_type():
    """Test that create_feature_249_markdown_file returns a dictionary with expected keys."""
    import os
    import tempfile
    from unittest import mock

    from sheep.features.feature_249_markdown_file_creation import (
        create_feature_249_markdown_file,
    )

    # Sample markdown content for testing
    sample_markdown = "# Test Title\n\nThis is the first sentence. This is the second sentence. This is the third sentence.\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            # Mock the content generation and git operations
            with mock.patch("sheep.features.feature_249_markdown_file_creation.generate_markdown_content") as mock_gen, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.write_markdown_file") as mock_write, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.validate_markdown_file") as mock_validate, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.commit_markdown_file") as mock_commit, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.push_markdown_file") as mock_push:

                # Configure mocks
                mock_gen.return_value = sample_markdown
                mock_write.return_value = "test-ey0s31.md"
                mock_validate.return_value = True
                mock_commit.return_value = {"commit": "abc123"}
                mock_push.return_value = {"pushed": True}

                result = create_feature_249_markdown_file(tmpdir)

                # Verify return type and keys
                assert isinstance(result, dict)
                assert "filepath" in result
                assert "content" in result
                assert "commit_message" in result
                assert "push_result" in result

                # Verify values
                assert result["filepath"] == "test-ey0s31.md"
                assert result["content"] == sample_markdown
                assert "feat(249):" in result["commit_message"]
                assert "test-ey0s31.md" in result["commit_message"]
        finally:
            os.chdir(original_cwd)


def test_feature_249_commit_message_format():
    """Test that commit message follows conventional format."""
    import os
    import tempfile
    from unittest import mock

    from sheep.features.feature_249_markdown_file_creation import (
        FEATURE_NUMBER,
        MARKDOWN_FILENAME,
        create_feature_249_markdown_file,
    )

    sample_markdown = "# Test\n\nOne. Two. Three.\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            with mock.patch("sheep.features.feature_249_markdown_file_creation.generate_markdown_content") as mock_gen, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.write_markdown_file") as mock_write, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.validate_markdown_file") as mock_validate, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.commit_markdown_file") as mock_commit, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.push_markdown_file") as mock_push:

                mock_gen.return_value = sample_markdown
                mock_write.return_value = MARKDOWN_FILENAME
                mock_validate.return_value = True
                mock_commit.return_value = {"commit": "abc123"}
                mock_push.return_value = {"pushed": True}

                result = create_feature_249_markdown_file(tmpdir)

                # Verify conventional commit format
                expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
                assert result["commit_message"] == expected_message
        finally:
            os.chdir(original_cwd)


# Phase 2: Content Generation & File I/O Tests


def test_task_3_generate_markdown_content_called():
    """Test that Task 3: generate_markdown_content is called during feature execution."""
    import os
    import tempfile
    from unittest import mock

    from sheep.features.feature_249_markdown_file_creation import (
        create_feature_249_markdown_file,
    )

    sample_markdown = "# Test Title\n\nThis is the first sentence. This is the second sentence. This is the third sentence.\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            with mock.patch("sheep.features.feature_249_markdown_file_creation.generate_markdown_content") as mock_gen, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.write_markdown_file") as mock_write, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.validate_markdown_file") as mock_validate, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.commit_markdown_file") as mock_commit, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.push_markdown_file") as mock_push:

                mock_gen.return_value = sample_markdown
                mock_write.return_value = "test-ey0s31.md"
                mock_validate.return_value = True
                mock_commit.return_value = {"commit": "abc123"}
                mock_push.return_value = {"pushed": True}

                result = create_feature_249_markdown_file(tmpdir)

                # Verify generate_markdown_content was called
                mock_gen.assert_called_once()
                assert result["content"] == sample_markdown
        finally:
            os.chdir(original_cwd)


def test_task_3_generated_content_has_h1_heading():
    """Test that generated content starts with H1 heading."""
    import os
    import tempfile
    from unittest import mock

    from sheep.features.feature_249_markdown_file_creation import (
        create_feature_249_markdown_file,
    )

    sample_markdown = "# Sample Topic\n\nFirst sentence here. Second sentence here. Third sentence here.\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            with mock.patch("sheep.features.feature_249_markdown_file_creation.generate_markdown_content") as mock_gen, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.write_markdown_file") as mock_write, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.validate_markdown_file") as mock_validate, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.commit_markdown_file") as mock_commit, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.push_markdown_file") as mock_push:

                mock_gen.return_value = sample_markdown
                mock_write.return_value = "test-ey0s31.md"
                mock_validate.return_value = True
                mock_commit.return_value = {"commit": "abc123"}
                mock_push.return_value = {"pushed": True}

                result = create_feature_249_markdown_file(tmpdir)

                # Verify content has H1 heading on first line
                assert result["content"].startswith("# ")
                lines = result["content"].split("\n")
                assert lines[0].startswith("# ")
        finally:
            os.chdir(original_cwd)


def test_task_4_write_markdown_file_to_disk():
    """Test that Task 4: file is written to disk with proper function call."""
    import os
    import tempfile
    from unittest import mock

    from sheep.features.feature_249_markdown_file_creation import (
        create_feature_249_markdown_file,
    )

    sample_markdown = "# Title\n\nSentence one. Sentence two. Sentence three.\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            with mock.patch("sheep.features.feature_249_markdown_file_creation.generate_markdown_content") as mock_gen, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.write_markdown_file") as mock_write, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.validate_markdown_file") as mock_validate, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.commit_markdown_file") as mock_commit, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.push_markdown_file") as mock_push:

                mock_gen.return_value = sample_markdown
                mock_write.return_value = "test-ey0s31.md"
                mock_validate.return_value = True
                mock_commit.return_value = {"commit": "abc123"}
                mock_push.return_value = {"pushed": True}

                result = create_feature_249_markdown_file(tmpdir)

                # Verify write_markdown_file was called with correct arguments
                mock_write.assert_called_once_with(sample_markdown, "test-ey0s31.md")
                assert result["filepath"] == "test-ey0s31.md"
        finally:
            os.chdir(original_cwd)


def test_task_5_validate_markdown_file_called():
    """Test that Task 5: validate_markdown_file is called during feature execution."""
    import os
    import tempfile
    from unittest import mock

    from sheep.features.feature_249_markdown_file_creation import (
        create_feature_249_markdown_file,
    )

    sample_markdown = "# Test\n\nOne. Two. Three.\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            with mock.patch("sheep.features.feature_249_markdown_file_creation.generate_markdown_content") as mock_gen, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.write_markdown_file") as mock_write, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.validate_markdown_file") as mock_validate, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.commit_markdown_file") as mock_commit, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.push_markdown_file") as mock_push:

                mock_gen.return_value = sample_markdown
                mock_write.return_value = "test-ey0s31.md"
                mock_validate.return_value = True
                mock_commit.return_value = {"commit": "abc123"}
                mock_push.return_value = {"pushed": True}

                result = create_feature_249_markdown_file(tmpdir)

                # Verify validate_markdown_file was called
                mock_validate.assert_called_once_with("test-ey0s31.md")
        finally:
            os.chdir(original_cwd)


def test_task_5_validation_failure_prevents_commit():
    """Test that if validation fails, git operations are not attempted."""
    import os
    import tempfile
    from unittest import mock

    from sheep.features.feature_249_markdown_file_creation import (
        create_feature_249_markdown_file,
    )

    sample_markdown = "# Test\n\nOne. Two. Three.\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            with mock.patch("sheep.features.feature_249_markdown_file_creation.generate_markdown_content") as mock_gen, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.write_markdown_file") as mock_write, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.validate_markdown_file") as mock_validate, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.commit_markdown_file") as mock_commit, \
                 mock.patch("sheep.features.feature_249_markdown_file_creation.push_markdown_file") as mock_push:

                mock_gen.return_value = sample_markdown
                mock_write.return_value = "test-ey0s31.md"
                # Simulate validation failure
                mock_validate.side_effect = ValueError("File has CRLF line endings")
                mock_commit.return_value = {"commit": "abc123"}
                mock_push.return_value = {"pushed": True}

                # Expect exception when validation fails
                try:
                    result = create_feature_249_markdown_file(tmpdir)
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    # Validation error should be propagated
                    assert "CRLF line endings" in str(e)
                    # commit and push should not be called
                    mock_commit.assert_not_called()
                    mock_push.assert_not_called()
        finally:
            os.chdir(original_cwd)


# Phase 3: Git Integration & End-to-End Tests


def test_task_6_git_add_stages_file():
    """Test that Task 6: 'git add test-ey0s31.md' stages the file."""
    import os
    import subprocess
    import tempfile
    from pathlib import Path
    from unittest import mock

    from sheep.features.feature_249_markdown_file_creation import (
        MARKDOWN_FILENAME,
        create_feature_249_markdown_file,
    )

    sample_markdown = "# Test\n\nOne. Two. Three.\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            # Initialize git repo
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                check=True,
                capture_output=True,
            )

            # Mock content generation to avoid LLM calls
            with mock.patch(
                "sheep.features.feature_249_markdown_file_creation.generate_markdown_content"
            ) as mock_gen:
                mock_gen.return_value = sample_markdown

                # Call feature function
                result = create_feature_249_markdown_file(tmpdir)

                # Verify file is in git index (using git ls-files which shows tracked files)
                git_ls_output = subprocess.run(
                    ["git", "ls-files"],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout

                # File should be in the git index after staging and commit
                assert MARKDOWN_FILENAME in git_ls_output, f"{MARKDOWN_FILENAME} should be tracked in git"

        finally:
            os.chdir(original_cwd)


def test_task_6_git_commit_message_format():
    """Test that Task 6: commit is created with exact message format."""
    import os
    import subprocess
    import tempfile
    from unittest import mock

    from sheep.features.feature_249_markdown_file_creation import (
        FEATURE_NUMBER,
        MARKDOWN_FILENAME,
        create_feature_249_markdown_file,
    )

    sample_markdown = "# Test\n\nOne. Two. Three.\n"
    expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            # Initialize git repo
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                check=True,
                capture_output=True,
            )

            # Mock content generation
            with mock.patch(
                "sheep.features.feature_249_markdown_file_creation.generate_markdown_content"
            ) as mock_gen:
                mock_gen.return_value = sample_markdown

                # Call feature function
                result = create_feature_249_markdown_file(tmpdir)

                # Verify commit message
                git_log_output = subprocess.run(
                    ["git", "log", "--oneline", "-1"],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout

                # Log should contain the exact commit message
                assert expected_message in git_log_output

        finally:
            os.chdir(original_cwd)


def test_task_7_git_push_upstream_tracking():
    """Test that Task 7: 'git push -u origin' is executed with upstream tracking."""
    import os
    import subprocess
    import tempfile
    from unittest import mock

    from sheep.features.feature_249_markdown_file_creation import (
        create_feature_249_markdown_file,
    )

    sample_markdown = "# Test\n\nOne. Two. Three.\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            # Initialize local repo
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                check=True,
                capture_output=True,
            )

            # Create a bare repo to act as remote
            with tempfile.TemporaryDirectory() as bare_repo_dir:
                subprocess.run(
                    ["git", "init", "--bare"],
                    cwd=bare_repo_dir,
                    check=True,
                    capture_output=True,
                )

                # Add remote to local repo
                subprocess.run(
                    ["git", "remote", "add", "origin", bare_repo_dir],
                    check=True,
                    capture_output=True,
                )

                # Mock content generation
                with mock.patch(
                    "sheep.features.feature_249_markdown_file_creation.generate_markdown_content"
                ) as mock_gen:
                    mock_gen.return_value = sample_markdown

                    # Call feature function
                    result = create_feature_249_markdown_file(tmpdir)

                    # Verify that current branch is tracked upstream
                    git_branch_output = subprocess.run(
                        ["git", "branch", "-vv"],
                        check=True,
                        capture_output=True,
                        text=True,
                    ).stdout

                    # Current branch should show upstream tracking
                    assert "origin/" in git_branch_output

        finally:
            os.chdir(original_cwd)


def test_task_8_end_to_end_file_creation_and_git_workflow():
    """Test complete workflow: create file -> validate -> stage -> commit -> push."""
    import os
    import subprocess
    import tempfile
    from pathlib import Path
    from unittest import mock

    from sheep.content_generators import validate_markdown_file
    from sheep.features.feature_249_markdown_file_creation import (
        FEATURE_NUMBER,
        MARKDOWN_FILENAME,
        create_feature_249_markdown_file,
    )

    sample_markdown = "# Comprehensive Test\n\nThis is the first sentence. This is the second sentence. This is the third sentence.\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            # Initialize local repo
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                check=True,
                capture_output=True,
            )

            # Create a bare repo to act as remote
            with tempfile.TemporaryDirectory() as bare_repo_dir:
                subprocess.run(
                    ["git", "init", "--bare"],
                    cwd=bare_repo_dir,
                    check=True,
                    capture_output=True,
                )

                # Add remote to local repo
                subprocess.run(
                    ["git", "remote", "add", "origin", bare_repo_dir],
                    check=True,
                    capture_output=True,
                )

                # Mock content generation
                with mock.patch(
                    "sheep.features.feature_249_markdown_file_creation.generate_markdown_content"
                ) as mock_gen:
                    mock_gen.return_value = sample_markdown

                    # Execute feature
                    result = create_feature_249_markdown_file(tmpdir)

                    # SUCCESS CRITERIA 1: File exists at correct location
                    filepath = Path(tmpdir) / MARKDOWN_FILENAME
                    assert filepath.exists(), f"File {MARKDOWN_FILENAME} should exist"

                    # SUCCESS CRITERIA 2: File is in git index (staged)
                    git_ls_output = subprocess.run(
                        ["git", "ls-files"],
                        check=True,
                        capture_output=True,
                        text=True,
                    ).stdout

                    assert (
                        MARKDOWN_FILENAME in git_ls_output
                    ), f"{MARKDOWN_FILENAME} should be in git index"

                    # SUCCESS CRITERIA 3: File has H1 heading and 2-3 sentences
                    content = filepath.read_text(encoding="utf-8")
                    assert content.startswith("# "), "Content should start with H1 heading"
                    assert content.count(".") >= 2 and content.count(".") <= 3, "Content should have 2-3 sentences"

                    # SUCCESS CRITERIA 4: File is UTF-8 without BOM
                    binary_content = filepath.read_bytes()
                    assert not binary_content.startswith(
                        b"\xef\xbb\xbf"
                    ), "File should not have UTF-8 BOM"

                    # SUCCESS CRITERIA 5: File uses LF line endings
                    assert b"\r\n" not in binary_content, "File should use LF, not CRLF"

                    # SUCCESS CRITERIA 6: File passes comprehensive validation
                    validate_markdown_file(str(filepath))

                    # SUCCESS CRITERIA 7: Commit message is correct
                    git_log_output = subprocess.run(
                        ["git", "log", "--oneline", "-1"],
                        check=True,
                        capture_output=True,
                        text=True,
                    ).stdout

                    expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
                    assert expected_message in git_log_output, f"Commit message should be: {expected_message}"

                    # SUCCESS CRITERIA 8: Current branch has upstream tracking
                    git_branch_output = subprocess.run(
                        ["git", "branch", "-vv"],
                        check=True,
                        capture_output=True,
                        text=True,
                    ).stdout

                    assert (
                        "origin/" in git_branch_output
                    ), "Branch should have upstream tracking after push"

                    # SUCCESS CRITERIA 9: Feature return value is complete
                    assert isinstance(result, dict)
                    assert "filepath" in result
                    assert "content" in result
                    assert "commit_message" in result
                    assert "push_result" in result
                    assert result["commit_message"] == expected_message

        finally:
            os.chdir(original_cwd)


def test_task_8_file_properties_encoding_and_line_endings():
    """Test that created file has correct encoding (UTF-8 no BOM) and line endings (LF)."""
    import os
    import subprocess
    import tempfile
    from pathlib import Path
    from unittest import mock

    from sheep.features.feature_249_markdown_file_creation import (
        MARKDOWN_FILENAME,
        create_feature_249_markdown_file,
    )

    sample_markdown = "# Title\n\nSentence one. Sentence two. Sentence three.\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            # Initialize git repo (minimal)
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                check=True,
                capture_output=True,
            )

            # Mock content generation
            with mock.patch(
                "sheep.features.feature_249_markdown_file_creation.generate_markdown_content"
            ) as mock_gen:
                mock_gen.return_value = sample_markdown

                # Execute feature
                result = create_feature_249_markdown_file(tmpdir)

                # Get file and check encoding/line endings
                filepath = Path(tmpdir) / MARKDOWN_FILENAME
                binary_content = filepath.read_bytes()

                # Check 1: No UTF-8 BOM
                assert not binary_content.startswith(
                    b"\xef\xbb\xbf"
                ), "File must not have UTF-8 BOM"

                # Check 2: No CRLF (must be LF)
                assert b"\r\n" not in binary_content, "File must use LF, not CRLF"

                # Check 3: Valid UTF-8
                try:
                    text_content = binary_content.decode("utf-8")
                except UnicodeDecodeError:
                    assert False, "File must be valid UTF-8"

                # Check 4: Ends with newline
                assert text_content.endswith("\n"), "File must end with trailing newline"

                # Check 5: File size is reasonable (at least 30 bytes, at most 700 bytes)
                file_size = len(binary_content)
                assert 30 <= file_size <= 700, f"File size should be 30-700 bytes, got {file_size}"

        finally:
            os.chdir(original_cwd)
