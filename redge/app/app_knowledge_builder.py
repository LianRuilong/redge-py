import sys
import os
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel

from redge.core.rag.knowledge_builder import KnowledgeBuilder

class KnowledgeApp(QWidget):
    def __init__(self):
        super().__init__()

        # 统一定义数据库和索引存储路径
        self.database_path = "data/knowledge.db"
        self.hnsw_path = "data/knowledge.hnsw"

        self.knowledge_builder = KnowledgeBuilder()  # 直接初始化
        self.selected_directory = None
        self.settings_file = "config/knowledge_path.txt"

        self.init_ui()
        self.load_saved_directory()

    def init_ui(self):
        """初始化 UI 界面"""
        self.setWindowTitle("知识构建工具")
        self.setGeometry(400, 200, 500, 200)

        layout = QVBoxLayout()

        # 路径显示标签
        self.path_label = QLabel("当前路径: 未设置", self)
        layout.addWidget(self.path_label)

        # "设置" 按钮
        self.btn_set_path = QPushButton("设置路径", self)
        self.btn_set_path.clicked.connect(self.set_knowledge_path)
        layout.addWidget(self.btn_set_path)

        # "知识构建" 按钮
        self.btn_build_knowledge = QPushButton("知识构建", self)
        self.btn_build_knowledge.clicked.connect(self.rebuild_knowledge)
        layout.addWidget(self.btn_build_knowledge)

        self.setLayout(layout)

    def set_knowledge_path(self):
        """弹出文件夹选择对话框，并保存选择的路径"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择知识构建文件夹")
        if folder_path:
            self.selected_directory = folder_path
            self.path_label.setText(f"当前路径: {folder_path}")

            # 保存路径到文件
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)  # 确保目录存在
            with open(self.settings_file, "w") as f:
                f.write(folder_path)

    def load_saved_directory(self):
        """加载上次保存的路径"""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                saved_path = f.read().strip()
                if os.path.isdir(saved_path):
                    self.selected_directory = saved_path
                    self.path_label.setText(f"当前路径: {saved_path}")

    def rebuild_knowledge(self):
        """重新构建知识库"""
        if not self.selected_directory:
            QMessageBox.warning(self, "错误", "请先设置文件夹路径！")
            return

        # 调用 KnowledgeBuilder 的 rebuild_knowledge 方法
        self.knowledge_builder.rebuild_knowledge(self.selected_directory)

        QMessageBox.information(self, "完成", "知识构建完成！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KnowledgeApp()
    window.show()
    sys.exit(app.exec())