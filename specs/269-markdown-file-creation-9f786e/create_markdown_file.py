#!/usr/bin/env python3
"""
Create a markdown file (test-hb8tyt.md) with auto-generated title and prose content.

This script automates the creation of a test markdown file using Anthropic Claude API
for intelligent content generation. This feature differs from prior implementations
(266-268) by using LLM-based auto-generation instead of hard-coded content, aligning
with Sheep platform's LLM-first architecture and CrewAI integration.

The implementation:
1. Generates intelligent, context-aware title + 2-3 sentences using Claude API
2. Creates a markdown file with H1 heading and prose content
3. Validates the file structure, encoding, and size
4. Stages, commits, and pushes the file to git

Uses only Python standard library modules (pathlib, subprocess, sys, os) plus
Anthropic SDK (assumed available in Sheep platform for CrewAI integration).

File requirements:
- UTF-8 encoding without BOM (Byte Order Mark)
- Unix-style LF line endings
- File size typically 400-600 bytes
- Conventional commit message format
"""

import os
import subprocess
import sys
from pathlib import Path

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic library not found. Install with: pip install anthropic", file=sys.stderr)
    sys.exit(1)

# Module-level constants
FILENAME = "test-hb8tyt.md"
COMMIT_MESSAGE = "feat(269): create markdown file test-hb8tyt.md with title and prose content"

# Claude API prompt for content generation
CONTENT_GENERATION_PROMPT = """Generate a title and 2-3 sentences of prose content for a markdown file.

Requirements:
- Title: A single short phrase (1-5 words) suitable for a markdown H1 heading
- Prose: Exactly 2-3 complete sentences on any topic, each ending with a period
- Format: Return ONLY the title on the first line, blank line, then prose sentences

Example format:
The Power of Iteration

Iteration is a fundamental principle in software development that drives improvement through repeated cycles of design, implementation, and refinement. Each iteration builds upon the previous one, incorporating feedback and lessons learned to refine approaches. By embracing iterative processes, teams adapt to changing requirements and deliver increasingly valuable solutions.

Generate unique, varied, and contextually relevant content."""


def generate_content():
    """
    Generate markdown title and prose content using Anthropic Claude API.

    This function calls Claude API to generate intelligent, context-aware content
    that follows the markdown file specification: title (1-5 words) + 2-3 sentences
    of prose. Uses ANTHROPIC_API_KEY environment variable for authentication.

    Returns:
        tuple: A tuple of (title, prose) as strings where:
            - title: 1-5 word markdown H1 heading
            - prose: 2-3 complete sentences ending with periods

    Raises:
        ValueError: If ANTHROPIC_API_KEY environment variable is not set
        Exception: If Claude API call fails (network, authentication, quota)
    """
    # Check for API key in environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is not set. "
            "Please set it before running this script."
        )

    try:
        # Initialize Anthropic client with API key from environment
        client = Anthropic(api_key=api_key)

        # Call Claude API to generate content
        print("Generating content with Claude API...")
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": CONTENT_GENERATION_PROMPT,
                }
            ],
        )

        # Extract text from Claude response
        generated_text = response.content[0].text.strip()

        # Parse the response: title is first line, prose is the rest after blank line
        lines = generated_text.split('\n')

        # Find title (first non-empty line)
        title = ""
        prose_start_idx = 0
        for i, line in enumerate(lines):
            if line.strip():
                title = line.strip()
                prose_start_idx = i + 1
                break

        # Find prose (lines after blank line following title)
        prose = ""
        for i in range(prose_start_idx, len(lines)):
            if lines[i].strip():
                prose = '\n'.join(lines[i:]).strip()
                break

        if not title:
            raise ValueError("Claude API did not generate a valid title")
        if not prose:
            raise ValueError("Claude API did not generate valid prose content")

        print(f"✓ Content generated: title='{title}' prose_length={len(prose)} bytes")
        return (title, prose)

    except ValueError as e:
        raise ValueError(f"Content generation error: {e}")
    except Exception as e:
        raise Exception(f"Claude API call failed: {e}")


def create_file(title, prose):
    """
    Create the markdown file with proper UTF-8 encoding and LF line endings.

    This function:
    - Takes generated title and prose as input
    - Constructs markdown content (H1 heading + blank line + prose)
    - Writes the file using pathlib.Path.write_text() with explicit encoding
    - Ensures UTF-8 encoding without BOM and Unix LF line endings

    Args:
        title (str): The markdown H1 heading title (1-5 words)
        prose (str): The prose content (2-3 sentences)

    Returns:
        Path: The pathlib.Path object pointing to the created file

    Raises:
        IOError: If file creation fails (e.g., permission denied, disk full)
    """
    # Construct the markdown content with H1 heading and prose
    # Using explicit '\n' characters ensures LF line endings
    content = f"# {title}\n\n{prose}\n"

    # Write the file using pathlib.Path.write_text() with explicit encoding
    # This ensures:
    # - UTF-8 encoding without BOM (Byte Order Mark)
    # - Unix LF line endings (not CRLF on Windows)
    # - Platform independence
    filepath = Path(FILENAME)
    filepath.write_text(content, encoding='utf-8', newline='\n')

    return filepath


