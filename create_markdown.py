"""Create markdown file test-aibs55.md (feature 123)."""
from pathlib import Path


# Task 1: Define markdown content with proper structure
# H1 heading + blank line + 2-3 sentences of prose
CONTENT = """# The Art of Storytelling

Stories connect us across time and distance, allowing people from different cultures and eras to understand each other's experiences and emotions. The best stories don't just inform; they transform our perspective and challenge our assumptions about the world. Throughout history, the ability to tell compelling stories has shaped civilizations and changed the course of human events."""


def write_markdown_file(filename: str = "test-aibs55.md") -> None:
    """
    Task 2: Write markdown file with proper encoding and line endings.
    
    Creates the markdown file with:
    - UTF-8 encoding without BOM
    - Unix LF line endings (not CRLF)
    - Content from CONTENT constant
    
    Args:
        filename: Name of the file to create (default: test-aibs55.md)
        
    Raises:
        FileNotFoundError: If directory doesn't exist or no write access
        PermissionError: If insufficient permissions to write file
        ValueError: If content validation fails
    """
    try:
        # Write file with explicit UTF-8 encoding and Unix LF line endings
        file_path = Path(filename)
        file_path.write_text(CONTENT, encoding="utf-8", newline="\n")
        
        # Validate file meets all requirements
        _validate_file(file_path)
        
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Cannot write to {filename}: directory not found or no write access. "
            f"Ensure you're in the repository root directory."
        ) from e
    except PermissionError as e:
        raise PermissionError(
            f"Cannot write to {filename}: insufficient permissions. "
            f"Check that you have write access to the repository root."
        ) from e


def _validate_file(file_path: Path) -> None:
    """
    Validate that the created file meets all requirements.
    
    Args:
        file_path: Path to the file to validate
        
    Raises:
        ValueError: If any validation check fails
    """
    # Check file exists
    if not file_path.exists():
        raise ValueError(f"File {file_path} was not created successfully")
    
    # Check file size (300-500 bytes)
    file_size = file_path.stat().st_size
    if not (300 <= file_size <= 500):
        raise ValueError(
            f"File size {file_size} bytes is outside required range 300-500 bytes. "
            f"Adjust prose content length."
        )
    
    # Check content is readable as UTF-8
    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(
            f"File is not valid UTF-8 encoding: {e}"
        ) from e
    
    # Validate content structure
    if not content.startswith("# "):
        raise ValueError("Content must start with H1 heading (# )")
    
    lines = content.split("\n")
    if len(lines) < 3:
        raise ValueError("Content must have heading, blank line, and prose")
    
    if lines[1] != "":
        raise ValueError("Second line must be blank (after H1 heading)")
    
    # Check for prose content
    prose_text = "\n".join(lines[2:]).strip()
    if not prose_text:
        raise ValueError("Content must include prose after blank line")
    
    # Count sentences (split by periods)
    sentences = [s.strip() for s in prose_text.split(".") if s.strip()]
    if not (2 <= len(sentences) <= 3):
        raise ValueError(
            f"Content must have 2-3 sentences, found {len(sentences)}. "
            f"Adjust prose content."
        )
    
    # Check for CRLF line endings (Windows)
    content_binary = file_path.read_bytes()
    if b"\r\n" in content_binary:
        raise ValueError("File contains CRLF (Windows) line endings. Must use Unix LF.")


if __name__ == "__main__":
    write_markdown_file()
    print("✓ Created test-aibs55.md successfully")
