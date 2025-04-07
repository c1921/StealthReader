from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon

class TrayUI:
    def __init__(self, parent):
        self.parent = parent
        
        # 创建系统托盘
        self.tray = QSystemTrayIcon(parent)
        self.tray.setIcon(QIcon("./resources/icon.svg"))  # 使用自定义SVG图标
        
        # 创建托盘菜单
        self.trayMenu = QMenu()
        self.showAction = self.trayMenu.addAction("显示")
        self.openFileAction = self.trayMenu.addAction("打开文件")
        self.settingsAction = self.trayMenu.addAction("设置")
        self.trayMenu.addSeparator()
        self.quitAction = self.trayMenu.addAction("退出")
        
        # 设置托盘上下文菜单
        self.tray.setContextMenu(self.trayMenu)
        self.tray.show() 