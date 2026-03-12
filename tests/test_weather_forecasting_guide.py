from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
WEATHER_FORECASTING_FILE = REPO_ROOT / "weather-forecasting-vhiwx5.md"


def test_file_exists():
    assert WEATHER_FORECASTING_FILE.exists(), f"{WEATHER_FORECASTING_FILE} does not exist"


def test_file_has_h1_heading():
    content = WEATHER_FORECASTING_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_mentions_weather_forecasting():
    content = WEATHER_FORECASTING_FILE.read_text(encoding="utf-8")
    assert "weather" in content.lower(), "File does not mention weather"


def test_file_under_80_lines():
    content = WEATHER_FORECASTING_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert len(lines) < 80, f"File has {len(lines)} lines, expected under 80"


def test_file_ends_with_newline():
    raw = WEATHER_FORECASTING_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
