import tempfile
import unittest
from pathlib import Path

from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.working_directory = Path(self.temp_dir.name)
        (self.working_directory / "sample.txt").write_text("hello", encoding="utf-8")
        (self.working_directory / "subdir").mkdir()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_lists_files_and_directories(self) -> None:
        result = get_files_info(str(self.working_directory))

        self.assertIn("- sample.txt: file_size=5 bytes, is_dir=False", result)
        self.assertIn("- subdir: file_size=", result)
        self.assertIn("is_dir=True", result)

    def test_lists_requested_subdirectory(self) -> None:
        result = get_files_info(str(self.working_directory), "subdir")
        self.assertEqual(result, "")

    def test_rejects_path_outside_working_directory(self) -> None:
        result = get_files_info(str(self.working_directory), "../")
        self.assertTrue(result.startswith('Error: Cannot list "../"'))

    def test_rejects_file_instead_of_directory(self) -> None:
        result = get_files_info(str(self.working_directory), "sample.txt")
        self.assertEqual(result, 'Error: "sample.txt" is not a directory')


if __name__ == "__main__":
    unittest.main()
