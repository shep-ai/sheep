"""Tests for Feature 203: Create markdown file test-saop27.md with title and prose.

This test suite covers:
- Task 4: create_markdown_file() function
- Task 5: Markdown format validator
- Task 6: Encoding validator
- Task 7: Line endings validator
- Task 8: File size validator
- Task 9: Sentence count validator
- Task 10: Comprehensive validation pipeline
"""

import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Import the feature module
from sheep.features.feature_203_markdown_file_creation import (
    BRANCH_NAME,
    COMMIT_MESSAGE,
    FILENAME,
    count_sentences,
    create_markdown_file,
    extract_prose_content,
    git_add_file,
    git_commit,
    git_push,
    validate_encoding,
    validate_file_size,
    validate_line_endings,
    validate_markdown_file,
    validate_markdown_format,
    validate_sentence_count,
    verify_file_exists,
    verify_file_size,
    verify_lf_line_endings,
    verify_prose_content,
    verify_utf8_encoding,
)


class TestTaskFour:
    """Tests for task-4: create_markdown_file() function."""

    def test_create_markdown_file_creates_file(self):
        """Test that create_markdown_file creates a file at specified location."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Test Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value="Sentence one. Sentence two. Sentence three."):
                        path = create_markdown_file("test.md")
                        assert Path("test.md").exists()
                        assert "test.md" in path
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_raises_on_existing_file(self):
        """Test that create_markdown_file raises FileExistsError if file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create a file first
                Path("existing.md").write_text("# Existing\n\nContent.\n")

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Test"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value="Content. More. Third."):
                        with pytest.raises(FileExistsError):
                            create_markdown_file("existing.md")
            finally:
                os.chdir(original_cwd)

    def test_created_file_contains_h1_and_prose(self):
        """Test that created file contains H1 heading and prose separated by blank line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="My Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value="First sentence. Second sentence. Third sentence."):
                        create_markdown_file("test.md")

                        content = Path("test.md").read_text(encoding="utf-8")
                        lines = content.split("\n")

                        assert lines[0] == "# My Title"
                        assert lines[1] == ""  # blank line
                        assert "First sentence. Second sentence. Third sentence." in content
            finally:
                os.chdir(original_cwd)

    def test_created_file_has_utf8_encoding(self):
        """Test that created file uses UTF-8 encoding without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value="First. Second. Third."):
                        create_markdown_file("test.md")

                        binary_content = Path("test.md").read_bytes()
                        assert not binary_content.startswith(b"\xef\xbb\xbf"), "Should not have UTF-8 BOM"

                        # Should be decodable as UTF-8
                        decoded = binary_content.decode("utf-8")
                        assert "# Title" in decoded
            finally:
                os.chdir(original_cwd)

    def test_created_file_has_lf_line_endings(self):
        """Test that created file uses Unix LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value="First. Second. Third."):
                        create_markdown_file("test.md")

                        binary_content = Path("test.md").read_bytes()
                        assert b"\r\n" not in binary_content, "Should not have CRLF"
                        assert b"\n" in binary_content, "Should have LF"
            finally:
                os.chdir(original_cwd)

    def test_created_file_returns_absolute_path(self):
        """Test that create_markdown_file returns absolute path as string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value="First. Second. Third."):
                        result = create_markdown_file("test.md")

                        assert isinstance(result, str)
                        assert result.endswith("test.md")
                        assert Path(result).is_absolute()
            finally:
                os.chdir(original_cwd)


