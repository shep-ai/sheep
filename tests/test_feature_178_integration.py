"""Integration tests for feature 178: Full workflow execution with mocked API.

This test suite covers the complete execution workflow by mocking the LLM API
but actually executing all file operations and git operations.
"""

import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import subprocess

import pytest


class TestFeature178Integration:
    """Integration tests for complete feature 178 workflow."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_complete_workflow_creates_markdown_file(self, mock_get_llm):
        """Test that complete workflow creates test-l2bcbe.md successfully."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        # Setup mock LLM
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Artificial Intelligence\n\nArtificial intelligence is transforming how we solve problems. Machine learning algorithms can now recognize patterns that humans might miss. These technologies continue to evolve rapidly.\n"
        }
        mock_get_llm.return_value = mock_llm

        # Get current directory for file creation
        repo_path = str(Path.cwd())

        # Execute the feature
        result = create_feature_178_markdown_file(repo_path)

        # Verify result structure
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

        # Verify file was created
        markdown_file = Path(repo_path) / "test-l2bcbe.md"
        assert markdown_file.exists(), f"File {markdown_file} was not created"
        assert markdown_file.is_file(), f"{markdown_file} is not a file"
        assert markdown_file.stat().st_size > 0, f"File {markdown_file} is empty"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_file_has_utf8_encoding_no_bom(self, mock_get_llm):
        """Test that created file has UTF-8 encoding without BOM."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        # Setup mock LLM
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Python Programming\n\nPython is a versatile programming language. It's widely used for data science and web development. The language emphasizes code readability.\n"
        }
        mock_get_llm.return_value = mock_llm

        repo_path = str(Path.cwd())
        create_feature_178_markdown_file(repo_path)

        # Check file encoding
        markdown_file = Path(repo_path) / "test-l2bcbe.md"
        with open(markdown_file, "rb") as f:
            binary_content = f.read()

        # Verify no UTF-8 BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File has UTF-8 BOM (should not)"

        # Verify valid UTF-8
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("File is not valid UTF-8")

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_file_uses_lf_line_endings(self, mock_get_llm):
        """Test that created file uses LF line endings, not CRLF."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        # Setup mock LLM
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Testing Framework\n\nTesting is critical for software quality. Unit tests verify individual functions. Integration tests check how components work together.\n"
        }
        mock_get_llm.return_value = mock_llm

        repo_path = str(Path.cwd())
        create_feature_178_markdown_file(repo_path)

        # Check line endings
        markdown_file = Path(repo_path) / "test-l2bcbe.md"
        with open(markdown_file, "rb") as f:
            binary_content = f.read()

        # Verify no CRLF
        assert b"\r\n" not in binary_content, "File uses CRLF (should use LF only)"

        # Verify has LF
        assert b"\n" in binary_content, "File should have LF line endings"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_file_contains_h1_heading(self, mock_get_llm):
        """Test that file contains H1 markdown heading."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        # Setup mock LLM
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Web Development Trends\n\nModern web development uses reactive frameworks. CSS frameworks simplify styling tasks. TypeScript adds type safety to JavaScript.\n"
        }
        mock_get_llm.return_value = mock_llm

        repo_path = str(Path.cwd())
        create_feature_178_markdown_file(repo_path)

        # Check content structure
        markdown_file = Path(repo_path) / "test-l2bcbe.md"
        with open(markdown_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Verify H1 heading
        assert content.lstrip().startswith("# "), "File should start with H1 heading"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_file_contains_2_to_3_sentences(self, mock_get_llm):
        """Test that file contains exactly 2-3 sentences."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        # Setup mock LLM
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Cloud Computing\n\nCloud services provide on-demand computing resources. They enable organizations to scale applications globally. This reduces infrastructure costs significantly.\n"
        }
        mock_get_llm.return_value = mock_llm

        repo_path = str(Path.cwd())
        create_feature_178_markdown_file(repo_path)

        # Check sentence count
        markdown_file = Path(repo_path) / "test-l2bcbe.md"
        with open(markdown_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Count periods (sentences)
        sentence_count = content.count(".")
        assert (
            2 <= sentence_count <= 3
        ), f"Should have 2-3 sentences, found {sentence_count}"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_file_ends_with_newline(self, mock_get_llm):
        """Test that file ends with newline character."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        # Setup mock LLM
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Cybersecurity Essentials\n\nCybersecurity protects systems from malicious attacks. Strong passwords form the foundation of security. Regular updates patch known vulnerabilities.\n"
        }
        mock_get_llm.return_value = mock_llm

        repo_path = str(Path.cwd())
        create_feature_178_markdown_file(repo_path)

        # Check trailing newline
        markdown_file = Path(repo_path) / "test-l2bcbe.md"
        with open(markdown_file, "rb") as f:
            binary_content = f.read()

        assert binary_content.endswith(b"\n"), "File should end with newline"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_file_is_git_tracked(self, mock_get_llm):
        """Test that created file is tracked by git."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        # Setup mock LLM
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Quantum Computing\n\nQuantum computers use quantum bits for computation. They can solve certain problems much faster than classical computers. The field is still in early development.\n"
        }
        mock_get_llm.return_value = mock_llm

        repo_path = str(Path.cwd())
        create_feature_178_markdown_file(repo_path)

        # Check git tracking
        try:
            result = subprocess.run(
                ["git", "ls-files", "test-l2bcbe.md"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            assert "test-l2bcbe.md" in result.stdout, "File not tracked by git"
        except subprocess.CalledProcessError:
            pytest.skip("Git not available for verification")

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_commit_message_is_conventional_format(self, mock_get_llm):
        """Test that file is committed with conventional commit message."""
        from sheep.features.feature_178_markdown_file_creation import (
            create_feature_178_markdown_file,
        )

        # Setup mock LLM
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Blockchain Technology\n\nBlockchain is a distributed ledger technology. It underpins cryptocurrencies like Bitcoin. Smart contracts automate transactions on blockchain networks.\n"
        }
        mock_get_llm.return_value = mock_llm

        repo_path = str(Path.cwd())
        create_feature_178_markdown_file(repo_path)

        # Check commit message
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-1"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            assert "feat(178)" in result.stdout, "Commit message should contain feat(178)"
            assert (
                "test-l2bcbe.md" in result.stdout
            ), "Commit message should mention the filename"
        except subprocess.CalledProcessError:
            pytest.skip("Git not available for verification")
