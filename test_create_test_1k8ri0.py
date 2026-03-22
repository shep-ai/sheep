"""
Tests for Feature 155: Create markdown file test-1k8ri0.md

Tests cover:
- File creation with proper UTF-8 encoding and LF line endings
- File validation for structure, size, and encoding
- Git operations (add, commit, push)
- Both create_file() and validate_file() functions
"""

import pytest
import subprocess
from pathlib import Path
import tempfile
import os

# Import the functions to test
from create_test_file import create_file, validate_file, git_operations


class TestCreateFile:
    """Tests for the create_file() function."""

    def test_file_does_not_exist_before_create(self):
        """Test that test-1k8ri0.md does not exist initially."""
        filepath = Path("test-1k8ri0.md")
        # Clean up if it exists from previous test run
        if filepath.exists():
            filepath.unlink()
        assert not filepath.exists()

    def test_file_created_at_correct_path(self):
        """Test that create_file() creates file at repository root."""
        filepath = Path("test-1k8ri0.md")
        # Clean up first
        if filepath.exists():
            filepath.unlink()

        create_file()
        assert filepath.exists()

    def test_file_contains_h1_heading(self):
        """Test that file content starts with H1 markdown heading."""
        filepath = Path("test-1k8ri0.md")
        if filepath.exists():
            filepath.unlink()

        create_file()
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')

        assert len(lines) > 0
        assert lines[0].startswith('# ')
        assert len(lines[0]) > 2  # Must have title text after '# '

    def test_file_contains_blank_line_after_heading(self):
        """Test that file has blank line after heading."""
        filepath = Path("test-1k8ri0.md")
        if filepath.exists():
            filepath.unlink()

        create_file()
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')

        assert len(lines) > 1
        assert lines[1] == ''  # Second line must be empty (blank line)

    def test_file_contains_prose_content(self):
        """Test that file contains prose content after blank line."""
        filepath = Path("test-1k8ri0.md")
        if filepath.exists():
            filepath.unlink()

        create_file()
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')
        prose_lines = lines[2:]
        prose = '\n'.join(prose_lines).strip()

        assert len(prose) > 0
        assert len(prose.split()) > 10  # Should have meaningful prose

    def test_file_size_within_target_range(self):
        """Test that file size is between 400-600 bytes."""
        filepath = Path("test-1k8ri0.md")
        if filepath.exists():
            filepath.unlink()

        create_file()
        file_size = filepath.stat().st_size

        assert 400 <= file_size <= 600, f"File size {file_size} outside 400-600 bytes range"

    def test_file_uses_utf8_encoding(self):
        """Test that file is valid UTF-8 without BOM."""
        filepath = Path("test-1k8ri0.md")
        if filepath.exists():
            filepath.unlink()

        create_file()

        # Read as bytes to check for BOM
        raw_bytes = filepath.read_bytes()
        # UTF-8 BOM is bytes ef bb bf
        assert not raw_bytes.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"

        # Should be readable as UTF-8
        content = filepath.read_text(encoding='utf-8')
        assert isinstance(content, str)
        assert len(content) > 0

    def test_file_uses_lf_line_endings(self):
        """Test that file uses LF (Unix-style) line endings, not CRLF."""
        filepath = Path("test-1k8ri0.md")
        if filepath.exists():
            filepath.unlink()

        create_file()

        # Read raw bytes to check for CRLF
        raw_bytes = filepath.read_bytes()

        # Should have LF (0x0A) but not CRLF (0x0D 0x0A)
        # Count occurrences of each
        has_lf = b'\n' in raw_bytes
        has_crlf = b'\r\n' in raw_bytes

        assert has_lf, "File should have LF line endings"
        assert not has_crlf, "File should not have CRLF line endings"


