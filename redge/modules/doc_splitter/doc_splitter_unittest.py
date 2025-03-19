
import unittest
from pathlib import Path
from redge.modules.doc_splitter.doc_splitter import DocSplitter

TEST_DIR = Path("./test_split")
TEST_FILE = TEST_DIR / "test.txt"

class TestDocSplitter(unittest.TestCase):
    """测试文档拆分模块"""

    @classmethod
    def setUpClass(cls):
        """创建测试文件"""
        TEST_DIR.mkdir(exist_ok=True)
        with open(TEST_FILE, "w", encoding="utf-8") as f:
            f.write("这是一段测试文本。" * 100)  # 生成 5000 多个字符

    @classmethod
    def tearDownClass(cls):
        """清理测试文件"""
        TEST_FILE.unlink()
        TEST_DIR.rmdir()

    def test_split_document(self):
        """测试文档拆分"""
        splitter = DocSplitter(file_path=str(TEST_FILE))
        fragments = splitter.split_document()

        self.assertGreater(len(fragments), 1)  # 确保拆分成功
        self.assertTrue(fragments[1].startswith(fragments[0][-128:]))  # 验证 128 字符重叠

    def test_single_fragment(self):
        """测试小于 512 个字符的文档"""
        short_text_file = TEST_DIR / "short.txt"
        with open(short_text_file, "w", encoding="utf-8") as f:
            f.write("短文本")

        splitter = DocSplitter(file_path=str(short_text_file))
        fragments = splitter.split_document()
        self.assertEqual(len(fragments), 1)

        short_text_file.unlink()

if __name__ == "__main__":
    unittest.main()