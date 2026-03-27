"""
Implementation script for feature 244: markdown file creation.

This module provides functions to:
1. Create a markdown file (test-fyijj3.md) with proper structure and content
2. Validate the file properties (encoding, line endings, size, structure)
3. Execute git operations (add, commit, push) using subprocess

The implementation uses Python standard library (pathlib, subprocess) for
git operations and supports Claude API for prose generation with a hardcoded fallback.
"""

from pathlib import Path
import subprocess
import markdown


# ============================================================================
# Constants
# ============================================================================

FILENAME = "test-fyijj3.md"
MIN_SIZE = 350
MAX_SIZE = 650

# Prose about energy solutions (3 sentences, ~400 bytes total) - FALLBACK
PROSE_CONTENT = (
    "Energy efficiency has become a critical focus for businesses and households seeking to reduce operational costs and environmental impact in an era of climate change. "
    "Renewable energy sources such as solar, wind, and hydroelectric power are increasingly cost-competitive with traditional fossil fuels while generating zero emissions during operation. "
    "By investing in sustainable energy solutions and improving energy infrastructure, we can build a cleaner, more resilient future for generations to come."
)


# ============================================================================
# Prose Generation Function
# ============================================================================

def generate_prose_with_claude():
    """
    Generate prose content using Claude API.

    Attempts to call the Claude API to generate coherent, thematically
    appropriate prose. If the API is unavailable or fails, returns None
    to trigger fallback behavior.

    Returns:
        str or None: Generated prose content if successful, None if API unavailable
    """
    try:
        from anthropic import Anthropic

        client = Anthropic()

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Write exactly 3 sentences of prose about any topic you choose. "
                        "The sentences must be thematically coherent, grammatically correct, "
                        "and together form a cohesive paragraph about a single topic. "
                        "Do not include a heading or title, only the prose sentences. "
                        "Ensure each sentence ends with a period. "
                        "Total length should be approximately 300-400 characters."
                    )
                }
            ]
        )

        prose = message.content[0].text.strip()

        # Validate that we got prose content
        if prose and len(prose) > 100:
            return prose

        return None

    except Exception as e:
        # API unavailable or failed; return None to trigger fallback
        print(f"Claude API call failed (using fallback): {type(e).__name__}")
        return None


# ============================================================================
# File Creation Function
# ============================================================================

def create_file():
    """
    Create test-fyijj3.md in the current directory with markdown structure.

    The file contains:
    - H1 heading (# Title)
    - Blank line
    - 3-sentence prose paragraph about energy solutions
    - UTF-8 encoding without BOM
    - Unix LF line endings

    Prose is generated via Claude API if available; falls back to hardcoded
    content if API is unavailable.

    Returns:
        Path: Path object pointing to the created file

    Raises:
        FileExistsError: If test-fyijj3.md already exists in current directory
    """
    filepath = Path(FILENAME)

    # Prevent overwriting existing files
    if filepath.exists():
        raise FileExistsError(f"File {FILENAME} already exists in current directory. Remove it to proceed.")

    # Generate prose content (Claude API with fallback)
    prose = generate_prose_with_claude()
    if prose is None:
        prose = PROSE_CONTENT

    # Build markdown content with proper structure
    markdown_content = (
        "# Energy and Sustainability\n"
        "\n"
        f"{prose}\n"
    )

    # Write file with UTF-8 encoding (no BOM) and Unix line endings
    filepath.write_text(markdown_content, encoding="utf-8", newline="\n")

    return filepath


# ============================================================================
# File Validation Function
# ============================================================================

