from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from redge.core.rag.knowledge_qa import KnowledgeQA

app = FastAPI()
qa = KnowledgeQA(model="deepseek-r1:1.5b")  # 启动 LLM 处理

class QueryRequest(BaseModel):
    question: str

@app.post("/query_stream")
def query_knowledge_base_stream(request: QueryRequest):
    """
    处理知识库问答请求（流式响应）
    """
    return StreamingResponse(qa.ask_stream(request.question), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)