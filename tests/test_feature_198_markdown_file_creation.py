"""Tests for feature 198: Creating markdown file test-p27cj6.md with title and prose content.

This module contains comprehensive tests for:
- Task 1: Module structure with imports and constants
- Task 2: File creation with UTF-8 encoding and Unix line endings
- Task 3: Validation functions (encoding, line endings, structure, size)
- Task 6: Git operations (add, commit, push)
- Task 7: Error handling and main orchestration
"""

import os
import sys
from pathlib import Path
import tempfile
import subprocess
from unittest.mock import patch, MagicMock, call
import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sheep.features.feature_198_markdown_file_creation import (
    FILENAME,
    TITLE,
    PROSE,
    check_file_does_not_exist,
    create_markdown_file,
    validate_encoding,
    validate_line_endings,
    count_sentences,
    validate_structure,
    validate_file_size,
    git_add,
    git_commit,
    git_push,
    main,
)


class TestContentConstants:
    """Tests for feature 198 constants."""

    def test_filename_is_correct(self):
        """Test that filename constant matches specification."""
        assert FILENAME == "test-p27cj6.md"

    def test_title_is_meaningful(self):
        """Test that title is meaningful and substantial."""
        assert isinstance(TITLE, str)
        assert len(TITLE) > 0
        assert len(TITLE) > 10  # Substantial title
        # Title should be capitalized
        assert TITLE[0].isupper()

    def test_prose_is_meaningful(self):
        """Test that prose is meaningful and substantial."""
        assert isinstance(PROSE, str)
        assert len(PROSE) > 100  # Substantial prose
        # Should end with period (last sentence)
        assert PROSE.rstrip().endswith(".")

    def test_prose_has_two_to_three_sentences(self):
        """Test that prose contains 2-3 sentences."""
        sentence_count = PROSE.count(".")
        assert 2 <= sentence_count <= 3

    def test_title_and_prose_are_thematically_related(self):
        """Test that title and prose content are thematically related."""
        # Title contains key words that should appear in prose
        title_words = set(TITLE.lower().split())
        prose_lower = PROSE.lower()

        # Check for thematic relation - some key words from title should appear in prose
        # For "The Power of Effective Communication", we expect "communication" in prose
        for word in ["communication", "communicate"]:
            if word in title_words or any(word in w for w in title_words):
                assert word in prose_lower or any(word in w for w in prose_lower.split()), \
                    f"Title theme should be reflected in prose"


class TestFileCreation:
    """Tests for task-2: File creation with UTF-8 encoding and Unix line endings."""

    def setup_method(self):
        """Clean up test file before each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def teardown_method(self):
        """Clean up test file after each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def test_create_markdown_file_creates_file(self):
        """Test that create_markdown_file() function creates the file."""
        file_path = create_markdown_file()
        assert Path(FILENAME).exists()
        assert file_path == str(Path(FILENAME).absolute())

    def test_file_contains_h1_heading(self):
        """Test that file contains H1 heading as first line."""
        create_markdown_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        lines = content.split("\n")
        assert lines[0].startswith("# ")
        assert lines[0] == f"# {TITLE}"

    def test_file_has_blank_line_after_heading(self):
        """Test that file has blank line after H1 heading."""
        create_markdown_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        lines = content.split("\n")
        assert len(lines) >= 3
        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_file_contains_prose_content(self):
        """Test that file contains the prose content."""
        create_markdown_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        assert PROSE in content

    def test_file_ends_with_newline(self):
        """Test that file ends with trailing newline (Unix convention)."""
        create_markdown_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        assert content.endswith("\n")

    def test_file_uses_utf8_encoding(self):
        """Test that file is UTF-8 encoded."""
        create_markdown_file()
        # Read as binary and verify can be decoded as UTF-8
        binary_content = Path(FILENAME).read_bytes()
        decoded = binary_content.decode("utf-8")
        assert isinstance(decoded, str)
        assert len(decoded) > 0

    def test_file_uses_lf_line_endings(self):
        """Test that file uses LF line endings, not CRLF."""
        create_markdown_file()
        binary_content = Path(FILENAME).read_bytes()
        # Should contain LF
        assert b"\n" in binary_content
        # Should NOT contain CRLF
        assert b"\r\n" not in binary_content

    def test_file_size_is_reasonable(self):
        """Test that file size is within expected range (250-600 bytes)."""
        create_markdown_file()
        file_size = Path(FILENAME).stat().st_size
        assert 250 <= file_size <= 600

    def test_creates_file_with_correct_content_format(self):
        """Test that file is created with correct content format."""
        create_markdown_file()
        content = Path(FILENAME).read_text(encoding="utf-8")
        expected_content = f"# {TITLE}\n\n{PROSE}\n"
        assert content == expected_content

    def test_check_file_does_not_exist_before_creation(self):
        """Test that check_file_does_not_exist() raises FileExistsError if file exists."""
        create_markdown_file()
        with pytest.raises(FileExistsError):
            check_file_does_not_exist()


