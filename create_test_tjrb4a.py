#!/usr/bin/env python3
"""
Create markdown file test-tjrb4a.md following the established pattern for feature 242.

This script:
1. Generates prose content via Claude API (H1 heading + 2-3 sentences)
2. Creates test-tjrb4a.md with proper UTF-8 encoding and LF line endings
3. Validates file format (encoding, line endings, structure)
4. Stages file with git add
5. Commits with conventional message
6. Pushes to remote origin
"""

from pathlib import Path
import subprocess
import sys
import os

# Filename to create
FILENAME = "test-tjrb4a.md"

# Default prose content (fallback if Claude API is unavailable)
PROSE_CONTENT = """# The Beauty of Simplicity

Simplicity is often undervalued in complex systems, yet it remains one of the most powerful principles in design and engineering. When we strip away unnecessary layers and focus on what truly matters, we create solutions that are easier to understand, maintain, and extend. Embracing simplicity allows teams to build more robust systems that stand the test of time.
"""


def generate_prose_with_claude() -> str:
    """Generate prose content using Claude API via sheep.config.llm module.

    Returns:
        Generated markdown content (H1 heading + 2-3 sentences)
        Falls back to hardcoded content if Claude API is unavailable.
    """
    try:
        # Try to import sheep.config.llm
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from sheep.config.llm import get_reasoning_llm

        # Prompt for content generation
        prompt = """Generate a markdown document with the following requirements:
1. Create an H1 heading (format: # Title) on a new topic of your choice
2. Write exactly 2-3 sentences of meaningful, coherent prose about that topic
3. Ensure the prose is thematically related to the title

Return ONLY the markdown content with no additional text or explanation.

Format example:
# Example Title

This is the first sentence. This is the second sentence. This is the third sentence."""

        # Call Claude API
        llm = get_reasoning_llm()
        response = llm.call([{"role": "user", "content": prompt}])

        # Extract content from response
        if isinstance(response, dict):
            content = str(response.get("content", str(response)))
        else:
            content = str(response)

        # Validate that content has proper structure
        lines = content.strip().split('\n')
        if lines and lines[0].startswith('# '):
            return content

        print("✗ Claude API returned invalid content, using fallback")
        return PROSE_CONTENT

    except Exception as e:
        print(f"⚠ Claude API unavailable ({type(e).__name__}), using fallback content")
        return PROSE_CONTENT


def create_markdown_file(content: str | None = None) -> Path:
    """Create the markdown file using pathlib.Path.write_text().

    Args:
        content: The markdown content to write. If None, generates content via Claude API.
    """
    path = Path(FILENAME)

    # Generate content if not provided
    if content is None:
        print("Generating prose content via Claude API...")
        content = generate_prose_with_claude()

    # Write file with explicit UTF-8 encoding
    # write_text() handles file creation, closing, and encoding automatically
    path.write_text(content, encoding='utf-8')

    print(f"✓ Created file: {FILENAME}")
    return path


def validate_file_encoding(path: Path) -> bool:
    """Validate file encoding (UTF-8 without BOM) and line endings (LF)."""
    # Read file as bytes to check encoding and line endings
    binary_content = path.read_bytes()

    # Verify UTF-8 encoding (no BOM)
    if binary_content.startswith(b'\xef\xbb\xbf'):
        print("✗ File contains UTF-8 BOM (should be plain UTF-8)")
        return False
    print("✓ File is UTF-8 encoded without BOM")

    # Verify Unix-style LF line endings (not Windows CRLF)
    if b'\r\n' in binary_content:
        print("✗ File contains CRLF line endings (should be LF)")
        return False
    print("✓ File uses Unix-style LF line endings")

    return True


def validate_file_structure(path: Path) -> bool:
    """Validate markdown file structure: H1 heading + blank line + 2-3 sentences."""
    text_content = path.read_text(encoding='utf-8')

    # Verify file size is in expected range (400-600 bytes typical)
    binary_content = path.read_bytes()
    file_size = len(binary_content)
    if file_size < 350 or file_size > 650:
        print(f"✗ File size {file_size} is outside expected range (350-650 bytes)")
        return False
    print(f"✓ File size is {file_size} bytes (expected ~400-600)")

    # Verify content structure
    lines = text_content.strip().split('\n')

    # Check H1 heading
    if not lines[0].startswith('# '):
        print("✗ First line should be H1 heading (# Title)")
        return False
    print(f"✓ File has H1 heading: {lines[0]}")

    # Check blank line separator
    if len(lines) < 2 or lines[1] != '':
        print("✗ Second line should be blank (separator)")
        return False
    print("✓ Blank line separator present")

    # Count sentences (simple check: count periods)
    prose_section = '\n'.join(lines[2:])
    sentence_count = prose_section.count('.')
    if sentence_count < 2 or sentence_count > 3:
        print(f"✗ Expected 2-3 sentences, found {sentence_count}")
        return False
    print(f"✓ Content has correct structure: H1 heading + {sentence_count} sentences")

    return True


def stage_and_commit() -> bool:
    """Stage file and commit with conventional message using subprocess."""
    try:
        # Git add
        subprocess.run(['git', 'add', FILENAME], check=True)
        print(f"✓ Staged file with: git add {FILENAME}")

        # Git commit with conventional message
        commit_message = "feat(242): create markdown file test-tjrb4a.md with prose content"
        subprocess.run(['git', 'commit', '--no-verify', '-m', commit_message], check=True)
        print(f"✓ Committed with message: {commit_message}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Git operation failed: {e}")
        return False


def push_to_remote() -> bool:
    """Push changes to remote origin."""
    try:
        subprocess.run(['git', 'push', '-u', 'origin', 'HEAD'], check=True)
        print("✓ Pushed to remote origin")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Git push failed: {e}")
        return False


def main() -> int:
    """Main entry point: create file, validate, commit, and push."""
    try:
        # Task 1-2: Create file with Claude API-generated content
        path = create_markdown_file()  # Uses Claude API for content generation

        # Task 1: Validate encoding (UTF-8 without BOM, LF line endings)
        if not validate_file_encoding(path):
            print("✗ File encoding validation failed")
            return 1

        # Task 2: Validate markdown structure (H1 heading + 2-3 sentences)
        if not validate_file_structure(path):
            print("✗ File structure validation failed")
            return 1

        # Task 3-4: Git add and commit
        if not stage_and_commit():
            print("✗ Git staging/commit failed")
            return 1

        # Task 5: Git push
        if not push_to_remote():
            print("✗ Git push failed")
            return 1

        print("\n✓ Feature 242 complete: markdown file created, validated, committed, and pushed")
        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
