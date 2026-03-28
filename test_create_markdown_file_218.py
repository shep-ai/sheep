#!/usr/bin/env python3
"""
Test suite for feature 218: markdown-file-creation-e92f29
Tests create_file(), validate_file(), and git workflow functions.
"""

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from create_markdown_file_218 import (
    COMMIT_MESSAGE,
    FILENAME,
    PROSE,
    TITLE,
    create_file,
    git_add,
    git_commit,
    git_push,
    validate_file,
)


class TestCreateFile:
    """Test suite for create_file function."""

    def test_create_file_returns_path_on_success(self):
        """Test that create_file returns Path when file is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                result = create_file()
                assert isinstance(result, Path)
                assert result.exists()
            finally:
                os.chdir(old_cwd)

    def test_create_file_returns_none_if_exists(self):
        """Test that create_file returns None if file already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create file first time
                result1 = create_file()
                assert result1 is not None
                # Try to create again
                result2 = create_file()
                assert result2 is None
            finally:
                os.chdir(old_cwd)

    def test_create_file_contains_h1_heading(self):
        """Test that created file contains H1 heading with TITLE."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                content = Path("test-gmvvpm.md").read_text(encoding="utf-8")
                assert content.startswith(f"# {TITLE}\n")
            finally:
                os.chdir(old_cwd)

    def test_create_file_contains_blank_line_after_heading(self):
        """Test that created file has blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                content = Path("test-gmvvpm.md").read_text(encoding="utf-8")
                lines = content.split("\n")
                assert lines[0].startswith("# ")
                assert lines[1] == ""
            finally:
                os.chdir(old_cwd)

    def test_create_file_contains_prose(self):
        """Test that created file contains PROSE content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                content = Path("test-gmvvpm.md").read_text(encoding="utf-8")
                assert PROSE in content
            finally:
                os.chdir(old_cwd)

    def test_create_file_uses_utf8_encoding(self):
        """Test that created file uses UTF-8 encoding without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                binary = Path("test-gmvvpm.md").read_bytes()
                # Should not start with UTF-8 BOM (EF BB BF)
                assert not binary.startswith(b"\xef\xbb\xbf")
                # Should decode as UTF-8
                content = binary.decode("utf-8")
                assert content is not None
            finally:
                os.chdir(old_cwd)

    def test_create_file_uses_lf_line_endings(self):
        """Test that created file uses Unix LF line endings only."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                binary = Path("test-gmvvpm.md").read_bytes()
                # Should not contain CRLF (0x0D 0x0A)
                assert b"\r\n" not in binary
                # Should contain LF (0x0A)
                assert b"\n" in binary
            finally:
                os.chdir(old_cwd)

    def test_create_file_ends_with_newline(self):
        """Test that created file ends with newline character."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                content = Path("test-gmvvpm.md").read_text(encoding="utf-8")
                assert content.endswith("\n")
            finally:
                os.chdir(old_cwd)

    def test_create_file_size_in_range(self):
        """Test that created file size is between 300-600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                file_size = Path("test-gmvvpm.md").stat().st_size
                assert 300 <= file_size <= 600
            finally:
                os.chdir(old_cwd)


class TestValidateFile:
    """Test suite for validate_file function."""

    def test_validate_file_passes_for_valid_file(self):
        """Test that validate_file passes for correctly created file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_file()
                result = validate_file("test-gmvvpm.md")
                assert result is True
            finally:
                os.chdir(old_cwd)

    def test_validate_file_raises_if_file_missing(self):
        """Test that validate_file raises FileNotFoundError if file missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                with pytest.raises(ValueError, match="does not exist"):
                    validate_file("test-gmvvpm.md")
            finally:
                os.chdir(old_cwd)

    def test_validate_file_raises_if_h1_missing(self):
        """Test that validate_file raises if first line is not H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path("test-gmvvpm.md").write_text("No heading\n\nProse here.", encoding="utf-8", newline="\n")
                with pytest.raises(ValueError, match="H1 heading"):
                    validate_file("test-gmvvpm.md")
            finally:
                os.chdir(old_cwd)

    def test_validate_file_raises_if_blank_line_missing(self):
        """Test that validate_file raises if second line is not blank."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path("test-gmvvpm.md").write_text("# Title\nProse here.\n", encoding="utf-8", newline="\n")
                with pytest.raises(ValueError, match="blank"):
                    validate_file("test-gmvvpm.md")
            finally:
                os.chdir(old_cwd)

    def test_validate_file_raises_if_wrong_sentence_count(self):
        """Test that validate_file raises if prose doesn't have 2-3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Only 1 sentence
                Path("test-gmvvpm.md").write_text("# Title\n\nOne sentence.\n", encoding="utf-8", newline="\n")
                with pytest.raises(ValueError, match="2-3 sentences"):
                    validate_file("test-gmvvpm.md")
            finally:
                os.chdir(old_cwd)

    def test_validate_file_raises_if_file_has_bom(self):
        """Test that validate_file raises if file has UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Write file with BOM
                Path("test-gmvvpm.md").write_bytes(
                    b"\xef\xbb\xbf# Title\n\nProse one. Prose two. Prose three.\n"
                )
                with pytest.raises(ValueError, match="BOM"):
                    validate_file("test-gmvvpm.md")
            finally:
                os.chdir(old_cwd)

    def test_validate_file_raises_if_file_has_crlf(self):
        """Test that validate_file raises if file has CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Write file with CRLF
                Path("test-gmvvpm.md").write_bytes(
                    b"# Title\r\n\r\nProse one. Prose two. Prose three.\r\n"
                )
                with pytest.raises(ValueError, match="CRLF"):
                    validate_file("test-gmvvpm.md")
            finally:
                os.chdir(old_cwd)

    def test_validate_file_raises_if_file_size_too_small(self):
        """Test that validate_file raises if file size is below 300 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create file smaller than 300 bytes with 2-3 sentences
                Path("test-gmvvpm.md").write_text("# Title\n\nShort prose. Very short.\n", encoding="utf-8", newline="\n")
                with pytest.raises(ValueError, match="300-600 byte range"):
                    validate_file("test-gmvvpm.md")
            finally:
                os.chdir(old_cwd)

    def test_validate_file_raises_if_file_size_too_large(self):
        """Test that validate_file raises if file size exceeds 600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create file larger than 600 bytes with 3 very long sentences
                long_prose = (
                    "This is an exceptionally long and detailed first sentence that provides an extensive amount of information "
                    "with numerous descriptive elements, elaborate explanations, comprehensive discussions about many different topics, "
                    "and thorough elaborations designed specifically to increase the total word and character count substantially. "
                    "The second sentence continues this pattern by offering substantial additional content with multiple layers of description "
                    "and detailed explanations that cover important concepts, theoretical frameworks, practical applications, and many other relevant details "
                    "that contribute meaningfully to the overall length and depth of the prose content. "
                    "Finally, the third and concluding sentence provides even more detailed information and comprehensive elaboration on the topics previously discussed, "
                    "ensuring that the combined total of all three sentences produces a file that exceeds the 600-byte maximum threshold while maintaining coherent and meaningful prose. "
                )
                Path("test-gmvvpm.md").write_text(
                    f"# Title\n\n{long_prose}\n",
                    encoding="utf-8",
                    newline="\n"
                )
                with pytest.raises(ValueError, match="300-600 byte range"):
                    validate_file("test-gmvvpm.md")
            finally:
                os.chdir(old_cwd)

    def test_validate_file_raises_if_not_utf8(self):
        """Test that validate_file raises if file is not valid UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Write invalid UTF-8 sequence
                Path("test-gmvvpm.md").write_bytes(
                    b"# Title\n\n\xff\xfe Invalid UTF-8.\n"
                )
                with pytest.raises(ValueError, match="not valid UTF-8"):
                    validate_file("test-gmvvpm.md")
            finally:
                os.chdir(old_cwd)


class TestGitWorkflow:
    """Test suite for git workflow functions."""

    @patch("subprocess.run")
    def test_git_add_calls_subprocess_with_correct_args(self, mock_run):
        """Test that git_add calls subprocess.run with correct arguments."""
        git_add()
        mock_run.assert_called_once_with(["git", "add", FILENAME], check=True)

    @patch("subprocess.run")
    def test_git_add_raises_on_git_failure(self, mock_run):
        """Test that git_add raises CalledProcessError if git add fails."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ["git", "add"])
        with pytest.raises(subprocess.CalledProcessError):
            git_add()

    @patch("subprocess.run")
    def test_git_commit_calls_subprocess_with_correct_args(self, mock_run):
        """Test that git_commit calls subprocess.run with correct arguments."""
        git_commit()
        mock_run.assert_called_once_with(
            ["git", "commit", "-m", COMMIT_MESSAGE], check=True
        )

    @patch("subprocess.run")
    def test_git_commit_raises_on_git_failure(self, mock_run):
        """Test that git_commit raises CalledProcessError if git commit fails."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ["git", "commit"])
        with pytest.raises(subprocess.CalledProcessError):
            git_commit()

    @patch("subprocess.run")
    def test_git_push_calls_subprocess_with_correct_args(self, mock_run):
        """Test that git_push calls subprocess.run with correct arguments."""
        git_push()
        mock_run.assert_called_once_with(
            ["git", "push", "-u", "origin", "HEAD"], check=True
        )

    @patch("subprocess.run")
    def test_git_push_raises_on_git_failure(self, mock_run):
        """Test that git_push raises CalledProcessError if git push fails."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ["git", "push"])
        with pytest.raises(subprocess.CalledProcessError):
            git_push()

    @patch("subprocess.run")
    def test_git_add_uses_check_true(self, mock_run):
        """Test that git_add uses check=True parameter."""
        git_add()
        call_args = mock_run.call_args
        assert call_args[1]["check"] is True

    @patch("subprocess.run")
    def test_git_commit_uses_check_true(self, mock_run):
        """Test that git_commit uses check=True parameter."""
        git_commit()
        call_args = mock_run.call_args
        assert call_args[1]["check"] is True

    @patch("subprocess.run")
    def test_git_push_uses_check_true(self, mock_run):
        """Test that git_push uses check=True parameter."""
        git_push()
        call_args = mock_run.call_args
        assert call_args[1]["check"] is True

    @patch("subprocess.run")
    def test_git_add_uses_list_format(self, mock_run):
        """Test that git_add uses list format (not string) for command."""
        git_add()
        cmd = mock_run.call_args[0][0]
        assert isinstance(cmd, list)
        assert cmd == ["git", "add", FILENAME]

    @patch("subprocess.run")
    def test_git_commit_uses_list_format(self, mock_run):
        """Test that git_commit uses list format (not string) for command."""
        git_commit()
        cmd = mock_run.call_args[0][0]
        assert isinstance(cmd, list)
        assert cmd == ["git", "commit", "-m", COMMIT_MESSAGE]

    @patch("subprocess.run")
    def test_git_push_uses_list_format(self, mock_run):
        """Test that git_push uses list format (not string) for command."""
        git_push()
        cmd = mock_run.call_args[0][0]
        assert isinstance(cmd, list)
        assert cmd == ["git", "push", "-u", "origin", "HEAD"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
