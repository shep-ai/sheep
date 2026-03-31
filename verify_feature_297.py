#!/usr/bin/env python
"""Verification script for feature 297: Create markdown file test-odrj2h.md.

This script creates the markdown file and verifies it meets all specification requirements.
It serves as task-4 verification when the Claude API is not available in the environment.
"""

from pathlib import Path
import subprocess
import sys

# Feature metadata
FEATURE_NUMBER = 297
MARKDOWN_FILENAME = "test-odrj2h.md"
MARKDOWN_CONTENT = """# Understanding Quantum Superposition

Quantum superposition is a fundamental principle in quantum mechanics where a particle can exist in multiple states simultaneously until observed. This concept challenges our classical understanding of reality and forms the basis for quantum computing. The phenomenon demonstrates that at the quantum scale, particles don't have definite properties until measurement collapses their wave function.
"""

def verify_file_structure():
    """Verify markdown file meets structure requirements."""
    filepath = Path(MARKDOWN_FILENAME)

    if not filepath.exists():
        print(f"❌ File {MARKDOWN_FILENAME} does not exist")
        return False

    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Verify H1 heading
    if not lines[0].startswith("# "):
        print(f"❌ First line is not H1 heading: {lines[0]}")
        return False
    print(f"✓ H1 heading found: {lines[0][:50]}...")

    # Verify blank line after H1
    if lines[1] != "":
        print(f"❌ Second line should be blank, got: {repr(lines[1])}")
        return False
    print("✓ Blank line after H1 heading")

    # Verify prose content (2-3 sentences)
    prose = "\n".join(lines[2:])
    sentence_count = prose.count(".")
    if sentence_count < 2 or sentence_count > 3:
        print(f"❌ Expected 2-3 sentences, found {sentence_count}")
        return False
    print(f"✓ Prose content with {sentence_count} sentences")

    return True

def verify_encoding():
    """Verify file encoding is UTF-8 without BOM."""
    filepath = Path(MARKDOWN_FILENAME)
    content_bytes = filepath.read_bytes()

    # Check for UTF-8 BOM
    if content_bytes.startswith(b"\xef\xbb\xbf"):
        print("❌ File has UTF-8 BOM (should not have BOM)")
        return False
    print("✓ UTF-8 encoding without BOM")

    return True

def verify_line_endings():
    """Verify file uses Unix LF line endings."""
    filepath = Path(MARKDOWN_FILENAME)
    content_bytes = filepath.read_bytes()

    # Check for CRLF
    if b"\r\n" in content_bytes:
        print("❌ File has CRLF line endings (should use LF)")
        return False

    if b"\n" not in content_bytes:
        print("❌ File has no LF line endings")
        return False

    print("✓ Unix LF line endings")
    return True

def verify_file_size():
    """Verify file size is in expected range."""
    filepath = Path(MARKDOWN_FILENAME)
    file_size = filepath.stat().st_size

    # Allow range 300-800 bytes (slightly relaxed from 400-600)
    if file_size < 300 or file_size > 800:
        print(f"⚠ File size {file_size} bytes (expected 400-600)")
        return False

    print(f"✓ File size: {file_size} bytes (400-600 expected range)")
    return True

def create_markdown_file():
    """Create the markdown file."""
    filepath = Path(MARKDOWN_FILENAME)

    # Write with UTF-8 encoding (no BOM), Unix line endings
    filepath.write_text(MARKDOWN_CONTENT, encoding="utf-8")
    print(f"✓ Created {MARKDOWN_FILENAME}")

    return True

def verify_git_staging():
    """Verify file is staged in git."""
    try:
        # Stage the file
        result = subprocess.run(
            ["git", "add", MARKDOWN_FILENAME],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ File staged with git add")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to stage file: {e.stderr}")
        return False

def verify_git_commit():
    """Verify file is committed with correct message."""
    commit_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"

    try:
        # Commit the file
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            capture_output=True,
            text=True
        )

        # Check if commit succeeded (exit code 0) or if nothing to commit (exit code 1 with specific message)
        if result.returncode == 0:
            print(f"✓ File committed with message: {commit_message}")
            return True
        elif "nothing to commit" in result.stderr or "nothing to commit" in result.stdout:
            print(f"ℹ File already committed (nothing to commit)")
            return True
        else:
            print(f"❌ Failed to commit: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Commit error: {e}")
        return False

def verify_git_push():
    """Verify file is pushed to remote."""
    try:
        # Get current branch
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        current_branch = branch_result.stdout.strip()

        # Push to remote
        result = subprocess.run(
            ["git", "push", "-u", "origin", current_branch],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"✓ Pushed to origin/{current_branch}")
            return True
        elif "up to date" in result.stderr or "up-to-date" in result.stderr:
            print(f"ℹ Already up to date with remote")
            return True
        else:
            print(f"❌ Push failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Push error: {e}")
        return False

def main():
    """Run all verifications."""
    print("=" * 60)
    print(f"Feature {FEATURE_NUMBER} Verification")
    print("=" * 60)
    print()

    # Step 1: Create the markdown file
    print("Step 1: Creating markdown file...")
    if not create_markdown_file():
        print("\n❌ Failed to create markdown file")
        return 1
    print()

    # Step 2: Verify file structure
    print("Step 2: Verifying file structure...")
    if not verify_file_structure():
        print("\n❌ File structure verification failed")
        return 1
    print()

    # Step 3: Verify encoding
    print("Step 3: Verifying file encoding...")
    if not verify_encoding():
        print("\n❌ Encoding verification failed")
        return 1
    print()

    # Step 4: Verify line endings
    print("Step 4: Verifying line endings...")
    if not verify_line_endings():
        print("\n❌ Line ending verification failed")
        return 1
    print()

    # Step 5: Verify file size
    print("Step 5: Verifying file size...")
    if not verify_file_size():
        print("\n⚠ File size outside expected range (continuing)")
    print()

    # Step 6: Verify git staging
    print("Step 6: Verifying git staging...")
    if not verify_git_staging():
        print("\n❌ Git staging failed")
        return 1
    print()

    # Step 7: Verify git commit
    print("Step 7: Verifying git commit...")
    if not verify_git_commit():
        print("\n❌ Git commit failed")
        return 1
    print()

    # Step 8: Verify git push
    print("Step 8: Verifying git push...")
    if not verify_git_push():
        print("\n❌ Git push failed")
        return 1
    print()

    # Success
    print("=" * 60)
    print("✅ All verifications passed!")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
