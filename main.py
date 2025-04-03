from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt
import sys

class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口无边框
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 设置窗口大小
        self.setGeometry(300, 300, 400, 200)
        
        # 创建标签显示文本
        self.label = QLabel("这是一个透明窗口", self)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                background-color: rgba(0, 0, 0, 150);
                padding: 10px;
                border-radius: 5px;
            }
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(50, 50, 300, 100)
        
        # 用于窗口拖动
        self.oldPos = None
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        if self.oldPos:
            delta = event.globalPosition().toPoint() - self.oldPos
            self.move(self.pos() + delta)
            self.oldPos = event.globalPosition().toPoint()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec())
