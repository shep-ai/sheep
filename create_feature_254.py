#!/usr/bin/env python3
"""Script to create markdown file for feature 254: test-llstaq.md with title and prose content."""

import subprocess
from pathlib import Path

# Git commit message (exact per specification)
COMMIT_MESSAGE = "feat(254): Create markdown file test-llstaq.md with prose content"


def main():
    """Create markdown file test-llstaq.md with H1 heading and 2-3 sentences of prose."""
    print("Feature 254: Creating markdown file test-llstaq.md")
    print("=" * 60)

    # Define the markdown content with H1 heading and prose
    # Topic chosen by implementer: The Art of Bread Baking
    # Prose: 3 sentences about bread baking (implementer-written)
    content = "# The Art of Bread Baking\n\nBread baking is a timeless craft that combines simple ingredients with precise technique to create wholesome, nourishing food. The process of mixing flour, water, salt, and yeast transforms these humble components into complex flavors and beautiful textures through fermentation and heat. Mastering bread baking requires patience, practice, and a deep understanding of how temperature and time interact with chemistry.\n"

    # Task 1: Create the markdown file
    print("\nTask 1: Creating markdown file...")
    try:
        # Use pathlib.Path with explicit UTF-8 encoding and LF line endings
        # This ensures proper file properties per NFR-1 and NFR-2
        filepath = Path.cwd() / "test-llstaq.md"
        filepath.write_text(content, encoding="utf-8", newline="\n")

        # Verify file was created
        if not filepath.exists():
            print("[FAIL] File was not created!")
            return False

        file_size = filepath.stat().st_size
        print(f"[OK] File created: {filepath}")
        print(f"[OK] File size: {file_size} bytes")

    except Exception as e:
        print(f"[FAIL] Failed to create file: {e}")
        return False

    # Task 2: Validate file encoding and line endings
    print("\nTask 2: Validating file encoding and line endings...")
    try:
        # Read file as binary to check encoding and line endings
        binary_content = filepath.read_bytes()

        # Check for UTF-8 BOM (should not be present)
        if binary_content.startswith(b"\xef\xbb\xbf"):
            print("[FAIL] File has UTF-8 BOM (should not be present)")
            return False

        # Check for CRLF line endings (should use LF instead)
        if b"\r\n" in binary_content:
            print("[FAIL] File uses CRLF line endings (should use LF)")
            return False

        # Verify file is valid UTF-8
        try:
            text_content = binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            print(f"[FAIL] File is not valid UTF-8: {e}")
            return False

        print("[OK] UTF-8 encoding without BOM verified")
        print("[OK] LF line endings (no CRLF) verified")

    except Exception as e:
        print(f"[FAIL] Encoding/line ending validation failed: {e}")
        return False

    # Task 3: Validate markdown structure
    print("\nTask 3: Validating markdown structure...")
    try:
        # Verify structure: H1 heading + blank line + 2-3 sentences
        lines = text_content.split("\n")

        # Check for H1 heading at start
        if not lines[0].startswith("# "):
            print("[FAIL] First line must be H1 heading (# )")
            return False

        # Check for blank line separator
        if len(lines) < 2 or lines[1] != "":
            print("[FAIL] Second line must be blank (separator after heading)")
            return False

        # Extract and validate prose content
        prose_lines = lines[2:]
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        if not prose_lines:
            print("[FAIL] No prose content found after heading")
            return False

        prose_content = "\n".join(prose_lines).strip()

        # Count sentences (by counting periods)
        sentence_count = prose_content.count(".")
        if sentence_count < 2 or sentence_count > 3:
            print(f"[FAIL] Content must have 2-3 sentences, found {sentence_count}")
            return False

        # Check for trailing newline
        if not text_content.endswith("\n"):
            print("[FAIL] File must end with trailing newline")
            return False

        print("[OK] H1 heading present")
        print("[OK] Blank line separator verified")
        print(f"[OK] Prose content: {sentence_count} sentences")
        print("[OK] Trailing newline verified")

    except Exception as e:
        print(f"[FAIL] Markdown structure validation failed: {e}")
        return False

    # Task 4: Git Integration - add, commit, push
    print("\nTask 4: Git integration...")
    try:
        # Stage the file
        print("  Running: git add test-llstaq.md")
        result = subprocess.run(
            ["git", "add", "test-llstaq.md"],
            cwd=Path.cwd(),
            capture_output=True,
            text=True,
            check=True
        )
        print("[OK] File staged in git")

        # Commit with conventional commit message
        print(f"  Running: git commit -m '{COMMIT_MESSAGE}'")
        result = subprocess.run(
            ["git", "commit", "-m", COMMIT_MESSAGE],
            cwd=Path.cwd(),
            capture_output=True,
            text=True,
            check=True
        )
        print("[OK] File committed with exact message")

        # Push to remote origin on feature branch
        # Get current branch name to ensure we push to the right branch
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=Path.cwd(),
            capture_output=True,
            text=True,
            check=True
        )
        current_branch = branch_result.stdout.strip()
        print(f"  Current branch: {current_branch}")
        print(f"  Running: git push origin {current_branch}")

        result = subprocess.run(
            ["git", "push", "origin", current_branch],
            cwd=Path.cwd(),
            capture_output=True,
            text=True,
            check=True
        )
        print("[OK] Changes pushed to remote origin")

    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Git command failed: {e.cmd}")
        if e.stderr:
            print(f"       Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"[FAIL] Git integration failed: {e}")
        return False

    # Summary
    print("\n" + "=" * 60)
    print("[SUCCESS] Feature 254 complete!")
    print(f"  File: test-llstaq.md")
    print(f"  Size: {file_size} bytes")
    print(f"  Sentences: {sentence_count}")
    print("  Encoding: UTF-8 (no BOM)")
    print("  Line endings: LF")
    print("  Git status: Committed and pushed to remote")
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
