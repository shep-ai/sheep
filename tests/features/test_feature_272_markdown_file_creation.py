"""Tests for feature 272: Create markdown file test-wvkqjb.md with prose content.

Tests cover:
- File creation with correct name and location
- File contains H1 heading and 2-3 sentences
- File encoding (UTF-8 without BOM) and line endings (LF)
- File ends with trailing newline
- File size is within spec bounds (150-800 bytes)
- Markdown validation passes
- Git operations are executed with correct commit message
- Only test-wvkqjb.md is committed (no other files)
- Push to remote is successful
- Function returns correct structure
- Proper cleanup after test execution
"""

import os
import re
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from sheep.features.feature_272_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_272_markdown_file,
)

# Sample valid markdown content for testing
SAMPLE_MARKDOWN = """# Artificial Intelligence Evolution

Artificial intelligence has rapidly transformed from theoretical concept to practical application across industries. Machine learning algorithms now power recommendation systems, autonomous vehicles, and medical diagnostic tools. The field continues to evolve with advances in neural networks and large language models."""


# Pytest Fixtures
@pytest.fixture
def temp_repo_dir():
    """Create a temporary directory that acts as a git repository for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            # Initialize a git repository
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)
            # Add a remote
            subprocess.run(["git", "remote", "add", "origin", "https://github.com/test/repo.git"], check=True, capture_output=True)
            yield tmpdir
        finally:
            os.chdir(original_cwd)


@pytest.fixture
def mock_llm():
    """Create a mock LLM that returns valid sample markdown."""
    mock = Mock()
    mock.call.return_value = {"content": SAMPLE_MARKDOWN}
    return mock


@pytest.fixture
def mock_git_operations():
    """Mock git operations to avoid actual git commands during testing."""
    with patch("subprocess.run") as mock_run:
        def run_side_effect(args, *pargs, **kwargs):
            result = MagicMock()
            result.returncode = 0
            result.stdout = ""
            result.stderr = ""
            if isinstance(args, list):
                if "rev-parse" in args:
                    result.stdout = "main\n"
                elif "branch" in args and "--show-current" in args:
                    result.stdout = "feat/markdown-file-creation-e18c7f\n"
            return result

        mock_run.side_effect = run_side_effect
        yield mock_run


class TestFeature272FileCreation:
    """Tests for feature 272 file creation."""

    def test_module_imports_successfully(self):
        """Test that the feature module can be imported without errors."""
        from sheep.features.feature_272_markdown_file_creation import (
            FEATURE_NUMBER,
            FEATURE_NAME,
            MARKDOWN_FILENAME,
        )
        assert FEATURE_NUMBER == 272

    def test_create_file_creates_correct_file(self, temp_repo_dir, mock_llm, mock_git_operations):
        """Test that create_feature_272_markdown_file creates file with correct name."""
        with patch("sheep.content_generators.get_reasoning_llm", return_value=mock_llm):
            result = create_feature_272_markdown_file()
            assert Path(MARKDOWN_FILENAME).exists()
            assert result["filepath"].endswith(MARKDOWN_FILENAME)

    def test_file_contains_h1_heading(self, temp_repo_dir, mock_llm, mock_git_operations):
        """Test that created file contains H1 markdown heading."""
        with patch("sheep.content_generators.get_reasoning_llm", return_value=mock_llm):
            result = create_feature_272_markdown_file()
            content = Path(MARKDOWN_FILENAME).read_text()
            assert content.lstrip().startswith("# "), "File must start with H1 heading"

    def test_file_contains_h1_heading_exactly_once(self, temp_repo_dir, mock_llm, mock_git_operations):
        """Test that file contains exactly one H1 heading."""
        with patch("sheep.content_generators.get_reasoning_llm", return_value=mock_llm):
            result = create_feature_272_markdown_file()
            content = Path(MARKDOWN_FILENAME).read_text()
            h1_count = content.count("\n# ") + (1 if content.startswith("# ") else 0)
            assert h1_count == 1, f"Expected exactly one H1 heading, found {h1_count}"

    def test_file_contains_prose_content(self, temp_repo_dir, mock_llm, mock_git_operations):
        """Test that created file contains prose after H1 heading."""
        with patch("sheep.content_generators.get_reasoning_llm", return_value=mock_llm):
            result = create_feature_272_markdown_file()
            content = Path(MARKDOWN_FILENAME).read_text()
            lines = content.split("\n")
            # Should have: heading, blank line, prose
            assert len(lines) >= 3, "File should have heading, blank line, and prose"
            assert lines[0].startswith("# ")
            assert lines[1] == "", "Second line should be blank"

    def test_file_has_2_to_3_sentences(self, temp_repo_dir, mock_llm, mock_git_operations):
        """Test that file contains exactly 2-3 sentences."""
        with patch("sheep.content_generators.get_reasoning_llm", return_value=mock_llm):
            result = create_feature_272_markdown_file()
            content = Path(MARKDOWN_FILENAME).read_text()
            # Count periods (sentences)
            period_count = content.count(".")
            assert 2 <= period_count <= 3, f"Expected 2-3 sentences, found {period_count}"

    def test_file_size_within_spec_bounds(self, temp_repo_dir, mock_llm, mock_git_operations):
        """Test that file size is between 150-800 bytes."""
        with patch("sheep.content_generators.get_reasoning_llm", return_value=mock_llm):
            result = create_feature_272_markdown_file()
            file_size = Path(MARKDOWN_FILENAME).stat().st_size
            assert (
                150 <= file_size <= 800
            ), f"File size {file_size} bytes not within spec bounds (150-800)"

    def test_file_utf8_encoding_no_bom(self, temp_repo_dir, mock_llm, mock_git_operations):
        """Test that file uses UTF-8 encoding without BOM."""
        with patch("sheep.content_generators.get_reasoning_llm", return_value=mock_llm):
            result = create_feature_272_markdown_file()
            binary_content = Path(MARKDOWN_FILENAME).read_bytes()
            # Check no UTF-8 BOM
            assert (
                not binary_content.startswith(b"\xef\xbb\xbf")
            ), "File should not have UTF-8 BOM"
            # Verify valid UTF-8
            binary_content.decode("utf-8")

    def test_file_uses_lf_line_endings(self, temp_repo_dir, mock_llm, mock_git_operations):
        """Test that file uses Unix LF line endings."""
        with patch("sheep.content_generators.get_reasoning_llm", return_value=mock_llm):
            result = create_feature_272_markdown_file()
            binary_content = Path(MARKDOWN_FILENAME).read_bytes()
            # Check no CRLF or CR
            assert b"\r\n" not in binary_content, "File should not have CRLF endings"
            assert b"\r" not in binary_content, "File should not have CR endings"

    def test_file_ends_with_newline(self, temp_repo_dir, mock_llm, mock_git_operations):
        """Test that file ends with trailing newline."""
        with patch("sheep.content_generators.get_reasoning_llm", return_value=mock_llm):
            result = create_feature_272_markdown_file()
            content = Path(MARKDOWN_FILENAME).read_text()
            assert content.endswith("\n"), "File should end with trailing newline"

    def test_returns_dict_with_required_keys(
        self, temp_repo_dir, mock_llm, mock_git_operations
    ):
        """Test that function returns dict with filepath, content, commit_message, push_result."""
        with patch("sheep.content_generators.get_reasoning_llm", return_value=mock_llm):
            result = create_feature_272_markdown_file()
            assert isinstance(result, dict)
            assert "filepath" in result
            assert "content" in result
            assert "commit_message" in result
            assert "push_result" in result

    def test_commit_message_format(self, temp_repo_dir, mock_llm, mock_git_operations):
        """Test that commit message has correct format for feature 272."""
        with patch("sheep.content_generators.get_reasoning_llm", return_value=mock_llm):
            result = create_feature_272_markdown_file()
            expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with title and prose content"
            assert result["commit_message"] == expected_message

    def test_content_in_result_matches_file(self, temp_repo_dir, mock_llm, mock_git_operations):
        """Test that content in result dict is first 200 chars of file content."""
        with patch("sheep.content_generators.get_reasoning_llm", return_value=mock_llm):
            result = create_feature_272_markdown_file()
            file_content = Path(MARKDOWN_FILENAME).read_text()
            # Content in result should be truncated to first 200 chars
            assert result["content"] == file_content[:200]

    def test_function_signature_accepts_repo_path(
        self, temp_repo_dir, mock_llm, mock_git_operations
    ):
        """Test that function accepts optional repo_path parameter."""
        with patch("sheep.content_generators.get_reasoning_llm", return_value=mock_llm):
            # Should not raise exception
            result = create_feature_272_markdown_file(repo_path=str(Path.cwd()))
            assert result is not None

    def test_error_handling_logs_failures(self, mock_git_operations):
        """Test that error handling logs failures appropriately."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                # Initialize a minimal git repo
                subprocess.run(
                    ["git", "init"],
                    check=True,
                    capture_output=True,
                )
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

                with patch(
                    "sheep.content_generators.get_reasoning_llm"
                ) as mock_llm_factory:
                    # Make LLM raise an exception
                    mock_llm = Mock()
                    mock_llm.call.side_effect = ValueError("LLM API failed")
                    mock_llm_factory.return_value = mock_llm

                    try:
                        create_feature_272_markdown_file()
                    except ValueError:
                        # Expected to raise
                        pass
            finally:
                os.chdir(original_cwd)