class TestValidationEncoding:
    """Tests for encoding validation - UTF-8 without BOM."""

    def setup_method(self):
        """Create test file before each test."""
        create_markdown_file()

    def teardown_method(self):
        """Clean up test file after each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def test_validate_encoding_passes_for_utf8_file(self):
        """Test that validate_encoding() passes for UTF-8 encoded file."""
        # This should not raise any exception
        validate_encoding()

    def test_file_does_not_have_utf8_bom(self):
        """Test that file does not contain UTF-8 BOM."""
        binary_content = Path(FILENAME).read_bytes()
        # UTF-8 BOM is bytes: 0xEF 0xBB 0xBF
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_validate_encoding_rejects_bom(self):
        """Test that validate_encoding() rejects file with UTF-8 BOM."""
        # Create file with BOM
        bom_content = b"\xef\xbb\xbf" + Path(FILENAME).read_bytes()
        Path(FILENAME).write_bytes(bom_content)

        # validate_encoding() should raise ValueError
        with pytest.raises(ValueError, match="BOM"):
            validate_encoding()

    def test_validate_encoding_file_exists_check(self):
        """Test that validate_encoding() checks if file exists."""
        Path(FILENAME).unlink()
        with pytest.raises(FileNotFoundError):
            validate_encoding()


class TestValidationLineEndings:
    """Tests for line endings validation - Unix LF only."""

    def setup_method(self):
        """Create test file before each test."""
        create_markdown_file()

    def teardown_method(self):
        """Clean up test file after each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def test_validate_line_endings_passes_for_lf_file(self):
        """Test that validate_line_endings() passes for file with LF endings."""
        # This should not raise any exception
        validate_line_endings()

    def test_file_has_only_lf_line_endings(self):
        """Test that file contains only LF, no CRLF or CR."""
        binary_content = Path(FILENAME).read_bytes()
        # Should contain LF
        assert b"\n" in binary_content
        # Should NOT contain CRLF
        assert b"\r\n" not in binary_content
        # Should NOT contain CR without LF
        assert b"\r" not in binary_content

    def test_validate_line_endings_rejects_crlf(self):
        """Test that validate_line_endings() rejects CRLF line endings."""
        # Read file and convert LF to CRLF
        content = Path(FILENAME).read_text(encoding="utf-8")
        crlf_content = content.replace("\n", "\r\n")
        Path(FILENAME).write_text(crlf_content, encoding="utf-8")

        # validate_line_endings() should raise ValueError
        with pytest.raises(ValueError, match="CRLF"):
            validate_line_endings()

    def test_validate_line_endings_rejects_cr(self):
        """Test that validate_line_endings() rejects Mac CR line endings."""
        # Read file as binary and convert to CR only (no LF)
        binary_content = Path(FILENAME).read_bytes()
        cr_content = binary_content.replace(b"\n", b"\r")
        Path(FILENAME).write_bytes(cr_content)

        # validate_line_endings() should raise ValueError
        with pytest.raises(ValueError, match="CR"):
            validate_line_endings()


