#!/usr/bin/env python3
"""
Test suite for Feature 262 Phase 1: Content Generation & File Creation

Tests verify:
1. Content generation produces valid markdown structure
2. File is created with proper encoding and line endings
3. Validation passes for generated content and created file
4. Retry logic uses exponential backoff
"""

import os
import re
import sys
import time
import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import Mock, patch

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.create_markdown import (
    generate_markdown_content,
    validate_content,
    create_markdown_file,
    validate_file_encoding,
)

# Valid mock content that passes all validation checks
# Must have: H1 heading, blank line, 2-3 sentences, 100-300 chars prose, 10+ unique words
VALID_MOCK_CONTENT = """# Cloud Computing

Cloud computing has revolutionized how organizations manage infrastructure. This technology enables companies to access resources online rather than maintaining expensive on-site systems. Cloud platforms provide scalability and cost efficiency for modern digital business."""


class TestContentGeneration(unittest.TestCase):
    """Test cases for markdown content generation with validation."""

    @patch('src.create_markdown.get_reasoning_llm')
    def test_generate_markdown_content_returns_valid_structure(self, mock_get_llm):
        """Test that generate_markdown_content returns content with valid structure."""
        # Mock the LLM
        mock_llm = Mock()
        mock_llm.call.return_value = VALID_MOCK_CONTENT
        mock_get_llm.return_value = mock_llm

        result = generate_markdown_content(max_retries=3)

        self.assertIsInstance(result, dict)
        self.assertIn('title', result)
        self.assertIn('prose', result)
        self.assertIn('full_content', result)

        # Verify structure
        content = result['full_content']
        self.assertTrue(content.lstrip().startswith('# '), "Content must start with H1 heading")

    @patch('src.create_markdown.get_reasoning_llm')
    def test_content_has_h1_heading_on_first_line(self, mock_get_llm):
        """Test that generated content has H1 heading on first line."""
        mock_llm = Mock()
        mock_llm.call.return_value = VALID_MOCK_CONTENT
        mock_get_llm.return_value = mock_llm

        result = generate_markdown_content(max_retries=3)
        content = result['full_content']

        first_line = content.strip().split('\n')[0]
        self.assertTrue(first_line.startswith('# '), "First line must start with '# '")

    @patch('src.create_markdown.get_reasoning_llm')
    def test_content_has_blank_line_separator(self, mock_get_llm):
        """Test that content has blank line as second line."""
        mock_llm = Mock()
        mock_llm.call.return_value = VALID_MOCK_CONTENT
        mock_get_llm.return_value = mock_llm

        result = generate_markdown_content(max_retries=3)
        content = result['full_content']

        lines = content.strip().split('\n')
        self.assertGreater(len(lines), 1, "Content must have at least 2 lines")
        self.assertEqual(lines[1], '', "Second line must be blank (separator)")

    @patch('src.create_markdown.get_reasoning_llm')
    def test_content_has_2_to_3_sentences(self, mock_get_llm):
        """Test that prose contains exactly 2-3 sentences."""
        mock_llm = Mock()
        mock_llm.call.return_value = VALID_MOCK_CONTENT
        mock_get_llm.return_value = mock_llm

        result = generate_markdown_content(max_retries=3)
        prose = result['prose']

        # Count sentences using regex (matches . ! ? followed by space)
        sentence_pattern = r'[.!?]\s+'
        sentences = re.split(sentence_pattern, prose.strip())
        # Remove empty strings and trailing content
        sentences = [s for s in sentences if s.strip()]

        self.assertGreaterEqual(len(sentences), 2, "Prose must have at least 2 sentences")
        self.assertLessEqual(len(sentences), 3, "Prose must have at most 3 sentences")

    @patch('src.create_markdown.get_reasoning_llm')
    def test_content_prose_length_in_range(self, mock_get_llm):
        """Test that prose length is between 100-300 characters."""
        mock_llm = Mock()
        mock_llm.call.return_value = VALID_MOCK_CONTENT
        mock_get_llm.return_value = mock_llm

        result = generate_markdown_content(max_retries=3)
        prose = result['prose']
        prose_length = len(prose)

        self.assertGreaterEqual(prose_length, 100, f"Prose too short: {prose_length} chars (min 100)")
        self.assertLessEqual(prose_length, 300, f"Prose too long: {prose_length} chars (max 300)")

    @patch('src.create_markdown.get_reasoning_llm')
    def test_content_has_vocabulary_variety(self, mock_get_llm):
        """Test that content has 10+ unique words."""
        mock_llm = Mock()
        mock_llm.call.return_value = VALID_MOCK_CONTENT
        mock_get_llm.return_value = mock_llm

        result = generate_markdown_content(max_retries=3)
        content = result['full_content']

        # Count unique words (case-insensitive)
        words = set(re.findall(r'\b\w+\b', content.lower()))
        self.assertGreaterEqual(len(words), 10, f"Content must have 10+ unique words, found {len(words)}")

    @patch('src.create_markdown.get_reasoning_llm')
    def test_validate_content_passes(self, mock_get_llm):
        """Test that generated content passes validate_content()."""
        mock_llm = Mock()
        mock_llm.call.return_value = VALID_MOCK_CONTENT
        mock_get_llm.return_value = mock_llm

        result = generate_markdown_content(max_retries=3)
        content = result['full_content']

        validation = validate_content(content)
        self.assertTrue(validation['is_valid'], f"Content validation failed: {validation['errors']}")

    def test_generate_markdown_content_with_retry_logic(self):
        """Test that retry logic implements exponential backoff."""
        # Mock the LLM to fail validation twice, then succeed
        call_count = [0]

        def mock_llm_call(messages):
            call_count[0] += 1
            if call_count[0] < 3:
                # Return invalid content (too short) - will trigger retry
                return "# Title\n\nInvalid content is too short here."
            else:
                # Return valid content
                return VALID_MOCK_CONTENT

        with mock.patch('src.create_markdown.get_reasoning_llm') as mock_llm:
            mock_instance = mock.Mock()
            mock_instance.call = mock_llm_call
            mock_llm.return_value = mock_instance

            start_time = time.time()
            result = generate_markdown_content(max_retries=3, retry_delay=0.1)
            elapsed = time.time() - start_time

            # Should have retried twice and eventually succeeded
            self.assertGreaterEqual(call_count[0], 3, "Should have retried at least twice")
            self.assertIsNotNone(result, "Should eventually succeed")
            # With exponential backoff (0.1 + 0.2 = 0.3s), should take at least 0.25s
            self.assertGreater(elapsed, 0.25, "Should have experienced delay from backoff")

    def test_generate_markdown_content_raises_after_max_retries(self):
        """Test that ValueError is raised after max retries fail."""
        def mock_llm_call_fail(messages):
            # Always return invalid content
            return "Invalid content"

        with mock.patch('src.create_markdown.get_reasoning_llm') as mock_llm:
            mock_instance = mock.Mock()
            mock_instance.call = mock_llm_call_fail
            mock_llm.return_value = mock_instance

            with self.assertRaises(ValueError) as context:
                generate_markdown_content(max_retries=2, retry_delay=0.01)

            self.assertIn("Failed to generate", str(context.exception))


