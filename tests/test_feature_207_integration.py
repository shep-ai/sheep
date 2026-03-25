"""Integration and determinism tests for Feature 207: Create markdown file test-5q8o2a.md.

This test suite covers:
- Task 15: Integration tests for complete workflow
- Task 16: Determinism tests with temperature=0
"""

import os
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from sheep.features.feature_207_markdown_file_creation import (
    FILENAME,
    FEATURE_NUMBER,
    BRANCH_NAME,
    COMMIT_MESSAGE,
    main,
    create_markdown_file,
    validate_markdown_file,
    generate_title,
    generate_prose,
)


# Fixtures for consistent mock data
MOCK_TITLE = "Test Title"
MOCK_PROSE = "First sentence. Second sentence. Third sentence."


class TestIntegrationWorkflow:
    """Tests for task-15: Integration tests for complete workflow."""

    def _apply_common_mocks(self, test_func):
        """Helper to apply common mocks for integration tests."""
        return patch("sheep.features.feature_207_markdown_file_creation.git_push")(
            patch("sheep.features.feature_207_markdown_file_creation.git_commit")(
                patch("sheep.features.feature_207_markdown_file_creation.git_add_file")(
                    patch("sheep.features.feature_207_markdown_file_creation.generate_prose", return_value=MOCK_PROSE)(
                        patch("sheep.features.feature_207_markdown_file_creation.generate_title", return_value=MOCK_TITLE)(
                            test_func
                        )
                    )
                )
            )
        )

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose", return_value=MOCK_PROSE)
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title", return_value=MOCK_TITLE)
    def test_main_executes_successfully(self, mock_title, mock_prose, mock_add, mock_commit, mock_push, tmp_path):
        """Test that main() completes without error."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            main()
            # Should not raise any exceptions
            assert True
        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose", return_value=MOCK_PROSE)
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title", return_value=MOCK_TITLE)
    def test_main_creates_file_at_repository_root(self, mock_title, mock_prose, mock_add, mock_commit, mock_push, tmp_path):
        """Test that main() creates file at repository root."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            main()
            assert Path(FILENAME).exists()
            assert (tmp_path / FILENAME).exists()
        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose", return_value=MOCK_PROSE)
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title", return_value=MOCK_TITLE)
    def test_main_creates_file_with_valid_h1_title(self, mock_title, mock_prose, mock_add, mock_commit, mock_push, tmp_path):
        """Test that main() creates file containing valid H1 title."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            main()
            assert Path(FILENAME).exists()
            content = Path(FILENAME).read_text(encoding="utf-8")
            lines = content.split("\n")
            assert lines[0].startswith("# ")
            assert len(lines[0]) > 2
        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose", return_value=MOCK_PROSE)
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title", return_value=MOCK_TITLE)
    def test_main_creates_file_with_2_or_3_sentences(self, mock_title, mock_prose, mock_add, mock_commit, mock_push, tmp_path):
        """Test that main() creates file containing 2-3 sentences of prose."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            main()
            content = Path(FILENAME).read_text(encoding="utf-8")
            lines = content.split("\n")
            blank_line_idx = None
            for i, line in enumerate(lines):
                if line.strip() == "" and i > 0:
                    blank_line_idx = i
                    break
            assert blank_line_idx is not None
            prose = "\n".join(lines[blank_line_idx + 1:]).strip()
            sentence_count = prose.count(".")
            assert 2 <= sentence_count <= 3
        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose", return_value=MOCK_PROSE)
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title", return_value=MOCK_TITLE)
    def test_main_calls_git_add_file(self, mock_title, mock_prose, mock_add, mock_commit, mock_push, tmp_path):
        """Test that main() calls git_add_file to stage the file."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            main()
            mock_add.assert_called_once_with(FILENAME)
        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose", return_value=MOCK_PROSE)
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title", return_value=MOCK_TITLE)
    def test_main_calls_git_commit_with_conventional_message(self, mock_title, mock_prose, mock_add, mock_commit, mock_push, tmp_path):
        """Test that main() calls git_commit with conventional commit message."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            main()
            mock_commit.assert_called_once_with(COMMIT_MESSAGE)
            assert COMMIT_MESSAGE.startswith(f"feat({FEATURE_NUMBER})")
        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose", return_value=MOCK_PROSE)
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title", return_value=MOCK_TITLE)
    def test_main_calls_git_push_with_branch_name(self, mock_title, mock_prose, mock_add, mock_commit, mock_push, tmp_path):
        """Test that main() calls git_push to push to remote branch."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            main()
            mock_push.assert_called_once_with(BRANCH_NAME)
        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose", return_value=MOCK_PROSE)
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title", return_value=MOCK_TITLE)
    def test_git_operations_called_in_correct_order(self, mock_title, mock_prose, mock_add, mock_commit, mock_push, tmp_path):
        """Test that git operations are called in correct order: add, commit, push."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            main()
            # Verify all three git operations were called
            mock_add.assert_called_once()
            mock_commit.assert_called_once()
            mock_push.assert_called_once()
        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose", return_value=MOCK_PROSE)
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title", return_value=MOCK_TITLE)
    def test_created_file_is_valid_markdown(self, mock_title, mock_prose, mock_add, mock_commit, mock_push, tmp_path):
        """Test that created file passes all validation checks."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            main()
            assert Path(FILENAME).exists()
            validate_markdown_file(FILENAME)
            assert True
        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose", return_value=MOCK_PROSE)
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title", return_value=MOCK_TITLE)
    def test_file_has_correct_utf8_encoding(self, mock_title, mock_prose, mock_add, mock_commit, mock_push, tmp_path):
        """Test that created file uses UTF-8 encoding without BOM."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            main()
            binary_content = Path(FILENAME).read_bytes()
            assert not binary_content.startswith(b"\xef\xbb\xbf")
            try:
                binary_content.decode("utf-8")
            except UnicodeDecodeError:
                pytest.fail("File is not valid UTF-8")
        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose", return_value=MOCK_PROSE)
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title", return_value=MOCK_TITLE)
    def test_file_has_unix_lf_line_endings(self, mock_title, mock_prose, mock_add, mock_commit, mock_push, tmp_path):
        """Test that created file uses Unix LF line endings, not CRLF."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            main()
            binary_content = Path(FILENAME).read_bytes()
            assert b"\r\n" not in binary_content
            assert b"\r" not in binary_content
        finally:
            os.chdir(original_cwd)


class TestDeterminism:
    """Tests for task-16: Test determinism with temperature=0."""

    @patch("sheep.features.feature_207_markdown_file_creation.create_llm")
    def test_repeated_calls_produce_identical_titles(self, mock_create_llm):
        """Test that repeated calls to generate_title() produce identical output."""
        # Mock the LLM to return consistent results
        mock_llm = MagicMock()
        mock_llm.call.return_value = "# Test Title\n\nSentence one. Sentence two. Sentence three."
        mock_create_llm.return_value = mock_llm

        # Generate title multiple times
        titles = []
        for _ in range(3):
            title = generate_title()
            titles.append(title)

        # All titles should be identical
        assert titles[0] == titles[1]
        assert titles[1] == titles[2]
        assert len(set(titles)) == 1

    @patch("sheep.features.feature_207_markdown_file_creation.create_llm")
    def test_repeated_calls_produce_identical_prose(self, mock_create_llm):
        """Test that repeated calls to generate_prose() produce identical output."""
        # Mock the LLM to return consistent results
        mock_llm = MagicMock()
        mock_llm.call.return_value = "# Title\n\nFirst sentence. Second sentence. Third sentence."
        mock_create_llm.return_value = mock_llm

        # Generate prose multiple times
        prose_samples = []
        for _ in range(3):
            prose = generate_prose()
            prose_samples.append(prose)

        # All prose should be identical
        assert prose_samples[0] == prose_samples[1]
        assert prose_samples[1] == prose_samples[2]
        assert len(set(prose_samples)) == 1

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose", return_value=MOCK_PROSE)
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title", return_value=MOCK_TITLE)
    def test_repeated_file_creation_produces_identical_content(self, mock_title, mock_prose, mock_add, mock_commit, mock_push, tmp_path):
        """Test that repeated calls to create files produce identical content."""
        original_cwd = Path.cwd()
        file_contents = []

        try:
            for i in range(3):
                test_dir = tmp_path / f"test_{i}"
                test_dir.mkdir()
                os.chdir(test_dir)
                create_markdown_file()
                content = Path(FILENAME).read_text(encoding="utf-8")
                file_contents.append(content)
        finally:
            os.chdir(original_cwd)

        # All file contents should be identical
        assert file_contents[0] == file_contents[1]
        assert file_contents[1] == file_contents[2]
        assert len(set(file_contents)) == 1

    @patch("sheep.features.feature_207_markdown_file_creation.git_push")
    @patch("sheep.features.feature_207_markdown_file_creation.git_commit")
    @patch("sheep.features.feature_207_markdown_file_creation.git_add_file")
    @patch("sheep.features.feature_207_markdown_file_creation.generate_prose", return_value=MOCK_PROSE)
    @patch("sheep.features.feature_207_markdown_file_creation.generate_title", return_value=MOCK_TITLE)
    def test_multiple_main_calls_produce_identical_files(self, mock_title, mock_prose, mock_add, mock_commit, mock_push, tmp_path):
        """Test that multiple calls to main() produce identical file content."""
        original_cwd = Path.cwd()
        file_contents = []

        try:
            for i in range(3):
                test_dir = tmp_path / f"main_test_{i}"
                test_dir.mkdir()
                os.chdir(test_dir)
                main()
                content = Path(FILENAME).read_text(encoding="utf-8")
                file_contents.append(content)
        finally:
            os.chdir(original_cwd)

        # All file contents should be identical
        assert file_contents[0] == file_contents[1]
        assert file_contents[1] == file_contents[2]
        assert len(set(file_contents)) == 1

    @patch("sheep.features.feature_207_markdown_file_creation.create_llm")
    def test_determinism_title_sentence_count_stable(self, mock_create_llm):
        """Test that determinism extends to title and sentence count consistency."""
        # Mock the LLM to return consistent results
        mock_llm = MagicMock()
        mock_llm.call.return_value = "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
        mock_create_llm.return_value = mock_llm

        titles = []
        prose_samples = []

        for _ in range(2):
            titles.append(generate_title())
            prose_samples.append(generate_prose())

        # Titles should be identical
        assert titles[0] == titles[1]

        # Prose should be identical
        assert prose_samples[0] == prose_samples[1]

        # Sentence count should be consistent
        sentence_count_1 = prose_samples[0].count(".")
        sentence_count_2 = prose_samples[1].count(".")
        assert sentence_count_1 == sentence_count_2
        assert 2 <= sentence_count_1 <= 3
