"""Tests for feature 207 validation functions.

Tests verify that all validation functions work correctly:
1. verify_file_exists() - checks file existence
2. validate_markdown_format() - checks H1 heading and blank line
3. extract_prose_content() - extracts prose after heading
4. count_sentences() - counts periods in prose
5. validate_sentence_count() - validates 2-3 sentences
6. validate_encoding() - checks UTF-8 without BOM
7. validate_line_endings() - checks Unix LF only
8. validate_file_size() - checks file size range
9. validate_markdown_file() - orchestrates all validations
"""

import sys
import tempfile
import os
from pathlib import Path


def setup_module():
    """Set up test environment by adding src to path."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


class TestVerifyFileExists:
    """Tests for verify_file_exists() function."""

    def test_verify_file_exists_on_existing_file(self):
        """Test verify_file_exists passes on existing file."""
        from sheep.features.feature_207_markdown_file_creation import verify_file_exists

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create a test file
                test_file = Path("test.md")
                test_file.write_text("# Test\n\nContent.")

                # Should not raise
                verify_file_exists("test.md")
            finally:
                os.chdir(original_cwd)

    def test_verify_file_exists_raises_on_missing_file(self):
        """Test verify_file_exists raises FileNotFoundError on missing file."""
        from sheep.features.feature_207_markdown_file_creation import verify_file_exists

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Try to verify non-existent file
                try:
                    verify_file_exists("nonexistent.md")
                    assert False, "Should have raised FileNotFoundError"
                except FileNotFoundError:
                    pass  # Expected
            finally:
                os.chdir(original_cwd)


class TestValidateMarkdownFormat:
    """Tests for validate_markdown_format() function."""

    def test_validate_markdown_format_on_valid_file(self):
        """Test validate_markdown_format passes on valid markdown."""
        from sheep.features.feature_207_markdown_file_creation import validate_markdown_format

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create valid markdown file
                Path("test.md").write_text("# Title\n\nProse content here.")

                # Should not raise
                validate_markdown_format("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_no_h1_heading(self):
        """Test validate_markdown_format fails without H1 heading."""
        from sheep.features.feature_207_markdown_file_creation import validate_markdown_format

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file without H1 heading
                Path("test.md").write_text("No heading here.\n\nJust prose.")

                try:
                    validate_markdown_format("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "H1" in str(e) or "heading" in str(e)
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_wrong_blank_line_position(self):
        """Test validate_markdown_format fails with wrong blank line position."""
        from sheep.features.feature_207_markdown_file_creation import validate_markdown_format

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file with no blank line after H1
                Path("test.md").write_text("# Title\nProse without blank line.")

                try:
                    validate_markdown_format("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "blank" in str(e).lower()
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_multiple_h1_headings(self):
        """Test validate_markdown_format fails with multiple H1 headings."""
        from sheep.features.feature_207_markdown_file_creation import validate_markdown_format

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file with multiple H1 headings
                Path("test.md").write_text("# Title\n\nContent.\n\n# Another Title")

                try:
                    validate_markdown_format("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "one" in str(e).lower() or "multiple" in str(e).lower()
            finally:
                os.chdir(original_cwd)


class TestExtractProseContent:
    """Tests for extract_prose_content() helper function."""

    def test_extract_prose_content_valid_file(self):
        """Test extract_prose_content returns content after blank line."""
        from sheep.features.feature_207_markdown_file_creation import extract_prose_content

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                prose = "This is the prose content."
                Path("test.md").write_text(f"# Title\n\n{prose}")

                result = extract_prose_content("test.md")
                assert prose in result, f"Expected '{prose}' in result"
            finally:
                os.chdir(original_cwd)


class TestCountSentences:
    """Tests for count_sentences() helper function."""

    def test_count_sentences_one_sentence(self):
        """Test count_sentences with one sentence."""
        from sheep.features.feature_207_markdown_file_creation import count_sentences

        prose = "This is one sentence."
        result = count_sentences(prose)
        assert result == 1, f"Expected 1 sentence, got {result}"

    def test_count_sentences_three_sentences(self):
        """Test count_sentences with three sentences."""
        from sheep.features.feature_207_markdown_file_creation import count_sentences

        prose = "This is first. This is second. This is third."
        result = count_sentences(prose)
        assert result == 3, f"Expected 3 sentences, got {result}"

    def test_count_sentences_two_sentences(self):
        """Test count_sentences with two sentences."""
        from sheep.features.feature_207_markdown_file_creation import count_sentences

        prose = "First sentence. Second sentence."
        result = count_sentences(prose)
        assert result == 2, f"Expected 2 sentences, got {result}"


class TestValidateSentenceCount:
    """Tests for validate_sentence_count() function."""

    def test_validate_sentence_count_two_sentences(self):
        """Test validate_sentence_count passes with 2 sentences."""
        from sheep.features.feature_207_markdown_file_creation import validate_sentence_count

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                Path("test.md").write_text("# Title\n\nFirst sentence. Second sentence.")

                # Should not raise
                validate_sentence_count("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_three_sentences(self):
        """Test validate_sentence_count passes with 3 sentences."""
        from sheep.features.feature_207_markdown_file_creation import validate_sentence_count

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                Path("test.md").write_text(
                    "# Title\n\nFirst sentence. Second sentence. Third sentence."
                )

                # Should not raise
                validate_sentence_count("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_one_sentence_fails(self):
        """Test validate_sentence_count fails with 1 sentence."""
        from sheep.features.feature_207_markdown_file_creation import validate_sentence_count

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                Path("test.md").write_text("# Title\n\nJust one sentence.")

                try:
                    validate_sentence_count("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "2" in str(e) or "3" in str(e)
            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_four_sentences_fails(self):
        """Test validate_sentence_count fails with 4 sentences."""
        from sheep.features.feature_207_markdown_file_creation import validate_sentence_count

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                Path("test.md").write_text(
                    "# Title\n\nFirst. Second. Third. Fourth."
                )

                try:
                    validate_sentence_count("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "2" in str(e) or "3" in str(e)
            finally:
                os.chdir(original_cwd)


class TestValidateEncoding:
    """Tests for validate_encoding() function."""

    def test_validate_encoding_valid_utf8(self):
        """Test validate_encoding passes on valid UTF-8 without BOM."""
        from sheep.features.feature_207_markdown_file_creation import validate_encoding

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                Path("test.md").write_text("# Title\n\nValid UTF-8 content.", encoding="utf-8")

                # Should not raise
                validate_encoding("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_encoding_with_bom_fails(self):
        """Test validate_encoding fails on file with UTF-8 BOM."""
        from sheep.features.feature_207_markdown_file_creation import validate_encoding

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file with UTF-8 BOM
                with open("test.md", "wb") as f:
                    f.write(b"\xef\xbb\xbf# Title\n\nContent.")

                try:
                    validate_encoding("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "BOM" in str(e)
            finally:
                os.chdir(original_cwd)

    def test_validate_encoding_invalid_utf8_fails(self):
        """Test validate_encoding fails on invalid UTF-8."""
        from sheep.features.feature_207_markdown_file_creation import validate_encoding

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file with invalid UTF-8 bytes
                with open("test.md", "wb") as f:
                    f.write(b"# Title\n\n\xff\xfe invalid")

                try:
                    validate_encoding("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "UTF-8" in str(e) or "encoding" in str(e).lower()
            finally:
                os.chdir(original_cwd)


class TestValidateLineEndings:
    """Tests for validate_line_endings() function."""

    def test_validate_line_endings_lf_only(self):
        """Test validate_line_endings passes with LF only."""
        from sheep.features.feature_207_markdown_file_creation import validate_line_endings

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                Path("test.md").write_text("# Title\n\nContent with LF.", encoding="utf-8")

                # Should not raise
                validate_line_endings("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_line_endings_crlf_fails(self):
        """Test validate_line_endings fails with CRLF."""
        from sheep.features.feature_207_markdown_file_creation import validate_line_endings

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file with CRLF
                with open("test.md", "wb") as f:
                    f.write(b"# Title\r\n\r\nContent.")

                try:
                    validate_line_endings("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "CRLF" in str(e) or "Windows" in str(e)
            finally:
                os.chdir(original_cwd)

    def test_validate_line_endings_cr_fails(self):
        """Test validate_line_endings fails with CR."""
        from sheep.features.feature_207_markdown_file_creation import validate_line_endings

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file with CR
                with open("test.md", "wb") as f:
                    f.write(b"# Title\r\r\rContent.")

                try:
                    validate_line_endings("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "CR" in str(e) or "Mac" in str(e)
            finally:
                os.chdir(original_cwd)


class TestValidateFileSize:
    """Tests for validate_file_size() function."""

    def test_validate_file_size_in_range(self):
        """Test validate_file_size passes when size is in range."""
        from sheep.features.feature_207_markdown_file_creation import validate_file_size

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file with appropriate content (~400-500 bytes)
                content = "# Title\n\n" + "x" * 400
                Path("test.md").write_text(content)

                # Should not raise (default range is 300-800)
                validate_file_size("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_too_small_fails(self):
        """Test validate_file_size fails when file too small."""
        from sheep.features.feature_207_markdown_file_creation import validate_file_size

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create small file (< 300 bytes)
                Path("test.md").write_text("# Title\n\nShort.")

                try:
                    validate_file_size("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "300" in str(e) or "small" in str(e).lower()
            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_too_large_fails(self):
        """Test validate_file_size fails when file too large."""
        from sheep.features.feature_207_markdown_file_creation import validate_file_size

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create large file (> 800 bytes)
                content = "# Title\n\n" + "x" * 900
                Path("test.md").write_text(content)

                try:
                    validate_file_size("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "800" in str(e) or "large" in str(e).lower()
            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_custom_range(self):
        """Test validate_file_size with custom min/max parameters."""
        from sheep.features.feature_207_markdown_file_creation import validate_file_size

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file of 50 bytes
                Path("test.md").write_text("x" * 50)

                # Should pass with min_bytes=40
                validate_file_size("test.md", min_bytes=40, max_bytes=100)

                # Should fail with min_bytes=60
                try:
                    validate_file_size("test.md", min_bytes=60, max_bytes=100)
                    assert False, "Should have raised ValueError"
                except ValueError:
                    pass  # Expected
            finally:
                os.chdir(original_cwd)


class TestValidateMarkdownFile:
    """Tests for validate_markdown_file() orchestrator function."""

    def test_validate_markdown_file_valid_file(self):
        """Test validate_markdown_file passes on valid file."""
        from sheep.features.feature_207_markdown_file_creation import validate_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create valid file with enough content (300-800 bytes) and exactly 2-3 sentences
                content = (
                    "# Title\n\n"
                    "This is the first sentence about an interesting topic that needs to be "
                    "long enough to meet the 300-800 byte requirement for the specification "
                    "and ensures we have meaningful content. "
                    "This is the second sentence that provides additional context and "
                    "information about the topic to round out the content requirements."
                )
                Path("test.md").write_text(content)

                # Should not raise
                validate_markdown_file("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_missing_file_fails(self):
        """Test validate_markdown_file fails on missing file."""
        from sheep.features.feature_207_markdown_file_creation import validate_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                try:
                    validate_markdown_file("nonexistent.md")
                    assert False, "Should have raised FileNotFoundError"
                except FileNotFoundError:
                    pass  # Expected
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_bad_format_fails(self):
        """Test validate_markdown_file fails on bad markdown format."""
        from sheep.features.feature_207_markdown_file_creation import validate_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file without H1 heading
                Path("test.md").write_text("No heading here. Just prose.")

                try:
                    validate_markdown_file("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError:
                    pass  # Expected
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_bad_sentence_count_fails(self):
        """Test validate_markdown_file fails on wrong sentence count."""
        from sheep.features.feature_207_markdown_file_creation import validate_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file with 1 sentence
                Path("test.md").write_text("# Title\n\nJust one.")

                try:
                    validate_markdown_file("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError:
                    pass  # Expected
            finally:
                os.chdir(original_cwd)
