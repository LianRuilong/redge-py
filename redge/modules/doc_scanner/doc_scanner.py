import os
from pathlib import Path
from typing import List, Dict

class DocScanner:
    """
    文档扫描模块：每次调用时扫描指定路径，返回文件信息。
    """

    def __init__(self, directory: str):
        """
        :param directory: 需要扫描的目录路径
        """
        self.directory = Path(directory)

    def scan_directory(self) -> List[Dict[str, str]]:
        """
        扫描目录，返回所有文件信息。

        :return: 文件信息列表，每个文件包含 path, size, format
        """
        if not self.directory.exists():
            raise FileNotFoundError(f"路径 {self.directory} 不存在")

        file_list = []
        for file in self.directory.rglob("*"):  # 遍历所有子目录
            if file.is_file():
                file_info = {
                    "path": str(file),
                    "size": file.stat().st_size,
                    "format": file.suffix
                }
                file_list.append(file_info)

        return file_list

if __name__ == "__main__":
    # 示例：扫描当前目录
    scanner = DocScanner(directory="./test_dir")
    files = scanner.scan_directory()
    for file in files:
        print(file)