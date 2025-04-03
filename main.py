from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QSystemTrayIcon, QMenu, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import sys

class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.svg"))  # 设置窗口图标
        # 设置窗口无边框
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 设置窗口大小
        self.setGeometry(1400, 600, 400, 200)
        
        # 创建标签显示文本
        self.label = QLabel("1234567890", self)
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
        
        # 创建最小化到托盘按钮
        self.hideButton = QPushButton("🗕", self)
        self.hideButton.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 150);
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 200);
            }
        """)
        self.hideButton.setGeometry(360, 10, 30, 30)
        self.hideButton.clicked.connect(self.hideToTray)
        
        # 创建系统托盘
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon("icon.svg"))  # 使用自定义SVG图标
        
        # 创建托盘菜单
        self.trayMenu = QMenu()
        self.showAction = self.trayMenu.addAction("显示")
        self.showAction.triggered.connect(self.showNormal)
        self.quitAction = self.trayMenu.addAction("退出")
        self.quitAction.triggered.connect(QApplication.quit)
        
        self.tray.setContextMenu(self.trayMenu)
        self.tray.show()
        
        # 托盘图标双击显示窗口
        self.tray.activated.connect(self.onTrayIconActivated)
        
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
    
    def hideToTray(self):
        self.hide()
        
    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.showNormal()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec())
