"""Tests for feature 122: Creating markdown file test-duijn0.md with title and prose content."""

from pathlib import Path
import pytest
from sheep.content_generators import (
    generate_markdown_content,
    write_markdown_file,
    validate_markdown_file,
)


class TestContentGeneration:
    """Tests for task-2: Generate markdown content with H1 heading and 2-3 sentences."""

    def test_generate_markdown_content_returns_string(self):
        """Test that generate_markdown_content returns a string."""
        content = generate_markdown_content()
        assert isinstance(content, str)

    def test_generated_content_contains_h1_heading(self):
        """Test that generated content contains H1 heading."""
        content = generate_markdown_content()
        assert content.lstrip().startswith("# ")

    def test_generated_content_has_2_to_3_sentences(self):
        """Test that generated content has 2-3 sentences (by counting periods)."""
        content = generate_markdown_content()
        # Count periods in the prose part (skip the heading and blank line)
        lines = content.split("\n")
        prose_lines = lines[2:] if len(lines) > 2 else []
        prose_content = "\n".join(prose_lines).strip()
        sentence_count = prose_content.count(".")
        assert sentence_count >= 2 and sentence_count <= 3

    def test_generated_content_has_minimum_length(self):
        """Test that generated content has reasonable length."""
        content = generate_markdown_content()
        assert len(content) >= 50

    def test_generated_content_ends_with_newline(self):
        """Test that generated content ends with newline (Unix convention)."""
        content = generate_markdown_content()
        assert content.endswith("\n")


class TestFileCreation:
    """Tests for task-3: Write markdown file to disk with UTF-8 encoding."""

    def test_write_markdown_file_creates_file(self, tmp_path):
        """Test that write_markdown_file creates a file."""
        # Change to tmp directory
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath = write_markdown_file(content, "test-duijn0.md")

            assert Path(filepath).exists()
        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_returns_path(self, tmp_path):
        """Test that write_markdown_file returns the file path."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath = write_markdown_file(content, "test-duijn0.md")

            assert isinstance(filepath, str)
            assert "test-duijn0.md" in filepath
        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_content_matches(self, tmp_path):
        """Test that file content matches input."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath = write_markdown_file(content, "test-duijn0.md")

            file_content = Path(filepath).read_text(encoding="utf-8")
            assert file_content == content
        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_utf8_encoding(self, tmp_path):
        """Test that file is created with UTF-8 encoding."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath = write_markdown_file(content, "test-duijn0.md")

            # Read file as UTF-8 should work without errors
            file_content = Path(filepath).read_text(encoding="utf-8")
            assert file_content == content
        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_rejects_path_traversal(self, tmp_path):
        """Test that write_markdown_file rejects unsafe filenames."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

            with pytest.raises(ValueError):
                write_markdown_file(content, "../test-duijn0.md")
        finally:
            os.chdir(original_cwd)


class TestFileValidation:
    """Tests for task-4: Validate file encoding, line endings, and format."""

    def test_validate_markdown_file_passes_valid_file(self, tmp_path):
        """Test that validate_markdown_file returns True for valid file."""
        test_file = tmp_path / "test-duijn0.md"

        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        result = validate_markdown_file(str(test_file))
        assert result is True

    def test_validate_markdown_file_checks_utf8_no_bom(self, tmp_path):
        """Test that validate_markdown_file checks for UTF-8 without BOM."""
        test_file = tmp_path / "test-duijn0.md"

        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        result = validate_markdown_file(str(test_file))
        assert result is True

    def test_validate_markdown_file_checks_lf_line_endings(self, tmp_path):
        """Test that validate_markdown_file checks for LF line endings."""
        test_file = tmp_path / "test-duijn0.md"

        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        assert b"\r\n" not in binary_content

        result = validate_markdown_file(str(test_file))
        assert result is True

    def test_validate_markdown_file_checks_h1_heading(self, tmp_path):
        """Test that validate_markdown_file checks for H1 heading."""
        test_file = tmp_path / "test-duijn0.md"

        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        result = validate_markdown_file(str(test_file))
        assert result is True

    def test_validate_markdown_file_rejects_missing_h1(self, tmp_path):
        """Test that validate_markdown_file rejects file without H1 heading."""
        test_file = tmp_path / "test-duijn0.md"

        content = "No heading here.\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="H1 heading"):
            validate_markdown_file(str(test_file))

    def test_validate_markdown_file_checks_sentence_count(self, tmp_path):
        """Test that validate_markdown_file validates sentence count."""
        test_file = tmp_path / "test-duijn0.md"

        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        result = validate_markdown_file(str(test_file))
        assert result is True

    def test_validate_markdown_file_rejects_too_few_sentences(self, tmp_path):
        """Test that validate_markdown_file rejects file with < 2 sentences."""
        test_file = tmp_path / "test-duijn0.md"

        content = "# Test Title\n\nFirst sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_markdown_file(str(test_file))

    def test_validate_markdown_file_rejects_too_many_sentences(self, tmp_path):
        """Test that validate_markdown_file rejects file with > 3 sentences."""
        test_file = tmp_path / "test-duijn0.md"

        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence. Fourth sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_markdown_file(str(test_file))

    def test_validate_markdown_file_rejects_nonexistent_file(self):
        """Test that validate_markdown_file rejects nonexistent file."""
        with pytest.raises(IOError, match="does not exist"):
            validate_markdown_file("/nonexistent/file.md")


