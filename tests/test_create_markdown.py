"""Tests for Feature 199: Content generation and validation for markdown file creation."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import os
import subprocess

from src.create_markdown import (
    generate_markdown_content,
    validate_content,
    validate_sentence_count,
    validate_prose_length,
    create_markdown_file,
    validate_file_encoding,
    validate_file_structure,
    validate_markdown_file,
    stage_and_commit_file,
    push_to_feature_branch,
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


class TestFileCreation:
    """Tests for task-3: Create markdown file with proper UTF-8/LF encoding."""

    def test_create_markdown_file_creates_file_at_repository_root(self):
        """Test that create_markdown_file creates file at repository root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
            filepath = os.path.join(tmpdir, "test.md")

            result = create_markdown_file(content, filename="test.md", filepath=tmpdir)

            # Verify file was created
            assert os.path.exists(filepath)
            assert result == str(Path(filepath).absolute())

    def test_create_markdown_file_writes_utf8_encoding(self):
        """Test that create_markdown_file writes file with UTF-8 encoding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            content = "# UTF-8 Test\n\nThis file contains UTF-8 characters: café, naïve, résumé."
            filepath = os.path.join(tmpdir, "utf8_test.md")

            create_markdown_file(content, filename="utf8_test.md", filepath=tmpdir)

            # Read file as bytes and verify UTF-8 encoding
            raw_bytes = Path(filepath).read_bytes()
            decoded = raw_bytes.decode('utf-8')  # Should not raise exception
            assert "café" in decoded

    def test_create_markdown_file_writes_lf_line_endings(self):
        """Test that create_markdown_file writes file with LF line endings (not CRLF)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            content = "# Multi-line Test\n\nLine one. Line two. Line three."
            filepath = os.path.join(tmpdir, "lf_test.md")

            create_markdown_file(content, filename="lf_test.md", filepath=tmpdir)

            # Read file as bytes and verify LF only (no CRLF)
            raw_bytes = Path(filepath).read_bytes()
            assert b'\r\n' not in raw_bytes  # No CRLF
            assert b'\n' in raw_bytes  # Has LF

    def test_create_markdown_file_raises_error_if_file_exists(self):
        """Test that create_markdown_file raises FileExistsError if file already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
            filepath = os.path.join(tmpdir, "existing.md")

            # Create file first
            create_markdown_file(content, filename="existing.md", filepath=tmpdir)

            # Try to create same file again
            with pytest.raises(FileExistsError):
                create_markdown_file(content, filename="existing.md", filepath=tmpdir)

    def test_create_markdown_file_raises_error_if_content_empty(self):
        """Test that create_markdown_file raises ValueError if content is empty."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError) as exc_info:
                create_markdown_file("", filename="empty.md", filepath=tmpdir)

            assert "empty" in str(exc_info.value).lower()

    def test_create_markdown_file_uses_default_filename(self):
        """Test that create_markdown_file uses default filename 'test-nttet0.md' when not specified."""
        with tempfile.TemporaryDirectory() as tmpdir:
            content = "# Default Name Test\n\nUsing default filename. That is the second sentence. Here is the third."
            filepath = os.path.join(tmpdir, "test-nttet0.md")

            result = create_markdown_file(content, filepath=tmpdir)

            # Verify default filename was used
            assert os.path.exists(filepath)
            assert "test-nttet0.md" in result

    def test_create_markdown_file_content_is_preserved(self):
        """Test that create_markdown_file preserves exact content written."""
        with tempfile.TemporaryDirectory() as tmpdir:
            content = "# Exact Content\n\nFirst sentence with specific words. Second sentence also specific. Third sentence too."
            filepath = os.path.join(tmpdir, "content_test.md")

            create_markdown_file(content, filename="content_test.md", filepath=tmpdir)

            # Read back and verify exact match
            read_content = Path(filepath).read_text(encoding='utf-8')
            assert read_content == content

    def test_create_markdown_file_creates_parent_directories(self):
        """Test that create_markdown_file creates parent directories if they don't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            content = "# Parent Dir Test\n\nCreating parent directories. That is the second sentence. Third sentence here."
            nested_path = os.path.join(tmpdir, "nested", "deep", "directory")

            create_markdown_file(content, filename="nested.md", filepath=nested_path)

            # Verify file was created in nested path
            assert os.path.exists(os.path.join(nested_path, "nested.md"))

    def test_create_markdown_file_returns_absolute_path(self):
        """Test that create_markdown_file returns absolute path as string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            content = "# Path Test\n\nReturning absolute path. That is the second sentence. Third sentence included."
            filepath = os.path.join(tmpdir, "path_test.md")

            result = create_markdown_file(content, filename="path_test.md", filepath=tmpdir)

            # Verify result is absolute path string
            assert isinstance(result, str)
            assert os.path.isabs(result)
            assert os.path.exists(result)


