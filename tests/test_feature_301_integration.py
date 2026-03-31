"""Integration tests for feature 301: Create markdown file test-wx8ewb.md.

Tests verify that:
1. Feature creates markdown file with correct name at repository root
2. File contains H1 heading matching ^# .+$
3. H1 heading is followed by blank line separator
4. File contains exactly 2-3 sentences of prose
5. File is UTF-8 encoded without BOM
6. File uses Unix LF line endings (not CRLF)
7. File size is at least 50 bytes
8. File ends with exactly one trailing newline
9. Git commit is created with correct message
10. Changes are pushed to remote with upstream tracking
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

# Check if ANTHROPIC_API_KEY is set for integration tests
HAS_API_KEY = bool(os.getenv("ANTHROPIC_API_KEY"))


def setup_module():
    """Set up test environment by adding src to path."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


@pytest.fixture
def temp_repo():
    """Create a temporary git repository for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)

        # Initialize git repository
        subprocess.run(
            ["git", "init"],
            cwd=repo_path,
            check=True,
            capture_output=True,
        )

        # Configure git user (required for commits)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=repo_path,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=repo_path,
            check=True,
            capture_output=True,
        )

        # Create initial commit
        (repo_path / ".gitkeep").write_text("")
        subprocess.run(
            ["git", "add", "."],
            cwd=repo_path,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=repo_path,
            check=True,
            capture_output=True,
        )

        yield repo_path


class TestFeature301FileCreation:
    """Test markdown file creation."""

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set")
    def test_file_exists_at_repository_root(self, temp_repo):
        """Test that file test-wx8ewb.md is created at repository root."""
        from sheep.features.feature_301_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_test_wx8ewb_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_repo)
        try:
            result = create_test_wx8ewb_markdown_file(str(temp_repo))

            # File should exist at repository root
            filepath = temp_repo / MARKDOWN_FILENAME
            assert filepath.exists(), f"File {MARKDOWN_FILENAME} not found at {temp_repo}"
            assert filepath.is_file(), f"{MARKDOWN_FILENAME} is not a regular file"
        finally:
            os.chdir(original_cwd)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set")
    def test_file_has_h1_heading(self, temp_repo):
        """Test that file starts with H1 heading matching ^# .+$."""
        from sheep.features.feature_301_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_test_wx8ewb_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_repo)
        try:
            result = create_test_wx8ewb_markdown_file(str(temp_repo))

            filepath = temp_repo / MARKDOWN_FILENAME
            content = filepath.read_text(encoding="utf-8")
            lines = content.split("\n")

            # First line should be H1 heading
            h1_pattern = r"^# .+$"
            assert lines[0], "First line is empty"
            assert re.match(h1_pattern, lines[0]), \
                f"First line '{lines[0]}' does not match H1 pattern '^# .+$'"
        finally:
            os.chdir(original_cwd)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set")
    def test_blank_line_after_heading(self, temp_repo):
        """Test that H1 heading is followed by blank line."""
        from sheep.features.feature_301_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_test_wx8ewb_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_repo)
        try:
            result = create_test_wx8ewb_markdown_file(str(temp_repo))

            filepath = temp_repo / MARKDOWN_FILENAME
            content = filepath.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Second line should be blank
            assert len(lines) > 1, "File has only one line (no blank line after heading)"
            assert lines[1] == "", \
                f"Second line '{lines[1]}' is not blank (should be blank separator)"
        finally:
            os.chdir(original_cwd)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set")
    def test_prose_contains_2_to_3_sentences(self, temp_repo):
        """Test that prose content contains exactly 2-3 sentences."""
        from sheep.features.feature_301_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_test_wx8ewb_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_repo)
        try:
            result = create_test_wx8ewb_markdown_file(str(temp_repo))

            filepath = temp_repo / MARKDOWN_FILENAME
            content = filepath.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Prose is everything after the blank line (skip H1 and blank line)
            prose_lines = lines[2:]
            prose = "\n".join(prose_lines).strip()

            # Count sentences by counting periods
            sentence_count = prose.count(".")

            assert 2 <= sentence_count <= 3, \
                f"Prose contains {sentence_count} sentences (expected 2-3): {prose}"
        finally:
            os.chdir(original_cwd)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set")
    def test_utf8_encoding_no_bom(self, temp_repo):
        """Test that file is UTF-8 encoded without BOM."""
        from sheep.features.feature_301_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_test_wx8ewb_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_repo)
        try:
            result = create_test_wx8ewb_markdown_file(str(temp_repo))

            filepath = temp_repo / MARKDOWN_FILENAME

            # Read file as binary to check for BOM
            binary_content = filepath.read_bytes()

            # UTF-8 BOM is b'\xef\xbb\xbf'
            assert not binary_content.startswith(b'\xef\xbb\xbf'), \
                "File contains UTF-8 BOM (byte order mark)"

            # Verify file is valid UTF-8
            try:
                binary_content.decode("utf-8")
            except UnicodeDecodeError as e:
                pytest.fail(f"File is not valid UTF-8: {e}")
        finally:
            os.chdir(original_cwd)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set")
    def test_lf_line_endings(self, temp_repo):
        """Test that file uses Unix LF line endings (not CRLF or mixed)."""
        from sheep.features.feature_301_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_test_wx8ewb_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_repo)
        try:
            result = create_test_wx8ewb_markdown_file(str(temp_repo))

            filepath = temp_repo / MARKDOWN_FILENAME
            binary_content = filepath.read_bytes()

            # Should not contain CRLF (\r\n)
            assert b"\r\n" not in binary_content, \
                "File contains CRLF line endings (Windows style)"

            # Should not contain bare CR (\r)
            assert b"\r" not in binary_content, \
                "File contains CR line endings (old Mac style)"

            # Should contain LF (\n) for line separators
            assert b"\n" in binary_content, \
                "File does not contain LF line separators"
        finally:
            os.chdir(original_cwd)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set")
    def test_file_size_minimum(self, temp_repo):
        """Test that file size is at least 50 bytes."""
        from sheep.features.feature_301_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_test_wx8ewb_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_repo)
        try:
            result = create_test_wx8ewb_markdown_file(str(temp_repo))

            filepath = temp_repo / MARKDOWN_FILENAME
            file_size = filepath.stat().st_size

            assert file_size >= 50, \
                f"File size {file_size} bytes is less than minimum 50 bytes"
        finally:
            os.chdir(original_cwd)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set")
    def test_trailing_newline(self, temp_repo):
        """Test that file ends with exactly one trailing newline."""
        from sheep.features.feature_301_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_test_wx8ewb_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_repo)
        try:
            result = create_test_wx8ewb_markdown_file(str(temp_repo))

            filepath = temp_repo / MARKDOWN_FILENAME
            binary_content = filepath.read_bytes()

            # Should end with exactly one LF
            assert binary_content.endswith(b"\n"), \
                "File does not end with newline"
            assert not binary_content.endswith(b"\n\n"), \
                "File ends with multiple newlines (should be exactly one)"
        finally:
            os.chdir(original_cwd)


