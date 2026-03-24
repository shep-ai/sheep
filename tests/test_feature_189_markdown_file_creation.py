"""Tests for feature 189: Creating markdown file test-joedur.md with title and prose content."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
import tempfile
import os


class TestFeature189Constants:
    """Tests for task 1: Define file content constants."""

    def test_filename_constant(self):
        """Test that FILENAME constant is correct."""
        from sheep.features.feature_189_markdown_file_creation import FILENAME

        assert FILENAME == "test-joedur.md"

    def test_title_constant_is_non_empty_string(self):
        """Test that TITLE is a non-empty string."""
        from sheep.features.feature_189_markdown_file_creation import TITLE

        assert isinstance(TITLE, str)
        assert len(TITLE) > 0

    def test_prose_constant_contains_2_to_3_sentences(self):
        """Test that PROSE contains exactly 2-3 sentences."""
        from sheep.features.feature_189_markdown_file_creation import PROSE

        # Count sentences by periods
        sentence_count = PROSE.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    def test_prose_is_substantive_not_placeholder(self):
        """Test that PROSE is meaningful content, not placeholder."""
        from sheep.features.feature_189_markdown_file_creation import PROSE

        # Check that content is substantive (contains real words, not lorem ipsum)
        assert len(PROSE) > 100, "Prose should be substantive (>100 chars)"
        assert "lorem" not in PROSE.lower(), "Should not contain lorem ipsum"

    def test_main_function_exists_and_callable(self):
        """Test that main() function is defined and callable."""
        from sheep.features.feature_189_markdown_file_creation import main

        assert callable(main)


class TestFeature189FileExistenceCheck:
    """Tests for task 2: Check file does not already exist."""

    def test_no_error_when_file_does_not_exist(self):
        """Test no error raised when file doesn't exist."""
        from sheep.features.feature_189_markdown_file_creation import (
            check_file_does_not_exist,
            FILENAME,
        )

        # Ensure file doesn't exist
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

        # Should not raise
        check_file_does_not_exist()

    def test_raises_value_error_when_file_exists(self):
        """Test ValueError raised when file already exists."""
        from sheep.features.feature_189_markdown_file_creation import (
            check_file_does_not_exist,
            FILENAME,
        )

        # Create the file
        Path(FILENAME).write_text("test content")

        try:
            with pytest.raises(ValueError, match="already exists"):
                check_file_does_not_exist()
        finally:
            # Cleanup
            if Path(FILENAME).exists():
                Path(FILENAME).unlink()

    def test_error_message_is_specific(self):
        """Test that error message is clear and specific."""
        from sheep.features.feature_189_markdown_file_creation import (
            check_file_does_not_exist,
            FILENAME,
        )

        Path(FILENAME).write_text("test")

        try:
            with pytest.raises(ValueError) as exc_info:
                check_file_does_not_exist()

            error_msg = str(exc_info.value)
            assert FILENAME in error_msg
            assert "already exists" in error_msg.lower()
        finally:
            if Path(FILENAME).exists():
                Path(FILENAME).unlink()


class TestFeature189FileCreation:
    """Tests for task 3: Create markdown file with proper encoding and line endings."""

    def test_file_is_created(self):
        """Test that file is created successfully."""
        from sheep.features.feature_189_markdown_file_creation import (
            create_markdown_file,
            FILENAME,
        )

        # Cleanup first
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

        try:
            filepath = create_markdown_file()
            assert Path(FILENAME).exists(), f"File {FILENAME} was not created"
            assert filepath is not None
        finally:
            if Path(FILENAME).exists():
                Path(FILENAME).unlink()

    def test_file_content_structure(self):
        """Test that file content has correct structure."""
        from sheep.features.feature_189_markdown_file_creation import (
            create_markdown_file,
            FILENAME,
            TITLE,
            PROSE,
        )

        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

        try:
            create_markdown_file()
            content = Path(FILENAME).read_text(encoding="utf-8")

            # Check structure: H1 + blank line + prose + trailing newline
            lines = content.split("\n")
            assert lines[0] == f"# {TITLE}", "First line should be H1 heading"
            assert lines[1] == "", "Second line should be blank"
            assert PROSE in content, "Prose should be in content"
            assert content.endswith("\n"), "Should end with newline"
        finally:
            if Path(FILENAME).exists():
                Path(FILENAME).unlink()

    def test_file_is_readable_utf8(self):
        """Test that file is readable as UTF-8."""
        from sheep.features.feature_189_markdown_file_creation import (
            create_markdown_file,
            FILENAME,
        )

        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

        try:
            create_markdown_file()
            # Should not raise UnicodeDecodeError
            content = Path(FILENAME).read_text(encoding="utf-8")
            assert isinstance(content, str)
            assert len(content) > 0
        finally:
            if Path(FILENAME).exists():
                Path(FILENAME).unlink()

    def test_file_has_unix_lf_line_endings(self):
        """Test that file uses Unix LF line endings, not CRLF."""
        from sheep.features.feature_189_markdown_file_creation import (
            create_markdown_file,
            FILENAME,
        )

        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

        try:
            create_markdown_file()
            binary_content = Path(FILENAME).read_bytes()
            # Should not contain CRLF
            assert b"\r\n" not in binary_content, "File should use LF, not CRLF"
            # Should contain LF
            assert b"\n" in binary_content, "File should use LF line endings"
        finally:
            if Path(FILENAME).exists():
                Path(FILENAME).unlink()


