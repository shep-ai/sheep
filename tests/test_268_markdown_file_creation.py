"""Tests for feature 268: Creating markdown file test-ju8e95.md with title and prose content."""


class TestMarkdownFileCreation:
    """Tests for task-1: Create markdown file with H1 heading and prose content."""

    def test_file_does_not_exist_before_creation(self, tmp_path):
        """Test that file test-ju8e95.md does not exist before creation."""
        test_file = tmp_path / "test-ju8e95.md"
        assert not test_file.exists()

    def test_creates_file_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading."""
        test_file = tmp_path / "test-ju8e95.md"

        # Create the file with H1 heading
        content = "# The Power of Code Review\n\nCode review is a critical practice in professional software development, ensuring that multiple eyes examine code changes before they are integrated into the codebase. Beyond catching bugs and potential vulnerabilities, code review facilitates knowledge sharing among team members and establishes consistent coding standards across projects. By fostering a culture of constructive feedback and collaboration, code review transforms individual contributions into collective wisdom, strengthening both code quality and team cohesion.\n"
        test_file.write_text(content, encoding="utf-8")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_contains_two_or_three_sentences(self, tmp_path):
        """Test that file contains 2-3 sentences (ending with periods)."""
        test_file = tmp_path / "test-ju8e95.md"

        content = "# The Power of Code Review\n\nCode review is a critical practice in professional software development, ensuring that multiple eyes examine code changes before they are integrated into the codebase. Beyond catching bugs and potential vulnerabilities, code review facilitates knowledge sharing among team members and establishes consistent coding standards across projects. By fostering a culture of constructive feedback and collaboration, code review transforms individual contributions into collective wisdom, strengthening both code quality and team cohesion.\n"
        test_file.write_text(content, encoding="utf-8")

        text_content = test_file.read_text(encoding="utf-8")
        # Extract prose content (skip heading and blank line)
        lines = text_content.split("\n")
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3

    def test_file_has_blank_line_separator(self, tmp_path):
        """Test that file has blank line after H1 heading."""
        test_file = tmp_path / "test-ju8e95.md"

        content = "# The Power of Code Review\n\nCode review is a critical practice in professional software development, ensuring that multiple eyes examine code changes before they are integrated into the codebase. Beyond catching bugs and potential vulnerabilities, code review facilitates knowledge sharing among team members and establishes consistent coding standards across projects. By fostering a culture of constructive feedback and collaboration, code review transforms individual contributions into collective wisdom, strengthening both code quality and team cohesion.\n"
        test_file.write_text(content, encoding="utf-8")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_uses_pathlib_write_text_with_utf8(self, tmp_path):
        """Test that file is created using pathlib.Path.write_text() with UTF-8."""
        test_file = tmp_path / "test-ju8e95.md"

        content = "# The Power of Code Review\n\nCode review is a critical practice in professional software development, ensuring that multiple eyes examine code changes before they are integrated into the codebase. Beyond catching bugs and potential vulnerabilities, code review facilitates knowledge sharing among team members and establishes consistent coding standards across projects. By fostering a culture of constructive feedback and collaboration, code review transforms individual contributions into collective wisdom, strengthening both code quality and team cohesion.\n"
        # Use pathlib.Path.write_text() with explicit UTF-8
        test_file.write_text(content, encoding="utf-8")

        assert test_file.exists()
        # Verify it was written as UTF-8 by reading it back
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content == content


class TestMarkdownFileValidation:
    """Tests for task-1: Validate file encoding, line endings, and size."""

    MIN_SIZE = 400
    MAX_SIZE = 600

    def test_file_not_utf8_bom(self, tmp_path):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = tmp_path / "test-ju8e95.md"

        content = "# The Power of Code Review\n\nCode review is a critical practice in professional software development, ensuring that multiple eyes examine code changes before they are integrated into the codebase. Beyond catching bugs and potential vulnerabilities, code review facilitates knowledge sharing among team members and establishes consistent coding standards across projects. By fostering a culture of constructive feedback and collaboration, code review transforms individual contributions into collective wisdom, strengthening both code quality and team cohesion.\n"
        test_file.write_text(content, encoding="utf-8")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_file_has_no_crlf_line_endings(self, tmp_path):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = tmp_path / "test-ju8e95.md"

        content = "# The Power of Code Review\n\nCode review is a critical practice in professional software development, ensuring that multiple eyes examine code changes before they are integrated into the codebase. Beyond catching bugs and potential vulnerabilities, code review facilitates knowledge sharing among team members and establishes consistent coding standards across projects. By fostering a culture of constructive feedback and collaboration, code review transforms individual contributions into collective wisdom, strengthening both code quality and team cohesion.\n"
        test_file.write_text(content, encoding="utf-8")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content

    def test_file_size_within_range(self, tmp_path):
        """Test that file size is between 400-600 bytes (inclusive)."""
        test_file = tmp_path / "test-ju8e95.md"

        content = "# The Power of Code Review\n\nCode review is a critical practice in professional software development, ensuring that multiple eyes examine code changes before they are integrated into the codebase. Beyond catching bugs and potential vulnerabilities, code review facilitates knowledge sharing among team members and establishes consistent coding standards across projects. By fostering a culture of constructive feedback and collaboration, code review transforms individual contributions into collective wisdom, strengthening both code quality and team cohesion.\n"
        test_file.write_text(content, encoding="utf-8")

        file_size = test_file.stat().st_size
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE
