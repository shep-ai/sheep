#!/usr/bin/env python3
"""
Feature 221: Create markdown file test-i1otr7.md with title and prose content.
Uses pathlib for file I/O and subprocess for git integration.
"""

import sys
import subprocess
from pathlib import Path

# Constants
FILENAME = "test-i1otr7.md"
TITLE = "The Importance of Consistent Testing"
PROSE = "Consistent testing practices form the foundation of reliable software systems. When developers write tests alongside their code, they catch bugs earlier and build stronger solutions. This disciplined approach to testing creates codebases that teams can confidently maintain and extend over time."

def create_file():
    """Create markdown file with proper UTF-8 encoding and Unix LF line endings."""
    file_path = Path(FILENAME)

    # Construct markdown content: H1 heading + blank line + prose + newline
    content = f"# {TITLE}\n\n{PROSE}\n"

    try:
        # Check if file exists and has correct content
        if file_path.exists():
            existing_content = file_path.read_text(encoding="utf-8")
            if existing_content == content:
                print(f"[OK] File already exists with correct content: {FILENAME}")
                print(f"  - Size: {len(content)} bytes")
                print(f"  - Encoding: UTF-8")
                print(f"  - Line endings: LF (Unix)")
                return True
            else:
                raise FileExistsError(f"File {FILENAME} exists but has different content")
        
        # Write with explicit UTF-8 encoding and Unix line endings
        file_path.write_text(content, encoding="utf-8", newline="\n")
        print(f"[OK] Created file: {FILENAME}")
        print(f"  - Size: {len(content)} bytes")
        print(f"  - Encoding: UTF-8 (no BOM)")
        print(f"  - Line endings: LF (Unix)")
        return True
    except OSError as e:
        raise OSError(f"Failed to create file: {e}")

def git_add():
    """Stage file in git."""
    try:
        subprocess.run(["git", "add", FILENAME], check=True)
        print(f"[OK] Staged file: {FILENAME}")
        return True
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(e.returncode, e.cmd, e.output, e.stderr)

def git_commit():
    """Create commit with conventional message."""
    commit_message = f"feat(221): Create markdown file {FILENAME}"
    try:
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print(f"[OK] Created commit: {commit_message}")
        return True
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(e.returncode, e.cmd, e.output, e.stderr)

def git_push():
    """Push commit to feature branch."""
    try:
        subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)
        print(f"[OK] Pushed to feature branch")
        return True
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(e.returncode, e.cmd, e.output, e.stderr)

def main():
    """Execute complete workflow: create file, stage, commit, push."""
    try:
        # Task 1: Create file
        create_file()

        # Task 2: Git workflow
        git_add()
        git_commit()
        git_push()

        print("\n[OK] Workflow completed successfully")
        return 0

    except FileExistsError as e:
        print(f"[ERROR] File error: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"[ERROR] I/O error: {e}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git command failed: {e.cmd}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