class TestFeature189EncodingValidation:
    """Tests for task 4: Validate file encoding (UTF-8 without BOM)."""

    def test_valid_utf8_passes(self):
        """Test that valid UTF-8 file passes validation."""
        from sheep.features.feature_189_markdown_file_creation import validate_encoding

        Path("test_file.md").write_text("# Test\n\nContent.", encoding="utf-8")

        try:
            # Should not raise
            validate_encoding("test_file.md")
        finally:
            Path("test_file.md").unlink()

    def test_utf8_with_bom_fails(self):
        """Test that UTF-8 with BOM fails validation."""
        from sheep.features.feature_189_markdown_file_creation import validate_encoding

        # Write file with UTF-8 BOM
        Path("test_file.md").write_bytes(b"\xef\xbb\xbf# Test\n")

        try:
            with pytest.raises(ValueError, match="BOM"):
                validate_encoding("test_file.md")
        finally:
            Path("test_file.md").unlink()

    def test_invalid_utf8_fails(self):
        """Test that non-UTF-8 file fails validation."""
        from sheep.features.feature_189_markdown_file_creation import validate_encoding

        # Write invalid UTF-8 bytes
        Path("test_file.md").write_bytes(b"\x80\x81\x82")

        try:
            with pytest.raises(ValueError, match="UTF-8"):
                validate_encoding("test_file.md")
        finally:
            Path("test_file.md").unlink()


class TestFeature189LineEndingsValidation:
    """Tests for task 5: Validate file line endings (Unix LF only)."""

    def test_unix_lf_passes(self):
        """Test that file with Unix LF passes validation."""
        from sheep.features.feature_189_markdown_file_creation import (
            validate_line_endings,
        )

        Path("test_file.md").write_text("# Test\n\nContent.\n", encoding="utf-8")

        try:
            # Should not raise
            validate_line_endings("test_file.md")
        finally:
            Path("test_file.md").unlink()

    def test_crlf_fails(self):
        """Test that file with CRLF fails validation."""
        from sheep.features.feature_189_markdown_file_creation import (
            validate_line_endings,
        )

        # Write file with CRLF
        Path("test_file.md").write_bytes(b"# Test\r\n\r\nContent.\r\n")

        try:
            with pytest.raises(ValueError, match="LF"):
                validate_line_endings("test_file.md")
        finally:
            Path("test_file.md").unlink()

    def test_mixed_line_endings_fail(self):
        """Test that file with mixed line endings fails validation."""
        from sheep.features.feature_189_markdown_file_creation import (
            validate_line_endings,
        )

        # Write file with mixed line endings
        Path("test_file.md").write_bytes(b"# Test\n\r\nContent.\n")

        try:
            with pytest.raises(ValueError, match="LF"):
                validate_line_endings("test_file.md")
        finally:
            Path("test_file.md").unlink()


