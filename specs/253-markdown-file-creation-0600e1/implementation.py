#!/usr/bin/env python3
"""
Implementation script for feature 253: markdown-file-creation-0600e1

Creates a markdown file (test-bvt0ve.md) with a title and 2-3 sentences of prose
content, and integrates it with git (add, commit, push).

This script demonstrates automated file creation with proper encoding (UTF-8),
line endings (LF), and git workflow integration following the established pattern
from 200+ existing test files in the repository.
"""

import subprocess
import sys
from pathlib import Path


def create_markdown_file(repo_root: Path) -> None:
    """
    Create test-bvt0ve.md with proper markdown structure and encoding.

    File structure: H1 heading + blank line + 2-3 sentences of prose
    Encoding: UTF-8 without BOM
    Line endings: Unix LF (\n), not Windows CRLF (\r\n)

    Args:
        repo_root: Path to repository root directory

    Raises:
        IOError: If file creation fails
    """
    # Define markdown content with a developer-chosen topic
    heading = "# Cloud Computing Innovations"

    prose = (
        "Cloud computing has fundamentally transformed how organizations manage "
        "infrastructure and deploy applications at scale. By leveraging distributed "
        "computing resources and on-demand services, enterprises can achieve greater "
        "flexibility and cost efficiency. Modern cloud platforms enable teams to "
        "focus on innovation rather than managing physical hardware."
    )

    # Construct content: H1 heading + blank line + prose
    content = f"{heading}\n\n{prose}\n"

    # Create file at repository root with explicit UTF-8 encoding and LF line endings
    file_path = repo_root / "test-bvt0ve.md"

    try:
        file_path.write_text(content, encoding='utf-8', newline='\n')
        print(f"✓ Created markdown file: {file_path}")
        print(f"  File size: {file_path.stat().st_size} bytes")
    except IOError as e:
        print(f"✗ Failed to create markdown file: {e}", file=sys.stderr)
        raise


def git_add(repo_root: Path, filename: str) -> None:
    """
    Stage file in git using 'git add' command.

    Args:
        repo_root: Path to repository root directory
        filename: Name of file to stage

    Raises:
        subprocess.CalledProcessError: If git add fails
    """
    try:
        result = subprocess.run(
            ['git', '-C', str(repo_root), 'add', filename],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ Staged file with git: {filename}")
    except subprocess.CalledProcessError as e:
        print(f"✗ git add failed: {e.stderr}", file=sys.stderr)
        raise


def git_commit(repo_root: Path, message: str) -> None:
    """
    Create git commit with conventional commit message.

    Args:
        repo_root: Path to repository root directory
        message: Commit message (exact format: feat(253): ...)

    Raises:
        subprocess.CalledProcessError: If git commit fails
    """
    try:
        result = subprocess.run(
            ['git', '-C', str(repo_root), 'commit', '-m', message],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ Created git commit: {message}")
    except subprocess.CalledProcessError as e:
        print(f"✗ git commit failed: {e.stderr}", file=sys.stderr)
        raise


def git_push(repo_root: Path) -> None:
    """
    Push commit to remote origin.

    Args:
        repo_root: Path to repository root directory

    Raises:
        subprocess.CalledProcessError: If git push fails
    """
    try:
        result = subprocess.run(
            ['git', '-C', str(repo_root), 'push', '-u', 'origin', 'HEAD'],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ Pushed commit to remote origin")
    except subprocess.CalledProcessError as e:
        print(f"✗ git push failed: {e.stderr}", file=sys.stderr)
        raise


def main() -> int:
    """
    Main entry point: create markdown file and perform git integration.

    Returns:
        0 on success, 1 on failure
    """
    # Determine repository root (script is in specs/253-markdown-file-creation-0600e1/)
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent.parent  # Go up 3 levels

    print(f"Repository root: {repo_root}")
    print()

    try:
        # Phase 1: Create markdown file with proper structure and encoding
        print("Phase 1: Creating markdown file...")
        create_markdown_file(repo_root)
        print()

        # Phase 2: Perform git integration (add, commit, push)
        print("Phase 2: Performing git integration...")
        git_add(repo_root, "test-bvt0ve.md")
        git_commit(
            repo_root,
            "feat(253): create markdown file test-bvt0ve.md with prose content"
        )
        git_push(repo_root)
        print()

        print("✓ Implementation complete!")
        return 0

    except Exception as e:
        print(f"\n✗ Implementation failed: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