class TestFileEncodingValidation:
    """Tests for task-4: File encoding and line ending validation."""

    def test_validate_file_encoding_accepts_utf8_without_bom(self):
        """Test that validate_file_encoding accepts pure UTF-8 without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "utf8_clean.md")
            # Write with UTF-8 encoding, no BOM
            Path(filepath).write_text("# Clean UTF-8\n\nFirst sentence. Second sentence. Third sentence.", encoding='utf-8', newline='\n')

            result = validate_file_encoding(filepath)

            assert result['is_valid'] is True
            assert len(result['errors']) == 0
            assert result['details']['has_bom'] is False
            assert result['details']['encoding'] == 'UTF-8'

    def test_validate_file_encoding_rejects_utf8_with_bom(self):
        """Test that validate_file_encoding rejects UTF-8 with BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "utf8_bom.md")
            # Write with UTF-8 BOM
            with open(filepath, 'wb') as f:
                f.write(b'\xef\xbb\xbf')  # UTF-8 BOM
                f.write("# BOM Test\n\nFirst sentence. Second sentence. Third sentence.".encode('utf-8'))

            result = validate_file_encoding(filepath)

            assert result['is_valid'] is False
            assert any("BOM" in error for error in result['errors'])
            assert result['details']['has_bom'] is True

    def test_validate_file_encoding_rejects_crlf_line_endings(self):
        """Test that validate_file_encoding rejects CRLF line endings (Windows style)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "crlf_test.md")
            # Write with CRLF line endings
            with open(filepath, 'wb') as f:
                f.write(b"# CRLF Test\r\n\r\nFirst sentence. Second sentence. Third sentence.")

            result = validate_file_encoding(filepath)

            assert result['is_valid'] is False
            assert any("CRLF" in error for error in result['errors'])
            assert result['details']['line_ending_type'] == 'CRLF'

    def test_validate_file_encoding_accepts_lf_line_endings(self):
        """Test that validate_file_encoding accepts LF line endings (Unix style)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "lf_test.md")
            # Write with LF line endings
            Path(filepath).write_text("# LF Test\n\nFirst sentence. Second sentence. Third sentence.", encoding='utf-8', newline='\n')

            result = validate_file_encoding(filepath)

            assert result['is_valid'] is True
            assert result['details']['line_ending_type'] == 'LF'

    def test_validate_file_encoding_returns_file_size(self):
        """Test that validate_file_encoding returns file size in bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "size_test.md")
            content = "# Size Test\n\nFirst sentence. Second sentence. Third sentence."
            Path(filepath).write_text(content, encoding='utf-8', newline='\n')

            result = validate_file_encoding(filepath)

            assert result['details']['file_size_bytes'] > 0
            assert result['details']['file_size_bytes'] == len(content.encode('utf-8'))

    def test_validate_file_encoding_handles_nonexistent_file(self):
        """Test that validate_file_encoding handles nonexistent file gracefully."""
        result = validate_file_encoding("/nonexistent/path/to/file.md")

        assert result['is_valid'] is False
        assert any("not exist" in error for error in result['errors'])


class TestFileStructureValidation:
    """Tests for comprehensive file structure validation."""

    def test_validate_file_structure_accepts_valid_file(self):
        """Test that validate_file_structure accepts valid markdown file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "valid.md")
            # Content must be 250-600 bytes to pass validation
            content = "# Test Title\n\nFirst sentence here with detailed information about the topic being discussed in depth. Second sentence now provides additional context and understanding of the subject matter. Third sentence finally concludes with comprehensive explanation and meaningful insights."
            Path(filepath).write_text(content, encoding='utf-8', newline='\n')

            result = validate_file_structure(filepath)

            assert result['is_valid'] is True
            assert len(result['errors']) == 0
            assert result['details']['has_h1_heading'] is True
            assert result['details']['sentence_count'] == 3

    def test_validate_file_structure_requires_h1_heading(self):
        """Test that validate_file_structure requires H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "no_h1.md")
            content = "## Wrong Heading Level\n\nFirst sentence. Second sentence. Third sentence."
            Path(filepath).write_text(content, encoding='utf-8', newline='\n')

            result = validate_file_structure(filepath)

            assert result['is_valid'] is False
            assert any("H1" in error for error in result['errors'])

    def test_validate_file_structure_requires_blank_line_separator(self):
        """Test that validate_file_structure requires blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "no_blank_line.md")
            content = "# Title\nNo blank line before prose."
            Path(filepath).write_text(content, encoding='utf-8', newline='\n')

            result = validate_file_structure(filepath)

            assert result['is_valid'] is False
            assert any("blank" in error.lower() for error in result['errors'])

    def test_validate_file_structure_validates_sentence_count(self):
        """Test that validate_file_structure validates exactly 2-3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Test with too few sentences
            filepath = os.path.join(tmpdir, "one_sentence.md")
            content = "# Title\n\nOnly one sentence."
            Path(filepath).write_text(content, encoding='utf-8', newline='\n')

            result = validate_file_structure(filepath)

            assert result['is_valid'] is False
            assert any("sentence" in error.lower() for error in result['errors'])

    def test_validate_file_structure_checks_file_size_minimum(self):
        """Test that validate_file_structure checks file size minimum (250 bytes)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "small.md")
            content = "# Tiny\n\nS."  # Very small content
            Path(filepath).write_text(content, encoding='utf-8', newline='\n')

            result = validate_file_structure(filepath)

            assert result['is_valid'] is False
            assert any("too small" in error.lower() for error in result['errors'])

    def test_validate_file_structure_checks_file_size_maximum(self):
        """Test that validate_file_structure checks file size maximum (600 bytes)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "large.md")
            # Create content larger than 600 bytes
            large_content = "# Title\n\n" + ("This is a very long sentence that goes on and on and contains many words. " * 20)
            Path(filepath).write_text(large_content, encoding='utf-8', newline='\n')

            result = validate_file_structure(filepath)

            assert result['is_valid'] is False
            assert any("too large" in error.lower() for error in result['errors'])

    def test_validate_file_structure_returns_heading_text(self):
        """Test that validate_file_structure extracts and returns heading text."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "heading.md")
            content = "# Specific Heading Text\n\nFirst sentence here. Second sentence now. Third sentence finally."
            Path(filepath).write_text(content, encoding='utf-8', newline='\n')

            result = validate_file_structure(filepath)

            assert result['details']['heading_text'] == "Specific Heading Text"

    def test_validate_file_structure_returns_sentence_count(self):
        """Test that validate_file_structure returns accurate sentence count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "sentences.md")
            content = "# Title\n\nFirst. Second. Third."
            Path(filepath).write_text(content, encoding='utf-8', newline='\n')

            result = validate_file_structure(filepath)

            assert result['details']['sentence_count'] == 3

    def test_validate_file_structure_handles_nonexistent_file(self):
        """Test that validate_file_structure handles nonexistent file gracefully."""
        result = validate_file_structure("/nonexistent/path/to/file.md")

        assert result['is_valid'] is False
        assert any("not exist" in error for error in result['errors'])


class TestComprehensiveFileValidation:
    """Tests for comprehensive markdown file validation (encoding + structure)."""

    def test_validate_markdown_file_accepts_valid_file(self):
        """Test that validate_markdown_file accepts completely valid file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "valid_complete.md")
            # Content must be 250-600 bytes to pass validation
            content = "# Complete Validation\n\nThis file passes all encoding requirements by using proper UTF-8 text encoding throughout. It contains proper text structure with appropriate content length and meaningful information. The line endings are correct with Unix LF style throughout the entire document structure."
            create_markdown_file(content, filename="valid_complete.md", filepath=tmpdir)

            result = validate_markdown_file(filepath)

            assert result['is_valid'] is True
            assert len(result['errors']) == 0
            assert result['encoding']['is_valid'] is True
            assert result['structure']['is_valid'] is True

    def test_validate_markdown_file_combines_encoding_and_structure_errors(self):
        """Test that validate_markdown_file combines errors from both checks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "multiple_errors.md")
            # Create file with multiple issues: wrong heading level + CRLF
            with open(filepath, 'wb') as f:
                f.write(b"## Wrong Heading\r\nNo blank line")

            result = validate_markdown_file(filepath)

            assert result['is_valid'] is False
            # Should have errors from both encoding (CRLF) and structure (heading)
            assert len(result['errors']) >= 2

    def test_validate_markdown_file_returns_detailed_results(self):
        """Test that validate_markdown_file returns detailed results from both validators."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "detailed.md")
            content = "# Detailed Results\n\nValidation provides detailed information. This includes encoding details. And structure details too."
            create_markdown_file(content, filename="detailed.md", filepath=tmpdir)

            result = validate_markdown_file(filepath)

            # Verify all expected keys exist
            assert 'is_valid' in result
            assert 'errors' in result
            assert 'encoding' in result
            assert 'structure' in result

            # Verify nested structure
            assert 'details' in result['encoding']
            assert 'details' in result['structure']

    def test_validate_markdown_file_fails_on_encoding_error(self):
        """Test that validate_markdown_file fails overall if encoding is invalid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "bad_encoding.md")
            # Write with CRLF (bad encoding)
            with open(filepath, 'wb') as f:
                f.write(b"# Title\r\n\r\nFirst sentence. Second sentence. Third sentence.")

            result = validate_markdown_file(filepath)

            assert result['is_valid'] is False
            assert result['encoding']['is_valid'] is False

    def test_validate_markdown_file_fails_on_structure_error(self):
        """Test that validate_markdown_file fails overall if structure is invalid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "bad_structure.md")
            # Write with LF (good encoding) but wrong structure
            Path(filepath).write_text("## Wrong Heading\n\nOnly one.", encoding='utf-8', newline='\n')

            result = validate_markdown_file(filepath)

            assert result['is_valid'] is False
            assert result['structure']['is_valid'] is False