class TestFeature189StructureValidation:
    """Tests for task 6: Validate markdown structure, sentence count, and file size."""

    def test_valid_structure_passes(self):
        """Test that valid markdown structure passes validation."""
        from sheep.features.feature_189_markdown_file_creation import (
            validate_structure,
        )

        content = "# Test Title\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua ut enim ad minim veniam quis nostrud exercitation. Ut laborum exercitation dolorem sed eiusmod tempor incididunt, ut dolore magna aliquip exea commodo consequat duis aute irure dolor in reprehenderit in voluptate. Velit esse cillum dolore eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum sit amet consectetur.\n"
        Path("test_file.md").write_text(content, encoding="utf-8")

        try:
            # Should not raise
            validate_structure("test_file.md")
        finally:
            Path("test_file.md").unlink()

    def test_missing_h1_fails(self):
        """Test that missing H1 heading fails validation."""
        from sheep.features.feature_189_markdown_file_creation import (
            validate_structure,
        )

        content = "Some title\n\nContent here. Second sentence. Third.\n"
        Path("test_file.md").write_text(content, encoding="utf-8")

        try:
            with pytest.raises(ValueError, match="H1"):
                validate_structure("test_file.md")
        finally:
            Path("test_file.md").unlink()

    def test_missing_blank_line_fails(self):
        """Test that missing blank line after H1 fails validation."""
        from sheep.features.feature_189_markdown_file_creation import (
            validate_structure,
        )

        content = "# Title\nContent here. Second sentence. Third.\n"
        Path("test_file.md").write_text(content, encoding="utf-8")

        try:
            with pytest.raises(ValueError, match="blank"):
                validate_structure("test_file.md")
        finally:
            Path("test_file.md").unlink()

    def test_wrong_sentence_count_fails(self):
        """Test that wrong sentence count fails validation."""
        from sheep.features.feature_189_markdown_file_creation import (
            validate_structure,
        )

        # Only 1 sentence
        content = "# Title\n\nJust one sentence.\n"
        Path("test_file.md").write_text(content, encoding="utf-8")

        try:
            with pytest.raises(ValueError, match="2-3 sentences"):
                validate_structure("test_file.md")
        finally:
            Path("test_file.md").unlink()

    def test_file_size_too_small_fails(self):
        """Test that file size < 400 bytes fails validation."""
        from sheep.features.feature_189_markdown_file_creation import (
            validate_structure,
        )

        # Create very small file
        content = "# T\n\nA. B.\n"
        Path("test_file.md").write_text(content, encoding="utf-8")

        try:
            with pytest.raises(ValueError, match="400-600 bytes"):
                validate_structure("test_file.md")
        finally:
            Path("test_file.md").unlink()

    def test_file_size_too_large_fails(self):
        """Test that file size > 600 bytes fails validation."""
        from sheep.features.feature_189_markdown_file_creation import (
            validate_structure,
        )

        # Create very large prose to exceed 600 bytes
        prose = "word " * 150  # Large content
        content = f"# Title\n\n{prose}First. Second. Third.\n"
        Path("test_file.md").write_text(content, encoding="utf-8")

        try:
            with pytest.raises(ValueError, match="400-600 bytes"):
                validate_structure("test_file.md")
        finally:
            Path("test_file.md").unlink()

    def test_missing_trailing_newline_fails(self):
        """Test that missing trailing newline fails validation."""
        from sheep.features.feature_189_markdown_file_creation import (
            validate_structure,
        )

        content = "# Title\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua ut enim ad minim veniam quis nostrud exercitation. Ut laborum exercitation dolorem sed eiusmod tempor incididunt, ut dolore magna aliquip exea commodo consequat duis aute irure dolor in reprehenderit in voluptate. Velit esse cillum dolore eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum sit amet consectetur."
        Path("test_file.md").write_bytes(content.encode("utf-8"))

        try:
            with pytest.raises(ValueError, match="trailing newline"):
                validate_structure("test_file.md")
        finally:
            Path("test_file.md").unlink()


class TestFeature189GitOperations:
    """Tests for git operations."""

    @patch("subprocess.run")
    def test_stage_file_calls_git_add(self, mock_run):
        """Test that stage_file calls git add with correct arguments."""
        from sheep.features.feature_189_markdown_file_creation import stage_file

        stage_file("test-joedur.md")

        mock_run.assert_called_once_with(
            ["git", "add", "test-joedur.md"],
            check=True,
            capture_output=True
        )

    @patch("subprocess.run")
    def test_commit_file_calls_git_commit(self, mock_run):
        """Test that commit_file calls git commit with correct message."""
        from sheep.features.feature_189_markdown_file_creation import commit_file

        commit_file("test-joedur.md", "feat(189): test message")

        mock_run.assert_called_once_with(
            ["git", "commit", "-m", "feat(189): test message"],
            check=True,
            capture_output=True
        )

    @patch("subprocess.run")
    def test_push_file_calls_git_push(self, mock_run):
        """Test that push_file calls git push with correct arguments."""
        from sheep.features.feature_189_markdown_file_creation import push_file

        push_file()

        mock_run.assert_called_once_with(
            ["git", "push", "-u", "origin", "HEAD"],
            check=True,
            capture_output=True
        )

    @patch("subprocess.run")
    def test_git_command_failure_raises_error(self, mock_run):
        """Test that git command failures raise CalledProcessError."""
        from sheep.features.feature_189_markdown_file_creation import stage_file

        mock_run.side_effect = subprocess.CalledProcessError(1, "git add")

        with pytest.raises(subprocess.CalledProcessError):
            stage_file("test-joedur.md")
