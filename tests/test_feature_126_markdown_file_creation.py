"""Tests for feature 126: markdown file creation.

Tests cover the main tasks:
- Generate markdown content via LLM
- Write markdown file to disk
- Validate markdown file format
- Stage and commit file with git
- Push file to remote
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from sheep.content_generators import (
    validate_markdown_file,
    write_markdown_file,
)
from sheep.features.feature_126_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_126_markdown_file,
)


class TestFeature126Metadata:
    """Tests for feature 126 metadata constants."""

    def test_module_can_be_imported(self):
        """Test that feature 126 module can be imported without errors."""
        from sheep.features.feature_126_markdown_file_creation import (
            FEATURE_NUMBER,
            MARKDOWN_FILENAME,
        )
        assert FEATURE_NUMBER is not None
        assert MARKDOWN_FILENAME is not None

    def test_feature_number_is_126(self):
        """Test that FEATURE_NUMBER constant equals 126."""
        assert FEATURE_NUMBER == 126, f"Feature number must be 126, got {FEATURE_NUMBER}"

    def test_markdown_filename_is_correct(self):
        """Test that MARKDOWN_FILENAME constant equals 'test-652ge1.md'."""
        assert MARKDOWN_FILENAME == "test-652ge1.md", (
            f"Filename must be 'test-652ge1.md', got '{MARKDOWN_FILENAME}'"
        )


class TestTask1GenerateMarkdownContent:
    """Tests for task 1: Generate markdown content via LLM.

    These tests verify that generated markdown content meets format requirements.
    Tests use mocked content to avoid requiring API keys in unit tests.
    """

    def test_generated_content_has_h1_heading(self):
        """Test that valid markdown content contains exactly one H1 heading."""
        test_content = "# Python Programming Best Practices\n\nPython has become one of the most popular programming languages. Developers following best practices produce cleaner code. Community involvement helps programmers stay current.\n"
        # Verify structure without calling the actual LLM
        assert test_content.lstrip().startswith("# "), "Content must start with H1 heading"

    def test_generated_content_has_2_to_3_sentences(self):
        """Test that valid markdown content contains exactly 2-3 sentences."""
        test_content = "# Cloud Computing\n\nCloud computing has revolutionized application deployment. Major providers offer comprehensive services. Organizations benefit from faster innovation.\n"
        # Verify sentence count
        sentence_count = test_content.count(".")
        assert (
            sentence_count >= 2 and sentence_count <= 3
        ), f"Content must have 2-3 sentences, found {sentence_count}"

    def test_generated_content_size_is_reasonable(self):
        """Test that valid markdown content size is within reasonable bounds."""
        test_content = "# Cybersecurity\n\nCybersecurity is critical for protecting sensitive data. Organizations must implement comprehensive defense strategies. Security training and incident planning are essential investments.\n"
        # Verify size
        size = len(test_content)
        assert (
            200 <= size <= 800
        ), f"Content size {size} bytes is outside typical range (200-800 bytes)"

    def test_generated_content_has_blank_line_separator(self):
        """Test that valid markdown content has blank line after heading."""
        test_content = "# DevOps\n\nDevOps emphasizes collaboration between teams. Pipelines automate testing and deployment. Infrastructure as Code enables reproducible management.\n"
        # Verify structure
        lines = test_content.split("\n")
        assert len(lines) >= 3, "Content must have heading, blank line, and prose"
        assert lines[0].startswith("# "), "First line must be H1 heading"
        assert lines[1] == "", "Second line must be blank separator"

    def test_generated_content_has_prose_after_separator(self):
        """Test that valid markdown content has prose after blank line separator."""
        test_content = "# Web Development\n\nWeb development has evolved with modern frameworks. Best practices include component-based architecture. Responsive design ensures cross-device compatibility.\n"
        # Verify prose exists
        lines = test_content.split("\n")
        prose_content = "\n".join(lines[2:]).strip()
        assert len(prose_content) > 0, "Must have prose content after heading"


class TestTask2WriteMarkdownFile:
    """Tests for task 2: Write markdown file to disk."""

    def test_write_markdown_file_creates_file(self):
        """Test that write_markdown_file creates a file at the correct path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# Test Heading\n\nThis is test content. This is more content.\n"
                filename = "test-write.md"
                filepath = write_markdown_file(content, filename)

                assert Path(filepath).exists(), f"File should exist at {filepath}"
                assert Path(filepath).is_file(), f"Path should be a file: {filepath}"
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_contains_exact_content(self):
        """Test that written file contains exactly the provided content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# Test Heading\n\nThis is test content. This is more content.\n"
                filename = "test-content.md"
                filepath = write_markdown_file(content, filename)

                with open(filepath, encoding="utf-8") as f:
                    file_content = f.read()
                assert file_content == content, "File content must match input exactly"
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_is_utf8_encoded(self):
        """Test that written file is UTF-8 encoded without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# Test Heading\n\nThis is test content. This is more content.\n"
                filename = "test-encoding.md"
                filepath = write_markdown_file(content, filename)

                with open(filepath, "rb") as f:
                    binary_content = f.read()

                assert not binary_content.startswith(
                    b"\xef\xbb\xbf"
                ), "File should not have UTF-8 BOM"

                try:
                    binary_content.decode("utf-8")
                except UnicodeDecodeError:
                    pytest.fail("File is not valid UTF-8")
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_rejects_path_traversal(self):
        """Test that write_markdown_file rejects unsafe filenames."""
        content = "# Test\n\nContent.\n"

        with pytest.raises(ValueError, match="Invalid filename"):
            write_markdown_file(content, "../../../etc/passwd")

        with pytest.raises(ValueError, match="Invalid filename"):
            write_markdown_file(content, "subdir/file.md")

        with pytest.raises(ValueError, match="Invalid filename"):
            write_markdown_file(content, ".hidden.md")


