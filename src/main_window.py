from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QSystemTrayIcon, QMenu, 
                             QPushButton, QMessageBox, QFileDialog)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QCursor, QIcon, QColor
import keyboard

from src.settings_dialog import SettingsDialog
from src.custom_widgets import CustomTextEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 加载设置
        self.settings = QSettings("StealthReader", "Settings")
        self.load_settings()
        
        # 设置无边框窗口
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # 设置窗口透明背景
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 创建主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建布局
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建自定义文本编辑器（只读模式）
        self.text_edit = CustomTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        layout.addWidget(self.text_edit)
        
        # 设置初始窗口大小
        self.resize(800, 600)
        
        # 用于窗口拖动和调整大小的变量
        self._drag_pos = None
        self._resizing = False
        self._resize_direction = None
        self.setMouseTracking(True)
        self.central_widget.setMouseTracking(True)
        self.text_edit.setMouseTracking(True)
        
        # 设置调整大小的边距
        self.MARGINS = 8
        
        # 加载文本文件（如果有）
        if self.file_path:
            self.load_file(self.file_path)
        else:
            # 添加一些示例文本
            self.text_edit.setText("这是一个示例文本，窗口是半透明的，文本是只读的。")
        
        # 最小窗口尺寸
        self.MIN_WIDTH = 200
        self.MIN_HEIGHT = 150
        
        # 存储初始窗口位置和大小
        self._initial_rect = None
        self._initial_pos = None
        
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
        
        # 添加最小化到托盘按钮
        self.minimizeButton = QPushButton("🗕", self)
        self.minimizeButton.setGeometry(self.width() - 40, 10, 30, 30)
        self.minimizeButton.clicked.connect(self.hideToTray)
        
        # 创建系统托盘
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon("./resources/icon.svg"))  # 使用自定义SVG图标
        
        # 创建托盘菜单
        self.trayMenu = QMenu()
        self.showAction = self.trayMenu.addAction("显示")
        self.showAction.triggered.connect(self.showNormal)
        
        self.openFileAction = self.trayMenu.addAction("打开文件")
        self.openFileAction.triggered.connect(self.open_file_dialog)
        
        # 添加设置菜单项
        self.settingsAction = self.trayMenu.addAction("设置")
        self.settingsAction.triggered.connect(self.show_settings)
        
        self.trayMenu.addSeparator()
        self.quitAction = self.trayMenu.addAction("退出")
        self.quitAction.triggered.connect(QApplication.quit)
        
        self.tray.setContextMenu(self.trayMenu)
        self.tray.show()
        
        # 托盘图标双击显示窗口
        self.tray.activated.connect(self.onTrayIconActivated)
        
        # 设置全局快捷键
        self.setup_global_hotkey()
        
        # 应用样式
        self.update_styles()
    
    def load_settings(self):
        """加载设置"""
        self.bg_color = QColor(self.settings.value("bg_color", "#FFFFFF"))
        self.bg_alpha = int(self.settings.value("bg_alpha", 180))
        self.text_color = QColor(self.settings.value("text_color", "#000000"))
        self.text_alpha = int(self.settings.value("text_alpha", 255))
        self.file_path = self.settings.value("file_path", "")
    
    def load_file(self, file_path):
        """加载文本文件到编辑器"""
        try:
            # 使用 Python 内置方式读取文件
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                self.text_edit.setText(text)
                
                # 更新窗口标题以显示文件名
                file_name = file_path.split("/")[-1].split("\\")[-1]
                self.setWindowTitle(f"StealthReader - {file_name}")
                return True
        except UnicodeDecodeError:
            # 如果 UTF-8 解码失败，尝试其他编码
            try:
                with open(file_path, 'r', encoding='gbk') as file:
                    text = file.read()
                    self.text_edit.setText(text)
                    
                    # 更新窗口标题以显示文件名
                    file_name = file_path.split("/")[-1].split("\\")[-1]
                    self.setWindowTitle(f"StealthReader - {file_name}")
                    return True
            except Exception as e:
                QMessageBox.critical(self, "错误", f"读取文件时出错 (GBK): {str(e)}")
                return False
        except Exception as e:
            QMessageBox.critical(self, "错误", f"读取文件时出错: {str(e)}")
            return False
    
    def open_file_dialog(self):
        """打开文件选择对话框"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择文本文件", "", "文本文件 (*.txt);;所有文件 (*)", options=options
        )
        
        if file_path:
            if self.load_file(file_path):
                self.file_path = file_path
                self.settings.setValue("file_path", file_path)
    
    def update_styles(self):
        """更新样式"""
        # 设置主窗口样式
        self.central_widget.setStyleSheet(f"""
            QWidget {{
                background: rgba({self.bg_color.red()}, {self.bg_color.green()}, {self.bg_color.blue()}, {self.bg_alpha});
                border: none;
                border-radius: 5px;
            }}
            QTextEdit {{
                border: none;
                background: transparent;
                color: rgba({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()}, {self.text_alpha});
                selection-background-color: transparent;
                selection-color: inherit;
            }}
        """)
        
        # 更新按钮样式
        self.minimizeButton.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba({self.bg_color.red()}, {self.bg_color.green()}, {self.bg_color.blue()}, 50);
                color: rgba({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()}, {self.text_alpha});
                border: none;
                border-radius: 3px;
                padding: 5px;
                font-size: 16px;
                min-width: 30px;
                min-height: 30px;
            }}
            QPushButton:hover {{
                background-color: rgba({self.bg_color.red()}, {self.bg_color.green()}, {self.bg_color.blue()}, 100);
            }}
        """)
    
    def show_settings(self):
        """显示设置对话框"""
        dialog = SettingsDialog(self)
        if dialog.exec():
            # 设置已经在对话框的save_settings方法中保存
            pass
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # 存储初始窗口位置和大小
            self._initial_rect = self.geometry()
            self._initial_pos = event.globalPosition().toPoint()
            
            # 检查是否在窗口边缘
            pos = event.position()
            x, y = pos.x(), pos.y()
            width, height = self.width(), self.height()
            
            # 确定调整方向
            self._resize_direction = self._get_resize_direction(x, y, width, height)
            
            if self._resize_direction:
                self._resizing = True
                QApplication.setOverrideCursor(self._cursors[self._resize_direction])
            else:
                self._drag_pos = event.globalPosition().toPoint()
                QApplication.setOverrideCursor(self._cursors["default"])

    def _get_resize_direction(self, x, y, width, height):
        """确定调整方向"""
        left = x <= self.MARGINS
        right = x >= width - self.MARGINS
        top = y <= self.MARGINS
        bottom = y >= height - self.MARGINS
        
        if left and top:
            return "topleft"
        elif left and bottom:
            return "bottomleft"
        elif right and top:
            return "topright"
        elif right and bottom:
            return "bottomright"
        elif left:
            return "left"
        elif right:
            return "right"
        elif top:
            return "top"
        elif bottom:
            return "bottom"
        return None

    def mouseMoveEvent(self, event):
        if self._resizing and event.buttons() == Qt.MouseButton.LeftButton:
            # 计算鼠标移动的距离
            current_pos = event.globalPosition().toPoint()
            dx = current_pos.x() - self._initial_pos.x()
            dy = current_pos.y() - self._initial_pos.y()
            
            # 获取初始几何信息
            x = self._initial_rect.x()
            y = self._initial_rect.y()
            width = self._initial_rect.width()
            height = self._initial_rect.height()
            
            # 根据调整方向计算新的几何信息
            new_x, new_y, new_width, new_height = x, y, width, height
            
            if "left" in self._resize_direction:
                new_x = x + dx
                new_width = max(self.MIN_WIDTH, width - dx)
                if new_width == self.MIN_WIDTH:
                    new_x = x + width - self.MIN_WIDTH
            
            if "right" in self._resize_direction:
                new_width = max(self.MIN_WIDTH, width + dx)
            
            if "top" in self._resize_direction:
                new_y = y + dy
                new_height = max(self.MIN_HEIGHT, height - dy)
                if new_height == self.MIN_HEIGHT:
                    new_y = y + height - self.MIN_HEIGHT
            
            if "bottom" in self._resize_direction:
                new_height = max(self.MIN_HEIGHT, height + dy)
            
            # 应用新的几何信息
            self.setGeometry(new_x, new_y, new_width, new_height)
                    
        elif event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos is not None:
            # 移动窗口
            new_pos = event.globalPosition().toPoint()
            self.move(self.pos() + new_pos - self._drag_pos)
            self._drag_pos = new_pos
        else:
            # 更新鼠标形状
            pos = event.position()
            x, y = pos.x(), pos.y()
            width, height = self.width(), self.height()
            
            direction = self._get_resize_direction(x, y, width, height)
            self._update_cursor(direction)

    def _update_cursor(self, direction):
        """根据调整方向更新鼠标形状"""
        QApplication.restoreOverrideCursor()  # 恢复之前的覆盖指针
        
        if direction:
            QApplication.setOverrideCursor(self._cursors[direction])
        else:
            QApplication.setOverrideCursor(self._cursors["default"])

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = None
            self._resizing = False
            self._resize_direction = None
            self._initial_rect = None
            self._initial_pos = None
            QApplication.restoreOverrideCursor()  # 恢复默认鼠标指针

    def hideToTray(self):
        """隐藏窗口到系统托盘"""
        self.hide()
        
    def onTrayIconActivated(self, reason):
        """处理托盘图标激活事件"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.showNormal()
    
    def resizeEvent(self, event):
        """重写resizeEvent以保持按钮位置"""
        super().resizeEvent(event)
        self.minimizeButton.move(self.width() - 40, 10)

    def setup_global_hotkey(self):
        """设置全局快捷键"""
        # 检查管理员权限
        from src.utils import is_admin
        
        if not is_admin():
            QMessageBox.warning(
                self, 
                "权限不足", 
                "全局快捷键功能需要管理员权限才能正常工作。\n"
                "请右键点击程序，选择'以管理员身份运行'。\n"
                "程序将继续运行，但全局快捷键可能无效。"
            )
        
        # 注册全局快捷键
        try:
            # 注册 Ctrl+Alt+H 用于隐藏/显示窗口
            keyboard.add_hotkey('ctrl+alt+h', self.toggle_visibility)
            
            # 在菜单中添加快捷键提示
            self.showAction.setText("显示 (Ctrl+Alt+H)")
        except Exception as e:
            QMessageBox.critical(self, "快捷键注册失败", f"无法注册全局快捷键: {str(e)}")
    
    def toggle_visibility(self):
        """切换窗口的可见状态"""
        if self.isVisible():
            self.hide()
        else:
            self.showNormal()
            self.activateWindow()  # 确保窗口获得焦点
    
    def closeEvent(self, event):
        """关闭事件处理"""
        # 程序退出前清理快捷键注册
        try:
            keyboard.unhook_all()
        except:
            pass
        event.accept() 