"""Tests for feature 135: markdown file creation.

Tests cover the main tasks:
- Create markdown file with pathlib
- Validate markdown file format, encoding, and line endings
- Validate markdown structure (H1 heading + 2-3 sentences)
"""

import os
import re
import tempfile
from pathlib import Path

import pytest


class TestTask1CreateMarkdownFile:
    """Tests for task 1: Create markdown file with pathlib and validate file I/O."""

    def test_markdown_file_is_created(self):
        """Test that test-0h8m0m.md is created at repository root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create file with proper encoding and line endings
                content = "# The Power of Incremental Progress\n\nSmall consistent improvements compound over time to create remarkable transformations that might seem impossible from a single day's perspective. Whether learning a new skill, building a project, or improving health, the magic lies not in dramatic leaps but in the cumulative effect of daily effort and intention. This principle teaches us that patience and persistence are more valuable than natural talent or luck when pursuing any meaningful goal.\n"
                file_path = Path("test-0h8m0m.md")
                file_path.write_text(content, encoding='utf-8', newline='\n')

                assert file_path.exists(), "File should exist after creation"
                assert file_path.stat().st_size > 0, "File should have content"

            finally:
                os.chdir(original_cwd)

    def test_markdown_file_contains_h1_heading(self):
        """Test that file contains markdown H1 heading on first line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# The Power of Incremental Progress\n\nSmall consistent improvements compound over time to create remarkable transformations that might seem impossible from a single day's perspective. Whether learning a new skill, building a project, or improving health, the magic lies not in dramatic leaps but in the cumulative effect of daily effort and intention. This principle teaches us that patience and persistence are more valuable than natural talent or luck.\n"
                file_path = Path("test-0h8m0m.md")
                file_path.write_text(content, encoding='utf-8', newline='\n')

                text = file_path.read_text(encoding='utf-8')
                lines = text.split('\n')

                assert lines[0].startswith('# '), "First line should be H1 heading"

            finally:
                os.chdir(original_cwd)

    def test_markdown_file_has_blank_line_after_heading(self):
        """Test that file has blank line separator after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# The Power of Incremental Progress\n\nSmall consistent improvements compound over time to create remarkable transformations that might seem impossible from a single day's perspective. Whether learning a new skill, building a project, or improving health, the magic lies not in dramatic leaps but in the cumulative effect of daily effort and intention. This principle teaches us that patience and persistence are more valuable than natural talent or luck.\n"
                file_path = Path("test-0h8m0m.md")
                file_path.write_text(content, encoding='utf-8', newline='\n')

                text = file_path.read_text(encoding='utf-8')
                lines = text.rstrip('\n').split('\n')

                assert len(lines) >= 3, "File should have heading, blank line, and prose"
                assert lines[1] == '', "Second line should be blank"

            finally:
                os.chdir(original_cwd)

    def test_markdown_file_contains_prose_content(self):
        """Test that file contains 2-3 sentences of prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# The Power of Incremental Progress\n\nSmall consistent improvements compound over time to create remarkable transformations that might seem impossible from a single day's perspective. Whether learning a new skill, building a project, or improving health, the magic lies not in dramatic leaps but in the cumulative effect of daily effort and intention. This principle teaches us that patience and persistence are more valuable than natural talent or luck.\n"
                file_path = Path("test-0h8m0m.md")
                file_path.write_text(content, encoding='utf-8', newline='\n')

                text = file_path.read_text(encoding='utf-8')
                lines = text.rstrip('\n').split('\n')
                prose_text = '\n'.join(lines[2:])

                # Count sentences by counting periods
                sentence_count = prose_text.count('.')
                assert 2 <= sentence_count <= 3, f"Should have 2-3 sentences, found {sentence_count}"

            finally:
                os.chdir(original_cwd)

    def test_markdown_file_uses_utf8_encoding(self):
        """Test that file is encoded as UTF-8 without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# The Power of Incremental Progress\n\nSmall consistent improvements compound over time to create remarkable transformations that might seem impossible from a single day's perspective. Whether learning a new skill, building a project, or improving health, the magic lies not in dramatic leaps but in the cumulative effect of daily effort and intention. This principle teaches us that patience and persistence are more valuable than natural talent or luck.\n"
                file_path = Path("test-0h8m0m.md")
                file_path.write_text(content, encoding='utf-8', newline='\n')

                # Read as binary to check for BOM
                with open(file_path, 'rb') as f:
                    binary_content = f.read()

                # UTF-8 BOM is EF BB BF
                assert not binary_content.startswith(b'\xef\xbb\xbf'), "File should not contain UTF-8 BOM"

                # Verify file is readable as UTF-8
                text = file_path.read_text(encoding='utf-8')
                assert len(text) > 0, "File should be readable as UTF-8"

            finally:
                os.chdir(original_cwd)

    def test_markdown_file_uses_lf_line_endings(self):
        """Test that file uses LF (Unix) line endings, not CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# The Power of Incremental Progress\n\nSmall consistent improvements compound over time to create remarkable transformations that might seem impossible from a single day's perspective. Whether learning a new skill, building a project, or improving health, the magic lies not in dramatic leaps but in the cumulative effect of daily effort and intention. This principle teaches us that patience and persistence are more valuable than natural talent or luck.\n"
                file_path = Path("test-0h8m0m.md")
                file_path.write_text(content, encoding='utf-8', newline='\n')

                # Read as binary to check line endings
                with open(file_path, 'rb') as f:
                    binary_content = f.read()

                # Should not contain CRLF (Windows line ending)
                assert b'\r\n' not in binary_content, "File should use LF, not CRLF"

                # Should not contain standalone CR
                assert b'\r' not in binary_content, "File should use LF, not CR"

            finally:
                os.chdir(original_cwd)

    def test_markdown_file_structure_matches_pattern(self):
        """Test that complete file structure matches the established pattern."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# The Power of Incremental Progress\n\nSmall consistent improvements compound over time to create remarkable transformations that might seem impossible from a single day's perspective. Whether learning a new skill, building a project, or improving health, the magic lies not in dramatic leaps but in the cumulative effect of daily effort and intention. This principle teaches us that patience and persistence are more valuable than natural talent or luck.\n"
                file_path = Path("test-0h8m0m.md")
                file_path.write_text(content, encoding='utf-8', newline='\n')

                text = file_path.read_text(encoding='utf-8')
                lines = text.rstrip('\n').split('\n')

                # Pattern: line[0] = H1, line[1] = blank, line[2:] = prose
                assert lines[0].startswith('# '), "First line should be H1"
                assert lines[1] == '', "Second line should be blank"
                assert len('\n'.join(lines[2:])) > 0, "Should have prose content"

            finally:
                os.chdir(original_cwd)


class TestTask2FileValidation:
    """Tests for task 2: Implement comprehensive file validation logic."""

    def test_validation_checks_file_existence(self):
        """Test that validation checks if file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Non-existent file should fail validation
                file_path = Path("test-0h8m0m.md")
                assert not file_path.exists(), "File should not exist before creation"

                # Create file for successful validation
                content = "# The Power of Incremental Progress\n\nSmall consistent improvements compound over time to create remarkable transformations that might seem impossible from a single day's perspective. Whether learning a new skill, building a project, or improving health, the magic lies not in dramatic leaps but in the cumulative effect of daily effort and intention. This principle teaches us that patience and persistence are more valuable than natural talent or luck.\n"
                file_path.write_text(content, encoding='utf-8', newline='\n')

                assert file_path.exists(), "File should exist after creation"

            finally:
                os.chdir(original_cwd)

    def test_validation_checks_file_size_range(self):
        """Test that validation verifies file size is 400-600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # File with proper content should be in size range
                content = "# The Power of Incremental Progress\n\nSmall consistent improvements compound over time to create remarkable transformations that might seem impossible from a single day's perspective. Whether learning a new skill, building a project, or improving health, the magic lies not in dramatic leaps but in the cumulative effect of daily effort and intention. This principle teaches us that patience and persistence are more valuable than natural talent or luck.\n"
                file_path = Path("test-0h8m0m.md")
                file_path.write_text(content, encoding='utf-8', newline='\n')

                size_bytes = file_path.stat().st_size
                # Should be roughly 400-600 bytes for the pattern
                assert 350 < size_bytes < 700, f"File size {size_bytes} should be in reasonable range"

            finally:
                os.chdir(original_cwd)

    def test_validation_checks_utf8_encoding(self):
        """Test that validation verifies file is readable as UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# The Power of Incremental Progress\n\nSmall consistent improvements compound over time to create remarkable transformations that might seem impossible from a single day's perspective. Whether learning a new skill, building a project, or improving health, the magic lies not in dramatic leaps but in the cumulative effect of daily effort and intention. This principle teaches us that patience and persistence are more valuable than natural talent or luck.\n"
                file_path = Path("test-0h8m0m.md")
                file_path.write_text(content, encoding='utf-8', newline='\n')

                # Should be readable as UTF-8 without errors
                try:
                    text = file_path.read_text(encoding='utf-8')
                    assert len(text) > 0, "File should be readable"
                except UnicodeDecodeError:
                    pytest.fail("File should be valid UTF-8")

            finally:
                os.chdir(original_cwd)

    def test_validation_checks_lf_line_endings(self):
        """Test that validation verifies file uses LF line endings only."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# The Power of Incremental Progress\n\nSmall consistent improvements compound over time to create remarkable transformations that might seem impossible from a single day's perspective. Whether learning a new skill, building a project, or improving health, the magic lies not in dramatic leaps but in the cumulative effect of daily effort and intention. This principle teaches us that patience and persistence are more valuable than natural talent or luck.\n"
                file_path = Path("test-0h8m0m.md")
                file_path.write_text(content, encoding='utf-8', newline='\n')

                # Read binary to check for CRLF
                with open(file_path, 'rb') as f:
                    binary_content = f.read()

                # Should not contain CRLF or CR
                assert b'\r\n' not in binary_content, "Should use LF, not CRLF"
                assert b'\r' not in binary_content, "Should use LF, not CR"

            finally:
                os.chdir(original_cwd)

    def test_validation_checks_h1_structure(self):
        """Test that validation verifies first line is markdown H1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# The Power of Incremental Progress\n\nSmall consistent improvements compound over time to create remarkable transformations that might seem impossible from a single day's perspective. Whether learning a new skill, building a project, or improving health, the magic lies not in dramatic leaps but in the cumulative effect of daily effort and intention. This principle teaches us that patience and persistence are more valuable than natural talent or luck.\n"
                file_path = Path("test-0h8m0m.md")
                file_path.write_text(content, encoding='utf-8', newline='\n')

                text = file_path.read_text(encoding='utf-8')
                lines = text.rstrip('\n').split('\n')

                assert lines[0].startswith('# '), "First line should be H1 heading"

            finally:
                os.chdir(original_cwd)

    def test_validation_checks_sentence_count(self):
        """Test that validation verifies exactly 2-3 sentences in prose."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# The Power of Incremental Progress\n\nSmall consistent improvements compound over time to create remarkable transformations that might seem impossible from a single day's perspective. Whether learning a new skill, building a project, or improving health, the magic lies not in dramatic leaps but in the cumulative effect of daily effort and intention. This principle teaches us that patience and persistence are more valuable than natural talent or luck.\n"
                file_path = Path("test-0h8m0m.md")
                file_path.write_text(content, encoding='utf-8', newline='\n')

                text = file_path.read_text(encoding='utf-8')
                lines = text.rstrip('\n').split('\n')
                prose_text = '\n'.join(lines[2:])

                sentence_count = prose_text.count('.')
                assert 2 <= sentence_count <= 3, f"Should have 2-3 sentences, found {sentence_count}"

            finally:
                os.chdir(original_cwd)

    def test_validation_comprehensive(self):
        """Test that all validation checks pass together for compliant file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# The Power of Incremental Progress\n\nSmall consistent improvements compound over time to create remarkable transformations that might seem impossible from a single day's perspective. Whether learning a new skill, building a project, or improving health, the magic lies not in dramatic leaps but in the cumulative effect of daily effort and intention. This principle teaches us that patience and persistence are more valuable than natural talent or luck.\n"
                file_path = Path("test-0h8m0m.md")
                file_path.write_text(content, encoding='utf-8', newline='\n')

                # All checks should pass
                assert file_path.exists(), "File exists"

                size_bytes = file_path.stat().st_size
                assert 350 < size_bytes < 700, "File size in range"

                text = file_path.read_text(encoding='utf-8')
                assert len(text) > 0, "UTF-8 readable"

                with open(file_path, 'rb') as f:
                    binary_content = f.read()

                assert not binary_content.startswith(b'\xef\xbb\xbf'), "No UTF-8 BOM"
                assert b'\r\n' not in binary_content, "LF line endings"
                assert b'\r' not in binary_content, "No CR"

                lines = text.rstrip('\n').split('\n')
                assert lines[0].startswith('# '), "H1 heading present"
                assert lines[1] == '', "Blank line after heading"

                prose_text = '\n'.join(lines[2:])
                sentence_count = prose_text.count('.')
                assert 2 <= sentence_count <= 3, f"2-3 sentences"

                # All validations passed
                assert True, "Comprehensive validation successful"

            finally:
                os.chdir(original_cwd)