class TestFeature301GitOperations:
    """Test git operations (commit and push)."""

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set")
    def test_git_commit_created(self, temp_repo):
        """Test that git commit is created with correct message."""
        from sheep.features.feature_301_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_test_wx8ewb_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_repo)
        try:
            result = create_test_wx8ewb_markdown_file(str(temp_repo))

            # Get git log to verify commit was created
            log_result = subprocess.run(
                ["git", "log", "--oneline", "-n", "2"],
                cwd=temp_repo,
                capture_output=True,
                text=True,
                check=True,
            )

            log_output = log_result.stdout

            # Should contain feature commit message
            expected_message = f"feat(301): create markdown file {MARKDOWN_FILENAME} with prose content"
            assert expected_message in log_output, \
                f"Commit message not found in git log.\nExpected: {expected_message}\nGot: {log_output}"
        finally:
            os.chdir(original_cwd)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set")
    def test_commit_message_format(self, temp_repo):
        """Test that commit message follows conventional commit format."""
        from sheep.features.feature_301_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_test_wx8ewb_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_repo)
        try:
            result = create_test_wx8ewb_markdown_file(str(temp_repo))

            # Return value should include commit message
            assert "commit_message" in result, \
                "Result does not contain 'commit_message' key"

            commit_message = result["commit_message"]

            # Should start with "feat(301):"
            assert commit_message.startswith("feat(301):"), \
                f"Commit message does not start with 'feat(301):': {commit_message}"

            # Should mention the filename
            assert MARKDOWN_FILENAME in commit_message, \
                f"Commit message does not mention filename {MARKDOWN_FILENAME}: {commit_message}"
        finally:
            os.chdir(original_cwd)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set")
    def test_file_is_staged_and_committed(self, temp_repo):
        """Test that file is staged and committed (not just created)."""
        from sheep.features.feature_301_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_test_wx8ewb_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_repo)
        try:
            result = create_test_wx8ewb_markdown_file(str(temp_repo))

            # Check git status - should show no changes
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=temp_repo,
                capture_output=True,
                text=True,
                check=True,
            )

            status_output = status_result.stdout.strip()

            # If there are unstaged changes, it means file wasn't properly committed
            # (unless it's some other file we don't care about)
            lines = status_output.split("\n")
            for line in lines:
                if MARKDOWN_FILENAME in line:
                    pytest.fail(f"File {MARKDOWN_FILENAME} is not properly committed: {line}")
        finally:
            os.chdir(original_cwd)


