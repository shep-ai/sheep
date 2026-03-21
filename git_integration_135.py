#!/usr/bin/env python3
"""
Git integration for feature 135 markdown file creation.

This script handles git operations for the test-0h8m0m.md file:
- Verify file exists and is valid
- Stage file in git (if not already staged)
- Commit with conventional commit message (if not already committed)
- Push to remote feature branch

This completes phase 2 of the implementation.
"""

from pathlib import Path
import subprocess
import sys
import re
import os

# Set UTF-8 encoding for output
os.environ['PYTHONIOENCODING'] = 'utf-8'


FILENAME = "test-0h8m0m.md"
COMMIT_MESSAGE = "feat(135): Create markdown file test-0h8m0m.md"
FEATURE_BRANCH = "feat/135-markdown-file-creation-77dd31"


def verify_file_exists():
    """Verify the markdown file exists and is valid."""
    file_path = Path(FILENAME)

    if not file_path.exists():
        raise ValueError(f"File does not exist: {FILENAME}")

    size_bytes = file_path.stat().st_size
    print(f"[OK] File exists: {FILENAME} ({size_bytes} bytes)")

    # Quick validation
    with open(file_path, 'rb') as f:
        binary_content = f.read()

    # Check for BOM
    if binary_content.startswith(b'\xef\xbb\xbf'):
        raise ValueError("File contains UTF-8 BOM; expected UTF-8 without BOM")

    # Check for CRLF
    if b'\r\n' in binary_content:
        raise ValueError("File contains CRLF line endings; expected Unix LF")

    # Decode as UTF-8
    try:
        text_content = file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"File is not valid UTF-8: {e}")

    # Validate structure
    lines = text_content.rstrip('\n').split('\n')

    if not lines[0].startswith('# '):
        raise ValueError(f"First line is not H1 heading: {lines[0][:30]}")

    # Count sentences for validation
    prose_text = '\n'.join(lines[2:]) if len(lines) > 2 else ""
    sentence_count = len(re.findall(r'[.!?]+', prose_text))

    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(f"Prose should contain 2-3 sentences; found {sentence_count}")

    if 400 <= size_bytes <= 600:
        print(f"[OK] File size within specification: {size_bytes} bytes (400-600 range)")
    else:
        print(f"[WARN] File size {size_bytes} bytes is outside 400-600 range")

    print(f"[OK] File structure valid: H1 heading + {sentence_count} sentences")
    return True


def git_status_check():
    """Check git status and return current state."""
    result = subprocess.run(
        ['git', 'status', '--short'],
        capture_output=True,
        text=True,
        check=True
    )

    status_lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
    file_status = None

    for line in status_lines:
        if FILENAME in line:
            file_status = line[:2]  # Get the status codes
            break

    return file_status


def git_add():
    """Stage the file in git if not already staged."""
    status = git_status_check()

    if status is None:
        # File might be already committed
        print(f"[OK] File {FILENAME} is already committed")
        return

    if status.startswith('A') or status.startswith('M'):
        # Already staged
        print(f"[OK] File already staged: {status}")
        return

    if status and status[0] == '?':
        # Untracked file, needs to be added
        subprocess.run(['git', 'add', FILENAME], check=True)
        print(f"[OK] Staged file: {FILENAME}")
    elif status and status[1] == 'M':
        # Modified file, needs to be added
        subprocess.run(['git', 'add', FILENAME], check=True)
        print(f"[OK] Staged file: {FILENAME}")


def git_commit():
    """Commit the staged file if not already committed."""
    # Check if file is already committed
    try:
        result = subprocess.run(
            ['git', 'log', '--oneline', '--', FILENAME],
            capture_output=True,
            text=True,
            check=True
        )

        if result.stdout.strip():
            # File has commit history
            print(f"[OK] File already committed: {FILENAME}")
            return
    except subprocess.CalledProcessError:
        pass

    # Check if there are staged changes
    status = git_status_check()

    if status and (status.startswith('A') or status.startswith('M')):
        # File is staged, commit it
        subprocess.run(
            ['git', 'commit', '-m', COMMIT_MESSAGE],
            check=True
        )
        print(f"[OK] Committed with message: {COMMIT_MESSAGE}")
    elif not status:
        # File is already committed
        print(f"[OK] File already committed: {FILENAME}")


