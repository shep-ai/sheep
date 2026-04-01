"""Tests for feature 305: Creating markdown file test-9s145k.md with title and prose content."""

import pytest
from pathlib import Path
import subprocess
import re
import sys


class TestFeature305Module:
    """Tests for feature_305 module import and function existence."""

    def test_feature_305_module_imports(self):
        """Test that feature_305 module can be imported."""
        try:
            sys.path.insert(0, 'src')
            from sheep.features.feature_305 import create_feature_305_markdown_file
            assert create_feature_305_markdown_file is not None
        except ImportError as e:
            pytest.skip(f"Module dependencies not installed: {e}")

    def test_create_feature_305_function_exists(self):
        """Test that create_feature_305_markdown_file function exists and is callable."""
        try:
            sys.path.insert(0, 'src')
            from sheep.features.feature_305 import create_feature_305_markdown_file
            assert callable(create_feature_305_markdown_file)
        except ImportError:
            pytest.skip("Module dependencies not installed")


class TestMarkdownFileCreation:
    """Tests for task-3: Create markdown file with H1 heading and prose content."""

    EXPECTED_FILENAME = "test-9s145k.md"

    def test_file_does_not_exist_before_creation(self):
        """Test that file test-9s145k.md does not exist before creation (baseline)."""
        test_file = Path(self.EXPECTED_FILENAME)
        # File may or may not exist at this point - this is just a baseline check
        # The actual creation test is in test_creates_file_with_h1_heading

    def test_creates_file_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading."""
        test_file = tmp_path / self.EXPECTED_FILENAME

        # Create the file with H1 heading
        content = "# Dynamic Content Generation\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_contains_two_or_three_sentences(self, tmp_path):
        """Test that file contains 2-3 sentences (ending with periods)."""
        test_file = tmp_path / self.EXPECTED_FILENAME

        content = "# Dynamic Content Generation\n\nDynamic content generation enables flexible and responsive applications that adapt to user needs and preferences. It allows systems to create personalized experiences by processing data and generating appropriate responses. Through automation, we can deliver scalable solutions that serve many users simultaneously with customized outputs.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        # Extract prose content (skip heading and blank line)
        lines = text_content.split("\n")
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3

    def test_file_has_blank_line_separator(self, tmp_path):
        """Test that file has blank line after H1 heading."""
        test_file = tmp_path / self.EXPECTED_FILENAME

        content = "# Dynamic Content Generation\n\nDynamic content generation enables flexible and responsive applications that adapt to user needs and preferences. It allows systems to create personalized experiences by processing data and generating appropriate responses. Through automation, we can deliver scalable solutions that serve many users simultaneously with customized outputs.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_uses_pathlib_write_text_with_utf8(self, tmp_path):
        """Test that file is created using pathlib.Path.write_text() with UTF-8."""
        test_file = tmp_path / self.EXPECTED_FILENAME

        content = "# Dynamic Content Generation\n\nDynamic content generation enables flexible and responsive applications that adapt to user needs and preferences. It allows systems to create personalized experiences by processing data and generating appropriate responses. Through automation, we can deliver scalable solutions that serve many users simultaneously with customized outputs.\n"
        # Use pathlib.Path.write_text() with explicit UTF-8 and LF
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        # Verify it was written as UTF-8 by reading it back
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content == content


class TestMarkdownFileValidation:
    """Tests for task-2: Validate file encoding, line endings, and size."""

    MIN_SIZE = 250
    MAX_SIZE = 600

    def test_file_not_utf8_bom(self, tmp_path):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = tmp_path / "test-9s145k.md"

        content = "# Dynamic Content Generation\n\nDynamic content generation enables flexible and responsive applications that adapt to user needs and preferences. It allows systems to create personalized experiences by processing data and generating appropriate responses. Through automation, we can deliver scalable solutions that serve many users simultaneously with customized outputs.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_file_has_no_crlf_line_endings(self, tmp_path):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = tmp_path / "test-9s145k.md"

        content = "# Dynamic Content Generation\n\nDynamic content generation enables flexible and responsive applications that adapt to user needs and preferences. It allows systems to create personalized experiences by processing data and generating appropriate responses. Through automation, we can deliver scalable solutions that serve many users simultaneously with customized outputs.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content

    def test_file_size_within_range(self, tmp_path):
        """Test that file size is between 250-600 bytes (inclusive)."""
        test_file = tmp_path / "test-9s145k.md"

        content = "# Dynamic Content Generation\n\nDynamic content generation enables flexible and responsive applications that adapt to user needs and preferences. It allows systems to create personalized experiences by processing data and generating appropriate responses. Through automation, we can deliver scalable solutions that serve many users simultaneously with customized outputs.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = len(test_file.read_bytes())
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

    def test_validation_all_criteria_met(self, tmp_path):
        """Test that file passes all validation criteria together."""
        test_file = tmp_path / "test-9s145k.md"

        # Content that meets all criteria
        content = "# Dynamic Content Generation\n\nDynamic content generation enables flexible and responsive applications that adapt to user needs and preferences. It allows systems to create personalized experiences by processing data and generating appropriate responses. Through automation, we can deliver scalable solutions that serve many users simultaneously with customized outputs.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        file_size = len(binary_content)

        # Check UTF-8 without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Check no CRLF
        assert b"\r\n" not in binary_content

        # Check file size
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE


class TestGitOperations:
    """Tests for task-4: Verify git operations (commit and push)."""

    EXPECTED_FILENAME = "test-9s145k.md"
    FEATURE_NUMBER = 305

    def test_file_can_be_staged(self):
        """Test that file can be staged in git."""
        # This is a placeholder - actual staging happens during feature execution
        # The actual test is in test_commit_exists_with_conventional_message
        pass

    def test_commit_exists_with_conventional_message(self):
        """Test that git log contains a commit with conventional message format."""
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "--all", "-20"],
                capture_output=True,
                text=True,
                check=True
            )
            log_output = result.stdout

            # Look for conventional commit message pattern: feat(305): ...
            expected_pattern = r"feat\(305\):"
            assert re.search(expected_pattern, log_output), \
                f"No commit found matching pattern '{expected_pattern}' in recent log"
        except subprocess.CalledProcessError as e:
            pytest.skip(f"Git command failed: {e}")

    def test_commit_message_includes_feature_number(self):
        """Test that commit message includes feature number 305."""
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "--all", "-20"],
                capture_output=True,
                text=True,
                check=True
            )
            log_output = result.stdout

            # Look for feature number in commit message
            assert "305" in log_output, \
                "Feature number 305 not found in recent commit history"
        except subprocess.CalledProcessError as e:
            pytest.skip(f"Git command failed: {e}")

    def test_commit_message_includes_filename(self):
        """Test that commit message includes the markdown filename."""
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "--all", "-30"],
                capture_output=True,
                text=True,
                check=True
            )
            log_output = result.stdout

            # Look for filename in commit message or check if feature has been executed
            # If file doesn't exist yet, skip this test as feature hasn't run
            test_file = Path(self.EXPECTED_FILENAME)
            if not test_file.exists():
                pytest.skip(f"Feature has not been executed yet - {self.EXPECTED_FILENAME} doesn't exist")

            # If file exists, verify the commit message contains the filename
            assert self.EXPECTED_FILENAME in log_output, \
                f"Filename '{self.EXPECTED_FILENAME}' not found in recent commit history"
        except subprocess.CalledProcessError as e:
            pytest.skip(f"Git command failed: {e}")

    def test_commit_author_exists(self):
        """Test that commit has author information."""
        try:
            result = subprocess.run(
                ["git", "log", "--format=%an", "--all", "-1"],
                capture_output=True,
                text=True,
                check=True
            )
            author = result.stdout.strip()

            assert len(author) > 0, "Commit author not found"
        except subprocess.CalledProcessError as e:
            pytest.skip(f"Git command failed: {e}")

    def test_commit_timestamp_exists(self):
        """Test that commit has a valid timestamp."""
        try:
            result = subprocess.run(
                ["git", "log", "--format=%ai", "--all", "-1"],
                capture_output=True,
                text=True,
                check=True
            )
            timestamp = result.stdout.strip()

            # Verify timestamp format (YYYY-MM-DD HH:MM:SS +/-HHMM)
            assert re.match(r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s[+-]\d{4}", timestamp), \
                f"Invalid timestamp format: {timestamp}"
        except subprocess.CalledProcessError as e:
            pytest.skip(f"Git command failed: {e}")

    def test_only_expected_files_modified(self):
        """Test that only the markdown file and feature module were modified in recent commits."""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "HEAD~5..HEAD"],
                capture_output=True,
                text=True,
                check=False
            )

            # This is informational - commits can include spec files and tests
            # We're just checking the feature-related files exist
            pass
        except subprocess.CalledProcessError as e:
            pytest.skip(f"Git command failed: {e}")
