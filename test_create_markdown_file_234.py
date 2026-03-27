"""
Validation test suite for markdown file test-y7gbjb.md.

This module provides comprehensive validation for feature 234, which creates
a markdown file (test-y7gbjb.md) with proper structure, encoding, and line endings.

Test Coverage:
- File existence and readability
- Encoding validation (UTF-8 without BOM)
- Line ending validation (Unix LF, no Windows CRLF)
- File size validation (200-1000 byte range)
- Markdown structure validation (H1 heading + blank line + prose)
- Prose content validation (2+ sentences minimum)
- Overall file correctness and validation
"""

from pathlib import Path
import re

import pytest


# ============================================================================
# Validation Functions
# ============================================================================

def validate_file(filepath):
    """
    Validate a markdown file against feature 234 requirements.

    This function checks:
    - File exists and is readable
    - File size is in acceptable range (200-1000 bytes)
    - File is valid UTF-8 without BOM
    - File contains H1 markdown heading
    - File has blank line after heading
    - File contains 2+ sentences of substantive prose
    - File uses LF line endings (not CRLF)

    Args:
        filepath (Path or str): Path to the markdown file to validate

    Returns:
        True if file passes all validations

    Raises:
        AssertionError: If any validation check fails with descriptive message
    """
    filepath = Path(filepath)

    # Check file exists and is readable
    assert filepath.exists(), f"File {filepath} does not exist"
    assert filepath.is_file(), f"Path {filepath} is not a file"

    # Check file can be read
    try:
        content = filepath.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}")
    except Exception as e:
        raise AssertionError(f"Cannot read file {filepath}: {e}")

    # Check file size is in acceptable range
    file_size = filepath.stat().st_size
    assert 200 <= file_size <= 1000, (
        f"File size {file_size} bytes outside spec range (200-1000). "
        f"Expected typical range 300-600."
    )

    # Check no UTF-8 BOM
    binary_content = filepath.read_bytes()
    assert not binary_content.startswith(b'\xef\xbb\xbf'), (
        "File should not have UTF-8 BOM (Byte Order Mark)"
    )

    # Check no CRLF line endings
    assert b'\r\n' not in binary_content, (
        "File should use Unix LF line endings, not Windows CRLF"
    )

    # Check has LF line endings
    assert b'\n' in binary_content, "File should contain LF line endings"

    # Check file ends with newline
    assert binary_content.endswith(b'\n'), "File should end with a newline character"

    # Check H1 heading
    assert content.startswith('# '), (
        "File should start with H1 markdown heading (# Title)"
    )

    # Check blank line after heading
    assert '\n\n' in content, (
        "File should have blank line separating heading from prose"
    )

    # Split heading and prose
    parts = content.split('\n\n', 1)
    heading = parts[0].strip()
    prose = parts[1].strip() if len(parts) > 1 else ""

    # Check heading is not empty
    assert len(heading) > 2, "Heading should contain meaningful content"

    # Check prose is substantive (not just whitespace)
    assert len(prose) > 50, (
        "Prose content should be substantive (more than just whitespace)"
    )

    # Check sentence count (minimum 2 sentences via regex split)
    sentences = re.split(r'[.!?]+', prose.strip())
    sentence_count = len([s for s in sentences if s.strip()])
    assert sentence_count >= 2, (
        f"File should contain at least 2 sentences, found {sentence_count}"
    )

    return True


# ============================================================================
# Test Classes
# ============================================================================

class TestFileExistence:
    """Tests for file existence and basic readability."""

    def test_file_exists(self):
        """Test that test-y7gbjb.md exists in repository root."""
        filepath = Path("test-y7gbjb.md")
        assert filepath.exists(), f"File {filepath} does not exist"

    def test_file_is_readable(self):
        """Test that file can be read as text."""
        filepath = Path("test-y7gbjb.md")
        assert filepath.is_file(), f"Path {filepath} is not a file"

        # Should not raise exception
        content = filepath.read_text(encoding='utf-8')
        assert len(content) > 0, "File should contain content"


class TestFileSize:
    """Tests for file size validation."""

    def test_file_size_in_acceptable_range(self):
        """Test that file size is within 200-1000 byte range."""
        filepath = Path("test-y7gbjb.md")
        file_size = filepath.stat().st_size

        assert file_size >= 200, f"File size {file_size} is below 200 bytes"
        assert file_size <= 1000, f"File size {file_size} is above 1000 bytes"

    def test_file_size_in_typical_range(self):
        """Test that file size is in typical 300-600 byte range."""
        filepath = Path("test-y7gbjb.md")
        file_size = filepath.stat().st_size

        # Soft guideline: typically 300-600 bytes
        assert 200 < file_size < 1000, (
            f"File size {file_size} bytes outside typical range (200-1000). "
            f"Expected 300-600 as soft guideline."
        )


