import tempfile
import unittest
from pathlib import Path

from config import MAX_CHARS
from functions.get_file_content import get_file_content


class TestGetFileContent(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.working_directory = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_reads_file_contents(self) -> None:
        (self.working_directory / "sample.txt").write_text("hello", encoding="utf-8")
        self.assertEqual(
            get_file_content(str(self.working_directory), "sample.txt"), "hello"
        )

    def test_truncates_large_file_and_marks_result(self) -> None:
        (self.working_directory / "large.txt").write_text(
            "x" * (MAX_CHARS + 1), encoding="utf-8"
        )

        result = get_file_content(str(self.working_directory), "large.txt")

        self.assertEqual(
            len(result),
            MAX_CHARS
            + len(f'[...File "large.txt" truncated at {MAX_CHARS} characters]'),
        )
        self.assertTrue(
            result.endswith(
                f'[...File "large.txt" truncated at {MAX_CHARS} characters]'
            )
        )

    def test_rejects_path_outside_working_directory(self) -> None:
        result = get_file_content(str(self.working_directory), "../secret.txt")
        self.assertTrue(result.startswith('Error: Cannot read "../secret.txt"'))

    def test_reports_missing_file(self) -> None:
        result = get_file_content(str(self.working_directory), "missing.txt")
        self.assertEqual(
            result,
            'Error: File not found or is not a regular file: "missing.txt"',
        )


if __name__ == "__main__":
    unittest.main()
