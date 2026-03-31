"""Tests for feature 292 phase 1: Content generation and validation."""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestTask1ContentGeneration:
    """Tests for Task 1: Generate markdown content with retry logic."""

    def test_generate_markdown_content_with_retry_success(self):
        """Test that generate_markdown_content_with_retry succeeds on first attempt."""
        from src.sheep_292_phase1 import generate_markdown_content_with_retry

        # Mock the LLM to return valid content (with minimum 100 chars of prose)
        valid_content = "# Test Title\n\nThis is a comprehensive first sentence about the topic at hand. This is the second sentence that provides additional information and context about the subject matter.\n"

        with patch('src.sheep_292_phase1.get_reasoning_llm') as mock_llm_factory:
            mock_llm = Mock()
            mock_llm.call.return_value = {"content": valid_content}
            mock_llm_factory.return_value = mock_llm

            result = generate_markdown_content_with_retry(max_retries=3, retry_delay=0.1)

            assert result is not None
            assert isinstance(result, str)
            assert "# Test Title" in result
            assert "first sentence" in result.lower()

    def test_generate_markdown_content_with_retry_fails_then_succeeds(self):
        """Test retry logic: fails once, then succeeds on second attempt."""
        from src.sheep_292_phase1 import generate_markdown_content_with_retry

        valid_content = "# Success Title\n\nThis is a comprehensive first sentence about the topic at hand. This is the second sentence that provides additional information and context about the subject matter.\n"
        invalid_content = "Not valid markdown"

        with patch('src.sheep_292_phase1.get_reasoning_llm') as mock_llm_factory:
            with patch('src.sheep_292_phase1.validate_content') as mock_validate:
                mock_llm = Mock()
                # First call fails validation, second succeeds
                mock_llm.call.side_effect = [
                    {"content": invalid_content},
                    {"content": valid_content},
                ]
                mock_llm_factory.return_value = mock_llm

                # First call raises ValueError, second returns True
                mock_validate.side_effect = [ValueError("Invalid"), True]

                result = generate_markdown_content_with_retry(max_retries=3, retry_delay=0.01)

                assert result is not None
                assert "# Success Title" in result

    def test_generate_markdown_content_with_exponential_backoff(self):
        """Test that exponential backoff is applied correctly."""
        from src.sheep_292_phase1 import generate_markdown_content_with_retry

        with patch('src.sheep_292_phase1.get_reasoning_llm') as mock_llm_factory:
            with patch('src.sheep_292_phase1.time.sleep') as mock_sleep:
                with patch('src.sheep_292_phase1.validate_content') as mock_validate:
                    mock_llm = Mock()
                    mock_llm.call.side_effect = Exception("API Error")
                    mock_llm_factory.return_value = mock_llm
                    mock_validate.side_effect = ValueError("Invalid")

                    with pytest.raises(Exception):
                        generate_markdown_content_with_retry(max_retries=3, retry_delay=1.0)

                    # Verify exponential backoff was applied: 1s, 2s, 4s
                    sleep_calls = mock_sleep.call_args_list
                    assert len(sleep_calls) == 2  # 2 retries (after first and second failure)
                    assert abs(sleep_calls[0][0][0] - 1.0) < 0.1
                    assert abs(sleep_calls[1][0][0] - 2.0) < 0.1

    def test_generate_markdown_content_max_retries_exceeded(self):
        """Test that function raises exception after max retries exceeded."""
        from src.sheep_292_phase1 import generate_markdown_content_with_retry

        with patch('src.sheep_292_phase1.get_reasoning_llm') as mock_llm_factory:
            mock_llm = Mock()
            mock_llm.call.side_effect = Exception("API Error")
            mock_llm_factory.return_value = mock_llm

            with pytest.raises(Exception):
                generate_markdown_content_with_retry(max_retries=1, retry_delay=0.01)


class TestTask2HeadingValidation:
    """Tests for Task 2: Validate markdown heading structure."""

    def test_validate_heading_valid_h1(self):
        """Test that valid H1 heading passes validation."""
        from src.sheep_292_phase1 import validate_heading

        content = "# Valid Title\n\nSome prose content."
        result = validate_heading(content)
        assert result is True

    def test_validate_heading_missing_raises_error(self):
        """Test that missing heading raises ValueError."""
        from src.sheep_292_phase1 import validate_heading

        content = "Just prose without a heading."
        with pytest.raises(ValueError, match="heading|H1"):
            validate_heading(content)

    def test_validate_heading_wrong_level_h2(self):
        """Test that H2 heading is rejected."""
        from src.sheep_292_phase1 import validate_heading

        content = "## Wrong Level\n\nSome prose."
        with pytest.raises(ValueError, match="heading|H1"):
            validate_heading(content)

    def test_validate_heading_missing_space(self):
        """Test that #Title (missing space) is rejected."""
        from src.sheep_292_phase1 import validate_heading

        content = "#NoSpace\n\nSome prose."
        with pytest.raises(ValueError, match="heading|format"):
            validate_heading(content)

    def test_validate_heading_empty_title(self):
        """Test that empty title is rejected."""
        from src.sheep_292_phase1 import validate_heading

        content = "# \n\nSome prose."
        with pytest.raises(ValueError, match="heading|empty|title"):
            validate_heading(content)


