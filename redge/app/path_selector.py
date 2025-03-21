import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog

class PathSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("路径选择器")
        self.setGeometry(400, 200, 500, 120)
        
        layout = QVBoxLayout()

        # 显示选定路径的文本框
        self.path_display = QLineEdit(self)
        self.path_display.setPlaceholderText("请选择一个路径...")
        layout.addWidget(self.path_display)

        # 选择路径的按钮
        self.select_button = QPushButton("选择路径", self)
        self.select_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.select_button)

        self.setLayout(layout)

    def open_file_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.path_display.setText(folder_path)

    def get_selected_path(self):
        """获取用户选择的路径"""
        return self.path_display.text()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PathSelector()
    window.show()
    sys.exit(app.exec())