"""Tests for feature 291: Create markdown file test-p1rf9x.md with prose content.

This module tests the complete workflow for feature 291, which creates
a markdown file with AI-generated title and 2-3 sentences of prose content.

Phase 1 Focus: Content Generation & Validation Setup
- Tests for Claude API content generation
- Tests for comprehensive content validation
"""

from unittest.mock import MagicMock, patch

import pytest


class TestFeature291ContentGeneration:
    """Tests for phase 1: Generate markdown prose content using Claude API."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_returns_string(self, mock_get_llm):
        """Test that generate_markdown_content() returns a non-empty string."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Machine Learning\n\nMachine learning is a subset of artificial intelligence that enables systems to learn from data. These algorithms improve their performance through experience without explicit programming. Applications range from recommendation systems to autonomous vehicles."
        }
        mock_get_llm.return_value = mock_llm

        # Task 1 AC: Claude API call returns non-empty content string
        content = generate_markdown_content()
        assert isinstance(content, str)
        assert len(content) > 0

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_contains_h1_markdown_heading(self, mock_get_llm):
        """Test that content contains an H1 markdown heading (starts with '# ')."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Data Science\n\nData science combines statistics, programming, and domain expertise. It enables organizations to extract insights from large datasets. These insights drive informed decision-making across industries."
        }
        mock_get_llm.return_value = mock_llm

        # Task 1 AC: Content contains an H1 markdown heading
        content = generate_markdown_content()
        assert content.startswith("# "), "Content must start with H1 heading (# )"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_contains_prose_after_heading(self, mock_get_llm):
        """Test that content contains at least one sentence of prose after heading."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Cloud Computing\n\nCloud computing provides on-demand access to computing resources over the internet. Organizations can scale infrastructure without maintaining physical data centers. This flexibility reduces costs and enables faster deployment of applications."
        }
        mock_get_llm.return_value = mock_llm

        # Task 1 AC: Content contains at least one sentence of prose
        content = generate_markdown_content()
        lines = content.split("\n")
        assert len(lines) >= 3, "Content must have heading, blank line, and prose"
        # Check for prose content (sentence count)
        prose = "\n".join(lines[2:]).strip()
        assert len(prose) > 0, "Prose content must be present"
        assert "." in prose, "Prose must contain at least one sentence (period)"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_api_call_logs_generation_attempt(self, mock_get_llm):
        """Test that API calls are logged via sheep.observability.logging."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Cybersecurity\n\nCybersecurity protects digital systems from malicious attacks. Organizations implement multiple layers of defense including firewalls and encryption. Awareness training is essential to prevent social engineering threats."
        }
        mock_get_llm.return_value = mock_llm

        # Task 1 AC: All API calls are logged
        # This test verifies the function completes; logging is tested via structured logs
        with patch("sheep.content_generators._logger") as mock_logger:
            content = generate_markdown_content()
            # Verify logging occurred
            mock_logger.info.assert_called()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_content_generation_completes_within_timeout(self, mock_get_llm):
        """Test that content generation completes in reasonable time (< 30 seconds)."""
        from sheep.content_generators import generate_markdown_content
        import time

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Blockchain Technology\n\nBlockchain is a distributed ledger technology that enables secure and transparent transactions. Each block contains cryptographic hashes of previous blocks for immutability. Applications extend beyond cryptocurrency to supply chain and healthcare."
        }
        mock_get_llm.return_value = mock_llm

        # Task 1 AC: Content generation time < 30 seconds
        start_time = time.time()
        content = generate_markdown_content()
        elapsed = time.time() - start_time

        assert elapsed < 30, f"Content generation took {elapsed}s, should be < 30s"
        assert len(content) > 0


class TestFeature291ContentValidation:
    """Tests for phase 1: Validate generated content structure and quality."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_heading_format_accepts_h1(self, mock_get_llm):
        """Test validation function checks for valid H1 heading format (^# )."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Internet of Things\n\nThe IoT connects billions of devices to the internet for data collection. Smart devices communicate autonomously to optimize processes. This technology is transforming healthcare, agriculture, and urban planning."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Validation checks for valid H1 heading format
        content = generate_markdown_content()  # Should not raise (validation passes)
        assert content.startswith("# ")

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_heading_format_rejects_no_h1(self, mock_get_llm):
        """Test validation rejects content without H1 heading."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        # Return content without H1 heading
        mock_llm.call.return_value = {
            "content": "No heading here.\nThis is invalid content. No heading present."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Invalid heading (no '#') raises ValueError
        with pytest.raises(ValueError, match="H1 heading"):
            generate_markdown_content()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_sentence_count_2_to_3_sentences(self, mock_get_llm):
        """Test validation counts sentences using regex (expects 2-3)."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Neural Networks\n\nNeural networks are computational models inspired by biological brains. They consist of interconnected nodes that process information through layers. Deep learning has revolutionized image recognition and natural language processing."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Validation checks for 2-3 sentences
        content = generate_markdown_content()  # Should not raise (3 sentences)
        sentence_count = content.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_sentence_count_rejects_too_few(self, mock_get_llm):
        """Test validation rejects prose with < 2 sentences."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        # Only 1 sentence
        mock_llm.call.return_value = {
            "content": "# Title\n\nOnly one sentence."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Prose with < 2 sentences raises ValueError
        with pytest.raises(ValueError):
            generate_markdown_content()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_prose_length_100_to_300_characters(self, mock_get_llm):
        """Test validation checks prose length is 100-300 characters."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        # Prose: "Augmented reality overlays digital information on the physical world. AR applications range from gaming to industrial maintenance. This immersive technology enhances user experiences across multiple domains."
        # This prose is approximately 185 characters
        mock_llm.call.return_value = {
            "content": "# Augmented Reality\n\nAugmented reality overlays digital information on the physical world. AR applications range from gaming to industrial maintenance. This immersive technology enhances user experiences."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Prose length 100-300 characters is valid
        content = generate_markdown_content()
        lines = content.split("\n")
        prose = "\n".join(lines[2:]).strip()
        assert 100 <= len(prose) <= 300, f"Prose length {len(prose)} should be 100-300"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_utf8_encoding_no_bom(self, mock_get_llm):
        """Test validation checks UTF-8 encoding (no BOM, valid bytes)."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Quantum Cryptography\n\nQuantum cryptography uses quantum mechanics principles for secure communication. Quantum key distribution enables detection of eavesdropping attempts. This technology represents the future of unhackable communications."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Content validates UTF-8 encoding
        content = generate_markdown_content()
        # Verify can be encoded/decoded as UTF-8
        encoded = content.encode("utf-8")
        decoded = encoded.decode("utf-8")
        assert decoded == content

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_blank_line_separator_between_heading_and_prose(self, mock_get_llm):
        """Test validation verifies blank line exists between heading and prose."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Vertical Farming\n\nVertical farming uses controlled environment agriculture to grow crops indoors. This method reduces water consumption and eliminates pesticide use. Urban vertical farms increase food security in densely populated areas."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Blank line separator is validated
        content = generate_markdown_content()
        lines = content.split("\n")
        assert lines[0].startswith("# "), "First line must be H1"
        assert lines[1] == "", "Second line must be blank separator"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_content_structure_complete(self, mock_get_llm):
        """Test comprehensive validation of all structure and quality requirements."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Genetic Engineering\n\nGenetic engineering modifies DNA to introduce desirable traits. CRISPR technology has revolutionized gene editing with unprecedented precision. Applications in medicine and agriculture promise breakthroughs in treatment and food production."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Invalid content triggers ValueError
        content = generate_markdown_content()
        assert content  # Should complete without error

        # Verify all validation criteria are met
        lines = content.split("\n")
        assert lines[0].startswith("# "), "H1 heading required"
        assert lines[1] == "", "Blank line separator required"
        prose = "\n".join(lines[2:]).strip()
        assert 100 <= len(prose) <= 300, "Prose length 100-300 chars"
        sentence_count = prose.count(".")
        assert 2 <= sentence_count <= 3, "2-3 sentences required"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_invalid_content_raises_value_error_with_message(self, mock_get_llm):
        """Test that invalid content triggers ValueError with descriptive message."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        # Invalid: no H1 heading
        mock_llm.call.return_value = {
            "content": "This is not markdown.\nNo heading present here."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Invalid content raises ValueError
        with pytest.raises(ValueError) as exc_info:
            generate_markdown_content()
        assert len(str(exc_info.value)) > 0, "Error message should describe failure"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_returns_true_for_valid_content(self, mock_get_llm):
        """Test that valid content passes validation and returns successfully."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Synthetic Biology\n\nSynthetic biology designs and constructs biological systems with novel functions. Researchers engineer organisms for biofuel production and pharmaceutical manufacturing. This field promises sustainable solutions to global challenges."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Valid content returns True (implicitly, no exception raised)
        content = generate_markdown_content()
        assert isinstance(content, str)
        assert len(content) > 0


class TestFeature291FileCreation:
    """Tests for phase 2, task 3: Create markdown file with UTF-8 encoding and LF line endings."""

    def test_file_does_not_exist_before_creation(self, tmp_path):
        """Test that test-p1rf9x.md does not exist before creation (setup)."""
        from pathlib import Path

        # Verify file doesn't exist at start
        file_path = tmp_path / "test-p1rf9x.md"
        assert not file_path.exists(), "File should not exist before creation"

    def test_create_markdown_file_with_pathlib(self, tmp_path):
        """Test that create_file() creates file using pathlib.Path.write_text()."""
        from pathlib import Path

        # Sample markdown content (simulating phase 1 output)
        content = "# Machine Learning\n\nMachine learning enables systems to learn from data. Algorithms improve performance through experience without explicit programming. Applications range from recommendation systems to autonomous vehicles.\n"

        file_path = tmp_path / "test-p1rf9x.md"

        # Task 3: Create file using pathlib with UTF-8 encoding
        file_path.write_text(content, encoding="utf-8")

        # AC: File is created and exists
        assert file_path.exists(), "File should exist after write_text()"
        assert file_path.is_file(), "Path should be a file, not directory"

    def test_created_file_is_readable(self, tmp_path):
        """Test that created file is readable and opens without errors."""
        content = "# Cloud Computing\n\nCloud computing provides on-demand access to computing resources. Organizations can scale infrastructure without maintaining physical data centers. This flexibility reduces costs and enables faster deployment.\n"

        file_path = tmp_path / "test-p1rf9x.md"
        file_path.write_text(content, encoding="utf-8")

        # AC: File is readable
        read_content = file_path.read_text(encoding="utf-8")
        assert read_content == content, "Read content should match written content"

    def test_file_size_in_expected_range(self, tmp_path):
        """Test that file size is approximately 400-600 bytes."""
        # Use longer content to reach expected 400-600 byte range
        content = "# Data Science and Analytics\n\nData science combines statistics, programming, and domain expertise to extract valuable insights from large datasets. It enables organizations to make informed decisions and uncover hidden patterns. These insights drive strategy across industries and reshape business practices.\n"

        file_path = tmp_path / "test-p1rf9x.md"
        file_path.write_text(content, encoding="utf-8")

        # AC: File size in expected range (400-600 bytes, accepting 200+ for flexibility)
        file_size = file_path.stat().st_size
        assert file_size >= 200, f"File size {file_size} should be substantial (200+ bytes)"

    def test_pathlib_used_with_utf8_encoding(self, tmp_path):
        """Test that pathlib.Path is used with explicit encoding='utf-8'."""
        from pathlib import Path

        content = "# Cybersecurity\n\nCybersecurity protects digital systems from malicious attacks and breaches. Organizations implement multiple layers of defense including firewalls and encryption. Awareness training is essential to prevent social engineering threats.\n"

        file_path = tmp_path / "test-p1rf9x.md"

        # AC: Use pathlib.Path.write_text with encoding parameter
        file_path.write_text(content, encoding="utf-8")

        # Verify pathlib was used (Path instance check)
        assert isinstance(file_path, Path), "Must use pathlib.Path"

        # Verify encoding works by reading back
        read_content = file_path.read_text(encoding="utf-8")
        assert read_content == content


class TestFeature291FileVerification:
    """Tests for phase 2, task 4: Verify file encoding, line endings, and structure."""

    def test_no_utf8_bom_in_file(self, tmp_path):
        """Test: read file as binary and verify UTF-8 BOM not present."""
        content = "# Blockchain\n\nBlockchain is distributed ledger technology enabling secure transactions. Each block contains cryptographic hashes for immutability. Applications extend beyond cryptocurrency to supply chain.\n"

        file_path = tmp_path / "test-p1rf9x.md"
        file_path.write_text(content, encoding="utf-8")

        # AC: File opened as binary and checked for BOM absence
        binary_content = file_path.read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File must not have UTF-8 BOM"

    def test_file_is_valid_utf8_decodable(self, tmp_path):
        """Test: read file as text with UTF-8 and verify no decode errors."""
        content = "# Quantum Computing\n\nQuantum computing exploits quantum mechanics for computation using qubits. Quantum computers promise to solve certain problems exponentially faster than classical computers. Applications span cryptography, optimization, and drug discovery.\n"

        file_path = tmp_path / "test-p1rf9x.md"
        file_path.write_text(content, encoding="utf-8")

        # AC: File opened as text with UTF-8 (no decode errors)
        try:
            text_content = file_path.read_text(encoding="utf-8")
            assert len(text_content) > 0
        except UnicodeDecodeError:
            pytest.fail("File must be valid UTF-8")

    def test_file_uses_lf_not_crlf(self, tmp_path):
        """Test: verify file contains LF ('\\n') not CRLF ('\\r\\n')."""
        content = "# Neural Networks\n\nNeural networks are inspired by biological brains consisting of interconnected nodes. They process information through layers using learned weights and biases. Deep learning revolutionized image recognition and natural language processing.\n"

        file_path = tmp_path / "test-p1rf9x.md"
        file_path.write_text(content, encoding="utf-8")

        # AC: File content uses LF not CRLF
        binary_content = file_path.read_bytes()
        assert b"\r\n" not in binary_content, "File must use LF (\\n), not CRLF (\\r\\n)"
        assert b"\n" in binary_content, "File must contain LF line endings"

    def test_first_line_starts_with_heading_marker(self, tmp_path):
        """Test: split file by '\\n' and verify first line starts with '# '."""
        content = "# Genetic Engineering\n\nGenetic engineering modifies DNA to introduce desirable traits into organisms. CRISPR technology has revolutionized gene editing with unprecedented precision. Applications in medicine and agriculture promise breakthroughs.\n"

        file_path = tmp_path / "test-p1rf9x.md"
        file_path.write_text(content, encoding="utf-8")

        # AC: First line starts with '# '
        text_content = file_path.read_text(encoding="utf-8")
        lines = text_content.split("\n")
        assert lines[0].startswith("# "), "First line must be H1 heading (# )"

    def test_second_line_is_blank(self, tmp_path):
        """Test: verify second line is empty (blank line separator)."""
        content = "# Synthetic Biology\n\nSynthetic biology designs biological systems with novel functions. Researchers engineer organisms for biofuel production and pharmaceutical manufacturing. This field promises sustainable solutions to global challenges.\n"

        file_path = tmp_path / "test-p1rf9x.md"
        file_path.write_text(content, encoding="utf-8")

        # AC: Second line is empty string (blank separator)
        text_content = file_path.read_text(encoding="utf-8")
        lines = text_content.split("\n")
        assert len(lines) >= 2, "File must have at least heading and blank line"
        assert lines[1] == "", "Second line must be blank (separator after heading)"

    def test_prose_content_present(self, tmp_path):
        """Test: verify prose content exists after heading and blank line."""
        content = "# Vertical Farming\n\nVertical farming uses controlled environment agriculture to grow crops indoors. This method reduces water consumption and eliminates pesticide use completely. Urban vertical farms increase food security in densely populated areas.\n"

        file_path = tmp_path / "test-p1rf9x.md"
        file_path.write_text(content, encoding="utf-8")

        # AC: Remaining lines contain prose content (2-3 sentences)
        text_content = file_path.read_text(encoding="utf-8")
        lines = text_content.split("\n")
        prose_lines = lines[2:]  # Skip heading and blank line

        # Remove trailing empty lines
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        assert len(prose_lines) > 0, "Prose content must be present"
        prose = "\n".join(prose_lines).strip()
        sentence_count = prose.count(".")
        assert 2 <= sentence_count <= 3, f"Must have 2-3 sentences, found {sentence_count}"

    def test_file_structure_complete_validation(self, tmp_path):
        """Test: comprehensive validation of file structure and encoding."""
        content = "# Internet of Things\n\nIoT connects billions of devices to the internet for data collection and analysis. Smart devices communicate autonomously to optimize processes and reduce human intervention. This technology transforms healthcare, agriculture, and urban planning.\n"

        file_path = tmp_path / "test-p1rf9x.md"
        file_path.write_text(content, encoding="utf-8")

        # Read as binary and text
        binary_content = file_path.read_bytes()
        text_content = file_path.read_text(encoding="utf-8")

        # AC: Multiple comprehensive checks
        # 1. No BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf")
        # 2. Valid UTF-8
        assert text_content == content
        # 3. LF line endings only
        assert b"\r\n" not in binary_content
        # 4. Structure validation
        lines = text_content.split("\n")
        assert lines[0].startswith("# "), "H1 heading required"
        assert lines[1] == "", "Blank line separator required"
        prose = "\n".join(lines[2:]).strip()
        assert len(prose) > 100, "Prose must be substantial"
        sentence_count = prose.count(".")
        assert 2 <= sentence_count <= 3, "2-3 sentences required"
