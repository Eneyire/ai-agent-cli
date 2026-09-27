import tempfile
import unittest
from pathlib import Path

from functions.run_python_file import run_python_file


class TestRunPythonFile(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.working_directory = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_runs_script_and_passes_arguments(self) -> None:
        script = self.working_directory / "script.py"
        script.write_text(
            "import sys\nprint('argument:', sys.argv[1])\n", encoding="utf-8"
        )

        result = run_python_file(str(self.working_directory), "script.py", ["hello"])

        self.assertIn("STDOUT:\nargument: hello", result)

    def test_reports_nonzero_exit_status(self) -> None:
        script = self.working_directory / "failure.py"
        script.write_text("raise SystemExit(3)\n", encoding="utf-8")

        result = run_python_file(str(self.working_directory), "failure.py")
        self.assertIn("Process exited with code 3", result)

    def test_rejects_path_outside_working_directory(self) -> None:
        result = run_python_file(str(self.working_directory), "../outside.py")
        self.assertTrue(result.startswith('Error: Cannot execute "../outside.py"'))

    def test_rejects_non_python_file(self) -> None:
        (self.working_directory / "notes.txt").write_text("text", encoding="utf-8")
        result = run_python_file(str(self.working_directory), "notes.txt")
        self.assertEqual(result, 'Error: "notes.txt" is not a Python file')


if __name__ == "__main__":
    unittest.main()
