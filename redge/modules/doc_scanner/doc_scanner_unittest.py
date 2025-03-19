import unittest
from pathlib import Path
from redge.modules.doc_scanner.doc_scanner import DocScanner

TEST_DIR = Path("./test_scan")

class TestDocScanner(unittest.TestCase):
    """测试文档扫描模块"""

    @classmethod
    def setUpClass(cls):
        """创建测试目录"""
        TEST_DIR.mkdir(exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        """清理测试目录"""
        for file in TEST_DIR.iterdir():
            file.unlink()
        TEST_DIR.rmdir()

    def test_scan_directory(self):
        """测试主动扫描"""
        test_file = TEST_DIR / "test.txt"
        test_file.write_text("Hello World!")

        scanner = DocScanner(directory=str(TEST_DIR))
        result = scanner.scan_directory()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["path"], str(test_file))
        self.assertEqual(result[0]["size"], len("Hello World!"))
        self.assertEqual(result[0]["format"], ".txt")

if __name__ == "__main__":
    unittest.main()