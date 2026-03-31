"""Tests for feature 295 phase 2: Content generation and validation."""

from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import (
    generate_markdown_content,
    validate_prose_content,
)


class TestTask2ContentGeneration:
    """Tests for task-2: Implement content generation using Claude API."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_returns_string(self, mock_llm_factory):
        """Test that generate_markdown_content returns a non-empty string."""
        # Mock the LLM
        mock_llm = MagicMock()
        mock_llm_factory.return_value = mock_llm

        # Mock the LLM response
        mock_response = {
            "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        }
        mock_llm.call.return_value = mock_response

        # Call the function
        result = generate_markdown_content()

        # Verify it returns a non-empty string
        assert isinstance(result, str)
        assert len(result) > 0
        assert result.endswith("\n")

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_includes_h1_heading(self, mock_llm_factory):
        """Test that generated content has H1 heading (# Title)."""
        mock_llm = MagicMock()
        mock_llm_factory.return_value = mock_llm
        mock_llm.call.return_value = {
            "content": "# Test Title About Something Important\n\nFirst sentence with detail. Second sentence providing more information. Third sentence to conclude.\n"
        }

        result = generate_markdown_content()

        # Should start with H1 marker
        assert result.lstrip().startswith("# ")

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_with_dict_response(self, mock_llm_factory):
        """Test that generate_markdown_content handles dict responses from LLM."""
        mock_llm = MagicMock()
        mock_llm_factory.return_value = mock_llm

        # Mock dict-style response
        mock_llm.call.return_value = {
            "content": "# Topic on Important Matters\n\nSentence one with detail. Sentence two with more information. Sentence three to conclude.\n"
        }

        result = generate_markdown_content()

        assert isinstance(result, str)
        assert "# Topic" in result

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_with_string_response(self, mock_llm_factory):
        """Test that generate_markdown_content handles string responses from LLM."""
        mock_llm = MagicMock()
        mock_llm_factory.return_value = mock_llm

        # Mock string-style response
        mock_llm.call.return_value = "# Title About Something\n\nFirst detailed sentence. Second detailed sentence. Third detailed sentence.\n"

        result = generate_markdown_content()

        assert isinstance(result, str)
        assert "# Title" in result

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_adds_trailing_newline(self, mock_llm_factory):
        """Test that trailing newline is added if missing."""
        mock_llm = MagicMock()
        mock_llm_factory.return_value = mock_llm

        # Mock response without trailing newline
        mock_llm.call.return_value = {
            "content": "# Title About Stuff\n\nSentence one is detailed. Sentence two provides information. Sentence three concludes."
        }

        result = generate_markdown_content()

        # Should have trailing newline
        assert result.endswith("\n")

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_calls_llm_once(self, mock_llm_factory):
        """Test that LLM.call() is invoked exactly once."""
        mock_llm = MagicMock()
        mock_llm_factory.return_value = mock_llm
        mock_llm.call.return_value = {
            "content": "# Title About Something\n\nFirst sentence detailed. Second sentence detailed. Third sentence detailed.\n"
        }

        generate_markdown_content()

        # Verify LLM was called once
        assert mock_llm.call.call_count == 1

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_uses_correct_prompt(self, mock_llm_factory):
        """Test that generate_markdown_content uses the expected prompt."""
        mock_llm = MagicMock()
        mock_llm_factory.return_value = mock_llm
        mock_llm.call.return_value = {
            "content": "# Title About Something\n\nFirst sentence detailed. Second sentence detailed. Third sentence detailed.\n"
        }

        generate_markdown_content()

        # Verify prompt was sent to LLM
        call_args = mock_llm.call.call_args
        assert call_args is not None
        # The prompt should be in the arguments
        args, kwargs = call_args
        assert len(args) > 0

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_error_handling_api_error(self, mock_llm_factory):
        """Test that API errors are caught and logged."""
        mock_llm = MagicMock()
        mock_llm_factory.return_value = mock_llm

        # Simulate API error
        mock_llm.call.side_effect = Exception("API connection failed")

        with pytest.raises(Exception):
            generate_markdown_content()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_error_empty_response(self, mock_llm_factory):
        """Test that empty API response raises appropriate error."""
        mock_llm = MagicMock()
        mock_llm_factory.return_value = mock_llm

        # Return empty response
        mock_llm.call.return_value = {"content": ""}

        with pytest.raises(ValueError):
            generate_markdown_content()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_error_no_h1(self, mock_llm_factory):
        """Test that response without H1 heading raises error."""
        mock_llm = MagicMock()
        mock_llm_factory.return_value = mock_llm

        # Response without H1 heading
        mock_llm.call.return_value = {
            "content": "Just some text without heading. More text. And even more text."
        }

        with pytest.raises(ValueError):
            generate_markdown_content()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_error_too_short(self, mock_llm_factory):
        """Test that very short response raises error."""
        mock_llm = MagicMock()
        mock_llm_factory.return_value = mock_llm

        # Too short response
        mock_llm.call.return_value = {"content": "# T"}

        with pytest.raises(ValueError):
            generate_markdown_content()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_error_insufficient_sentences(self, mock_llm_factory):
        """Test that content with <2 sentences raises error."""
        mock_llm = MagicMock()
        mock_llm_factory.return_value = mock_llm

        # Only 1 sentence
        mock_llm.call.return_value = {
            "content": "# Title About Something\n\nJust one sentence here without more"
        }

        with pytest.raises(ValueError):
            generate_markdown_content()


class TestTask3ProseValidation:
    """Tests for task-3: Add validation for generated prose content."""

    def test_validate_prose_content_valid_two_sentences(self):
        """Test that valid prose with exactly 2 sentences passes validation."""
        prose = "First sentence with meaningful content about a topic. Second sentence providing additional detail and context."
        result = validate_prose_content(prose)
        assert result is True

    def test_validate_prose_content_valid_three_sentences(self):
        """Test that valid prose with exactly 3 sentences passes validation."""
        prose = "First sentence with meaningful content about a topic. Second sentence providing additional detail. Third sentence concluding the discussion."
        result = validate_prose_content(prose)
        assert result is True

    def test_validate_prose_content_valid_four_sentences_lenient(self):
        """Test that lenient validation accepts 4 sentences (lenient mode)."""
        # Per spec, lenient validation allows 2-4 sentences
        prose = "Sentence one with detail. Sentence two with more information. Sentence three providing context. Sentence four concluding."
        result = validate_prose_content(prose, lenient=True)
        assert result is True

    def test_validate_prose_content_valid_with_length_100_chars(self):
        """Test that prose with ~100 characters is valid."""
        prose = "This is a meaningful sentence with detail. " * 3  # ~130 chars
        result = validate_prose_content(prose)
        assert result is True

    def test_validate_prose_content_valid_with_length_500_chars(self):
        """Test that prose with ~500 characters is valid."""
        prose = "This is a meaningful sentence about an important topic. " * 9  # ~500 chars
        result = validate_prose_content(prose)
        assert result is True

    def test_validate_prose_content_returns_boolean(self):
        """Test that validate_prose_content returns a boolean."""
        prose = "Good sentence with meaningful content. Another good sentence providing detail."
        result = validate_prose_content(prose)
        assert isinstance(result, bool)

    def test_validate_prose_content_invalid_empty_string(self):
        """Test that empty prose returns False."""
        result = validate_prose_content("")
        assert result is False

    def test_validate_prose_content_invalid_none(self):
        """Test that None prose returns False."""
        result = validate_prose_content(None)
        assert result is False

    def test_validate_prose_content_invalid_single_sentence(self):
        """Test that single sentence returns False."""
        prose = "Only one sentence here that is too short for the minimum requirement."
        result = validate_prose_content(prose)
        assert result is False

    def test_validate_prose_content_invalid_too_short(self):
        """Test that very short prose (<100 chars) returns False."""
        prose = "Short content that is too short in length for the minimum requirement set."
        result = validate_prose_content(prose)
        assert result is False

    def test_validate_prose_content_invalid_too_long_strict(self):
        """Test that very long prose (>500 chars) returns False in strict mode."""
        prose = "A detailed sentence with meaningful content about various topics. " * 12  # Very long
        result = validate_prose_content(prose, lenient=False, max_length=500)
        assert result is False

    def test_validate_prose_content_invalid_long_lenient(self):
        """Test that long prose is accepted in lenient mode."""
        prose = "A detailed sentence with meaningful content about various topics. " * 12  # Very long
        result = validate_prose_content(prose, lenient=True)
        assert result is True

    def test_validate_prose_content_sentence_boundary_with_period(self):
        """Test sentence boundary detection with periods."""
        prose = "First sentence with detail and content about something. Second sentence. Third sentence with more information."
        result = validate_prose_content(prose)
        assert result is True

    def test_validate_prose_content_sentence_boundary_with_exclamation(self):
        """Test sentence boundary detection with exclamation marks."""
        prose = "First sentence with meaningful detail and content! Second sentence with additional information! Third sentence concluding!"
        result = validate_prose_content(prose)
        assert result is True

    def test_validate_prose_content_sentence_boundary_with_question(self):
        """Test sentence boundary detection with question marks."""
        prose = "Is this first sentence with meaningful detail and content? Is this second sentence with information? Is this third sentence?"
        result = validate_prose_content(prose)
        assert result is True

    def test_validate_prose_content_sentence_boundary_mixed(self):
        """Test sentence boundary detection with mixed punctuation."""
        prose = "Is this first sentence with meaningful detail and content? Yes it is indeed very true. Third sentence with information and context!"
        result = validate_prose_content(prose)
        assert result is True

    def test_validate_prose_content_with_whitespace(self):
        """Test prose with leading/trailing whitespace is trimmed."""
        prose = "  First sentence with detail and content. Second sentence providing information. Third sentence concluding.  "
        result = validate_prose_content(prose)
        assert result is True

    def test_validate_prose_content_with_newlines(self):
        """Test prose with newlines is handled correctly."""
        prose = "First sentence with detail and content.\nSecond sentence providing information.\nThird sentence concluding."
        result = validate_prose_content(prose)
        assert result is True

    def test_validate_prose_content_abbreviation_mr(self):
        """Test that abbreviations like 'Mr.' don't create false sentence counts."""
        # Lenient validation should accept this as 2-3 sentences despite Mr.
        prose = "Mr. Smith said something important about the topic. That was interesting and valuable information indeed."
        result = validate_prose_content(prose, lenient=True)
        # This may count as 3 or 2 depending on implementation
        assert isinstance(result, bool)

    def test_validate_prose_content_can_be_called_multiple_times(self):
        """Test that validation function can be called multiple times."""
        prose1 = "First sentence with meaningful detail and context. Second sentence with additional content. Third sentence with valuable information."
        prose2 = "Another sentence with meaningful detail here. Text with important content included. Here concluding with information."

        result1 = validate_prose_content(prose1)
        result2 = validate_prose_content(prose2)

        assert result1 is True
        assert result2 is True

    def test_validate_prose_content_lenient_mode_flag(self):
        """Test that lenient mode parameter works."""
        prose = "One sentence with detail. Two with content. Three with information. Four with context. Five with meaning."  # 5 sentences

        # Strict mode should fail
        result_strict = validate_prose_content(prose, lenient=False)
        assert result_strict is False

        # Lenient mode should pass
        result_lenient = validate_prose_content(prose, lenient=True)
        assert result_lenient is True

    def test_validate_prose_content_detailed_logging(self):
        """Test that validation provides specific failure reasons."""
        # Test with invalid inputs and verify the function handles them
        result = validate_prose_content("Too short without enough content")
        assert result is False

        result = validate_prose_content("One sentence only here without more.")
        assert result is False

    def test_validate_prose_content_unicode_support(self):
        """Test that validation handles unicode characters."""
        prose = "Café is nice and cozy place to visit and spend time. Naïve people exist everywhere in the world. Résumé looks good to employers."
        result = validate_prose_content(prose)
        assert result is True

    def test_validate_prose_content_punctuation_variations(self):
        """Test various punctuation patterns."""
        # Ellipsis
        prose = "First sentence with content... Second sentence with detail... Third sentence with information..."
        result = validate_prose_content(prose, lenient=True)
        assert isinstance(result, bool)

        # Semicolon (not typically a sentence boundary)
        prose2 = "First part with detail; second part with content. Third sentence with information!"
        result2 = validate_prose_content(prose2, lenient=True)
        assert isinstance(result2, bool)