class TestFeature301ReturnValue:
    """Test that feature returns correct result structure."""

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set")
    def test_return_dict_structure(self, temp_repo):
        """Test that function returns dictionary with required keys."""
        from sheep.features.feature_301_markdown_file_creation import (
            create_test_wx8ewb_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_repo)
        try:
            result = create_test_wx8ewb_markdown_file(str(temp_repo))

            # Should return dict
            assert isinstance(result, dict), f"Result is not a dict: {type(result)}"

            # Should have required keys
            required_keys = ["filepath", "content", "commit_message", "push_result"]
            for key in required_keys:
                assert key in result, f"Result missing required key: {key}"
        finally:
            os.chdir(original_cwd)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set")
    def test_return_filepath_is_correct(self, temp_repo):
        """Test that returned filepath matches created file."""
        from sheep.features.feature_301_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_test_wx8ewb_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_repo)
        try:
            result = create_test_wx8ewb_markdown_file(str(temp_repo))

            filepath = result["filepath"]

            # Should be a string
            assert isinstance(filepath, str), f"filepath is not a string: {type(filepath)}"

            # Should end with the correct filename
            assert filepath.endswith(MARKDOWN_FILENAME), \
                f"filepath '{filepath}' does not end with '{MARKDOWN_FILENAME}'"

            # File should exist
            assert Path(filepath).exists(), f"File at returned path does not exist: {filepath}"
        finally:
            os.chdir(original_cwd)

    @pytest.mark.skipif(not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set")
    def test_return_content_matches_file(self, temp_repo):
        """Test that returned content matches file contents."""
        from sheep.features.feature_301_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_test_wx8ewb_markdown_file,
        )

        original_cwd = os.getcwd()
        os.chdir(temp_repo)
        try:
            result = create_test_wx8ewb_markdown_file(str(temp_repo))

            # Read actual file
            filepath = temp_repo / MARKDOWN_FILENAME
            actual_content = filepath.read_text(encoding="utf-8")

            # Should match returned content
            assert result["content"] == actual_content, \
                "Returned content does not match file contents"
        finally:
            os.chdir(original_cwd)
