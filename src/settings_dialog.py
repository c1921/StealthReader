from PySide6.QtWidgets import (QDialog, QLabel, QPushButton, QSlider, 
                             QColorDialog, QGridLayout, QHBoxLayout,
                             QFileDialog)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QColor

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("设置")
        self.settings = QSettings("StealthReader", "Settings")
        
        # 设置对话框大小
        self.resize(500, 250)
        
        # 创建布局
        layout = QGridLayout(self)
        
        # 文件选择设置 - 改为第一行，放在位置 (0, 0) 和 (0, 1)
        layout.addWidget(QLabel("文本文件:"), 0, 0)
        fileLayout = QHBoxLayout()
        self.filePathLabel = QLabel(parent.file_path if parent.file_path else "未选择文件")
        self.filePathLabel.setStyleSheet("border: 1px solid gray; padding: 2px;")
        self.filePathLabel.setWordWrap(True)
        self.filePathLabel.setMinimumWidth(300)
        fileLayout.addWidget(self.filePathLabel, 1)
        
        self.fileChooseBtn = QPushButton("浏览...")
        self.fileChooseBtn.clicked.connect(self.choose_file)
        fileLayout.addWidget(self.fileChooseBtn)
        layout.addLayout(fileLayout, 0, 1)
        
        # 背景颜色设置 - 改为第二行，放在位置 (1, 0) 和 (1, 1)
        layout.addWidget(QLabel("背景颜色:"), 1, 0)
        self.bgColorBtn = QPushButton()
        self.bgColorBtn.setStyleSheet(f"background-color: {parent.bg_color.name()}")
        self.bgColorBtn.clicked.connect(self.choose_bg_color)
        layout.addWidget(self.bgColorBtn, 1, 1)
        
        # 背景透明度设置 - 改为第三行
        layout.addWidget(QLabel("背景透明度:"), 2, 0)
        self.bgAlphaSlider = QSlider(Qt.Orientation.Horizontal)
        self.bgAlphaSlider.setRange(0, 255)
        self.bgAlphaSlider.setValue(parent.bg_alpha)
        self.bgAlphaSlider.valueChanged.connect(self.update_parent_styles)
        layout.addWidget(self.bgAlphaSlider, 2, 1)
        
        # 文本颜色设置 - 改为第四行
        layout.addWidget(QLabel("文本颜色:"), 3, 0)
        self.textColorBtn = QPushButton()
        self.textColorBtn.setStyleSheet(f"background-color: {parent.text_color.name()}")
        self.textColorBtn.clicked.connect(self.choose_text_color)
        layout.addWidget(self.textColorBtn, 3, 1)
        
        # 文本透明度设置 - 改为第五行
        layout.addWidget(QLabel("文本透明度:"), 4, 0)
        self.textAlphaSlider = QSlider(Qt.Orientation.Horizontal)
        self.textAlphaSlider.setRange(0, 255)
        self.textAlphaSlider.setValue(parent.text_alpha)
        self.textAlphaSlider.valueChanged.connect(self.update_parent_styles)
        layout.addWidget(self.textAlphaSlider, 4, 1)
        
        # 保存和取消按钮 - 改为第六行
        buttonLayout = QHBoxLayout()
        saveBtn = QPushButton("保存")
        saveBtn.clicked.connect(self.save_settings)
        cancelBtn = QPushButton("取消")
        cancelBtn.clicked.connect(self.reject)
        buttonLayout.addWidget(saveBtn)
        buttonLayout.addWidget(cancelBtn)
        layout.addLayout(buttonLayout, 5, 0, 1, 2)
        
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