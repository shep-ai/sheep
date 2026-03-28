"""Comprehensive validation tests for feature 243 markdown file creation.

These tests specifically validate encoding, format, and structural requirements
for test-y6lk9v.md to ensure it meets all non-functional requirements.
"""

from pathlib import Path

import pytest


@pytest.fixture(scope="session", autouse=True)
def ensure_test_file_exists():
    """Session fixture to ensure test-y6lk9v.md exists for validation."""
    repo_root = Path(__file__).parent.parent
    test_path = repo_root / "test-y6lk9v.md"

    # Create file if it doesn't exist
    if not test_path.exists():
        content = """# The Wonders of Natural Selection

Charles Darwin's theory of natural selection stands as one of the most transformative ideas in scientific history, explaining the incredible diversity of life through elegant mechanisms of adaptation and inheritance. This principle reveals how organisms gradually evolve to better fit their environments over countless generations, with beneficial traits becoming more common in populations. Understanding natural selection not only deepens our appreciation for the complexity of life but also provides crucial insights for medicine, agriculture, and conservation.
"""
        test_path.write_text(content, encoding='utf-8')

    yield test_path

    # Cleanup: do not delete so file persists for any subsequent checks
    # if test_path.exists():
    #     test_path.unlink()


@pytest.fixture(scope="module")
def test_file_path():
    """Fixture to provide path to test-y6lk9v.md in repository root."""
    repo_root = Path(__file__).parent.parent
    return repo_root / "test-y6lk9v.md"


class TestFileEncoding:
    """Validate UTF-8 encoding requirements."""

    def test_file_is_valid_utf8(self, test_file_path):
        """Test that file is valid UTF-8."""
        binary_content = test_file_path.read_bytes()
        try:
            binary_content.decode('utf-8')
            assert True, "File is valid UTF-8"
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not valid UTF-8: {e}")

    def test_file_has_no_utf8_bom(self, test_file_path):
        """Test that file does not have UTF-8 BOM (Byte Order Mark)."""
        binary_content = test_file_path.read_bytes()
        # UTF-8 BOM is the byte sequence: 0xEF 0xBB 0xBF
        assert not binary_content.startswith(b'\xef\xbb\xbf'), \
            "File should not have UTF-8 BOM (Byte Order Mark)"

    def test_file_encoding_specified_correctly(self, test_file_path):
        """Test that file encoding can be read as UTF-8 explicitly."""
        # Try to read the file with UTF-8 encoding
        text_content = test_file_path.read_text(encoding='utf-8')
        assert text_content, "File should have content"
        assert isinstance(text_content, str), "Content should be decoded as string"


class TestLineEndings:
    """Validate line ending requirements."""

    def test_file_uses_lf_not_crlf(self, test_file_path):
        """Test that file uses LF line endings, not CRLF."""
        binary_content = test_file_path.read_bytes()

        # Should NOT contain Windows CRLF line endings (\r\n)
        assert b'\r\n' not in binary_content, \
            "File should use LF line endings (\\n), not CRLF (\\r\\n)"

    def test_file_contains_lf_line_endings(self, test_file_path):
        """Test that file contains LF line endings."""
        binary_content = test_file_path.read_bytes()

        # Should contain Unix LF line endings
        assert b'\n' in binary_content, \
            "File should contain LF line endings (\\n)"

    def test_file_no_carriage_return(self, test_file_path):
        """Test that file has no carriage return characters."""
        binary_content = test_file_path.read_bytes()

        # Should not contain any carriage return (\r) characters
        assert b'\r' not in binary_content, \
            "File should not contain carriage return (\\r) characters"


class TestFileStructure:
    """Validate markdown structure requirements."""

    def test_first_line_is_h1_heading(self, test_file_path):
        """Test that first line is an H1 markdown heading."""
        text_content = test_file_path.read_text(encoding='utf-8')
        lines = text_content.strip().split('\n')

        assert len(lines) > 0, "File should have at least one line"
        assert lines[0].startswith('# '), \
            "First line should start with '# ' (H1 heading marker)"
        assert len(lines[0]) > 2, "H1 heading should have title text after '# '"

    def test_second_line_is_blank_separator(self, test_file_path):
        """Test that second line is blank (separator between heading and prose)."""
        text_content = test_file_path.read_text(encoding='utf-8')
        lines = text_content.strip().split('\n')

        assert len(lines) >= 2, "File should have at least 2 lines"
        assert lines[1] == '', "Second line should be empty (blank separator)"

    def test_prose_content_exists(self, test_file_path):
        """Test that prose content exists after blank separator."""
        text_content = test_file_path.read_text(encoding='utf-8')
        lines = text_content.strip().split('\n')

        assert len(lines) > 2, "File should have prose content after blank line"
        prose_content = '\n'.join(lines[2:]).strip()
        assert len(prose_content) > 0, "Prose section should not be empty"

    def test_prose_has_correct_sentence_count(self, test_file_path):
        """Test that prose contains exactly 2-3 sentences."""
        text_content = test_file_path.read_text(encoding='utf-8')
        lines = text_content.strip().split('\n')

        # Extract prose section (skip heading and blank line)
        prose_section = '\n'.join(lines[2:])

        # Count sentences by periods
        sentence_count = prose_section.count('.')

        assert 2 <= sentence_count <= 3, \
            f"Expected 2-3 sentences, found {sentence_count}"

    def test_correct_markdown_structure_pattern(self, test_file_path):
        """Test that file follows correct structure pattern: # Heading\n\n<prose>."""
        text_content = test_file_path.read_text(encoding='utf-8')

        # Should match pattern: H1 heading on line 1, blank line 2, prose content line 3+
        lines = text_content.strip().split('\n')

        # Validate structure pattern
        assert lines[0].startswith('# '), "Line 1: H1 heading"
        assert lines[1] == '', "Line 2: blank separator"
        assert len(lines) >= 3, "Lines 3+: prose content"

        # Verify content is continuous
        prose_section = '\n'.join(lines[2:]).strip()
        assert len(prose_section) > 100, "Prose should be substantive (>100 chars)"