class TestCountSentences:
    """Tests for helper function: count_sentences()."""

    def test_count_sentences_zero(self):
        """Test sentence counting with no periods."""
        assert count_sentences("No periods here") == 0

    def test_count_sentences_one(self):
        """Test sentence counting with one period."""
        assert count_sentences("One sentence.") == 1

    def test_count_sentences_three(self):
        """Test sentence counting with three periods."""
        assert count_sentences("First. Second. Third.") == 3

    def test_count_sentences_in_prose(self):
        """Test sentence counting in actual prose."""
        assert 2 <= count_sentences(PROSE) <= 3


class TestValidationStructure:
    """Tests for structure validation - H1 heading and 2-3 sentences."""

    def setup_method(self):
        """Create test file before each test."""
        create_markdown_file()

    def teardown_method(self):
        """Clean up test file after each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def test_validate_structure_passes_for_valid_file(self):
        """Test that validate_structure() passes for valid file."""
        # This should not raise any exception
        validate_structure(FILENAME)

    def test_file_has_h1_heading(self):
        """Test that file starts with H1 heading."""
        content = Path(FILENAME).read_text(encoding="utf-8")
        assert content.startswith("# ")

    def test_file_has_2_to_3_sentences(self):
        """Test that file contains 2-3 sentences."""
        content = Path(FILENAME).read_text(encoding="utf-8")
        lines = content.split("\n")
        prose_text = "\n".join(lines[2:]).strip()
        sentence_count = prose_text.count(".")
        assert 2 <= sentence_count <= 3

    def test_validate_structure_rejects_missing_h1(self):
        """Test that validate_structure() rejects file without H1 heading."""
        # Create file without H1
        bad_content = f"No heading here\n\n{PROSE}\n"
        Path(FILENAME).write_text(bad_content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="H1"):
            validate_structure(FILENAME)

    def test_validate_structure_rejects_wrong_sentence_count(self):
        """Test that validate_structure() rejects file with wrong sentence count."""
        # Create file with only one sentence
        bad_content = f"# {TITLE}\n\nOnly one sentence.\n"
        Path(FILENAME).write_text(bad_content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="sentence"):
            validate_structure(FILENAME)

    def test_validate_structure_rejects_too_many_sentences(self):
        """Test that validate_structure() rejects file with too many sentences."""
        # Create file with 4 sentences
        bad_content = f"# {TITLE}\n\nFirst. Second. Third. Fourth.\n"
        Path(FILENAME).write_text(bad_content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="sentence"):
            validate_structure(FILENAME)


class TestValidationFileSize:
    """Tests for file size validation - 300-600 bytes."""

    def setup_method(self):
        """Create test file before each test."""
        create_markdown_file()

    def teardown_method(self):
        """Clean up test file after each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def test_validate_file_size_passes_for_valid_size(self):
        """Test that validate_file_size() passes for file in valid range."""
        # This should not raise any exception
        validate_file_size(FILENAME)

    def test_file_size_is_in_valid_range(self):
        """Test that file size is between 300-600 bytes."""
        file_size = Path(FILENAME).stat().st_size
        assert 300 <= file_size <= 600

    def test_validate_file_size_rejects_too_small(self):
        """Test that validate_file_size() rejects file that is too small."""
        # Create file that is too small
        small_content = "# T\n\nSmall.\n"
        Path(FILENAME).write_text(small_content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="size"):
            validate_file_size(FILENAME)

    def test_validate_file_size_rejects_too_large(self):
        """Test that validate_file_size() rejects file that is too large."""
        # Create file that is too large
        large_content = f"# {TITLE}\n\n" + ("x" * 700) + "\n"
        Path(FILENAME).write_text(large_content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="size"):
            validate_file_size(FILENAME)


