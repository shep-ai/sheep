#!/usr/bin/env python3
"""
Mocked integration tests for feature 293.

This test suite runs the same integration tests but with mocked API calls,
so they can run without ANTHROPIC_API_KEY configured.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sheep.content_generators import (
    write_markdown_file,
    validate_markdown_file,
    git_add,
    git_commit,
    git_push,
)


def test_complete_workflow_mocked():
    """
    Integration test with mocked content generation.
    """
    representative_content = """# Quantum Computing Fundamentals

Quantum computers leverage the principles of quantum mechanics to perform computations at scales impossible for classical computers. These machines use quantum bits (qubits) that can exist in multiple states simultaneously, allowing them to process vast amounts of information in parallel. The potential applications range from drug discovery to cryptography and optimization problems.
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Initialize git repo
            subprocess.run(["git", "init"], capture_output=True, check=True)
            subprocess.run(["git", "config", "user.email", "test@test.com"], capture_output=True, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], capture_output=True, check=True)

            # Step 1: Use mocked content
            content = representative_content
            filename = "test-integration-mocked.md"

            # Step 2: Write file
            filepath = write_markdown_file(content, filename)
            assert Path(filepath).exists(), "File not created"

            # Step 3: Validate file
            assert validate_markdown_file(filepath), "Validation failed"

            # Step 4: Git add
            add_result = git_add(filename)
            assert "Successfully added" in add_result or "exit code: 0" in add_result

            # Step 5: Git commit
            message = "feat(293): test-integration-mocked.md"
            commit_result = git_commit(message)
            assert "feat(293)" in commit_result or "Committed:" in commit_result

            # Verify git status is clean
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True,
                cwd=temp_dir
            )
            assert status_result.stdout.strip() == "", "Working tree should be clean"

            print("✓ test_complete_workflow_mocked passed")

        finally:
            os.chdir(original_cwd)


def test_file_format_validation():
    """
    Test markdown format validation with representative content.
    """
    valid_content = """# Machine Learning Basics

Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without explicit programming. Algorithms analyze patterns in data to make predictions and decisions autonomously. This technology powers recommendation systems, image recognition, and natural language processing applications.
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Create and validate
            filepath = Path(temp_dir) / "test-format.md"
            filepath.write_text(valid_content)

            # Should pass validation
            assert validate_markdown_file(str(filepath)), "Valid file should pass"

            # Test invalid formats
            invalid_files = {
                "no-heading.md": "Just prose without heading.\n",
                "no-separator.md": "# Title\nProse without blank line.\n",
                "one-sentence.md": "# Title\n\nOnly one sentence.\n",
            }

            for invalid_file, invalid_content in invalid_files.items():
                Path(temp_dir, invalid_file).write_text(invalid_content)
                try:
                    validate_markdown_file(str(Path(temp_dir) / invalid_file))
                    assert False, f"Should have rejected {invalid_file}"
                except ValueError:
                    pass  # Expected

            print("✓ test_file_format_validation passed")

        finally:
            os.chdir(original_cwd)


def test_git_workflow_complete():
    """
    Test complete git workflow without API calls.
    """
    content = """# Cloud Computing Architecture

Cloud computing delivers computing services over the internet, including servers, storage, and databases. This model provides scalability, flexibility, and cost-efficiency compared to traditional on-premises infrastructure. Major cloud providers offer various service models including IaaS, PaaS, and SaaS.
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Initialize repo
            subprocess.run(["git", "init"], capture_output=True, check=True)
            subprocess.run(["git", "config", "user.email", "test@test.com"], capture_output=True, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], capture_output=True, check=True)

            filename = "test-git-workflow.md"

            # Create and add file
            filepath = write_markdown_file(content, filename)
            git_add(filename)

            # Check git status shows staged file
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True,
                cwd=temp_dir
            )
            assert "A " in status.stdout, "File should be staged"

            # Commit
            message = "feat(293): create test-git-workflow.md with prose content"
            git_commit(message)

            # Verify commit is in log
            log = subprocess.run(
                ["git", "log", "--oneline"],
                capture_output=True,
                text=True,
                check=True,
                cwd=temp_dir
            )
            assert "feat(293)" in log.stdout, "Commit should be in log"

            print("✓ test_git_workflow_complete passed")

        finally:
            os.chdir(original_cwd)


def test_prose_validation():
    """
    Test that prose content meets all requirements.
    """
    test_cases = [
        # (title, prose, should_pass)
        ("AI", "One topic. Two sentences here. Three more.", True),  # 3 sentences, valid
        ("Networks", "First sentence about networks. Second sentence.", True),  # 2 sentences, valid
        ("Data", "Only one sentence.", False),  # 1 sentence, invalid
        ("Science", "First. Second. Third. Fourth.", False),  # 4 sentences, invalid
    ]

    for title, prose, should_pass in test_cases:
        content = f"# {title}\n\n{prose}\n"

        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = Path(temp_dir) / "test.md"
            filepath.write_text(content)

            try:
                validate_markdown_file(str(filepath))
                assert should_pass, f"Should have failed: {title}"
            except ValueError:
                assert not should_pass, f"Should have passed: {title}"

    print("✓ test_prose_validation passed")


def test_file_encoding_and_line_endings():
    """
    Test that files have correct encoding and line endings.
    """
    content = """# Data Structures

Data structures organize information in memory for efficient access and modification. Common types include arrays, linked lists, stacks, queues, and trees. Choosing the right data structure significantly impacts algorithm performance and code maintainability.
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = Path(temp_dir) / "test-encoding.md"

        # Write as UTF-8 without BOM
        filepath.write_text(content, encoding="utf-8")

        # Verify UTF-8 encoding
        binary_content = filepath.read_bytes()
        assert not binary_content.startswith(b'\xef\xbb\xbf'), "Should not have UTF-8 BOM"

        # Verify LF line endings (not CRLF)
        assert b'\r\n' not in binary_content, "Should use LF, not CRLF"

        # Verify content is valid UTF-8
        try:
            binary_content.decode('utf-8')
        except UnicodeDecodeError:
            assert False, "Content should be valid UTF-8"

        # Should pass validation
        assert validate_markdown_file(str(filepath)), "Encoding should be valid"

        print("✓ test_file_encoding_and_line_endings passed")


if __name__ == "__main__":
    print("Running Mocked Integration Tests\n" + "=" * 60)

    test_complete_workflow_mocked()
    test_file_format_validation()
    test_git_workflow_complete()
    test_prose_validation()
    test_file_encoding_and_line_endings()

    print("\n" + "=" * 60)
    print("✓ All mocked integration tests passed!")
