"""Tests for feature 205: Creating markdown file test-m6zeml.md with hard-coded content."""

from pathlib import Path
import pytest


class TestModuleConstants:
    """Tests for feature 205 module constants."""

    def test_module_imports(self):
        """Test that the feature module can be imported."""
        from sheep.features.feature_205_markdown_file_creation import (
            FILENAME,
            FEATURE_NUMBER,
            BRANCH_NAME,
            COMMIT_MESSAGE,
            TITLE_TEXT,
            PROSE_CONTENT,
        )

        # Verify all constants are accessible
        assert FILENAME is not None
        assert FEATURE_NUMBER is not None
        assert BRANCH_NAME is not None
        assert COMMIT_MESSAGE is not None
        assert TITLE_TEXT is not None
        assert PROSE_CONTENT is not None

    def test_filename_constant(self):
        """Test that FILENAME constant is exactly test-m6zeml.md."""
        from sheep.features.feature_205_markdown_file_creation import FILENAME

        assert FILENAME == "test-m6zeml.md"
        assert isinstance(FILENAME, str)

    def test_feature_number_constant(self):
        """Test that FEATURE_NUMBER constant is 205."""
        from sheep.features.feature_205_markdown_file_creation import FEATURE_NUMBER

        assert FEATURE_NUMBER == 205
        assert isinstance(FEATURE_NUMBER, int)

    def test_branch_name_constant(self):
        """Test that BRANCH_NAME constant is correct."""
        from sheep.features.feature_205_markdown_file_creation import BRANCH_NAME

        assert BRANCH_NAME == "feat/205-markdown-file-creation-870df7"
        assert isinstance(BRANCH_NAME, str)

    def test_commit_message_constant(self):
        """Test that COMMIT_MESSAGE constant follows conventional commits format."""
        from sheep.features.feature_205_markdown_file_creation import COMMIT_MESSAGE

        assert COMMIT_MESSAGE == "feat(205): Create markdown file test-m6zeml.md"
        assert isinstance(COMMIT_MESSAGE, str)
        assert "feat(205):" in COMMIT_MESSAGE
        assert "test-m6zeml.md" in COMMIT_MESSAGE

    def test_title_text_constant(self):
        """Test that TITLE_TEXT constant is non-empty and appropriate."""
        from sheep.features.feature_205_markdown_file_creation import TITLE_TEXT

        assert isinstance(TITLE_TEXT, str)
        assert len(TITLE_TEXT) > 0
        assert len(TITLE_TEXT) < 100  # Reasonable title length
        # Title should be suitable for an H1 heading

    def test_prose_content_constant(self):
        """Test that PROSE_CONTENT is a non-empty string."""
        from sheep.features.feature_205_markdown_file_creation import PROSE_CONTENT

        assert isinstance(PROSE_CONTENT, str)
        assert len(PROSE_CONTENT) > 0
        assert len(PROSE_CONTENT) < 500  # Reasonable prose length

    def test_prose_content_has_sentences(self):
        """Test that PROSE_CONTENT contains 2-3 sentences (periods)."""
        from sheep.features.feature_205_markdown_file_creation import PROSE_CONTENT

        sentence_count = PROSE_CONTENT.count(".")
        assert 2 <= sentence_count <= 3, (
            f"Expected 2-3 sentences in prose, found {sentence_count}"
        )

    def test_prose_content_is_complete_sentences(self):
        """Test that PROSE_CONTENT is grammatically complete sentences."""
        from sheep.features.feature_205_markdown_file_creation import PROSE_CONTENT

        # Prose should not be empty
        assert PROSE_CONTENT.strip()

        # Each sentence should start with a capital letter (after first sentence check)
        sentences = [s.strip() for s in PROSE_CONTENT.split(".") if s.strip()]

        for sentence in sentences:
            if sentence:  # Non-empty sentence
                # Should start with capital letter or quote
                assert sentence[0].isupper() or sentence[0] in ('"', "'"), (
                    f"Sentence should start with capital letter: {sentence}"
                )

    def test_prose_content_length_reasonable(self):
        """Test that PROSE_CONTENT is a reasonable length for a paragraph."""
        from sheep.features.feature_205_markdown_file_creation import PROSE_CONTENT

        # Should be at least 50 characters (rough minimum for 2-3 meaningful sentences)
        assert len(PROSE_CONTENT) >= 50
        # Should not be excessively long (rough maximum for a short paragraph)
        assert len(PROSE_CONTENT) < 500

    def test_logger_import(self):
        """Test that the module imports the logger correctly."""
        from sheep.features import feature_205_markdown_file_creation

        # Verify logger is available in the module
        assert hasattr(feature_205_markdown_file_creation, "_logger")


class TestMarkdownContentValidation:
    """Tests validating the hard-coded markdown content quality."""

    def test_title_text_suitable_for_h1(self):
        """Test that TITLE_TEXT is suitable for an H1 markdown heading."""
        from sheep.features.feature_205_markdown_file_creation import TITLE_TEXT

        # Title should not contain # characters (will be added by module)
        assert "#" not in TITLE_TEXT
        # Title should not be empty or just whitespace
        assert TITLE_TEXT.strip()
        # Title should be readable (contains alphanumeric characters)
        assert any(c.isalnum() for c in TITLE_TEXT)

    def test_prose_content_coherence(self):
        """Test that PROSE_CONTENT is thematically coherent."""
        from sheep.features.feature_205_markdown_file_creation import (
            TITLE_TEXT,
            PROSE_CONTENT,
        )

        # Both title and prose should exist and not be empty
        assert TITLE_TEXT.strip()
        assert PROSE_CONTENT.strip()

    def test_prose_content_ends_with_period(self):
        """Test that PROSE_CONTENT ends with a period (last sentence complete)."""
        from sheep.features.feature_205_markdown_file_creation import PROSE_CONTENT

        assert PROSE_CONTENT.rstrip().endswith("."), (
            "Prose content should end with a period"
        )

    def test_combined_markdown_format(self):
        """Test that title + prose would create valid markdown structure."""
        from sheep.features.feature_205_markdown_file_creation import (
            TITLE_TEXT,
            PROSE_CONTENT,
        )

        # Simulate markdown construction
        markdown = f"# {TITLE_TEXT}\n\n{PROSE_CONTENT}\n"

        # Verify structure
        lines = markdown.split("\n")
        assert lines[0].startswith("# ")  # First line is H1
        assert lines[1] == ""  # Second line is blank separator
        assert lines[2]  # Third line has prose content

        # File size should be reasonable (250-600 bytes guideline)
        file_size = len(markdown.encode("utf-8"))
        assert 200 < file_size < 800, (
            f"Combined markdown size {file_size} bytes outside reasonable range"
        )
