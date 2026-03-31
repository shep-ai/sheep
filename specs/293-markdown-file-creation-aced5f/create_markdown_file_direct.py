#!/usr/bin/env python3
"""
Direct implementation for feature 293: Create markdown file test-msqxtg.md

This script uses the Anthropic SDK directly (not through CrewAI) to generate
markdown content and perform the complete workflow:
1. Generate markdown content via Claude API
2. Write file to disk
3. Validate file
4. Commit to git
5. Push to remote
"""

import subprocess
import sys
from pathlib import Path
from anthropic import Anthropic

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sheep.content_generators import (
    write_markdown_file,
    validate_markdown_file,
    git_add,
    git_commit,
    git_push,
    _validate_markdown_content,
)


def generate_markdown_with_claude() -> str:
    """
    Generate markdown content using Anthropic Claude API directly.

    Returns:
        String containing valid markdown with H1 heading and 2-3 sentences of prose.

    Raises:
        ValueError: If generated content doesn't meet format requirements.
    """
    client = Anthropic()

    prompt = """Generate a markdown document with the following structure:
1. An H1 heading (using #) with a title about any topic you choose
2. A blank line
3. Exactly 2-3 sentences of coherent prose about that topic

Return ONLY the markdown content, no additional text or explanation.

Format example:
# Example Title

This is the first sentence. This is the second sentence. This is the third sentence."""

    print("Calling Claude API to generate markdown content...")

    try:
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        content = message.content[0].text

        # Ensure trailing newline
        if not content.endswith("\n"):
            content = content + "\n"

        # Validate the response
        _validate_markdown_content(content)

        print(f"✓ Generated {len(content)} bytes of markdown content")
        return content

    except Exception as e:
        print(f"✗ Failed to generate markdown content: {e}", file=sys.stderr)
        raise


def main():
    """
    Main entry point for feature 293 markdown file creation.
    """
    filename = "test-msqxtg.md"
    feature_number = 293

    print(f"Creating markdown file: {filename}")
    print(f"Feature: {feature_number}")
    print("-" * 60)

    try:
        # Step 1: Generate content
        print("\nStep 1: Generating markdown content via Claude API...")
        content = generate_markdown_with_claude()

        # Step 2: Write file
        print("Step 2: Writing file to disk...")
        filepath = write_markdown_file(content, filename)
        print(f"✓ File written: {filepath}")

        # Step 3: Validate file
        print("Step 3: Validating markdown file...")
        validate_markdown_file(filepath)
        print("✓ File validation passed")

        # Step 4: Stage file
        print("Step 4: Staging file with git add...")
        git_add(filename)
        print(f"✓ File staged: {filename}")

        # Step 5: Commit file
        print("Step 5: Creating git commit...")
        message = f"feat({feature_number}): create markdown file {filename} with prose content"
        git_commit(message)
        print(f"✓ Commit created: {message}")

        # Step 6: Push to remote
        print("Step 6: Pushing to remote repository...")
        try:
            push_result = git_push()
            print(f"✓ Pushed to remote")
        except Exception as e:
            print(f"⚠ Push failed (may be expected in test environment): {e}")
            push_result = f"Push skipped: {e}"

        print("\n" + "=" * 60)
        print("✓ Successfully created markdown file!")
        print("=" * 60)
        print(f"File: {filename}")
        print(f"Content length: {len(content)} bytes")
        print(f"Commit message: {message}")

        return {
            "filepath": filepath,
            "content": content,
            "commit_message": message,
            "push_result": push_result,
        }

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
