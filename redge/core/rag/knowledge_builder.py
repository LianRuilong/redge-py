import sqlite3
import sqlite_vec
import json
import os
from pathlib import Path
from redge.modules.doc_scanner.doc_scanner import DocScanner
from redge.modules.doc_splitter.doc_splitter import DocSplitter
from redge.modules.text_embedding.text_embedding import TextEmbedding

class KnowledgeBuilder:
    def __init__(self, database_path="knowledge.db"):
        # 获取 sqlite-vec 在 venv 中的路径
        vec_extension_path = os.path.join(os.path.dirname(sqlite_vec.__file__), "vec0.dylib")
        self.database_path = database_path
        self.conn = sqlite3.connect(self.database_path)
        self.conn.enable_load_extension(True)
        self.conn.load_extension(vec_extension_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT vec_version();")
        print("SQLite-Vec 版本:", self.cursor.fetchone()[0])
        self._initialize_database()
        self.embedding_model = TextEmbedding()

    def _initialize_database(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS fragments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_name TEXT NOT NULL
        )
        """)
        self.cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS vectors USING vec0(
            vector(1536)  -- 假设嵌入向量的维度为 1536
        )
        """)
        self.conn.commit()

    def build_knowledge(self, directory: str):
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
                vector = self.embedding_model.encode([fragment])[0].tolist()
                self._insert_vector(vector, fragment_id)

        print("知识构建完成！")

    def _insert_fragment(self, content: str, file_path: str, file_name: str) -> int:
        self.cursor.execute(
            "INSERT INTO fragments (content, file_path, file_name) VALUES (?, ?, ?)",
            (content, file_path, file_name),
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def _insert_vector(self, vector, fragment_id: int):
        vector_str = ' '.join(map(str, vector))
        self.cursor.execute(
            "INSERT INTO vectors (vector, rowid) VALUES (zeroblob(?), ?)",
            (len(vector), fragment_id),
        )
        self.cursor.execute(
            "UPDATE vectors SET vector = (?) WHERE rowid = ?",
            (vector_str, fragment_id)
        )
        self.conn.commit()

if __name__ == "__main__":
    knowledge_builder = KnowledgeBuilder()
    knowledge_builder.build_knowledge("/Users/lianruilong/Documents/work/mywork/redge/test_docs")