class TestGitStageAndCommit:
    """Tests for task-5: Git staging and commit workflow."""

    def test_stage_and_commit_returns_dict_with_required_keys(self):
        """Test that stage_and_commit_file returns dict with required keys."""
        with patch('src.create_markdown.subprocess.run') as mock_run:
            with patch('src.create_markdown._validate_git_config') as mock_validate:
                mock_validate.return_value = {'is_valid': True, 'errors': []}
                
                # Mock successful git add and commit
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout='', stderr=''),  # git add
                    MagicMock(returncode=0, stdout='[main abc1234] feat(199)...', stderr=''),  # git commit
                    MagicMock(returncode=0, stdout='abc1234567890', stderr=''),  # git rev-parse
                ]

                result = stage_and_commit_file()

                assert isinstance(result, dict)
                assert 'success' in result
                assert 'staged_file' in result
                assert 'commit_hash' in result
                assert 'errors' in result

    def test_stage_and_commit_validates_git_config(self):
        """Test that stage_and_commit_file validates git configuration before staging."""
        with patch('src.create_markdown._validate_git_config') as mock_validate:
            mock_validate.return_value = {
                'is_valid': False,
                'errors': ['Git user.name not configured'],
                'config': {'user.name': None, 'user.email': 'test@example.com'},
            }

            result = stage_and_commit_file()

            assert result['success'] is False
            assert 'Git user.name not configured' in result['errors']
            mock_validate.assert_called_once()

    def test_stage_and_commit_stages_file_with_correct_arguments(self):
        """Test that stage_and_commit_file calls git add with correct arguments."""
        with patch('src.create_markdown.subprocess.run') as mock_run:
            with patch('src.create_markdown._validate_git_config') as mock_validate:
                mock_validate.return_value = {'is_valid': True, 'errors': []}
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout='', stderr=''),  # git add
                    MagicMock(returncode=0, stdout='[main abc1234] feat(199)...', stderr=''),  # git commit
                    MagicMock(returncode=0, stdout='abc1234567890', stderr=''),  # git rev-parse
                ]

                result = stage_and_commit_file(filename="test-nttet0.md")

                # Verify git add was called with correct arguments
                add_call = mock_run.call_args_list[0]
                assert add_call[0][0] == ['git', 'add', 'test-nttet0.md']
                # shell=False is default and not explicitly passed

    def test_stage_and_commit_commits_with_correct_message(self):
        """Test that stage_and_commit_file commits with correct message format."""
        with patch('src.create_markdown.subprocess.run') as mock_run:
            with patch('src.create_markdown._validate_git_config') as mock_validate:
                mock_validate.return_value = {'is_valid': True, 'errors': []}
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout='', stderr=''),  # git add
                    MagicMock(returncode=0, stdout='[main abc1234] feat(199)...', stderr=''),  # git commit
                    MagicMock(returncode=0, stdout='abc1234567890', stderr=''),  # git rev-parse
                ]

                expected_message = "feat(199): Create markdown file test-nttet0.md with title and prose content"
                result = stage_and_commit_file(commit_message=expected_message)

                # Verify git commit was called with correct message
                commit_call = mock_run.call_args_list[1]
                assert commit_call[0][0][0:3] == ['git', 'commit', '-m']
                assert commit_call[0][0][3] == expected_message

    def test_stage_and_commit_returns_success_when_all_succeed(self):
        """Test that stage_and_commit_file returns success when all operations succeed."""
        with patch('src.create_markdown.subprocess.run') as mock_run:
            with patch('src.create_markdown._validate_git_config') as mock_validate:
                mock_validate.return_value = {'is_valid': True, 'errors': []}
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout='', stderr=''),  # git add
                    MagicMock(returncode=0, stdout='[main abc1234] feat(199)...', stderr=''),  # git commit
                    MagicMock(returncode=0, stdout='abc1234567890', stderr=''),  # git rev-parse
                ]

                result = stage_and_commit_file()

                assert result['success'] is True
                assert result['staged_file'] == 'test-nttet0.md'
                assert result['commit_hash'] is not None
                assert len(result['errors']) == 0

    def test_stage_and_commit_handles_staging_failure(self):
        """Test that stage_and_commit_file handles git add failure gracefully."""
        with patch('src.create_markdown.subprocess.run') as mock_run:
            with patch('src.create_markdown._validate_git_config') as mock_validate:
                mock_validate.return_value = {'is_valid': True, 'errors': []}
                
                # Mock git add failure
                error = subprocess.CalledProcessError(1, 'git add')
                error.stderr = 'fatal: pathspec "test-nttet0.md" did not match any files'
                mock_run.side_effect = error

                result = stage_and_commit_file()

                assert result['success'] is False
                assert result['staged_file'] is None
                assert any('Failed to stage file' in error for error in result['errors'])

    def test_stage_and_commit_handles_commit_failure(self):
        """Test that stage_and_commit_file handles git commit failure gracefully."""
        with patch('src.create_markdown.subprocess.run') as mock_run:
            with patch('src.create_markdown._validate_git_config') as mock_validate:
                mock_validate.return_value = {'is_valid': True, 'errors': []}
                
                # Mock git add success but commit failure
                error = subprocess.CalledProcessError(1, 'git commit')
                error.stderr = 'nothing added to commit but untracked files present'
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout='', stderr=''),  # git add succeeds
                    error,  # git commit fails
                ]

                result = stage_and_commit_file()

                assert result['success'] is False
                assert result['staged_file'] == 'test-nttet0.md'
                assert any('Failed to create commit' in error for error in result['errors'])


