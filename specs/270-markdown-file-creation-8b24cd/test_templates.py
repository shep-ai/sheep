"""
Tests for template pool validation in feature 270.

Validates that all templates meet requirements for markdown file creation:
- 30+ templates available
- Each template has 'title' and 'prose' string keys
- Each template produces 400-600 byte markdown files
- All prose contains 2-3 sentences ending with proper punctuation
"""

import pytest
from templates import (
    TEMPLATES,
    load_templates,
    calculate_markdown_bytes,
    validate_template,
    validate_all_templates,
)


class TestTemplatePoolLoading:
    """Tests for loading the template pool."""

    def test_load_templates_returns_list(self) -> None:
        """load_templates() returns a list."""
        templates = load_templates()
        assert isinstance(templates, list)

    def test_load_templates_has_minimum_count(self) -> None:
        """Template pool has at least 30 templates."""
        templates = load_templates()
        assert len(templates) >= 30

    def test_templates_constant_matches_loader(self) -> None:
        """TEMPLATES constant matches load_templates() result."""
        assert TEMPLATES == load_templates()


class TestTemplateStructure:
    """Tests for template structure and schema."""

    def test_each_template_is_dict(self) -> None:
        """Each template is a dictionary."""
        for template in TEMPLATES:
            assert isinstance(template, dict)

    def test_each_template_has_title_key(self) -> None:
        """Each template has 'title' key."""
        for template in TEMPLATES:
            assert 'title' in template

    def test_each_template_has_prose_key(self) -> None:
        """Each template has 'prose' key."""
        for template in TEMPLATES:
            assert 'prose' in template

    def test_title_is_string(self) -> None:
        """Each title is a string."""
        for template in TEMPLATES:
            assert isinstance(template['title'], str)

    def test_prose_is_string(self) -> None:
        """Each prose is a string."""
        for template in TEMPLATES:
            assert isinstance(template['prose'], str)

    def test_no_extra_keys_in_template(self) -> None:
        """Templates have only 'title' and 'prose' keys."""
        for template in TEMPLATES:
            assert set(template.keys()) == {'title', 'prose'}


class TestTitleValidation:
    """Tests for title field requirements."""

    def test_each_title_is_nonempty(self) -> None:
        """Each title is non-empty."""
        for template in TEMPLATES:
            assert len(template['title']) > 0

    def test_each_title_has_minimum_length(self) -> None:
        """Each title is at least 3 characters."""
        for template in TEMPLATES:
            assert len(template['title']) >= 3

    def test_each_title_has_reasonable_max_length(self) -> None:
        """Each title is at most 100 characters."""
        for template in TEMPLATES:
            assert len(template['title']) <= 100

    def test_title_is_not_just_whitespace(self) -> None:
        """Title is not just whitespace."""
        for template in TEMPLATES:
            assert template['title'].strip() == template['title']


class TestProseValidation:
    """Tests for prose field requirements."""

    def test_each_prose_is_nonempty(self) -> None:
        """Each prose is non-empty."""
        for template in TEMPLATES:
            assert len(template['prose']) > 0

    def test_each_prose_has_minimum_length(self) -> None:
        """Each prose is at least 100 characters."""
        for template in TEMPLATES:
            assert len(template['prose']) >= 100

    def test_each_prose_has_sentence_count(self) -> None:
        """Each prose has 2-3 sentences (ends with . ! or ?)."""
        for i, template in enumerate(TEMPLATES):
            prose = template['prose']
            sentence_endings = sum(1 for c in prose if c in '.!?')
            assert 2 <= sentence_endings <= 3, (
                f"Template {i} ({template['title']}) has {sentence_endings} sentences, "
                "expected 2-3"
            )

    def test_each_sentence_ends_with_punctuation(self) -> None:
        """Each sentence ends with . ! or ?."""
        for i, template in enumerate(TEMPLATES):
            prose = template['prose']
            # Split by sentence endings and check that each part ends appropriately
            sentences = []
            current = ""
            for char in prose:
                current += char
                if char in '.!?':
                    sentences.append(current)
                    current = ""

            # All non-empty remaining text should be just whitespace
            assert current.strip() == "", (
                f"Template {i}: prose ends with non-punctuated text: '{current}'"
            )

            # Check that we found sentences
            assert len(sentences) >= 2


class TestMarkdownBytesCalculation:
    """Tests for markdown byte size calculation."""

    def test_calculate_markdown_bytes_returns_int(self) -> None:
        """calculate_markdown_bytes() returns an integer."""
        result = calculate_markdown_bytes("Test", "This is a sentence.")
        assert isinstance(result, int)

    def test_calculate_markdown_bytes_simple_content(self) -> None:
        """calculate_markdown_bytes() calculates correct size for simple content."""
        # "# Test\n\nThis is a sentence.\n" should be this many bytes
        title = "Test"
        prose = "This is a sentence."
        expected = len("# Test\n\nThis is a sentence.\n".encode('utf-8'))
        result = calculate_markdown_bytes(title, prose)
        assert result == expected

    def test_calculate_markdown_bytes_utf8_encoded(self) -> None:
        """calculate_markdown_bytes() counts UTF-8 encoded bytes."""
        # Test with non-ASCII characters
        title = "Test"
        prose = "This is a café."
        byte_size = calculate_markdown_bytes(title, prose)
        content = f"# {title}\n\n{prose}\n"
        assert byte_size == len(content.encode('utf-8'))

    def test_calculate_markdown_bytes_includes_structure(self) -> None:
        """calculate_markdown_bytes() includes markdown structure bytes."""
        title = "Test"
        prose = "Content."
        byte_size = calculate_markdown_bytes(title, prose)
        # Should include: "# " + title + "\n\n" + prose + "\n"
        assert byte_size > len(title) + len(prose)
        assert "# " in f"# {title}" and "\n\n" in f"\n\n{prose}\n"