class TestFileCreation(unittest.TestCase):
    """Test cases for markdown file creation and encoding validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_filename = "test-qvlm4j.md"
        self.test_file_path = Path(self.test_filename)

    def tearDown(self):
        """Clean up test files."""
        if self.test_file_path.exists():
            self.test_file_path.unlink()

    def test_create_markdown_file_creates_file_in_repo_root(self):
        """Test that create_markdown_file creates file in repository root."""
        content = "# Test Title\n\nThis is a valid sentence. This is another valid sentence. And a third one."

        file_path = create_markdown_file(content, filename=self.test_filename, filepath=".")

        self.assertTrue(Path(file_path).exists(), "File should exist after creation")
        self.assertEqual(
            Path(file_path).name, self.test_filename,
            "Filename should match specified name"
        )

    def test_created_file_contains_exact_content(self):
        """Test that created file contains the exact content provided."""
        content = "# Test Title\n\nThis is a valid sentence. This is another valid sentence. And a third one."

        file_path = create_markdown_file(content, filename=self.test_filename, filepath=".")

        with open(file_path, encoding='utf-8') as f:
            file_content = f.read()

        self.assertEqual(file_content, content, "File content should match input")

    def test_file_encoding_is_utf8_without_bom(self):
        """Test that created file is UTF-8 without BOM."""
        content = "# Test Title\n\nThis is a valid sentence. This is another valid sentence. And a third one."

        file_path = create_markdown_file(content, filename=self.test_filename, filepath=".")

        # Read raw bytes
        with open(file_path, 'rb') as f:
            raw_bytes = f.read()

        # Check for BOM
        self.assertFalse(
            raw_bytes.startswith(b'\xef\xbb\xbf'),
            "File should not have UTF-8 BOM"
        )

        # Verify it's valid UTF-8
        try:
            raw_bytes.decode('utf-8')
        except UnicodeDecodeError:
            self.fail("File should be valid UTF-8")

    def test_file_uses_unix_lf_line_endings(self):
        """Test that created file uses Unix LF line endings (no CRLF)."""
        content = "# Test Title\n\nThis is a valid sentence. This is another valid sentence. And a third one."

        file_path = create_markdown_file(content, filename=self.test_filename, filepath=".")

        with open(file_path, 'rb') as f:
            raw_bytes = f.read()

        self.assertNotIn(b'\r\n', raw_bytes, "File should not have CRLF line endings")
        self.assertIn(b'\n', raw_bytes, "File should have LF line endings")

    def test_validate_file_encoding_passes(self):
        """Test that validate_file_encoding passes for created file."""
        content = "# Test Title\n\nThis is a valid sentence. This is another valid sentence. And a third one."

        file_path = create_markdown_file(content, filename=self.test_filename, filepath=".")

        validation = validate_file_encoding(file_path)

        self.assertTrue(validation['is_valid'], f"Encoding validation should pass: {validation['errors']}")
        self.assertEqual(validation['details']['encoding'], 'UTF-8')
        self.assertEqual(validation['details']['line_ending_type'], 'LF')
        self.assertFalse(validation['details']['has_bom'])

    def test_create_markdown_file_raises_if_file_exists(self):
        """Test that FileExistsError is raised if file already exists."""
        content = "# Test Title\n\nThis is a valid sentence. This is another valid sentence. And a third one."

        # Create file first
        create_markdown_file(content, filename=self.test_filename, filepath=".")

        # Try to create it again
        with self.assertRaises(FileExistsError):
            create_markdown_file(content, filename=self.test_filename, filepath=".")

    @patch('src.create_markdown.get_reasoning_llm')
    def test_create_markdown_file_with_generated_content(self, mock_get_llm):
        """Test creating file with actual generated content."""
        mock_llm = Mock()
        mock_llm.call.return_value = VALID_MOCK_CONTENT
        mock_get_llm.return_value = mock_llm

        result = generate_markdown_content(max_retries=3)
        content = result['full_content']

        file_path = create_markdown_file(content, filename=self.test_filename, filepath=".")

        self.assertTrue(Path(file_path).exists())

        # Validate encoding
        encoding_result = validate_file_encoding(file_path)
        self.assertTrue(encoding_result['is_valid'], f"Encoding should be valid: {encoding_result['errors']}")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_filename = "test-qvlm4j.md"
        self.test_file_path = Path(self.test_filename)

    def tearDown(self):
        """Clean up test files."""
        if self.test_file_path.exists():
            self.test_file_path.unlink()

    @patch('src.create_markdown.get_reasoning_llm')
    def test_complete_generation_and_creation_workflow(self, mock_get_llm):
        """Test complete workflow: generate content, create file, validate."""
        mock_llm = Mock()
        mock_llm.call.return_value = VALID_MOCK_CONTENT
        mock_get_llm.return_value = mock_llm

        # Generate content
        result = generate_markdown_content(max_retries=3)
        self.assertIsNotNone(result)
        self.assertTrue(validate_content(result['full_content'])['is_valid'])

        # Create file
        file_path = create_markdown_file(
            result['full_content'],
            filename=self.test_filename,
            filepath="."
        )
        self.assertTrue(Path(file_path).exists())

        # Validate encoding
        encoding_result = validate_file_encoding(file_path)
        self.assertTrue(encoding_result['is_valid'])


if __name__ == '__main__':
    unittest.main()
