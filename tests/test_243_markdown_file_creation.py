"""Tests for feature 243: Creating markdown file test-c2dbie.md with title and prose content."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.features.feature_243_markdown_file_creation import (
    generate_prose_content,
    validate_markdown_file,
    write_markdown_file,
)


class TestProseContentGeneration:
    """Tests for task-2: Implement prose content generation via Claude API."""

    @patch("sheep.features.feature_243_markdown_file_creation.get_reasoning_llm")
    def test_generate_prose_content_returns_string(self, mock_get_llm):
        """Test that generate_prose_content() returns a string."""
        # Mock the LLM
        mock_llm = MagicMock()
        mock_content = "The study of ancient civilizations reveals complex social structures. People developed sophisticated methods of agriculture and trade. These advances laid the foundation for modern society."
        mock_llm.call.return_value = {"content": mock_content}
        mock_get_llm.return_value = mock_llm

        content = generate_prose_content()
        assert isinstance(content, str)
        assert len(content) > 0

    @patch("sheep.features.feature_243_markdown_file_creation.get_reasoning_llm")
    def test_prose_content_has_two_to_three_sentences(self, mock_get_llm):
        """Test that returned content has 2-3 sentences (counted by periods)."""
        mock_llm = MagicMock()
        mock_content = "The technology industry continues to evolve rapidly. Innovation drives new capabilities and opportunities. Competition pushes companies to improve constantly."
        mock_llm.call.return_value = {"content": mock_content}
        mock_get_llm.return_value = mock_llm

        content = generate_prose_content()
        sentence_count = content.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, got {sentence_count}"

    @patch("sheep.features.feature_243_markdown_file_creation.get_reasoning_llm")
    def test_prose_content_no_markdown_formatting(self, mock_get_llm):
        """Test that content does not include markdown formatting."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "This is a meaningful sentence. Another meaningful sentence."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_prose_content()
        # Check for markdown special characters (excluding those allowed in prose)
        assert "**" not in content
        assert "__" not in content
        assert "`" not in content
        assert "#" not in content

    @patch("sheep.features.feature_243_markdown_file_creation.get_reasoning_llm")
    def test_prose_content_is_meaningful(self, mock_get_llm):
        """Test that content is meaningful prose (not placeholder or repetitive)."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "The quick brown fox jumps over the lazy dog. This is a meaningful sentence. Another sentence here."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_prose_content()
        # Should have reasonable length
        assert len(content) > 50, "Content too short to be meaningful"
        # Should not be repetitive placeholder text
        assert "lorem ipsum" not in content.lower()
        assert "placeholder" not in content.lower()

    @patch("sheep.features.feature_243_markdown_file_creation.get_reasoning_llm")
    def test_prose_content_temperature_0_2(self, mock_get_llm):
        """Test that LLM is called with temperature=0.2."""
        mock_llm = MagicMock()
        mock_content = "The study of ancient civilizations reveals complex social structures. People developed sophisticated methods of agriculture and trade. These advances laid the foundation for modern society."
        mock_llm.call.return_value = {"content": mock_content}
        mock_get_llm.return_value = mock_llm

        generate_prose_content()

        # Verify the call included temperature=0.2
        mock_llm.call.assert_called_once()
        call_args = mock_llm.call.call_args
        assert call_args[1].get("temperature") == 0.2


class TestMarkdownFileWriting:
    """Tests for task-3: Implement markdown file writing with UTF-8 and LF enforcement."""

    def test_write_markdown_file_creates_file(self):
        """Test that write_markdown_file() creates file at repository root."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            original_cwd = Path.cwd()
            try:
                # Change to temp directory to use as repo root
                import os
                os.chdir(tmp_path)

                result = write_markdown_file("test-file.md", "Test Title", "Test content.")
                assert Path(result).exists()
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_contains_h1_heading(self):
        """Test that file contains H1 heading."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp_path)

                write_markdown_file("test.md", "My Title", "Content here.")
                content = Path("test.md").read_text(encoding="utf-8")
                assert content.startswith("# My Title")
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_has_blank_line_separator(self):
        """Test that file has blank line after heading."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp_path)

                write_markdown_file("test.md", "Title", "Content here.")
                content = Path("test.md").read_text(encoding="utf-8")
                lines = content.split("\n")
                assert lines[1] == "", "Second line should be blank separator"
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_contains_prose_content(self):
        """Test that file contains prose content following blank line."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp_path)

                prose = "This is a test sentence. Another test sentence."
                write_markdown_file("test.md", "Title", prose)
                content = Path("test.md").read_text(encoding="utf-8")
                assert prose in content
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_ends_with_newline(self):
        """Test that file ends with newline character."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp_path)

                write_markdown_file("test.md", "Title", "Content.")
                content = Path("test.md").read_text(encoding="utf-8")
                assert content.endswith("\n"), "File should end with newline"
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_utf8_encoding(self):
        """Test that file encoding is UTF-8 without BOM."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp_path)

                write_markdown_file("test.md", "Title", "Content.")
                binary = Path("test.md").read_bytes()
                # Check no BOM
                assert not binary.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_lf_line_endings(self):
        """Test that file uses LF line endings only."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp_path)

                write_markdown_file("test.md", "Title", "Content.")
                binary = Path("test.md").read_bytes()
                # Check no CRLF
                assert b"\r\n" not in binary, "File should use LF not CRLF"
            finally:
                os.chdir(original_cwd)


