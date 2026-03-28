"""Tests for feature 227 comprehensive verification functions.

Tests verify that all verification functions correctly validate:
1. File existence and location
2. Markdown structure (heading, blank line, prose)
3. File encoding (UTF-8 without BOM)
4. Line endings (Unix LF)
5. File size and content
6. Git trackability
7. Comprehensive verification harness
"""

import os
import sys
import tempfile
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Sample markdown content for testing
VALID_MARKDOWN = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible.\n"


def test_verify_file_exists_passes_for_valid_file():
    """Test that verify_file_exists passes when file exists and is readable."""
    from sheep.features.feature_227_verification import verify_file_exists

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            # Create a test file
            filepath = Path("test-file.md")
            filepath.write_text(VALID_MARKDOWN)

            # Should not raise
            result = verify_file_exists(str(filepath))
            assert result is True

        finally:
            os.chdir(original_cwd)


def test_verify_file_exists_fails_for_missing_file():
    """Test that verify_file_exists raises VerificationError for missing file."""
    from sheep.features.feature_227_verification import (
        VerificationError,
        verify_file_exists,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "nonexistent.md")

        try:
            verify_file_exists(filepath)
            assert False, "Should have raised VerificationError"
        except VerificationError as e:
            assert "does not exist" in str(e).lower()


def test_verify_file_in_repository_root_passes():
    """Test that verify_file_in_repository_root passes for file in repo root."""
    from sheep.features.feature_227_verification import verify_file_in_repository_root

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            # Create file in temp directory (acting as repo root)
            filepath = Path("test-arvwkm.md")
            filepath.write_text(VALID_MARKDOWN)

            result = verify_file_in_repository_root(str(filepath))
            assert result is True

        finally:
            os.chdir(original_cwd)


