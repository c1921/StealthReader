from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from src.ui.custom_widgets import CustomTextEdit

class MainWindowUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置无边框窗口
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # 设置窗口透明背景
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 创建主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建布局
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建自定义文本编辑器（只读模式）
        self.text_edit = CustomTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.layout.addWidget(self.text_edit)
        
        # 设置初始窗口大小
        self.resize(800, 600)
        
        # 添加最小化到托盘按钮
        self.minimizeButton = QPushButton("🗕", self)
        self.minimizeButton.setGeometry(self.width() - 40, 10, 30, 30)
        
        # 设置鼠标追踪
        self.setMouseTracking(True)
        self.central_widget.setMouseTracking(True)
        self.text_edit.setMouseTracking(True)
        
        # 预定义鼠标指针
        self._cursors = {
            "topleft": QCursor(Qt.CursorShape.SizeFDiagCursor),
            "bottomright": QCursor(Qt.CursorShape.SizeFDiagCursor),
            "topright": QCursor(Qt.CursorShape.SizeBDiagCursor),
            "bottomleft": QCursor(Qt.CursorShape.SizeBDiagCursor),
            "left": QCursor(Qt.CursorShape.SizeHorCursor),
            "right": QCursor(Qt.CursorShape.SizeHorCursor),
            "top": QCursor(Qt.CursorShape.SizeVerCursor),
            "bottom": QCursor(Qt.CursorShape.SizeVerCursor),
            "default": QCursor(Qt.CursorShape.ArrowCursor)
        } 