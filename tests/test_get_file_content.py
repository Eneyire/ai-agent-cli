from pathlib import Path

from config import MAX_CHARS
from functions.get_file_content import get_file_content


def test_reads_file_contents(tmp_path: Path) -> None:
    (tmp_path / "sample.txt").write_text("hello", encoding="utf-8")

    assert get_file_content(str(tmp_path), "sample.txt") == "hello"


def test_truncates_large_file_and_marks_result(tmp_path: Path) -> None:
    (tmp_path / "large.txt").write_text("x" * (MAX_CHARS + 1), encoding="utf-8")

    result = get_file_content(str(tmp_path), "large.txt")
    marker = f'[...File "large.txt" truncated at {MAX_CHARS} characters]'

    assert len(result) == MAX_CHARS + len(marker)
    assert result.endswith(marker)


def test_rejects_path_outside_working_directory(tmp_path: Path) -> None:
    result = get_file_content(str(tmp_path), "../secret.txt")

    assert result.startswith('Error: Cannot read "../secret.txt"')


def test_reports_missing_file(tmp_path: Path) -> None:
    result = get_file_content(str(tmp_path), "missing.txt")

    assert result == 'Error: File not found or is not a regular file: "missing.txt"'
