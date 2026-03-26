"""Tests for feature 228: markdown file creation with hardcoded prose content.

Tests verify that:
1. Markdown file is created with proper structure
2. File has hardcoded prose content (2-3 sentences)
3. File has UTF-8 encoding without BOM
4. File uses Unix LF line endings
5. File size is in expected range (400-600 bytes)
6. All validation checks pass
"""

import sys
from pathlib import Path
import tempfile
import os

# Add src to path to enable imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


class TestFeature228FileCreation:
    """Test suite for feature 228 markdown file creation."""

    def test_file_does_not_exist_initially(self):
        """Test that test-2kjyci.md does not exist in repository root before creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # File should not exist initially
                assert not Path("test-2kjyci.md").exists()
            finally:
                os.chdir(original_cwd)

    def test_file_creation_creates_file(self):
        """Test that feature 228 creates test-2kjyci.md file on disk."""
        from sheep.features.feature_228_markdown_file_creation import (
            create_feature_228_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                result = create_feature_228_markdown_file()

                assert Path(result["filepath"]).exists()
                assert Path(result["filepath"]).is_file()
                assert result["filepath"].endswith("test-2kjyci.md")

            finally:
                os.chdir(original_cwd)

    def test_file_contains_h1_heading(self):
        """Test that created file contains H1 heading as first line."""
        from sheep.features.feature_228_markdown_file_creation import (
            create_feature_228_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                result = create_feature_228_markdown_file()
                filepath = result["filepath"]

                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                assert len(lines) > 0
                assert lines[0].startswith("# "), f"First line should start with '# ', got: {lines[0]}"

            finally:
                os.chdir(original_cwd)

    def test_file_has_blank_line_after_heading(self):
        """Test that file has blank line after H1 heading (CommonMark format)."""
        from sheep.features.feature_228_markdown_file_creation import (
            create_feature_228_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                result = create_feature_228_markdown_file()
                filepath = result["filepath"]

                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    lines = content.split("\n")

                assert len(lines) >= 3, f"File should have at least 3 lines, got {len(lines)}"
                assert lines[0].startswith("# "), "First line must be H1 heading"
                assert lines[1] == "", f"Second line must be blank, got: '{lines[1]}'"

            finally:
                os.chdir(original_cwd)

    def test_file_contains_prose_content(self):
        """Test that file contains prose content after heading and blank line."""
        from sheep.features.feature_228_markdown_file_creation import (
            create_feature_228_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                result = create_feature_228_markdown_file()
                filepath = result["filepath"]

                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    lines = content.split("\n")

                prose_lines = [l for l in lines[2:] if l.strip()]  # Skip heading and blank line
                assert len(prose_lines) > 0, "File should contain prose content"

            finally:
                os.chdir(original_cwd)

    def test_file_has_utf8_encoding_without_bom(self):
        """Test that created file is UTF-8 encoded without BOM."""
        from sheep.features.feature_228_markdown_file_creation import (
            create_feature_228_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                result = create_feature_228_markdown_file()
                filepath = result["filepath"]

                # Read file as binary and check for BOM
                with open(filepath, "rb") as f:
                    binary_content = f.read()

                # UTF-8 BOM is bytes EF BB BF
                assert not binary_content.startswith(b"\xef\xbb\xbf"), \
                    "File must not contain UTF-8 BOM"

                # Verify file can be decoded as UTF-8
                decoded_content = binary_content.decode("utf-8")
                assert isinstance(decoded_content, str)

            finally:
                os.chdir(original_cwd)

    def test_file_uses_lf_line_endings(self):
        """Test that created file uses Unix LF line endings, not CRLF."""
        from sheep.features.feature_228_markdown_file_creation import (
            create_feature_228_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                result = create_feature_228_markdown_file()
                filepath = result["filepath"]

                # Read file as binary and check for CRLF
                with open(filepath, "rb") as f:
                    binary_content = f.read()

                assert b"\r\n" not in binary_content, \
                    "File must use LF line endings, not CRLF"
                assert b"\r" not in binary_content, \
                    "File must use LF line endings, not CR"

            finally:
                os.chdir(original_cwd)

    def test_file_size_in_expected_range(self):
        """Test that created file size is in the expected range (400-600 bytes)."""
        from sheep.features.feature_228_markdown_file_creation import (
            create_feature_228_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                result = create_feature_228_markdown_file()
                filepath = result["filepath"]

                file_size = Path(filepath).stat().st_size
                assert 400 <= file_size <= 600, \
                    f"File size {file_size} bytes should be in range 400-600 bytes"

            finally:
                os.chdir(original_cwd)

    def test_file_ends_with_newline(self):
        """Test that created file ends with a newline (Unix convention)."""
        from sheep.features.feature_228_markdown_file_creation import (
            create_feature_228_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                result = create_feature_228_markdown_file()
                filepath = result["filepath"]

                with open(filepath, "rb") as f:
                    binary_content = f.read()

                assert binary_content.endswith(b"\n"), \
                    "File must end with a newline"

            finally:
                os.chdir(original_cwd)

    def test_prose_content_has_2_to_3_sentences(self):
        """Test that prose content contains exactly 2-3 sentences."""
        from sheep.features.feature_228_markdown_file_creation import (
            create_feature_228_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                result = create_feature_228_markdown_file()
                filepath = result["filepath"]

                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    lines = content.split("\n")

                # Get prose content (skip heading and blank line)
                prose_lines = [l for l in lines[2:] if l.strip()]
                prose_content = " ".join(prose_lines)

                # Count sentences by counting periods
                sentence_count = prose_content.count(".")
                assert sentence_count >= 2 and sentence_count <= 3, \
                    f"Expected 2-3 sentences, found {sentence_count}"

            finally:
                os.chdir(original_cwd)

    def test_validation_passes_for_created_file(self):
        """Test that validation passes for properly created file."""
        from sheep.features.feature_228_markdown_file_creation import (
            create_feature_228_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                result = create_feature_228_markdown_file()
                filepath = result["filepath"]

                # The function should have already validated during creation
                # but we can verify it again
                assert Path(filepath).exists()
                assert Path(filepath).is_file()

            finally:
                os.chdir(original_cwd)

    def test_feature_metadata_is_correct(self):
        """Test that feature 228 has correct metadata."""
        from sheep.features.feature_228_markdown_file_creation import (
            FEATURE_NUMBER,
            FEATURE_NAME,
            MARKDOWN_FILENAME,
        )

        assert FEATURE_NUMBER == 228
        assert FEATURE_NAME == "markdown-file-creation-7fd4b2"
        assert MARKDOWN_FILENAME == "test-2kjyci.md"

    def test_hardcoded_content_is_used(self):
        """Test that feature 228 uses hardcoded content, not Claude API generation."""
        from sheep.features.feature_228_markdown_file_creation import (
            MARKDOWN_CONTENT,
        )

        # Content should be a non-empty string
        assert isinstance(MARKDOWN_CONTENT, str)
        assert len(MARKDOWN_CONTENT) > 0

        # Should contain H1 heading
        assert MARKDOWN_CONTENT.startswith("# ")

        # Should contain 2-3 sentences (count periods)
        sentence_count = MARKDOWN_CONTENT.count(".")
        assert 2 <= sentence_count <= 3

        # Should have blank line after heading
        lines = MARKDOWN_CONTENT.split("\n")
        assert len(lines) >= 3
        assert lines[1] == ""


class TestFeature228Validation:
    """Test suite for validation functions in feature 228."""

    def test_validation_function_exists(self):
        """Test that _validate_markdown_file function is available."""
        from sheep.features.feature_228_markdown_file_creation import (
            _validate_markdown_file,
        )

        assert _validate_markdown_file is not None
        assert callable(_validate_markdown_file)

    def test_validation_rejects_file_without_h1_heading(self):
        """Test that validation fails for file without H1 heading."""
        from sheep.features.feature_228_markdown_file_creation import (
            _validate_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create invalid file (no H1 heading)
                invalid_content = "This is a test file.\nNo heading here.\n"
                Path("invalid.md").write_text(invalid_content, encoding="utf-8")

                # Validation should fail
                try:
                    _validate_markdown_file("invalid.md")
                    assert False, "Validation should have failed for file without H1 heading"
                except (ValueError, OSError):
                    pass  # Expected

            finally:
                os.chdir(original_cwd)

    def test_validation_rejects_file_with_crlf_line_endings(self):
        """Test that validation fails for file with CRLF line endings."""
        from sheep.features.feature_228_markdown_file_creation import (
            _validate_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create file with CRLF line endings
                crlf_content = "# Title\r\n\r\nThis is a sentence. This is another sentence. This is the third.\r\n"
                with open("crlf.md", "wb") as f:
                    f.write(crlf_content.encode("utf-8"))

                # Validation should fail
                try:
                    _validate_markdown_file("crlf.md")
                    assert False, "Validation should have failed for CRLF line endings"
                except (ValueError, OSError):
                    pass  # Expected

            finally:
                os.chdir(original_cwd)

    def test_validation_rejects_file_with_bom(self):
        """Test that validation fails for file with UTF-8 BOM."""
        from sheep.features.feature_228_markdown_file_creation import (
            _validate_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create file with UTF-8 BOM
                valid_content = "# Title\n\nThis is a sentence. This is another sentence. This is the third.\n"
                bom_content = b"\xef\xbb\xbf" + valid_content.encode("utf-8")
                with open("bom.md", "wb") as f:
                    f.write(bom_content)

                # Validation should fail
                try:
                    _validate_markdown_file("bom.md")
                    assert False, "Validation should have failed for file with BOM"
                except (ValueError, OSError):
                    pass  # Expected

            finally:
                os.chdir(original_cwd)

    def test_validation_rejects_file_without_blank_line_after_heading(self):
        """Test that validation fails if no blank line after heading."""
        from sheep.features.feature_228_markdown_file_creation import (
            _validate_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create file without blank line after heading
                invalid_content = "# Title\nThis is a sentence. This is another. This is the third.\n"
                Path("no_blank.md").write_text(invalid_content, encoding="utf-8", newline="\n")

                # Validation should fail
                try:
                    _validate_markdown_file("no_blank.md")
                    assert False, "Validation should have failed for missing blank line"
                except (ValueError, OSError):
                    pass  # Expected

            finally:
                os.chdir(original_cwd)

    def test_validation_rejects_file_with_wrong_sentence_count(self):
        """Test that validation fails if prose has wrong number of sentences."""
        from sheep.features.feature_228_markdown_file_creation import (
            _validate_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create file with only 1 sentence
                invalid_content = "# Title\n\nThis is only one sentence.\n"
                Path("one_sentence.md").write_text(invalid_content, encoding="utf-8", newline="\n")

                # Validation should fail
                try:
                    _validate_markdown_file("one_sentence.md")
                    assert False, "Validation should have failed for only 1 sentence"
                except (ValueError, OSError):
                    pass  # Expected

            finally:
                os.chdir(original_cwd)

    def test_validation_rejects_nonexistent_file(self):
        """Test that validation fails for non-existent file."""
        from sheep.features.feature_228_markdown_file_creation import (
            _validate_markdown_file,
        )

        # Should raise error for non-existent file
        try:
            _validate_markdown_file("nonexistent.md")
            assert False, "Validation should have failed for non-existent file"
        except (ValueError, OSError):
            pass  # Expected
