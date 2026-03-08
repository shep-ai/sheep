from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
JOKE_FILE = REPO_ROOT / "JOKE_4CYDBED8.md"


def test_file_exists():
    assert JOKE_FILE.exists(), f"{JOKE_FILE} does not exist"


def test_file_is_markdown():
    assert JOKE_FILE.suffix == ".md", f"Expected .md suffix, got {JOKE_FILE.suffix}"


def test_file_has_joke_heading():
    content = JOKE_FILE.read_text(encoding="utf-8")
    assert "# Joke" in content, "File should contain a '# Joke' heading"


def test_file_has_question_and_answer():
    content = JOKE_FILE.read_text(encoding="utf-8")
    assert "**Q:**" in content, "File should contain a question"
    assert "**A:**" in content, "File should contain an answer"


def test_file_is_not_empty():
    content = JOKE_FILE.read_text(encoding="utf-8")
    assert len(content.strip()) > 0, "File should not be empty"


def test_file_ends_with_newline():
    raw = JOKE_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File should end with a newline"
