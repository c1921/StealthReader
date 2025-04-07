from PySide6.QtWidgets import (QDialog, QLabel, QPushButton, QSlider, 
                              QGridLayout, QHBoxLayout)
from PySide6.QtCore import Qt

class SettingsDialogUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("设置")
        
        # 设置对话框大小
        self.resize(500, 250)
        
        # 创建布局
        self.layout = QGridLayout(self)
        
        # 文件选择设置
        self.layout.addWidget(QLabel("文本文件:"), 0, 0)
        self.fileLayout = QHBoxLayout()
        self.filePathLabel = QLabel("")
        self.filePathLabel.setStyleSheet("border: 1px solid gray; padding: 2px;")
        self.filePathLabel.setWordWrap(True)
        self.filePathLabel.setMinimumWidth(300)
        self.fileLayout.addWidget(self.filePathLabel, 1)
        
        self.fileChooseBtn = QPushButton("浏览...")
        self.fileLayout.addWidget(self.fileChooseBtn)
        self.layout.addLayout(self.fileLayout, 0, 1)
        
        # 背景颜色设置
        self.layout.addWidget(QLabel("背景颜色:"), 1, 0)
        self.bgColorBtn = QPushButton()
        self.layout.addWidget(self.bgColorBtn, 1, 1)
        
        # 背景透明度设置
        self.layout.addWidget(QLabel("背景透明度:"), 2, 0)
        self.bgAlphaSlider = QSlider(Qt.Orientation.Horizontal)
        self.bgAlphaSlider.setRange(0, 255)
        self.layout.addWidget(self.bgAlphaSlider, 2, 1)
        
        # 文本颜色设置
        self.layout.addWidget(QLabel("文本颜色:"), 3, 0)
        self.textColorBtn = QPushButton()
        self.layout.addWidget(self.textColorBtn, 3, 1)
        
        # 文本透明度设置
        self.layout.addWidget(QLabel("文本透明度:"), 4, 0)
        self.textAlphaSlider = QSlider(Qt.Orientation.Horizontal)
        self.textAlphaSlider.setRange(0, 255)
        self.layout.addWidget(self.textAlphaSlider, 4, 1)
        
        # 保存和取消按钮
        self.buttonLayout = QHBoxLayout()
        self.saveBtn = QPushButton("保存")
        self.cancelBtn = QPushButton("取消")
        self.buttonLayout.addWidget(self.saveBtn)
        self.buttonLayout.addWidget(self.cancelBtn)
        self.layout.addLayout(self.buttonLayout, 5, 0, 1, 2) 