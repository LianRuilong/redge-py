import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QTextCursor
from redge.core.rag.knowledge_qa import KnowledgeQA

class AIWorker(QThread):
    """后台线程处理 LLM 生成，支持流式输出"""
    new_text = pyqtSignal(str)  # 发送新生成的文本
    finished = pyqtSignal()     # 任务完成信号

    def __init__(self, qa_instance, question):
        super().__init__()
        self.qa = qa_instance
        self.question = question

    def run(self):
        """运行 LLM 问答，并流式返回结果"""
        for chunk in self.qa.ask_stream(self.question):
            self.new_text.emit(chunk)  # 逐步更新 UI
            time.sleep(0.05)  # 模拟打字机效果
        self.finished.emit()  # 任务完成

class ChatApp(QWidget):
    """GUI 主界面"""
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.qa = KnowledgeQA(model="deepseek-r1:1.5b")  # 直接调用 KnowledgeQA

    def init_ui(self):
        """初始化 UI 组件"""
        self.setWindowTitle("AI 知识问答系统")
        self.setGeometry(300, 200, 800, 600)

        self.layout = QVBoxLayout()

        # **显示 AI 回答**
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        self.layout.addWidget(self.output_area)

        # **底部输入框 + 发送按钮**
        self.input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("请输入您的问题，按回车键发送...")
        self.input_field.returnPressed.connect(self.send_question)  # 绑定回车发送
        self.input_layout.addWidget(self.input_field)

        self.layout.addLayout(self.input_layout)  # 把输入框+按钮加入主布局
        self.setLayout(self.layout)

    def send_question(self):
        """处理用户输入，并调用 LLM"""
        question = self.input_field.text().strip()
        if not question:
            return

        self.output_area.append(f"❓ **问题**: {question}\n")
        self.input_field.clear()

        # **创建后台线程处理 AI 生成**
        self.worker = AIWorker(self.qa, question)
        self.worker.new_text.connect(self.update_output)
        self.worker.finished.connect(lambda: self.output_area.append("\n✅ **回答完成！** \n\n"))
        self.worker.start()

    def update_output(self, text):
        """更新 AI 生成的回答，直接输出所有文本"""
        cursor = self.output_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)  # 移动光标到末尾
        cursor.insertText(text)
        self.output_area.ensureCursorVisible()  # 保证滚动条跟随输出

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_app = ChatApp()
    chat_app.show()
    sys.exit(app.exec())
