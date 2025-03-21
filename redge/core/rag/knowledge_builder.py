import sqlite3
import hnswlib
import numpy as np
import os
from pathlib import Path
from redge.modules.doc_scanner.doc_scanner import DocScanner
from redge.modules.doc_splitter.doc_splitter import DocSplitter
from redge.modules.text_embedding.text_embedding import TextEmbedding

class KnowledgeBuilder:
    """
    知识构建模块：
    1. 扫描指定目录，获取所有文档信息
    2. 拆分文档成片段
    3. 计算文本向量
    4. 存储文本片段到 SQLite，存储向量到 HNSWLib
    """

    def __init__(self, database_path="knowledge.db", hnsw_path="knowledge.hnsw", dim=512):
        """
        初始化 SQLite 数据库和 HNSWLib 向量索引
        """
        self.database_path = database_path
        self.hnsw_path = hnsw_path
        self.dim = dim  # 向量维度，需与 text_embedding 输出向量一致

        # 初始化 SQLite
        self.conn = sqlite3.connect(self.database_path)
        self.cursor = self.conn.cursor()
        self._initialize_database()

        # 初始化 HNSWLib
        self.hnsw_index = hnswlib.Index(space='cosine', dim=self.dim)
        self._initialize_hnsw()

        self.embedding_model = TextEmbedding()

    def _initialize_database(self):
        """初始化 SQLite 数据库表结构"""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS fragments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_name TEXT NOT NULL
        )
        """)
        self.conn.commit()

    def _initialize_hnsw(self):
        """初始化 HNSWLib 向量索引"""
        try:
            self.hnsw_index.load_index(self.hnsw_path)  # 尝试加载已有索引
            print("HNSWLib 索引已加载")
        except Exception:
            print("初始化新的 HNSWLib 索引")
            self.hnsw_index.init_index(max_elements=100000, ef_construction=200, M=16)
            self.hnsw_index.set_ef(50)

    def build_knowledge(self, directory: str):
        """
        扫描指定目录，构建知识库
        :param directory: 要扫描的文档目录路径
        """
        scanner = DocScanner(directory)
        files = scanner.scan_directory()

        for file_info in files:
            file_path = file_info["path"]
            file_name = Path(file_path).name

            print(f"Processing: {file_name}")
            splitter = DocSplitter(file_path)
            fragments = splitter.split_document()

            for fragment in fragments:
                fragment_id = self._insert_fragment(fragment, file_path, file_name)
                vector = self.embedding_model.encode([fragment])[0]

                # 存储向量到 HNSWLib
                self.hnsw_index.add_items(np.array([vector]), np.array([fragment_id]))

        # 保存 HNSWLib 索引
        self.hnsw_index.save_index(self.hnsw_path)
        print("知识构建完成！")

    def rebuild_knowledge(self, directory: str):
        """
        删除数据库和索引文件后，重新构建知识库
        :param directory: 需要重新扫描的目录
        """
        print("正在删除旧的知识库...")
        if os.path.exists(self.database_path):
            os.remove(self.database_path)
            print(f"已删除数据库文件: {self.database_path}")

        if os.path.exists(self.hnsw_path):
            os.remove(self.hnsw_path)
            print(f"已删除 HNSWLib 索引文件: {self.hnsw_path}")

        # 重新初始化数据库和索引
        self.conn = sqlite3.connect(self.database_path)
        self.cursor = self.conn.cursor()
        self._initialize_database()

        self.hnsw_index = hnswlib.Index(space='cosine', dim=self.dim)
        self._initialize_hnsw()

        print("重新构建知识库...")
        self.build_knowledge(directory)
        print("知识库重建完成！")

    def _insert_fragment(self, content: str, file_path: str, file_name: str) -> int:
        """存储文本片段到 SQLite"""
        self.cursor.execute(
            "INSERT INTO fragments (content, file_path, file_name) VALUES (?, ?, ?)",
            (content, file_path, file_name),
        )
        self.conn.commit()
        return self.cursor.lastrowid

if __name__ == "__main__":
    knowledge_builder = KnowledgeBuilder()
    knowledge_builder.rebuild_knowledge("/Users/lianruilong/Documents/work/mywork/redge-py/test_docs")  # 替换为你的文档目录