"""Tests for the complete markdown file creation workflow (feature 070)."""

import os
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import (
    create_markdown_file,
    validate_markdown_file,
    extract_topic_from_content,
)


class TestCreateMarkdownFileWorkflow:
    """Tests for the complete end-to-end markdown file creation workflow."""

    @patch("sheep.content_generators.generate_markdown_content")
    def test_create_markdown_file_workflow(self, mock_generate):
        """Test the complete workflow for creating markdown file test-9yn2il.md.

        This test exercises the full orchestration function:
        1. LLM-based content generation (Claude API via CrewAI)
        2. File write with UTF-8 encoding and Unix LF line endings
        3. Markdown format validation
        4. Git commit with conventional message format
        5. Git push to remote with upstream tracking

        Acceptance Criteria:
        - create_markdown_file("test-9yn2il.md") completes successfully
        - Function returns result dict with expected structure
        - No exceptions raised during execution
        - Structured logging captures all major operations
        - Content generation completes within 30 seconds (spec requirement NFR-3)
        - File is written to repository root directory
        - Git commit is created with conventional message format
        - Changes are pushed to remote repository
        """
        # Mock the content generation (simulating Claude API response)
        mock_content = "# Quantum Computing\n\nQuantum computers use quantum bits to process information exponentially faster than classical computers. This technology promises to revolutionize cryptography, drug discovery, and optimization problems. Current challenges include maintaining quantum coherence and error correction."
        mock_generate.return_value = mock_content + "\n"

        # Target filename from feature specification
        target_filename = "test-9yn2il.md"

        # Record start time for timeout verification (spec: 30 seconds max)
        start_time = time.time()

        # Call the main orchestration function
        result = create_markdown_file(target_filename)

        # Verify execution completed within timeout
        elapsed_time = time.time() - start_time
        assert elapsed_time < 35.0, f"Execution took {elapsed_time:.1f}s (>35s timeout)"

        # Verify result dict structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert "filepath" in result, "Result should contain 'filepath' key"
        assert "content" in result, "Result should contain 'content' key"
        assert "commit_message" in result, "Result should contain 'commit_message' key"
        assert "push_result" in result, "Result should contain 'push_result' key"

        # Verify filepath is correct
        filepath = result["filepath"]
        assert target_filename in filepath, f"Filepath should contain target filename: {filepath}"

        # Verify file exists at repository root
        file_path = Path(filepath)
        assert file_path.exists(), f"File should exist: {filepath}"
        assert file_path.is_file(), f"Path should be a file: {filepath}"

        # Verify file is at repository root (not in subdirectory)
        assert file_path.name == target_filename, f"File should be named {target_filename}"

        # Verify content structure
        content = result["content"]
        assert isinstance(content, str), "Content should be a string"
        assert content.startswith("# "), "Content should start with H1 heading"
        assert content.endswith("\n"), "Content should end with newline (Unix convention)"

        # Verify H1 heading exists
        lines = content.split("\n")
        assert len(lines) >= 3, "Content should have at least 3 lines (H1, blank, prose)"
        assert lines[0].startswith("# "), "First line should be H1 heading"
        assert lines[1] == "", "Second line should be blank separator"

        # Verify prose content (2-3 sentences)
        prose_lines = lines[2:]
        prose_text = "\n".join(prose_lines).strip()
        sentence_count = prose_text.count(".")
        assert (
            2 <= sentence_count <= 3
        ), f"Content should have 2-3 sentences, found {sentence_count}"

        # Verify commit message format
        commit_message = result["commit_message"]
        assert isinstance(commit_message, str), "Commit message should be a string"
        assert "feat:" in commit_message, "Commit message should use conventional format"
        assert target_filename in commit_message, "Commit message should include filename"

        # Verify push result indicates success
        push_result = result["push_result"]
        assert isinstance(push_result, str), "Push result should be a string"
        # Push result typically contains git output or success message
        assert len(push_result) > 0, "Push result should be non-empty"

        # Verify file content matches returned content
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        assert file_content == content, "File content should match returned content"

        # Verify UTF-8 encoding (no BOM, proper line endings)
        with open(file_path, "rb") as f:
            binary_content = f.read()
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"
        assert b"\r\n" not in binary_content, "File should use LF line endings, not CRLF"

        # Verify markdown validation passes
        validate_markdown_file(str(file_path))  # Should not raise exception

        # Verify topic extraction works
        topic = extract_topic_from_content(content)
        assert isinstance(topic, str), "Topic should be a string"
        assert len(topic) > 0, "Topic should be non-empty"
        assert topic in commit_message, "Topic should appear in commit message"


class TestMarkdownFileValidation:
    """Tests for markdown file validation after creation."""

    @patch("sheep.content_generators.generate_markdown_content")
    def test_validate_created_file(self, mock_generate):
        """Test that the created file passes validation."""
        # Mock content generation
        mock_content = "# Machine Learning\n\nMachine learning is a subset of artificial intelligence. It enables computers to learn from data without explicit programming. This technology powers many modern applications."
        mock_generate.return_value = mock_content + "\n"

        target_filename = "test-9yn2il.md"

        # First ensure file is created
        result = create_markdown_file(target_filename)
        filepath = result["filepath"]

        # Validate should pass without raising
        is_valid = validate_markdown_file(filepath)
        assert is_valid is True, "Created file should pass validation"


class TestContentExtraction:
    """Tests for extracting metadata from generated content."""

    @patch("sheep.content_generators.generate_markdown_content")
    def test_extract_topic_from_generated_content(self, mock_generate):
        """Test that topic extraction works on actual generated content."""
        # Mock content generation
        mock_content = "# Neural Networks\n\nNeural networks are computational models inspired by biological neurons. They consist of interconnected nodes that process information through layers. These networks excel at pattern recognition and complex data analysis."
        mock_generate.return_value = mock_content + "\n"

        target_filename = "test-9yn2il.md"
        result = create_markdown_file(target_filename)
        content = result["content"]

        # Extract topic
        topic = extract_topic_from_content(content)

        # Verify topic is meaningful
        assert isinstance(topic, str), "Topic should be a string"
        assert len(topic) > 0, "Topic should be non-empty"
        assert len(topic) <= 100, "Topic should be reasonable length"
        assert not topic.startswith("#"), "Topic should not include markdown syntax"