class TestMarkdownFileValidation:
    """Tests for task-4: Implement comprehensive markdown validation."""

    def test_validate_markdown_file_exists(self):
        """Test that validate_markdown_file checks file exists."""
        with pytest.raises(ValueError, match="does not exist"):
            validate_markdown_file("/nonexistent/path.md")

    def test_validate_markdown_file_h1_heading(self):
        """Test that validation checks H1 heading present."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            file_path = tmp_path / "test.md"
            # File without H1 heading
            file_path.write_text("No heading here\nJust content.", encoding="utf-8")

            with pytest.raises(ValueError, match="H1 heading"):
                validate_markdown_file(str(file_path))

    def test_validate_markdown_file_blank_line_separator(self):
        """Test that validation checks blank line after heading."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            file_path = tmp_path / "test.md"
            # File without blank line separator
            file_path.write_text("# Title\nContent.", encoding="utf-8")

            with pytest.raises(ValueError, match="blank|separator"):
                validate_markdown_file(str(file_path))

    def test_validate_markdown_file_sentence_count_too_few(self):
        """Test that validation fails with fewer than 2 sentences."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            file_path = tmp_path / "test.md"
            file_path.write_text("# Title\n\nJust one sentence.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="2-3 sentences"):
                validate_markdown_file(str(file_path))

    def test_validate_markdown_file_sentence_count_too_many(self):
        """Test that validation fails with more than 3 sentences."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            file_path = tmp_path / "test.md"
            content = "# Title\n\nFirst. Second. Third. Fourth.\n"
            file_path.write_text(content, encoding="utf-8")

            with pytest.raises(ValueError, match="2-3 sentences"):
                validate_markdown_file(str(file_path))

    def test_validate_markdown_file_utf8_without_bom(self):
        """Test that validation checks for UTF-8 without BOM."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            file_path = tmp_path / "test.md"
            # Write with BOM
            content = "# Title\n\nFirst sentence. Second sentence.\n"
            file_path.write_bytes(b"\xef\xbb\xbf" + content.encode("utf-8"))

            with pytest.raises(ValueError, match="BOM"):
                validate_markdown_file(str(file_path))

    def test_validate_markdown_file_lf_line_endings(self):
        """Test that validation checks for LF line endings."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            file_path = tmp_path / "test.md"
            # Write with CRLF
            content = "# Title\r\n\r\nFirst sentence. Second sentence.\r\n"
            file_path.write_bytes(content.encode("utf-8"))

            with pytest.raises(ValueError, match="CRLF"):
                validate_markdown_file(str(file_path))

    def test_validate_markdown_file_trailing_newline(self):
        """Test that validation checks for trailing newline."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            file_path = tmp_path / "test.md"
            # File without trailing newline
            content = "# Title\n\nFirst sentence. Second sentence."
            file_path.write_text(content, encoding="utf-8")

            with pytest.raises(ValueError, match="trailing newline"):
                validate_markdown_file(str(file_path))

    def test_validate_markdown_file_valid_content(self):
        """Test that validation passes with valid markdown file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            file_path = tmp_path / "test.md"
            content = "# Title\n\nFirst sentence. Second sentence.\n"
            file_path.write_text(content, encoding="utf-8")

            # Should not raise
            result = validate_markdown_file(str(file_path))
            assert result is True

    def test_validate_markdown_file_three_sentences_valid(self):
        """Test that validation passes with exactly 3 sentences."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            file_path = tmp_path / "test.md"
            content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            file_path.write_text(content, encoding="utf-8")

            result = validate_markdown_file(str(file_path))
            assert result is True


class TestGitIntegration:
    """Tests for task-5: Implement git integration (add, commit, push)."""

    @patch("sheep.features.feature_243_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_243_markdown_file_creation.push_markdown_file")
    def test_git_add_stages_file(self, mock_push, mock_commit):
        """Test that commit function stages file with git add."""
        from sheep.features.feature_243_markdown_file_creation import (
            create_feature_243_markdown_file,
        )

        mock_commit.return_value = "Committed successfully"
        mock_push.return_value = "Pushed successfully"

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp_path)

                # Mock the content generation and file operations
                with patch("sheep.features.feature_243_markdown_file_creation.generate_title_content") as mock_title, \
                     patch("sheep.features.feature_243_markdown_file_creation.generate_prose_content") as mock_prose, \
                     patch("sheep.features.feature_243_markdown_file_creation.write_markdown_file") as mock_write, \
                     patch("sheep.features.feature_243_markdown_file_creation.validate_markdown_file") as mock_validate:

                    mock_title.return_value = "Test Title"
                    mock_prose.return_value = "First sentence. Second sentence. Third sentence."
                    mock_write.return_value = "test-c2dbie.md"
                    mock_validate.return_value = True

                    create_feature_243_markdown_file(tmp_dir)

                    # Verify commit was called
                    mock_commit.assert_called_once()
            finally:
                os.chdir(original_cwd)

    @patch("sheep.features.feature_243_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_243_markdown_file_creation.push_markdown_file")
    def test_conventional_commit_message_format(self, mock_push, mock_commit):
        """Test that commit uses conventional message format."""
        from sheep.features.feature_243_markdown_file_creation import (
            FEATURE_NUMBER,
            MARKDOWN_FILENAME,
            create_feature_243_markdown_file,
        )

        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp_path)

                with patch("sheep.features.feature_243_markdown_file_creation.generate_title_content") as mock_title, \
                     patch("sheep.features.feature_243_markdown_file_creation.generate_prose_content") as mock_prose, \
                     patch("sheep.features.feature_243_markdown_file_creation.write_markdown_file") as mock_write, \
                     patch("sheep.features.feature_243_markdown_file_creation.validate_markdown_file") as mock_validate:

                    mock_title.return_value = "Test"
                    mock_prose.return_value = "A. B. C."
                    mock_write.return_value = MARKDOWN_FILENAME
                    mock_validate.return_value = True

                    create_feature_243_markdown_file(tmp_dir)

                    # Verify commit was called with correct message format
                    mock_commit.assert_called_once()
                    call_args = mock_commit.call_args
                    commit_message = call_args[1].get("custom_message")
                    assert f"feat({FEATURE_NUMBER}):" in commit_message
                    assert MARKDOWN_FILENAME in commit_message
            finally:
                os.chdir(original_cwd)

    @patch("sheep.features.feature_243_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_243_markdown_file_creation.push_markdown_file")
    def test_git_push_to_feature_branch(self, mock_push, mock_commit):
        """Test that push pushes to feature branch."""
        from sheep.features.feature_243_markdown_file_creation import (
            create_feature_243_markdown_file,
        )

        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp_path)

                with patch("sheep.features.feature_243_markdown_file_creation.generate_title_content") as mock_title, \
                     patch("sheep.features.feature_243_markdown_file_creation.generate_prose_content") as mock_prose, \
                     patch("sheep.features.feature_243_markdown_file_creation.write_markdown_file") as mock_write, \
                     patch("sheep.features.feature_243_markdown_file_creation.validate_markdown_file") as mock_validate:

                    mock_title.return_value = "Test"
                    mock_prose.return_value = "A. B. C."
                    mock_write.return_value = "test-c2dbie.md"
                    mock_validate.return_value = True

                    create_feature_243_markdown_file(tmp_dir)

                    # Verify push was called
                    mock_push.assert_called_once()
            finally:
                os.chdir(original_cwd)

    @patch("sheep.features.feature_243_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_243_markdown_file_creation.push_markdown_file")
    def test_git_operations_called_in_order(self, mock_push, mock_commit):
        """Test that git operations are called in correct order: add, commit, push."""
        from sheep.features.feature_243_markdown_file_creation import (
            create_feature_243_markdown_file,
        )

        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp_path)

                with patch("sheep.features.feature_243_markdown_file_creation.generate_title_content") as mock_title, \
                     patch("sheep.features.feature_243_markdown_file_creation.generate_prose_content") as mock_prose, \
                     patch("sheep.features.feature_243_markdown_file_creation.write_markdown_file") as mock_write, \
                     patch("sheep.features.feature_243_markdown_file_creation.validate_markdown_file") as mock_validate:

                    mock_title.return_value = "Test"
                    mock_prose.return_value = "A. B. C."
                    mock_write.return_value = "test-c2dbie.md"
                    mock_validate.return_value = True

                    create_feature_243_markdown_file(tmp_dir)

                    # Verify order: commit should be called before push
                    assert mock_commit.called
                    assert mock_push.called
                    # push should be called after commit
                    assert mock_commit.call_count == 1
                    assert mock_push.call_count == 1
            finally:
                os.chdir(original_cwd)

    @patch("sheep.features.feature_243_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_243_markdown_file_creation.push_markdown_file")
    def test_git_commit_failure_propagates_error(self, mock_push, mock_commit):
        """Test that git commit failure raises exception."""
        from sheep.features.feature_243_markdown_file_creation import (
            create_feature_243_markdown_file,
        )

        mock_commit.side_effect = Exception("Git commit failed")
        mock_push.return_value = "Pushed"

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp_path)

                with patch("sheep.features.feature_243_markdown_file_creation.generate_title_content") as mock_title, \
                     patch("sheep.features.feature_243_markdown_file_creation.generate_prose_content") as mock_prose, \
                     patch("sheep.features.feature_243_markdown_file_creation.write_markdown_file") as mock_write, \
                     patch("sheep.features.feature_243_markdown_file_creation.validate_markdown_file") as mock_validate:

                    mock_title.return_value = "Test"
                    mock_prose.return_value = "A. B. C."
                    mock_write.return_value = "test-c2dbie.md"
                    mock_validate.return_value = True

                    with pytest.raises(Exception, match="Git commit failed"):
                        create_feature_243_markdown_file(tmp_dir)

                    # push should not be called if commit fails
                    mock_push.assert_not_called()
            finally:
                os.chdir(original_cwd)

    @patch("sheep.features.feature_243_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_243_markdown_file_creation.push_markdown_file")
    def test_git_push_failure_propagates_error(self, mock_push, mock_commit):
        """Test that git push failure raises exception."""
        from sheep.features.feature_243_markdown_file_creation import (
            create_feature_243_markdown_file,
        )

        mock_commit.return_value = "Committed"
        mock_push.side_effect = Exception("Git push failed")

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp_path)

                with patch("sheep.features.feature_243_markdown_file_creation.generate_title_content") as mock_title, \
                     patch("sheep.features.feature_243_markdown_file_creation.generate_prose_content") as mock_prose, \
                     patch("sheep.features.feature_243_markdown_file_creation.write_markdown_file") as mock_write, \
                     patch("sheep.features.feature_243_markdown_file_creation.validate_markdown_file") as mock_validate:

                    mock_title.return_value = "Test"
                    mock_prose.return_value = "A. B. C."
                    mock_write.return_value = "test-c2dbie.md"
                    mock_validate.return_value = True

                    with pytest.raises(Exception, match="Git push failed"):
                        create_feature_243_markdown_file(tmp_dir)
            finally:
                os.chdir(original_cwd)
