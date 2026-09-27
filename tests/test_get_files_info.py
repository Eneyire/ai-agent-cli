from pathlib import Path

from functions.get_files_info import get_files_info


def test_lists_files_and_directories(tmp_path: Path) -> None:
    (tmp_path / "sample.txt").write_text("hello", encoding="utf-8")
    (tmp_path / "subdir").mkdir()

    result = get_files_info(str(tmp_path))

    assert "- sample.txt: file_size=5 bytes, is_dir=False" in result
    assert "- subdir: file_size=" in result
    assert "is_dir=True" in result


def test_lists_requested_empty_subdirectory(tmp_path: Path) -> None:
    (tmp_path / "subdir").mkdir()

    assert get_files_info(str(tmp_path), "subdir") == ""


def test_rejects_path_outside_working_directory(tmp_path: Path) -> None:
    result = get_files_info(str(tmp_path), "../")

    assert result.startswith('Error: Cannot list "../"')


def test_rejects_file_instead_of_directory(tmp_path: Path) -> None:
    (tmp_path / "sample.txt").write_text("hello", encoding="utf-8")

    assert get_files_info(str(tmp_path), "sample.txt") == (
        'Error: "sample.txt" is not a directory'
    )
