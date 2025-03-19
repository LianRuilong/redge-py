import re

class DocSplitter:
    """
    文档拆分模块：将文档拆分成多个片段，每个片段长度为 512，且每个片段的前 128 个字符与前一个片段的后 128 个字符相同。
    """

    def __init__(self, file_path: str):
        """
        :param file_path: 文档的绝对路径
        """
        self.file_path = file_path

    def read_document(self) -> str:
        """
        读取文档内容。

        :return: 文档内容的字符串
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            return file.read()

    def split_document(self) -> list:
        """
        将文档拆分成多个片段，每个片段长度为 512，且相邻片段前后 128 个字符相同。

        :return: 按顺序排列的片段列表
        """
        content = self.read_document().strip()

        # 定义每个片段的长度
        segment_length = 512
        overlap_length = 128
        content_length = len(content)

        # 如果文档长度小于 segment_length，则直接返回整个文档
        if content_length <= segment_length:
            return [content]

        segments = []
        start_idx = 0

        while start_idx < content_length:
            end_idx = min(start_idx + segment_length, content_length)  # 防止越界
            segment = content[start_idx:end_idx]

            # 处理跨界分割，避免 Unicode 字符被拆分
            if end_idx < content_length:
                while not re.match(r"[\w\u4e00-\u9fff]", content[end_idx - 1]) and end_idx > start_idx:
                    end_idx -= 1
                segment = content[start_idx:end_idx]

            segments.append(segment)

            # 如果已经处理到文档末尾，跳出循环
            if end_idx == content_length:
                break

            # 更新起始位置，重叠 128 个字符
            start_idx = end_idx - overlap_length

        return segments


if __name__ == "__main__":
    # 示例：拆分文档
    file_path = "./sample.txt"  # 请替换为你自己的文档路径
    splitter = DocSplitter(file_path=file_path)
    fragments = splitter.split_document()
    for idx, fragment in enumerate(fragments):
        print(f"Fragment {idx + 1}: {fragment[:50]}...")  # 仅打印每个片段的前50个字符