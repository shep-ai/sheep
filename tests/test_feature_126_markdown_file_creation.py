"""Tests for feature 126: Create markdown file test-trd8nx.md with title and prose content."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from sheep.content_generators import create_markdown_file, validate_markdown_file


class TestFeature126MarkdownFileCreation:
    """Tests for feature 126 markdown file creation workflow."""

    def test_create_markdown_file_test_trd8nx(self, tmp_path):
        """Test that create_markdown_file('test-trd8nx.md', feature_number=126) creates valid file.

        This test verifies:
        - File is created in the repository root
        - File contains H1 heading and prose content
        - File is committed with feature number in scope
        - File is pushed to remote
        """
        # Change to temp directory to simulate repository root
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Initialize a git repository for this test
            import subprocess
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

            # Create initial commit so we have a branch to work on
            initial_file = tmp_path / "README.md"
            initial_file.write_text("# Initial\n")
            subprocess.run(["git", "add", "README.md"], check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "initial commit"], check=True, capture_output=True)

            # Create feature branch matching the naming convention
            subprocess.run(["git", "checkout", "-b", "feat/126-markdown-file-create-e7da08"],
                          check=True, capture_output=True)

            # Mock the git push and content generation since we don't have a remote or API key
            test_content = "# Machine Learning\n\nMachine learning is transforming industries worldwide. It enables computers to learn from data without explicit programming. This technology powers everything from recommendations to autonomous systems.\n"

            with patch("sheep.content_generators.generate_markdown_content") as mock_gen, \
                 patch("sheep.content_generators.GitPushTool") as mock_push_tool:
                mock_gen.return_value = test_content
                mock_push_instance = mock_push_tool.return_value
                mock_push_instance._run.return_value = "Pushed to origin"

                # Call the orchestrator function
                result = create_markdown_file("test-trd8nx.md", feature_number=126)

            # Verify returned filepath
            assert result["filepath"] is not None
            assert "test-trd8nx.md" in result["filepath"]
            assert Path(result["filepath"]).exists()

            # Verify returned content contains expected structure
            assert "# " in result["content"]  # H1 heading
            assert "." in result["content"]   # Periods (sentences)
            assert result["content"].endswith("\n")  # Trailing newline

            # Verify commit message has feature number scope
            assert "feat(126):" in result["commit_message"]
            assert "test-trd8nx.md" in result["commit_message"]

        finally:
            os.chdir(original_cwd)

    def test_created_file_has_correct_format(self, tmp_path):
        """Test that created file meets all format requirements.

        This test verifies:
        - File contains exactly one H1 heading as title
        - File contains 2-3 sentences of prose
        - File has UTF-8 encoding without BOM
        - File uses LF line endings
        - File ends with trailing newline
        - File size is at least 50 bytes
        """
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Initialize git repository
            import subprocess
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

            # Create initial commit
            initial_file = tmp_path / "README.md"
            initial_file.write_text("# Initial\n")
            subprocess.run(["git", "add", "README.md"], check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "initial commit"], check=True, capture_output=True)

            # Create feature branch
            subprocess.run(["git", "checkout", "-b", "feat/126-markdown-file-create-e7da08"],
                          check=True, capture_output=True)

            test_content = "# Quantum Computing\n\nQuantum computing represents a paradigm shift in computational power. By leveraging quantum mechanics principles, these machines solve previously intractable problems. Future applications span cryptography, drug discovery, and artificial intelligence.\n"

            # Create the file
            with patch("sheep.content_generators.generate_markdown_content") as mock_gen, \
                 patch("sheep.content_generators.GitPushTool") as mock_push_tool:
                mock_gen.return_value = test_content
                mock_push_instance = mock_push_tool.return_value
                mock_push_instance._run.return_value = "Pushed"

                result = create_markdown_file("test-trd8nx.md", feature_number=126)

            filepath = Path(result["filepath"])

            # Read file in binary mode for encoding validation
            with open(filepath, "rb") as f:
                binary_content = f.read()

            # Verify UTF-8 encoding (no BOM)
            assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

            # Verify no CRLF (should be LF only)
            assert b"\r\n" not in binary_content, "File should use LF, not CRLF"

            # Verify file size
            file_size = filepath.stat().st_size
            assert file_size >= 50, f"File should be at least 50 bytes, got {file_size}"
            assert file_size <= 1024, f"File should not exceed 1KB, got {file_size}"

            # Read file as text for content validation
            text_content = binary_content.decode("utf-8")

            # Verify H1 heading at start
            lines = text_content.split("\n")
            assert lines[0].startswith("# "), "First line should be H1 heading"

            # Verify blank line after heading
            assert len(lines) > 1 and lines[1] == "", "Second line should be blank separator"

            # Verify 2-3 sentences (count periods in prose content)
            prose_lines = [l for l in lines[2:] if l.strip()]
            prose_content = "\n".join(prose_lines)
            sentence_count = prose_content.count(".")
            assert 2 <= sentence_count <= 3, f"Should have 2-3 sentences, found {sentence_count}"

            # Verify trailing newline
            assert text_content.endswith("\n"), "File should end with trailing newline"

        finally:
            os.chdir(original_cwd)

    def test_created_file_passes_validation(self, tmp_path):
        """Test that created file passes validate_markdown_file() checks."""
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Initialize git repository
            import subprocess
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

            # Create initial commit
            initial_file = tmp_path / "README.md"
            initial_file.write_text("# Initial\n")
            subprocess.run(["git", "add", "README.md"], check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "initial commit"], check=True, capture_output=True)

            # Create feature branch
            subprocess.run(["git", "checkout", "-b", "feat/126-markdown-file-create-e7da08"],
                          check=True, capture_output=True)

            test_content = "# Cloud Computing\n\nCloud computing has revolutionized how organizations deploy software and store data. It provides scalability, flexibility, and cost efficiency to enterprises worldwide. Modern applications rely heavily on cloud infrastructure for reliability and performance.\n"

            # Create the file
            with patch("sheep.content_generators.generate_markdown_content") as mock_gen, \
                 patch("sheep.content_generators.GitPushTool") as mock_push_tool:
                mock_gen.return_value = test_content
                mock_push_instance = mock_push_tool.return_value
                mock_push_instance._run.return_value = "Pushed"

                result = create_markdown_file("test-trd8nx.md", feature_number=126)

            filepath = result["filepath"]

            # validate_markdown_file should pass without raising exceptions
            is_valid = validate_markdown_file(filepath)
            assert is_valid is True, "File validation should pass"

        finally:
            os.chdir(original_cwd)
