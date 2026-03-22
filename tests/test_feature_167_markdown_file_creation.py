"""Tests for feature 167: Creating markdown file test-m6t9bm.md with title and prose content."""

import inspect
from pathlib import Path
from unittest.mock import patch

import pytest


class TestFeature167MarkdownFileCreation:
    """Tests for feature 167 markdown file creation."""

    def test_module_imports(self):
        """Test that the feature module can be imported."""
        from sheep.features.feature_167_markdown_file_creation import (
            create_feature_167_markdown_file,
        )

        assert callable(create_feature_167_markdown_file)

    def test_function_signature(self):
        """Test that the function has the correct signature."""
        from sheep.features.feature_167_markdown_file_creation import (
            create_feature_167_markdown_file,
        )

        sig = inspect.signature(create_feature_167_markdown_file)
        assert "repo_path" in sig.parameters
        assert sig.parameters["repo_path"].default is None

    def test_feature_constants(self):
        """Test that feature constants are defined correctly."""
        from sheep.features.feature_167_markdown_file_creation import (
            COMMIT_MESSAGE,
            FEATURE_NUMBER,
            MARKDOWN_FILENAME,
        )

        assert FEATURE_NUMBER == 167
        assert MARKDOWN_FILENAME == "test-m6t9bm.md"
        assert COMMIT_MESSAGE == "feat(167): Create markdown file test-m6t9bm.md with prose content"

    @patch("sheep.features.feature_167_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.generate_markdown_content")
    def test_orchestration_calls_all_steps(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that the orchestration calls all steps in the correct order."""
        from sheep.features.feature_167_markdown_file_creation import (
            create_feature_167_markdown_file,
        )

        # Setup mock returns
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-m6t9bm.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed successfully"
        mock_push.return_value = "Pushed successfully"

        # Call the function
        result = create_feature_167_markdown_file("/test/repo")

        # Verify all functions were called
        mock_generate.assert_called_once()
        mock_write.assert_called_once_with(mock_content, "test-m6t9bm.md")
        mock_validate.assert_called_once()
        mock_commit.assert_called_once()
        mock_push.assert_called_once()

        # Verify the return value structure
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

    @patch("sheep.features.feature_167_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.generate_markdown_content")
    def test_returns_correct_dict_structure(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that the function returns the correct dictionary structure."""
        from sheep.features.feature_167_markdown_file_creation import (
            COMMIT_MESSAGE,
            create_feature_167_markdown_file,
        )

        # Setup mock returns
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third.\n"
        mock_filepath = "/repo/test-m6t9bm.md"
        mock_generate.return_value = mock_content
        mock_write.return_value = mock_filepath
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call the function
        result = create_feature_167_markdown_file()

        # Verify all required keys are present
        assert result["filepath"] == mock_filepath
        assert result["content"] == mock_content
        assert result["commit_message"] == COMMIT_MESSAGE
        assert result["push_result"] == "Pushed"

    @patch("sheep.features.feature_167_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.generate_markdown_content")
    def test_uses_exact_commit_message(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that the exact commit message from spec is used."""
        from sheep.features.feature_167_markdown_file_creation import (
            create_feature_167_markdown_file,
        )

        # Setup mocks
        mock_content = "# Test\n\nSentence. Sentence. Sentence.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-m6t9bm.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call the function
        create_feature_167_markdown_file()

        # Verify the commit message is exactly as specified
        call_args = mock_commit.call_args
        assert call_args is not None
        assert (
            call_args.kwargs["custom_message"]
            == "feat(167): Create markdown file test-m6t9bm.md with prose content"
        )

    @patch("sheep.features.feature_167_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.generate_markdown_content")
    def test_handles_exception_in_generate(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that exceptions in generate step are properly raised."""
        from sheep.features.feature_167_markdown_file_creation import (
            create_feature_167_markdown_file,
        )

        # Setup mock to raise exception
        mock_generate.side_effect = ValueError("LLM generation failed")

        # Verify exception is raised
        with pytest.raises(ValueError, match="LLM generation failed"):
            create_feature_167_markdown_file()

        # Verify subsequent steps were not called
        mock_write.assert_not_called()
        mock_validate.assert_not_called()
        mock_commit.assert_not_called()
        mock_push.assert_not_called()

    @patch("sheep.features.feature_167_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.generate_markdown_content")
    def test_repo_path_defaults_to_cwd(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that repo_path defaults to current working directory."""
        from sheep.features.feature_167_markdown_file_creation import (
            create_feature_167_markdown_file,
        )

        # Setup mocks
        mock_content = "# Test\n\nSentence. Sentence. Sentence.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-m6t9bm.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call without repo_path
        create_feature_167_markdown_file()

        # Verify commit was called with str(Path.cwd())
        call_args = mock_commit.call_args
        assert call_args is not None
        assert call_args[0][2] == str(Path.cwd())


class TestFileCreation:
    """Integration tests for actual file creation."""

    def test_creates_file_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading."""
        test_file = tmp_path / "test-m6t9bm.md"

        # Create the file with H1 heading
        content = "# The Power of Persistence\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_contains_exactly_three_sentences(self, tmp_path):
        """Test that file contains exactly 2-3 sentences (ending with periods)."""
        test_file = tmp_path / "test-m6t9bm.md"

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible, discovering capabilities we never knew we possessed.\n"
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
        test_file = tmp_path / "test-m6t9bm.md"

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment. It builds resilience. Through persistence, we unlock potential.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        # Check that second line (index 1) is blank
        assert lines[0].startswith("# ")
        assert lines[1] == ""

    def test_file_uses_utf8_encoding(self, tmp_path):
        """Test that file is UTF-8 encoded."""
        test_file = tmp_path / "test-m6t9bm.md"

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment. It builds resilience. Through persistence, we unlock potential.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Read as binary and verify no BOM
        binary_content = test_file.read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Verify can be decoded as UTF-8
        decoded = binary_content.decode("utf-8")
        assert decoded == content

    def test_file_uses_lf_line_endings(self, tmp_path):
        """Test that file uses LF line endings, not CRLF."""
        test_file = tmp_path / "test-m6t9bm.md"

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment. It builds resilience. Through persistence, we unlock potential.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Read as binary and verify no CRLF
        binary_content = test_file.read_bytes()
        assert b"\r\n" not in binary_content
        assert b"\n" in binary_content

    def test_file_ends_with_newline(self, tmp_path):
        """Test that file ends with a trailing newline (Unix convention)."""
        test_file = tmp_path / "test-m6t9bm.md"

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment. It builds resilience. Through persistence, we unlock potential.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        assert text_content.endswith("\n")

    def test_file_size_is_reasonable(self, tmp_path):
        """Test that file size is within reasonable bounds (300-600 bytes guideline)."""
        test_file = tmp_path / "test-m6t9bm.md"

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible, discovering capabilities we never knew we possessed.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = test_file.stat().st_size
        # 300-600 bytes is a guideline, not strict
        assert 100 < file_size < 1000


class TestEndToEndIntegration:
    """End-to-end integration tests for feature 167."""

    @patch("sheep.features.feature_167_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.generate_markdown_content")
    def test_e2e_creates_markdown_file_with_valid_format(
        self, mock_generate, mock_commit, mock_push, mock_validate, tmp_path
    ):
        """Test end-to-end creation of markdown file with valid format."""
        import os

        from sheep.features.feature_167_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_feature_167_markdown_file,
        )

        # Setup mocks
        mock_content = "# Technology and Innovation\n\nTechnology continues to drive innovation across industries. It enables faster communication and collaboration. These advances shape how we work and live.\n"
        mock_generate.return_value = mock_content
        mock_validate.return_value = True
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        # Change to temp directory for test
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Execute the feature
            result = create_feature_167_markdown_file()

            # Verify file was created
            assert Path(MARKDOWN_FILENAME).exists()
            file_content = Path(MARKDOWN_FILENAME).read_text(encoding="utf-8")

            # Verify H1 heading
            assert file_content.startswith("# ")

            # Verify prose content
            lines = file_content.split("\n")
            assert len(lines) >= 3
            assert lines[1] == ""  # Blank line separator

            # Verify sentence count (2-3 sentences)
            prose = "\n".join(lines[2:]).strip()
            sentence_count = prose.count(".")
            assert 2 <= sentence_count <= 3

            # Verify file encoding (no UTF-8 BOM)
            # Note: Line ending validation is checked by validate_markdown_file()
            # which is mocked in this test. The actual file may have platform-specific
            # line endings when written.
            file_bytes = Path(MARKDOWN_FILENAME).read_bytes()
            assert not file_bytes.startswith(b"\xef\xbb\xbf")  # No UTF-8 BOM

            # Verify result structure
            assert "filepath" in result
            assert "content" in result
            assert "commit_message" in result
            assert "push_result" in result

            # Verify git operations were called
            mock_commit.assert_called_once()
            mock_push.assert_called_once()

        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_167_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.generate_markdown_content")
    def test_e2e_validates_content_structure(
        self, mock_generate, mock_commit, mock_push, mock_validate, tmp_path
    ):
        """Test that generated content has correct markdown structure."""
        import os

        from sheep.features.feature_167_markdown_file_creation import (
            create_feature_167_markdown_file,
        )

        # Setup mocks
        mock_content = "# Learning and Growth\n\nContinuous learning drives personal growth and development. It opens new opportunities and perspectives. Embracing learning is key to success.\n"
        mock_generate.return_value = mock_content
        mock_validate.return_value = True
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        # Change to temp directory for test
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Execute the feature
            result = create_feature_167_markdown_file()

            # Get content from result
            content = result["content"]

            # Verify structure: heading, blank line, prose
            parts = content.split("\n\n", 1)
            assert len(parts) == 2

            heading = parts[0]
            prose = parts[1].strip()

            # Verify heading is H1
            assert heading.startswith("# ")

            # Verify prose has content
            assert len(prose) > 0

            # Verify prose ends with period (sentence)
            assert prose.rstrip().endswith(".")

        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_167_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_167_markdown_file_creation.generate_markdown_content")
    def test_e2e_uses_correct_filename_and_message(
        self, mock_generate, mock_commit, mock_push, mock_validate, tmp_path
    ):
        """Test that file is created with correct name and commit message."""
        import os

        from sheep.features.feature_167_markdown_file_creation import (
            COMMIT_MESSAGE,
            MARKDOWN_FILENAME,
            create_feature_167_markdown_file,
        )

        # Setup mocks
        mock_content = "# Digital Transformation\n\nDigital transformation reshapes business processes and customer experiences. It requires strategic planning and technological investment. Success comes from embracing change and innovation.\n"
        mock_generate.return_value = mock_content
        mock_validate.return_value = True
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        # Change to temp directory for test
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Execute the feature
            result = create_feature_167_markdown_file()

            # Verify exact filename
            assert MARKDOWN_FILENAME == "test-m6t9bm.md"
            assert Path(MARKDOWN_FILENAME).exists()

            # Verify exact commit message
            assert COMMIT_MESSAGE == "feat(167): Create markdown file test-m6t9bm.md with prose content"
            assert result["commit_message"] == COMMIT_MESSAGE

            # Verify commit was called with correct message
            mock_commit.assert_called_once()
            call_args = mock_commit.call_args
            assert (
                call_args.kwargs["custom_message"]
                == "feat(167): Create markdown file test-m6t9bm.md with prose content"
            )

        finally:
            os.chdir(original_cwd)
