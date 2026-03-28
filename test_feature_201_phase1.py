"""
Tests for Feature 201 Phase 1: Content Generation via Claude API

This test suite validates that:
1. The Claude API prose generation function works correctly (task-1-1)
2. Content for test-y9go1c.md is generated and validated (task-1-2)
"""

from unittest.mock import Mock, patch

from src.create_markdown import (
    generate_markdown_content,
    validate_prose_length,
    validate_sentence_count,
)


class TestPhase1Task1ProseGeneration:
    """Task 1-1: Implement Claude API prose generation function."""

    def test_generate_markdown_returns_dict_with_title_and_prose(self):
        """Test that function returns dict with 'title' and 'prose' keys."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()
            mock_llm.call.return_value = (
                "# Feature 201 Test\n\n"
                "Test content requires proper length and meaningful sentences with varied vocabulary. "
                "This is the second sentence with additional words and information included. "
                "This is the third and final sentence completing the required format."
            )
            mock_get_llm.return_value = mock_llm

            result = generate_markdown_content()

            assert isinstance(result, dict)
            assert 'title' in result
            assert 'prose' in result
            assert result['title'] == "Feature 201 Test"

    def test_prose_contains_exactly_2_3_sentences(self):
        """Test that generated prose contains exactly 2-3 sentences."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()
            mock_llm.call.return_value = (
                "# Example Title\n\n"
                "First sentence here with some words. Second sentence here with content. "
                "Third and final sentence with more words and information."
            )
            mock_get_llm.return_value = mock_llm

            result = generate_markdown_content()
            prose = result['prose']

            is_valid, sentence_count, error = validate_sentence_count(prose)
            assert is_valid, f"Sentence validation failed: {error}"
            assert 2 <= sentence_count <= 3

    def test_generated_title_is_meaningful(self):
        """Test that generated title is a meaningful non-empty string."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()
            mock_llm.call.return_value = (
                "# The Power of Implementation\n\n"
                "Implementation requires careful planning and execution. "
                "Success comes from attention to detail and persistence. "
                "Excellence emerges through consistent effort and improvement."
            )
            mock_get_llm.return_value = mock_llm

            result = generate_markdown_content()
            title = result['title']

            assert isinstance(title, str)
            assert len(title) > 0
            assert len(title.split()) >= 2  # Multiple words

    def test_prose_is_coherent_and_meaningful(self):
        """Test that prose is coherent and not just placeholder text."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()
            mock_llm.call.return_value = (
                "# Coherent Content\n\n"
                "Content quality matters because readers deserve meaningful information. "
                "Well-written prose engages the audience and communicates clearly. "
                "Every sentence should contribute purpose and value to the document."
            )
            mock_get_llm.return_value = mock_llm

            result = generate_markdown_content()
            prose = result['prose']

            # Check for vocabulary variety (at least 10 unique words)
            unique_words = len(set(prose.lower().split()))
            assert unique_words >= 10, f"Insufficient vocabulary: {unique_words} unique words"

            # Check prose length is reasonable
            assert 100 <= len(prose) <= 300, f"Prose length out of range: {len(prose)}"


class TestPhase1Task2ContentValidation:
    """Task 1-2: Generate and validate title and prose content for test-y9go1c.md."""

    def test_feature_201_content_generation_and_validation(self):
        """Test complete task 1-2: Generate and validate content for feature 201."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()

            # Deterministic content for Feature 201
            mock_llm.call.return_value = (
                "# Automated Implementation Excellence\n\n"
                "Automated systems achieve excellence through systematic design and careful validation. "
                "The Sheep platform demonstrates how agents can generate high-quality artifacts consistently. "
                "Every implementation follows strict standards for reliability and maintainability."
            )
            mock_get_llm.return_value = mock_llm

            # Generate content
            result = generate_markdown_content()

            # Validate all requirements for task 1-2
            title = result['title']
            prose = result['prose']

            # Requirement 1: Generated prose content exists
            assert result is not None
            assert 'title' in result
            assert 'prose' in result

            # Requirement 2: Generated prose contains exactly 2-3 sentences
            is_valid, sentence_count, error_msg = validate_sentence_count(prose)
            assert is_valid, f"Sentence validation failed: {error_msg}"
            assert sentence_count == 3

            # Requirement 3: Generated title is coherent and thematically related
            assert title == "Automated Implementation Excellence"
            assert isinstance(title, str) and len(title) > 0

            # Requirement 4: Content is non-empty and meaningful
            assert len(prose) > 100
            assert "automated" in prose.lower() or "implementation" in prose.lower()

            # Requirement 5: Sentence count validation passes
            is_valid, count, error = validate_sentence_count(prose)
            assert is_valid
            assert count == 3

    def test_prose_length_validation(self):
        """Test that prose length is validated correctly."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()
            mock_llm.call.return_value = (
                "# Length Validation\n\n"
                "This is a test to ensure prose length validation works properly. "
                "The validation system checks for minimum and maximum character counts. "
                "Proper length ensures quality content without being too verbose."
            )
            mock_get_llm.return_value = mock_llm

            result = generate_markdown_content()
            prose = result['prose']

            is_valid, length, error = validate_prose_length(prose, min_length=100, max_length=300)
            assert is_valid, f"Prose length validation failed: {error}"
            assert 100 <= length <= 300

    def test_generated_content_determinism(self):
        """Test that same input produces same output (determinism requirement)."""
        with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
            mock_llm = Mock()

            fixed_content = (
                "# Deterministic Content\n\n"
                "Deterministic systems produce identical output given identical input. "
                "This property ensures reproducibility and reliable testing. "
                "Consistent output enables verification and debugging."
            )
            mock_llm.call.return_value = fixed_content
            mock_get_llm.return_value = mock_llm

            # Call function multiple times
            result1 = generate_markdown_content()
            result2 = generate_markdown_content()

            # With mocked LLM returning same content, results should be identical
            assert result1['title'] == result2['title']
            assert result1['prose'] == result2['prose']