class TestTaskFive:
    """Tests for task-5: Markdown format validator."""

    def test_verify_file_exists_raises_on_missing_file(self):
        """Test that verify_file_exists raises FileNotFoundError if file missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with pytest.raises(FileNotFoundError):
                    verify_file_exists("nonexistent.md")
            finally:
                os.chdir(original_cwd)

    def test_verify_file_exists_succeeds_if_file_exists(self):
        """Test that verify_file_exists succeeds if file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path("test.md").write_text("# Title\n\nContent. More.\n")

                # Should not raise
                verify_file_exists("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_accepts_valid_structure(self):
        """Test that validate_markdown_format accepts valid markdown structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                valid_content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
                Path("test.md").write_text(valid_content, encoding="utf-8")

                # Should not raise
                validate_markdown_format("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_rejects_missing_h1(self):
        """Test that validate_markdown_format rejects content without H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                invalid_content = "No heading here\n\nJust prose. More prose. And more.\n"
                Path("test.md").write_text(invalid_content, encoding="utf-8")

                with pytest.raises(ValueError, match="H1 heading"):
                    validate_markdown_format("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_rejects_missing_blank_line(self):
        """Test that validate_markdown_format rejects missing blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                invalid_content = "# Title\nDirect prose. No blank line. Missing space.\n"
                Path("test.md").write_text(invalid_content, encoding="utf-8")

                with pytest.raises(ValueError, match="blank"):
                    validate_markdown_format("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_rejects_multiple_h1(self):
        """Test that validate_markdown_format rejects multiple H1 headings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                invalid_content = "# First\n\nContent. More. Third.\n\n# Second\n\nMore content.\n"
                Path("test.md").write_text(invalid_content, encoding="utf-8")

                with pytest.raises(ValueError, match="one H1"):
                    validate_markdown_format("test.md")
            finally:
                os.chdir(original_cwd)


class TestTaskSix:
    """Tests for task-6: Encoding validator."""

    def test_validate_encoding_accepts_valid_utf8(self):
        """Test that validate_encoding accepts valid UTF-8 without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Title\n\nContent with special chars: é, ñ, 中文. More. Third.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                # Should not raise
                validate_encoding("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_encoding_rejects_bom(self):
        """Test that validate_encoding rejects UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Write content with BOM
                content = "# Title\n\nContent. More. Third.\n"
                binary_content = b"\xef\xbb\xbf" + content.encode("utf-8")
                Path("test.md").write_bytes(binary_content)

                with pytest.raises(ValueError, match="BOM"):
                    validate_encoding("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_encoding_rejects_invalid_utf8(self):
        """Test that validate_encoding rejects invalid UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Write invalid UTF-8
                Path("test.md").write_bytes(b"\xff\xfe invalid utf8")

                with pytest.raises(ValueError, match="UTF-8"):
                    validate_encoding("test.md")
            finally:
                os.chdir(original_cwd)

    def test_verify_utf8_encoding_wrapper(self):
        """Test that verify_utf8_encoding is a working backward-compatibility wrapper."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Title\n\nFirst. Second. Third.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                # Should work like validate_encoding
                verify_utf8_encoding("test.md")
            finally:
                os.chdir(original_cwd)


class TestTaskSeven:
    """Tests for task-7: Line endings validator."""

    def test_validate_line_endings_accepts_lf_only(self):
        """Test that validate_line_endings accepts Unix LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Write with LF only
                Path("test.md").write_bytes(b"# Title\n\nFirst. Second. Third.\n")

                # Should not raise
                validate_line_endings("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_line_endings_rejects_crlf(self):
        """Test that validate_line_endings rejects CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Write with CRLF
                Path("test.md").write_bytes(b"# Title\r\n\r\nFirst. Second. Third.\r\n")

                with pytest.raises(ValueError, match="CRLF"):
                    validate_line_endings("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_line_endings_rejects_cr(self):
        """Test that validate_line_endings rejects CR line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Write with CR only (old Mac style)
                Path("test.md").write_bytes(b"# Title\r\rFirst. Second. Third.\r")

                with pytest.raises(ValueError, match="CR"):
                    validate_line_endings("test.md")
            finally:
                os.chdir(original_cwd)

    def test_verify_lf_line_endings_wrapper(self):
        """Test that verify_lf_line_endings is a working backward-compatibility wrapper."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                Path("test.md").write_bytes(b"# Title\n\nFirst. Second. Third.\n")

                # Should work like validate_line_endings
                verify_lf_line_endings("test.md")
            finally:
                os.chdir(original_cwd)


class TestTaskEight:
    """Tests for task-8: File size validator."""

    def test_validate_file_size_accepts_in_range(self):
        """Test that validate_file_size accepts files within range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create file in valid range (250-600 bytes)
                content = "# Technology and Innovation\n\n" + "This is an important sentence. " * 10 + "\n"  # ~300+ bytes
                Path("test.md").write_text(content, encoding="utf-8")

                # Verify it's in range before testing
                file_size = Path("test.md").stat().st_size
                assert 250 <= file_size <= 600, f"Test content is {file_size} bytes, outside test range"

                # Should not raise
                validate_file_size("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_rejects_too_small(self):
        """Test that validate_file_size rejects files too small."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create file too small
                Path("test.md").write_text("# T\n\nSmall.\n", encoding="utf-8")

                with pytest.raises(ValueError, match="outside range"):
                    validate_file_size("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_rejects_too_large(self):
        """Test that validate_file_size rejects files too large."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create file too large
                content = "# Title\n\n" + "Word. " * 150 + "\n"  # Approx 1000+ bytes
                Path("test.md").write_text(content, encoding="utf-8")

                with pytest.raises(ValueError, match="outside range"):
                    validate_file_size("test.md")
            finally:
                os.chdir(original_cwd)

    def test_verify_file_size_wrapper(self):
        """Test that verify_file_size is a working backward-compatibility wrapper."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Technology and Innovation\n\n" + "This is an important sentence. " * 10 + "\n"
                Path("test.md").write_text(content, encoding="utf-8")

                # Should work like validate_file_size
                verify_file_size("test.md")
            finally:
                os.chdir(original_cwd)


class TestTaskNine:
    """Tests for task-9: Sentence count validator."""

    def test_extract_prose_content_returns_text_after_blank_line(self):
        """Test that extract_prose_content returns prose after blank line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                prose = extract_prose_content("test.md")
                assert prose == "First sentence. Second sentence. Third sentence."
            finally:
                os.chdir(original_cwd)

    def test_count_sentences_counts_periods(self):
        """Test that count_sentences counts periods correctly."""
        prose = "First sentence. Second sentence. Third sentence."
        assert count_sentences(prose) == 3

        prose = "One. Two."
        assert count_sentences(prose) == 2

        prose = "Just one."
        assert count_sentences(prose) == 1

    def test_validate_sentence_count_accepts_2_to_3(self):
        """Test that validate_sentence_count accepts 2-3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Test with 2 sentences
                content = "# Title\n\nFirst. Second.\n"
                Path("test.md").write_text(content, encoding="utf-8")
                validate_sentence_count("test.md")

                # Test with 3 sentences
                Path("test.md").write_text("# Title\n\nFirst. Second. Third.\n", encoding="utf-8")
                validate_sentence_count("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_rejects_too_few(self):
        """Test that validate_sentence_count rejects sentences < 2."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Title\n\nJust one.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                with pytest.raises(ValueError, match="2-3"):
                    validate_sentence_count("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_rejects_too_many(self):
        """Test that validate_sentence_count rejects sentences > 3."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Title\n\nOne. Two. Three. Four.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                with pytest.raises(ValueError, match="2-3"):
                    validate_sentence_count("test.md")
            finally:
                os.chdir(original_cwd)

    def test_verify_prose_content_wrapper(self):
        """Test that verify_prose_content is a working backward-compatibility wrapper."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Title\n\nFirst. Second. Third.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                # Should work like validate_sentence_count
                verify_prose_content("test.md")
            finally:
                os.chdir(original_cwd)


class TestTaskTen:
    """Tests for task-10: Comprehensive validation pipeline."""

    def test_validate_markdown_file_passes_on_valid_file(self):
        """Test that validate_markdown_file passes on fully valid file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create fully valid file with sufficient content (250-600 bytes)
                # Must have exactly 2-3 sentences and be 250-600 bytes
                # Using padding without periods to reach 250+ bytes while keeping sentence count at 3
                padding = " This is additional filler text to increase the byte count of this file without adding periods to the sentence count" * 2
                content = f"# Technology and Innovation\n\nTechnology shapes modern society in important ways. Progress continues steadily through innovation and development{padding}. The future looks bright.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                # Verify size is in valid range
                file_size = Path("test.md").stat().st_size
                assert 250 <= file_size <= 600, f"Test content is {file_size} bytes, outside valid range"

                # Verify it has 2-3 sentences before testing
                sentences = content.count(".")
                assert 2 <= sentences <= 3, f"Test content has {sentences} sentences, need 2-3"

                # Should not raise
                validate_markdown_file("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_fails_on_missing_file(self):
        """Test that validate_markdown_file fails if file missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with pytest.raises(FileNotFoundError):
                    validate_markdown_file("nonexistent.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_stops_on_first_error(self):
        """Test that validate_markdown_file fails fast on first error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # File with no H1 heading - should fail at format check
                content = "No heading\n\nFirst. Second. Third.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                with pytest.raises(ValueError):
                    validate_markdown_file("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_rejects_invalid_encoding(self):
        """Test that validate_markdown_file rejects invalid UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Valid structure but invalid encoding
                Path("test.md").write_bytes(b"# Title\n\n\xff\xfe invalid\n")

                with pytest.raises(ValueError):
                    validate_markdown_file("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_rejects_crlf_endings(self):
        """Test that validate_markdown_file rejects CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Valid structure but CRLF endings
                Path("test.md").write_bytes(b"# Title\r\n\r\nFirst. Second. Third.\r\n")

                with pytest.raises(ValueError):
                    validate_markdown_file("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_rejects_wrong_size(self):
        """Test that validate_markdown_file rejects files outside size range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Valid structure but too small
                Path("test.md").write_text("# A\n\nSmall.\n", encoding="utf-8")

                with pytest.raises(ValueError):
                    validate_markdown_file("test.md")
            finally:
                os.chdir(original_cwd)


class TestTaskEleven:
    """Tests for task-11: Git integration functions."""

    def test_git_add_file_calls_git_add(self):
        """Test that git_add_file calls git add with correct arguments."""
        with patch("sheep.features.feature_203_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

            git_add_file("test.md")

            # Verify subprocess.run was called with correct git add command
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == ["git", "add", "test.md"]
            assert call_args[1]["check"] is True
            assert call_args[1]["capture_output"] is True
            assert call_args[1]["text"] is True

    def test_git_add_file_raises_on_failure(self):
        """Test that git_add_file raises CalledProcessError on git failure."""
        with patch("sheep.features.feature_203_markdown_file_creation.subprocess.run") as mock_run:
            error = subprocess.CalledProcessError(1, ["git", "add"], stderr="fatal: not a git repository")
            mock_run.side_effect = error

            with pytest.raises(subprocess.CalledProcessError):
                git_add_file("test.md")

    def test_git_commit_calls_git_commit(self):
        """Test that git_commit calls git commit with correct message."""
        with patch("sheep.features.feature_203_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

            test_message = "feat(203): Test commit message"
            git_commit("test.md", test_message)

            # Verify subprocess.run was called with correct git commit command
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == ["git", "commit", "-m", test_message]
            assert call_args[1]["check"] is True
            assert call_args[1]["capture_output"] is True
            assert call_args[1]["text"] is True

    def test_git_commit_uses_default_message(self):
        """Test that git_commit uses COMMIT_MESSAGE constant when not provided."""
        with patch("sheep.features.feature_203_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

            git_commit()

            # Verify subprocess.run was called with default COMMIT_MESSAGE
            call_args = mock_run.call_args
            assert COMMIT_MESSAGE in call_args[0][0]

    def test_git_commit_raises_on_failure(self):
        """Test that git_commit raises CalledProcessError on failure."""
        with patch("sheep.features.feature_203_markdown_file_creation.subprocess.run") as mock_run:
            error = subprocess.CalledProcessError(1, ["git", "commit"], stderr="nothing to commit")
            mock_run.side_effect = error

            with pytest.raises(subprocess.CalledProcessError):
                git_commit()

    def test_git_push_calls_git_push(self):
        """Test that git_push calls git push with correct branch."""
        with patch("sheep.features.feature_203_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

            test_branch = "feat/test-branch"
            git_push(test_branch)

            # Verify subprocess.run was called with correct git push command
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == ["git", "push", "-u", "origin", test_branch]
            assert call_args[1]["check"] is True
            assert call_args[1]["capture_output"] is True
            assert call_args[1]["text"] is True

    def test_git_push_uses_default_branch(self):
        """Test that git_push uses BRANCH_NAME constant when not provided."""
        with patch("sheep.features.feature_203_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

            git_push()

            # Verify subprocess.run was called with default BRANCH_NAME
            call_args = mock_run.call_args
            assert BRANCH_NAME in call_args[0][0]

    def test_git_push_raises_on_failure(self):
        """Test that git_push raises CalledProcessError on failure."""
        with patch("sheep.features.feature_203_markdown_file_creation.subprocess.run") as mock_run:
            error = subprocess.CalledProcessError(1, ["git", "push"], stderr="rejected by remote")
            mock_run.side_effect = error

            with pytest.raises(subprocess.CalledProcessError):
                git_push()

    def test_git_operations_raise_on_failure(self):
        """Test that all git operations properly raise exceptions on failure."""
        with patch("sheep.features.feature_203_markdown_file_creation.subprocess.run") as mock_run:
            error = subprocess.CalledProcessError(1, ["git"], stderr="error message")
            mock_run.side_effect = error

            # Test git_add_file raises
            with pytest.raises(subprocess.CalledProcessError):
                git_add_file("test.md")

            # Test git_commit raises
            with pytest.raises(subprocess.CalledProcessError):
                git_commit()

            # Test git_push raises
            with pytest.raises(subprocess.CalledProcessError):
                git_push()


class TestTaskTwelve:
    """Tests for task-12: main() orchestration function."""

    def test_main_creates_file_validates_and_commits(self):
        """Test that main() coordinates complete workflow: create, validate, git ops."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Use longer prose to meet 250+ byte requirement
                long_prose = "This is the first comprehensive sentence with extensive meaningful content about modern technology and innovation. This is the second sentence that expands further on the topic with additional detailed insights and analysis. This is the third sentence providing final concluding thoughts on the entire subject matter."

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Test Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value=long_prose):
                        with patch("sheep.features.feature_203_markdown_file_creation.subprocess.run") as mock_run:
                            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

                            # Import main here to avoid circular imports
                            from sheep.features.feature_203_markdown_file_creation import main

                            result = main()

                            # Check return value is 0 (success)
                            assert result == 0

                            # Verify file was created
                            assert Path(FILENAME).exists()

                            # Verify git operations were called (3 calls: add, commit, push)
                            assert mock_run.call_count == 3
            finally:
                os.chdir(original_cwd)

    def test_main_handles_validation_errors(self):
        """Test that main() handles validation errors gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Mock generate_prose to return invalid content (no periods)
                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value="No periods at all"):

                        from sheep.features.feature_203_markdown_file_creation import main

                        result = main()

                        # Should return 1 (failure)
                        assert result == 1
            finally:
                os.chdir(original_cwd)

    def test_main_handles_git_errors(self):
        """Test that main() handles git operation failures gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value="First. Second. Third."):
                        with patch("sheep.features.feature_203_markdown_file_creation.subprocess.run") as mock_run:
                            # Simulate git failure
                            error = subprocess.CalledProcessError(1, ["git"], stderr="not a git repo")
                            mock_run.side_effect = error

                            from sheep.features.feature_203_markdown_file_creation import main

                            result = main()

                            # Should return 1 (failure)
                            assert result == 1
            finally:
                os.chdir(original_cwd)

    def test_main_handles_file_exists_error(self):
        """Test that main() handles FileExistsError when file already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create file first
                Path(FILENAME).write_text("# Existing\n\nContent. More. Text.\n")

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value="First. Second. Third."):

                        from sheep.features.feature_203_markdown_file_creation import main

                        result = main()

                        # Should return 1 (failure)
                        assert result == 1
            finally:
                os.chdir(original_cwd)

    def test_main_handles_unexpected_exceptions(self):
        """Test that main() handles unexpected exceptions gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", side_effect=Exception("Unexpected error")):

                    from sheep.features.feature_203_markdown_file_creation import main

                    result = main()

                    # Should return 1 (failure)
                    assert result == 1
            finally:
                os.chdir(original_cwd)


class TestTaskThirteen:
    """Tests for task-13: End-to-end integration test."""

    def test_end_to_end_workflow_creates_valid_file(self):
        """Test complete feature workflow creates valid markdown file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                long_prose = "Technology continues to shape our modern world in profound and meaningful ways every single day. Innovation drives progress forward and creates new exciting opportunities for our entire society. The future remains bright and promising with endless limitless possibilities waiting ahead."

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Test Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value=long_prose):
                        with patch("sheep.features.feature_203_markdown_file_creation.subprocess.run") as mock_run:
                            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

                            from sheep.features.feature_203_markdown_file_creation import main

                            # Execute main workflow
                            result = main()
                            assert result == 0

                            # Verify file exists
                            assert Path(FILENAME).exists()

                            # Verify content structure
                            content = Path(FILENAME).read_text(encoding="utf-8")
                            lines = content.split("\n")
                            assert lines[0] == "# Test Title"
                            assert lines[1] == ""  # blank line
                            assert "Technology continues to shape" in content
            finally:
                os.chdir(original_cwd)

    def test_end_to_end_validates_all_criteria(self):
        """Test end-to-end workflow validates all success criteria."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                long_prose = "Technology shapes our world in many profound and significant ways affecting all humanity. Innovation drives progress forward continuously and creates new opportunities for development. The future is bright with endless potential and possibilities ahead of us."

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Technology Topics"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value=long_prose):
                        with patch("sheep.features.feature_203_markdown_file_creation.subprocess.run") as mock_run:
                            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

                            from sheep.features.feature_203_markdown_file_creation import (
                                main,
                                validate_markdown_file,
                            )

                            # Execute main workflow
                            result = main()
                            assert result == 0

                            # Verify file passes all validation checks
                            # This should not raise any exceptions
                            validate_markdown_file(FILENAME)

                            # Verify file properties
                            content = Path(FILENAME).read_text(encoding="utf-8")
                            binary_content = Path(FILENAME).read_bytes()
                            file_size = Path(FILENAME).stat().st_size

                            # Check encoding (no BOM)
                            assert not binary_content.startswith(b"\xef\xbb\xbf")

                            # Check line endings (LF only)
                            assert b"\r\n" not in binary_content
                            assert b"\n" in binary_content

                            # Check file size (250-600 bytes)
                            assert 250 <= file_size <= 600

                            # Check sentence count (2-3)
                            sentence_count = content.count(".")
                            assert 2 <= sentence_count <= 3

                            # Check markdown format
                            lines = content.split("\n")
                            assert lines[0].startswith("# ")
                            assert lines[1] == ""
            finally:
                os.chdir(original_cwd)

    def test_end_to_end_stages_and_commits(self):
        """Test end-to-end workflow stages and commits file with git."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                long_prose = "This is a comprehensive and detailed analysis of the current technological landscape. Development continues steadily with new features being added regularly. Progress is made every single day through dedicated hard work and innovation."

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Great Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value=long_prose):
                        with patch("sheep.features.feature_203_markdown_file_creation.subprocess.run") as mock_run:
                            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

                            from sheep.features.feature_203_markdown_file_creation import main

                            result = main()
                            assert result == 0

                            # Verify git operations were called in correct order
                            assert mock_run.call_count == 3

                            # Check call sequence: add, commit, push
                            calls = mock_run.call_args_list
                            assert calls[0][0][0] == ["git", "add", FILENAME]
                            assert calls[1][0][0][0:3] == ["git", "commit", "-m"]
                            assert calls[1][0][0][3] == f"feat(203): Create markdown file {FILENAME} with title and prose content"
                            assert calls[2][0][0] == ["git", "push", "-u", "origin", BRANCH_NAME]
            finally:
                os.chdir(original_cwd)