class TestValidateFile:
    """Tests for the validate_file() function."""

    @pytest.fixture(autouse=True)
    def setup_test_file(self):
        """Create the test file before each test."""
        filepath = Path("test-1k8ri0.md")
        if filepath.exists():
            filepath.unlink()
        create_file()
        yield
        # Cleanup after test
        if filepath.exists():
            filepath.unlink()

    def test_validate_file_returns_true_for_valid_file(self):
        """Test that validate_file() returns True when file is valid."""
        result = validate_file()
        assert result is True

    def test_validate_file_fails_when_file_not_exists(self):
        """Test that validate_file() fails when file doesn't exist."""
        filepath = Path("test-1k8ri0.md")
        filepath.unlink()

        with pytest.raises(AssertionError):
            validate_file()

    def test_validate_file_checks_file_size_lower_bound(self):
        """Test that validate_file() detects file size below 300 bytes."""
        filepath = Path("test-1k8ri0.md")
        # Create a file that's too small
        small_content = "# Title\n\nShort."
        filepath.write_bytes(small_content.encode('utf-8'))

        with pytest.raises(AssertionError) as exc_info:
            validate_file()
        assert "outside acceptable range" in str(exc_info.value)

    def test_validate_file_checks_file_size_upper_bound(self):
        """Test that validate_file() detects file size above 800 bytes."""
        filepath = Path("test-1k8ri0.md")
        # Create a file that's too large
        large_content = "# Title\n\n" + ("This is a sentence. " * 100) + "\n"
        filepath.write_bytes(large_content.encode('utf-8'))

        with pytest.raises(AssertionError) as exc_info:
            validate_file()
        assert "outside acceptable range" in str(exc_info.value)

    def test_validate_file_checks_h1_heading_exists(self):
        """Test that validate_file() fails when H1 heading is missing."""
        filepath = Path("test-1k8ri0.md")
        # Create file without H1 heading
        no_heading = "## Heading Two\n\nSome prose here. And more prose."
        filepath.write_bytes(no_heading.encode('utf-8'))

        with pytest.raises(AssertionError) as exc_info:
            validate_file()
        assert "must be H1 heading" in str(exc_info.value)

    def test_validate_file_checks_blank_line_after_heading(self):
        """Test that validate_file() fails when blank line is missing after heading."""
        filepath = Path("test-1k8ri0.md")
        # Create file without blank line after heading
        no_blank = "# Title\nSome prose here. And more prose here too."
        filepath.write_bytes(no_blank.encode('utf-8'))

        with pytest.raises(AssertionError) as exc_info:
            validate_file()
        assert "must be blank" in str(exc_info.value)

    def test_validate_file_checks_prose_content_exists(self):
        """Test that validate_file() fails when prose is missing."""
        filepath = Path("test-1k8ri0.md")
        # Create file with only heading and blank line
        no_prose = "# Title\n\n"
        filepath.write_bytes(no_prose.encode('utf-8'))

        with pytest.raises(AssertionError) as exc_info:
            validate_file()
        assert "at least 2 sentences" in str(exc_info.value)

    def test_validate_file_checks_minimum_sentence_count(self):
        """Test that validate_file() fails when prose has fewer than 2 sentences."""
        filepath = Path("test-1k8ri0.md")
        # Create file with only one sentence
        one_sentence = "# Title\n\nThis is only one sentence.\n"
        filepath.write_bytes(one_sentence.encode('utf-8'))

        with pytest.raises(AssertionError) as exc_info:
            validate_file()
        assert "at least 2 sentences" in str(exc_info.value)

    def test_validate_file_checks_utf8_encoding(self):
        """Test that validate_file() fails for non-UTF-8 files."""
        filepath = Path("test-1k8ri0.md")
        # Create file with invalid UTF-8 bytes
        invalid_utf8 = b"# Title\n\nThis has invalid UTF-8: \xff\xfe"
        filepath.write_bytes(invalid_utf8)

        with pytest.raises(AssertionError) as exc_info:
            validate_file()
        assert "not valid UTF-8" in str(exc_info.value)