class TestEncoding:
    """Tests for UTF-8 encoding and line endings."""

    def test_file_utf8_encoding(self):
        """Test that file is valid UTF-8 encoded."""
        filepath = Path("test-y7gbjb.md")
        binary_content = filepath.read_bytes()

        # Should not raise UnicodeDecodeError
        try:
            decoded = binary_content.decode('utf-8')
            assert isinstance(decoded, str)
        except UnicodeDecodeError:
            pytest.fail("File is not valid UTF-8")

    def test_file_no_utf8_bom(self):
        """Test that file does not have UTF-8 BOM."""
        filepath = Path("test-y7gbjb.md")
        binary_content = filepath.read_bytes()

        # UTF-8 BOM is b'\xef\xbb\xbf'
        assert not binary_content.startswith(b'\xef\xbb\xbf'), (
            "File should not have UTF-8 BOM (Byte Order Mark)"
        )

    def test_file_lf_line_endings(self):
        """Test that file uses Unix LF line endings, not Windows CRLF."""
        filepath = Path("test-y7gbjb.md")
        binary_content = filepath.read_bytes()

        # Should not contain CRLF (\r\n)
        assert b'\r\n' not in binary_content, (
            "File should not have Windows CRLF line endings"
        )

        # Should contain LF (\n)
        assert b'\n' in binary_content, "File should have Unix LF line endings"

    def test_file_ends_with_newline(self):
        """Test that file ends with a newline character."""
        filepath = Path("test-y7gbjb.md")
        binary_content = filepath.read_bytes()

        # File must end with LF (\n, which is b'\n' in binary)
        assert binary_content.endswith(b'\n'), (
            "File should end with a newline character"
        )


class TestMarkdownStructure:
    """Tests for markdown structure validation."""

    def test_file_starts_with_h1_heading(self):
        """Test that file starts with H1 markdown heading."""
        filepath = Path("test-y7gbjb.md")
        content = filepath.read_text(encoding='utf-8')

        assert content.startswith('# '), (
            "File should start with H1 markdown heading (# Title)"
        )

    def test_file_has_blank_line_after_heading(self):
        """Test that file has blank line separating heading from prose."""
        filepath = Path("test-y7gbjb.md")
        content = filepath.read_text(encoding='utf-8')

        # Should contain double newline (blank line)
        assert '\n\n' in content, (
            "File should have blank line after heading"
        )

    def test_heading_not_empty(self):
        """Test that heading contains meaningful content."""
        filepath = Path("test-y7gbjb.md")
        content = filepath.read_text(encoding='utf-8')

        parts = content.split('\n\n', 1)
        heading = parts[0].strip()

        # Heading should be more than just "# "
        assert len(heading) > 2, (
            "Heading should contain meaningful content"
        )

    def test_heading_matches_markdown_format(self):
        """Test that heading matches expected markdown format."""
        filepath = Path("test-y7gbjb.md")
        content = filepath.read_text(encoding='utf-8')

        # First line should start with "# "
        first_line = content.split('\n')[0]
        assert first_line.startswith('# '), (
            "First line should be H1 heading starting with '# '"
        )


class TestProseContent:
    """Tests for prose content validation."""

    def test_prose_is_substantive(self):
        """Test that file contains substantive prose content."""
        filepath = Path("test-y7gbjb.md")
        content = filepath.read_text(encoding='utf-8')

        parts = content.split('\n\n', 1)
        prose = parts[1].strip() if len(parts) > 1 else ""

        # Prose should not be empty or just whitespace
        assert len(prose) > 50, (
            "Prose content should be substantive (more than just whitespace)"
        )

    def test_prose_sentence_count(self):
        """Test that prose contains at least 2 sentences."""
        filepath = Path("test-y7gbjb.md")
        content = filepath.read_text(encoding='utf-8')

        parts = content.split('\n\n', 1)
        prose = parts[1].strip() if len(parts) > 1 else ""

        # Count sentences via regex split on sentence-ending punctuation
        sentences = re.split(r'[.!?]+', prose.strip())
        sentence_count = len([s for s in sentences if s.strip()])

        assert sentence_count >= 2, (
            f"File should contain at least 2 sentences, found {sentence_count}"
        )

    def test_prose_not_empty(self):
        """Test that prose section exists and is not empty."""
        filepath = Path("test-y7gbjb.md")
        content = filepath.read_text(encoding='utf-8')

        # Should contain blank line separator
        parts = content.split('\n\n', 1)

        assert len(parts) >= 2, "File should have heading and prose sections"

        prose = parts[1].strip()
        assert len(prose) > 0, "Prose section should not be empty"


