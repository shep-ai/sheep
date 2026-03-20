"""Tests for feature 126, Phase 2, Task 2-1: Generate Prose via Claude API."""

import pytest
import os
import re
import subprocess
from unittest.mock import patch, MagicMock


class TestGenerateProseReturnType:
    """Tests for return type of generate_prose()."""

    def test_generate_prose_returns_dict(self):
        """Test that generate_prose() returns a dictionary."""
        from prose_generation import generate_prose

        # Mock the subprocess.run to avoid actual API call
        mock_response = {
            "title": "The Power of Rain",
            "prose": "Rain is essential for life on Earth. It replenishes freshwater in lakes, rivers, and aquifers. This natural cycle sustains ecosystems and human civilizations across the globe."
        }

        with patch("prose_generation.os.environ.get") as mock_env:
            mock_env.return_value = "fake-api-key"
            with patch("prose_generation.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='{"content": [{"text": "{\\"title\\": \\"The Power of Rain\\", \\"prose\\": \\"Rain is essential for life on Earth. It replenishes freshwater in lakes, rivers, and aquifers. This natural cycle sustains ecosystems and human civilizations across the globe.\\"}"}]}',
                    returncode=0
                )

                result = generate_prose()
                assert isinstance(result, dict), "generate_prose() should return a dictionary"

    def test_generate_prose_returns_dict_with_title_key(self):
        """Test that returned dict has 'title' key."""
        from prose_generation import generate_prose

        with patch("prose_generation.os.environ.get") as mock_env:
            mock_env.return_value = "fake-api-key"
            with patch("prose_generation.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='{"content": [{"text": "{\\"title\\": \\"The Power of Rain\\", \\"prose\\": \\"Rain is essential for life on Earth. It replenishes freshwater in lakes, rivers, and aquifers. This natural cycle sustains ecosystems and human civilizations across the globe.\\"}"}]}',
                    returncode=0
                )

                result = generate_prose()
                assert "title" in result, "Returned dict should have 'title' key"

    def test_generate_prose_returns_dict_with_prose_key(self):
        """Test that returned dict has 'prose' key."""
        from prose_generation import generate_prose

        with patch("prose_generation.os.environ.get") as mock_env:
            mock_env.return_value = "fake-api-key"
            with patch("prose_generation.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='{"content": [{"text": "{\\"title\\": \\"The Power of Rain\\", \\"prose\\": \\"Rain is essential for life on Earth. It replenishes freshwater in lakes, rivers, and aquifers. This natural cycle sustains ecosystems and human civilizations across the globe.\\"}"}]}',
                    returncode=0
                )

                result = generate_prose()
                assert "prose" in result, "Returned dict should have 'prose' key"


class TestGenerateProseTitle:
    """Tests for the title field in generate_prose() result."""

    def test_title_is_non_empty_string(self):
        """Test that returned title is a non-empty string."""
        from prose_generation import generate_prose

        with patch("prose_generation.os.environ.get") as mock_env:
            mock_env.return_value = "fake-api-key"
            with patch("prose_generation.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='{"content": [{"text": "{\\"title\\": \\"The Power of Rain\\", \\"prose\\": \\"Rain is essential for life on Earth. It replenishes freshwater in lakes, rivers, and aquifers. This natural cycle sustains ecosystems and human civilizations across the globe.\\"}"}]}',
                    returncode=0
                )

                result = generate_prose()
                assert isinstance(result["title"], str), "Title should be a string"
                assert len(result["title"]) > 0, "Title should not be empty"

    def test_title_is_suitable_for_markdown_heading(self):
        """Test that title is suitable for markdown heading (no leading/trailing whitespace, no special chars)."""
        from prose_generation import generate_prose

        with patch("prose_generation.os.environ.get") as mock_env:
            mock_env.return_value = "fake-api-key"
            with patch("prose_generation.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='{"content": [{"text": "{\\"title\\": \\"The Power of Rain\\", \\"prose\\": \\"Rain is essential for life on Earth. It replenishes freshwater in lakes, rivers, and aquifers. This natural cycle sustains ecosystems and human civilizations across the globe.\\"}"}]}',
                    returncode=0
                )

                result = generate_prose()
                title = result["title"]
                # Title should not have leading/trailing whitespace
                assert title == title.strip(), "Title should not have leading/trailing whitespace"
                # Title should be reasonable length for markdown heading
                assert len(title) < 200, "Title should not be excessively long"


