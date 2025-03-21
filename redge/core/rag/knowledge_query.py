import os
import sqlite3
import hnswlib
import numpy as np
from redge.modules.text_embedding.text_embedding import TextEmbedding

class KnowledgeQuery:
    """
    知识问答模块：
    1. 输入用户的问题
    2. 通过向量检索找到最相关的 3 个文档片段
    3. 返回片段内容
    """

    def __init__(self, database_path="knowledge.db", hnsw_path="knowledge.hnsw", dim=512):
        self.file_name = os.path.basename(__file__)
        """
        初始化 SQLite 和 HNSWLib
        """
        self.database_path = database_path
        self.hnsw_path = hnsw_path
        self.dim = dim

        # 加载 HNSWLib 索引
        self.hnsw_index = hnswlib.Index(space='cosine', dim=self.dim)
        self.hnsw_index.load_index(self.hnsw_path)
        print("HNSWLib 索引加载成功")

        # 初始化 Text Embedding 模型
        self.embedding_model = TextEmbedding()

    def query(self, question: str, top_k=3):
        """
        查询与输入问题最相似的片段
        """
        # 1️⃣ **动态创建 SQLite 连接**
        conn = sqlite3.connect(self.database_path, check_same_thread=False)
        cursor = conn.cursor()

        # 2️⃣ **获取查询向量**
        question_vector = self.embedding_model.encode([question])[0]
        question_vector = np.array(question_vector, dtype=np.float32).reshape(1, -1)

        # 3️⃣ **执行向量检索**
        labels, distances = self.hnsw_index.knn_query(question_vector, k=top_k)

        results = []
        for fragment_id, distance in zip(labels[0], distances[0]):
            cursor.execute(
                "SELECT content, file_path, file_name FROM fragments WHERE id=?",
                (int(fragment_id),)
            )
            result = cursor.fetchone()
            if result:
                results.append({
                    "content": result[0], 
                    "file_path": result[1], 
                    "file_name": result[2], 
                    "score": round(1 - distance, 4)
                })

        conn.close()  # 关闭数据库连接
        return results

if __name__ == "__main__":
    query = KnowledgeQuery()

    # 测试查询
    query_text = "中华人民共和国的基本法律有哪些？"
    results = query.query(query_text)

    print("\n🔍 **查询结果** 🔍\n")
    for idx, res in enumerate(results):
        print(f"📄 **文档 {idx+1}:** {res['file_name']}")
        print(f"📍 路径: {res['file_path']}")
        print(f"⭐ 相似度: {res['score']}")
        print(f"🔹 片段: {res['content'][:100]}...\n")  # 仅展示前 100 个字符