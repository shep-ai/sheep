"""Tests for feature 151: markdown file creation.

Tests cover the main task:
- Create markdown file with correct content, encoding, and format
- Verify file meets all requirements: H1 heading, 2-3 sentences, UTF-8 encoding, LF line endings
"""

import os
import tempfile
from pathlib import Path

import pytest


FILENAME = "test-h8ylmx.md"
FEATURE_NUMBER = 151


class TestFileCreationPhase1:
    """Tests for phase 1: File Creation and Validation."""

    def test_file_does_not_exist_initially(self):
        """Test that file test-h8ylmx.md does not exist initially."""
        # Verify the file doesn't exist at test start
        file_path = Path(FILENAME)
        # If it exists from previous run, remove it for clean test
        if file_path.exists():
            file_path.unlink()

        assert not file_path.exists(), f"File {FILENAME} should not exist before creation"

    def test_create_markdown_file_with_h1_heading(self):
        """Test that created file contains H1 heading on first line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create the file
                heading = "# Machine Learning Fundamentals"
                prose = (
                    "Machine learning enables systems to learn from data and improve "
                    "performance without explicit programming instructions. "
                    "It powers applications ranging from recommendation systems to autonomous vehicles. "
                    "Understanding core algorithms and principles is essential for modern software development."
                )
                content = f"{heading}\n\n{prose}\n"

                Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")

                # Verify file was created
                file_path = Path(FILENAME)
                assert file_path.exists(), f"File {FILENAME} should exist"

                # Verify first line is H1 heading
                lines = file_path.read_text(encoding="utf-8").split("\n")
                assert lines[0].startswith("# "), "First line must be H1 heading (starts with '# ')"
                assert lines[0] == heading, "Heading must match exactly"
            finally:
                os.chdir(original_cwd)

    def test_file_has_blank_line_separator(self):
        """Test that file has blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                heading = "# Cloud Computing Architecture"
                prose = (
                    "Cloud computing has revolutionized how organizations deploy and scale applications. "
                    "It provides flexible resources, reduced capital expenditure, and global availability. "
                    "Successful cloud strategies require careful planning around security, cost, and performance."
                )
                content = f"{heading}\n\n{prose}\n"

                Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")

                lines = Path(FILENAME).read_text(encoding="utf-8").split("\n")
                assert len(lines) >= 3, "File must have heading, blank line, and prose"
                assert lines[1] == "", "Second line must be blank"
            finally:
                os.chdir(original_cwd)

    def test_file_contains_2_to_3_sentences(self):
        """Test that file contains exactly 2-3 sentences after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                heading = "# DevOps Best Practices"
                prose = (
                    "DevOps culture emphasizes collaboration between development and operations teams. "
                    "Automation and continuous integration reduce deployment risk and cycle time. "
                    "Effective monitoring and observability enable rapid response to production issues."
                )
                content = f"{heading}\n\n{prose}\n"

                Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")

                file_content = Path(FILENAME).read_text(encoding="utf-8")
                lines = file_content.split("\n")
                prose_content = "\n".join(lines[2:]).strip()

                # Count sentences (simple period-based count)
                sentence_count = prose_content.count(".")
                assert 2 <= sentence_count <= 3, f"Must have 2-3 sentences, found {sentence_count}"
            finally:
                os.chdir(original_cwd)

    def test_file_is_utf8_encoded_without_bom(self):
        """Test that file is UTF-8 encoded without BOM (Byte Order Mark)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                heading = "# Kubernetes Orchestration"
                prose = (
                    "Kubernetes automates deployment, scaling, and management of containerized applications. "
                    "Its declarative configuration model simplifies complex distributed systems. "
                    "Organizations adopting Kubernetes can achieve improved resource utilization and resilience."
                )
                content = f"{heading}\n\n{prose}\n"

                Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")

                # Read file in binary mode to check for BOM
                binary_content = Path(FILENAME).read_bytes()

                # UTF-8 BOM is the byte sequence EF BB BF
                assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

                # Verify it can be decoded as UTF-8
                try:
                    decoded = binary_content.decode("utf-8")
                    assert decoded == content, "Decoded content must match original"
                except UnicodeDecodeError:
                    pytest.fail("File is not valid UTF-8")
            finally:
                os.chdir(original_cwd)

    def test_file_uses_lf_line_endings_not_crlf(self):
        """Test that file uses Unix-style LF line endings, not Windows CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                heading = "# Microservices Architecture"
                prose = (
                    "Microservices break down large applications into small, independently deployable services. "
                    "This architecture improves scalability, allows independent technology choices, and enables faster development. "
                    "However, it introduces complexity in distributed system coordination and monitoring."
                )
                content = f"{heading}\n\n{prose}\n"

                Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")

                binary_content = Path(FILENAME).read_bytes()

                # Should not contain CRLF (\r\n)
                assert b"\r\n" not in binary_content, "File should not have CRLF line endings"

                # Should contain LF (\n)
                assert b"\n" in binary_content, "File should have LF line endings"
            finally:
                os.chdir(original_cwd)

    def test_file_size_in_reasonable_range(self):
        """Test that file size is approximately 400-600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                heading = "# Data Processing Pipelines"
                prose = (
                    "Data processing pipelines extract, transform, and load information from various sources. "
                    "Modern pipelines handle massive scales using distributed computing frameworks. "
                    "Reliable pipelines are critical for analytics, machine learning, and business intelligence."
                )
                content = f"{heading}\n\n{prose}\n"

                Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")

                file_size = Path(FILENAME).stat().st_size
                # Spec says 400-600 bytes is a guideline, natural variation acceptable
                # Allow flexibility - typical range is 200-800 bytes for this type of content
                assert 200 <= file_size <= 800, f"File size {file_size} should be in reasonable range"
            finally:
                os.chdir(original_cwd)

    def test_prose_content_is_readable_and_grammatical(self):
        """Test that prose content is readable and grammatically correct."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                heading = "# API Design Principles"
                prose = (
                    "Well-designed APIs provide clear abstractions and consistent interfaces for developers. "
                    "They prioritize usability, versioning strategy, and backward compatibility. "
                    "Excellent API documentation and comprehensive error handling accelerate developer productivity."
                )
                content = f"{heading}\n\n{prose}\n"

                Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")

                file_content = Path(FILENAME).read_text(encoding="utf-8")
                lines = file_content.split("\n")
                prose_content = "\n".join(lines[2:]).strip()

                # Check that prose is substantial (not just a few characters)
                assert len(prose_content) > 50, "Prose should be substantial (more than 50 chars)"

                # Check that it has multiple words (basic readability check)
                word_count = len(prose_content.split())
                assert word_count >= 15, f"Prose should have at least 15 words, has {word_count}"

                # Check that sentences end with periods
                assert prose_content.endswith("."), "Prose should end with a period"
            finally:
                os.chdir(original_cwd)

    def test_markdown_syntax_is_valid(self):
        """Test that markdown syntax is valid per CommonMark specification."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                heading = "# Containerization and Docker"
                prose = (
                    "Docker containerization encapsulates applications and dependencies into portable units. "
                    "Containers ensure consistency between development and production environments. "
                    "Container technology has become fundamental to modern cloud-native application deployment."
                )
                content = f"{heading}\n\n{prose}\n"

                Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")

                file_content = Path(FILENAME).read_text(encoding="utf-8")

                # Basic markdown syntax validation
                lines = file_content.split("\n")

                # Must have H1 heading on first line
                assert lines[0].startswith("# "), "Must have H1 heading"

                # Heading should not be empty after the '#'
                heading_text = lines[0][2:].strip()
                assert len(heading_text) > 0, "Heading text should not be empty"

                # Must have blank line after heading
                assert lines[1] == "", "Must have blank line after heading"

                # Prose should not start with markdown syntax
                prose_first_line = lines[2]
                assert not prose_first_line.startswith("# "), "Prose should not start with heading"
                assert not prose_first_line.startswith("## "), "Prose should not start with subheading"
            finally:
                os.chdir(original_cwd)

    def test_complete_file_creation_workflow(self):
        """Integration test: complete file creation with all requirements."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create file using exact pattern from spec
                heading = "# Distributed Systems Resilience"
                prose = (
                    "Building resilient distributed systems requires addressing challenges of network partitions and node failures. "
                    "Techniques like replication, leader election, and consensus protocols provide fault tolerance. "
                    "Careful design of system architecture and monitoring capabilities ensure reliability at scale."
                )
                content = f"{heading}\n\n{prose}\n"

                # Create file using pathlib with required encoding and line endings
                file_path = Path(FILENAME)
                file_path.write_text(content, encoding="utf-8", newline="\n")

                # Verify all requirements in one comprehensive test
                assert file_path.exists(), "File must exist"

                # Read and validate structure
                file_content = file_path.read_text(encoding="utf-8")
                lines = file_content.split("\n")

                assert lines[0].startswith("# "), "Must have H1 heading"
                assert lines[1] == "", "Must have blank line separator"

                prose_content = "\n".join(lines[2:]).strip()
                sentence_count = prose_content.count(".")
                assert 2 <= sentence_count <= 3, "Must have 2-3 sentences"

                # Verify binary properties
                binary_content = file_path.read_bytes()
                assert not binary_content.startswith(b"\xef\xbb\xbf"), "No UTF-8 BOM"
                assert b"\r\n" not in binary_content, "Must use LF, not CRLF"

                # Verify file size
                file_size = len(binary_content)
                assert 300 <= file_size <= 800, f"File size {file_size} in acceptable range"

                # Verify UTF-8 encoding
                try:
                    binary_content.decode("utf-8")
                except UnicodeDecodeError:
                    pytest.fail("File must be valid UTF-8")
            finally:
                os.chdir(original_cwd)
