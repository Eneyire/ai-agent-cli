from pathlib import Path

from functions.write_file import write_file


def test_writes_file_and_creates_parent_directories(tmp_path: Path) -> None:
    result = write_file(str(tmp_path), "nested/new.txt", "hello world")

    assert (tmp_path / "nested" / "new.txt").read_text(
        encoding="utf-8"
    ) == "hello world"
    assert result == 'Successfully wrote to "nested/new.txt" (11 characters written)'


def test_rejects_path_outside_working_directory(tmp_path: Path) -> None:
    result = write_file(str(tmp_path), "../outside.txt", "nope")

    assert result.startswith('Error: Cannot write to "../outside.txt"')


def test_rejects_directory_target(tmp_path: Path) -> None:
    (tmp_path / "existing-dir").mkdir()

    assert write_file(str(tmp_path), "existing-dir", "nope") == (
        'Error: Cannot write to "existing-dir" as it is a directory'
    )
