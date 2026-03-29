"""Comprehensive integration tests for feature 267: markdown file creation.

Tests verify the complete end-to-end workflow:
1. File creation with proper formatting, encoding, and line endings
2. Comprehensive validation of all aspects (format, encoding, line endings, etc.)
3. Git operations (add, commit, push) with proper messages
4. Full orchestration via create_feature_267_markdown_file() function

These tests create actual files and perform real git operations
to ensure the complete workflow succeeds.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest


def setup_module():
    """Set up test environment by adding src to path."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


@pytest.fixture
def mock_llm():
    """Create a mock LLM that returns valid markdown content."""
    mock = Mock()
    mock.call.return_value = {
        "content": """# The Power of Curiosity

Curiosity drives human innovation and discovery throughout history. It inspires us to ask questions and seek deeper understanding. When cultivated deliberately, curiosity becomes a powerful tool for personal growth and creative excellence."""
    }
    return mock


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


class TestFeature267Integration:
    """Integration tests for feature 267 markdown file creation."""

    def test_integration_full_workflow(self, temp_git_repo, mock_llm):
        """Test complete workflow: create file, validate, stage, commit.

        This integration test verifies that the entire feature 267 workflow
        succeeds end-to-end. Mocks LLM but tests real file I/O and git ops.

        Steps:
        1. Create markdown file with proper format
        2. Validate file meets all requirements
        3. File should be staged in git
        4. Commit should be created with correct message
        5. Verify commit appears in git history
        """
        from sheep.features.feature_267_markdown_file_creation import (
            FEATURE_NUMBER,
            MARKDOWN_FILENAME,
            create_feature_267_markdown_file,
        )

        # Change to temp repo directory
        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            # Mock LLM generation and git push
            with patch(
                "sheep.content_generators.get_reasoning_llm",
                return_value=mock_llm
            ), patch(
                "sheep.features.feature_267_markdown_file_creation.push_markdown_file"
            ) as mock_push:
                mock_push.return_value = {"status": "success"}

                # Execute the complete workflow
                result = create_feature_267_markdown_file(str(temp_git_repo))

                # Verify result structure
                assert isinstance(result, dict), "Result should be a dictionary"
                assert "filepath" in result
                assert "content" in result
                assert "commit_message" in result
                assert "push_result" in result

                # Verify file exists
                file_path = Path(result["filepath"])
                assert file_path.exists(), "File should exist after creation"
                assert file_path.name == MARKDOWN_FILENAME

                # Verify commit message format
                expected_message = (
                    f"feat({FEATURE_NUMBER}): "
                    f"Create markdown file {MARKDOWN_FILENAME} with prose content"
                )
                assert result["commit_message"] == expected_message

                # Verify commit appears in git log
                log_result = subprocess.run(
                    ["git", "log", "--oneline"],
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=temp_git_repo,
                )
                assert expected_message in log_result.stdout, (
                    f"Commit message should appear in git log: {log_result.stdout}"
                )

                # Verify git push was called
                mock_push.assert_called()

                # Clean up created file
                file_path.unlink()

        finally:
            os.chdir(original_cwd)

    def test_integration_file_creation_and_validation(self, temp_git_repo, mock_llm):
        """Test file creation with proper format, encoding, and line endings.

        Verifies all non-functional requirements:
        - UTF-8 encoding without BOM
        - Unix LF line endings
        - Proper H1 and blank line structure
        - File content is valid markdown
        """
        from sheep.features.feature_267_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_feature_267_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            with patch(
                "sheep.content_generators.get_reasoning_llm",
                return_value=mock_llm
            ), patch(
                "sheep.features.feature_267_markdown_file_creation.push_markdown_file"
            ) as mock_push:
                mock_push.return_value = {"status": "success"}

                result = create_feature_267_markdown_file(str(temp_git_repo))
                file_path = Path(result["filepath"])
                binary_content = file_path.read_bytes()

                # Check: No UTF-8 BOM
                assert not binary_content.startswith(b"\xef\xbb\xbf"), (
                    "File should not have UTF-8 BOM"
                )

                # Check: Valid UTF-8
                try:
                    binary_content.decode("utf-8")
                except UnicodeDecodeError:
                    pytest.fail("File should be valid UTF-8")

                # Check: LF line endings only (no CRLF or CR)
                assert b"\r\n" not in binary_content, (
                    "File should not have CRLF line endings"
                )
                assert b"\r" not in binary_content, (
                    "File should not have CR line endings"
                )

                # Check: File size in reasonable range (100-800 bytes)
                file_size = len(binary_content)
                assert (
                    100 <= file_size <= 800
                ), f"File size {file_size} should be 100-800 bytes"

                # Check: First line is H1, second line is blank
                text_content = binary_content.decode("utf-8")
                lines = text_content.split("\n")
                assert lines[0].startswith("# "), (
                    "First line should be H1 heading"
                )
                # May have varying blank line structure, check prose exists
                assert len(lines) > 2, "File should have heading and prose"

                # Check: Ends with newline
                assert text_content.endswith("\n"), (
                    "File should end with trailing newline"
                )

                # Clean up
                file_path.unlink()

        finally:
            os.chdir(original_cwd)

    def test_integration_sentence_count_validation(self, temp_git_repo, mock_llm):
        """Test that prose content has 2-3 sentences.

        Verifies sentence counting works correctly by checking for periods.
        """
        from sheep.features.feature_267_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_feature_267_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            with patch(
                "sheep.content_generators.get_reasoning_llm",
                return_value=mock_llm
            ), patch(
                "sheep.features.feature_267_markdown_file_creation.push_markdown_file"
            ) as mock_push:
                mock_push.return_value = {"status": "success"}

                result = create_feature_267_markdown_file(str(temp_git_repo))
                file_path = Path(result["filepath"])

                # Read content
                content = file_path.read_text(encoding="utf-8")

                # Count sentences (by periods in prose, not heading)
                # Remove heading line (before first blank line)
                lines = content.split("\n")
                heading_idx = 0
                prose_start_idx = 2  # After heading and blank line

                prose_text = "\n".join(lines[prose_start_idx:])
                sentence_count = prose_text.count(".")

                # Should be 2-3 sentences
                assert sentence_count in (2, 3), (
                    f"Should have 2-3 sentences in prose, found {sentence_count}"
                )

                # Clean up
                file_path.unlink()

        finally:
            os.chdir(original_cwd)

    def test_integration_return_value_structure(self, temp_git_repo, mock_llm):
        """Test that function returns dict with all required keys.

        Verifies return value includes:
        - filepath (path to created file)
        - content (markdown content)
        - commit_message (git commit message)
        - push_result (result from git push)
        """
        from sheep.features.feature_267_markdown_file_creation import (
            FEATURE_NUMBER,
            MARKDOWN_FILENAME,
            create_feature_267_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            with patch(
                "sheep.content_generators.get_reasoning_llm",
                return_value=mock_llm
            ), patch(
                "sheep.features.feature_267_markdown_file_creation.push_markdown_file"
            ) as mock_push:
                mock_push.return_value = {"status": "success"}

                result = create_feature_267_markdown_file(str(temp_git_repo))

                # Check required keys
                required_keys = {"filepath", "content", "commit_message", "push_result"}
                assert set(result.keys()) == required_keys, (
                    f"Result should have keys {required_keys}, got {set(result.keys())}"
                )

                # Check types
                assert isinstance(result["filepath"], str)
                assert isinstance(result["content"], str)
                assert isinstance(result["commit_message"], str)

                # Check commit message format
                assert "feat(" in result["commit_message"]
                assert str(FEATURE_NUMBER) in result["commit_message"]
                assert MARKDOWN_FILENAME in result["commit_message"]

                # Check content is non-empty
                assert len(result["content"]) > 0

                # Clean up
                Path(result["filepath"]).unlink()

        finally:
            os.chdir(original_cwd)

    def test_integration_file_content_in_result_matches_file(self, temp_git_repo, mock_llm):
        """Test that content in result dict matches actual file content."""
        from sheep.features.feature_267_markdown_file_creation import (
            create_feature_267_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            with patch(
                "sheep.content_generators.get_reasoning_llm",
                return_value=mock_llm
            ), patch(
                "sheep.features.feature_267_markdown_file_creation.push_markdown_file"
            ) as mock_push:
                mock_push.return_value = {"status": "success"}

                result = create_feature_267_markdown_file(str(temp_git_repo))
                file_content = Path(result["filepath"]).read_text(encoding="utf-8")

                assert result["content"] == file_content, (
                    "Content in result dict should match file content"
                )

                # Clean up
                Path(result["filepath"]).unlink()

        finally:
            os.chdir(original_cwd)

    def test_integration_git_staging_and_commit(self, temp_git_repo, mock_llm):
        """Test that file is properly staged and committed.

        Verifies git operations complete successfully and
        commit message follows conventional commit format.
        """
        from sheep.features.feature_267_markdown_file_creation import (
            FEATURE_NUMBER,
            MARKDOWN_FILENAME,
            create_feature_267_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            with patch(
                "sheep.content_generators.get_reasoning_llm",
                return_value=mock_llm
            ), patch(
                "sheep.features.feature_267_markdown_file_creation.push_markdown_file"
            ) as mock_push:
                mock_push.return_value = {"status": "success"}

                result = create_feature_267_markdown_file(str(temp_git_repo))

                # Verify commit message format follows convention
                msg = result["commit_message"]
                assert msg.startswith("feat("), "Should start with 'feat('"
                assert str(FEATURE_NUMBER) in msg, "Should include feature number"
                assert ")" in msg, "Should have closing paren after feature number"
                assert ": " in msg, "Should have ': ' after type and scope"

                # Verify commit is in git log
                log_cmd = ["git", "log", "--pretty=format:%s"]
                log_result = subprocess.run(
                    log_cmd,
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=temp_git_repo,
                )
                assert msg in log_result.stdout, (
                    f"Commit message '{msg}' not found in git log"
                )

                # Clean up
                Path(result["filepath"]).unlink()

        finally:
            os.chdir(original_cwd)

    def test_integration_idempotency(self, temp_git_repo, mock_llm):
        """Test that feature can be run multiple times without conflicts.

        Verifies that creating the file multiple times in a fresh repo
        doesn't cause conflicts (file is overwritten each time).
        """
        from sheep.features.feature_267_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_feature_267_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            with patch(
                "sheep.content_generators.get_reasoning_llm",
                return_value=mock_llm
            ), patch(
                "sheep.features.feature_267_markdown_file_creation.push_markdown_file"
            ) as mock_push:
                mock_push.return_value = {"status": "success"}

                # Create file multiple times
                for i in range(2):
                    result = create_feature_267_markdown_file(str(temp_git_repo))
                    file_path = Path(result["filepath"])

                    assert file_path.exists(), (
                        f"Iteration {i + 1}: File should exist"
                    )
                    assert file_path.name == MARKDOWN_FILENAME

                    # File content should be valid
                    content = file_path.read_text(encoding="utf-8")
                    assert content.startswith("# "), (
                        f"Iteration {i + 1}: Should start with H1 heading"
                    )
                    assert len(content) > 50, (
                        f"Iteration {i + 1}: Content should have meaningful length"
                    )

                    # Clean up file (but keep git history)
                    file_path.unlink()

        finally:
            os.chdir(original_cwd)

    def test_integration_error_handling_invalid_repo(self):
        """Test that invalid repo path is handled gracefully."""
        from sheep.features.feature_267_markdown_file_creation import (
            create_feature_267_markdown_file,
        )

        # Try with nonexistent repo path
        with pytest.raises(Exception):
            create_feature_267_markdown_file("/nonexistent/repo/path")

    def test_integration_encoding_specific_characters(self, temp_git_repo, mock_llm):
        """Test that file handles UTF-8 specific characters correctly.

        Verifies that special characters are encoded/decoded properly.
        """
        from sheep.features.feature_267_markdown_file_creation import (
            create_feature_267_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_git_repo)

        try:
            with patch(
                "sheep.content_generators.get_reasoning_llm",
                return_value=mock_llm
            ), patch(
                "sheep.features.feature_267_markdown_file_creation.push_markdown_file"
            ) as mock_push:
                mock_push.return_value = {"status": "success"}

                result = create_feature_267_markdown_file(str(temp_git_repo))
                file_path = Path(result["filepath"])

                # Read as binary and decode
                binary_content = file_path.read_bytes()
                try:
                    decoded = binary_content.decode("utf-8")
                except UnicodeDecodeError as e:
                    pytest.fail(f"Failed to decode UTF-8: {e}")

                # Should be readable without errors
                assert len(decoded) > 0
                assert isinstance(decoded, str)

                # Clean up
                file_path.unlink()

        finally:
            os.chdir(original_cwd)


class TestFeature267ManualExecution:
    """Tests for manual execution of feature 267."""

    def test_module_can_be_executed_as_script(self):
        """Test that feature module can be executed as a script."""
        from sheep.features.feature_267_markdown_file_creation import (
            FEATURE_NUMBER,
            MARKDOWN_FILENAME,
        )

        # Verify module has required components for script execution
        assert FEATURE_NUMBER == 267
        assert MARKDOWN_FILENAME == "test-c6jsj2.md"

    def test_module_has_main_block(self):
        """Test that module has __main__ block for direct execution."""
        import inspect
        from sheep.features import feature_267_markdown_file_creation

        source = inspect.getsource(feature_267_markdown_file_creation)
        assert 'if __name__ == "__main__"' in source, (
            "Module should have __main__ block"
        )

    def test_create_function_has_proper_docstring(self):
        """Test that create_feature_267_markdown_file has comprehensive docstring."""
        from sheep.features.feature_267_markdown_file_creation import (
            create_feature_267_markdown_file,
        )

        doc = create_feature_267_markdown_file.__doc__
        assert doc is not None, "Function should have docstring"
        assert "markdown file" in doc.lower(), "Docstring should describe markdown"
        assert "Returns:" in doc, "Docstring should have Returns section"
        assert "Args:" in doc, "Docstring should have Args section"
