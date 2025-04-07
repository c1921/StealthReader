from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, 
                               QPushButton, QSystemTrayIcon, QMenu)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QIcon

from src.ui.custom_widgets import CustomTextEdit

class MainUI:
    def setup_ui(self, window):
        # 设置无边框窗口
        window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # 设置窗口透明背景
        window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 创建主窗口部件
        self.central_widget = QWidget()
        window.setCentralWidget(self.central_widget)
        
        # 创建布局
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建自定义文本编辑器（只读模式）
        self.text_edit = CustomTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.layout.addWidget(self.text_edit)
        
        # 设置初始窗口大小
        window.resize(800, 600)
        
        # 添加最小化到托盘按钮
        self.minimizeButton = QPushButton("🗕", window)
        self.minimizeButton.setGeometry(window.width() - 40, 10, 30, 30)
        
        # 创建系统托盘
        self.tray = QSystemTrayIcon(window)
        self.tray.setIcon(QIcon("./resources/icon.svg"))  # 使用自定义SVG图标
        
        # 创建托盘菜单
        self.trayMenu = QMenu()
        self.showAction = self.trayMenu.addAction("显示")
        self.openFileAction = self.trayMenu.addAction("打开文件")
        self.settingsAction = self.trayMenu.addAction("设置")
        self.trayMenu.addSeparator()
        self.quitAction = self.trayMenu.addAction("退出")
        
        self.tray.setContextMenu(self.trayMenu)
        
        # 设置鼠标跟踪
        window.setMouseTracking(True)
        self.central_widget.setMouseTracking(True)
        self.text_edit.setMouseTracking(True) 