class TestGenerateProseProse:
    """Tests for the prose field in generate_prose() result."""

    def test_prose_is_non_empty_string(self):
        """Test that returned prose is a non-empty string."""
        from prose_generation import generate_prose

        with patch("prose_generation.os.environ.get") as mock_env:
            mock_env.return_value = "fake-api-key"
            with patch("prose_generation.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='{"content": [{"text": "{\\"title\\": \\"The Power of Rain\\", \\"prose\\": \\"Rain is essential for life on Earth. It replenishes freshwater in lakes, rivers, and aquifers. This natural cycle sustains ecosystems and human civilizations across the globe.\\"}"}]}',
                    returncode=0
                )

                result = generate_prose()
                assert isinstance(result["prose"], str), "Prose should be a string"
                assert len(result["prose"]) > 0, "Prose should not be empty"

    def test_prose_contains_2_to_3_sentences(self):
        """Test that prose contains exactly 2-3 sentences."""
        from prose_generation import generate_prose

        with patch("prose_generation.os.environ.get") as mock_env:
            mock_env.return_value = "fake-api-key"
            with patch("prose_generation.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='{"content": [{"text": "{\\"title\\": \\"The Power of Rain\\", \\"prose\\": \\"Rain is essential for life on Earth. It replenishes freshwater in lakes, rivers, and aquifers. This natural cycle sustains ecosystems and human civilizations across the globe.\\"}"}]}',
                    returncode=0
                )

                result = generate_prose()
                prose = result["prose"]
                # Count sentences by looking for sentence-ending punctuation
                # A simple heuristic: count periods, question marks, and exclamation points
                sentence_count = len(re.findall(r'[.!?]+', prose))
                assert 2 <= sentence_count <= 3, \
                    f"Prose should contain 2-3 sentences, found {sentence_count}"

    def test_prose_is_grammatically_coherent(self):
        """Test that prose is not obviously malformed."""
        from prose_generation import generate_prose

        with patch("prose_generation.os.environ.get") as mock_env:
            mock_env.return_value = "fake-api-key"
            with patch("prose_generation.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='{"content": [{"text": "{\\"title\\": \\"The Power of Rain\\", \\"prose\\": \\"Rain is essential for life on Earth. It replenishes freshwater in lakes, rivers, and aquifers. This natural cycle sustains ecosystems and human civilizations across the globe.\\"}"}]}',
                    returncode=0
                )

                result = generate_prose()
                prose = result["prose"]
                # Basic checks: not empty, has reasonable length, no excessive whitespace
                assert len(prose) > 20, "Prose should have meaningful content"
                assert "  " not in prose, "Prose should not have excessive whitespace"
                assert prose[0].isupper(), "Prose should start with uppercase letter"


class TestGenerateProseAPIKeyValidation:
    """Tests for ANTHROPIC_API_KEY environment variable validation."""

    def test_raises_error_when_api_key_not_set(self):
        """Test that generate_prose() raises exception when ANTHROPIC_API_KEY not set."""
        from prose_generation import generate_prose

        # Remove ANTHROPIC_API_KEY from environment temporarily
        api_key = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
                generate_prose()
        finally:
            # Restore the API key
            if api_key:
                os.environ["ANTHROPIC_API_KEY"] = api_key

    def test_does_not_raise_when_api_key_set(self):
        """Test that function works when ANTHROPIC_API_KEY is set."""
        from prose_generation import generate_prose

        # Ensure API key is set
        if "ANTHROPIC_API_KEY" not in os.environ:
            pytest.skip("ANTHROPIC_API_KEY not set in test environment")

        with patch("prose_generation.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout='{"content": [{"text": "{\\"title\\": \\"The Power of Rain\\", \\"prose\\": \\"Rain is essential for life on Earth. It replenishes freshwater in lakes, rivers, and aquifers. This natural cycle sustains ecosystems and human civilizations across the globe.\\"}"}]}',
                returncode=0
            )

            # Should not raise an exception
            result = generate_prose()
            assert result is not None


class TestGenerateProseErrorHandling:
    """Tests for error handling in API calls."""

    def test_raises_error_when_subprocess_fails(self):
        """Test that generate_prose() raises exception if subprocess call fails."""
        from prose_generation import generate_prose

        with patch("prose_generation.os.environ.get") as mock_env:
            mock_env.return_value = "fake-api-key"
            with patch("prose_generation.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    returncode=1,
                    stderr="API error: authentication failed"
                )

                with pytest.raises(Exception):
                    generate_prose()

    def test_raises_error_when_response_invalid_json(self):
        """Test that generate_prose() raises exception if response is not valid JSON."""
        from prose_generation import generate_prose

        with patch("prose_generation.os.environ.get") as mock_env:
            mock_env.return_value = "fake-api-key"
            with patch("prose_generation.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout="This is not JSON",
                    returncode=0
                )

                with pytest.raises(Exception):
                    generate_prose()

    def test_raises_error_when_response_missing_title(self):
        """Test that generate_prose() raises exception if response missing 'title'."""
        from prose_generation import generate_prose

        with patch("prose_generation.os.environ.get") as mock_env:
            mock_env.return_value = "fake-api-key"
            with patch("prose_generation.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='{"content": [{"text": "{\\"prose\\": \\"Some prose without title\\"}"}]}',
                    returncode=0
                )

                with pytest.raises(Exception):
                    generate_prose()

    def test_raises_error_when_response_missing_prose(self):
        """Test that generate_prose() raises exception if response missing 'prose'."""
        from prose_generation import generate_prose

        with patch("prose_generation.os.environ.get") as mock_env:
            mock_env.return_value = "fake-api-key"
            with patch("prose_generation.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='{"content": [{"text": "{\\"title\\": \\"Some Title\\"}"}]}',
                    returncode=0
                )

                with pytest.raises(Exception):
                    generate_prose()

    def test_raises_error_with_clear_message_on_api_failure(self):
        """Test that error message is clear and helpful when API call fails."""
        from prose_generation import generate_prose

        with patch("prose_generation.os.environ.get") as mock_env:
            mock_env.return_value = "fake-api-key"
            error_msg = "API rate limit exceeded"
            with patch("prose_generation.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    returncode=1,
                    stderr=error_msg
                )

                with pytest.raises(Exception) as exc_info:
                    generate_prose()

                # Error message should mention the underlying issue
                assert "Claude API" in str(exc_info.value) or "rate limit" in str(exc_info.value) or "API" in str(exc_info.value)
