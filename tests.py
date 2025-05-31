import unittest

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.overwrite_file import overwrite_file
from functions.run_python_file import run_python_file

class TestGetFilesInfo(unittest.TestCase):
    def test_get_files_info_dot(self):
        result = get_files_info("calculator", ".")
        print(f"Result for '.': {result}")
    
    def test_get_files_info_pkg(self):
        result = get_files_info("calculator", "pkg")
        print(f"Result for 'pkg': {result}")
    
    def test_get_files_info_slash_bin(self):
        result = get_files_info("calculator", "/bin")
        print(f"Result for '/bin': {result}")

    def test_get_files_info_double_dot_slash(self):
        result = get_files_info("calculator", "../")
        print(f"Result for '../': {result}")

    def test_get_file_content_truncate(self):
        result = get_file_content("calculator", "lorem.txt")
        print(f"Result for 'lorem.txt': {result}")
        self.assertTrue(len(result) < 15000, "File content should not be empty")

    def test_get_file_content_main_py(self):
        result = get_file_content("calculator", "main.py")
        print(f"Result for 'main.py': {result}")
    
    def test_get_file_content_pkg_calculator_py(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        print(f"Result for 'pkg/calculator.py': {result}")

    def test_get_file_content_slash_bin_cat(self):
        result = get_file_content("calculator", "/bin/cat")
        print(f"Result for '/bin/cat': {result}")

    def test_overwrite_file_lorem_txt(self):
        result = overwrite_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(f"Result for overwriting 'lorem.txt': {result}")
        self.assertIn("Successfully wrote to", result)

    def test_overwrite_file_pkg_slash_morelorem_txt(self):
        result = overwrite_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(f"Result for overwriting 'pkg/morelorem.txt': {result}")
        self.assertIn("Successfully wrote to", result)

    def test_overwrite_file_slash_tmp_temp_txt(self):
        result = overwrite_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(f"Result for overwriting '/tmp/temp.txt': {result}")
        self.assertIn("Error: Cannot write to", result)

    def test_run_python_file_main_py(self):
        result = run_python_file("calculator", "main.py")
        print(f"Result for running 'main.py': {result}")
        

    def test_run_python_file_tests_py(self):
        result = run_python_file("calculator", "tests.py")
        print(f"Result for running 'tests.py': {result}")
        
    
    def test_run_python_file_dot_dot_slash_main_py(self):
        result = run_python_file("calculator", "../main.py")
        print(f"Result for running '../main.py': {result}")


    def test_run_python_file_nonexistsent_py(self):
        result = run_python_file("calculator", "nonexistent.py")
        print(f"Result for running 'nonexistent.py': {result}")

    def test_run_python_file_nonexistsent_py(self):
        result = run_python_file("calculator", "empty.py")
        print(f"Result for running 'empty.py': {result}")
        

if __name__ == "__main__":
    unittest.main()