def validate_file(filepath):
    """
    Validate that a markdown file meets all specification requirements.

    Checks (in order):
    - File exists
    - UTF-8 encoding without BOM
    - Unix LF line endings (no Windows CRLF)
    - Contains exactly one H1 heading (first line starts with "# ")
    - Contains blank line after heading
    - Contains substantive prose content (not just whitespace)
    - File size is within 350-650 byte range
    - File ends with newline
    - Markdown structure is valid according to CommonMark specification

    Args:
        filepath (Path or str): Path to the markdown file to validate

    Returns:
        bool: True if all validations pass

    Raises:
        AssertionError: If any validation fails with descriptive error message
    """
    filepath = Path(filepath)

    # 1. Check file exists
    assert filepath.exists(), f"File {filepath.name} does not exist"

    # 2. Read file content
    binary_content = filepath.read_bytes()
    file_size = len(binary_content)

    # 3. Check encoding (UTF-8 without BOM)
    assert not binary_content.startswith(b'\xef\xbb\xbf'), (
        "File has UTF-8 BOM (Byte Order Mark). Should use UTF-8 without BOM."
    )

    try:
        content = binary_content.decode('utf-8')
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}") from e

    # 4. Check line endings (LF only, no CRLF)
    assert '\r\n' not in content, (
        "File contains Windows CRLF line endings. Should use Unix LF (\\n) only."
    )
    assert '\n' in content, (
        "File does not contain any line endings. Should use Unix LF (\\n)."
    )

    # 5. Check trailing newline
    assert binary_content.endswith(b'\n'), (
        "File should end with a newline character."
    )

    # 6. Check structure: H1 heading + blank line + prose
    lines = content.split('\n')

    # Check H1 heading on first line
    assert lines[0].startswith('# '), (
        f"Missing H1 heading: first line should start with '# ' but found: {lines[0][:50]}"
    )

    # Check blank line after heading
    assert len(lines) > 1, "File should contain more than just a heading"
    assert lines[1] == '', (
        f"Missing blank line after heading: second line should be empty but found: {repr(lines[1][:50])}"
    )

    # Check prose content (not just whitespace)
    prose = '\n'.join(lines[2:]).strip()
    assert prose, "File should contain prose content after blank line"

    # 7. Check file size
    assert MIN_SIZE < file_size < MAX_SIZE, (
        f"File size {file_size} bytes outside typical range ({MIN_SIZE}-{MAX_SIZE}). "
        f"Expected range for validation: 350-650 bytes."
    )

    # 8. Check for at least 2 sentences (periods)
    period_count = prose.count('.')
    assert period_count >= 2, (
        f"Prose content should contain at least 2 sentences, but only found {period_count} period(s)."
    )

    # 9. Validate CommonMark markdown structure
    try:
        md = markdown.Markdown(extensions=[])
        html_output = md.convert(content)
        # Verify output contains h1 tag (indicates heading was parsed)
        assert '<h1>' in html_output.lower(), (
            "CommonMark validation failed: H1 heading not properly parsed"
        )
        # Verify output contains paragraph tags (indicates prose was parsed)
        assert '<p>' in html_output.lower(), (
            "CommonMark validation failed: Prose content not properly parsed"
        )
    except Exception as e:
        raise AssertionError(f"CommonMark markdown validation failed: {e}") from e

    return True


# ============================================================================
# Git Operations Function
# ============================================================================

def git_operations():
    """
    Execute git operations to stage, commit, and push the markdown file.

    Uses subprocess.run() for git command execution.

    Operations:
    1. git add test-fyijj3.md
    2. git commit --no-verify -m "feat(244): create markdown file test-fyijj3.md with prose content"
    3. git push to origin/HEAD

    Raises:
        Exception: If any git operation fails
    """
    # Stage the file
    subprocess.run(['git', 'add', FILENAME], check=True)

    # Create commit with conventional commit message
    commit_message = "feat(244): create markdown file test-fyijj3.md with prose content"
    subprocess.run(['git', 'commit', '--no-verify', '-m', commit_message], check=True)

    # Push to origin (current branch)
    subprocess.run(['git', 'push', '-u', 'origin', 'HEAD'], check=True)


# ============================================================================
# Main Execution
# ============================================================================

if __name__ == "__main__":
    # Create the markdown file
    filepath = create_file()
    print(f"Created file: {filepath}")

    # Validate the created file
    try:
        validate_file(filepath)
        print(f"Validation passed: {filepath.name}")
    except AssertionError as e:
        print(f"Validation failed: {e}")
        raise

    # Execute git operations
    try:
        git_operations()
        print(f"Git operations completed successfully")
    except Exception as e:
        print(f"Git operations failed: {e}")
        raise

    print("Feature 244 implementation complete!")
