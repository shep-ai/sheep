from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RANDOM_JOKE_FILE = REPO_ROOT / "RANDOM_JOKE.md"


def test_file_exists():
    assert RANDOM_JOKE_FILE.exists(), f"{RANDOM_JOKE_FILE} does not exist"


def test_file_has_h1_heading():
    content = RANDOM_JOKE_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_contains_question_and_answer():
    content = RANDOM_JOKE_FILE.read_text(encoding="utf-8")
    assert "**Q:**" in content, "File does not contain a question"
    assert "**A:**" in content, "File does not contain an answer"


def test_file_is_not_empty():
    content = RANDOM_JOKE_FILE.read_text(encoding="utf-8").strip()
    assert len(content) > 0, "File is empty"
