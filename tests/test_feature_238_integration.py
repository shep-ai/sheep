"""Comprehensive integration tests for feature 238: markdown file creation.

Tests verify the complete workflow:
1. Content generation orchestration (mocked at LLM boundary only)
2. File creation with correct encoding and line endings (real I/O)
3. Markdown structure validation (H1 heading + 2-3 sentences) (real validation)
4. File size within specification (300-700 bytes)
5. Git staging and commit operations (real git operations)
6. Return value structure and contents
7. No unexpected side effects (clean working directory)

Note: Tests mock only the external Claude API at the boundary (generate_markdown_content).
All file I/O, validation, and git operations use real functions to test integration.
"""

import sys
import os
import tempfile
import subprocess
from pathlib import Path
from unittest import mock

# Add src to path to enable imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Sample markdown content for integration tests
# This simulates the output from Claude API
SAMPLE_MARKDOWN_CONTENT = "# The Art of Innovation\n\nInnovation drives progress and transforms industries by challenging conventional thinking and introducing novel solutions. It combines creativity with practical problem-solving to create value and improve human experience. Through innovation, we unlock new possibilities and achieve breakthroughs that seemed impossible before.\n"


class TestFeature238Integration:
    """Integration tests for feature 238 complete workflow."""

    @staticmethod
    def setup_test_repo(tmpdir: str) -> None:
        """Initialize a git repository for testing."""
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

    @staticmethod
    def get_git_status(filepath: str) -> str:
        """Get git status for a file."""
        result = subprocess.run(
            ["git", "status", "--porcelain", filepath],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    @staticmethod
    def verify_file_encoding(filepath: str) -> bool:
        """Verify file is UTF-8 without BOM with LF line endings."""
        with open(filepath, "rb") as f:
            content = f.read()

        # Check for UTF-8 BOM
        if content.startswith(b"\xef\xbb\xbf"):
            raise AssertionError("File has UTF-8 BOM (should not)")

        # Check for CRLF line endings
        if b"\r\n" in content:
            raise AssertionError("File has CRLF line endings (should use LF)")

        # Verify UTF-8 decoding works
        try:
            content.decode("utf-8")
        except UnicodeDecodeError as e:
            raise AssertionError(f"File is not valid UTF-8: {e}")

        return True

    @staticmethod
    def count_sentences(text: str) -> int:
        """Count sentences by counting periods (simple heuristic)."""
        return text.count(".")

    @staticmethod
    def verify_markdown_structure(filepath: str) -> bool:
        """Verify markdown has H1 heading, blank line, and prose content."""
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines:
            raise AssertionError("File is empty")

        # Check first line is H1 heading
        if not lines[0].startswith("# "):
            raise AssertionError(f"First line should be H1 heading, got: {lines[0]}")

        # Check second line is blank
        if len(lines) < 2 or lines[1].strip() != "":
            raise AssertionError("Second line should be blank line after heading")

        # Check there's prose content
        if len(lines) < 3:
            raise AssertionError("File should contain prose content after heading")

        prose_text = "".join(lines[2:]).strip()
        if not prose_text:
            raise AssertionError("No prose content found")

        # Count sentences in prose
        sentence_count = TestFeature238Integration.count_sentences(prose_text)
        if sentence_count < 2 or sentence_count > 3:
            raise AssertionError(
                f"Prose should have 2-3 sentences, found {sentence_count}"
            )

        return True

    def test_complete_workflow_integration(self):
        """Test complete feature 238 workflow with real utilities (LLM mocked at boundary)."""
        from sheep.features.feature_238_markdown_file_creation import (
            create_feature_238_markdown_file,
            MARKDOWN_FILENAME,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                self.setup_test_repo(tmpdir)

                # Mock only the LLM API boundary (generate_markdown_content)
                # All file I/O, validation, and git operations are real
                with mock.patch("sheep.features.feature_238_markdown_file_creation.generate_markdown_content") as mock_gen:
                    mock_gen.return_value = SAMPLE_MARKDOWN_CONTENT

                    # Execute feature
                    result = create_feature_238_markdown_file(repo_path=tmpdir)

                # Verify return dict structure
                assert isinstance(result, dict), "Result should be a dictionary"
                assert "filepath" in result, "Result should have 'filepath' key"
                assert "content" in result, "Result should have 'content' key"
                assert (
                    "commit_message" in result
                ), "Result should have 'commit_message' key"
                assert "push_result" in result, "Result should have 'push_result' key"

                # Verify filepath
                assert (
                    MARKDOWN_FILENAME in result["filepath"]
                ), f"Filepath should contain {MARKDOWN_FILENAME}"

            finally:
                os.chdir(original_cwd)

    def test_file_existence_and_location(self):
        """Test that file is created at repository root with correct name."""
        from sheep.features.feature_238_markdown_file_creation import (
            create_feature_238_markdown_file,
            MARKDOWN_FILENAME,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                self.setup_test_repo(tmpdir)

                with mock.patch("sheep.features.feature_238_markdown_file_creation.generate_markdown_content") as mock_gen:
                    mock_gen.return_value = SAMPLE_MARKDOWN_CONTENT
                    result = create_feature_238_markdown_file(repo_path=tmpdir)

                filepath = Path(result["filepath"])

                # File should exist
                assert filepath.exists(), f"File {filepath} should exist"

                # File should be in repository root
                assert filepath.name == MARKDOWN_FILENAME, (
                    f"File should be named {MARKDOWN_FILENAME}, "
                    f"got {filepath.name}"
                )

                # File should be readable
                assert filepath.is_file(), "Path should be a regular file"

            finally:
                os.chdir(original_cwd)

    def test_markdown_structure(self):
        """Test that file has correct markdown structure: H1 + blank line + prose."""
        from sheep.features.feature_238_markdown_file_creation import (
            create_feature_238_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                self.setup_test_repo(tmpdir)

                with mock.patch("sheep.features.feature_238_markdown_file_creation.generate_markdown_content") as mock_gen:
                    mock_gen.return_value = SAMPLE_MARKDOWN_CONTENT
                    result = create_feature_238_markdown_file(repo_path=tmpdir)

                filepath = result["filepath"]
                self.verify_markdown_structure(filepath)

            finally:
                os.chdir(original_cwd)

    def test_file_encoding_utf8_no_bom(self):
        """Test that file is UTF-8 without BOM."""
        from sheep.features.feature_238_markdown_file_creation import (
            create_feature_238_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                self.setup_test_repo(tmpdir)

                with mock.patch("sheep.features.feature_238_markdown_file_creation.generate_markdown_content") as mock_gen:
                    mock_gen.return_value = SAMPLE_MARKDOWN_CONTENT
                    result = create_feature_238_markdown_file(repo_path=tmpdir)

                filepath = result["filepath"]
                self.verify_file_encoding(filepath)

            finally:
                os.chdir(original_cwd)

    def test_file_line_endings_lf_only(self):
        """Test that file uses Unix LF line endings (no CRLF)."""
        from sheep.features.feature_238_markdown_file_creation import (
            create_feature_238_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                self.setup_test_repo(tmpdir)

                with mock.patch("sheep.features.feature_238_markdown_file_creation.generate_markdown_content") as mock_gen:
                    mock_gen.return_value = SAMPLE_MARKDOWN_CONTENT
                    result = create_feature_238_markdown_file(repo_path=tmpdir)

                filepath = result["filepath"]

                with open(filepath, "rb") as f:
                    content = f.read()

                # Should not have CRLF
                assert (
                    b"\r\n" not in content
                ), "File should use LF, not CRLF line endings"

                # Should have at least one LF (for line endings)
                assert b"\n" in content, "File should contain LF line endings"

            finally:
                os.chdir(original_cwd)

    def test_file_size_within_specification(self):
        """Test that file size is between 300-700 bytes."""
        from sheep.features.feature_238_markdown_file_creation import (
            create_feature_238_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                self.setup_test_repo(tmpdir)

                with mock.patch("sheep.features.feature_238_markdown_file_creation.generate_markdown_content") as mock_gen:
                    mock_gen.return_value = SAMPLE_MARKDOWN_CONTENT
                    result = create_feature_238_markdown_file(repo_path=tmpdir)

                filepath = result["filepath"]
                file_size = Path(filepath).stat().st_size

                assert (
                    300 <= file_size <= 700
                ), f"File size should be 300-700 bytes, got {file_size}"

            finally:
                os.chdir(original_cwd)

    def test_return_dict_content_matches_file(self):
        """Test that return dict content matches actual file content."""
        from sheep.features.feature_238_markdown_file_creation import (
            create_feature_238_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                self.setup_test_repo(tmpdir)

                with mock.patch("sheep.features.feature_238_markdown_file_creation.generate_markdown_content") as mock_gen:
                    mock_gen.return_value = SAMPLE_MARKDOWN_CONTENT
                    result = create_feature_238_markdown_file(repo_path=tmpdir)

                filepath = result["filepath"]

                # Read actual file content
                with open(filepath, "r", encoding="utf-8") as f:
                    file_content = f.read()

                # Should match return dict content
                assert result["content"] == file_content, (
                    "Return dict content should match actual file content"
                )

            finally:
                os.chdir(original_cwd)

    def test_commit_message_format(self):
        """Test that commit message follows conventional format."""
        from sheep.features.feature_238_markdown_file_creation import (
            create_feature_238_markdown_file,
            FEATURE_NUMBER,
            MARKDOWN_FILENAME,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                self.setup_test_repo(tmpdir)

                with mock.patch("sheep.features.feature_238_markdown_file_creation.generate_markdown_content") as mock_gen:
                    mock_gen.return_value = SAMPLE_MARKDOWN_CONTENT
                    result = create_feature_238_markdown_file(repo_path=tmpdir)

                commit_message = result["commit_message"]

                # Should follow conventional commit format
                assert commit_message.startswith(
                    f"feat({FEATURE_NUMBER}):"
                ), "Should start with feat(238):"

                assert MARKDOWN_FILENAME in commit_message, (
                    f"Commit message should contain {MARKDOWN_FILENAME}"
                )

                expected = (
                    f"feat({FEATURE_NUMBER}): Create markdown file {MARKDOWN_FILENAME} with prose content"
                )
                assert commit_message == expected, (
                    f"Commit message should be exactly: {expected}, "
                    f"got: {commit_message}"
                )

            finally:
                os.chdir(original_cwd)

    def test_git_file_is_staged(self):
        """Test that file is staged in git after operation."""
        from sheep.features.feature_238_markdown_file_creation import (
            create_feature_238_markdown_file,
            MARKDOWN_FILENAME,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                self.setup_test_repo(tmpdir)

                with mock.patch("sheep.features.feature_238_markdown_file_creation.generate_markdown_content") as mock_gen:
                    mock_gen.return_value = SAMPLE_MARKDOWN_CONTENT
                    result = create_feature_238_markdown_file(repo_path=tmpdir)

                # Check git status - file should be in a committed state
                # (either committed or part of the latest commit)
                git_result = subprocess.run(
                    ["git", "log", "--oneline", "-1"],
                    capture_output=True,
                    text=True,
                )

                assert (
                    git_result.returncode == 0
                ), "Should have git commits available"
                assert "feat(238):" in git_result.stdout, (
                    "Latest commit should be the feature commit"
                )

            finally:
                os.chdir(original_cwd)

    def test_no_unexpected_files_created(self):
        """Test that only test-mcfudw.md is created, no other files."""
        from sheep.features.feature_238_markdown_file_creation import (
            create_feature_238_markdown_file,
            MARKDOWN_FILENAME,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                self.setup_test_repo(tmpdir)

                # Get initial file list
                initial_files = set(os.listdir("."))

                with mock.patch("sheep.features.feature_238_markdown_file_creation.generate_markdown_content") as mock_gen:
                    mock_gen.return_value = SAMPLE_MARKDOWN_CONTENT
                    result = create_feature_238_markdown_file(repo_path=tmpdir)

                # Get final file list
                final_files = set(os.listdir("."))

                # Only test-mcfudw.md and .git directory should be new
                new_files = final_files - initial_files

                # Filter out git-related entries
                new_files = {f for f in new_files if not f.startswith(".")}

                assert (
                    new_files == {MARKDOWN_FILENAME}
                ), f"Should only create {MARKDOWN_FILENAME}, but created: {new_files}"

            finally:
                os.chdir(original_cwd)

    def test_prose_has_2_to_3_sentences(self):
        """Test that prose content has exactly 2-3 sentences."""
        from sheep.features.feature_238_markdown_file_creation import (
            create_feature_238_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                self.setup_test_repo(tmpdir)

                with mock.patch("sheep.features.feature_238_markdown_file_creation.generate_markdown_content") as mock_gen:
                    mock_gen.return_value = SAMPLE_MARKDOWN_CONTENT
                    result = create_feature_238_markdown_file(repo_path=tmpdir)

                filepath = result["filepath"]

                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                # Get prose content (skip heading and blank line)
                prose_text = "".join(lines[2:]).strip()
                sentence_count = self.count_sentences(prose_text)

                assert 2 <= sentence_count <= 3, (
                    f"Prose should have 2-3 sentences, found {sentence_count}: {prose_text}"
                )

            finally:
                os.chdir(original_cwd)

    def test_h1_heading_exists(self):
        """Test that file starts with H1 heading."""
        from sheep.features.feature_238_markdown_file_creation import (
            create_feature_238_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                self.setup_test_repo(tmpdir)

                with mock.patch("sheep.features.feature_238_markdown_file_creation.generate_markdown_content") as mock_gen:
                    mock_gen.return_value = SAMPLE_MARKDOWN_CONTENT
                    result = create_feature_238_markdown_file(repo_path=tmpdir)

                filepath = result["filepath"]

                with open(filepath, "r", encoding="utf-8") as f:
                    first_line = f.readline()

                assert first_line.startswith("# "), (
                    f"First line should be H1 heading (# ...), got: {first_line}"
                )

                # Heading should have content after "# "
                heading_text = first_line[2:].strip()
                assert (
                    heading_text
                ), "H1 heading should have text content after '# '"

            finally:
                os.chdir(original_cwd)

    def test_blank_line_after_heading(self):
        """Test that there's a blank line after the H1 heading."""
        from sheep.features.feature_238_markdown_file_creation import (
            create_feature_238_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                self.setup_test_repo(tmpdir)

                with mock.patch("sheep.features.feature_238_markdown_file_creation.generate_markdown_content") as mock_gen:
                    mock_gen.return_value = SAMPLE_MARKDOWN_CONTENT
                    result = create_feature_238_markdown_file(repo_path=tmpdir)

                filepath = result["filepath"]

                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                assert len(lines) >= 2, "File should have at least 2 lines"
                assert lines[1].strip() == "", "Second line should be blank"

            finally:
                os.chdir(original_cwd)

    def test_prose_content_not_empty(self):
        """Test that prose content exists and is not empty."""
        from sheep.features.feature_238_markdown_file_creation import (
            create_feature_238_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                self.setup_test_repo(tmpdir)

                with mock.patch("sheep.features.feature_238_markdown_file_creation.generate_markdown_content") as mock_gen:
                    mock_gen.return_value = SAMPLE_MARKDOWN_CONTENT
                    result = create_feature_238_markdown_file(repo_path=tmpdir)

                filepath = result["filepath"]

                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                # Prose is from line 3 onward
                prose_text = "".join(lines[2:]).strip()

                assert prose_text, "Prose content should not be empty"
                assert len(prose_text) > 20, (
                    "Prose content should be substantial (>20 chars)"
                )

            finally:
                os.chdir(original_cwd)
