"""
Standalone validation script for test-4ulmku.md

This script validates that the created markdown file meets all specifications:
- UTF-8 encoding without BOM
- Unix LF line endings (no Windows CRLF)
- Proper markdown structure (H1 heading + blank line + prose)
- Correct file size (300-600 bytes)
- Proper sentence count (2-3 sentences)
"""

from pathlib import Path


def validate_encoding_and_line_endings(filepath):
    """
    Validate file encoding (UTF-8 without BOM) and line endings (Unix LF).

    Args:
        filepath (Path or str): Path to the markdown file

    Returns:
        dict: Validation results with keys for each check
    """
    filepath = Path(filepath)
    results = {
        "file_exists": False,
        "utf8_valid": False,
        "has_no_bom": False,
        "has_lf_endings": False,
        "has_no_crlf": False,
        "ends_with_lf": False,
    }

    # Check file exists
    if not filepath.exists():
        print(f"❌ File does not exist: {filepath}")
        return results

    results["file_exists"] = True
    print(f"✓ File exists: {filepath}")

    # Read binary content
    binary_content = filepath.read_bytes()

    # Check UTF-8 encoding (no BOM)
    if binary_content.startswith(b'\xef\xbb\xbf'):
        print("❌ File has UTF-8 BOM (Byte Order Mark)")
        print(f"   First 3 bytes: {binary_content[:3].hex()}")
    else:
        results["has_no_bom"] = True
        print("✓ File has no UTF-8 BOM")

    # Check valid UTF-8 encoding
    try:
        content = binary_content.decode('utf-8')
        results["utf8_valid"] = True
        print("✓ File is valid UTF-8 encoded")
    except UnicodeDecodeError as e:
        print(f"❌ File is not valid UTF-8: {e}")
        return results

    # Check for CRLF line endings
    if b'\r\n' in binary_content:
        print("❌ File contains Windows CRLF line endings (\\r\\n)")
    else:
        results["has_no_crlf"] = True
        print("✓ File has no CRLF line endings")

    # Check for LF line endings
    if b'\n' in binary_content:
        results["has_lf_endings"] = True
        print("✓ File has LF line endings")
    else:
        print("❌ File has no LF line endings")

    # Check file ends with LF
    if binary_content.endswith(b'\n'):
        results["ends_with_lf"] = True
        print("✓ File ends with LF (\\n)")
    else:
        print("❌ File does not end with LF")
        print(f"   Last 2 bytes: {binary_content[-2:].hex()}")

    return results


def validate_structure(filepath):
    """
    Validate markdown file structure.

    Args:
        filepath (Path or str): Path to the markdown file

    Returns:
        dict: Validation results
    """
    filepath = Path(filepath)
    results = {
        "has_h1_heading": False,
        "has_blank_line": False,
        "has_prose_content": False,
        "has_valid_size": False,
        "has_valid_sentence_count": False,
    }

    if not filepath.exists():
        print(f"❌ File does not exist: {filepath}")
        return results

    # Read text content
    try:
        content = filepath.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        print(f"❌ Cannot read file as UTF-8: {e}")
        return results

    # Check H1 heading
    if content.startswith("# "):
        results["has_h1_heading"] = True
        first_line = content.split('\n')[0]
        print(f"✓ File has H1 heading: {first_line}")
    else:
        print(f"❌ File does not start with H1 heading")
        print(f"   First 30 chars: {content[:30]}")

    # Check blank line
    if '\n\n' in content:
        results["has_blank_line"] = True
        print("✓ File has blank line after heading")
    else:
        print("❌ File does not have blank line after heading")

    # Check prose content
    lines = content.split('\n')
    if len(lines) > 2:
        prose = '\n'.join(lines[2:]).strip()
        if prose:
            results["has_prose_content"] = True
            prose_preview = prose[:60] + "..." if len(prose) > 60 else prose
            print(f"✓ File has prose content: {prose_preview}")
        else:
            print("❌ File has no prose content")
    else:
        print("❌ File structure is incomplete")

    # Check file size
    file_size = filepath.stat().st_size
    if 300 < file_size < 600:
        results["has_valid_size"] = True
        print(f"✓ File size is valid: {file_size} bytes (300-600 range)")
    else:
        print(f"❌ File size is invalid: {file_size} bytes (outside 300-600 range)")

    # Check sentence count
    prose = '\n'.join(lines[2:]).strip() if len(lines) > 2 else ""
    sentences = [s.strip() for s in prose.split('.') if s.strip()]
    if 2 <= len(sentences) <= 3:
        results["has_valid_sentence_count"] = True
        print(f"✓ File has valid sentence count: {len(sentences)} sentences")
    else:
        print(f"❌ File has invalid sentence count: {len(sentences)} sentences (should be 2-3)")

    return results


def main():
    """Run all validation checks."""
    filepath = Path("test-4ulmku.md")

    print("=" * 70)
    print("Validating Markdown File: test-4ulmku.md")
    print("=" * 70)

    # Encoding and line endings validation
    print("\n--- Encoding and Line Endings ---")
    encoding_results = validate_encoding_and_line_endings(filepath)

    # Structure validation
    print("\n--- File Structure ---")
    structure_results = validate_structure(filepath)

    # Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    all_results = {**encoding_results, **structure_results}
    passed = sum(1 for v in all_results.values() if v is True)
    total = len([v for v in all_results.values() if isinstance(v, bool)])

    print(f"Passed: {passed}/{total} checks")

    if passed == total:
        print("\n✓ ALL VALIDATION CHECKS PASSED!")
        return 0
    else:
        print(f"\n❌ {total - passed} validation check(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
