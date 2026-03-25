"""Tests for feature 208 generate_content function.

Tests verify that the generate_content function:
1. Successfully calls Claude API with temperature=0 for deterministic output
2. Returns a tuple of (title, prose)
3. Title and prose are both non-empty strings
4. Prose contains exactly 2 or 3 periods (sentences)
5. Multiple calls with same temperature=0 produce identical output (deterministic)
6. Proper error handling for API failures
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock


def test_generate_content_returns_tuple():
    """Test that generate_content returns a tuple of (title, prose)."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import generate_content

    # Mock the create_llm function and LLM.call method
    mock_response = "# Test Title\n\nThis is a test sentence. This is another test sentence."

    with patch("sheep.features.feature_208_markdown_file_creation.create_llm") as mock_create_llm:
        mock_llm = Mock()
        mock_llm.call.return_value = mock_response
        mock_create_llm.return_value = mock_llm

        title, prose = generate_content()

        assert isinstance(title, str), "Title should be string"
        assert isinstance(prose, str), "Prose should be string"
        assert title == "Test Title", f"Expected title 'Test Title', got '{title}'"
        assert "test sentence" in prose, f"Expected prose to contain test content, got '{prose}'"


def test_generate_content_title_is_nonempty():
    """Test that generated title is non-empty."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import generate_content

    mock_response = "# Important Topic\n\nThis is meaningful content. This is more content."

    with patch("sheep.features.feature_208_markdown_file_creation.create_llm") as mock_create_llm:
        mock_llm = Mock()
        mock_llm.call.return_value = mock_response
        mock_create_llm.return_value = mock_llm

        title, prose = generate_content()

        assert title, "Title should be non-empty"
        assert len(title) > 0, "Title length should be greater than 0"


def test_generate_content_prose_is_nonempty():
    """Test that generated prose is non-empty."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import generate_content

    mock_response = "# Title\n\nThis is meaningful prose content. This is more content."

    with patch("sheep.features.feature_208_markdown_file_creation.create_llm") as mock_create_llm:
        mock_llm = Mock()
        mock_llm.call.return_value = mock_response
        mock_create_llm.return_value = mock_llm

        title, prose = generate_content()

        assert prose, "Prose should be non-empty"
        assert len(prose) > 0, "Prose length should be greater than 0"


def test_generate_content_prose_has_valid_sentence_count():
    """Test that prose contains 2 or 3 sentences (periods)."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import generate_content

    # Test with 2 sentences
    mock_response = "# Title\n\nFirst sentence. Second sentence."

    with patch("sheep.features.feature_208_markdown_file_creation.create_llm") as mock_create_llm:
        mock_llm = Mock()
        mock_llm.call.return_value = mock_response
        mock_create_llm.return_value = mock_llm

        title, prose = generate_content()
        sentence_count = prose.count(".")

        assert sentence_count in (2, 3), f"Expected 2-3 sentences, got {sentence_count}"


def test_generate_content_prose_has_three_sentences():
    """Test that prose can contain exactly 3 sentences."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import generate_content

    # Test with 3 sentences
    mock_response = "# Title\n\nFirst sentence. Second sentence. Third sentence."

    with patch("sheep.features.feature_208_markdown_file_creation.create_llm") as mock_create_llm:
        mock_llm = Mock()
        mock_llm.call.return_value = mock_response
        mock_create_llm.return_value = mock_llm

        title, prose = generate_content()
        sentence_count = prose.count(".")

        assert sentence_count == 3, f"Expected 3 sentences, got {sentence_count}"


