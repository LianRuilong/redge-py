import ollama
import time
from redge.core.rag.knowledge_query import KnowledgeQuery

class KnowledgeQA:
    """
    知识问答模块：
    1. 接收用户问题
    2. 通过 KnowledgeQuery 获取文档片段
    3. 组织 prompt，调用 Ollama 本地大模型
    4. 返回答案和去重后的参考文档列表
    """

    def __init__(self, model="mistral"):
        """
        初始化 Ollama 模型
        :param model: Ollama 本地部署的 LLM 名称
        """
        self.model = model
        self.knowledge_query = KnowledgeQuery()

    def generate_prompt(self, question, documents):
        """
        生成 LLM 输入的 Prompt
        :param question: 用户问题
        :param documents: 相关文档片段列表
        :return: 生成的 prompt
        """
        doc_texts = "\n\n".join([f"片段 {i+1}: {doc['content']}" for i, doc in enumerate(documents)])
        prompt = f"""你是一个专业的 AI 助手，以下是相关文档片段，请基于这些信息回答用户的问题。

### 用户问题：
{question}

### 相关文档：
{doc_texts}

请综合这些信息，给出准确、简洁的回答。
"""
        return prompt

    def ask(self, question):
        """
        执行问答流程：
        1. 查询知识库
        2. 调用 LLM 生成回答
        3. 返回结构化数据，包括回答内容和去重后的引用文档
        """
        # 1️⃣ **调用 knowledge_query 获取相关文档**
        documents = self.knowledge_query.query(question, top_k=3)
        if not documents:
            return {
                "answer": "未找到相关内容",
                "references": []
            }

        # 2️⃣ **生成 Prompt**
        prompt = self.generate_prompt(question, documents)

        # 3️⃣ **调用 Ollama LLM**
        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        answer = response['message']['content']

        # 4️⃣ **去重并整理引用文档**
        seen_files = set()  # 存储已输出的 `file_path`
        references = []
        for doc in documents:
            if doc['file_path'] not in seen_files:
                references.append({"file_name": doc["file_name"], "file_path": doc["file_path"]})
                seen_files.add(doc['file_path'])  # 标记为已输出

        # 5️⃣ **返回 JSON 结构化数据**
        return {
            "answer": answer,
            "references": references
        }

    def ask_stream(self, question):
        """
        **流式回答**
        1. 逐步获取 LLM 生成的 token
        2. 使用 yield 逐步返回数据（适用于 FastAPI Streaming）
        """
        # 1️⃣ **调用 knowledge_query 获取相关文档**
        documents = self.knowledge_query.query(question, top_k=3)
        if not documents:
            yield "未找到相关内容\n"
            return

        # 2️⃣ **生成 Prompt**
        prompt = self.generate_prompt(question, documents)

        # 3️⃣ **流式调用 Ollama LLM**
        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}], stream=True)
        
        for chunk in response:
            yield chunk["message"]["content"]

        # 4️⃣ **输出参考文档**
        yield "\n\n📂 **参考文档:**\n"
        seen_files = set()
        for doc in documents:
            if doc["file_path"] not in seen_files:
                yield f"📄 {doc['file_name']} | 📍 {doc['file_path']}\n"
                seen_files.add(doc["file_path"])

if __name__ == "__main__":
    qa = KnowledgeQA(model="deepseek-r1:1.5b")  # 选择本地 LLM
    query_text = input("\n❓ 请输入您的问题: ")
    response = qa.ask(query_text)

    # 打印结构化返回数据
    print("\n🤖 **回答:** \n")
    print(response["answer"])
    print("\n📂 **参考文档:**")
    for ref in response["references"]:
        print(f"📄 {ref['file_name']} | 📍 {ref['file_path']}")