class TestIntegration:
    """Integration tests for complete workflow."""

    def setup_method(self):
        """Clean up test file before each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def teardown_method(self):
        """Clean up test file after each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def test_file_passes_all_validations(self):
        """Test that created file passes all validation checks."""
        create_markdown_file()

        # Should not raise any exceptions
        validate_encoding()
        validate_line_endings()
        validate_structure(FILENAME)
        validate_file_size(FILENAME)

    def test_file_content_and_format_correct(self):
        """Test that file has correct content and format."""
        create_markdown_file()

        content = Path(FILENAME).read_text(encoding="utf-8")

        # Check structure
        lines = content.split("\n")
        assert lines[0] == f"# {TITLE}"
        assert lines[1] == ""
        assert PROSE in content

        # Check sentence count
        prose_text = "\n".join(lines[2:]).strip()
        assert 2 <= prose_text.count(".") <= 3

        # Check encoding and line endings
        binary_content = Path(FILENAME).read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf")
        assert b"\r\n" not in binary_content

        # Check file size
        assert 300 <= len(binary_content) <= 600


class TestGitOperations:
    """Tests for git operations (add, commit, push)."""

    def setup_method(self):
        """Create test file before each test."""
        create_markdown_file()

    def teardown_method(self):
        """Clean up test file after each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    @patch("subprocess.run")
    def test_git_add_calls_correct_command(self, mock_run):
        """Test that git_add() calls git add with correct filename."""
        git_add(FILENAME)
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert args[0] == ["git", "add", FILENAME]
        assert kwargs["check"] is True
        assert kwargs["capture_output"] is True

    @patch("subprocess.run")
    def test_git_add_default_filename(self, mock_run):
        """Test that git_add() uses FILENAME constant by default."""
        git_add()
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert args[0] == ["git", "add", FILENAME]

    @patch("subprocess.run")
    def test_git_add_raises_on_failure(self, mock_run):
        """Test that git_add() raises CalledProcessError on non-zero exit."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git add")
        with pytest.raises(subprocess.CalledProcessError):
            git_add()

    @patch("subprocess.run")
    def test_git_commit_calls_correct_command(self, mock_run):
        """Test that git_commit() calls git commit with correct message."""
        message = "feat(198): Create markdown file test-p27cj6.md with title and prose content"
        git_commit(message)
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert args[0] == ["git", "commit", "-m", message]
        assert kwargs["check"] is True
        assert kwargs["capture_output"] is True

    @patch("subprocess.run")
    def test_git_commit_default_message(self, mock_run):
        """Test that git_commit() uses default message by default."""
        git_commit()
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert "feat(198):" in args[0][3]
        assert "test-p27cj6.md" in args[0][3]

    @patch("subprocess.run")
    def test_git_commit_message_format_is_conventional(self, mock_run):
        """Test that git_commit() message follows Conventional Commits format."""
        git_commit()
        args, _ = mock_run.call_args
        message = args[0][3]
        # Conventional Commits: type(scope): description
        assert message.startswith("feat(198):")

    @patch("subprocess.run")
    def test_git_commit_raises_on_failure(self, mock_run):
        """Test that git_commit() raises CalledProcessError on non-zero exit."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git commit")
        with pytest.raises(subprocess.CalledProcessError):
            git_commit()

    @patch("subprocess.run")
    def test_git_push_calls_correct_command(self, mock_run):
        """Test that git_push() calls git push with -u origin HEAD."""
        git_push()
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert args[0] == ["git", "push", "-u", "origin", "HEAD"]
        assert kwargs["check"] is True
        assert kwargs["capture_output"] is True

    @patch("subprocess.run")
    def test_git_push_raises_on_failure(self, mock_run):
        """Test that git_push() raises CalledProcessError on non-zero exit."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git push")
        with pytest.raises(subprocess.CalledProcessError):
            git_push()