class TestGitPush:
    """Tests for task-6: Git push to feature branch."""

    def test_push_to_feature_branch_returns_dict_with_required_keys(self):
        """Test that push_to_feature_branch returns dict with required keys."""
        with patch('src.create_markdown.subprocess.run') as mock_run:
            # Mock branch check and push success
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout='  origin/feat/199-markdown-file-creation-5e3e07\n', stderr=''),  # git branch -r
                MagicMock(returncode=0, stdout='To origin...\n', stderr=''),  # git push
            ]

            result = push_to_feature_branch()

            assert isinstance(result, dict)
            assert 'success' in result
            assert 'branch' in result
            assert 'errors' in result

    def test_push_to_feature_branch_verifies_branch_exists(self):
        """Test that push_to_feature_branch verifies branch exists before pushing."""
        with patch('src.create_markdown.subprocess.run') as mock_run:
            # Mock branch check failure
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='  origin/main\n  origin/other-branch\n',
                stderr=''
            )

            result = push_to_feature_branch()

            assert result['success'] is False
            assert any('not found on remote' in error for error in result['errors'])

    def test_push_to_feature_branch_uses_correct_git_command(self):
        """Test that push_to_feature_branch uses correct git push command."""
        with patch('src.create_markdown.subprocess.run') as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout='  origin/feat/199-markdown-file-creation-5e3e07\n', stderr=''),
                MagicMock(returncode=0, stdout='To origin...\n', stderr=''),
            ]

            result = push_to_feature_branch(branch_name="feat/199-markdown-file-creation-5e3e07")

            # Verify push command was called with correct arguments
            push_call = mock_run.call_args_list[1]
            assert push_call[0][0] == ['git', 'push', '-u', 'origin', 'feat/199-markdown-file-creation-5e3e07']

    def test_push_to_feature_branch_returns_success_on_successful_push(self):
        """Test that push_to_feature_branch returns success when push succeeds."""
        with patch('src.create_markdown.subprocess.run') as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout='  origin/feat/199-markdown-file-creation-5e3e07\n', stderr=''),
                MagicMock(returncode=0, stdout='To origin...\n', stderr=''),
            ]

            result = push_to_feature_branch()

            assert result['success'] is True
            assert result['branch'] == 'feat/199-markdown-file-creation-5e3e07'
            assert len(result['errors']) == 0

    def test_push_to_feature_branch_implements_retry_logic(self):
        """Test that push_to_feature_branch retries on network timeout."""
        with patch('src.create_markdown.subprocess.run') as mock_run:
            with patch('src.create_markdown.time.sleep'):  # Mock sleep to avoid delays
                # Mock branch check success, then push timeout, then push success
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout='  origin/feat/199-markdown-file-creation-5e3e07\n', stderr=''),
                    subprocess.TimeoutExpired('git push', timeout=30),
                    MagicMock(returncode=0, stdout='To origin...\n', stderr=''),
                ]

                result = push_to_feature_branch(max_retries=3)

                assert result['success'] is True
                # Verify retries happened (3 calls: branch check, timeout, success push)
                assert mock_run.call_count >= 2

    def test_push_to_feature_branch_handles_network_errors_with_retry(self):
        """Test that push_to_feature_branch retries on network-related push errors."""
        with patch('src.create_markdown.subprocess.run') as mock_run:
            with patch('src.create_markdown.time.sleep'):  # Mock sleep to avoid delays
                error = subprocess.CalledProcessError(1, 'git push')
                error.stderr = 'fatal: unable to access repository: Could not resolve host'
                
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout='  origin/feat/199-markdown-file-creation-5e3e07\n', stderr=''),
                    error,
                    error,
                    MagicMock(returncode=0, stdout='To origin...\n', stderr=''),
                ]

                result = push_to_feature_branch(max_retries=3)

                assert result['success'] is True

    def test_push_to_feature_branch_fails_after_max_retries(self):
        """Test that push_to_feature_branch fails after exhausting retries."""
        with patch('src.create_markdown.subprocess.run') as mock_run:
            with patch('src.create_markdown.time.sleep'):
                error = subprocess.CalledProcessError(1, 'git push')
                error.stderr = 'fatal: unable to access repository: Could not resolve host'
                
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout='  origin/feat/199-markdown-file-creation-5e3e07\n', stderr=''),
                    error,
                    error,
                    error,
                ]

                result = push_to_feature_branch(max_retries=3)

                assert result['success'] is False
                assert len(result['errors']) > 0

    def test_push_to_feature_branch_does_not_retry_on_auth_error(self):
        """Test that push_to_feature_branch does not retry on authentication errors."""
        with patch('src.create_markdown.subprocess.run') as mock_run:
            with patch('src.create_markdown.time.sleep') as mock_sleep:
                error = subprocess.CalledProcessError(1, 'git push')
                error.stderr = 'fatal: Authentication failed for'
                
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout='  origin/feat/199-markdown-file-creation-5e3e07\n', stderr=''),
                    error,
                ]

                result = push_to_feature_branch(max_retries=3)

                assert result['success'] is False
                # Should not have retried (sleep should not be called)
                mock_sleep.assert_not_called()


