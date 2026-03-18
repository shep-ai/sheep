"""Tests for feature 100 Phase 2: File Creation & Encoding."""

from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from sheep.content_generators import (
    write_markdown_file,
    validate_markdown_file,
    generate_markdown_content,
)


class TestPhase2FileCreation:
    """Task 2-1: Write markdown file to repository root."""

    def test_file_does_not_exist_before_creation(self):
        """Test that test-h49uqm.md does not exist initially."""
        repo_root = Path.cwd()
        test_file = repo_root / "test-h49uqm.md"

        # Ensure file doesn't exist initially (cleanup from previous runs)
        if test_file.exists():
            test_file.unlink()

        assert not test_file.exists(), "test-h49uqm.md should not exist initially"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_file_is_created_at_repository_root(self, mock_get_llm):
        """Test that file exists at correct path after writing."""
        # Setup mock content
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Distributed Systems\n\nDistributed systems enable fault tolerance and scalability. Consensus algorithms coordinate state across multiple nodes. Eventual consistency manages trade-offs between availability and correctness.\n"
        }
        mock_get_llm.return_value = mock_llm

        # Generate content
        content = generate_markdown_content()

        # Write file
        filepath = write_markdown_file(content, "test-h49uqm.md")

        # Assert file exists
        assert Path(filepath).exists(), f"File should exist at {filepath}"

        # Cleanup
        Path(filepath).unlink()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_file_contains_exact_content(self, mock_get_llm):
        """Test that file contents match input exactly."""
        # Setup mock content
        expected_content = "# Software Engineering\n\nVersion control systems manage code evolution. Automated testing ensures code quality and reliability. Continuous integration streamlines deployment workflows.\n"
        mock_llm = MagicMock()
        mock_llm.call.return_value = {"content": expected_content}
        mock_get_llm.return_value = mock_llm

        # Generate and write
        content = generate_markdown_content()
        filepath = write_markdown_file(content, "test-h49uqm.md")

        # Read back and verify
        written_content = Path(filepath).read_text(encoding="utf-8")
        assert written_content == expected_content, "File content should match exactly"

        # Cleanup
        Path(filepath).unlink()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_file_size_within_specification_bounds(self, mock_get_llm):
        """Test that file size is within 320-600 byte range."""
        # Setup mock content with longer prose to meet size requirement
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Cloud Infrastructure and Modern Deployment Patterns\n\nCloud platforms provide elasticity and global reach for application workloads. Containerization enables consistent deployment across heterogeneous environments and simplifies dependency management. Orchestration tools automate scaling, updates, and resource allocation in distributed systems.\n"
        }
        mock_get_llm.return_value = mock_llm

        # Generate and write
        content = generate_markdown_content()
        filepath = write_markdown_file(content, "test-h49uqm.md")

        # Check file size
        file_size = Path(filepath).stat().st_size
        assert 320 <= file_size <= 600, f"File size {file_size} should be between 320-600 bytes"

        # Cleanup
        Path(filepath).unlink()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_file_is_accessible_and_readable(self, mock_get_llm):
        """Test that file is accessible and readable."""
        # Setup mock content
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Network Protocols\n\nTCP/IP provides reliable communication across networks. DNS resolves domain names to IP addresses. HTTP defines request/response semantics for web communication.\n"
        }
        mock_get_llm.return_value = mock_llm

        # Generate and write
        content = generate_markdown_content()
        filepath = write_markdown_file(content, "test-h49uqm.md")

        # Test readability
        try:
            Path(filepath).read_text(encoding="utf-8")
            assert True, "File should be readable"
        except Exception as e:
            pytest.fail(f"File should be readable: {e}")

        # Cleanup
        Path(filepath).unlink()


