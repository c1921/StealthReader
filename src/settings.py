from PySide6.QtWidgets import QFileDialog, QColorDialog
from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor

from src.ui.settings_ui import SettingsDialogUI

class SettingsDialog(SettingsDialogUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("StealthReader", "Settings")
        
        # 设置初始值
        self.filePathLabel.setText(parent.file_path if parent.file_path else "未选择文件")
        self.bgColorBtn.setStyleSheet(f"background-color: {parent.bg_color.name()}")
        self.bgAlphaSlider.setValue(parent.bg_alpha)
        self.textColorBtn.setStyleSheet(f"background-color: {parent.text_color.name()}")
        self.textAlphaSlider.setValue(parent.text_alpha)
        
        # 连接信号和槽
        self.fileChooseBtn.clicked.connect(self.choose_file)
        self.bgColorBtn.clicked.connect(self.choose_bg_color)
        self.textColorBtn.clicked.connect(self.choose_text_color)
        self.bgAlphaSlider.valueChanged.connect(self.update_parent_styles)
        self.textAlphaSlider.valueChanged.connect(self.update_parent_styles)
        self.saveBtn.clicked.connect(self.save_settings)
        self.cancelBtn.clicked.connect(self.reject)
        
        # 存储原始设置以便取消时还原
        self.original_settings = {
            'bg_color': QColor(parent.bg_color),
            'bg_alpha': parent.bg_alpha,
            'text_color': QColor(parent.text_color),
            'text_alpha': parent.text_alpha,
            'file_path': parent.file_path
        }
        
        # 临时文件路径
        self.temp_file_path = parent.file_path
    
    def choose_file(self):
        """选择要显示的文本文件"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择文本文件", "", "文本文件 (*.txt);;所有文件 (*)", options=options
        )
        
        if file_path:
            self.temp_file_path = file_path
            self.filePathLabel.setText(file_path)
            
            # 加载文件并更新显示
            self.parent.load_file(file_path)
    
    def choose_bg_color(self):
        color = QColorDialog.getColor(self.parent.bg_color, self, "选择背景颜色")
        if color.isValid():
            self.parent.bg_color = color
            self.bgColorBtn.setStyleSheet(f"background-color: {color.name()}")
            self.update_parent_styles()
    
    def choose_text_color(self):
        color = QColorDialog.getColor(self.parent.text_color, self, "选择文本颜色")
        if color.isValid():
            self.parent.text_color = color
            self.textColorBtn.setStyleSheet(f"background-color: {color.name()}")
            self.update_parent_styles()
    
    def update_parent_styles(self):
        """实时更新主窗口样式"""
        # 临时更新父窗口的属性
        self.parent.bg_alpha = self.bgAlphaSlider.value()
        self.parent.text_alpha = self.textAlphaSlider.value()
        
        # 更新主窗口样式
        self.parent.update_styles()
    
    def save_settings(self):
        """保存设置到配置文件"""
        # 将临时文件路径保存到父窗口
        self.parent.file_path = self.temp_file_path
        
        # 保存到配置文件
        self.settings.setValue("bg_color", self.parent.bg_color.name())
        self.settings.setValue("bg_alpha", self.parent.bg_alpha)
        self.settings.setValue("text_color", self.parent.text_color.name())
        self.settings.setValue("text_alpha", self.parent.text_alpha)
        self.settings.setValue("file_path", self.parent.file_path)
        
        self.accept()
    
    def reject(self):
        """取消设置更改，恢复原始设置"""
        # 恢复原始设置
        self.parent.bg_color = self.original_settings['bg_color']
        self.parent.bg_alpha = self.original_settings['bg_alpha']
        self.parent.text_color = self.original_settings['text_color']
        self.parent.text_alpha = self.original_settings['text_alpha']
        
        # 如果文件路径已更改，则恢复原始文件
        if self.temp_file_path != self.original_settings['file_path']:
            self.parent.file_path = self.original_settings['file_path']
            if self.parent.file_path:
                self.parent.load_file(self.parent.file_path)
            else:
                self.parent.text_edit.setText("这是一个示例文本，窗口是半透明的，文本是只读的。")
        
        # 更新主窗口样式
        self.parent.update_styles()
        
        super().reject() 