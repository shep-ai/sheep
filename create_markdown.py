#!/usr/bin/env python3
"""Create and validate markdown file for feature 262."""

from pathlib import Path


def create_markdown_file(filename="test-mylh5m.md"):
    """Create markdown file with H1 heading and 2-3 sentences of prose.

    Returns:
        Path: Path object pointing to the created file
    """
    # Compose H1 heading and prose content
    heading = "# The Elegance of Mountain Ecosystems"
    prose = (
        "Mountain ecosystems represent some of the most biodiverse and resilient "
        "environments on Earth, supporting countless species adapted to harsh alpine conditions. "
        "These landscapes have shaped human culture for millennia, providing inspiration for art, "
        "literature, and spiritual practices across civilizations."
    )

    # Construct complete content with proper structure
    content = f"{heading}\n\n{prose}\n"

    # Write file with explicit UTF-8 encoding (no BOM) and LF line endings
    filepath = Path(filename)
    filepath.write_text(content, encoding='utf-8', newline='\n')

    return filepath


def validate_markdown_file(filename="test-mylh5m.md"):
    """Validate markdown file meets all structural and encoding requirements.

    Returns:
        dict: Validation results with keys for each check (all should be True)
    """
    filepath = Path(filename)

    results = {
        "file_exists": False,
        "h1_heading_present": False,
        "blank_line_after_heading": False,
        "prose_sentence_count": 0,
        "prose_sentences_valid": False,
        "utf8_no_bom": False,
        "lf_line_endings": False,
        "file_size_valid": False,
        "prose_coherent": False,
    }

    # Check file exists
    if not filepath.exists():
        return results
    results["file_exists"] = True

    # Read file as bytes to check for BOM
    file_bytes = filepath.read_bytes()

    # Check for UTF-8 BOM (EF BB BF)
    has_bom = file_bytes.startswith(b'\xef\xbb\xbf')
    results["utf8_no_bom"] = not has_bom

    # Read file content as text
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Check H1 heading on line 1
    if lines and lines[0].startswith('# '):
        results["h1_heading_present"] = True

    # Check blank line after heading
    if len(lines) > 1 and lines[1] == '':
        results["blank_line_after_heading"] = True

    # Check prose content (lines 2+)
    prose_lines = lines[2:]
    prose_text = '\n'.join(prose_lines).strip()

    # Count sentences (split on '. ' and '.\n')
    sentences = [s.strip() for s in prose_text.replace('.\n', '. ').split('. ') if s.strip()]
    sentence_count = len(sentences)
    results["prose_sentence_count"] = sentence_count
    results["prose_sentences_valid"] = 2 <= sentence_count <= 3

    # Check for prose coherence (basic: non-empty, no obvious gibberish)
    results["prose_coherent"] = bool(prose_text) and len(prose_text) > 50

    # Check line endings (no CRLF)
    results["lf_line_endings"] = '\r\n' not in content

    # Check file size (300-600 bytes)
    file_size = len(file_bytes)
    results["file_size_valid"] = 300 <= file_size <= 600

    return results


if __name__ == "__main__":
    # Create the markdown file
    filepath = create_markdown_file()
    print(f"[OK] Created {filepath}")

    # Validate the file
    validation = validate_markdown_file()
    print("\nValidation Results:")
    all_passed = True
    for check, result in validation.items():
        status = "PASS" if result else "FAIL"
        print(f"  [{status}] {check}: {result}")
        if check != "prose_sentence_count" and not result:
            all_passed = False

    if all_passed:
        print("\n[OK] All validations passed!")
    else:
        print("\n[FAIL] Some validations failed!")
        exit(1)
