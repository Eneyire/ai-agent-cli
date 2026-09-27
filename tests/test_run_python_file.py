from pathlib import Path

from functions.run_python_file import run_python_file


def test_runs_script_and_passes_arguments(tmp_path: Path) -> None:
    (tmp_path / "script.py").write_text(
        "import sys\nprint('argument:', sys.argv[1])\n", encoding="utf-8"
    )

    result = run_python_file(str(tmp_path), "script.py", ["hello"])

    assert "STDOUT:\nargument: hello" in result


def test_reports_nonzero_exit_status(tmp_path: Path) -> None:
    (tmp_path / "failure.py").write_text("raise SystemExit(3)\n", encoding="utf-8")

    result = run_python_file(str(tmp_path), "failure.py")

    assert "Process exited with code 3" in result


def test_rejects_path_outside_working_directory(tmp_path: Path) -> None:
    result = run_python_file(str(tmp_path), "../outside.py")

    assert result.startswith('Error: Cannot execute "../outside.py"')


def test_rejects_non_python_file(tmp_path: Path) -> None:
    (tmp_path / "notes.txt").write_text("text", encoding="utf-8")

    assert run_python_file(str(tmp_path), "notes.txt") == (
        'Error: "notes.txt" is not a Python file'
    )
