import tempfile
import unittest
from pathlib import Path

from functions.write_file import write_file


class TestWriteFile(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.working_directory = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_writes_file_and_creates_parent_directories(self) -> None:
        result = write_file(
            str(self.working_directory), "nested/new.txt", "hello world"
        )

        self.assertEqual(
            (self.working_directory / "nested" / "new.txt").read_text(encoding="utf-8"),
            "hello world",
        )
        self.assertEqual(
            result, 'Successfully wrote to "nested/new.txt" (11 characters written)'
        )

    def test_rejects_path_outside_working_directory(self) -> None:
        result = write_file(str(self.working_directory), "../outside.txt", "nope")
        self.assertTrue(result.startswith('Error: Cannot write to "../outside.txt"'))

    def test_rejects_directory_target(self) -> None:
        (self.working_directory / "existing-dir").mkdir()
        result = write_file(str(self.working_directory), "existing-dir", "nope")
        self.assertEqual(
            result, 'Error: Cannot write to "existing-dir" as it is a directory'
        )


if __name__ == "__main__":
    unittest.main()