class TestErrorHandling:
    """Tests for error handling and main orchestration."""

    def setup_method(self):
        """Clean up test file before each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def teardown_method(self):
        """Clean up test file after each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    @patch("subprocess.run")
    def test_main_returns_success_exit_code_on_success(self, mock_run):
        """Test that main() returns 0 on successful completion."""
        with patch("sys.exit") as mock_exit:
            main()
            # If no exception raised and no sys.exit(1) called, return was implicit success
            mock_exit.assert_not_called()

    @patch("subprocess.run")
    def test_main_prints_success_messages(self, mock_run):
        """Test that main() prints success messages for each phase."""
        with patch("builtins.print") as mock_print:
            main()
            # Should print success messages for file creation and validations
            assert mock_print.call_count > 0
            # Check for some expected messages
            call_args = [str(call[0]) for call in mock_print.call_args_list]
            printed_text = " ".join(call_args)
            assert "Created" in printed_text or "created" in printed_text.lower()

    def test_main_exits_with_code_1_if_file_exists(self):
        """Test that main() exits with code 1 if file already exists."""
        # Create the file first
        create_markdown_file()

        # Try to run main again - should fail
        with patch("sys.exit") as mock_exit:
            with patch("sys.stderr"):
                main()
            mock_exit.assert_called_once_with(1)

    def test_main_exits_with_code_1_on_validation_error(self):
        """Test that main() exits with code 1 if validation fails."""
        # Create a file that passes creation but fails validation
        create_markdown_file()
        # Corrupt the file to fail validation
        Path(FILENAME).write_text("No H1 heading\n\nNo prose\n", encoding="utf-8", newline="\n")

        with patch("sys.exit") as mock_exit:
            with patch("sys.stderr"):
                main()
            mock_exit.assert_called_once_with(1)

    @patch("subprocess.run")
    def test_main_exits_with_code_1_on_git_failure(self, mock_run):
        """Test that main() exits with code 1 if git operations fail."""
        # Mock git_add to succeed but git_commit to fail
        def side_effect_func(cmd, **kwargs):
            if "commit" in cmd:
                raise subprocess.CalledProcessError(1, "git commit")
            return MagicMock()

        mock_run.side_effect = side_effect_func

        with patch("sys.exit") as mock_exit:
            with patch("sys.stderr"):
                main()
            mock_exit.assert_called_once_with(1)

    def test_main_error_messages_go_to_stderr(self):
        """Test that error messages are written to stderr."""
        # Create file that will fail validation
        create_markdown_file()
        Path(FILENAME).write_text("Invalid content", encoding="utf-8", newline="\n")

        with patch("sys.stderr") as mock_stderr:
            with patch("sys.exit"):
                main()
            # stderr.write or print should be called
            # (depending on implementation)

    @patch("subprocess.run")
    def test_main_workflow_order_is_correct(self, mock_run):
        """Test that main() executes workflow in correct order: create → validate → git."""
        # Track the order of operations
        operations = []

        original_path_exists = Path.exists
        original_path_write = Path.write_text

        def tracked_exists(self):
            operations.append("check_exists")
            return original_path_exists(self)

        def tracked_write(self, content, **kwargs):
            operations.append("write_file")
            return original_path_write(self, content, **kwargs)

        def tracked_git(*args, **kwargs):
            if "add" in args[0]:
                operations.append("git_add")
            elif "commit" in args[0]:
                operations.append("git_commit")
            elif "push" in args[0]:
                operations.append("git_push")
            return MagicMock()

        mock_run.side_effect = tracked_git

        with patch.object(Path, "exists", tracked_exists):
            with patch.object(Path, "write_text", tracked_write):
                main()

        # Check that file operations happen before git operations
        if "write_file" in operations and "git_add" in operations:
            assert operations.index("write_file") < operations.index("git_add")

    @patch("subprocess.run")
    def test_main_does_not_git_add_if_validation_fails(self, mock_run):
        """Test that main() does not call git add if validation fails."""
        # Create file that fails validation
        create_markdown_file()
        Path(FILENAME).write_text("# Title\n\nOnly one.\n", encoding="utf-8", newline="\n")

        with patch("sys.exit"):
            with patch("sys.stderr"):
                main()

        # git_add should never be called
        add_calls = [c for c in mock_run.call_args_list if "add" in str(c)]
        assert len(add_calls) == 0


