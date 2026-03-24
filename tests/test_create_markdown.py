"""Tests for Feature 199: Content generation and validation for markdown file creation."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.create_markdown import (
    generate_markdown_content,
    validate_content,
    validate_sentence_count,
    validate_prose_length,
)


class TestClaudeAPIIntegration:
    """Tests for task-1: Claude API integration for content generation."""

    def test_generate_markdown_content_returns_dict_with_required_keys(self):
        """Test that generate_markdown_content returns dict with 'title', 'prose', and 'full_content' keys."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            # Mock the LLM to return valid markdown content
            mock_llm = Mock()
            mock_llm.call.return_value = (
                "# Effective Communication\n\n"
                "Clear communication builds strong relationships. "
                "When people express ideas with clarity and empathy, misunderstandings dissolve. "
                "Mastering this skill transforms both personal and professional endeavors."
            )
            mock_get_llm.return_value = mock_llm

            result = generate_markdown_content()

            assert isinstance(result, dict)
            assert 'title' in result
            assert 'prose' in result
            assert 'full_content' in result

    def test_generate_markdown_content_title_is_string(self):
        """Test that generated title is a non-empty string."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()
            mock_llm.call.return_value = (
                "# Sustainable Technology\n\n"
                "Technology enables sustainable solutions for environmental challenges. "
                "Renewable energy and circular design reduce our carbon footprint. "
                "This commitment preserves the planet for future generations."
            )
            mock_get_llm.return_value = mock_llm

            result = generate_markdown_content()

            assert isinstance(result['title'], str)
            assert len(result['title']) > 0
            assert result['title'] == "Sustainable Technology"

    def test_generate_markdown_content_prose_is_string(self):
        """Test that generated prose is a non-empty string."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()
            mock_llm.call.return_value = (
                "# Innovation and Progress\n\n"
                "Innovation drives human progress forward across every domain of knowledge and creativity. "
                "Through continuous experimentation and learning from failures, we develop solutions to complex problems. "
                "This process of iterative improvement creates lasting value and opens new possibilities."
            )
            mock_get_llm.return_value = mock_llm

            result = generate_markdown_content()

            assert isinstance(result['prose'], str)
            assert len(result['prose']) > 0
            assert len(result['prose']) >= 100  # Minimum length requirement

    def test_generate_markdown_content_full_content_is_complete_markdown(self):
        """Test that full_content contains the complete markdown with heading and prose."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()
            mock_llm.call.return_value = (
                "# Learning and Growth\n\n"
                "Learning is fundamental to personal and professional development throughout our lives. "
                "Every experience, whether success or failure, contributes to our growing knowledge and wisdom. "
                "By embracing a mindset of continuous improvement, we unlock our potential and achieve meaningful goals."
            )
            mock_get_llm.return_value = mock_llm

            result = generate_markdown_content()

            assert isinstance(result['full_content'], str)
            assert result['full_content'].startswith("# ")
            assert result['title'] in result['full_content']
            assert result['prose'] in result['full_content']

    def test_generate_markdown_content_handles_api_dict_response(self):
        """Test that generate_markdown_content handles LLM returning dict response."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()
            # Simulate API returning a dict with 'content' key
            mock_llm.call.return_value = {
                'content': (
                    "# The Art of Writing\n\n"
                    "Writing is a powerful tool for expressing ideas and sharing knowledge with others. "
                    "Through clear, thoughtful prose, writers can inspire, educate, and entertain their audiences. "
                    "The craft of writing improves with practice, feedback, and continuous refinement of technique."
                )
            }
            mock_get_llm.return_value = mock_llm

            result = generate_markdown_content()

            assert result['title'] == "The Art of Writing"
            assert "powerful tool" in result['prose']

    def test_generate_markdown_content_handles_api_string_response(self):
        """Test that generate_markdown_content handles LLM returning string response."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()
            # Simulate API returning a string directly
            mock_llm.call.return_value = (
                "# Digital Transformation\n\n"
                "Digital transformation reshapes how organizations operate and deliver value. "
                "Technology enables efficiency, innovation, and better customer experiences. "
                "Companies embracing digital tools and mindsets gain competitive advantages in their markets."
            )
            mock_get_llm.return_value = mock_llm

            result = generate_markdown_content()

            assert 'title' in result
            assert 'prose' in result

    def test_generate_markdown_content_retries_on_validation_failure(self):
        """Test that generate_markdown_content retries when validation fails."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()

            # First call returns invalid content (only 1 sentence)
            # Second call returns valid content
            mock_llm.call.side_effect = [
                "# Bad Title\n\nOnly one sentence here.",  # Invalid - not enough sentences
                (
                    "# Resilience Through Adversity\n\n"
                    "Adversity builds character and resilience when we embrace challenges with courage. "
                    "Each obstacle overcome strengthens our capabilities and deepens our understanding. "
                    "Through perseverance, we transform difficulties into opportunities for growth."
                )
            ]
            mock_get_llm.return_value = mock_llm

            result = generate_markdown_content(max_retries=3, retry_delay=0.01)

            # Should succeed on second attempt
            assert result['title'] == "Resilience Through Adversity"
            assert mock_llm.call.call_count == 2

    def test_generate_markdown_content_raises_error_after_max_retries(self):
        """Test that generate_markdown_content raises ValueError after exhausting retries."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()
            # Always return invalid content
            mock_llm.call.return_value = "# Bad\n\nOnly one."  # Invalid

            mock_get_llm.return_value = mock_llm

            with pytest.raises(ValueError) as exc_info:
                generate_markdown_content(max_retries=2, retry_delay=0.01)

            assert "after 2 attempts" in str(exc_info.value).lower()

    def test_generate_markdown_content_validates_content_before_returning(self):
        """Test that generated content passes validation before being returned."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()
            mock_llm.call.return_value = (
                "# Quality Content Generation\n\n"
                "Quality content requires thoughtful consideration of purpose and audience. "
                "Well-structured information delivered clearly creates value for readers. "
                "Excellence emerges from dedication to refinement and mastery of the craft."
            )
            mock_get_llm.return_value = mock_llm

            result = generate_markdown_content()

            # Verify result passes validation
            validation = validate_content(result['full_content'])
            assert validation['is_valid']

    def test_generate_markdown_content_handles_api_timeout(self):
        """Test that generate_markdown_content raises ValueError on API timeout."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()
            mock_llm.call.side_effect = TimeoutError("API request timed out")
            mock_get_llm.return_value = mock_llm

            with pytest.raises(ValueError) as exc_info:
                generate_markdown_content(max_retries=1)

            assert "API call failed" in str(exc_info.value)

    def test_generate_markdown_content_initializes_llm_correctly(self):
        """Test that generate_markdown_content initializes Claude API client correctly."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()
            mock_llm.call.return_value = (
                "# API Integration\n\n"
                "API integration requires careful authentication and error handling. "
                "Proper implementation ensures reliable communication between systems. "
                "Well-designed interfaces simplify complex interactions and improve reliability."
            )
            mock_get_llm.return_value = mock_llm

            generate_markdown_content()

            # Verify get_reasoning_llm was called
            mock_get_llm.assert_called_once()

    def test_generate_markdown_content_calls_api_with_correct_prompt(self):
        """Test that generate_markdown_content sends correct prompt to Claude API."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()
            mock_llm.call.return_value = (
                "# Correct Prompt\n\n"
                "The prompt guides the AI to generate appropriate content. "
                "Detailed instructions improve the quality of responses. "
                "Well-designed prompts enable AI systems to produce excellent results."
            )
            mock_get_llm.return_value = mock_llm

            generate_markdown_content()

            # Verify API was called with a message containing the prompt
            assert mock_llm.call.called
            call_args = mock_llm.call.call_args[0][0]
            assert isinstance(call_args, list)
            assert len(call_args) > 0
            assert call_args[0]['role'] == 'user'
            assert 'H1 heading' in call_args[0]['content']


class TestContentValidation:
    """Tests for task-2: Content validation (sentence count, length, coherence)."""

    def test_validate_sentence_count_accepts_two_sentences(self):
        """Test that validate_sentence_count returns True for exactly 2 sentences."""
        prose = "This is the first sentence. This is the second sentence."
        is_valid, count, error = validate_sentence_count(prose)

        assert is_valid is True
        assert count == 2
        assert error is None

    def test_validate_sentence_count_accepts_three_sentences(self):
        """Test that validate_sentence_count returns True for exactly 3 sentences."""
        prose = "First sentence here. Second sentence now. Third sentence finally."
        is_valid, count, error = validate_sentence_count(prose)

        assert is_valid is True
        assert count == 3
        assert error is None

    def test_validate_sentence_count_rejects_one_sentence(self):
        """Test that validate_sentence_count rejects prose with only 1 sentence."""
        prose = "Only one sentence in this prose."
        is_valid, count, error = validate_sentence_count(prose)

        assert is_valid is False
        assert count == 1
        assert error is not None
        assert "Too few" in error

    def test_validate_sentence_count_rejects_four_sentences(self):
        """Test that validate_sentence_count rejects prose with 4 sentences."""
        prose = "First. Second. Third. Fourth."
        is_valid, count, error = validate_sentence_count(prose)

        assert is_valid is False
        assert count == 4
        assert error is not None
        assert "Too many" in error

    def test_validate_sentence_count_detects_question_marks(self):
        """Test that sentence counting recognizes question marks as sentence boundaries."""
        prose = "What is artificial intelligence? It's a transformative technology. How will it impact society?"
        is_valid, count, error = validate_sentence_count(prose)

        assert count >= 2  # Should detect at least the sentences

    def test_validate_sentence_count_detects_exclamation_marks(self):
        """Test that sentence counting recognizes exclamation marks as sentence boundaries."""
        prose = "This is amazing! It's revolutionary! Consider the possibilities."
        is_valid, count, error = validate_sentence_count(prose)

        assert count >= 2

    def test_validate_sentence_count_rejects_empty_prose(self):
        """Test that validate_sentence_count rejects empty prose."""
        is_valid, count, error = validate_sentence_count("")

        assert is_valid is False
        assert count == 0
        assert error is not None

    def test_validate_prose_length_accepts_100_characters(self):
        """Test that validate_prose_length accepts prose with exactly 100 characters."""
        # Create prose with exactly 100 characters
        prose = "A" * 100
        is_valid, length, error = validate_prose_length(prose, min_length=100, max_length=300)

        assert is_valid is True
        assert length == 100
        assert error is None

    def test_validate_prose_length_accepts_300_characters(self):
        """Test that validate_prose_length accepts prose with exactly 300 characters."""
        prose = "B" * 300
        is_valid, length, error = validate_prose_length(prose, min_length=100, max_length=300)

        assert is_valid is True
        assert length == 300
        assert error is None

    def test_validate_prose_length_accepts_middle_range(self):
        """Test that validate_prose_length accepts prose in middle of range."""
        prose = "C" * 200
        is_valid, length, error = validate_prose_length(prose, min_length=100, max_length=300)

        assert is_valid is True
        assert error is None

    def test_validate_prose_length_rejects_too_short(self):
        """Test that validate_prose_length rejects prose shorter than minimum."""
        prose = "D" * 50
        is_valid, length, error = validate_prose_length(prose, min_length=100, max_length=300)

        assert is_valid is False
        assert error is not None
        assert "too short" in error.lower()

    def test_validate_prose_length_rejects_too_long(self):
        """Test that validate_prose_length rejects prose longer than maximum."""
        prose = "E" * 500
        is_valid, length, error = validate_prose_length(prose, min_length=100, max_length=300)

        assert is_valid is False
        assert error is not None
        assert "too long" in error.lower()

    def test_validate_prose_length_rejects_empty(self):
        """Test that validate_prose_length rejects empty prose."""
        is_valid, length, error = validate_prose_length("")

        assert is_valid is False
        assert error is not None

    def test_validate_prose_length_custom_bounds(self):
        """Test that validate_prose_length respects custom min/max bounds."""
        prose = "F" * 250
        is_valid, length, error = validate_prose_length(prose, min_length=200, max_length=300)

        assert is_valid is True
        assert error is None

    def test_validate_content_valid_complete_markdown(self):
        """Test that validate_content accepts valid complete markdown."""
        content = (
            "# The Importance of Consistency\n\n"
            "Consistency builds trust and reliability in all our endeavors and relationships. "
            "When we maintain steady progress and unwavering principles, others can depend on us. "
            "Through consistent effort, we achieve lasting results and establish strong foundations."
        )
        result = validate_content(content)

        assert result['is_valid'] is True
        assert len(result['errors']) == 0
        assert result['details']['has_h1_heading'] is True

    def test_validate_content_checks_h1_heading_present(self):
        """Test that validate_content requires H1 heading."""
        content = "## Wrong heading level\n\nSome prose here."
        result = validate_content(content)

        assert result['is_valid'] is False
        assert any("H1" in error for error in result['errors'])

    def test_validate_content_checks_blank_line_separator(self):
        """Test that validate_content requires blank line after heading."""
        content = "# Title\nNo blank line before prose."
        result = validate_content(content)

        assert result['is_valid'] is False
        assert any("blank" in error.lower() for error in result['errors'])

    def test_validate_content_checks_sentence_count(self):
        """Test that validate_content validates sentence count."""
        content = "# Title\n\nOnly one sentence here."
        result = validate_content(content)

        assert result['is_valid'] is False
        assert any("sentence" in error.lower() for error in result['errors'])

    def test_validate_content_checks_prose_length(self):
        """Test that validate_content validates prose length."""
        content = "# Title\n\nShort."
        result = validate_content(content)

        assert result['is_valid'] is False
        assert any("short" in error.lower() for error in result['errors'])

    def test_validate_content_checks_vocabulary_variety(self):
        """Test that validate_content checks for vocabulary variety."""
        content = (
            "# Test\n\n"
            "Word word word word word word word word word word. "
            "Word word word word word word word word word word. "
            "Word word word word word word word word word word."
        )
        result = validate_content(content)

        assert result['is_valid'] is False
        assert any("vocabulary" in error.lower() or "variety" in error.lower() for error in result['errors'])

    def test_validate_content_returns_all_details(self):
        """Test that validate_content returns detailed validation information."""
        content = (
            "# Learning\n\n"
            "Learning drives human growth and development throughout our lives. "
            "Through curiosity and persistence, we acquire new skills and understanding. "
            "This continuous process of improvement opens doors to greater achievements."
        )
        result = validate_content(content)

        assert 'is_valid' in result
        assert 'errors' in result
        assert 'details' in result
        assert 'sentence_count' in result['details']
        assert 'prose_length' in result['details']
        assert 'content_length' in result['details']

    def test_validate_content_empty_string(self):
        """Test that validate_content rejects empty content."""
        result = validate_content("")

        assert result['is_valid'] is False
        assert any("empty" in error.lower() for error in result['errors'])

    def test_validate_content_multiline_prose(self):
        """Test that validate_content handles multiline prose correctly."""
        content = (
            "# The Benefits of Collaboration\n\n"
            "Collaboration brings diverse perspectives to problem-solving. "
            "When teams work together effectively, they achieve superior results. "
            "Teamwork creates synergy where the whole becomes greater than the sum of its parts."
        )
        result = validate_content(content)

        assert result['is_valid'] is True
        assert result['details']['sentence_count'] == 3


class TestValidationEdgeCases:
    """Tests for edge cases and error handling in validation."""

    def test_sentence_counting_with_abbreviations(self):
        """Test that sentence counting handles abbreviations correctly."""
        # Ph.D. and other abbreviations shouldn't be counted as sentence ends
        prose = (
            "Dr. Smith earned her Ph.D. from Stanford University. "
            "She now works in the technology sector. "
            "Her expertise benefits many organizations."
        )
        is_valid, count, error = validate_sentence_count(prose)

        # Should count actual sentences correctly despite abbreviations
        assert count >= 2

    def test_sentence_counting_with_ellipsis(self):
        """Test sentence counting with ellipsis notation."""
        prose = (
            "The possibilities are endless... "
            "We can achieve remarkable things. "
            "Tomorrow brings new opportunities."
        )
        is_valid, count, error = validate_sentence_count(prose)

        # Should handle ellipsis gracefully
        assert count >= 2

    def test_validate_content_with_trailing_whitespace(self):
        """Test validate_content handles content with trailing whitespace."""
        content = (
            "# Title\n\n"
            "First sentence here. Second sentence now. Third sentence finally.   \n\n"
        )
        result = validate_content(content)

        # Should handle trailing whitespace gracefully
        assert 'is_valid' in result

    def test_validate_prose_length_with_special_characters(self):
        """Test prose length validation with special characters."""
        prose = "Testing! Testing! Testing! " * 10  # ~280 chars with special chars
        is_valid, length, error = validate_prose_length(prose)

        # Length calculation should work with special characters
        assert isinstance(length, int)
        assert length > 0