def validate_file(filepath):
    """
    Validate the markdown file structure, encoding, and size.

    This function checks:
    - File exists and is readable
    - File is valid UTF-8 encoding without BOM
    - File uses Unix LF line endings (not Windows CRLF)
    - File contains H1 heading on first line
    - File contains blank line after heading
    - File contains prose content
    - File size is in typical range (400-600 bytes, tolerating 300-800)

    Args:
        filepath (Path): Path object pointing to the markdown file

    Returns:
        bool: True if all validations pass

    Raises:
        AssertionError: If any validation fails with descriptive error message
    """
    # Check 1: File exists
    assert filepath.exists(), f"File {filepath} does not exist"

    # Check 2: File is valid UTF-8 without BOM
    binary_content = filepath.read_bytes()
    assert not binary_content.startswith(b'\xef\xbb\xbf'), (
        f"File must be UTF-8 encoded without BOM (Byte Order Mark)"
    )

    try:
        binary_content.decode('utf-8')
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}")

    # Check 3: File uses Unix LF line endings (not Windows CRLF)
    assert b'\r\n' not in binary_content, (
        "File must use Unix LF line endings (\\n), not Windows CRLF (\\r\\n)"
    )

    # Check 4: File ends with newline
    assert binary_content.endswith(b'\n'), (
        "File must end with a newline character"
    )

    # Check 5: File contains H1 heading on first line
    content = filepath.read_text(encoding='utf-8')
    assert content.startswith('# '), "File must start with H1 heading (# )"

    # Check 6: File contains blank line after heading
    assert '\n\n' in content, "File must contain blank line after heading (double newline)"

    # Check 7: File has prose content after blank line
    # Split by double newline to separate heading from prose
    parts = content.split('\n\n', 1)
    assert len(parts) == 2, "File structure should be: heading, blank line, prose"
    prose = parts[1].strip()
    assert len(prose) > 0, "File must contain prose content after heading"

    # Check 8: File size is in typical range (400-600 bytes, tolerating 300-800)
    file_size = filepath.stat().st_size
    assert 300 < file_size < 800, (
        f"File size {file_size} bytes is outside typical range (300-800 bytes). "
        f"Expected approximately 400-600 bytes for structure: H1 heading + blank line + 2-3 sentences."
    )

    return True


def git_operations():
    """
    Stage, commit, and push the markdown file to git.

    This function performs:
    1. git add test-hb8tyt.md (stage the file)
    2. git commit -m "feat(269): create markdown file test-hb8tyt.md with title and prose content"
    3. git push -u origin HEAD (push to remote with upstream tracking)

    Uses subprocess.run() with check=True for comprehensive error handling.
    Any git command failure raises CalledProcessError with details.

    Raises:
        subprocess.CalledProcessError: If any git command fails, with descriptive context
    """
    # Stage the file using git add
    # check=True ensures CalledProcessError is raised if git add fails
    print("Staging file with git add...")
    subprocess.run(["git", "add", FILENAME], check=True)
    print("✓ File staged")

    # Commit the file with conventional commit message
    print(f"Committing with message: {COMMIT_MESSAGE}")
    subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], check=True)
    print("✓ File committed")

    # Push to remote origin using current branch
    # The -u flag sets upstream tracking for the current branch
    # HEAD refers to the current branch being worked on
    print("Pushing to remote origin...")
    subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)
    print("✓ File pushed to remote")


def main():
    """
    Main entry point: orchestrate content generation, file creation, validation, and git operations.

    This function coordinates the workflow:
    1. Generate content (title + prose) using Claude API
    2. Create the markdown file with proper structure
    3. Validate the file structure, encoding, and content
    4. Perform git operations (add, commit, push)

    Exits with status code 0 on success, 1 on failure with descriptive error messages.
    """
    try:
        # Phase 1: Content generation using Claude API
        print("Phase 1: Content Generation & File Creation")
        print("=" * 50)
        title, prose = generate_content()

        # Phase 2: File creation and validation
        print("\nCreating markdown file...")
        filepath = create_file(title, prose)
        print(f"✓ File created: {filepath}")

        print("Validating file...")
        validate_file(filepath)
        print("✓ File validation passed")
        print(f"  - File size: {filepath.stat().st_size} bytes")
        print(f"  - Title: {title}")
        print(f"  - Content length: {len(prose)} characters")

        # Phase 3: Git integration and execution
        print("\nPhase 2: Git Workflow Integration")
        print("=" * 50)
        print("\nPerforming git operations...")
        git_operations()

        print("\n" + "=" * 50)
        print("✓ Workflow complete!")
        print("=" * 50)
        print("File has been created, validated, staged, committed, and pushed to remote.")
        sys.exit(0)

    except ValueError as e:
        print(f"✗ Content generation error: {e}", file=sys.stderr)
        sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"✗ Git command failed: {e}", file=sys.stderr)
        print(f"Command: {e.cmd}", file=sys.stderr)
        print(f"Return code: {e.returncode}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
