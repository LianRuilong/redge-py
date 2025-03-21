import requests

def chat_with_server():
    """
    交互式客户端：
    - 用户输入问题
    - 逐步接收并打印 LLM 生成的答案
    - 输入 "exit" 退出
    """
    url = "http://127.0.0.1:8000/query_stream"

    print("\n🤖 **欢迎使用 AI 问答系统**（输入 'exit' 退出）\n")

    while True:
        # 1️⃣ **用户输入问题**
        question = input("❓ 请输入您的问题: ")
        if question.lower() == "exit":
            print("\n👋 退出问答系统，再见！\n")
            break

        # 2️⃣ **发送请求**
        response = requests.post(url, json={"question": question}, stream=True)

        print("\n🤖 **回答:** \n")
        
        # 3️⃣ **逐步打印 LLM 生成的内容**
        for chunk in response.iter_content(chunk_size=1024):
            print(chunk.decode(), end="", flush=True)

        print("\n" + "="*50 + "\n")  # 分隔线，方便阅读

if __name__ == "__main__":
    chat_with_server()