class TestTemplateValidation:
    """Tests for validate_template() function."""

    def test_validate_template_returns_tuple(self) -> None:
        """validate_template() returns a tuple."""
        template = {"title": "Test", "prose": "This is a test sentence."}
        result = validate_template(template)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_validate_template_success_returns_true_and_none(self) -> None:
        """validate_template() returns (True, None) for valid template."""
        template = {
            "title": "Test Title",
            "prose": "This is a comprehensive first sentence that explores the topic in detail and provides a solid foundation for understanding. The second sentence builds upon this foundation by providing additional context, examples, and deeper analysis of the subject matter. Finally, the third sentence brings everything together into a cohesive conclusion that ties all the threads together effectively."
        }
        is_valid, error = validate_template(template)
        assert is_valid is True, f"Unexpected validation error: {error}"
        assert error is None

    def test_validate_template_non_dict_fails(self) -> None:
        """validate_template() fails if not a dict."""
        is_valid, error = validate_template("not a dict")  # type: ignore
        assert is_valid is False
        assert error is not None

    def test_validate_template_missing_title_fails(self) -> None:
        """validate_template() fails if title key is missing."""
        is_valid, error = validate_template({"prose": "Test."})
        assert is_valid is False
        assert "title" in error

    def test_validate_template_missing_prose_fails(self) -> None:
        """validate_template() fails if prose key is missing."""
        is_valid, error = validate_template({"title": "Test"})
        assert is_valid is False
        assert "prose" in error

    def test_validate_template_invalid_byte_range(self) -> None:
        """validate_template() fails if byte size is outside 400-600."""
        # Create a template with enough prose but that will be outside byte range
        # (e.g., much longer than 600 bytes - but we need valid prose first)
        short_template = {"title": "Test", "prose": "Short."}
        is_valid, error = validate_template(short_template)
        assert is_valid is False
        # First check is prose length
        assert "100 characters" in error or "bytes" in error

    def test_all_templates_pass_validation(self) -> None:
        """All templates in TEMPLATES pass validate_template()."""
        for i, template in enumerate(TEMPLATES):
            is_valid, error = validate_template(template)
            assert is_valid, f"Template {i} ({template['title']}) failed: {error}"


class TestAllTemplatesValidation:
    """Tests for validate_all_templates() function."""

    def test_validate_all_templates_returns_tuple(self) -> None:
        """validate_all_templates() returns a tuple."""
        result = validate_all_templates()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_validate_all_templates_all_pass(self) -> None:
        """validate_all_templates() returns all_valid=True."""
        all_valid, errors = validate_all_templates()
        assert all_valid is True
        assert len(errors) == 0


class TestTemplateByteRange:
    """Tests for template byte size range compliance."""

    def test_all_templates_produce_400_600_bytes(self) -> None:
        """All templates produce 400-600 byte markdown files."""
        for i, template in enumerate(TEMPLATES):
            byte_size = calculate_markdown_bytes(template['title'], template['prose'])
            assert 400 <= byte_size <= 600, (
                f"Template {i} ({template['title']}) produces {byte_size} bytes, "
                "expected 400-600"
            )

    def test_no_template_below_400_bytes(self) -> None:
        """No template produces less than 400 bytes."""
        for template in TEMPLATES:
            byte_size = calculate_markdown_bytes(template['title'], template['prose'])
            assert byte_size >= 400

    def test_no_template_above_600_bytes(self) -> None:
        """No template produces more than 600 bytes."""
        for template in TEMPLATES:
            byte_size = calculate_markdown_bytes(template['title'], template['prose'])
            assert byte_size <= 600


class TestTemplateContent:
    """Tests for template content quality."""

    def test_all_templates_have_unique_titles(self) -> None:
        """All templates have unique titles."""
        titles = [t['title'] for t in TEMPLATES]
        assert len(titles) == len(set(titles)), "Duplicate titles found"

    def test_all_templates_have_unique_prose(self) -> None:
        """All templates have unique prose content."""
        prose_texts = [t['prose'] for t in TEMPLATES]
        assert len(prose_texts) == len(set(prose_texts)), "Duplicate prose found"

    def test_template_pool_has_topic_diversity(self) -> None:
        """Template pool covers diverse topics."""
        # Check that we have templates from multiple categories
        titles = [t['title'].lower() for t in TEMPLATES]

        # Expect some tech/software topics
        tech_topics = sum(1 for t in titles if any(
            word in t for word in ['code', 'testing', 'development', 'api',
                                   'intelligence', 'research', 'algorithm']
        ))

        # Expect some personal development topics
        personal_topics = sum(1 for t in titles if any(
            word in t for word in ['persisten', 'learning', 'collaborat',
                                   'resilience', 'creativity']
        ))

        # Expect some nature/environment topics
        nature_topics = sum(1 for t in titles if any(
            word in t for word in ['forest', 'ocean', 'ecosystem', 'energy',
                                   'climate', 'wildlife']
        ))

        # Each category should have at least some representation
        assert tech_topics > 0, "No tech/software topics found"
        assert personal_topics > 0, "No personal development topics found"
        assert nature_topics > 0, "No nature/environment topics found"