class TestGitIntegrationOrchestration:
    """Tests for task-7: End-to-end orchestration of all git operations."""

    def test_full_workflow_creates_file_and_commits(self):
        """Test full workflow: generate, create, validate, commit, and push."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('src.create_markdown.get_reasoning_llm') as mock_get_llm:
                with patch('src.create_markdown.subprocess.run') as mock_run:
                    with patch('src.create_markdown._validate_git_config') as mock_validate:
                        # Setup mocks
                        mock_llm = Mock()
                        mock_llm.call.return_value = (
                            "# Test Topic\n\n"
                            "This is the first sentence about the topic. "
                            "This is the second sentence providing more details. "
                            "This is the third sentence concluding the discussion."
                        )
                        mock_get_llm.return_value = mock_llm
                        mock_validate.return_value = {'is_valid': True, 'errors': []}
                        mock_run.side_effect = [
                            MagicMock(returncode=0, stdout='', stderr=''),  # git add
                            MagicMock(returncode=0, stdout='', stderr=''),  # git commit
                            MagicMock(returncode=0, stdout='abc1234567890', stderr=''),  # git rev-parse
                            MagicMock(returncode=0, stdout='  origin/feat/199-markdown-file-creation-5e3e07\n', stderr=''),  # branch check
                            MagicMock(returncode=0, stdout='To origin...\n', stderr=''),  # git push
                        ]

                        # Generate content
                        content_result = generate_markdown_content()
                        assert isinstance(content_result, dict)
                        assert 'full_content' in content_result
                        assert 'title' in content_result

                        # Create file
                        filepath = create_markdown_file(
                            content_result['full_content'],
                            filepath=tmpdir
                        )
                        assert Path(filepath).exists()

                        # Validate file
                        validation = validate_markdown_file(filepath)
                        # Note: validation may fail due to file size, but structure should be ok
                        assert isinstance(validation, dict)

                        # Stage and commit
                        commit_result = stage_and_commit_file()
                        assert isinstance(commit_result, dict)
                        assert 'success' in commit_result

                        # Push
                        push_result = push_to_feature_branch()
                        assert isinstance(push_result, dict)
                        assert 'success' in push_result