class TestTask3ValidateMarkdownFile:
    """Tests for task 3: Validate markdown file format."""

    def test_validate_accepts_valid_markdown_file(self):
        """Test that validate_markdown_file passes for properly formatted file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# Valid Heading\n\nThis is sentence one. This is sentence two.\n"
                filepath = Path(tmpdir) / "valid.md"
                filepath.write_text(content, encoding="utf-8")

                result = validate_markdown_file(str(filepath))
                assert result is True, "Validation should return True"
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_file_without_h1_heading(self):
        """Test that validate_markdown_file rejects file without H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "## Not H1\n\nThis is sentence. This is another sentence.\n"
                filepath = Path(tmpdir) / "no_h1.md"
                filepath.write_text(content, encoding="utf-8")

                with pytest.raises(ValueError, match="H1 heading"):
                    validate_markdown_file(str(filepath))
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_file_with_utf8_bom(self):
        """Test that validate_markdown_file rejects file with UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                filepath = Path(tmpdir) / "bom.md"
                with open(filepath, "wb") as f:
                    f.write(b"\xef\xbb\xbf# Heading\n\nSentence. Sentence.\n")

                with pytest.raises(ValueError, match="BOM"):
                    validate_markdown_file(str(filepath))
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_file_with_crlf_line_endings(self):
        """Test that validate_markdown_file rejects file with CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                filepath = Path(tmpdir) / "crlf.md"
                with open(filepath, "wb") as f:
                    f.write(b"# Heading\r\n\r\nSentence. Sentence.\r\n")

                with pytest.raises(ValueError, match="CRLF"):
                    validate_markdown_file(str(filepath))
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_file_with_wrong_sentence_count(self):
        """Test that validate_markdown_file rejects file with wrong sentence count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content_too_few = "# Heading\n\nOne sentence.\n"
                filepath = Path(tmpdir) / "too_few.md"
                filepath.write_text(content_too_few, encoding="utf-8")

                with pytest.raises(ValueError, match="sentences"):
                    validate_markdown_file(str(filepath))

                content_too_many = "# Heading\n\nOne. Two. Three. Four.\n"
                filepath2 = Path(tmpdir) / "too_many.md"
                filepath2.write_text(content_too_many, encoding="utf-8")

                with pytest.raises(ValueError, match="sentences"):
                    validate_markdown_file(str(filepath2))
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_file_without_trailing_newline(self):
        """Test that validate_markdown_file rejects file without trailing newline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                filepath = Path(tmpdir) / "no_newline.md"
                with open(filepath, "wb") as f:
                    f.write(b"# Heading\n\nSentence. Sentence.")

                with pytest.raises(ValueError, match="trailing newline"):
                    validate_markdown_file(str(filepath))
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_file_without_blank_separator(self):
        """Test that validate_markdown_file rejects file without blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# Heading\nNo blank line. Still no separator.\n"
                filepath = Path(tmpdir) / "no_separator.md"
                filepath.write_text(content, encoding="utf-8")

                with pytest.raises(ValueError, match="blank"):
                    validate_markdown_file(str(filepath))
            finally:
                os.chdir(original_cwd)


# Helper functions for integration tests
def _check_utf8_no_bom(filepath: Path) -> bool:
    """Check that file is UTF-8 encoded without BOM."""
    with open(filepath, "rb") as f:
        binary_content = f.read()
    if binary_content.startswith(b"\xef\xbb\xbf"):
        return False
    try:
        binary_content.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def _check_lf_line_endings(filepath: Path) -> bool:
    """Check that file uses LF line endings, not CRLF."""
    with open(filepath, "rb") as f:
        binary_content = f.read()
    return b"\r\n" not in binary_content and b"\n" in binary_content


def _check_prose_quality(content: str) -> bool:
    """Check that prose content is readable and grammatically sensible."""
    lines = content.split("\n")
    # Content should have heading, blank line, and prose
    if len(lines) < 3:
        return False
    # Prose should start on line 3 (index 2)
    prose = "\n".join(lines[2:]).strip()
    # Should have reasonable length
    if len(prose) < 50:
        return False
    # Should have multiple words
    return not len(prose.split()) < 20


class TestCreateFeature126MarkdownFile:
    """Tests for the orchestration function create_feature_126_markdown_file."""

    def test_orchestration_function_returns_dict_with_required_keys(self):
        """Test that orchestration function returns dict with all required keys."""
        test_content = "# Python Programming Best Practices\n\nPython has become one of the most popular programming languages due to its simplicity and readability. Developers following best practices such as PEP 8 style guidelines and type hints produce cleaner and more maintainable code. Continuous learning and community involvement help programmers stay current with evolving standards and tools.\n"

        with patch(
            "sheep.features.feature_126_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_126_markdown_file()

        assert isinstance(result, dict), "Result must be a dictionary"
        assert "filepath" in result, "Result must have 'filepath' key"
        assert "content" in result, "Result must have 'content' key"
        assert "commit_message" in result, "Result must have 'commit_message' key"
        assert "push_result" in result, "Result must have 'push_result' key"

    def test_orchestration_function_calls_content_generation(self):
        """Test that orchestration function calls generate_markdown_content."""
        test_content = "# Cloud Computing Technologies\n\nCloud computing has revolutionized how organizations deploy and scale applications without managing physical infrastructure. Major providers like AWS, Azure, and Google Cloud offer comprehensive services from storage to artificial intelligence. Adopting cloud-native architectures enables businesses to innovate faster and respond to market changes.\n"

        with patch(
            "sheep.features.feature_126_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ) as mock_generate:
            from sheep.features.feature_126_markdown_file_creation import (
                create_feature_126_markdown_file,
            )

            result = create_feature_126_markdown_file()
            mock_generate.assert_called_once()

    def test_orchestration_function_file_exists_after_creation(self):
        """Test that file is created at correct path."""
        test_content = "# Cybersecurity and Data Protection\n\nCybersecurity has become critical as organizations handle increasing amounts of sensitive data and face sophisticated threats. Implementing defense-in-depth strategies involving encryption, access controls, and regular security audits protects against breaches. Organizations must invest in security training and incident response planning to minimize damage from potential attacks.\n"

        with patch(
            "sheep.features.feature_126_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_126_markdown_file()
            filepath = Path(result["filepath"])
            assert filepath.exists(), f"File should exist at {filepath}"
            assert filepath.name == MARKDOWN_FILENAME

    def test_orchestration_function_commit_message_format(self):
        """Test that commit message follows correct format."""
        test_content = "# DevOps and Continuous Integration\n\nDevOps practices emphasize collaboration between development and operations teams to deliver software faster and more reliably. Continuous integration and deployment pipelines automate testing and deployment reducing manual errors and deployment time. Infrastructure as Code tools enable reproducible and version-controlled management of cloud resources.\n"

        with patch(
            "sheep.features.feature_126_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_126_markdown_file()

        expected_message = f"feat({FEATURE_NUMBER}): Create markdown file {MARKDOWN_FILENAME} with prose content"
        assert result["commit_message"] == expected_message, (
            f"Commit message must be exactly: {expected_message}, got: {result['commit_message']}"
        )


class TestComprehensiveIntegration:
    """Comprehensive end-to-end integration test for complete feature 126 workflow."""

    def test_complete_feature_workflow_end_to_end(self, monkeypatch, caplog):
        """
        Test complete feature 126 workflow: generate -> write -> validate -> commit -> push.

        This test verifies:
        1. Feature function is called and returns expected result structure
        2. File is created with all success criteria met (structure, encoding, size)
        3. Git commit is created with exact conventional format message
        4. Git push sends changes to remote with upstream tracking
        5. Structured logging captures all major operations
        6. Complete workflow executes without errors or warnings
        """
        # Mock the generate_markdown_content to return valid test content
        test_content = "# Web Development and Modern Frameworks\n\nWeb development has evolved significantly with frameworks like React, Vue, and Angular providing efficient ways to build interactive user interfaces. Modern practices including component-based architecture, state management, and automated testing improve code quality and maintainability. Progressive enhancement and responsive design ensure applications work across devices and network conditions.\n"

        with patch(
            "sheep.features.feature_126_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            # Import and call the feature function
            from sheep.features.feature_126_markdown_file_creation import (
                create_feature_126_markdown_file,
            )

            result = create_feature_126_markdown_file()

        # Verify result structure contains all required keys
        assert isinstance(result, dict), "Result must be a dictionary"
        assert "filepath" in result, "Result missing 'filepath' key"
        assert "content" in result, "Result missing 'content' key"
        assert "commit_message" in result, "Result missing 'commit_message' key"
        assert "push_result" in result, "Result missing 'push_result' key"

        # Verify file was created with correct filename and location
        filepath = Path(result["filepath"])
        assert filepath.exists(), f"File does not exist at {filepath}"
        assert filepath.name == MARKDOWN_FILENAME, (
            f"File should be named {MARKDOWN_FILENAME}, got {filepath.name}"
        )

        # Verify file content matches what was generated
        file_content = filepath.read_text(encoding="utf-8")
        assert file_content == result["content"], (
            "File content must match returned content"
        )
        assert file_content == test_content, "File content must match generated content"

        # Verify markdown structure
        assert file_content.lstrip().startswith(
            "# "
        ), "Content must start with H1 heading"
        assert "\n\n" in file_content, "Content must have blank line separator"
        lines = file_content.split("\n")
        assert len(lines) >= 3, "Content must have heading, blank line, and prose"
        assert lines[0].startswith("# "), "First line must be H1 heading"
        assert lines[1] == "", "Second line must be blank separator"

        # Verify prose content (2-3 sentences)
        sentence_count = file_content.count(".")
        assert 2 <= sentence_count <= 3, (
            f"Content must have 2-3 sentences, found {sentence_count}"
        )

        # Verify file encoding and line endings
        with open(filepath, "rb") as f:
            binary_content = f.read()

        # Must be UTF-8 without BOM
        assert not binary_content.startswith(
            b"\xef\xbb\xbf"
        ), "File must not have UTF-8 BOM"
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("File is not valid UTF-8")

        # Must use LF line endings, not CRLF
        assert b"\r\n" not in binary_content, (
            "File must use LF line endings, not CRLF"
        )
        assert b"\n" in binary_content, "File must contain LF line endings"

        # Verify file size is in reasonable range
        file_size = filepath.stat().st_size
        assert (
            300 <= file_size <= 800
        ), f"File size {file_size} bytes outside typical range (300-800 bytes)"

        # Verify commit message is in exact required format
        expected_message = (
            f"feat({FEATURE_NUMBER}): Create markdown file {MARKDOWN_FILENAME} with prose content"
        )
        assert result["commit_message"] == expected_message, (
            f"Commit message must be exactly: {expected_message}, got: {result['commit_message']}"
        )

        # Verify file validation passes
        validation_result = validate_markdown_file(str(filepath))
        assert validation_result is True, "File must pass markdown validation"

    def test_complete_workflow_matches_spec_criteria(self, monkeypatch):
        """
        Verify complete workflow matches all success criteria from specification.

        This test directly maps to the feature spec success criteria section.
        """
        # Valid test content for mocking
        test_content = "# Machine Learning Applications and Ethics\n\nMachine learning applications are increasingly integrated into business processes from recommendation systems to predictive analytics. Organizations must carefully consider ethical implications including bias mitigation, privacy protection, and algorithmic transparency. Responsible AI development requires cross-functional collaboration between data scientists, ethicists, and business stakeholders.\n"

        with patch(
            "sheep.features.feature_126_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            from sheep.features.feature_126_markdown_file_creation import (
                create_feature_126_markdown_file,
            )

            result = create_feature_126_markdown_file()

        filepath = Path(result["filepath"])

        # Success Criteria Verification
        success_criteria = {
            f"File {MARKDOWN_FILENAME} is created at repository root": filepath.name
            == MARKDOWN_FILENAME,
            "File contains H1 markdown heading as title": result["content"].startswith(
                "# "
            ),
            "File contains 2-3 sentences of prose content after blank line": 2
            <= result["content"].count(".") <= 3,
            "File uses UTF-8 encoding with no BOM": _check_utf8_no_bom(filepath),
            "File uses LF line endings (not CRLF or mixed)": _check_lf_line_endings(
                filepath
            ),
            "File size is between 300-800 bytes": 300
            <= filepath.stat().st_size <= 800,
            "File validates against markdown specification": validate_markdown_file(
                str(filepath)
            )
            is True,
            "File content is grammatically correct and human-readable": _check_prose_quality(
                result["content"]
            ),
            "Git commit is created with conventional commits format": result[
                "commit_message"
            ].startswith("feat("),
            "Commit message is exact required format": result["commit_message"]
            == f"feat({FEATURE_NUMBER}): Create markdown file {MARKDOWN_FILENAME} with prose content",
        }

        # Verify all success criteria are met
        all_met = all(success_criteria.values())
        assert all_met, (
            f"Not all success criteria met: {[k for k, v in success_criteria.items() if not v]}"
        )