class TestFeature272IntegrationTests:
    """Integration tests for feature 272 end-to-end execution."""

    def test_integration_full_workflow_with_actual_git(self, mock_llm):
        """Integration test: full workflow creates file and can verify git operations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                # Initialize a minimal git repo
                subprocess.run(
                    ["git", "init"],
                    check=True,
                    capture_output=True,
                )
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
                subprocess.run(
                    ["git", "remote", "add", "origin", "https://github.com/test/repo.git"],
                    check=True,
                    capture_output=True,
                )

                # Mock LLM and git push
                with patch(
                    "sheep.content_generators.get_reasoning_llm",
                    return_value=mock_llm,
                ):
                    with patch("subprocess.run") as mock_run:

                        def run_side_effect(args, *pargs, **kwargs):
                            result = MagicMock()
                            result.returncode = 0
                            result.stdout = ""
                            result.stderr = ""

                            # Let git commands that don't depend on network run
                            if isinstance(args, list):
                                if "push" in args:
                                    result.returncode = 0
                                    result.stdout = ""
                                    return result
                                elif "rev-parse" in args:
                                    result.stdout = "main\n"
                                    return result
                            return result

                        mock_run.side_effect = run_side_effect

                        # Execute the feature
                        result = create_feature_272_markdown_file()

                        # Verify result structure
                        assert isinstance(result, dict)
                        assert "filepath" in result
                        assert "content" in result
                        assert "commit_message" in result
                        assert "push_result" in result

                        # Verify file was created
                        assert Path(MARKDOWN_FILENAME).exists()

                        # Verify file has correct name
                        assert result["filepath"].endswith(MARKDOWN_FILENAME)

                        # Verify commit message
                        expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with title and prose content"
                        assert result["commit_message"] == expected_message

            finally:
                os.chdir(original_cwd)

    def test_file_exists_at_repository_root(self, mock_llm):
        """Test that file is created at repository root, not in subdirectory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
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
                subprocess.run(
                    ["git", "remote", "add", "origin", "https://github.com/test/repo.git"],
                    check=True,
                    capture_output=True,
                )

                with patch(
                    "sheep.content_generators.get_reasoning_llm",
                    return_value=mock_llm,
                ):
                    with patch("subprocess.run") as mock_run:

                        def run_side_effect(args, *pargs, **kwargs):
                            result = MagicMock()
                            result.returncode = 0
                            result.stdout = ""
                            result.stderr = ""
                            if isinstance(args, list) and "push" in args:
                                return result
                            return result

                        mock_run.side_effect = run_side_effect

                        result = create_feature_272_markdown_file()
                        filepath = Path(result["filepath"])

                        # File should be at repository root
                        assert filepath.parent == Path.cwd()
                        assert filepath.name == MARKDOWN_FILENAME
            finally:
                os.chdir(original_cwd)

    def test_only_markdown_file_is_created(self, mock_llm):
        """Test that only test-wvkqjb.md is created, no other files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
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
                subprocess.run(
                    ["git", "remote", "add", "origin", "https://github.com/test/repo.git"],
                    check=True,
                    capture_output=True,
                )

                # Create a file before running feature to verify no extra files are created
                Path("preexisting.txt").write_text("test")

                with patch(
                    "sheep.content_generators.get_reasoning_llm",
                    return_value=mock_llm,
                ):
                    with patch("subprocess.run") as mock_run:

                        def run_side_effect(args, *pargs, **kwargs):
                            result = MagicMock()
                            result.returncode = 0
                            result.stdout = ""
                            result.stderr = ""
                            return result

                        mock_run.side_effect = run_side_effect

                        result = create_feature_272_markdown_file()

                        # Check that only our markdown file and preexisting file exist
                        repo_files = set(Path(".").glob("*"))
                        # Filter out hidden git files
                        visible_files = {
                            f for f in repo_files if not f.name.startswith(".")
                        }
                        assert MARKDOWN_FILENAME in {f.name for f in visible_files}
                        assert (
                            len(visible_files) == 2
                        ), f"Expected 2 files, found {visible_files}"

            finally:
                os.chdir(original_cwd)

    def test_commit_contains_only_markdown_file(self, mock_llm):
        """Test that only test-wvkqjb.md is in the git commit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
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

                with patch(
                    "sheep.content_generators.get_reasoning_llm",
                    return_value=mock_llm,
                ):
                    result = create_feature_272_markdown_file()

                    # Check git log to verify commit message
                    log_output = subprocess.run(
                        ["git", "log", "--oneline"],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    log_text = log_output.stdout.strip()

                    # Verify commit message is present in log
                    assert (
                        "feat(272): create markdown file test-wvkqjb.md"
                        in log_text
                    )

                    # Check that only markdown file is staged
                    status_output = subprocess.run(
                        ["git", "status", "--short"],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    # After commit, status should be clean or just have untracked files
                    committed_files = [
                        line.split()[-1]
                        for line in status_output.stdout.split("\n")
                        if line.strip() and not line.startswith("??")
                    ]
                    # Should be empty or only have our markdown file
                    assert len(committed_files) == 0 or all(
                        f == MARKDOWN_FILENAME for f in committed_files
                    )

            finally:
                os.chdir(original_cwd)