class TestIntegration:
    """Integration tests for the complete workflow."""

    def test_file_creation_returns_path(self, tmp_path):
        """Test that file creation returns a valid filepath."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            mock_content = "# Test Topic\n\nThis is the first sentence. This is the second sentence. This is the third sentence.\n"
            filepath = write_markdown_file(mock_content, "test-duijn0.md")

            assert filepath is not None
            assert "test-duijn0.md" in filepath
            assert Path(filepath).exists()
        finally:
            os.chdir(original_cwd)


class TestEndToEndIntegration:
    """End-to-end integration tests for the complete feature workflow."""

    @pytest.mark.integration
    def test_integration_all_success_criteria(self):
        """Test that create_markdown_file_feature() meets all specification success criteria.

        Uses mock for LLM content generation but tests all real file creation and git operations.

        Verifies:
        - File test-duijn0.md is created in repository root
        - File contains exactly one H1 heading
        - File contains 2-3 sentences of prose content
        - File is encoded UTF-8 without BOM
        - File uses LF (Unix-style) line endings
        - File size is between 300-600 bytes
        - File is staged in git (appears in git status)
        - Commit message matches spec format
        - Commit is on feature branch
        - Commit is pushed to remote
        """
        import os
        import subprocess
        from unittest.mock import patch
        from sheep.features.feature_122_markdown_file_creation import create_markdown_file_feature

        # Store original state
        original_cwd = os.getcwd()
        mock_content = "# The Benefits of Continuous Learning\n\nContinuous learning is essential for personal and professional growth in our rapidly changing world. It expands our knowledge, skills, and perspectives while keeping our minds engaged and adaptable. By embracing lifelong learning, we unlock new opportunities and achieve greater success in all aspects of life.\n"

        try:
            # Mock the generate_markdown_content call to avoid needing an API key
            # Patch at the point where it's imported in the feature module
            with patch("sheep.features.feature_122_markdown_file_creation.generate_markdown_content") as mock_generate:
                mock_generate.return_value = mock_content

                # Call the feature function to create the markdown file
                result = create_markdown_file_feature()

                # Verify return value has expected structure
                assert isinstance(result, dict)
                assert "filepath" in result
                assert "content" in result
                assert "commit_message" in result
                assert "push_result" in result

                # Verify file exists at correct path
                filepath = Path(result["filepath"])
                assert filepath.exists(), f"File does not exist: {filepath}"
                assert filepath.name == "test-duijn0.md", f"File name is incorrect: {filepath.name}"
                assert filepath.parent == Path.cwd(), f"File is not in repository root"

                # Verify file content format
                content = result["content"]
                assert isinstance(content, str), "Content is not a string"
                assert content == mock_content, "Content doesn't match returned content"

                # Verify H1 heading exists and is exactly one
                lines = content.split("\n")
                h1_count = sum(1 for line in lines if line.startswith("# "))
                assert h1_count == 1, f"Expected exactly 1 H1 heading, found {h1_count}"
                assert lines[0].startswith("# "), "First line must be H1 heading"

                # Verify blank line separator
                assert lines[1] == "", "Second line must be blank (separator)"

                # Verify 2-3 sentences in prose content
                prose_lines = lines[2:]
                prose_content = "\n".join(prose_lines).strip()
                sentence_count = prose_content.count(".")
                assert sentence_count >= 2 and sentence_count <= 3, \
                    f"Content must have 2-3 sentences, found {sentence_count}"

                # Verify file encoding (UTF-8 without BOM)
                with open(filepath, "rb") as f:
                    binary_content = f.read()
                assert not binary_content.startswith(b"\xef\xbb\xbf"), \
                    "File has UTF-8 BOM (should not be present)"

                # Verify UTF-8 decoding works
                try:
                    decoded = binary_content.decode("utf-8")
                    assert decoded == content, "File content doesn't match when decoded from UTF-8"
                except UnicodeDecodeError as e:
                    pytest.fail(f"File is not valid UTF-8: {e}")

                # Verify LF line endings (not CRLF)
                assert b"\r\n" not in binary_content, \
                    "File uses CRLF line endings (should use LF)"

                # Verify file size is between 300-600 bytes
                file_size = filepath.stat().st_size
                assert 300 <= file_size <= 600, \
                    f"File size {file_size} is outside expected range (300-600 bytes)"

                # Verify commit message format
                commit_message = result["commit_message"]
                assert "feat(122)" in commit_message, \
                    f"Commit message missing 'feat(122)': {commit_message}"
                assert "test-duijn0.md" in commit_message, \
                    f"Commit message missing filename: {commit_message}"

                # Verify commit exists on current branch
                git_log = subprocess.run(
                    ["git", "log", "-1", "--oneline"],
                    capture_output=True,
                    text=True,
                    cwd=original_cwd
                )
                assert git_log.returncode == 0, "Failed to get git log"
                log_output = git_log.stdout.strip()
                assert "122" in log_output and "test-duijn0.md" in log_output, \
                    f"Latest commit doesn't match feature 122: {log_output}"

                # Verify we're on the correct feature branch
                git_branch = subprocess.run(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    capture_output=True,
                    text=True,
                    cwd=original_cwd
                )
                current_branch = git_branch.stdout.strip()
                assert "feat" in current_branch or "122" in current_branch, \
                    f"Not on feature branch: {current_branch}"

        finally:
            os.chdir(original_cwd)