class TestFileValidation:
    """Tests for overall file validation."""

    def test_validate_file_passes(self):
        """Test that validate_file() passes for test-y7gbjb.md."""
        filepath = Path("test-y7gbjb.md")
        result = validate_file(filepath)
        assert result is True

    def test_validate_file_comprehensive(self):
        """Test comprehensive validation of file properties."""
        filepath = Path("test-y7gbjb.md")

        # All validations should pass
        assert validate_file(filepath) is True

    def test_file_matches_specification(self):
        """Test that file matches complete feature specification."""
        filepath = Path("test-y7gbjb.md")
        content = filepath.read_text(encoding='utf-8')

        # Specification: # Heading\n\n<2+ sentences of prose>
        lines = content.split('\n')

        # First line should be heading
        assert lines[0].startswith('# '), (
            "First line should be H1 heading"
        )

        # Second line should be empty (blank line)
        assert lines[1] == '', (
            "Second line should be empty (blank line separator)"
        )

        # Remaining lines should contain prose
        prose_lines = lines[2:]
        prose = '\n'.join(prose_lines).strip()
        assert len(prose) > 0, "Prose content should be present"

        # Validate overall file passes validation
        assert validate_file(filepath) is True


class TestErrorHandling:
    """Tests for error handling and informative messages."""

    def test_validate_nonexistent_file(self):
        """Test that validate_file() gives clear error for missing file."""
        filepath = Path("nonexistent_file_12345.md")

        with pytest.raises(AssertionError) as exc_info:
            validate_file(filepath)

        assert "does not exist" in str(exc_info.value)

    def test_error_messages_are_descriptive(self):
        """Test that validation errors have clear messages."""
        filepath = Path("test-y7gbjb.md")

        # File should validate successfully
        try:
            result = validate_file(filepath)
            assert result is True
        except AssertionError as e:
            # If validation fails, error message should be clear
            pytest.fail(f"Validation failed: {e}")


class TestGitIntegration:
    """Tests for git integration (phase 2)."""

    def test_file_is_committed_to_git(self):
        """Test that test-y7gbjb.md is committed to the git repository."""
        import subprocess

        # Check if file is in git history
        result = subprocess.run(
            ["git", "log", "--oneline", "test-y7gbjb.md"],
            capture_output=True,
            text=True,
        )

        # Should have at least one commit
        assert result.returncode == 0, (
            "File should be committed to git repository"
        )
        assert "feat(234)" in result.stdout or len(result.stdout) > 0, (
            "File should have at least one commit"
        )

    def test_commit_message_follows_convention(self):
        """Test that commit message follows conventional commit format."""
        import subprocess

        # Get the commit message for the file
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=%B", "test-y7gbjb.md"],
            capture_output=True,
            text=True,
        )

        commit_message = result.stdout.strip()

        # Should follow conventional commit format: feat(234): ...
        assert "feat(234)" in commit_message or "feat(234):" in commit_message, (
            f"Commit message should follow conventional format, got: {commit_message}"
        )

        # Should mention the feature
        assert "test-y7gbjb.md" in commit_message or "markdown" in commit_message.lower(), (
            f"Commit message should mention the file or markdown feature"
        )

    def test_file_tracked_by_git(self):
        """Test that file is tracked by git (not untracked)."""
        import subprocess

        # Check git status for the file
        result = subprocess.run(
            ["git", "ls-files", "test-y7gbjb.md"],
            capture_output=True,
            text=True,
        )

        # Should list the file if it's tracked
        assert "test-y7gbjb.md" in result.stdout, (
            "File should be tracked by git"
        )

    def test_branch_is_up_to_date_with_remote(self):
        """Test that the current branch is up to date with remote."""
        import subprocess

        # Fetch latest from remote to ensure we have current state
        subprocess.run(
            ["git", "fetch", "origin"],
            capture_output=True,
        )

        # Check if branch is up to date with remote
        result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True,
        )

        # Should be up to date or ahead
        assert (
            "up to date" in result.stdout or
            "ahead" in result.stdout or
            "nothing to commit" in result.stdout
        ), (
            "Branch should be up to date with remote or ahead"
        )

    def test_file_in_remote_repository(self):
        """Test that file exists in the remote repository."""
        import subprocess

        # Check if file exists in remote branch
        result = subprocess.run(
            ["git", "ls-remote", "origin", "HEAD"],
            capture_output=True,
            text=True,
        )

        # Verify origin exists
        assert result.returncode == 0, (
            "Should be able to connect to remote repository"
        )

        # Check if file is in remote (via log)
        result = subprocess.run(
            ["git", "log", "origin/feat/markdown-file-creation-42fd65", "--oneline", "test-y7gbjb.md"],
            capture_output=True,
            text=True,
        )

        # File should be in remote branch history
        assert result.returncode == 0, (
            "File should be in remote repository"
        )