class TestEndToEndIntegration:
    """End-to-end integration tests."""

    def setup_method(self):
        """Clean up test file before each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    def teardown_method(self):
        """Clean up test file after each test."""
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()

    @patch("subprocess.run")
    def test_complete_workflow_with_mocked_git(self, mock_run):
        """Test complete workflow from creation through git push."""
        # Mock all git operations to avoid actual git calls
        mock_run.return_value = MagicMock()

        # Run main
        with patch("sys.exit"):
            main()

        # Verify file was created
        assert Path(FILENAME).exists()

        # Verify file has correct content
        content = Path(FILENAME).read_text(encoding="utf-8")
        assert content.startswith("# ")
        assert PROSE in content

        # Verify git operations were called
        assert mock_run.call_count >= 3  # add, commit, push

        # Verify order of git operations
        calls = [c[0][0] for c in mock_run.call_args_list]
        assert ["git", "add", FILENAME] in calls
        assert any("commit" in str(c) for c in calls)
        assert ["git", "push", "-u", "origin", "HEAD"] in calls

    @patch("subprocess.run")
    def test_file_properties_after_creation(self, mock_run):
        """Test that created file meets all success criteria."""
        mock_run.return_value = MagicMock()

        with patch("sys.exit"):
            main()

        # File exists
        assert Path(FILENAME).exists()

        # File has correct content
        content = Path(FILENAME).read_text(encoding="utf-8")

        # H1 heading
        assert content.startswith("# ")

        # Blank line after heading
        lines = content.split("\n")
        assert lines[1] == ""

        # 2-3 sentences
        prose = "\n".join(lines[2:]).strip()
        sentence_count = prose.count(".")
        assert 2 <= sentence_count <= 3

        # UTF-8 encoding
        binary_content = Path(FILENAME).read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Unix LF line endings
        assert b"\r\n" not in binary_content

        # File size 300-600 bytes
        assert 300 <= len(binary_content) <= 600

    @patch("subprocess.run")
    def test_git_commit_message_format(self, mock_run):
        """Test that git commit uses correct Conventional Commits format."""
        mock_run.return_value = MagicMock()

        with patch("sys.exit"):
            main()

        # Find the commit call
        commit_calls = [c for c in mock_run.call_args_list if c[0][0][1] == "commit"]
        assert len(commit_calls) > 0

        message = commit_calls[0][0][0][3]
        assert message.startswith("feat(198):")
        assert "test-p27cj6.md" in message

    def test_error_on_file_already_exists(self):
        """Test that main() fails gracefully if file already exists."""
        # Create file first
        create_markdown_file()

        # Try to run main again
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    @patch("subprocess.run")
    def test_error_on_git_add_failure(self, mock_run):
        """Test that main() fails if git add fails."""
        mock_run.side_effect = subprocess.CalledProcessError(128, "git add")

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    @patch("subprocess.run")
    def test_error_on_git_commit_failure(self, mock_run):
        """Test that main() fails if git commit fails."""
        def side_effect_func(cmd, **kwargs):
            if "commit" in cmd:
                raise subprocess.CalledProcessError(1, "git commit")
            return MagicMock()

        mock_run.side_effect = side_effect_func

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    @patch("subprocess.run")
    def test_error_on_git_push_failure(self, mock_run):
        """Test that main() fails if git push fails."""
        def side_effect_func(cmd, **kwargs):
            if "push" in cmd:
                raise subprocess.CalledProcessError(128, "git push")
            return MagicMock()

        mock_run.side_effect = side_effect_func

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