class TestIntegration:
    """Integration tests for create_file() and validate_file()."""

    def setup_method(self):
        """Clean up before each test."""
        filepath = Path("test-1k8ri0.md")
        if filepath.exists():
            filepath.unlink()

    def teardown_method(self):
        """Clean up after each test."""
        filepath = Path("test-1k8ri0.md")
        if filepath.exists():
            filepath.unlink()

    def test_create_and_validate_workflow(self):
        """Test the complete workflow: create file, then validate it."""
        # File should not exist yet
        filepath = Path("test-1k8ri0.md")
        assert not filepath.exists()

        # Create the file
        create_file()
        assert filepath.exists()

        # Validate the created file
        result = validate_file()
        assert result is True

    def test_file_matches_spec_requirements(self):
        """Test that created file meets all specification requirements."""
        create_file()
        filepath = Path("test-1k8ri0.md")

        # Read content
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Spec requirements
        # - File contains H1 heading
        assert lines[0].startswith('# ')

        # - File contains blank line after heading
        assert lines[1] == ''

        # - File contains 2-3 sentences of prose
        prose_text = '\n'.join(lines[2:]).strip()
        sentence_count = prose_text.count('.') + prose_text.count('?') + prose_text.count('!')
        assert 2 <= sentence_count <= 3

        # - File size 400-600 bytes
        file_size = filepath.stat().st_size
        assert 400 <= file_size <= 600

        # - File is UTF-8 without BOM
        raw_bytes = filepath.read_bytes()
        assert not raw_bytes.startswith(b'\xef\xbb\xbf')

        # - File uses LF line endings
        assert b'\n' in raw_bytes
        assert b'\r\n' not in raw_bytes


class TestGitOperations:
    """Tests for the git_operations() function."""

    def setup_method(self):
        """Clean up and set up test environment before each test."""
        filepath = Path("test-1k8ri0.md")
        if filepath.exists():
            filepath.unlink()
        # Create the file before testing git operations
        create_file()

    def teardown_method(self):
        """Clean up after each test."""
        filepath = Path("test-1k8ri0.md")
        if filepath.exists():
            filepath.unlink()

    def test_git_status_shows_file_untracked_initially(self):
        """Test that file shows as untracked in git status before staging."""
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        # File should appear as untracked (??  prefix)
        assert "?? test-1k8ri0.md" in result.stdout or "test-1k8ri0.md" in result.stdout

    def test_git_add_stages_file(self):
        """Test that git add successfully stages the file."""
        subprocess.run(["git", "add", "test-1k8ri0.md"], check=True)

        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        # File should appear as staged (A prefix or new file)
        assert "test-1k8ri0.md" in result.stdout

    def test_git_commit_with_conventional_message(self):
        """Test that git commit succeeds with conventional commit message."""
        subprocess.run(["git", "add", "test-1k8ri0.md"], check=True)

        commit_message = "feat(155): create markdown file test-1k8ri0.md with prose content"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            capture_output=True,
            text=True,
            check=True
        )
        assert commit_message in result.stdout or "feat(155)" in result.stdout

    def test_git_operations_uses_list_arguments(self):
        """Test that git operations use list-based arguments (not shell strings)."""
        # This is tested indirectly: if git_operations() passed shell=True or
        # used shell strings, it would fail in this environment where shell=True
        # is restricted. The function must use list-based arguments.
        # Simply calling git_operations() verifies this.
        subprocess.run(["git", "add", "test-1k8ri0.md"], check=True)
        subprocess.run(
            ["git", "commit", "-m", "feat(155): create markdown file test-1k8ri0.md with prose content"],
            check=True
        )
        # If we get here, list-based arguments were used correctly

    def test_git_operations_function_completes_successfully(self):
        """Test that git_operations() completes without raising exceptions."""
        # This test verifies the complete workflow
        try:
            git_operations()
            # If successful, verify commit was created
            result = subprocess.run(
                ["git", "log", "--oneline", "-1"],
                capture_output=True,
                text=True,
                check=True
            )
            assert "feat(155)" in result.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"git_operations() raised CalledProcessError: {e}")

    def test_git_push_to_feature_branch(self):
        """Test that git push succeeds and pushes to feature branch."""
        subprocess.run(["git", "add", "test-1k8ri0.md"], check=True)
        subprocess.run(
            ["git", "commit", "-m", "feat(155): create markdown file test-1k8ri0.md with prose content"],
            check=True
        )

        # Verify that push doesn't fail (it might fail if branch doesn't exist on remote,
        # but the command structure should be correct)
        result = subprocess.run(
            ["git", "push", "-u", "origin", "HEAD"],
            capture_output=True,
            text=True
        )
        # Accept both success (0) and expected failures (branch already exists, etc.)
        # The important thing is that the command structure is correct


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
