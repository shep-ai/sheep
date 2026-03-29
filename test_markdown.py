#!/usr/bin/env python3
"""Tests for markdown file creation (task-1) and validation (task-2)."""

from pathlib import Path
from create_markdown import validate_markdown_file


class TestMarkdownFileCreation:
    """Tests for Task 1: Create markdown file with H1 heading and prose content."""

    def test_file_created_in_root(self):
        """Test that file test-mylh5m.md exists in repository root."""
        filepath = Path("test-mylh5m.md")
        assert filepath.exists(), "File test-mylh5m.md should exist"

    def test_h1_heading_on_first_line(self):
        """Test that file starts with exactly one H1 markdown heading."""
        filepath = Path("test-mylh5m.md")
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        assert len(lines) > 0, "File should have at least one line"
        assert lines[0].startswith('# '), "First line should start with '# '"
        h1_count = sum(1 for line in lines if line.startswith('# '))
        assert h1_count == 1, f"File should have 1 H1, found {h1_count}"

    def test_blank_line_after_heading(self):
        """Test that file has blank line after H1 heading."""
        filepath = Path("test-mylh5m.md")
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        assert len(lines) > 1, "File should have at least 2 lines"
        assert lines[1] == '', "Line 2 should be blank"

    def test_prose_sentence_count(self):
        """Test that file contains exactly 2-3 sentences of prose."""
        filepath = Path("test-mylh5m.md")
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        prose_lines = lines[2:]
        prose_text = '\n'.join(prose_lines).strip()
        sentences = [s.strip() for s in prose_text.replace('.\n', '. ').split('. ') if s.strip()]
        
        assert 2 <= len(sentences) <= 3, f"Should have 2-3 sentences, found {len(sentences)}"

    def test_utf8_encoding_no_bom(self):
        """Test that file is encoded in UTF-8 without Byte Order Mark."""
        filepath = Path("test-mylh5m.md")
        file_bytes = filepath.read_bytes()
        
        has_bom = file_bytes.startswith(b'\xef\xbb\xbf')
        assert not has_bom, "File should not have UTF-8 BOM"

    def test_lf_line_endings(self):
        """Test that file uses LF line endings, not CRLF."""
        filepath = Path("test-mylh5m.md")
        file_bytes = filepath.read_bytes()
        
        has_crlf = b'\r\n' in file_bytes
        assert not has_crlf, "File should use LF, not CRLF"

    def test_file_size_in_range(self):
        """Test that file size is between 300-600 bytes."""
        filepath = Path("test-mylh5m.md")
        file_size = len(filepath.read_bytes())
        
        assert 300 <= file_size <= 600, f"File should be 300-600 bytes, got {file_size}"


class TestMarkdownFileValidation:
    """Tests for Task 2: Validate markdown file structure and encoding."""

    def test_validation_function_exists(self):
        """Test that validate_markdown_file function exists."""
        assert callable(validate_markdown_file), "validate_markdown_file should be callable"

    def test_validation_returns_dict(self):
        """Test that validator returns a dictionary with expected keys."""
        validation = validate_markdown_file()
        
        assert isinstance(validation, dict), "Validator should return dict"
        expected_keys = {
            "file_exists", "h1_heading_present", "blank_line_after_heading",
            "prose_sentence_count", "prose_sentences_valid", "utf8_no_bom",
            "lf_line_endings", "file_size_valid", "prose_coherent",
        }
        assert set(validation.keys()) == expected_keys, "Should return all expected keys"

    def test_all_validations_pass(self):
        """Test that all validation checks pass for the created file."""
        validation = validate_markdown_file()
        
        for key, result in validation.items():
            if key != "prose_sentence_count":
                assert result is True, f"Validation '{key}' should be True, got {result}"

    def test_validation_detects_missing_file(self):
        """Test that validator detects missing files."""
        validation = validate_markdown_file("nonexistent.md")
        assert validation["file_exists"] is False, "Should detect missing file"


if __name__ == "__main__":
    import sys
    
    test_classes = [TestMarkdownFileCreation, TestMarkdownFileValidation]
    failed = 0
    passed = 0
    
    for test_class in test_classes:
        test_instance = test_class()
        methods = [m for m in dir(test_instance) if m.startswith('test_')]
        
        for method_name in methods:
            try:
                method = getattr(test_instance, method_name)
                method()
                print(f"[PASS] {test_class.__name__}.{method_name}")
                passed += 1
            except AssertionError as e:
                print(f"[FAIL] {test_class.__name__}.{method_name}: {e}")
                failed += 1
            except Exception as e:
                print(f"[ERROR] {test_class.__name__}.{method_name}: {e}")
                failed += 1
    
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