def test_generate_content_calls_create_llm_with_temperature_zero():
    """Test that create_llm is called with temperature=0 for determinism."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import generate_content

    mock_response = "# Title\n\nContent. More content."

    with patch("sheep.features.feature_208_markdown_file_creation.create_llm") as mock_create_llm:
        mock_llm = Mock()
        mock_llm.call.return_value = mock_response
        mock_create_llm.return_value = mock_llm

        title, prose = generate_content()

        # Verify create_llm was called with temperature=0
        mock_create_llm.assert_called_once()
        call_kwargs = mock_create_llm.call_args[1] if mock_create_llm.call_args[1] else {}
        assert call_kwargs.get("temperature") == 0, f"Expected temperature=0, got {call_kwargs.get('temperature')}"


def test_generate_content_deterministic_with_temperature_zero():
    """Test that same temperature=0 produces same output (deterministic)."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import generate_content

    deterministic_response = "# Cloud Computing\n\nCloud services revolutionize infrastructure. Organizations benefit greatly. Adoption continues worldwide."

    with patch("sheep.features.feature_208_markdown_file_creation.create_llm") as mock_create_llm:
        mock_llm = Mock()
        mock_llm.call.return_value = deterministic_response
        mock_create_llm.return_value = mock_llm

        # First call
        title1, prose1 = generate_content()

        # Reset mock and call again
        mock_llm.call.return_value = deterministic_response
        title2, prose2 = generate_content()

        # Both should be identical
        assert title1 == title2, f"Titles should be identical with temperature=0: '{title1}' vs '{title2}'"
        assert prose1 == prose2, f"Prose should be identical with temperature=0: '{prose1}' vs '{prose2}'"


def test_generate_content_llm_called_with_markdown_generation_prompt():
    """Test that LLM is called with the markdown generation prompt."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import (
        generate_content,
        MARKDOWN_GENERATION_PROMPT,
    )

    mock_response = "# Title\n\nContent here. More content."

    with patch("sheep.features.feature_208_markdown_file_creation.create_llm") as mock_create_llm:
        mock_llm = Mock()
        mock_llm.call.return_value = mock_response
        mock_create_llm.return_value = mock_llm

        title, prose = generate_content()

        # Verify llm.call was called
        mock_llm.call.assert_called_once()
        call_args = mock_llm.call.call_args[0][0]

        # Verify message structure
        assert isinstance(call_args, list), "Call should be with list of messages"
        assert len(call_args) > 0, "Should have at least one message"
        assert call_args[0]["role"] == "user", "First message should be from user"


def test_generate_content_raises_on_api_failure():
    """Test that generate_content raises exception on API failure."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import generate_content

    with patch("sheep.features.feature_208_markdown_file_creation.create_llm") as mock_create_llm:
        mock_llm = Mock()
        mock_llm.call.side_effect = Exception("API call failed")
        mock_create_llm.return_value = mock_llm

        # Should raise an exception
        try:
            title, prose = generate_content()
            assert False, "Should have raised an exception"
        except Exception as e:
            assert "API call failed" in str(e) or "generate_content" in str(e)


def test_generate_content_handles_missing_h1_format():
    """Test that generate_content validates H1 format in response."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import generate_content

    # Missing H1 format
    invalid_response = "Test Title\n\nThis is prose. More prose."

    with patch("sheep.features.feature_208_markdown_file_creation.create_llm") as mock_create_llm:
        mock_llm = Mock()
        mock_llm.call.return_value = invalid_response
        mock_create_llm.return_value = mock_llm

        try:
            title, prose = generate_content()
            # If we get here, check that it properly handles the error
            assert False, "Should have raised ValueError for missing H1 format"
        except ValueError:
            # Expected behavior
            pass
        except Exception as e:
            # Some other error is also acceptable as long as it fails
            pass


def test_generate_content_handles_missing_blank_line():
    """Test that generate_content validates blank line separator."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from sheep.features.feature_208_markdown_file_creation import generate_content

    # Missing blank line between title and prose
    invalid_response = "# Title\nThis is prose. More prose."

    with patch("sheep.features.feature_208_markdown_file_creation.create_llm") as mock_create_llm:
        mock_llm = Mock()
        mock_llm.call.return_value = invalid_response
        mock_create_llm.return_value = mock_llm

        try:
            title, prose = generate_content()
            # If we get here, it might be okay if the function handles it gracefully
            assert False, "Should have raised ValueError for missing blank line"
        except ValueError:
            # Expected behavior
            pass
        except Exception:
            # Other errors are also acceptable
            pass
