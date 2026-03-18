"""File creation implementation for feature 089.

Creates a markdown file (test-objvv0.md) at the repository root with proper
UTF-8 encoding, Unix line endings, and validated file size.
"""

import os
from pathlib import Path


def create_file() -> None:
    """Create test-objvv0.md with markdown H1 title and prose content.

    File specifications:
    - Location: repository root (test-objvv0.md)
    - Encoding: UTF-8 without BOM
    - Line endings: Unix LF (not CRLF)
    - Content: H1 heading + blank line + 2-3 sentences
    - File size: 320-600 bytes

    Raises:
        RuntimeError: If file size is outside acceptable range
    """
    title = "# The Value of Learning from Experience"
    prose = (
        "Every challenge we face becomes an opportunity to develop deeper understanding "
        "and resilience that shapes our character. Experience teaches lessons that no textbook "
        "can fully convey, offering wisdom through lived encounters. By reflecting on what we "
        "learn from both successes and failures, we grow stronger and more equipped to handle "
        "future obstacles with grace and confidence."
    )

    # Combine content: title + blank line + prose + final newline
    content = f"{title}\n\n{prose}\n"

    # Write file with explicit UTF-8 encoding and Unix line endings
    file_path = Path("test-objvv0.md")
    file_path.write_text(content, encoding='utf-8', newline='\n')

    # Validate file size is within acceptable range
    file_size = os.path.getsize(file_path)
    if not (320 <= file_size <= 600):
        raise RuntimeError(
            f"File size {file_size} bytes is outside acceptable range [320, 600]"
        )


if __name__ == "__main__":
    create_file()
    print("✓ File test-objvv0.md created successfully")