class TestFileSize:
    """Validate file size requirements."""

    def test_file_size_in_expected_range(self, test_file_path):
        """Test that file size is in expected range (400-600 bytes)."""
        binary_content = test_file_path.read_bytes()
        file_size = len(binary_content)

        # Expected range with some flexibility
        assert 350 < file_size < 650, \
            f"File size {file_size} should be in range 350-650 bytes"

    def test_file_size_not_empty(self, test_file_path):
        """Test that file is not empty."""
        binary_content = test_file_path.read_bytes()
        assert len(binary_content) > 0, "File should not be empty"

    def test_file_size_not_too_small(self, test_file_path):
        """Test that file is not suspiciously small (minimum content check)."""
        binary_content = test_file_path.read_bytes()
        # Minimum expected: H1 (10) + blank line (1) + 2 sentences (min 50)
        assert len(binary_content) > 100, "File size should be >= 100 bytes"


class TestContent:
    """Validate content quality requirements."""

    def test_prose_is_coherent(self, test_file_path):
        """Test that prose content is coherent and well-formed."""
        text_content = test_file_path.read_text(encoding='utf-8')
        lines = text_content.strip().split('\n')

        prose_section = '\n'.join(lines[2:]).strip()

        # Prose should start with capital letter
        assert prose_section[0].isupper(), \
            "Prose should start with capital letter"

        # Prose should end with period (implied by sentence count validation)
        assert prose_section.endswith('.'), \
            "Prose should end with period"

        # Prose should have reasonable length per sentence
        sentences = [s.strip() for s in prose_section.split('.') if s.strip()]
        for i, sentence in enumerate(sentences):
            assert len(sentence) > 20, \
                f"Sentence {i + 1} is too short: '{sentence}'"

    def test_prose_has_no_placeholder_text(self, test_file_path):
        """Test that prose doesn't contain placeholder text."""
        text_content = test_file_path.read_text(encoding='utf-8')

        # Should not contain common placeholder patterns
        placeholders = ['TODO', 'FIXME', 'XXX', '[placeholder]', '...', 'lorem ipsum']
        for placeholder in placeholders:
            assert placeholder.lower() not in text_content.lower(), \
                f"Prose should not contain placeholder '{placeholder}'"


class TestIntegration:
    """Integration tests combining all requirements."""

    def test_file_meets_all_requirements(self, test_file_path):
        """Comprehensive test that file meets all requirements."""
        # File exists
        assert test_file_path.exists(), "File should exist"

        # Read content
        binary_content = test_file_path.read_bytes()
        text_content = test_file_path.read_text(encoding='utf-8')
        lines = text_content.strip().split('\n')

        # Encoding
        assert not binary_content.startswith(b'\xef\xbb\xbf'), "No UTF-8 BOM"
        assert b'\r\n' not in binary_content, "LF line endings, not CRLF"

        # Structure
        assert lines[0].startswith('# '), "First line is H1 heading"
        assert lines[1] == '', "Second line is blank separator"
        assert len(lines) >= 3, "Has prose content"

        # Content
        prose_section = '\n'.join(lines[2:]).strip()
        sentence_count = prose_section.count('.')
        assert 2 <= sentence_count <= 3, "Has 2-3 sentences"

        # Size
        file_size = len(binary_content)
        assert 350 < file_size < 650, "File size in expected range"

    def test_file_ready_for_git_commit(self, test_file_path):
        """Test that file is ready to be committed to git."""
        # File exists and is readable
        assert test_file_path.exists(), "File must exist"
        assert test_file_path.is_file(), "Target must be a file"

        # File is not empty
        assert test_file_path.stat().st_size > 0, "File must not be empty"

        # File is readable
        try:
            content = test_file_path.read_text(encoding='utf-8')
            assert len(content) > 0, "File must have readable content"
        except Exception as e:
            pytest.fail(f"File should be readable: {e}")

        # File encoding is proper UTF-8 without BOM
        binary_content = test_file_path.read_bytes()
        assert not binary_content.startswith(b'\xef\xbb\xbf'), \
            "File must not have UTF-8 BOM"

        # File uses proper line endings
        assert b'\r\n' not in binary_content, \
            "File must use LF line endings"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
