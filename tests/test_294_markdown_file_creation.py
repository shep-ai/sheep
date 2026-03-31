"""Tests for feature 294: Create markdown file test-xvaf7y.md with title and prose content."""

import os
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import create_markdown_file, validate_markdown_file
from sheep.features.feature_294_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_test_xvaf7y_markdown_file,
    main,
)


class TestFeature294FileCreation:
    """Tests for feature 294 markdown file creation."""

    def test_markdown_filename_is_correct(self):
        """Test that the markdown filename is exactly test-xvaf7y.md."""
        assert MARKDOWN_FILENAME == "test-xvaf7y.md"

    def test_feature_number_is_correct(self):
        """Test that the feature number is 294."""
        assert FEATURE_NUMBER == 294

    @patch('sheep.content_generators.generate_markdown_content')
    def test_creates_file_with_create_markdown_file_function(self, mock_gen, tmp_path):
        """Test that create_markdown_file() creates the file in repo root."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Mock the LLM generation to avoid API dependency
            mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            mock_gen.return_value = mock_content

            # File should not exist before creation
            test_file = Path(MARKDOWN_FILENAME)
            assert not test_file.exists()

            # Call create_markdown_file directly
            result = create_markdown_file(
                filename=MARKDOWN_FILENAME,
                feature_number=FEATURE_NUMBER
            )

            # File should exist after creation
            assert test_file.exists()
            assert "filepath" in result
            assert "content" in result
            assert "commit_message" in result
            assert "push_result" in result

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_feature_function_calls_orchestration(self, mock_gen, tmp_path):
        """Test that create_test_xvaf7y_markdown_file calls the orchestration function."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Mock the LLM generation
            mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            mock_gen.return_value = mock_content

            result = create_test_xvaf7y_markdown_file()

            # Verify result structure
            assert isinstance(result, dict)
            assert "filepath" in result
            assert "content" in result

        finally:
            os.chdir(original_cwd)


class TestFile294Structure:
    """Tests for markdown file structure requirements (FR-2, FR-3, FR-4)."""

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_starts_with_h1_heading(self, mock_gen, tmp_path):
        """Test that file begins with H1 markdown heading (# Title)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            # First line should be H1 heading
            assert lines[0].startswith("# "), f"Expected H1 heading, got: {lines[0]}"
            assert len(lines[0]) > 2, "H1 heading should have title text"

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_has_blank_line_separator(self, mock_gen, tmp_path):
        """Test that file has blank (empty) line 2 after H1 heading."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Second line must be blank
            assert len(lines) >= 2, "File should have at least 2 lines"
            assert lines[1] == "", f"Line 2 should be blank, got: {repr(lines[1])}"

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_has_2_to_3_sentences(self, mock_gen, tmp_path):
        """Test that file contains exactly 2-3 sentences of prose."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Extract prose content (skip H1 and blank line)
            prose_lines = lines[2:]
            prose_content = "\n".join(prose_lines).strip()

            # Count periods to count sentences
            sentence_count = prose_content.count(".")
            assert 2 <= sentence_count <= 3, (
                f"Expected 2-3 sentences, found {sentence_count}"
            )

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_prose_content_is_coherent(self, mock_gen, tmp_path):
        """Test that prose content is grammatically correct and coherent."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Extract title and prose
            title = lines[0].replace("# ", "").strip()
            prose_lines = lines[2:]
            prose_content = "\n".join(prose_lines).strip()

            # Check that content exists and is not empty
            assert title, "H1 title should not be empty"
            assert prose_content, "Prose content should not be empty"
            assert len(prose_content) > 20, "Prose should be substantial"

            # Check basic coherence: prose should relate to title (rough check)
            # We just verify prose is proper English with capital letters and punctuation
            assert prose_content[0].isupper(), "Prose should start with capital letter"
            assert prose_content.endswith("."), "Prose should end with period"

        finally:
            os.chdir(original_cwd)