class TestTask3SentenceCountValidation:
    """Tests for Task 3: Validate sentence count."""

    def test_validate_sentence_count_2_sentences(self):
        """Test that exactly 2 sentences passes validation."""
        from src.sheep_292_phase1 import validate_sentence_count

        prose = "First sentence. Second sentence."
        result = validate_sentence_count(prose)
        assert result is True

    def test_validate_sentence_count_3_sentences(self):
        """Test that exactly 3 sentences passes validation."""
        from src.sheep_292_phase1 import validate_sentence_count

        prose = "First sentence. Second sentence. Third sentence."
        result = validate_sentence_count(prose)
        assert result is True

    def test_validate_sentence_count_1_sentence(self):
        """Test that 1 sentence is rejected."""
        from src.sheep_292_phase1 import validate_sentence_count

        prose = "Only one sentence."
        with pytest.raises(ValueError, match="sentence|count|2-3"):
            validate_sentence_count(prose)

    def test_validate_sentence_count_4_sentences(self):
        """Test that 4 sentences is rejected."""
        from src.sheep_292_phase1 import validate_sentence_count

        prose = "First. Second. Third. Fourth."
        with pytest.raises(ValueError, match="sentence|count|2-3"):
            validate_sentence_count(prose)

    def test_validate_sentence_count_with_question_mark(self):
        """Test that question marks are counted as sentence endings."""
        from src.sheep_292_phase1 import validate_sentence_count

        prose = "Is this correct? Yes it is."
        result = validate_sentence_count(prose)
        assert result is True

    def test_validate_sentence_count_with_exclamation_mark(self):
        """Test that exclamation marks are counted as sentence endings."""
        from src.sheep_292_phase1 import validate_sentence_count

        prose = "This is exciting! This is the second sentence."
        result = validate_sentence_count(prose)
        assert result is True


class TestTask4ProseValidation:
    """Tests for Task 4: Validate prose length and encoding."""

    def test_validate_content_valid(self):
        """Test that completely valid content passes validation."""
        from src.sheep_292_phase1 import validate_content

        content = "# Valid Title\n\nThis is a comprehensive first sentence about the topic at hand. This is the second sentence that provides additional information and context about the subject matter.\n"
        result = validate_content(content)
        assert result is True

    def test_validate_content_prose_too_short(self):
        """Test that prose < 100 chars is rejected."""
        from src.sheep_292_phase1 import validate_content

        content = "# Title\n\nShort. Text.\n"
        with pytest.raises(ValueError, match="length|100"):
            validate_content(content)

    def test_validate_content_prose_too_long(self):
        """Test that prose > 300 chars is rejected."""
        from src.sheep_292_phase1 import validate_content

        # Create prose that's too long (> 300 chars) with 2 sentences
        long_prose = "This is a very long sentence with lots of words to exceed three hundred characters total " + "x" * 250 + ". This is the second sentence."
        content = f"# Title\n\n{long_prose}\n"
        with pytest.raises(ValueError, match="length|300"):
            validate_content(content)

    def test_validate_content_missing_heading(self):
        """Test that missing heading is rejected."""
        from src.sheep_292_phase1 import validate_content

        content = "Just some prose. This is the second sentence."
        with pytest.raises(ValueError, match="heading"):
            validate_content(content)

    def test_validate_content_missing_blank_line(self):
        """Test that missing blank line after heading is rejected."""
        from src.sheep_292_phase1 import validate_content

        content = "# Title\nProse without blank line separator. Another sentence here."
        with pytest.raises(ValueError, match="blank|line|separator"):
            validate_content(content)

    def test_validate_content_invalid_sentence_count(self):
        """Test that invalid sentence count is rejected."""
        from src.sheep_292_phase1 import validate_content

        content = "# Title\n\nOnly one sentence.\n"
        with pytest.raises(ValueError, match="sentence"):
            validate_content(content)

    def test_validate_content_utf8_encoding_check(self):
        """Test that UTF-8 encoding is validated."""
        from src.sheep_292_phase1 import validate_content

        # Valid UTF-8 content
        content = "# Café Title\n\nThis is a sentence with special chars: é, ñ, ü. This is the second sentence.\n"
        # Should not raise for valid UTF-8
        try:
            validate_content(content)
        except ValueError as e:
            if "encoding" in str(e).lower():
                pytest.fail(f"Valid UTF-8 content rejected: {e}")