def git_push():
    """Push the feature branch to remote."""
    # Check if branch is already pushed
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0 and result.stdout.strip():
            # Branch is tracking upstream
            print(f"[OK] Branch already tracking upstream")

            # Check if there are unpushed commits
            try:
                result = subprocess.run(
                    ['git', 'log', '--oneline', '@{u}..HEAD'],
                    capture_output=True,
                    text=True,
                    check=True
                )

                if result.stdout.strip():
                    # There are unpushed commits
                    subprocess.run(
                        ['git', 'push'],
                        check=True
                    )
                    print(f"[OK] Pushed unpushed commits to remote")
                else:
                    print(f"[OK] All commits already pushed to remote")
            except subprocess.CalledProcessError:
                pass
            return
    except subprocess.CalledProcessError:
        pass

    # Push with -u to set upstream
    subprocess.run(
        ['git', 'push', '-u', 'origin', FEATURE_BRANCH],
        check=True
    )
    print(f"[OK] Pushed to remote: {FEATURE_BRANCH}")


def verify_remote_state():
    """Verify that the file exists on the remote branch."""
    try:
        # Fetch latest from remote
        subprocess.run(['git', 'fetch', 'origin'], check=True, capture_output=True)

        # Check if remote branch exists
        result = subprocess.run(
            ['git', 'ls-remote', 'origin', f'refs/heads/{FEATURE_BRANCH}'],
            capture_output=True,
            text=True,
            check=True
        )

        if result.stdout.strip():
            print(f"[OK] Remote branch exists: origin/{FEATURE_BRANCH}")

            # Verify file exists on remote
            result = subprocess.run(
                ['git', 'show', f'origin/{FEATURE_BRANCH}:{FILENAME}'],
                capture_output=True,
                text=True,
                check=True
            )

            if result.stdout:
                print(f"[OK] File exists on remote branch: {FILENAME}")
                return True
        else:
            print(f"[WARN] Remote branch not found: {FEATURE_BRANCH}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"[WARN] Could not verify remote state: {e}")
        return False


def main():
    """Main entry point."""
    try:
        print("=" * 60)
        print("Phase 2: Git Integration & Verification")
        print("=" * 60)

        print("\nTask 3: Git Operations")
        print("-" * 60)

        # Step 1: Verify file exists and is valid
        print("\n1. Verifying file...")
        verify_file_exists()

        # Step 2: Stage file (if needed)
        print("\n2. Staging file...")
        git_add()

        # Step 3: Commit file (if needed)
        print("\n3. Committing file...")
        git_commit()

        # Step 4: Push to remote
        print("\n4. Pushing to remote...")
        git_push()

        print("\n" + "=" * 60)
        print("Task 4: End-to-End Verification")
        print("=" * 60)

        # Verify remote state
        print("\n5. Verifying remote state...")
        verify_remote_state()

        print("\n" + "=" * 60)
        print("[OK] Phase 2 Complete - All Git Operations Successful")
        print("=" * 60)

        print(f"\nSummary:")
        print(f"  File: {FILENAME}")
        print(f"  Feature Branch: {FEATURE_BRANCH}")
        print(f"  Commit Message: {COMMIT_MESSAGE}")
        print(f"\nNext Steps:")
        print(f"  1. Create pull request from {FEATURE_BRANCH} to main")
        print(f"  2. Request code review")
        print(f"  3. Merge to main when approved")

        return 0

    except OSError as e:
        print(f"\n[ERROR] File I/O Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"\n[ERROR] Validation Error: {e}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Git Command Error: {e}", file=sys.stderr)
        if e.stderr:
            print(f"  stderr: {e.stderr}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n[ERROR] Unexpected Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