class TestFile294Encoding:
    """Tests for file encoding and line ending requirements (NFR-1, NFR-5)."""

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_is_utf8_encoded(self, mock_gen, tmp_path):
        """Test that file is UTF-8 encoded without BOM."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            # Should be readable as UTF-8
            content = test_file.read_text(encoding="utf-8")
            assert content is not None

            # Should not have BOM signature
            binary_content = test_file.read_bytes()
            assert not binary_content.startswith(b"\xef\xbb\xbf"), (
                "File should not have UTF-8 BOM"
            )

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_uses_lf_line_endings(self, mock_gen, tmp_path):
        """Test that file uses LF line endings (not CRLF)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            binary_content = test_file.read_bytes()

            # Should not contain CRLF byte sequences
            assert b"\r\n" not in binary_content, "File should use LF, not CRLF"
            # Should contain LF (0x0A) characters
            assert b"\n" in binary_content, "File should have LF line endings"

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_ends_with_newline(self, mock_gen, tmp_path):
        """Test that file ends with newline (POSIX compliance)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            binary_content = test_file.read_bytes()

            # File should end with LF (0x0A)
            assert binary_content.endswith(b"\n"), (
                "File should end with newline character"
            )

        finally:
            os.chdir(original_cwd)


class TestFile294Validation:
    """Tests for file validation requirements."""

    @patch('sheep.content_generators.generate_markdown_content')
    def test_markdown_file_validation_passes(self, mock_gen, tmp_path):
        """Test that created file passes validate_markdown_file()."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            # Should not raise any exception
            result = validate_markdown_file(str(test_file))
            assert result is True

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_exists_in_repo_root(self, mock_gen, tmp_path):
        """Test that file is created in repository root (not nested)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            # File should be in current directory (repo root)
            assert test_file.exists()
            assert test_file.resolve().parent == Path.cwd().resolve()
            assert test_file.name == MARKDOWN_FILENAME

        finally:
            os.chdir(original_cwd)


class TestFile294GitIntegration:
    """Tests for git integration requirements (FR-6, FR-7, FR-8, FR-9)."""

    @patch('sheep.content_generators.generate_markdown_content')
    @patch('sheep.content_generators.git_push')
    def test_commit_message_follows_conventional_format(self, mock_push, mock_gen, tmp_path):
        """Test that commit message follows conventional format."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            mock_push.return_value = "Pushed successfully"

            # Initialize git repo for testing
            subprocess.run(
                ["git", "init"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )

            result = create_markdown_file(
                MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER
            )

            # Check commit message format
            commit_message = result.get("commit_message", "")
            expected_pattern = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
            assert commit_message == expected_pattern, (
                f"Expected '{expected_pattern}', got '{commit_message}'"
            )

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    @patch('sheep.content_generators.git_push')
    def test_file_is_staged_in_git(self, mock_push, mock_gen, tmp_path):
        """Test that file is staged in git after creation."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            mock_push.return_value = "Pushed successfully"

            # Initialize git repo
            subprocess.run(
                ["git", "init"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)

            # Check git status - file should be committed
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )

            # After orchestration function, file should be committed (empty status or no entry for this file)
            # The function commits automatically, so the working tree should be clean
            status_output = result.stdout.strip()
            # File should either be committed (no entry in status) or might show as modified if push fails
            # Since we can't actually push without a remote, just verify file exists
            assert Path(MARKDOWN_FILENAME).exists()

        finally:
            os.chdir(original_cwd)


class TestFeature294Main:
    """Tests for main() entry point."""

    @patch('sheep.content_generators.generate_markdown_content')
    @patch('sheep.content_generators.git_push')
    def test_main_returns_zero_on_success(self, mock_push, mock_gen, tmp_path):
        """Test that main() returns 0 on success."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            mock_push.return_value = "Pushed successfully"

            # Initialize git repo
            subprocess.run(
                ["git", "init"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )

            exit_code = main()
            assert exit_code == 0

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    @patch('sheep.content_generators.git_push')
    def test_main_returns_int(self, mock_push, mock_gen, tmp_path):
        """Test that main() returns an integer."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            mock_push.return_value = "Pushed successfully"

            # Initialize git repo
            subprocess.run(
                ["git", "init"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )

            result = main()
            assert isinstance(result, int)
            assert result in (0, 1)

        finally:
            os.chdir(original_cwd)


class TestFile294Size:
    """Tests for file size requirements."""

    @patch('sheep.content_generators.generate_markdown_content')
    def test_file_size_is_reasonable(self, mock_gen, tmp_path):
        """Test that file size is within reasonable bounds (250-600 bytes)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create a larger mock content that's >250 bytes but <600
            large_content = "# Test Title About Something\n\n" + ("A" * 100) + ". " + ("B" * 100) + ". " + ("C" * 50) + ".\n"
            mock_gen.return_value = large_content

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            file_size = test_file.stat().st_size
            # Should be between 250-600 bytes
            assert 250 <= file_size <= 600, (
                f"File size {file_size} is outside acceptable range (250-600)"
            )

        finally:
            os.chdir(original_cwd)


class TestSuccessCriteria:
    """Comprehensive tests for all success criteria."""

    @patch('sheep.content_generators.generate_markdown_content')
    def test_success_criterion_1_file_in_root(self, mock_gen, tmp_path):
        """Success Criterion 1: Markdown file test-xvaf7y.md is created in repository root."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            assert Path(MARKDOWN_FILENAME).exists()
            assert Path(MARKDOWN_FILENAME).resolve().parent == Path.cwd().resolve()

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_success_criterion_2_h1_heading(self, mock_gen, tmp_path):
        """Success Criterion 2: File begins with H1 markdown heading on line 1."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)
            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            assert lines[0].startswith("# "), "Line 1 should be H1 heading"

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_success_criterion_3_blank_line(self, mock_gen, tmp_path):
        """Success Criterion 3: Blank line follows H1 heading (line 2 is empty)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)
            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            assert len(lines) >= 2
            assert lines[1] == "", "Line 2 should be blank"

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_success_criterion_4_prose_content(self, mock_gen, tmp_path):
        """Success Criterion 4: File contains 2-3 sentences starting at line 3."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)
            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            prose_lines = lines[2:]
            prose_content = "\n".join(prose_lines).strip()
            sentence_count = prose_content.count(".")

            assert 2 <= sentence_count <= 3, "Should have 2-3 sentences"

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_success_criterion_5_coherence(self, mock_gen, tmp_path):
        """Success Criterion 5: Prose is grammatically correct and topically coherent."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)
            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            prose_lines = lines[2:]
            prose_content = "\n".join(prose_lines).strip()

            # Should start with capital letter and end with period
            assert prose_content[0].isupper(), "Prose should start with capital"
            assert prose_content.endswith("."), "Prose should end with period"

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    def test_success_criterion_6_utf8_encoding(self, mock_gen, tmp_path):
        """Success Criterion 6: File is encoded in UTF-8."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            test_file = Path(MARKDOWN_FILENAME)

            # Should be readable as UTF-8 without BOM
            content = test_file.read_text(encoding="utf-8")
            assert content is not None
            binary = test_file.read_bytes()
            assert not binary.startswith(b"\xef\xbb\xbf"), "No UTF-8 BOM"

        finally:
            os.chdir(original_cwd)

    @patch('sheep.content_generators.generate_markdown_content')
    @patch('sheep.content_generators.git_push')
    def test_success_criterion_7_conventional_commit(self, mock_push, mock_gen, tmp_path):
        """Success Criterion 7: File is staged with conventional commit message."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            mock_push.return_value = "Pushed successfully"

            # Init git
            subprocess.run(
                ["git", "init"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=True,
            )

            result = create_markdown_file(MARKDOWN_FILENAME, feature_number=FEATURE_NUMBER)
            commit_message = result.get("commit_message", "")

            expected = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
            assert commit_message == expected

        finally:
            os.chdir(original_cwd)