def test_verify_file_in_repository_root_fails_for_wrong_name():
    """Test that verify_file_in_repository_root fails for wrong filename."""
    from sheep.features.feature_227_verification import (
        VerificationError,
        verify_file_in_repository_root,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("wrong-name.md")
            filepath.write_text(VALID_MARKDOWN)

            try:
                verify_file_in_repository_root(str(filepath))
                assert False, "Should have raised VerificationError"
            except VerificationError as e:
                assert "test-arvwkm.md" in str(e)

        finally:
            os.chdir(original_cwd)


def test_verify_heading_format_passes():
    """Test that verify_heading_format passes for valid H1 heading."""
    from sheep.features.feature_227_verification import verify_heading_format

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-file.md")
            filepath.write_text(VALID_MARKDOWN)

            result = verify_heading_format(str(filepath))
            assert result is True

        finally:
            os.chdir(original_cwd)


def test_verify_heading_format_fails_for_missing_heading():
    """Test that verify_heading_format fails without H1 heading."""
    from sheep.features.feature_227_verification import (
        VerificationError,
        verify_heading_format,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-file.md")
            filepath.write_text("No heading here\n\nJust prose.")

            try:
                verify_heading_format(str(filepath))
                assert False, "Should have raised VerificationError"
            except VerificationError as e:
                assert "must start with" in str(e).lower()

        finally:
            os.chdir(original_cwd)


def test_verify_blank_line_separator_passes():
    """Test that verify_blank_line_separator passes for blank line after heading."""
    from sheep.features.feature_227_verification import verify_blank_line_separator

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-file.md")
            filepath.write_text(VALID_MARKDOWN)

            result = verify_blank_line_separator(str(filepath))
            assert result is True

        finally:
            os.chdir(original_cwd)


def test_verify_blank_line_separator_fails_without_blank_line():
    """Test that verify_blank_line_separator fails without blank line."""
    from sheep.features.feature_227_verification import (
        VerificationError,
        verify_blank_line_separator,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-file.md")
            content = "# Heading\nContent without blank line.\n"
            filepath.write_text(content)

            try:
                verify_blank_line_separator(str(filepath))
                assert False, "Should have raised VerificationError"
            except VerificationError as e:
                assert "blank" in str(e).lower()

        finally:
            os.chdir(original_cwd)


def test_verify_prose_structure_passes():
    """Test that verify_prose_structure passes for valid prose."""
    from sheep.features.feature_227_verification import verify_prose_structure

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-file.md")
            filepath.write_text(VALID_MARKDOWN)

            result = verify_prose_structure(str(filepath))
            assert result is True

        finally:
            os.chdir(original_cwd)


def test_verify_prose_structure_fails_with_wrong_sentence_count():
    """Test that verify_prose_structure fails with incorrect sentence count."""
    from sheep.features.feature_227_verification import (
        VerificationError,
        verify_prose_structure,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-file.md")
            # Only 1 sentence
            content = "# Heading\n\nOne sentence.\n"
            filepath.write_text(content)

            try:
                verify_prose_structure(str(filepath))
                assert False, "Should have raised VerificationError"
            except VerificationError as e:
                assert "sentences" in str(e).lower()

        finally:
            os.chdir(original_cwd)


def test_verify_utf8_encoding_without_bom_passes():
    """Test that verify_utf8_encoding_without_bom passes for UTF-8 without BOM."""
    from sheep.features.feature_227_verification import verify_utf8_encoding_without_bom

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-file.md")
            filepath.write_text(VALID_MARKDOWN, encoding="utf-8")

            result = verify_utf8_encoding_without_bom(str(filepath))
            assert result is True

        finally:
            os.chdir(original_cwd)


def test_verify_utf8_encoding_without_bom_fails_with_bom():
    """Test that verify_utf8_encoding_without_bom fails with BOM."""
    from sheep.features.feature_227_verification import (
        VerificationError,
        verify_utf8_encoding_without_bom,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-file.md")
            # Write with UTF-8 BOM
            with open(filepath, "wb") as f:
                f.write(b"\xef\xbb\xbf" + VALID_MARKDOWN.encode("utf-8"))

            try:
                verify_utf8_encoding_without_bom(str(filepath))
                assert False, "Should have raised VerificationError"
            except VerificationError as e:
                assert "bom" in str(e).lower()

        finally:
            os.chdir(original_cwd)


def test_verify_lf_line_endings_passes():
    """Test that verify_lf_line_endings passes for LF line endings."""
    from sheep.features.feature_227_verification import verify_lf_line_endings

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-file.md")
            filepath.write_text(VALID_MARKDOWN)  # Uses LF by default on Unix

            result = verify_lf_line_endings(str(filepath))
            assert result is True

        finally:
            os.chdir(original_cwd)


def test_verify_lf_line_endings_fails_with_crlf():
    """Test that verify_lf_line_endings fails with CRLF line endings."""
    from sheep.features.feature_227_verification import (
        VerificationError,
        verify_lf_line_endings,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-file.md")
            # Write with CRLF
            with open(filepath, "wb") as f:
                content = VALID_MARKDOWN.replace("\n", "\r\n")
                f.write(content.encode("utf-8"))

            try:
                verify_lf_line_endings(str(filepath))
                assert False, "Should have raised VerificationError"
            except VerificationError as e:
                assert "crlf" in str(e).lower() or "line endings" in str(e).lower()

        finally:
            os.chdir(original_cwd)


def test_verify_file_size_passes():
    """Test that verify_file_size passes for file in expected size range."""
    from sheep.features.feature_227_verification import verify_file_size

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-file.md")
            filepath.write_text(VALID_MARKDOWN)

            result = verify_file_size(str(filepath))
            assert result is True

        finally:
            os.chdir(original_cwd)


def test_verify_file_size_fails_for_too_small_file():
    """Test that verify_file_size fails for file that is too small."""
    from sheep.features.feature_227_verification import (
        VerificationError,
        verify_file_size,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-file.md")
            filepath.write_text("# H\n\nSmall.\n")  # Too small

            try:
                verify_file_size(str(filepath))
                assert False, "Should have raised VerificationError"
            except VerificationError as e:
                assert "size" in str(e).lower()

        finally:
            os.chdir(original_cwd)


def test_verify_trailing_newline_passes():
    """Test that verify_trailing_newline passes when file ends with newline."""
    from sheep.features.feature_227_verification import verify_trailing_newline

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-file.md")
            filepath.write_text(VALID_MARKDOWN)  # Ends with newline

            result = verify_trailing_newline(str(filepath))
            assert result is True

        finally:
            os.chdir(original_cwd)


def test_verify_trailing_newline_fails_without_newline():
    """Test that verify_trailing_newline fails without trailing newline."""
    from sheep.features.feature_227_verification import (
        VerificationError,
        verify_trailing_newline,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-file.md")
            # Write without trailing newline
            with open(filepath, "wb") as f:
                f.write(VALID_MARKDOWN.rstrip("\n").encode("utf-8"))

            try:
                verify_trailing_newline(str(filepath))
                assert False, "Should have raised VerificationError"
            except VerificationError as e:
                assert "newline" in str(e).lower()

        finally:
            os.chdir(original_cwd)


def test_verify_markdown_syntax_passes():
    """Test that verify_markdown_syntax passes for valid markdown."""
    from sheep.features.feature_227_verification import verify_markdown_syntax

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-file.md")
            filepath.write_text(VALID_MARKDOWN)

            result = verify_markdown_syntax(str(filepath))
            assert result is True

        finally:
            os.chdir(original_cwd)


def test_verify_all_requirements_passes_for_valid_file():
    """Test that verify_all_requirements passes when all checks pass."""
    from sheep.features.feature_227_verification import verify_all_requirements

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("test-arvwkm.md")
            filepath.write_text(VALID_MARKDOWN)

            result = verify_all_requirements(str(filepath))

            assert result["all_pass"] is True
            assert len(result["passed"]) > 0
            assert len(result["failed"]) == 0
            assert result["total"] > 0

        finally:
            os.chdir(original_cwd)


def test_verify_all_requirements_reports_failures():
    """Test that verify_all_requirements reports failures correctly."""
    from sheep.features.feature_227_verification import verify_all_requirements

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)

            filepath = Path("invalid-file.md")
            # Create invalid file (no heading)
            filepath.write_text("Not a heading.\n\nJust content.\n")

            result = verify_all_requirements(str(filepath))

            assert result["all_pass"] is False
            assert len(result["failed"]) > 0
            assert "summary" in result

        finally:
            os.chdir(original_cwd)