class TestPhase2FileEncoding:
    """Task 2-2: Verify file encoding and line endings."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_file_has_no_utf8_bom(self, mock_get_llm):
        """Test that file does not have UTF-8 BOM marker."""
        # Setup mock content
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Data Structures\n\nArrays provide fast random access with fixed memory layout. Hash tables enable constant-time lookups with proper design. Trees organize hierarchical relationships efficiently.\n"
        }
        mock_get_llm.return_value = mock_llm

        # Generate and write
        content = generate_markdown_content()
        filepath = write_markdown_file(content, "test-h49uqm.md")

        # Read as bytes and check for BOM
        file_bytes = Path(filepath).read_bytes()
        assert not file_bytes.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

        # Cleanup
        Path(filepath).unlink()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_file_uses_lf_line_endings(self, mock_get_llm):
        """Test that file uses LF (\\n) line endings, not CRLF."""
        # Setup mock content with longer prose to meet size requirement
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Compiler Design and Implementation\n\nLexical analysis tokenizes source code input into meaningful tokens for further processing. Syntax analysis builds abstract syntax trees to represent program structure. Code generation produces executable instructions that implement the original source semantics.\n"
        }
        mock_get_llm.return_value = mock_llm

        # Generate and write
        content = generate_markdown_content()
        filepath = write_markdown_file(content, "test-h49uqm.md")

        # Read as bytes and check for CRLF
        file_bytes = Path(filepath).read_bytes()
        assert b"\r\n" not in file_bytes, "File should use LF endings, not CRLF"
        assert b"\r" not in file_bytes, "File should not have CR characters"

        # Cleanup
        Path(filepath).unlink()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_file_is_valid_utf8(self, mock_get_llm):
        """Test that file can be decoded as UTF-8 without errors."""
        # Setup mock content
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Machine Learning\n\nNeural networks learn complex patterns from data. Training optimizes weights through backpropagation. Validation prevents overfitting during model development.\n"
        }
        mock_get_llm.return_value = mock_llm

        # Generate and write
        content = generate_markdown_content()
        filepath = write_markdown_file(content, "test-h49uqm.md")

        # Try to decode as UTF-8
        file_bytes = Path(filepath).read_bytes()
        try:
            file_bytes.decode("utf-8")
            assert True, "File should be valid UTF-8"
        except UnicodeDecodeError as e:
            pytest.fail(f"File should be valid UTF-8: {e}")

        # Cleanup
        Path(filepath).unlink()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_file_is_within_specification_size(self, mock_get_llm):
        """Test that file size is within 320-600 byte specification."""
        # Setup mock content with longer prose to meet size requirement
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# API Gateway Architecture and Microservices\n\nAPI gateways aggregate distributed services and provide unified endpoints for client applications and internal services. Rate limiting protects backend resources from overload and ensures fair usage patterns across consumers. Authentication validates client credentials and permissions before routing requests to appropriate backend services.\n"
        }
        mock_get_llm.return_value = mock_llm

        # Generate and write
        content = generate_markdown_content()
        filepath = write_markdown_file(content, "test-h49uqm.md")

        # Check file size
        file_size = Path(filepath).stat().st_size
        assert 320 <= file_size <= 600, f"File size {file_size} should be between 320-600"

        # Cleanup
        Path(filepath).unlink()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_file_markdown_syntax_is_valid(self, mock_get_llm):
        """Test that markdown syntax is valid per specification."""
        # Setup mock content with longer prose to meet size requirement
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Container Orchestration and Kubernetes\n\nKubernetes automates deployment, scaling, and management of containerized applications. Services provide stable network endpoints for pod communication and enable load balancing. ConfigMaps and secrets manage application configuration and sensitive data.\n"
        }
        mock_get_llm.return_value = mock_llm

        # Generate and write
        content = generate_markdown_content()
        filepath = write_markdown_file(content, "test-h49uqm.md")

        # Validate markdown file
        try:
            validate_markdown_file(filepath)
            assert True, "File should have valid markdown syntax"
        except ValueError as e:
            pytest.fail(f"File markdown validation failed: {e}")

        # Cleanup
        Path(filepath).unlink()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_complete_verification_workflow(self, mock_get_llm):
        """Test the complete verification workflow for file creation."""
        # Setup mock content with longer prose to meet size requirement
        mock_llm = MagicMock()
        valid_content = "# Security Protocols and Cryptography\n\nEncryption protects data confidentiality in transit and at rest through mathematical algorithms. Authentication verifies identity through credentials, tokens, or biometric measures. Authorization controls resource access based on user roles and permissions.\n"
        mock_llm.call.return_value = {"content": valid_content}
        mock_get_llm.return_value = mock_llm

        # Step 1: Generate content
        content = generate_markdown_content()
        assert isinstance(content, str), "Content should be string"

        # Step 2: Write file
        filepath = write_markdown_file(content, "test-h49uqm.md")
        assert Path(filepath).exists(), "File should exist"

        # Step 3: Verify encoding
        file_bytes = Path(filepath).read_bytes()
        assert not file_bytes.startswith(b"\xef\xbb\xbf"), "Should have no BOM"
        assert b"\r\n" not in file_bytes, "Should use LF endings"

        # Step 4: Verify file validation
        try:
            validate_markdown_file(filepath)
            assert True, "Validation should pass"
        except ValueError as e:
            pytest.fail(f"Validation should pass: {e}")

        # Cleanup
        Path(filepath).unlink()
